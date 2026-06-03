# Prompt para Requisitos No Funcionales (NFR) — Pipeline AI-Ready

> **Módulo complementario del Modelo Operativo de Análisis Funcional AI-Ready**
> Versión 1.0 · Complementa los puntos 4, 5 y 6 del modelo core

---

## Por qué los NFR necesitan su propio pipeline

Los prompts del modelo core (puntos 4, 5 y 6) están optimizados para requisitos funcionales: describen **qué hace el sistema** en respuesta a una acción de un actor. Un requisito funcional tiene un flujo observable, un actor que lo desencadena y un resultado verificable en la interfaz.

Un NFR describe **cómo debe comportarse el sistema** de forma transversal: no responde a una acción puntual, sino que establece una restricción que aplica a toda la arquitectura, a un conjunto de funcionalidades o a la plataforma completa. Esta diferencia estructural hace que los prompts del pipeline funcional generen artefactos incorrectos cuando se aplican directamente a un NFR:

- Generan historias de usuario con formato "Como actor, quiero..." cuando el NFR no tiene un actor funcional específico.
- Generan tareas técnicas de implementación cuando el NFR requiere primero un spike de investigación o un benchmark de validación.
- Generan test cases de flujo cuando el NFR requiere pruebas de carga, escaneos de seguridad o auditorías de accesibilidad.
- Omiten la referencia normativa o contractual que da origen a muchos NFR (SLA, WCAG, ISO 27001, RGPD).

El pipeline NFR no reemplaza al funcional: lo complementa con una rama especializada que reconoce el tipo de NFR, adapta el formato de captura, y genera los artefactos correctos para cada categoría.

---

## Taxonomía de NFR

Antes del pipeline, hay que clasificar el NFR. La clasificación determina qué prompts se usan, qué artefactos se generan y qué herramientas de validación se invocan.

```
NFR
│
├── RENDIMIENTO
│   ├── Tiempo de respuesta (latencia)
│   ├── Throughput (volumen de operaciones/segundo)
│   ├── Capacidad (volumen máximo de datos o usuarios)
│   └── Escalabilidad (comportamiento bajo crecimiento)
│
├── DISPONIBILIDAD Y RESILIENCIA
│   ├── Uptime y SLA
│   ├── Tolerancia a fallos y degradación controlada
│   ├── Tiempo de recuperación (RTO/RPO)
│   └── Redundancia y failover
│
├── SEGURIDAD
│   ├── Autenticación y autorización
│   ├── Cifrado en tránsito y en reposo
│   ├── Protección frente a vulnerabilidades (OWASP)
│   └── Auditoría y trazabilidad de accesos
│
├── ACCESIBILIDAD
│   ├── Conformidad WCAG (nivel A, AA, AAA)
│   ├── Compatibilidad con tecnologías asistivas
│   └── Internacionalización y localización
│
├── MANTENIBILIDAD Y OPERABILIDAD
│   ├── Observabilidad (logs, métricas, trazas)
│   ├── Desplegabilidad (CI/CD, rollback)
│   └── Configurabilidad sin redespliegue
│
└── CUMPLIMIENTO NORMATIVO
    ├── Protección de datos (RGPD, LOPD)
    ├── Sectorial (PSD2, SOX, ISO 27001, etc.)
    └── Accesibilidad regulada (EN 301 549, Section 508)
```

Esta clasificación se captura en el YAML de NFR como campo `categoria` y subcategoría `tipo`. El pipeline la usa para elegir el conjunto de prompts correcto.

---

## Plantilla YAML de NFR

La plantilla de NFR es análoga a la del requisito funcional (punto 1 del modelo), con tres diferencias estructurales clave:

1. **No tiene actor funcional**: tiene `alcance` (qué partes del sistema afecta) y `partes_afectadas` (equipos o sistemas que deben cumplirlo).
2. **El comportamiento esperado se expresa en métricas verificables**, no en flujos Dado/Cuando/Entonces. Los criterios de aceptación de un NFR son umbrales medibles.
3. **Genera artefactos distintos**: spikes de investigación, tareas de benchmark, pruebas de carga o escaneos automatizados, en lugar de historias de usuario con flujos de interacción.

