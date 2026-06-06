# Gestión de versiones de un mismo requisito en sprints distintos — Implementación parcial

> **Módulo complementario del Modelo Operativo AI-Ready**
> Capa: Núcleo técnico del pipeline · Dependencias: Puntos 4, 5, 7, 8, 9, 10

---

## El problema que este módulo resuelve

El pipeline descrito en los puntos 4 al 10 asume implícitamente que un requisito validado genera sus artefactos una vez y se implementa completamente en un único sprint. Esta es la situación ideal, pero no es la más frecuente en proyectos reales de cierta envergadura.

Los escenarios de implementación parcial son más habituales de lo que los procesos Agile reconocen formalmente:

- Un requisito de 13 story points que el equipo decide implementar en dos sprints consecutivos entregando valor incremental en cada uno.
- Un requisito que bloquea por una dependencia técnica externa y cuya segunda parte se pospone dos sprints.
- Un requisito cuyo alcance el negocio amplía después de ver la primera entrega funcional, generando una segunda fase que comparte el mismo origen funcional.
- Un requisito de integración cuya primera fase es el backend y la segunda el frontend, entregados en sprints distintos por restricciones de equipo.

En todos estos casos, el pipeline estándar no tiene respuesta. Si se ejecuta de nuevo sobre el mismo YAML genera duplicados en Jira. Si no se ejecuta, la segunda fase no tiene artefactos estructurados ni trazabilidad correcta. Si se crea un requisito nuevo sin relación con el original, la matriz de trazabilidad queda rota y el grafo del punto 9 no refleja la historia real del desarrollo.

Este módulo define el modelo de implementación parcial: cómo estructurar el YAML, cómo gestionar las versiones de entrega, cómo mantener la trazabilidad entre fases y cómo el pipeline las procesa de forma diferenciada sin generar inconsistencias.

---

## Conceptos fundamentales del modelo

### Requisito vs. entrega

El modelo distingue dos niveles que en los proyectos sin este módulo se confunden sistemáticamente:

El **requisito** es la unidad funcional de negocio. Define qué capacidad necesita el usuario, con qué criterios de aceptación y bajo qué reglas de negocio. Es estable: no cambia porque el equipo decida implementarlo en dos sprints en lugar de uno.

La **entrega** es la unidad de implementación. Define qué subconjunto del requisito se construye en un sprint concreto, qué criterios de aceptación cubre esa entrega específica y qué queda pendiente para entregas siguientes. Es flexible: puede cambiar según la capacidad del equipo, las dependencias técnicas o las prioridades del negocio.

Esta distinción es la clave arquitectónica del módulo. El YAML del requisito no cambia entre entregas: lo que cambia es el bloque de entregas que crece con cada sprint en el que se trabaja parcialmente sobre él.

### La regla de completitud progresiva

Una entrega es válida si y solo si cumple estas tres condiciones:

1. **Entregable independiente:** la funcionalidad incluida en la entrega tiene valor de negocio por sí sola, aunque sea reducido. Una entrega que solo tiene valor si se completa con la siguiente no es una entrega válida: es un trabajo a medias disfrazado de entrega parcial.

2. **Criterios de aceptación propios:** cada entrega tiene sus propios criterios de aceptación, que son un subconjunto de los criterios del requisito completo o criterios intermedios específicos de esa fase. Nunca criterios que se "pasan" de una entrega a la siguiente.

3. **Trazabilidad explícita:** la entrega declara qué porcentaje del requisito original cubre y qué queda pendiente. Esta información alimenta la matriz de trazabilidad del punto 9 y el dashboard de gobierno del punto 12.

---

## Estructura YAML del requisito con implementación parcial

El YAML del requisito mantiene exactamente la misma estructura de los cinco bloques definidos en el punto 1 del modelo operativo. La implementación parcial se gestiona añadiendo un bloque específico `entregas` que vive en el Bloque 5 (metadatos técnicos) y que el analista actualiza al inicio de cada sprint en que se trabaja sobre el requisito.

