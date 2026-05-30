# Capítulo 4. El requisito AI-ready

---

*En este capítulo aprenderás:*
- *Por qué el formato del requisito determina la calidad de todo lo que el pipeline genera a partir de él*
- *Qué son los cinco bloques de la plantilla AI-ready y qué propósito cumple cada uno*
- *Cuáles son los campos obligatorios, cuáles son opcionales y por qué esa distinción importa*
- *Cómo transformar un requisito tradicional en uno AI-ready, con ejemplos del módulo de Facturación de Meridian*

---

## El contrato de datos

Cuando Carlos Ruiz se sienta a diseñar la plantilla de requisitos para Meridian, el primer error que comete es el mismo que cometen casi todos los analistas que pasan por este ejercicio por primera vez: diseña el formulario pensando en quién lo va a rellenar.

Piensa en Ana López, que necesita un formato comprensible sin jerga técnica. Piensa en los desarrolladores, que necesitan suficiente detalle para implementar sin adivinar. Piensa en sí mismo, que necesita una guía que le recuerde qué información capturar en la reunión sin que sea tan rígida que encorsete conversaciones que necesitan fluir.

Todo eso es correcto. Y todo eso es insuficiente.

Lo que Carlos tarda en entender es que la plantilla no es un formulario. Es un **contrato de datos** entre tres partes con necesidades distintas y ninguna disposición a leer el manual del otro: el usuario de negocio, que habla en lenguaje natural; el equipo técnico, que habla en código; y la IA, que solo puede procesar lo que está explícitamente escrito.

El diseño del formulario pensando solo en quien lo rellena produce plantillas que son cómodas de completar y difíciles de procesar automáticamente. El diseño pensando solo en la IA produce plantillas que generan outputs de calidad y que nadie del equipo quiere usar. El diseño correcto satisface a las tres audiencias simultáneamente, y lo hace asignando a cada bloque de la plantilla una responsabilidad distinta.

Eso es lo que hace la plantilla de cinco bloques.

> 💡 **Idea clave**
>
> La plantilla AI-ready no es un formulario para capturar información. Es un contrato de datos que define exactamente qué información debe estar presente, en qué formato y con qué nivel de precisión para que el pipeline pueda transformarla en artefactos correctos. Cada campo tiene un coste de mantenimiento y un beneficio en calidad del output. Si el beneficio no justifica el coste, el campo no debería estar.

---

## Los cinco bloques

La plantilla tiene cinco bloques. Cada bloque tiene una responsabilidad distinta y es procesado de forma diferente por el pipeline. Entender la responsabilidad de cada bloque es más importante que memorizar sus campos: es lo que permite adaptar la plantilla al contexto específico de tu organización sin romper la lógica que hace funcionar el sistema.