```yaml
# ─────────────────────────────────────────────────────────────────
# BLOQUE 1 — IDENTIDAD
# Mismo esquema que el requisito funcional para coherencia del repositorio
# ─────────────────────────────────────────────────────────────────
id: NFR-001
# Formato: NFR-NNN. Espacio de IDs separado de REQ-NNN.
# La IA usa el prefijo para identificar que debe aplicar el pipeline NFR.

titulo: "Tiempo de respuesta del módulo de búsqueda de facturas bajo carga"
# Máximo 80 caracteres. Debe incluir: QUÉ calidad + DE QUÉ parte del sistema.
# Incorrecto: "El sistema debe ser rápido"
# Correcto:   "Tiempo de respuesta p95 < 500ms en búsqueda de facturas con 100 usuarios concurrentes"

version: "1.0"
estado: validado
# Mismo vocabulario que los requisitos funcionales:
# borrador | en-revision | validado | rechazado | deprecado

epica: EP-04
# NFR vinculado a una épica existente cuando es específico de un módulo.
# Para NFR transversales usar: epica: PLATAFORMA

modulo: "Gestión de Facturación"
categoria: rendimiento
# Valores del enum de categorías (ver taxonomía):
# rendimiento | disponibilidad | seguridad | accesibilidad |
# mantenibilidad | cumplimiento_normativo

tipo: tiempo_de_respuesta
# Subtipo dentro de la categoría. Determina el conjunto de prompts a aplicar.

origen:
  solicitante: "Ana López"
  area: "Dirección Financiera"
  fecha_solicitud: "2025-04-10"
  referencia: "SLA contractual cliente ACME — Cláusula 8.3"
  # La referencia es especialmente importante en NFR:
  # indica si el requisito es contractual, regulatorio o de negocio interno.

fecha_creacion: "2025-04-12"
fecha_validacion: "2025-04-18"
analista: "Carlos Ruiz"

# ─────────────────────────────────────────────────────────────────
# BLOQUE 2 — CONTEXTO Y ALCANCE
# En NFR no hay actor funcional, sino alcance del sistema y contexto de negocio
# ─────────────────────────────────────────────────────────────────
alcance:
  modulos_afectados:
    - "EP-04 Gestión de Facturación"
    # Lista todas las épicas o módulos que deben cumplir este NFR.
    # Para NFR transversales: ["TODOS"]
  endpoints_afectados:
    - "GET /api/v1/facturas"
    - "GET /api/v1/facturas/{id}"
    # Para NFR de rendimiento o seguridad: especificar endpoints concretos.
    # Si aplica a toda la API: ["TODOS LOS ENDPOINTS"]
  capas_afectadas:
    - backend
    - base_datos
    # backend | frontend | base_datos | integracion | infraestructura
  exento:
    - "Módulo de administración interna (acceso restringido a 5 usuarios)"
    # Partes del sistema explícitamente fuera del alcance de este NFR.
    # Si no se documenta, el equipo técnico asume que aplica a todo.

partes_afectadas:
  equipos:
    - "Equipo backend — implementación y benchmarking"
    - "Equipo de infraestructura — configuración de caché y base de datos"
    - "QA — diseño y ejecución de pruebas de carga"
  sistemas_dependientes:
    - "PostgreSQL — base de datos principal"
    - "Redis — caché de sesiones"

objetivo_negocio: >
  El gestor de facturación realiza entre 50 y 200 búsquedas diarias durante
  el cierre contable mensual. Un tiempo de respuesta superior a 2 segundos
  interrumpe el flujo de trabajo y aumenta el tiempo del cierre en un 40%.
  El cliente ACME tiene contractualizado un SLA de p95 < 500ms bajo carga normal.
  El incumplimiento genera penalizaciones de 5.000€/mes.
# El objetivo de negocio de un NFR debe incluir:
# - Por qué existe esta restricción (contexto de negocio)
# - Qué pasa si no se cumple (consecuencia medible)
# - Si es contractual o regulatorio, la referencia exacta

prioridad: must-have
# must-have | should-have | could-have | wont-have
# Un NFR con referencia contractual o regulatoria es siempre must-have.

dependencias:
  requisitos_funcionales:
    - REQ-021
    - REQ-022
    - REQ-023
    # Los requisitos funcionales que implementan la funcionalidad
    # sobre la que aplica este NFR. La IA los usa para generar
    # tareas técnicas asociadas a las historias correctas.
  nfr_previos:
    - NFR-005
    # NFR que deben cumplirse antes (ej: un NFR de caché antes de uno de latencia).
  decisiones_pendientes:
    - "Definir si se usa Redis o caché en memoria (decisión de arquitectura)"
    # Decisiones abiertas que bloquean la implementación.

# ─────────────────────────────────────────────────────────────────
# BLOQUE 3 — MÉTRICAS Y UMBRALES
# El núcleo del NFR: lo que hace que sea verificable
# ─────────────────────────────────────────────────────────────────
metricas:
  # Cada métrica tiene un umbral, una condición de carga y un método de medición.
  # Sin estos tres elementos, el NFR no es verificable.

  - id: M-NFR001-01
    nombre: "Tiempo de respuesta p95"
    descripcion: >
      El percentil 95 del tiempo de respuesta del endpoint
      GET /api/v1/facturas debe estar por debajo del umbral
      bajo las condiciones de carga definidas.
    umbral_aceptacion: 500
    umbral_advertencia: 350
    # umbral_advertencia: valor que dispara una alerta interna aunque no incumpla el SLA.
    unidad: ms
    condicion_de_carga:
      usuarios_concurrentes: 100
      duracion_prueba_minutos: 10
      patron_carga: "rampa"
      # rampa | constante | pico | soak
      # rampa: incremento gradual hasta el pico
      # constante: carga fija durante toda la prueba
      # pico: spike repentino al máximo
      # soak: carga moderada durante períodos largos (horas)
      ramp_up_segundos: 60
    dataset_prueba:
      volumen_registros: 100000
      descripcion: "Dataset representativo del entorno de producción con 100.000 facturas"
    metodo_medicion: "p95 calculado por JMeter/k6 sobre el tiempo de respuesta del servidor"
    herramienta_sugerida: "k6 con InfluxDB + Grafana"

  - id: M-NFR001-02
    nombre: "Tiempo de respuesta p99"
    descripcion: "El percentil 99 no debe superar el doble del umbral del p95."
    umbral_aceptacion: 1000
    umbral_advertencia: 750
    unidad: ms
    condicion_de_carga:
      usuarios_concurrentes: 100
      duracion_prueba_minutos: 10
      patron_carga: "rampa"
    metodo_medicion: "p99 calculado por k6"

  - id: M-NFR001-03
    nombre: "Tasa de error bajo carga"
    descripcion: "La tasa de errores HTTP 5xx no debe superar el 0.1% bajo carga."
    umbral_aceptacion: 0.1
    unidad: "%"
    condicion_de_carga:
      usuarios_concurrentes: 100
      duracion_prueba_minutos: 10
    metodo_medicion: "Porcentaje de respuestas con status >= 500 sobre el total"

  - id: M-NFR001-04
    nombre: "Throughput mínimo"
    descripcion: "El sistema debe soportar al menos 50 requests por segundo."
    umbral_aceptacion: 50
    unidad: "req/s"
    condicion_de_carga:
      usuarios_concurrentes: 100
      duracion_prueba_minutos: 10
    metodo_medicion: "Requests/segundo medidos por k6"

criterios_aceptacion:
  # En NFR los criterios de aceptación son verificaciones de las métricas.
  # No usan formato Dado/Cuando/Entonces porque no describen flujos de interacción.
  # Usan formato: Condición + Métrica + Resultado esperado.

  - id: AC-NFR001-01
    titulo: "p95 < 500ms bajo carga de 100 usuarios durante 10 minutos"
    condicion: >
      Con 100 usuarios concurrentes ejecutando GET /api/v1/facturas
      sobre un dataset de 100.000 facturas durante 10 minutos continuos
    metrica: "Percentil 95 del tiempo de respuesta del servidor"
    resultado_esperado: "p95 <= 500ms"
    metodo_verificacion: "Informe de k6 o JMeter. El pipeline de CI falla si p95 > 500ms."
    automatizable: true
    herramienta: "k6"

  - id: AC-NFR001-02
    titulo: "p99 < 1000ms bajo la misma carga"
    condicion: "Misma condición que AC-NFR001-01"
    metrica: "Percentil 99 del tiempo de respuesta"
    resultado_esperado: "p99 <= 1000ms"
    metodo_verificacion: "Informe de k6"
    automatizable: true
    herramienta: "k6"

  - id: AC-NFR001-03
    titulo: "Tasa de error HTTP 5xx < 0.1%"
    condicion: "Misma condición que AC-NFR001-01"
    metrica: "Porcentaje de respuestas con status >= 500"
    resultado_esperado: "<= 0.1%"
    metodo_verificacion: "Informe de k6. Incluir desglose por tipo de error."
    automatizable: true
    herramienta: "k6"

  - id: AC-NFR001-04
    titulo: "Throughput >= 50 req/s sostenido"
    condicion: "Misma condición que AC-NFR001-01"
    metrica: "Requests por segundo sostenidos durante al menos 8 de los 10 minutos"
    resultado_esperado: ">= 50 req/s"
    metodo_verificacion: "Informe de k6 con serie temporal de throughput"
    automatizable: true
    herramienta: "k6"

# ─────────────────────────────────────────────────────────────────
# BLOQUE 4 — RESTRICCIONES NO FUNCIONALES ADICIONALES
# Condiciones que acotan cómo se puede cumplir el NFR
# ─────────────────────────────────────────────────────────────────
restricciones_implementacion:
  presupuesto_infraestructura: >
    La solución no puede requerir más de 2 instancias adicionales del servidor
    de aplicación. El coste de infraestructura incremental debe ser < 500€/mes.
  tecnologias_permitidas:
    - "PostgreSQL — índices, particionado, query optimization"
    - "Redis — caché de resultados de búsqueda (TTL configurable)"
    - "Paginación del lado del servidor (ya implementada)"
  tecnologias_prohibidas:
    - "Elasticsearch — fuera del stack aprobado para este proyecto"
    - "Colas de mensajes — el requisito es de lectura síncrona"
  entorno_de_validacion: >
    La prueba de carga debe ejecutarse en el entorno de staging con
    infraestructura idéntica a producción. No se acepta validación en entornos
    de menor capacidad.

# ─────────────────────────────────────────────────────────────────
# BLOQUE 5 — REFERENCIA NORMATIVA O CONTRACTUAL
# Solo para NFR de cumplimiento o con SLA contractual
# ─────────────────────────────────────────────────────────────────
referencia_normativa:
  tipo: contractual
  # contractual | regulatorio | estandar | buenas_practicas
  documento: "Contrato de servicio cliente ACME — Rev. 3"
  clausula: "8.3.1 — Disponibilidad y rendimiento del portal de facturación"
  fecha_vigencia: "2025-01-01"
  consecuencia_incumplimiento: >
    Penalización de 5.000€/mes por cada mes en que el p95 medido en producción
    supere los 500ms durante más de 24 horas acumuladas.
  evidencia_requerida: >
    Informe mensual de métricas de rendimiento firmado por el responsable técnico.
    Los informes deben conservarse durante 36 meses.

# ─────────────────────────────────────────────────────────────────
# BLOQUE 6 — TRAZABILIDAD
# Auto-rellenado por el pipeline. No editar a mano.
# ─────────────────────────────────────────────────────────────────
trazabilidad:
  spikes_generados: []
  tareas_tecnicas_generadas: []
  pruebas_de_carga_generadas: []
  jira_issues: []
  historias_funcionales_afectadas:
    - US-045
    - US-046
    - US-047
```

---

## Arquitectura del pipeline NFR

El pipeline NFR se bifurca según la categoría del NFR. Cada rama produce artefactos distintos porque las acciones que se derivan de un NFR de rendimiento son completamente diferentes a las de uno de seguridad o accesibilidad.

```
YAML de NFR validado
       │
       ▼
[Clasificador] → ¿Qué categoría es?
       │
       ├── rendimiento ────────────────────────────────────────────────────────────────────┐
       │   [Llamada 1] Spike de benchmark (investigación previa si se necesita)            │
       │   [Llamada 2] Tareas técnicas de optimización (indexación, caché, query tuning)   │
       │   [Llamada 3] Scripts de prueba de carga (k6/JMeter)                              │
       │   [Llamada 4] Criterios de aceptación de benchmark para CI/CD                     │
       │                                                                                   │
       ├── disponibilidad ─────────────────────────────────────────────────────────────────┤
       │   [Llamada 1] Spike de arquitectura de resiliencia                                │
       │   [Llamada 2] Tareas técnicas (circuit breaker, health checks, failover)          │
       │   [Llamada 3] Runbook de respuesta a incidentes                                   │
       │   [Llamada 4] Scripts de prueba de chaos engineering                              │
       │                                                                                   │
       ├── seguridad ──────────────────────────────────────────────────────────────────────┤
       │   [Llamada 1] Spike de análisis de superficie de ataque                           │
       │   [Llamada 2] Tareas técnicas de hardening                                        │
       │   [Llamada 3] Checklist de revisión de seguridad por capa                         │
       │   [Llamada 4] Criterios de aceptación para escaneo automático (DAST/SAST)         │
       │                                                                                   │
       ├── accesibilidad ──────────────────────────────────────────────────────────────────┤
       │   [Llamada 1] Checklist WCAG por componente afectado                              │
       │   [Llamada 2] Tareas técnicas de corrección por criterio de fallo                 │
       │   [Llamada 3] Plan de pruebas manuales con tecnologías asistivas                  │
       │   [Llamada 4] Criterios de aceptación para auditoría automática (axe, Lighthouse) │
       │                                                                                   │
       └── cumplimiento_normativo ─────────────────────────────────────────────────────────┘
           [Llamada 1] Análisis de brechas (gap analysis) respecto a la norma
           [Llamada 2] Tareas técnicas de remediación
           [Llamada 3] Evidencias requeridas para auditoría
           [Llamada 4] Criterios de aceptación verificables por auditor externo

                                    │
                                    ▼
                        JSON estructurado → Jira API
                        (Spikes + Tareas técnicas)
```

