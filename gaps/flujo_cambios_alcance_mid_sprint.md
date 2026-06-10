# Flujo de gestión de cambios de alcance mid-sprint

> **Contexto del modelo operativo:** Este documento desarrolla uno de los puntos pendientes identificados al cierre del modelo operativo. Se integra con los componentes ya construidos: el motor de detección de impacto de cambios (punto 8), el grafo de trazabilidad (punto 9), la integración con Jira API (punto 10) y el pipeline de validación (punto 6).

---

## El problema que resuelve

En el flujo estándar del modelo, los cambios en un requisito validado activan el analizador de impacto (punto 8), que identifica artefactos afectados y genera un plan de acción. Pero ese analizador asume que el cambio ocurre **antes** de que el equipo haya empezado a trabajar sobre los artefactos afectados.

El escenario mid-sprint es distinto y más delicado: el negocio solicita un cambio **mientras una historia está en desarrollo activo**. Hay un desarrollador que ya tomó decisiones de implementación basadas en los criterios de aceptación anteriores. Hay test cases que el QA puede estar ejecutando en este momento. El sprint tiene una fecha de cierre comprometida.

Un cambio de alcance mal gestionado en este punto genera cuatro problemas simultáneos:

- El desarrollador trabaja sobre una versión del requisito que ya no es la correcta, sin saberlo.
- El QA ejecuta pruebas contra criterios que han cambiado.
- El sprint planning queda invalidado porque el esfuerzo estimado ya no corresponde al alcance real.
- La trazabilidad se rompe: el código entregado no corresponde a los criterios de aceptación documentados.

El flujo descrito en este punto gestiona exactamente ese escenario, con tres objetivos: **detectar el cambio antes de que se materialice el daño**, **cuantificar el impacto sobre el sprint en curso** y **presentar al Product Owner opciones concretas con sus consecuencias**, no una petición de decisión sin contexto.

---

## Taxonomía de cambios mid-sprint

No todos los cambios tienen el misma urgencia ni el mismo tratamiento. La primera clasificación que hace el sistema es por **tipo de cambio** y por **momento del ciclo de desarrollo** en que se detecta.

### Por tipo de cambio

**Tipo 1 — Restricción nueva o modificación de regla de negocio.**
Ejemplo: el rango máximo de filtrado de facturas pasa de 365 días a 90 días. El comportamiento esperado cambia. El código ya implementado puede ser incorrecto. Los test cases que verificaban el límite de 365 días son ahora inválidos.

**Tipo 2 — Ampliación de alcance.**
Ejemplo: además del filtrado por fecha, el negocio quiere también filtrado por estado de factura en la misma historia. El alcance crece. La estimación original ya no es válida. Puede que la historia deba partirse.

**Tipo 3 — Reducción de alcance.**
Ejemplo: se elimina el requisito de mostrar el contador de resultados. El alcance se reduce. El trabajo ya hecho puede ser aprovechable o no. Los test cases asociados a esa funcionalidad quedan obsoletos.

**Tipo 4 — Cambio de actor o permisos.**
Ejemplo: la funcionalidad que se pensaba para el Gestor de facturación debe estar también disponible para el Responsable financiero. El impacto técnico puede ser significativo si la autorización está implementada a nivel de rol.

**Tipo 5 — Cambio de datos de interfaz.**
Ejemplo: el campo `fecha_inicio` pasa de ser obligatorio a opcional, con valor por defecto igual a la fecha de inicio del ejercicio fiscal. El frontend, el backend y los test cases están afectados.

### Por momento del ciclo de desarrollo

| Momento | Estado del issue en Jira | Riesgo | Tratamiento |
|---|---|---|---|
| Historia comprometida, desarrollo no iniciado | To Do / Backlog del sprint | Bajo | Actualizar historia y regenerar artefactos antes de que empiece |
| Desarrollo iniciado, sin código en revisión | In Progress | Medio | Notificación inmediata al desarrollador + decisión del PO |
| Código en revisión (PR abierto) | In Review | Alto | Bloquear el merge hasta que se resuelva el alcance |
| Historia en QA | In Testing | Muy alto | Parar la ejecución de tests + reabrir la historia |
| Historia marcada como hecha | Done | Crítico | Reabrir la historia + análisis de regresión |

---

## Arquitectura del flujo

El flujo tiene seis fases en cadena. Las fases 1 y 2 son automáticas. Las fases 3 y 4 requieren intervención humana. Las fases 5 y 6 son de nuevo automáticas condicionadas a la decisión humana.

```
Solicitud de cambio detectada
          │
          ▼
[Fase 1] Clasificación automática del cambio
          │
          ▼
[Fase 2] Cálculo de impacto sobre el sprint
          │
          ▼
[Fase 3] Presentación de opciones al Product Owner
          │
          ▼
[Fase 4] Decisión humana
          │
          ├──── Opción A: Aceptar en sprint actual
          │              │
          │              ▼
          │     [Fase 5A] Actualización de artefactos
          │              + notificación al equipo
          │
          ├──── Opción B: Posponer al siguiente sprint
          │              │
          │              ▼
          │     [Fase 5B] Congelación del alcance actual
          │              + creación de deuda técnica documentada
          │
          └──── Opción C: Partir la historia
                         │
                         ▼
                [Fase 5C] Split de historia
                         + redistribución de artefactos
                         │
                         ▼
                [Fase 6] Actualización del grafo de trazabilidad
                         + notificaciones automáticas al equipo
```

---

## Fase 1 — Clasificación automática del cambio

El punto de entrada es el mismo webhook que usa el motor de impacto del punto 8: cuando el analista modifica el YAML de un requisito cuya historia tiene issues en el sprint activo, el sistema activa este flujo en lugar del flujo estándar de detección de impacto.