```
┌─────────────────────────────────────────────────────────────┐
│              PLANTILLA AI-READY — CINCO BLOQUES             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BLOQUE 1 — IDENTIDAD                                       │
│  Identifica, versiona y enruta el requisito                 │
│  Campos: id, título, versión, estado, épica, origen         │
│                         │                                   │
│                         ▼                                   │
│  BLOQUE 2 — CONTEXTO DE NEGOCIO                             │
│  Da a la IA el "por qué" para generar historias con         │
│  valor de negocio real, no solo técnicas                    │
│  Campos: actor, evento disparador, objetivo, descripción,   │
│  prioridad, reglas de negocio, dependencias                 │
│                         │                                   │
│                         ▼                                   │
│  BLOQUE 3 — COMPORTAMIENTO ESPERADO                         │
│  Define qué debe hacer el sistema de forma verificable      │
│  Fuente principal de test cases                             │
│  Campos: flujo principal, flujos alternativos,              │
│  excepciones, criterios de aceptación, DoD                  │
│                         │                                   │
│                         ▼                                   │
│  BLOQUE 4 — DATOS                                           │
│  Especifica la forma de los datos para generar              │
│  casos de contorno correctos                                │
│  Campos: datos de entrada, datos de salida                  │
│                         │                                   │
│                         ▼                                   │
│  BLOQUE 5 — METADATOS TÉCNICOS                              │
│  Contexto para el equipo técnico y para la IA               │
│  Lo completa el equipo en el refinamiento, no el analista   │
│  Campos: componentes, integraciones, NFRs, trazabilidad     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Bloque 1 — Identidad

El bloque de identidad tiene una sola responsabilidad: hacer que el requisito sea localizable, versionable y enrutable dentro del sistema. La IA lo usa para construir la matriz de trazabilidad, para detectar cuándo un requisito ha cambiado y qué artefactos hay que regenerar, y para vincular la historia generada a la épica correcta en Jira.

Los campos de este bloque son los más mecánicos de la plantilla y los que el analista tarda menos en rellenar. Son también los que más impacto tienen en la coherencia del sistema a largo plazo: un ID que se reutiliza, un título ambiguo o una épica incorrecta generan errores de trazabilidad que son muy costosos de corregir cuando el repositorio ya tiene cientos de requisitos.

**Campos del Bloque 1:**

| Campo | Obligatorio | Descripción | Ejemplo |
|---|---|---|---|
| `id` | ★ Sí | Identificador único y estable. Nunca reutilizar aunque el requisito se elimine. | `REQ-023` |
| `titulo` | ★ Sí | Una frase, máximo 80 caracteres, sin verbos ambiguos. Empieza por sustantivo o verbo en infinitivo. | `Filtrar facturas por rango de fechas` |
| `version` | Sí | Incrementar el menor (1.1) para cambios menores, el mayor (2.0) si cambia el comportamiento. | `1.0` |
| `estado` | ★ Sí | Vocabulario controlado: borrador, en-revision, validado, rechazado, deprecado. | `validado` |
| `epica` | ★ Sí | ID de la épica a la que pertenece. Debe existir en el catálogo. | `EP-04` |
| `modulo` | No | Nombre legible del módulo. Para usuarios de negocio que no trabajan con IDs. | `Gestión de Facturación` |
| `origen` | Sí | Quién lo pidió, en qué área, cuándo y con qué referencia (ticket, acta). | Ver ejemplo |
| `analista` | No | Nombre del analista responsable. | `Carlos Ruiz` |
| `fecha_validacion` | No | Fecha en que se aprobó. Se rellena al mover a estado `validado`. | `2025-05-15` |

La regla más importante de este bloque es la del `titulo`: sin verbos ambiguos. La lista de verbos prohibidos en un título no es arbitraria. Cada uno de ellos genera un defecto específico en el output del pipeline.

| ❌ Título con verbo ambiguo | Problema que genera | ✅ Título correcto |
|---|---|---|
| Gestionar facturas | "Gestionar" no especifica qué operación. La IA genera una historia que mezcla filtrado, exportación y archivado en una sola. | Filtrar facturas por rango de fechas |
| Permitir la exportación de datos | "Permitir" es pasivo y vago. La historia generada describe un permiso, no una funcionalidad. | Exportar facturas filtradas a formato CSV |
| Mejorar el rendimiento del módulo | "Mejorar" no especifica qué, ni cuánto, ni bajo qué condiciones. | Reducir el tiempo de carga del listado de facturas a menos de 2 segundos |
| Administrar usuarios del sistema | "Administrar" agrupa alta, baja, modificación y consulta. Son cuatro requisitos distintos. | Dar de alta un usuario con rol y permisos |

> ⚠️ **Error frecuente**
>
> El error más habitual en el `titulo` es heredar el lenguaje de los documentos Word anteriores, donde un título como "Gestión de facturas" encabezaba un documento de diez páginas. En la plantilla AI-ready, el título es una descripción atómica de una única funcionalidad. Si el título necesita la palabra "y" para describir lo que hace, probablemente hay dos requisitos disfrazados de uno.

---

## Bloque 2 — Contexto de negocio

El bloque de contexto es el que diferencia un requisito AI-ready de un formulario técnico. Contiene el "por qué" del requisito: el problema de negocio que resuelve, quién lo tiene, cuándo ocurre y qué reglas lo gobiernan.

La IA usa este bloque para dos cosas que marcan la diferencia entre una historia genérica y una historia con valor de negocio real. Primero, para generar el campo "para [beneficio]" de la narrativa de usuario con algo concreto y medible en lugar de una frase vacía. Segundo, para priorizar qué flujos son más importantes en la descomposición en tareas técnicas.

Sin este bloque bien rellenado, el pipeline genera historias sintácticamente correctas pero semánticamente huecas: "Como gestor de facturación, quiero filtrar facturas para poder hacerlo". Con el bloque bien rellenado, genera: "Como gestor de facturación, quiero filtrar facturas por rango de fechas para reducir el tiempo de búsqueda manual durante el cierre mensual de 30 minutos a menos de 2 minutos".

**Campos del Bloque 2:**

| Campo | Obligatorio | Descripción |
|---|---|---|
| `actor` | ★ Sí | El rol específico que ejecuta la acción principal. Debe existir en el glosario. Nunca "el usuario" o "el cliente". |
| `actores_secundarios` | No | Roles que intervienen pero no son el actor principal. |
| `evento_disparador` | ★ Sí | Qué situación concreta activa este requisito. No "cuando el usuario lo necesita". |
| `objetivo_negocio` | Recomendado | Por qué existe este requisito. Qué problema de negocio resuelve. Mínimo 20 palabras. |
| `descripcion` | ★ Sí | Narrativa del requisito en lenguaje de negocio. Mínimo 30 palabras. Sin tecnicismos. |
| `prioridad` | ★ Sí | MoSCoW: must-have, should-have, could-have, wont-have. Vocabulario controlado. |
| `reglas_negocio` | Recomendado | Lista de restricciones y condiciones. Cada regla debe ser una afirmación verificable. |
| `dependencias` | No | IDs de requisitos que deben implementarse antes, sistemas externos, decisiones pendientes. |

El campo más subestimado de este bloque es el `objetivo_negocio`. Cuando el analista lo rellena bien —con el problema concreto que resuelve el requisito, con datos si los hay—, el pipeline genera una historia cuyo campo "para qué" tiene suficiente información para que el desarrollador entienda qué está construyendo y por qué importa. Cuando se omite, la historia describe una funcionalidad sin contexto, y el desarrollador toma decisiones de implementación basadas en su criterio en lugar de en las necesidades del negocio.

El campo `reglas_negocio` merece una atención especial porque es el puente entre el bloque 2 y el bloque 3. Cada regla de negocio documentada aquí debe tener al menos un criterio de aceptación en el bloque 3 que la verifique. Si hay una regla sin criterio, el pipeline lo detectará en la validación como un gap de completitud: la regla existe en el papel pero nadie va a comprobar que se cumple.

> 🛠️ **En la práctica**
>
> La forma más eficaz de rellenar el `objetivo_negocio` es preguntarle al usuario de negocio: "Si este requisito no existiera, ¿cuánto tiempo se perdería en este proceso y quién lo perdería?" La respuesta suele ser un número concreto que es exactamente lo que necesita este campo. Ana López respondería: "El equipo de facturación tarda entre 20 y 30 minutos buscando facturas manualmente en cada cierre mensual. Son cuatro cierres al mes con tres personas implicadas. Cada minuto reducido ahorra tiempo real."

---

## Bloque 3 — Comportamiento esperado

Este es el bloque más importante de la plantilla para el pipeline de generación de test cases. Contiene la descripción precisa de qué debe hacer el sistema: el flujo principal (el camino feliz), los flujos alternativos (los desvíos previstos), las excepciones (los errores), y los criterios de aceptación en formato Dado/Cuando/Entonces.

La regla de oro del bloque 3 es que cada cosa que se describe aquí debe poder verificarse con una prueba concreta que produzca un resultado de verdadero o falso. Si algo no puede verificarse, no es un criterio de aceptación: es una aspiración, y las aspiraciones no generan test cases ejecutables.

**Campos del Bloque 3:**

| Campo | Obligatorio | Descripción |
|---|---|---|
| `flujo_principal` | Recomendado | El camino feliz paso a paso. Máximo 10 pasos. Actor + acción + resultado por cada uno. |
| `flujos_alternativos` | No | Desvíos previstos del flujo principal. Condición que los activa + pasos. |
| `excepciones` | ★ Sí | Qué ocurre cuando algo falla. Mínimo una excepción por campo obligatorio de entrada. |
| `criterios_aceptacion` | ★ Sí | Mínimo un criterio en formato Dado/Cuando/Entonces. Cada uno con ID único. |
| `definition_of_done` | Recomendado | Condiciones que deben cumplirse para cerrar la historia. |

### Los criterios de aceptación: cuatro reglas de oro

Los criterios de aceptación son el elemento más crítico de la plantilla para la generación automática de artefactos. Un criterio bien escrito genera un test case ejecutable directamente. Un criterio mal escrito genera un test case que parece correcto pero que no verifica nada concreto.

Estas son las cuatro reglas que todo criterio de aceptación debe cumplir:

**Regla 1: El `dado` describe un estado, no una acción.**

El `dado` establece las condiciones previas al momento en que el actor ejecuta la acción. Debe describir en qué situación está el sistema y el actor, no lo que han hecho para llegar ahí.

| ❌ Dado incorrecto | ✅ Dado correcto |
|---|---|
| Dado que el usuario ha hecho clic en el módulo Facturas | Dado que el usuario está autenticado con rol gestor_facturacion y se encuentra en la pantalla de listado de Facturas |
| Dado que el gestor ha introducido las fechas | Dado que el gestor tiene el campo fecha_inicio con valor 2024-01-01 y el campo fecha_fin con valor 2024-03-31 |

**Regla 2: El `cuando` describe una única acción concreta.**

El `cuando` es la acción que dispara el comportamiento que se quiere verificar. Debe ser una sola acción, ejecutada por un solo actor, en un solo paso.

| ❌ Cuando incorrecto | ✅ Cuando correcto |
|---|---|
| Cuando filtra, ordena y exporta los resultados | Cuando pulsa el botón Buscar |
| Cuando el usuario hace lo necesario para buscar | Cuando pulsa el botón Buscar con los campos de fecha rellenos |

**Regla 3: El `entonces` describe algo observable externamente.**

El resultado esperado debe ser algo que el tester pueda ver, medir o verificar sin conocimiento del funcionamiento interno del sistema.

| ❌ Entonces incorrecto | ✅ Entonces correcto |
|---|---|
| Entonces el sistema funciona correctamente | Entonces el listado muestra las facturas del período ordenadas por fecha descendente en menos de 2 segundos, y el contador indica el número total de resultados |
| Entonces el sistema procesa la solicitud | Entonces el campo fecha_inicio se resalta en rojo y aparece el mensaje: "El rango no puede superar 365 días" |

**Regla 4: Los datos son concretos, no placeholders.**

Un criterio con valores reales genera un test case ejecutable. Un criterio con placeholders genera un test case que el tester tiene que completar a mano, lo que elimina parte del valor de la generación automática.

| ❌ Datos como placeholder | ✅ Datos concretos |
|---|---|
| Cuando introduce una fecha de inicio válida | Cuando introduce fecha_inicio = 2024-01-01 |
| Si el rango es demasiado grande | Si fecha_fin - fecha_inicio = 366 días |

Aplicando estas cuatro reglas, los tres criterios de aceptación de REQ-023 quedan así:

```yaml
criterios_aceptacion:
  - id: AC-023-01
    titulo: "Filtrado válido devuelve resultados ordenados en tiempo"
    dado: >
      El gestor está autenticado con rol gestor_facturacion
      y se encuentra en la pantalla de listado de Facturas
    cuando: >
      Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31
      y pulsa el botón Buscar
    entonces: >
      El sistema devuelve las facturas del período en menos de 2 segundos,
      ordenadas por fecha descendente, mostrando el contador de resultados
    tipo: positivo
    datos_ejemplo:
      fecha_inicio: "2024-01-01"
      fecha_fin: "2024-03-31"
      registros_esperados_minimo: 5

  - id: AC-023-02
    titulo: "Rango superior a 365 días bloquea la búsqueda"
    dado: >
      El gestor está en la pantalla de listado de Facturas
    cuando: >
      Introduce fecha_inicio=2023-01-01 y fecha_fin=2024-01-02
      y pulsa el botón Buscar
    entonces: >
      El sistema no ejecuta la consulta, muestra el mensaje
      "El rango no puede superar 365 días" y resalta los campos
      de fecha en rojo
    tipo: negativo
    datos_ejemplo:
      fecha_inicio: "2023-01-01"
      fecha_fin: "2024-01-02"
      dias_diferencia: 366

  - id: AC-023-03
    titulo: "Búsqueda sin resultados muestra estado vacío con acción"
    dado: >
      El gestor está en la pantalla de listado de Facturas
      y no existen facturas en el período 2000-01-01 a 2000-01-31
    cuando: >
      Introduce fecha_inicio=2000-01-01 y fecha_fin=2000-01-31
      y pulsa el botón Buscar
    entonces: >
      El sistema muestra el texto "No se encontraron facturas
      para el período seleccionado" y el botón "Ampliar búsqueda"
    tipo: positivo
    datos_ejemplo:
      fecha_inicio: "2000-01-01"
      fecha_fin: "2000-01-31"
