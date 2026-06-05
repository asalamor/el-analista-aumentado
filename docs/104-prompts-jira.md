# Punto 4 — Prompts de generación de artefactos Jira

Vamos a construir esto de forma que puedas copiar, probar y adaptar cada prompt directamente.

La estructura tiene tres niveles que funcionan en cadena.

---

## Arquitectura del pipeline de prompts

Antes de los prompts en sí, necesitas entender cómo se encadenan. No es una única llamada a la IA, sino **cuatro llamadas especializadas** con contexto compartido:

```
YAML de requisito validado
        │
        ▼
[Llamada 1] → Épica (si no existe)
        │
        ▼
[Llamada 2] → Historia de usuario + criterios AC
        │
        ▼
[Llamada 3] → Tareas técnicas (desde la historia)
        │
        ▼
[Llamada 4] → Subtareas (desde cada tarea técnica)
        │
        ▼
JSON estructurado → Jira API
```

Cada llamada recibe como contexto: el **glosario** de la organización, el **YAML del requisito**, y el **output de la llamada anterior**. Así se garantiza coherencia vertical.

---

## Prompt 0 — System prompt base (compartido por todas las llamadas)

Este es el prompt de sistema que se inyecta en **todas** las llamadas. Define el comportamiento, las restricciones y el vocabulario.

```
Eres un analista funcional senior especializado en metodologías Agile (Scrum/SAFe).
Tu función es transformar requisitos funcionales estructurados en artefactos Jira
con precisión, consistencia y sin añadir asunciones no documentadas.

REGLAS ESTRICTAS:
1. Nunca inventes información que no esté explícita en el requisito de entrada.
   Si falta información, indícalo con el marcador [PENDIENTE: descripción].
2. Usa exclusivamente los términos del glosario proporcionado.
   Si un concepto no está en el glosario, usa el término del requisito sin modificarlo.
3. El tono de todas las descripciones es profesional, conciso y en segunda persona
   del singular para el actor ("El gestor puede…", "El sistema muestra…").
4. Los criterios de aceptación SIEMPRE siguen el formato
   Dado / Cuando / Entonces. Sin excepciones.
5. Nunca fusiones dos requisitos en una sola historia.
   Un requisito = una historia.
6. Si detectas ambigüedad en el requisito de entrada, indícala al final de tu
   respuesta en una sección llamada ⚠️ ALERTAS DE CALIDAD.
7. El output es siempre JSON válido. Sin texto antes ni después del JSON.
   Sin bloques de código markdown envolviendo el JSON.

GLOSARIO DE LA ORGANIZACIÓN:
{{glosario_yaml}}

CONTEXTO DEL PROYECTO:
- Proyecto: {{nombre_proyecto}}
- Equipo: {{nombre_equipo}}
- Sprint actual: {{sprint_actual}}
- Prefijo Jira: {{prefijo_jira}}
```

---

## Prompt 1 — Generación de Épica

Se ejecuta **una sola vez por módulo funcional**, no por cada requisito. Si la épica ya existe en Jira, se salta este paso y se usa el ID existente.

```
A partir del módulo funcional descrito a continuación, genera una Épica Jira.

MÓDULO FUNCIONAL:
{{epica_yaml}}

REQUISITOS QUE CONTIENE ESTE MÓDULO:
{{lista_ids_requisitos}}

Genera el siguiente JSON:

{
  "issue_type": "Epic",
  "summary": "[Título conciso, máximo 8 palabras, en infinitivo]",
  "description": {
    "objetivo": "[Qué capacidad de negocio habilita esta épica. 2-3 frases.]",
    "alcance": "[Qué incluye y qué excluye explícitamente.]",
    "valor_negocio": "[Beneficio medible para el negocio o usuario final.]",
    "actores_principales": ["[Actor 1]", "[Actor 2]"],
    "kpis_exito": ["[KPI 1]", "[KPI 2]"]
  },
  "epic_name": "[Nombre corto para el campo Epic Name de Jira, máx. 4 palabras]",
  "priority": "[Must Have │ Should Have │ Could Have]",
  "labels": ["[etiqueta_1]", "[etiqueta_2]"],
  "components": ["[componente_sistema]"],
  "custom_fields": {
    "modulo_funcional": "{{id_epica}}",
    "origen_requisito": "{{lista_ids_requisitos}}"
  }
}
```

**Ejemplo de output generado:**

