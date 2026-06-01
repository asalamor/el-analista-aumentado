# Capítulo 9. Generación automática de test cases

---

> **En este capítulo:**
> - Por qué los test cases son el artefacto que más se beneficia del análisis funcional estructurado
> - La arquitectura de siete llamadas ramificadas que genera cobertura completa desde los criterios de aceptación
> - Los prompts para casos positivos, negativos y de contorno, con los outputs reales de REQ-023
> - La matriz de cobertura AC ↔ TC generada automáticamente
> - Cómo integrar los test cases en Xray o Zephyr Scale sin trabajo manual

---

El martes siguiente al que Carlos generó los artefactos Jira de REQ-023, Lucía —la QA lead del equipo de Meridian— abrió el tablero de Xray y encontró algo que no esperaba: nueve casos de prueba ya creados, vinculados a la historia FACT-47, con pasos detallados, datos de prueba concretos y el criterio de aceptación de origen referenciado en cada uno.

Tres de esos nueve casos verificaban flujos de error que Lucía sabe, por experiencia, que el equipo normalmente olvida documentar hasta que el bug aparece en producción. Y los cuatro casos de contorno —los que verifican los valores límite exactos del rango de 365 días— eran precisamente los que habrían pasado desapercibidos en la sesión de refinamiento.

«¿Esto lo generó el mismo sistema que creó las historias?», preguntó.

«El mismo», respondió Carlos. «Tardó unos quince segundos.»

Lo que Lucía estaba viendo no era un truco ni una simplificación: era el resultado de un principio que este capítulo va a explicar en detalle. Cuando el criterio de aceptación está bien escrito —en formato Dado/Cuando/Entonces, con datos concretos, con flujos de error documentados—, el salto hasta el caso de prueba ejecutable es casi mecánico. La IA no adivina: transforma una estructura en otra estructura equivalente.

El problema histórico del testing funcional no ha sido la falta de intención de documentar casos de prueba. Ha sido la falta de tiempo: el QA llega al sprint cuando el desarrollo ya ha empezado, con el backlog lleno de historias que nadie ha testeado formalmente, y hace lo que puede. Los flujos felices se documentan. Los flujos de error se recuerdan a medias. Los casos de contorno casi nunca aparecen.

Este capítulo resuelve ese problema en su raíz.

---

## El valor de unos criterios bien escritos

En el Capítulo 4 se insistió en una cosa: el formato Dado/Cuando/Entonces no es una convención estética. Es una estructura determinista que un sistema puede procesar de forma predecible. El *dado* describe un estado del sistema. El *cuando* describe una acción concreta. El *entonces* describe un resultado observable.

Esa estructura es exactamente la que necesita un caso de prueba:

- Las **precondiciones** salen del *dado*
- Los **pasos** salen del *cuando*
- El **resultado esperado** sale del *entonces*

Cuando los criterios de aceptación tienen esa forma, el pipeline no genera test cases: los *transcribe*, enriqueciéndolos con datos concretos y organizándolos en una jerarquía que una herramienta de QA puede importar directamente.

Cuando los criterios no tienen esa forma —cuando el *entonces* dice «el sistema funciona correctamente» o cuando el *dado* describe una acción en lugar de un estado—, el pipeline no puede ayudar. O mejor dicho: puede generar algo, pero ese algo será tan vago como el input.

> 💡 **Idea clave**
>
> La calidad de los test cases generados es una función directa de la calidad de los criterios de aceptación de los que derivan. No hay prompt suficientemente bueno que compense un criterio mal escrito. Por eso el Capítulo 7 (validación) va antes del Capítulo 9 (test cases): el validador detecta los criterios no verificables antes de que lleguen al pipeline.

---

## Arquitectura del pipeline de test cases

El pipeline de test cases tiene una lógica diferente al de artefactos Jira. El de Jira es lineal: cada llamada alimenta a la siguiente. El de test cases es **ramificado**: desde cada criterio de aceptación y desde las reglas de negocio del requisito se generan tipos distintos de prueba en paralelo, y al final se ensamblan en una matriz de cobertura.

```
Historia de usuario (FACT-47)
│
├── Criterios de aceptación positivos (AC-023-01)
│   └── [Llamada 1] → Casos funcionales (flujo feliz)
│
├── Criterios de aceptación negativos + flujos de error
│   └── [Llamada 2] → Casos negativos y de error
│
├── Reglas de negocio con rangos numéricos o condiciones límite
│   └── [Llamada 3] → Casos de contorno (boundary values)
│
├── Datos de entrada con tipos, formatos y restricciones
│   └── [Llamada 4] → Casos de validación de campos
│
└── [Llamada 5] → Scripts Gherkin para automatización
    │
    └── [Llamada 6] → Matriz de cobertura AC ↔ TC
```

Cada llamada tiene su propio system prompt y su propio enfoque. No es lo mismo generar un caso positivo (el sistema debe hacer X cuando todo va bien) que un caso negativo (el sistema debe rechazar Y cuando falta Z) que un caso de contorno (el valor exactamente en el límite debe funcionar; el valor un paso por encima debe fallar).

