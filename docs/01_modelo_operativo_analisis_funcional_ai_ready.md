# Modelo Operativo: Análisis Funcional AI-Ready

---

## 1. Cómo debe cambiar la captura de requisitos

El punto de partida es reemplazar la recogida de requisitos en formato narrativo libre por una **captura estructurada y orientada a eventos**. Esto no significa que el usuario de negocio tenga que aprender a escribir JSON, sino que el analista introduce una capa de estructuración durante el propio workshop.

Los cambios prácticos son tres. Primero, se pasa de reuniones abiertas de toma de requisitos a **workshops de Event Storming facilitados**, donde el analista identifica eventos de negocio, comandos y actores con post-its digitales (Miro, FigJam). Esto produce un mapa causal del proceso, no una lista de requisitos. Segundo, el analista captura en tiempo real en una plantilla estructurada, no en un Word en blanco. Tercero, se introduce un paso de validación inmediata: antes de salir del workshop, cada requisito se lee en voz alta siguiendo el formato "Dado / Cuando / Entonces" para detectar ambigüedades en el momento.

---

## 2. Estructura del documento funcional AI-Ready

Un documento AI-ready no es un Word narrativo. Es un documento con **estructura semántica explícita** que una IA puede segmentar, indexar y transformar sin ambigüedad.

La arquitectura recomendada tiene cinco capas:

| Capa | Contenido |
|---|---|
| **Cabecera del documento** | ID · versión · proyecto · stakeholders · fecha · estado · glosario |
| **Contexto de negocio** | Objetivo · alcance · actores · restricciones · dependencias · KPIs |
| **Módulos de requisito (1…N)** | Requisito · Historia US · Criterios AC · Metadatos técnicos |
| **Apéndices** | Matriz de trazabilidad · Glosario estructurado · Diagramas de proceso |
| **Capa de exportación** | Word (lectura humana) · Markdown · YAML/JSON (IA y automatización) · Jira API |

---

## 3. Información obligatoria en cada requisito

Cada requisito debe incluir estos campos sin excepción. Los marcados con ★ son los más críticos para que la IA genere artefactos de calidad:

| Campo | Descripción | Ejemplo |
|---|---|---|
| ★ `REQ-ID` | Identificador único y estable | `REQ-023` |
| ★ `Título` | Una frase, sin verbos ambiguos | "Filtrado de facturas por rango de fechas" |
| ★ `Actor/Rol` | Quién ejecuta la acción | `Gestor de facturación` |
| ★ `Evento disparador` | Qué lo activa | "El usuario accede al módulo de facturas" |
| ★ `Resultado esperado` | Qué debe ocurrir | "El sistema muestra facturas del rango seleccionado" |
| ★ `Criterios de aceptación` | En formato Dado/Cuando/Entonces | Ver sección 12 |
| `Reglas de negocio` | Condiciones y restricciones | "Sólo facturas del ejercicio en curso" |
| `Datos de entrada` | Campos, tipos, validaciones | `fecha_inicio: Date, fecha_fin: Date` |
| `Datos de salida` | Qué devuelve el sistema | Lista paginada, máx. 100 registros |
| `Excepciones` | Qué ocurre si falla | "Mensaje de error si el rango supera 365 días" |
| `Prioridad` | MoSCoW o numérica | `Must Have` |
| `Origen` | Quién lo pidió | `Ana López, Dirección Financiera` |
| `Épica` | A qué módulo pertenece | `EP-04 Gestión de Facturación` |
| `Trazabilidad` | US y TCs derivados | `US-047, TC-112, TC-113` |

---

## 4. Plantillas y formatos recomendados

La clave es usar **dos representaciones en paralelo**: una para humanos (Word/Confluence) y otra para máquinas. No son documentos distintos, sino vistas distintas del mismo dato.

**Plantilla YAML de requisito (machine-readable):**

