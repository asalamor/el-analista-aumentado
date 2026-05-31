# Capítulo 8. Generación de artefactos Jira

Carlos tiene el café todavía caliente. REQ-023 acaba de pasar la validación con un score de 84 sobre 100 y un único campo `puede_entrar_al_pipeline: true`. El informe tiene tres advertencias menores sobre casos de contorno que decide dejar para el refinamiento. Abre el terminal, escribe un comando y espera.

Cuarenta y siete segundos después, en Jira hay una historia de usuario vinculada a su épica, cuatro tareas técnicas desglosadas por capa, los links de dependencia entre ellas y la estimación en story points ya calculada. Carlos la revisa durante cinco minutos, aprueba con un ajuste menor en la descripción de una tarea, y empuja. El trabajo que antes le llevaba entre noventa minutos y dos horas está hecho antes de que el café se enfríe.

Este capítulo describe exactamente cómo ocurre eso. No la magia: el mecanismo.

---

*En este capítulo aprenderás:*

- *La arquitectura de cuatro llamadas encadenadas que transforma un YAML en una jerarquía completa de artefactos Jira.*
- *Los cuatro prompts de generación con sus variables, su lógica interna y los ejemplos de output real para REQ-023.*
- *Cómo el contexto viaja entre las llamadas para garantizar coherencia vertical entre la épica, la historia y las tareas.*
- *El gate de aprobación humana: qué revisa el analista, en cuánto tiempo y con qué criterio decide.*
- *Las variantes de prompt para requisitos de integración, reglas de negocio complejas y modificaciones de funcionalidad existente.*

---

## La arquitectura de cuatro llamadas

El pipeline de generación no es una única llamada al LLM. Es una cadena de cuatro llamadas especializadas, cada una con una responsabilidad distinta y con el output de la anterior como parte de su contexto.

```
YAML de requisito validado
        │
        ▼
[Llamada 1] → Épica
        │       (si no existe; si ya existe en Jira, se reutiliza su key)
        ▼
[Llamada 2] → Historia de usuario + criterios de aceptación
        │
        ▼
[Llamada 3] → Tareas técnicas por capa
        │
        ▼
[Llamada 4] → Subtareas (solo para tareas > 8 horas)
        │
        ▼
JSON estructurado → cola de aprobación → Jira API
```

Cada llamada recibe tres tipos de contexto: el glosario del proyecto (para garantizar terminología consistente), el YAML del requisito (la fuente de verdad funcional) y el output de la llamada anterior (para que la historia conozca la épica a la que pertenece, y las tareas conozcan la historia que descomponen).

Esta cadena resuelve el problema de coherencia vertical que aparece cuando se intenta generar todo en una sola llamada: la historia pierde el vínculo semántico con la épica, las tareas pierden la relación con los criterios de aceptación, y el conjunto resultante parece un collage en lugar de una jerarquía coherente.

> 💡 **Idea clave**
>
> El sistema genera en el mismo orden en que un equipo humano construiría los artefactos: primero se entiende el módulo (épica), luego la funcionalidad concreta (historia), luego el trabajo técnico necesario (tareas). Respetar ese orden en el pipeline no es un capricho de diseño: es lo que garantiza que cada nivel tiene el contexto suficiente para ser coherente con el nivel anterior.

---

## El system prompt base

Antes de los cuatro prompts especializados, hay uno que todos comparten: el system prompt base. Define el comportamiento global del modelo durante toda la generación y establece las reglas que ninguna llamada puede violar.

---

📋 **Prompt de IA — System prompt base de generación**

```
Eres un analista funcional senior especializado en metodologías
Agile (Scrum/SAFe). Tu función es transformar requisitos funcionales
estructurados en artefactos Jira con precisión, consistencia y sin
añadir asunciones no documentadas en el requisito de entrada.

REGLAS ESTRICTAS:

1. Nunca inventes información que no esté explícita en el requisito.
   Si falta información necesaria, indícalo con el marcador:
   [PENDIENTE: descripción de qué falta]

2. Usa exclusivamente los términos del glosario proporcionado.
   Si un concepto no está en el glosario, usa el término del
   requisito sin modificarlo.

3. El tono de todas las descripciones es profesional y conciso.
   El actor se expresa en segunda persona del singular:
   "El gestor puede…", "El sistema muestra…"

4. Los criterios de aceptación SIEMPRE siguen el formato
   Dado / Cuando / Entonces. Sin excepciones.

5. Nunca fusiones dos requisitos en una sola historia.
   Un requisito = una historia. Siempre.

6. Si detectas ambigüedad en el requisito de entrada, indícala
   al final de tu respuesta en una sección llamada
   ⚠️ ALERTAS DE CALIDAD.

7. El output es siempre JSON válido. Sin texto antes ni después
   del JSON. Sin bloques de código markdown envolviendo el JSON.

GLOSARIO DEL PROYECTO:
{{glosario_yaml}}

CONTEXTO DEL PROYECTO:
- Proyecto: {{nombre_proyecto}}
- Equipo: {{nombre_equipo}}
- Prefijo Jira: {{prefijo_jira}}
```

