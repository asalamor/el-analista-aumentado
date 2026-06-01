# 2. Matriz de trazabilidad automática

La matriz de trazabilidad es el artefacto que más tiempo consume cuando se mantiene manualmente y el primero que se abandona cuando el proyecto acelera. Automatizarla elimina ese trade-off: el equipo tiene trazabilidad completa sin coste de mantenimiento.

---

## Por qué la trazabilidad automatizada cambia la dinámica del proyecto

En un proyecto tradicional, la matriz de trazabilidad existe en tres momentos: al inicio del proyecto cuando alguien la crea con entusiasmo, tras la primera auditoría cuando alguien la actualiza por obligación, y nunca más. El motivo es que mantenerla manualmente es un trabajo de horas que produce valor días después, cuando ya nadie recuerda por qué se hizo el cambio.

Una matriz automatizada existe en tiempo real. Cada vez que se genera un artefacto, se actualiza la traza. Cada vez que cambia un requisito, se propaga el cambio. Y lo más importante: responde preguntas que en un proyecto manual son imposibles de responder en menos de una hora.

- ¿Qué requisito de negocio justifica este test case que está fallando en CI?
- ¿Qué test cases debo ejecutar si modifico este endpoint?
- ¿Qué historias no tienen ningún test case asociado?
- ¿Qué requisitos del cliente están cubiertos por el sprint actual?

---

## Modelo de datos de la trazabilidad

Antes de construir el pipeline, hay que definir el grafo de relaciones que la matriz representa. No es una tabla plana: es un **grafo dirigido** donde cada nodo es un artefacto y cada arista es una relación tipada.

```
REQUISITO (REQ-023)
│
├── pertenece_a ──────────► ÉPICA (EP-04)
│
└── genera ───────────────► HISTORIA (US-047)
                            │
                            ├── pertenece_a ──► ÉPICA (EP-04)
                            ├── vincula ──────► ISSUE JIRA (FACT-47)
                            │
                            ├── genera ───────► CRITERIO AC (AC-023-01)
                            │                   └── verifica ◄── TEST CASE (TC-111)
                            │
                            └── descompone ──► TAREA TÉCNICA (TK-001)
                                              └── implementa ◄── COMMIT (abc123)
```

### Modelo de datos: el grafo de trazabilidad en base de datos

El grafo se implementa con dos tablas: nodos y aristas. Esta estructura permite recorrer la trazabilidad en cualquier dirección sin rediseñar el esquema cuando aparece un nuevo tipo de artefacto.

```sql
-- Tabla de nodos: cualquier artefacto del proyecto
CREATE TABLE nodos_trazabilidad (
    id              TEXT PRIMARY KEY,
    -- Formato: REQ-023, US-047, TC-111, FACT-47, PR-892
    tipo            TEXT NOT NULL,
    -- requisito | historia | test_case | tarea | issue_jira |
    -- criterio_ac | commit | epic
    titulo          TEXT,
    estado          TEXT,
    metadatos       JSONB,
    -- Campos específicos por tipo almacenados como JSON
    -- Para historias: sprint, story_points, assignee
    -- Para test cases: resultado_ultimo, automatizable
    -- Para commits: hash, rama, autor
    fecha_creacion      TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
    activo          BOOLEAN DEFAULT TRUE
);

-- Tabla de aristas: relaciones tipadas entre artefactos
CREATE TABLE aristas_trazabilidad (
    id              SERIAL PRIMARY KEY,
    origen_id       TEXT REFERENCES nodos_trazabilidad(id),
    destino_id      TEXT REFERENCES nodos_trazabilidad(id),
    tipo_relacion   TEXT NOT NULL,
    -- genera | verifica | implementa | descompone | depende_de |
    -- pertenece_a | reemplaza | vincula
    confianza       FLOAT DEFAULT 1.0,
    -- 1.0   = relación explícita documentada
    -- 0.7-0.9 = inferida por RAG con alta similitud
    -- 0.5-0.7 = inferida con similitud media (requiere revisión)
    origen_relacion TEXT,
    -- pipeline_generacion | rag_inference | manual | webhook_jira
    metadatos       JSONB,
    fecha_creacion  TIMESTAMP DEFAULT NOW(),
    activo          BOOLEAN DEFAULT TRUE,

    UNIQUE (origen_id, destino_id, tipo_relacion)
);

-- Índices para recorrido eficiente del grafo en ambas direcciones
CREATE INDEX idx_aristas_origen  ON aristas_trazabilidad (origen_id, tipo_relacion);
CREATE INDEX idx_aristas_destino ON aristas_trazabilidad (destino_id, tipo_relacion);
CREATE INDEX idx_nodos_tipo      ON nodos_trazabilidad (tipo, estado);
CREATE INDEX idx_nodos_metadatos ON nodos_trazabilidad USING gin (metadatos);
```

