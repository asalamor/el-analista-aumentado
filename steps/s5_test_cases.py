# steps/s5_test_cases.py
"""
Paso 5 — Generación automática de test cases desde criterios de aceptación.
Ejecuta cinco prompts especializados:
  Prompt 1 → Casos funcionales (flujo feliz)
  Prompt 2 → Casos negativos y de error
  Prompt 3 → Casos de contorno (boundary values)
  Prompt 4 → Scripts Gherkin para automatización
  Prompt 5 → Matriz de cobertura AC↔TC
"""

import json
import re
import anthropic
from config import PipelineConfig


SYSTEM_QA = """
Eres un QA engineer senior especializado en testing funcional y automatización.
Tu función es generar casos de prueba exhaustivos, precisos y directamente
ejecutables a partir de criterios de aceptación y requisitos funcionales.

REGLAS ESTRICTAS:
1. Cada caso de prueba debe ser ejecutable sin conocimiento previo del sistema.
2. Los datos de prueba deben ser concretos. Nunca uses placeholders.
3. Cada paso tiene exactamente un resultado esperado verificable.
4. Un caso no puede tener más de 10 pasos. Si necesita más, se divide en dos.
5. Por cada flujo feliz, genera al menos un caso negativo.
6. Los casos de contorno son obligatorios para campos con rango.
7. El resultado esperado describe comportamiento OBSERVABLE, no lógica interna.
8. El output es siempre JSON válido. Sin texto fuera del JSON.
"""


async def generar_test_cases(
    historia: dict,
    requisito: dict,
    config: PipelineConfig
) -> list[dict]:
    """
    Genera el conjunto completo de test cases para una historia de usuario.
    Retorna lista de TCs listos para importar a Xray/Zephyr.
    """
    cliente = anthropic.Anthropic(api_key=config.llm.api_key)
    todos_tcs = []

    criterios = historia.get("acceptance_criteria", [])
    if not criterios:
        return []

    req_id = requisito.get("id", "REQ-???")

    # ── Prompt 1: Casos positivos ────────────────────────────
    ac_positivos = [ac for ac in criterios if ac.get("tipo", "positivo") == "positivo"]
    if ac_positivos:
        tcs_pos = await _generar_casos_positivos(
            cliente, historia, ac_positivos, req_id, config
        )
        todos_tcs.extend(tcs_pos)

    # ── Prompt 2: Casos negativos ────────────────────────────
    tcs_neg = await _generar_casos_negativos(
        cliente, historia, requisito, req_id, config
    )
    todos_tcs.extend(tcs_neg)

    # ── Prompt 3: Casos de contorno ──────────────────────────
    datos_entrada = requisito.get("datos_entrada", [])
    if datos_entrada:
        tcs_cont = await _generar_casos_contorno(
            cliente, requisito, req_id, config
        )
        todos_tcs.extend(tcs_cont)

    return todos_tcs


async def _generar_casos_positivos(
    cliente, historia: dict, ac_positivos: list,
    req_id: str, config: PipelineConfig
) -> list:
    prompt = f"""
A partir de la historia de usuario y sus criterios de aceptación positivos,
genera los casos de prueba del flujo principal (happy path).

HISTORIA:
{json.dumps(historia, ensure_ascii=False, indent=2)}

CRITERIOS POSITIVOS:
{json.dumps(ac_positivos, ensure_ascii=False, indent=2)}

Para cada criterio genera UN caso de prueba con esta estructura JSON:
{{
  "test_cases": [
    {{
      "id": "TC-{req_id.replace('REQ-','')}-01",
      "titulo": "Descripción concreta del caso",
      "tipo": "funcional_positivo",
      "criterio_origen": "AC-XXX-XX",
      "historia_origen": "US-XXX",
      "requisito_origen": "{req_id}",
      "prioridad": "critica | alta | media | baja",
      "precondiciones": ["Estado previo requerido"],
      "datos_prueba": {{"campo": "valor_concreto"}},
      "pasos": [
        {{
          "numero": 1,
          "accion": "Qué hace el usuario exactamente",
          "resultado_esperado": "Qué debe ocurrir (observable)"
        }}
      ],
      "resultado_final_esperado": "Estado final del sistema",
      "automatizable": true,
      "notas_automatizacion": "Selectores CSS/XPath clave"
    }}
  ]
}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_QA, prompt, config)
    resultado = _parsear_json_seguro(texto)
    return resultado.get("test_cases", [])


async def _generar_casos_negativos(
    cliente, historia: dict, requisito: dict,
    req_id: str, config: PipelineConfig
) -> list:
    flujos_error = historia.get("description", {}).get("flujos_error", [])
    reglas = requisito.get("reglas_negocio", [])

    prompt = f"""