```python
# mid_sprint_change_detector.py

from dataclasses import dataclass
from typing import Optional
import yaml
from datetime import datetime


@dataclass
class CambioMidSprint:
    requisito_id: str
    historia_jira_key: str
    estado_historia: str           # To Do │ In Progress │ In Review │ In Testing │ Done
    desarrollador_asignado: str
    sprint_id: str
    sprint_nombre: str
    sprint_fecha_cierre: str       # ISO-8601
    dias_restantes_sprint: int
    tipo_cambio: str               # Tipo 1..5 de la taxonomía
    severidad: str                 # bloqueante │ alta │ media │ baja
    campo_modificado: str
    valor_anterior: any
    valor_nuevo: any
    descripcion_cambio: str
    artefactos_afectados: dict     # {test_cases: [...], tareas: [...]}
    esfuerzo_adicional_estimado_h: Optional[float]


class DetectorCambioMidSprint:
    """
    Detecta si un cambio en un requisito afecta a una historia
    que está actualmente en desarrollo activo (sprint en curso).
    Punto de entrada del flujo mid-sprint.
    """

    TIPOS_CAMBIO_POR_CAMPO = {
        # Tipo 1 — Restricción / regla de negocio
        "criterios_aceptacion":  (1, "bloqueante"),
        "reglas_negocio":        (1, "alta"),
        "excepciones":           (1, "alta"),
        "flujo_principal":       (1, "bloqueante"),
        "flujos_alternativos":   (1, "alta"),
        # Tipo 2/3 — Cambio de alcance
        "descripcion":           (2, "media"),
        "objetivo_negocio":      (2, "baja"),
        "datos_salida":          (2, "alta"),
        # Tipo 4 — Actor / permisos
        "actor":                 (4, "alta"),
        "actores_secundarios":   (4, "media"),
        # Tipo 5 — Datos de interfaz
        "datos_entrada":         (5, "alta"),
    }

    def __init__(self, cliente_jira, motor_trazabilidad):
        self.jira = cliente_jira
        self.trazabilidad = motor_trazabilidad

    def evaluar(
        self,
        requisito_id: str,
        campo_modificado: str,
        valor_anterior,
        valor_nuevo,
        yaml_nuevo: dict
    ) -> Optional[CambioMidSprint]:
        """
        Evalúa si el cambio afecta a una historia en el sprint activo.
        Retorna el objeto CambioMidSprint si el cambio requiere
        tratamiento mid-sprint, None si no hay historia activa afectada.
        """

        # Buscar historia en sprint activo derivada de este requisito
        historia = self._buscar_historia_en_sprint_activo(requisito_id)
        if not historia:
            return None  # No hay historia activa: flujo estándar

        tipo, severidad = self.TIPOS_CAMBIO_POR_CAMPO.get(
            campo_modificado, (2, "baja")
        )

        # Calcular días restantes en el sprint
        sprint = historia["sprint"]
        fecha_cierre = datetime.fromisoformat(
            sprint.get("endDate", datetime.now().isoformat())
        )
        dias_restantes = max(0, (fecha_cierre - datetime.now()).days)

        # Identificar artefactos afectados en el sprint
        artefactos = self._identificar_artefactos_afectados(
            historia["key"], campo_modificado, valor_anterior, valor_nuevo
        )

        # Estimar esfuerzo adicional según tipo de cambio
        esfuerzo_adicional = self._estimar_esfuerzo_adicional(
            tipo, artefactos, yaml_nuevo
        )

        descripcion = self._describir_cambio(
            campo_modificado, valor_anterior, valor_nuevo
        )

        return CambioMidSprint(
            requisito_id=requisito_id,
            historia_jira_key=historia["key"],
            estado_historia=historia["fields"]["status"]["name"],
            desarrollador_asignado=(
                historia["fields"].get("assignee", {}) or {}
            ).get("displayName", "Sin asignar"),
            sprint_id=sprint.get("id", ""),
            sprint_nombre=sprint.get("name", ""),
            sprint_fecha_cierre=sprint.get("endDate", ""),
            dias_restantes_sprint=dias_restantes,
            tipo_cambio=f"Tipo {tipo}",
            severidad=severidad,
            campo_modificado=campo_modificado,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            descripcion_cambio=descripcion,
            artefactos_afectados=artefactos,
            esfuerzo_adicional_estimado_h=esfuerzo_adicional
        )

    def _buscar_historia_en_sprint_activo(
        self, requisito_id: str
    ) -> Optional[dict]:
        """Consulta Jira para encontrar la historia del requisito en sprint activo."""
        resultado = self.jira.get(
            "search",
            params={
                "jql": (
                    f"project = {self.jira.config.project_key} "
                    f"AND sprint in openSprints() "
                    f"AND issuetype = Story "
                    f"AND '{self.jira.config.campo_requisito_origen}' ~ '{requisito_id}'"
                ),
                "fields": (
                    "summary,status,assignee,sprint,"
                    "customfield_10016,subtasks"  # story_points, subtasks
                ),
                "maxResults": 1
            }
        )
        issues = resultado.get("issues", [])
        if not issues:
            return None
        historia = issues[0]
        # Extraer sprint del campo customfield
        sprints = historia["fields"].get("customfield_10020", [])
        if sprints:
            historia["sprint"] = sprints[-1]
        else:
            return None
        return historia

    def _identificar_artefactos_afectados(
        self,
        historia_key: str,
        campo: str,
        anterior,
        nuevo
    ) -> dict:
        """
        Identifica qué artefactos concretos del sprint están afectados.
        Consulta el grafo de trazabilidad para máxima precisión.
        """
        afectados = {
            "test_cases_invalidos": [],
            "test_cases_a_regenerar": [],
            "tareas_a_revisar": [],
            "subtareas_en_curso": []
        }

        # Test cases que verifican criterios afectados
        if campo in ("criterios_aceptacion", "reglas_negocio", "excepciones"):
            with self.trazabilidad.db.cursor() as cur:
                cur.execute("""
                    SELECT n_tc.id, n_tc.titulo, n_tc.estado, n_tc.metadatos
                    FROM nodos_trazabilidad n_tc
                    JOIN aristas_trazabilidad a ON a.origen_id = n_tc.id
                        AND a.tipo_relacion = 'verifica'
                    JOIN nodos_trazabilidad n_us ON n_us.id = a.destino_id
                    WHERE n_us.id = %s
                      AND n_tc.tipo = 'test_case'
                      AND n_tc.activo = TRUE
                """, (historia_key,))
                for tc_id, titulo, estado, meta in cur.fetchall():
                    if estado in ("en_ejecucion", "fallido"):
                        afectados["test_cases_invalidos"].append({
                            "id": tc_id,
                            "titulo": titulo,
                            "estado": estado
                        })
                    else:
                        afectados["test_cases_a_regenerar"].append({
                            "id": tc_id,
                            "titulo": titulo,
                            "estado": estado
                        })

        # Tareas técnicas afectadas
        if campo in ("datos_entrada", "datos_salida", "actor"):
            with self.trazabilidad.db.cursor() as cur:
                cur.execute("""
                    SELECT n_tk.id, n_tk.titulo, n_tk.estado, n_tk.metadatos
                    FROM nodos_trazabilidad n_tk
                    JOIN aristas_trazabilidad a ON a.origen_id = n_tk.id
                        AND a.tipo_relacion = 'descompone'
                    JOIN nodos_trazabilidad n_us ON n_us.id = a.destino_id
                    WHERE n_us.id = %s
                      AND n_tk.tipo IN ('tarea', 'subtarea')
                      AND n_tk.activo = TRUE
                """, (historia_key,))
                for tk_id, titulo, estado, meta in cur.fetchall():
                    if estado in ("In Progress", "In Review"):
                        afectados["subtareas_en_curso"].append({
                            "id": tk_id,
                            "titulo": titulo,
                            "estado": estado,
                            "capa": (meta or {}).get("capa", "")
                        })
                    else:
                        afectados["tareas_a_revisar"].append({
                            "id": tk_id,
                            "titulo": titulo,
                            "estado": estado,
                            "capa": (meta or {}).get("capa", "")
                        })

        return afectados

    def _estimar_esfuerzo_adicional(
        self,
        tipo: int,
        artefactos: dict,
        yaml_nuevo: dict
    ) -> float:
        """
        Estimación heurística del esfuerzo adicional en horas.
        No pretende ser precisa; sirve para que el PO tome
        una decisión informada, no para el sprint planning.
        """
        horas = 0.0
        # Coste de regenerar test cases
        horas += len(artefactos["test_cases_a_regenerar"]) * 0.5
        # Coste de rehacer código en tareas en curso
        horas += len(artefactos["subtareas_en_curso"]) * 2.0
        # Coste base por tipo de cambio
        coste_base = {1: 4.0, 2: 6.0, 3: 1.0, 4: 5.0, 5: 3.0}
        horas += coste_base.get(tipo, 2.0)
        return round(horas, 1)

    def _describir_cambio(self, campo: str, anterior, nuevo) -> str:
        if campo == "criterios_aceptacion":
            ids_ant = {ac["id"] for ac in (anterior or [])}
            ids_nue = {ac["id"] for ac in (nuevo or [])}
            mod = ids_ant & ids_nue - {
                ac["id"] for ac in (nuevo or [])
                if ac == next((a for a in (anterior or []) if a["id"] == ac["id"]), None)
            }
            partes = []
            if ids_nue - ids_ant:
                partes.append(f"Criterios añadidos: {', '.join(ids_nue - ids_ant)}")
            if ids_ant - ids_nue:
                partes.append(f"Criterios eliminados: {', '.join(ids_ant - ids_nue)}")
            if mod:
                partes.append(f"Criterios modificados: {', '.join(mod)}")
            return ". ".join(partes) or "Cambio en criterios de aceptación"
        if campo == "actor":
            return f"Actor cambia de '{anterior}' a '{nuevo}'"
        if campo == "reglas_negocio":
            return f"Reglas de negocio modificadas en {len(nuevo or [])} items"
        if campo == "datos_entrada":
            return "Estructura de datos de entrada modificada"
        return f"Campo '{campo}' modificado"
```

