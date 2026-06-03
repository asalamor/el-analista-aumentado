# Capítulo 14. Gobierno del modelo

---

Carlos lleva cuatro meses usando el pipeline. Los números son buenos: la tasa de aprobación directa supera el 83%, el tiempo de ciclo funcional se ha reducido a poco más de tres horas, y Lucía ya no tiene que preguntar al finalizar el sprint de dónde viene el test case que acaba de fallar en el entorno de preproducción. El sistema funciona.

Pero el lunes de la semana doce, algo falla de una forma que nadie esperaba. El pipeline genera una historia para REQ-039 —un nuevo requisito de conciliación de pagos— y la estimación automática sale disparada: trece puntos de historia para algo que el equipo sabe que es un trabajo de cuatro. En el refinamiento, David Sanz mira la pantalla con la misma cara que ponía antes de que existiera el pipeline. «Carlos, ¿está roto esto?»

Carlos revisa el prompt de generación de historias. No ha cambiado. Revisa el YAML de REQ-039. Está bien formado. Revisa el glosario. Correcto. Tarda cuarenta minutos en encontrar el origen del problema: el nuevo módulo de pagos introdujo el término «conciliación» en tres requisitos sin añadirlo al glosario. La IA, ante la incertidumbre terminológica, estimó conservadoramente hacia arriba.

El problema no estaba en la tecnología. Estaba en el gobierno.

---

## En este capítulo

- Por qué el pipeline se degrada silenciosamente si nadie lo gobierna, y cuáles son las señales de alerta que anuncian esa degradación antes de que sea visible en los artefactos.
- Los cinco pilares del sistema de gobierno: observabilidad, gestión de prompts, calidad del repositorio, estructura de decisión y gestión del riesgo.
- Cómo estructurar el comité mensual y las métricas semanales para que el gobierno sea una práctica ligera, no una burocracia.
- Las herramientas concretas que usa Meridian para mantener el sistema en buen estado doce meses después de la implantación.

---

## El problema de la degradación silenciosa

Un sistema de software tradicional falla de forma ruidosa: un error 500, una excepción en el log, un test que falla en CI. El pipeline de IA funciona al revés: puede producir output técnicamente correcto —JSON válido, sin errores de ejecución— que es funcionalmente incorrecto. Una historia que estima mal, un criterio de aceptación que es verificable en teoría pero no refleja la intención del negocio, un test case que cubre el flujo feliz pero ignora la excepción que más le importa al equipo de QA.

Este tipo de degradación es especialmente peligroso porque nadie la detecta de inmediato. Los artefactos llegan a Jira, el equipo los procesa, y el problema solo emerge semanas después en el sprint, cuando alguien implementa algo diferente a lo que el negocio necesitaba.

La degradación silenciosa tiene tres orígenes principales.

**El primero es la deriva del input.** Los requisitos que entran al pipeline hoy son distintos de los que entrenaron implícitamente los prompts durante las primeras semanas. Un nuevo módulo con vocabulario distinto, un analista nuevo que usa sinónimos no oficiales del glosario, una regla de negocio que se añadió sin el criterio de aceptación correspondiente. Los prompts no fallan; simplemente trabajan con un input diferente al que fueron optimizados.

**El segundo es el envejecimiento de los prompts.** Un prompt que hoy genera historias excelentes puede generar historias mediocres en seis meses sin que nadie lo haya modificado. El contexto del proyecto cambia: nuevos actores, nuevas reglas de negocio, un stack tecnológico actualizado. El prompt sigue haciendo lo mismo que siempre; lo que cambia es que «lo mismo» ya no es suficiente.

**El tercero es la fragmentación del glosario.** Como vio Carlos con «conciliación», el glosario solo tiene valor si está actualizado. Cada módulo nuevo introduce términos que el pipeline no conoce. Si nadie los añade al glosario, la IA rellena los huecos con su propio juicio, que rara vez coincide con el vocabulario que usa el equipo.

> 💡 **Idea clave**
>
> El pipeline no se rompe: se erosiona. La erosión es gradual, silenciosa y difícil de detectar sin un sistema de observabilidad activo. El gobierno existe para detectar esa erosión antes de que llegue al sprint.

---

## Los cinco pilares del sistema de gobierno

El sistema de gobierno de Meridian se articula en cinco pilares independientes. Cada uno responde a una pregunta distinta, se revisa con una cadencia distinta y tiene un responsable distinto.

| Pilar | Pregunta que responde | Cadencia |
|---|---|---|
| Observabilidad | ¿El sistema funciona como debería esta semana? | Semanal |
| Gestión de prompts | ¿Los prompts siguen siendo los mejores posibles? | Por demanda + mensual |
| Calidad del repositorio | ¿La materia prima del pipeline está en buen estado? | Quincenal |
| Estructura de decisión | ¿Quién decide qué y con qué autoridad? | Continuo |
| Gestión del riesgo | ¿Qué puede salir mal y cómo estamos preparados? | Trimestral |

No hace falta implantar los cinco pilares a la vez. En Meridian, el pillar de observabilidad llegó en el mes dos, la gestión de prompts en el mes cuatro —después del incidente de REQ-039— y la gestión del riesgo en el mes siete, cuando el sistema ya procesaba más de cien requisitos por sprint. La secuencia importa menos que la consistencia: cada pilar, una vez activado, debe revisarse sin excepciones.

---

## Pilar 1: Observabilidad

La observabilidad es el conjunto de métricas e indicadores que permiten saber, en cualquier momento, si el pipeline produce output de la calidad esperada. Sin observabilidad, el gobierno es reactivo: solo se detectan los problemas cuando alguien se queja. Con observabilidad, el gobierno es proactivo: los problemas se detectan antes de que impacten al sprint.

