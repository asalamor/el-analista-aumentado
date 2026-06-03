# Pipeline de generación de épicas desde cero
## Desde el mapa de Event Storming hasta la jerarquía funcional en Jira

> **Posición en el modelo operativo:** Este documento cubre el gap identificado en la sección de puntos pendientes: el proceso de descubrimiento y creación de la jerarquía de épicas desde el mapa de Event Storming. Complementa el punto 4 (prompts de generación de artefactos Jira), que asume que la épica ya existe o se proporciona su JSON.

---

## Por qué las épicas merecen su propio pipeline

En el modelo operativo completo, el pipeline de generación de artefactos comienza en el requisito validado. Pero los requisitos no aparecen de la nada: son el resultado de un proceso de descubrimiento que transforma un mapa de Event Storming en una jerarquía funcional estructurada. Ese proceso de transformación —del post-it naranja al bloque YAML de épica— es exactamente lo que este pipeline cubre.

Sin él, la arquitectura de épicas se decide en conversaciones informales, en reuniones donde alguien propone nombres que nadie cuestiona, o directamente en Jira, donde es costoso cambiarla. Con este pipeline, la jerarquía emerge del mapa del dominio con criterios explícitos, se valida antes de convertirse en estructura permanente y llega a Jira con toda la información necesaria para que el equipo trabaje sobre ella desde el primer sprint.

La diferencia respecto al prompt de épica del punto 4 es de alcance y de entrada. El punto 4 toma el JSON de una épica ya definida y lo empuja a Jira. Este pipeline toma el artefacto bruto del taller de Event Storming —la captura YAML del punto 3 de la guía para analistas— y produce los YAMLs de épica listos para entrar en el repositorio y en Jira.

---

## Arquitectura del pipeline

El pipeline tiene cinco fases que operan en secuencia. Las tres primeras son de análisis y transformación; las dos últimas son de validación y generación de artefactos.

```
Captura YAML del taller de Event Storming
          │
          ▼
[Fase 1] Extracción y clasificación de eventos
          Identifica eventos de negocio, agrupa por dominio funcional,
          detecta dependencias causales entre eventos
          │
          ▼
[Fase 2] Propuesta de límites de dominio
          Genera candidatos a épica con criterios de cohesión,
          detecta solapamientos y propone alternativas de agrupación
          │
          ▼
[Fase 3] Validación con el glosario y las reglas de negocio globales
          Normaliza terminología, verifica coherencia con las épicas
          existentes en el repositorio, detecta conflictos
          │
          ▼
[Fase 4] Generación de YAMLs de épica
          Produce un archivo YAML completo por cada épica candidata
          aprobada, con todos los campos de la plantilla del punto 1
          │
          ▼
[Fase 5] Push a Jira y registro en el grafo de trazabilidad
          Crea las épicas en Jira con su jerarquía correcta,
          registra los nodos y aristas en el motor de trazabilidad
```

---

## Entrada del pipeline: la captura YAML del taller

El pipeline consume directamente el artefacto que produce la Fase 5 del taller de Event Storming, descrito en la guía para analistas (punto 3 del modelo operativo). El formato de entrada es el siguiente:

```yaml
# captura-taller-EP-04.yaml
# Salida directa de la Fase 5 del taller de Event Storming
# Proyecto: Sistema de Gestión de Facturación
# Fecha: 2025-05-12
# Participantes: Ana López, Carlos Ruiz, María García, Pedro Sánchez

eventos_identificados:
  - evento: "Factura recibida"
    epica_candidata: "Recepción de facturas"
    actores_involucrados: ["Proveedor", "Sistema de correo"]
    comandos_que_lo_causan: ["Registrar factura en el sistema"]
    politicas_asociadas:
      - "Si el importe supera 10.000€, asignar al Responsable financiero"
    puntos_de_dolor:
      - "Actualmente se registra manualmente copiando datos del email"
    preguntas_abiertas:
      - "¿Cuál es el plazo máximo para registrar una factura recibida?"
    vistas_necesarias:
      - "Bandeja de facturas pendientes de registro"
    dependencias_causales: []

  - evento: "Revisión iniciada"
    epica_candidata: "Gestión y revisión de facturas"
    actores_involucrados: ["Gestor de facturación"]
    comandos_que_lo_causan: ["Abrir factura para revisión"]
    politicas_asociadas:
      - "Solo facturas en estado pendiente pueden iniciarse para revisión"
    puntos_de_dolor: []
    preguntas_abiertas: []
    vistas_necesarias:
      - "Detalle de factura con histórico de cambios"
    dependencias_causales: ["Factura recibida"]

  - evento: "Factura aprobada"
    epica_candidata: "Gestión y revisión de facturas"
    actores_involucrados: ["Gestor de facturación", "Responsable financiero"]
    comandos_que_lo_causan: ["Aprobar factura"]
    politicas_asociadas:
      - "Facturas con importe >10.000€ requieren Responsable financiero"
      - "La aprobación queda registrada con fecha, hora y usuario"
    puntos_de_dolor:
      - "No hay trazabilidad de quién aprobó qué y cuándo"
    preguntas_abiertas:
      - "¿Puede un gestor aprobar su propia factura?"
    vistas_necesarias:
      - "Historial de aprobaciones"
    dependencias_causales: ["Revisión iniciada"]

  - evento: "Factura rechazada"
    epica_candidata: "Gestión y revisión de facturas"
    actores_involucrados: ["Gestor de facturación", "Responsable financiero"]
    comandos_que_lo_causan: ["Rechazar factura"]
    politicas_asociadas:
      - "El rechazo requiere nota de motivo de al menos 20 caracteres"
    puntos_de_dolor: []
    preguntas_abiertas: []
    vistas_necesarias: []
    dependencias_causales: ["Revisión iniciada"]

  - evento: "Pago programado"
    epica_candidata: "Proceso de pago"
    actores_involucrados: ["Sistema", "Área de tesorería"]
    comandos_que_lo_causan: ["Programar pago según condiciones del proveedor"]
    politicas_asociadas:
      - "El pago se programa según las condiciones pactadas con el proveedor"
    puntos_de_dolor:
      - "El proceso de programación de pagos es manual y propenso a errores"
    preguntas_abiertas:
      - "¿Qué ocurre si el banco rechaza la transferencia?"
    vistas_necesarias:
      - "Calendario de pagos pendientes"
    dependencias_causales: ["Factura aprobada"]

  - evento: "Pago ejecutado"
    epica_candidata: "Proceso de pago"
    actores_involucrados: ["Sistema banco", "Área de tesorería"]
    comandos_que_lo_causan: ["Ejecutar transferencia"]
    politicas_asociadas: []
    puntos_de_dolor: []
    preguntas_abiertas: []
    vistas_necesarias: []
    dependencias_causales: ["Pago programado"]

preguntas_sin_resolver:
  - pregunta: "¿Cuál es el plazo máximo de revisión de una factura?"
    impacto: "Define el SLA y los criterios de escalado automático"
    responsable_respuesta: "Ana López (Dirección Financiera)"
    plazo_respuesta: "2025-05-15"
  - pregunta: "¿Puede un gestor aprobar su propia factura?"
    impacto: "Define las reglas de segregación de funciones"
    responsable_respuesta: "Pedro Sánchez (Cumplimiento)"
    plazo_respuesta: "2025-05-15"
  - pregunta: "¿Qué ocurre si el banco rechaza la transferencia?"
    impacto: "Define el flujo de excepción del proceso de pago"
    responsable_respuesta: "María García (Tesorería)"
    plazo_respuesta: "2025-05-20"

epicas_candidatas_del_taller:
  - nombre_provisional: "Recepción de facturas"
    eventos: ["Factura recibida"]
  - nombre_provisional: "Gestión y revisión de facturas"
    eventos: ["Revisión iniciada", "Factura aprobada", "Factura rechazada"]
  - nombre_provisional: "Proceso de pago"
    eventos: ["Pago programado", "Pago ejecutado"]
```

