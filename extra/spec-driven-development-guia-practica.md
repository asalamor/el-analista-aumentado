# Spec-Driven Development: guía práctica para proyectos TI con IA

> **Versión:** Junio 2026 · **Audiencia:** Equipos de desarrollo, arquitectos, tech leads y profesionales TI que trabajan con IA generativa

---

## 1. Qué es Spec-Driven Development

**Spec-Driven Development (SDD)** es una metodología de desarrollo de software en la que una especificación estructurada, versionada y ejecutable —no el código— es la fuente de verdad del proyecto. El equipo (o un agente de IA) escribe primero una especificación detallada que describe *qué* debe hacer el sistema, deriva después un plan de implementación, lo divide en tareas atómicas y solo entonces genera el código.

La especificación no es un documento estático: vive en el repositorio junto al código, evoluciona con el proyecto y puede regenerar el código cuando los requisitos cambian.

SDD surgió en 2025 como respuesta directa al fracaso del *vibe coding* —la práctica de prompting improvisado con LLMs que produce código plausible pero que deriva del intento original, alucina APIs y se degrada a medida que el proyecto escala. Para 2026, todas las herramientas principales de codificación con IA (GitHub Spec Kit, AWS Kiro, Claude Code, Cursor, OpenSpec, BMAD, Tessl, Google Antigravity) han incorporado su propio sabor de SDD.

### Los tres problemas que SDD resuelve

| Problema | Descripción | Cómo lo resuelve SDD |
|---|---|---|
| **Intent drift** | Un prompt como "añadir login" está infraespecificado; el modelo elige defaults razonables que raramente coinciden con lo que el equipo quería | La spec define comportamiento, precondiciones, postcondiciones y casos borde explícitamente |
| **Context decay** | A medida que la base de código crece más allá de la ventana de contexto del agente, este olvida decisiones previas y las contradice silenciosamente | La spec es un registro duradero de lo que se decidió, qué está en scope y qué restricciones aplican |
| **Unverifiable output** | Sin criterios de aceptación explícitos, no hay forma de saber si el código del agente es "correcto" | La spec incluye criterios de aceptación ejecutables que actúan como gate de validación |

### Los tres niveles de madurez SDD

Según el análisis de Martin Fowler y el paper fundacional de arXiv (Feb 2026):

- **Spec-first:** Las specs guían la generación y el código se mantiene manualmente.
- **Spec-anchored:** Specs y código coexisten; la spec rige el diseño pero el código puede divergir.
- **Spec-as-source:** La spec es el único artefacto mantenido por humanos; el código es completamente generado.

---

## 2. Por qué SDD encaja bien con la IA generativa

La IA generativa es extraordinariamente capaz de transformar *intención clara* en *implementación correcta*. El problema no es la capacidad del modelo: es la claridad de la entrada. SDD actúa como el puente entre el pensamiento humano y la ejecución de la máquina.

### La paradoja de la productividad con IA

El 75% de los ingenieros ya usa herramientas de IA, pero la mayoría de organizaciones no observa mejora medible en métricas de entrega (DORA State of DevOps 2024/2025). El cuello de botella nunca fue escribir código. Siempre fue la claridad de lo que se construye antes de escribir una sola línea.

Cuando la IA acelera la generación de código sin mejorar la capa de especificación, los problemas llegan más rápido, no más despacio.

### Por qué la IA necesita specs, no prompts

| Dimensión | Prompt ad-hoc | Especificación SDD |
|---|---|---|
| **Precisión** | Ambigüedad natural → outputs variables | Contrato formal → outputs consistentes |
| **Contexto** | Se pierde entre sesiones | Persiste en el repo, siempre disponible |
| **Verificación** | No hay referencia → revisiones interminables | Los criterios de aceptación son el juez |
| **Trazabilidad** | Ninguna (el código no tiene parent) | Código ← Tarea ← Plan ← Spec ← Requisito |
| **Escalabilidad** | Se degrada con el tamaño | La spec delimita el scope explícitamente |

### Datos que respaldan SDD con IA

- GitHub reporta que los equipos que usan Spec Kit en proyectos internos completan features con un orden de magnitud menos ciclos de "regenerar desde cero" que con prompting ad-hoc.
- AWS Kiro documenta casos reales donde features de 40 horas se entregaron en menos de 8 horas de tiempo humano al escribir specs primero.
- El paper de arXiv (Nov 2025) sobre adopción de Cursor AI en 807 repositorios de GitHub encontró ganancias de velocidad transitorias junto a incrementos persistentes en complejidad del código cuando no se usaban specs.
- Los LLMs generan código vulnerable en rangos del 9.8% al 42.1% según benchmarks; para febrero de 2026 más de 110.000 issues introducidas por IA seguían vivas en repositorios de producción.

---

## 3. Diferencia entre SDD, TDD y BDD

SDD comparte ADN con TDD y BDD, pero difiere en qué trata como artefacto canónico y en quién implementa.

| Dimensión | TDD | BDD | SDD |
|---|---|---|---|
| **Artefacto primario** | Test unitario | Escenario en lenguaje natural (Gherkin) | Especificación estructurada multi-nivel |
| **Principio central** | Escribe el test antes que el código | Escribe el comportamiento en lenguaje de negocio | Escribe la spec antes que el plan, y el plan antes que el código |
| **Implementador** | Desarrollador humano | Desarrollador humano | Humano, agente de IA o ambos |
| **Scope** | Función/unidad | Comportamiento/feature | Sistema completo: requisitos + diseño + tareas + restricciones |
| **Feedback loop** | Red-Green-Refactor | Failing scenario → implementation | Spec review → plan review → task → código → criterios de aceptación |
| **Complementariedad** | SDD genera los tests de TDD | SDD puede generar los escenarios de BDD | Orquesta TDD y BDD como subprocesos |
| **Vigencia** | Bien establecido desde los 2000s | Bien establecido desde los 2010s | Emergió como práctica mainstream en 2025 |