### Las métricas que importan

No todas las métricas tienen el mismo valor. Hay tres categorías: las que miden la calidad del output del pipeline, las que miden el impacto en el proceso del equipo, y las que miden la satisfacción de las personas que usan el sistema.

**Métricas de calidad del output** — se registran automáticamente en cada ejecución del pipeline:

| Métrica | Qué mide | Objetivo | Señal de alarma |
|---|---|---|---|
| Tasa de aprobación directa | % de JSONs aprobados sin ediciones por el analista | > 80% (mes 6), > 90% (mes 12) | Caída de más de 10 puntos en dos semanas |
| Tasa de rechazo | % de JSONs rechazados completamente | < 5% | > 10% en cualquier semana |
| Ediciones por artefacto | Número de campos que modifica el analista antes de aprobar | < 3 por historia | > 6 de media en una semana |
| Campos más editados | Qué campos modifica el analista con más frecuencia | Sin campo dominante | Un campo supera el 60% de las ediciones |
| Score de calidad del validador | Puntuación 0-100 asignada al requisito de entrada | Media > 75 en el repositorio | Media < 60 durante dos semanas consecutivas |

**Métricas de impacto en el proceso** — se miden semanalmente:

| Métrica | Qué mide | Objetivo | Señal de alarma |
|---|---|---|---|
| Tiempo de ciclo funcional | Horas desde la reunión de requisitos hasta las historias aprobadas en Jira | Reducción > 60% respecto a la línea base | Regresión de más de dos horas respecto al mes anterior |
| Tasa de cambio de alcance en sprint | % de historias con cambios de alcance una vez comprometidas | < 10% | > 20% en cualquier sprint |
| Cobertura de criterios de aceptación | % de historias con al menos dos criterios AC verificables | 100% | < 85% |
| Bugs por ambigüedad funcional | Bugs en producción cuya causa raíz es un requisito mal definido | Reducción > 40% en doce meses | Aumento del 30% respecto al mes anterior |

**Métricas de satisfacción** — encuesta trimestral al equipo, escala 1-5:

Los tres ítems que más predicen la adopción sostenida son:

1. «El pipeline reduce mi carga de trabajo en tareas repetitivas.»
2. «El output del pipeline representa bien la intención del requisito.»
3. «Recomendaría este sistema a un analista de otro proyecto.»

El objetivo es superar 4,0 en los tres ítems antes del noveno mes. Cuando la segunda pregunta baja por debajo de 3,5 y la primera se mantiene alta, el diagnóstico casi siempre es el mismo: el pipeline es rápido pero poco preciso. El prompt de generación de historias necesita ajuste.

### El dashboard semanal

Carlos dedica treinta minutos cada lunes a revisar las métricas de la semana anterior. No usa una herramienta sofisticada: un script Python lee los archivos de la carpeta `/reports/` del orquestador —los informes Markdown que se generan tras cada ejecución— y produce un resumen en formato tabla que se publica en el canal de Slack del equipo.

