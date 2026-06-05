# Spec-Driven Development: guía práctica para proyectos TI con IA

## 1. Qué es Spec-Driven Development

**Spec-Driven Development**, o **SDD**, es una forma de trabajar en la que la especificación funcional y técnica se convierte en el eje central del desarrollo de software.

La idea principal es sencilla: antes de construir, se define con claridad qué debe hacer el sistema, bajo qué reglas, con qué restricciones, qué escenarios debe cubrir y cómo se validará que el resultado es correcto.

En un enfoque tradicional, la documentación suele quedar como un subproducto del proyecto. En SDD ocurre lo contrario: la especificación es el artefacto principal desde el que se generan, derivan o validan otros elementos del ciclo de vida del software.

Entre esos elementos pueden estar:

- épicas;
- historias de usuario;
- criterios de aceptación;
- escenarios BDD;
- tareas técnicas;
- casos de prueba;
- documentación funcional;
- contratos de API;
- trazabilidad;
- scripts de validación;
- prompts y skills de IA;
- documentación para negocio, desarrollo, QA y soporte.

---

## 2. Por qué SDD encaja bien con la IA generativa

La IA generativa trabaja especialmente bien cuando recibe información clara, estructurada y contextualizada.

Por eso, SDD y la IA se complementan muy bien: cuanto mejor sea la especificación, mejores serán los artefactos que podrá generar o revisar la IA.

Un buen modelo SDD permite usar IA para:

- convertir requisitos iniciales en especificaciones estructuradas;
- detectar ambigüedades, contradicciones o lagunas;
- generar historias de usuario;
- generar escenarios BDD;
- generar casos de prueba funcionales;
- proponer tareas técnicas;
- revisar cobertura de requisitos;
- mantener trazabilidad entre requisitos, historias, pruebas y entregables;
- generar documentación ejecutiva o técnica;
- preparar entregables para Jira, Confluence, GitHub, HPQC/ALM u otras herramientas.

La clave no es pedirle a la IA que “invente” la solución, sino usarla como asistente de estructuración, revisión, generación y control de calidad.

---

## 3. Diferencia entre SDD, TDD y BDD

| Enfoque | Punto de partida | Artefacto principal | Objetivo |
|---|---|---|---|
| **TDD** | Prueba técnica | Test automatizado | Diseñar el código desde pruebas unitarias |
| **BDD** | Comportamiento esperado | Escenario Given/When/Then | Alinear negocio, desarrollo y QA |
| **SDD** | Especificación | Documento estructurado de requisitos y reglas | Dirigir todo el ciclo de desarrollo desde la especificación |

SDD no sustituye a TDD ni a BDD. Puede integrarlos.

Una forma práctica de verlo sería:

```text
SDD define qué debe hacer el sistema.
BDD expresa ese comportamiento en escenarios comprensibles.
TDD ayuda a construir el código desde pruebas técnicas.
```

---

## 4. Principios básicos de SDD

### 4.1. La especificación es el artefacto fuente

La especificación debe ser tratada como una fuente de verdad.

Esto implica que debe estar:

- versionada;
- revisada;
- trazada;
- estructurada;
- mantenida;
- vinculada a los artefactos derivados.

La especificación no debería vivir únicamente en correos, actas, conversaciones o documentos dispersos.

---

### 4.2. La especificación debe ser legible por humanos y procesable por IA

Una buena especificación SDD debe servir tanto para personas como para sistemas automáticos.

Por eso conviene trabajar con formatos como:

- Markdown;
- YAML;
- JSON;
- tablas estructuradas;
- plantillas homogéneas;
- identificadores únicos;
- secciones estables;
- reglas numeradas;
- escenarios trazables.

Ejemplo:

```markdown
## REQ-001 — Alta de producto

### Descripción
El sistema debe permitir dar de alta un nuevo producto de seguro para clientes empresa.

### Reglas de negocio
- RN-001: El producto debe estar asociado a un segmento comercial.
- RN-002: El producto debe tener condiciones particulares configurables.
- RN-003: El producto no podrá emitirse si falta documentación precontractual obligatoria.

### Criterios de aceptación
- CA-001: Dado un usuario autorizado, cuando informa todos los datos obligatorios, entonces el sistema permite guardar el producto.
- CA-002: Dado un usuario autorizado, cuando falta documentación obligatoria, entonces el sistema bloquea la emisión.
```