---

La regla 1 —nunca inventar— es la más importante del sistema. Un LLM bien entrenado tiende a completar los huecos con suposiciones razonables. En análisis funcional, esas suposiciones son exactamente el origen de los bugs de ambigüedad que el capítulo anterior buscaba detectar. El marcador `[PENDIENTE: ...]` fuerza al modelo a hacer visible lo que falta en lugar de inventarlo, y ese marcador llega a la cola de aprobación para que Carlos lo resuelva.

---

## Llamada 1: La épica

La épica se genera una sola vez por módulo funcional, no por cada requisito. Si la épica ya existe en Jira —lo habitual en proyectos en curso—, el pipeline recupera su key y la usa directamente. Este prompt solo se ejecuta cuando se inicia un módulo nuevo o cuando el analista decide reorganizar la jerarquía de épicas.

---

📋 **Prompt de IA — Generación de épica**

```
A partir del módulo funcional descrito a continuación, genera
una Épica Jira.

MÓDULO FUNCIONAL:
{{epica_yaml}}

REQUISITOS QUE CONTIENE ESTE MÓDULO:
{{lista_ids_requisitos}}

Genera el siguiente JSON:
{
  "issue_type": "Epic",
  "summary": "[Título conciso, máximo 8 palabras, en infinitivo]",
  "description": {
    "objetivo": "[Qué capacidad de negocio habilita esta épica.
                  2-3 frases.]",
    "alcance": "[Qué incluye y qué excluye explícitamente.]",
    "valor_negocio": "[Beneficio medible para el negocio o usuario
                       final.]",
    "actores_principales": ["[Actor 1]", "[Actor 2]"],
    "kpis_exito": ["[KPI 1]", "[KPI 2]"]
  },
  "epic_name": "[Nombre corto para el campo Epic Name, máx. 4 palabras]",
  "priority": "[Must Have | Should Have | Could Have]",
  "labels": ["[etiqueta_1]", "[etiqueta_2]"],
  "components": ["[componente_sistema]"],
  "custom_fields": {
    "modulo_funcional": "{{id_epica}}",
    "origen_requisito": "{{lista_ids_requisitos}}"
  }
}
```

---

Para EP-04 de Meridian, el output generado sería:

```json
{
  "issue_type": "Epic",
  "summary": "Gestionar y filtrar facturas de proveedor",
  "description": {
    "objetivo": "Habilitar al gestor de facturación para localizar,
                 filtrar y exportar facturas según criterios temporales
                 y de estado. Reduce el tiempo de búsqueda manual y
                 elimina la dependencia de informes ad-hoc.",
    "alcance": "Incluye: filtrado por fecha, estado y proveedor,
                paginación y exportación. Excluye: edición de
                facturas, aprobación de pagos.",
    "valor_negocio": "Reducción estimada del 60% en tiempo de
                      localización de facturas para el cierre
                      contable mensual.",
    "actores_principales": [
      "Gestor de facturación",
      "Responsable financiero"
    ],
    "kpis_exito": [
      "Tiempo de búsqueda de factura < 30 segundos",
      "Tasa de error en localización < 2%"
    ]
  },
  "epic_name": "Gestión facturas",
  "priority": "Must Have",
  "labels": ["facturacion", "busqueda", "fase-1"],
  "components": ["modulo-facturacion"],
  "custom_fields": {
    "modulo_funcional": "EP-04",
    "origen_requisito": "REQ-021, REQ-022, REQ-023, REQ-024"
  }
}
```