---

## Fase 2 — Cálculo de impacto sobre el sprint

Con el cambio clasificado, el sistema calcula si el sprint puede absorber el cambio o si la fecha de cierre está en riesgo. El cálculo combina el esfuerzo adicional estimado, la capacidad restante del sprint y el estado actual de las tareas afectadas.

```python
# mid_sprint_impact_calculator.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class ImpactoSprint:
    historia_key: str
    sprint_nombre: str
    dias_restantes: int
    capacidad_restante_h: float     # Horas laborables estimadas hasta cierre
    esfuerzo_adicional_h: float     # Del CambioMidSprint
    deficit_h: float                # esfuerzo_adicional - capacidad_restante
    puede_absorber: bool            # True si capacidad_restante > esfuerzo_adicional
    nivel_riesgo: str               # verde │ amarillo │ rojo
    opciones_disponibles: list[str] # Opciones que el sistema presenta al PO
    contexto_sprint: dict           # Velocidad del equipo, issues completados, etc.


class CalculadorImpactoSprint:
    """
    Calcula si el sprint puede absorber un cambio mid-sprint
    y qué opciones tiene el Product Owner.
    """

    # Factor de capacidad: no todas las horas del sprint son productivas.
    # Se asume un 70% de eficiencia para absorber trabajo no planificado.
    FACTOR_CAPACIDAD = 0.70

    def __init__(self, cliente_jira):
        self.jira = cliente_jira

    def calcular(self, cambio: "CambioMidSprint") -> ImpactoSprint:

        # Obtener métricas del sprint activo
        contexto = self._obtener_contexto_sprint(
            cambio.sprint_id, cambio.historia_jira_key
        )

        # Capacidad restante estimada
        horas_por_dia = 6.0  # Horas productivas por día de sprint
        capacidad_bruta = cambio.dias_restantes * horas_por_dia
        capacidad_restante = capacidad_bruta * self.FACTOR_CAPACIDAD

        deficit = cambio.esfuerzo_adicional_estimado_h - capacidad_restante

        puede_absorber = deficit <= 0

        # Nivel de riesgo combinando capacidad y estado del desarrollo
        nivel_riesgo = self._calcular_nivel_riesgo(
            cambio, puede_absorber, deficit, contexto
        )

        # Opciones disponibles según el análisis
        opciones = self._calcular_opciones_disponibles(
            cambio, puede_absorber, nivel_riesgo, contexto
        )

        return ImpactoSprint(
            historia_key=cambio.historia_jira_key,
            sprint_nombre=cambio.sprint_nombre,
            dias_restantes=cambio.dias_restantes,
            capacidad_restante_h=round(capacidad_restante, 1),
            esfuerzo_adicional_h=cambio.esfuerzo_adicional_estimado_h,
            deficit_h=round(deficit, 1),
            puede_absorber=puede_absorber,
            nivel_riesgo=nivel_riesgo,
            opciones_disponibles=opciones,
            contexto_sprint=contexto
        )

    def _obtener_contexto_sprint(
        self, sprint_id: str, historia_key: str
    ) -> dict:
        """Recopila métricas del sprint para enriquecer la decisión."""

        # Issues del sprint y sus estados
        resultado = self.jira.get(
            "search",
            params={
                "jql": (
                    f"project = {self.jira.config.project_key} "
                    f"AND sprint = {sprint_id}"
                ),
                "fields": "summary,status,issuetype,story_points",
                "maxResults": 50
            }
        )
        issues = resultado.get("issues", [])

        total = len(issues)
        completados = sum(
            1 for i in issues
            if i["fields"]["status"]["statusCategory"]["key"] == "done"
        )
        en_progreso = sum(
            1 for i in issues
            if i["fields"]["status"]["name"] in ("In Progress", "In Review")
        )

        return {
            "total_issues_sprint": total,
            "issues_completados": completados,
            "issues_en_progreso": en_progreso,
            "issues_pendientes": total - completados - en_progreso,
            "porcentaje_completado": round(
                completados / total * 100 if total else 0
            ),
            "historia_es_unica_en_progreso": en_progreso == 1
        }

    def _calcular_nivel_riesgo(
        self,
        cambio: "CambioMidSprint",
        puede_absorber: bool,
        deficit: float,
        contexto: dict
    ) -> str:
        """
        Verde: el cambio cabe en el sprint sin impacto en la entrega.
        Amarillo: el cambio es posible pero comprime el margen del sprint.
        Rojo: el cambio no cabe o el estado del desarrollo lo hace inviable.
        """
        # Siempre rojo si hay código en revisión o en QA con el cambio afectando tests
        if cambio.estado_historia in ("In Review", "In Testing"):
            if cambio.artefactos_afectados.get("test_cases_invalidos"):
                return "rojo"

        # Rojo si no puede absorber y el déficit supera el 50% de la capacidad
        if not puede_absorber and abs(deficit) > cambio.dias_restantes * 3:
            return "rojo"

        # Rojo si queda menos de 2 días y hay tareas en curso afectadas
        if (cambio.dias_restantes <= 2 and
                cambio.artefactos_afectados.get("subtareas_en_curso")):
            return "rojo"

        # Amarillo si puede absorber pero el margen es ajustado
        if puede_absorber and deficit > -4:
            return "amarillo"

        # Amarillo si el sprint ya tiene alta carga
        if contexto.get("porcentaje_completado", 0) < 30 and not puede_absorber:
            return "amarillo"

        return "verde" if puede_absorber else "rojo"

    def _calcular_opciones_disponibles(
        self,
        cambio: "CambioMidSprint",
        puede_absorber: bool,
        nivel_riesgo: str,
        contexto: dict
    ) -> list[str]:
        """
        Las opciones que se presentarán al PO dependen del estado
        del desarrollo y del nivel de riesgo calculado.
        """
        opciones = []

        # Opción A: siempre disponible si el cambio no afecta código en curso
        if cambio.estado_historia not in ("In Review", "In Testing", "Done"):
            if puede_absorber or nivel_riesgo != "rojo":
                opciones.append("A")  # Aceptar en sprint actual

        # Opción B: siempre disponible
        opciones.append("B")  # Posponer al siguiente sprint

        # Opción C: disponible cuando el cambio supone una ampliación de alcance
        if cambio.tipo_cambio in ("Tipo 2", "Tipo 1"):
            opciones.append("C")  # Partir la historia

        # Opción D: solo si la historia está en Done (reabrir)
        if cambio.estado_historia == "Done":
            opciones.append("D")  # Reabrir historia y regresar al sprint

        return opciones
```

---

## Fase 3 — Presentación de opciones al Product Owner

El sistema genera un informe estructurado que el Product Owner recibe por el canal configurado (Slack, Teams, email) y que contiene toda la información necesaria para tomar la decisión en menos de cinco minutos. No es un alerta genérico: es un documento de decisión con las consecuencias de cada opción ya calculadas.