---

## Prompt 0 — System prompt base para NFR

Este system prompt reemplaza al del pipeline funcional cuando se procesa un NFR. Define el rol, las restricciones y el vocabulario específico para la generación de artefactos no funcionales.

```
Eres un arquitecto de software senior y especialista en ingeniería de calidad (QA/SRE).
Tu función es transformar requisitos no funcionales (NFR) estructurados en artefactos
Jira accionables: spikes de investigación, tareas técnicas de implementación, scripts
de prueba y criterios de aceptación verificables.

DIFERENCIAS CRÍTICAS RESPECTO A REQUISITOS FUNCIONALES:
1. Los NFR NO generan historias de usuario en formato "Como [rol], quiero [acción]".
   Generan Spikes Técnicos (para investigación) y Tareas Técnicas (para implementación).
2. Los criterios de aceptación NO son flujos Dado/Cuando/Entonces.
   Son umbrales medibles con método de verificación explícito y herramienta indicada.
3. Las pruebas NO son flujos de interfaz de usuario.
   Son scripts de carga (k6, JMeter), escaneos automatizados (OWASP ZAP, axe) o
   auditorías (Lighthouse, Deque axe-core).
4. El contexto de un NFR es TRANSVERSAL: puede afectar a múltiples módulos
   y múltiples equipos. Siempre indica qué equipos deben coordinarse.

REGLAS ESTRICTAS:
1. Nunca generes una historia de usuario para un NFR. Si detectas que el input
   parece funcional además de no funcional, indica la discrepancia en alertas_calidad.
2. Los umbrales de las métricas son CONTRATOS, no sugerencias. Nunca los suavices.
   Si el YAML dice p95 < 500ms, el criterio de aceptación dice p95 < 500ms exactamente.
3. Cada tarea técnica debe indicar explícitamente el equipo responsable.
   Los NFR afectan a múltiples equipos y la responsabilidad debe ser explícita.
4. Si el NFR tiene referencia_normativa de tipo contractual o regulatorio, incluye
   siempre la evidencia requerida en la definición de terminado (DoD) de cada tarea.
5. Genera siempre el spike de investigación antes que las tareas de implementación
   cuando existe incertidumbre técnica sobre cómo cumplir el NFR.
6. El output es siempre JSON válido. Sin texto fuera del JSON.

GLOSARIO OFICIAL DEL PROYECTO:
{{glosario_yaml}}

STACK TECNOLÓGICO:
{{stack_tecnologico}}

CONTEXTO DEL PROYECTO:
- Proyecto: {{nombre_proyecto}}
- Prefijo Jira: {{prefijo_jira}}
- Herramientas de testing disponibles: {{herramientas_testing}}
```

---

## Prompt 1 — Clasificación y routing del NFR

Este prompt se ejecuta primero, antes de cualquier generación. Determina la rama del pipeline que se aplicará y detecta si el input está bien formado como NFR.

```
Analiza el siguiente NFR y determina su clasificación para routing al pipeline correcto.

NFR DE ENTRADA:
{{nfr_yaml}}

ANÁLISIS REQUERIDO:

1. VERIFICACIÓN DE TIPO: ¿Es realmente un NFR o describe funcionalidad?
   Un NFR describe UNA RESTRICCIÓN DE CALIDAD del sistema.
   Un requisito funcional describe UNA ACCIÓN que el sistema debe realizar.
   Si hay ambigüedad, indica qué parte es NFR y qué parte es funcional.

2. CLASIFICACIÓN:
   Determina la categoría y tipo exactos según la taxonomía:
   - rendimiento: tiempo_de_respuesta | throughput | capacidad | escalabilidad
   - disponibilidad: uptime | tolerancia_fallos | recuperacion | redundancia
   - seguridad: autenticacion | cifrado | vulnerabilidades | auditoria
   - accesibilidad: wcag | tecnologias_asistivas | internacionalizacion
   - mantenibilidad: observabilidad | desplegabilidad | configurabilidad
   - cumplimiento_normativo: proteccion_datos | sectorial | accesibilidad_regulada

3. COMPLETITUD PARA EL PIPELINE:
   Verifica que estos campos están presentes y tienen valores válidos:
   - metricas: con al menos un umbral_aceptacion, unidad y condicion_de_carga
   - criterios_aceptacion: al menos uno por cada métrica
   - alcance: módulos_afectados no vacío
   - origen: con referencia si es contractual o regulatorio

4. DETECTAR MÉTRICAS IMPLÍCITAS:
   ¿El NFR menciona restricciones de calidad sin cuantificar?
   Ej: "el sistema debe ser rápido" → métrica implícita no cuantificada.
   Lista las métricas implícitas que faltan como BLOQUEANTES.

Genera el siguiente JSON:

{
  "clasificacion": {
    "categoria": "[rendimiento | disponibilidad | seguridad | accesibilidad | mantenibilidad | cumplimiento_normativo]",
    "tipo": "[subtipo específico]",
    "es_nfr_puro": true,
    "componente_funcional_detectado": "[descripción si mezcla NFR y funcional, null si no]"
  },
  "rama_pipeline": "[rendimiento | disponibilidad | seguridad | accesibilidad | mantenibilidad | cumplimiento]",
  "completitud": {
    "tiene_metricas_cuantificadas": true,
    "tiene_condicion_de_carga": true,
    "tiene_metodo_verificacion": true,
    "tiene_alcance_definido": true,
    "metricas_implicitas_sin_cuantificar": [
      "[descripción de métrica no cuantificada]"
    ]
  },
  "puede_entrar_al_pipeline": true,
  "bloqueantes": [
    "[Descripción del problema que impide el procesamiento]"
  ],
  "advertencias": [
    "[Problema menor que no bloquea]"
  ]
}
```

---

## Prompt 2A — Spike técnico de investigación

Se genera cuando existe incertidumbre técnica significativa sobre cómo cumplir el NFR. Un spike es un timeboxed de investigación que el equipo técnico ejecuta antes de comprometerse a tareas de implementación.

**Criterio de uso:** generar el spike cuando el NFR tiene `decisiones_pendientes` no vacío, cuando el NFR es nuevo en el stack tecnológico del equipo, o cuando las métricas objetivo son significativamente más exigentes que el estado actual del sistema.

```
A partir del NFR estructurado, genera un Spike Técnico de investigación
que el equipo debe ejecutar antes de comprometerse a la implementación.

NFR DE ENTRADA:
{{nfr_yaml}}

CONTEXTO TÉCNICO ACTUAL:
{{contexto_tecnico_actual}}
(Incluir: métricas actuales del sistema si se conocen, decisiones de arquitectura
existentes, restricciones de infraestructura)

Un Spike Técnico tiene estas características:
- Está TIMBOXED: tiene una duración máxima fija (normalmente 1-3 días)
- Produce un ENTREGABLE CONCRETO: un documento de decisión, un benchmark, un PoC
- NO produce código de producción
- Termina con una recomendación de implementación o con la conclusión de que
  se necesita más información (lo que desencadena otro spike más acotado)

Genera el siguiente JSON:

{
  "issue_type": "Story",
  "summary": "SPIKE: [descripción de lo que se investiga — máximo 60 caracteres]",
  "labels": ["spike", "nfr", "{{categoria}}"],
  "components": ["{{componentes_afectados}}"],
  "story_points": 3,
  "description": {
    "contexto": "[Por qué existe incertidumbre. Qué no se sabe actualmente.]",
    "objetivo": "[Qué debe responderse al terminar el spike. Máximo 3 preguntas concretas.]",
    "preguntas_a_responder": [
      "[Pregunta concreta 1 con resultado esperado]",
      "[Pregunta concreta 2]",
      "[Pregunta concreta 3]"
    ],
    "timebox": "[Duración máxima: 1 día | 2 días | 3 días]",
    "entregable": "[Qué documento o artefacto debe producirse al terminar]",
    "enfoque_sugerido": "[Cómo abordar la investigación: benchmark, PoC, revisión de documentación, consulta con experto]"
  },
  "definition_of_done": [
    "Las N preguntas del spike tienen respuesta documentada",
    "El documento de decisión está disponible en Confluence en [ruta]",
    "La recomendación de implementación está aprobada por el Tech Lead",
    "[DoD específico del spike]"
  ],
  "custom_fields": {
    "nfr_origen": "{{nfr_id}}",
    "tipo_issue": "spike"
  },
  "alertas_calidad": []
}
```

**Ejemplo de output para NFR-001 (rendimiento):**

