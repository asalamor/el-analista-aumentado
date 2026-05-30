-- sql/schema.sql
-- Esquema completo de base de datos para el pipeline AI funcional.
-- Compatible con PostgreSQL 14+ con la extensión pgvector instalada.
-- Ejecutar: psql -U pipeline -d pipeline_ai -f sql/schema.sql

-- ─────────────────────────────────────────────────────────────
-- EXTENSIONES
-- ─────────────────────────────────────────────────────────────

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- Para búsqueda de texto


-- ─────────────────────────────────────────────────────────────
-- MÓDULO RAG: Indexación del repositorio de requisitos
-- ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS chunks_requisitos (
    id              TEXT PRIMARY KEY,
    -- Formato: REQ-023::identidad, REQ-023::AC-023-01, etc.

    texto           TEXT NOT NULL,
    -- Texto que se embedda y se indexa semánticamente

    tipo            TEXT NOT NULL,
    -- identidad_requisito | reglas_negocio | criterio_aceptacion |
    -- datos_interfaz | flujos_error

    embedding       vector(1536),
    -- Embedding generado por text-embedding-3-large de OpenAI

    metadatos       JSONB,
    -- {requisito_id, epica, estado, version, actor, chunk_tipo, ac_id}

    hash_contenido  TEXT,
    -- MD5 del texto para detectar cambios sin re-embedir

    fecha_indexado  TIMESTAMP DEFAULT NOW(),
    activo          BOOLEAN DEFAULT TRUE
    -- FALSE para requisitos deprecados (no se eliminan para mantener historial)
);

-- Índice HNSW para búsqueda aproximada de vecinos más cercanos
-- ef_construction=128, m=16: buenos valores para hasta 100.000 chunks
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON chunks_requisitos
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 128);

-- Índices para filtrado por metadatos (búsqueda híbrida)
CREATE INDEX IF NOT EXISTS idx_chunks_tipo
    ON chunks_requisitos (tipo);

CREATE INDEX IF NOT EXISTS idx_chunks_activo
    ON chunks_requisitos (activo);

CREATE INDEX IF NOT EXISTS idx_chunks_metadatos
    ON chunks_requisitos USING gin (metadatos);

COMMENT ON TABLE chunks_requisitos IS
    'Repositorio vectorial de chunks de requisitos para el sistema RAG. '
    'Permite recuperar contexto semántico antes de generar artefactos.';