```python
# mid_sprint_po_briefing.py

import json
from dataclasses import dataclass


@dataclass
class BriefingPO:
    """
    Documento de decisión que se entrega al Product Owner.
    Diseñado para ser legible en menos de 5 minutos.
    """
    id_solicitud: str
    urgencia: str               # inmediata │ hoy │ antes_de_manana
    resumen_ejecutivo: str      # 3 frases máximo
    cambio: dict                # Resumen del cambio
    impacto: dict               # Resumen del impacto en el sprint
    opciones: list[dict]        # Cada opción con sus consecuencias
    recomendacion_sistema: str  # La opción que el sistema recomienda
    pregunta_clave: str         # La pregunta concreta que debe responder el PO
    plazo_decision: str         # Cuándo se necesita la decisión


class GeneradorBriefingPO:
    """
    Genera el documento de decisión para el Product Owner
    usando el LLM para la parte narrativa y cálculos
    deterministas para las consecuencias de cada opción.
    """

    PLANTILLAS_OPCIONES = {
        "A": {
            "titulo": "Aceptar el cambio en el sprint actual",
            "cuando_aplicar": (
                "Cuando el cambio cabe en el sprint y el equipo "
                "tiene capacidad para absorberlo sin riesgo de entrega."
            ),
            "que_ocurre": [
                "El analista actualiza el requisito y se regeneran los artefactos.",
                "Se notifica al desarrollador asignado del cambio en los criterios.",
                "Los test cases afectados se actualizan antes de que QA los ejecute.",
                "La historia se entrega en este sprint con el alcance nuevo."
            ],
            "riesgo": (
                "Si la estimación de esfuerzo adicional es incorrecta, "
                "la historia puede no completarse en el sprint."
            ),
            "tiempo_de_coordinacion_h": 1.5
        },
        "B": {
            "titulo": "Posponer el cambio al siguiente sprint",
            "cuando_aplicar": (
                "Cuando el cambio es demasiado grande para el sprint actual "
                "o el desarrollo está demasiado avanzado para incorporarlo sin riesgo."
            ),
            "que_ocurre": [
                "La historia actual se completa con el alcance original.",
                "El cambio se documenta como deuda de producto en el backlog.",
                "Se crea una nueva historia o se modifica el requisito para el siguiente sprint.",
                "El desarrollador termina lo que ya está haciendo sin interrupciones."
            ],
            "riesgo": (
                "El negocio tendrá disponible la funcionalidad original durante "
                "el tiempo entre este sprint y el siguiente. "
                "Si el cambio era urgente, este retraso tiene coste."
            ),
            "tiempo_de_coordinacion_h": 0.5
        },
        "C": {
            "titulo": "Partir la historia en dos",
            "cuando_aplicar": (
                "Cuando parte del alcance original puede entregarse en este sprint "
                "y el cambio solicitado se añade como una historia nueva."
            ),
            "que_ocurre": [
                "La historia actual se reduce al alcance que ya está implementado.",
                "Se crea una historia nueva con el alcance adicional o el cambio.",
                "La historia reducida se puede cerrar en este sprint.",
                "La historia nueva entra al backlog para priorización."
            ],
            "riesgo": (
                "Complejidad de gestión: dos historias en lugar de una, "
                "con riesgo de que la segunda quede desprioritizada indefinidamente."
            ),
            "tiempo_de_coordinacion_h": 2.0
        },
        "D": {
            "titulo": "Reabrir la historia y aplicar el cambio",
            "cuando_aplicar": (
                "Solo cuando la historia está en Done y el cambio es crítico "
                "para el negocio. Esta opción tiene el mayor coste."
            ),
            "que_ocurre": [
                "La historia se reabre y vuelve a In Progress.",
                "El desarrollador debe retomar el contexto y aplicar el cambio.",
                "Los test cases ejecutados como PASS pueden necesitar re-ejecución.",
                "La velocidad del sprint queda afectada si el sprint todavía no cerró."
            ],
            "riesgo": (
                "Alto riesgo de regresión. El código ya pasó revisión y testing; "
                "reabrirlo introduce inestabilidad en una historia que se consideraba estable."
            ),
            "tiempo_de_coordinacion_h": 3.0
        }
    }

    def __init__(self, openai_client, config):
        self.openai = openai_client
        self.config = config

    def generar(
        self,
        cambio: "CambioMidSprint",
        impacto: "ImpactoSprint"
    ) -> BriefingPO:

        id_solicitud = f"MID-{cambio.requisito_id}-{cambio.historia_jira_key}"

        # Calcular urgencia basada en días restantes y nivel de riesgo
        urgencia = (
            "inmediata" if (
                impacto.dias_restantes <= 1 or
                impacto.nivel_riesgo == "rojo"
            )
            else "hoy" if impacto.dias_restantes <= 3
            else "antes_de_manana"
        )

        # Construir las opciones con sus consecuencias calculadas
        opciones_calculadas = self._calcular_opciones(cambio, impacto)

        # Determinar la recomendación del sistema
        recomendacion = self._recomendar_opcion(cambio, impacto)

        # Generar el resumen ejecutivo y la pregunta clave con el LLM
        narrativa = self._generar_narrativa_llm(
            cambio, impacto, recomendacion
        )

        # Calcular plazo de decisión
        plazo = self._calcular_plazo_decision(urgencia, impacto)

        return BriefingPO(
            id_solicitud=id_solicitud,
            urgencia=urgencia,
            resumen_ejecutivo=narrativa["resumen_ejecutivo"],
            cambio={
                "requisito_id": cambio.requisito_id,
                "historia_key": cambio.historia_jira_key,
                "tipo": cambio.tipo_cambio,
                "severidad": cambio.severidad,
                "descripcion": cambio.descripcion_cambio,
                "desarrollador": cambio.desarrollador_asignado,
                "estado_historia": cambio.estado_historia
            },
            impacto={
                "sprint": cambio.sprint_nombre,
                "dias_restantes": cambio.dias_restantes,
                "nivel_riesgo": impacto.nivel_riesgo,
                "esfuerzo_adicional_h": impacto.esfuerzo_adicional_h,
                "capacidad_restante_h": impacto.capacidad_restante_h,
                "puede_absorber": impacto.puede_absorber,
                "artefactos_afectados": cambio.artefactos_afectados
            },
            opciones=opciones_calculadas,
            recomendacion_sistema=recomendacion,
            pregunta_clave=narrativa["pregunta_clave"],
            plazo_decision=plazo
        )

    def _calcular_opciones(
        self,
        cambio: "CambioMidSprint",
        impacto: "ImpactoSprint"
    ) -> list[dict]:
        """
        Construye la lista de opciones disponibles con sus
        consecuencias concretas para este caso específico.
        """
        opciones = []
        for letra in impacto.opciones_disponibles:
            plantilla = self.PLANTILLAS_OPCIONES[letra]
            opcion = {
                "letra": letra,
                "titulo": plantilla["titulo"],
                "cuando_aplicar": plantilla["cuando_aplicar"],
                "que_ocurre": plantilla["que_ocurre"],
                "riesgo": plantilla["riesgo"],
                "tiempo_coordinacion_h": plantilla["tiempo_de_coordinacion_h"],
                # Consecuencias específicas para este caso
                "impacto_en_sprint": self._calcular_impacto_opcion_sprint(
                    letra, cambio, impacto
                ),
                "impacto_en_equipo": self._calcular_impacto_opcion_equipo(
                    letra, cambio
                )
            }
            opciones.append(opcion)
        return opciones

    def _calcular_impacto_opcion_sprint(
        self, letra: str, cambio: "CambioMidSprint", impacto: "ImpactoSprint"
    ) -> str:
        if letra == "A":
            if impacto.puede_absorber:
                return (
                    f"El sprint puede absorber las ~{impacto.esfuerzo_adicional_h}h "
                    f"adicionales estimadas. Margen: "
                    f"{abs(impacto.deficit_h):.1f}h."
                )
            return (
                f"El sprint NO puede absorber el cambio cómodamente. "
                f"Déficit estimado: {abs(impacto.deficit_h):.1f}h. "
                f"Riesgo de no completar en el sprint."
            )
        if letra == "B":
            return (
                f"Sin impacto en el sprint actual. "
                f"{cambio.desarrollador_asignado} termina sin interrupciones."
            )
        if letra == "C":
            return (
                f"La historia reducida puede cerrarse en el sprint. "
                f"La nueva historia entra al siguiente sprint o al backlog."
            )
        if letra == "D":
            return (
                f"La historia reabierta puede no cerrarse antes del "
                f"cierre del sprint ({impacto.dias_restantes} días restantes)."
            )
        return ""

    def _calcular_impacto_opcion_equipo(
        self, letra: str, cambio: "CambioMidSprint"
    ) -> str:
        developer = cambio.desarrollador_asignado
        n_tc = (
            len(cambio.artefactos_afectados.get("test_cases_invalidos", [])) +
            len(cambio.artefactos_afectados.get("test_cases_a_regenerar", []))
        )
        if letra == "A":
            return (
                f"{developer} recibe notificación inmediata del cambio. "
                f"{n_tc} test cases deben actualizarse antes del QA."
            )
        if letra == "B":
            return (
                f"{developer} no se interrumpe. "
                f"El cambio se comunica al equipo como deuda documentada."
            )
        if letra == "C":
            return (
                f"{developer} recibe instrucciones de qué parte del trabajo "
                f"completar y qué dejar para la historia nueva."
            )
        if letra == "D":
            return (
                f"{developer} debe retomar el contexto de una historia "
                f"que ya consideraba cerrada. Alto coste cognitivo."
            )
        return ""

    def _recomendar_opcion(
        self, cambio: "CambioMidSprint", impacto: "ImpactoSprint"
    ) -> str:
        """
        Reglas deterministas para la recomendación del sistema.
        El sistema recomienda, pero el PO decide.
        """
        # Historia ya completada: siempre posponer salvo urgencia crítica
        if cambio.estado_historia == "Done":
            return "B"

        # Historia en QA con tests inválidos: partir o posponer
        if (cambio.estado_historia == "In Testing" and
                cambio.artefactos_afectados.get("test_cases_invalidos")):
            return "C" if "C" in impacto.opciones_disponibles else "B"

        # Poco tiempo y déficit grande: posponer
        if impacto.dias_restantes <= 2 and not impacto.puede_absorber:
            return "B"

        # Sprint puede absorber y hay margen: aceptar
        if impacto.puede_absorber and impacto.nivel_riesgo == "verde":
            return "A"

        # Ampliación de alcance con sprint a más del 50% completado: partir
        if (cambio.tipo_cambio == "Tipo 2" and
                impacto.contexto_sprint.get("porcentaje_completado", 0) > 50 and
                "C" in impacto.opciones_disponibles):
            return "C"

        # Por defecto: posponer (conservador)
        return "B"

    def _generar_narrativa_llm(
        self,
        cambio: "CambioMidSprint",
        impacto: "ImpactoSprint",
        recomendacion: str
    ) -> dict:
        """Genera la parte narrativa del briefing con el LLM."""

        prompt = f"""
Eres un Scrum Master senior. Redacta el resumen ejecutivo y la pregunta
clave para el Product Owner sobre este cambio mid-sprint.

CAMBIO:
- Requisito: {cambio.requisito_id}
- Historia en desarrollo: {cambio.historia_jira_key}
- Estado: {cambio.estado_historia}
- Desarrollador: {cambio.desarrollador_asignado}
- Tipo de cambio: {cambio.tipo_cambio}
- Descripción: {cambio.descripcion_cambio}

IMPACTO EN EL SPRINT:
- Sprint: {cambio.sprint_nombre} ({cambio.dias_restantes} días restantes)
- Nivel de riesgo: {impacto.nivel_riesgo}
- Puede absorber el cambio: {impacto.puede_absorber}
- Esfuerzo adicional estimado: {impacto.esfuerzo_adicional_h}h

RECOMENDACIÓN DEL SISTEMA: Opción {recomendacion}

Responde SOLO con este JSON, sin texto adicional:
{{
  "resumen_ejecutivo": "[3 frases máximo. Sin tecnicismos. Explica el problema y la urgencia.]",
  "pregunta_clave": "[La pregunta específica que necesita responder el PO para desbloquear al equipo.]"
}}
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.choices[0].message.content)

    def _calcular_plazo_decision(
        self, urgencia: str, impacto: "ImpactoSprint"
    ) -> str:
        from datetime import datetime, timedelta
        ahora = datetime.now()
        if urgencia == "inmediata":
            return f"Antes de las {(ahora + timedelta(hours=2)).strftime('%H:%M')} de hoy"
        if urgencia == "hoy":
            return "Antes del final de la jornada de hoy"
        return f"Antes del inicio de la jornada del {(ahora + timedelta(days=1)).strftime('%Y-%m-%d')}"
```