```json
{
  "issue_type": "Epic",
  "summary": "Gestión y filtrado de facturas",
  "description": {
    "objetivo": "Habilitar al gestor de facturación para localizar, filtrar y exportar facturas según criterios temporales y de estado. Reduce el tiempo de búsqueda manual y elimina la dependencia de informes ad-hoc.",
    "alcance": "Incluye: filtrado por fecha, estado y proveedor, paginación y exportación. Excluye: edición de facturas, aprobación de pagos.",
    "valor_negocio": "Reducción estimada del 60% en tiempo de localización de facturas para cierre contable mensual.",
    "actores_principales": ["Gestor de facturación", "Responsable financiero"],
    "kpis_exito": ["Tiempo de búsqueda < 30 segundos", "Tasa de error en localización < 2%"]
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

---

## Prompt 2 — Generación de Historia de Usuario

Este es el prompt más crítico del pipeline. Se ejecuta **una vez por requisito**.

```
A partir del requisito funcional estructurado que se proporciona, genera
una Historia de Usuario Jira completa y lista para refinamiento.

REQUISITO DE ENTRADA:
{{requisito_yaml}}

ÉPICA PADRE (ya creada en Jira):
- ID Jira: {{epic_jira_id}}
- Título: {{epic_summary}}

HISTORIAS YA EXISTENTES EN ESTA ÉPICA (para evitar duplicidades):
{{historias_existentes_resumen}}

Genera el siguiente JSON:

{
  "issue_type": "Story",
  "summary": "Como [rol], quiero [acción concreta] para [beneficio medible]",
  "epic_link": "{{epic_jira_id}}",
  "description": {
    "contexto": "[Por qué existe esta historia. Problema de negocio que resuelve.]",
    "narrativa": "Como [rol]\nquiero [acción]\npara [beneficio]",
    "notas_importantes": ["[Restricción o aclaración relevante 1]"],
    "flujo_principal": [
      "1. [Paso 1 del flujo feliz]",
      "2. [Paso 2]",
      "3. [Paso 3]"
    ],
    "flujos_alternativos": [
      {
        "condicion": "[Cuándo se activa este flujo]",
        "pasos": ["1. [Paso]"]
      }
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
      "dado": "[Contexto previo y estado del sistema]",
      "cuando": "[Acción concreta que ejecuta el actor]",
      "entonces": "[Resultado observable y verificable]"
    }
  ],
  "definition_of_done": [
    "Todos los criterios de aceptación superan pruebas de regresión",
    "Revisión de código aprobada por al menos un peer",
    "Documentación técnica actualizada",
    "[DoD específico derivado del requisito]"
  ],
  "priority": "[Must Have │ Should Have │ Could Have │ Won't Have]",
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
1  = trivial, sin lógica de negocio
2  = simple, un flujo, sin integraciones
3  = moderado, 2-3 flujos o una integración simple
5  = complejo, múltiples flujos o reglas de negocio
8  = muy complejo, múltiples integraciones o alta incertidumbre
13 = demasiado grande, considera partir la historia
```

**Ejemplo de output generado desde REQ-023:**

```json
{
  "issue_type": "Story",
  "summary": "Como gestor de facturación, quiero filtrar facturas por rango de fechas para localizar rápidamente documentos de un período contable",
  "epic_link": "FACT-12",
  "description": {
    "contexto": "El gestor de facturación dedica actualmente entre 15 y 30 minutos al cierre mensual buscando facturas manualmente. Un filtro por rango de fechas elimina esta fricción.",
    "narrativa": "Como gestor de facturación\nquiero filtrar el listado de facturas por fecha de inicio y fecha de fin\npara localizar rápidamente las facturas de un período contable concreto",
    "notas_importantes": [
      "El rango máximo permitido es 365 días por restricción de rendimiento",
      "Solo se muestran facturas del ejercicio fiscal en curso"
    ],
    "flujo_principal": [
      "1. El gestor accede al módulo Facturas",
      "2. Introduce fecha_inicio y fecha_fin en los campos de filtro",
      "3. Pulsa el botón Buscar",
      "4. El sistema devuelve las facturas del período ordenadas por fecha descendente",
      "5. El gestor visualiza el listado paginado con el contador de resultados"
    ],
    "flujos_alternativos": [
      {
        "condicion": "El gestor no introduce fecha_fin",
        "pasos": ["1. El sistema usa la fecha actual como fecha_fin por defecto"]
      }
    ],
    "flujos_error": [
      {
        "condicion": "El rango de fechas supera 365 días",
        "comportamiento_esperado": "El sistema no ejecuta la consulta y muestra el mensaje 'El rango no puede superar 365 días'. Los campos de fecha se resaltan en rojo."
      },
      {
        "condicion": "No existen facturas en el período seleccionado",
        "comportamiento_esperado": "El sistema muestra estado vacío con el mensaje 'No se encontraron facturas para el período seleccionado' y el botón 'Ampliar búsqueda'."
      }
    ]
  },
  "acceptance_criteria": [
    {
      "id": "AC-023-01",
      "dado": "El gestor está autenticado con rol gestor_facturacion y accede al módulo Facturas",
      "cuando": "Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31 y pulsa Buscar",
      "entonces": "El sistema devuelve las facturas del período en menos de 2 segundos, ordenadas por fecha descendente, mostrando el contador de resultados"
    },
    {
      "id": "AC-023-02",
      "dado": "El gestor selecciona un rango de fechas superior a 365 días",
      "cuando": "Pulsa Buscar",
      "entonces": "El sistema no ejecuta la consulta, muestra el mensaje 'El rango no puede superar 365 días' y resalta los campos de fecha en rojo"
    },
    {
      "id": "AC-023-03",
      "dado": "El gestor ejecuta una búsqueda válida sin resultados en el período",
      "cuando": "El sistema procesa la consulta",
      "entonces": "Se muestra el estado vacío con el mensaje definido y el botón 'Ampliar búsqueda'"
    }
  ],
  "definition_of_done": [
    "Todos los criterios de aceptación superan pruebas de regresión",
    "Revisión de código aprobada por al menos un peer",
    "Documentación técnica actualizada",
    "Rendimiento validado con dataset de 10.000 registros en entorno de staging"
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

---

## Prompt 3 — Generación de Tareas Técnicas

Se ejecuta una vez por historia. El LLM analiza qué trabajo técnico implica cada historia y lo descompone en tareas por capa tecnológica.

```
A partir de la Historia de Usuario generada, descompón el trabajo técnico
necesario en Tareas Técnicas Jira por capa tecnológica.

HISTORIA DE USUARIO:
{{historia_json}}

STACK TECNOLÓGICO DEL PROYECTO:
{{stack_tecnologico}}
(Ejemplo: "Frontend: React 18 + TypeScript. Backend: Java 17 + Spring Boot.
BD: PostgreSQL 15. API: REST JSON. Auth: OAuth2 + JWT.")

CONVENCIONES DEL EQUIPO:
{{convenciones_equipo}}
(Ejemplo: "Las tareas de backend incluyen siempre tests unitarios.
Las tareas de frontend incluyen accesibilidad WCAG 2.1 AA.")

REGLAS DE DESCOMPOSICIÓN:
- Crea una tarea por capa tecnológica afectada.
- Nunca mezcles trabajo de frontend y backend en la misma tarea.
- Incluye siempre una tarea de testing si la historia tiene lógica de negocio.
- Incluye una tarea de base de datos si hay cambios en esquema o consultas nuevas.
- El campo "dependencias" indica qué tareas deben completarse antes.
- La estimación es en horas ideales (sin interrupciones).

Genera el siguiente JSON:

{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "[Verbo en infinitivo] + [componente] + [para qué]",
      "capa": "[backend │ frontend │ base_datos │ integracion │ testing │ devops]",
      "parent_story": "{{historia_jira_id}}",
      "description": {
        "objetivo": "[Qué debe implementarse exactamente]",
        "criterios_tecnico": [
          "[Criterio técnico verificable 1]",
          "[Criterio técnico verificable 2]"
        ],
        "consideraciones": ["[Decisión técnica relevante o restricción]"],
        "referencias": ["[Endpoint, tabla, componente o documento relevante]"]
      },
      "estimacion_horas": NÚMERO,
      "dependencias": ["[ID o summary de tarea que debe completarse antes]"],
      "labels": ["[etiqueta_tecnica]"],
      "components": ["[componente]"]
    }
  ]
}
```

**Ejemplo de output para la historia de filtrado de facturas:**

```json
{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "Implementar endpoint REST de filtrado de facturas por rango de fechas",
      "capa": "backend",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Crear el endpoint GET /api/v1/facturas con parámetros fecha_inicio y fecha_fin. Debe validar el rango máximo de 365 días, devolver resultados paginados ordenados por fecha descendente y responder en menos de 2 segundos para datasets de hasta 10.000 registros.",
        "criterios_tecnico": [
          "Validación de rango máximo 365 días con respuesta HTTP 400 y mensaje de error estándar",
          "Paginación con parámetros page y size (default: size=100)",
          "Respuesta en formato JSON con estructura: {data: [], total: N, page: N}",
          "Tests unitarios con cobertura mínima 80% de la lógica de validación"
        ],
        "consideraciones": [
          "Usar índice compuesto sobre (fecha_factura, id_empresa) para garantizar rendimiento",
          "El filtro se aplica sobre fecha_factura, no fecha_creacion"
        ],
        "referencias": ["Tabla: facturas", "Swagger: /api/v1/facturas#GET"]
      },
      "estimacion_horas": 6,
      "dependencias": ["Crear índice en tabla facturas"],
      "labels": ["backend", "api", "facturacion"],
      "components": ["api-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Crear índice de rendimiento en tabla facturas para filtrado por fecha",
      "capa": "base_datos",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Añadir índice compuesto (fecha_factura, id_empresa) a la tabla facturas para garantizar que las consultas por rango de fechas respondan en menos de 2 segundos con 10.000 registros.",
        "criterios_tecnico": [
          "Script de migración versionado con Flyway/Liquibase",
          "Validación de rendimiento en entorno de staging con dataset representativo",
          "Script de rollback incluido"
        ],
        "consideraciones": ["Ejecutar en ventana de mantenimiento en producción por impacto del índice"],
        "referencias": ["Tabla: facturas", "Política de migraciones: /docs/db-migrations"]
      },
      "estimacion_horas": 3,
      "dependencias": [],
      "labels": ["base-datos", "migracion", "facturacion"],
      "components": ["base-datos"]
    },
    {
      "issue_type": "Task",
      "summary": "Implementar componente de filtrado por fechas en el módulo Facturas",
      "capa": "frontend",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Añadir los campos fecha_inicio y fecha_fin al panel de filtros del listado de facturas. Incluir validación visual (campos en rojo) cuando el rango supere 365 días y mostrar el mensaje de error definido. El componente debe ser accesible según WCAG 2.1 AA.",
        "criterios_tecnico": [
          "Validación client-side del rango antes de llamar al API",
          "Estado de carga (skeleton loader) durante la petición",
          "Estado vacío con mensaje y botón 'Ampliar búsqueda'",
          "Tests de componente con React Testing Library",
          "Accesibilidad: labels asociados a inputs, mensajes de error con aria-live"
        ],
        "consideraciones": ["Reutilizar el componente DateRangePicker del design system interno"],
        "referencias": ["Design system: DateRangePicker", "Figma: Módulo Facturas v2.3"]
      },
      "estimacion_horas": 8,
      "dependencias": ["Implementar endpoint REST de filtrado de facturas por rango de fechas"],
      "labels": ["frontend", "facturacion", "accesibilidad"],
      "components": ["frontend-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Ejecutar pruebas de integración y rendimiento del filtrado de facturas",
      "capa": "testing",
      "parent_story": "FACT-47",
      "description": {
        "objetivo": "Validar los criterios de aceptación AC-023-01, AC-023-02 y AC-023-03 en entorno de integración. Incluir prueba de rendimiento con dataset de 10.000 registros.",
        "criterios_tecnico": [
          "Todos los AC documentados en Xray con resultado PASS",
          "Prueba de carga: p95 < 2 segundos con 50 usuarios concurrentes",
          "Prueba de contorno: rango exacto de 365 días debe funcionar, 366 debe fallar"
        ],
        "consideraciones": ["Usar datos de prueba anonimizados del entorno de staging"],
        "referencias": ["Test cases: TC-111, TC-112, TC-113, TC-114", "Xray: EP-04"]
      },
      "estimacion_horas": 4,
      "dependencias": [
        "Implementar endpoint REST de filtrado de facturas por rango de fechas",
        "Implementar componente de filtrado por fechas en el módulo Facturas"
      ],
      "labels": ["testing", "facturacion", "rendimiento"],
      "components": ["qa"]
    }
  ]
}
```

---

## Prompt 4 — Generación de Subtareas

Este prompt es **opcional** y se usa solo para tareas complejas (más de 8 horas estimadas) o cuando el equipo trabaja con subtareas para el tracking diario.

```
La siguiente Tarea Técnica supera las 8 horas estimadas o requiere descomposición
para seguimiento diario. Descomponla en subtareas que puedan completarse
de forma independiente en no más de 4 horas cada una.

TAREA TÉCNICA:
{{tarea_json}}

REGLAS:
- Cada subtarea debe ser completable en una sesión de trabajo (máx. 4 horas).
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
      "description": "[Qué exactamente debe estar hecho al terminar esta subtarea]",
      "criterio_completitud": "[Condición binaria: cómo saber que está terminada]",
      "estimacion_horas": NÚMERO,
      "orden": NÚMERO
    }
  ]
}
```

---

## Variantes de prompt por tipo de requisito

Los prompts anteriores funcionan para requisitos funcionales estándar. Estos son los **modificadores** que se añaden al Prompt 2 según el tipo:

**Para requisitos de integración con sistemas externos:**

```
CONTEXTO ADICIONAL - INTEGRACIÓN:
Este requisito implica integración con el sistema externo {{nombre_sistema}}.
Añade en las tareas técnicas una tarea específica de tipo "integracion" que incluya:
- Análisis del contrato de API/mensaje del sistema externo
- Manejo de errores de conectividad y timeouts
- Estrategia de retry y circuit breaker si aplica
```

**Para requisitos con reglas de negocio complejas:**

```
CONTEXTO ADICIONAL - REGLAS DE NEGOCIO:
Este requisito contiene reglas de negocio complejas o cálculos.
Para cada regla de negocio identificada, genera un criterio de aceptación
específico con ejemplos de datos concretos (Specification by Example).
Formato del ejemplo: "Dado que [valor_entrada], el resultado debe ser [valor_salida]".
```

**Para requisitos de modificación de funcionalidad existente:**

```
CONTEXTO ADICIONAL - MODIFICACIÓN DE FUNCIONALIDAD EXISTENTE:
Este requisito modifica funcionalidad ya existente en producción.
Añade obligatoriamente:
1. Una sección "impacto_en_funcionalidad_existente" en la descripción de la historia.
2. Un criterio de aceptación de regresión: el comportamiento anterior que NO debe cambiar.
3. Una tarea técnica de tipo "testing" específica para pruebas de regresión.
```

---

## Checklist de validación antes del push a Jira

Antes de que cualquier artefacto llegue a Jira, este prompt ejecuta una validación final:

```
Revisa el siguiente conjunto de artefactos generados y verifica que cumplen
todos los criterios de calidad. Responde SOLO con el JSON de validación.

ARTEFACTOS A REVISAR:
{{artefactos_json}}

Verifica cada punto y marca como true/false:

{
  "validacion": {
    "historia": {
      "tiene_rol_especifico": boolean,
      "tiene_beneficio_medible": boolean,
      "todos_ac_tienen_formato_dado_cuando_entonces": boolean,
      "ac_son_verificables_sin_ambiguedad": boolean,
      "no_mezcla_multiples_funcionalidades": boolean,
      "story_points_razonables": boolean
    },
    "tareas": {
      "cada_capa_tiene_su_tarea": boolean,
      "estimaciones_menores_de_8h": boolean,
      "dependencias_sin_ciclos": boolean,
      "tarea_testing_incluida": boolean
    },
    "trazabilidad": {
      "historia_vinculada_a_epica": boolean,
      "tareas_vinculadas_a_historia": boolean,
      "requisito_origen_referenciado": boolean
    }
  },
  "aprobado": boolean,
  "bloqueos": ["[Descripción del problema que impide el push]"],
  "advertencias": ["[Problema menor que no bloquea pero debería revisarse]"],
  "recomendacion": "[PUSH APROBADO │ REQUIERE REVISIÓN HUMANA │ BLOQUEADO]"
}
```

---

## Cómo implementarlo en la práctica hoy mismo

Si quieres probarlo antes de tener el pipeline automatizado, el flujo manual es:

1. Rellena el YAML de requisito con la plantilla de la sección 4 del modelo operativo.
2. Abre Claude o ChatGPT. Pega el System Prompt base + el Prompt 2.
3. Sustituye los placeholders `{{...}}` con tus valores reales.
4. Recibe el JSON de la historia. Revísalo.
5. Usa ese JSON como entrada del Prompt 3 para las tareas.
6. Pasa el conjunto por el checklist de validación.
7. Crea manualmente los issues en Jira o usa el importador CSV/JSON de Jira.

Con este flujo manual ya recuperas entre el 60% y el 70% del tiempo de creación de artefactos. La automatización completa con Jira API llega después, pero el valor es inmediato.

---

A continuación: [Punto 5 — Generación automática de test cases.](./105-test-cases.md)

---