```json
{
  "issue_type": "Story",
  "summary": "SPIKE: Estrategia de optimización p95 < 500ms endpoint /api/v1/facturas",
  "labels": ["spike", "nfr", "rendimiento", "facturacion"],
  "components": ["api-facturacion", "base-datos"],
  "story_points": 3,
  "description": {
    "contexto": "El endpoint GET /api/v1/facturas tiene actualmente un p95 de 1.200ms con 50 usuarios concurrentes (medición de staging del 2025-04-01). El SLA contractual exige p95 < 500ms con 100 usuarios. Se desconoce si la brecha se cierra con optimización de queries, indexación, caché o una combinación de las tres. La decisión de arquitectura sobre Redis como capa de caché está pendiente.",
    "objetivo": "Determinar la estrategia de optimización más eficiente para alcanzar p95 < 500ms con 100 usuarios concurrentes y documentar la decisión con datos de benchmark.",
    "preguntas_a_responder": [
      "¿El índice compuesto (fecha_factura, id_empresa) reduce el p95 a < 500ms por sí solo? Ejecutar EXPLAIN ANALYZE antes y después con el dataset de 100.000 registros.",
      "¿La caché Redis con TTL de 5 minutos sobre resultados de búsqueda frecuentes aporta la reducción adicional necesaria? Medir hit ratio esperado con el patrón de uso real.",
      "¿La combinación de índice + caché es suficiente o se necesita particionado de tabla o una capa de búsqueda dedicada?"
    ],
    "timebox": "2 días",
    "entregable": "Documento de decisión en Confluence con: resultados de benchmark por estrategia, recomendación final con justificación técnica y coste de implementación estimado.",
    "enfoque_sugerido": "Benchmark iterativo en staging: 1) medir baseline actual, 2) añadir índice y medir, 3) añadir caché Redis y medir, 4) comparar resultados y documentar recomendación."
  },
  "definition_of_done": [
    "Las 3 preguntas del spike tienen respuesta documentada con datos de benchmark reales",
    "El documento de decisión está en Confluence en /EP-04/NFR/NFR-001-decision",
    "La recomendación está aprobada por el Tech Lead antes de crear las tareas de implementación",
    "Los scripts de benchmark usados están en el repositorio en /tests/benchmark/nfr-001/"
  ],
  "custom_fields": {
    "nfr_origen": "NFR-001",
    "tipo_issue": "spike"
  },
  "alertas_calidad": []
}
```

---

## Prompt 2B — Tareas técnicas de NFR de rendimiento

Se ejecuta después del spike (o directamente si no hay incertidumbre técnica). Genera las tareas de implementación específicas para NFR de rendimiento.

```
A partir del NFR de rendimiento y del resultado del spike (si existe), genera
las tareas técnicas de implementación ordenadas por capa tecnológica.

NFR DE ENTRADA:
{{nfr_yaml}}

RESULTADO DEL SPIKE (si existe):
{{resultado_spike}}
(Si no hay spike, usar "Sin spike previo. Estrategia de implementación conocida.")

STACK TECNOLÓGICO:
{{stack_tecnologico}}

REGLAS DE DESCOMPOSICIÓN PARA NFR DE RENDIMIENTO:
- Genera SIEMPRE una tarea de baseline: medir el estado actual antes de optimizar.
  Sin baseline no se puede demostrar que el NFR se ha cumplido.
- Genera tareas de optimización por capa: base de datos, backend, caché, frontend
  (solo si el NFR incluye métricas de frontend).
- Genera SIEMPRE una tarea de benchmark final: validar con las métricas del NFR
  en el entorno correcto con el dataset correcto.
- Genera una tarea de integración en CI/CD: el threshold del NFR debe fallar
  el pipeline de CI si se incumple en cada despliegue.
- El campo "equipo_responsable" es OBLIGATORIO en cada tarea.

Genera el siguiente JSON:

{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "[Verbo] + [artefacto técnico] + [para NFR-NNN]",
      "capa": "[base_datos | backend | cache | frontend | ci_cd | testing]",
      "equipo_responsable": "[backend | frontend | infraestructura | qa | devops]",
      "description": {
        "objetivo": "[Qué debe conseguirse exactamente con esta tarea]",
        "criterios_tecnicos": [
          "[Criterio técnico verificable 1]",
          "[Criterio técnico verificable 2]"
        ],
        "metodo_validacion": "[Cómo saber que la tarea está completada correctamente]",
        "consideraciones": ["[Decisión técnica relevante o riesgo]"],
        "referencias": ["[Documentación, query, endpoint o componente relevante]"]
      },
      "nfr_origen": "{{nfr_id}}",
      "historias_funcionales_afectadas": ["US-XXX"],
      "estimacion_horas": 0,
      "dependencias": ["[Summary de tarea que debe completarse antes]"],
      "labels": ["nfr", "rendimiento", "{{etiqueta_modulo}}"],
      "components": ["{{componente}}"]
    }
  ]
}
```

**Ejemplo de output para NFR-001:**