---

## Fase 1 — Motor de registro de trazabilidad

El motor es el componente que actualiza el grafo cada vez que el pipeline genera o modifica un artefacto. Se llama automáticamente al final de cada paso del pipeline de generación.

```python
from dataclasses import dataclass
from typing import Optional
import psycopg2
import json
from datetime import datetime


@dataclass
class Nodo:
    id: str
    tipo: str
    titulo: str = ""
    estado: str = "activo"
    metadatos: dict = None


@dataclass
class Arista:
    origen_id: str
    destino_id: str
    tipo_relacion: str
    confianza: float = 1.0
    origen_relacion: str = "pipeline_generacion"
    metadatos: dict = None


class MotorTrazabilidad:
    """
    Gestiona el grafo de trazabilidad del proyecto.
    Se llama automáticamente desde el pipeline de generación
    y desde los webhooks de Jira y Xray.
    """

    TIPOS_RELACION_VALIDOS = {
        "genera",        # REQ → US, US → TC
        "verifica",      # TC → AC, TC → US
        "implementa",    # commit → US, commit → TK
        "descompone",    # US → TK, TK → subtarea
        "depende_de",    # REQ → REQ (dependencia declarada)
        "pertenece_a",   # REQ → EP, US → EP
        "reemplaza",     # REQ nuevo → REQ deprecado
        "vincula",       # Issue Jira → US (relación bidireccional)
        "deriva_de",     # AC → REQ (criterio derivado del requisito)
    }

    def __init__(self, db_config: dict):
        self.db = psycopg2.connect(**db_config)

    def registrar_nodo(self, nodo: Nodo) -> bool:
        """
        Registra o actualiza un nodo en el grafo.
        Retorna True si es nuevo, False si ya existía.
        """
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO nodos_trazabilidad
                    (id, tipo, titulo, estado, metadatos)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    titulo              = EXCLUDED.titulo,
                    estado              = EXCLUDED.estado,
                    metadatos           = EXCLUDED.metadatos,
                    fecha_actualizacion = NOW()
                RETURNING (xmax = 0) AS es_nuevo
            """, (
                nodo.id, nodo.tipo, nodo.titulo,
                nodo.estado, json.dumps(nodo.metadatos or {})
            ))
            es_nuevo = cur.fetchone()[0]
            self.db.commit()
            return es_nuevo

    def registrar_arista(self, arista: Arista) -> bool:
        """
        Registra una relación entre dos nodos.
        Si ya existe con menor confianza, la actualiza.
        """
        if arista.tipo_relacion not in self.TIPOS_RELACION_VALIDOS:
            raise ValueError(
                f"Tipo de relación '{arista.tipo_relacion}' no válido. "
                f"Válidos: {self.TIPOS_RELACION_VALIDOS}"
            )
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO aristas_trazabilidad
                    (origen_id, destino_id, tipo_relacion,
                     confianza, origen_relacion, metadatos)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (origen_id, destino_id, tipo_relacion)
                DO UPDATE SET
                    confianza       = GREATEST(
                        aristas_trazabilidad.confianza,
                        EXCLUDED.confianza
                    ),
                    origen_relacion = EXCLUDED.origen_relacion,
                    metadatos       = EXCLUDED.metadatos,
                    fecha_creacion  = NOW()
            """, (
                arista.origen_id, arista.destino_id, arista.tipo_relacion,
                arista.confianza, arista.origen_relacion,
                json.dumps(arista.metadatos or {})
            ))
            self.db.commit()
            return True

    def registrar_generacion_completa(
        self,
        requisito_id: str,
        historia_id: str,
        criterios_ac: list[str],
        tareas: list[str],
        test_cases: list[str],
        issue_jira_key: str,
        epica_id: str
    ):
        """
        Registra en una sola transacción todas las relaciones
        generadas por el pipeline para un requisito completo.
        Este es el método que se llama al final del pipeline de generación.
        """
        with self.db.cursor() as cur:
            try:
                # REQ → EP (pertenece a épica)
                cur.execute(self._sql_upsert_arista(), (
                    requisito_id, epica_id, "pertenece_a", 1.0,
                    "pipeline_generacion", json.dumps({})
                ))

                # REQ → US (el requisito genera la historia)
                cur.execute(self._sql_upsert_arista(), (
                    requisito_id, historia_id, "genera", 1.0,
                    "pipeline_generacion",
                    json.dumps({"timestamp": datetime.now().isoformat()})
                ))

                # US → EP (la historia pertenece a la épica)
                cur.execute(self._sql_upsert_arista(), (
                    historia_id, epica_id, "pertenece_a", 1.0,
                    "pipeline_generacion", json.dumps({})
                ))

                # US → Issue Jira (vinculación)
                if issue_jira_key:
                    cur.execute(self._sql_upsert_arista(), (
                        historia_id, issue_jira_key, "vincula", 1.0,
                        "pipeline_generacion", json.dumps({})
                    ))

                # US → AC (criterios de aceptación derivados)
                for ac_id in criterios_ac:
                    cur.execute(self._sql_upsert_arista(), (
                        historia_id, ac_id, "genera", 1.0,
                        "pipeline_generacion", json.dumps({})
                    ))
                    # REQ → AC (el requisito origina el criterio)
                    cur.execute(self._sql_upsert_arista(), (
                        requisito_id, ac_id, "deriva_de", 1.0,
                        "pipeline_generacion", json.dumps({})
                    ))

                # US → TK (la historia se descompone en tareas)
                for tarea_id in tareas:
                    cur.execute(self._sql_upsert_arista(), (
                        historia_id, tarea_id, "descompone", 1.0,
                        "pipeline_generacion", json.dumps({})
                    ))

                # TC → US (cada test case verifica la historia)
                for tc_id in test_cases:
                    cur.execute(self._sql_upsert_arista(), (
                        tc_id, historia_id, "verifica", 1.0,
                        "pipeline_generacion", json.dumps({})
                    ))

                self.db.commit()

            except Exception as e:
                self.db.rollback()
                raise RuntimeError(
                    f"Error registrando trazabilidad de {requisito_id}: {e}"
                )
```

