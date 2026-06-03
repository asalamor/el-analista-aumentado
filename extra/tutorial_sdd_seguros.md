# Tutorial SDD para evolucionar una aplicación de seguros existente

## Introducción

Este documento explica cómo aplicar **SDD —Specification-Driven Development—** a un proyecto en el que se va a modificar una aplicación de seguros existente para comercializar nuevos productos.

La idea central de SDD es que la **especificación sea la fuente de verdad**: antes de tocar código, se define con precisión qué debe cambiar, qué no debe cambiar, qué reglas de negocio aplican, qué impactos existen, cómo se verificará y qué trazabilidad habrá desde requisito hasta pruebas y despliegue.

Este enfoque encaja especialmente bien en dominios regulados o con necesidad de auditoría, como seguros, porque facilita la trazabilidad entre requisitos, implementación y verificación.

---

## 1. Cambie el enfoque: no está “haciendo una aplicación”, está modificando un sistema vivo

En este caso, el error típico sería tratar los nuevos productos como “pequeños cambios” y empezar directamente con historias de usuario o tareas técnicas.

Con SDD debería plantearlo al revés:

> “Vamos a introducir nuevos productos de seguros en una aplicación existente, preservando el comportamiento actual salvo en los puntos explícitamente especificados.”

Esta frase es importante porque en SDD no solo se documenta **lo nuevo**, sino también:

- qué comportamiento existente debe mantenerse;
- qué pantallas, procesos, servicios, reglas o documentos cambian;
- qué productos antiguos no deben verse afectados;
- qué reglas son parametrización y cuáles requieren desarrollo;
- qué pruebas de no regresión son obligatorias;
- qué trazabilidad se necesita para auditoría, QA, negocio y producción.

En aplicaciones de seguros esto es clave, porque un “pequeño ajuste” puede impactar en cotización, emisión, documentación precontractual, validaciones, firma, cumplimiento normativo, pricing, reporting o integraciones.

---

## 2. Defina el alcance con una matriz “Producto / Proceso / Impacto”

Antes de escribir historias de usuario, cree una matriz de impacto funcional. Esta será el primer artefacto SDD.

| Área | Producto actual | Nuevo producto | ¿Cambia? | Tipo de cambio |
|---|---:|---:|---|---|
| Alta de simulación | Sí | Sí | Sí | Nuevos campos / reglas |
| Cotización | Sí | Sí | Sí | Nueva tarifa o variante |
| Validaciones | Sí | Sí | Sí | Reglas específicas |
| Documentación precontractual | Sí | Sí | Sí | Nuevos textos/documentos |
| Firma | Sí | Sí | Quizá | Condiciones por producto |
| Emisión | Sí | Sí | Sí | Nuevos controles |
| Postproceso | Sí | Sí | Sí | Reporting / documentación |
| Reporting DWH | Sí | Sí | Quizá | Nuevos códigos |
| Producto antiguo | Sí | Sí | No debería | No regresión |

Esta matriz evita uno de los mayores riesgos: que negocio diga “solo es un nuevo producto”, pero tecnología descubra tarde que afecta a múltiples módulos.

---

## 3. Cree una especificación principal del cambio

En SDD, la especificación debe ser estructurada, versionable y trazable. Puede estar en Markdown dentro del repositorio, por ejemplo:

```text
/specs/
  000_contexto.md
  001_alcance_producto.md
  002_reglas_negocio.md
  003_impacto_aplicacion_existente.md
  004_casos_uso.md
  005_criterios_aceptacion.md
  006_trazabilidad.md
  007_plan_pruebas.md
```

La especificación debe actuar como contrato entre negocio, análisis funcional, desarrollo, QA y despliegue.

---

## 4. Estructura recomendada de la especificación SDD

### 4.1. Contexto

```markdown
# Contexto

La aplicación actual permite la simulación, contratación y gestión de productos de seguros ya existentes.

El objetivo del cambio es permitir la comercialización de nuevos productos reutilizando la aplicación actual, introduciendo únicamente los ajustes funcionales, técnicos, documentales y de parametrización necesarios.

Principio rector:
Todo comportamiento actual debe mantenerse salvo que esta especificación indique explícitamente lo contrario.
```

Este principio es muy importante. En una aplicación existente, SDD debe proteger el comportamiento heredado.