---

## Fase 4 — Decisión humana

El Product Owner recibe el briefing y elige una de las opciones disponibles. La decisión llega al sistema a través del mismo endpoint de aprobación del punto 10, con un tipo de solicitud específico.

```python
# mid_sprint_decision_endpoint.py

# Este endpoint se añade al servidor FastAPI del punto 10

from fastapi import HTTPException
from pydantic import BaseModel


class DecisionMidSprint(BaseModel):
    solicitud_id: str
    opcion: str                # A │ B │ C │ D
    motivo: str = ""
    product_owner: str
    # Para opción C: cómo partir la historia
    descripcion_historia_nueva: str = ""
    criterios_historia_nueva: list = []
    # Para opción A con modificaciones: ajustes al scope
    ajustes_scope: dict = {}


@app.post("/mid-sprint/decidir")
async def decidir_cambio_mid_sprint(
    decision: DecisionMidSprint,
    ejecutor: "EjecutorDecisionMidSprint" = None
):
    """
    El PO envía su decisión. El sistema ejecuta automáticamente
    las acciones correspondientes a la opción elegida.
    """
    if decision.solicitud_id not in cola_mid_sprint:
        raise HTTPException(404, "Solicitud no encontrada")

    solicitud = cola_mid_sprint[decision.solicitud_id]

    resultado = await ejecutor.ejecutar(
        solicitud=solicitud,
        decision=decision
    )

    return {
        "estado": "procesado",
        "opcion_ejecutada": decision.opcion,
        "acciones_realizadas": resultado["acciones"],
        "proximos_pasos": resultado["proximos_pasos"]
    }
```

---

## Fase 5 — Ejecución de la decisión

Cada opción tiene su propio ejecutor con las acciones concretas que el sistema realiza automáticamente.

### Opción A — Aceptar el cambio en el sprint actual

