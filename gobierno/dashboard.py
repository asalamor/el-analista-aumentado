# gobierno/dashboard.py
"""
Dashboard semanal de métricas del pipeline AI funcional.
Genera el informe Markdown para el comité de gobierno.

Uso:
  python gobierno/dashboard.py --semana 2025-W20
  python gobierno/dashboard.py --semana 2025-W20 --output reports/dashboard.md
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Asegurar que el raíz del proyecto está en el path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PipelineConfig


# ─────────────────────────────────────────────────────────────
# OBTENCIÓN DE MÉTRICAS
# ─────────────────────────────────────────────────────────────

def obtener_metricas_semana(semana: str, config: PipelineConfig) -> dict:
    """
    Consulta las métricas de la semana desde la base de datos.
    Si la BD no está disponible, retorna datos de ejemplo con aviso.
    """
    try:
        import psycopg2
        db = psycopg2.connect(**config.db.to_dict())
        metricas = _consultar_metricas(db, semana)
        alertas  = _consultar_alertas_activas(db)
        tendencia = _consultar_tendencia(db)
        db.close()
        return {**metricas, "alertas_activas": alertas, "tendencia": tendencia}
    except Exception as e:
        print(f"  ⚠ BD no disponible ({e}). Usando datos de ejemplo.")
        return _metricas_ejemplo(semana)


def _consultar_metricas(db, semana: str) -> dict:
    with db.cursor() as cur:
        cur.execute("""
            SELECT
                AVG(tasa_aprobacion_directa)    AS tasa_aprobacion,
                AVG(ediciones_por_artefacto)    AS ediciones,
                AVG(score_calidad_requisito)    AS score_calidad,
                AVG(tiempo_ciclo_horas)         AS tiempo_ciclo,
                AVG(tiempo_procesamiento_seg)   AS tiempo_proc,
                COUNT(*)                        AS total_ejecuciones,
                SUM(CASE WHEN tasa_aprobacion_directa >= 0.8 THEN 1 ELSE 0 END)
                                                AS ejecuciones_ok
            FROM metricas_pipeline
            WHERE semana = %s
        """, (semana,))
        fila = cur.fetchone()

        # Campo más editado en la semana
        cur.execute("""
            SELECT campos_mas_editados
            FROM metricas_pipeline
            WHERE semana = %s AND campos_mas_editados IS NOT NULL
            LIMIT 10
        """, (semana,))
        registros_campos = cur.fetchall()

    if not fila or (fila[5] or 0) == 0:
        return _metricas_ejemplo(semana)

    # Agregar los campos más editados
    campo_top = "N/A"
    ediciones_top = 0
    contador_campos: dict = {}
    for (campos_json,) in registros_campos:
        if campos_json:
            for campo, freq in campos_json.items():
                contador_campos[campo] = contador_campos.get(campo, 0) + freq
    if contador_campos:
        campo_top = max(contador_campos, key=contador_campos.get)
        ediciones_top = contador_campos[campo_top]

    return {
        "semana": semana,
        "tasa_aprobacion_directa": round(float(fila[0] or 0), 2),
        "ediciones_por_artefacto": round(float(fila[1] or 0), 1),
        "score_calidad_medio":     round(float(fila[2] or 0), 1),
        "tiempo_ciclo_horas":      round(float(fila[3] or 0), 1),
        "tiempo_procesamiento_seg": round(float(fila[4] or 0), 1),
        "total_ejecuciones":       int(fila[5] or 0),
        "ejecuciones_ok":          int(fila[6] or 0),
        "campo_mas_editado":       campo_top,
        "ediciones_campo_top":     ediciones_top,
        "fuente": "base_de_datos"
    }


def _consultar_alertas_activas(db) -> list[str]:
    with db.cursor() as cur:
        cur.execute("""
            SELECT nombre_regla, descripcion
            FROM alertas_gobierno
            WHERE resuelto = FALSE
            ORDER BY fecha_alerta DESC
            LIMIT 5
        """)
        return [f"{f[0]}: {f[1]}" for f in cur.fetchall()]


def _consultar_tendencia(db) -> list[float]:
    """Retorna la tasa de aprobación de las últimas 4 semanas."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT semana, AVG(tasa_aprobacion_directa)
            FROM metricas_pipeline
            GROUP BY semana
            ORDER BY semana DESC
            LIMIT 4
        """)
        filas = cur.fetchall()
    return [round(float(f[1] or 0), 2) for f in reversed(filas)]


def _metricas_ejemplo(semana: str) -> dict:
    """Métricas de ejemplo cuando la BD no está disponible."""
    return {
        "semana": semana,
        "tasa_aprobacion_directa":  0.82,
        "ediciones_por_artefacto":  2.3,
        "score_calidad_medio":      79.5,
        "tiempo_ciclo_horas":       4.2,
        "tiempo_procesamiento_seg": 47.0,
        "total_ejecuciones":        12,
        "ejecuciones_ok":           10,
        "campo_mas_editado":        "criterios_aceptacion",
        "ediciones_campo_top":      8,
        "alertas_activas":          [],
        "tendencia":                [0.74, 0.78, 0.80, 0.82],
        "fuente": "ejemplo",
        "nota": "⚠ Datos de ejemplo — conectar la BD para métricas reales"
    }


# ─────────────────────────────────────────────────────────────
# GENERACIÓN DEL INFORME
# ─────────────────────────────────────────────────────────────

def formatear_dashboard(m: dict) -> str:
    """Genera el informe Markdown del dashboard semanal."""

    def semaforo(val, obj, invertido=False):
        if invertido:
            ok   = val <= obj * 1.1
            warn = val <= obj * 1.5
        else:
            ok   = val >= obj * 0.9
            warn = val >= obj * 0.7
        return "🟢" if ok else ("🟡" if warn else "🔴")

    tendencia = m.get("tendencia", [])
    tendencia_str = (
        " → ".join(f"{v:.0%}" for v in tendencia)
        if tendencia else "Sin datos"
    )

    alertas = m.get("alertas_activas", [])
    alertas_str = (
        "\n".join(f"- ⚠ {a}" for a in alertas)
        if alertas else "- Ninguna alerta activa"
    )

    nota = m.get("nota", "")
    nota_bloque = f"\n> {nota}\n" if nota else ""

    md = f"""# Dashboard de gobierno del pipeline — Semana {m['semana']}