```yaml
# ─────────────────────────────────────────────────
# BLOQUE 1 — IDENTIDAD (sin cambios respecto al estándar)
# ─────────────────────────────────────────────────
id: REQ-031
titulo: "Configurar notificaciones por categoría desde el perfil de usuario"
version: "1.0"
estado: validado        # El estado del REQUISITO no cambia entre entregas.
                        # Solo cambia cuando todo el requisito está implementado.
epica: EP-06
modulo: "Gestión de perfil de usuario"
prioridad: should-have

# ─────────────────────────────────────────────────
# BLOQUE 2 — CONTEXTO DE NEGOCIO (sin cambios)
# ─────────────────────────────────────────────────
actor: "Usuario autenticado"
evento_disparador: >
  El usuario accede a la sección de notificaciones de su perfil
  para controlar qué comunicaciones recibe de la plataforma.
objetivo_negocio: >
  Reducir las solicitudes de baja de comunicaciones dirigidas al soporte
  (actualmente 40 por semana) permitiendo al usuario gestionar sus
  preferencias de forma autónoma.
descripcion: >
  El usuario autenticado debe poder activar y desactivar las notificaciones
  por categoría (Marketing, Operativas, Seguridad) desde su perfil, con
  efecto inmediato y confirmación visual del cambio.
reglas_negocio:
  - "Las notificaciones de categoría 'Seguridad' no pueden desactivarse."
  - "El cambio de preferencias tiene efecto en menos de 5 minutos."
  - "Cada cambio queda registrado en el log de auditoría del usuario."

# ─────────────────────────────────────────────────
# BLOQUE 3 — COMPORTAMIENTO ESPERADO (completo desde el inicio)
# Los criterios de aceptación del requisito son todos los del
# alcance completo, independientemente de cuántas entregas necesite.
# ─────────────────────────────────────────────────
criterios_aceptacion:
  - id: AC-031-01
    titulo: "Visualización del estado actual de notificaciones"
    dado: "El usuario está autenticado y accede a Perfil > Notificaciones"
    cuando: "La pantalla se carga"
    entonces: >
      Se muestran las categorías disponibles con su estado actual
      (activo/inactivo) representado mediante un toggle.
      La categoría 'Seguridad' aparece bloqueada y marcada como obligatoria.
    tipo: positivo

  - id: AC-031-02
    titulo: "Desactivación de una categoría permitida"
    dado: "El usuario está en la pantalla de notificaciones con 'Marketing' activo"
    cuando: "Pulsa el toggle de la categoría 'Marketing'"
    entonces: >
      El toggle cambia visualmente a inactivo de forma inmediata.
      Aparece el mensaje 'Preferencias guardadas'.
      En menos de 5 minutos el usuario deja de recibir notificaciones
      de esa categoría.
    tipo: positivo

  - id: AC-031-03
    titulo: "Intento de desactivar notificaciones de Seguridad"
    dado: "El usuario está en la pantalla de notificaciones"
    cuando: "Intenta pulsar el toggle de la categoría 'Seguridad'"
    entonces: >
      El toggle no responde. Se muestra el tooltip
      'Las notificaciones de Seguridad son obligatorias y no pueden desactivarse.'
    tipo: negativo

  - id: AC-031-04
    titulo: "Registro en el log de auditoría"
    dado: "El usuario ha realizado un cambio de preferencia"
    cuando: "El sistema procesa el cambio"
    entonces: >
      Se registra una entrada en el log de auditoría con:
      usuario_id, categoría modificada, estado anterior, estado nuevo,
      timestamp UTC y dirección IP de la sesión.
    tipo: positivo

  - id: AC-031-05
    titulo: "Histórico de cambios accesible desde el perfil"
    dado: "El usuario está en la pantalla de notificaciones"
    cuando: "Pulsa el enlace 'Ver historial de cambios'"
    entonces: >
      Se muestra la lista de los últimos 20 cambios de preferencias
      ordenados por fecha descendente, con fecha, categoría y acción.
    tipo: positivo

excepciones:
  - condicion: "El servicio de preferencias no responde en menos de 3 segundos"
    comportamiento: >
      El toggle vuelve a su estado anterior. Se muestra el mensaje
      'No se pudo guardar el cambio. Inténtalo de nuevo.' sin perder
      el resto de la sesión del usuario.
  - condicion: "El usuario pierde la sesión durante un cambio"
    comportamiento: >
      El cambio no se aplica si no fue confirmado por el servidor.
      Al reautenticarse, la pantalla muestra el estado guardado más reciente.

definition_of_done:
  - "Todos los criterios de aceptación de la entrega actual superan pruebas de regresión"
  - "Revisión de código aprobada por al menos un peer"
  - "Documentación técnica actualizada con el estado de implementación de cada entrega"

# ─────────────────────────────────────────────────
# BLOQUE 4 — DATOS (sin cambios respecto al estándar)
# ─────────────────────────────────────────────────
datos_entrada:
  - nombre: categoria_id
    tipo: enum
    valores_enum: ["marketing", "operativas", "seguridad"]
    requerido: true
  - nombre: estado_nuevo
    tipo: boolean
    requerido: true

datos_salida:
  campos: [categoria_id, estado_anterior, estado_nuevo, timestamp_cambio]
  formato: JSON
  tiempo_respuesta_max_ms: 3000

# ─────────────────────────────────────────────────
# BLOQUE 5 — METADATOS TÉCNICOS
# Aquí vive el bloque 'entregas', específico de este módulo.
# ─────────────────────────────────────────────────
componentes_afectados:
  - "api-perfil"
  - "frontend-perfil"
  - "servicio-notificaciones"
  - "bd-auditoria"

restricciones_no_funcionales:
  rendimiento: "Cambio aplicado en < 3 segundos p95"
  seguridad: "Log de auditoría inmutable. Solo lectura para el usuario."
  accesibilidad: "WCAG 2.1 AA. Toggles con label aria asociado."

# ─────────────────────────────────────────────────
# BLOQUE DE ENTREGAS — núcleo de este módulo
# Se añade al Bloque 5. Crece con cada sprint.
# ─────────────────────────────────────────────────
implementacion_parcial:
  activa: true
  motivo: >
    El equipo estimó 13 story points para el alcance completo.
    Se divide en dos entregas para encajar en el sprint de dos semanas
    y poder obtener feedback del negocio sobre la UX antes de implementar
    el histórico de cambios (AC-031-05), que tiene mayor complejidad técnica.
  porcentaje_completado: 60    # Actualizar tras cada entrega
  estado_implementacion: "en_progreso"
  # Valores posibles: pendiente | en_progreso | completado
  # 'completado' solo cuando TODAS las entregas están en estado Done en Jira

  entregas:

    - id: ENT-031-01
      sprint: "Sprint-08"
      fecha_planificacion: "2025-05-26"
      fecha_entrega_real: null      # Se rellena al cerrar el sprint
      estado: "planificada"
      # Valores: planificada | en_progreso | entregada | bloqueada

      descripcion: >
        Primera entrega: visualización del estado actual de notificaciones
        y capacidad de activar/desactivar categorías permitidas con
        confirmación visual inmediata. No incluye el log de auditoría
        ni el histórico de cambios.

      alcance_incluido:
        criterios_aceptacion: [AC-031-01, AC-031-02, AC-031-03]
        porcentaje_requisito: 40
        valor_negocio: >
          El usuario puede controlar sus preferencias de notificación
          de forma autónoma, eliminando la necesidad de contactar con soporte
          para las categorías Marketing y Operativas.

      alcance_excluido:
        criterios_aceptacion: [AC-031-04, AC-031-05]
        motivo_exclusion: >
          El log de auditoría y el histórico requieren un nuevo modelo
          de datos en bd-auditoria que necesita revisión de arquitectura.
          Se implementan en ENT-031-02 una vez confirmado el diseño.

      dependencias_tecnicas:
        - "Diseño de API de preferencias aprobado por el Tech Lead"
        - "Componente Toggle del design system disponible en v2.1"

      artefactos_jira:
        historia_key: null        # Se rellena tras el push
        tareas_keys: []
        test_cases_xray: []

      definition_of_done_entrega:
        - "AC-031-01, AC-031-02 y AC-031-03 superan pruebas de regresión"
        - "Accesibilidad WCAG 2.1 AA verificada en los toggles"
        - "Rendimiento: cambio aplicado en < 3 segundos en staging"

    - id: ENT-031-02
      sprint: "Sprint-10"           # Dos sprints después: Sprint-09 reservado
      fecha_planificacion: "2025-06-23"   # para revisión de arquitectura de BD
      fecha_entrega_real: null
      estado: "pendiente"

      descripcion: >
        Segunda entrega: registro en el log de auditoría con cada cambio
        e histórico de cambios accesible desde el perfil.

      alcance_incluido:
        criterios_aceptacion: [AC-031-04, AC-031-05]
        porcentaje_requisito: 60
        valor_negocio: >
          Cumplimiento del requisito de auditoría del proceso de gestión
          de preferencias. Permite al usuario revisar su historial de cambios
          y al área de soporte atender reclamaciones con evidencia.

      alcance_excluido:
        criterios_aceptacion: []
        motivo_exclusion: null

      dependencias_tecnicas:
        - "Modelo de datos bd-auditoria aprobado (decisión pendiente Sprint-09)"
        - "ENT-031-01 entregada y en producción"

      artefactos_jira:
        historia_key: null
        tareas_keys: []
        test_cases_xray: []

      definition_of_done_entrega:
        - "AC-031-04 y AC-031-05 superan pruebas de regresión"
        - "Log de auditoría verificado como inmutable"
        - "Documentación técnica del modelo de datos actualizada"
        - "Requisito REQ-031 marcado como completado en el repositorio"

trazabilidad:
  historias_generadas: []     # Acumula los keys de TODAS las entregas
  test_cases_generados: []
  jira_issues: []
```

