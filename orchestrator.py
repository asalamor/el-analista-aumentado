"""
orchestrator.py — Orquestador principal del pipeline AI de análisis funcional.

Uso básico:
  python orchestrator.py --req REQ-023
  python orchestrator.py --epica EP-04
  python orchestrator.py --req REQ-023 --dry-run
  python orchestrator.py --req REQ-023 --desde s4_generacion_artefactos
  python orchestrator.py --epica EP-04 --paralelo 3

Flags disponibles:
  --req            ID de un requisito individual
  --epica          ID de épica para procesar todos sus requisitos
  --dry-run        Genera artefactos pero no push a Jira/Xray
  --sin-aprobacion Modo automático sin intervención humana
  --desde          Reanudar desde un paso específico
  --paralelo N     Número de requisitos en paralelo (modo épica)
  --verbose        Output detallado de cada llamada al LLM
"""

import argparse
import asyncio
import sys
import time
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import PipelineConfig
from state import GestorEstado, EstadoEjecucion, EstadoPaso

# Importar los pasos del pipeline
from steps.s1_load        import cargar_requisito
from steps.s2_validate    import validar_requisito
from steps.s3_rag_context import recuperar_contexto_rag
from steps.s4_generate    import generar_artefactos_jira
from steps.s5_test_cases  import generar_test_cases
from steps.s6_impact      import analizar_impacto_cambios
from steps.s7_traceability import registrar_en_grafo
from steps.s8_approval    import solicitar_aprobacion
from steps.s9_push        import push_a_jira, push_a_xray

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("pipeline")


class PipelineFallo(Exception):
    def __init__(self, paso: str, mensaje: str):
        self.paso = paso
        self.mensaje = mensaje
        super().__init__(f"[{paso}] {mensaje}")


# ─────────────────────────────────────────────────────────────
# PIPELINE DE UN REQUISITO
# ─────────────────────────────────────────────────────────────