---

### 4.3. Todo requisito debe poder probarse

Un requisito que no puede probarse suele estar incompleto o mal formulado.

En SDD, cada requisito debería poder derivar en:

- criterios de aceptación;
- escenarios BDD;
- casos de prueba;
- validaciones funcionales;
- evidencias de cobertura.

Ejemplo:

```text
REQ-003 → CA-003.1 → BDD-003.1 → TC-003.1 → Evidencia QA
```

---

### 4.4. La trazabilidad debe mantenerse desde el inicio

La trazabilidad no debe reconstruirse al final del proyecto.

Debe nacer con la especificación y evolucionar con ella.

Una matriz mínima podría incluir:

| Requisito | Historia Jira | Criterio de aceptación | Caso de prueba | Estado |
|---|---|---|---|---|
| REQ-001 | US-101 | CA-001 | TC-001 | Cubierto |
| REQ-002 | US-102 | CA-002 | TC-002 | Pendiente |
| REQ-003 | US-103 | CA-003 | TC-003 | En revisión |

---

## 5. Flujo práctico de trabajo con SDD

Un flujo SDD aplicado a un proyecto real puede organizarse así:

```text
1. Entrada inicial de negocio
2. Estructuración de requisitos
3. Identificación de reglas de negocio
4. Detección de dudas y open points
5. Generación de especificación funcional
6. Derivación de épicas e historias
7. Generación de criterios de aceptación
8. Generación de escenarios BDD
9. Generación de casos de prueba
10. Revisión humana
11. Carga en herramientas corporativas
12. Seguimiento de trazabilidad
13. Actualización continua de la especificación
```

---

## 6. Artefactos principales de un modelo SDD

### 6.1. Documento de especificación funcional

Debe recoger:

- objetivo del cambio;
- alcance;
- fuera de alcance;
- actores;
- procesos afectados;
- sistemas afectados;
- reglas de negocio;
- validaciones;
- escenarios;
- dependencias;
- restricciones;
- dudas abiertas;
- criterios de aceptación;
- trazabilidad.

---

### 6.2. Backlog estructurado

A partir de la especificación pueden generarse:

- épicas;
- features;
- historias de usuario;
- tareas técnicas;
- subtareas;
- bugs;
- spikes;
- dependencias.

Ejemplo de historia:

```markdown
## US-001 — Validar documentación precontractual

Como usuario de negocio,
quiero que el sistema valide la existencia de la documentación precontractual obligatoria,
para evitar la emisión de pólizas incompletas.

### Criterios de aceptación
- CA-001: Si falta la documentación obligatoria, el sistema debe bloquear la emisión.
- CA-002: Si la documentación está completa, el sistema debe permitir continuar.
- CA-003: El sistema debe mostrar un mensaje claro indicando qué documento falta.
```

---

### 6.3. Escenarios BDD

Los escenarios BDD permiten expresar el comportamiento esperado de forma clara.

```gherkin
Feature: Validación de documentación precontractual

Scenario: Bloqueo de emisión por falta de documentación obligatoria
  Given que existe una solicitud de seguro de empresa
  And falta la documentación precontractual obligatoria
  When el usuario intenta emitir la póliza
  Then el sistema bloquea la emisión
  And muestra un mensaje indicando la documentación pendiente
```

---

### 6.4. Casos de prueba

Los casos de prueba pueden derivarse de los criterios de aceptación y escenarios BDD.

| ID | Requisito | Escenario | Resultado esperado |
|---|---|---|---|
| TC-001 | REQ-001 | Falta documentación obligatoria | El sistema bloquea la emisión |
| TC-002 | REQ-001 | Documentación completa | El sistema permite emitir |
| TC-003 | REQ-001 | Documento incorrecto | El sistema informa del error |

---

### 6.5. Open points

Los open points son dudas, decisiones pendientes o información incompleta.

Ejemplo:

| ID | Descripción | Responsable | Estado | Impacto |
|---|---|---|---|---|
| OP-001 | Confirmar si la validación aplica a todos los productos o solo a LC Empresas | Negocio | Abierto | Alto |
| OP-002 | Confirmar literal del mensaje de error | UX / Negocio | Pendiente | Medio |

---

