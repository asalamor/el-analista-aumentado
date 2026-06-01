# Punto 6 — Validación automática de calidad de requisitos

La validación automática es la **red de seguridad de todo el pipeline**: si entra un requisito ambiguo, todo lo que se genera aguas abajo hereda esa ambigüedad. Un checklist automático ejecutado antes del Prompt 1 evita que el problema se multiplique.

---

## Por qué la validación merece su propio pipeline

La tentación es incluir la validación como un paso dentro del prompt de generación. Es un error. Los motivos son tres.

Primero, **mezclar generación y validación degrada la calidad de ambas**. El modelo optimiza para generar algo, no para encontrar fallos. Segundo, **la validación necesita contexto externo** que la generación no usa: el glosario, los otros requisitos del mismo módulo, las reglas de negocio globales del proyecto. Tercero, **los errores de validación deben bloquear el pipeline**, no ser notas al pie de un JSON de historia generada que nadie leerá.

El resultado es un pipeline separado con cuatro llamadas especializadas, cada una buscando un tipo de problema diferente.

---

## Arquitectura del pipeline de validación

```
YAML de requisito candidato
         │
         ▼
[Llamada 1] Validación estructural
  ¿Están todos los campos obligatorios?
  ¿Tienen el formato correcto?
         │
         ▼ (solo si pasa)
[Llamada 2] Validación semántica
  ¿Es ambiguo? ¿Es verificable?
  ¿Mezcla responsabilidades?
         │
         ▼ (solo si pasa)
[Llamada 3] Validación de consistencia
  ¿Contradice otros requisitos?
  ¿Usa términos del glosario?
  ¿La épica es coherente?
         │
         ▼ (solo si pasa)
[Llamada 4] Validación de completitud funcional
  ¿Están los flujos de error?
  ¿Están los casos de contorno?
  ¿Los datos de entrada tienen tipos y validaciones?
         │
         ▼
Informe consolidado de validación
  APROBADO → entra al pipeline de generación
  APROBADO CON ADVERTENCIAS → entra con alertas visibles
  BLOQUEADO → devuelto al analista con diagnóstico
```

---

## Prompt 0 — System prompt base para validación

```
Eres un auditor de calidad de requisitos funcionales con experiencia
en proyectos Agile enterprise. Tu función es detectar problemas en
requisitos funcionales ANTES de que entren en un pipeline de generación
de artefactos.

Tu sesgo debe ser conservador: ante la duda, marca el problema.
Es mejor un falso positivo que un requisito ambiguo en producción.

REGLAS DE COMPORTAMIENTO:
1. No generes contenido nuevo ni corrijas el requisito.
   Solo diagnostica. Las correcciones las hace el analista.
2. Para cada problema encontrado, indica:
   - Qué campo o sección lo contiene
   - Por qué es un problema (consecuencia concreta)
   - Un ejemplo de cómo debería expresarse correctamente
3. Clasifica cada problema como:
   BLOQUEANTE → impide la generación correcta de artefactos
   ADVERTENCIA → degrada la calidad pero no impide la generación
   SUGERENCIA → mejora opcional
4. Un requisito con un solo problema BLOQUEANTE se rechaza completamente.
5. El output es siempre JSON válido. Sin texto fuera del JSON.

GLOSARIO OFICIAL DEL PROYECTO:
{{glosario_yaml}}

REQUISITOS DEL MISMO MÓDULO (para detectar contradicciones y duplicados):
{{requisitos_mismo_modulo}}

REGLAS DE NEGOCIO GLOBALES DEL PROYECTO:
{{reglas_negocio_globales}}
```

---

## Prompt 1 — Validación estructural

El más rápido de ejecutar. Verifica que el YAML tiene todos los campos y que tienen el formato correcto. No requiere razonamiento semántico, solo comprobación contra un esquema.