```yaml
requisito:
  id: REQ-023
  titulo: "Filtrado de facturas por rango de fechas"
  epica: EP-04
  actor: "Gestor de facturación"
  prioridad: must-have
  estado: validado
  origen: "Ana López - Dirección Financiera"
  descripcion: >
    El gestor de facturación necesita filtrar el listado de facturas
    por un rango de fechas para agilizar la búsqueda y exportación.
  evento_disparador: "Acceso al módulo de Facturas"
  reglas_negocio:
    - "Solo facturas del ejercicio fiscal en curso"
    - "Rango máximo permitido: 365 días"
  datos_entrada:
    - nombre: fecha_inicio
      tipo: date
      requerido: true
      formato: ISO-8601
    - nombre: fecha_fin
      tipo: date
      requerido: true
      formato: ISO-8601
  datos_salida:
    tipo: lista_paginada
    max_registros: 100
    campos: [id_factura, fecha, importe, estado, proveedor]
  criterios_aceptacion:
    - id: AC-023-01
      dado: "El gestor está en el módulo de Facturas"
      cuando: "Selecciona fecha_inicio=2024-01-01 y fecha_fin=2024-03-31"
      entonces: "El sistema muestra las facturas del período ordenadas por fecha desc"
    - id: AC-023-02
      dado: "El gestor selecciona un rango superior a 365 días"
      cuando: "Confirma la búsqueda"
      entonces: "El sistema muestra el mensaje 'El rango no puede superar 365 días'"
  excepciones:
    - "Sin resultados: mostrar estado vacío con sugerencia de ampliar el rango"
  trazabilidad:
    historias: []
    test_cases: []
    jira_issues: []
```

Este YAML se puede almacenar en Confluence, Git o un repositorio documental. La IA lo lee directamente y puede generar los artefactos Jira con una sola instrucción.

---

## 5. División funcional para facilitar la generación automática

La información debe estar **modularizada en unidades atómicas y cohesivas**. Cada unidad debe tener un único propósito funcional. Un requisito que mezcla autenticación con gestión de perfiles imposibilita la generación automática precisa.

La regla de oro es: **un requisito = un evento de negocio = una historia de usuario = N criterios de aceptación = N×2 casos de prueba**.

```
EP-04 Gestión de Facturación
│
├── REQ-021 → US-045 → AC-021-01..03 → TC-101..106
├── REQ-022 → US-046 → AC-022-01..02 → TC-107..110
├── REQ-023 → US-047 → AC-023-01..02 → TC-111..114
│            └── Tarea técnica TK-089 (filtro DB)
│            └── Tarea técnica TK-090 (paginación API)
└── REQ-024 → ...
```

Esta jerarquía es la que consume el pipeline de IA para generar los artefactos en Jira. Cada nivel tiene su propio prompt template y su propia validación.

---

## 6. Metodología recomendada: BDD + Event Storming + User Stories

No se recomienda una única metodología sino una **combinación en capas**:

**Fase de descubrimiento → Event Storming.** El Event Storming Big Picture identifica todos los eventos de negocio relevantes sin entrar en detalles técnicos. Es la técnica más eficaz para involucrar a usuarios de negocio no técnicos porque trabajan con lenguaje natural sobre un lienzo visual.

**Fase de definición → User Stories en formato estándar + BDD.** Una vez identificados los eventos, cada uno se convierte en una historia de usuario con criterios de aceptación en formato Gherkin (Dado/Cuando/Entonces). Esta combinación es la que produce el mejor input para la IA porque el formato Gherkin es estructuralmente determinista: la IA sabe exactamente qué es el contexto, qué es la acción y qué es el resultado esperado.

**Specification by Example** se incorpora cuando existen reglas de negocio complejas (cálculos, validaciones condicionales). Consiste en definir el comportamiento mediante ejemplos concretos con datos reales, lo que también alimenta directamente los casos de prueba.

Los Use Cases formales se reservan únicamente para sistemas con muchos flujos alternativos complejos (como aplicaciones legales o médicas) donde la narrativa estructurada aporta valor.

---

## 7. Combinación de Word con formatos explotables por IA

La estrategia es un modelo de **documento híbrido en Confluence** que combina ambas representaciones:

```
[Sección narrativa en prosa] ← Para el usuario de negocio
[Tabla de requisito estructurada] ← Para la IA y el equipo técnico
[Bloque YAML colapsable] ← Para automatización y APIs
[Criterios en Gherkin] ← Para BDD y generación de tests
```

En la práctica, el analista trabaja en Confluence con una plantilla preconfigurada que incluye macros que renderizan el YAML como tabla legible. El usuario de negocio ve una tabla amigable. El sistema de automatización lee el YAML raw. Word se reserva para entregas formales externas o actas firmadas.

Si el equipo está aún muy anclado en Word, se puede usar **Pandoc** para convertir automáticamente documentos Word con estilos definidos (Heading 1, Heading 2, tablas con cabeceras normalizadas) a Markdown y luego a YAML mediante un script de transformación. Esto permite una migración progresiva sin romper el flujo existente.

---

## 8. Proceso end-to-end recomendado

El flujo completo tiene seis fases, cada una con su intervención de IA correspondiente:

| Fase | Descripción | Intervención de IA |
|---|---|---|
| **1. Workshop** | Event Storming · Miro · notas estructuradas | Transcripción + resumen |
| **2. Análisis funcional** | Plantilla YAML + BDD · Confluence · Git | Validación de ambigüedad |
| **3. Validación** | Revisión con negocio · Firma digital / aprobación | Checklist de completitud |
| **4. Generación automática Jira** | Épicas · Historias · Tareas técnicas · Subtareas | Pipeline LLM → Jira API (revisión humana antes de push) |
| **5. Generación automática de pruebas** | Casos de prueba · Scripts Gherkin · Matriz trazabilidad | Generación desde criterios AC · revisión QA Lead obligatoria |
| **6. Desarrollo + feedback loop** | Sprint activo · Cambios → actualización YAML · Re-gen artefactos | Detección de impacto de cambios · sugerencia de regresión |

La regla de oro es: **la IA propone, el humano aprueba**. Ningún artefacto debe ir a Jira sin revisión humana en el MVP del proceso.

---

## 9. Papel de la IA en cada fase

| Fase | Rol de la IA | Nivel de autonomía |
|---|---|---|
| Workshop | Transcripción en tiempo real, extracción de entidades (actores, eventos, sistemas) desde grabación o notas | Semi-auto (supervisión) |
| Análisis funcional | Detección de ambigüedades, requisitos incompletos, contradicciones entre requisitos | Asistido |
| Validación | Checklist automático de completitud (¿tiene AC?, ¿tiene actor?, ¿tiene excepciones?) | Automático |
| Generación Jira | LLM transforma YAML → Epics/Stories/Tasks/Subtasks con formato estándar de la organización | Semi-auto (aprobación humana) |
| Generación QA | LLM genera test cases desde criterios AC en Gherkin; integración con Xray/Zephyr | Semi-auto |
| Impacto de cambios | RAG sobre el repositorio de requisitos para detectar qué historias se ven afectadas por un cambio | Asistido |

---

## 10. Riesgos, limitaciones y errores habituales

Los errores más frecuentes al implantar este tipo de transformación, ordenados por impacto:

**Requisitos ambiguos disfrazados de bien definidos.** Un requisito con "el sistema debe ser rápido" o "el usuario podrá gestionar sus datos" parece completo pero no lo es. La IA generará historias igualmente ambiguas. La solución es el checklist de validación automático antes de que el requisito entre en el pipeline.

**Sobreautomatizar desde el día uno.** El error más común es intentar que la IA genere artefactos Jira sin revisión humana desde el inicio. Los primeros meses deben servir para calibrar los prompts y construir confianza en el equipo. Se recomienda empezar con la IA como asistente de escritura y escalar hacia automatización progresiva.

**Glosario de negocio inconsistente.** Si el mismo concepto aparece como "cliente", "usuario", "comprador" y "cuenta" en distintos documentos, la IA generará historias con entidades diferentes para el mismo concepto. El glosario estructurado no es opcional.