---

## Ciclo de vida del estado del requisito con implementación parcial

El campo `estado` del requisito en el Bloque 1 tiene un significado diferente al habitual cuando hay implementación parcial. La siguiente tabla establece las reglas de transición:

```
ESTADO DEL REQUISITO    CONDICIÓN QUE LO ACTIVA
─────────────────────────────────────────────────────────────────
validado              → El requisito está aprobado para entrar al pipeline.
                        implementacion_parcial.estado_implementacion = pendiente

validado              → La primera entrega está planificada o en progreso.
(sin cambio)            implementacion_parcial.estado_implementacion = en_progreso

                        IMPORTANTE: el estado del REQUISITO no pasa a 'en_progreso'
                        porque eso indicaría que el análisis funcional está en curso,
                        no que el desarrollo lo está. Esta distinción es crítica
                        para que el pipeline de validación no bloquee el requisito.

completado            → Todas las entregas están en estado 'entregada' y
(nuevo estado)          el equipo técnico ha confirmado que el requisito
                        está completamente implementado en producción.
                        implementacion_parcial.estado_implementacion = completado
                        implementacion_parcial.porcentaje_completado = 100

deprecado             → El negocio cancela el requisito antes de completarlo.
                        Las entregas ya entregadas permanecen en producción.
                        Se documenta qué parte del alcance original quedó sin implementar.
```

El estado `completado` es nuevo respecto al modelo base del punto 1. Se añade específicamente para este módulo porque el estado `validado` no distingue entre "validado y pendiente de implementar" y "completamente implementado". Esta distinción es necesaria para que las consultas de trazabilidad del punto 9 puedan filtrar correctamente el estado real de cada requisito.

---

## Pipeline diferenciado por entrega

El orquestador del punto final del modelo operativo recibe un parámetro adicional `--entrega` que indica qué bloque `ENT-XXX-NN` debe procesar. Esto diferencia el comportamiento del pipeline en cada fase.

```bash
# Primera entrega
python orchestrator.py --req REQ-031 --entrega ENT-031-01

# Segunda entrega (sprints después)
python orchestrator.py --req REQ-031 --entrega ENT-031-02
```

### Paso 1 — Carga con contexto de entrega

El paso de carga del orquestador extrae tanto el requisito completo como el bloque específico de la entrega solicitada. El pipeline trabaja siempre con ambos: el requisito completo para el contexto y la entrega concreta para el alcance generado.

```python
def cargar_requisito_con_entrega(
    yaml_path: str,
    entrega_id: str
) -> tuple[dict, dict]:
    """
    Carga el requisito completo y extrae el bloque de la entrega solicitada.
    Retorna ambos por separado para que el pipeline los use según corresponda.
    """
    with open(yaml_path, encoding="utf-8") as f:
        requisito = yaml.safe_load(f)

    entregas = (
        requisito
        .get("implementacion_parcial", {})
        .get("entregas", [])
    )
    entrega = next(
        (e for e in entregas if e["id"] == entrega_id),
        None
    )

    if not entrega:
        raise ValueError(
            f"Entrega '{entrega_id}' no encontrada en {requisito['id']}. "
            f"Entregas disponibles: {[e['id'] for e in entregas]}"
        )

    # Verificar que las dependencias de esta entrega están satisfechas
    errores_dependencias = _verificar_dependencias_entrega(
        entrega, entregas
    )
    if errores_dependencias:
        raise DependenciaEntregaInsatisfecha(errores_dependencias)

    return requisito, entrega


def _verificar_dependencias_entrega(
    entrega: dict,
    todas_las_entregas: list[dict]
) -> list[str]:
    """
    Verifica que las entregas anteriores de las que depende esta
    están en estado 'entregada'. Si no, bloquea el pipeline.
    """
    errores = []
    id_entrega_actual = entrega["id"]

    # Extraer número de entrega del ID (ENT-031-02 → 2)
    num_actual = int(id_entrega_actual.split("-")[-1])

    for entrega_previa in todas_las_entregas:
        num_previo = int(entrega_previa["id"].split("-")[-1])

        # Solo revisar entregas anteriores a la actual
        if num_previo >= num_actual:
            continue

        # Las entregas anteriores deben estar entregadas
        if entrega_previa.get("estado") not in ("entregada",):
            errores.append(
                f"La entrega {entrega_previa['id']} está en estado "
                f"'{entrega_previa.get('estado', 'desconocido')}'. "
                f"Debe estar en estado 'entregada' antes de procesar "
                f"{id_entrega_actual}."
            )

    return errores
```