**La diferencia clave:** TDD dice *"escribe el test primero"*. BDD dice *"escribe el comportamiento primero, en lenguaje de negocio"*. SDD dice *"escribe la especificación completa del sistema primero —incluyendo intención, arquitectura, restricciones y criterios de aceptación— y que el agente derive todo lo demás desde ella"*.

> SDD no reemplaza a TDD ni a BDD. Los engloba: una buena spec SDD genera los tests de TDD y los escenarios de BDD como artefactos derivados.

---

## 4. Principios básicos de SDD

### P1 — La spec es la fuente de verdad

El código es un artefacto derivado, regenerable. La spec es lo que los humanos mantienen. Cuando hay discrepancia entre spec y código, el código está mal.

### P2 — La spec es versionada y vive en el repositorio

La spec no es un documento en Confluence o un Google Doc. Vive en el mismo repositorio que el código, se versiona con Git, evoluciona en las mismas PRs y tiene sus propios reviewers.

### P3 — La spec es estructurada, no prosa libre

Usa un esquema fijo: historias de usuario, criterios de aceptación en notación EARS, restricciones arquitectónicas, una "constitución" de reglas del proyecto. La prosa libre es ambigua para los agentes.

### P4 — La spec es ejecutable (en el sentido del agente)

Un agente de codificación puede leerla, generar un plan, dividirlo en tareas, escribir el código y verificar el resultado contra los criterios de aceptación originales. La spec es el prompt maestro.

### P5 — Los cambios van primero a la spec

Cuando llega un bug o una petición de feature, se edita la spec primero. El código se regenera o modifica para coincidir. Nunca al revés.

### P6 — Los checkpoints humanos son obligatorios

Cada transición de fase (Spec → Plan → Tareas → Código) requiere revisión y aprobación humana. SDD no es automatización ciega: es colaboración estructurada entre humanos y agentes.

### P7 — La notación EARS hace los requisitos AI-parseable

EARS (Easy Approach to Requirements Syntax), creado por Alistair Mavin en Rolls-Royce en 2009, define cinco patrones de frases que convierten requisitos ambiguos en declaraciones testables e inequívocas:

| Tipo | Patrón | Ejemplo |
|---|---|---|
| **Ubiquitous** | The \[system\] shall \[action\] | El sistema debe registrar todos los intentos de login |
| **Event-driven** | When \[trigger\], the \[system\] shall \[action\] | Cuando el usuario envíe el formulario, el sistema debe validar el email |
| **State-driven** | While \[state\], the \[system\] shall \[action\] | Mientras el usuario esté autenticado, el sistema debe mostrar el dashboard |
| **Unwanted behavior** | If \[condition\], then the \[system\] shall \[action\] | Si el token ha expirado, el sistema debe redirigir al login |
| **Optional feature** | Where \[feature included\], the \[system\] shall \[action\] | Donde la integración con SSO esté habilitada, el sistema debe usar OAuth 2.0 |

---

## 5. Flujo práctico de trabajo con SDD

El flujo estándar que ha popularizado GitHub Spec Kit es de **cuatro fases**, cada una con un checkpoint humano obligatorio.

```
IDEA / REQUISITO
      │
      ▼
┌─────────────┐     revisión humana obligatoria
│  FASE 1     │ ──────────────────────────────────►  ¿Aprobada?
│  SPECIFY    │                                         │
│  (spec.md)  │                                         │ Sí
└─────────────┘                                         ▼
                                              ┌─────────────┐     revisión humana
                                              │  FASE 2     │ ───────────────────►  ¿Aprobado?
                                              │  PLAN       │                            │
                                              │  (plan.md)  │                            │ Sí
                                              └─────────────┘                            ▼
                                                                             ┌─────────────┐     revisión humana
                                                                             │  FASE 3     │ ──────────────────►  ¿Aprobadas?
                                                                             │  TASKS      │                           │
                                                                             │ (tasks.md)  │                           │ Sí
                                                                             └─────────────┘                           ▼
                                                                                                         ┌─────────────┐
                                                                                                         │  FASE 4     │
                                                                                                         │  IMPLEMENT  │
                                                                                                         │  (código)   │
                                                                                                         └─────────────┘
```

### Fase 1 — Specify (Especificar)

El humano o el agente redacta el documento de especificación usando la plantilla estructurada. Incluye:

- Descripción del feature/sistema
- Historias de usuario con criterios de aceptación en EARS
- Requisitos no funcionales (rendimiento, seguridad, escalabilidad)
- Restricciones técnicas y de negocio
- Out of scope explícito

**Checkpoint:** El equipo revisa y aprueba la spec antes de continuar.

### Fase 2 — Plan (Planificar)

El agente lee la spec aprobada y genera un plan técnico. Incluye:

- Arquitectura de la solución
- Componentes a crear o modificar
- Diagrama de secuencia o flujo de datos
- Dependencias y orden de implementación
- Riesgos técnicos identificados

**Checkpoint:** El arquitecto o tech lead revisa y aprueba el plan.

### Fase 3 — Tasks (Descomponer en tareas)

El agente transforma el plan en tareas atómicas, trazables e independientes. Cada tarea:

- Tiene un criterio de done claro
- Referencia el requisito padre en la spec
- Cabe en una sola sesión de agente
- Indica si requiere test unitario, de integración o ambos

**Checkpoint:** El equipo revisa las tareas, ajusta prioridades, detecta solapamientos.

### Fase 4 — Implement (Implementar)

El agente ejecuta las tareas en orden. Para cada tarea:

1. Lee la spec y la tarea
2. Genera el código
3. Genera los tests
4. Verifica contra los criterios de aceptación
5. Reporta resultado (pass/fail)

