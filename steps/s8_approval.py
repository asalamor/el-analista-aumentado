# steps/s8_approval.py
"""
Paso 8 — Interfaz de aprobación humana en línea de comandos.
Muestra los artefactos generados de forma legible y solicita
la decisión del analista: aprobar, editar o rechazar.
"""

import json
from state import EstadoRun


async def solicitar_aprobacion(
    run: EstadoRun,
    artefactos: dict,
    test_cases: list,
    informe_validacion: dict,
    informe_impacto: dict
) -> dict:
    """
    Muestra el resumen de artefactos al analista y solicita su decisión.
    Retorna dict con 'decision' (aprobado|rechazado) y datos adicionales.
    """
    historia = artefactos.get("historia", {})
    tareas   = artefactos.get("tareas", [])

    print("\n" + "╔" + "═" * 52 + "╗")
    print(f"║  REVISIÓN DE ARTEFACTOS — {run.requisito_id:<24} ║")
    print("╠" + "═" * 52 + "╣")

    # Historia
    print("║  HISTORIA" + " " * 43 + "║")
    summary = historia.get("summary", "Sin título")[:50]
    print(f"║  {summary:<51}║")
    sp = historia.get("story_points", "?")
    prio = historia.get("priority", "?")
    epica = artefactos.get("epica_id", "?")
    print(f"║  Story Points: {sp}  │  Prioridad: {prio:<12} ║")
    print(f"║  Épica: {epica:<44} ║")

    # Criterios AC
    criterios = historia.get("acceptance_criteria", [])
    print("╠" + "═" * 52 + "╣")
    print(f"║  CRITERIOS DE ACEPTACIÓN ({len(criterios)})" + " " * (28 - len(str(len(criterios)))) + "║")
    for ac in criterios[:4]:
        ac_id = ac.get("id", "?")
        cuando = ac.get("cuando", "")[:40]
        print(f"║  {ac_id}: {cuando:<43}║")

    # Tareas
    print("╠" + "═" * 52 + "╣")
    print(f"║  TAREAS TÉCNICAS ({len(tareas)})" + " " * (34 - len(str(len(tareas)))) + "║")
    for t in tareas[:5]:
        capa = t.get("capa", "?")[:10]
        titulo = t.get("summary", "")[:38]
        print(f"║  [{capa:<10}] {titulo:<39}║")

    # Test cases
    n_tc = len(test_cases)
    n_pos  = sum(1 for tc in test_cases if "positivo" in tc.get("tipo", ""))
    n_neg  = sum(1 for tc in test_cases if "negativo" in tc.get("tipo", ""))
    n_cont = sum(1 for tc in test_cases if "contorno" in tc.get("tipo", ""))
    print("╠" + "═" * 52 + "╣")
    print(f"║  TEST CASES ({n_tc}): {n_pos} pos · {n_neg} neg · {n_cont} contorno" +
          " " * max(0, 20 - len(str(n_tc))) + "║")

    # Alertas de validación
    if informe_validacion:
        advertencias = informe_validacion.get(
            "problemas_por_prioridad", {}
        ).get("advertencias", [])
        if advertencias:
            print("╠" + "═" * 52 + "╣")
            print(f"║  ⚠ {len(advertencias)} ADVERTENCIAS DE VALIDACIÓN" + " " * 20 + "║")

    # Alertas de impacto
    if informe_impacto:
        nivel = informe_impacto.get("informe_impacto", {}).get("nivel_urgencia", "")
        if nivel in ("CRITICO", "ALTO"):
            print("╠" + "═" * 52 + "╣")
            print(f"║  ⚠ IMPACTO DE CAMBIO: {nivel:<30} ║")

    print("╠" + "═" * 52 + "╣")
    print("║  [A] Aprobar y empujar a Jira" + " " * 23 + "║")
    print("║  [E] Editar antes de aprobar" + " " * 24 + "║")
    print("║  [R] Rechazar (devolver al analista)" + " " * 16 + "║")
    print("║  [V] Ver JSON completo" + " " * 30 + "║")
    print("╚" + "═" * 52 + "╝")

    while True:
        decision_raw = input("  Decisión: ").strip().upper()

        if decision_raw == "A":
            analista = input("  Tu nombre/email para el registro: ").strip()
            return {
                "decision": "aprobado",
                "analista": analista,
                "timestamp": _now_iso()
            }

        elif decision_raw == "E":
            print("\n  Abriendo el JSON en el editor...")
            ruta_temp = _guardar_json_temp(artefactos, test_cases)
            print(f"  Archivo: {ruta_temp}")
            print("  Edita el archivo y guárdalo. Pulsa ENTER cuando termines.")
            input()
            import json
            with open(ruta_temp) as f:
                artefactos_editados = json.load(f)
            analista = input("  Tu nombre/email: ").strip()
            return {
                "decision": "aprobado",
                "analista": analista,
                "artefactos_editados": artefactos_editados,
                "timestamp": _now_iso()
            }

        elif decision_raw == "R":
            motivo = input("  Motivo del rechazo: ").strip()
            return {
                "decision": "rechazado",
                "motivo": motivo,
                "timestamp": _now_iso()
            }

        elif decision_raw == "V":
            print("\n" + json.dumps(artefactos, ensure_ascii=False, indent=2)[:3000])
            print("...")
        else:
            print("  Opción no reconocida. Usa A, E, R o V.")


def _guardar_json_temp(artefactos: dict, test_cases: list) -> str:
    import tempfile, json, os
    payload = {"artefactos": artefactos, "test_cases": test_cases}
    fd, ruta = tempfile.mkstemp(suffix=".json", prefix="pipeline_aprobacion_")
    os.close(fd)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return ruta


def _now_iso() -> str:
    from datetime import datetime
    return datetime.now().isoformat()