async def ejecutar_pipeline_requisito(
    requisito_id: str,
    config: PipelineConfig,
    gestor: GestorEstado,
    forzar_desde: Optional[str] = None
) -> dict:
    """Ejecuta el pipeline completo para un único requisito."""

    separador = "─" * 56
    print(f"\n{separador}")
    print(f"  PIPELINE → {requisito_id}")
    print(f"  Modo: {'DRY-RUN' if config.dry_run else 'PRODUCCIÓN'}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separador)

    inicio_total = time.time()

    ruta_yaml = _encontrar_yaml(requisito_id, config)
    if not ruta_yaml:
        log.error(f"YAML no encontrado para {requisito_id}")
        return {"exito": False, "error": "YAML no encontrado"}

    yaml_content = ruta_yaml.read_text(encoding="utf-8")
    run = gestor.crear_run(requisito_id, yaml_content, config.dry_run)

    if forzar_desde:
        run = _resetear_desde_paso(run, forzar_desde, gestor)

    try:
        # ── PASO 1: Carga ────────────────────────────────────
        paso = "s1_carga"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(1, "Carga y parseo del requisito")
            run = gestor.iniciar_paso(run, paso)
            try:
                requisito = cargar_requisito(yaml_content)
                run.artefactos_generados = run.artefactos_generados or {}
                run.artefactos_generados["requisito"] = requisito
                run = gestor.completar_paso(run, paso, {
                    "titulo": requisito.get("titulo"),
                    "epica": requisito.get("epica"),
                    "estado": requisito.get("estado")
                })
                _log_ok(f"'{requisito.get('titulo', '')[:60]}'")
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)
            requisito = run.artefactos_generados.get("requisito", {})

        if requisito.get("estado") not in ("en-revision", "validado"):
            msg = (f"Estado '{requisito.get('estado')}' no procesable. "
                   f"Requiere 'en-revision' o 'validado'.")
            run = gestor.fallar_paso(run, "s1_carga", msg)
            run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
            return _resultado_fallido(run, msg, time.time() - inicio_total)

        # ── PASO 2: Validación ───────────────────────────────
        paso = "s2_validacion"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(2, "Validación automática de calidad")
            run = gestor.iniciar_paso(run, paso)
            try:
                glosario = _cargar_glosario(config)
                informe_val = await validar_requisito(requisito, glosario, config)
                run.informe_validacion = informe_val
                score = informe_val.get("puntuacion_global", {}).get("valor", 0)
                veredicto = informe_val.get("veredicto_final", "")
                run = gestor.completar_paso(run, paso, {"score": score, "veredicto": veredicto})

                if veredicto == "BLOQUEADO":
                    _log_error(f"Score {score}/100 · BLOQUEADO")
                    _imprimir_problemas_bloqueantes(informe_val)
                    run = gestor.finalizar(run, EstadoEjecucion.VALIDACION_FALLIDA)
                    _generar_informe_validacion(run, config)
                    return _resultado_fallido(run, "Validación bloqueada.", time.time() - inicio_total)
                elif veredicto == "APROBADO_CON_ADVERTENCIAS":
                    _log_advertencia(f"Score {score}/100 · CON ADVERTENCIAS")
                    _imprimir_advertencias(informe_val)
                else:
                    _log_ok(f"Score {score}/100 · APROBADO")
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)
            glosario = _cargar_glosario(config)
            informe_val = run.informe_validacion

        # ── PASO 3: RAG ──────────────────────────────────────
        paso = "s3_rag_contexto"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(3, "Recuperando contexto del repositorio (RAG)")
            run = gestor.iniciar_paso(run, paso)
            try:
                contexto_rag = await recuperar_contexto_rag(requisito, glosario, config)
                run.artefactos_generados["contexto_rag"] = contexto_rag
                duplicados_criticos = [
                    d for d in contexto_rag.get("criterios_similares", [])
                    if d.get("similitud", 0) > config.similitud_duplicado_umbral
                ]
                if duplicados_criticos:
                    _log_advertencia(f"⚠ {len(duplicados_criticos)} posibles duplicados detectados")
                n_rel = len(contexto_rag.get("funcionalidad_similar", []))
                run = gestor.completar_paso(run, paso, {
                    "requisitos_relacionados": n_rel,
                    "duplicados_criticos": len(duplicados_criticos)
                })
                _log_ok(f"{n_rel} requisitos relacionados recuperados")
            except Exception as e:
                log.warning(f"  ⚠ RAG no disponible: {e}. Continuando sin contexto.")
                run.artefactos_generados["contexto_rag"] = {}
                run = gestor.omitir_paso(run, paso, f"RAG no disponible: {e}")
        else:
            _log_reanudado(paso)
            contexto_rag = run.artefactos_generados.get("contexto_rag", {})

        # ── PASO 4: Generación artefactos Jira ───────────────
        paso = "s4_generacion_artefactos"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(4, "Generando artefactos Jira con IA")
            run = gestor.iniciar_paso(run, paso)
            try:
                artefactos = await generar_artefactos_jira(
                    requisito, glosario, contexto_rag, config
                )
                run.artefactos_generados.update(artefactos)
                n_tareas = len(artefactos.get("tareas", []))
                n_ac = len(artefactos.get("historia", {}).get("acceptance_criteria", []))
                run = gestor.completar_paso(run, paso, {
                    "historia_generada": bool(artefactos.get("historia")),
                    "n_tareas": n_tareas,
                    "n_criterios_ac": n_ac
                })
                _log_ok(f"Historia · {n_tareas} tareas · {n_ac} criterios AC")
                for alerta in artefactos.get("historia", {}).get("alertas_calidad", []):
                    _log_advertencia(f"LLM: {alerta}")
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ── PASO 5: Generación test cases ────────────────────
        paso = "s5_generacion_test_cases"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(5, "Generando test cases")
            run = gestor.iniciar_paso(run, paso)
            try:
                test_cases = await generar_test_cases(
                    run.artefactos_generados.get("historia", {}), requisito, config
                )
                run.test_cases_generados = test_cases
                n_pos  = sum(1 for tc in test_cases if "positivo" in tc.get("tipo", ""))
                n_neg  = sum(1 for tc in test_cases if "negativo" in tc.get("tipo", ""))
                n_cont = sum(1 for tc in test_cases if "contorno" in tc.get("tipo", ""))
                run = gestor.completar_paso(run, paso, {
                    "total": len(test_cases), "positivos": n_pos,
                    "negativos": n_neg, "contorno": n_cont
                })
                _log_ok(f"{len(test_cases)} TCs ({n_pos} pos · {n_neg} neg · {n_cont} contorno)")
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ── PASO 6: Impacto de cambios ───────────────────────
        paso = "s6_analisis_impacto"
        version = requisito.get("version", "1.0")
        es_actualizacion = version != "1.0" and not version.endswith(".0") or \
                           float(version.split(".")[0]) > 1

        if not es_actualizacion:
            run = gestor.omitir_paso(run, paso, "Requisito nuevo.")
            _log_omitido(paso, "requisito nuevo")
        elif gestor.debe_ejecutar(run, paso):
            _log_paso(6, "Analizando impacto de cambios")
            run = gestor.iniciar_paso(run, paso)
            try:
                informe_impacto = await analizar_impacto_cambios(
                    requisito_id, requisito, config
                )
                run.informe_impacto = informe_impacto
                nivel = informe_impacto.get("informe_impacto", {}).get("nivel_urgencia", "?")
                n_afectados = informe_impacto.get("informe_impacto", {}).get(
                    "estadisticas", {}).get("total_artefactos_afectados", 0)
                run = gestor.completar_paso(run, paso, {
                    "nivel_urgencia": nivel, "artefactos_afectados": n_afectados
                })
                if nivel in ("CRITICO", "ALTO"):
                    _log_advertencia(f"Impacto {nivel}: {n_afectados} artefactos afectados")
                else:
                    _log_ok(f"Impacto {nivel}: {n_afectados} afectados")
            except Exception as e:
                log.warning(f"  ⚠ Análisis de impacto falló: {e}")
                run = gestor.omitir_paso(run, paso, f"Error: {e}")
        else:
            _log_reanudado(paso)

        # ── PASO 7: Trazabilidad ─────────────────────────────
        paso = "s7_registro_trazabilidad"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(7, "Registrando en el grafo de trazabilidad")
            run = gestor.iniciar_paso(run, paso)
            try:
                resultado_traz = await registrar_en_grafo(
                    requisito, run.artefactos_generados,
                    run.test_cases_generados or [], config
                )
                run = gestor.completar_paso(run, paso, resultado_traz)
                _log_ok(f"{resultado_traz.get('nodos_registrados', 0)} nodos · "
                        f"{resultado_traz.get('aristas_registradas', 0)} aristas")
            except Exception as e:
                log.warning(f"  ⚠ Trazabilidad falló: {e}")
                run = gestor.omitir_paso(run, paso, str(e))
        else:
            _log_reanudado(paso)

        # ── PASO 8: Aprobación ───────────────────────────────
        paso = "s8_aprobacion"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(8, "Solicitud de aprobación humana")
            run = gestor.iniciar_paso(run, paso)

            if config.dry_run:
                _log_ok("DRY-RUN: aprobación simulada.")
                run.artefactos_generados["aprobacion"] = {"decision": "aprobado_dry_run"}
                run = gestor.completar_paso(run, paso, {"decision": "dry_run"})
            elif not config.modo_interactivo:
                log.warning("  ⚠ Modo no-interactivo: aprobación automática.")
                run.artefactos_generados["aprobacion"] = {"decision": "aprobado_automatico"}
                run = gestor.completar_paso(run, paso, {"decision": "automatico"})
            else:
                decision = await solicitar_aprobacion(
                    run=run,
                    artefactos=run.artefactos_generados,
                    test_cases=run.test_cases_generados or [],
                    informe_validacion=run.informe_validacion,
                    informe_impacto=run.informe_impacto
                )
                if decision["decision"] == "rechazado":
                    run = gestor.fallar_paso(run, paso, f"Rechazado: {decision.get('motivo', '')}")
                    run = gestor.finalizar(run, EstadoEjecucion.RECHAZADO)
                    return _resultado_rechazado(run, decision, time.time() - inicio_total)
                if decision.get("artefactos_editados"):
                    run.artefactos_generados.update(decision["artefactos_editados"])
                    log.info("  ✓ Artefactos actualizados con ediciones")
                run.artefactos_generados["aprobacion"] = decision
                run = gestor.completar_paso(run, paso, {
                    "decision": decision["decision"],
                    "por": decision.get("analista", "desconocido")
                })
                _log_ok(f"Aprobado por {decision.get('analista', 'analista')}")
        else:
            _log_reanudado(paso)

        if config.dry_run:
            _generar_informe_completo(run, config)
            run = gestor.finalizar(run, EstadoEjecucion.COMPLETADO)
            return _resultado_exitoso(run, time.time() - inicio_total,
                                      "DRY-RUN completado. No se empujó a Jira.")

        # ── PASO 9: Push Jira ────────────────────────────────
        paso = "s9_push_jira"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(9, "Push a Jira")
            run = gestor.iniciar_paso(run, paso)
            try:
                resultado_jira = await push_a_jira(
                    run.artefactos_generados, requisito_id, config
                )
                run.resultado_jira = resultado_jira
                if not resultado_jira.get("exito"):
                    errores = resultado_jira.get("errores", [])
                    run = gestor.fallar_paso(run, paso, str(errores))
                    raise PipelineFallo(paso, str(errores))
                run = gestor.completar_paso(run, paso, {
                    "epica_key":   resultado_jira.get("epica_key"),
                    "historia_key": resultado_jira.get("historia_key"),
                    "tareas_keys": resultado_jira.get("tareas_keys", [])
                })
                _log_ok(f"Historia {resultado_jira.get('historia_key')} · "
                        f"{len(resultado_jira.get('tareas_keys', []))} tareas")
            except PipelineFallo:
                raise
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ── PASO 9B: Push Xray ───────────────────────────────
        paso = "s9b_push_xray"
        if not config.xray.activo:
            run = gestor.omitir_paso(run, paso, "Xray desactivado.")
            _log_omitido(paso, "Xray desactivado")
        elif gestor.debe_ejecutar(run, paso):
            _log_paso("9b", "Push test cases a Xray")
            run = gestor.iniciar_paso(run, paso)
            try:
                historia_key = run.resultado_jira.get("historia_key")
                resultado_xray = await push_a_xray(
                    run.test_cases_generados or [], historia_key, requisito_id, config
                )
                n_tc = resultado_xray.get("test_cases_creados", 0)
                run = gestor.completar_paso(run, paso, resultado_xray)
                _log_ok(f"{n_tc} test cases en Xray")
            except Exception as e:
                log.warning(f"  ⚠ Push Xray falló: {e}")
                run = gestor.omitir_paso(run, paso, str(e))
        else:
            _log_reanudado(paso)

        # ── FIN ──────────────────────────────────────────────
        duracion = time.time() - inicio_total
        _generar_informe_completo(run, config)
        run = gestor.finalizar(run, EstadoEjecucion.COMPLETADO)
        return _resultado_exitoso(run, duracion)

    except PipelineFallo as e:
        duracion = time.time() - inicio_total
        log.error(f"\n  ✗ Pipeline detenido en [{e.paso}]: {e.mensaje}")
        _generar_informe_completo(run, config)
        run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
        return _resultado_fallido(run, str(e), duracion)

    except Exception as e:
        duracion = time.time() - inicio_total
        log.exception(f"Error inesperado: {e}")
        run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
        return _resultado_fallido(run, str(e), duracion)