### Paso 2 — Validación adaptada al alcance de la entrega

El validador del punto 6 se ejecuta sobre el requisito completo, pero la puntuación de completitud funcional se evalúa solo sobre los criterios incluidos en la entrega actual. Los criterios excluidos no penalizan la validación: están documentados y diferidos de forma explícita, lo que es diferente a estar ausentes.

```python
async def validar_requisito_con_entrega(
    requisito: dict,
    entrega: dict,
    glosario: dict,
    config: PipelineConfig
) -> dict:
    """
    Ejecuta la validación del punto 6 con contexto de entrega parcial.
    Los criterios excluidos no generan errores de completitud.
    """
    criterios_incluidos = entrega["alcance_incluido"]["criterios_aceptacion"]
    criterios_excluidos = entrega["alcance_excluido"]["criterios_aceptacion"]

    # Construir una vista reducida del requisito
    # con solo los criterios de esta entrega
    requisito_entrega = {
        **requisito,
        "criterios_aceptacion": [
            ac for ac in requisito["criterios_aceptacion"]
            if ac["id"] in criterios_incluidos
        ],
        # Inyectar contexto de entrega para el validador
        "_contexto_entrega": {
            "entrega_id": entrega["id"],
            "es_implementacion_parcial": True,
            "criterios_diferidos": criterios_excluidos,
            "motivo_diferimiento": entrega["alcance_excluido"].get(
                "motivo_exclusion", ""
            ),
            "porcentaje_entrega": entrega["alcance_incluido"]["porcentaje_requisito"]
        }
    }

    # El system prompt del validador recibe el contexto de entrega
    # para que no marque los criterios diferidos como gaps de completitud
    system_prompt_adicional = f"""
CONTEXTO DE IMPLEMENTACIÓN PARCIAL:
Este requisito se implementa en entregas sucesivas.
La entrega actual ({entrega['id']}) cubre el {entrega['alcance_incluido']['porcentaje_requisito']}%
del alcance total.

Criterios diferidos a entregas posteriores (NO marcar como gaps):
{', '.join(criterios_excluidos)}

Motivo del diferimiento: {entrega['alcance_excluido'].get('motivo_exclusion', 'no especificado')}

Evalúa la completitud SOLO sobre los criterios incluidos en esta entrega.
Los criterios diferidos están documentados y son intencionales, no son omisiones.
    """

    return await validar_requisito(
        requisito=requisito_entrega,
        glosario=glosario,
        config=config,
        system_prompt_adicional=system_prompt_adicional
    )
```

### Paso 3 — Recuperación de contexto RAG con historia de entregas

El motor RAG del punto 7 tiene acceso a los chunks de las entregas anteriores del mismo requisito. Esto es crítico para evitar que el pipeline genere tareas técnicas duplicadas o inconsistentes con las ya implementadas en sprints anteriores.

```python
async def recuperar_contexto_rag_con_historia(
    requisito: dict,
    entrega_actual: dict,
    motor_rag: MotorConsultaRAG
) -> dict:
    """
    Recupera contexto RAG estándar más la historia de entregas anteriores.
    Permite al LLM generar artefactos coherentes con lo ya implementado.
    """
    req_id = requisito["id"]
    entrega_id = entrega_actual["id"]
    num_entrega_actual = int(entrega_id.split("-")[-1])

    # Contexto estándar del punto 7
    contexto_base = await motor_rag.recuperar_contexto_completo(requisito)

    # Recuperar artefactos de entregas anteriores del mismo requisito
    entregas_anteriores = [
        e for e in requisito.get("implementacion_parcial", {}).get("entregas", [])
        if int(e["id"].split("-")[-1]) < num_entrega_actual
        and e.get("estado") == "entregada"
    ]

    historia_implementacion = []
    for entrega_previa in entregas_anteriores:
        historia_implementacion.append({
            "entrega_id": entrega_previa["id"],
            "sprint": entrega_previa["sprint"],
            "criterios_implementados": (
                entrega_previa["alcance_incluido"]["criterios_aceptacion"]
            ),
            "historia_jira": (
                entrega_previa.get("artefactos_jira", {}).get("historia_key")
            ),
            "tareas_jira": (
                entrega_previa.get("artefactos_jira", {}).get("tareas_keys", [])
            ),
            "descripcion": entrega_previa.get("descripcion", "")
        })

    contexto_base["historia_entregas_anteriores"] = historia_implementacion

    return contexto_base
```

### Paso 4 — Generación de artefactos diferenciada

El prompt de generación de historias del punto 4 recibe información adicional sobre la entrega. Esto garantiza que la historia generada refleje exactamente el alcance de la entrega y no el del requisito completo, y que haga referencia explícita a lo que se entregó antes y lo que quedará para después.