```json
{
  "tareas": [
    {
      "issue_type": "Task",
      "summary": "Medir baseline de rendimiento endpoint /api/v1/facturas para NFR-001",
      "capa": "testing",
      "equipo_responsable": "qa",
      "description": {
        "objetivo": "Establecer la línea base de rendimiento actual del endpoint GET /api/v1/facturas antes de aplicar ninguna optimización. Los datos de baseline son la referencia para demostrar la mejora.",
        "criterios_tecnicos": [
          "Script k6 ejecutado con 100 usuarios concurrentes durante 10 minutos en entorno de staging",
          "Dataset de 100.000 facturas cargado en la BD de staging (script de carga en /tests/data/)",
          "Informe exportado con p50, p90, p95, p99, throughput y tasa de error",
          "Informe publicado en Confluence en /EP-04/NFR/NFR-001-baseline"
        ],
        "metodo_validacion": "Informe de k6 disponible en Confluence con las métricas requeridas. El Tech Lead valida que el dataset y las condiciones son representativas.",
        "consideraciones": [
          "El entorno de staging debe tener infraestructura idéntica a producción (NFR-001 restricción)",
          "Ejecutar la prueba en horario de baja carga de staging para no interferir con otras pruebas"
        ],
        "referencias": [
          "Script base k6: /tests/benchmark/nfr-001/baseline.js",
          "Instrucciones de carga de dataset: /tests/data/README.md"
        ]
      },
      "nfr_origen": "NFR-001",
      "historias_funcionales_afectadas": ["US-045", "US-046", "US-047"],
      "estimacion_horas": 4,
      "dependencias": [],
      "labels": ["nfr", "rendimiento", "facturacion", "baseline"],
      "components": ["qa", "api-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Crear índice compuesto (fecha_factura, id_empresa) en tabla facturas para NFR-001",
      "capa": "base_datos",
      "equipo_responsable": "backend",
      "description": {
        "objetivo": "Añadir el índice compuesto que reduce el tiempo de ejecución de las queries de búsqueda por rango de fechas de O(n) a O(log n), según la recomendación del spike NFR-001.",
        "criterios_tecnicos": [
          "Script de migración versionado con Flyway/Liquibase (V20250418__add_factura_date_index.sql)",
          "EXPLAIN ANALYZE de la query principal muestra Index Scan en lugar de Seq Scan",
          "Script de rollback incluido y probado",
          "Validación en staging: EXPLAIN ANALYZE del endpoint con y sin índice documentada"
        ],
        "metodo_validacion": "EXPLAIN ANALYZE de GET /api/v1/facturas con rango de fechas muestra Index Scan. El script de migración se ejecuta sin errores en staging.",
        "consideraciones": [
          "La creación del índice en producción puede bloquear la tabla durante segundos. Ejecutar con CREATE INDEX CONCURRENTLY",
          "Ventana de mantenimiento recomendada: fuera del horario de cierre contable mensual"
        ],
        "referencias": [
          "Tabla: facturas",
          "Query principal: SELECT * FROM facturas WHERE fecha_factura BETWEEN $1 AND $2 AND id_empresa = $3",
          "Resultado spike: /EP-04/NFR/NFR-001-decision (índice reduce p95 de 1.200ms a ~350ms en prueba aislada)"
        ]
      },
      "nfr_origen": "NFR-001",
      "historias_funcionales_afectadas": ["US-045", "US-046", "US-047"],
      "estimacion_horas": 3,
      "dependencias": ["Medir baseline de rendimiento endpoint /api/v1/facturas para NFR-001"],
      "labels": ["nfr", "rendimiento", "base-datos", "migracion"],
      "components": ["base-datos"]
    },
    {
      "issue_type": "Task",
      "summary": "Implementar caché Redis para resultados de búsqueda de facturas para NFR-001",
      "capa": "cache",
      "equipo_responsable": "backend",
      "description": {
        "objetivo": "Añadir una capa de caché Redis sobre los resultados del endpoint GET /api/v1/facturas para reducir la carga sobre la base de datos y mejorar el p95 bajo carga concurrente.",
        "criterios_tecnicos": [
          "TTL configurable via variable de entorno FACTURA_CACHE_TTL_SECONDS (default: 300)",
          "La caché se invalida automáticamente cuando se crea, modifica o elimina una factura del id_empresa afectado",
          "La clave de caché incluye todos los parámetros de filtro (fecha_inicio, fecha_fin, id_empresa, estado, page, size)",
          "La caché no almacena datos de empresas diferentes (particionado por id_empresa en la clave)",
          "Métricas de hit/miss ratio expuestas en el endpoint /actuator/metrics (Spring) o equivalente"
        ],
        "metodo_validacion": "Con 100 usuarios ejecutando la misma búsqueda: hit ratio > 80% visible en métricas. p95 medido con k6 < 300ms en el segundo minuto de carga (tras calentamiento de caché).",
        "consideraciones": [
          "La caché NO debe almacenarse en memoria del proceso (riesgo de memory pressure bajo 100 usuarios concurrentes). Usar Redis externo.",
          "Evaluar si la invalidación por empresa es suficientemente granular o si se necesita invalidación por query hash."
        ],
        "referencias": [
          "Documentación Redis Spring Cache: https://docs.spring.io/spring-data/redis/",
          "Patrón de clave de caché: factura:search:{id_empresa}:{hash_parametros}"
        ]
      },
      "nfr_origen": "NFR-001",
      "historias_funcionales_afectadas": ["US-045", "US-046", "US-047"],
      "estimacion_horas": 8,
      "dependencias": ["Crear índice compuesto (fecha_factura, id_empresa) en tabla facturas para NFR-001"],
      "labels": ["nfr", "rendimiento", "cache", "redis"],
      "components": ["api-facturacion", "infraestructura"]
    },
    {
      "issue_type": "Task",
      "summary": "Ejecutar benchmark final y validar NFR-001 en entorno de staging",
      "capa": "testing",
      "equipo_responsable": "qa",
      "description": {
        "objetivo": "Ejecutar la prueba de carga completa con todas las optimizaciones implementadas y validar que se cumplen todos los criterios de aceptación del NFR-001 (AC-NFR001-01 a AC-NFR001-04).",
        "criterios_tecnicos": [
          "Script k6 ejecutado con 100 usuarios concurrentes en rampa de 60s durante 10 minutos",
          "Dataset de 100.000 facturas idéntico al usado en el baseline",
          "Validación de AC-NFR001-01: p95 <= 500ms ✓/✗",
          "Validación de AC-NFR001-02: p99 <= 1000ms ✓/✗",
          "Validación de AC-NFR001-03: tasa de error HTTP 5xx <= 0.1% ✓/✗",
          "Validación de AC-NFR001-04: throughput >= 50 req/s ✓/✗",
          "Informe completo en Confluence en /EP-04/NFR/NFR-001-benchmark-final",
          "Comparativa baseline vs. resultado final documentada"
        ],
        "metodo_validacion": "Todos los criterios de aceptación AC-NFR001-01 a AC-NFR001-04 marcados como PASS en el informe. Informe firmado por el responsable técnico para el expediente contractual.",
        "consideraciones": [
          "Esta tarea produce la EVIDENCIA CONTRACTUAL requerida por la cláusula 8.3.1 del contrato con ACME. El informe debe conservarse 36 meses.",
          "Si algún criterio falla, abrir nueva tarea de análisis antes de repetir el benchmark."
        ],
        "referencias": [
          "Script de benchmark: /tests/benchmark/nfr-001/final-benchmark.js",
          "Plantilla de informe: /EP-04/NFR/NFR-001-informe-template"
        ]
      },
      "nfr_origen": "NFR-001",
      "historias_funcionales_afectadas": ["US-045", "US-046", "US-047"],
      "estimacion_horas": 6,
      "dependencias": [
        "Crear índice compuesto (fecha_factura, id_empresa) en tabla facturas para NFR-001",
        "Implementar caché Redis para resultados de búsqueda de facturas para NFR-001"
      ],
      "labels": ["nfr", "rendimiento", "benchmark", "evidencia-contractual"],
      "components": ["qa", "api-facturacion"]
    },
    {
      "issue_type": "Task",
      "summary": "Integrar threshold de rendimiento NFR-001 en pipeline de CI/CD",
      "capa": "ci_cd",
      "equipo_responsable": "devops",
      "description": {
        "objetivo": "Añadir una prueba de rendimiento automatizada ligera al pipeline de CI que falla el build si el p95 supera el umbral del NFR-001, evitando regresiones de rendimiento en despliegues futuros.",
        "criterios_tecnicos": [
          "Script k6 con 20 usuarios durante 2 minutos ejecutado en el pipeline (prueba ligera, no el benchmark completo)",
          "Threshold configurado: p95 < 600ms (umbral de CI, 20% más permisivo que el SLA para compensar variación de entorno)",
          "El pipeline falla si el threshold se supera",
          "Los resultados se publican como artefacto del build (HTML report de k6)",
          "La prueba se ejecuta en el entorno de staging tras cada merge a la rama principal"
        ],
        "metodo_validacion": "El pipeline de CI falla con mensaje descriptivo cuando p95 > 600ms. Los resultados del último run están accesibles en la UI de CI.",
        "consideraciones": [
          "El umbral de CI (600ms) es intencionalmente más permisivo que el SLA (500ms) para evitar falsos positivos por variaciones de infraestructura de staging.",
          "Si el pipeline falla frecuentemente cerca del umbral, revisar si hay degradación progresiva de rendimiento antes de ajustar el threshold."
        ],
        "referencias": [
          "Script CI k6: /tests/benchmark/nfr-001/ci-check.js",
          "Integración GitHub Actions: .github/workflows/performance-check.yml"
        ]
      },
      "nfr_origen": "NFR-001",
      "historias_funcionales_afectadas": ["US-045", "US-046", "US-047"],
      "estimacion_horas": 4,
      "dependencias": ["Ejecutar benchmark final y validar NFR-001 en entorno de staging"],
      "labels": ["nfr", "rendimiento", "ci-cd", "automatizacion"],
      "components": ["devops", "api-facturacion"]
    }
  ]
}
```

---

## Prompt 2C — Tareas técnicas de NFR de seguridad

Rama específica para NFR de categoría seguridad. La diferencia principal es que genera tareas de análisis de superficie de ataque, hardening por capa y criterios de aceptación para escaneos automatizados.

```
A partir del NFR de seguridad, genera las tareas técnicas organizadas
en tres grupos: análisis, remediación y verificación.

NFR DE ENTRADA:
{{nfr_yaml}}

CONTEXTO DE SEGURIDAD DEL PROYECTO:
{{contexto_seguridad}}
(Incluir: resultados del último escaneo OWASP si existe, decisiones de arquitectura
de seguridad ya implementadas, nivel de sensibilidad de los datos manejados)

GRUPOS DE TAREAS PARA NFR DE SEGURIDAD:

GRUPO A — Análisis (ejecutar primero, siempre):
  - Revisión de superficie de ataque: ¿qué endpoints/datos/flujos están en alcance?
  - Modelado de amenazas simplificado: ¿cuáles son los vectores de ataque más relevantes?
  - Identificación de controles existentes: ¿qué ya está implementado?

GRUPO B — Remediación (una tarea por control de seguridad a implementar):
  - Tareas específicas por vulnerabilidad o control
  - Cada tarea tiene un criterio técnico de verificación determinista

GRUPO C — Verificación (ejecutar al finalizar la remediación):
  - Escaneo SAST (análisis estático de código): integración en CI/CD
  - Escaneo DAST (análisis dinámico): OWASP ZAP o equivalente
  - Revisión manual de código de las partes más críticas (si aplica)
  - Prueba de penetración (si el NFR lo requiere explícitamente)

REGLAS ESPECÍFICAS DE SEGURIDAD:
- Nunca generes criterios de aceptación que digan "sin vulnerabilidades conocidas"
  sin especificar el nivel de severidad. Usa: "sin vulnerabilidades críticas ni altas
  según la clasificación CVSS 3.1".
- Incluye siempre la referencia OWASP Top 10 cuando sea aplicable.
- Para datos personales, incluye referencia al artículo del RGPD que aplica.
- Las tareas de verificación siempre incluyen un DoD que especifica qué
  evidencia debe conservarse y durante cuánto tiempo.

Usa la misma estructura JSON que el Prompt 2B, añadiendo el campo
"grupo_seguridad": "analisis | remediacion | verificacion" en cada tarea.
```

---

## Prompt 2D — Tareas técnicas de NFR de accesibilidad

