# Punto 1 — Taller de plantillas

## Qué es y qué no es este taller

El objetivo no es diseñar un formulario bonito. Es diseñar el **contrato de datos** entre el analista funcional, la IA y las herramientas (Jira, Xray, Confluence). Cada campo que entra en la plantilla tiene un coste de mantenimiento. Cada campo que falta tiene un coste en calidad de los artefactos generados.

La plantilla tiene que satisfacer simultáneamente a tres audiencias con necesidades distintas:

| Audiencia | Lo que necesita de la plantilla |
|---|---|
| Usuario de negocio | Lenguaje natural, sin jerga técnica, campos comprensibles |
| Analista funcional | Estructura que guíe sin encorsetar, campos que reduzcan el trabajo |
| Pipeline de IA | Campos atómicos, vocabulario controlado, sin texto libre donde pueda evitarse |

Cuando estas tres necesidades entran en conflicto, la prioridad es: **usuario de negocio primero, IA segundo, analista tercero**. El analista es el profesional que puede adaptarse. El usuario de negocio no debería tener que hacerlo. Y la IA no puede interpretar lo que no está.

---

## Fase 1 — Inventario de campos (antes del taller)

Antes de sentarse a diseñar la plantilla, el analista responsable debe hacer este ejercicio durante 30 minutos: revisar los últimos 10 documentos funcionales del equipo e identificar qué información aparece siempre, qué aparece a veces y qué nunca aparece pero siempre hace falta durante el refinamiento.

El resultado típico de ese ejercicio es este patrón:

```
APARECE SIEMPRE (pero en formatos distintos):
  - Descripción del requisito
  - Quién lo pidió
  - Para qué sirve
  - Qué debe hacer el sistema

APARECE A VECES (cuando el analista lo recuerda):
  - Qué pasa si algo falla
  - Qué datos entran y salen
  - Qué rol tiene permiso

NUNCA APARECE (pero siempre se pregunta en refinamiento):
  - Casos de contorno
  - Rendimiento esperado
  - Dependencias con otros requisitos
  - Criterios de aceptación verificables
```

Este inventario es la base para decidir qué campos son obligatorios, cuáles opcionales y cuáles no entran en la plantilla pero se recogen en otro lugar.

---

## Fase 2 — Anatomía de la plantilla completa

La plantilla tiene cinco bloques. Cada bloque tiene una responsabilidad distinta y se procesa de forma diferente por la IA.

| Bloque | Propósito | Audiencia principal | Uso por la IA |
|---|---|---|---|
| **Bloque 1 — Identidad** | Identificar, versionar y enrutar el requisito | Todos | Clave de trazabilidad |
| **Bloque 2 — Contexto de negocio** | Dar el "por qué" para generar historias con valor real | Negocio | Narrativa de la historia y tareas técnicas |
| **Bloque 3 — Comportamiento esperado** | Definir qué debe hacer el sistema de forma verificable | Analista + QA | Fuente principal de test cases |
| **Bloque 4 — Datos** | Especificar la forma de los datos para casos de contorno | Técnico | Casos de contorno y validaciones |
| **Bloque 5 — Metadatos técnicos** | Dar contexto al equipo técnico para tareas técnicas | Técnico | Tareas técnicas y dependencias Jira |

**Responsabilidades por rol:**
El analista rellena los bloques 1, 2 y 3. El equipo técnico completa el bloque 4 y 5 durante el refinamiento. La IA valida la completitud antes del pipeline.

---

## Fase 3 — La plantilla completa comentada

Esta es la plantilla de referencia. Los comentarios explican **por qué existe cada campo** y qué ocurre si falta.