# ─────────────────────────────────────────────────────────────
# PIPELINE DE ÉPICA (lote)
# ─────────────────────────────────────────────────────────────

async def ejecutar_pipeline_epica(
    epica_id: str,
    config: PipelineConfig,
    gestor: GestorEstado,
    max_paralelo: int = 1
) -> dict:
    """Procesa todos los requisitos de una épica respetando dependencias."""
    print(f"\n{'═' * 56}")
    print(f"  ÉPICA → {epica_id}  (paralelo: {max_paralelo})")
    print(f"{'═' * 56}")

    requisitos = _descubrir_requisitos_epica(epica_id, config)
    if not requisitos:
        print(f"  ⚠ No se encontraron requisitos para {epica_id}")
        return {"exito": False, "error": "Sin requisitos"}

    print(f"  {len(requisitos)} requisitos encontrados")
    requisitos_ordenados = _ordenar_por_dependencias(requisitos, config)
    resultados = {}
    inicio = time.time()

    for i in range(0, len(requisitos_ordenados), max_paralelo):
        lote = requisitos_ordenados[i:i + max_paralelo]
        print(f"\n  Lote {i // max_paralelo + 1}: {[r['id'] for r in lote]}")
        tareas = [
            ejecutar_pipeline_requisito(req["id"], config, gestor)
            for req in lote
        ]
        resultados_lote = await asyncio.gather(*tareas, return_exceptions=True)
        for req, resultado in zip(lote, resultados_lote):
            resultados[req["id"]] = (
                {"exito": False, "error": str(resultado)}
                if isinstance(resultado, Exception) else resultado
            )
        if i + max_paralelo < len(requisitos_ordenados):
            await asyncio.sleep(3)

    duracion = time.time() - inicio
    exitosos = sum(1 for r in resultados.values() if r.get("exito"))
    fallidos = len(resultados) - exitosos

    print(f"\n{'═' * 56}")
    print(f"  RESUMEN ÉPICA {epica_id}")
    print(f"  Total: {len(resultados)} · ✓ {exitosos} · ✗ {fallidos}")
    print(f"  Tiempo total: {duracion:.1f}s")
    print(f"{'═' * 56}\n")

    return {
        "epica_id": epica_id, "exito": fallidos == 0,
        "total": len(resultados), "exitosos": exitosos,
        "fallidos": fallidos, "duracion_segundos": round(duracion, 1),
        "detalle": resultados
    }


