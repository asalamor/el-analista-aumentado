# Punto 5 — Generación automática de test cases

Los test cases son donde la inversión en criterios de aceptación bien escritos paga el dividendo más grande. Un AC en formato Gherkin correcto se convierte en un test case casi sin intervención humana.

---

## Arquitectura del pipeline de test cases

El pipeline tiene una lógica diferente al de artefactos Jira. No es lineal sino **ramificado**: desde cada criterio de aceptación se generan múltiples tipos de prueba, y desde las reglas de negocio se generan casos de contorno que el analista normalmente olvida.

```
Historia de usuario
        │
        ├── Criterios de aceptación (AC)
        │         │
        │         ├──[Llamada 1]→ Casos funcionales (flujo feliz)
        │         ├──[Llamada 2]→ Casos negativos y de error
        │         └──[Llamada 3]→ Casos de contorno (boundary values)
        │
        ├── Reglas de negocio
        │         └──[Llamada 4]→ Casos de regla de negocio
        │
        └── Datos de entrada (tipos, rangos, formatos)
                  └──[Llamada 5]→ Casos de validación de datos
                            │
                            ▼
              [Llamada 6] → Scripts Gherkin (Cucumber/Behave)
                            │
                            ▼
              [Llamada 7] → Matriz de cobertura AC↔TC
```

---

## Prompt 0 — System prompt base para QA

Diferente al de generación de artefactos Jira. El modelo debe pensar como un QA engineer, no como un analista.

```
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
- Usuario de prueba por defecto: {{usuario_prueba}}
- Datos de referencia: {{referencia_datos_prueba}}
```

---

## Prompt 1 — Casos funcionales (flujo feliz)

Se ejecuta una vez por historia. Genera los casos del camino principal, uno por cada criterio de aceptación positivo.

```
A partir de la historia de usuario y sus criterios de aceptación, genera
los casos de prueba del flujo principal (happy path).

HISTORIA DE USUARIO:
{{historia_json}}

CRITERIOS DE ACEPTACIÓN POSITIVOS (flujos que deben funcionar):
{{lista_ac_positivos}}

DATOS DE PRUEBA DISPONIBLES EN EL ENTORNO:
{{datos_prueba_disponibles}}

Para cada criterio de aceptación positivo genera UN caso de prueba
con esta estructura:

{
  "test_cases": [
    {
      "id": "TC-{{req_id}}-{{numero_secuencial}}",
      "titulo": "[Verbo] + [funcionalidad] + [condición específica]",
      "tipo": "funcional_positivo",
      "criterio_origen": "{{ac_id}}",
      "historia_origen": "{{historia_id}}",
      "requisito_origen": "{{req_id}}",
      "prioridad": "[critica │ alta │ media │ baja]",
      "precondiciones": [
        "[Estado del sistema antes de iniciar el test]",
        "[Datos que deben existir previamente]",
        "[Permisos o rol del usuario]"
      ],
      "datos_prueba": {
        "[campo_1]": "[valor_concreto]",
        "[campo_2]": "[valor_concreto]"
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "[Qué hace el usuario o el sistema exactamente]",
          "resultado_esperado": "[Qué debe ocurrir. Observable y verificable.]"
        }
      ],
      "resultado_final_esperado": "[Estado final del sistema tras completar todos los pasos]",
      "automatizable": true,
      "notas_automatizacion": "[Selector CSS/XPath clave, endpoint a mockear, etc.]"
    }
  ]
}
```