```yaml
# ─────────────────────────────────────────────
# BLOQUE 1 — IDENTIDAD
# Propósito: identificar, versionar y enrutar el requisito
# ─────────────────────────────────────────────

id: REQ-000
# Formato: REQ-NNN. Nunca reutilizar IDs aunque el requisito se elimine.
# La IA usa este campo como clave en la matriz de trazabilidad.

titulo: ""
# Máximo 80 caracteres. Empieza por sustantivo o verbo en infinitivo.
# Incorrecto: "Gestión de facturas" (ambiguo)
# Correcto:   "Filtrar facturas por rango de fechas"

version: "1.0"
# Incrementar el menor (1.1, 1.2) para cambios menores.
# Incrementar el mayor (2.0) si cambia el comportamiento esperado.
# La IA detecta cambios de versión para regenerar artefactos afectados.

estado: borrador
# Valores permitidos (vocabulario controlado):
#   borrador        → en elaboración, no válido para pipeline
#   en-revision     → enviado a validación con negocio
#   validado        → aprobado, puede entrar al pipeline de generación
#   rechazado       → descartado, no eliminar del repositorio
#   deprecado       → sustituido por otro requisito (indicar sucesor)

sucesor: null
# Solo si estado = deprecado. Formato: REQ-NNN

epica: EP-00
# Formato: EP-NN. Debe existir en el catálogo de épicas.
# La IA usa este campo para vincular la historia a la épica correcta en Jira.

modulo: ""
# Nombre legible del módulo de negocio. Ej: "Gestión de Facturación"
# Para usuarios de negocio que no trabajan con IDs.

origen:
  solicitante: ""     # Nombre completo de quien pide el requisito
  area: ""            # Departamento o área de negocio
  fecha_solicitud: "" # Formato: YYYY-MM-DD
  referencia: ""      # Número de ticket, email, acta de reunión donde se originó

fecha_creacion: ""    # YYYY-MM-DD — auto-rellenado por la plantilla si es posible
fecha_validacion: ""  # YYYY-MM-DD — rellenado al mover a estado 'validado'
analista: ""          # Nombre del analista responsable


# ─────────────────────────────────────────────
# BLOQUE 2 — CONTEXTO DE NEGOCIO
# Propósito: dar a la IA el "por qué" para generar
# historias con valor de negocio real, no solo técnicas
# ─────────────────────────────────────────────

actor: ""
# El rol específico que ejecuta la acción principal.
# DEBE existir en el glosario de actores del proyecto.
# Incorrecto: "el usuario", "el cliente", "el sistema"
# Correcto:   "Gestor de facturación", "Responsable financiero"

actores_secundarios: []
# Roles que intervienen pero no son el actor principal.

evento_disparador: ""
# Qué situación concreta activa este requisito.
# Incorrecto: "cuando el usuario lo necesita"
# Correcto:   "El gestor accede al módulo Facturas para el cierre mensual"

objetivo_negocio: ""
# Por qué existe este requisito. Qué problema de negocio resuelve.
# Mínimo 20 palabras. La IA usa este campo para generar el 'para qué'
# de la historia de usuario y la justificación de la épica.

descripcion: ""
# Narrativa del requisito en lenguaje de negocio.
# Mínimo 30 palabras. Sin tecnicismos.
# La IA usa este campo para generar el contexto de la historia.

prioridad: must-have
# Valores permitidos (MoSCoW):
#   must-have    → crítico para el MVP, sin esto no hay entrega
#   should-have  → importante pero no bloqueante para el lanzamiento
#   could-have   → deseable si hay capacidad
#   wont-have    → descartado para este release, documentado para el futuro

reglas_negocio:
  - ""
# Lista de restricciones, condiciones y políticas de negocio.
# Cada regla debe ser una afirmación verificable.
# Incorrecto: "Los datos deben ser correctos"
# Correcto:   "Solo se muestran facturas del ejercicio fiscal en curso (año natural)"
# IMPORTANTE: Cada regla de negocio debe tener al menos un criterio de
# aceptación en el Bloque 3 que la verifique.

dependencias:
  requisitos: []      # IDs de requisitos que deben estar implementados antes
  sistemas: []        # Sistemas externos de los que depende
  decisiones: []      # Decisiones de negocio pendientes que podrían afectarlo


# ─────────────────────────────────────────────
# BLOQUE 3 — COMPORTAMIENTO ESPERADO
# Propósito: definir qué debe hacer el sistema de forma
# verificable. Es la fuente principal de test cases.
# ─────────────────────────────────────────────

flujo_principal:
  - paso: 1
    actor: ""         # Quién ejecuta este paso: el usuario o "sistema"
    accion: ""        # Qué hace
    resultado: ""     # Qué ocurre como consecuencia

# Documenta el camino feliz paso a paso.
# Máximo 10 pasos. Si necesita más, el requisito es demasiado grande.

flujos_alternativos:
  - condicion: ""     # Cuándo se activa este flujo alternativo
    pasos:
      - paso: 1
        actor: ""
        accion: ""
        resultado: ""

excepciones:
  - condicion: ""     # Condición de error o caso no esperado
    comportamiento: ""# Qué debe hacer el sistema (mensaje, redirección, log...)

# REGLA: Mínimo una excepción por cada campo obligatorio de entrada.

criterios_aceptacion:
  - id: AC-000-01
    titulo: ""        # Resumen de una línea de lo que verifica este criterio
    dado: ""          # Estado previo del sistema y del actor
    cuando: ""        # UNA acción concreta. Solo una.
    entonces: ""      # Resultado observable. Verificable con true/false.
    tipo: positivo    # positivo | negativo | contorno
    datos_ejemplo:    # Datos concretos para este criterio específico
      campo: valor

# REGLAS DE ORO PARA LOS CRITERIOS:
# 1. El 'dado' describe un ESTADO, no una acción.
#    Mal: "Dado que el usuario ha hecho clic en Facturas"
#    Bien: "Dado que el usuario está en la pantalla de listado de Facturas"
# 2. El 'cuando' describe UNA SOLA acción.
#    Mal: "Cuando filtra y ordena y exporta"
#    Bien: "Cuando pulsa el botón Buscar"
# 3. El 'entonces' describe algo que se VE o se MIDE.
#    Mal: "Entonces el sistema funciona correctamente"
#    Bien: "Entonces el listado muestra las facturas ordenadas por fecha
#           descendente en menos de 2 segundos"
# 4. Mínimo un criterio por cada regla de negocio.
# 5. Mínimo un criterio negativo por cada validación de campo.

definition_of_done:
  - "Todos los criterios de aceptación superan las pruebas de regresión"
  - "Revisión de código aprobada"
  - ""  # Añadir criterios específicos del requisito aquí


# ─────────────────────────────────────────────
# BLOQUE 4 — DATOS
# Propósito: especificar la forma de los datos para
# que la IA genere casos de contorno correctos y el
# equipo técnico implemente validaciones precisas
# ─────────────────────────────────────────────

datos_entrada:
  - nombre: ""
    tipo: ""
    # Tipos permitidos: string | integer | decimal | boolean |
    #                   date | datetime | enum | file | array | object
    requerido: true
    formato: ""       # ISO-8601 para fechas, regex para patrones, etc.
    longitud_max: null# Solo para string
    rango:
      min: null       # Para integer, decimal, date
      max: null
    valores_enum: []  # Solo si tipo = enum. Lista de valores permitidos.
    valor_defecto: null
    descripcion: ""   # Explicación en lenguaje de negocio

datos_salida:
  campos: []          # Lista de campos que devuelve el sistema
  formato: ""         # JSON | CSV | PDF | pantalla | email
  paginacion:
    aplica: false
    tamanyo_pagina_defecto: null
    max_registros: null
  orden_defecto: ""   # Campo y dirección. Ej: "fecha_factura DESC"
  tiempo_respuesta_max_ms: null


# ─────────────────────────────────────────────
# BLOQUE 5 — METADATOS TÉCNICOS
# Propósito: dar contexto al equipo técnico y a la IA
# para generar tareas técnicas relevantes.
# Este bloque lo completa el equipo técnico en el refinamiento.
# ─────────────────────────────────────────────

componentes_afectados: []
# Lista de componentes del sistema que requieren cambios.
# Ej: ["api-facturacion", "frontend-facturas", "bd-principal"]

integraciones_externas: []
# Sistemas externos con los que interactúa este requisito.

restricciones_no_funcionales:
  rendimiento: ""     # Ej: "< 2 segundos p95 con 100 usuarios concurrentes"
  seguridad: ""       # Ej: "Solo accesible con rol gestor_facturacion. Audit log."
  disponibilidad: ""  # Ej: "99.5% uptime. Degradación controlada si BD no responde."
  accesibilidad: ""   # Ej: "WCAG 2.1 AA"
  volumen_datos: ""   # Ej: "Hasta 100.000 facturas por empresa"

notas_implementacion: ""
# Orientaciones técnicas no prescriptivas para el desarrollador.

trazabilidad:
  historias_generadas: []   # Auto-rellenado por el pipeline. No editar a mano.
  test_cases_generados: []  # Auto-rellenado por el pipeline. No editar a mano.
  jira_issues: []           # Auto-rellenado por el pipeline. No editar a mano.
```