El humano supervisa, interviene si hay fallo y hace code review final.

---

## 6. Artefactos principales de un modelo SDD

### Artefactos núcleo (los tres fundamentales)

**`requirements.md` / `spec.md`**
El corazón de SDD. Contiene las historias de usuario con criterios de aceptación en EARS, requisitos no funcionales y restricciones. Es el único documento que nunca se puede omitir.

**`design.md` / `plan.md`**
La arquitectura técnica de la solución: decisiones de diseño, diagramas de secuencia, stack tecnológico, estructura de datos, interfaces entre componentes.

**`tasks.md`**
Lista ordenada de tareas atómicas de implementación. Cada tarea incluye descripción, criterio de done, referencia a requisito padre y estimación de complejidad.

### Artefactos de gobernanza

**`CONSTITUTION.md` / `PROJECT_RULES.md`**
Las reglas del proyecto que aplican a todos los features: convenciones de código, patrones prohibidos, principios de seguridad, stack tecnológico fijo, estilo de tests. El agente las lee en cada sesión para no contradecir decisiones previas.

**`TECH_STACK.md`**
Inventario de las tecnologías, versiones, librerías y frameworks del proyecto. Previene que el agente alucine APIs de librerías incorrectas o mezcle versiones incompatibles.

**`ARCHITECTURE.md`**
Descripción de la arquitectura general del sistema (puede incluir diagramas C4): contexto, contenedores, componentes y código.

### Artefactos de trazabilidad

**`TRACEABILITY_MATRIX.md`**
Mapeo bidireccional entre requisitos, tareas y tests. Permite auditar si cada requisito tiene implementación y cobertura de test, y si cada línea de código tiene un requisito padre.

**`CHANGELOG_SPEC.md`**
Historial de cambios en la spec, con justificación de cada decisión. Esencial para proyectos regulados (DO-178C, ISO 26262, FDA 21 CFR Part 11).

---

## 7. Cómo usar IA en cada fase de SDD

### IA en la fase de Specify

| Tarea | Prompt / Acción |
|---|---|
| Generar borrador de spec desde una idea | `"Actúa como analista de requisitos. Dado este brief: [idea], genera un spec.md con historias de usuario en formato EARS, criterios de aceptación, requisitos no funcionales y out of scope."` |
| Validar cobertura de edge cases | `"Revisa esta spec y lista los casos borde no cubiertos, las ambigüedades y los requisitos contradictorios."` |
| Convertir prosa a EARS | `"Convierte estos requisitos en prosa a notación EARS, usando los cinco patrones: ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature."` |
| Detectar requisitos faltantes | `"Dado el dominio [X], ¿qué requisitos típicos faltan en esta spec?"` |

### IA en la fase de Plan

| Tarea | Prompt / Acción |
|---|---|
| Generar diseño técnico | `"Lee esta spec aprobada y genera un design.md con arquitectura propuesta, diagrama de secuencia y decisiones de diseño justificadas."` |
| Evaluar alternativas técnicas | `"Propón tres enfoques arquitectónicos para este requisito y compara sus trade-offs."` |
| Detectar conflictos con arquitectura existente | `"Dado este ARCHITECTURE.md existente y esta nueva spec, identifica conflictos y propón resoluciones."` |

### IA en la fase de Tasks

| Tarea | Prompt / Acción |
|---|---|
| Generar lista de tareas | `"Dado este plan.md aprobado, genera un tasks.md con tareas atómicas ordenadas por dependencia, cada una con criterio de done y referencia al requisito padre."` |
| Estimar complejidad | `"Evalúa la complejidad de cada tarea (S/M/L) y justifica tu estimación."` |
| Detectar dependencias circulares | `"Analiza este tasks.md y detecta dependencias circulares o tareas que deberían reordenarse."` |

### IA en la fase de Implement

| Tarea | Prompt / Acción |
|---|---|
| Implementar tarea atómica | `"Lee CONSTITUTION.md, TECH_STACK.md y spec.md. Implementa la tarea #7 del tasks.md. Escribe el código y los tests. Verifica contra los criterios de aceptación."` |
| Code review automatizado | `"Dado este código generado y la spec de referencia, verifica: (1) cumple los criterios de aceptación, (2) sigue las reglas de CONSTITUTION.md, (3) no introduce vulnerabilidades."` |
| Actualizar spec tras cambio | `"El requisito R-04 ha cambiado. Actualiza spec.md, identifica qué tareas del tasks.md se ven afectadas y genera las tareas de re-implementación necesarias."` |

---

## 8. Estructura recomendada de repositorio SDD

```
mi-proyecto/
├── .specify/                    # Config de herramientas SDD (Spec Kit, etc.)
│   └── config.yaml
│
├── specs/                       # Artefactos SDD (fuente de verdad)
│   ├── CONSTITUTION.md          # Reglas del proyecto (siempre cargado)
│   ├── TECH_STACK.md            # Stack y versiones fijas
│   ├── ARCHITECTURE.md          # Arquitectura general del sistema
│   ├── TRACEABILITY_MATRIX.md   # Requisito ↔ Tarea ↔ Test
│   │
│   └── features/                # Un subdirectorio por feature/épica
│       ├── auth/
│       │   ├── spec.md          # Requisitos del feature
│       │   ├── plan.md          # Diseño técnico
│       │   └── tasks.md         # Tareas atómicas
│       └── payments/
│           ├── spec.md
│           ├── plan.md
│           └── tasks.md
│
├── src/                         # Código fuente (artefacto derivado)
│   └── ...
│
├── tests/                       # Tests (artefacto derivado de specs)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                        # Documentación para humanos
│   └── adr/                     # Architecture Decision Records
│
└── README.md
```

### Convenciones clave