```python
PROMPT_HISTORIA_ENTREGA_PARCIAL = """
A partir del requisito funcional y el bloque de entrega específico,
genera una Historia de Usuario Jira que represente ÚNICAMENTE el alcance
de esta entrega. No el requisito completo.

REQUISITO COMPLETO (para contexto):
{requisito_yaml}

ENTREGA A IMPLEMENTAR EN ESTE SPRINT:
{entrega_yaml}

ENTREGAS ANTERIORES YA IMPLEMENTADAS:
{historia_entregas}

INSTRUCCIONES ESPECÍFICAS PARA IMPLEMENTACIÓN PARCIAL:

1. El título de la historia debe indicar la fase:
   "Como [rol], quiero [acción de ESTA entrega] — Fase {num_entrega} de {total_entregas}"

2. La descripción debe incluir una sección 'Contexto de implementación':
   - Qué se implementó en entregas anteriores (si las hay)
   - Qué cubre esta entrega
   - Qué queda para entregas posteriores

3. Los criterios de aceptación deben ser SOLO los del campo
   'alcance_incluido.criterios_aceptacion' de la entrega.
   NO incluir los criterios del alcance_excluido.

4. La Definition of Done debe usar la
   'definition_of_done_entrega', no la del requisito completo.

5. Los story points deben estimarse para ESTA entrega,
   no para el requisito completo.

6. Añade el label 'entrega-parcial' y el label '{entrega_id}'
   a la historia para que sea identificable en Jira.

7. En el campo 'Requisito Origen' incluye tanto el ID del requisito
   como el ID de la entrega: '{req_id} / {entrega_id}'

{prompt_historia_estandar}
"""
```

El output de la historia refleja el alcance parcial con total transparencia para el equipo:

```json
{
  "issue_type": "Story",
  "summary": "Como usuario autenticado, quiero gestionar mis preferencias de notificación por categoría — Fase 1 de 2",
  "description": {
    "contexto_implementacion": {
      "entregas_anteriores": "Esta es la primera entrega. No hay implementación previa.",
      "esta_entrega": "Visualización del estado actual de notificaciones y capacidad de activar/desactivar categorías permitidas (Marketing, Operativas). No incluye el log de auditoría ni el historial.",
      "entregas_posteriores": "ENT-031-02 (Sprint-10) implementará el log de auditoría y el historial de cambios."
    },
    "narrativa": "Como usuario autenticado\nquiero activar y desactivar mis preferencias de notificación por categoría\npara dejar de recibir comunicaciones que no me interesan sin necesitar contactar con soporte",
    "flujo_principal": [
      "1. El usuario navega a Perfil > Notificaciones",
      "2. El sistema carga y muestra el estado actual de cada categoría",
      "3. El usuario pulsa el toggle de una categoría permitida",
      "4. El sistema confirma el cambio con el mensaje 'Preferencias guardadas'",
      "5. El cambio se propaga al servicio de notificaciones en < 5 minutos"
    ],
    "flujos_error": [
      {
        "condicion": "El servicio de preferencias no responde en 3 segundos",
        "comportamiento_esperado": "El toggle vuelve a su estado anterior con mensaje de error no bloqueante"
      }
    ]
  },
  "acceptance_criteria": [
    {
      "id": "AC-031-01",
      "dado": "El usuario está autenticado y accede a Perfil > Notificaciones",
      "cuando": "La pantalla se carga",
      "entonces": "Se muestran las categorías con su estado actual mediante toggles. 'Seguridad' aparece bloqueada."
    },
    {
      "id": "AC-031-02",
      "dado": "El usuario está en la pantalla con 'Marketing' activo",
      "cuando": "Pulsa el toggle de 'Marketing'",
      "entonces": "El toggle cambia a inactivo. Aparece 'Preferencias guardadas'. El efecto se aplica en < 5 minutos."
    },
    {
      "id": "AC-031-03",
      "dado": "El usuario está en la pantalla de notificaciones",
      "cuando": "Intenta pulsar el toggle de 'Seguridad'",
      "entonces": "El toggle no responde. Se muestra el tooltip informativo."
    }
  ],
  "definition_of_done": [
    "AC-031-01, AC-031-02 y AC-031-03 superan pruebas de regresión",
    "Accesibilidad WCAG 2.1 AA verificada en los toggles",
    "Rendimiento: cambio aplicado en < 3 segundos en staging"
  ],
  "story_points": 5,
  "labels": ["entrega-parcial", "ENT-031-01", "perfil", "notificaciones"],
  "custom_fields": {
    "requisito_origen": "REQ-031 / ENT-031-01",
    "modulo_funcional": "EP-06"
  }
}
```

### Paso 5 — Generación de test cases por entrega

Los test cases se generan exclusivamente para los criterios de la entrega actual. El sistema mantiene un índice de qué criterios del requisito ya tienen cobertura de test, acumulado a través de todas las entregas previas.

```python
async def generar_test_cases_entrega(
    historia: dict,
    requisito: dict,
    entrega: dict,
    entregas_anteriores: list[dict],
    config: PipelineConfig
) -> dict:
    """
    Genera test cases solo para los criterios de la entrega actual.
    Verifica que los criterios de entregas anteriores ya tienen cobertura
    para construir la suite de regresión incremental.
    """
    criterios_esta_entrega = entrega["alcance_incluido"]["criterios_aceptacion"]

    # Calcular qué criterios ya tienen test cases de entregas anteriores
    criterios_con_cobertura_previa = []
    for entrega_prev in entregas_anteriores:
        criterios_con_cobertura_previa.extend(
            entrega_prev["alcance_incluido"]["criterios_aceptacion"]
        )

    # Generar test cases nuevos para esta entrega
    test_cases_nuevos = await _generar_test_cases_para_criterios(
        criterios_ids=criterios_esta_entrega,
        historia=historia,
        requisito=requisito,
        config=config
    )

    # Recuperar test cases de regresión de entregas anteriores
    # para incluirlos en la suite del sprint actual
    test_cases_regresion = await _recuperar_tcs_regresion(
        criterios_ids=criterios_con_cobertura_previa,
        requisito_id=requisito["id"],
        config=config
    )

    return {
        "test_cases_nuevos": test_cases_nuevos,
        "test_cases_regresion": test_cases_regresion,
        "suite_completa": test_cases_nuevos + test_cases_regresion,
        "cobertura_acumulada": {
            "criterios_cubiertos": (
                criterios_esta_entrega + criterios_con_cobertura_previa
            ),
            "criterios_pendientes": entrega["alcance_excluido"]["criterios_aceptacion"],
            "porcentaje": entrega["alcance_incluido"]["porcentaje_requisito"]
                          + sum(
                              e["alcance_incluido"]["porcentaje_requisito"]
                              for e in entregas_anteriores
                          )
        }
    }
```