```python
# governance/dashboard.py
# Script semanal que agrega las métricas de los informes del pipeline
# y publica el dashboard en el canal de Slack del equipo

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class MetricasSemana:
    """
    Agrega las métricas de todos los runs de la semana.
    Se construye leyendo los archivos JSON de la carpeta /runs/.
    """
    # Período analizado
    semana: str = ""
    runs_procesados: int = 0

    # Métricas de calidad del output
    aprobaciones_directas: int = 0      # Aprobados sin ediciones
    rechazos: int = 0                   # Rechazados por el analista
    ediciones_totales: int = 0          # Total de campos editados
    campos_editados: dict = field(default_factory=dict)  # Campo → frecuencia

    # Métricas de tiempo
    tiempos_ciclo_horas: list = field(default_factory=list)
    tiempos_pipeline_segundos: list = field(default_factory=list)

    # Scores de validación
    scores_validacion: list = field(default_factory=list)

    @property
    def tasa_aprobacion_directa(self) -> float:
        """Porcentaje de runs aprobados sin ediciones."""
        total = self.aprobaciones_directas + self.rechazos
        if total == 0:
            return 0.0
        return self.aprobaciones_directas / total

    @property
    def ediciones_por_artefacto(self) -> float:
        """Media de campos editados por artefacto aprobado."""
        if self.aprobaciones_directas == 0:
            return 0.0
        return self.ediciones_totales / self.aprobaciones_directas

    @property
    def campo_mas_editado(self) -> tuple[str, int]:
        """Devuelve el campo que más se edita y su frecuencia."""
        if not self.campos_editados:
            return ("ninguno", 0)
        return max(self.campos_editados.items(), key=lambda x: x[1])

    @property
    def score_calidad_medio(self) -> float:
        """Score medio de calidad de los requisitos procesados."""
        if not self.scores_validacion:
            return 0.0
        return sum(self.scores_validacion) / len(self.scores_validacion)


def leer_metricas_semana(carpeta_runs: Path) -> MetricasSemana:
    """
    Lee todos los archivos JSON de la carpeta /runs/ de la última semana
    y construye el objeto de métricas agregadas.
    """
    hace_una_semana = datetime.now() - timedelta(days=7)
    metricas = MetricasSemana(
        semana=datetime.now().strftime("%Y-W%W")
    )

    for archivo in carpeta_runs.glob("*.json"):
        # Leer solo los runs de la última semana
        try:
            with open(archivo) as f:
                run = json.load(f)

            inicio = datetime.fromisoformat(run.get("inicio", ""))
            if inicio < hace_una_semana:
                continue

            metricas.runs_procesados += 1

            # Registrar resultado de la aprobación
            aprobacion = run.get("artefactos_generados", {}).get("aprobacion", {})
            decision = aprobacion.get("decision", "")

            if decision in ("aprobado", "aprobado_dry_run"):
                metricas.aprobaciones_directas += 1

                # Contar ediciones realizadas por el analista
                editados = aprobacion.get("campos_editados", [])
                metricas.ediciones_totales += len(editados)
                for campo in editados:
                    metricas.campos_editados[campo] = (
                        metricas.campos_editados.get(campo, 0) + 1
                    )

            elif decision == "rechazado":
                metricas.rechazos += 1

            # Registrar score de validación
            score = (
                run.get("informe_validacion", {})
                .get("puntuacion_global", {})
                .get("valor", 0)
            )
            if score > 0:
                metricas.scores_validacion.append(score)

            # Registrar tiempo de ciclo si está disponible
            tiempo_ciclo = run.get("tiempo_ciclo_horas")
            if tiempo_ciclo:
                metricas.tiempos_ciclo_horas.append(tiempo_ciclo)

        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    return metricas


def formatear_semaforo(valor: float, objetivo: float, invertido: bool = False) -> str:
    """
    Devuelve un emoji de semáforo según si el valor cumple el objetivo.
    invertido=True para métricas donde menor es mejor (tiempos, errores).
    """
    if invertido:
        ok = valor <= objetivo * 1.1
        warn = valor <= objetivo * 1.5
    else:
        ok = valor >= objetivo * 0.9
        warn = valor >= objetivo * 0.7

    return "🟢" if ok else "🟡" if warn else "🔴"


def generar_dashboard_markdown(metricas: MetricasSemana) -> str:
    """
    Genera el dashboard semanal en Markdown para publicar en Confluence
    o enviar al canal de Slack del equipo.
    """
    campo_top, freq_top = metricas.campo_mas_editado

    return f"""
## Dashboard de gobierno — {metricas.semana}

**Runs procesados esta semana:** {metricas.runs_procesados}

### Calidad del output

| Métrica | Valor | Objetivo | Estado |
|---|---|---|---|
| Tasa de aprobación directa | {metricas.tasa_aprobacion_directa:.0%} | > 80% | {formatear_semaforo(metricas.tasa_aprobacion_directa, 0.80)} |
| Ediciones por artefacto | {metricas.ediciones_por_artefacto:.1f} | < 3 | {formatear_semaforo(metricas.ediciones_por_artefacto, 3, invertido=True)} |
| Score medio del validador | {metricas.score_calidad_medio:.0f}/100 | > 75 | {formatear_semaforo(metricas.score_calidad_medio, 75)} |

### Campo más editado esta semana

**{campo_top}** ({freq_top} ediciones)

> Si un campo concentra más del 60% de las ediciones, revisar el prompt
> que genera ese campo. Es la señal más directa de que el prompt necesita ajuste.
""".strip()
```

> 🛠️ **En la práctica**
>
> El campo más editado es el indicador de gobierno más accionable del dashboard. En Meridian, durante el mes tres, «story_points» concentraba el 71% de las ediciones: Carlos siempre ajustaba la estimación hacia abajo. La investigación reveló que el prompt usaba como criterio de referencia proyectos de mayor complejidad que los propios de Meridian. Tres líneas añadidas al prompt resolvieron el problema en una semana.

---

## Pilar 2: Gestión de prompts

Los prompts son el código del pipeline. Como todo código, necesitan mantenimiento: se quedan obsoletos cuando cambia el contexto, se degradan cuando el input evoluciona y mejorar cuando el equipo aprende qué funciona mejor. Gestionarlos con el mismo rigor que el código fuente es lo que garantiza que el sistema evoluciona de forma controlada en lugar de degradarse silenciosamente.

### El repositorio de prompts

Cada prompt del pipeline vive en el repositorio Git del proyecto, bajo la carpeta `/pipeline/prompts/`, versionado igual que el código. La estructura es:

```
pipeline/
├── prompts/
│   ├── v1.0/                       ← primera versión en producción
│   │   ├── system_base.txt
│   │   ├── p1_epica.txt
│   │   ├── p2_historia.txt
│   │   ├── p3_tareas.txt
│   │   └── ...
│   ├── v1.1/                       ← versión actual en producción
│   │   └── ...
│   └── draft/                      ← versión en desarrollo, no en producción
│       └── ...
│
├── tests/
│   ├── dataset_evaluacion/         ← 20 requisitos de referencia fijos
│   │   ├── REQ-TEST-001.yaml       ← requisito de prueba
│   │   ├── REQ-TEST-001.expected.json  ← output esperado
│   │   └── ...
│   └── evaluar_prompts.py          ← script de comparación entre versiones
│
└── changelog_prompts.md            ← historial de cambios con fecha y motivo
```

El dataset de evaluación es la pieza más importante de este repositorio. Son veinte requisitos representativos del proyecto, elegidos para cubrir los casos más frecuentes y los más problemáticos. Este dataset nunca cambia: es la referencia estable contra la que se mide cualquier propuesta de cambio de prompt.

### El proceso de cambio en cuatro pasos

Ningún prompt cambia en producción sin pasar por este proceso. La regla es que un cambio de prompt es equivalente a un cambio de código: necesita revisión, prueba y aprobación.

**Paso 1 — Proponer.** Cualquier miembro del equipo puede proponer un cambio abriendo una incidencia en el proyecto Jira del pipeline con el prefijo `[PROMPT]`. La propuesta debe incluir qué campo genera el problema, qué salida se obtiene actualmente y qué salida debería obtenerse. Sin estos tres elementos, la propuesta se devuelve al autor.