- Todo cambio de código que no tenga una spec padre es rechazado en PR.
- La CONSTITUTION.md se inyecta en el contexto del agente en cada sesión.
- Los archivos `tasks.md` usan checkboxes de Markdown para trackear progreso.
- Los spec changes requieren un segundo revisor humano (four-eyes principle).

---

## 9. Plantilla mínima de especificación SDD

```markdown
# Spec: [Nombre del Feature]

**ID:** FEAT-001
**Versión:** 1.0
**Estado:** Draft | In Review | Aprobada | Implementada
**Fecha:** YYYY-MM-DD
**Autor:** [nombre]
**Revisor:** [nombre]

---

## 1. Contexto y objetivo

[Descripción breve del problema que resuelve este feature y por qué es necesario ahora]

## 2. Historias de usuario

### US-01: [Nombre]
**Como** [rol de usuario]
**Quiero** [capacidad]
**Para** [beneficio]

#### Criterios de aceptación (EARS)

- [ ] **EARS-01** [Ubiquitous] El sistema debe [acción]
- [ ] **EARS-02** [Event-driven] Cuando [trigger], el sistema debe [acción]
- [ ] **EARS-03** [State-driven] Mientras [estado], el sistema debe [acción]
- [ ] **EARS-04** [Unwanted] Si [condición de error], el sistema debe [respuesta]

### US-02: [Nombre]
...

## 3. Requisitos no funcionales

| Categoría | Requisito | Métrica |
|---|---|---|
| Rendimiento | Tiempo de respuesta | < 200ms en p95 |
| Seguridad | Autenticación requerida | JWT con expiración de 1h |
| Escalabilidad | Usuarios concurrentes | Soportar 1000 concurrent users |

## 4. Restricciones técnicas

- Stack: [tecnologías obligatorias]
- Restricciones: [lo que NO se puede usar]
- Integraciones: [sistemas externos afectados]

## 5. Out of scope

- [Item explícitamente excluido 1]
- [Item explícitamente excluido 2]

## 6. Dependencias

- **Requiere:** [Feature o sistema del que depende]
- **Afecta a:** [Features o sistemas que pueden verse impactados]

## 7. Glosario

| Término | Definición |
|---|---|
| [Término] | [Definición precisa en el contexto de este feature] |
```

---

## 10. Ventajas de SDD

### Para el equipo de desarrollo

- **Contexto siempre disponible:** el agente de IA tiene toda la información que necesita en cada sesión, sin depender de conversaciones anteriores.
- **Reducción de retrabajos:** los criterios de aceptación explícitos eliminan la ambigüedad que genera código incorrecto.
- **Onboarding acelerado:** un nuevo miembro del equipo puede leer las specs y entender el sistema sin revisar el código.
- **Code reviews más rápidas:** el revisor verifica contra la spec, no contra su propia interpretación de los requisitos.

### Para el proyecto

- **Trazabilidad completa:** cada línea de código puede rastrearse hasta un requisito de negocio.
- **Deuda técnica visible:** la spec revela dónde el código diverge del diseño original.
- **Estimaciones más precisas:** el plan descompone el trabajo antes de empezar, no durante.
- **Cambios de requisitos gestionables:** cambiar la spec primero permite evaluar el impacto antes de tocar el código.

### Para la organización

- **Cumplimiento normativo facilitado:** en sectores regulados (aeroespacial, médico, automotriz), la trazabilidad requisito-código es obligatoria por norma (DO-178C, ISO 26262, FDA 21 CFR).
- **Reducción del bus factor:** el conocimiento del sistema vive en las specs, no solo en las cabezas de los desarrolladores.
- **Independencia de modelo:** las specs son agnósticas al modelo de IA. Un equipo con specs maduras puede cambiar de GPT a Claude a Gemini y obtener resultados equivalentes.
- **Leverage sobre nuevas generaciones de IA:** equipos que construyeron su librería de specs en 2025-2026 pueden regenerar contra Claude 6 o GPT-6 y beneficiarse inmediatamente; los que no, no pueden.

### Datos empíricos

- Tasa de éxito en primera generación de código: ~3-10× superior con SDD versus prompting ad-hoc (reportes de early adopters en GitHub y AWS).
- Features de 2 semanas reducidas a 2 días con AWS Kiro (caso de feature de notificaciones documentado por AWS).

---

## 11. Riesgos y errores frecuentes

### ❌ Error 1: Specs como documentos ceremoniales

**Problema:** Escribir specs extensas que nadie lee ni mantiene, convirtiéndolas en documentación muerta.
**Solución:** La spec debe ser el input directo del agente. Si no puedes pegarla en el contexto del agente y obtener código correcto, está mal escrita. Empieza pequeña y crece iterativamente.

### ❌ Error 2: Especificar el "cómo" en vez del "qué"

**Problema:** Escribir specs que prescriben la implementación ("usa una clase UserService con un método `findById`") en vez del comportamiento esperado.
**Solución:** La spec define comportamiento observable, inputs, outputs y edge cases. El diseño de la implementación va en `plan.md`, no en `spec.md`.

### ❌ Error 3: Intentar especificar todo el sistema de golpe

**Problema:** Intentar escribir la spec completa de un sistema grande antes de empezar, lo que lleva a análisis-parálisis y specs que nunca se aprueban.
**Solución:** Spec por feature. Empieza con el MVP más pequeño y expande. Como dice el análisis de InfoQ Enterprise: "la spec necesita ser más granular cerca del área de cambio".

### ❌ Error 4: No versionar las specs

**Problema:** Mantener specs en herramientas externas (Confluence, Notion, Google Docs) desconectadas del código.
**Solución:** Las specs viven en el repo, se versionan con Git y evolucionan en las mismas PRs que el código.

### ❌ Error 5: Omitir los checkpoints humanos