```

---

## Bloque 4 — Datos

El bloque de datos tiene una función específica que el bloque de comportamiento no puede cumplir: especificar la forma exacta de los datos que entran y salen del sistema. Tipos, formatos, rangos, longitudes máximas, valores permitidos en enumerados, valores por defecto.

La IA usa este bloque para generar los casos de contorno automáticamente. Si el bloque especifica que `fecha_inicio` es de tipo `date` con formato ISO-8601, el pipeline sabe que debe generar test cases con fechas en el límite del rango, con fechas en formato incorrecto, con fechas nulas, y con fechas posteriores a `fecha_fin`. Sin este bloque, esos casos de contorno no se generan porque el modelo no tiene información suficiente para saber qué constituye un valor límite.

**Campos del Bloque 4:**

```yaml
datos_entrada:
  - nombre: fecha_inicio
    tipo: date              # string | integer | decimal | boolean |
                            # date | datetime | enum | file | array | object
    requerido: true
    formato: ISO-8601       # Para fechas. Regex para patrones. Libre para otros.
    descripcion: "Fecha de inicio del rango de búsqueda"

  - nombre: fecha_fin
    tipo: date
    requerido: true
    formato: ISO-8601
    descripcion: "Fecha de fin del rango de búsqueda"

datos_salida:
  campos: [id_factura, fecha_factura, importe_total, estado, proveedor]
  formato: lista_paginada
  paginacion:
    aplica: true
    tamanyo_pagina_defecto: 20
    max_registros: 100
  orden_defecto: "fecha_factura DESC"
  tiempo_respuesta_max_ms: 2000