```python
# executor_opcion_a.py

async def ejecutar_opcion_a(
    cambio: "CambioMidSprint",
    briefing: "BriefingPO",
    decision: "DecisionMidSprint",
    conector_jira,
    motor_pipeline,
    notificador
) -> dict:
    """
    Acepta el cambio en el sprint actual.
    1. Actualiza los artefactos generados (historia, test cases).
    2. Notifica al desarrollador con el contexto exacto del cambio.
    3. Marca los test cases inválidos como obsoletos en Xray.
    4. Registra el cambio en el grafo de trazabilidad.
    """
    acciones = []

    # 1. Regenerar historia y test cases con el nuevo requisito
    artefactos_nuevos = await motor_pipeline.regenerar_desde_requisito(
        requisito_id=cambio.requisito_id,
        campo_modificado=cambio.campo_modificado,
        dry_run=False
    )
    acciones.append(
        f"Historia {cambio.historia_jira_key} actualizada en Jira"
    )

    # 2. Invalidar test cases obsoletos en Xray
    for tc in cambio.artefactos_afectados.get("test_cases_invalidos", []):
        await conector_jira.xray.marcar_obsoleto(
            tc_id=tc["id"],
            motivo=f"Invalidado por cambio mid-sprint en {cambio.requisito_id}",
            issue_origen=cambio.historia_jira_key
        )
        acciones.append(f"Test case {tc['id']} marcado como obsoleto en Xray")

    # 3. Añadir comentario en la historia de Jira con el contexto del cambio
    comentario = _generar_comentario_cambio_aceptado(cambio, decision)
    await conector_jira.cliente.post(
        f"issue/{cambio.historia_jira_key}/comment",
        payload={"body": comentario}
    )
    acciones.append(f"Comentario de cambio añadido en {cambio.historia_jira_key}")

    # 4. Notificar al desarrollador con contexto accionable
    await notificador.notificar_desarrollador(
        historia_key=cambio.historia_jira_key,
        desarrollador=cambio.desarrollador_asignado,
        cambio=cambio,
        artefactos_nuevos=artefactos_nuevos,
        mensaje_personalizado=_generar_mensaje_desarrollador(
            cambio, artefactos_nuevos
        )
    )
    acciones.append(
        f"Desarrollador {cambio.desarrollador_asignado} notificado"
    )

    # 5. Notificar al QA lead si hay test cases en ejecución afectados
    if cambio.artefactos_afectados.get("test_cases_invalidos"):
        await notificador.notificar_qa_lead(
            historia_key=cambio.historia_jira_key,
            cambio=cambio,
            mensaje=(
                f"⚠ Cambio mid-sprint en {cambio.historia_jira_key}. "
                f"{len(cambio.artefactos_afectados['test_cases_invalidos'])} "
                f"test cases invalidados. Pausar ejecución hasta que los "
                f"nuevos test cases estén disponibles (~30 min)."
            )
        )
        acciones.append("QA lead notificado de test cases invalidados")

    return {
        "acciones": acciones,
        "proximos_pasos": [
            f"El desarrollador {cambio.desarrollador_asignado} revisará "
            f"los criterios actualizados en los próximos 30 min.",
            "Los nuevos test cases estarán disponibles en Xray en ~15 min.",
            "QA puede reanudar testing cuando el desarrollador confirme "
            "que el código refleja los nuevos criterios."
        ]
    }


def _generar_mensaje_desarrollador(
    cambio: "CambioMidSprint",
    artefactos_nuevos: dict
) -> str:
    """Mensaje directo y accionable para el desarrollador."""
    n_ac_nuevos = len(
        artefactos_nuevos.get("historia", {})
        .get("acceptance_criteria", [])
    )
    return (
        f"⚠ *Cambio de alcance en {cambio.historia_jira_key}*\n\n"
        f"*Qué cambió:* {cambio.descripcion_cambio}\n\n"
        f"*Lo que tienes que revisar:*\n"
        f"- Los criterios de aceptación han sido actualizados "
        f"({n_ac_nuevos} criterios activos).\n"
        f"- Revisa la historia actualizada en Jira antes de continuar.\n"
        f"- Si ya tenías código que verificaba el comportamiento anterior, "
        f"puede necesitar ajuste.\n\n"
        f"*No bloquees tu trabajo:* si necesitas más contexto, "
        f"avisa al analista antes de tomar decisiones técnicas."
    )
```

### Opción B — Posponer al siguiente sprint

```python
# executor_opcion_b.py

async def ejecutar_opcion_b(
    cambio: "CambioMidSprint",
    decision: "DecisionMidSprint",
    conector_jira,
    motor_trazabilidad,
    notificador
) -> dict:
    """
    Pospone el cambio al siguiente sprint.
    1. Crea una issue de tipo 'Deuda de producto' en el backlog.
    2. Añade un comentario en la historia actual explicando
       que existe un cambio pendiente para el siguiente sprint.
    3. El requisito YAML no se modifica todavía: el analista
       lo actualizará cuando la historia nueva entre al sprint.
    """
    acciones = []

    # 1. Crear issue de deuda de producto en el backlog
    payload_deuda = {
        "fields": {
            "project": {"key": conector_jira.config.project_key},
            "issuetype": {"name": "Story"},
            "summary": (
                f"[Cambio pendiente] {cambio.descripcion_cambio} "
                f"— {cambio.requisito_id}"
            ),
            "description": conector_jira.constructor._construir_adf(
                _generar_descripcion_deuda(cambio, decision)
            ),
            "priority": {"name": "High"},
            "labels": [
                "cambio-mid-sprint",
                "deuda-producto",
                cambio.requisito_id
            ],
            conector_jira.config.campo_requisito_origen: cambio.requisito_id
        }
    }
    respuesta = conector_jira.cliente.post("issue", payload_deuda)
    deuda_key = respuesta["key"]
    acciones.append(f"Deuda de producto creada: {deuda_key}")

    # 2. Vincular la deuda con la historia actual
    conector_jira.cliente.post("issueLink", {
        "type": {"name": "is preceded by"},
        "inwardIssue": {"key": deuda_key},
        "outwardIssue": {"key": cambio.historia_jira_key}
    })
    acciones.append(
        f"Link creado: {deuda_key} continúa {cambio.historia_jira_key}"
    )

    # 3. Comentar en la historia actual
    comentario = (
        f"ℹ *Cambio de alcance pospuesto al siguiente sprint*\n\n"
        f"El negocio ha solicitado el siguiente cambio: "
        f"{cambio.descripcion_cambio}\n\n"
        f"*Decisión del PO ({decision.product_owner}):* "
        f"implementar en el siguiente sprint.\n\n"
        f"Esta historia se completa con el alcance original. "
        f"El cambio está documentado en {deuda_key}."
    )
    conector_jira.cliente.post(
        f"issue/{cambio.historia_jira_key}/comment",
        payload={"body": conector_jira.constructor._construir_adf(comentario)}
    )
    acciones.append(f"Comentario añadido en {cambio.historia_jira_key}")

    # 4. Registrar en el grafo de trazabilidad
    motor_trazabilidad.registrar_arista(Arista(
        origen_id=deuda_key,
        destino_id=cambio.historia_jira_key,
        tipo_relacion="depende_de",
        origen_relacion="mid_sprint_cambio",
        metadatos={
            "tipo": "cambio_pospuesto",
            "requisito_id": cambio.requisito_id,
            "decision_po": decision.product_owner
        }
    ))

    # 5. Notificar al desarrollador (sin interrumpir su trabajo)
    await notificador.notificar_desarrollador(
        historia_key=cambio.historia_jira_key,
        desarrollador=cambio.desarrollador_asignado,
        cambio=cambio,
        mensaje_personalizado=(
            f"ℹ FYI: el negocio ha pedido un cambio en "
            f"{cambio.historia_jira_key} pero el PO ha decidido "
            f"posponerlo al siguiente sprint. "
            f"Continúa con el alcance original sin cambios. "
            f"El cambio queda documentado en {deuda_key}."
        )
    )
    acciones.append(
        f"Desarrollador {cambio.desarrollador_asignado} notificado (sin interrupción)"
    )

    return {
        "acciones": acciones,
        "proximos_pasos": [
            f"Deuda {deuda_key} en backlog para priorización del siguiente sprint.",
            f"El analista actualizará el YAML de {cambio.requisito_id} "
            f"cuando {deuda_key} entre al sprint planning.",
            f"{cambio.desarrollador_asignado} continúa sin interrupciones."
        ]
    }


def _generar_descripcion_deuda(
    cambio: "CambioMidSprint",
    decision: "DecisionMidSprint"
) -> str:
    return (
        f"## Origen\n"
        f"Cambio de alcance solicitado por el negocio durante el sprint "
        f"{cambio.sprint_nombre}, cuando la historia {cambio.historia_jira_key} "
        f"ya estaba en desarrollo ({cambio.estado_historia}).\n\n"
        f"## Cambio solicitado\n{cambio.descripcion_cambio}\n\n"
        f"## Por qué se pospuso\n"
        f"{decision.motivo or 'El sprint no tenía capacidad para absorber el cambio sin riesgo de entrega.'}\n\n"
        f"## Decisión del PO\n"
        f"Pospuesto por {decision.product_owner}. "
        f"Implementar en el siguiente sprint con prioridad alta.\n\n"
        f"## Requisito origen\n"
        f"Este cambio debe incorporarse al YAML de {cambio.requisito_id} "
        f"cuando esta historia entre al sprint planning."
    )
```