```
Valida que el siguiente requisito tiene todos los campos obligatorios
con el formato correcto.

REQUISITO A VALIDAR:
{{requisito_yaml}}

ESQUEMA OBLIGATORIO:
campos_requeridos:
  - id:               [formato: REQ-NNN, donde NNN es numérico de 3 dígitos]
  - titulo:           [no vacío, máximo 80 caracteres, sin verbos ambiguos]
  - epica:            [formato: EP-NN]
  - actor:            [debe existir en el glosario de actores]
  - prioridad:        [valores: must-have | should-have | could-have | wont-have]
  - estado:           [valores: borrador | en-revision | validado | rechazado]
  - descripcion:      [mínimo 30 palabras]
  - evento_disparador:[no vacío]
  - criterios_aceptacion: [mínimo 1 criterio]
    cada_criterio:
      - id:     [formato: AC-NNN-NN]
      - dado:   [no vacío]
      - cuando: [no vacío]
      - entonces: [no vacío]
  - datos_entrada:    [si existen, deben tener nombre y tipo]
  - excepciones:      [mínimo 1 excepción]
  - origen:           [no vacío]

VERBOS AMBIGUOS PROHIBIDOS EN EL TÍTULO:
[gestionar, manejar, administrar, controlar, procesar, tratar,
 permitir, posibilitar, facilitar, mejorar, optimizar, soportar]

Genera:
{
  "validacion_estructural": {
    "requisito_id": "{{req_id}}",
    "timestamp": "{{timestamp}}",
    "resultado": "APROBADO | BLOQUEADO",
    "problemas": [
      {
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "campo": "[campo afectado]",
        "problema": "[descripción del problema]",
        "valor_actual": "[valor que tiene el campo]",
        "valor_esperado": "[formato o valor correcto]",
        "ejemplo_correcto": "[ejemplo concreto]"
      }
    ],
    "campos_validados": N,
    "campos_con_problema": N
  }
}
```

### Ejemplo de output — requisito con problemas estructurales

```json
{
  "validacion_estructural": {
    "requisito_id": "REQ-031",
    "timestamp": "2025-05-06T09:14:00Z",
    "resultado": "BLOQUEADO",
    "problemas": [
      {
        "severidad": "BLOQUEANTE",
        "campo": "titulo",
        "problema": "El título contiene el verbo ambiguo 'gestionar', que no especifica qué operación concreta se realiza",
        "valor_actual": "Gestionar las notificaciones del usuario",
        "valor_esperado": "Título que indique la acción concreta: crear, consultar, filtrar, exportar, desactivar...",
        "ejemplo_correcto": "Desactivar notificaciones por categoría desde el perfil de usuario"
      },
      {
        "severidad": "BLOQUEANTE",
        "campo": "criterios_aceptacion",
        "problema": "El campo 'entonces' del criterio AC-031-01 está vacío",
        "valor_actual": "",
        "valor_esperado": "Resultado observable y verificable que el sistema produce",
        "ejemplo_correcto": "Entonces el sistema muestra un mensaje de confirmación 'Notificaciones de Marketing desactivadas' y el toggle aparece en posición OFF"
      },
      {
        "severidad": "ADVERTENCIA",
        "campo": "excepciones",
        "problema": "El campo excepciones no contiene ningún valor",
        "valor_actual": "[]",
        "valor_esperado": "Al menos una excepción o flujo de error documentado",
        "ejemplo_correcto": "- El usuario no tiene notificaciones activas: mostrar mensaje informativo sin error"
      },
      {
        "severidad": "SUGERENCIA",
        "campo": "descripcion",
        "problema": "La descripción tiene 18 palabras, por debajo del mínimo de 30",
        "valor_actual": "El usuario podrá gestionar sus notificaciones desde su perfil.",
        "valor_esperado": "Descripción de al menos 30 palabras con contexto de negocio",
        "ejemplo_correcto": "El usuario registrado necesita poder desactivar categorías de notificaciones desde su perfil sin necesidad de contactar con soporte, reduciendo las solicitudes de baja de comunicaciones en un 40%."
      }
    ],
    "campos_validados": 12,
    "campos_con_problema": 3
  }
}
```

---

## Prompt 2 — Validación semántica

El más valioso. Detecta los problemas que el esquema no puede ver: ambigüedad, mezcla de responsabilidades, criterios no verificables.