**Ejemplo de output para AC-023-01:**

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
        "Usuario autenticado con rol gestor_facturacion (usuario: gestor01@empresa.com)",
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
          "resultado_esperado": "Se carga el listado de facturas con el panel de filtros visible"
        },
        {
          "numero": 2,
          "accion": "Introducir '2024-01-01' en el campo 'Desde'",
          "resultado_esperado": "El campo muestra la fecha 01/01/2024 formateada"
        },
        {
          "numero": 3,
          "accion": "Introducir '2024-03-31' en el campo 'Hasta'",
          "resultado_esperado": "El campo muestra la fecha 31/03/2024 formateada"
        },
        {
          "numero": 4,
          "accion": "Pulsar el botón 'Buscar'",
          "resultado_esperado": "Aparece un indicador de carga (spinner o skeleton)"
        },
        {
          "numero": 5,
          "accion": "Esperar a que carguen los resultados",
          "resultado_esperado": "El listado muestra facturas en menos de 2 segundos. La primera factura tiene fecha igual o anterior a 2024-03-31. La última factura visible tiene fecha igual o posterior a 2024-01-01."
        },
        {
          "numero": 6,
          "accion": "Verificar el orden de las facturas",
          "resultado_esperado": "Las facturas están ordenadas por fecha de forma descendente (la más reciente primero)"
        },
        {
          "numero": 7,
          "accion": "Verificar el contador de resultados",
          "resultado_esperado": "Se muestra un texto del tipo 'X facturas encontradas' con un número mayor que 0"
        }
      ],
      "resultado_final_esperado": "El listado muestra todas las facturas del período 2024-Q1, ordenadas por fecha descendente, con el contador de resultados visible",
      "automatizable": true,
      "notas_automatizacion": "Selector campo Desde: #filter-date-from. Selector campo Hasta: #filter-date-to. Botón buscar: [data-testid='btn-search']. Contador: [data-testid='results-count']"
    }
  ]
}
```

---

## Prompt 2 — Casos negativos y de error

Este prompt es donde la IA aporta más valor que un QA humano bajo presión de tiempo: **sistemáticamente genera todos los casos de error**, no solo los obvios.

```
A partir de la historia de usuario, genera TODOS los casos de prueba negativos
y de error posibles. Sé exhaustivo: estos casos son donde viven la mayoría
de los bugs en producción.

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
  ¿Qué pasa si un usuario sin permiso intenta ejecutar la acción?

CATEGORÍA D — Concurrencia y estado:
  ¿Qué pasa si el recurso ya no existe cuando se ejecuta la acción?
  ¿Qué pasa si dos usuarios actúan simultáneamente?

CATEGORÍA E — Errores de sistema:
  ¿Qué pasa si el servicio externo o BD no responde?

Usa la misma estructura JSON que los casos positivos, con
"tipo": "[negativo_validacion │ negativo_permiso │ negativo_regla_negocio │ negativo_concurrencia │ negativo_sistema]"