---

## Fase 1 — Extracción y clasificación de eventos

### System prompt base para el pipeline de épicas

```
Eres un arquitecto de dominio con experiencia en Event Storming y diseño
de sistemas Agile. Tu función es transformar los artefactos brutos de un
taller de Event Storming en una jerarquía de épicas estructurada, coherente
y lista para ser gestionada en Jira.

REGLAS ESTRICTAS:
1. Nunca fusiones eventos de dominios funcionales claramente distintos en
   una misma épica solo porque tengan actores en común.
2. Una épica debe poder describirse con una capacidad de negocio completa:
   "El sistema permite al negocio [hacer X completo]". Si la frase queda
   incompleta sin mencionar otra épica, los límites están mal trazados.
3. Las dependencias causales entre eventos son información, no necesariamente
   fronteras. Que el evento B dependa del evento A no significa que deban
   estar en la misma épica.
4. Las preguntas abiertas del taller son riesgos de alcance. Si una pregunta
   abierta afecta al alcance de una épica candidata, indícalo explícitamente.
5. El output es siempre JSON válido. Sin texto antes ni después del JSON.

GLOSARIO DEL PROYECTO:
{{glosario_yaml}}

ÉPICAS EXISTENTES EN EL REPOSITORIO (para detectar solapamientos):
{{epicas_existentes}}
```

### Prompt 1 — Análisis de cohesión de eventos

```
A partir de la captura del taller de Event Storming, analiza la cohesión
de los eventos identificados y valida o propone alternativas a las
agrupaciones provisionales del analista.

CAPTURA DEL TALLER:
{{captura_taller_yaml}}

Para cada agrupación candidata del taller, evalúa:

CRITERIO A — Cohesión funcional
  ¿Los eventos del grupo describen un proceso de negocio completo y cohesivo?
  ¿Comparten el mismo objetivo de negocio o resuelven el mismo problema?
  ¿El conjunto de eventos puede implementarse de forma relativamente independiente?

CRITERIO B — Homogeneidad de actores
  ¿Los actores principales de los eventos son los mismos o relacionados?
  ¿Un cambio en las reglas de negocio de un evento afectaría a todos los demás?

CRITERIO C — Tamaño razonable
  Un grupo con más de 8 eventos probablemente es demasiado grande.
  Un grupo con menos de 2 eventos probablemente es demasiado pequeño.
  ¿El tamaño es implementable en 2-4 sprints?

CRITERIO D — Independencia de entrega
  ¿El grupo puede entregarse con valor para el negocio aunque los demás
  grupos no estén completados?

Para cada agrupación, indica si la propuesta del analista es:
  APROBADA      → cohesión correcta, ningún cambio
  AJUSTADA      → correcta en concepto pero con límites que mejorar
  RECHAZADA     → la agrupación mezcla dominios distintos o no tiene coherencia

Genera:
{
  "analisis_agrupaciones": [
    {
      "nombre_provisional": "[nombre del taller]",
      "eventos_incluidos": ["[evento 1]", "[evento 2]"],
      "veredicto": "APROBADA | AJUSTADA | RECHAZADA",
      "puntuacion_cohesion": N,
      "escala_cohesion": "0-10 donde 10 es cohesión perfecta",
      "justificacion": "[Por qué se aprueba, ajusta o rechaza]",
      "ajuste_propuesto": {
        "aplica": true | false,
        "descripcion": "[Qué cambio se propone y por qué]",
        "eventos_a_mover": ["[evento]"],
        "destino_sugerido": "[nombre de la agrupación destino]"
      },
      "riesgos_de_alcance": [
        {
          "pregunta_abierta": "[pregunta sin resolver del taller]",
          "impacto_en_esta_epica": "[cómo afecta al alcance]"
        }
      ]
    }
  ],
  "eventos_sin_agrupacion": ["[evento que no encaja en ninguna candidata]"],
  "solapamientos_con_repositorio": [
    {
      "epica_existente": "[ID de épica en el repositorio]",
      "eventos_en_conflicto": ["[evento]"],
      "tipo_conflicto": "duplicado | extensión | contradicción",
      "recomendacion": "[Qué hacer]"
    }
  ]
}
```

### Ejemplo de output del Prompt 1