**Paso 2 — Evaluar.** El champion ejecuta el script `evaluar_prompts.py` que compara el output del prompt actual y del propuesto sobre los veinte requisitos del dataset. El script calcula un score de similitud campo a campo entre el output generado y el output esperado, y produce un informe comparativo con mejoras, regresiones y veredicto automático.

```python
# governance/evaluar_prompts.py
# Compara dos versiones de prompt sobre el dataset de referencia.
# Uso: python evaluar_prompts.py --actual v1.1 --propuesta draft

import argparse
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ResultadoComparacion:
    """
    Resultado de comparar dos versiones de prompt sobre el dataset.
    Producido por comparar_versiones() y usado en el informe.
    """
    version_actual: str
    version_propuesta: str
    score_actual: float          # Score medio sobre el dataset (0–100)
    score_propuesto: float       # Score medio de la versión propuesta
    mejoras: list[str]           # IDs de requisitos donde mejora
    regresiones: list[str]       # IDs de requisitos donde empeora
    sin_cambio: list[str]        # IDs sin diferencia significativa

    @property
    def veredicto(self) -> str:
        """
        Veredicto automático para orientar la decisión humana.
        No es vinculante: el champion y el comité deciden siempre.
        """
        if len(self.regresiones) > len(self.mejoras):
            return "RECOMENDAR_RECHAZO"
        if self.score_propuesto < self.score_actual:
            return "RECOMENDAR_RECHAZO"
        if len(self.mejoras) >= len(self.regresiones) * 2:
            return "RECOMENDAR_APROBACION"
        return "REQUIERE_REVISION_HUMANA"

    def a_markdown(self) -> str:
        """Formatea el resultado como Markdown para el informe de decisión."""
        return f"""
## Evaluación de cambio de prompt

| | Versión actual ({self.version_actual}) | Versión propuesta ({self.version_propuesta}) |
|---|---|---|
| Score medio | {self.score_actual:.1f}/100 | {self.score_propuesto:.1f}/100 |
| Mejoras | — | {len(self.mejoras)} requisitos |
| Regresiones | — | {len(self.regresiones)} requisitos |

**Veredicto automático:** `{self.veredicto}`

> El veredicto automático orienta la decisión pero no la reemplaza.
> El champion y el comité de gobierno aprueban todos los cambios.

### Casos de regresión (revisar antes de decidir)

{chr(10).join(f"- {r}" for r in self.regresiones) or "Ninguno."}
""".strip()
```

**Paso 3 — Decidir.** El champion presenta el informe en el comité mensual (o asíncronamente por Slack si el cambio es urgente y de bajo riesgo). La decisión es sencilla: aprobar, rechazar o posponer con fecha.

**Paso 4 — Documentar y desplegar.** Si se aprueba, el champion actualiza el `changelog_prompts.md` con el motivo del cambio, el before y after y las métricas que mejora. El despliegue es simplemente mover los archivos de la carpeta `draft/` a la carpeta con el número de versión siguiente.

### El changelog de prompts

Un ejemplo del `changelog_prompts.md` de Meridian:

```markdown
## v1.2.0 — 2025-06-09

**Tipo de cambio:** Mejora del prompt de generación de historias (p2_historia.txt)
**Aprobado por:** Carlos Ruiz (champion)
**Motivo:** El campo «story_points» se editaba en el 71% de los artefactos del mes 3.
El análisis de los rechazos mostró que el prompt usaba como referencia proyectos
de mayor complejidad que los de Meridian. Los criterios de estimación Fibonacci
se recalibraron para el tamaño de historias real del equipo.

**Resultado de la evaluación:**
- Score medio en dataset: 81 → 88
- Regresiones: ninguna
- Mejoras: 14 de los 20 requisitos del dataset

---

## v1.1.0 — 2025-05-15 (incidente REQ-039)

**Tipo de cambio:** Corrección del vocabulario de módulo nuevo
**Aprobado por:** Carlos Ruiz (champion)
**Motivo:** El término «conciliación» apareció en tres requisitos del módulo de pagos
sin estar en el glosario. El pipeline estimó REQ-039 con 13 story points.
Tras añadir «conciliación» al glosario (acción 1) y ajustar el system prompt
para indicar que un campo terminológico desconocido debe marcarse como
[PENDIENTE: definición en glosario] en lugar de inferir (acción 2), la estimación
se normalizó.

**Resultado:** REQ-039 re-procesado con score 79 y estimación de 5 story points.
```

> ⚠️ **Error frecuente**
>
> Cambiar el prompt de generación cuando el problema real está en el input. Si el campo más editado es «criterios_aceptacion», el primer diagnóstico debe ser: ¿los requisitos que entran tienen criterios AC bien escritos? Si el score del validador está cayendo, el problema está en la plantilla o en el glosario, no en el prompt. Cambiar el prompt para compensar input deficiente es un parche que crea más ruido a medio plazo.

---

## Pilar 3: Calidad del repositorio

El repositorio de requisitos es la materia prima del pipeline. Si la materia prima se degrada, el output se degrada con ella, aunque los prompts sean perfectos. El mantenimiento del repositorio tiene tres dimensiones: el glosario, la calidad de los requisitos existentes, y la arquitectura de archivos.

### Auditoría quincenal del glosario

El glosario necesita dos tipos de revisión: una revisión de contenido (¿están todos los términos actualizados?) y una revisión de cobertura (¿hay términos nuevos en los requisitos recientes que no están en el glosario?).

Para la revisión de cobertura, el pipeline ya tiene el mecanismo del Cap. 10: cuando el validador de consistencia detecta un término no oficial en un requisito, lo registra. Agregar esas detecciones en una lista semanal es suficiente para tener un backlog de términos candidatos al glosario.