### 4.2. Objetivo de negocio

```markdown
# Objetivo de negocio

Permitir la comercialización de los nuevos productos [PRODUCTO_A], [PRODUCTO_B] y [PRODUCTO_C] sobre la aplicación existente.

Los nuevos productos deberán poder:

- simularse;
- cotizarse;
- validarse;
- generar su documentación correspondiente;
- contratarse;
- emitirse;
- quedar trazados en sistemas posteriores.
```

### 4.3. Fuera de alcance

El “fuera de alcance” es tan importante como el alcance.

```markdown
# Fuera de alcance

No forma parte de este cambio:

- rediseñar la aplicación completa;
- modificar el flujo general de contratación;
- alterar productos actualmente comercializados;
- cambiar el motor de pricing salvo en las reglas indicadas;
- modificar integraciones no afectadas por los nuevos productos;
- cambiar la arquitectura base.
```

Esto reduce discusiones posteriores y protege el proyecto frente a ampliaciones informales.

---

## 5. Documente el comportamiento actual antes de definir el nuevo

Como no se parte de cero, necesita una fase de **baseline funcional**.

Es decir: antes de decir cómo será el nuevo producto, documente cómo funciona hoy el producto o flujo más parecido.

```markdown
# Baseline funcional actual

## Flujo actual de simulación

1. El usuario accede a la pantalla de simulación.
2. Selecciona producto.
3. Introduce datos del tomador.
4. Introduce datos del asegurado.
5. El sistema valida datos obligatorios.
6. El sistema calcula prima.
7. El sistema genera documentación precontractual.
8. El usuario puede continuar a contratación.

## Reglas actuales relevantes

- Si tomador = asegurado, se reutilizan los datos personales.
- Si tomador ≠ asegurado, se solicitan datos diferenciados.
- La documentación se genera según código de producto.
- Las validaciones dependen del segmento y modalidad.
```

Este baseline sirve para comparar:

| Elemento | Actual | Nuevo | Decisión |
|---|---|---|---|
| Pantalla de selección | Lista actual de productos | Añadir nuevos productos | Modificar catálogo |
| Datos tomador | Igual | Igual | Reutilizar |
| Datos asegurado | Igual | Igual con validación adicional | Ajustar regla |
| Cálculo prima | Motor actual | Nueva tarifa | Parametrización/desarrollo |
| Documentación | Plantillas actuales | Nuevas plantillas/textos | Ajustar generación |
| Emisión | Flujo actual | Mismo flujo con nuevo código | Reutilizar |

---

## 6. Clasifique cada cambio: parametrización, regla, pantalla, integración o documento

En seguros, muchos cambios no deberían ser “desarrollo puro”. Por eso conviene clasificar.

| ID | Cambio | Tipo | Requiere código | Requiere parametrización | Requiere QA |
|---|---|---|---|---|---|
| CHG-001 | Alta nuevo código de producto | Parametrización | No | Sí | Sí |
| CHG-002 | Nueva regla de validación de edad | Regla negocio | Sí | Quizá | Sí |
| CHG-003 | Nuevo texto en documentación | Documento | No/Sí | Sí | Sí |
| CHG-004 | Envío nuevo código a DWH | Integración | Sí | No | Sí |
| CHG-005 | Nuevo campo en pantalla | UI / Backend | Sí | No | Sí |

Esto ayuda a derivar tareas técnicas, estimar esfuerzo y evitar que todo se convierta en una historia genérica.

---

## 7. Use identificadores trazables desde el principio

Cada requisito debe tener un ID estable.

```markdown
REQ-PROD-001: El sistema deberá permitir seleccionar el nuevo producto "Seguro X" en el flujo de simulación.

REQ-PROD-002: El sistema deberá calcular la prima del nuevo producto aplicando la tarifa definida para la modalidad seleccionada.

REQ-VAL-001: El sistema deberá validar que la edad del asegurado esté dentro del rango permitido para el nuevo producto.

REQ-DOC-001: El sistema deberá generar la documentación precontractual específica del nuevo producto.

REQ-INT-001: El sistema deberá enviar a los sistemas posteriores el código de producto correspondiente.
```

La trazabilidad mediante identificadores únicos permite vincular requisito, diseño, desarrollo, prueba y entrega.

---

## 8. Defina reglas de negocio en formato tabular