```
A partir del NFR de accesibilidad, genera las tareas técnicas organizadas
por nivel de conformidad WCAG y por tipo de componente afectado.

NFR DE ENTRADA:
{{nfr_yaml}}

NIVEL WCAG OBJETIVO: {{nivel_wcag}}
(A | AA | AAA — el nivel más frecuente en proyectos empresariales es AA)

INVENTARIO DE COMPONENTES AFECTADOS:
{{componentes_ui}}
(Lista de componentes de interfaz que deben cumplir el NFR)

REGLAS ESPECÍFICAS DE ACCESIBILIDAD:
- Genera una tarea por CRITERIO DE ÉXITO WCAG que sea relevante para los
  componentes afectados. No generes una tarea genérica de "cumplir WCAG AA".
- Incluye siempre una tarea de auditoría con herramienta automática (axe-core,
  Lighthouse) Y una tarea de prueba manual con lector de pantalla (NVDA, VoiceOver).
  La automatización detecta ~40% de los problemas; la prueba manual es imprescindible.
- Para formularios: incluir criterios específicos de etiquetado (1.3.1),
  mensajes de error (3.3.1) y orden de foco (2.4.3).
- El criterio de aceptación de accesibilidad nunca es "0 errores en axe".
  Es: "0 errores de nivel critical o serious en axe-core + verificación manual
  de los criterios de éxito listados".
- Si el proyecto está en el ámbito de la Directiva de Accesibilidad de la UE
  (sector público o servicio esencial), incluir referencia a EN 301 549.

Usa la misma estructura JSON que el Prompt 2B, añadiendo:
- "criterio_wcag": "N.N.N — Nombre del criterio" en cada tarea
- "nivel_conformidad": "A | AA | AAA"
- "tipo_prueba": "automatica | manual | ambas"
```

---

## Prompt 3 — Generación de scripts de prueba de carga (k6)

Específico para NFR de rendimiento. Genera el script de k6 listo para ejecutar a partir de las métricas del NFR.

```
A partir del NFR de rendimiento, genera el script k6 completo para
la prueba de carga que valida los criterios de aceptación.

NFR DE ENTRADA:
{{nfr_yaml}}

ENDPOINTS A PROBAR:
{{endpoints_yaml}}
(Incluir: URL completa, método HTTP, headers de autenticación requeridos,
parámetros de ejemplo)

CREDENCIALES DE PRUEBA DISPONIBLES:
{{credenciales_prueba}}
(Describir el mecanismo de autenticación del entorno de pruebas)

El script debe:
1. Implementar el patrón de carga descrito en condicion_de_carga (rampa/constante/pico/soak)
2. Validar cada métrica del NFR como threshold de k6 (el script falla si no se cumplen)
3. Incluir checks de correctitud de la respuesta (status code, estructura básica del JSON)
4. Exportar métricas a InfluxDB o al formato nativo de k6 Cloud si está disponible
5. Estar documentado con comentarios que explican cada sección
6. Usar variables de entorno para URL base, credenciales y parámetros de carga
   (nunca hardcodear datos sensibles)

Genera el script como string dentro del JSON:

{
  "script_k6": {
    "nombre_archivo": "nfr-{{nfr_id}}-load-test.js",
    "contenido": "[SCRIPT K6 COMPLETO]",
    "variables_entorno_requeridas": [
      { "nombre": "BASE_URL", "descripcion": "URL base del entorno de pruebas" },
      { "nombre": "AUTH_TOKEN", "descripcion": "Token de autenticación para el usuario de pruebas" }
    ],
    "comando_ejecucion": "k6 run --env BASE_URL=https://staging.empresa.com --env AUTH_TOKEN=xxx nfr-NFR001-load-test.js",
    "comando_ci": "k6 run --out influxdb=http://influxdb:8086/k6 nfr-NFR001-load-test.js"
  }
}
```

**Ejemplo de script k6 generado para NFR-001:**

```javascript
/**
 * Prueba de carga — NFR-001
 * Objetivo: Validar p95 < 500ms en GET /api/v1/facturas con 100 usuarios concurrentes
 * Entorno: Staging con dataset de 100.000 facturas
 * Ejecutar: k6 run --env BASE_URL=https://staging.empresa.com --env AUTH_TOKEN=xxx nfr-NFR001-load-test.js
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// ── Métricas personalizadas ─────────────────────────────────────
const errorRate = new Rate('errors');
const searchTrend = new Trend('search_duration');

// ── Opciones de carga (patrón: rampa según NFR-001) ─────────────
export const options = {
  stages: [
    { duration: '60s', target: 100 },  // Ramp-up a 100 usuarios en 60s
    { duration: '8m',  target: 100 },  // Mantener 100 usuarios durante 8 minutos
    { duration: '1m',  target: 0   },  // Ramp-down
  ],

  // Thresholds: el script falla si no se cumplen (criterios de aceptación del NFR)
  thresholds: {
    // AC-NFR001-01: p95 < 500ms
    'http_req_duration{name:busqueda_facturas}': ['p(95)<500'],

    // AC-NFR001-02: p99 < 1000ms
    'http_req_duration{name:busqueda_facturas}': ['p(99)<1000'],

    // AC-NFR001-03: tasa de error < 0.1%
    'http_req_failed': ['rate<0.001'],

    // AC-NFR001-04: throughput >= 50 req/s (verificación manual en el informe)
    // k6 no soporta threshold de throughput directamente; se verifica en el informe
  },
};

// ── Setup: obtener token de autenticación ───────────────────────
export function setup() {
  const loginRes = http.post(`${__ENV.BASE_URL}/auth/token`, JSON.stringify({
    username: 'qa-load-test@empresa.com',
    password: __ENV.AUTH_TOKEN,
  }), { headers: { 'Content-Type': 'application/json' } });

  if (loginRes.status !== 200) {
    throw new Error(`Autenticación fallida: ${loginRes.status}`);
  }

  return { token: loginRes.json('access_token') };
}

// ── Escenario principal ─────────────────────────────────────────
export default function (data) {
  const params = {
    headers: {
      'Authorization': `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
    tags: { name: 'busqueda_facturas' }, // Asocia la métrica al threshold
  };

  // Simular diferentes rangos de fechas (patrón de uso real del gestor de facturación)
  const rangos = [
    { fecha_inicio: '2024-01-01', fecha_fin: '2024-03-31' },
    { fecha_inicio: '2024-04-01', fecha_fin: '2024-06-30' },
    { fecha_inicio: '2024-07-01', fecha_fin: '2024-09-30' },
    { fecha_inicio: '2024-10-01', fecha_fin: '2024-12-31' },
  ];
  const rango = rangos[Math.floor(Math.random() * rangos.length)];

  const url = `${__ENV.BASE_URL}/api/v1/facturas`
    + `?fecha_inicio=${rango.fecha_inicio}`
    + `&fecha_fin=${rango.fecha_fin}`
    + `&page=0&size=100`;

  const res = http.get(url, params);

  // ── Checks de correctitud de la respuesta ──────────────────────
  const checkResult = check(res, {
    'status 200': (r) => r.status === 200,
    'tiene campo data': (r) => r.json('data') !== undefined,
    'tiene campo total': (r) => r.json('total') !== undefined,
    'data es array': (r) => Array.isArray(r.json('data')),
  });

  errorRate.add(!checkResult);
  searchTrend.add(res.timings.duration);

  // Pausa entre requests (simula comportamiento real del usuario)
  sleep(Math.random() * 2 + 1); // Entre 1 y 3 segundos
}

// ── Teardown: publicar resumen ──────────────────────────────────
export function teardown(data) {
  console.log('Prueba completada. Revisar el informe en el dashboard de k6.');
}
```

---

## Prompt 4 — Criterios de aceptación de NFR para Jira

Transforma los criterios de aceptación del YAML del NFR al formato que el sistema Xray o Zephyr espera para test cases de tipo no funcional.

```
A partir de los criterios de aceptación del NFR, genera los test cases
en formato Jira/Xray para gestión del ciclo de pruebas no funcionales.

NFR DE ENTRADA:
{{nfr_yaml}}

DIFERENCIAS CON TEST CASES FUNCIONALES:
- El campo "pasos" describe CÓMO EJECUTAR LA PRUEBA, no flujos de UI.
- El resultado esperado es un UMBRAL MEDIBLE, no un estado observable en pantalla.
- Siempre incluir el campo "entorno_requerido" con las condiciones del entorno.
- Siempre incluir "evidencia_requerida" para el expediente de calidad.
- Los test cases NFR tienen tipo: "rendimiento | seguridad | accesibilidad | disponibilidad"

Genera el siguiente JSON por cada criterio de aceptación del NFR:

{
  "test_cases": [
    {
      "id": "TC-NFR-{{nfr_id}}-{{numero}}",
      "titulo": "[Verificación de] + [métrica] + [condición]",
      "tipo": "{{categoria_nfr}}",
      "criterio_origen": "{{ac_id}}",
      "nfr_origen": "{{nfr_id}}",
      "prioridad": "critica | alta | media",
      "entorno_requerido": {
        "entorno": "[staging | produccion | local]",
        "infraestructura": "[descripción de infraestructura necesaria]",
        "dataset": "[descripción del dataset requerido]",
        "herramientas": ["[herramienta 1]", "[herramienta 2]"]
      },
      "precondiciones": [
        "[Estado previo necesario]"
      ],
      "pasos": [
        {
          "numero": 1,
          "accion": "[Qué hacer exactamente]",
          "resultado_esperado": "[Qué debe obtenerse como resultado de este paso]"
        }
      ],
      "resultado_esperado_global": "[Umbral o condición que determina PASS]",
      "evidencia_requerida": [
        "[Qué debe documentarse como evidencia de la prueba]"
      ],
      "automatizable": true,
      "herramienta_automatizacion": "[k6 | JMeter | OWASP ZAP | axe-core | Lighthouse]",
      "frecuencia_ejecucion": "por_despliegue | semanal | mensual | por_release"
    }
  ]
}
```

---

## Prompt 5 — Validación de calidad de NFR

Análogo al validador del punto 6 del modelo core, pero adaptado a las características de los NFR. Detecta los problemas más frecuentes antes de que el NFR entre al pipeline.

```
Eres un auditor de calidad de requisitos no funcionales.
Valida el siguiente NFR antes de que entre en el pipeline de generación.