```json
{
  "analisis_agrupaciones": [
    {
      "nombre_provisional": "Recepción de facturas",
      "eventos_incluidos": ["Factura recibida"],
      "veredicto": "AJUSTADA",
      "puntuacion_cohesion": 6,
      "escala_cohesion": "0-10 donde 10 es cohesión perfecta",
      "justificacion": "El único evento identificado en el taller es 'Factura recibida', pero el proceso de recepción implica necesariamente el registro, la validación del proveedor y la notificación. Con un solo evento, la épica no es implementable de forma independiente. Se recomienda explorar si existen eventos de registro y validación que no se capturaron en el taller.",
      "ajuste_propuesto": {
        "aplica": true,
        "descripcion": "Añadir los eventos de registro de factura y validación de proveedor activo que son prerequisito lógico del evento 'Factura recibida' para que la épica sea autónoma.",
        "eventos_a_mover": [],
        "destino_sugerido": ""
      },
      "riesgos_de_alcance": [
        {
          "pregunta_abierta": "¿Cuál es el plazo máximo para registrar una factura recibida?",
          "impacto_en_esta_epica": "Define si existe un flujo de alerta o escalado por registro tardío que debe incluirse en el alcance de esta épica."
        }
      ]
    },
    {
      "nombre_provisional": "Gestión y revisión de facturas",
      "eventos_incluidos": ["Revisión iniciada", "Factura aprobada", "Factura rechazada"],
      "veredicto": "APROBADA",
      "puntuacion_cohesion": 9,
      "escala_cohesion": "0-10 donde 10 es cohesión perfecta",
      "justificacion": "Los tres eventos forman un proceso cohesivo con el mismo objetivo de negocio (validar la factura), comparten los mismos actores principales y sus reglas de negocio están interrelacionadas. La épica puede entregarse con valor independiente.",
      "ajuste_propuesto": {
        "aplica": false,
        "descripcion": "",
        "eventos_a_mover": [],
        "destino_sugerido": ""
      },
      "riesgos_de_alcance": [
        {
          "pregunta_abierta": "¿Puede un gestor aprobar su propia factura?",
          "impacto_en_esta_epica": "Si la respuesta es no, el flujo de aprobación necesita una validación de segregación de funciones que aumenta el alcance de esta épica."
        }
      ]
    },
    {
      "nombre_provisional": "Proceso de pago",
      "eventos_incluidos": ["Pago programado", "Pago ejecutado"],
      "veredicto": "APROBADA",
      "puntuacion_cohesion": 8,
      "escala_cohesion": "0-10 donde 10 es cohesión perfecta",
      "justificacion": "Los dos eventos forman un proceso cohesivo con objetivo claro. La dependencia causal con 'Factura aprobada' es de entrada, no de pertenencia funcional.",
      "ajuste_propuesto": {
        "aplica": false,
        "descripcion": "",
        "eventos_a_mover": [],
        "destino_sugerido": ""
      },
      "riesgos_de_alcance": [
        {
          "pregunta_abierta": "¿Qué ocurre si el banco rechaza la transferencia?",
          "impacto_en_esta_epica": "Determina si existe un flujo de excepción de reintento o notificación de rechazo que debe incluirse en el alcance."
        }
      ]
    }
  ],
  "eventos_sin_agrupacion": [],
  "solapamientos_con_repositorio": []
}
```

---

## Fase 2 — Propuesta de límites de dominio y jerarquía

### Prompt 2 — Definición de la jerarquía de épicas

```
A partir del análisis de cohesión, genera la propuesta definitiva de
jerarquía de épicas con sus relaciones, dependencias y el orden de
implementación recomendado.

ANÁLISIS DE COHESIÓN:
{{analisis_agrupaciones_json}}

CAPTURA COMPLETA DEL TALLER:
{{captura_taller_yaml}}

ESTRUCTURA DEL PROYECTO EXISTENTE (épicas en Jira):
{{estructura_existente}}

REGLAS DE JERARQUÍA:
- Una épica es un conjunto de funcionalidad que habilita una capacidad
  de negocio completa. No es un módulo técnico.
- El nombre oficial de la épica usa el formato: [Verbo en gerundio]
  + [objeto de negocio] + [contexto si es necesario].
  Ejemplos: "Recepción y registro de facturas",
  "Revisión y aprobación de facturas", "Ejecución de pagos a proveedores".
- Los IDs de épica siguen el formato EP-NN. Asignar el siguiente disponible
  tras las épicas existentes.
- El campo 'orden_implementacion' indica la secuencia recomendada basada
  en las dependencias causales entre eventos. Valor 1 = primera a implementar.

Genera:
{
  "jerarquia_epicas": [
    {
      "id_propuesto": "EP-NN",
      "nombre_oficial": "[Nombre en formato estándar]",
      "nombre_corto": "[Máximo 4 palabras para Epic Name en Jira]",
      "descripcion": {
        "objetivo": "[Qué capacidad de negocio habilita esta épica. 2-3 frases.]",
        "alcance_incluye": ["[Funcionalidad incluida 1]", "[Funcionalidad incluida 2]"],
        "alcance_excluye": ["[Funcionalidad explícitamente excluida]"],
        "valor_negocio": "[Beneficio medible para el negocio o usuario final]",
        "problemas_que_resuelve": ["[Punto de dolor del taller que resuelve]"]
      },
      "actores_principales": ["[Actor del glosario]"],
      "eventos_origen": ["[Evento del taller que justifica esta épica]"],
      "dependencias": {
        "epicas_previas": ["[EP-NN que debe estar implementada antes]"],
        "tipo_dependencia": "bloqueante | deseable | ninguna"
      },
      "orden_implementacion": N,
      "estimacion_sprints": {
        "minimo": N,
        "maximo": N,
        "base": "[Justificación de la estimación]"
      },
      "prioridad": "must-have | should-have | could-have",
      "preguntas_abiertas_asociadas": ["[Pregunta del taller que afecta a esta épica]"],
      "riesgos": [
        {
          "descripcion": "[Riesgo identificado]",
          "probabilidad": "alta | media | baja",
          "impacto": "alto | medio | bajo"
        }
      ],
      "kpis_exito": ["[KPI medible que indica que la épica aporta valor]"]
    }
  ],
  "resumen_jerarquia": {
    "total_epicas": N,
    "epicas_must_have": N,
    "sprints_estimados_total": N,
    "dependencias_criticas": [
      {
        "epica_bloqueante": "EP-NN",
        "epica_bloqueada": "EP-NN",
        "motivo": "[Por qué la dependencia es crítica]"
      }
    ]
  }
}
```

### Ejemplo de output del Prompt 2