Para cada caso negativo incluye:
"comportamiento_incorrecto_habitual": "[Error típico que cometen los desarrolladores
en este caso, para que el QA lo busque específicamente]"
```

**Ejemplo de output — casos negativos para US-047:**

```json
{
  "test_cases": [
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
          "resultado_esperado": "Los campos aceptan los valores introducidos sin error visual"
        },
        {
          "numero": 2,
          "accion": "Pulsar el botón 'Buscar'",
          "resultado_esperado": "El sistema NO ejecuta ninguna consulta a la base de datos. Los campos fecha_inicio y fecha_fin se resaltan en rojo. Aparece el mensaje exacto: 'El rango no puede superar 365 días'."
        },
        {
          "numero": 3,
          "accion": "Verificar que no aparecen resultados en el listado",
          "resultado_esperado": "El listado permanece en su estado anterior, sin mostrar nuevas filas ni estado vacío"
        }
      ],
      "resultado_final_esperado": "Validación activa, sin consulta ejecutada, mensaje de error visible",
      "automatizable": true,
      "comportamiento_incorrecto_habitual": "El desarrollador ejecuta la consulta y después valida, mostrando resultados un instante antes del error. O valida el error pero no resalta los campos."
    },
    {
      "id": "TC-023-03",
      "titulo": "Buscar sin introducir fecha de inicio muestra error de campo obligatorio",
      "tipo": "negativo_validacion",
      "criterio_origen": "AC-023-01",
      "prioridad": "alta",
      "precondiciones": ["Usuario autenticado con rol gestor_facturacion"],
      "datos_prueba": {
        "fecha_inicio": "",
        "fecha_fin": "2024-03-31"
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "Navegar a /facturas, dejar el campo 'Desde' vacío e introducir fecha_fin='2024-03-31'",
          "resultado_esperado": "El campo 'Hasta' muestra la fecha. El campo 'Desde' está vacío."
        },
        {
          "numero": 2,
          "accion": "Pulsar el botón 'Buscar'",
          "resultado_esperado": "El campo 'Desde' se resalta como campo obligatorio con un mensaje de validación. No se ejecuta ninguna búsqueda."
        }
      ],
      "resultado_final_esperado": "Error de validación en campo obligatorio visible. Sin resultados mostrados.",
      "automatizable": true,
      "comportamiento_incorrecto_habitual": "El sistema usa la fecha mínima del sistema como valor por defecto silencioso, ejecutando una consulta no intencionada."
    },
    {
      "id": "TC-023-04",
      "titulo": "Usuario sin rol gestor_facturacion no puede acceder al módulo Facturas",
      "tipo": "negativo_permiso",
      "criterio_origen": "AC-023-01",
      "prioridad": "critica",
      "precondiciones": ["Usuario autenticado con rol consultor_basico (sin acceso a facturación)"],
      "datos_prueba": {
        "usuario": "consultor01@empresa.com",
        "rol": "consultor_basico"
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "Navegar directamente a la URL /facturas",
          "resultado_esperado": "El sistema redirige a la página de acceso denegado o muestra un mensaje HTTP 403. No se carga el módulo ni se muestran datos."
        }
      ],
      "resultado_final_esperado": "Acceso denegado. Ningún dato de facturación visible.",
      "automatizable": true,
      "comportamiento_incorrecto_habitual": "El menú de navegación oculta el enlace pero la URL directa sigue siendo accesible (seguridad solo en frontend)."
    },
    {
      "id": "TC-023-05",
      "titulo": "Búsqueda válida sin resultados muestra estado vacío con opción de ampliar",
      "tipo": "funcional_positivo",
      "criterio_origen": "AC-023-03",
      "prioridad": "media",
      "precondiciones": [
        "Usuario autenticado con rol gestor_facturacion",
        "No existen facturas en BD con fechas entre 2000-01-01 y 2000-01-31"
      ],
      "datos_prueba": {
        "fecha_inicio": "2000-01-01",
        "fecha_fin": "2000-01-31"
      },
      "pasos": [
        {
          "numero": 1,
          "accion": "Introducir fecha_inicio='2000-01-01' y fecha_fin='2000-01-31' y pulsar 'Buscar'",
          "resultado_esperado": "La consulta se ejecuta correctamente (sin error)"
        },
        {
          "numero": 2,
          "accion": "Observar el área de resultados",
          "resultado_esperado": "Se muestra el estado vacío con el texto exacto 'No se encontraron facturas para el período seleccionado' y el botón 'Ampliar búsqueda' visible"
        },
        {
          "numero": 3,
          "accion": "Pulsar el botón 'Ampliar búsqueda'",
          "resultado_esperado": "Los campos de fecha se limpian o se amplía el rango de forma asistida"
        }
      ],
      "resultado_final_esperado": "Estado vacío informativo con acción de recuperación disponible",
      "automatizable": true,
      "comportamiento_incorrecto_habitual": "Se muestra un estado vacío genérico sin mensaje específico, o se muestra un error de sistema en lugar del estado vacío diseñado."
    }
  ]
}
```

---

## Prompt 3 — Casos de contorno (boundary values)

Este prompt es **el más ignorado por los QAs humanos bajo presión** y donde la IA recupera más valor. Analiza automáticamente todos los campos con rangos y genera los casos de contorno exactos.

```
Analiza todos los campos con restricciones numéricas, de longitud o de fecha
en el siguiente requisito y genera los casos de prueba de valores límite.

REQUISITO:
{{requisito_yaml}}