```
Analiza el contenido semántico del siguiente requisito en busca de
ambigüedades, inconsistencias internas y problemas de calidad funcional.

REQUISITO A VALIDAR:
{{requisito_yaml}}

ANÁLISIS REQUERIDO:

BLOQUE A — Ambigüedad lingüística
Busca en TODOS los campos de texto:
  - Cuantificadores vagos: rápido, eficiente, adecuado, correcto,
    fácil, intuitivo, robusto, escalable, flexible, suficiente
  - Verbos sin sujeto definido: "se podrá", "se mostrará", "se enviará"
    (¿quién lo hace? ¿el sistema? ¿el usuario? ¿un proceso batch?)
  - Condiciones implícitas: "si es necesario", "cuando corresponda",
    "según proceda", "en su caso"
  - Plurales sin cuantificar: "los documentos", "los usuarios"
    (¿todos? ¿algunos? ¿cuántos?)

BLOQUE B — Verificabilidad de criterios de aceptación
Para cada criterio Dado/Cuando/Entonces verifica:
  - ¿Puede responderse con PASS o FAIL mediante una prueba concreta?
  - ¿El 'dado' describe un estado del sistema, no una acción?
  - ¿El 'cuando' describe UNA acción concreta, no un proceso complejo?
  - ¿El 'entonces' describe algo OBSERVABLE externamente?
  - ¿Hay datos concretos o usa placeholders vagos?

BLOQUE C — Atomicidad
  - ¿El requisito mezcla más de una funcionalidad diferente?
    (síntoma: el título tiene "y", "también", "además")
  - ¿Un único criterio de aceptación verifica más de una cosa?
    (síntoma: el 'entonces' tiene más de 3 condiciones no relacionadas)

BLOQUE D — Completitud lógica
  - ¿Cada regla de negocio tiene su correspondiente criterio de aceptación?
  - ¿Los flujos de error están documentados o solo el flujo feliz?
  - ¿Los datos de entrada tienen validaciones definidas?

Genera:
{
  "validacion_semantica": {
    "requisito_id": "{{req_id}}",
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "puntuacion_calidad": N,
    "escala_puntuacion": "0-100 donde 100 es calidad perfecta",
    "analisis_por_bloque": {
      "ambiguedad": {
        "resultado": "LIMPIO | PROBLEMAS_ENCONTRADOS",
        "problemas": []
      },
      "verificabilidad": {
        "resultado": "LIMPIO | PROBLEMAS_ENCONTRADOS",
        "problemas": []
      },
      "atomicidad": {
        "resultado": "LIMPIO | PROBLEMAS_ENCONTRADOS",
        "problemas": []
      },
      "completitud_logica": {
        "resultado": "LIMPIO | PROBLEMAS_ENCONTRADOS",
        "problemas": []
      }
    },
    "problemas_consolidados": [
      {
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "bloque": "ambiguedad | verificabilidad | atomicidad | completitud_logica",
        "ubicacion": "[campo exacto y fragmento de texto problemático]",
        "problema": "[descripción del problema y su consecuencia]",
        "ejemplo_correcto": "[cómo debería expresarse]"
      }
    ]
  }
}
```

### Ejemplo de output con un requisito semánticamente deficiente