La suite de regresión es un elemento diferenciador de este módulo. Cada sprint que se trabaja sobre un requisito con implementación parcial, los test cases de las entregas anteriores se re-ejecutan automáticamente como pruebas de regresión. Esto garantiza que la segunda entrega no rompe lo que la primera entregó.

---

## Actualización del grafo de trazabilidad por entrega

El grafo del punto 9 introduce un nuevo tipo de nodo y dos nuevas aristas para representar correctamente la implementación parcial.

### Nuevo tipo de nodo: `entrega`

```sql
-- El nodo de entrega es el puente entre el requisito y los artefactos Jira
-- de cada sprint. Permite consultar la trazabilidad en cualquier corte temporal.
INSERT INTO nodos_trazabilidad (id, tipo, titulo, estado, metadatos)
VALUES (
    'ENT-031-01',
    'entrega',
    'REQ-031 — Fase 1 de 2 (Sprint-08)',
    'planificada',
    '{
        "requisito_id": "REQ-031",
        "sprint": "Sprint-08",
        "porcentaje": 40,
        "criterios": ["AC-031-01", "AC-031-02", "AC-031-03"]
    }'
);
```

### Nuevas aristas en el grafo

```
REQ-031 ──[tiene_entrega]──→ ENT-031-01
REQ-031 ──[tiene_entrega]──→ ENT-031-02

ENT-031-01 ──[genera]──→ FACT-67 (Historia Jira sprint 8)
ENT-031-01 ──[genera]──→ FACT-68 (Tarea backend sprint 8)
ENT-031-01 ──[genera]──→ FACT-69 (Tarea frontend sprint 8)

ENT-031-02 ──[depende_de]──→ ENT-031-01
ENT-031-02 ──[genera]──→ FACT-89 (Historia Jira sprint 10)

FACT-71 (TC positivo) ──[verifica]──→ ENT-031-01
FACT-72 (TC negativo) ──[verifica]──→ ENT-031-01
FACT-73 (TC regresión) ──[verifica]──→ ENT-031-02
                         └──[origen]──→ ENT-031-01
```

```python
def registrar_entrega_en_grafo(
    motor: MotorTrazabilidad,
    requisito_id: str,
    entrega: dict,
    historia_key: str,
    tareas_keys: list[str],
    test_cases_keys: list[str],
    test_cases_regresion_keys: list[str]
):
    """
    Registra todos los nodos y aristas de una entrega en el grafo.
    Mantiene la trazabilidad completa entre requisito, entrega y artefactos Jira.
    """
    entrega_id = entrega["id"]

    # Nodo de la entrega
    motor.registrar_nodo(Nodo(
        id=entrega_id,
        tipo="entrega",
        titulo=f"{requisito_id} — {entrega_id}",
        estado=entrega.get("estado", "planificada"),
        metadatos={
            "requisito_id": requisito_id,
            "sprint": entrega.get("sprint"),
            "porcentaje": entrega["alcance_incluido"]["porcentaje_requisito"],
            "criterios": entrega["alcance_incluido"]["criterios_aceptacion"]
        }
    ))

    # REQ → ENT (el requisito tiene esta entrega)
    motor.registrar_arista(Arista(
        origen_id=requisito_id,
        destino_id=entrega_id,
        tipo_relacion="tiene_entrega",
        confianza=1.0,
        origen_relacion="pipeline_generacion"
    ))

    # ENT → Historia Jira
    motor.registrar_arista(Arista(
        origen_id=entrega_id,
        destino_id=historia_key,
        tipo_relacion="genera",
        confianza=1.0,
        origen_relacion="pipeline_generacion"
    ))

    # ENT → Tareas técnicas
    for tarea_key in tareas_keys:
        motor.registrar_arista(Arista(
            origen_id=entrega_id,
            destino_id=tarea_key,
            tipo_relacion="genera",
            confianza=1.0,
            origen_relacion="pipeline_generacion"
        ))

    # TCs nuevos → ENT (verifican esta entrega)
    for tc_key in test_cases_keys:
        motor.registrar_arista(Arista(
            origen_id=tc_key,
            destino_id=entrega_id,
            tipo_relacion="verifica",
            confianza=1.0,
            origen_relacion="pipeline_generacion"
        ))

    # TCs de regresión → ENT actual (también la verifican)
    # con metadato que indica que son herencia de una entrega anterior
    for tc_key in test_cases_regresion_keys:
        motor.registrar_arista(Arista(
            origen_id=tc_key,
            destino_id=entrega_id,
            tipo_relacion="verifica",
            confianza=0.9,
            origen_relacion="regresion_entrega_anterior",
            metadatos={"tipo": "regresion"}
        ))
```

---

## Consultas de trazabilidad específicas para implementación parcial

El consultor de trazabilidad del punto 9 incorpora dos nuevas consultas que solo tienen sentido en el contexto de implementación parcial.

### Consulta 1: Estado de implementación de un requisito