# ─────────────────────────────────────────────────────────────
# UTILIDADES INTERNAS
# ─────────────────────────────────────────────────────────────

def _encontrar_yaml(req_id: str, config: PipelineConfig):
    for ruta in config.repo_requisitos.rglob(f"{req_id}.yaml"):
        return ruta
    for ruta in config.repo_requisitos.rglob("*.yaml"):
        try:
            contenido = yaml.safe_load(ruta.read_text())
            if contenido and contenido.get("id") == req_id:
                return ruta
        except Exception:
            continue
    return None

def _cargar_glosario(config: PipelineConfig) -> dict:
    with open(config.repo_glosario, encoding="utf-8") as f:
        return yaml.safe_load(f)

def _descubrir_requisitos_epica(epica_id: str, config: PipelineConfig) -> list:
    requisitos = []
    for ruta in config.repo_requisitos.rglob("*.yaml"):
        try:
            contenido = yaml.safe_load(ruta.read_text())
            if (contenido and contenido.get("epica") == epica_id and
                    contenido.get("estado") in ("en-revision", "validado")):
                requisitos.append(contenido)
        except Exception:
            continue
    return requisitos

def _ordenar_por_dependencias(requisitos: list, config) -> list:
    ids = {r["id"] for r in requisitos}
    ordenados = []
    visitados = set()

    def visitar(req):
        if req["id"] in visitados:
            return
        visitados.add(req["id"])
        for dep_id in req.get("dependencias", {}).get("requisitos", []):
            if dep_id in ids:
                dep = next((r for r in requisitos if r["id"] == dep_id), None)
                if dep:
                    visitar(dep)
        ordenados.append(req)

    for req in requisitos:
        visitar(req)
    return ordenados