```json
{
  "validacion_semantica": {
    "requisito_id": "REQ-028",
    "resultado": "BLOQUEADO",
    "puntuacion_calidad": 34,
    "escala_puntuacion": "0-100 donde 100 es calidad perfecta",
    "analisis_por_bloque": {
      "ambiguedad": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "descripcion → 'el sistema debe responder de forma rápida'",
            "problema": "'Rápida' no es verificable. No hay umbral de tiempo definido. La IA generará un criterio de aceptación igualmente vago y el equipo de QA no sabrá qué medir.",
            "ejemplo_correcto": "'El sistema debe devolver los resultados en menos de 1,5 segundos para el percentil 95 de las peticiones bajo carga normal de 100 usuarios concurrentes'"
          },
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "criterios_aceptacion[0].cuando → 'cuando se realizan las operaciones necesarias'",
            "problema": "'Las operaciones necesarias' no especifica qué acción concreta ejecuta el actor. La IA no puede generar un paso de test verificable a partir de esto.",
            "ejemplo_correcto": "'cuando el gestor pulsa el botón Exportar y selecciona el formato CSV'"
          },
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "reglas_negocio[1] → 'solo los usuarios autorizados podrán acceder'",
            "problema": "'Usuarios autorizados' no define qué roles concretos tienen acceso. El equipo de desarrollo implementará restricciones diferentes a las esperadas.",
            "ejemplo_correcto": "'Solo los usuarios con rol gestor_facturacion o responsable_financiero pueden acceder a la exportación'"
          }
        ]
      },
      "verificabilidad": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "criterios_aceptacion[1].entonces → 'el sistema funciona correctamente'",
            "problema": "'Funciona correctamente' no describe ningún comportamiento observable. Es imposible escribir un test que valide esto.",
            "ejemplo_correcto": "'el sistema genera el archivo facturas_Q1_2024.csv con exactamente N filas, una por factura del período, y lo descarga automáticamente'"
          }
        ]
      },
      "atomicidad": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "titulo → 'Exportar facturas y configurar preferencias de exportación'",
            "problema": "El requisito mezcla dos funcionalidades distintas: la exportación puntual y la configuración de preferencias. Deben ser dos requisitos separados con sus propias historias y criterios.",
            "ejemplo_correcto": "REQ-028a: 'Exportar listado de facturas filtradas a formato CSV' / REQ-028b: 'Configurar formato y campos por defecto para exportación de facturas'"
          }
        ]
      },
      "completitud_logica": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "excepciones",
            "problema": "No se documenta qué ocurre si el conjunto de resultados a exportar supera el límite de memoria del servidor o un número máximo de registros.",
            "ejemplo_correcto": "- Si el resultado contiene más de 50.000 registros, el sistema muestra el mensaje 'El volumen de datos supera el límite de exportación directa. Use la exportación programada.' y no genera el archivo."
          }
        ]
      }
    },
    "problemas_consolidados": [
      {
        "severidad": "BLOQUEANTE",
        "bloque": "atomicidad",
        "ubicacion": "titulo",
        "problema": "El requisito mezcla dos funcionalidades. Debe dividirse en REQ-028a y REQ-028b.",
        "ejemplo_correcto": "Ver análisis de atomicidad"
      }
    ]
  }
}
```

---

## Prompt 3 — Validación de consistencia

Requiere contexto externo: el glosario y los otros requisitos del módulo. Es la llamada que más se beneficia de RAG cuando el repositorio crece.

```
Valida que el siguiente requisito es consistente con el resto del proyecto.

REQUISITO A VALIDAR:
{{requisito_yaml}}

GLOSARIO OFICIAL (términos y definiciones canónicas):
{{glosario_yaml}}

OTROS REQUISITOS DEL MISMO MÓDULO {{epica_id}}:
{{requisitos_mismo_modulo_yaml}}

REGLAS DE NEGOCIO GLOBALES DEL PROYECTO:
{{reglas_negocio_globales}}

ANÁLISIS REQUERIDO:

BLOQUE A — Consistencia terminológica
  ¿Se usan los términos del glosario con sus nombres exactos?
  ¿Se usan sinónimos no oficiales que crearán entidades distintas en Jira?
  Ejemplos comunes: cliente/usuario/cuenta, pedido/orden/solicitud,
  módulo/sección/pantalla/vista

BLOQUE B — Contradicciones con otros requisitos
  ¿Alguna regla de negocio de este requisito contradice las de otro?
  ¿Algún comportamiento definido aquí entra en conflicto con
  el de otro requisito del mismo módulo?
  ¿Los datos de entrada/salida son compatibles con los de requisitos
  que comparten el mismo flujo?

BLOQUE C — Duplicidad
  ¿Existe ya un requisito que cubre total o parcialmente
  la misma funcionalidad?
  ¿Podría fusionarse con otro requisito existente o es realmente distinto?

BLOQUE D — Coherencia con la épica
  ¿La funcionalidad descrita pertenece realmente al módulo {{epica_id}}?
  ¿Debería estar en una épica diferente?

Genera:
{
  "validacion_consistencia": {
    "requisito_id": "{{req_id}}",
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "analisis_por_bloque": {
      "terminologia": { "resultado": "...", "problemas": [] },
      "contradicciones": { "resultado": "...", "problemas": [] },
      "duplicidad": { "resultado": "...", "problemas": [] },
      "coherencia_epica": { "resultado": "...", "problemas": [] }
    },
    "problemas_consolidados": [
      {
        "severidad": "BLOQUEANTE | ADVERTENCIA | SUGERENCIA",
        "bloque": "...",
        "ubicacion": "...",
        "problema": "...",
        "requisito_en_conflicto": "REQ-NNN (si aplica)",
        "ejemplo_correcto": "..."
      }
    ]
  }
}
```

### Ejemplo de output — problema de terminología y contradicción