**Problema:** Dejar que el agente pase de spec a plan a tareas a código sin revisión, asumiendo que la spec era perfecta.
**Solución:** Cada transición de fase es un checkpoint obligatorio. El agente propone; el humano aprueba.

### ❌ Error 6: CONSTITUTION.md desactualizada

**Problema:** Las reglas del proyecto en `CONSTITUTION.md` se quedan obsoletas, y el agente genera código que contradice las convenciones actuales.
**Solución:** La CONSTITUTION.md es un artefacto de equipo con ownership claro. Cualquier cambio de arquitectura o convención actualiza la CONSTITUTION.md primero.

### ❌ Error 7: Aplicar SDD a proyectos de exploración

**Problema:** Usar SDD con todo el rigor documental para prototipos, pruebas de concepto o exploración técnica.
**Solución:** SDD es para software que va a producción y necesita mantenerse. Para exploración, el *vibe coding* es válido. La regla: "vibe coding para explorar, SDD para producción".

### ⚠️ Riesgo: Falsa sensación de seguridad

Tener specs no garantiza código correcto si las specs son imprecisas o incompletas. La calidad de la spec determina la calidad del output. Invertir en revisar specs antes de ejecutar es siempre más barato que corregir código incorrecto después.

---

## 12. SDD aplicado a una modificación de aplicación existente

Uno de los desafíos más comunes es introducir SDD en una base de código existente, sin specs previas. El enfoque recomendado por el paper fundacional de arXiv y por OpenSpec es incremental y no requiere especificar todo el sistema de golpe.

### Estrategia: Spec-near-the-change

```
CODEBASE EXISTENTE (sin specs)
         │
         ▼
FASE A: Reconstruir el comportamiento actual
  └─ Usar IA para reverse-engineering de specs desde el código
  └─ Foco: solo el área que va a cambiar, no todo el sistema
         │
         ▼
FASE B: Validar la spec extraída
  └─ Ejecutar tests existentes contra la spec reconstruida
  └─ Corregir discrepancias spec vs comportamiento real
         │
         ▼
FASE C: Especificar el cambio
  └─ Escribir spec del cambio solicitado (nueva funcionalidad o bugfix)
  └─ Referenciar la spec base extraída en FASE A
         │
         ▼
FASE D: Ciclo SDD estándar (Plan → Tasks → Implement)
```

### Prompt para reverse-engineering de specs

```
Actúa como analista de requisitos experto en reverse engineering.
Analiza el siguiente código [pegar código o módulo] y extrae:
1. Los comportamientos observables (en formato EARS)
2. Las precondiciones y postcondiciones implícitas
3. Los casos borde y comportamientos de error
4. Las dependencias externas y contratos de API
Genera un spec.md siguiendo esta plantilla: [plantilla del §9]
```

### Principios para brownfield SDD

- **Granularidad cerca del cambio:** La spec no necesita cubrir todo el sistema; debe ser más detallada cerca del código que se va a modificar.
- **Trazabilidad incremental:** Cada bug fix o feature addition es una oportunidad para añadir specs al código que se toca.
- **Tests existentes como punto de partida:** Los tests existentes (si los hay) son evidencia de comportamiento esperado; úsalos para validar la spec extraída.
- **No retroespecificar todo:** Intentar especificar retroactivamente sistemas grandes es impráctico. La cobertura de specs crece orgánicamente con cada cambio.

---

## 13. SDD y repositorio de conocimiento interno

SDD transforma naturalmente el repositorio de código en un **repositorio de conocimiento organizacional**. Las specs acumuladas representan la intención de negocio cristalizada del sistema, no solo su implementación.

### La CONSTITUTION.md como memoria institucional

La constitución del proyecto captura decisiones que de otro modo solo vivirían en las cabezas de los desarrolladores o en tickets cerrados:

```markdown
# CONSTITUTION.md — Nombre del Proyecto

## Principios de diseño
- Este sistema prioriza la consistencia eventual sobre la sincronía fuerte
- Toda comunicación entre servicios usa eventos (no llamadas síncronas)
- Los IDs son UUIDs v4, nunca auto-incrementales

## Stack tecnológico (no negociable)
- Backend: Node.js 22 + Fastify
- Base de datos: PostgreSQL 16 (no MongoDB, no Redis como base de datos primaria)
- Auth: JWT + refresh tokens (no sesiones en servidor)

## Patrones prohibidos
- No usar `any` en TypeScript
- No queries directas a BD desde controllers (siempre a través de repositorios)
- No lógica de negocio en la capa de presentación

## Convenciones
- Tests: Vitest, cobertura mínima del 80% en servicios
- Nombres de branches: feature/FEAT-XXX-nombre-corto
- Commits: Conventional Commits (feat, fix, docs, test, refactor)
```

### SDD como base de datos de decisiones

Cada `plan.md` aprobado es un Architecture Decision Record (ADR) implícito. Con una estructura de specs bien mantenida, la organización puede:

- Responder "¿por qué se construyó así?" sin buscar en Slack o emails
- Incorporar nuevos miembros de equipo con contexto real, no suposiciones
- Auditar el sistema para cumplimiento normativo con evidencia documental
- Regenerar módulos completos ante cambios de stack tecnológico

### Integración con herramientas de gestión

| Herramienta | Integración SDD |
|---|---|
| Jira / Linear | Las tareas del `tasks.md` se sincronizan como tickets, con referencia al spec padre |
| Confluence | Las specs aprobadas se publican automáticamente como documentación de producto |
| GitHub / GitLab | Las PRs exigen que el código referencie un requisito de spec (enforced via CI) |
| MCP Servers | Los agentes con acceso a MCP pueden leer Jira, Confluence y el repo simultáneamente para mantener alineación en tiempo real |

---

## 14. Relación entre SDD y skills de IA