NFR A VALIDAR:
{{nfr_yaml}}

VERIFICACIONES REQUERIDAS:

BLOQUE A — Métricas cuantificadas
  ¿Cada métrica tiene umbral_aceptacion, unidad y condicion_de_carga?
  ¿Los umbrales son SMART (específicos, medibles, alcanzables, relevantes, temporales)?
  ¿Hay métricas implícitas no cuantificadas? ("rápido", "eficiente", "seguro")

BLOQUE B — Verificabilidad
  ¿Cada criterio de aceptación tiene un método de verificación concreto?
  ¿La herramienta de medición está especificada?
  ¿El entorno de prueba está definido?
  ¿Puede responderse PASS o FAIL sin ambigüedad?

BLOQUE C — Alcance
  ¿Está especificado qué módulos o componentes deben cumplir el NFR?
  ¿Están documentadas las excepciones (partes que quedan exentas)?
  ¿Hay múltiples equipos implicados y están identificados?

BLOQUE D — Trazabilidad funcional
  ¿Están referenciados los requisitos funcionales sobre los que aplica el NFR?
  Si no hay referencia, ¿el NFR es transversal a toda la plataforma?

BLOQUE E — Referencia normativa (solo si aplica)
  ¿La referencia contractual o regulatoria es específica (cláusula, artículo, fecha)?
  ¿Está documentada la evidencia requerida para auditoría?
  ¿Está documentada la consecuencia de incumplimiento?

LOS 8 ERRORES MÁS FRECUENTES EN NFR:
1. "El sistema debe ser rápido/seguro/accesible" — sin umbral cuantificado → BLOQUEANTE
2. Umbral sin condición de carga ("p95 < 500ms" sin especificar usuarios ni duración) → BLOQUEANTE
3. Criterio de aceptación sin método de verificación → BLOQUEANTE
4. NFR que mezcla múltiples categorías (rendimiento + seguridad en un solo NFR) → ADVERTENCIA
5. Alcance no definido (¿aplica a todo el sistema o a un módulo?) → BLOQUEANTE
6. Restricciones de implementación ausentes (¿puede añadirse infraestructura?) → ADVERTENCIA
7. Referencia contractual sin especificidad (sin cláusula exacta ni consecuencia) → ADVERTENCIA
8. Métricas de percentil sin especificar el percentil ("tiempo de respuesta < 500ms"
   en lugar de "p95 < 500ms") → BLOQUEANTE (100ms de percentil 50 es muy distinto de p99)

Genera el mismo formato JSON de informe de validación que el punto 6 del modelo core,
con el campo adicional:
"metricas_implicitas_sin_cuantificar": ["[descripción]"]
```

---

## Integración con el pipeline core

El pipeline NFR se integra con el resto del modelo operativo en cuatro puntos.

### 1. Detección automática en el clasificador del orquestador

El script `orchestrator.py` detecta el prefijo `NFR-` en el ID del requisito y redirige al pipeline NFR en lugar del funcional:

```python
# En orchestrator.py — paso s1_carga
def detectar_tipo_requisito(req_id: str, contenido: dict) -> str:
    """
    Determina si el requisito debe procesarse con el pipeline funcional o el NFR.
    Criterios de clasificación:
    1. ID comienza por NFR- → pipeline NFR
    2. Contiene campo 'categoria' con valor de la taxonomía NFR → pipeline NFR
    3. Contiene campo 'metricas' con umbrales → pipeline NFR
    4. En cualquier otro caso → pipeline funcional
    """
    if req_id.startswith("NFR-"):
        return "nfr"
    if contenido.get("categoria") in {
        "rendimiento", "disponibilidad", "seguridad",
        "accesibilidad", "mantenibilidad", "cumplimiento_normativo"
    }:
        return "nfr"
    if contenido.get("metricas"):
        return "nfr"
    return "funcional"
```

### 2. Arquitectura documental del repositorio

Los NFR tienen su propio espacio en el repositorio, paralelo a los requisitos funcionales:

```
repositorio-funcional/
│
├── requisitos/                   ← REQ-NNN.yaml (funcionales)
│   └── EP-04/
│       └── REQ-023.yaml
│
├── nfr/                          ← NFR-NNN.yaml (no funcionales)
│   ├── plataforma/               ← NFR transversales a todo el sistema
│   │   ├── NFR-010-disponibilidad.yaml
│   │   └── NFR-011-seguridad-autenticacion.yaml
│   └── EP-04/                    ← NFR específicos de una épica
│       └── NFR-001-rendimiento-busqueda.yaml
│
├── benchmarks/                   ← Scripts y resultados de pruebas NFR
│   └── NFR-001/
│       ├── baseline-2025-04-15.json
│       ├── final-benchmark-2025-05-08.json
│       └── ci-check.js
│
└── evidencias/                   ← Evidencias para auditoría (solo NFR regulatorios)
    └── NFR-001/
        └── informe-sla-2025-05.pdf