El campo `alcance` merece atención especial. Definir explícitamente qué excluye la épica es tan importante como definir qué incluye. Sin ese campo, el equipo interpretará el alcance de forma diferente en cada conversación y los debates de scope llegará al sprint planning en lugar de al refinamiento de la épica.

---

## Llamada 2: La historia de usuario

Este es el prompt más crítico del pipeline. Una historia bien generada hace que el refinamiento sea una conversación de diez minutos; una mal generada lo convierte en una renegociación completa del alcance.

---

📋 **Prompt de IA — Generación de historia de usuario**

```
A partir del requisito funcional estructurado, genera una Historia
de Usuario Jira completa y lista para refinamiento.

REQUISITO DE ENTRADA:
{{requisito_yaml}}

ÉPICA PADRE (ya creada o identificada en Jira):
- ID Jira: {{epic_jira_id}}
- Título: {{epic_summary}}

HISTORIAS YA EXISTENTES EN ESTA ÉPICA (para evitar duplicidades):
{{historias_existentes_resumen}}

Genera el siguiente JSON:
{
  "issue_type": "Story",
  "summary": "Como [rol], quiero [acción concreta]
              para [beneficio medible]",
  "epic_link": "{{epic_jira_id}}",
  "description": {
    "contexto": "[Por qué existe esta historia. Problema de negocio
                  que resuelve. 2-3 frases.]",
    "narrativa": "Como [rol]\nquiero [acción]\npara [beneficio]",
    "notas_importantes": [
      "[Restricción o aclaración relevante 1]"
    ],
    "flujo_principal": [
      "1. [Paso 1 del flujo feliz]",
      "2. [Paso 2]",
      "3. [Paso 3]"
    ],
    "flujos_error": [
      {
        "condicion": "[Condición de error]",
        "comportamiento_esperado": "[Qué hace el sistema]"
      }
    ]
  },
  "acceptance_criteria": [
    {
      "id": "AC-{{req_id}}-01",
      "dado": "[Estado previo del sistema y del actor]",
      "cuando": "[UNA acción concreta]",
      "entonces": "[Resultado observable y verificable]"
    }
  ],
  "definition_of_done": [
    "Todos los criterios de aceptación superan pruebas de regresión",
    "Revisión de código aprobada por al menos un peer",
    "Documentación técnica actualizada",
    "[DoD específico derivado del requisito]"
  ],
  "priority": "[Must Have | Should Have | Could Have | Won't Have]",
  "story_points": [NÚMERO entre 1 y 13, escala Fibonacci],
  "labels": ["[etiqueta]"],
  "components": ["[componente]"],
  "custom_fields": {
    "requisito_origen": "{{req_id}}",
    "modulo_funcional": "{{epica_id}}"
  },
  "alertas_calidad": []
}

CRITERIOS DE ESTIMACIÓN (story points):
1  = trivial, un flujo, sin lógica de negocio
2  = simple, un flujo, sin integraciones
3  = moderado, 2-3 flujos o una integración simple
5  = complejo, múltiples flujos o reglas de negocio
8  = muy complejo, múltiples integraciones o alta incertidumbre
13 = demasiado grande — considera partir la historia antes de estimar
```

---

Aplicado a REQ-023, el output es:

```json
{
  "issue_type": "Story",
  "summary": "Como gestor de facturación, quiero filtrar facturas
              por rango de fechas para localizar documentos de un
              período contable sin búsqueda manual",
  "epic_link": "FACT-12",
  "description": {
    "contexto": "El gestor de facturación dedica entre 15 y 30 minutos
                 en cada cierre mensual buscando facturas de forma
                 manual. Un filtro por rango de fechas elimina esa
                 fricción y reduce el tiempo de localización a menos
                 de 30 segundos.",
    "narrativa": "Como gestor de facturación\nquiero filtrar el
                  listado de facturas por fecha de inicio y fecha
                  de fin\npara localizar rápidamente las facturas
                  de un período contable concreto",
    "notas_importantes": [
      "El rango máximo permitido es 365 días por restricción de rendimiento",
      "Solo se muestran facturas del ejercicio fiscal en curso"
    ],
    "flujo_principal": [
      "1. El gestor accede al módulo Facturas",
      "2. Introduce fecha_inicio y fecha_fin en los campos de filtro",
      "3. Pulsa el botón Buscar",
      "4. El sistema devuelve las facturas del período ordenadas
          por fecha descendente",
      "5. El gestor visualiza el listado paginado con el contador
          de resultados"
    ],
    "flujos_error": [
      {
        "condicion": "El rango de fechas supera 365 días",
        "comportamiento_esperado": "El sistema no ejecuta la consulta
                                    y muestra el mensaje 'El rango no
                                    puede superar 365 días'. Los campos
                                    de fecha se resaltan en rojo."
      },
      {
        "condicion": "No existen facturas en el período seleccionado",
        "comportamiento_esperado": "El sistema muestra el estado vacío
                                    con el mensaje 'No se encontraron
                                    facturas para el período seleccionado'
                                    y el botón 'Ampliar búsqueda'."
      }
    ]
  },
  "acceptance_criteria": [
    {
      "id": "AC-023-01",
      "dado": "El gestor está autenticado con rol gestor_facturacion
               y accede al módulo Facturas",
      "cuando": "Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31
                 y pulsa Buscar",
      "entonces": "El sistema devuelve las facturas del período en menos
                   de 2 segundos, ordenadas por fecha descendente,
                   mostrando el contador de resultados"
    },
    {
      "id": "AC-023-02",
      "dado": "El gestor selecciona un rango de fechas superior a 365 días",
      "cuando": "Pulsa Buscar",
      "entonces": "El sistema no ejecuta la consulta, muestra el mensaje
                   'El rango no puede superar 365 días' y resalta los
                   campos de fecha en rojo"
    },
    {
      "id": "AC-023-03",
      "dado": "El gestor ejecuta una búsqueda válida sin resultados
               en el período",
      "cuando": "El sistema procesa la consulta",
      "entonces": "Se muestra el estado vacío con el mensaje definido
                   y el botón 'Ampliar búsqueda'"
    }
  ],
  "definition_of_done": [
    "Todos los criterios de aceptación superan pruebas de regresión",
    "Revisión de código aprobada por al menos un peer",
    "Documentación técnica actualizada",
    "Rendimiento validado con dataset de 10.000 registros en staging"
  ],
  "priority": "Must Have",
  "story_points": 5,
  "labels": ["facturacion", "filtrado", "fase-1"],
  "components": ["modulo-facturacion"],
  "custom_fields": {
    "requisito_origen": "REQ-023",
    "modulo_funcional": "EP-04"
  },
  "alertas_calidad": []
}
```

Hay tres decisiones de diseño en este output que vale la pena señalar.

El campo `contexto` en la descripción no es un resumen del requisito: es la justificación de negocio. «El gestor dedica entre 15 y 30 minutos en cada cierre mensual» es el dato que hace que el equipo entienda por qué esta historia existe y por qué tiene prioridad Must Have. Sin ese dato, la historia es una especificación técnica; con él, es una solución a un problema real.

El campo `story_points` con valor 5 no es arbitrario. El LLM aplica los criterios de estimación del prompt: la historia tiene múltiples flujos (principal + dos de error), una regla de negocio con validación de contorno (el límite de 365 días) y un criterio de rendimiento. Eso la sitúa en la banda de «compleja» según la escala del prompt. No reemplaza la estimación del equipo en el planning poker, pero sí da un punto de partida fundamentado.

El campo `alertas_calidad` está vacío para REQ-023 porque el requisito pasó la validación correctamente. Si el prompt detecta algo que no estaba en el requisito —un caso no documentado que infiere del contexto— lo registra aquí. Carlos ve esas alertas en la cola de aprobación antes de decidir si empujar.

---

## Llamada 3: Las tareas técnicas

Una vez generada la historia, el pipeline descompone el trabajo en tareas técnicas por capa tecnológica. Este prompt recibe la historia generada en la llamada anterior y el stack tecnológico del proyecto.

---

📋 **Prompt de IA — Generación de tareas técnicas**