Evite reglas ambiguas en párrafos largos. Para productos de seguros, use tablas.

**Reglas de elegibilidad**

| Regla | Condición | Resultado | Mensaje |
|---|---|---|---|
| REG-001 | Edad asegurado < 18 | Bloquear simulación | El asegurado debe ser mayor de edad |
| REG-002 | Edad asegurado > 70 | Bloquear simulación | Edad fuera del rango permitido |
| REG-003 | Modalidad = Premium y capital < 50.000 | Bloquear | Capital insuficiente para modalidad Premium |
| REG-004 | Tomador ≠ asegurado | Solicitar datos diferenciados | N/A |

Después vincule cada regla a requisitos:

```markdown
REG-001 satisface REQ-VAL-001
REG-002 satisface REQ-VAL-001
REG-003 satisface REQ-VAL-002
REG-004 satisface REQ-DAT-001
```

---

## 9. Especifique escenarios en estilo BDD dentro del SDD

SDD y BDD encajan muy bien. BDD permite expresar requisitos mediante escenarios en lenguaje semiestructurado comprensible para negocio, desarrollo y QA.

Ejemplo:

```gherkin
Feature: Simulación de nuevo producto de seguro

Scenario: Simulación correcta para un asegurado elegible
  Given que el usuario selecciona el producto "Seguro X"
  And introduce un asegurado de 45 años
  And selecciona la modalidad "Estándar"
  When solicita la simulación
  Then el sistema calcula la prima
  And muestra el resultado de la simulación
  And permite continuar a contratación
```

Escenario de validación:

```gherkin
Scenario: Bloqueo por edad no permitida
  Given que el usuario selecciona el producto "Seguro X"
  And introduce un asegurado de 75 años
  When solicita la simulación
  Then el sistema bloquea la simulación
  And muestra el mensaje "Edad fuera del rango permitido"
```

Escenario de no regresión:

```gherkin
Scenario: Producto existente no se ve afectado
  Given que el usuario selecciona un producto ya existente
  When realiza una simulación con datos válidos
  Then el sistema mantiene el comportamiento previo
  And calcula la prima según las reglas actuales
  And genera la documentación actual
```

Este último tipo de escenario es esencial cuando se modifica una aplicación existente.

---

## 10. Añada una sección específica de “no regresión”

En proyectos de evolución, SDD debe proteger lo que ya funciona.

```markdown
# Requisitos de no regresión

NOREG-001: Los productos existentes deberán seguir apareciendo con los mismos códigos, descripciones y modalidades actuales.

NOREG-002: Las reglas de validación de productos existentes no deberán modificarse.

NOREG-003: La documentación de productos existentes no deberá cambiar salvo indicación expresa.

NOREG-004: Las integraciones actuales deberán recibir los mismos valores para productos existentes.

NOREG-005: Los procesos batch, reporting y postprocesos deberán mantener el comportamiento actual para productos existentes.
```

Y después:

**Pruebas de no regresión obligatorias**

| ID | Caso | Producto | Resultado esperado |
|---|---|---|---|
| T-NR-001 | Simulación producto actual | Producto A | Prima igual a baseline |
| T-NR-002 | Contratación producto actual | Producto A | Contrato emitido |
| T-NR-003 | Documentación producto actual | Producto A | Documento sin cambios |
| T-NR-004 | Envío a DWH | Producto A | Mismos códigos actuales |

---

## 11. Cree una matriz de trazabilidad

Este es uno de los artefactos más importantes de SDD.

**Matriz de trazabilidad**

| Requisito | Regla | Historia Jira | Tarea técnica | Caso de prueba | Estado |
|---|---|---|---|---|---|
| REQ-PROD-001 | N/A | US-001 | TASK-001 | TC-001 | Pendiente |
| REQ-VAL-001 | REG-001, REG-002 | US-002 | TASK-002 | TC-002, TC-003 | Pendiente |
| REQ-DOC-001 | REG-DOC-001 | US-003 | TASK-003 | TC-004 | Pendiente |
| REQ-INT-001 | REG-INT-001 | US-004 | TASK-004 | TC-005 | Pendiente |
| NOREG-001 | N/A | US-005 | TASK-005 | TC-NR-001 | Pendiente |

El objetivo no es burocracia. El objetivo es poder responder rápidamente:

- ¿Qué requisito justifica esta línea de trabajo?
- ¿Qué prueba demuestra que está terminado?
- ¿Qué producto queda afectado?
- ¿Qué parte de la aplicación se ha tocado?
- ¿Qué riesgo de regresión existe?
- ¿Qué evidencia se puede entregar a negocio, QA o auditoría?

---

## 12. Transforme la especificación en historias de usuario

Una vez definida la especificación, entonces sí puede generar historias Jira.

```markdown
# US-001 - Selección de nuevo producto en simulación

Como usuario comercial,
quiero poder seleccionar el nuevo producto "Seguro X" en la pantalla de simulación,
para poder iniciar una simulación del nuevo producto.

## Requisitos relacionados

- REQ-PROD-001

## Criterios de aceptación

CA-001: El producto "Seguro X" aparece en la lista de productos disponibles.
CA-002: El producto aparece únicamente para los canales autorizados.
CA-003: Al seleccionar el producto, el sistema carga las modalidades correspondientes.
CA-004: Los productos existentes siguen apareciendo sin cambios.

## Casos de prueba relacionados

- TC-001
- TC-NR-001
```

Otra historia:

```markdown
# US-002 - Validación de elegibilidad del asegurado

Como sistema,
quiero validar la elegibilidad del asegurado para el nuevo producto,
para impedir simulaciones no permitidas.

## Requisitos relacionados

- REQ-VAL-001

## Reglas relacionadas

- REG-001
- REG-002

## Criterios de aceptación

CA-001: Si la edad del asegurado es inferior al mínimo permitido, se bloquea la simulación.
CA-002: Si la edad supera el máximo permitido, se bloquea la simulación.
CA-003: Si la edad está dentro del rango permitido, se permite continuar.
CA-004: El mensaje mostrado coincide con el definido en la especificación.
```

---

## 13. Separe “historia funcional” de “tarea técnica”

En SDD conviene evitar historias enormes como:

> “Adaptar la aplicación para el nuevo producto”.

Eso no es trazable ni verificable.

Mejor:

### Historia funcional

```markdown
US-003 - Generar documentación precontractual del nuevo producto
```

### Tareas técnicas derivadas

```markdown
TASK-003.1 - Añadir código documental del nuevo producto
TASK-003.2 - Incorporar plantilla documental
TASK-003.3 - Mapear variables de la simulación al documento
TASK-003.4 - Añadir pruebas unitarias de generación documental
TASK-003.5 - Añadir prueba de comparación documental
```

Cada tarea técnica debe apuntar a un requisito.

---

## 14. Defina contratos de entrada y salida

Para cada módulo afectado, documente contratos.

Ejemplo para cálculo:

```markdown
# Contrato de cálculo de prima

## Entrada

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| codigoProducto | String | Sí | Código del nuevo producto |
| modalidad | String | Sí | Modalidad seleccionada |
| edadAsegurado | Number | Sí | Edad del asegurado |
| capital | Number | Sí | Capital asegurado |
| canal | String | Sí | Canal de comercialización |

## Salida

| Campo | Tipo | Descripción |
|---|---|---|
| primaNeta | Decimal | Prima antes de impuestos |
| impuestos | Decimal | Importe de impuestos |
| primaTotal | Decimal | Prima final |
| mensajes | Array | Advertencias o bloqueos |
| codigoResultado | String | OK / KO |
```

Ejemplo para integración:

```markdown
# Contrato de integración con sistemas posteriores

| Campo | Origen | Destino | Regla |
|---|---|---|---|
| codigoProducto | Simulación | DWH | Nuevo código definido en catálogo |
| modalidad | Pantalla | DWH | Código homologado |
| primaTotal | Motor cálculo | DWH | Dos decimales |
| fechaEfecto | Contratación | DWH | Formato YYYY-MM-DD |
```

Esto reduce errores entre front, back, batch, DWH y documentación.

---

## 15. Defina decisiones explícitas

En proyectos de modificación de aplicaciones existentes, muchas decisiones quedan implícitas. En SDD deben quedar registradas.