**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Fuente de datos:** {m.get('fuente', 'desconocida')}
**Ejecuciones en el período:** {m.get('total_ejecuciones', 0)} \
({m.get('ejecuciones_ok', 0)} dentro de objetivo)
{nota_bloque}
---

## Métricas de calidad del output

| Métrica | Valor | Objetivo | Estado |
|---|---|---|---|
| Tasa aprobación directa | {m['tasa_aprobacion_directa']:.0%} | >80% | {semaforo(m['tasa_aprobacion_directa'], 0.80)} |
| Ediciones por artefacto | {m['ediciones_por_artefacto']:.1f} | <3 | {semaforo(m['ediciones_por_artefacto'], 3, invertido=True)} |
| Score calidad requisitos | {m['score_calidad_medio']:.0f}/100 | >75 | {semaforo(m['score_calidad_medio'], 75)} |
| Tiempo de ciclo | {m['tiempo_ciclo_horas']:.1f}h | <8h | {semaforo(m['tiempo_ciclo_horas'], 8, invertido=True)} |
| Tiempo procesamiento pipeline | {m.get('tiempo_procesamiento_seg', 0):.0f}s | <120s | {semaforo(m.get('tiempo_procesamiento_seg', 0), 120, invertido=True)} |

---

## Campo más editado esta semana

**{m.get('campo_mas_editado', 'N/A')}** \
({m.get('ediciones_campo_top', 0)} ediciones en el período)

> Si este campo lleva más de 2 semanas siendo el más editado, revisar
> si el prompt correspondiente necesita ajuste.

---

## Tendencia de aprobación (últimas 4 semanas)

{tendencia_str}

---

## Alertas activas

{alertas_str}

---

## Recomendaciones para el comité

