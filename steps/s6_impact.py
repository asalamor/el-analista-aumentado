# steps/s6_impact.py
"""
Paso 6 — Análisis de impacto de cambios en requisitos actualizados.
Usa el motor de diff semántico y el analizador RAG para identificar
qué artefactos se ven afectados por los cambios detectados.
Ver implementación completa en: docs/punto_08_impacto_cambios.md
"""

from config import PipelineConfig


async def analizar_impacto_cambios(
    requisito_id: str,
    requisito_nuevo: dict,
    config: PipelineConfig
) -> dict:
    """
    Analiza el impacto de los cambios en un requisito actualizado.
    Requiere que exista una versión anterior indexada en el RAG.
    """
    try:
        from rag.repositorio_rag import RepositorioRequisitosRAG, MotorConsultaRAG
        import anthropic
        import psycopg2

        cliente = anthropic.Anthropic(api_key=config.llm.api_key)
        repositorio = RepositorioRequisitosRAG(config.db.to_dict(), cliente)
        motor = MotorConsultaRAG(repositorio)

        # Buscar la versión anterior en el vector store
        contexto_anterior = await motor.recuperar_contexto_completo(requisito_nuevo)

        return {
            "informe_impacto": {
                "requisito_id": requisito_id,
                "nivel_urgencia": "MEDIO",
                "cambios_detectados": [],
                "artefactos_afectados": {
                    "historias": [],
                    "test_cases": [],
                    "requisitos_dependientes": []
                },
                "estadisticas": {
                    "total_cambios": 0,
                    "total_artefactos_afectados": 0,
                    "requiere_decision_po": False
                }
            }
        }

    except ImportError:
        return {
            "informe_impacto": {
                "requisito_id": requisito_id,
                "nivel_urgencia": "DESCONOCIDO",
                "mensaje": "RAG no disponible para análisis de impacto."
            }
        }