---

## Fase 2 — Motor de consulta del grafo

Con el grafo construido, el motor de consulta responde las preguntas de trazabilidad en tiempo real. Todas las consultas se implementan como recorridos de grafo sobre las dos tablas.

```python
class ConsultorTrazabilidad:
    """
    Responde consultas de trazabilidad sobre el grafo.
    Cada método responde una pregunta concreta del equipo.
    """

    def __init__(self, db_config: dict):
        self.db = psycopg2.connect(**db_config)

    # ── CONSULTAS DESCENDENTES (de requisito a test) ──────────────

    def traza_completa_requisito(self, requisito_id: str) -> dict:
        """
        Retorna la cadena completa de trazabilidad descendente:
        REQ → US → AC → TC → Ejecuciones
             └──→ TK → Issue Jira → Commit
        """
        with self.db.cursor() as cur:
            # CTE recursivo para recorrer el grafo en profundidad
            cur.execute("""
                WITH RECURSIVE grafo AS (
                    SELECT
                        id, tipo, titulo, estado, metadatos,
                        0 AS nivel,
                        ARRAY[id] AS camino,
                        NULL::TEXT AS relacion_padre
                    FROM nodos_trazabilidad
                    WHERE id = %s AND activo = TRUE

                    UNION ALL

                    SELECT
                        n.id, n.tipo, n.titulo, n.estado, n.metadatos,
                        g.nivel + 1,
                        g.camino || n.id,
                        a.tipo_relacion
                    FROM grafo g
                    JOIN aristas_trazabilidad a ON a.origen_id = g.id
                    JOIN nodos_trazabilidad n ON n.id = a.destino_id
                    WHERE
                        n.activo = TRUE
                        AND a.activo = TRUE
                        AND a.confianza >= 0.7
                        AND NOT (n.id = ANY(g.camino))  -- evitar ciclos
                        AND g.nivel < 6                 -- limitar profundidad
                )
                SELECT id, tipo, titulo, estado, metadatos, nivel, relacion_padre
                FROM grafo
                ORDER BY nivel, tipo, id
            """, (requisito_id,))
            filas = cur.fetchall()

        return self._estructurar_traza_descendente(requisito_id, filas)

    # ── CONSULTAS ASCENDENTES (de artefacto a requisito) ─────────

    def origen_de_test_case(self, tc_id: str) -> dict:
        """
        Dado un test case (por ejemplo uno que falla en CI),
        retorna la cadena ascendente hasta el requisito de negocio.
        Responde: ¿qué requisito de negocio justifica este test?
        """
        with self.db.cursor() as cur:
            cur.execute("""
                WITH RECURSIVE ascendente AS (
                    SELECT id, tipo, titulo, estado, 0 AS nivel,
                           ARRAY[id] AS camino
                    FROM nodos_trazabilidad
                    WHERE id = %s AND activo = TRUE

                    UNION ALL

                    SELECT n.id, n.tipo, n.titulo, n.estado,
                           a.nivel + 1, a.camino || n.id
                    FROM ascendente a
                    JOIN aristas_trazabilidad ar ON ar.destino_id = a.id
                    JOIN nodos_trazabilidad n ON n.id = ar.origen_id
                    WHERE
                        n.activo = TRUE
                        AND ar.activo = TRUE
                        AND NOT (n.id = ANY(a.camino))
                        AND a.nivel < 5
                )
                SELECT id, tipo, titulo, estado, nivel
                FROM ascendente
                ORDER BY nivel
            """, (tc_id,))
            cadena = cur.fetchall()

        return {
            "test_case_id": tc_id,
            "cadena_ascendente": [
                {"id": f[0], "tipo": f[1], "titulo": f[2], "estado": f[3], "nivel": f[4]}
                for f in cadena
            ],
            "requisito_origen": next(
                (f[0] for f in cadena if f[1] == "requisito"), None
            ),
            "historia_origen": next(
                (f[0] for f in cadena if f[1] == "historia"), None
            )
        }

    def test_cases_de_componente(
        self,
        componente: str,
        solo_fallidos: bool = False
    ) -> dict:
        """
        Dado un componente técnico (por ejemplo 'api-facturacion'),
        retorna todos los test cases que verifican funcionalidad
        implementada en ese componente.
        Responde: ¿qué tests debo ejecutar si modifico este componente?
        """
        with self.db.cursor() as cur:
            filtro_estado = "AND n_tc.estado = 'fallido'" if solo_fallidos else ""
            cur.execute(f"""
                SELECT DISTINCT
                    n_tc.id, n_tc.titulo, n_tc.estado, n_tc.metadatos,
                    n_us.id, n_us.titulo,
                    n_req.id, n_req.titulo
                FROM nodos_trazabilidad n_tk
                JOIN aristas_trazabilidad a_us_tk
                    ON a_us_tk.destino_id = n_tk.id
                    AND a_us_tk.tipo_relacion = 'descompone'
                JOIN nodos_trazabilidad n_us
                    ON n_us.id = a_us_tk.origen_id AND n_us.tipo = 'historia'
                JOIN aristas_trazabilidad a_tc_us
                    ON a_tc_us.destino_id = n_us.id
                    AND a_tc_us.tipo_relacion = 'verifica'
                JOIN nodos_trazabilidad n_tc
                    ON n_tc.id = a_tc_us.origen_id AND n_tc.tipo = 'test_case'
                    {filtro_estado}
                JOIN aristas_trazabilidad a_req_us
                    ON a_req_us.destino_id = n_us.id
                    AND a_req_us.tipo_relacion = 'genera'
                JOIN nodos_trazabilidad n_req
                    ON n_req.id = a_req_us.origen_id AND n_req.tipo = 'requisito'
                WHERE
                    n_tk.tipo = 'tarea'
                    AND n_tk.metadatos->>'componente' = %s
                    AND n_tk.activo = TRUE
                ORDER BY n_req.id, n_us.id, n_tc.id
            """, (componente,))
            filas = cur.fetchall()

        return {
            "componente": componente,
            "total_test_cases": len(filas),
            "test_cases": [
                {
                    "tc_id": f[0], "titulo": f[1], "estado": f[2],
                    "automatizable": (f[3] or {}).get("automatizable", False),
                    "historia_id": f[4], "historia_titulo": f[5],
                    "requisito_id": f[6], "requisito_titulo": f[7]
                }
                for f in filas
            ]
        }

    # ── CONSULTAS DE COBERTURA Y GAPS ────────────────────────────

    def gaps_de_trazabilidad(self, epica_id: str) -> dict:
        """
        Identifica todos los gaps de trazabilidad en una épica:
        requisitos sin historia, historias sin test cases,
        criterios sin cobertura, issues sin commits.
        """
        gaps = {
            "epica_id": epica_id,
            "requisitos_sin_historia": [],
            "historias_sin_test_cases": [],
            "criterios_sin_test_case": [],
            "historias_sin_issue_jira": [],
            "issues_sin_commits": [],
            "resumen": {}
        }

        with self.db.cursor() as cur:
            # Gap 1: Requisitos sin historia generada
            cur.execute("""
                SELECT n.id, n.titulo, n.estado
                FROM nodos_trazabilidad n
                WHERE n.tipo = 'requisito'
                  AND n.activo = TRUE
                  AND n.metadatos->>'epica' = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM aristas_trazabilidad a
                      WHERE a.origen_id = n.id
                        AND a.tipo_relacion = 'genera'
                        AND a.activo = TRUE
                  )
            """, (epica_id,))
            gaps["requisitos_sin_historia"] = [
                {"id": f[0], "titulo": f[1], "estado": f[2]}
                for f in cur.fetchall()
            ]

            # Gap 2: Historias sin test cases
            cur.execute("""
                SELECT n.id, n.titulo, n.estado, n.metadatos->>'sprint' AS sprint
                FROM nodos_trazabilidad n
                WHERE n.tipo = 'historia'
                  AND n.activo = TRUE
                  AND n.metadatos->>'epica' = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM aristas_trazabilidad a
                      WHERE a.destino_id = n.id
                        AND a.tipo_relacion = 'verifica'
                        AND a.activo = TRUE
                  )
            """, (epica_id,))
            gaps["historias_sin_test_cases"] = [
                {"id": f[0], "titulo": f[1], "estado": f[2], "sprint": f[3]}
                for f in cur.fetchall()
            ]

            # Gap 3: Criterios AC sin test case asociado
            cur.execute("""
                SELECT n_ac.id, n_ac.titulo, n_req.id AS req_id
                FROM nodos_trazabilidad n_ac
                JOIN aristas_trazabilidad a
                    ON a.destino_id = n_ac.id AND a.tipo_relacion = 'deriva_de'
                JOIN nodos_trazabilidad n_req
                    ON n_req.id = a.origen_id AND n_req.metadatos->>'epica' = %s
                WHERE n_ac.tipo = 'criterio_ac'
                  AND n_ac.activo = TRUE
                  AND NOT EXISTS (
                      SELECT 1 FROM aristas_trazabilidad a2
                      WHERE a2.origen_id = n_ac.id
                        AND a2.tipo_relacion = 'verifica'
                        AND a2.activo = TRUE
                  )
            """, (epica_id,))
            gaps["criterios_sin_test_case"] = [
                {"ac_id": f[0], "titulo": f[1], "requisito_id": f[2]}
                for f in cur.fetchall()
            ]

        # Calcular resumen
        total_gaps = sum(len(v) for v in gaps.values() if isinstance(v, list))
        gaps["resumen"] = {
            "total_gaps": total_gaps,
            "nivel_riesgo": (
                "critico"   if total_gaps > 10 else
                "alto"      if total_gaps > 5  else
                "medio"     if total_gaps > 2  else
                "bajo"
            ),
            "gap_mas_critico": (
                "Requisitos sin historia"
                if gaps["requisitos_sin_historia"] else
                "Criterios AC sin test case"
                if gaps["criterios_sin_test_case"] else
                "Historias sin test cases"
                if gaps["historias_sin_test_cases"] else
                "Sin gaps críticos"
            )
        }
        return gaps

    def cobertura_sprint(self, sprint_id: str) -> dict:
        """
        Para un sprint dado, retorna qué porcentaje de los requisitos
        comprometidos tienen cobertura completa de test cases.
        Responde: ¿estamos listos para entregar este sprint?
        """
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT
                    n_req.id, n_req.titulo,
                    n_us.id, n_us.estado,
                    COUNT(DISTINCT n_tc.id) FILTER (WHERE n_tc.tipo = 'test_case') AS total_tc,
                    COUNT(DISTINCT n_tc.id) FILTER (WHERE n_tc.tipo = 'test_case' AND n_tc.estado = 'pasado') AS tc_pasados,
                    COUNT(DISTINCT n_tc.id) FILTER (WHERE n_tc.tipo = 'test_case' AND n_tc.estado = 'fallido') AS tc_fallidos,
                    COUNT(DISTINCT n_ac.id) AS total_ac
                FROM nodos_trazabilidad n_us
                JOIN nodos_trazabilidad n_ij
                    ON n_ij.metadatos->>'historia_id' = n_us.id
                    AND n_ij.metadatos->>'sprint_id' = %s
                JOIN aristas_trazabilidad a_req
                    ON a_req.destino_id = n_us.id AND a_req.tipo_relacion = 'genera'
                JOIN nodos_trazabilidad n_req ON n_req.id = a_req.origen_id
                LEFT JOIN aristas_trazabilidad a_tc
                    ON a_tc.destino_id = n_us.id AND a_tc.tipo_relacion = 'verifica'
                LEFT JOIN nodos_trazabilidad n_tc ON n_tc.id = a_tc.origen_id AND n_tc.tipo = 'test_case'
                LEFT JOIN aristas_trazabilidad a_ac
                    ON a_ac.origen_id = n_us.id AND a_ac.tipo_relacion = 'genera'
                LEFT JOIN nodos_trazabilidad n_ac
                    ON n_ac.id = a_ac.destino_id AND n_ac.tipo = 'criterio_ac'
                WHERE n_us.tipo = 'historia'
                GROUP BY n_req.id, n_req.titulo, n_us.id, n_us.estado
                ORDER BY n_req.id
            """, (sprint_id,))
            filas = cur.fetchall()

        historias = []
        for f in filas:
            total_tc = f[4] or 0
            tc_pasados = f[5] or 0
            tc_fallidos = f[6] or 0
            historias.append({
                "requisito_id": f[0], "requisito_titulo": f[1],
                "historia_id": f[2], "estado_historia": f[3],
                "total_ac": f[7] or 0,
                "total_tc": total_tc, "tc_pasados": tc_pasados, "tc_fallidos": tc_fallidos,
                "tc_pendientes": total_tc - tc_pasados - tc_fallidos,
                "cobertura": (
                    "sin_tests"   if total_tc == 0 else
                    "todo_pass"   if tc_pasados == total_tc else
                    "con_fallos"  if tc_fallidos > 0 else
                    "en_progreso"
                ),
                "lista_para_entrega": (
                    f[3] == "Hecho" and total_tc > 0 and
                    tc_fallidos == 0 and tc_pasados == total_tc
                )
            })

        total = len(historias)
        listas = sum(1 for h in historias if h["lista_para_entrega"])
        return {
            "sprint_id": sprint_id,
            "total_historias": total,
            "historias_listas": listas,
            "porcentaje_listo": round(listas / total * 100) if total > 0 else 0,
            "semaforo": (
                "verde"    if listas == total else
                "amarillo" if listas >= total * 0.8 else
                "rojo"
            ),
            "historias": historias
        }
```

