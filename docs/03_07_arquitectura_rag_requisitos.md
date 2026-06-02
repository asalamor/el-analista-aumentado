# Punto 7 — Arquitectura RAG para el repositorio de requisitos

La arquitectura RAG es el salto cualitativo que separa un pipeline de generación puntual de un sistema que aprende y es coherente con todo el historial del proyecto. Sin RAG, la IA trabaja con el requisito que tiene delante y nada más. Con RAG, trabaja con el requisito actual más todo el conocimiento acumulado del proyecto.

---

## Por qué RAG cambia las reglas del juego

Sin RAG, cada llamada al pipeline es ciega al contexto histórico. La IA puede generar una historia que contradice otra aprobada hace tres sprints, duplicar funcionalidad ya implementada, o ignorar una decisión de arquitectura documentada en otro requisito. El analista detecta estos problemas en el refinamiento, si los detecta.

Con RAG, antes de generar cualquier artefacto, el sistema recupera automáticamente los requisitos, historias y decisiones más relevantes del repositorio y los inyecta como contexto. La IA genera sabiendo qué existe ya, qué se decidió antes y qué patrones usa el equipo.

El beneficio no es solo evitar errores. Es también **consistencia de estilo**: las historias generadas para el sprint 15 tienen el mismo tono, estructura y nivel de detalle que las del sprint 1, porque el sistema aprende del patrón establecido por el equipo.

---

## Conceptos clave antes de la arquitectura

Antes de diseñar el sistema, conviene tener claros tres conceptos que en la práctica se confunden frecuentemente.

**Embedding** es la representación numérica del significado de un texto. Dos frases semánticamente similares tienen embeddings cercanos en el espacio vectorial, aunque no compartan palabras. «El gestor filtra facturas por fecha» y «El operador busca documentos por período» tienen embeddings próximos porque significan algo parecido, aunque el vocabulario sea diferente.

**Vector store** es la base de datos que almacena esos embeddings y permite buscar por similitud semántica. No busca por palabras clave exactas como un buscador tradicional, sino por significado. Es lo que permite recuperar «requisitos relacionados con filtrado de facturas» sin necesidad de que contengan esa frase exacta.

**Retrieval** es el proceso de consultar el vector store con la pregunta o el texto de entrada y recuperar los fragmentos más relevantes. Esos fragmentos se añaden al prompt como contexto antes de llamar al LLM.

---

## Arquitectura completa del sistema RAG

### Fase 1 — Chunking semántico del repositorio

El chunking es la decisión más crítica de todo el sistema RAG. Un chunk demasiado grande recupera información irrelevante junto con la relevante. Un chunk demasiado pequeño pierde contexto y la IA genera respuestas parciales.

La estrategia para un repositorio de requisitos es **chunking por bloque funcional**, no por longitud de texto. Cada bloque de la plantilla se indexa como un chunk independiente con sus metadatos:

```python
from dataclasses import dataclass
from typing import Optional
import yaml
import hashlib

@dataclass
class Chunk:
    """Unidad de indexación del repositorio de requisitos."""
    id: str                    # Identificador único del chunk
    texto: str                 # Texto a embeddar
    tipo: str                  # Tipo de chunk para filtrado
    metadatos: dict            # Metadatos para filtrado y presentación


def chunkerizar_requisito(yaml_path: str) -> list[Chunk]:
    """
    Convierte un YAML de requisito en chunks semánticos independientes.
    Cada bloque funcional se indexa por separado para maximizar
    la precisión del retrieval.
    """
    with open(yaml_path) as f:
        req = yaml.safe_load(f)

    chunks = []
    req_id = req["id"]
    epica = req["epica"]
    estado = req["estado"]
    version = req["version"]

    metadatos_base = {
        "requisito_id": req_id,
        "epica": epica,
        "estado": estado,
        "version": version,
        "modulo": req.get("modulo", ""),
        "prioridad": req.get("prioridad", ""),
        "actor": req.get("actor", ""),
        "fuente": yaml_path
    }

    # ── CHUNK 1: Identidad + contexto completo
    # El chunk más consultado: lo recupera cualquier búsqueda
    # sobre la funcionalidad general del requisito
    texto_identidad = f"""
    Requisito {req_id}: {req['titulo']}
    Módulo: {req.get('modulo', '')} ({epica})
    Actor: {req.get('actor', '')}
    Prioridad: {req.get('prioridad', '')}
    Descripción: {req.get('descripcion', '')}
    Evento disparador: {req.get('evento_disparador', '')}
    Objetivo de negocio: {req.get('objetivo_negocio', '')}
    """.strip()

    chunks.append(Chunk(
        id=f"{req_id}::identidad",
        texto=texto_identidad,
        tipo="identidad_requisito",
        metadatos={**metadatos_base, "chunk_tipo": "identidad"}
    ))

    # ── CHUNK 2: Reglas de negocio
    # Se recupera cuando hay que verificar consistencia de reglas
    # entre requisitos del mismo módulo
    if req.get("reglas_negocio"):
        reglas_texto = "\n".join(
            f"- {r}" for r in req["reglas_negocio"]
        )
        texto_reglas = f"""
        Reglas de negocio del requisito {req_id} ({req['titulo']}):
        {reglas_texto}
        Módulo: {epica}
        Actor: {req.get('actor', '')}
        """.strip()

        chunks.append(Chunk(
            id=f"{req_id}::reglas_negocio",
            texto=texto_reglas,
            tipo="reglas_negocio",
            metadatos={**metadatos_base, "chunk_tipo": "reglas_negocio"}
        ))

    # ── CHUNK 3: Criterios de aceptación (uno por criterio)
    # Granularidad máxima: permite recuperar criterios similares
    # para detectar duplicidades y sugerir reutilización
    for ac in req.get("criterios_aceptacion", []):
        texto_ac = f"""
        Criterio de aceptación {ac['id']} del requisito {req_id}:
        Dado: {ac['dado']}
        Cuando: {ac['cuando']}
        Entonces: {ac['entonces']}
        Tipo: {ac.get('tipo', 'positivo')}
        Contexto: {req['titulo']} — {epica}
        Actor: {req.get('actor', '')}
        """.strip()

        chunks.append(Chunk(
            id=f"{req_id}::{ac['id']}",
            texto=texto_ac,
            tipo="criterio_aceptacion",
            metadatos={
                **metadatos_base,
                "chunk_tipo": "criterio_aceptacion",
                "ac_id": ac["id"],
                "ac_tipo": ac.get("tipo", "positivo")
            }
        ))

    # ── CHUNK 4: Datos de entrada y salida
    # Se recupera para verificar compatibilidad de interfaces
    # entre requisitos que comparten datos
    if req.get("datos_entrada") or req.get("datos_salida"):
        campos_entrada = [
            f"{d['nombre']} ({d['tipo']}, {'requerido' if d.get('requerido') else 'opcional'})"
            for d in req.get("datos_entrada", [])
        ]
        campos_salida = req.get("datos_salida", {}).get("campos", [])

        texto_datos = f"""
        Datos del requisito {req_id} ({req['titulo']}):
        Entradas: {', '.join(campos_entrada) if campos_entrada else 'No especificadas'}
        Salidas: {', '.join(campos_salida) if campos_salida else 'No especificadas'}
        Formato respuesta: {req.get('datos_salida', {}).get('formato', '')}
        Tiempo máximo respuesta: {req.get('datos_salida', {}).get('tiempo_respuesta_max_ms', '')}ms
        Módulo: {epica}
        """.strip()

        chunks.append(Chunk(
            id=f"{req_id}::datos",
            texto=texto_datos,
            tipo="datos_interfaz",
            metadatos={**metadatos_base, "chunk_tipo": "datos_interfaz"}
        ))

    # ── CHUNK 5: Excepciones y flujos de error
    # Se recupera para sugerir flujos de error ya documentados
    # en requisitos similares y detectar tratamientos inconsistentes
    if req.get("excepciones"):
        excepciones_texto = "\n".join(
            f"- Si {e['condicion']}: {e['comportamiento']}"
            for e in req["excepciones"]
        )
        texto_excepciones = f"""
        Flujos de error del requisito {req_id} ({req['titulo']}):
        {excepciones_texto}
        Módulo: {epica}
        Actor afectado: {req.get('actor', '')}
        """.strip()

        chunks.append(Chunk(
            id=f"{req_id}::excepciones",
            texto=texto_excepciones,
            tipo="flujos_error",
            metadatos={**metadatos_base, "chunk_tipo": "flujos_error"}
        ))

    return chunks
```