La revisión de contenido es manual y tarda menos de lo que parece: veinte minutos cada dos sprints, revisando los términos que han aparecido en las conversaciones recientes y comparándolos con las definiciones del glosario. El propietario del glosario —el analista líder en Meridian— es el único que puede aprobar cambios, pero cualquier miembro del equipo puede proponer términos nuevos a través de una incidencia Jira con el prefijo `[GLOSARIO]`.

La métrica de madurez del glosario más directa es la tasa de detección de sinónimos no oficiales: el porcentaje de requisitos en los que el validador detecta al menos un término fuera del glosario. Al inicio de un proyecto es normal que sea alta (30–50%). Debe caer por debajo del 10% tras dos meses de uso activo del glosario.

### Auditoría quincenal del repositorio

Una vez cada dos semanas, un script recorre todos los requisitos en estado `validado` o `en-revision` y ejecuta el validador de calidad sobre cada uno. El resultado es un informe que lista los requisitos con score por debajo de 60, agrupados por campo problemático.

```python
# governance/auditoria_repositorio.py
# Ejecuta el validador sobre todos los requisitos del repositorio
# y genera un informe de estado de calidad.
# Se recomienda ejecutar cada dos semanas vía cron o CI.

import yaml
from pathlib import Path
from datetime import datetime


def auditar_repositorio(ruta_requisitos: Path, validador) -> dict:
    """
    Recorre todos los YAMLs del repositorio, ejecuta el validador
    sobre los que están en estado procesable, y agrega los resultados.

    Retorna un diccionario con:
    - total de requisitos auditados
    - score medio del repositorio
    - lista de requisitos que necesitan revisión urgente (score < 60)
    - tabla de campos más problemáticos por frecuencia
    """
    resultados = {
        "fecha_auditoria": datetime.now().isoformat(),
        "total_auditados": 0,
        "score_medio": 0,
        "requisitos_a_revisar": [],
        "campos_mas_problematicos": {}
    }

    scores = []

    # Recorrer recursivamente todos los archivos YAML del repositorio
    for ruta in ruta_requisitos.rglob("*.yaml"):
        try:
            with open(ruta) as f:
                req = yaml.safe_load(f)

            # Solo auditar requisitos en estados procesables
            if req.get("estado") not in ("validado", "en-revision"):
                continue

            resultados["total_auditados"] += 1

            # Ejecutar el validador completo del Cap. 7
            informe = validador.ejecutar_completo(req)
            score = informe.get("puntuacion_global", {}).get("valor", 0)
            scores.append(score)

            # Agregar problemas por campo para identificar patrones
            for problema in informe.get("todos_los_problemas", []):
                campo = problema.get("campo", "desconocido")
                resultados["campos_mas_problematicos"][campo] = (
                    resultados["campos_mas_problematicos"].get(campo, 0) + 1
                )

            # Marcar como urgente si el score es muy bajo
            if score < 60:
                resultados["requisitos_a_revisar"].append({
                    "id": req.get("id"),
                    "score": score,
                    "epica": req.get("epica"),
                    "analista": req.get("analista", "no especificado"),
                    "urgencia": "alta" if score < 40 else "media"
                })

        except Exception:
            # Un YAML mal formado no detiene la auditoría
            continue

    # Calcular score medio del repositorio
    if scores:
        resultados["score_medio"] = round(sum(scores) / len(scores), 1)

    # Ordenar los campos por frecuencia de problema
    resultados["campos_mas_problematicos"] = dict(
        sorted(
            resultados["campos_mas_problematicos"].items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    # Ordenar los requisitos a revisar por urgencia y score
    resultados["requisitos_a_revisar"].sort(key=lambda x: x["score"])

    return resultados
```

El informe que produce esta auditoría tiene tres secciones accionables: los requisitos con score por debajo de 60 que necesitan revisión antes del próximo refinamiento, los cinco campos que más problemas acumulan en el repositorio completo, y el score medio del repositorio como indicador de tendencia.

Si el score medio cae por debajo de 70 durante dos semanas consecutivas, es señal de que el equipo ha relajado la adherencia a la plantilla. En Meridian, ese escenario se resolvió con una sesión de recalibración de cuarenta y cinco minutos en la que Carlos mostró tres ejemplos reales del repositorio y el equipo acordó qué nivel de detalle era aceptable.

---

## Pilar 4: Estructura de decisión

El gobierno necesita una estructura clara de quién decide qué y con qué autoridad. Sin ella, las decisiones se demoran porque nadie sabe si tiene autorización para tomarlas, o se toman sin el nivel correcto de contexto porque quien las toma no tiene toda la información.

### Los cuatro roles del sistema de gobierno

**El champion** es el analista más experimentado con el sistema. En Meridian es Carlos. Su responsabilidad operativa incluye revisar las métricas semanales, responder las dudas del equipo en menos de cuatro horas laborables, mantener actualizado el glosario junto con el propietario, preparar la agenda del comité mensual, y proponer y evaluar cambios de prompts. Dedica entre tres y cuatro horas semanales al gobierno del sistema. Puede aprobar cambios de prompts de bajo riesgo (correcciones ortográficas, ajustes de estilo) sin necesidad de escalarlos al comité.

**El responsable técnico** es quien construyó el pipeline. Aprueba los cambios de prompts de alto riesgo, mantiene la infraestructura, resuelve incidencias técnicas y evoluciona la arquitectura cuando es necesario. En régimen de crucero —después del mes seis— dedica entre dos y tres horas semanales al sistema. Puede pausar el pipeline en producción si detecta un problema grave; el comité lo valida a posteriori.