La razón de separarlos en llamadas distintas es la misma que en el pipeline de Jira: el modelo optimiza para el objetivo que tiene delante. Si le pedimos que genere «todos los tipos de test cases», tenderá a generar los positivos con detalle y los negativos con menos cuidado. Si le pedimos exclusivamente casos negativos, los genera con el nivel de exhaustividad que esos casos merecen.

---

## System prompt base para el pipeline de QA

El system prompt del pipeline de test cases es diferente al del pipeline de Jira. El modelo debe pensar como un QA engineer experimentado, no como un analista funcional.

```
📋 Prompt de IA — System prompt base para generación de test cases
────────────────────────────────────────────────────────────────────

Eres un QA engineer senior especializado en testing funcional y automatización.
Tu función es generar casos de prueba exhaustivos, precisos y directamente
ejecutables a partir de criterios de aceptación y requisitos funcionales.

REGLAS ESTRICTAS:
1. Cada caso de prueba debe ser ejecutable por una persona sin conocimiento
   previo del sistema. Nada puede darse por implícito.
2. Los datos de prueba deben ser concretos. Nunca uses placeholders como
   "introducir un valor válido". Usa "introducir fecha 2024-01-15".
3. Cada paso tiene exactamente un resultado esperado verificable.
4. Un caso de prueba no puede tener más de 10 pasos. Si necesita más,
   se divide en dos casos.
5. Los casos negativos son tan importantes como los positivos.
   Por cada flujo feliz, genera al menos un caso negativo.
6. Los casos de contorno son obligatorios para cualquier campo
   con rango numérico, longitud de texto o fecha.
7. El resultado esperado describe el comportamiento OBSERVABLE:
   lo que ve el usuario, el mensaje que aparece, el estado que cambia.
   Nunca describe lógica interna.
8. Nunca dupliques casos. Si detectas solapamiento, indícalo en alertas.
9. El output es siempre JSON válido.

GLOSARIO DEL PROYECTO:
{{glosario_yaml}}

ENTORNO DE PRUEBAS:
- URL base: {{url_entorno}}
- Usuario de prueba: {{usuario_prueba}}
- Datos disponibles: {{referencia_datos_prueba}}
```

Hay una regla que merece detenerse un momento: la regla 7, que dice que el resultado esperado describe comportamiento *observable*. Es la regla más violada en la escritura de test cases.

«El sistema valida la fecha correctamente» no es un resultado observable. «El campo 'Desde' se resalta en rojo y aparece el texto 'El rango no puede superar 365 días'» sí lo es. La diferencia es que el primero requiere que quien ejecuta el test sepa qué considera el sistema como «validación correcta». El segundo puede ejecutarlo alguien que no conoce el sistema.

---

## Llamada 1: casos funcionales del flujo feliz

El primer prompt genera los casos del camino principal, uno por cada criterio de aceptación de tipo positivo. Es el más sencillo de generar, pero también el más importante: si el flujo feliz falla, nada más importa.

```
📋 Prompt de IA — Casos funcionales (flujo feliz)
───────────────────────────────────────────────────

A partir de la historia de usuario y sus criterios de aceptación positivos,
genera los casos de prueba del flujo principal.

HISTORIA DE USUARIO:
{{historia_json}}

CRITERIOS DE ACEPTACIÓN POSITIVOS:
{{lista_ac_positivos}}

DATOS DE PRUEBA DISPONIBLES EN EL ENTORNO:
{{datos_prueba_disponibles}}

Para cada criterio de aceptación positivo genera UN caso de prueba:

{
  "test_cases": [
    {
      "id": "TC-{{req_id}}-{{numero}}",
      "titulo": "[Verbo] + [funcionalidad] + [condición específica]",
      "tipo": "funcional_positivo",
      "criterio_origen": "{{ac_id}}",
      "historia_origen": "{{historia_id}}",
      "requisito_origen": "{{req_id}}",
      "prioridad": "critica | alta | media | baja",
      "precondiciones": [
        "[Estado del sistema antes de iniciar]",
        "[Datos que deben existir]",
        "[Rol del usuario]"
      ],
      "datos_prueba": {
        "[campo]": "[valor concreto]"
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "[Qué hace el usuario o el sistema]",
          "resultado_esperado": "[Qué ocurre. Observable y verificable.]"
        }
      ],
      "resultado_final_esperado": "[Estado final del sistema]",
      "automatizable": true,
      "notas_automatizacion": "[Selector CSS/XPath, endpoint, etc.]"
    }
  ]
}
```

Este es el output real que el pipeline generó para AC-023-01 de REQ-023:

```json
{
  "test_cases": [
    {
      "id": "TC-023-01",
      "titulo": "Filtrar facturas con rango de fechas válido devuelve resultados correctos",
      "tipo": "funcional_positivo",
      "criterio_origen": "AC-023-01",
      "historia_origen": "US-047",
      "requisito_origen": "REQ-023",
      "prioridad": "critica",
      "precondiciones": [
        "Usuario autenticado con rol gestor_facturacion (gestor01@meridian.com)",
        "Existen al menos 5 facturas en BD con fecha entre 2024-01-01 y 2024-03-31",
        "El módulo Facturas está accesible y sin errores de sistema"
      ],
      "datos_prueba": {
        "fecha_inicio": "2024-01-01",
        "fecha_fin": "2024-03-31",
        "registros_esperados_minimo": 5
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "Navegar a la URL /facturas",
          "resultado_esperado": "Se carga el listado de facturas con el panel de filtros visible en la parte superior"
        },
        {
          "numero": 2,
          "accion": "Introducir '2024-01-01' en el campo 'Desde'",
          "resultado_esperado": "El campo muestra la fecha 01/01/2024 con el formato local del sistema"
        },
        {
          "numero": 3,
          "accion": "Introducir '2024-03-31' en el campo 'Hasta'",
          "resultado_esperado": "El campo muestra la fecha 31/03/2024. Ningún mensaje de error visible."
        },
        {
          "numero": 4,
          "accion": "Pulsar el botón 'Buscar'",
          "resultado_esperado": "Aparece un indicador de carga (spinner o skeleton de filas)"
        },
        {
          "numero": 5,
          "accion": "Esperar a que termine la carga",
          "resultado_esperado": "El listado muestra facturas en menos de 2 segundos. La primera factura tiene fecha igual o anterior a 2024-03-31. La última factura visible tiene fecha igual o posterior a 2024-01-01."
        },
        {
          "numero": 6,
          "accion": "Verificar el orden de los resultados",
          "resultado_esperado": "Las facturas aparecen ordenadas por fecha de forma descendente: la más reciente primero, la más antigua al final"
        },
        {
          "numero": 7,
          "accion": "Verificar el contador de resultados",
          "resultado_esperado": "Se muestra un texto del tipo 'X facturas encontradas' con un número mayor que 0"
        }
      ],
      "resultado_final_esperado": "El listado muestra todas las facturas del período Q1 2024 ordenadas por fecha descendente, con el contador de resultados visible y el tiempo de respuesta inferior a 2 segundos.",
      "automatizable": true,
      "notas_automatizacion": "Selector campo Desde: #filter-date-from. Selector campo Hasta: #filter-date-to. Botón buscar: [data-testid='btn-search']. Contador: [data-testid='results-count']. Verificar tiempo de respuesta con performance.now() antes y después del clic."
    }
  ]
}
```

Hay un detalle en el paso 5 que merece atención: el resultado esperado verifica tres cosas a la vez —el tiempo de respuesta, la fecha de la primera factura y la fecha de la última—. Esto parece violar la regla de «un paso, un resultado», pero en este caso las tres condiciones corresponden al mismo momento de observación: cuando la lista aparece. Separarlas en tres pasos distintos haría el test innecesariamente largo. La regla se aplica con criterio, no de forma mecánica.

---

## Llamada 2: casos negativos y de error

Esta es la llamada donde la IA aporta más valor que un QA humano bajo presión de tiempo. Cuando hay un sprint que entregar y el tiempo es escaso, los flujos de error son los primeros que se sacrifican. El pipeline no tiene esa presión.

El prompt le pide al modelo que analice cuatro categorías de casos negativos: validaciones de campos obligatorios, violaciones de reglas de negocio, problemas de permisos y errores de sistema. La instrucción más importante es la última: para cada caso negativo, debe indicar cuál es el **comportamiento incorrecto habitual** que cometen los desarrolladores.

```
📋 Prompt de IA — Casos negativos y de error
──────────────────────────────────────────────

A partir de la historia de usuario, genera TODOS los casos de prueba
negativos y de error posibles. Sé exhaustivo: estos son los casos donde
viven la mayoría de los bugs en producción.

HISTORIA DE USUARIO:
{{historia_json}}

FLUJOS DE ERROR DOCUMENTADOS:
{{flujos_error_historia}}

REGLAS DE NEGOCIO DEL REQUISITO:
{{reglas_negocio}}

Genera casos negativos para TODAS estas categorías que apliquen:

CATEGORÍA A — Validaciones de campos obligatorios:
  Por cada campo obligatorio: ¿qué pasa si se omite?

CATEGORÍA B — Violaciones de reglas de negocio:
  Por cada regla de negocio: ¿qué pasa si se viola?

CATEGORÍA C — Permisos y autorización:
  ¿Qué pasa si un usuario sin permiso intenta la acción?

CATEGORÍA D — Errores de sistema:
  ¿Qué pasa si el servicio externo o BD no responde?

Usa la misma estructura JSON que los casos positivos, añadiendo:
"comportamiento_incorrecto_habitual": "[Error típico de los desarrolladores
en este caso, para que el QA lo busque específicamente]"
```

El output para REQ-023 generó cuatro casos negativos. Aquí están los dos más representativos:

```json
{
  "id": "TC-023-02",
  "titulo": "Buscar con rango de fechas superior a 365 días muestra error de validación",
  "tipo": "negativo_regla_negocio",
  "criterio_origen": "AC-023-02",
  "prioridad": "alta",
  "precondiciones": [
    "Usuario autenticado con rol gestor_facturacion",
    "Módulo Facturas accesible"
  ],
  "datos_prueba": {
    "fecha_inicio": "2023-01-01",
    "fecha_fin": "2024-01-02",
    "dias_diferencia": 366
  },
  "pasos": [
    {
      "numero": 1,
      "accion": "Navegar a /facturas e introducir fecha_inicio='2023-01-01' y fecha_fin='2024-01-02'",
      "resultado_esperado": "Los campos aceptan los valores sin mostrar ningún error"
    },
    {
      "numero": 2,
      "accion": "Pulsar el botón 'Buscar'",
      "resultado_esperado": "El sistema NO ejecuta ninguna consulta a la base de datos. Los campos fecha_inicio y fecha_fin se resaltan en rojo. Aparece el mensaje exacto: 'El rango no puede superar 365 días'."
    },
    {
      "numero": 3,
      "accion": "Verificar que no aparecen resultados en el listado",
      "resultado_esperado": "El listado permanece en su estado anterior. No se muestran filas nuevas ni estado vacío."
    }
  ],
  "resultado_final_esperado": "Validación activa, sin consulta ejecutada, mensaje de error visible, campos resaltados.",
  "automatizable": true,
  "comportamiento_incorrecto_habitual": "El desarrollador ejecuta la consulta y después valida, mostrando los resultados un instante antes de mostrar el error. O valida el error pero no resalta los campos en rojo, solo muestra el mensaje."
}
```

```json
{
  "id": "TC-023-04",
  "titulo": "Usuario sin rol gestor_facturacion no puede acceder al módulo Facturas",
  "tipo": "negativo_permiso",
  "criterio_origen": "AC-023-01",
  "prioridad": "critica",
  "precondiciones": [
    "Usuario autenticado con rol consultor_basico (consultor01@meridian.com)",
    "El rol consultor_basico no tiene permisos sobre el módulo de Facturación"
  ],
  "datos_prueba": {
    "usuario": "consultor01@meridian.com",
    "rol": "consultor_basico",
    "url_directa": "/facturas"
  },
  "pasos": [
    {
      "numero": 1,
      "accion": "Navegar directamente a la URL /facturas sin usar el menú de navegación",
      "resultado_esperado": "El sistema redirige a la página de acceso denegado o devuelve HTTP 403. No se carga el módulo. No se muestran datos de facturación."
    }
  ],
  "resultado_final_esperado": "Acceso denegado. Ningún dato de facturación visible.",
  "automatizable": true,
  "comportamiento_incorrecto_habitual": "El menú de navegación oculta el enlace al módulo, pero la URL directa sigue siendo accesible. La seguridad solo está implementada en el frontend, no en el backend. Este es uno de los bugs de seguridad más frecuentes."
}
```

El campo `comportamiento_incorrecto_habitual` es el que más aprecia el equipo de QA de Meridian. No es un campo decorativo: es una instrucción de búsqueda activa. Cuando Lucía ejecuta TC-023-02, sabe exactamente qué mirar: ¿el sistema ejecutó la consulta y mostró datos antes del error? Si es así, el bug está ahí aunque el mensaje final parezca correcto.

---

## Llamada 3: casos de contorno (boundary values)

Los valores límite son el tipo de prueba que más consistentemente genera bugs en producción y que más consistentemente se omite bajo presión de tiempo. La razón es intuitiva: si el máximo de días permitido es 365, ¿quién va a probar exactamente 365 días, 364 días y 366 días? En un mundo ideal, todo el mundo. En la práctica, nadie.

El pipeline genera estos casos automáticamente desde la especificación de los datos de entrada. La regla es simple y sistemática: para cada restricción numérica, de longitud o de fecha, se generan cuatro casos:

- El valor exactamente en el límite inferior → debe funcionar (PASS)
- El valor un paso por debajo del límite inferior → debe fallar (FAIL)
- El valor exactamente en el límite superior → debe funcionar (PASS)
- El valor un paso por encima del límite superior → debe fallar (FAIL)

«Un paso» significa ±1 para enteros, ±1 día para fechas, ±1 carácter para texto.

```
📋 Prompt de IA — Casos de contorno (boundary values)
───────────────────────────────────────────────────────

Analiza todos los campos con restricciones numéricas, de longitud o de fecha
en el siguiente requisito y genera los casos de prueba de valores límite.

REQUISITO:
{{requisito_yaml}}

Para cada restricción identificada, genera exactamente estos 4 casos:
- Valor en el límite inferior exacto → debe funcionar (PASS)
- Valor un paso por debajo del límite inferior → debe fallar (FAIL)
- Valor en el límite superior exacto → debe funcionar (PASS)
- Valor un paso por encima del límite superior → debe fallar (FAIL)

"Un paso" significa:
- Para enteros: ±1
- Para fechas: ±1 día
- Para texto: ±1 carácter
- Para decimales: la precisión mínima del campo (ej: ±0.01 para 2 decimales)

Añade el campo "valor_limite" que especifica qué restricción se está probando.
```

El output para REQ-023 identificó una restricción con cuatro casos de contorno: el rango máximo de 365 días entre `fecha_inicio` y `fecha_fin`.