---

### Fase 2 — Indexación en el vector store

Con los chunks generados, el pipeline de indexación los embeda y los persiste. Se recomienda **pgvector sobre PostgreSQL** para la mayoría de organizaciones medianas porque reutiliza la infraestructura existente, soporta filtrado por metadatos con SQL estándar y no requiere una base de datos adicional.

```python
import openai
import psycopg2
from psycopg2.extras import execute_values
import json

class RepositorioRequisitosRAG:
    """
    Gestiona la indexación y consulta del repositorio de requisitos
    usando pgvector como vector store.
    """
    def __init__(self, db_config: dict, openai_client):
        self.db = psycopg2.connect(**db_config)
        self.openai = openai_client
        self._inicializar_schema()

    def _inicializar_schema(self):
        """Crea las tablas necesarias si no existen."""
        with self.db.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chunks_requisitos (
                    id              TEXT PRIMARY KEY,
                    texto           TEXT NOT NULL,
                    tipo            TEXT NOT NULL,
                    embedding       vector(1536),
                    metadatos       JSONB,
                    hash_contenido  TEXT,   -- Para detectar si el chunk cambió
                    fecha_indexado  TIMESTAMP DEFAULT NOW(),
                    activo          BOOLEAN DEFAULT TRUE
                );
                -- Índice HNSW para búsqueda aproximada de alta velocidad
                -- ef_construction=128 y m=16 son buenos valores para
                -- repositorios de hasta 100.000 chunks
                CREATE INDEX IF NOT EXISTS idx_chunks_embedding
                    ON chunks_requisitos
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 128);
                -- Índices para filtrado por metadatos (búsqueda híbrida)
                CREATE INDEX IF NOT EXISTS idx_chunks_tipo
                    ON chunks_requisitos (tipo);
                CREATE INDEX IF NOT EXISTS idx_chunks_metadatos
                    ON chunks_requisitos USING gin (metadatos);
            """)
            self.db.commit()

    def embeder_texto(self, texto: str) -> list[float]:
        """Genera el embedding de un texto usando el modelo de OpenAI."""
        respuesta = self.openai.embeddings.create(
            model="text-embedding-3-large",
            input=texto,
            dimensions=1536
        )
        return respuesta.data[0].embedding

    def indexar_chunk(self, chunk: Chunk) -> bool:
        """
        Indexa un chunk en el vector store.
        Si el chunk ya existe y el contenido no cambió, lo omite.
        Si cambió, lo actualiza.
        """
        hash_actual = hashlib.md5(chunk.texto.encode()).hexdigest()
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT hash_contenido FROM chunks_requisitos WHERE id = %s",
                (chunk.id,)
            )
            fila = cur.fetchone()
            if fila and fila[0] == hash_actual:
                return False  # Sin cambios, no re-indexar

            embedding = self.embeder_texto(chunk.texto)

            cur.execute("""
                INSERT INTO chunks_requisitos
                    (id, texto, tipo, embedding, metadatos, hash_contenido)
                VALUES (%s, %s, %s, %s::vector, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    texto           = EXCLUDED.texto,
                    tipo            = EXCLUDED.tipo,
                    embedding       = EXCLUDED.embedding,
                    metadatos       = EXCLUDED.metadatos,
                    hash_contenido  = EXCLUDED.hash_contenido,
                    fecha_indexado  = NOW(),
                    activo          = TRUE
            """, (
                chunk.id,
                chunk.texto,
                chunk.tipo,
                embedding,
                json.dumps(chunk.metadatos),
                hash_actual
            ))
            self.db.commit()
            return True  # Chunk indexado o actualizado

    def indexar_requisito_completo(self, yaml_path: str) -> dict:
        """Chunkeriza un requisito e indexa todos sus chunks."""
        chunks = chunkerizar_requisito(yaml_path)
        resultado = {"indexados": 0, "sin_cambios": 0, "errores": []}
        for chunk in chunks:
            try:
                actualizado = self.indexar_chunk(chunk)
                if actualizado:
                    resultado["indexados"] += 1
                else:
                    resultado["sin_cambios"] += 1
            except Exception as e:
                resultado["errores"].append(
                    {"chunk_id": chunk.id, "error": str(e)}
                )
        return resultado

    def desactivar_requisito(self, requisito_id: str):
        """
        Marca como inactivos todos los chunks de un requisito deprecado.
        No los elimina para mantener trazabilidad histórica.
        """
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE chunks_requisitos
                SET activo = FALSE
                WHERE metadatos->>'requisito_id' = %s
            """, (requisito_id,))
            self.db.commit()
```