```python
def estado_implementacion_requisito(
    self,
    requisito_id: str
) -> dict:
    """
    Retorna el estado completo de implementación de un requisito
    con implementación parcial: qué se ha entregado, qué está en curso
    y qué queda pendiente.
    """
    with self.db.cursor() as cur:
        cur.execute("""
            SELECT
                n_ent.id                         AS entrega_id,
                n_ent.estado                     AS estado_entrega,
                n_ent.metadatos->>'sprint'        AS sprint,
                n_ent.metadatos->>'porcentaje'    AS porcentaje,
                n_ent.metadatos->'criterios'      AS criterios,
                COUNT(DISTINCT n_hist.id)
                    FILTER (WHERE n_hist.tipo = 'historia') AS historias,
                COUNT(DISTINCT n_tc.id)
                    FILTER (WHERE n_tc.tipo = 'test_case') AS test_cases,
                COUNT(DISTINCT n_tc.id)
                    FILTER (
                        WHERE n_tc.tipo = 'test_case'
                        AND n_tc.estado = 'pasado'
                    )                            AS test_cases_pasados
            FROM nodos_trazabilidad n_ent
            LEFT JOIN aristas_trazabilidad a_hist
                ON a_hist.origen_id = n_ent.id
                AND a_hist.tipo_relacion = 'genera'
            LEFT JOIN nodos_trazabilidad n_hist
                ON n_hist.id = a_hist.destino_id
            LEFT JOIN aristas_trazabilidad a_tc
                ON a_tc.destino_id = n_ent.id
                AND a_tc.tipo_relacion = 'verifica'
            LEFT JOIN nodos_trazabilidad n_tc
                ON n_tc.id = a_tc.origen_id
            WHERE n_ent.tipo = 'entrega'
              AND n_ent.metadatos->>'requisito_id' = %s
              AND n_ent.activo = TRUE
            GROUP BY n_ent.id, n_ent.estado, n_ent.metadatos
            ORDER BY n_ent.id
        """, (requisito_id,))

        entregas = cur.fetchall()

    porcentaje_total = sum(
        int(e[3] or 0) for e in entregas
        if e[1] == "entregada"
    )

    return {
        "requisito_id": requisito_id,
        "porcentaje_implementado": porcentaje_total,
        "estado_global": (
            "completado"    if porcentaje_total == 100 else
            "en_progreso"   if porcentaje_total > 0   else
            "pendiente"
        ),
        "entregas": [
            {
                "id": e[0],
                "estado": e[1],
                "sprint": e[2],
                "porcentaje_del_requisito": int(e[3] or 0),
                "criterios_cubiertos": e[4],
                "historias": e[5],
                "test_cases": e[6],
                "test_cases_pasados": e[7],
                "lista_para_produccion": (
                    e[1] == "entregada"
                    and e[6] > 0
                    and e[6] == e[7]
                )
            }
            for e in entregas
        ]
    }
```

### Consulta 2: Requisitos parcialmente implementados en el proyecto

```python
def requisitos_implementacion_incompleta(
    self,
    epica_id: str = None
) -> list[dict]:
    """
    Lista todos los requisitos con implementación parcial activa
    que aún no están completamente implementados.
    Útil para el dashboard de governance del punto 12.
    """
    filtro_epica = (
        f"AND n_req.metadatos->>'epica' = '{epica_id}'"
        if epica_id else ""
    )

    with self.db.cursor() as cur:
        cur.execute(f"""
            SELECT
                n_req.id,
                n_req.titulo,
                n_req.metadatos->>'epica'    AS epica,
                COUNT(n_ent.id)              AS total_entregas,
                COUNT(n_ent.id)
                    FILTER (WHERE n_ent.estado = 'entregada') AS entregas_completadas,
                COUNT(n_ent.id)
                    FILTER (WHERE n_ent.estado = 'en_progreso') AS entregas_en_curso,
                COUNT(n_ent.id)
                    FILTER (WHERE n_ent.estado = 'pendiente') AS entregas_pendientes,
                SUM((n_ent.metadatos->>'porcentaje')::int)
                    FILTER (WHERE n_ent.estado = 'entregada') AS porcentaje_completado
            FROM nodos_trazabilidad n_req
            JOIN aristas_trazabilidad a_ent
                ON a_ent.origen_id = n_req.id
                AND a_ent.tipo_relacion = 'tiene_entrega'
            JOIN nodos_trazabilidad n_ent
                ON n_ent.id = a_ent.destino_id
                AND n_ent.tipo = 'entrega'
            WHERE n_req.tipo = 'requisito'
              AND n_req.estado != 'completado'
              AND n_req.activo = TRUE
              {filtro_epica}
            GROUP BY n_req.id, n_req.titulo, n_req.metadatos
            HAVING COUNT(n_ent.id) > 0
               AND COUNT(n_ent.id)
                   FILTER (WHERE n_ent.estado = 'entregada') < COUNT(n_ent.id)
            ORDER BY porcentaje_completado DESC
        """)

        return [
            {
                "requisito_id": row[0],
                "titulo": row[1],
                "epica": row[2],
                "total_entregas": row[3],
                "entregas_completadas": row[4],
                "entregas_en_curso": row[5],
                "entregas_pendientes": row[6],
                "porcentaje_completado": row[7] or 0,
                "alerta": (
                    "bloqueada"
                    if row[5] == 0 and row[6] > 0 else
                    "en_progreso"
                )
            }
            for row in self.db.cursor().fetchall()
        ]
```

---

## Actualización del YAML tras cada entrega

Cuando el equipo cierra el sprint y la entrega se confirma como `Done` en Jira, el pipeline ejecuta un paso de cierre que actualiza el YAML del requisito con los datos reales de la entrega. Este paso es automático y se dispara vía webhook de Jira al cambiar el estado de la historia al estado `Done`.