**El propietario del glosario** es el analista líder funcional. Tiene la decisión final sobre el vocabulario del proyecto: qué términos son oficiales, qué sinónimos no son aceptables, y qué definiciones prevalecen cuando hay discrepancias entre módulos. Revisa el glosario cada dos sprints y convoca las sesiones de alineación terminológica con el negocio cuando un módulo nuevo lo requiere.

**El comité de gobierno** es el órgano de máxima autoridad del sistema. Está formado por el champion, el responsable técnico, el analista líder y el product owner. Se reúne una vez al mes durante cuarenta y cinco minutos. Tiene autoridad para aprobar cambios de proceso, decidir sobre la evolución del roadmap y resolver conflictos entre calidad y velocidad que no pueden resolverse en el nivel operativo.

### La matriz de decisión

Esta tabla elimina la ambigüedad sobre quién aprueba cada tipo de decisión:

| Tipo de decisión | Champion | Resp. técnico | Comité |
|---|---|---|---|
| Corrección menor en un prompt | ✓ Solo | | |
| Mejora de un campo específico en el prompt | ✓ Propone | ✓ Aprueba | |
| Cambio en la lógica de validación | ✓ Propone | ✓ Aprueba | |
| Nuevo tipo de artefacto en el pipeline | ✓ Propone | ✓ Revisa | ✓ Aprueba |
| Cambio en el proceso de aprobación humana | ✓ Propone | ✓ Revisa | ✓ Aprueba |
| Pausa del pipeline en producción | | ✓ Puede pausar | ✓ Valida a posteriori |
| Cambio de modelo LLM | ✓ Propone | ✓ Evalúa | ✓ Aprueba |
| Nuevo término en el glosario | Propietario del glosario | | |
| Cambio de definición en el glosario | Propietario + negocio | | |

### La reunión mensual del comité

La reunión tiene un guión fijo de cuarenta y cinco minutos. No es negociable: si no hay guión, la reunión deriva en conversaciones abiertas que consumen tiempo sin producir decisiones.

```
AGENDA FIJA — Comité de gobierno del pipeline
Primer lunes de cada mes, 45 minutos

[00:00 – 00:10] Revisión de métricas del mes
El champion presenta el dashboard mensual en tres diapositivas:
tendencia de la tasa de aprobación directa, campo más editado del mes,
y bugs por ambigüedad en producción. Foco en tendencias,
no en valores puntuales.
Pregunta clave: ¿qué ha mejorado y qué ha empeorado respecto al mes anterior?

[00:10 – 00:20] Revisión de incidencias abiertas
Incidencias etiquetadas [PIPELINE] o [GLOSARIO] en Jira.
Clasificar en tres grupos: resueltas (informar brevemente),
en progreso (actualizar estado), pendientes de decisión del comité
(son el único punto de debate real de esta sección).

[00:20 – 00:30] Propuestas de cambio pendientes
El champion presenta las propuestas que necesitan aprobación del comité.
Cada propuesta tiene máximo tres minutos: problema detectado,
cambio propuesto, resultado de la evaluación sobre el dataset.
Decisión inmediata: aprobar, rechazar o posponer con fecha.

[00:30 – 00:40] Tema de fondo (rotativo mensualmente)
Mes 1: evolución del glosario
Mes 2: calidad del repositorio (informe de auditoría)
Mes 3: satisfacción del equipo (encuesta trimestral)
Mes 4: revisión de los quince problemas más frecuentes del validador
Mes 5: métricas de impacto en producción (bugs, cambios de alcance)
Mes 6: balance semestral y ajuste de objetivos

[00:40 – 00:45] Acuerdos y próximos pasos
Exactamente tres frases:
1. Qué se ha decidido hoy.
2. Quién hace qué antes de la próxima reunión.
3. Qué tema de fondo corresponde el mes que viene.
```

> 🛠️ **En la práctica**
>
> En Meridian, los primeros dos meses el comité tardaba más de una hora porque el debate se abría sin estructura. El cambio que marcó la diferencia fue simple: el champion manda las métricas del mes por Slack el viernes anterior a la reunión. Cuando el equipo llega ya ha procesado los números y puede ir directamente a las decisiones. El tiempo promedio de reunión cayó de setenta minutos a treinta y ocho.

---

## Pilar 5: Gestión del riesgo

El gobierno necesita anticipar qué puede salir mal y tener respuestas preparadas antes de que ocurra. No para eliminar los riesgos —muchos son inevitables— sino para que cuando se materialicen, el equipo sepa exactamente qué hacer sin improvisar bajo presión.

### Los cinco riesgos principales

Estos son los riesgos que más probabilidad tienen de materializarse en organizaciones como Meridian, ordenados por impacto potencial sobre el proceso de análisis.

**Riesgo 1 — Degradación silenciosa del output (probabilidad alta, impacto alto)**

Es el riesgo que se ha descrito al inicio del capítulo. El output del pipeline cae de calidad gradualmente sin que nadie lo detecte porque el deterioro es incremental.

Señales tempranas: aumento gradual de las ediciones por artefacto durante dos semanas consecutivas, comentarios informales del tipo «el pipeline últimamente no da tanto» en las retros, aumento del tiempo en la cola de aprobación.

Mitigación preventiva: el dashboard semanal con alertas automáticas, el dataset de evaluación fijo para detectar regresiones, la auditoría quincenal del repositorio.

Plan de contingencia: si la tasa de aprobación directa cae por debajo del 60%, el responsable técnico activa el rollback al prompt anterior y convoca al comité en modo urgente en cuarenta y ocho horas. El pipeline continúa en modo asistido —genera artefactos pero no los empuja a Jira automáticamente— hasta que se resuelva la causa raíz.