---

### Fase 3 — Pipeline de consulta (retrieval)

Esta es la parte que se ejecuta en tiempo real cuando llega un nuevo requisito. El objetivo es construir el contexto más relevante posible en menos de 2 segundos.

La clave es usar **múltiples consultas paralelas especializadas** en lugar de una sola consulta genérica. Cada consulta busca un tipo de información diferente y el resultado se ensambla en un contexto estructurado.

```python
import asyncio
from typing import NamedTuple

class ResultadoRetrieval(NamedTuple):
    chunk_id: str
    texto: str
    similitud: float
    metadatos: dict
    tipo: str


class MotorConsultaRAG:
    """
    Ejecuta las consultas al vector store y ensambla el contexto
    para el pipeline de generación y validación.
    """

    UMBRAL_SIMILITUD_MINIMO = 0.72
    # Chunks con similitud < 0.72 suelen ser ruido, no contexto relevante.
    # Ajustar según el dominio: dominios muy especializados pueden
    # requerir umbrales más bajos (0.65).

    TOP_K_POR_CONSULTA = 5
    # Recuperar los 5 más similares por consulta especializada.
    # Con 5 consultas paralelas, el contexto máximo es 25 chunks
    # (antes de deduplicación).

    def __init__(self, repositorio: RepositorioRequisitosRAG):
        self.repo = repositorio

    def buscar_por_similitud(
        self,
        query_texto: str,
        filtros: dict = None,
        top_k: int = None
    ) -> list[ResultadoRetrieval]:
        """
        Búsqueda híbrida: similitud semántica + filtros por metadatos.
        Los filtros se aplican como condiciones SQL sobre la columna JSONB.
        """
        top_k = top_k or self.TOP_K_POR_CONSULTA
        embedding_query = self.repo.embeder_texto(query_texto)

        where_clauses = ["activo = TRUE"]
        params = [embedding_query, self.UMBRAL_SIMILITUD_MINIMO, top_k]

        if filtros:
            for clave, valor in filtros.items():
                where_clauses.append(
                    f"metadatos->>'{clave}' = %s"
                )
                params.append(str(valor))

        where_sql = " AND ".join(where_clauses)

        with self.repo.db.cursor() as cur:
            cur.execute(f"""
                SELECT
                    id,
                    texto,
                    1 - (embedding <=> %s::vector) AS similitud,
                    metadatos,
                    tipo
                FROM chunks_requisitos
                WHERE {where_sql}
                  AND 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [embedding_query] + params[1:] + [embedding_query])

            return [
                ResultadoRetrieval(
                    chunk_id=fila[0],
                    texto=fila[1],
                    similitud=float(fila[2]),
                    metadatos=fila[3],
                    tipo=fila[4]
                )
                for fila in cur.fetchall()
            ]

    async def recuperar_contexto_completo(
        self,
        requisito: dict
    ) -> dict:
        """
        Ejecuta 5 consultas especializadas en paralelo y ensambla
        el contexto para el pipeline de generación.
        """
        epica = requisito.get("epica", "")
        actor = requisito.get("actor", "")
        titulo = requisito.get("titulo", "")
        descripcion = requisito.get("descripcion", "")

        # ── 5 consultas paralelas especializadas ──────────────────────

        async def q1_funcionalidad_similar():
            """Requisitos con funcionalidad similar en todo el proyecto."""
            return self.buscar_por_similitud(
                query_texto=f"{titulo}. {descripcion}",
                filtros={"estado": "validado"},
                top_k=5
            )

        async def q2_mismo_modulo():
            """Todos los requisitos validados del mismo módulo."""
            return self.buscar_por_similitud(
                query_texto=f"requisitos del módulo {epica}",
                filtros={"epica": epica, "estado": "validado"},
                top_k=8
            )

        async def q3_mismo_actor():
            """Requisitos con el mismo actor para detectar permisos inconsistentes."""
            return self.buscar_por_similitud(
                query_texto=f"acciones del actor {actor}",
                filtros={"actor": actor, "chunk_tipo": "identidad"},
                top_k=5
            )

        async def q4_reglas_negocio_relacionadas():
            """Reglas de negocio del mismo módulo para detectar contradicciones."""
            return self.buscar_por_similitud(
                query_texto=" ".join(requisito.get("reglas_negocio", [])),
                filtros={
                    "epica": epica,
                    "chunk_tipo": "reglas_negocio",
                    "estado": "validado"
                },
                top_k=5
            )

        async def q5_criterios_similares():
            """Criterios de aceptación similares para detectar duplicados."""
            ac_texto = " ".join([
                f"{ac.get('dado', '')} {ac.get('cuando', '')} {ac.get('entonces', '')}"
                for ac in requisito.get("criterios_aceptacion", [])
            ])
            return self.buscar_por_similitud(
                query_texto=ac_texto,
                filtros={"chunk_tipo": "criterio_aceptacion"},
                top_k=5
            )

        # Ejecutar en paralelo
        resultados = await asyncio.gather(
            q1_funcionalidad_similar(),
            q2_mismo_modulo(),
            q3_mismo_actor(),
            q4_reglas_negocio_relacionadas(),
            q5_criterios_similares()
        )

        # ── Deduplicación y re-ranking ─────────────────────────────────
        chunks_vistos = set()
        chunks_finales = {
            "funcionalidad_similar": [],
            "mismo_modulo": [],
            "mismo_actor": [],
            "reglas_relacionadas": [],
            "criterios_similares": []
        }
        categorias = list(chunks_finales.keys())

        for i, resultado_consulta in enumerate(resultados):
            for chunk in resultado_consulta:
                if chunk.chunk_id not in chunks_vistos:
                    chunks_vistos.add(chunk.chunk_id)
                    chunks_finales[categorias[i]].append(chunk)

        return chunks_finales
```