Las **skills de IA** (también llamadas agent skills, custom agents o slash commands) son la forma de empaquetar un flujo SDD como una capacidad reutilizable del agente. En lugar de repetir el mismo conjunto de instrucciones en cada sesión, se codifican una vez y se invocan bajo demanda.

### Qué es una skill SDD

Una skill SDD es un artefacto que encapsula:

1. **Las plantillas de spec, plan y tasks** del proyecto
2. **Las reglas de la CONSTITUTION** inyectadas automáticamente
3. **El flujo de fases** (Specify → Plan → Tasks → Implement) con sus checkpoints
4. **Los patrones de EARS** con ejemplos del dominio específico
5. **Los prompts de cada fase** optimizados para el proyecto

### Ejemplo: skill SDD en Claude Code

```markdown
<!-- .claude/skills/sdd-feature.md -->
# Skill: SDD Feature Development

## Cuando se invoca /sdd-feature [descripción]

1. LEE: specs/CONSTITUTION.md, specs/TECH_STACK.md, specs/ARCHITECTURE.md
2. GENERA: specs/features/[nombre]/spec.md usando la plantilla estándar
3. ESPERA APROBACIÓN HUMANA antes de continuar
4. GENERA: specs/features/[nombre]/plan.md
5. ESPERA APROBACIÓN HUMANA antes de continuar
6. GENERA: specs/features/[nombre]/tasks.md
7. ESPERA APROBACIÓN HUMANA antes de continuar
8. IMPLEMENTA: una tarea a la vez, verificando criterios de aceptación
9. ACTUALIZA: TRACEABILITY_MATRIX.md al completar cada tarea

## Restricciones
- Nunca escribas código sin spec aprobada
- Nunca pases de fase sin checkpoint explícito
- Siempre referencia el requisito EARS en cada función que implementes
```

### GitHub Spec Kit y Claude Code Skills

GitHub Spec Kit (open source, +90k estrellas en mid-2026) es el toolkit que popularizó las cuatro fases de SDD. Funciona con más de 30 agentes: Claude Code, Copilot, Codex, Gemini, Cursor, Windsurf. AWS Kiro integra el flujo SDD directamente en el IDE (VSCode fork), con agent hooks que disparan automáticamente actualizaciones de specs cuando se guardan archivos de código.

---

## 15. Modelo operativo recomendado

El modelo operativo SDD redistribuye los roles del equipo. El trabajo de alto valor se desplaza hacia arriba (especificación, arquitectura, revisión) y el trabajo de implementación lo ejecutan los agentes.

### Roles en un equipo SDD

| Rol | Responsabilidades en SDD |
|---|---|
| **Product Owner / BA** | Escribe o valida los requisitos en lenguaje de negocio. Aprueba la spec en Fase 1. Define criterios de aceptación con el equipo. |
| **Arquitecto / Tech Lead** | Diseña y aprueba el plan técnico (Fase 2). Mantiene CONSTITUTION.md y ARCHITECTURE.md. Revisa las tareas de Fase 3 para coherencia técnica. |
| **Desarrollador Senior** | Revisa el código generado en Fase 4. Resuelve casos donde el agente falla. Mejora las specs basándose en lo aprendido en implementación. |
| **Agente de IA** | Genera borradores de specs (Fase 1). Genera planes y tareas (Fases 2-3). Implementa tareas atómicas (Fase 4). Verifica criterios de aceptación. |
| **QA / Test Engineer** | Valida los criterios de aceptación EARS. Asegura cobertura de la matriz de trazabilidad. Gestiona tests de regresión. |

### Cadencia operativa recomendada

```
SPRINT (2 semanas)
│
├── Day 1-2: SPECIFY
│   └── Escribir specs para los features del sprint
│   └── Revisión y aprobación en standup
│
├── Day 2-3: PLAN
│   └── Agente genera planes técnicos
│   └── Tech lead revisa y aprueba
│
├── Day 3-4: TASKS
│   └── Agente descompone en tareas
│   └── Equipo revisa, ajusta y asigna
│
├── Day 4-9: IMPLEMENT
│   └── Agentes implementan tarea a tarea
│   └── Devs senior supervisan y revisan PRs
│
└── Day 10: RETROSPECTIVE
    └── ¿Qué specs fueron imprecisas? → Mejorar plantillas
    └── ¿Qué falló en implementación? → Actualizar CONSTITUTION.md
    └── ¿Qué criterios de aceptación faltaron? → Actualizar checklist
```

### Indicadores de salud del proceso SDD

| Métrica | Objetivo | Señal de alarma |
|---|---|---|
| % de código con spec padre | > 90% | < 70% |
| % de criterios EARS con test | > 80% | < 60% |
| Ciclos de regeneración por feature | < 2 | > 5 |
| Tiempo de spec a PR aprobado | Definido por equipo | 3× la media → spec incompleta |
| Divergencias spec vs código detectadas | 0 en producción | Cualquiera → auditoría |

---

## 16. Checklist de calidad SDD

### ✅ Checklist de spec (antes de aprobar Fase 1)

- [ ] ¿Tiene ID único y versión?
- [ ] ¿Cada historia de usuario sigue el formato "Como / Quiero / Para"?
- [ ] ¿Cada criterio de aceptación usa notación EARS (uno de los cinco patrones)?
- [ ] ¿Los criterios de aceptación son testables (binarios, no subjetivos)?
- [ ] ¿Se ha definido el "out of scope" explícitamente?
- [ ] ¿Los requisitos no funcionales tienen métricas concretas?
- [ ] ¿Se han listado todas las dependencias externas?
- [ ] ¿El glosario define todos los términos ambiguos del dominio?
- [ ] ¿Un agente puede leer esta spec y generar el código correcto sin preguntas adicionales?

### ✅ Checklist de plan (antes de aprobar Fase 2)