```json
{
  "restricciones_identificadas": [
    {
      "campo": "rango_fechas",
      "restriccion": "Máximo 365 días entre fecha_inicio y fecha_fin",
      "test_cases": [
        {
          "id": "TC-023-06",
          "titulo": "Rango de exactamente 364 días es aceptado (límite superior - 1)",
          "tipo": "contorno",
          "valor_limite": "límite superior - 1 — debe pasar",
          "datos_prueba": {
            "fecha_inicio": "2023-01-01",
            "fecha_fin": "2023-12-31",
            "dias_diferencia": 364
          },
          "pasos": [
            {
              "numero": 1,
              "accion": "Introducir fecha_inicio='2023-01-01', fecha_fin='2023-12-31' y pulsar Buscar",
              "resultado_esperado": "La búsqueda se ejecuta correctamente. No aparece ningún mensaje de error de validación."
            }
          ],
          "resultado_final_esperado": "Resultados visibles o estado vacío, pero sin error de validación.",
          "prioridad": "alta"
        },
        {
          "id": "TC-023-07",
          "titulo": "Rango de exactamente 365 días es aceptado (límite superior exacto)",
          "tipo": "contorno",
          "valor_limite": "límite superior exacto — debe pasar",
          "datos_prueba": {
            "fecha_inicio": "2023-01-01",
            "fecha_fin": "2024-01-01",
            "dias_diferencia": 365
          },
          "pasos": [
            {
              "numero": 1,
              "accion": "Introducir fecha_inicio='2023-01-01', fecha_fin='2024-01-01' y pulsar Buscar",
              "resultado_esperado": "La búsqueda se ejecuta correctamente. No aparece ningún mensaje de error de validación."
            }
          ],
          "resultado_final_esperado": "Resultados visibles o estado vacío, sin error de validación.",
          "prioridad": "alta"
        },
        {
          "id": "TC-023-08",
          "titulo": "Rango de 366 días es rechazado (límite superior + 1)",
          "tipo": "contorno",
          "valor_limite": "límite superior + 1 — debe fallar",
          "datos_prueba": {
            "fecha_inicio": "2023-01-01",
            "fecha_fin": "2024-01-02",
            "dias_diferencia": 366
          },
          "pasos": [
            {
              "numero": 1,
              "accion": "Introducir fecha_inicio='2023-01-01', fecha_fin='2024-01-02' y pulsar Buscar",
              "resultado_esperado": "El sistema muestra el mensaje de validación 'El rango no puede superar 365 días'. No se ejecuta ninguna consulta."
            }
          ],
          "resultado_final_esperado": "Error de validación visible. Sin resultados mostrados.",
          "prioridad": "alta"
        },
        {
          "id": "TC-023-09",
          "titulo": "Rango de un solo día (fecha_inicio igual a fecha_fin) es aceptado",
          "tipo": "contorno",
          "valor_limite": "límite inferior exacto — debe pasar",
          "datos_prueba": {
            "fecha_inicio": "2024-03-15",
            "fecha_fin": "2024-03-15",
            "dias_diferencia": 0
          },
          "pasos": [
            {
              "numero": 1,
              "accion": "Introducir fecha_inicio='2024-03-15', fecha_fin='2024-03-15' y pulsar Buscar",
              "resultado_esperado": "La búsqueda se ejecuta correctamente. Se muestran las facturas de ese día o el estado vacío si no hay ninguna."
            }
          ],
          "resultado_final_esperado": "Resultados del día o estado vacío. Sin error de validación.",
          "prioridad": "media"
        }
      ]
    }
  ]
}
```

> ⚠️ **Error frecuente**
>
> El caso TC-023-07 es el más revelador. El límite exacto de 365 días: ¿es válido o no? La regla de negocio dice «el rango máximo es 365 días». Eso implica que 365 días debe funcionar y 366 debe fallar. Pero el desarrollador puede haber implementado la condición como `diferencia > 365` (correcto) o como `diferencia >= 365` (incorrecto, bloquearía también el límite exacto). Solo un caso de prueba con exactamente 365 días detecta ese error.

---

## Llamada 4: scripts Gherkin para automatización

Una vez generados los casos de prueba en JSON, el pipeline los convierte en *feature files* ejecutables para frameworks de automatización como Cucumber, Behave o Playwright + Cucumber. Esta llamada es opcional: algunos equipos gestionan la automatización por separado y prefieren recibir los test cases en formato manual primero.

```
📋 Prompt de IA — Scripts Gherkin para automatización
───────────────────────────────────────────────────────

Convierte los siguientes casos de prueba en scripts Gherkin (BDD)
listos para ejecutarse con Cucumber o Behave.

CASOS DE PRUEBA:
{{test_cases_json}}

REGLAS DE FORMATO GHERKIN:
- Usa Background para precondiciones comunes a todos los escenarios.
- Usa Scenario Outline + Examples cuando varios casos usan la misma
  estructura con datos distintos.
- Los steps deben ser reutilizables: escríbelos pensando en que existirá
  un step definition que los implementa.
- Incluye tags por prioridad (@critica, @alta, @media), por tipo
  (@positivo, @negativo, @contorno) y por historia (@US-047).
- Los datos van en la tabla Examples o como parámetros entre comillas dobles.
- Idioma: {{idioma_gherkin}}

Genera el feature file completo como string dentro del JSON, más los
step definitions sugeridos para que el equipo de automatización pueda
implementarlos.
```

Este es el *feature file* generado para REQ-023:

```gherkin
# language: es
@facturacion @US-047 @REQ-023
Característica: Filtrado de facturas por rango de fechas

  Como gestor de facturación
  Quiero filtrar el listado de facturas por rango de fechas
  Para localizar rápidamente las facturas de un período contable concreto

  Antecedentes:
    Dado que el usuario "gestor01@meridian.com" está autenticado con rol "gestor_facturacion"
    Y que accede al módulo "Facturas"
    Y que existen facturas en el sistema con fechas entre "2024-01-01" y "2024-03-31"

  @critica @positivo @TC-023-01
  Esquema del escenario: Filtrado válido devuelve resultados ordenados correctamente
    Dado que introduce la fecha de inicio "<fecha_inicio>"
    Y que introduce la fecha de fin "<fecha_fin>"
    Cuando pulsa el botón "Buscar"
    Entonces el sistema devuelve resultados en menos de "<tiempo_max>" segundos
    Y los resultados están ordenados por fecha de forma descendente
    Y se muestra el contador con el número de facturas encontradas

    Ejemplos:
      | fecha_inicio | fecha_fin  | tiempo_max |
      | 2024-01-01   | 2024-03-31 | 2          |
      | 2024-01-01   | 2024-01-31 | 2          |
      | 2024-03-01   | 2024-03-31 | 2          |

  @alta @negativo @TC-023-02
  Escenario: Rango superior a 365 días muestra error de validación
    Dado que introduce la fecha de inicio "2023-01-01"
    Y que introduce la fecha de fin "2024-01-02"
    Cuando pulsa el botón "Buscar"
    Entonces el sistema no ejecuta ninguna búsqueda
    Y los campos de fecha se resaltan en rojo
    Y se muestra el mensaje de error "El rango no puede superar 365 días"

  @alta @negativo @TC-023-03
  Escenario: Búsqueda sin fecha de inicio muestra campo obligatorio
    Dado que deja el campo de fecha de inicio vacío
    Y que introduce la fecha de fin "2024-03-31"
    Cuando pulsa el botón "Buscar"
    Entonces el campo "Desde" se muestra como obligatorio con error de validación
    Y no se ejecuta ninguna búsqueda

  @critica @negativo @TC-023-04
  Escenario: Usuario sin permisos no puede acceder al módulo
    Dado que el usuario "consultor01@meridian.com" está autenticado con rol "consultor_basico"
    Cuando navega directamente a la URL "/facturas"
    Entonces el sistema deniega el acceso
    Y no se muestran datos de facturación

  @media @positivo @TC-023-05
  Escenario: Búsqueda sin resultados muestra estado vacío con acción disponible
    Dado que introduce la fecha de inicio "2000-01-01"
    Y que introduce la fecha de fin "2000-01-31"
    Cuando pulsa el botón "Buscar"
    Entonces se muestra el mensaje "No se encontraron facturas para el período seleccionado"
    Y se muestra el botón "Ampliar búsqueda"

  @alta @contorno @TC-023-06 @TC-023-07 @TC-023-08 @TC-023-09
  Esquema del escenario: Valores límite del rango de 365 días
    Dado que introduce la fecha de inicio "<fecha_inicio>"
    Y que introduce la fecha de fin "<fecha_fin>"
    Cuando pulsa el botón "Buscar"
    Entonces el resultado es "<resultado>"

    Ejemplos:
      | fecha_inicio | fecha_fin  | dias | resultado                        |
      | 2023-01-01   | 2023-12-31 | 364  | búsqueda ejecutada correctamente |
      | 2023-01-01   | 2024-01-01 | 365  | búsqueda ejecutada correctamente |
      | 2023-01-01   | 2024-01-02 | 366  | error de validación mostrado     |
      | 2024-03-15   | 2024-03-15 | 0    | búsqueda ejecutada correctamente |
```

El *feature file* incluye los mismos IDs de test case (TC-023-01 a TC-023-09) que los JSONs anteriores. Esa coherencia es lo que permite vincularlos en Xray: el campo `id` del JSON se mapea al identificador del test en Xray, y el *feature file* lleva los mismos tags para que la trazabilidad funcione en ambas direcciones.

---

## Llamada 5: matriz de cobertura AC ↔ TC

La última llamada genera el artefacto que el equipo de QA normalmente tarda horas en producir y que habitualmente está desactualizado a las dos semanas de crearse: la matriz de trazabilidad entre criterios de aceptación y casos de prueba.

```
📋 Prompt de IA — Matriz de cobertura AC ↔ TC
───────────────────────────────────────────────

A partir de la historia de usuario y los test cases generados,
produce la matriz de cobertura completa.

HISTORIA:
{{historia_json}}

TEST CASES GENERADOS:
{{todos_test_cases_json}}

Genera:
{
  "matriz_cobertura": {
    "historia_id": "{{historia_id}}",
    "fecha_generacion": "{{fecha}}",
    "resumen": {
      "total_ac": N,
      "total_tc": N,
      "ac_con_cobertura_completa": N,
      "ac_con_cobertura_parcial": N,
      "ac_sin_cobertura": N,
      "porcentaje_cobertura": "N%"
    },
    "cobertura_por_ac": [
      {
        "ac_id": "AC-023-01",
        "descripcion_resumida": "[Qué verifica]",
        "test_cases_asociados": {
          "positivos": ["TC-023-01"],
          "negativos": ["TC-023-02", "TC-023-03"],
          "contorno": ["TC-023-06", "TC-023-07", "TC-023-08", "TC-023-09"]
        },
        "cobertura": "completa | parcial | sin_cobertura",
        "gaps_detectados": []
      }
    ],
    "recomendaciones": [
      "[Test adicional recomendado no derivable de los AC actuales]"
    ]
  }
}
```