```python
async def cerrar_entrega(
    requisito_id: str,
    entrega_id: str,
    historia_key: str,
    config: PipelineConfig
):
    """
    Actualiza el YAML del requisito al cerrar una entrega en Jira.
    Marca la entrega como 'entregada', registra los artefactos reales
    y actualiza el porcentaje de implementación global.
    """
    ruta_yaml = _encontrar_yaml(requisito_id, config)
    requisito = yaml.safe_load(ruta_yaml.read_text())

    entregas = requisito["implementacion_parcial"]["entregas"]
    entrega = next(e for e in entregas if e["id"] == entrega_id)

    # Actualizar la entrega cerrada
    entrega["estado"] = "entregada"
    entrega["fecha_entrega_real"] = datetime.now().strftime("%Y-%m-%d")
    entrega["artefactos_jira"]["historia_key"] = historia_key

    # Recalcular porcentaje global
    porcentaje_acumulado = sum(
        e["alcance_incluido"]["porcentaje_requisito"]
        for e in entregas
        if e.get("estado") == "entregada"
    )
    requisito["implementacion_parcial"]["porcentaje_completado"] = porcentaje_acumulado

    # Si todas las entregas están completadas, marcar el requisito
    todas_entregadas = all(
        e.get("estado") == "entregada" for e in entregas
    )
    if todas_entregadas and porcentaje_acumulado >= 100:
        requisito["implementacion_parcial"]["estado_implementacion"] = "completado"
        requisito["estado"] = "completado"

    # Persistir el YAML actualizado
    with open(ruta_yaml, "w", encoding="utf-8") as f:
        yaml.dump(requisito, f, allow_unicode=True, default_flow_style=False)

    # Re-indexar el requisito actualizado en el RAG
    repositorio_rag.indexar_requisito_completo(str(ruta_yaml))

    return {
        "requisito_id": requisito_id,
        "entrega_cerrada": entrega_id,
        "porcentaje_completado": porcentaje_acumulado,
        "requisito_completado": todas_entregadas
    }
```

---

## Impacto en el glosario y en el RAG

La implementación parcial introduce un riesgo terminológico específico que el modelo estándar no contempla: entre la primera y la segunda entrega de un requisito pueden pasar varias semanas, y el glosario puede haber evolucionado. Si el término oficial de un actor cambia entre la ENT-031-01 y la ENT-031-02, el pipeline de la segunda entrega generará artefactos con terminología diferente a los de la primera.

La solución es anclar la versión del glosario utilizada en cada entrega:

```yaml
# En el bloque de cada entrega
- id: ENT-031-01
  sprint: "Sprint-08"
  version_glosario: "1.3"    # Versión del glosario activa en el momento
                              # de planificar esta entrega.
                              # El pipeline usa SIEMPRE la versión declarada aquí,
                              # no la versión actual del glosario.
```

Si la versión del glosario de la entrega anterior difiere de la actual en términos que afectan a los criterios de la nueva entrega, el pipeline emite una advertencia y sugiere una revisión de coherencia terminológica antes de generar los artefactos.

---

## Integración con el sistema de gobierno del punto 12

El dashboard de gobierno incorpora una sección específica para el seguimiento de la implementación parcial. Las métricas adicionales que se monitorizan son:

**Requisitos con implementación paralizada.** Requisitos que llevan más de dos sprints con una entrega en estado `en_progreso` o `planificada` sin avanzar. Indican dependencias técnicas no resueltas, bloqueos de negocio o pérdida de prioridad sin documentar.

**Tiempo medio entre entregas.** Si el tiempo entre la primera y la segunda entrega de un requisito supera los tres sprints, el riesgo de inconsistencia aumenta significativamente: el contexto del equipo cambia, el glosario evoluciona y la deuda de trazabilidad crece.

**Cobertura de regresión acumulada.** Porcentaje de test cases de entregas anteriores que se re-ejecutan en el sprint de la entrega siguiente. El objetivo es 100%: todas las entregas anteriores deben tener cobertura de regresión activa en el sprint de cada nueva entrega.

**Requisitos completados en el sprint objetivo.** Porcentaje de requisitos con implementación parcial que se completan en el sprint planificado para su última entrega. Un valor bajo indica que la planificación inicial de las entregas no es realista.

---

## Checklist del analista para implementación parcial

### Al definir el plan de entregas (antes del primer sprint)

```
□ ¿Cada entrega tiene valor de negocio independiente y demostrable?
□ ¿Los criterios de aceptación están repartidos sin solapamiento entre entregas?
□ ¿Las dependencias técnicas entre entregas están declaradas explícitamente?
□ ¿El sprint asignado a cada entrega es realista dado el sprint actual?
□ ¿La suma de porcentajes de todas las entregas es exactamente 100?
□ ¿Se ha informado al product owner del plan de entregas y lo ha aprobado?
□ ¿Se ha registrado la versión del glosario activa en cada entrega?
```

### Al ejecutar el pipeline de una entrega

```
□ ¿Las entregas anteriores están en estado 'entregada'?
□ ¿El orquestador se ha invocado con --entrega ENT-XXX-NN?
□ ¿La historia generada referencia explícitamente qué fase es y qué queda?
□ ¿Los test cases generados son solo los de esta entrega?
□ ¿La suite de regresión incluye los test cases de entregas anteriores?
```

### Al cerrar el sprint con una entrega completada

```
□ ¿Se ha ejecutado el paso de cierre de entrega para actualizar el YAML?
□ ¿El porcentaje de implementación del requisito se ha actualizado correctamente?
□ ¿Si era la última entrega, el estado del requisito es ahora 'completado'?
□ ¿Los test cases de esta entrega se han añadido a la suite de regresión permanente?
□ ¿Los artefactos Jira de la entrega están registrados en el bloque 'artefactos_jira'?
```

---

> **Nota de implementación:** Este módulo se activa junto con el de gestión de requisitos deprecados o divididos en la Fase 2 del roadmap (semi-automatización). El requisito previo es que el equipo tenga al menos dos meses de experiencia con el pipeline estándar y que la plantilla YAML base esté estabilizada. Introducir el bloque `implementacion_parcial` antes de que la plantilla base sea estable genera deuda de adaptación: cada cambio en los cinco bloques principales obliga a revisar también la estructura de entregas.
>
> En proyectos donde la implementación parcial es la norma y no la excepción (proyectos de más de seis meses con equipos pequeños), considerar activar este módulo desde la Fase 1 con una versión simplificada del bloque `entregas` que solo registre los campos imprescindibles: `id`, `sprint`, `criterios_aceptacion` y `estado`.