**Riesgo 2 — Pérdida del champion (probabilidad media, impacto alto)**

Carlos deja el proyecto o la organización y el conocimiento del sistema queda concentrado en una sola persona.

Señales tempranas: el champion anuncia su salida o un período de baja prolongado, reasignación a otro proyecto con carga completa.

Mitigación preventiva: todo el conocimiento del sistema debe vivir en Confluence y en el `changelog_prompts.md`, no en la cabeza del champion. Desde el mes cuatro, el responsable técnico o el analista líder debe participar en todas las revisiones semanales como observador activo. No como sustituto: como redundancia.

Plan de contingencia: si el champion deja el proyecto, el responsable técnico asume temporalmente el rol operativo durante el primer mes de transición y dedica cinco horas semanales al sistema en lugar de dos. El comité revisa la documentación y la actualiza si hay huecos.

**Riesgo 3 — Dependencia de un único proveedor de LLM (probabilidad media, impacto alto)**

El pipeline depende de la API de Claude. Un corte de servicio, un cambio de precios significativo o la deprecación del modelo de referencia puede paralizar el pipeline sin aviso.

Señales tempranas: comunicaciones del proveedor sobre deprecación de modelos, aumento de latencia o de tasa de errores en las llamadas a la API, cambios en los términos de servicio.

Mitigación preventiva: el cliente LLM del orquestador está diseñado desde el Cap. 12 como capa intercambiable. La variable de entorno `LLM_PROVIDER` permite cambiar a GPT-4o sin modificar los prompts. Mantener acceso activo a al menos un proveedor alternativo, incluso si no se usa habitualmente.

Plan de contingencia: si el proveedor principal no está disponible, cambiar `LLM_PROVIDER` al alternativo, ejecutar el dataset de evaluación para verificar que la calidad es aceptable (umbral: score medio > 70), y notificar al equipo del cambio temporal. Si la calidad del alternativo es inferior al umbral, el equipo continúa creando artefactos manualmente hasta resolver el problema con el proveedor principal.

**Riesgo 4 — Rechazo del equipo por sobrecarga percibida (probabilidad media, impacto medio)**

Los analistas perciben que el nuevo proceso exige más trabajo del que ahorra, especialmente en las primeras semanas, y empiezan a evitar el pipeline sin comunicarlo abiertamente.

Señales tempranas: frecuencia de uso del pipeline por debajo del 70% de los requisitos del período, analistas que crean issues en Jira manualmente sin pasar por el pipeline, puntaciones de satisfacción por debajo de 3,5 en la encuesta trimestral.

Mitigación preventiva: medir el tiempo antes y después con datos objetivos para poder rebatir la percepción con hechos. Sesión mensual de feedback donde los analistas pueden proponer simplificaciones a la plantilla. Eliminar cualquier campo que no aporte valor demostrable al output.

Plan de contingencia: si la frecuencia de uso cae por debajo del 70%, el champion convoca entrevistas individuales con los analistas que evitan el sistema para identificar los tres principales puntos de fricción. Los cambios acordados se implementan en menos de dos semanas.

**Riesgo 5 — Artefacto incorrecto en producción sin detección (probabilidad baja, impacto alto)**

Un artefacto generado con errores pasa el gate de aprobación humana, llega a Jira, el equipo lo implementa, y el bug llega a producción. En Meridian, el escenario más probable no es un error técnico del pipeline sino un criterio de aceptación ambiguo que el analista aprobó sin cuestionar.

Señales tempranas: bug en producción cuya causa raíz es un criterio AC que no describía el comportamiento real esperado, historia implementada de forma diferente a lo que el negocio entendía.

Mitigación preventiva: el checklist de revisión del analista antes de aprobar (heredado del Cap. 7), la sesión de refinamiento como segunda barrera de detección, los criterios de aceptación leídos en voz alta en el sprint planning.

Plan de contingencia: cuando se detecta un artefacto incorrecto que llegó a producción, abrir una incidencia `[PIPELINE-FALLO]` con el requisito origen, analizar si el fallo fue del prompt o del gate de aprobación humana, documentar el caso en el dataset de evaluación para que no se repita, y ajustar el checklist de revisión si el patrón de fallo es nuevo.

> 💡 **Idea clave**
>
> El catálogo de riesgos no es un ejercicio teórico. Debe revisarse una vez por trimestre en el comité de gobierno, actualizando la probabilidad y el plan de contingencia según lo que haya ocurrido en los meses anteriores. Un riesgo que se materializa y se gestiona correctamente pasa a tener probabilidad baja en el trimestre siguiente: el equipo ya sabe qué hacer.

---

## El modelo de madurez del gobierno

El gobierno no se implanta de golpe. Evoluciona en paralelo con las fases de adopción del capítulo anterior. Intentar poner en marcha los cinco pilares desde el primer día genera burocracia sin valor: el equipo no tiene suficientes datos para que las métricas sean significativas, los prompts son demasiado nuevos para necesitar versionado formal, y el repositorio tiene tan pocos requisitos que la auditoría no detecta nada.

La secuencia que funciona en la práctica es esta:

**Meses 1–3 (Gobierno mínimo viable).** Solo el champion revisa las métricas básicas cada semana: tasa de aprobación directa y campo más editado. No hay comité formal. El responsable técnico resuelve los problemas técnicos según aparecen. El glosario se actualiza informalmente. El objetivo de esta fase es que el sistema funcione, no que esté perfectamente gobernado.

**Meses 4–6 (Gobierno estructurado).** Se activa el comité mensual con el guión fijo. El dashboard de métricas está operativo. El proceso de cambio de prompts está documentado, aunque a veces se salta algún paso. La auditoría del repositorio se hace manualmente cada dos semanas. En Meridian, esta fase empezó justo después del incidente de REQ-039.