**Criterios de aceptación que no son verificables.** "El sistema debe ser intuitivo" no es un criterio de aceptación, es una opinión. Cada AC debe poder responderse con verdadero/falso mediante una prueba concreta.

**Ignorar los flujos de excepción.** El 80% de los bugs viven en los flujos alternativos y de error. La IA solo genera casos de prueba para los flujos que están documentados. Si los flujos de excepción no están en el YAML, no existirán en los tests.

**Falta de versionado documental.** El YAML de requisitos debe estar en Git o en un sistema con control de versiones. Sin esto, no hay trazabilidad de cambios y la IA puede trabajar sobre información desactualizada.

---

## 11. Arquitectura documental recomendada

```
repositorio-funcional/
│
├── glosario.yaml                     # Términos únicos y canónicos
├── epicas/
│   ├── EP-01-autenticacion.yaml
│   ├── EP-02-gestion-usuarios.yaml
│   └── EP-04-facturacion.yaml
│
├── requisitos/
│   ├── EP-04/
│   │   ├── REQ-021.yaml
│   │   ├── REQ-022.yaml
│   │   └── REQ-023.yaml              # Cada requisito = un archivo
│   └── ...
│
├── historias/                        # Auto-generadas (no editar a mano)
│   └── US-047.yaml
│
├── test-cases/                       # Auto-generados + revisados
│   └── TC-111.yaml
│
├── matrices/
│   └── trazabilidad.yaml             # Auto-generada desde relaciones
│
├── templates/
│   ├── requisito.template.yaml       # Plantilla base
│   ├── historia.template.yaml
│   └── test-case.template.yaml
│
└── pipelines/
    ├── validate-requisitos.py        # Checklist de completitud
    ├── generate-jira-issues.py       # Push a Jira API
    └── generate-test-cases.py        # Generación con LLM
```

Esta arquitectura permite **reutilización máxima**: el glosario se inyecta como contexto en cada llamada a la IA, las épicas se referencian desde múltiples requisitos, y las plantillas garantizan consistencia estructural.

---

## 12. Ejemplos concretos

### Requisito mal definido

> *"El sistema debe permitir al usuario gestionar sus facturas de forma eficiente, con un buen rendimiento y opciones de filtrado adecuadas."*

**Problemas:** "gestionar" no especifica qué operaciones, "eficiente" no es medible, "adecuadas" es subjetivo, no hay actor concreto, no hay criterios de aceptación.

---

### Requisito bien definido

> *"El gestor de facturación debe poder filtrar el listado de facturas por rango de fechas (máximo 365 días). El sistema debe devolver los resultados en menos de 2 segundos para conjuntos de hasta 10.000 registros. Si el rango supera 365 días, el sistema muestra el mensaje de validación 'El rango no puede superar 365 días'."*

---

### Historia AI-ready

```yaml
historia:
  id: US-047
  titulo: "Filtrado de facturas por rango de fechas"
  tipo: funcional
  epica: EP-04
  requisito_origen: REQ-023
  como: "gestor de facturación"
  quiero: "filtrar el listado de facturas por fecha_inicio y fecha_fin"
  para: "localizar rápidamente las facturas de un período contable concreto"
  criterios_aceptacion:
    - id: AC-047-01
      dado: "El gestor está autenticado y accede al módulo Facturas"
      cuando: "Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31 y pulsa Buscar"
      entonces: |
        - El sistema devuelve las facturas del período en menos de 2 segundos
        - Los resultados aparecen ordenados por fecha descendente
        - Se muestra el número total de resultados encontrados
    - id: AC-047-02
      dado: "El gestor selecciona un rango de fechas superior a 365 días"
      cuando: "Pulsa Buscar"
      entonces: |
        - El sistema NO ejecuta la consulta
        - Muestra el mensaje: 'El rango no puede superar 365 días'
        - Los campos de fecha quedan resaltados en rojo
    - id: AC-047-03
      dado: "El gestor ejecuta una búsqueda válida sin resultados"
      cuando: "El sistema procesa la consulta"
      entonces: |
        - Se muestra un estado vacío con el texto 'No se encontraron facturas para el período seleccionado'
        - Se ofrece el botón 'Ampliar búsqueda'
  definition_of_done:
    - "Todos los criterios de aceptación superan las pruebas de regresión"
    - "Rendimiento validado con dataset de 10.000 registros"
    - "Revisión de accesibilidad WCAG 2.1 AA"
  estimacion_story_points: 5
```