### Opción C — Partir la historia

```python
# executor_opcion_c.py

async def ejecutar_opcion_c(
    cambio: "CambioMidSprint",
    decision: "DecisionMidSprint",
    conector_jira,
    motor_pipeline,
    motor_trazabilidad,
    notificador
) -> dict:
    """
    Parte la historia en dos:
    - Historia actual: se reduce al alcance ya implementado.
    - Historia nueva: contiene el cambio o la ampliación solicitada.
    """
    acciones = []

    # 1. Reducir el alcance de la historia actual
    # Actualizar la descripción y los criterios de aceptación
    # para reflejar solo lo que ya está implementado
    descripcion_reducida = _generar_descripcion_historia_reducida(cambio)
    conector_jira.cliente.put(
        f"issue/{cambio.historia_jira_key}",
        payload={
            "fields": {
                "description": conector_jira.constructor._construir_adf(
                    descripcion_reducida
                ),
                "labels": (
                    conector_jira.cliente.get(
                        f"issue/{cambio.historia_jira_key}",
                        params={"fields": "labels"}
                    ).get("fields", {}).get("labels", []) +
                    ["split-original"]
                )
            }
        }
    )
    acciones.append(
        f"Historia {cambio.historia_jira_key} reducida al alcance original"
    )

    # 2. Crear la historia nueva con el cambio solicitado
    # El PO puede haber proporcionado la descripción en la DecisionMidSprint
    historia_nueva_summary = (
        decision.descripcion_historia_nueva or
        f"[Split de {cambio.historia_jira_key}] {cambio.descripcion_cambio}"
    )

    payload_nueva = {
        "fields": {
            "project": {"key": conector_jira.config.project_key},
            "issuetype": {"name": "Story"},
            "summary": historia_nueva_summary,
            "description": conector_jira.constructor._construir_adf(
                _generar_descripcion_historia_nueva(
                    cambio, decision, historia_nueva_summary
                )
            ),
            "priority": {"name": "High"},
            "labels": [
                "split-nuevo",
                "cambio-mid-sprint",
                cambio.requisito_id
            ],
            conector_jira.config.campo_requisito_origen: cambio.requisito_id
        }
    }

    # Copiar la épica de la historia original
    epica = conector_jira.cliente.get(
        f"issue/{cambio.historia_jira_key}",
        params={"fields": conector_jira.config.campo_epic_link}
    ).get("fields", {}).get(conector_jira.config.campo_epic_link)
    if epica:
        payload_nueva["fields"][conector_jira.config.campo_epic_link] = epica

    respuesta_nueva = conector_jira.cliente.post("issue", payload_nueva)
    nueva_key = respuesta_nueva["key"]
    acciones.append(f"Historia nueva {nueva_key} creada en el backlog")

    # 3. Vincular las dos historias
    conector_jira.cliente.post("issueLink", {
        "type": {"name": "splits into"},
        "inwardIssue": {"key": cambio.historia_jira_key},
        "outwardIssue": {"key": nueva_key}
    })
    acciones.append(
        f"Link split: {cambio.historia_jira_key} → {nueva_key}"
    )

    # 4. Generar test cases para la historia nueva (si hay AC definidos)
    if decision.criterios_historia_nueva:
        test_cases_nuevos = await motor_pipeline.generar_test_cases_desde_criterios(
            criterios=decision.criterios_historia_nueva,
            historia_key=nueva_key,
            requisito_id=cambio.requisito_id
        )
        acciones.append(
            f"{len(test_cases_nuevos)} test cases generados para {nueva_key}"
        )

    # 5. Registrar en el grafo
    motor_trazabilidad.registrar_nodo(Nodo(
        id=nueva_key,
        tipo="historia",
        titulo=historia_nueva_summary,
        estado="Backlog",
        metadatos={
            "requisito_origen": cambio.requisito_id,
            "split_desde": cambio.historia_jira_key,
            "tipo": "split-nuevo"
        }
    ))
    motor_trazabilidad.registrar_arista(Arista(
        origen_id=cambio.historia_jira_key,
        destino_id=nueva_key,
        tipo_relacion="genera",
        origen_relacion="mid_sprint_split",
        metadatos={"tipo": "split"}
    ))
    acciones.append("Grafo de trazabilidad actualizado con el split")

    # 6. Notificar al equipo completo
    await notificador.notificar_equipo_split(
        historia_original=cambio.historia_jira_key,
        historia_nueva=nueva_key,
        desarrollador=cambio.desarrollador_asignado,
        decision_po=decision.product_owner,
        cambio=cambio
    )
    acciones.append("Equipo notificado del split")

    return {
        "acciones": acciones,
        "proximos_pasos": [
            f"Historia {cambio.historia_jira_key} continúa en el sprint "
            f"con el alcance reducido.",
            f"Historia {nueva_key} en el backlog para el siguiente sprint planning.",
            f"El analista actualizará el YAML de {cambio.requisito_id} antes "
            f"del sprint planning donde {nueva_key} entre al sprint.",
            f"{cambio.desarrollador_asignado} recibe instrucciones de "
            f"qué completar y qué dejar pendiente."
        ]
    }
```

---

## Fase 6 — Actualización del grafo de trazabilidad

Independientemente de la opción elegida, el sistema registra el evento mid-sprint en el grafo con suficiente detalle para que la auditoría del punto 12 pueda reconstruir exactamente qué ocurrió, cuándo y por qué.

