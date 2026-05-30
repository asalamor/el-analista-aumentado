# steps/s3_rag_context.py
"""
Paso 3 — Recuperación de contexto RAG del repositorio de requisitos.
Ejecuta 5 consultas paralelas especializadas al vector store y
ensambla el contexto para los prompts de generación.
Ver arquitectura completa en rag/repositorio_rag.py
"""

import asyncio
from config import PipelineConfig


async def recuperar_contexto_rag(
    requisito: dict,
    glosario: dict,
    config: PipelineConfig
) -> dict:
    """
    Recupera el contexto relevante del repositorio vectorial.
    Retorna un dict con chunks agrupados por categoría:
      - funcionalidad_similar
      - mismo_modulo
      - mismo_actor
      - reglas_relacionadas
      - criterios_similares
    """
    try:
        from rag.repositorio_rag import RepositorioRequisitosRAG, MotorConsultaRAG
        import psycopg2
        import anthropic

        cliente_openai = anthropic.Anthropic(api_key=config.llm.api_key)
        db = psycopg2.connect(**config.db.to_dict())
        repositorio = RepositorioRequisitosRAG(config.db.to_dict(), cliente_openai)
        motor = MotorConsultaRAG(repositorio)
        contexto = await motor.recuperar_contexto_completo(requisito)
        return contexto

    except ImportError:
        # Si el RAG no está configurado, retornar contexto vacío
        return {
            "funcionalidad_similar": [],
            "mismo_modulo": [],
            "mismo_actor": [],
            "reglas_relacionadas": [],
            "criterios_similares": []
        }
    except Exception as e:
        raise RuntimeError(f"Error en RAG: {e}")