Esta es la matriz generada para FACT-47:

| AC | Descripción | Positivos | Negativos | Contorno | Cobertura |
|---|---|---|---|---|---|
| AC-023-01 | Filtrado válido devuelve resultados <br>ordenados en < 2s | TC-023-01 | TC-023-03, <br>TC-023-04 | TC-023-06..09 | ✅ Completa |
| AC-023-02 | Rango > 365 días bloquea la búsqueda <br>y muestra error | — | TC-023-02 | TC-023-08 | ✅ Completa |
| AC-023-03 | Sin resultados muestra estado vacío <br>con botón de acción | TC-023-05 | — | — | ✅ Completa |

**Resumen de cobertura:**
- Total criterios AC: 3
- Total test cases: 9 (2 positivos · 4 negativos · 3 de contorno)
- Cobertura completa: 100%
- Ratio TC/AC: 3,0

**Recomendaciones del sistema:**
- Añadir prueba de rendimiento con 10.000 registros en entorno de staging (no derivable de los AC actuales; requiere dataset específico).
- Considerar prueba de sesión expirada durante una búsqueda activa (el sistema redirige al login o muestra mensaje de sesión expirada).
- Validar comportamiento en zona horaria diferente a la del servidor para fechas en el cambio de día.

Las tres recomendaciones al final de la matriz son el tipo de observación que solo aparece cuando alguien ha pensado en el problema más allá del texto del requisito. La IA las genera porque el system prompt le pide explícitamente que identifique escenarios que no son directamente derivables de los AC actuales pero que un QA experimentado consideraría. No siempre son pertinentes, pero cuando lo son, su valor es desproporcionado.

---

## Integración con Xray y Zephyr Scale

Los nueve test cases de REQ-023 llegaron al tablero de Xray de Meridian mediante un push por API que el propio orquestador gestiona. El proceso es simple: el JSON generado se transforma al formato de importación de Xray y se envía en una sola llamada.

```python
# push_xray.py
# Recibe los test cases en formato JSON del pipeline y los importa a Xray

import requests

def push_test_cases_xray(test_cases, jira_config):
    """
    Importa los test cases generados a Xray como test issues vinculados
    a la historia de usuario correspondiente.
    
    Parámetros:
      test_cases     — lista de dicts en el formato del pipeline
      jira_config    — dict con base_url, user, token y project_key
    """
    
    # Construir el payload en el formato de importación de Xray
    payload = {
        "testExecution": {
            # Crear una ejecución de test vinculada a la historia
            "projectKey": jira_config["project_key"],
            "summary": f"Test cases generados automáticamente — {test_cases[0]['historia_origen']}",
            "description": "Generados desde criterios de aceptación via pipeline IA"
        },
        "tests": [
            {
                "summary": tc["titulo"],
                "type": "Cucumber" if tc.get("automatizable") else "Manual",
                "steps": [
                    {
                        # Xray espera "action" y "result" como campos del paso
                        "action": paso["accion"],
                        "result": paso["resultado_esperado"]
                    }
                    for paso in tc.get("pasos", [])
                ],
                # Precondiciones del test case
                "precondition": "\n".join(tc.get("precondiciones", [])),
                # Etiquetas para filtrado y reporting
                "labels": [
                    tc.get("tipo", ""),
                    tc.get("criterio_origen", ""),
                    tc.get("requisito_origen", "")
                ],
                # Vínculo con la historia de usuario en Jira
                "requirements": [tc.get("historia_origen", "")]
            }
            for tc in test_cases
        ]
    }
    
    # Llamada a la API de Xray
    response = requests.post(
        f"{jira_config['base_url']}/rest/raven/1.0/import/test",
        json=payload,
        auth=(jira_config["user"], jira_config["token"])
    )
    
    response.raise_for_status()
    return response.json()
```

El conector con Zephyr Scale es equivalente pero usa su propia API. El principio es el mismo: el JSON del pipeline es el formato intermedio que se adapta al formato de cada herramienta. Si el equipo usa una herramienta distinta, solo cambia el conector, no el pipeline de generación.

> 🛠️ **En la práctica**
>
> El primer push a Xray en Meridian tardó más de lo esperado, no por el código sino por los campos personalizados. Xray tiene campos obligatorios que varían según la configuración de la instancia. El consejo práctico: antes de automatizar el push, hacer un export manual de un test case existente en Xray para ver exactamente qué campos espera esa instancia concreta. Ese export es la plantilla del payload.

---

## Los nueve test cases de REQ-023: el resultado completo

Al final del pipeline, REQ-023 tiene nueve test cases organizados en cuatro categorías:

| ID | Tipo | Criterio origen | Prioridad |
|---|---|---|---|
| TC-023-01 | Positivo — flujo feliz | AC-023-01 | Crítica |
| TC-023-02 | Negativo — regla de negocio | AC-023-02 | Alta |
| TC-023-03 | Negativo — validación de campo | AC-023-01 | Alta |
| TC-023-04 | Negativo — permiso | AC-023-01 | Crítica |
| TC-023-05 | Positivo — estado vacío | AC-023-03 | Media |
| TC-023-06 | Contorno — límite superior -1 | AC-023-02 | Alta |
| TC-023-07 | Contorno — límite superior exacto | AC-023-02 | Alta |
| TC-023-08 | Contorno — límite superior +1 | AC-023-02 | Alta |
| TC-023-09 | Contorno — límite inferior exacto | AC-023-02 | Media |

Estos nueve test cases tienen una propiedad notable: ninguno es redundante y ningún criterio de aceptación queda sin cobertura. Eso no es un accidente: es el resultado de haber separado las llamadas por tipo de caso. Si los hubiera generado todos en una sola llamada, la distribución habría sido diferente —probablemente más cargada de positivos y más escasa de contorno—.

> 💡 **Idea clave**
>
> El número de test cases no es una métrica de calidad. Una historia con tres criterios de aceptación bien escritos puede necesitar doce test cases. Una historia con diez criterios vagos puede generar veinte test cases que no verifican nada útil. La métrica que importa es el ratio de bugs detectados en testing respecto a los que llegan a producción. Eso tarda meses en medirse, pero es lo único que dice si el sistema funciona.

---

## Lo que el pipeline no puede hacer

Este capítulo ha mostrado lo que el pipeline genera. Conviene ser igual de claro sobre lo que no genera, porque las expectativas mal calibradas son el origen de la mayoría de las decepciones con la IA.

**No genera pruebas de rendimiento con datos reales.** El sistema recomienda añadir una prueba de rendimiento con 10.000 registros para REQ-023, pero no puede generarla porque no tiene acceso al volumen real de datos del entorno de staging de Meridian. El QA recibe la recomendación y crea esa prueba manualmente.

**No genera pruebas exploratorias.** El testing exploratorio —el que hace Lucía cuando tiene un rato y empieza a hacer cosas que el sistema no espera— no es reemplazable por el pipeline. El pipeline cubre el espacio de lo documentado; el testing exploratorio cubre el espacio de lo que nadie pensó en documentar.

**No actualiza los test cases automáticamente cuando cambia el requisito.** Si REQ-023 cambia (el capítulo 11 explicará cómo el sistema detecta ese cambio), los test cases existentes en Xray no se actualizan solos. El pipeline puede *regenerar* test cases desde el requisito actualizado, pero la decisión de qué hacer con los test cases anteriores —obsoletos, aún válidos, parcialmente válidos— la toma siempre una persona.

**No reemplaza el juicio experto sobre qué probar primero.** Con nueve test cases disponibles y poco tiempo antes del sprint review, Lucía decide qué ejecuta primero: los dos de prioridad crítica (TC-023-01 y TC-023-04). Esa decisión de priorización no la toma el sistema.

---

## Lo que funciona en la práctica

En Meridian, el equipo de QA adoptó el pipeline de test cases antes que cualquier otro componente. La razón es simple: el dolor era inmediato y el beneficio era inmediato. No había que esperar semanas para medir el impacto.

Lucía, que al principio era la más escéptica del equipo («los test cases automáticos no pueden tener la profundidad que les doy yo»), cambió de posición al tercer sprint. No porque los test cases fueran perfectos —todavía revisa y ajusta algunos datos de prueba—, sino porque le liberaron tiempo para el testing exploratorio y para los casos de integración entre módulos que el pipeline no puede generar.

Su observación más valiosa después de dos meses: «El pipeline es excelente generando los casos que yo haría en el 70% de mi tiempo. Eso me libera para el 30% que de verdad requiere que sepa cómo funciona el negocio».

La primera semana, los analistas descubrieron un patrón: los test cases de contorno eran siempre los que encontraban más bugs en el primer sprint. No porque el pipeline los generara especialmente bien, sino porque antes simplemente no existían. Cero pruebas de contorno encontraban cero bugs de contorno. Cuatro pruebas de contorno encontraban bugs de contorno. La matemática es brutal en su sencillez.

---

## Tres puntos clave

1. La calidad de los test cases generados es inseparable de la calidad de los criterios de aceptación. El pipeline transforma estructuras, no corrige requisitos vagos.

2. Separar las llamadas por tipo de caso —positivos, negativos, contorno— es lo que garantiza cobertura equilibrada. Una sola llamada produce test cases sesgados hacia el flujo feliz.

3. El campo `comportamiento_incorrecto_habitual` es una instrucción de búsqueda activa para el QA, no un campo decorativo. Hace explícito lo que el equipo de desarrollo suele equivocarse, para que el QA sepa exactamente qué buscar.

---

> 💡 **Pregunta de reflexión para tu equipo**
>
> De los requisitos que llegaron al último sprint, ¿cuántos tenían casos de contorno documentados? Si la respuesta es «ninguno» o «alguno», ese es el gap que el pipeline resuelve de forma más inmediata.

---

*El siguiente capítulo construye el sistema que da al pipeline memoria: la arquitectura RAG que permite que la IA conozca el contexto de todo lo que se ha definido antes, y no repita ni contradiga lo que ya existe en el repositorio.*