```python
# mid_sprint_traceability.py

def registrar_evento_mid_sprint(
    motor_trazabilidad,
    cambio: "CambioMidSprint",
    decision: "DecisionMidSprint",
    resultado: dict
):
    """
    Registra el evento completo en el grafo de trazabilidad.
    Esto permite:
    - Auditar la decisión (quién decidió qué y cuándo).
    - Medir la frecuencia de cambios mid-sprint por módulo.
    - Detectar patrones de inestabilidad en ciertos requisitos.
    - Calcular el coste real de los cambios tardíos.
    """

    evento_id = (
        f"MID-{cambio.requisito_id}-"
        f"{cambio.historia_jira_key}-"
        f"{datetime.now().strftime('%Y%m%d%H%M')}"
    )

    # Nodo del evento
    motor_trazabilidad.registrar_nodo(Nodo(
        id=evento_id,
        tipo="evento_mid_sprint",
        titulo=f"Cambio mid-sprint: {cambio.descripcion_cambio[:80]}",
        estado="resuelto",
        metadatos={
            "requisito_id": cambio.requisito_id,
            "historia_key": cambio.historia_jira_key,
            "tipo_cambio": cambio.tipo_cambio,
            "severidad": cambio.severidad,
            "campo_modificado": cambio.campo_modificado,
            "estado_historia_al_detectar": cambio.estado_historia,
            "dias_restantes_sprint": cambio.dias_restantes_sprint,
            "opcion_elegida": decision.opcion,
            "product_owner": decision.product_owner,
            "motivo": decision.motivo,
            "timestamp": datetime.now().isoformat(),
            "esfuerzo_adicional_estimado_h": cambio.esfuerzo_adicional_estimado_h,
            "artefactos_invalidados": len(
                cambio.artefactos_afectados.get("test_cases_invalidos", [])
            ),
            "artefactos_regenerados": len(
                cambio.artefactos_afectados.get("test_cases_a_regenerar", [])
            )
        }
    ))

    # Aristas hacia los nodos afectados
    motor_trazabilidad.registrar_arista(Arista(
        origen_id=evento_id,
        destino_id=cambio.historia_jira_key,
        tipo_relacion="vincula",
        origen_relacion="mid_sprint_change",
        metadatos={"rol": "historia_afectada"}
    ))

    motor_trazabilidad.registrar_arista(Arista(
        origen_id=cambio.requisito_id,
        destino_id=evento_id,
        tipo_relacion="genera",
        origen_relacion="mid_sprint_change",
        metadatos={"rol": "origen_del_cambio"}
    ))
```

---

## Integración con el pipeline existente

El flujo mid-sprint se activa como una rama condicional del webhook que ya existe en el punto 10. El orquestador del punto 12 detecta automáticamente si debe ejecutar el flujo estándar de impacto o el flujo mid-sprint.

```python
# En el webhook receiver del punto 10, añadir esta lógica:

async def recibir_cambio_requisito(payload: dict):
    """
    Punto de entrada unificado para cambios en requisitos.
    Decide automáticamente qué flujo activar.
    """
    requisito_id = payload.get("requisito_id")
    campo = payload.get("campo_modificado")
    yaml_nuevo = payload.get("yaml_nuevo")

    # Intentar activar el flujo mid-sprint primero
    cambio_mid = detector_mid_sprint.evaluar(
        requisito_id=requisito_id,
        campo_modificado=campo,
        valor_anterior=payload.get("valor_anterior"),
        valor_nuevo=payload.get("valor_nuevo"),
        yaml_nuevo=yaml_nuevo
    )

    if cambio_mid:
        # Historia en sprint activo: flujo mid-sprint
        impacto = calculador_impacto.calcular(cambio_mid)
        briefing = generador_briefing.generar(cambio_mid, impacto)
        cola_mid_sprint[briefing.id_solicitud] = {
            "cambio": cambio_mid,
            "impacto": impacto,
            "briefing": briefing
        }
        await notificador.enviar_briefing_po(briefing)
        return {"flujo": "mid_sprint", "solicitud_id": briefing.id_solicitud}
    else:
        # Sin historia activa: flujo estándar del punto 8
        informe = await analizador_impacto.analizar(
            requisito_id=requisito_id,
            cambios=[...],
            yaml_nuevo=yaml_nuevo
        )
        await notificador.enviar_informe_impacto(informe)
        return {"flujo": "estandar", "informe": informe}
```

---

## Métricas de gobierno del flujo mid-sprint

Este flujo genera datos de gran valor para medir la calidad del proceso de análisis. Las métricas que deben monitorizarse en el dashboard del punto 12:

| Métrica | Descripción | Señal de alarma |
|---|---|---|
| **Frecuencia de cambios mid-sprint** | Cambios por sprint y por módulo | >3 cambios por sprint en el mismo módulo indica inestabilidad de requisitos |
| **Opción más elegida por el PO** | Distribución A/B/C/D en el tiempo | >60% de opción B indica que los cambios llegan sistemáticamente tarde |
| **Coste medio de un cambio mid-sprint** | Horas adicionales reales vs estimadas | Divergencia >50% indica que el modelo de estimación necesita recalibración |
| **Tiempo de decisión del PO** | Desde el briefing hasta la decisión | >4 horas indica que el briefing no es suficientemente accionable |
| **Tasa de test cases invalidados** | Test cases marcados obsoletos por cambios mid-sprint | >2 por sprint indica que los cambios llegan demasiado tarde en el ciclo |
| **Requisitos con >1 cambio mid-sprint** | Requisitos que generan cambios repetidos | Cualquier requisito con >2 cambios es candidato a ser reescritto desde cero |

---

## Ejemplo de briefing completo enviado al PO

Este es el aspecto del mensaje que recibe el Product Owner en Slack cuando se detecta un cambio mid-sprint:

```
⚠ CAMBIO MID-SPRINT — Decisión requerida hoy antes de las 17:00
Solicitud: MID-REQ-023-FACT-47
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESUMEN
El negocio ha pedido reducir el rango máximo de búsqueda de facturas
de 365 a 90 días. La historia FACT-47 está en desarrollo activo y María
García ya ha implementado la validación de 365 días. El sprint cierra en
3 días. Sin tu decisión hoy, María puede entregar código que ya no es
correcto.

CAMBIO SOLICITADO
Campo: criterios_aceptacion
Descripción: Criterios modificados: AC-023-01 (límite de 365 días
cambia a 90 días), AC-023-02 (mensaje de error actualizado)

ESTADO ACTUAL
Historia: FACT-47 (In Progress)
Desarrollador: María García
Sprint: Sprint 42 — cierra el 2025-05-15 (3 días)
Nivel de riesgo: 🟡 AMARILLO

IMPACTO SI NO SE DECIDE HOY
3 test cases ejecutados con el criterio de 365 días quedan inválidos.
María puede completar código incorrecto que fallará en QA.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPCIONES DISPONIBLES

[A] Aceptar el cambio en este sprint (~6.5h adicionales estimadas)
    → María recibe notificación inmediata de los nuevos criterios
    → 3 test cases se regeneran automáticamente
    → El sprint puede absorberlo; margen: 2.5h
    ✓ RECOMENDADO POR EL SISTEMA

[B] Posponer al siguiente sprint (0.5h de coordinación)
    → María termina con el límite de 365 días
    → Se crea FACT-48 en el backlog para el próximo sprint
    → Sin interrupción para el equipo

[C] Partir la historia
    → FACT-47 se cierra con el alcance original (365 días)
    → Se crea una historia nueva para el cambio a 90 días
    → Mayor complejidad de gestión

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREGUNTA CLAVE
¿El cambio de 365 a 90 días debe estar disponible para el cierre
contable del próximo mes (26 mayo) o puede esperar al siguiente sprint?

[Responder] → pipeline-ai.interno/mid-sprint/MID-REQ-023-FACT-47
```

---

## Relación con los demás componentes del modelo

Este flujo no es un componente aislado: se apoya en todos los puntos del núcleo técnico y los enriquece.

El **motor de detección de impacto del punto 8** actúa como detector de entrada. La diferencia es que el flujo mid-sprint toma el control cuando ese detector encuentra una historia en sprint activo, en lugar de limitarse a generar un informe de impacto.

El **grafo de trazabilidad del punto 9** es la fuente de datos para identificar qué test cases y tareas están afectados, y el destino donde se registran los eventos mid-sprint para auditoría.

La **integración con Jira del punto 10** ejecuta los cambios en Jira: actualización de historias, creación de historias nuevas, añadir comentarios y crear issue links de tipo split o depende-de.

El **sistema de alertas del gobierno del punto 12** consume las métricas generadas por este flujo para detectar patrones de inestabilidad de requisitos a nivel de módulo o de analista.

El **pipeline de generación del punto 4 y 5** se reutiliza en la opción A para regenerar los artefactos actualizados sin necesidad de que el analista ejecute el pipeline manualmente.