def _resetear_desde_paso(run, desde_paso: str, gestor: GestorEstado):
    pasos = list(run.pasos.keys())
    if desde_paso not in pasos:
        log.warning(f"Paso '{desde_paso}' no reconocido.")
        return run
    desde_idx = pasos.index(desde_paso)
    for paso in pasos[desde_idx:]:
        run.pasos[paso]["estado"] = EstadoPaso.PENDIENTE
        run.pasos[paso]["resultado"] = None
        run.pasos[paso]["error"] = None
    gestor._persistir(run)
    return run

def _generar_informe_completo(run, config: PipelineConfig):
    ruta = config.carpeta_reports / f"{run.run_id}_report.md"
    pasos_ok   = sum(1 for p in run.pasos.values() if p.get("estado") == "completado")
    pasos_fail = sum(1 for p in run.pasos.values() if p.get("estado") == "fallido")
    duracion   = sum(p.get("duracion_segundos") or 0 for p in run.pasos.values())

    md = f"""# Informe de ejecución — {run.requisito_id}

**Run ID:** {run.run_id}
**Estado:** {run.estado}
**Inicio:** {run.inicio}
**Fin:** {run.fin or 'en curso'}
**Modo:** {'DRY-RUN' if run.dry_run else 'PRODUCCIÓN'}

## Resumen

| Métrica | Valor |
|---|---|
| Pasos completados | {pasos_ok} |
| Pasos fallidos | {pasos_fail} |
| Duración total | {duracion:.1f}s |

## Pasos del pipeline

| Paso | Estado | Duración | Resultado |
|---|---|---|---|
"""
    iconos = {"completado":"✅","fallido":"❌","omitido":"⏭","en_curso":"🔄","pendiente":"⏸"}
    for nombre, paso in run.pasos.items():
        estado = paso.get("estado", "pendiente")
        icono = iconos.get(estado, "?")
        dur = f"{paso.get('duracion_segundos', 0):.1f}s"
        res = str(paso.get("resultado", ""))[:80] if not paso.get("error") \
              else f"ERROR: {paso['error'][:80]}"
        md += f"| {nombre} | {icono} {estado} | {dur} | {res} |\n"

    if run.resultado_jira:
        md += f"""
## Artefactos en Jira

| Tipo | Key |
|---|---|
| Épica | {run.resultado_jira.get('epica_key', '—')} |
| Historia | {run.resultado_jira.get('historia_key', '—')} |
| Tareas | {', '.join(run.resultado_jira.get('tareas_keys', []))} |
"""
    if run.errores_globales:
        md += "\n## Errores\n" + "\n".join(f"- {e}" for e in run.errores_globales)
    if run.advertencias_globales:
        md += "\n## Advertencias\n" + "\n".join(f"- {a}" for a in run.advertencias_globales)

    ruta.write_text(md, encoding="utf-8")

