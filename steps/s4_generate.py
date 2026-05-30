# steps/s4_generate.py
"""
Paso 4 — Generación de artefactos Jira mediante LLM.
Ejecuta cuatro prompts encadenados:
  Prompt 1 → Épica (si no existe)
  Prompt 2 → Historia de usuario + criterios AC
  Prompt 3 → Tareas técnicas por capa
  Prompt 4 → Subtareas (para tareas >8h)

Ver prompts completos en prompts/v1.1/
"""

import json
import re
import anthropic
from config import PipelineConfig
from steps.s2_validate import _formatear_glosario_compacto


SYSTEM_GENERACION = """
Eres un analista funcional senior especializado en metodologías Agile (Scrum/SAFe).
Tu función es transformar requisitos funcionales estructurados en artefactos Jira
con precisión, consistencia y sin añadir asunciones no documentadas.

REGLAS ESTRICTAS:
1. Nunca inventes información no explícita en el requisito.
   Si falta información, usa [PENDIENTE: descripción].
2. Usa exclusivamente los términos del glosario proporcionado.
3. Los criterios de aceptación SIEMPRE siguen formato Dado/Cuando/Entonces.
4. Nunca fusiones dos requisitos en una sola historia.
5. Si detectas ambigüedad, indícala en 'alertas_calidad'.
6. El output es siempre JSON válido. Sin texto antes ni después.
"""


async def generar_artefactos_jira(
    requisito: dict,
    glosario: dict,
    contexto_rag: dict,
    config: PipelineConfig
) -> dict:
    """
    Genera la épica (si procede), la historia, las tareas técnicas
    y ensambla el resultado completo listo para aprobación.
    """
    cliente = anthropic.Anthropic(api_key=config.llm.api_key)
    glosario_txt = _formatear_glosario_compacto(glosario)
    contexto_txt = _formatear_contexto_rag(contexto_rag)

    # Cargar prompts desde archivos
    p2_historia = _cargar_prompt("p2_historia", config)
    p3_tareas   = _cargar_prompt("p3_tareas",   config)

    system = f"{SYSTEM_GENERACION}\n\nGLOSARIO:\n{glosario_txt}\n\nCONTEXTO RAG:\n{contexto_txt}"

    # ── Prompt 2: Historia de usuario ────────────────────────
    user_historia = p2_historia.format(
        requisito_yaml=json.dumps(requisito, ensure_ascii=False, indent=2),
        epic_jira_id=requisito.get("epica", "EP-??"),
        epic_summary=requisito.get("modulo", ""),
        historias_existentes_resumen=contexto_txt[:500],
        req_id=requisito.get("id", "REQ-???")
    )
    texto_historia = await _llamar_llm(cliente, system, user_historia, config)
    historia = _parsear_json_seguro(texto_historia)

    # ── Prompt 3: Tareas técnicas ────────────────────────────
    stack_txt = _cargar_prompt("stack_tecnologico", config)
    user_tareas = p3_tareas.format(
        historia_json=json.dumps(historia, ensure_ascii=False, indent=2),
        stack_tecnologico=stack_txt,
        convenciones_equipo="Las tareas de backend incluyen tests unitarios. "
                            "Las de frontend incluyen accesibilidad WCAG 2.1 AA."
    )
    texto_tareas = await _llamar_llm(cliente, system, user_tareas, config)
    resultado_tareas = _parsear_json_seguro(texto_tareas)
    tareas = resultado_tareas.get("tareas", [])

    return {
        "historia": historia,
        "tareas": tareas,
        "requisito_id": requisito.get("id"),
        "epica_id": requisito.get("epica"),
    }


async def _llamar_llm(cliente, system: str, user: str, config: PipelineConfig) -> str:
    import time
    for intento in range(config.llm.max_reintentos):
        try:
            respuesta = cliente.messages.create(
                model=config.llm.model,
                max_tokens=config.llm.max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}]
            )
            return respuesta.content[0].text
        except Exception as e:
            if intento < config.llm.max_reintentos - 1:
                time.sleep(2 ** intento)
            else:
                raise


def _cargar_prompt(nombre: str, config: PipelineConfig) -> str:
    """Carga un prompt desde el directorio de prompts versionados."""
    ruta = config.repo_prompts / f"{nombre}.txt"
    if ruta.exists():
        return ruta.read_text(encoding="utf-8")
    # Retornar placeholder si el archivo no existe
    return f"[PROMPT {nombre} NO ENCONTRADO EN {config.repo_prompts}]"


def _parsear_json_seguro(texto: str) -> dict:
    texto = re.sub(r"```(?:json)?", "", texto).strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"error": "JSON no parseable", "texto_raw": texto[:300]}


def _formatear_contexto_rag(contexto: dict) -> str:
    """Formatea el contexto RAG para inyección en el prompt."""
    if not contexto:
        return "Sin contexto RAG disponible."
    lineas = []
    similares = contexto.get("funcionalidad_similar", [])
    if similares:
        lineas.append("REQUISITOS CON FUNCIONALIDAD SIMILAR (validados):")
        for c in similares[:3]:
            req_id = c.get("metadatos", {}).get("requisito_id", "?")
            sim = int(c.get("similitud", 0) * 100)
            lineas.append(f"  [{req_id}] ({sim}% similitud): {c.get('texto', '')[:200]}")
    reglas = contexto.get("reglas_relacionadas", [])
    if reglas:
        lineas.append("\nREGLAS DE NEGOCIO EXISTENTES EN EL MÓDULO:")
        for c in reglas[:3]:
            req_id = c.get("metadatos", {}).get("requisito_id", "?")
            lineas.append(f"  [{req_id}]: {c.get('texto', '')[:200]}")
    return "\n".join(lineas) if lineas else "Sin contexto relevante recuperado."