---

### Criterio de aceptación útil para IA

```yaml
- id: AC-023-01
  dado: "El gestor está autenticado con rol gestor_facturacion y accede al módulo Facturas"
  cuando: "Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31 y pulsa Buscar"
  entonces: "El sistema devuelve las facturas del período en menos de 2 segundos, ordenadas por fecha descendente, mostrando el contador de resultados"
```

**Por qué funciona para la IA:** el dado describe un estado concreto del sistema, el cuando describe UNA acción específica con datos reales, y el entonces describe un resultado observable y medible (tiempo, orden, contador). No hay ambigüedad que la IA tenga que resolver.

---

### Caso de prueba generado automáticamente

```yaml
test_case:
  id: TC-111
  titulo: "Filtrado válido de facturas por rango de fechas"
  historia: US-047
  criterio_origen: AC-047-01
  tipo: funcional
  prioridad: alta
  precondiciones:
    - "Usuario autenticado con rol gestor_facturacion"
    - "Existen facturas en BD con fechas entre 2024-01-01 y 2024-03-31"
  pasos:
    - paso: 1
      accion: "Navegar al módulo Facturas"
      resultado_esperado: "Se carga la pantalla de listado de facturas"
    - paso: 2
      accion: "Introducir fecha_inicio = 2024-01-01 en el campo Desde"
      resultado_esperado: "El campo muestra la fecha seleccionada"
    - paso: 3
      accion: "Introducir fecha_fin = 2024-03-31 en el campo Hasta"
      resultado_esperado: "El campo muestra la fecha seleccionada"
    - paso: 4
      accion: "Pulsar el botón Buscar"
      resultado_esperado: |
        - Lista de facturas del período visible en menos de 2 segundos
        - Ordenadas por fecha descendente
        - Contador de resultados visible
  datos_prueba:
    fecha_inicio: "2024-01-01"
    fecha_fin: "2024-03-31"
    registros_esperados: 47
  resultado_esperado_global: "PASS si se cumplen todos los resultados esperados por paso"
  automatizable: true
  framework_sugerido: "Selenium / Playwright + Cucumber"
```

---

## 13. Herramientas del mercado

**Núcleo del stack recomendado:**

`Confluence` como repositorio documental con plantillas estructuradas y soporte nativo de YAML/Markdown. `Jira` como destino de artefactos, con automatizaciones via API REST y Atlassian Intelligence para sugerencias contextuales. `Xray o Zephyr Scale` para gestión de test cases integrada con Jira.

**Capa de IA:**

`OpenAI GPT-4o o Claude` para el pipeline de generación de artefactos. Se recomienda Claude (Anthropic) para tareas de análisis funcional por su mayor capacidad de seguir instrucciones estructuradas complejas. `LangChain o LlamaIndex` para construir el pipeline RAG que permite a la IA consultar el repositorio de requisitos existente antes de generar nuevos artefactos, evitando duplicidades y contradicciones.

**RAG (Retrieval-Augmented Generation)** es especialmente valioso aquí: en lugar de darle a la IA el documento completo cada vez, se indexan todos los requisitos en una base vectorial (Pinecone, Chroma, pgvector) y el sistema recupera automáticamente los requisitos relacionados antes de generar una nueva historia.

**Para ingeniería de requisitos específica:** `Codebeamer` o `Jama Connect` son herramientas enterprise de gestión de requisitos con trazabilidad nativa. Se recomienda para proyectos regulados (finanzas, salud, defensa). Para equipos con menos overhead, Confluence + Git es suficiente.

**Para validación de calidad de requisitos:** `Copilot for Microsoft 365` puede ayudar a analistas que trabajan en Word a detectar ambigüedades y completar campos obligatorios.