```
A partir de la Historia de Usuario generada, descompón el trabajo
técnico necesario en Tareas Técnicas Jira por capa tecnológica.

HISTORIA DE USUARIO:
{{historia_json}}

STACK TECNOLÓGICO DEL PROYECTO:
{{stack_tecnologico}}

CONVENCIONES DEL EQUIPO:
{{convenciones_equipo}}

REGLAS DE DESCOMPOSICIÓN:
- Crea una tarea por capa tecnológica afectada.
- Nunca mezcles trabajo de frontend y backend en la misma tarea.
- Incluye siempre una tarea de testing si la historia tiene
  lógica de negocio.
- Incluye una tarea de base de datos si hay cambios en esquema
  o consultas nuevas.
- El campo "dependencias" indica qué tareas deben completarse antes.
- La estimación es en horas ideales (sin interrupciones ni contexto).

Genera el siguiente JSON:
{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "[Verbo en infinitivo] [componente] [para qué]",
      "capa": "[backend | frontend | base_datos |
                integracion | testing | devops]",
      "parent_story": "{{historia_jira_id}}",
      "description": {
        "objetivo": "[Qué debe implementarse exactamente]",
        "criterios_tecnico": [
          "[Criterio técnico verificable 1]",
          "[Criterio técnico verificable 2]"
        ],
        "consideraciones": [
          "[Decisión técnica relevante o restricción]"
        ],
        "referencias": [
          "[Endpoint, tabla, componente o documento relevante]"
        ]
      },
      "estimacion_horas": NÚMERO,
      "dependencias": [
        "[Summary de tarea que debe completarse antes]"
      ],
      "labels": ["[etiqueta_tecnica]"],
      "components": ["[componente]"]
    }
  ]
}
```

---

Para la historia de filtrado de facturas de Meridian, el output sería:

```json
{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "Crear índice de rendimiento en tabla facturas
                  para filtrado por fecha",
      "capa": "base_datos",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Añadir índice compuesto (fecha_factura, id_empresa)
                     a la tabla facturas para garantizar respuesta
                     inferior a 2 segundos con 10.000 registros.",
        "criterios_tecnico": [
          "Script de migración versionado con Flyway/Liquibase",
          "Validación de rendimiento en staging con dataset representativo",
          "Script de rollback incluido"
        ],
        "consideraciones": [
          "Ejecutar en ventana de mantenimiento en producción
           por el impacto del índice durante la creación"
        ],
        "referencias": [
          "Tabla: facturas",
          "Política de migraciones: /docs/db-migrations"
        ]
      },
      "estimacion_horas": 3,
      "dependencias": [],
      "labels": ["base-datos", "migracion", "facturacion"],
      "components": ["base-datos"]
    },
    {
      "issue_type": "Task",
      "summary": "Implementar endpoint REST de filtrado de facturas
                  por rango de fechas",
      "capa": "backend",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Crear el endpoint GET /api/v1/facturas con
                     parámetros fecha_inicio y fecha_fin. Debe validar
                     el rango máximo de 365 días, devolver resultados
                     paginados ordenados por fecha descendente y
                     responder en menos de 2 segundos para datasets
                     de hasta 10.000 registros.",
        "criterios_tecnico": [
          "Validación de rango máximo 365 días con respuesta HTTP 400
           y mensaje de error estándar",
          "Paginación con parámetros page y size (default: size=100)",
          "Respuesta en formato JSON: {data: [], total: N, page: N}",
          "Tests unitarios con cobertura mínima 80% de la lógica
           de validación"
        ],
        "consideraciones": [
          "Usar el índice compuesto de (fecha_factura, id_empresa)
           para garantizar rendimiento",
          "El filtro aplica sobre fecha_factura, no fecha_creacion"
        ],
        "referencias": [
          "Tabla: facturas",
          "Swagger: /api/v1/facturas#GET"
        ]
      },
      "estimacion_horas": 6,
      "dependencias": [
        "Crear índice de rendimiento en tabla facturas para filtrado
         por fecha"
      ],
      "labels": ["backend", "api", "facturacion"],
      "components": ["api-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Implementar componente de filtrado por fechas
                  en el módulo Facturas",
      "capa": "frontend",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Añadir los campos fecha_inicio y fecha_fin al
                     panel de filtros del listado de facturas. Incluir
                     validación visual cuando el rango supere 365 días
                     y mostrar el estado vacío con el botón de acción
                     cuando no haya resultados.",
        "criterios_tecnico": [
          "Validación client-side del rango antes de llamar al API",
          "Estado de carga (skeleton loader) durante la petición",
          "Estado vacío con mensaje y botón 'Ampliar búsqueda'",
          "Campos de fecha en rojo cuando el rango supera 365 días",
          "Tests de componente con React Testing Library",
          "Accesibilidad: labels asociados a inputs, mensajes de
           error con aria-live (WCAG 2.1 AA)"
        ],
        "consideraciones": [
          "Reutilizar el componente DateRangePicker del design system
           interno"
        ],
        "referencias": [
          "Design system: DateRangePicker",
          "Figma: Módulo Facturas v2.3"
        ]
      },
      "estimacion_horas": 8,
      "dependencias": [
        "Implementar endpoint REST de filtrado de facturas por rango
         de fechas"
      ],
      "labels": ["frontend", "facturacion", "accesibilidad"],
      "components": ["frontend-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Ejecutar pruebas de integración y rendimiento
                  del filtrado de facturas",
      "capa": "testing",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Validar los tres criterios de aceptación
                     (AC-023-01, AC-023-02, AC-023-03) en entorno
                     de integración. Incluir prueba de rendimiento
                     con dataset de 10.000 registros.",
        "criterios_tecnico": [
          "Todos los AC documentados en Xray con resultado PASS",
          "Prueba de carga: p95 < 2 segundos con 50 usuarios
           concurrentes",
          "Prueba de contorno: rango exacto de 365 días debe funcionar,
           366 debe fallar"
        ],
        "consideraciones": [
          "Usar datos de prueba anonimizados del entorno de staging"
        ],
        "referencias": [
          "Test cases: TC-111, TC-112, TC-113",
          "Xray: EP-04"
        ]
      },
      "estimacion_horas": 4,
      "dependencias": [
        "Implementar endpoint REST de filtrado de facturas por rango
         de fechas",
        "Implementar componente de filtrado por fechas en el módulo
         Facturas"
      ],
      "labels": ["testing", "facturacion", "rendimiento"],
      "components": ["qa"]
    }
  ]
}
```