def _generar_informe_validacion(run, config: PipelineConfig):
    if not run.informe_validacion:
        return
    ruta = config.carpeta_reports / f"{run.run_id}_validacion.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(run.informe_validacion, f, ensure_ascii=False, indent=2)
    log.info(f"  Informe de validación: {ruta}")

def _resultado_exitoso(run, duracion: float, nota: str = "") -> dict:
    historia_key = (run.resultado_jira or {}).get("historia_key")
    tareas = (run.resultado_jira or {}).get("tareas_keys", [])
    n_tc = len(run.test_cases_generados or [])
    print(f"\n  {'─' * 48}")
    print(f"  ✓ COMPLETADO en {duracion:.1f}s")
    if historia_key:
        print(f"    Historia:   {historia_key}")
        print(f"    Tareas:     {', '.join(tareas)}")
        print(f"    Test cases: {n_tc}")
    if nota:
        print(f"    Nota: {nota}")
    print(f"  {'─' * 48}\n")
    return {"exito": True, "requisito_id": run.requisito_id, "run_id": run.run_id,
            "historia_key": historia_key, "tareas_keys": tareas, "test_cases": n_tc,
            "duracion_segundos": round(duracion, 1), "dry_run": run.dry_run, "nota": nota}

def _resultado_fallido(run, error: str, duracion: float) -> dict:
    print(f"\n  {'─' * 48}")
    print(f"  ✗ FALLIDO en {duracion:.1f}s  —  {error[:120]}")
    print(f"  {'─' * 48}\n")
    return {"exito": False, "requisito_id": run.requisito_id, "run_id": run.run_id,
            "error": error, "duracion_segundos": round(duracion, 1)}