---

### Fase 4 — Ensamblado del contexto para el prompt

Los chunks recuperados se convierten en contexto estructurado legible para el LLM. Este es el paso que más impacta en la calidad del output.

```python
def ensamblar_contexto_prompt(
    chunks: dict,
    glosario_relevante: dict,
    requisito_actual: dict
) -> str:
    """
    Construye el bloque de contexto que se inyecta en el prompt
    junto al requisito candidato.
    """
    secciones = []

    # ── Sección 1: Glosario relevante (siempre presente) ──────────────
    secciones.append("""
═══════════════════════════════════════════════
GLOSARIO APLICABLE
═══════════════════════════════════════════════
""" + formatear_glosario_compacto(glosario_relevante))

    # ── Sección 2: Funcionalidad similar (para evitar duplicados) ──────
    if chunks["funcionalidad_similar"]:
        items = []
        for c in chunks["funcionalidad_similar"][:3]:
            req_id = c.metadatos.get("requisito_id", "")
            similitud_pct = int(c.similitud * 100)
            items.append(
                f"▸ [{req_id}] (similitud {similitud_pct}%):\n"
                f"  {c.texto[:300]}..."
            )
        secciones.append(
            "═══════════════════════════════════════════════\n"
            "REQUISITOS CON FUNCIONALIDAD SIMILAR (validados)\n"
            "Verifica que el nuevo requisito no duplica estos:\n"
            "═══════════════════════════════════════════════\n"
            + "\n\n".join(items)
        )

    # ── Sección 3: Contexto del módulo ────────────────────────────────
    if chunks["mismo_modulo"]:
        ids_modulo = list({
            c.metadatos.get("requisito_id")
            for c in chunks["mismo_modulo"]
        })
        secciones.append(
            "═══════════════════════════════════════════════\n"
            f"REQUISITOS DEL MÓDULO {requisito_actual.get('epica', '')}\n"
            "El nuevo requisito debe ser coherente con estos:\n"
            "═══════════════════════════════════════════════\n"
            f"IDs existentes: {', '.join(ids_modulo)}\n\n"
            + "\n\n".join(
                f"▸ {c.metadatos.get('requisito_id')}: {c.texto[:200]}..."
                for c in chunks["mismo_modulo"][:4]
            )
        )

    # ── Sección 4: Reglas de negocio del módulo ───────────────────────
    if chunks["reglas_relacionadas"]:
        secciones.append(
            "═══════════════════════════════════════════════\n"
            "REGLAS DE NEGOCIO EXISTENTES EN EL MÓDULO\n"
            "El nuevo requisito NO puede contradecir estas reglas:\n"
            "═══════════════════════════════════════════════\n"
            + "\n".join(
                f"▸ [{c.metadatos.get('requisito_id')}]: {c.texto[:250]}"
                for c in chunks["reglas_relacionadas"][:4]
            )
        )

    # ── Sección 5: Criterios de aceptación similares ──────────────────
    if chunks["criterios_similares"]:
        criterios_alta_similitud = [
            c for c in chunks["criterios_similares"]
            if c.similitud > 0.88
        ]
        if criterios_alta_similitud:
            secciones.append(
                "═══════════════════════════════════════════════\n"
                "⚠ CRITERIOS DE ACEPTACIÓN MUY SIMILARES DETECTADOS\n"
                "Similitud > 88%. Revisa si son duplicados antes de continuar:\n"
                "═══════════════════════════════════════════════\n"
                + "\n".join(
                    f"▸ [{c.metadatos.get('ac_id')}] "
                    f"de {c.metadatos.get('requisito_id')} "
                    f"(similitud {int(c.similitud*100)}%):\n"
                    f"  {c.texto[:300]}"
                    for c in criterios_alta_similitud[:3]
                )
            )

    # ── Sección 6: Decisiones de arquitectura relevantes ─────────────
    # (si se indexan también las actas de decisión técnica)
    if chunks.get("decisiones_arquitectura"):
        secciones.append(
            "═══════════════════════════════════════════════\n"
            "DECISIONES TÉCNICAS APLICABLES\n"
            "═══════════════════════════════════════════════\n"
            + "\n".join(
                f"▸ {c.texto[:200]}"
                for c in chunks["decisiones_arquitectura"][:2]
            )
        )

    return "\n\n".join(secciones)
```