Cuatro tareas: una de base de datos, una de backend, una de frontend y una de testing. Las dependencias están declaradas explícitamente: la de base de datos va primera porque el endpoint la necesita; las de backend y frontend deben estar listas antes de las pruebas de integración. El pipeline empujará estos links como issue links de tipo «blocks» en Jira, de forma que el tablero refleje el orden real de implementación.

> 🛠️ **En la práctica**
>
> La división por capa tecnológica parece obvia en el papel, pero en muchos proyectos las tareas mezclan trabajo de frontend y backend en el mismo issue «para simplificar». El problema es que esa simplificación hace imposible el tracking de progreso real: la tarea aparece como «en progreso» durante días porque dos personas trabajan en ella en paralelo sin que el tablero refleje el estado de cada parte. Separar por capas no es burocracia: es hacer visible el trabajo real.

---

## Llamada 4: Las subtareas (opcional)

Esta llamada solo se ejecuta para tareas que superan las ocho horas estimadas o cuando el equipo trabaja con subtareas para el seguimiento diario. En el ejemplo de Meridian, la tarea de frontend con ocho horas estimadas está en el límite; el analista puede decidir mantenerla como tarea única o solicitar la descomposición.

---

📋 **Prompt de IA — Generación de subtareas**

```
La siguiente Tarea Técnica supera las 8 horas estimadas o requiere
descomposición para seguimiento diario. Descomponla en subtareas
que puedan completarse de forma independiente en no más de 4 horas.

TAREA TÉCNICA:
{{tarea_json}}

REGLAS:
- Cada subtarea debe ser completable en una sesión de trabajo
  (máx. 4 horas).
- El título sigue el patrón: [Verbo] + [artefacto específico].
- Las subtareas deben tener un orden lógico de ejecución.
- El campo "orden" indica la secuencia recomendada (1 = primero).

Genera el siguiente JSON:
{
  "subtareas": [
    {
      "issue_type": "Subtask",
      "parent_task": "{{tarea_jira_id}}",
      "summary": "[Verbo] + [artefacto muy específico]",
      "description": "[Qué exactamente debe estar hecho al terminar]",
      "criterio_completitud": "[Condición binaria: cómo saber que
                               está terminada]",
      "estimacion_horas": NÚMERO,
      "orden": NÚMERO
    }
  ]
}
```

---

Para la tarea de frontend de ocho horas, el resultado sería:

```json
{
  "subtareas": [
    {
      "issue_type": "Subtask",
      "parent_task": "FACT-50",
      "summary": "Integrar DateRangePicker en el panel de filtros",
      "description": "Añadir el componente DateRangePicker del design
                      system al panel de filtros del listado de facturas,
                      conectado a los campos fecha_inicio y fecha_fin
                      del estado del componente padre.",
      "criterio_completitud": "El componente renderiza correctamente
                               y los valores seleccionados se reflejan
                               en el estado del padre",
      "estimacion_horas": 2,
      "orden": 1
    },
    {
      "issue_type": "Subtask",
      "parent_task": "FACT-50",
      "summary": "Implementar validación client-side y estados visuales",
      "description": "Añadir la lógica de validación del rango de fechas
                      (máximo 365 días) con resaltado en rojo de los
                      campos y el mensaje de error. Implementar el
                      estado de carga (skeleton loader) durante la
                      petición al API.",
      "criterio_completitud": "El campo muestra el error visual al
                               superar 365 días y el skeleton aparece
                               durante la carga",
      "estimacion_horas": 3,
      "orden": 2
    },
    {
      "issue_type": "Subtask",
      "parent_task": "FACT-50",
      "summary": "Implementar estado vacío y tests de componente",
      "description": "Añadir el estado vacío con el mensaje definido
                      y el botón 'Ampliar búsqueda'. Escribir los
                      tests de componente con React Testing Library
                      para los flujos principal, de error y vacío.",
      "criterio_completitud": "Tests de componente pasan en CI y el
                               estado vacío renderiza correctamente",
      "estimacion_horas": 3,
      "orden": 3
    }
  ]
}
```

---

## El gate de aprobación humana

Antes de que cualquier JSON llegue a Jira, Carlos revisa el output completo en la interfaz de aprobación. Esto no es una formalidad: es el punto donde el analista añade el valor que la IA no puede.

La revisión tiene cinco preguntas concretas y no debería llevar más de cinco minutos por historia:

**¿El actor es el correcto?** En proyectos con varios roles, el LLM puede confundir actores si el glosario no es preciso. Esta es la primera comprobación.

**¿Los criterios de aceptación reflejan lo que pidió el negocio?** No si son técnicamente correctos: si capturan la intención real de Ana López cuando describió el problema.

**¿Las tareas técnicas tienen sentido para el stack del equipo?** El LLM no sabe que el equipo de Meridian tiene una convención interna para los tests de integración que difiere de la convención general. Carlos lo ajusta si hace falta.

**¿La estimación de story points es razonable?** No para aceptarla sin más, sino como punto de partida para el planning poker. Si el LLM estima 5 y Carlos sabe que hay una dependencia técnica compleja que el requisito no menciona, cambia el valor antes de empujar.

**¿Hay alertas de calidad que resolver?** Si el campo `alertas_calidad` tiene contenido, Carlos decide si actualizar el requisito, añadir contexto a la historia o documentar la decisión como una asunción explícita.

El resultado de la revisión es binario: aprobar (con o sin ediciones) o rechazar con motivo. Si rechaza, el requisito vuelve al analista con el motivo documentado. Si aprueba con ediciones, el JSON editado es el que llega a Jira, no el generado originalmente.

> ⚠️ **Error frecuente**
>
> El gate de aprobación pierde todo su valor cuando el analista lo convierte en un trámite de «aprobar sin leer» bajo presión de sprint. La IA propone; el humano decide. Si ese principio se erosiona en las semanas de alta carga, los primeros artefactos incorrectos que llegan a producción generan una desconfianza en el sistema que es mucho más difícil de recuperar que el tiempo que se habría tardado en revisar.

---

## Variantes de prompt por tipo de requisito

Los cuatro prompts anteriores funcionan para el 80% de los requisitos funcionales estándar. Para los casos especiales, el analista añade un bloque de contexto adicional al Prompt 2 antes de ejecutarlo.

### Para requisitos de integración con sistemas externos

```
CONTEXTO ADICIONAL — INTEGRACIÓN:

Este requisito implica integración con el sistema externo
{{nombre_sistema}}.

Añade en las tareas técnicas una tarea específica de tipo
"integracion" que incluya:
- Análisis del contrato de API o mensaje del sistema externo
- Manejo de errores de conectividad y timeouts
- Estrategia de retry y circuit breaker si aplica
```

### Para requisitos con reglas de negocio complejas

```
CONTEXTO ADICIONAL — REGLAS DE NEGOCIO COMPLEJAS:

Este requisito contiene reglas de negocio con cálculos o condiciones
múltiples. Para cada regla de negocio identificada, genera un criterio
de aceptación específico con ejemplos de datos concretos siguiendo
el patrón de Specification by Example:

"Dado que [valor_entrada_concreto], el resultado debe ser
[valor_salida_concreto]."
```