```json
{
  "jerarquia_epicas": [
    {
      "id_propuesto": "EP-03",
      "nombre_oficial": "Recepción y registro de facturas de proveedor",
      "nombre_corto": "Recepción facturas",
      "descripcion": {
        "objetivo": "Habilitar la recepción estructurada y el registro centralizado de facturas de proveedor, eliminando el proceso manual basado en correo electrónico. Garantiza que toda factura quede registrada en el sistema con los datos necesarios para iniciar su revisión.",
        "alcance_incluye": [
          "Registro manual de facturas por el Gestor de facturación",
          "Recepción automática desde buzón de correo electrónico",
          "Validación de proveedor activo en el catálogo",
          "Notificación al gestor asignado al recibir una factura",
          "Vista de bandeja de facturas pendientes de registro"
        ],
        "alcance_excluye": [
          "Revisión y aprobación de facturas (cubierto por EP-04)",
          "Gestión del catálogo de proveedores",
          "Integración EDI con proveedores (fase futura)"
        ],
        "valor_negocio": "Reducción del tiempo de registro de facturas de 30 minutos a menos de 5 minutos por factura. Eliminación de facturas perdidas o no registradas.",
        "problemas_que_resuelve": [
          "Actualmente se registra manualmente copiando datos del email"
        ]
      },
      "actores_principales": ["Gestor de facturación"],
      "eventos_origen": ["Factura recibida"],
      "dependencias": {
        "epicas_previas": [],
        "tipo_dependencia": "ninguna"
      },
      "orden_implementacion": 1,
      "estimacion_sprints": {
        "minimo": 2,
        "maximo": 3,
        "base": "Proceso de recepción de complejidad media. La integración con buzón de correo puede requerir un sprint adicional si hay restricciones de seguridad del servidor de correo."
      },
      "prioridad": "must-have",
      "preguntas_abiertas_asociadas": [
        "¿Cuál es el plazo máximo para registrar una factura recibida?"
      ],
      "riesgos": [
        {
          "descripcion": "La integración automática con el buzón de correo puede bloquearse por políticas de seguridad IT",
          "probabilidad": "media",
          "impacto": "medio"
        }
      ],
      "kpis_exito": [
        "Tiempo medio de registro por factura < 5 minutos",
        "0% de facturas recibidas sin registro en 24 horas laborables"
      ]
    },
    {
      "id_propuesto": "EP-04",
      "nombre_oficial": "Revisión y aprobación de facturas",
      "nombre_corto": "Gestión facturas",
      "descripcion": {
        "objetivo": "Habilitar al Gestor de facturación y al Responsable financiero para revisar, filtrar, aprobar o rechazar facturas con trazabilidad completa de cada decisión. Garantiza el cumplimiento de las políticas de aprobación según importe y el registro auditable de cada acción.",
        "alcance_incluye": [
          "Filtrado y búsqueda de facturas por múltiples criterios",
          "Flujo de aprobación para facturas ≤ 10.000€ (Gestor)",
          "Flujo de aprobación para facturas > 10.000€ (Responsable financiero)",
          "Flujo de rechazo con nota de motivo obligatoria",
          "Historial de acciones por factura",
          "Validación de segregación de funciones"
        ],
        "alcance_excluye": [
          "Registro de nuevas facturas (cubierto por EP-03)",
          "Ejecución del pago (cubierto por EP-05)",
          "Configuración de umbrales de aprobación"
        ],
        "valor_negocio": "Reducción del tiempo del ciclo de aprobación de facturas. Trazabilidad completa para auditoría. Cumplimiento automático de las políticas de aprobación por importe.",
        "problemas_que_resuelve": [
          "No hay trazabilidad de quién aprobó qué y cuándo"
        ]
      },
      "actores_principales": ["Gestor de facturación", "Responsable financiero"],
      "eventos_origen": ["Revisión iniciada", "Factura aprobada", "Factura rechazada"],
      "dependencias": {
        "epicas_previas": ["EP-03"],
        "tipo_dependencia": "bloqueante"
      },
      "orden_implementacion": 2,
      "estimacion_sprints": {
        "minimo": 3,
        "maximo": 4,
        "base": "Proceso con múltiples flujos alternativos (aprobación por umbral de importe, rechazo, filtrado avanzado). La pregunta abierta sobre segregación de funciones puede añadir complejidad."
      },
      "prioridad": "must-have",
      "preguntas_abiertas_asociadas": [
        "¿Puede un gestor aprobar su propia factura?"
      ],
      "riesgos": [
        {
          "descripcion": "La regla de segregación de funciones puede requerir cambios en el modelo de datos de usuarios si no existe el concepto de 'propietario de factura'",
          "probabilidad": "media",
          "impacto": "alto"
        }
      ],
      "kpis_exito": [
        "Tiempo medio de ciclo de aprobación < 48 horas laborables",
        "100% de aprobaciones con registro de usuario, fecha y hora",
        "0% de facturas aprobadas violando la política de segregación de funciones"
      ]
    },
    {
      "id_propuesto": "EP-05",
      "nombre_oficial": "Ejecución de pagos a proveedores",
      "nombre_corto": "Pagos proveedores",
      "descripcion": {
        "objetivo": "Habilitar la programación y ejecución de pagos a proveedores desde las facturas aprobadas, con calendario de pagos visible y gestión de excepciones por rechazo bancario.",
        "alcance_incluye": [
          "Programación automática del pago según condiciones del proveedor",
          "Vista de calendario de pagos pendientes",
          "Registro de pago ejecutado",
          "Notificación al proveedor tras el pago",
          "Flujo de excepción por rechazo bancario"
        ],
        "alcance_excluye": [
          "Aprobación de facturas (cubierto por EP-04)",
          "Configuración de condiciones de pago por proveedor",
          "Conciliación bancaria automática (fase futura)"
        ],
        "valor_negocio": "Eliminación del proceso manual de programación de pagos. Reducción de errores en transferencias. Trazabilidad completa del ciclo factura-pago.",
        "problemas_que_resuelve": [
          "El proceso de programación de pagos es manual y propenso a errores"
        ]
      },
      "actores_principales": ["Área de tesorería"],
      "eventos_origen": ["Pago programado", "Pago ejecutado"],
      "dependencias": {
        "epicas_previas": ["EP-04"],
        "tipo_dependencia": "bloqueante"
      },
      "orden_implementacion": 3,
      "estimacion_sprints": {
        "minimo": 2,
        "maximo": 4,
        "base": "La integración con el sistema bancario es la variable de mayor incertidumbre. Si existe un API bancario estándar, 2 sprints. Si requiere integración con un core bancario propietario, hasta 4."
      },
      "prioridad": "must-have",
      "preguntas_abiertas_asociadas": [
        "¿Qué ocurre si el banco rechaza la transferencia?"
      ],
      "riesgos": [
        {
          "descripcion": "La integración con el sistema bancario puede estar fuera del alcance del equipo y requerir un proveedor externo",
          "probabilidad": "alta",
          "impacto": "alto"
        }
      ],
      "kpis_exito": [
        "0% de pagos programados manualmente (en el estado final)",
        "Tiempo entre aprobación de factura y programación del pago < 1 hora",
        "100% de pagos ejecutados con notificación al proveedor"
      ]
    }
  ],
  "resumen_jerarquia": {
    "total_epicas": 3,
    "epicas_must_have": 3,
    "sprints_estimados_total": "7-11 sprints",
    "dependencias_criticas": [
      {
        "epica_bloqueante": "EP-03",
        "epica_bloqueada": "EP-04",
        "motivo": "Sin facturas registradas no existe material para revisar"
      },
      {
        "epica_bloqueante": "EP-04",
        "epica_bloqueada": "EP-05",
        "motivo": "Solo se pueden pagar facturas aprobadas"
      }
    ]
  }
}
```