REGLA DE CONTORNO ESTÁNDAR:
Para cada restricción, genera exactamente estos 4 casos:
  - Valor en el límite inferior exacto → debe funcionar (PASS)
  - Valor un paso por debajo del límite inferior → debe fallar (FAIL)
  - Valor en el límite superior exacto → debe funcionar (PASS)
  - Valor un paso por encima del límite superior → debe fallar (FAIL)

"Un paso" significa:
  - Para enteros: ±1
  - Para fechas: ±1 día
  - Para texto: ±1 carácter
  - Para decimales: la precisión mínima del campo (ej: ±0.01 para 2 decimales)

Para cada restricción identificada genera los 4 casos con "tipo": "contorno"
y el campo "valor_limite" que especifica qué restricción se está probando.
```

**Ejemplo de output:**

```json
{
  "restricciones_identificadas": [
    {
      "campo": "rango_fechas",
      "restriccion": "máximo 365 días entre fecha_inicio y fecha_fin",
      "test_cases": [
        {
          "id": "TC-023-06",
          "titulo": "Rango de exactamente 365 días es aceptado",
          "tipo": "contorno",
          "valor_limite": "límite superior exacto — debe pasar",
          "datos_prueba": {
            "fecha_inicio": "2023-01-01",
            "fecha_fin": "2023-12-31",
            "dias_diferencia": 364
          },
          "resultado_esperado": "La búsqueda se ejecuta correctamente sin mensaje de error",
          "prioridad": "alta"
        },
        {
          "id": "TC-023-07",
          "titulo": "Rango de 366 días es rechazado",
          "tipo": "contorno",
          "valor_limite": "límite superior + 1 — debe fallar",
          "datos_prueba": {
            "fecha_inicio": "2023-01-01",
            "fecha_fin": "2024-01-02",
            "dias_diferencia": 366
          },
          "resultado_esperado": "El sistema muestra el mensaje de validación. No se ejecuta la búsqueda.",
          "prioridad": "alta"
        },
        {
          "id": "TC-023-08",
          "titulo": "Rango de un solo día es aceptado",
          "tipo": "contorno",
          "valor_limite": "límite inferior exacto — debe pasar",
          "datos_prueba": {
            "fecha_inicio": "2024-03-15",
            "fecha_fin": "2024-03-15",
            "dias_diferencia": 0
          },
          "resultado_esperado": "La búsqueda se ejecuta y devuelve facturas de ese día (o estado vacío si no hay)",
          "prioridad": "media"
        },
        {
          "id": "TC-023-09",
          "titulo": "fecha_fin anterior a fecha_inicio es rechazada",
          "tipo": "contorno",
          "valor_limite": "límite inferior - 1 — debe fallar",
          "datos_prueba": {
            "fecha_inicio": "2024-03-15",
            "fecha_fin": "2024-03-14",
            "dias_diferencia": -1
          },
          "resultado_esperado": "El sistema muestra un error de validación indicando que la fecha de fin no puede ser anterior a la de inicio",
          "prioridad": "alta"
        }
      ]
    }
  ]
}
```

---

## Prompt 4 — Scripts Gherkin para automatización

Una vez generados los casos de prueba, este prompt los convierte en **feature files ejecutables** para Cucumber, Behave o Playwright + Cucumber.

```
Convierte los siguientes casos de prueba en scripts Gherkin (BDD) listos
para ejecutarse con Cucumber o Behave.

CASOS DE PRUEBA:
{{test_cases_json}}

REGLAS DE FORMATO GHERKIN:
- Usa Background para las precondiciones comunes a todos los escenarios.
- Usa Scenario Outline + Examples cuando varios casos usan la misma
  estructura con diferentes datos.
- Los steps (Dado/Cuando/Entonces) deben ser reutilizables:
  escríbelos pensando en que existirá un step definition que los implementa.
- Incluye tags por prioridad (@critica, @alta, @media),
  por tipo (@positivo, @negativo, @contorno) y por historia (@US-047).
- Los datos van en la tabla Examples o como parámetros entre comillas dobles.
- Usa el idioma configurado en el proyecto: {{idioma_gherkin}}

Genera el feature file completo como string dentro del JSON:

{
  "feature_file": {
    "nombre_archivo": "{{nombre_funcionalidad}}.feature",
    "contenido": "[CONTENIDO COMPLETO DEL FEATURE FILE]",
    "step_definitions_sugeridos": [
      {
        "step": "[Texto del step]",
        "patron_regex": "[Regex para el step definition]",
        "notas_implementacion": "[Qué debe hacer el step definition]"
      }
    ]
  }
}
```

**Ejemplo de feature file generado:**

```gherkin
# language: es
@facturacion @US-047 @REQ-023
Característica: Filtrado de facturas por rango de fechas
  Como gestor de facturación
  Quiero filtrar el listado de facturas por rango de fechas
  Para localizar rápidamente facturas de un período contable concreto

  Antecedentes:
    Dado que el usuario "gestor01@empresa.com" está autenticado con rol "gestor_facturacion"
    Y que accede al módulo "Facturas"
    Y que existen facturas en el sistema con fechas entre "2024-01-01" y "2024-03-31"

  @critica @positivo @TC-023-01
  Esquema del escenario: Filtrado válido devuelve resultados ordenados
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
    Dado que el usuario "consultor01@empresa.com" está autenticado con rol "consultor_basico"
    Cuando navega directamente a la URL "/facturas"
    Entonces el sistema deniega el acceso
    Y no se muestran datos de facturación

  @media @positivo @TC-023-05
  Escenario: Búsqueda sin resultados muestra estado vacío con acción
    Dado que introduce la fecha de inicio "2000-01-01"
    Y que introduce la fecha de fin "2000-01-31"
    Cuando pulsa el botón "Buscar"
    Entonces se muestra el mensaje "No se encontraron facturas para el período seleccionado"
    Y se muestra el botón "Ampliar búsqueda"

  @alta @contorno @TC-023-06 @TC-023-07
  Esquema del escenario: Casos de contorno del límite de 365 días
    Dado que introduce la fecha de inicio "<fecha_inicio>"
    Y que introduce la fecha de fin "<fecha_fin>"
    Cuando pulsa el botón "Buscar"
    Entonces el resultado es "<resultado>"

    Ejemplos:
      | fecha_inicio | fecha_fin  | dias | resultado                        |
      | 2023-01-01   | 2023-12-31 | 364  | búsqueda ejecutada correctamente |
      | 2023-01-01   | 2024-01-02 | 366  | error de validación mostrado     |
      | 2024-03-15   | 2024-03-15 | 0    | búsqueda ejecutada correctamente |
      | 2024-03-15   | 2024-03-14 | -1   | error de validación mostrado     |