## 7. Cómo usar IA en cada fase de SDD

### 7.1. Captura inicial

La IA puede ayudar a transformar notas, actas, correos o documentos iniciales en una primera estructura funcional.

Prompt ejemplo:

```text
Analiza el siguiente texto de negocio y extrae:
- requisitos funcionales;
- reglas de negocio;
- restricciones;
- dependencias;
- dudas abiertas;
- posibles criterios de aceptación.
Devuelve el resultado en formato Markdown con identificadores únicos.
```

---

### 7.2. Revisión de ambigüedades

Prompt ejemplo:

```text
Revisa esta especificación funcional e identifica:
- ambigüedades;
- contradicciones;
- requisitos incompletos;
- reglas no verificables;
- casos límite no tratados;
- preguntas que deberían trasladarse a negocio.
```

---

### 7.3. Generación de backlog

Prompt ejemplo:

```text
A partir de esta especificación, genera un backlog Jira con:
- épicas;
- historias de usuario;
- criterios de aceptación;
- tareas técnicas sugeridas;
- dependencias;
- prioridad funcional.
Mantén la trazabilidad con los requisitos originales.
```

---

### 7.4. Generación de casos de prueba

Prompt ejemplo:

```text
A partir de los requisitos y criterios de aceptación, genera casos de prueba funcionales con:
- ID;
- requisito asociado;
- precondiciones;
- pasos;
- datos de prueba;
- resultado esperado;
- prioridad;
- tipo de prueba.
```

---

### 7.5. Control de calidad

Prompt ejemplo:

```text
Actúa como revisor funcional senior.
Comprueba si existe trazabilidad completa entre requisitos, historias, criterios de aceptación y casos de prueba.
Indica qué elementos están cubiertos, parcialmente cubiertos o sin cubrir.
```

---

## 8. Estructura recomendada de repositorio SDD

Una estructura sencilla podría ser:

```text
/sdd-project
│
├── README.md
├── 00_contexto/
│   ├── vision.md
│   ├── alcance.md
│   └── glosario.md
│
├── 01_requisitos/
│   ├── requisitos_funcionales.md
│   ├── reglas_negocio.md
│   └── open_points.md
│
├── 02_especificacion/
│   ├── especificacion_funcional.md
│   ├── flujos.md
│   └── validaciones.md
│
├── 03_backlog/
│   ├── epicas.md
│   ├── historias_usuario.md
│   └── tareas_tecnicas.md
│
├── 04_bdd/
│   └── escenarios_bdd.feature
│
├── 05_testing/
│   ├── casos_prueba.md
│   └── matriz_cobertura.md
│
├── 06_trazabilidad/
│   └── matriz_trazabilidad.md
│
├── 07_prompts/
│   ├── generar_requisitos.md
│   ├── revisar_especificacion.md
│   ├── generar_backlog.md
│   └── generar_tests.md
│
└── 08_skills/
    ├── analista_funcional/SKILL.md
    ├── generador_bdd/SKILL.md
    └── revisor_trazabilidad/SKILL.md
```

---

## 9. Plantilla mínima de especificación SDD

```markdown
# Especificación funcional — [Nombre del cambio]

## 1. Contexto

## 2. Objetivo

## 3. Alcance

## 4. Fuera de alcance

## 5. Actores

## 6. Sistemas afectados

## 7. Requisitos funcionales

### REQ-001 — [Título]

#### Descripción

#### Reglas de negocio asociadas

#### Criterios de aceptación

#### Casos límite

#### Dependencias

#### Open points

## 8. Requisitos no funcionales

## 9. Flujos funcionales

## 10. Validaciones

## 11. Mensajes de error

## 12. Trazabilidad

## 13. Casos de prueba derivados

## 14. Anexos
```

---

## 10. Ventajas de SDD

### 10.1. Para negocio

- Mayor claridad sobre lo que se va a construir.
- Menos ambigüedad.
- Mejor validación temprana.
- Trazabilidad entre necesidad y solución.
- Documentación más comprensible.

### 10.2. Para análisis funcional

- Mejor estructura de requisitos.
- Menos pérdida de conocimiento.
- Reutilización de plantillas y criterios.
- Mayor capacidad de revisión con IA.
- Mejor control de open points.

### 10.3. Para desarrollo