### Para modificaciones de funcionalidad existente

```
CONTEXTO ADICIONAL — MODIFICACIÓN DE FUNCIONALIDAD EXISTENTE:

Este requisito modifica funcionalidad ya en producción. Añade
obligatoriamente:

1. Una sección "impacto_en_funcionalidad_existente" en la descripción
   de la historia que describa qué comportamiento actual cambia.
2. Un criterio de aceptación de regresión: el comportamiento anterior
   que NO debe cambiar.
3. Una tarea técnica de tipo "testing" específica para pruebas de
   regresión sobre la funcionalidad existente.
```

---

## Lo que funciona en la práctica

Tres observaciones de la implantación real que no aparecen en la documentación del pipeline pero que hacen la diferencia entre un sistema que el equipo usa y uno que abandona.

**El primer requisito es el más difícil y el más valioso.** La primera vez que Carlos ejecuta el pipeline con un requisito real de Meridian, el output no será perfecto. El stack tecnológico no estará bien configurado, una convención del equipo no estará en el prompt, y una tarea tendrá un nombre que nadie del equipo reconoce. Eso es normal y esperado. El valor de ese primer requisito no es el artefacto generado: es la lista de ajustes que Carlos hace durante la revisión, porque esos ajustes van a mejorar el prompt para todos los requisitos siguientes. La calidad del output crece con el uso, no con la configuración inicial.

**El campo `stack_tecnologico` es más importante de lo que parece.** Un prompt que no sabe que el equipo usa Flyway para migraciones generará tareas que mencionan scripts SQL manuales. Un prompt que no sabe que el design system tiene un DateRangePicker generará tareas de construcción del componente desde cero. Cuatro líneas bien escritas en el campo de stack tecnológico ahorran decenas de ediciones manuales en la cola de aprobación.

**Las estimaciones del LLM son un punto de partida, no un resultado.** En Meridian, David Sanz usó los story points generados como referencia para el planning poker, no como sustituto. El equipo llegaba a la sesión con una propuesta fundamentada en lugar de con el lienzo en blanco, y el debate se centraba en los matices técnicos que el LLM no podía conocer. El tiempo de estimación cayó de veinte minutos por historia a ocho. No porque la IA estimara mejor que el equipo, sino porque el equipo empezó desde un punto de partida razonado en lugar de desde cero.

---

## Tres puntos clave

El pipeline de generación no reemplaza el refinamiento: lo mejora. El equipo llega al sprint planning con historias ya estructuradas, criterios de aceptación ya formulados y tareas técnicas ya desglosadas por capa. El refinamiento se convierte en una conversación sobre los matices, no en la construcción desde cero de los artefactos.

La cadena de cuatro llamadas no es un detalle de implementación: es la garantía de coherencia vertical. Una épica que no conoce sus requisitos, una historia que no conoce su épica y unas tareas que no conocen su historia producen un backlog técnicamente correcto pero funcionalmente desarticulado. El contexto que viaja entre llamadas es lo que hace que el conjunto tenga sentido.

El gate de aprobación humana es el componente más importante del pipeline. No por lo que bloquea, sino por lo que enseña: cada edición que Carlos hace durante la revisión es información sobre cómo mejorar el prompt siguiente. Un sistema que genera artefactos perfectos desde el primer día no existe. Un sistema que mejora con cada uso, sí.

---

> 💡 **Pregunta de reflexión para tu equipo**
>
> Tomad el último sprint planning que os llevó más de dos horas. ¿Cuánto de ese tiempo fue debatir el alcance de historias que nadie había leído antes de entrar a la sala, y cuánto fue tomar decisiones reales sobre cómo construirlas? La respuesta define el impacto potencial del pipeline en vuestro proceso.

---

El capítulo siguiente cierra el triángulo del núcleo técnico: si el capítulo 7 garantizó que el input es correcto y este capítulo transformó ese input en artefactos Jira, el capítulo 9 convierte esos mismos criterios de aceptación en test cases ejecutables. El mismo REQ-023 que acaba de producir cuatro tareas técnicas producirá nueve casos de prueba, tres de ellos para flujos de error que ningún QA habría documentado bajo la presión del sprint.