- [ ] ¿El plan referencia explícitamente cada requisito de la spec?
- [ ] ¿Las decisiones de diseño están justificadas (no solo "hemos elegido X")?
- [ ] ¿El plan es consistente con CONSTITUTION.md y TECH_STACK.md?
- [ ] ¿Se ha identificado el impacto en módulos existentes?
- [ ] ¿El diagrama de secuencia o flujo cubre los happy path y los error path?

### ✅ Checklist de tareas (antes de aprobar Fase 3)

- [ ] ¿Cada tarea es atómica (no puede dividirse más sin perder sentido)?
- [ ] ¿Cada tarea tiene un criterio de done binario?
- [ ] ¿Cada tarea referencia el requisito EARS padre?
- [ ] ¿Las dependencias entre tareas están ordenadas correctamente?
- [ ] ¿Ninguna tarea tarda más de media jornada de agente?

### ✅ Checklist de implementación (antes de aprobar PR)

- [ ] ¿El código implementa todos los criterios EARS de la spec?
- [ ] ¿Los tests cubren los happy path y los error path de la spec?
- [ ] ¿No hay código que no tenga un requisito padre en la spec?
- [ ] ¿La TRACEABILITY_MATRIX.md está actualizada?
- [ ] ¿El código sigue todas las reglas de CONSTITUTION.md?
- [ ] ¿La spec y el plan se han actualizado si hubo cambios durante la implementación?

---

## 17. Ejemplo de prompt maestro para SDD

El siguiente prompt maestro es un point of entry para iniciar un flujo SDD completo desde una idea de negocio. Está diseñado para ser usado con Claude Code, GitHub Copilot, Cursor o cualquier agente capaz de manejar archivos.

```markdown
# PROMPT MAESTRO SDD — Iniciar nuevo feature

## Contexto del proyecto (inyectar siempre)
Lee los siguientes archivos de contexto antes de cualquier acción:
- specs/CONSTITUTION.md (reglas inmutables del proyecto)
- specs/TECH_STACK.md (stack tecnológico fijo)
- specs/ARCHITECTURE.md (arquitectura del sistema)
- specs/TRACEABILITY_MATRIX.md (mapa de requisitos actuales)

## Tu rol
Eres un ingeniero de software senior y analista de requisitos experto en
Spec-Driven Development. Tu trabajo es guiar al equipo a través de las
cuatro fases de SDD sin saltarte ningún checkpoint humano.

## Instrucciones de comportamiento
1. NUNCA escribas código sin una spec aprobada por el humano
2. SIEMPRE espera aprobación explícita antes de pasar de fase
3. SIEMPRE usa notación EARS para criterios de aceptación
4. SIEMPRE referencia el requisito padre en cada función que implementes
5. Si encuentras ambigüedad en la spec, detente y pregunta antes de asumir
6. Si un requisito contradice CONSTITUTION.md, alerta al humano antes de continuar

## Feature a desarrollar
[DESCRIPCIÓN DEL FEATURE: escribe aquí en lenguaje natural lo que necesitas]

## Fase de inicio
Comienza en FASE 1 (Specify).

Genera el archivo `specs/features/[nombre-del-feature]/spec.md` siguiendo
esta plantilla: [insertar plantilla del §9]

Al terminar, presenta la spec al humano y espera su aprobación.
NO pases a Fase 2 hasta recibir "aprobado" o "approved".
```

### Prompt para sesión de continuación (retomar trabajo)

```markdown
## Contexto
Estamos implementando el feature [NOMBRE] usando SDD.

Lee estos archivos:
- specs/CONSTITUTION.md
- specs/TECH_STACK.md
- specs/features/[nombre]/spec.md (APROBADA)
- specs/features/[nombre]/plan.md (APROBADO)
- specs/features/[nombre]/tasks.md (APROBADO)

## Estado actual
Las tareas completadas son: [lista de checkboxes marcados]
La próxima tarea a implementar es: [TASK-XX]

## Instrucción
Implementa TASK-XX. Escribe el código y los tests.
Verifica que cumple los criterios de aceptación EARS-XX, EARS-YY.
Al terminar, muestra el código para revisión humana.
NO marques la tarea como completada hasta recibir "aprobado".
```

---

## 18. Mejores cursos para aprender SDD

### 🎓 Cursos online

**[Spec-Driven Development with Coding Agents — DeepLearning.AI](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents)**
El curso de referencia de la industria, lanzado en late 2025 y enseñado por Sandeep Dinesh. Cubre el flujo SDD completo, la introducción de SDD en codebases legacy y cómo empaquetar workflows en agent skills portables. Compatible con DeepLearning.AI Pro para quizzes y proyectos. Recomendado como punto de partida para profesionales.

**[AI Agent Factory — Chapter 16: Spec-Driven Development with Claude Code](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/spec-driven-development)**
Capítulo dedicado a SDD dentro del currículo de Panaversity's AI Agent Factory. Foco en Claude Code como herramienta de implementación. Orientado a developers que ya trabajan con agentes.