```

El campo `tiempo_respuesta_max_ms` en `datos_salida` merece atención especial. Es el único lugar de la plantilla donde se especifica un criterio de rendimiento de forma medible. Si este campo no está, el desarrollador implementará el rendimiento que le parezca razonable, que puede o no coincidir con lo que el negocio necesita. El validador detecta la ausencia de este campo como advertencia cuando el requisito tiene lógica de consulta o procesamiento de datos.

> ⚠️ **Error frecuente**
>
> La ausencia del bloque de datos es el gap más frecuente en los primeros requisitos que los equipos escriben con la plantilla. Parece redundante con el bloque de comportamiento y los analistas tienden a omitirlo. El coste de omitirlo aparece en la fase de testing: los test cases generados sin este bloque no incluyen casos de contorno de tipos de dato, y los bugs de validación que esos casos habrían detectado llegan a producción.

---

## Bloque 5 — Metadatos técnicos

El bloque de metadatos técnicos tiene una característica que lo distingue de los cuatro anteriores: **no lo rellena el analista funcional en el análisis**. Lo rellena el equipo técnico durante el refinamiento.

Esta separación es intencional. El analista funcional no siempre sabe qué componentes del sistema se ven afectados por un requisito, qué integraciones externas implica, o qué restricciones no funcionales de rendimiento, seguridad o disponibilidad aplican. Pedirle que rellene ese bloque en el análisis produce, en el mejor caso, estimaciones imprecisas. En el peor caso, produce compromisos técnicos que el equipo no puede cumplir.

El bloque existe en la plantilla desde el inicio para que el equipo técnico tenga dónde escribir esa información cuando llegue el refinamiento. Pero hasta ese momento, sus campos permanecen vacíos o con valores por defecto.

```yaml
componentes_afectados: []
  # El equipo técnico añade aquí los componentes del sistema
  # que requieren cambios. Ej: ["api-facturacion", "frontend-facturas"]