**Meses 7–9 (Gobierno automatizado).** Las alertas automáticas del dashboard están activas. La auditoría del repositorio es automática. El evaluador de prompts corre automáticamente sobre cada propuesta de cambio. El comité mensual tiene datos objetivos para todas sus decisiones.

**Mes 10 en adelante (Gobierno maduro).** El sistema se gobierna casi solo: las alertas detectan los problemas, el evaluador valida los cambios, el comité decide sobre los casos excepcionales. El tiempo de gobierno del champion baja de cuatro horas semanales a dos. El responsable técnico interviene solo cuando hay cambios de arquitectura.

> 🛠️ **En la práctica**
>
> Meridian llegó al gobierno maduro en el mes once, no en el diez. El retraso fue positivo: el equipo llegó a esa fase con confianza real en el sistema porque había gestionado dos incidentes —el de REQ-039 y uno menor relacionado con una actualización del modelo de Claude— sin que ninguno llegara a impactar a producción. La confianza en el sistema de gobierno se construye gestionando incidentes reales, no solo leyendo la documentación.

---

## Meridian doce meses después

Ha pasado un año desde que Carlos instaló el pipeline en un martes por la tarde. El equipo de análisis de Meridian ha procesado más de cuatrocientos requisitos. La tasa de aprobación directa se mantiene en el 88%. El score medio del repositorio es 82. Los bugs por ambigüedad funcional cayeron un 47% respecto al año anterior.

Pero los números no son lo que más le importa a Carlos. Lo que más le importa es lo que ocurrió en la última retrospectiva del equipo.

María García, la desarrolladora que hace un año preguntó si la IA iba a reemplazarlos, dijo algo que Carlos anotó en su cuaderno: «Antes el refinamiento era la reunión que más temía. Llegabas con historias llenas de preguntas que nadie había respondido. Ahora llego con historias que ya tienen respuestas y me dedico a las preguntas que realmente importan.»

Lucía añadió que sus casos de prueba antes de implementar ya cubrían el 70% de lo que encontraba después. Ana López, que al principio miraba con escepticismo las preguntas estructuradas que Carlos le hacía en los workshops, admitió que las reuniones habían pasado de ser una extracción de información a ser una conversación real sobre el problema de negocio.

Y David Sanz cerró la retro con la frase que resume mejor lo que ha cambiado en Meridian: «Antes el pipeline era la herramienta de Carlos. Ahora es parte de cómo trabajamos.»

Ese es el objetivo real del gobierno del modelo. No mantener el pipeline funcionando: hacer que el equipo no pueda imaginar trabajar sin él.

---

## Lo que funciona en la práctica

**El gobierno ligero es mejor que el gobierno perfecto.** Intentar implantarlo todo desde el principio garantiza que no se implante nada de forma sostenida. El comité mensual de cuarenta y cinco minutos con guión fijo aporta más valor que una reunión mensual de dos horas sin estructura.

**Las métricas importan solo si alguien actúa sobre ellas.** Un dashboard que nadie lee es un generador de falsa seguridad. En Meridian, el acuerdo explícito fue este: si el campo más editado supera el 60% de las ediciones durante dos semanas consecutivas, el champion propone un cambio de prompt esa semana, no en la siguiente reunión de gobierno.

**El champion necesita apoyo visible de la dirección.** No apoyo retórico: apoyo concreto en forma de tiempo protegido. Si el champion no tiene esas tres o cuatro horas semanales garantizadas, el gobierno colapsa en el mes tres cuando el proyecto entra en período de alta presión.

**El incidente bien gestionado fortalece el sistema.** Cada vez que el equipo detecta un problema, activa el proceso de contingencia y lo resuelve sin que llegue al sprint, la confianza en el sistema aumenta. Los equipos que evitan los incidentes —que no los registran o que los resuelven informalmente sin documentar— pierden la oportunidad de fortalecer el sistema y repetirán el mismo error.

**El glosario es la inversión con mayor retorno.** De los cinco pilares, el mantenimiento del glosario es el que más impacto tiene sobre la calidad del output con menor coste de mantenimiento. Veinte minutos cada dos semanas para revisar los términos nuevos del repositorio es la práctica de gobierno de mayor ROI que tiene el sistema.

---

## Tres puntos clave

1. El pipeline no se rompe: se erosiona silenciosamente cuando el input cambia, los prompts envejecen o el glosario se fragmenta. El sistema de gobierno existe para detectar esa erosión antes de que llegue al sprint.

2. Los cinco pilares del gobierno son observabilidad, gestión de prompts, calidad del repositorio, estructura de decisión y gestión del riesgo. No se implantan a la vez: la secuencia importa, y el gobierno mínimo viable de los primeros meses es suficiente para que el sistema no se degrade mientras madura.

3. El objetivo del gobierno no es mantener el pipeline funcionando. Es hacer que el equipo no pueda imaginar trabajar sin él.

---

## Pregunta de reflexión para el equipo

Piensa en los últimos cinco requisitos que procesaste con el pipeline. ¿Hubo algún campo que editaste siempre antes de aprobar? Si la respuesta es sí, ese campo es el primer candidato a un ajuste de prompt. ¿Tienes un proceso para proponer ese ajuste, evaluarlo y desplegarlo de forma controlada?

---

*El capítulo siguiente aborda la medición del impacto y el retorno sobre la inversión: cómo traducir las métricas técnicas del pipeline en el lenguaje de la dirección, y cómo construir el argumento de negocio que justifica la inversión a largo plazo.*