---

## Fase 3 — Validación con el glosario y las épicas existentes

### Prompt 3 — Validación de consistencia

```
Valida que la jerarquía de épicas propuesta es coherente con el glosario
del proyecto, no solapa con épicas existentes y usa terminología oficial.

JERARQUÍA PROPUESTA:
{{jerarquia_epicas_json}}

GLOSARIO DEL PROYECTO:
{{glosario_yaml}}

ÉPICAS EXISTENTES EN EL REPOSITORIO:
{{epicas_existentes_yaml}}

ANÁLISIS REQUERIDO:

BLOQUE A — Terminología
  ¿Los nombres de los actores coinciden con los nombres oficiales del glosario?
  ¿Los nombres de las entidades de negocio coinciden con el glosario?
  ¿Los verbos usados en los nombres de las épicas son los verbos oficiales?

BLOQUE B — Solapamiento con épicas existentes
  ¿Alguna funcionalidad del alcance_incluye de las nuevas épicas ya está
  cubierta por una épica existente en el repositorio?
  ¿Alguna nueva épica es extensión natural de una existente en lugar de
  ser una épica nueva?

BLOQUE C — Completitud causal
  ¿Las dependencias entre épicas forman un grafo acíclico sin gaps?
  ¿Existe alguna funcionalidad que se menciona en el alcance_incluye de
  una épica pero depende de algo que ninguna otra épica cubre?

BLOQUE D — Coherencia de prioridad
  ¿Es coherente que una épica de prioridad must-have dependa de una
  épica de prioridad should-have o could-have?

Genera:
{
  "validacion": {
    "resultado": "APROBADA | APROBADA_CON_AJUSTES | BLOQUEADA",
    "analisis_por_bloque": {
      "terminologia": { "resultado": "LIMPIO | PROBLEMAS", "problemas": [] },
      "solapamiento": { "resultado": "LIMPIO | PROBLEMAS", "problemas": [] },
      "completitud_causal": { "resultado": "LIMPIO | PROBLEMAS", "problemas": [] },
      "coherencia_prioridad": { "resultado": "LIMPIO | PROBLEMAS", "problemas": [] }
    },
    "ajustes_requeridos": [
      {
        "epica_afectada": "EP-NN",
        "campo": "[campo a ajustar]",
        "valor_actual": "[valor que tiene]",
        "valor_correcto": "[valor que debe tener]",
        "motivo": "[por qué]"
      }
    ]
  }
}
```

---

## Fase 4 — Generación de YAMLs de épica

Una vez validada la jerarquía, el pipeline genera un archivo YAML completo por cada épica. Este YAML cumple exactamente el formato del Bloque 1 de la plantilla del punto 1 del modelo operativo, con los campos propios de una épica en lugar de un requisito.

### Plantilla YAML de épica

```yaml
# ─────────────────────────────────────────────────────────────
# ÉPICA — Plantilla AI-Ready
# Fuente: Pipeline de generación de épicas desde Event Storming
# ─────────────────────────────────────────────────────────────

# BLOQUE 1 — IDENTIDAD
id: EP-NN
nombre_oficial: ""
nombre_corto: ""           # Máximo 4 palabras para el campo Epic Name de Jira
version: "1.0"
estado: propuesta          # propuesta | aprobada | en-desarrollo | completada | deprecada
origen:
  taller_event_storming: ""  # Nombre o fecha del taller donde emergió esta épica
  captura_yaml: ""           # Ruta al archivo de captura del taller
  aprobado_por: ""
  fecha_aprobacion: ""
analista_responsable: ""

# BLOQUE 2 — DESCRIPCIÓN DE NEGOCIO
descripcion:
  objetivo: ""
  alcance_incluye: []
  alcance_excluye: []
  valor_negocio: ""
  problemas_que_resuelve: []
actores_principales: []
eventos_origen: []           # Eventos del taller que justifican esta épica
prioridad: must-have         # must-have | should-have | could-have | wont-have

# BLOQUE 3 — DEPENDENCIAS Y ORDEN
dependencias:
  epicas_previas: []
  tipo_dependencia: ninguna  # bloqueante | deseable | ninguna
orden_implementacion: N
estimacion_sprints:
  minimo: N
  maximo: N
  base: ""

# BLOQUE 4 — CALIDAD Y MÉTRICAS
kpis_exito: []
preguntas_abiertas_asociadas: []
riesgos: []

# BLOQUE 5 — TRAZABILIDAD (auto-generado por el pipeline)
trazabilidad:
  requisitos: []             # IDs de requisitos derivados de esta épica
  jira_epic_key: null        # Clave Jira asignada al crear la épica
  fecha_creacion_jira: null
```

### Prompt 4 — Generación del YAML completo por épica

