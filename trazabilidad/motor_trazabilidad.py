# trazabilidad/motor_trazabilidad.py
"""
Motor del grafo de trazabilidad.
Gestiona nodos y aristas que conectan:
  requisito → historia → criterio_ac → test_case → issue_jira → commit

Punto 9 del modelo operativo AI-ready.
"""

import json
import psycopg2
from dataclasses import dataclass
from typing import Optional


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
        "genera", "verifica", "implementa", "descompone",
        "depende_de", "pertenece_a", "reemplaza", "vincula", "deriva_de"
    }

    def __init__(self, db_config: dict):
        self.db = psycopg2.connect(**db_config)
        self._inicializar_schema()

    def _inicializar_schema(self):
        with self.db.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS nodos_trazabilidad (
                    id                  TEXT PRIMARY KEY,
                    tipo                TEXT NOT NULL,
                    titulo              TEXT,
                    estado              TEXT,
                    metadatos           JSONB,
                    fecha_creacion      TIMESTAMP DEFAULT NOW(),
                    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
                    activo              BOOLEAN DEFAULT TRUE
                );

                CREATE TABLE IF NOT EXISTS aristas_trazabilidad (
                    id              SERIAL PRIMARY KEY,
                    origen_id       TEXT REFERENCES nodos_trazabilidad(id),
                    destino_id      TEXT REFERENCES nodos_trazabilidad(id),
                    tipo_relacion   TEXT NOT NULL,
                    confianza       FLOAT DEFAULT 1.0,
                    origen_relacion TEXT,
                    metadatos       JSONB,
                    fecha_creacion  TIMESTAMP DEFAULT NOW(),
                    activo          BOOLEAN DEFAULT TRUE,
                    UNIQUE (origen_id, destino_id, tipo_relacion)
                );

                CREATE INDEX IF NOT EXISTS idx_aristas_origen
                    ON aristas_trazabilidad (origen_id, tipo_relacion);
                CREATE INDEX IF NOT EXISTS idx_aristas_destino
                    ON aristas_trazabilidad (destino_id, tipo_relacion);
                CREATE INDEX IF NOT EXISTS idx_nodos_tipo
                    ON nodos_trazabilidad (tipo, estado);
                CREATE INDEX IF NOT EXISTS idx_nodos_metadatos
                    ON nodos_trazabilidad USING gin (metadatos);
            """)
            self.db.commit()

    def registrar_nodo(self, nodo: Nodo) -> bool:
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO nodos_trazabilidad (id, tipo, titulo, estado, metadatos)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    titulo              = EXCLUDED.titulo,
                    estado              = EXCLUDED.estado,
                    metadatos           = EXCLUDED.metadatos,
                    fecha_actualizacion = NOW()
                RETURNING (xmax = 0) AS es_nuevo
            """, (
                nodo.id, nodo.tipo, nodo.titulo, nodo.estado,
                json.dumps(nodo.metadatos or {})
            ))
            es_nuevo = cur.fetchone()[0]
            self.db.commit()
            return es_nuevo

    def registrar_arista(self, arista: Arista) -> bool:
        if arista.tipo_relacion not in self.TIPOS_RELACION_VALIDOS:
            raise ValueError(f"Tipo de relación '{arista.tipo_relacion}' no válido.")

        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO aristas_trazabilidad
                    (origen_id, destino_id, tipo_relacion, confianza, origen_relacion, metadatos)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (origen_id, destino_id, tipo_relacion)
                DO UPDATE SET
                    confianza       = GREATEST(aristas_trazabilidad.confianza, EXCLUDED.confianza),
                    origen_relacion = EXCLUDED.origen_relacion,
                    fecha_creacion  = NOW()
            """, (
                arista.origen_id, arista.destino_id, arista.tipo_relacion,
                arista.confianza, arista.origen_relacion,
                json.dumps(arista.metadatos or {})
            ))
            self.db.commit()
            return True

    def registrar_generacion_completa(
        self, requisito_id: str, historia_id: str,
        criterios_ac: list[str], tareas: list[str],
        test_cases: list[str], issue_jira_key: str, epica_id: str
    ):
        """Registra en una transacción todas las relaciones de un requisito."""
        with self.db.cursor() as cur:
            try:
                def upsert(origen, destino, tipo):
                    cur.execute("""
                        INSERT INTO aristas_trazabilidad
                            (origen_id, destino_id, tipo_relacion, confianza, origen_relacion)
                        VALUES (%s, %s, %s, 1.0, 'pipeline_generacion')
                        ON CONFLICT (origen_id, destino_id, tipo_relacion)
                        DO UPDATE SET confianza = 1.0, fecha_creacion = NOW()
                    """, (origen, destino, tipo))

                upsert(requisito_id, epica_id, "pertenece_a")
                upsert(requisito_id, historia_id, "genera")
                upsert(historia_id, epica_id, "pertenece_a")

                if issue_jira_key:
                    upsert(historia_id, issue_jira_key, "vincula")

                for ac_id in criterios_ac:
                    upsert(historia_id, ac_id, "genera")
                    upsert(requisito_id, ac_id, "deriva_de")

                for tarea_id in tareas:
                    upsert(historia_id, tarea_id, "descompone")

                for tc_id in test_cases:
                    upsert(tc_id, historia_id, "verifica")

                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise RuntimeError(f"Error registrando trazabilidad: {e}")

    def gaps_de_trazabilidad(self, epica_id: str) -> dict:
        """Identifica gaps de trazabilidad en una épica."""
        gaps = {
            "epica_id": epica_id,
            "requisitos_sin_historia": [],
            "historias_sin_test_cases": [],
            "criterios_sin_test_case": [],
            "historias_sin_issue_jira": [],
        }

        with self.db.cursor() as cur:
            # Requisitos sin historia
            cur.execute("""
                SELECT n.id, n.titulo FROM nodos_trazabilidad n
                WHERE n.tipo = 'requisito' AND n.activo = TRUE
                  AND n.metadatos->>'epica' = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM aristas_trazabilidad a
                      WHERE a.origen_id = n.id AND a.tipo_relacion = 'genera'
                        AND a.activo = TRUE
                  )
            """, (epica_id,))
            gaps["requisitos_sin_historia"] = [
                {"id": f[0], "titulo": f[1]} for f in cur.fetchall()
            ]

            # Historias sin test cases
            cur.execute("""
                SELECT n.id, n.titulo FROM nodos_trazabilidad n
                WHERE n.tipo = 'historia' AND n.activo = TRUE
                  AND n.metadatos->>'epica' = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM aristas_trazabilidad a
                      WHERE a.destino_id = n.id AND a.tipo_relacion = 'verifica'
                        AND a.activo = TRUE
                  )
            """, (epica_id,))
            gaps["historias_sin_test_cases"] = [
                {"id": f[0], "titulo": f[1]} for f in cur.fetchall()
            ]

        total = sum(len(v) for v in gaps.values() if isinstance(v, list))
        gaps["resumen"] = {
            "total_gaps": total,
            "nivel_riesgo": (
                "critico" if total > 10 else
                "alto"    if total > 5  else
                "medio"   if total > 2  else
                "bajo"
            )
        }
        return gaps