---

## Fase 3 — Generación del informe de matriz

El informe de la matriz no es un volcado de datos: es un documento estructurado que responde preguntas concretas. Se genera bajo demanda o automáticamente al final de cada sprint.

```python
class GeneradorMatrizTrazabilidad:
    """
    Genera el informe completo de la matriz de trazabilidad
    en múltiples formatos: JSON, Markdown, CSV, Confluence.
    """

    def __init__(self, consultor: ConsultorTrazabilidad, openai_client):
        self.consultor = consultor
        self.openai = openai_client

    def generar_matriz_epica(self, epica_id: str) -> dict:
        """
        Genera la matriz completa para una épica.
        Incluye cobertura, gaps y recomendaciones.
        """
        gaps = self.consultor.gaps_de_trazabilidad(epica_id)
        trazas = self._obtener_todas_las_trazas(epica_id)
        metricas = self._calcular_metricas_globales(trazas, gaps)
        analisis = self._generar_analisis_narrativo(epica_id, metricas, gaps)

        return {
            "matriz_trazabilidad": {
                "epica_id": epica_id,
                "fecha_generacion": datetime.now().isoformat(),
                "metricas_globales": metricas,
                "gaps": gaps,
                "trazas_por_requisito": trazas,
                "analisis": analisis,
                "tabla_resumen": self._generar_tabla_resumen(trazas)
            }
        }

    def _calcular_metricas_globales(
        self,
        trazas: list[dict],
        gaps: dict
    ) -> dict:
        total_req = len(trazas)
        total_us  = sum(len(t["historias"]) for t in trazas)
        total_ac  = sum(len(t["criterios_aceptacion"]) for t in trazas)
        total_tc  = sum(len(t["test_cases"]) for t in trazas)
        total_tk  = sum(len(t["tareas_tecnicas"]) for t in trazas)

        req_con_historia = sum(1 for t in trazas if len(t["historias"]) > 0)
        us_con_tc = total_us - len(gaps["historias_sin_test_cases"])
        ac_con_tc = total_ac - len(gaps["criterios_sin_test_case"])

        return {
            "totales": {
                "requisitos":      total_req,
                "historias":       total_us,
                "criterios_ac":    total_ac,
                "test_cases":      total_tc,
                "tareas_tecnicas": total_tk
            },
            "cobertura": {
                "req_con_historia_pct": round(req_con_historia / total_req * 100) if total_req else 0,
                "us_con_test_pct":      round(us_con_tc / total_us * 100) if total_us else 0,
                "ac_con_test_pct":      round(ac_con_tc / total_ac * 100) if total_ac else 0,
                "ratio_tc_por_ac":      round(total_tc / total_ac, 1) if total_ac else 0
            },
            "salud_trazabilidad": (
                "excelente" if (
                    req_con_historia == total_req and
                    us_con_tc == total_us and
                    total_tc >= total_ac * 2
                ) else
                "buena"     if req_con_historia >= total_req * 0.9 and us_con_tc >= total_us * 0.8 else
                "mejorable" if req_con_historia >= total_req * 0.7 else
                "deficiente"
            )
        }

    def _generar_tabla_resumen(self, trazas: list[dict]) -> list[dict]:
        """
        Genera la tabla plana de la matriz para exportar a CSV
        o renderizar en Confluence. Una fila por criterio de aceptación.
        """
        filas = []
        for traza in trazas:
            req_id = traza["requisito_id"]

            if not traza["historias"]:
                filas.append({
                    "requisito_id": req_id, "historia_id": "❌ Sin historia",
                    "criterio_ac": "—", "test_case_id": "—",
                    "estado_tc": "—", "issue_jira": "—",
                    "cobertura": "sin_historia"
                })
                continue

            for historia in traza["historias"]:
                us_id  = historia["id"]
                issue  = next((i["id"] for i in traza["issues_jira"]), "❌ Sin issue")

                if not traza["criterios_aceptacion"]:
                    filas.append({
                        "requisito_id": req_id, "historia_id": us_id,
                        "criterio_ac": "❌ Sin AC", "test_case_id": "—",
                        "estado_tc": "—", "issue_jira": issue,
                        "cobertura": "sin_ac"
                    })
                    continue

                for ac in traza["criterios_aceptacion"]:
                    tcs_del_ac = [
                        tc for tc in traza["test_cases"]
                        if ac["id"] in tc.get("metadatos", {}).get("criterio_origen", "")
                    ]
                    if not tcs_del_ac:
                        filas.append({
                            "requisito_id": req_id, "historia_id": us_id,
                            "criterio_ac": ac["id"], "test_case_id": "❌ Sin TC",
                            "estado_tc": "—", "issue_jira": issue,
                            "cobertura": "sin_test"
                        })
                    else:
                        for tc in tcs_del_ac:
                            filas.append({
                                "requisito_id": req_id, "historia_id": us_id,
                                "criterio_ac": ac["id"], "test_case_id": tc["id"],
                                "estado_tc": tc.get("estado", "pendiente"),
                                "issue_jira": issue, "cobertura": "completa"
                            })
        return filas

    def _generar_analisis_narrativo(
        self,
        epica_id: str,
        metricas: dict,
        gaps: dict
    ) -> dict:
        prompt = f"""
        Eres un auditor de calidad de software. Analiza las métricas de
        trazabilidad de la épica {epica_id} y genera un informe ejecutivo conciso.

        MÉTRICAS: {json.dumps(metricas, indent=2, ensure_ascii=False)}

        GAPS DETECTADOS:
        - Requisitos sin historia:  {len(gaps['requisitos_sin_historia'])}
        - Historias sin test cases: {len(gaps['historias_sin_test_cases'])}
        - Criterios AC sin test:    {len(gaps['criterios_sin_test_case'])}
        - Historias sin issue Jira: {len(gaps['historias_sin_issue_jira'])}

        Genera el siguiente JSON:
        {{
          "estado_general": "...",
          "riesgos_principales": ["..."],
          "recomendaciones_prioritarias": [
            {{"orden": 1, "accion": "...", "responsable": "...", "impacto": "..."}}
          ],
          "mensaje_para_stakeholders": "..."
        }}
        """
        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    # ── EXPORTADORES ──────────────────────────────────────────────

    def exportar_csv(self, matriz: dict, ruta: str):
        """Exporta la tabla resumen a CSV para Excel o Sheets."""
        import csv
        tabla = matriz["matriz_trazabilidad"]["tabla_resumen"]
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "requisito_id", "historia_id", "criterio_ac",
                "test_case_id", "estado_tc", "issue_jira", "cobertura"
            ])
            writer.writeheader()
            writer.writerows(tabla)

    def exportar_markdown(self, matriz: dict) -> str:
        """Genera la matriz en Markdown para Confluence o GitHub."""
        datos    = matriz["matriz_trazabilidad"]
        metricas = datos["metricas_globales"]
        analisis = datos["analisis"]

        md  = f"# Matriz de Trazabilidad — {datos['epica_id']}\n\n"
        md += f"**Generada:** {datos['fecha_generacion']}  \n"
        md += f"**Estado general:** {analisis['estado_general']}\n\n"

        md += "## Métricas de cobertura\n\n"
        md += "| Artefacto | Total | Cobertura |\n|---|---|---|\n"
        md += f"| Requisitos con historia   | {metricas['totales']['requisitos']}   | {metricas['cobertura']['req_con_historia_pct']}% |\n"
        md += f"| Historias con test cases  | {metricas['totales']['historias']}    | {metricas['cobertura']['us_con_test_pct']}% |\n"
        md += f"| Criterios AC con test     | {metricas['totales']['criterios_ac']} | {metricas['cobertura']['ac_con_test_pct']}% |\n"
        md += f"| Ratio TC por AC           | —                                     | {metricas['cobertura']['ratio_tc_por_ac']} |\n\n"
        md += f"**Salud de la trazabilidad:** `{metricas['salud_trazabilidad'].upper()}`\n\n"

        md += "## Tabla de trazabilidad\n\n"
        md += "| Requisito | Historia | Criterio AC | Test Case | Estado TC | Issue Jira | Cobertura |\n"
        md += "|---|---|---|---|---|---|---|\n"

        iconos = {
            "completa":     "✅",
            "sin_historia": "❌",
            "sin_ac":       "⚠️",
            "sin_test":     "🔴"
        }
        for fila in datos["tabla_resumen"]:
            icono = iconos.get(fila["cobertura"], "—")
            md += (
                f"| {fila['requisito_id']} | {fila['historia_id']} "
                f"| {fila['criterio_ac']} | {fila['test_case_id']} "
                f"| {fila['estado_tc']} | {fila['issue_jira']} "
                f"| {icono} {fila['cobertura']} |\n"
            )

        md += "\n## Recomendaciones\n\n"
        for r in analisis["recomendaciones_prioritarias"]:
            md += f"{r['orden']}. **{r['accion']}** — Responsable: {r['responsable']}\n"

        md += f"\n## Para el Product Owner\n\n{analisis['mensaje_para_stakeholders']}\n"
        return md
```