```
A partir de la jerarquía validada y la captura del taller, genera el
archivo YAML completo para la épica indicada, listo para ser almacenado
en el repositorio de requisitos.

ÉPICA A GENERAR:
{{epica_json}}

CAPTURA COMPLETA DEL TALLER (para extraer contexto adicional):
{{captura_taller_yaml}}

GLOSARIO (para garantizar terminología correcta):
{{glosario_yaml}}

INSTRUCCIONES:
- Usa exclusivamente los términos oficiales del glosario.
- El campo 'objetivo' debe explicar el valor de negocio en lenguaje
  que entienda un usuario de negocio, sin tecnicismos.
- El campo 'alcance_excluye' es tan importante como 'alcance_incluye':
  gestiona expectativas desde el inicio.
- Los 'kpis_exito' deben ser medibles sin ambigüedad.
- Los 'riesgos' deben incluir solo los identificados en el taller o
  inferibles del análisis de cohesión. No inventar riesgos genéricos.
- El output es el YAML completo del archivo, no un JSON envolvente.
  Empieza directamente con los comentarios de cabecera del YAML.
```

### Ejemplo de YAML generado para EP-04

```yaml
# ─────────────────────────────────────────────────────────────
# ÉPICA — AI-Ready
# Fuente: Taller Event Storming — Gestión de Facturación
# Generado por pipeline: 2025-05-12T10:47:00Z
# ─────────────────────────────────────────────────────────────

id: EP-04
nombre_oficial: "Revisión y aprobación de facturas"
nombre_corto: "Gestión facturas"
version: "1.0"
estado: propuesta
origen:
  taller_event_storming: "Taller Facturación — 2025-05-10"
  captura_yaml: "talleres/captura-taller-EP-04.yaml"
  aprobado_por: null
  fecha_aprobacion: null
analista_responsable: "Carlos Ruiz"

descripcion:
  objetivo: >
    El Gestor de facturación y el Responsable financiero necesitan poder
    revisar las facturas recibidas, aprobarlas o rechazarlas con trazabilidad
    completa de cada decisión. Esta épica habilita ese proceso completo,
    garantizando que las facturas superiores a 10.000€ siempre pasen por el
    Responsable financiero y que cada acción quede registrada para auditoría.
  alcance_incluye:
    - "Filtrado y búsqueda de facturas por fecha, estado, proveedor e importe"
    - "Flujo de aprobación para facturas con importe ≤ 10.000€ (Gestor de facturación)"
    - "Flujo de aprobación para facturas con importe > 10.000€ (Responsable financiero)"
    - "Flujo de rechazo con nota de motivo obligatoria (mínimo 20 caracteres)"
    - "Historial de acciones por factura: quién hizo qué y cuándo"
    - "Validación de segregación de funciones: un gestor no puede aprobar facturas que él mismo registró"
  alcance_excluye:
    - "Registro de nuevas facturas: cubierto por EP-03"
    - "Ejecución y programación del pago: cubierto por EP-05"
    - "Configuración de umbrales de aprobación por importe: módulo de administración"
    - "Gestión del catálogo de proveedores"
  valor_negocio: >
    Reducción del tiempo del ciclo de aprobación de facturas de varios días a
    menos de 48 horas laborables. Trazabilidad completa para auditoría interna
    y externa. Cumplimiento automático de las políticas de aprobación por importe
    sin dependencia de la memoria o criterio individual de cada gestor.
  problemas_que_resuelve:
    - "No hay trazabilidad de quién aprobó qué y cuándo"
    - "Las aprobaciones se gestionan por email sin registro centralizado"

actores_principales:
  - "Gestor de facturación"
  - "Responsable financiero"
eventos_origen:
  - "Revisión iniciada"
  - "Factura aprobada"
  - "Factura rechazada"
prioridad: must-have

dependencias:
  epicas_previas:
    - "EP-03"
  tipo_dependencia: bloqueante
orden_implementacion: 2
estimacion_sprints:
  minimo: 3
  maximo: 4
  base: >
    Proceso con múltiples flujos alternativos (aprobación por umbral de importe,
    rechazo, filtrado avanzado, historial). La pregunta abierta sobre segregación
    de funciones puede añadir un sprint si el modelo de datos actual no tiene el
    concepto de propietario de factura.

kpis_exito:
  - "Tiempo medio de ciclo de aprobación < 48 horas laborables"
  - "100% de aprobaciones con registro de usuario, fecha y hora exactos"
  - "0% de facturas aprobadas violando la política de importe"
  - "Reducción del 80% en el tiempo de preparación de documentación para auditoría"

preguntas_abiertas_asociadas:
  - pregunta: "¿Puede un gestor aprobar su propia factura?"
    impacto: "Define si existe la regla de segregación de funciones y cómo se implementa técnicamente"
    responsable_respuesta: "Pedro Sánchez (Cumplimiento)"
    plazo_respuesta: "2025-05-15"
    bloquea_inicio: true

riesgos:
  - descripcion: "La regla de segregación de funciones puede requerir cambios en el modelo de datos de usuarios si no existe el concepto de propietario de factura"
    probabilidad: media
    impacto: alto
    mitigacion: "Analizar el modelo de datos de usuarios en la fase de arquitectura antes de comenzar el sprint 1 de esta épica"
  - descripcion: "La pregunta sobre segregación de funciones está sin resolver y bloquea la definición de los criterios de aceptación del flujo de aprobación"
    probabilidad: alta
    impacto: medio
    mitigacion: "Escalar al responsable de cumplimiento para respuesta antes de la fecha límite del 2025-05-15"

trazabilidad:
  requisitos: []
  jira_epic_key: null
  fecha_creacion_jira: null
```

---

## Fase 5 — Push a Jira y registro en el grafo de trazabilidad

Esta fase reutiliza directamente el `ConectorJira` y el `MotorTrazabilidad` del punto 10 del modelo operativo, con adaptaciones específicas para épicas.

### Adaptación del constructor de payloads para épicas desde este pipeline

Las épicas generadas por este pipeline tienen un campo adicional respecto a las del punto 4: el campo `eventos_origen`, que documenta su procedencia del Event Storming. Se persiste en un campo personalizado de Jira para mantener la trazabilidad completa desde el taller hasta el artefacto.