---

### Fase 5 — Casos de uso específicos del RAG

Además de enriquecer la generación, el RAG habilita cuatro capacidades que no son posibles sin él.

#### Caso de uso 1: Detección de impacto de cambios

Cuando un requisito validado se modifica, el sistema identifica automáticamente qué otros artefactos se ven afectados:

```python
async def analizar_impacto_cambio(
    requisito_id: str,
    campo_modificado: str,
    valor_anterior: str,
    valor_nuevo: str,
    motor: MotorConsultaRAG
) -> dict:
    """
    Cuando cambia un requisito validado, recupera todos los artefactos
    que referencian ese requisito o que son semánticamente dependientes.
    """
    # Buscar requisitos que referencian explícitamente al modificado
    dependencias_directas = motor.buscar_por_similitud(
        query_texto=f"dependencia de {requisito_id}",
        filtros={"estado": "validado"}
    )

    # Buscar criterios de aceptación que podrían verse afectados
    query_cambio = f"""
    El requisito {requisito_id} ha cambiado su {campo_modificado}.
    Antes: {valor_anterior}
    Ahora: {valor_nuevo}
    """
    criterios_afectados = motor.buscar_por_similitud(
        query_texto=query_cambio,
        filtros={"chunk_tipo": "criterio_aceptacion"},
        top_k=10
    )

    # Filtrar solo los de alta similitud (probablemente afectados)
    criterios_riesgo = [
        c for c in criterios_afectados
        if c.similitud > 0.80
        and c.metadatos.get("requisito_id") != requisito_id
    ]

    return {
        "requisito_modificado": requisito_id,
        "campo_modificado": campo_modificado,
        "dependencias_directas": [
            c.metadatos.get("requisito_id")
            for c in dependencias_directas
        ],
        "criterios_en_riesgo": [
            {
                "ac_id": c.metadatos.get("ac_id"),
                "requisito": c.metadatos.get("requisito_id"),
                "similitud": round(c.similitud, 2),
                "texto": c.texto[:200]
            }
            for c in criterios_riesgo
        ],
        "accion_recomendada": (
            "Revisar los criterios de aceptación listados antes de "
            "re-generar los artefactos Jira afectados."
            if criterios_riesgo else
            "No se detectan dependencias de alto riesgo. El cambio parece aislado."
        )
    }
```