A partir de la historia de usuario, genera TODOS los casos de prueba negativos
y de error posibles. Estos casos son donde viven la mayoría de los bugs.

HISTORIA:
{json.dumps(historia, ensure_ascii=False, indent=2)}

FLUJOS DE ERROR DOCUMENTADOS:
{json.dumps(flujos_error, ensure_ascii=False, indent=2)}

REGLAS DE NEGOCIO:
{json.dumps(reglas, ensure_ascii=False, indent=2)}

Genera casos para estas categorías:
A) Validaciones de campos obligatorios (qué pasa si falta cada campo)
B) Violaciones de reglas de negocio
C) Permisos y autorización (usuario sin permiso)
D) Errores de sistema (servicio no disponible)

Usa la misma estructura JSON que los casos positivos pero con:
"tipo": "negativo_validacion | negativo_permiso | negativo_regla_negocio | negativo_sistema"

Añade también:
"comportamiento_incorrecto_habitual": "Error típico del desarrollador en este caso"

Formato: {{"test_cases": [...]}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_QA, prompt, config)
    resultado = _parsear_json_seguro(texto)
    return resultado.get("test_cases", [])


async def _generar_casos_contorno(
    cliente, requisito: dict, req_id: str, config: PipelineConfig
) -> list:
    datos_entrada = requisito.get("datos_entrada", [])
    campos_con_rango = [
        d for d in datos_entrada
        if d.get("rango") or d.get("tipo") in ("date", "integer", "decimal")
    ]

    if not campos_con_rango:
        return []

    prompt = f"""
Analiza los campos con restricciones de rango en el requisito y genera
los casos de prueba de valores límite (boundary value analysis).

CAMPOS CON RESTRICCIONES:
{json.dumps(campos_con_rango, ensure_ascii=False, indent=2)}

REQUISITO COMPLETO:
{json.dumps(requisito, ensure_ascii=False, indent=2)}

Para cada restricción genera exactamente 4 casos:
1. Valor en el límite inferior exacto → debe funcionar (PASS)
2. Valor un paso por debajo del límite inferior → debe fallar (FAIL)
3. Valor en el límite superior exacto → debe funcionar (PASS)
4. Valor un paso por encima del límite superior → debe fallar (FAIL)

"Un paso" = ±1 para enteros, ±1 día para fechas, ±1 carácter para texto.

Usa "tipo": "contorno" y añade "valor_limite" describiendo qué restricción prueba.

Formato: {{"restricciones_identificadas": [{{"campo": "...", "test_cases": [...]}}]}}
"""
    texto = await _llamar_llm(cliente, SYSTEM_QA, prompt, config)
    resultado = _parsear_json_seguro(texto)

    # Aplanar los TCs de todas las restricciones
    tcs = []
    for restriccion in resultado.get("restricciones_identificadas", []):
        tcs.extend(restriccion.get("test_cases", []))
    return tcs


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


def _parsear_json_seguro(texto: str) -> dict:
    texto = re.sub(r"```(?:json)?", "", texto).strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return {"test_cases": [], "error": texto[:200]}