integraciones_externas: []
  # Sistemas externos con los que interactúa este requisito.

restricciones_no_funcionales:
  rendimiento: ""      # Ej: "< 2 segundos p95 con 100 usuarios concurrentes"
  seguridad: ""        # Ej: "Solo accesible con rol gestor_facturacion. Audit log."
  disponibilidad: ""
  accesibilidad: ""    # Ej: "WCAG 2.1 AA"

notas_implementacion: ""
  # Orientaciones técnicas no prescriptivas para el desarrollador.

trazabilidad:
  historias_generadas: []   # Auto-rellenado por el pipeline. No editar a mano.
  test_cases_generados: []  # Auto-rellenado por el pipeline. No editar a mano.
  jira_issues: []           # Auto-rellenado por el pipeline. No editar a mano.
```

El subbloques de `trazabilidad` merece una nota especial: sus campos son de solo lectura para el analista. Los rellena automáticamente el pipeline cuando genera los artefactos. Si el analista los edita a mano, rompe la coherencia del grafo de trazabilidad que describe el Capítulo 11.

---

## El requisito completo: REQ-023

Con los cinco bloques definidos, el YAML completo de REQ-023 tiene este aspecto. Este es el documento que Carlos envía a validación y que el pipeline procesará para generar los artefactos de FACT-47.

```yaml
# ─────────────────────────────────────────────
# BLOQUE 1 — IDENTIDAD
# ─────────────────────────────────────────────
id: REQ-023
titulo: "Filtrar facturas por rango de fechas"
version: "1.0"
estado: validado
epica: EP-04
modulo: "Gestión de Facturación"
origen:
  solicitante: "Ana López"
  area: "Dirección Financiera"
  fecha_solicitud: "2025-05-12"
  referencia: "Reunión cierre mensual — Acta 2025-05-12"
fecha_validacion: "2025-05-14"
analista: "Carlos Ruiz"

# ─────────────────────────────────────────────
# BLOQUE 2 — CONTEXTO DE NEGOCIO
# ─────────────────────────────────────────────
actor: "Gestor de facturación"
evento_disparador: >
  El gestor accede al módulo Facturas para preparar
  el cierre mensual y necesita localizar las facturas
  de un período contable concreto.
objetivo_negocio: >
  Reducir el tiempo de búsqueda manual de facturas durante
  el cierre mensual, actualmente de 20-30 minutos por cierre,
  a menos de 2 minutos. El equipo realiza cuatro cierres
  mensuales con tres personas implicadas.