#### Caso de uso 2: Sugerencia de requisitos relacionados al analista

Durante la escritura de un nuevo requisito, el sistema sugiere en tiempo real qué requisitos existentes son relevantes, reduciendo la duplicidad desde el origen:

```python
def sugerir_relacionados_en_tiempo_real(
    texto_parcial: str,
    epica_actual: str,
    motor: MotorConsultaRAG
) -> list[dict]:
    """
    Se llama cada vez que el analista guarda el borrador de un requisito.
    Devuelve sugerencias de requisitos relacionados para mostrar
    en el panel lateral de Confluence.
    """
    resultados = motor.buscar_por_similitud(
        query_texto=texto_parcial,
        filtros={"estado": "validado"},
        top_k=5
    )
    return [
        {
            "requisito_id": r.metadatos.get("requisito_id"),
            "titulo": r.metadatos.get("titulo", r.texto[:80]),
            "epica": r.metadatos.get("epica"),
            "similitud_pct": int(r.similitud * 100),
            "relacion": (
                "⚠ Posible duplicado"
                if r.similitud > 0.90 else
                "→ Relacionado"
                if r.similitud > 0.80 else
                "~ Referencia"
            )
        }
        for r in resultados
        if r.metadatos.get("requisito_id")  # Excluir chunks sin ID
    ]
```

#### Caso de uso 3: Generación de matriz de trazabilidad automática

```python
def generar_matriz_trazabilidad(
    epica_id: str,
    motor: MotorConsultaRAG
) -> dict:
    """
    Genera la matriz de trazabilidad completa para una épica
    consultando el vector store y las tablas de metadatos.
    """
    with motor.repo.db.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT
                metadatos->>'requisito_id'   AS req_id,
                metadatos->>'ac_id'          AS ac_id,
                metadatos->>'chunk_tipo'     AS tipo,
                metadatos->>'estado'         AS estado
            FROM chunks_requisitos
            WHERE metadatos->>'epica' = %s
              AND activo = TRUE
            ORDER BY req_id, ac_id
        """, (epica_id,))

        filas = cur.fetchall()

    # Agrupar por requisito
    matriz = {}
    for req_id, ac_id, tipo, estado in filas:
        if req_id not in matriz:
            matriz[req_id] = {
                "criterios_aceptacion": [],
                "estado": estado
            }
        if ac_id and tipo == "criterio_aceptacion":
            matriz[req_id]["criterios_aceptacion"].append(ac_id)

    return {
        "epica": epica_id,
        "total_requisitos": len(matriz),
        "trazabilidad": matriz
    }
```

