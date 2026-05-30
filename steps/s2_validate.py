# steps/s2_validate.py
"""
Paso 2 — Validación automática de calidad del requisito.
Ejecuta cuatro llamadas LLM especializadas:
  1. Validación estructural (campos obligatorios y formatos)
  2. Validación semántica (ambigüedad, verificabilidad, atomicidad)
  3. Validación de consistencia (glosario, contradicciones)
  4. Validación de completitud funcional (flujos, datos, contornos)
Y consolida los resultados en un informe único.
"""

import json
import anthropic
from config import PipelineConfig


SYSTEM_VALIDACION = """
Eres un auditor de calidad de requisitos funcionales con experiencia en
proyectos Agile enterprise. Tu función es detectar problemas en requisitos
funcionales ANTES de que entren en un pipeline de generación de artefactos.

Tu sesgo debe ser conservador: ante la duda, marca el problema.
Es mejor un falso positivo que un requisito ambiguo en producción.

REGLAS DE COMPORTAMIENTO:
1. No generes contenido nuevo ni corrijas el requisito. Solo diagnostica.
2. Para cada problema indica: campo afectado, por qué es un problema,
   ejemplo de cómo debería expresarse correctamente.
3. Clasifica cada problema como:
   BLOQUEANTE → impide la generación correcta de artefactos
   ADVERTENCIA → degrada la calidad pero no impide la generación
   SUGERENCIA → mejora opcional
4. Un requisito con un solo problema BLOQUEANTE se rechaza completamente.
5. El output es siempre JSON válido. Sin texto fuera del JSON.
"""


async def validar_requisito(
    requisito: dict,
    glosario: dict,
    config: PipelineConfig
) -> dict:
    """
    Ejecuta el pipeline completo de validación de cuatro fases
    y retorna el informe consolidado.
    """
    cliente = anthropic.Anthropic(api_key=config.llm.api_key)

    # Ejecutar las cuatro validaciones secuencialmente
    val_estructural  = await _validar_estructural(cliente, requisito, config)
    val_semantica    = await _validar_semantica(cliente, requisito, config)
    val_consistencia = await _validar_consistencia(cliente, requisito, glosario, config)
    val_completitud  = await _validar_completitud(cliente, requisito, config)

    # Consolidar en informe único
    informe = await _consolidar(
        cliente, requisito,
        val_estructural, val_semantica, val_consistencia, val_completitud,
        config
    )

    return informe


async def _llamar_llm(cliente, system: str, user: str, config: PipelineConfig) -> str:
    """Llamada genérica al LLM con reintentos."""
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


async def _validar_estructural(cliente, requisito: dict, config: PipelineConfig) -> dict:
    prompt = f"""
Valida que el siguiente requisito tiene todos los campos obligatorios
con el formato correcto.

REQUISITO A VALIDAR:
{json.dumps(requisito, ensure_ascii=False, indent=2)}

CAMPOS REQUERIDOS:
- id: formato REQ-NNN
- titulo: no vacío, máximo 80 caracteres, sin verbos ambiguos
  (gestionar, administrar, manejar, controlar, procesar, permitir)
- epica: formato EP-NN
- actor: no vacío, debe ser un rol específico (no "el usuario")
- prioridad: must-have | should-have | could-have | wont-have
- estado: borrador | en-revision | validado | rechazado | deprecado
- descripcion: mínimo 30 palabras
- evento_disparador: no vacío
- criterios_aceptacion: mínimo 1 criterio con dado/cuando/entonces
- excepciones: mínimo 1 excepción

Genera JSON con estructura:
{{
  "validacion_estructural": {{
    "resultado": "APROBADO | BLOQUEADO",
    "problemas": [
      {{
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "campo": "nombre del campo",
        "problema": "descripción del problema",
        "valor_actual": "valor actual del campo",
        "ejemplo_correcto": "cómo debería ser"
      }}
    ],
    "campos_validados": 0,
    "campos_con_problema": 0
  }}
}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_VALIDACION, prompt, config)
    return _parsear_json(texto)


async def _validar_semantica(cliente, requisito: dict, config: PipelineConfig) -> dict:
    prompt = f"""
Analiza el contenido semántico del siguiente requisito buscando
ambigüedades, criterios no verificables y problemas de atomicidad.

REQUISITO:
{json.dumps(requisito, ensure_ascii=False, indent=2)}

Busca:
A) Cuantificadores vagos: rápido, eficiente, adecuado, correcto, intuitivo
B) Verbos sin sujeto definido: "se podrá", "se mostrará"
C) Condiciones implícitas: "si es necesario", "cuando proceda"
D) Criterios AC no verificables (no pueden responderse PASS/FAIL)
E) Requisito que mezcla más de una funcionalidad (tiene "y", "también")

Genera JSON con estructura:
{{
  "validacion_semantica": {{
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "puntuacion_calidad": 0,
    "problemas_consolidados": [
      {{
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "bloque": "ambiguedad | verificabilidad | atomicidad | completitud",
        "ubicacion": "campo y fragmento problemático",
        "problema": "descripción y consecuencia",
        "ejemplo_correcto": "cómo debería expresarse"
      }}
    ]
  }}
}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_VALIDACION, prompt, config)
    return _parsear_json(texto)