descripcion: >
  El gestor de facturación necesita filtrar el listado de
  facturas por un rango de fechas para localizar rápidamente
  los documentos de un período contable y agilizar las tareas
  de revisión y exportación del cierre mensual.
prioridad: must-have
reglas_negocio:
  - "Solo se muestran facturas del ejercicio fiscal en curso (año natural)"
  - "El rango máximo de búsqueda es de 365 días"
  - "Los resultados se ordenan por fecha descendente por defecto"
dependencias:
  requisitos: []
  sistemas: []
  decisiones: []

# ─────────────────────────────────────────────
# BLOQUE 3 — COMPORTAMIENTO ESPERADO
# ─────────────────────────────────────────────
flujo_principal:
  - paso: 1
    actor: "Gestor de facturación"
    accion: "Accede al módulo Facturas"
    resultado: "Se carga el listado con el panel de filtros visible"
  - paso: 2
    actor: "Gestor de facturación"
    accion: "Introduce fecha_inicio y fecha_fin en los campos de filtro"
    resultado: "Los campos muestran las fechas seleccionadas"
  - paso: 3
    actor: "Gestor de facturación"
    accion: "Pulsa el botón Buscar"
    resultado: "Aparece indicador de carga"
  - paso: 4
    actor: sistema
    accion: "Ejecuta la consulta con los filtros"
    resultado: "Devuelve resultados en menos de 2 segundos"
  - paso: 5
    actor: "Gestor de facturación"
    accion: "Visualiza el listado paginado"
    resultado: "Ve las facturas del período ordenadas por fecha descendente con contador de resultados"

flujos_alternativos:
  - condicion: "El gestor no introduce fecha_fin"
    pasos:
      - paso: 1
        actor: sistema
        accion: "Usa la fecha actual como fecha_fin por defecto"
        resultado: "La búsqueda se ejecuta con fecha_fin = hoy"

excepciones:
  - condicion: "El rango de fechas supera 365 días"
    comportamiento: >
      El sistema no ejecuta la consulta. Muestra el mensaje
      "El rango no puede superar 365 días". Los campos de fecha
      se resaltan en rojo.
  - condicion: "No existen facturas en el período seleccionado"
    comportamiento: >
      El sistema muestra el estado vacío con el texto
      "No se encontraron facturas para el período seleccionado"
      y el botón "Ampliar búsqueda".
  - condicion: "La base de datos no responde en menos de 5 segundos"
    comportamiento: >
      El sistema muestra el mensaje "El servicio no está disponible
      temporalmente. Inténtelo de nuevo en unos minutos."
      con botón de reintento.

criterios_aceptacion:
  - id: AC-023-01
    titulo: "Filtrado válido devuelve resultados ordenados en tiempo"
    dado: >
      El gestor está autenticado con rol gestor_facturacion
      y se encuentra en la pantalla de listado de Facturas
    cuando: >
      Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31
      y pulsa el botón Buscar
    entonces: >
      El sistema devuelve las facturas del período en menos de 2 segundos,
      ordenadas por fecha descendente, mostrando el contador de resultados
    tipo: positivo
    datos_ejemplo:
      fecha_inicio: "2024-01-01"
      fecha_fin: "2024-03-31"

  - id: AC-023-02
    titulo: "Rango superior a 365 días bloquea la búsqueda"
    dado: "El gestor está en la pantalla de listado de Facturas"
    cuando: >
      Introduce fecha_inicio=2023-01-01 y fecha_fin=2024-01-02
      y pulsa el botón Buscar
    entonces: >
      El sistema no ejecuta la consulta, muestra el mensaje
      "El rango no puede superar 365 días" y resalta los campos
      de fecha en rojo
    tipo: negativo
    datos_ejemplo:
      fecha_inicio: "2023-01-01"
      fecha_fin: "2024-01-02"

  - id: AC-023-03
    titulo: "Búsqueda sin resultados muestra estado vacío con acción"
    dado: >
      El gestor está en la pantalla de listado de Facturas
      y no existen facturas entre 2000-01-01 y 2000-01-31
    cuando: >
      Introduce fecha_inicio=2000-01-01 y fecha_fin=2000-01-31
      y pulsa el botón Buscar
    entonces: >
      El sistema muestra "No se encontraron facturas para el período
      seleccionado" y el botón "Ampliar búsqueda"
    tipo: positivo
    datos_ejemplo:
      fecha_inicio: "2000-01-01"
      fecha_fin: "2000-01-31"

definition_of_done:
  - "Todos los criterios de aceptación superan pruebas de regresión"
  - "Rendimiento validado con dataset de 10.000 registros en staging"
  - "Revisión de código aprobada por al menos un peer"
  - "Accesibilidad WCAG 2.1 AA verificada"