---

## Fase 4 — Decisiones de adaptación que hay que tomar en el taller

### Decisión 1: ¿Cuántos campos obligatorios?

La tentación es marcar todo como obligatorio. Es un error. Un campo obligatorio que nadie puede rellenar en el momento de la captura se convierte en un bloqueo que el analista sortea poniendo texto basura ("N/A", "TBD", "pendiente") que inutiliza el campo para la IA.

La regla práctica es: **un campo es obligatorio si su ausencia hace que el pipeline genere artefactos incorrectos o incompletos**.

Para la mayoría de organizaciones, el conjunto mínimo bloqueante es:

```yaml
# OBLIGATORIOS BLOQUEANTES (sin estos, el pipeline no arranca):
- id
- titulo
- epica
- estado
- actor
- descripcion          # mínimo 30 palabras
- evento_disparador
- prioridad
- criterios_aceptacion # mínimo 1, con dado/cuando/entonces completos
- excepciones          # mínimo 1

# RECOMENDADOS (advertencia si faltan):
- objetivo_negocio
- reglas_negocio
- flujo_principal
- datos_entrada        # si el requisito tiene inputs
- datos_salida         # si el requisito devuelve datos

# OPCIONALES (sin impacto en el pipeline básico):
- restricciones_no_funcionales
- notas_implementacion
- integraciones_externas
```