```python
def construir_epica_desde_pipeline_es(
    self,
    epica_yaml: dict,
    config: JiraConfig
) -> dict:
    """
    Construye el payload Jira para una épica generada por el
    pipeline de Event Storming. Extiende el constructor base
    del punto 10 con los campos específicos de este pipeline.
    """
    payload_base = self.construir_epica(epica_yaml)

    # Añadir campos específicos del pipeline de Event Storming
    payload_base["fields"].update({
        # Documenta el taller de origen para trazabilidad
        config.campo_taller_origen: (
            epica_yaml.get("origen", {})
            .get("taller_event_storming", "")
        ),
        # Lista los eventos del taller que justifican la épica
        config.campo_eventos_origen: ", ".join(
            epica_yaml.get("eventos_origen", [])
        ),
        # Orden de implementación para la planificación de roadmap
        config.campo_orden_implementacion: (
            epica_yaml.get("orden_implementacion", 99)
        )
    })

    return payload_base


def registrar_epica_en_grafo(
    self,
    epica_yaml: dict,
    jira_key: str,
    motor_trazabilidad
):
    """
    Registra la épica en el grafo de trazabilidad con sus
    dependencias con otras épicas y su origen en el taller.
    """
    # Registrar el nodo de la épica
    motor_trazabilidad.registrar_nodo(Nodo(
        id=jira_key,
        tipo="epic",
        titulo=epica_yaml["nombre_oficial"],
        estado="To Do",
        metadatos={
            "id_funcional": epica_yaml["id"],
            "prioridad": epica_yaml["prioridad"],
            "orden_implementacion": epica_yaml.get(
                "orden_implementacion", 99
            ),
            "eventos_origen": epica_yaml.get("eventos_origen", []),
            "taller_origen": epica_yaml.get("origen", {}).get(
                "taller_event_storming", ""
            )
        }
    ))

    # Registrar las dependencias entre épicas
    for epica_previa_id in (
        epica_yaml.get("dependencias", {}).get("epicas_previas", [])
    ):
        # El ID funcional (EP-NN) se resuelve al key Jira real
        # usando el mapa almacenado durante el procesamiento del lote
        motor_trazabilidad.registrar_arista(Arista(
            origen_id=jira_key,
            destino_id=epica_previa_id,  # Se resuelve a key Jira en el orquestador
            tipo_relacion="depende_de",
            confianza=1.0,
            origen_relacion="pipeline_event_storming"
        ))
```

### Orquestación del lote de épicas

Cuando el pipeline procesa varias épicas de un mismo taller, el orden de creación en Jira debe respetar las dependencias: primero las épicas sin dependencias, luego las que dependen de ellas.

```python
async def push_jerarquia_epicas(
    jerarquia: dict,
    config: PipelineConfig,
    motor_trazabilidad
) -> dict:
    """
    Crea todas las épicas de la jerarquía en Jira respetando
    el orden de implementación y registrando las dependencias.
    """
    epicas = sorted(
        jerarquia["jerarquia_epicas"],
        key=lambda e: e["orden_implementacion"]
    )

    # Mapa de ID funcional (EP-NN) a key Jira real (FACT-12)
    mapa_ids = {}
    resultados = []

    conector = ConectorJira(config.jira, motor_trazabilidad)
    constructor = ConstructorPayloadJira(config.jira)

    for epica_yaml in epicas:
        # Resolver dependencias al key Jira real
        epicas_previas_keys = [
            mapa_ids.get(ep_id, ep_id)
            for ep_id in (
                epica_yaml.get("dependencias", {})
                .get("epicas_previas", [])
            )
        ]

        # Crear la épica en Jira
        payload = constructor.construir_epica_desde_pipeline_es(
            epica_yaml, config.jira
        )
        respuesta = conector.cliente.post("issue", payload)
        jira_key = respuesta["key"]

        # Actualizar el mapa
        mapa_ids[epica_yaml["id"]] = jira_key

        # Registrar en el grafo con las dependencias resueltas
        conector.registrar_epica_en_grafo(
            epica_yaml, jira_key, motor_trazabilidad
        )

        # Crear links de dependencia en Jira
        for prev_key in epicas_previas_keys:
            if prev_key in mapa_ids.values():
                conector.cliente.post("issueLink", {
                    "type": {"name": "Blocks"},
                    "inwardIssue": {"key": prev_key},
                    "outwardIssue": {"key": jira_key}
                })

        # Actualizar el YAML con el key Jira asignado
        epica_yaml["trazabilidad"]["jira_epic_key"] = jira_key

        resultados.append({
            "id_funcional": epica_yaml["id"],
            "nombre": epica_yaml["nombre_oficial"],
            "jira_key": jira_key,
            "orden": epica_yaml["orden_implementacion"]
        })

    return {
        "exito": True,
        "epicas_creadas": len(resultados),
        "mapa_ids": mapa_ids,
        "detalle": resultados
    }
```

---

## Integración con el orquestador principal

El pipeline de épicas se integra en el `orchestrator.py` del modelo operativo como un subcomando independiente. La entrada es la ruta al YAML de captura del taller; la salida es la jerarquía de épicas en Jira lista para recibir requisitos.

```bash
# Procesar las épicas de un taller
python orchestrator.py --taller talleres/captura-taller-EP-04.yaml

# Con dry-run para previsualizar sin crear en Jira
python orchestrator.py --taller talleres/captura-taller-EP-04.yaml --dry-run

# Forzar una fase específica para depuración
python orchestrator.py \
  --taller talleres/captura-taller-EP-04.yaml \
  --desde fase3_validacion
```

El log de una ejecución completa tiene este aspecto:

```
════════════════════════════════════════════════════════
  PIPELINE ÉPICAS → talleres/captura-taller-EP-04.yaml
  Modo: PRODUCCIÓN
  2025-05-12 10:45:00
════════════════════════════════════════════════════════

  [ 1] Carga de la captura del taller
       ✓ 6 eventos · 3 épicas candidatas · 3 preguntas sin resolver

  [ 2] Análisis de cohesión de agrupaciones
       ✓ EP-03 (Recepción): AJUSTADA — falta evento de registro
       ✓ EP-04 (Revisión):  APROBADA — cohesión 9/10
       ✓ EP-05 (Pago):      APROBADA — cohesión 8/10

  [ 3] Generación de jerarquía de épicas
       ✓ 3 épicas · orden: EP-03 → EP-04 → EP-05
       ⚠ 2 dependencias críticas identificadas

  [ 4] Validación con glosario y repositorio
       ✓ Terminología: LIMPIO
       ✓ Solapamientos: LIMPIO
       ✓ Completitud causal: LIMPIO
       ✓ Coherencia de prioridad: LIMPIO

  [ 5] Generación de YAMLs de épica
       ✓ EP-03-recepcion-facturas.yaml generado
       ✓ EP-04-revision-aprobacion-facturas.yaml generado
       ✓ EP-05-ejecucion-pagos.yaml generado

  [ 6] Solicitud de aprobación

  ╔═══════════════════════════════════════════════════╗
  ║  REVISIÓN DE JERARQUÍA DE ÉPICAS                  ║
  ║                                                   ║
  ║  EP-03 Recepción y registro de facturas           ║
  ║        Orden: 1 · Must Have · 2-3 sprints         ║
  ║                                                   ║
  ║  EP-04 Revisión y aprobación de facturas          ║
  ║        Orden: 2 · Must Have · 3-4 sprints         ║
  ║        Depende de: EP-03                          ║
  ║                                                   ║
  ║  EP-05 Ejecución de pagos a proveedores           ║
  ║        Orden: 3 · Must Have · 2-4 sprints         ║
  ║        Depende de: EP-04                          ║
  ║                                                   ║
  ║  ⚠ 1 pregunta abierta bloquea inicio de EP-04     ║
  ║    → ¿Puede un gestor aprobar su propia factura?  ║
  ║                                                   ║
  ║  [A] Aprobar y crear épicas en Jira               ║
  ║  [E] Editar antes de aprobar                      ║
  ║  [R] Rechazar                                     ║
  ╚═══════════════════════════════════════════════════╝
  Decisión: A

  [ 7] Push a Jira
       ✓ EP-03 → FACT-10 creada
       ✓ EP-04 → FACT-11 creada (depende de FACT-10)
       ✓ EP-05 → FACT-12 creada (depende de FACT-11)

  [ 8] Registro en grafo de trazabilidad
       ✓ 3 nodos · 2 aristas de dependencia

────────────────────────────────────────────────────
  ✓ COMPLETADO en 38.7s
    Épicas creadas: FACT-10, FACT-11, FACT-12
    YAMLs en repositorio: requisitos/EP-03/, EP-04/, EP-05/
────────────────────────────────────────────────────
```

---

## Conexión con el pipeline principal de requisitos

Una vez creadas las épicas, el flujo continúa directamente hacia el pipeline estándar de requisitos. Los YAMLs de épica generados contienen todos los campos que necesita el `contexto_rag` del Paso 3 del orquestador principal para enriquecer la generación de historias con el contexto funcional completo de la épica.

La conexión es directa: el campo `id` del YAML de épica es el mismo valor que se usa en el campo `epica` de cada requisito. El pipeline de requisitos lo resuelve automáticamente al key Jira real usando el campo `trazabilidad.jira_epic_key` del YAML.

```yaml
# En el YAML de cualquier requisito de EP-04:
epica: EP-04

# El pipeline resuelve EP-04 → FACT-11 (el key Jira real)
# usando requisitos/EP-04/EP-04-revision-aprobacion-facturas.yaml
# campo: trazabilidad.jira_epic_key
```

La trazabilidad completa queda registrada en el grafo desde el primer artefacto:

```
Taller de Event Storming
        │
        ▼ (captura YAML)
    EP-04 (YAML)
        │ pertenece_a
        ▼
    FACT-11 (Epic en Jira)
        │ pertenece_a ←────────────────────┐
        ▼                                  │
    REQ-023 (YAML) ──genera──▶ FACT-47 (Story)
        │                          │
        │                   descompone
        │                          │
        │                          ▼
        │                   FACT-48..51 (Tasks)
        │
        └──deriva_de──▶ AC-023-01..03
                              │
                           verifica
                              │
                              ▼
                         TC-111..119 (Test Cases)
```

---

## Checklist de calidad para el analista

Antes de aprobar la jerarquía generada, el analista recorre este checklist en menos de cinco minutos:

**Sobre los nombres:**
- El nombre oficial de cada épica describe una capacidad de negocio completa, no un módulo técnico
- El nombre corto tiene cuatro palabras como máximo
- No hay dos épicas con nombres que suenen a lo mismo

**Sobre el alcance:**
- Cada campo `alcance_excluye` menciona explícitamente las épicas que cubren lo excluido
- Ninguna funcionalidad aparece en el `alcance_incluye` de dos épicas distintas
- El analista puede explicar el alcance de cada épica en una frase sin mencionar las demás

**Sobre las dependencias:**
- El grafo de dependencias no tiene ciclos
- Todas las épicas de prioridad `must-have` dependen únicamente de otras `must-have`
- El orden de implementación es coherente con las dependencias causales del mapa del taller

**Sobre las preguntas abiertas:**
- Cada pregunta abierta tiene responsable y fecha de respuesta
- Las preguntas marcadas como `bloquea_inicio: true` tienen fecha de respuesta anterior a la fecha de inicio del sprint donde entraría la épica

**Sobre los KPIs:**
- Cada KPI puede medirse con las herramientas disponibles del equipo
- No hay KPIs que digan "mejorar" o "reducir" sin especificar cuánto

---

## Errores frecuentes en este pipeline y cómo evitarlos

**Confundir un módulo técnico con una épica de negocio.** "Backend de facturación" no es una épica; "Revisión y aprobación de facturas" sí lo es. La prueba es simple: si el nombre de la épica no puede completar la frase "El negocio puede ahora...", no es una épica de negocio.

**Crear épicas demasiado granulares desde el taller.** Un Event Storming de tres horas sobre un dominio complejo puede producir 30 eventos. Convertir cada evento en una épica es un error. Las épicas agrupan eventos con el mismo objetivo de negocio; los eventos individuales se convierten en requisitos dentro de la épica.

**Ignorar las preguntas abiertas rojas del taller al definir el alcance.** Si una pregunta sin resolver puede cambiar el alcance de una épica, esa incertidumbre debe reflejarse en el campo `preguntas_abiertas_asociadas` con `bloquea_inicio: true`. No definir el alcance como si la respuesta ya se conociera.

**Forzar límites de épica donde no los hay.** Si dos agrupaciones del taller comparten todos sus actores, tienen reglas de negocio completamente interrelacionadas y no pueden entregarse de forma independiente, es probable que sean una sola épica. El pipeline propone ajustes, pero la decisión final es del analista con el product owner.

**No actualizar el glosario antes de ejecutar este pipeline.** Los eventos del taller traen vocabulario nuevo: nuevos actores, nuevas entidades, nuevos verbos. Si ese vocabulario no está en el glosario antes de que el pipeline lo procese, el validador no puede detectar inconsistencias y el output usa terminología que no es oficial.
