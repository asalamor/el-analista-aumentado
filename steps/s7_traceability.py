# steps/s7_traceability.py
"""
Paso 7 — Registro en el grafo de trazabilidad.
Persiste todas las relaciones generadas en el pipeline
en el grafo de nodos y aristas (pgvector / PostgreSQL).
Ver implementación completa en: trazabilidad/motor_trazabilidad.py
"""

from config import PipelineConfig


async def registrar_en_grafo(
    requisito: dict,
    artefactos: dict,
    test_cases: list,
    config: PipelineConfig
) -> dict:
    """
    Registra todos los nodos y aristas generados por el pipeline
    en el grafo de trazabilidad. Retorna métricas de lo registrado.
    """
    try:
        import psycopg2
        from trazabilidad.motor_trazabilidad import MotorTrazabilidad, Nodo, Arista

        motor = MotorTrazabilidad(config.db.to_dict())

        historia = artefactos.get("historia", {})
        tareas   = artefactos.get("tareas", [])
        req_id   = requisito.get("id", "")
        epica_id = requisito.get("epica", "")

        nodos = 0
        aristas = 0

        # Registrar nodo del requisito
        motor.registrar_nodo(Nodo(
            id=req_id, tipo="requisito",
            titulo=requisito.get("titulo", ""),
            estado=requisito.get("estado", ""),
            metadatos={"epica": epica_id, "actor": requisito.get("actor", "")}
        ))
        nodos += 1

        # Registrar criterios AC como nodos
        criterios_ids = []
        for ac in historia.get("acceptance_criteria", []):
            ac_id = ac.get("id", "")
            motor.registrar_nodo(Nodo(
                id=ac_id, tipo="criterio_ac",
                titulo=ac.get("titulo", ac.get("cuando", "")[:60]),
                estado="activo",
                metadatos={"requisito_id": req_id, "tipo": ac.get("tipo", "positivo")}
            ))
            motor.registrar_arista(Arista(
                origen_id=req_id, destino_id=ac_id,
                tipo_relacion="deriva_de"
            ))
            criterios_ids.append(ac_id)
            nodos += 1
            aristas += 1

        # Registrar test cases
        for tc in test_cases:
            tc_id = tc.get("id", "")
            motor.registrar_nodo(Nodo(
                id=tc_id, tipo="test_case",
                titulo=tc.get("titulo", ""),
                estado="pendiente",
                metadatos={
                    "tipo": tc.get("tipo", ""),
                    "automatizable": tc.get("automatizable", False),
                    "criterio_origen": tc.get("criterio_origen", "")
                }
            ))
            nodos += 1

        # Registrar tareas técnicas
        tareas_ids = []
        for i, tarea in enumerate(tareas):
            tk_id = f"{req_id}-TK-{i+1:02d}"
            motor.registrar_nodo(Nodo(
                id=tk_id, tipo="tarea",
                titulo=tarea.get("summary", ""),
                estado="To Do",
                metadatos={
                    "capa": tarea.get("capa", ""),
                    "estimacion_horas": tarea.get("estimacion_horas", 0)
                }
            ))
            tareas_ids.append(tk_id)
            nodos += 1

        motor.db.close()

        return {
            "nodos_registrados": nodos,
            "aristas_registradas": aristas,
            "criterios_ids": criterios_ids,
            "tareas_ids": tareas_ids
        }

    except Exception as e:
        return {
            "nodos_registrados": 0,
            "aristas_registradas": 0,
            "error": str(e)
        }