```json
{
  "validacion_consistencia": {
    "requisito_id": "REQ-035",
    "resultado": "BLOQUEADO",
    "analisis_por_bloque": {
      "terminologia": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "actor → 'Cliente registrado'",
            "problema": "El término oficial en el glosario es 'Usuario autenticado'. 'Cliente registrado' es un sinónimo no oficial que, al llegar a Jira, creará historias con dos entidades distintas para el mismo rol.",
            "termino_oficial": "Usuario autenticado",
            "ejemplo_correcto": "Sustituir 'Cliente registrado' por 'Usuario autenticado' en todos los campos del requisito"
          }
        ]
      },
      "contradicciones": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "BLOQUEANTE",
            "ubicacion": "reglas_negocio[0] → 'El usuario puede tener múltiples direcciones de facturación activas'",
            "problema": "REQ-018 (del mismo módulo EP-04) establece: 'Cada usuario tiene exactamente una dirección de facturación activa en cada momento'. Las dos reglas son contradictorias.",
            "requisito_en_conflicto": "REQ-018",
            "ejemplo_correcto": "Alinear ambos requisitos antes de continuar. Si la regla ha cambiado, actualizar REQ-018 explícitamente y registrar la decisión en el historial de cambios."
          }
        ]
      },
      "duplicidad": {
        "resultado": "LIMPIO",
        "problemas": []
      },
      "coherencia_epica": {
        "resultado": "LIMPIO",
        "problemas": []
      }
    },
    "problemas_consolidados": [
      {
        "severidad": "BLOQUEANTE",
        "bloque": "contradicciones",
        "ubicacion": "reglas_negocio[0]",
        "problema": "Contradicción directa con REQ-018. Requiere decisión de negocio antes de continuar.",
        "requisito_en_conflicto": "REQ-018",
        "ejemplo_correcto": "Convocar sesión de resolución con el stakeholder responsable de ambos requisitos"
      }
    ]
  }
}
```

---

## Prompt 4 — Validación de completitud funcional

El más especializado. Actúa como un QA senior que pregunta «¿y qué pasa si...?» sobre cada aspecto del requisito.

```
Analiza si el requisito está funcionalmente completo para que pueda
generar artefactos sin lagunas que se conviertan en bugs.

REQUISITO A VALIDAR:
{{requisito_yaml}}

ANÁLISIS DE COMPLETITUD:

BLOQUE A — Cobertura de flujos
  ¿Está documentado el flujo principal (happy path)?
  ¿Está documentado qué ocurre cuando cada campo obligatorio falta?
  ¿Está documentado qué ocurre cuando los datos son inválidos?
  ¿Está documentado qué ocurre si un servicio dependiente falla?
  ¿Está documentado el comportamiento para usuarios sin permiso?

BLOQUE B — Completitud de datos de entrada
  Para cada dato de entrada, ¿se especifica?
    - Tipo de dato (string, integer, date, boolean, enum)
    - Si es obligatorio u opcional
    - Rango de valores válidos (para numéricos y fechas)
    - Longitud máxima (para texto)
    - Formato (para fechas, códigos, identificadores)
    - Valor por defecto si existe

BLOQUE C — Completitud de datos de salida
  ¿Se especifican los campos que devuelve el sistema?
  ¿Se especifica el formato de la respuesta?
  ¿Se especifica el comportamiento de paginación si aplica?
  ¿Se especifica el orden por defecto si aplica?

BLOQUE D — Casos de contorno identificados
  ¿Se ha considerado el valor mínimo y máximo de cada campo numérico?
  ¿Se ha considerado qué ocurre con conjuntos vacíos de datos?
  ¿Se ha considerado el comportamiento con el volumen máximo de datos?

Para cada laguna detectada, indica qué pregunta sin respuesta generaría
un bug en producción.

Genera:
{
  "validacion_completitud": {
    "requisito_id": "{{req_id}}",
    "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "analisis_por_bloque": {
      "cobertura_flujos": { "resultado": "...", "problemas": [] },
      "datos_entrada": { "resultado": "...", "problemas": [] },
      "datos_salida": { "resultado": "...", "problemas": [] },
      "casos_contorno": { "resultado": "...", "problemas": [] }
    },
    "preguntas_sin_responder": [
      {
        "pregunta": "[¿Qué pasa si...?]",
        "consecuencia_si_no_se_resuelve": "[Bug o comportamiento indefinido concreto]",
        "severidad": "BLOQUEANTE | ADVERTENCIA"
      }
    ]
  }
}
```