# ─────────────────────────────────────────────
# BLOQUE 4 — DATOS
# ─────────────────────────────────────────────
datos_entrada:
  - nombre: fecha_inicio
    tipo: date
    requerido: true
    formato: ISO-8601
    descripcion: "Fecha de inicio del rango de búsqueda"
  - nombre: fecha_fin
    tipo: date
    requerido: true
    formato: ISO-8601
    descripcion: "Fecha de fin del rango de búsqueda"

datos_salida:
  campos: [id_factura, fecha_factura, importe_total, estado, proveedor]
  formato: lista_paginada
  paginacion:
    aplica: true
    tamanyo_pagina_defecto: 20
    max_registros: 100
  orden_defecto: "fecha_factura DESC"
  tiempo_respuesta_max_ms: 2000

# ─────────────────────────────────────────────
# BLOQUE 5 — METADATOS TÉCNICOS
# (Lo completa el equipo en el refinamiento)
# ─────────────────────────────────────────────
componentes_afectados: []
integraciones_externas: []
restricciones_no_funcionales:
  rendimiento: ""
  seguridad: ""
  accesibilidad: ""
notas_implementacion: ""
trazabilidad:
  historias_generadas: []
  test_cases_generados: []
  jira_issues: []
```

---

## Campos obligatorios y el error del formulario perfecto

Una de las decisiones más importantes del taller de plantillas —el ejercicio que describe el próximo capítulo— es decidir qué campos son obligatorios. La tentación natural es marcar todos como obligatorios para maximizar la calidad del input. Es un error con consecuencias predecibles.

Un campo obligatorio que el analista no puede rellenar en el momento de la captura no produce calidad: produce ruido. El analista escribe "TBD", "pendiente", "N/A" o cualquier otra variante del placeholder que deja el campo técnicamente rellenado y funcionalmente vacío. El validador no detecta el problema porque el campo tiene un valor. El pipeline procesa ese valor como si fuera información real. El output hereda el ruido.

La regla práctica es esta: **un campo es obligatorio si su ausencia hace que el pipeline genere artefactos incorrectos o incompletos**. Si su ausencia solo reduce la calidad del output, es un campo recomendado que genera una advertencia en el validador, no un bloqueante.

Para la mayoría de organizaciones, el conjunto mínimo bloqueante es este:

```
OBLIGATORIOS BLOQUEANTES (sin estos, el pipeline no arranca):
  id, titulo, epica, estado, actor, descripcion (≥30 palabras),
  evento_disparador, prioridad, criterios_aceptacion (≥1 criterio
  con dado/cuando/entonces completos), excepciones (≥1)

RECOMENDADOS (advertencia si faltan):
  objetivo_negocio, reglas_negocio, flujo_principal,
  datos_entrada (si el requisito tiene inputs),
  datos_salida (si el requisito devuelve datos)

OPCIONALES (sin impacto en el pipeline básico):
  restricciones_no_funcionales, notas_implementacion,
  integraciones_externas