-- ─────────────────────────────────────────────────────────────
-- MÓDULO TRAZABILIDAD: Grafo de artefactos del proyecto
-- ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS nodos_trazabilidad (
    id                  TEXT PRIMARY KEY,
    -- REQ-023, US-047, TC-111, FACT-47, PR-892, commit-abc123

    tipo                TEXT NOT NULL,
    -- requisito | historia | criterio_ac | tarea | subtarea |
    -- test_case | issue_jira | epic | commit | ejecucion_tc

    titulo              TEXT,
    estado              TEXT,
    -- Para issues Jira: To Do / In Progress / Done
    -- Para requisitos: borrador / validado / deprecado
    -- Para test cases: pendiente / pasado / fallido

    metadatos           JSONB,
    -- Campos específicos por tipo (sprint, story_points, capa, etc.)

    fecha_creacion      TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
    activo              BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_nodos_tipo
    ON nodos_trazabilidad (tipo, estado);

CREATE INDEX IF NOT EXISTS idx_nodos_activo
    ON nodos_trazabilidad (activo);

CREATE INDEX IF NOT EXISTS idx_nodos_metadatos
    ON nodos_trazabilidad USING gin (metadatos);

COMMENT ON TABLE nodos_trazabilidad IS
    'Nodos del grafo de trazabilidad. Representa cualquier artefacto '
    'del proyecto: requisitos, historias, test cases, issues Jira, commits.';


CREATE TABLE IF NOT EXISTS aristas_trazabilidad (
    id              SERIAL PRIMARY KEY,

    origen_id       TEXT NOT NULL REFERENCES nodos_trazabilidad(id),
    destino_id      TEXT NOT NULL REFERENCES nodos_trazabilidad(id),

    tipo_relacion   TEXT NOT NULL,
    -- genera | verifica | implementa | descompone | depende_de |
    -- pertenece_a | reemplaza | vincula | deriva_de

    confianza       FLOAT DEFAULT 1.0,
    -- 1.0 = relación explícita documentada
    -- 0.7-0.9 = inferida por RAG con alta similitud
    -- 0.5-0.7 = inferida con similitud media (requiere revisión)

    origen_relacion TEXT,
    -- pipeline_generacion | rag_inference | manual | webhook_jira | webhook_xray

    metadatos       JSONB,
    fecha_creacion  TIMESTAMP DEFAULT NOW(),
    activo          BOOLEAN DEFAULT TRUE,

    CONSTRAINT uq_arista UNIQUE (origen_id, destino_id, tipo_relacion)
);

CREATE INDEX IF NOT EXISTS idx_aristas_origen
    ON aristas_trazabilidad (origen_id, tipo_relacion);

CREATE INDEX IF NOT EXISTS idx_aristas_destino
    ON aristas_trazabilidad (destino_id, tipo_relacion);

CREATE INDEX IF NOT EXISTS idx_aristas_activo
    ON aristas_trazabilidad (activo);

COMMENT ON TABLE aristas_trazabilidad IS
    'Aristas tipadas del grafo de trazabilidad. '
    'Conecta cualquier artefacto con cualquier otro con semántica explícita.';


-- ─────────────────────────────────────────────────────────────
-- MÓDULO GOBIERNO: Métricas y alertas del pipeline
-- ─────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS metricas_pipeline (
    id              SERIAL PRIMARY KEY,
    semana          TEXT NOT NULL,
    -- Formato: 2025-W20

    requisito_id    TEXT,
    epica_id        TEXT,
    analista        TEXT,

    -- Métricas de calidad del output
    tasa_aprobacion_directa  FLOAT,
    ediciones_por_artefacto  FLOAT,
    score_calidad_requisito  FLOAT,
    tiempo_procesamiento_seg FLOAT,

    -- Métricas de proceso
    tiempo_ciclo_horas       FLOAT,
    campos_mas_editados      JSONB,

    fecha_registro  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_metricas_semana
    ON metricas_pipeline (semana);

CREATE INDEX IF NOT EXISTS idx_metricas_epica
    ON metricas_pipeline (epica_id);

COMMENT ON TABLE metricas_pipeline IS
    'Métricas semanales del pipeline para el dashboard de gobierno.';


CREATE TABLE IF NOT EXISTS alertas_gobierno (
    id              SERIAL PRIMARY KEY,
    nombre_regla    TEXT NOT NULL,
    descripcion     TEXT,
    severidad       TEXT,
    -- critica | alta | media
    metricas_snapshot JSONB,
    -- Estado de las métricas que activó la alerta
    notificado_a    TEXT[],
    fecha_alerta    TIMESTAMP DEFAULT NOW(),
    resuelto        BOOLEAN DEFAULT FALSE,
    fecha_resolucion TIMESTAMP
);

COMMENT ON TABLE alertas_gobierno IS
    'Registro de alertas automáticas del sistema de gobierno.';


CREATE TABLE IF NOT EXISTS versiones_prompts (
    id              SERIAL PRIMARY KEY,
    propuesta_id    TEXT UNIQUE NOT NULL,
    -- Formato: PROMPT-20250512-1032
    prompt_id       TEXT NOT NULL,
    -- p2_historia | p3_tareas | etc.
    version_desde   TEXT,
    -- Versión activa antes del cambio
    version_hasta   TEXT,
    -- Nueva versión propuesta
    motivo          TEXT,
    autor           TEXT,
    evaluacion      JSONB,
    -- Resultado de la evaluación sobre el dataset de referencia
    estado          TEXT DEFAULT 'propuesto',
    -- propuesto | evaluado | aprobado | rechazado | desplegado
    aprobado_por    TEXT,
    fecha_propuesta TIMESTAMP DEFAULT NOW(),
    fecha_despliegue TIMESTAMP
);

COMMENT ON TABLE versiones_prompts IS
    'Historial de cambios en los prompts del pipeline con trazabilidad completa.';


-- ─────────────────────────────────────────────────────────────
-- VISTAS ÚTILES
-- ─────────────────────────────────────────────────────────────

-- Vista: Trazabilidad completa por requisito (nivel 1)
CREATE OR REPLACE VIEW v_trazabilidad_nivel1 AS
SELECT
    n_req.id            AS requisito_id,
    n_req.titulo        AS requisito_titulo,
    n_req.estado        AS requisito_estado,
    n_req.metadatos->>'epica' AS epica,
    n_us.id             AS historia_id,
    n_us.titulo         AS historia_titulo,
    n_us.estado         AS historia_estado,
    n_us.metadatos->>'sprint' AS sprint,
    n_ij.id             AS issue_jira_key,
    n_ij.estado         AS issue_estado
FROM nodos_trazabilidad n_req
LEFT JOIN aristas_trazabilidad a_us
    ON a_us.origen_id = n_req.id AND a_us.tipo_relacion = 'genera'
LEFT JOIN nodos_trazabilidad n_us
    ON n_us.id = a_us.destino_id AND n_us.tipo = 'historia'
LEFT JOIN aristas_trazabilidad a_ij
    ON a_ij.origen_id = n_us.id AND a_ij.tipo_relacion = 'vincula'
LEFT JOIN nodos_trazabilidad n_ij
    ON n_ij.id = a_ij.destino_id AND n_ij.tipo = 'issue_jira'
WHERE n_req.tipo = 'requisito' AND n_req.activo = TRUE;

COMMENT ON VIEW v_trazabilidad_nivel1 IS
    'Vista rápida de trazabilidad Requisito → Historia → Issue Jira.';


-- Vista: Gaps de cobertura por épica
CREATE OR REPLACE VIEW v_gaps_cobertura AS
SELECT
    n_req.metadatos->>'epica' AS epica,
    COUNT(*) AS total_requisitos,
    COUNT(n_us.id) AS con_historia,
    COUNT(*) - COUNT(n_us.id) AS sin_historia,
    ROUND(COUNT(n_us.id)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 1)
        AS pct_cobertura_historias
FROM nodos_trazabilidad n_req
LEFT JOIN aristas_trazabilidad a
    ON a.origen_id = n_req.id AND a.tipo_relacion = 'genera'
LEFT JOIN nodos_trazabilidad n_us
    ON n_us.id = a.destino_id AND n_us.tipo = 'historia'
WHERE n_req.tipo = 'requisito' AND n_req.activo = TRUE
GROUP BY n_req.metadatos->>'epica'
ORDER BY pct_cobertura_historias;

COMMENT ON VIEW v_gaps_cobertura IS
    'Resumen de cobertura de historias por épica. Útil para el dashboard de gobierno.';