---

## Ejemplo de informe generado para EP-04

Este es el aspecto del output real para la épica de facturación con cuatro requisitos:

```markdown
# Matriz de Trazabilidad — EP-04

**Generada:** 2025-05-08T10:15:00Z
**Estado general:** La épica tiene cobertura de historias completa pero
el 30% de los criterios de aceptación carece de test case asociado.

## Métricas de cobertura

| Artefacto                | Total | Cobertura |
|---|---|---|
| Requisitos con historia  |     4 |     100%  |
| Historias con test cases |     4 |      75%  |
| Criterios AC con test    |    14 |      71%  |
| Ratio TC por AC          |     — |       2.1 |

**Salud de la trazabilidad:** `MEJORABLE`

## Tabla de trazabilidad

| Requisito | Historia | Criterio AC | Test Case  | Estado TC | Issue Jira | Cobertura     |
|---|---|---|---|---|---|---|
| REQ-021   | US-045   | AC-021-01   | TC-101     | pasado    | FACT-41    | ✅ completa   |
| REQ-021   | US-045   | AC-021-02   | TC-102     | pasado    | FACT-41    | ✅ completa   |
| REQ-021   | US-045   | AC-021-03   | ❌ Sin TC  | —         | FACT-41    | 🔴 sin_test   |
| REQ-022   | US-046   | AC-022-01   | TC-107     | pasado    | FACT-44    | ✅ completa   |
| REQ-022   | US-046   | AC-022-02   | TC-108     | fallido   | FACT-44    | ✅ completa   |
| REQ-023   | US-047   | AC-023-01   | TC-111     | pasado    | FACT-47    | ✅ completa   |
| REQ-023   | US-047   | AC-023-02   | TC-112     | pasado    | FACT-47    | ✅ completa   |
| REQ-023   | US-047   | AC-023-03   | TC-113     | pasado    | FACT-47    | ✅ completa   |
| REQ-024   | US-049   | AC-024-01   | ❌ Sin TC  | —         | FACT-51    | 🔴 sin_test   |
| REQ-024   | US-049   | AC-024-02   | ❌ Sin TC  | —         | FACT-51    | 🔴 sin_test   |

## Recomendaciones

1. **Generar test cases para AC-021-03, AC-024-01 y AC-024-02** — Responsable: QA Lead
2. **Investigar TC-108 fallido antes del cierre del sprint** — Responsable: Tech Lead + QA Lead
3. **Ejecutar pipeline de generación de test cases sobre US-049** — Responsable: Analista funcional

## Para el Product Owner

La épica tiene todas las historias definidas y tres cuartas partes de los test cases
aprobados. Antes de dar el sprint por cerrado hay que resolver un test fallido y generar
cobertura para la historia US-049 que actualmente no tiene ninguna prueba.
```

---

## Integración con el resto del pipeline

La matriz no es un artefacto estático que se genera una vez. Se actualiza en cuatro momentos del ciclo de vida:

**Al generar artefactos.** Cada llamada al pipeline registra automáticamente las nuevas aristas en el grafo vía `registrar_generacion_completa`. La matriz se actualiza en tiempo real sin intervención manual.

**Al detectar impacto de cambios.** Cuando el analizador de impacto marca artefactos como afectados, sus nodos se actualizan en el grafo con estado `requiere_revision`, lo que aparece en la matriz como una advertencia visual.

**Al actualizar issues en Jira.** Un webhook de Jira llama a `registrar_nodo` cuando cambia el estado de un issue, y a `registrar_arista` cuando se crea un commit con referencia al issue en el mensaje.

**Al ejecutar test cases en Xray.** Un webhook registra el resultado de cada ejecución como un nodo de tipo `ejecucion_tc` con arista `produce` desde el test case, lo que permite que la columna `estado_tc` de la matriz refleje el resultado real más reciente.