**Azure DevOps** como alternativa a Jira si el stack ya es Microsoft, con integración nativa con GitHub Copilot para la capa de desarrollo.

---

## 14. Roadmap de implantación por fases

| Fase | Duración | Objetivos | Herramientas |
|---|---|---|---|
| **Fase 0: Fundación** | 4-6 semanas | Definir plantillas YAML, glosario, estructura de repositorio. Formar a analistas en BDD y Event Storming. Piloto con 1 módulo. | Confluence, Git, plantillas |
| **Fase 1: Asistencia** | 2-3 meses | IA como asistente de escritura (sugerencias, validación de completitud). El analista decide siempre. Métricas de adopción. | Claude/GPT-4o via API, Confluence |
| **Fase 2: Semi-automatización** | 3-4 meses | Pipeline de generación de historias y tareas desde YAML. Revisión humana obligatoria. Generación de test cases básicos. | LangChain, Jira API, Xray |
| **Fase 3: RAG y trazabilidad** | 2-3 meses | Base vectorial de requisitos. Detección automática de impacto de cambios. Matriz de trazabilidad auto-generada. | Pinecone/pgvector, RAG pipeline |
| **Fase 4: Autonomía supervisada** | Ongoing | El pipeline genera y empuja a Jira con aprobación por excepción. Métricas de calidad de IA. | MLflow/LangSmith para trazabilidad de prompts |

---

## 15. Recomendaciones prácticas para la adopción

La tecnología es la parte fácil. La adopción es el reto verdadero.

**Para los analistas funcionales**, el mensaje debe ser: "la IA hace el trabajo repetitivo, tú haces el trabajo de valor". La primera resistencia viene del miedo a la sustitución. Hay que demostrar con ejemplos reales que el analista que usa la herramienta produce más y mejor, no que es reemplazado. El primer sprint de adopción debe mostrar una reducción concreta del tiempo invertido en tareas mecánicas (rellenar campos en Jira, formatear documentos) y un aumento del tiempo en workshops y validación con negocio.

**Para los usuarios de negocio**, el cambio debe ser invisible. No deben ver YAML ni Gherkin. Deben ver una plantilla de Word o Confluence ligeramente más estructurada que la que ya usaban. El analista es el traductor entre el lenguaje de negocio y el formato estructurado.

**Para la dirección**, los KPIs que justifican la inversión son: reducción del tiempo desde requisito aprobado hasta historia en Jira (de días a horas), reducción de defectos por ambigüedad funcional en producción, aumento de cobertura de test cases, y reducción del tiempo de onboarding de nuevos analistas al proyecto.

**Estrategia de roll-out**: empezar con el analista más entusiasta en el proyecto más pequeño. Documentar el antes y el después con métricas reales. Usar ese caso de éxito como evangelización interna antes de escalar. No intentar un big bang.

**La formación más eficaz** no es un curso de prompt engineering. Es una sesión práctica de 2 horas donde el analista ve cómo su propio requisito se transforma automáticamente en 3 historias, 2 tareas técnicas y 6 casos de prueba. Esa demostración vale más que cualquier presentación estratégica.

---

## Resumen ejecutivo del modelo

El modelo propuesto es incremental por diseño. No requiere reemplazar ninguna herramienta existente en la Fase 0, sólo estructurar mejor lo que ya se produce. La automatización llega en las fases siguientes, cuando el equipo ya confía en el formato y la IA tiene suficientes ejemplos propios de la organización para generar artefactos con el tono, vocabulario y estructura correctos.

| Dimensión | Situación actual | Con el modelo AI-ready |
|---|---|---|
| Tiempo de ciclo funcional | 2-5 días (req → Jira) | 2-4 horas |
| Cobertura de test cases | Parcial, manual | Completa, automática |
| Trazabilidad | Inexistente o en Excel | Automática y en tiempo real |
| Detección de ambigüedades | En refinamiento o en bugs | Antes del pipeline |
| Consistencia terminológica | Variable por analista | Garantizada por el glosario |
| Impacto de cambios | Detectado tarde (o no detectado) | Automático e inmediato |