**[GitHub Spec Kit — Official Documentation and Tutorials](https://github.com/github/spec-kit)**
La documentación oficial del CLI open source de GitHub (+90k estrellas). Incluye tutoriales paso a paso para las cuatro fases, integración con 30+ agentes y plantillas de comunidad. Imprescindible para quien use el ecosistema GitHub.

**[AWS Kiro — Getting Started](https://kiro.dev)**
Guías oficiales del IDE de Amazon construido sobre SDD. Incluye walkthrough del flujo Requirements (EARS) → Design → Tasks → Implementation + Agent Hooks. Ideal para equipos en el ecosistema AWS.

**[Spec-Driven Development with AI: InfoQ Learning Path](https://www.infoq.com/articles/spec-driven-development/)**
Serie de artículos técnicos en profundidad publicada por InfoQ en enero de 2026 (Griffin & Carroll). Cubre adopción enterprise, patrones de trazabilidad y SDD para equipos regulados.

### 📺 Recursos de aprendizaje complementarios

- **Martin Fowler — "Exploring Gen AI: Spec-Driven Development"** (martinfowler.com, 2025): El marco conceptual que dio vocabulario moderno al campo.
- **Red Hat Developer — "How Spec-Driven Development Improves AI Coding Quality"** (Naszcyniec, Oct 2025): Perspectiva práctica desde equipos enterprise.
- **Addy Osmani — "How to write a good spec for AI agents"** (addyosmani.com, 2025): Guía de un ex-Google engineer sobre redacción efectiva de specs.
- **Birgitta Böckeler — "Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl"** (martinfowler.com, 2025): Comparativa de herramientas.

---

## 19. Libros y sites en la Web para aprender SDD

### 📚 Libros

**[Spec-Driven Development — Leanpub (2026)](https://leanpub.com/spec-driven-development-build-with-ai)**
Publicado en mayo de 2026 y 100% completo. Orientado a practitioners que quieren pasar de vibe coding a SDD con un flujo concreto. Cubre PRD, issues, tests y código como artefactos trazables y conectados. Sin teoría abstracta: cada concepto viene con proyecto real.

**[The AI Agent Factory — Spec-Driven Development Chapter](https://agentfactory.panaversity.org)**
Parte del libro/currículo de Panaversity sobre construcción de agentes de IA. El capítulo 16 está dedicado a SDD con Claude Code.

**[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180)**
El paper académico fundacional (arXiv, febrero 2026). Define formalmente los tres niveles de rigor (spec-first, spec-anchored, spec-as-source), el flujo estándar y el marco de evaluación. Referencia obligatoria para equipos que quieren fundamento teórico sólido.

### 🌐 Sites y recursos web

| Recurso | URL | Tipo | Descripción |
|---|---|---|---|
| BCMS Blog — SDD Guide | thebcms.com/blog/spec-driven-development | Guía | Referencia 2026 completa con comparativa de herramientas |
| Augment Code — SDD Guide | augmentcode.com/guides/what-is-spec-driven-development | Guía | Perspectiva técnica en profundidad, muy actualizada |
| Jama Software — SDD for AI Engineering | jamasoftware.com/blog/what-is-sdd | Guía | Enfoque en equipos regulados y trazabilidad enterprise |
| Product Builder — SDD 2026 | productbuilder.net/learn/spec-driven-development | Guía | Foco en Claude Code Skills y ecosistema de herramientas |
| Thoughtworks Blog | thoughtworks.medium.com/spec-driven-development | Blog | Perspectiva de consultoría enterprise, origen del término |
| InfoQ — SDD Article | infoq.com/articles/spec-driven-development | Artículo | Análisis técnico profundo, adopción enterprise |
| Martin Fowler | martinfowler.com/articles/exploring-gen-ai | Blog | Marco conceptual fundacional |
| arXiv — SDD Paper | arxiv.org/abs/2602.00180 | Paper | Paper académico fundacional (feb 2026) |
| GitHub Spec Kit | github.com/github/spec-kit | Tool | CLI open source, +90k estrellas |
| AWS Kiro | kiro.dev | Tool | IDE SDD nativo de Amazon |
| OpenSpec (Fission AI) | — | Tool | Alternativa minimalista, brownfield-friendly |
| BMAD-METHOD | github.com/bmadcode/BMAD-METHOD | Tool | Framework SDD orientado a comunidad |
| DeepLearning.AI SDD | deeplearning.ai/courses/spec-driven-development-with-coding-agents | Curso | Curso canónico de referencia |

---

## 20. Conclusión

Spec-Driven Development no es una moda pasajera ni un regreso al waterfall. Es la respuesta estructural de la industria a un problema concreto: la IA generativa ha eliminado la escasez de *implementación*, pero no ha eliminado la escasez de *claridad*. El cuello de botella en el desarrollo de software siempre fue la precisión de lo que se construye antes de escribir una sola línea. SDD pone ese cuello de botella en el centro de la metodología.

### Por qué SDD es inevitable en 2026

Tres fuerzas convergentes hacen de SDD la metodología de facto para proyectos TI serios con IA:

1. **La IA sin estructura produce caos a escala.** El vibe coding funciona para prototipos; destruye proyectos en producción. SDD es el antídoto probado.

2. **Las specs son el activo más duradero.** Los modelos de IA se reemplazan cada 12-18 meses. Las specs del proyecto no. Equipos con specs maduras pueden regenerar contra el próximo modelo y beneficiarse inmediatamente; equipos sin specs no.

3. **El cumplimiento normativo exige trazabilidad.** En sectores regulados —aeroespacial, médico, automotriz, financiero— la trazabilidad requisito-código es obligatoria. SDD la entrega como subproducto del flujo.

### El camino recomendado para empezar

1. **Empieza pequeño:** aplica SDD al próximo feature, no a todo el sistema existente.
2. **Usa herramientas maduras:** GitHub Spec Kit o AWS Kiro eliminan la fricción inicial.
3. **Haz la CONSTITUTION.md primero:** captura las reglas de tu proyecto antes de especificar features.
4. **Sigue los checkpoints:** la tentación de saltarse revisiones es constante; resístela.
5. **Itera sobre las plantillas:** cada sprint revela qué faltaba en las specs; mejora las plantillas.

> *"La escasez que modeló todo sobre cómo se organizan los equipos, cómo se valoran las habilidades y cómo se trata el código —la escasez de implementación— se está disolviendo. Lo que la IA no ha hecho barato es la claridad."*
>
> — mobiusvp.com, Spec Driven Development, mayo 2026

SDD es la disciplina que convierte esa claridad en ventaja competitiva sostenible.

---

*Documento generado en junio de 2026. Las herramientas y URLs pueden haber evolucionado; verificar versiones actuales antes de adopción.*