### Decisión 2: ¿Vocabulario controlado o texto libre?

La regla: **si el campo se usa para enrutar, filtrar o generar lógica condicional en los prompts, debe ser vocabulario controlado**.

| Campo | Recomendación | Motivo |
|---|---|---|
| `estado` | Enum | La IA decide si procesar según el estado |
| `prioridad` | Enum (MoSCoW) | Los prompts ajustan el tono según la prioridad |
| `tipo` del criterio AC | Enum | La IA genera tests diferentes según el tipo |
| `tipo` de dato de entrada | Enum | La IA genera validaciones específicas por tipo |
| `descripcion` | Texto libre | Contexto narrativo, no se procesa lógicamente |
| `objetivo_negocio` | Texto libre | Mismo motivo |
| `reglas_negocio` | Lista de texto libre | Pero cada ítem debe ser una afirmación, no una pregunta |

### Decisión 3: ¿Dónde vive la plantilla?

Hay tres opciones con diferentes trade-offs:

**Confluence (recomendado para el piloto).** La plantilla vive como una página con macros que renderizan el YAML como tabla legible. El analista edita el YAML en modo código o usa un formulario generado con la macro de Confluence. Es la opción más accesible para equipos no técnicos y permite comentarios inline de stakeholders.

**Git (recomendado cuando el equipo madura).** Cada requisito es un archivo `.yaml` en un repositorio. Permite control de versiones nativo, pull requests para revisión de requisitos, y pipelines CI/CD que ejecutan la validación automáticamente al hacer commit.

**Ambos en paralelo.** Confluence como interfaz de edición para analistas y usuarios de negocio. Git como repositorio de autoridad para el pipeline de automatización. Un script de sincronización exporta el YAML de Confluence a Git al cambiar de estado a `validado`.

### Decisión 4: ¿Cómo se adaptan los campos al contexto específico del proyecto?

Algunos proyectos necesitan campos adicionales. Los más frecuentes son:

```yaml
# Para proyectos regulados (banca, salud, seguros):
cumplimiento_normativo:
  regulacion: ""      # GDPR, PSD2, Solvencia II...
  articulo: ""        # Referencia exacta al artículo regulatorio
  evidencia_requerida: "" # Qué debe quedar registrado para auditoría

# Para proyectos con múltiples mercados o idiomas:
localizacion:
  mercados: []        # [ES, PT, MX]
  consideraciones: "" # Diferencias de comportamiento por mercado

# Para proyectos con SLAs contractuales:
sla:
  tiempo_respuesta: ""
  disponibilidad: ""
  penalizacion_incumplimiento: ""

# Para proyectos de migración:
migracion:
  sistema_origen: ""
  comportamiento_actual: ""
  diferencias_con_actual: ""
```

La regla es: **añade campos específicos del dominio al Bloque 5, nunca al Bloque 2 o 3**. Los bloques 2 y 3 deben ser estables entre proyectos para que los prompts de generación sean reutilizables.

---

## Fase 5 — La plantilla en formato Word/Confluence (vista para el usuario de negocio)

El YAML es para la máquina. El usuario de negocio necesita ver esto:

```
┌─────────────────────────────────────────────────────────────┐
│ REQUISITO  REQ-023  │  Módulo: Gestión de Facturación       │
│ Estado: En revisión │  Prioridad: Must Have                 │
├─────────────────────────────────────────────────────────────┤
│ TÍTULO                                                       │
│ Filtrar facturas por rango de fechas                        │
├─────────────────────────────────────────────────────────────┤
│ ¿QUIÉN LO NECESITA?        │ ¿POR QUÉ?                      │
│ Gestor de facturación      │ Para localizar facturas de un  │
│                            │ período contable en el cierre  │
│                            │ mensual sin búsqueda manual    │
├─────────────────────────────────────────────────────────────┤
│ ¿QUÉ DEBE HACER EL SISTEMA?                                 │
│ El gestor introduce un rango de fechas y el sistema muestra │
│ las facturas de ese período ordenadas de más reciente a más │
│ antigua. Si el rango supera 365 días, avisa de que no está  │
│ permitido. Si no hay facturas, lo indica con un mensaje.    │
├─────────────────────────────────────────────────────────────┤
│ ¿CUÁNDO DEBE FUNCIONAR? (Criterios de aceptación)          │
│                                                             │
│ ✓ Si introduzco fechas válidas y pulso Buscar,             │
│   veo las facturas del período en menos de 2 segundos      │
│                                                             │
│ ✓ Si el rango supera 365 días,                             │
│   el sistema me avisa y no busca                           │
│                                                             │
│ ✓ Si no hay facturas en ese período,                       │
│   el sistema me lo indica y me ofrece ampliar la búsqueda  │
├─────────────────────────────────────────────────────────────┤
│ REGLAS IMPORTANTES                                          │
│ • Solo se ven facturas del ejercicio fiscal en curso       │
│ • El rango máximo de búsqueda es de 365 días               │
├─────────────────────────────────────────────────────────────┤
│ SOLICITADO POR: Ana López (Dir. Financiera) · 2025-04-10   │
│ ANALISTA: Carlos Ruiz · Validado: pendiente                 │
└─────────────────────────────────────────────────────────────┘
```

Esta vista se genera automáticamente desde el YAML mediante una macro de Confluence o un script de renderizado. El usuario de negocio valida en esta vista, no en el YAML.

---

## Fase 6 — Ejercicio práctico del taller (90 minutos)

Este es el plan concreto para la sesión de taller con el equipo:

**Bloque 1 — Calibración (20 min).** Cada participante trae un requisito real y reciente. Se lee en voz alta y el grupo identifica: ¿quién es el actor exacto?, ¿qué dispara este requisito?, ¿cómo sabemos que está hecho? Si no puede responderse en 30 segundos, el requisito necesita trabajo. Este ejercicio calibra al equipo sobre qué nivel de detalle se necesita.

**Bloque 2 — Completar la plantilla juntos (30 min).** El facilitador toma uno de los requisitos del bloque anterior y lo rellena en la plantilla en pantalla compartida, con el grupo aportando. Se detiene en cada campo que genera debate: eso indica un campo que necesita definición adicional o que el equipo no está alineado. Los debates son el output más valioso del taller, no la plantilla rellena.

**Bloque 3 — Decisiones de adaptación (25 min).** El grupo toma las cuatro decisiones de la Fase 4 para su contexto específico. Se documenta cada decisión y su motivo. Estas decisiones son el documento de gobierno de la plantilla.

**Bloque 4 — Prueba de validación (15 min).** Se toma un requisito mal escrito del histórico del equipo y se pasa por el checklist de validación manual (sin IA todavía). El grupo identifica qué habría bloqueado ese requisito si la plantilla hubiera existido. Esto conecta el esfuerzo del taller con problemas reales que el equipo ha vivido.

---

## Entregables del taller

Al terminar el taller deben existir tres documentos:

**La plantilla base adaptada**, con los campos obligatorios/recomendados/opcionales definidos para el contexto de la organización y los vocabularios controlados acordados.

**El documento de decisiones**, que registra las cuatro decisiones de adaptación con su justificación. Esto es crucial para cuando el equipo crezca o cambien los analistas: permite entender por qué la plantilla tiene la forma que tiene.

**El ejemplo de referencia**: un requisito real del proyecto rellenado completamente en la plantilla. Este ejemplo vale más que cualquier documentación de instrucciones porque muestra el nivel de detalle esperado con datos reales del dominio de la organización.