### Ejemplo de output

```json
{
  "validacion_completitud": {
    "requisito_id": "REQ-023",
    "resultado": "APROBADO_CON_ADVERTENCIAS",
    "analisis_por_bloque": {
      "cobertura_flujos": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "excepciones",
            "problema": "No se documenta el comportamiento cuando el servicio de base de datos no responde durante la búsqueda.",
            "ejemplo_correcto": "- Si la BD no responde en menos de 5 segundos: mostrar mensaje 'El servicio no está disponible temporalmente. Inténtelo de nuevo en unos minutos.' con botón de reintento."
          }
        ]
      },
      "datos_entrada": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "datos_entrada → fecha_inicio",
            "problema": "No se especifica el formato de fecha aceptado. El frontend puede enviar DD/MM/YYYY, el backend puede esperar YYYY-MM-DD.",
            "ejemplo_correcto": "formato: ISO-8601 (YYYY-MM-DD). El frontend formatea antes de enviar al API."
          },
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "datos_entrada",
            "problema": "No se documenta si fecha_fin tiene valor por defecto cuando se omite.",
            "ejemplo_correcto": "fecha_fin: opcional. Valor por defecto: fecha actual del sistema."
          }
        ]
      },
      "datos_salida": {
        "resultado": "LIMPIO",
        "problemas": []
      },
      "casos_contorno": {
        "resultado": "PROBLEMAS_ENCONTRADOS",
        "problemas": [
          {
            "severidad": "ADVERTENCIA",
            "ubicacion": "datos_entrada → rango_fechas",
            "problema": "No se documenta el comportamiento con un rango de exactamente 365 días (el valor límite exacto). ¿Se acepta o se rechaza?",
            "ejemplo_correcto": "El rango máximo es de 365 días inclusive (fecha_fin - fecha_inicio <= 365). Un rango de 366 días es rechazado."
          }
        ]
      }
    },
    "preguntas_sin_responder": [
      {
        "pregunta": "¿Qué ocurre si el servicio de base de datos no responde durante la búsqueda?",
        "consecuencia_si_no_se_resuelve": "El desarrollador implementará un timeout genérico sin mensaje de usuario. El gestor verá una pantalla en blanco o un error 500 sin explicación.",
        "severidad": "ADVERTENCIA"
      },
      {
        "pregunta": "¿Es fecha_fin obligatoria o tiene valor por defecto?",
        "consecuencia_si_no_se_resuelve": "Frontend y backend implementarán comportamientos distintos. En producción, omitir la fecha de fin devolverá resultados inesperados o un error no controlado.",
        "severidad": "ADVERTENCIA"
      }
    ]
  }
}
```

---

## Prompt 5 — Informe consolidado de validación

Agrega los resultados de las cuatro llamadas anteriores en un único informe accionable para el analista.

```
Consolida los resultados de las cuatro validaciones del requisito en un
informe único, ordenado por prioridad de resolución.

RESULTADOS DE LAS CUATRO VALIDACIONES:
{{validacion_estructural_json}}
{{validacion_semantica_json}}
{{validacion_consistencia_json}}
{{validacion_completitud_json}}

Genera el informe consolidado con esta estructura:
{
  "informe_validacion": {
    "requisito_id": "{{req_id}}",
    "titulo_requisito": "{{titulo}}",
    "timestamp": "{{timestamp}}",
    "analista_responsable": "{{analista}}",
    "veredicto_final": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
    "puede_entrar_al_pipeline": true | false,
    "resumen_ejecutivo": "[2-3 frases describiendo el estado del requisito]",
    "puntuacion_global": {
      "valor": N,
      "escala": "0-100",
      "desglose": {
        "estructura": N,
        "semantica": N,
        "consistencia": N,
        "completitud": N
      }
    },
    "problemas_por_prioridad": {
      "bloqueantes": [
        {
          "id_problema": "P001",
          "origen_validacion": "estructural | semantica | consistencia | completitud",
          "campo": "...",
          "problema": "...",
          "accion_requerida": "[Qué debe hacer el analista exactamente]",
          "ejemplo_correcto": "..."
        }
      ],
      "advertencias": [],
      "sugerencias": []
    },
    "checklist_rapido": {
      "tiene_id_valido": true | false,
      "tiene_actor_definido": true | false,
      "tiene_ac_verificables": true | false,
      "sin_ambiguedad_bloqueante": true | false,
      "sin_contradicciones": true | false,
      "flujos_error_documentados": true | false,
      "datos_entrada_completos": true | false,
      "usa_glosario_oficial": true | false
    },
    "proximos_pasos": [
      "[Acción concreta 1 ordenada por urgencia]",
      "[Acción concreta 2]"
    ],
    "estimacion_tiempo_correccion": "[X-Y minutos estimados para resolver los problemas bloqueantes]"
  }
}
```