- Historias más claras.
- Menos idas y vueltas.
- Mejor definición de reglas y casos límite.
- Mayor alineamiento con QA.
- Posibilidad de generar tareas técnicas desde especificaciones.

### 10.4. Para QA

- Casos de prueba derivados desde requisitos.
- Mayor cobertura funcional.
- Mejor trazabilidad.
- Escenarios BDD reutilizables.
- Detección temprana de huecos.

### 10.5. Para gestión

- Mejor visibilidad del alcance.
- Mejor control de cambios.
- Mejor seguimiento de dependencias.
- Evidencias más claras.
- Mayor capacidad de auditoría.

---

## 11. Riesgos y errores frecuentes

### 11.1. Convertir SDD en burocracia

SDD no consiste en escribir documentos enormes, sino en escribir especificaciones útiles, claras y accionables.

### 11.2. Delegar todo en la IA

La IA puede ayudar, pero no sustituye la validación humana.

Especialmente en sectores regulados, la revisión de negocio, arquitectura, seguridad, legal y QA sigue siendo necesaria.

### 11.3. No versionar la especificación

Si la especificación cambia y no queda trazabilidad, se pierde el valor del enfoque.

### 11.4. No cerrar open points

Los open points deben gestionarse como elementos vivos, no como una lista olvidada al final del documento.

### 11.5. No conectar con herramientas reales

SDD gana valor cuando se conecta con Jira, Confluence, GitHub, GitLab, Azure DevOps, HPQC/ALM u otras herramientas corporativas.

---

## 12. SDD aplicado a una modificación de aplicación existente

En proyectos donde se comercializan nuevos productos sobre una aplicación ya existente, SDD es especialmente útil.

El motivo es que el problema no suele ser construir todo desde cero, sino entender qué piezas existentes se reutilizan, qué reglas cambian, qué parametrizaciones se añaden y qué impactos laterales pueden aparecer.

En este contexto, la especificación debe distinguir claramente entre:

- comportamiento existente;
- comportamiento nuevo;
- comportamiento modificado;
- comportamiento eliminado;
- parametrización;
- reglas heredadas;
- impactos en otros módulos;
- dependencias con proyectos paralelos;
- pruebas de regresión necesarias.

Ejemplo de estructura:

| Elemento | Situación actual | Cambio propuesto | Impacto | Pruebas necesarias |
|---|---|---|---|---|
| Segmento comercial | Solo particulares | Añadir empresas | Alto | Pruebas de cotización y emisión |
| Documentación | Validación genérica | Validación específica por producto | Medio | Pruebas de bloqueo y mensajes |
| Firmantes | Un firmante principal | Múltiples firmantes | Alto | Pruebas de generación documental |

---

## 13. SDD y repositorio de conocimiento interno

Un modelo SDD bien diseñado permite construir un repositorio de conocimiento reutilizable.

Este repositorio puede contener:

- plantillas de especificación;
- criterios de aceptación tipo;
- prompts validados;
- skills de IA internas;
- checklists de revisión;
- patrones funcionales;
- modelos de trazabilidad;
- ejemplos de buenas especificaciones;
- catálogos de reglas de negocio;
- convenciones de Jira;
- formatos de casos de prueba;
- guías de revisión.

Este conocimiento puede diferenciar entre:

- **entregables del cliente**, que son los documentos, historias, pruebas o evidencias contractualmente requeridas;
- **know-how interno**, que son las plantillas, prompts, skills, procesos, automatizaciones y métodos propios usados para producir esos entregables.

La separación es importante para proteger la capacidad metodológica de la organización sin dejar de entregar al cliente la documentación acordada.

---

## 14. Relación entre SDD y skills de IA

Una skill de IA puede entenderse como una capacidad especializada que ayuda a ejecutar una tarea concreta dentro del proceso SDD.

Ejemplos:

| Skill | Función |
|---|---|
| Analista funcional | Extraer requisitos, reglas y dudas desde documentos de negocio |
| Revisor de ambigüedades | Detectar huecos, contradicciones y requisitos no verificables |
| Generador de historias Jira | Transformar requisitos en épicas, historias y tareas |
| Generador BDD | Crear escenarios Given/When/Then |
| Generador de casos de prueba | Crear casos de prueba funcionales trazables |
| Revisor de trazabilidad | Verificar cobertura entre requisitos, historias y pruebas |
| Preparador de entregables | Generar documentación final para cliente o comités |