```markdown
# Decisiones funcionales y técnicas

DEC-001: Los nuevos productos reutilizarán el flujo actual de simulación.
DEC-002: No se creará una pantalla nueva salvo que se identifique una incompatibilidad funcional.
DEC-003: Las reglas de elegibilidad se implementarán en el mismo componente de validación que los productos actuales.
DEC-004: Los textos documentales se gestionarán mediante parametrización cuando sea posible.
DEC-005: Los productos existentes no deberán modificar su comportamiento.
```

Esto es muy útil cuando semanas después alguien pregunta: “¿Por qué no hicimos una pantalla nueva?” o “¿Por qué esto va parametrizado y no por código?”.

---

## 16. Use IA, pero contra la especificación

SDD es especialmente útil cuando se usan asistentes de IA, porque la IA puede generar historias, tareas, pruebas o código solo si tiene una especificación clara.

Puede trabajar así:

### Prompt para generar historias desde la especificación

```text
Actúa como analista funcional senior de seguros.

A partir de la siguiente especificación SDD, genera historias de usuario Jira.

Reglas:
- Cada historia debe referenciar los requisitos REQ correspondientes.
- Cada historia debe incluir criterios de aceptación verificables.
- Cada historia debe indicar casos de prueba sugeridos.
- No inventes alcance no incluido en la especificación.
- Si detectas ambigüedades, crea una sección "Open Points".

Especificación:
[pegar especificación]
```

### Prompt para detectar huecos

```text
Actúa como revisor SDD.

Revisa esta especificación para una modificación de una aplicación de seguros existente.

Identifica:
- requisitos ambiguos;
- reglas de negocio incompletas;
- impactos no cubiertos;
- riesgos de regresión;
- integraciones afectadas;
- pruebas que faltan;
- decisiones que deberían documentarse;
- open points para negocio o arquitectura.

No propongas implementación todavía.
```

### Prompt para generar matriz de trazabilidad

```text
A partir de esta especificación, genera una matriz de trazabilidad con columnas:

- ID requisito
- Descripción
- Regla de negocio relacionada
- Historia Jira sugerida
- Tarea técnica sugerida
- Caso de prueba
- Tipo de prueba
- Riesgo de regresión
- Evidencia esperada

No inventes requisitos nuevos. Si falta información, márcala como pendiente.
```

---

## 17. Gestione Open Points como parte formal del SDD

No deje dudas en correos dispersos. Cree una sección o fichero:

```markdown
# Open Points

| ID | Pregunta | Área | Responsable | Estado | Decisión |
|---|---|---|---|---|---|
| OP-001 | ¿El nuevo producto estará disponible en todos los canales? | Negocio | Producto | Abierto | Pendiente |
| OP-002 | ¿La documentación requiere nuevo condicionado? | Legal/Cumplimiento | Cumplimiento | Abierto | Pendiente |
| OP-003 | ¿El código de producto ya existe en DWH? | Datos | Arquitectura | Abierto | Pendiente |
| OP-004 | ¿La tarifa se parametriza o requiere desarrollo? | Pricing/TI | Sistemas | Abierto | Pendiente |
```

Regla práctica:

> Ningún requisito afectado por un Open Point debería pasar a desarrollo sin decisión o hipótesis aprobada.

---

## 18. Cree un flujo de trabajo SDD adaptado a su proyecto

Flujo recomendado:

```text
1. Inventario funcional actual
   ↓
2. Matriz de impacto por producto/proceso
   ↓
3. Especificación SDD del cambio
   ↓
4. Revisión con negocio, arquitectura, QA, cumplimiento y sistemas
   ↓
5. Open Points y decisiones
   ↓
6. Historias Jira trazadas a requisitos
   ↓
7. Tareas técnicas trazadas a historias
   ↓
8. Casos de prueba trazados a requisitos
   ↓
9. Desarrollo
   ↓
10. Validación contra especificación
   ↓
11. Pruebas de regresión
   ↓
12. Evidencia de aceptación
   ↓
13. Despliegue controlado
```

---

## 19. Cómo saber si una especificación SDD está lista

Use esta checklist antes de pasar a desarrollo:

```markdown
# Checklist de preparación SDD

## Alcance
- [ ] El objetivo de negocio está claro.
- [ ] Los nuevos productos están identificados.
- [ ] El fuera de alcance está documentado.
- [ ] Los productos existentes protegidos están identificados.

## Aplicación existente
- [ ] Se ha documentado el flujo actual.
- [ ] Se han identificado módulos afectados.
- [ ] Se han identificado módulos no afectados.
- [ ] Se han definido pruebas de no regresión.

## Reglas
- [ ] Las reglas de elegibilidad están definidas.
- [ ] Las reglas de cálculo están definidas.
- [ ] Las reglas documentales están definidas.
- [ ] Las reglas de integración están definidas.

## Trazabilidad
- [ ] Cada requisito tiene ID.
- [ ] Cada historia apunta a requisitos.
- [ ] Cada tarea técnica apunta a historia/requisito.
- [ ] Cada prueba apunta a requisito.
- [ ] Los Open Points están identificados.

## Verificación
- [ ] Hay criterios de aceptación.
- [ ] Hay escenarios BDD.
- [ ] Hay casos de prueba funcionales.
- [ ] Hay casos de regresión.
- [ ] Hay evidencia esperada para aceptación.
```

---

## 20. Plantilla base que puede usar

```markdown
# SDD - Nuevos productos de seguros sobre aplicación existente

## 1. Contexto

[Describir aplicación actual, productos actuales y objetivo del cambio.]

## 2. Objetivo de negocio

[Describir qué nuevos productos se quieren comercializar y para qué.]

## 3. Principio rector

Todo comportamiento existente deberá mantenerse salvo que esta especificación indique explícitamente lo contrario.

## 4. Alcance

### Incluido

- [Nuevo producto 1]
- [Nuevo producto 2]
- [Proceso de simulación]
- [Proceso de contratación]
- [Documentación]
- [Integraciones afectadas]

### Fuera de alcance

- [Elementos no incluidos]

## 5. Baseline funcional actual

[Describir cómo funciona hoy el proceso equivalente.]

## 6. Matriz de impacto

| Área | Impacto | Descripción | Riesgo |
|---|---|---|---|

## 7. Requisitos

| ID | Descripción | Prioridad | Tipo |
|---|---|---|---|

## 8. Reglas de negocio

| ID | Condición | Resultado | Mensaje | Requisito |
|---|---|---|---|---|

## 9. Contratos de datos

### Entrada

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|

### Salida

| Campo | Tipo | Descripción |
|---|---|---|

## 10. Documentación

| Documento | Cambio | Producto | Responsable |
|---|---|---|---|

## 11. Integraciones

| Sistema | Campo | Cambio | Requisito |
|---|---|---|---|

## 12. Escenarios BDD

```gherkin
Scenario: [Nombre]
  Given ...
  When ...
  Then ...
```

## 13. No regresión

| ID | Caso | Producto existente | Resultado esperado |
|---|---|---|---|

## 14. Open Points

| ID | Pregunta | Responsable | Estado | Decisión |
|---|---|---|---|---|

## 15. Matriz de trazabilidad

| Requisito | Historia | Tarea | Prueba | Estado |
|---|---|---|---|---|

## 16. Criterios de aceptación globales

- [ ] Los nuevos productos pueden simularse.
- [ ] Los nuevos productos pueden contratarse.
- [ ] La documentación se genera correctamente.
- [ ] Las integraciones reciben los códigos esperados.
- [ ] Los productos existentes no se ven afectados.
```

---

## 21. Recomendación final para su caso

Para este proyecto, no empezaría escribiendo historias Jira directamente. Empezaría con estos cinco documentos mínimos:

```text
01_contexto_y_alcance.md
02_matriz_impacto_producto_proceso.md
03_reglas_negocio_y_validaciones.md
04_escenarios_bdd_y_no_regresion.md
05_trazabilidad_requisitos_jira_pruebas.md
```

Y seguiría esta regla:

> Si un cambio no aparece en la especificación SDD, no se desarrolla.  
> Si una prueba no está vinculada a un requisito, no demuestra aceptación.  
> Si un producto existente puede verse afectado, debe tener prueba de no regresión.

Ese es el verdadero valor de SDD en este caso: no convertir una modificación aparentemente pequeña en una cadena de impactos no controlados.

---

## Fuentes de referencia

- IBM Think: *Spec-driven development*.
- Augment Code: *What is Spec-Driven Development?*
- TestGrid: *Software Requirements Specification document*.
- arXiv: *Behaviour Driven Development: A systematic literature review*.
- Jama Software: *What is Spec-Driven Development for AI-powered engineering?*