```

### 3. Trazabilidad entre NFR y requisitos funcionales

Los NFR se registran en el grafo de trazabilidad (punto 9 del modelo) con el tipo de relación `restringe`:

```
NFR-001 ──[restringe]──► REQ-021
NFR-001 ──[restringe]──► REQ-022
NFR-001 ──[restringe]──► REQ-023
NFR-001 ──[genera]──────► SPIKE-001 (spike técnico)
NFR-001 ──[genera]──────► TK-089 (índice BD)
NFR-001 ──[genera]──────► TK-090 (caché Redis)
NFR-001 ──[genera]──────► TK-091 (benchmark final)
NFR-001 ──[genera]──────► TK-092 (integración CI/CD)
```

Esto permite responder preguntas como: "Si modifico el requisito REQ-023 para añadir un nuevo campo en la respuesta, ¿qué NFR pueden verse afectados?"

### 4. Detección de impacto de cambios (punto 8 del modelo)

Cuando un requisito funcional cambia, el analizador de impacto incluye ahora los NFR relacionados en su análisis:

```python
# Extensión del AnalizadorImpactoRAG para NFR
async def analizar_nfr_afectados(
    self,
    requisito_id: str,
    cambios: list[CambioDetectado]
) -> list[dict]:
    """
    Cuando cambia un requisito funcional, identifica los NFR que aplican
    sobre ese requisito y evalúa si el cambio puede afectar al cumplimiento
    de las métricas del NFR.
    Ej: añadir un JOIN complejo a una query puede degradar el p95 del NFR de rendimiento.
    """
    nfr_relacionados = []
    with self.rag.repo.db.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT
                n_nfr.id,
                n_nfr.titulo,
                n_nfr.metadatos->>'categoria' AS categoria,
                n_nfr.metadatos->>'umbral_critico' AS umbral
            FROM nodos_trazabilidad n_nfr
            JOIN aristas_trazabilidad a
                ON a.origen_id = n_nfr.id
                AND a.tipo_relacion = 'restringe'
            WHERE a.destino_id = %s
              AND n_nfr.tipo = 'nfr'
              AND n_nfr.activo = TRUE
        """, (requisito_id,))
        for nfr_id, titulo, categoria, umbral in cur.fetchall():
            nfr_relacionados.append({
                "nfr_id": nfr_id,
                "titulo": titulo,
                "categoria": categoria,
                "alerta": (
                    f"⚠ Verificar que el cambio en {requisito_id} no degrada "
                    f"el cumplimiento de {nfr_id} ({categoria})"
                    if any(c.tipo_cambio == "A" for c in cambios) else None
                )
            })
    return nfr_relacionados
```

---

## Ejemplos por categoría

### NFR de seguridad — Campos clave adicionales

```yaml
id: NFR-010
titulo: "Protección OWASP Top 10 en endpoints autenticados del módulo de facturación"
categoria: seguridad
tipo: vulnerabilidades

metricas:
  - id: M-NFR010-01
    nombre: "Ausencia de vulnerabilidades críticas y altas (CVSS >= 7.0)"
    umbral_aceptacion: 0
    unidad: "vulnerabilidades CVSS >= 7.0"
    condicion_de_carga:
      tipo_prueba: "escaneo_dast"
      herramienta: "OWASP ZAP"
      alcance: "Todos los endpoints de /api/v1/ con autenticación"
    metodo_medicion: "Informe de OWASP ZAP en modo activo sobre el entorno de staging"

  - id: M-NFR010-02
    nombre: "Cabeceras de seguridad HTTP correctamente configuradas"
    umbral_aceptacion: 0
    unidad: "cabeceras faltantes o incorrectas"
    condicion_de_carga:
      tipo_prueba: "escaneo_automatico"
      herramienta: "Mozilla Observatory o securityheaders.com"
    metodo_medicion: "Puntuación A o superior en Mozilla Observatory"

criterios_aceptacion:
  - id: AC-NFR010-01
    titulo: "0 vulnerabilidades CVSS >= 7.0 en escaneo DAST"
    condicion: >
      Escaneo OWASP ZAP en modo activo sobre todos los endpoints de /api/v1/
      con usuario autenticado como gestor_facturacion
    metrica: "Número de vulnerabilidades con CVSS Score >= 7.0"
    resultado_esperado: "0 vulnerabilidades críticas ni altas"
    metodo_verificacion: "Informe HTML de OWASP ZAP. El pipeline de CI falla si CVSS >= 7.0."
    automatizable: true
    herramienta: "OWASP ZAP"
```

### NFR de disponibilidad — Campos clave adicionales

```yaml
id: NFR-015
titulo: "SLA de disponibilidad 99.5% mensual para el módulo de facturación"
categoria: disponibilidad
tipo: uptime

metricas:
  - id: M-NFR015-01
    nombre: "Disponibilidad mensual"
    umbral_aceptacion: 99.5
    unidad: "%"
    condicion_de_carga:
      ventana_medicion: "mensual"
      excluir: "ventanas de mantenimiento programado notificadas con 48h de antelación"
    metodo_medicion: >
      Porcentaje de minutos en el mes en que el health check GET /api/health
      responde HTTP 200 en < 1000ms desde el monitor externo.
    herramienta_sugerida: "Datadog o UptimeRobot"

  - id: M-NFR015-02
    nombre: "Tiempo de recuperación ante fallo (RTO)"
    umbral_aceptacion: 15
    unidad: "minutos"
    condicion_de_carga:
      tipo_prueba: "simulacion_fallo"
      escenario: "Caída completa del proceso de aplicación en una instancia"
    metodo_medicion: "Tiempo desde la detección del fallo hasta la restauración del servicio"

rto_rpo:
  rto_minutos: 15
  rpo_minutos: 5
  # RTO: Recovery Time Objective — tiempo máximo de interrupción tolerable
  # RPO: Recovery Point Objective — pérdida máxima de datos tolerable
```

### NFR de accesibilidad — Campos clave adicionales

```yaml
id: NFR-020
titulo: "Conformidad WCAG 2.1 nivel AA en el módulo de facturación"
categoria: accesibilidad
tipo: wcag

metricas:
  - id: M-NFR020-01
    nombre: "Errores críticos y serios en axe-core"
    umbral_aceptacion: 0
    unidad: "errores de nivel critical o serious"
    condicion_de_carga:
      herramienta: "axe-core 4.x integrado en Playwright"
      paginas_auditadas:
        - "/facturas (listado)"
        - "/facturas/{id} (detalle)"
    metodo_medicion: "axe-core ejecutado sobre cada página con usuario autenticado"

  - id: M-NFR020-02
    nombre: "Criterios de éxito WCAG AA superados en prueba manual"
    umbral_aceptacion: 100
    unidad: "% de criterios aplicables superados"
    condicion_de_carga:
      tipo_prueba: "prueba_manual"
      tecnologia_asistiva: "NVDA 2024 + Firefox en Windows"
      tester: "Persona con discapacidad visual o especialista certificado"
    metodo_medicion: "Lista de verificación WCAG 2.1 AA completada por el tester"

criterios_wcag_aplicables:
  # Lista explícita de criterios de éxito WCAG que aplican a este módulo
  - id: "1.1.1"
    nombre: "Contenido no textual"
    nota: "Los iconos de estado de factura deben tener texto alternativo"
  - id: "1.3.1"
    nombre: "Información y relaciones"
    nota: "La tabla de facturas debe usar elementos <th> con scope correcto"
  - id: "2.4.3"
    nombre: "Orden del foco"
    nota: "El orden de tabulación en el formulario de filtros debe ser lógico"
  - id: "3.3.1"
    nombre: "Identificación de errores"
    nota: "Los mensajes de error del filtro de fechas deben describir el error"
  - id: "4.1.2"
    nombre: "Nombre, función, valor"
    nota: "Todos los controles del filtro deben tener label accesible"
```

---

## Errores más frecuentes al capturar NFR

Esta lista complementa el catálogo del punto 10 del modelo core, específicamente para NFR:

| # | Error | Tipo | Consecuencia |
|---|-------|------|-------------|
| 1 | "El sistema debe ser rápido" sin umbral | Semántico | Imposible generar criterio de aceptación; el equipo implementa cualquier cosa |
| 2 | Umbral sin condición de carga | Estructural | El benchmark es inválido: 500ms con 1 usuario es trivial; con 1000 es imposible |
| 3 | Percentil no especificado ("tiempo < 500ms") | Semántico | p50 y p99 difieren en un orden de magnitud; el equipo optimiza el promedio e ignora los outliers |
| 4 | NFR que mezcla rendimiento y seguridad | Atomicidad | Pipeline incorrecto; artefactos mezclados que ningún equipo sabe quién debe ejecutar |
| 5 | Alcance sin excepciones documentadas | Completitud | El equipo aplica el NFR a todo el sistema cuando solo aplica a módulos de negocio |
| 6 | Sin referencia al entorno de validación | Completitud | El benchmark se hace en un entorno de baja capacidad y no es representativo |
| 7 | Referencia normativa genérica ("cumplir RGPD") | Semántico | Sin artículo específico ni evidencia requerida; la auditoría no puede verificarse |
| 8 | Sin tarea de baseline | Completitud | Sin línea base no se puede demostrar que el NFR se ha cumplido ni cuantificar la mejora |
| 9 | NFR de accesibilidad sin prueba manual | Completitud | Los escaneos automáticos detectan ~40% de los problemas; sin prueba manual el NFR no está realmente validado |
| 10 | Criterios de aceptación sin herramienta especificada | Verificabilidad | QA no sabe cómo ejecutar la prueba; se retrasa la validación hasta el sprint de QA |

---

## Glosario de términos NFR para el glosario del proyecto

Estos términos deben añadirse al `glosario.yaml` del proyecto (punto 2 del modelo) para que el pipeline los use correctamente en todos los prompts:

```yaml
# Añadir en la sección "abreviaturas" del glosario.yaml
abreviaturas:
  - sigla: "NFR"
    expansion: "Requisito No Funcional (Non-Functional Requirement)"
  - sigla: "SLA"
    expansion: "Acuerdo de Nivel de Servicio (Service Level Agreement)"
  - sigla: "RTO"
    expansion: "Objetivo de Tiempo de Recuperación (Recovery Time Objective)"
  - sigla: "RPO"
    expansion: "Objetivo de Punto de Recuperación (Recovery Point Objective)"
  - sigla: "DAST"
    expansion: "Prueba de Seguridad Dinámica (Dynamic Application Security Testing)"
  - sigla: "SAST"
    expansion: "Prueba de Seguridad Estática (Static Application Security Testing)"
  - sigla: "WCAG"
    expansion: "Pautas de Accesibilidad para el Contenido Web (Web Content Accessibility Guidelines)"
  - sigla: "CVSS"
    expansion: "Sistema de Puntuación de Vulnerabilidades Común (Common Vulnerability Scoring System)"
  - sigla: "p95"
    expansion: "Percentil 95 — el valor por debajo del cual se encuentran el 95% de las mediciones"
  - sigla: "p99"
    expansion: "Percentil 99 — el valor por debajo del cual se encuentran el 99% de las mediciones"

# Añadir en la sección "entidades" del glosario.yaml
entidades:
  - id: ENT-NFR-001
    nombre_oficial: "Requisito No Funcional"
    descripcion: >
      Restricción de calidad que aplica de forma transversal al sistema o a un módulo,
      y que no describe una acción de un actor sino una propiedad medible del sistema
      (rendimiento, disponibilidad, seguridad, accesibilidad, etc.).
      Los NFR no generan historias de usuario: generan spikes técnicos y tareas de
      implementación y validación.
    sinonimos_no_oficiales:
      - "requisito de calidad"
      - "restricción técnica"
      - "requisito transversal"
    atributos_clave:
      - nombre: "categoria"
        tipo: enum
        valores: ["rendimiento", "disponibilidad", "seguridad", "accesibilidad",
                  "mantenibilidad", "cumplimiento_normativo"]
      - nombre: "metricas"
        tipo: array
        descripcion: "Lista de métricas cuantificadas con umbral, unidad y condición de carga"
```

---

*Este módulo forma parte del Modelo Operativo de Análisis Funcional AI-Ready.*
*Versión 1.0 — Complementa los puntos 4, 5 y 6 del modelo core.*
*Siguiente módulo recomendado: Gestión de requisitos de integración con sistemas externos.*