Ejemplo de estructura simple de `SKILL.md`:

```markdown
# Skill: Revisor de trazabilidad funcional

## Objetivo
Comprobar que todos los requisitos funcionales tienen cobertura en historias, criterios de aceptación y casos de prueba.

## Entradas esperadas
- Documento de requisitos.
- Backlog de historias.
- Criterios de aceptación.
- Casos de prueba.

## Salida esperada
- Matriz de cobertura.
- Requisitos sin cubrir.
- Requisitos parcialmente cubiertos.
- Recomendaciones de corrección.

## Reglas
- No inventar requisitos.
- Mantener los identificadores originales.
- Señalar cualquier ambigüedad como open point.
```

---

## 15. Modelo operativo recomendado

Un modelo operativo SDD con IA podría organizarse en estos roles:

| Rol | Responsabilidad |
|---|---|
| Negocio | Define necesidad, valida reglas y resuelve dudas |
| Analista funcional | Estructura requisitos, reglas, flujos y criterios |
| Arquitectura | Revisa impactos técnicos y restricciones |
| Desarrollo | Estima, implementa y propone tareas técnicas |
| QA | Define y ejecuta estrategia de pruebas |
| IA | Ayuda a generar, revisar, transformar y validar artefactos |
| PM / Scrum Master | Gestiona alcance, dependencias, planificación y seguimiento |

La IA no aparece como sustituto de un rol, sino como una capacidad transversal.

---

## 16. Checklist de calidad SDD

Antes de considerar una especificación lista para derivar backlog y pruebas, conviene revisar:

- ¿El objetivo está claro?
- ¿El alcance está delimitado?
- ¿El fuera de alcance está documentado?
- ¿Los actores están identificados?
- ¿Los sistemas afectados están claros?
- ¿Cada requisito tiene identificador único?
- ¿Cada requisito tiene reglas de negocio asociadas?
- ¿Cada requisito tiene criterios de aceptación?
- ¿Los casos límite están contemplados?
- ¿Las dependencias están documentadas?
- ¿Los open points tienen responsable?
- ¿Los requisitos son verificables?
- ¿Existe trazabilidad con historias?
- ¿Existe trazabilidad con casos de prueba?
- ¿La documentación está versionada?
- ¿La IA ha sido usada como apoyo, pero revisada por una persona responsable?

---

## 17. Ejemplo de prompt maestro para SDD

```text
Actúa como analista funcional senior experto en Spec-Driven Development.

Voy a proporcionarte información de negocio sobre una modificación en una aplicación existente.

Tu tarea es generar una especificación funcional estructurada que sea legible por humanos y procesable por IA.

Debes devolver:

1. Contexto del cambio.
2. Objetivo.
3. Alcance.
4. Fuera de alcance.
5. Actores.
6. Sistemas afectados.
7. Requisitos funcionales con identificador único.
8. Reglas de negocio.
9. Validaciones.
10. Casos límite.
11. Criterios de aceptación.
12. Escenarios BDD.
13. Casos de prueba sugeridos.
14. Open points.
15. Matriz de trazabilidad.

Reglas:
- No inventes información no presente.
- Si algo no está claro, márcalo como open point.
- Mantén una redacción formal.
- Usa tablas cuando ayuden a la trazabilidad.
- Mantén identificadores estables.
- Distingue entre comportamiento existente, nuevo y modificado.
```

---

## 18. Conclusión

Spec-Driven Development es especialmente útil cuando se combina con IA generativa, porque transforma la especificación en una base viva desde la que se pueden generar, revisar y conectar todos los artefactos del ciclo de vida del software.

Para proyectos de modificación de aplicaciones existentes, como la incorporación de nuevos productos de seguros sobre una plataforma ya operativa, SDD permite controlar mejor el impacto, separar comportamiento existente y nuevo, reducir ambigüedad y mejorar la trazabilidad.

La clave es no verlo como una metodología documental pesada, sino como un modelo operativo basado en especificaciones claras, estructuradas, versionadas y reutilizables.

Bien aplicado, SDD puede convertirse en una ventaja diferencial: mejora la calidad del análisis, reduce retrabajos, facilita el uso de IA y permite construir un repositorio interno de conocimiento reutilizable.