"""
    # Generar recomendaciones automáticas basadas en las métricas
    recomendaciones = _generar_recomendaciones(m)
    for i, rec in enumerate(recomendaciones, 1):
        md += f"{i}. {rec}\n"

    md += f"""
---

## Próximos pasos

- [ ] Revisar las alertas activas y asignar responsable
- [ ] Evaluar si el campo más editado requiere ajuste de prompt
- [ ] Actualizar el glosario si han aparecido términos nuevos
- [ ] Confirmar fecha del próximo comité de gobierno

---

*Generado automáticamente por `gobierno/dashboard.py`*
"""
    return md


def _generar_recomendaciones(m: dict) -> list[str]:
    """Genera recomendaciones automáticas basadas en el estado de las métricas."""
    recs = []

    tasa = m.get("tasa_aprobacion_directa", 1.0)
    if tasa < 0.60:
        recs.append(
            f"🔴 **URGENTE**: La tasa de aprobación ({tasa:.0%}) está por debajo del "
            f"umbral crítico (60%). Revisar los últimos 10 rechazos e identificar "
            f"el patrón de fallo antes de la próxima sesión."
        )
    elif tasa < 0.80:
        recs.append(
            f"🟡 La tasa de aprobación ({tasa:.0%}) está por debajo del objetivo (80%). "
            f"Revisar si el campo más editado tiene un problema sistemático en el prompt."
        )

    score = m.get("score_calidad_medio", 100)
    if score < 65:
        recs.append(
            f"🔴 El score medio del repositorio ({score:.0f}/100) está en zona crítica. "
            f"Convocar sesión de recalibración con los analistas esta semana."
        )
    elif score < 75:
        recs.append(
            f"🟡 El score medio del repositorio ({score:.0f}/100) está por debajo del "
            f"objetivo (75). Revisar los requisitos con score <60 identificados en "
            f"la auditoría automática."
        )

    campo_top = m.get("campo_mas_editado", "")
    ediciones = m.get("ediciones_campo_top", 0)
    if ediciones > 5 and campo_top:
        recs.append(
            f"El campo **{campo_top}** ha sido editado {ediciones} veces esta semana. "
            f"Evaluar si el prompt que genera este campo necesita ajuste."
        )

    alertas = m.get("alertas_activas", [])
    if alertas:
        recs.append(
            f"Hay {len(alertas)} alerta(s) activa(s) sin resolver. "
            f"Asignar responsable y plazo de resolución."
        )

    if not recs:
        recs.append(
            "✅ Todas las métricas están dentro de los objetivos. "
            "Continuar con la cadencia habitual de revisión."
        )

    return recs


# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dashboard semanal de métricas del pipeline AI funcional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python gobierno/dashboard.py --semana 2025-W20
  python gobierno/dashboard.py --semana 2025-W20 --output reports/semana20.md
  python gobierno/dashboard.py --semana 2025-W20 --imprimir
        """
    )
    parser.add_argument(
        "--semana",
        required=True,
        help="Semana ISO (ej: 2025-W20)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Ruta del archivo de salida (por defecto: reports/dashboard_SEMANA.md)"
    )
    parser.add_argument(
        "--imprimir",
        action="store_true",
        help="Imprimir el informe en consola además de guardarlo"
    )
    args = parser.parse_args()

    config = PipelineConfig()
    metricas = obtener_metricas_semana(args.semana, config)
    informe  = formatear_dashboard(metricas)

    # Determinar ruta de salida
    ruta_output = Path(args.output) if args.output else \
                  Path(f"reports/dashboard_{args.semana}.md")
    ruta_output.parent.mkdir(parents=True, exist_ok=True)
    ruta_output.write_text(informe, encoding="utf-8")

    if args.imprimir:
        print(informe)

    print(f"\n✓ Dashboard generado: {ruta_output}")
    print(f"  Semana: {args.semana}")
    print(f"  Ejecuciones: {metricas.get('total_ejecuciones', 0)}")
    print(f"  Tasa aprobación: {metricas.get('tasa_aprobacion_directa', 0):.0%}")
    print(f"  Score calidad: {metricas.get('score_calidad_medio', 0):.0f}/100")


if __name__ == "__main__":
    main()