async def _validar_consistencia(
    cliente, requisito: dict, glosario: dict, config: PipelineConfig
) -> dict:
    glosario_compacto = _formatear_glosario_compacto(glosario)
    prompt = f"""
Valida que el requisito es consistente con el glosario del proyecto.

REQUISITO:
{json.dumps(requisito, ensure_ascii=False, indent=2)}

GLOSARIO (términos oficiales):
{glosario_compacto}

Verifica:
A) ¿Se usan los términos oficiales del glosario?
B) ¿Se usan sinónimos no oficiales que crearán inconsistencias?
C) ¿Alguna regla de negocio contradice el glosario o las reglas globales?

Genera JSON con estructura:
{{
  "validacion_consistencia": {{
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "problemas_consolidados": [
      {{
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "bloque": "terminologia | contradicciones | duplicidad",
        "ubicacion": "campo afectado",
        "problema": "descripción",
        "ejemplo_correcto": "cómo debería ser"
      }}
    ]
  }}
}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_VALIDACION, prompt, config)
    return _parsear_json(texto)


async def _validar_completitud(cliente, requisito: dict, config: PipelineConfig) -> dict:
    prompt = f"""
Analiza si el requisito está funcionalmente completo para generar
artefactos sin lagunas que se conviertan en bugs.

REQUISITO:
{json.dumps(requisito, ensure_ascii=False, indent=2)}

Verifica:
A) ¿Está documentado el flujo principal?
B) ¿Están documentados los flujos de error?
C) ¿Los datos de entrada tienen tipo, formato y validaciones?
D) ¿Se han considerado los casos de contorno?
E) ¿Cada regla de negocio tiene su criterio AC?

Genera JSON con estructura:
{{
  "validacion_completitud": {{
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "preguntas_sin_responder": [
      {{
        "pregunta": "¿Qué pasa si...?",
        "consecuencia_si_no_se_resuelve": "Bug o comportamiento indefinido",
        "severidad": "BLOQUEANTE | ADVERTENCIA"
      }}
    ]
  }}
}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_VALIDACION, prompt, config)
    return _parsear_json(texto)


async def _consolidar(
    cliente, requisito: dict,
    val_est, val_sem, val_cons, val_comp,
    config: PipelineConfig
) -> dict:
    """Consolida los cuatro informes en uno único con veredicto final."""

    # Recopilar todos los problemas
    todos_bloqueantes = []
    todas_advertencias = []

    for val in [val_est, val_sem, val_cons, val_comp]:
        for clave in val:
            problemas = val[clave].get("problemas_consolidados", []) or \
                        val[clave].get("problemas", [])
            for p in problemas:
                if p.get("severidad") == "BLOQUEANTE":
                    todos_bloqueantes.append(p)
                elif p.get("severidad") == "ADVERTENCIA":
                    todas_advertencias.append(p)

    # Calcular puntuación
    score_semantica = val_sem.get("validacion_semantica", {}).get("puntuacion_calidad", 80)
    penalizacion = len(todos_bloqueantes) * 15 + len(todas_advertencias) * 5
    score_final = max(0, score_semantica - penalizacion)

    # Determinar veredicto
    if todos_bloqueantes:
        veredicto = "BLOQUEADO"
    elif todas_advertencias:
        veredicto = "APROBADO_CON_ADVERTENCIAS"
    else:
        veredicto = "APROBADO"

    return {
        "requisito_id": requisito.get("id"),
        "veredicto_final": veredicto,
        "puede_entrar_al_pipeline": veredicto != "BLOQUEADO",
        "puntuacion_global": {
            "valor": score_final,
            "escala": "0-100"
        },
        "problemas_por_prioridad": {
            "bloqueantes": todos_bloqueantes,
            "advertencias": todas_advertencias
        },
        "checklist_rapido": {
            "tiene_id_valido": not any(
                p.get("campo") == "id" for p in todos_bloqueantes
            ),
            "tiene_actor_definido": not any(
                p.get("campo") == "actor" for p in todos_bloqueantes
            ),
            "tiene_ac_verificables": val_sem.get(
                "validacion_semantica", {}
            ).get("resultado") != "BLOQUEADO",
            "usa_glosario_oficial": val_cons.get(
                "validacion_consistencia", {}
            ).get("resultado") == "APROBADO",
            "flujos_error_documentados": val_comp.get(
                "validacion_completitud", {}
            ).get("resultado") != "BLOQUEADO",
        },
        "detalle_por_fase": {
            "estructural":  val_est,
            "semantica":    val_sem,
            "consistencia": val_cons,
            "completitud":  val_comp,
        }
    }


def _parsear_json(texto: str) -> dict:
    """Parsea JSON desde el texto del LLM con limpieza de marcadores."""
    import re
    texto = re.sub(r"```(?:json)?", "", texto).strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"error": "JSON no parseable", "texto_raw": texto[:500]}


def _formatear_glosario_compacto(glosario: dict) -> str:
    """Formatea el glosario en texto compacto para inyección en prompts."""
    lineas = []
    for actor in glosario.get("actores", []):
        sinon = ", ".join(actor.get("sinonimos_no_oficiales", []))
        lineas.append(
            f"ACTOR '{actor['nombre_oficial']}' [NO usar: {sinon}]: "
            f"{actor.get('descripcion', '')[:120]}"
        )
    for entidad in glosario.get("entidades", []):
        sinon = ", ".join(entidad.get("sinonimos_no_oficiales", []))
        lineas.append(
            f"ENTIDAD '{entidad['nombre_oficial']}' [NO usar: {sinon}]: "
            f"{entidad.get('descripcion', '')[:120]}"
        )
    for regla in glosario.get("reglas_globales", []):
        lineas.append(f"REGLA GLOBAL: {regla.get('descripcion', '')[:150]}")
    return "\n".join(lineas)