```

---

## Prompt 5 — Matriz de cobertura AC ↔ TC

Este prompt genera la **trazabilidad automática** entre criterios de aceptación y casos de prueba, el documento que más tiempo cuesta mantener manualmente y que más se desactualiza.

```
A partir de la historia de usuario y los test cases generados, produce
la matriz de cobertura completa.

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
        "descripcion_resumida": "[Qué verifica este AC]",
        "test_cases_asociados": {
          "positivos": ["TC-023-01"],
          "negativos": ["TC-023-02", "TC-023-03"],
          "contorno": ["TC-023-06", "TC-023-07", "TC-023-08", "TC-023-09"]
        },
        "cobertura": "completa │ parcial │ sin_cobertura",
        "gaps_detectados": ["[Escenario no cubierto si los hay]"]
      }
    ],
    "tipos_prueba_generados": {
      "funcionales_positivos": N,
      "negativos_validacion": N,
      "negativos_permiso": N,
      "negativos_regla_negocio": N,
      "contorno": N,
      "total": N
    },
    "recomendaciones": [
      "[Test adicional recomendado no derivable de los AC actuales]"
    ]
  }
}
```

**Ejemplo de matriz generada para US-047:**

```json
{
  "matriz_cobertura": {
    "historia_id": "US-047",
    "fecha_generacion": "2025-05-06",
    "resumen": {
      "total_ac": 3,
      "total_tc": 9,
      "ac_con_cobertura_completa": 3,
      "ac_con_cobertura_parcial": 0,
      "ac_sin_cobertura": 0,
      "porcentaje_cobertura": "100%"
    },
    "cobertura_por_ac": [
      {
        "ac_id": "AC-023-01",
        "descripcion_resumida": "Filtrado válido devuelve resultados ordenados en < 2 segundos",
        "test_cases_asociados": {
          "positivos": ["TC-023-01"],
          "negativos": ["TC-023-03", "TC-023-04"],
          "contorno": ["TC-023-06", "TC-023-07", "TC-023-08", "TC-023-09"]
        },
        "cobertura": "completa",
        "gaps_detectados": []
      },
      {
        "ac_id": "AC-023-02",
        "descripcion_resumida": "Rango > 365 días bloquea la búsqueda y muestra error",
        "test_cases_asociados": {
          "positivos": [],
          "negativos": ["TC-023-02"],
          "contorno": ["TC-023-07"]
        },
        "cobertura": "completa",
        "gaps_detectados": []
      },
      {
        "ac_id": "AC-023-03",
        "descripcion_resumida": "Sin resultados muestra estado vacío con botón de acción",
        "test_cases_asociados": {
          "positivos": ["TC-023-05"],
          "negativos": [],
          "contorno": []
        },
        "cobertura": "completa",
        "gaps_detectados": []
      }
    ],
    "tipos_prueba_generados": {
      "funcionales_positivos": 2,
      "negativos_validacion": 2,
      "negativos_permiso": 1,
      "negativos_regla_negocio": 1,
      "contorno": 4,
      "total": 10
    },
    "recomendaciones": [
      "Añadir prueba de rendimiento con 10.000 registros en staging (no derivable de los AC actuales)",
      "Considerar prueba de sesión expirada durante una búsqueda activa",
      "Validar comportamiento con zona horaria diferente a la del servidor"
    ]
  }
}
```

---

## Integración con Xray y Zephyr Scale

Una vez generados los test cases en JSON, el push a las herramientas de QA es directo.

**Para Xray (Jira nativo):**

```python
# El JSON generado se transforma al formato de importación de Xray
import requests

def push_test_cases_to_xray(test_cases, jira_config):
    xray_payload = {
        "testExecution": {
            "projectKey": jira_config["project_key"],
            "summary": f"Test cases generados automáticamente - {test_cases[0]['historia_origen']}",
            "description": "Generados desde criterios de aceptación via pipeline IA"
        },
        "tests": [
            {
                "testKey": tc.get("jira_key"),  # Si ya existe en Xray
                "summary": tc["titulo"],
                "type": "Manual",
                "steps": [
                    {
                        "action": paso["accion"],
                        "result": paso["resultado_esperado"]
                    }
                    for paso in tc["pasos"]
                ],
                "precondition": "\n".join(tc["precondiciones"]),
                "labels": [tc["tipo"], tc["criterio_origen"]]
            }
            for tc in test_cases
        ]
    }

    response = requests.post(
        f"{jira_config['base_url']}/rest/raven/1.0/import/test",
        json=xray_payload,
        auth=(jira_config["user"], jira_config["token"])
    )
    return response.json()
```

---

## Qué hacer hoy mismo sin automatización

Al igual que con los prompts de Jira, puedes empezar a usar esto **manualmente esta semana**:

1. Toma un criterio de aceptación de un requisito real de tu proyecto.
2. Pega el System Prompt QA + el Prompt 2 en Claude.
3. Observa cuántos casos negativos genera que normalmente no se documentarían hasta que aparece el bug.
4. Usa los casos de contorno del Prompt 3 en la próxima sesión de refinamiento para mostrar al equipo el valor de los requisitos bien estructurados.

El retorno es inmediato: **de un solo AC bien escrito, estos prompts generan entre 4 y 8 test cases** que un QA humano tardaría entre 30 y 60 minutos en redactar, y que habitualmente quedan incompletos por falta de tiempo.

---

A continuación: [Punto 6 — Validación automática de calidad de requisitos.](./106-validacion-calidad.md)

---