---

## Cómo integrar la validación en el flujo real

La validación se puede ejecutar en tres momentos distintos con diferente nivel de automatización:

**Durante la escritura (tiempo real).** Si el analista trabaja en Confluence, un script puede validar el YAML cada vez que guarda el documento y mostrar un panel de estado en la barra lateral. Los problemas aparecen en el momento en que se cometen, no cuando el requisito llega al pipeline días después.

**Al cambiar de estado (gate automático).** Cuando el analista mueve el requisito de `borrador` a `en-revision`, el pipeline de validación se ejecuta automáticamente. Si hay bloqueantes, el estado vuelve a `borrador` y se notifica al analista con el informe. Este es el gate más crítico porque impide que requisitos deficientes lleguen al refinamiento.

**En el pipeline de generación (última línea de defensa).** Antes del Prompt 1 de generación de artefactos Jira, una comprobación rápida verifica que el requisito tiene estado `validado`. Si no, el pipeline se detiene.

---

## Catálogo de los 15 problemas más frecuentes

Estos son los errores que aparecen en el 80% de los proyectos. Configurarlos como reglas fijas en el System Prompt mejora la precisión de la detección:

| # | Problema | Tipo | Consecuencia real |
|---|----------|------|-------------------|
| 1 | Verbos ambiguos en el título (gestionar, administrar) | Semántico | Historias demasiado amplias, imposibles de estimar |
| 2 | "El sistema debe ser rápido/eficiente" | Semántico | QA no sabe qué medir. Se aprueba cualquier cosa. |
| 3 | Criterio de aceptación con múltiples condiciones en el "entonces" | Semántico | Un solo test verifica cosas no relacionadas. Falsos PASS |
| 4 | Actor no especificado o genérico ("el usuario") | Estructural | El desarrollo no implementa permisos correctamente |
| 5 | Sin flujo de error documentado | Completitud | El comportamiento en error lo decide el desarrollador |
| 6 | Datos de entrada sin tipo ni formato | Completitud | Desajuste frontend/backend en producción |
| 7 | Sinónimos del glosario mezclados | Consistencia | Dos entidades Jira para el mismo concepto |
| 8 | Requisito que mezcla dos funcionalidades | Atomicidad | Historia irrompible, sprint bloqueado |
| 9 | Contradicción con otro requisito del módulo | Consistencia | Dos implementaciones contradictorias en producción |
| 10 | Criterio "el sistema funciona correctamente" | Verificabilidad | Imposible escribir un test válido |
| 11 | Regla de negocio sin criterio de aceptación asociado | Completitud | La regla existe en el papel, pero no se testea |
| 12 | Campo "excepciones" vacío | Estructural | Flujos de error no implementados |
| 13 | Casos de contorno no documentados | Completitud | Bugs en valores límite en producción |
| 14 | Condición implícita ("si es necesario", "cuando proceda") | Semántico | El desarrollador decide cuándo es necesario |
| 15 | Dependencia de otro requisito no documentada | Consistencia | Historias implementadas en orden incorrecto |

---

## Métricas para medir la mejora

Una vez implantado el pipeline de validación, estas métricas demuestran el impacto al equipo directivo:

**Antes de implantar:** medir durante 4 semanas el porcentaje de historias que llegan al sprint con cambios de alcance, el número de bugs clasificados como "ambigüedad funcional" y el tiempo medio entre que un requisito se aprueba y llega a Jira.

**Después de implantar:** el mismo conjunto de métricas muestra la reducción. En proyectos similares, la validación automática reduce entre un 40% y un 60% los bugs por ambigüedad funcional en los primeros tres meses, y elimina prácticamente las contradicciones entre requisitos del mismo módulo.