```

El Capítulo 7 describe el validador que aplica este checklist automáticamente antes de que el requisito entre al pipeline. Pero el checklist también puede aplicarse manualmente desde el primer día, sin ninguna herramienta: es la lista de preguntas que el analista se hace antes de mover un requisito de borrador a en-revisión.

---

## La vista del usuario de negocio

El YAML es para la máquina. Ana López nunca debería ver un YAML.

Lo que Ana ve cuando Carlos le pide validación de REQ-023 es una versión renderizada automáticamente desde el YAML, en formato de tabla comprensible para alguien que no ha oído hablar de YAML ni de pipelines:

```
┌───────────────────────────────────────────────────────────────┐
│  REQUISITO  REQ-023  │  Módulo: Gestión de Facturación        │
│  Estado: En revisión │  Prioridad: Must Have                  │
├───────────────────────────────────────────────────────────────┤
│  TÍTULO                                                       │
│  Filtrar facturas por rango de fechas                         │
├───────────────────────────────────────────────────────────────┤
│  ¿QUIÉN LO NECESITA?       │  ¿POR QUÉ?                       │
│  Gestor de facturación     │  Para localizar facturas de un   │
│                            │  período contable en el cierre   │
│                            │  mensual sin búsqueda manual     │
├───────────────────────────────────────────────────────────────┤
│  ¿QUÉ DEBE HACER EL SISTEMA?                                  │
│  El gestor introduce un rango de fechas y el sistema muestra  │
│  las facturas de ese período ordenadas de más reciente a más  │
│  antigua. Si el rango supera 365 días, avisa. Si no hay       │
│  facturas, lo indica con un mensaje.                          │
├───────────────────────────────────────────────────────────────┤
│  ¿CUÁNDO DEBE FUNCIONAR? (Criterios de aceptación)            │
│                                                               │
│  ✓ Si introduzco fechas válidas y pulso Buscar,               │
│    veo las facturas del período en menos de 2 segundos        │
│                                                               │
│  ✓ Si el rango supera 365 días,                               │
│    el sistema me avisa y no busca                             │
│                                                               │
│  ✓ Si no hay facturas en ese período,                         │
│    el sistema me lo indica y me ofrece ampliar                │
├───────────────────────────────────────────────────────────────┤
│  REGLAS IMPORTANTES                                           │
│  • Solo se ven facturas del ejercicio fiscal en curso         │
│  • El rango máximo de búsqueda es de 365 días                 │
├───────────────────────────────────────────────────────────────┤
│  SOLICITADO POR: Ana López (Dir. Financiera) · 2025-05-12     │
│  ANALISTA: Carlos Ruiz · Validado: pendiente                  │
└───────────────────────────────────────────────────────────────┘
```

Esta vista la genera automáticamente una macro de Confluence o un script de renderizado. Ana la lee, la entiende en dos minutos y la aprueba o pide cambios. No sabe que detrás hay un YAML. No necesita saberlo.

Esta separación entre la vista para humanos y la estructura para máquinas es uno de los principios de diseño más importantes de la plantilla. Si el usuario de negocio tiene que aprender YAML para validar un requisito, el sistema no se adoptará. Si el analista tiene que traducir manualmente entre los dos formatos, el coste de mantenimiento se vuelve inasumible. La solución es que ambas vistas se generen desde la misma fuente: el YAML es la única fuente de verdad, y las vistas son representaciones automáticas de esa fuente.

---

## Lo que funciona en la práctica

El mayor obstáculo en la implantación de la plantilla no es técnico: es cultural. Los analistas que llevan años escribiendo requisitos en Word tienen una forma establecida de trabajar que el nuevo formato interrumpe. La resistencia no viene de que la plantilla sea mala. Viene de que cualquier cambio en un flujo de trabajo establecido genera fricción, y la fricción se percibe como un problema con el cambio, no con el estado anterior.

Hay tres estrategias que reducen esa fricción de forma demostrable.

La primera es empezar por los criterios de aceptación, no por la plantilla completa. El formato Dado/Cuando/Entonces es el cambio más valioso y también el más fácil de introducir de forma aislada. Un analista que empieza a escribir sus criterios en ese formato en sus documentos Word actuales ya está generando el insumo más crítico para el pipeline, sin cambiar nada más en su proceso.

La segunda es el taller de plantillas: una sesión de dos horas donde el equipo diseña juntos la versión adaptada de la plantilla para el contexto de la organización, usando requisitos reales como material de trabajo. Cuando los analistas participan en el diseño de la plantilla en lugar de recibirla como un estándar impuesto, la adopción es significativamente más rápida. El Capítulo 13 describe este taller en detalle.

La tercera es la demostración inmediata del valor: tomar el primer requisito que alguien complete en la plantilla, pasarlo por el pipeline, y mostrar el output en pantalla. Ese momento —ver el propio trabajo transformado en artefactos correctos en menos de un minuto— es el argumento más poderoso que existe para la adopción. Ningún número de slides lo supera.

---

*Los tres puntos clave de este capítulo:*

1. La plantilla AI-ready es un contrato de datos entre el usuario de negocio, el equipo técnico y el pipeline de IA. Sus cinco bloques tienen responsabilidades distintas: identidad (localizar y versionar), contexto de negocio (el por qué), comportamiento esperado (qué debe hacer el sistema), datos (la forma de los datos), y metadatos técnicos (contexto para el refinamiento).

2. Los criterios de aceptación son el elemento más crítico de la plantilla para la generación automática de artefactos. Cuatro reglas los definen: el `dado` describe un estado, el `cuando` una única acción, el `entonces` algo observable externamente, y los datos son concretos en lugar de placeholders. Un criterio que no cumple estas cuatro reglas no genera un test case ejecutable.

3. Marcar todos los campos como obligatorios no mejora la calidad del input: produce ruido. Un campo es obligatorio si su ausencia genera artefactos incorrectos. Si solo reduce la calidad, es recomendado. El conjunto mínimo bloqueante tiene once campos; los demás son recomendados u opcionales.

---

*Pregunta para llevar a tu próxima reunión de equipo:*

Si tomamos los criterios de aceptación de las últimas cinco historias de nuestro backlog y los evaluamos contra las cuatro reglas del formato Dado/Cuando/Entonces, ¿cuántos cumplen las cuatro reglas? ¿Cuál es la regla que se incumple con más frecuencia?