def _resultado_rechazado(run, decision: dict, duracion: float) -> dict:
    print(f"\n  {'─' * 48}")
    print(f"  ↩ RECHAZADO — {decision.get('motivo', 'no especificado')}")
    print(f"  {'─' * 48}\n")
    return {"exito": False, "requisito_id": run.requisito_id, "run_id": run.run_id,
            "estado": "rechazado", "motivo": decision.get("motivo"),
            "duracion_segundos": round(duracion, 1)}

def _log_paso(num, desc): print(f"\n  [{str(num):>2}] {desc}")
def _log_ok(msg):          print(f"       ✓ {msg}")
def _log_error(msg):       print(f"       ✗ {msg}")
def _log_advertencia(msg): print(f"       ⚠ {msg}")
def _log_reanudado(paso):  print(f"\n  [--] {paso} (ya completado, omitiendo)")
def _log_omitido(paso, m): print(f"\n  [⏭] {paso} omitido ({m})")
def _imprimir_problemas_bloqueantes(informe):
    for p in informe.get("problemas_por_prioridad", {}).get("bloqueantes", [])[:5]:
        print(f"       → [{p.get('campo','?')}] {p.get('problema','')[:80]}")
def _imprimir_advertencias(informe):
    for a in informe.get("problemas_por_prioridad", {}).get("advertencias", [])[:3]:
        print(f"       → [{a.get('campo','?')}] {a.get('problema','')[:80]}")


# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Orquestador del pipeline AI de análisis funcional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python orchestrator.py --req REQ-023
  python orchestrator.py --req REQ-023 --dry-run
  python orchestrator.py --epica EP-04 --paralelo 2
  python orchestrator.py --req REQ-023 --desde s4_generacion_artefactos
  python orchestrator.py --req REQ-023 --sin-aprobacion
        """
    )
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--req",   help="ID del requisito a procesar")
    grupo.add_argument("--epica", help="ID de épica (procesa todos sus requisitos)")
    parser.add_argument("--dry-run",        action="store_true")
    parser.add_argument("--sin-aprobacion", action="store_true")
    parser.add_argument("--desde",          metavar="PASO")
    parser.add_argument("--paralelo",       type=int, default=1, metavar="N")
    parser.add_argument("--verbose",        action="store_true")
    return parser.parse_args()


async def main():
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    config = PipelineConfig(
        dry_run=args.dry_run,
        modo_interactivo=not args.sin_aprobacion,
        max_paralelo=args.paralelo
    )

    errores_config = config.validar()
    if errores_config:
        print("\n✗ Errores de configuración:")
        for e in errores_config:
            print(f"  - {e}")
        sys.exit(1)

    gestor = GestorEstado(config.carpeta_runs)

    if args.req:
        resultado = await ejecutar_pipeline_requisito(
            args.req, config, gestor, forzar_desde=args.desde
        )
    else:
        resultado = await ejecutar_pipeline_epica(
            args.epica, config, gestor, max_paralelo=args.paralelo
        )

    sys.exit(0 if resultado.get("exito") else 1)


if __name__ == "__main__":
    asyncio.run(main())