---

### Fase 6 — Pipeline de re-indexación automática

El repositorio solo tiene valor si se mantiene sincronizado. El trigger de re-indexación se engancha al workflow de estado del requisito:

```python
# webhook_confluence.py
# Se ejecuta cuando el estado de un requisito cambia en Confluence

from fastapi import FastAPI, BackgroundTasks
import yaml

app = FastAPI()

@app.post("/webhook/requisito-actualizado")
async def webhook_requisito(
    payload: dict,
    background_tasks: BackgroundTasks
):
    """
    Confluence llama a este endpoint cuando se guarda un requisito.
    La re-indexación ocurre en background para no bloquear al analista.
    """
    requisito_id = payload.get("page_title_id")
    nuevo_estado = payload.get("nuevo_estado")
    yaml_content = payload.get("yaml_content")

    # Solo indexar requisitos en estados procesables
    ESTADOS_INDEXABLES = {"en-revision", "validado", "deprecado"}

    if nuevo_estado not in ESTADOS_INDEXABLES:
        return {"accion": "omitido", "motivo": f"Estado '{nuevo_estado}' no indexable"}

    if nuevo_estado == "deprecado":
        # Marcar como inactivo en el vector store
        background_tasks.add_task(
            repositorio.desactivar_requisito,
            requisito_id
        )
        return {"accion": "desactivado"}

    # Para en-revision y validado: re-indexar
    background_tasks.add_task(
        indexar_desde_yaml_string,
        yaml_content,
        requisito_id
    )

    return {"accion": "re-indexacion_programada"}


async def indexar_desde_yaml_string(yaml_content: str, requisito_id: str):
    """Parsea el YAML y re-indexa todos los chunks del requisito."""
    try:
        req = yaml.safe_load(yaml_content)
        chunks = chunkerizar_requisito_desde_dict(req)
        for chunk in chunks:
            repositorio.indexar_chunk(chunk)
    except Exception as e:
        logger.error(f"Error re-indexando {requisito_id}: {e}")
```

---

## Decisiones de infraestructura

Estas son las tres opciones reales para el vector store, ordenadas por adecuación según el tamaño del proyecto:

| Criterio | pgvector | Chroma | Pinecone |
|----------|----------|--------|----------|
| **Cuándo usarlo** | Equipo ya tiene PostgreSQL, <50.000 chunks | Prototipo rápido, local | >50.000 chunks, multi-proyecto |
| **Ventaja clave** | Sin infraestructura nueva, filtros SQL nativos | Sin servidor, setup en minutos | Escala automática, SLA gestionado |
| **Limitación** | Rendimiento limitado a >100.000 chunks | No apto para producción con alta concurrencia | Coste por vector almacenado |
| **Modelo embedding** | text-embedding-3-large (OpenAI) | Cualquiera | Cualquiera |
| **Setup inicial** | 2-4 horas | 30 minutos | 1-2 horas |

Para una organización que empieza, **pgvector es la recomendación práctica**. Un repositorio de 500 requisitos con 5 chunks cada uno genera 2.500 vectores de 1.536 dimensiones, que pgvector maneja sin ningún problema y sin coste adicional de infraestructura.

---

## Lo que cambia con RAG respecto al pipeline base

El RAG enriquece cada componente del pipeline de forma concreta:

**Prompts de generación de artefactos Jira** — reciben ahora el contexto de funcionalidades similares ya implementadas. La IA no genera una historia que duplica otra existente porque ve las historias relacionadas en su contexto.

**Generación de test cases** — recibe los flujos de error de requisitos similares ya documentados, lo que permite sugerir casos de prueba que el analista del nuevo requisito habría omitido porque no sabía que ya estaban resueltos en otro módulo.

**Validación de calidad** — gana su capacidad más valiosa: la detección de contradicciones con requisitos existentes. Sin RAG, esa validación solo puede comprobar el requisito en sí mismo. Con RAG, comprueba el requisito contra todo el historial validado del proyecto.
