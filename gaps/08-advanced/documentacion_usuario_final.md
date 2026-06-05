# Generación de documentación de usuario final

## De los requisitos estructurados a los manuales, release notes y ayuda en línea

---

## El problema que nadie anticipa

Cuando un equipo completa una funcionalidad, suele quedar pendiente una deuda silenciosa: la documentación que necesita el usuario final para entender qué ha cambiado y cómo utilizarlo. Esa deuda se paga tarde, mal o directamente no se paga.

El motivo es estructural. La documentación de usuario se redacta desde cero, a mano, por alguien que tiene que reconstruir el contexto funcional desde el código o desde las historias de Jira. Es el trabajo de mayor coste por unidad de información producida en todo el ciclo de desarrollo, y el primero que se elimina cuando hay presión de entrega.

Lo que el modelo operativo AI-ready ya ha resuelto cambia esta ecuación por completo. Los requisitos YAML estructurados, los criterios de aceptación en formato Gherkin, el glosario canónico y la jerarquía épica → historia → tarea contienen toda la información que necesita un generador de documentación de usuario. No como un subproducto de la documentación técnica, sino como la fuente primaria más precisa disponible: describe el comportamiento esperado del sistema desde la perspectiva del actor que lo usa, en el lenguaje del negocio, con los casos de error ya documentados.

Este documento describe cómo construir el pipeline de generación de documentación de usuario final que convierte esa materia prima en tres tipos de entregables: manuales de usuario, release notes y ayuda en línea contextual.

---

## Qué información está disponible en el repositorio

Antes de diseñar los prompts y el pipeline, conviene inventariar exactamente qué tiene la IA a su disposición cuando accede al repositorio de requisitos de un proyecto maduro.

**Del requisito YAML** extrae el actor y su rol, el evento disparador que contextualiza cuándo se usa la funcionalidad, la descripción en lenguaje de negocio, el flujo principal paso a paso, los flujos alternativos y de error, los datos de entrada con sus validaciones, y los datos de salida con su formato y paginación.

**De los criterios de aceptación** extrae el comportamiento exacto que el sistema debe mostrar ante cada acción del usuario, incluidos los mensajes de error literales (campo `entonces`) y las condiciones que los provocan (campo `dado` y `cuando`). Estos criterios son la base más fiable disponible para redactar ayuda contextual: son los mismos que verifican que el sistema funciona correctamente.

**Del glosario estructurado** extrae los términos oficiales que deben aparecer en la documentación (y los sinónimos que no deben aparecer), las descripciones canónicas de las entidades con sus estados posibles, y las reglas de negocio globales que afectan a todo el módulo.

**De la jerarquía épica → historia** extrae la agrupación funcional que determina la estructura de capítulos del manual y la agrupación de novedades en las release notes.

**Del grafo de trazabilidad** extrae qué historias forman parte de qué sprint o release, lo que permite generar las release notes por versión sin necesidad de que nadie enumere manualmente qué cambió.

Esta disponibilidad de información hace que la generación de documentación de usuario sea la aplicación con mayor ratio beneficio/esfuerzo de todo el modelo operativo, una vez que el repositorio está maduro.

---

## Los tres tipos de documentación y su relación con el repositorio

### Manual de usuario

El manual de usuario es la documentación de referencia completa de un módulo o producto. Su estructura natural mapea directamente sobre la jerarquía de épicas e historias del repositorio.

**Estructura generada automáticamente:**

```
Manual del módulo EP-04 — Gestión de Facturación
│
├── Capítulo 1: Introducción al módulo
│   └── Generado desde: descripción de la épica + actores del glosario
│
├── Capítulo 2: Acceso y permisos
│   └── Generado desde: actores del glosario + reglas_negocio globales de acceso
│
├── Capítulo 3: Filtrado de facturas por rango de fechas
│   └── Generado desde: REQ-023 (US-047)
│       ├── Cuándo usar esta función     ← evento_disparador
│       ├── Paso a paso                  ← flujo_principal
│       ├── Variantes del proceso        ← flujos_alternativos
│       ├── Mensajes y errores habituales ← excepciones + criterios AC negativos
│       └── Preguntas frecuentes         ← reglas_negocio como FAQ
│
└── Capítulo N: Glosario del módulo
    └── Generado desde: glosario.yaml (sección entidades del módulo)
```

La granularidad es configurable: cada historia genera una sección, cada épica genera un capítulo. Para módulos simples con pocas historias, puede usarse una historia por subsección dentro de un único capítulo.

---

### Release notes

Las release notes describen qué ha cambiado entre dos versiones del producto desde la perspectiva del usuario. Su generación automática requiere consultar el grafo de trazabilidad para identificar qué historias se completaron en el sprint o la release correspondiente.

La ventaja del repositorio estructurado es que las release notes no son un resumen técnico de commits (que el usuario no entiende) ni un resumen de alto nivel sin detalle (que no le permite saber si le afecta). Son una descripción exacta del comportamiento nuevo desde la perspectiva del actor, con ejemplos concretos derivados de los datos de prueba de los test cases.

**Estructura tipo de release note por historia:**

```markdown
## Filtrado de facturas por rango de fechas

El gestor de facturación puede ahora buscar facturas introduciendo una 
fecha de inicio y una fecha de fin. Los resultados aparecen ordenados 
de más reciente a más antiguo.

**Cómo funciona:** Accede al módulo Facturas, introduce el rango de 
fechas en los campos Desde y Hasta, y pulsa Buscar. Los resultados 
aparecen en menos de 2 segundos.

**A tener en cuenta:** El rango máximo de búsqueda es de 365 días. 
Si introduces un rango mayor, el sistema te lo indicará antes de 
ejecutar la búsqueda.

**¿A quién afecta?** Gestores de facturación y responsables financieros.
```

Este formato se genera desde los campos `descripcion`, `actor`, `flujo_principal`, `excepciones` y `reglas_negocio` del requisito YAML, más el campo `entonces` de los criterios de aceptación que documentan el comportamiento observable.

---

### Ayuda en línea contextual

La ayuda en línea contextual es el tipo de documentación de mayor impacto para el usuario final y el más difícil de mantener manualmente. Se trata de textos cortos, específicos de cada pantalla o acción, que aparecen cuando el usuario necesita orientación: tooltips, mensajes de ayuda, paneles de información emergente y textos de estado vacío.

Su generación es especialmente natural desde el repositorio estructurado porque cada criterio de aceptación ya describe exactamente el comportamiento de un elemento de la interfaz. El campo `entonces` de un criterio positivo es el texto de un tooltip. El campo `entonces` de un criterio negativo con la condición documentada es el texto de un mensaje de error.

**Mapeo criterio de aceptación → elemento de ayuda en línea:**

| Campo del requisito | Elemento de ayuda en línea |
|---|---|
| `AC-023-01.entonces` (flujo positivo) | Tooltip del botón Buscar |
| `AC-023-02.entonces` (error rango) | Mensaje de validación del campo de fechas |
| `AC-023-03.entonces` (estado vacío) | Texto del estado vacío del listado |
| `reglas_negocio[0]` (solo ejercicio en curso) | Nota informativa en el filtro de fechas |
| `datos_entrada.fecha_inicio.formato` (ISO-8601) | Placeholder del campo de fecha |

---

## Arquitectura del pipeline de documentación

El pipeline se integra como un paso adicional del orquestador principal. A diferencia del pipeline de artefactos Jira o del de test cases, la documentación de usuario no se genera requisito a requisito sino por agrupaciones funcionales: una historia produce una sección del manual, una épica produce un capítulo, una release produce las notas de versión.

```
INPUTS
  ├── YAML de requisitos (validados)
  ├── Glosario estructurado
  ├── Grafo de trazabilidad (para release notes por sprint)
  └── Plantilla de estilo documental

         │
         ▼

PIPELINE DE DOCUMENTACIÓN
  │
  ├── [Paso 1] Consulta al grafo → selección de historias por scope
  │           (módulo completo, sprint, release, historia individual)
  │
  ├── [Paso 2] Recuperación de contexto RAG
  │           (requisitos relacionados, reglas globales, glosario relevante)
  │
  ├── [Paso 3] Generación por tipo de documento
  │           ├── Manual: sección por historia + capítulo por épica
  │           ├── Release notes: entrada por historia completada
  │           └── Ayuda en línea: elementos por criterio de aceptación
  │
  ├── [Paso 4] Validación de terminología
  │           (verificar que solo aparecen términos del glosario oficial)
  │
  └── [Paso 5] Ensamblado y exportación
              ├── Markdown → Confluence / GitHub Pages / Docusaurus
              ├── HTML → portales de ayuda / sistemas de help desk
              └── JSON estructurado → integración con plataformas CMS

         │
         ▼

OUTPUTS
  ├── Manual de usuario (por módulo o producto completo)
  ├── Release notes (por sprint o versión de release)
  └── Biblioteca de ayuda en línea (JSON indexable por pantalla/acción)
```

---

## Los prompts del pipeline de documentación

### System prompt base para documentación de usuario

```
Eres un redactor técnico especializado en documentación de software 
orientada al usuario final. Tu función es transformar especificaciones 
funcionales estructuradas en documentación clara, útil y directa.

PRINCIPIOS DE REDACCIÓN:
1. Escribe siempre en segunda persona ("usted puede", "introduzca", 
   "pulse"). El usuario es el protagonista, no el sistema.
2. Usa exclusivamente los términos del glosario proporcionado. 
   Si el glosario dice "Gestor de facturación", nunca escribas 
   "usuario", "operador" ni "empleado".
3. Los pasos de un procedimiento van siempre numerados.
4. Describe el resultado observable de cada paso, no la lógica interna.
5. Los mensajes de error y validación van en texto literal 
   entre comillas: el sistema muestra "El rango no puede superar 365 días".
6. No uses jerga técnica: "campo", "formulario", "módulo" sí. 
   "Endpoint", "payload", "query" nunca.
7. Las advertencias y notas importantes van en párrafos destacados 
   precedidos de "Importante:" o "Tenga en cuenta:".
8. El output es siempre Markdown válido, con la estructura de 
   encabezados especificada en el prompt de tarea.

GLOSARIO APLICABLE:
{{glosario_compacto}}

CONTEXTO DEL MÓDULO:
{{descripcion_epica}}
```

---

### Prompt 1 — Sección de manual para una historia de usuario

```
A partir de la historia de usuario y el requisito estructurado que se 
proporcionan, genera una sección de manual de usuario completa.

HISTORIA DE USUARIO:
{{historia_yaml}}

REQUISITO ORIGEN:
{{requisito_yaml}}

ESTRUCTURA REQUERIDA (usar exactamente estos encabezados H3):

### [Título de la función — derivado del campo `titulo` del requisito]

**¿Para qué sirve?**
[1-2 frases. Derivado del campo `objetivo_negocio`. En lenguaje de negocio, 
sin tecnicismos. Qué problema resuelve para el usuario, no qué hace el sistema.]

**¿Quién puede usarla?**
[Lista de actores con sus permisos clave. Derivado del glosario de actores 
y del campo `actor` y `actores_secundarios` del requisito.]

**Paso a paso**
[Lista numerada derivada del `flujo_principal`. Cada paso incluye la acción 
del usuario y el resultado observable inmediato. Máximo 10 pasos.
Si hay flujos alternativos relevantes para el usuario, incluirlos como 
subsección "Otras formas de hacerlo".]

**Mensajes y situaciones habituales**
[Tabla de dos columnas: "Si ve esto..." / "Significa que...". 
Derivada de los criterios de aceptación negativos y de las excepciones.
Incluir el texto literal del mensaje entre comillas en la primera columna.]

**Lo que debe saber**
[Lista de viñetas con las reglas de negocio relevantes para el usuario.
Derivada del campo `reglas_negocio`. Solo las que afectan al comportamiento 
visible, no las técnicas o de implementación.]

Genera el JSON de salida con este formato:
{
  "tipo": "seccion_manual",
  "historia_id": "{{historia_id}}",
  "requisito_id": "{{req_id}}",
  "epica_id": "{{epica_id}}",
  "titulo_seccion": "...",
  "contenido_markdown": "...",
  "palabras": N,
  "alertas_terminologia": ["término no oficial detectado si los hay"]
}
```

**Ejemplo de output para REQ-023 / US-047:**

```markdown
### Filtrar facturas por rango de fechas

**¿Para qué sirve?**
Esta función le permite localizar rápidamente todas las facturas de un período 
contable concreto sin necesidad de buscar manualmente entre todos los registros. 
Es especialmente útil durante el cierre mensual.

**¿Quién puede usarla?**
- **Gestor de facturación:** acceso completo al filtro y a los resultados.
- **Responsable financiero:** acceso completo al filtro y a los resultados.

**Paso a paso**

1. Acceda al módulo **Facturas** desde el menú principal.
2. Localice los campos **Desde** y **Hasta** en el panel de filtros 
   superior de la pantalla.
3. Introduzca la fecha de inicio en el campo **Desde** 
   (por ejemplo, 01/01/2024).
4. Introduzca la fecha de fin en el campo **Hasta** 
   (por ejemplo, 31/03/2024).
5. Pulse el botón **Buscar**.
6. El listado muestra las facturas del período, ordenadas de más 
   reciente a más antigua. En la parte superior aparece el número 
   total de resultados encontrados.

**Otras formas de hacerlo**

Si no introduce la fecha de fin, el sistema utiliza la fecha de hoy 
como límite superior de la búsqueda.

**Mensajes y situaciones habituales**

| Si ve esto... | Significa que... |
|---|---|
| "El rango no puede superar 365 días" | Las fechas introducidas abarcan más de un año. Ajuste el rango a un máximo de 365 días. |
| "No se encontraron facturas para el período seleccionado" | No existen facturas registradas en ese rango de fechas. Pulse **Ampliar búsqueda** para ver otros períodos. |
| Los campos **Desde** y **Hasta** aparecen resaltados en rojo | Las fechas introducidas no son válidas o el rango supera el límite permitido. |

**Lo que debe saber**

- Solo puede consultar facturas del ejercicio fiscal en curso (año natural).
- El rango máximo de búsqueda es de 365 días.
- Los resultados muestran un máximo de 100 facturas por página.
```

---

### Prompt 2 — Release notes por sprint o versión

```
A partir de la lista de historias completadas en el sprint o release 
indicado, genera las notas de versión orientadas al usuario final.

HISTORIAS COMPLETADAS EN {{nombre_sprint_o_release}}:
{{lista_historias_yaml}}

ÉPICAS AFECTADAS:
{{lista_epicas}}

FORMATO DE SALIDA:

Las release notes tienen tres secciones fijas en este orden:
1. Resumen ejecutivo (3-4 frases: qué tipo de mejoras trae esta versión 
   y a quién afecta principalmente)
2. Novedades y mejoras (una entrada por historia, ordenadas por épica)
3. Lo que debe tener en cuenta (cambios de comportamiento respecto a la 
   versión anterior, si los hay — derivados de criterios AC que modifican 
   comportamiento existente)

Para cada entrada de "Novedades y mejoras", usar este formato:
**[Título breve de la mejora]** — [Actor/es afectados]
[2-3 frases describiendo qué puede hacer ahora el usuario que antes no podía, 
o cómo ha mejorado algo que ya existía. Sin tecnicismos.]
> Acceso: [ruta de navegación hasta la función, derivada del evento_disparador]

REGLAS:
- No mencionar IDs técnicos (REQ-023, US-047, FACT-47) en el texto visible.
- No describir la implementación técnica, solo el resultado para el usuario.
- Si la historia resuelve un problema conocido (punto de dolor del Event 
  Storming), mencionar la mejora respecto al proceso anterior.
- Las mejoras de rendimiento (tiempo de respuesta, volumen de datos) 
  se mencionan con valores concretos cuando están en los criterios AC.

Genera el JSON de salida:
{
  "tipo": "release_notes",
  "version": "{{nombre_version}}",
  "fecha": "{{fecha}}",
  "historias_incluidas": ["{{historia_id}}", ...],
  "contenido_markdown": "...",
  "resumen_en_tres_palabras": "...",
  "alertas": []
}
```

**Ejemplo de output para el Sprint 4 de Meridian (EP-04):**

```markdown
# Notas de versión — Sprint 4 / Módulo de Facturación

## Resumen

Esta versión incorpora las primeras funcionalidades de búsqueda y 
filtrado en el módulo de Gestión de Facturación. Los gestores de 
facturación y responsables financieros pueden ahora localizar 
facturas por período, proveedor y estado sin necesidad de revisar 
el listado completo manualmente.

## Novedades y mejoras

**Búsqueda de facturas por rango de fechas** — Gestores de facturación, 
Responsables financieros

Introduzca una fecha de inicio y una de fin para ver todas las facturas 
de ese período, ordenadas de más reciente a más antigua. Los resultados 
aparecen en menos de 2 segundos incluso para períodos con miles de 
registros. El rango máximo de búsqueda es de 365 días.
> Acceso: Módulo Facturas → panel de filtros superior

**Filtrado por estado de factura** — Gestores de facturación

Filtre el listado por el estado actual de la factura (pendiente, 
en revisión, aprobada, rechazada, pagada o archivada) para concentrarse 
en las que requieren su atención inmediata.
> Acceso: Módulo Facturas → panel de filtros → desplegable Estado

## Lo que debe tener en cuenta

- El módulo de Facturas solo muestra facturas del ejercicio fiscal en 
  curso. Las facturas de ejercicios anteriores estarán disponibles en 
  la próxima versión a través del archivo histórico.
- Las búsquedas con más de 100 resultados muestran el listado 
  paginado. Use los controles de navegación en la parte inferior 
  de la pantalla para avanzar entre páginas.
```

---

### Prompt 3 — Biblioteca de ayuda en línea contextual

```
A partir de los criterios de aceptación y los datos del requisito, 
genera los elementos de ayuda en línea para cada componente de la 
interfaz de usuario de esta historia.

HISTORIA Y REQUISITO:
{{historia_yaml}}
{{requisito_yaml}}

COMPONENTES DE UI IDENTIFICADOS:
[Lista los componentes que aparecen en el flujo_principal y en los 
criterios de aceptación: campos de formulario, botones, listados, 
mensajes de estado, tooltips]

Para cada componente, genera los elementos de ayuda aplicables 
según este catálogo:

TIPO A — Tooltip (aparece al pasar el cursor o pulsar el icono ?)
  Longitud: máximo 80 caracteres
  Fuente: campo `cuando` del criterio de aceptación positivo relevante
  Tono: imperativo directo ("Introduzca", "Seleccione", "Pulse")

TIPO B — Mensaje de validación inline
  Longitud: máximo 120 caracteres. Incluir el valor límite si existe.
  Fuente: campo `entonces` del criterio de aceptación negativo
  Tono: informativo, sin culpar al usuario ("El rango no puede..." 
        no "Ha introducido un rango incorrecto")

TIPO C — Texto de estado vacío
  Longitud: 1 frase + 1 acción sugerida
  Fuente: criterio de aceptación con condición "sin resultados"
  Tono: neutral y orientado a la acción siguiente

TIPO D — Texto placeholder de campo
  Longitud: máximo 40 caracteres
  Fuente: campo `formato` o `descripcion` de datos_entrada
  Tono: ejemplo concreto ("ej. 01/01/2024") o descripción mínima

TIPO E — Nota informativa de módulo
  Longitud: 1-2 frases
  Fuente: reglas_negocio visibles para el usuario
  Tono: informativo preventivo ("Solo se muestran...")

Genera el JSON de salida indexado por componente para integración 
directa con el frontend:

{
  "tipo": "ayuda_en_linea",
  "historia_id": "{{historia_id}}",
  "elementos": [
    {
      "componente_id": "{{selector_css_o_id_ui}}",
      "componente_descripcion": "...",
      "tipo_ayuda": "A|B|C|D|E",
      "texto": "...",
      "criterio_origen": "{{ac_id}}",
      "longitud": N
    }
  ]
}
```

**Ejemplo de output para US-047:**

```json
{
  "tipo": "ayuda_en_linea",
  "historia_id": "US-047",
  "elementos": [
    {
      "componente_id": "#filter-date-from",
      "componente_descripcion": "Campo fecha de inicio del filtro",
      "tipo_ayuda": "D",
      "texto": "ej. 01/01/2024",
      "criterio_origen": "AC-023-01",
      "longitud": 14
    },
    {
      "componente_id": "#filter-date-to",
      "componente_descripcion": "Campo fecha de fin del filtro",
      "tipo_ayuda": "D",
      "texto": "ej. 31/03/2024",
      "criterio_origen": "AC-023-01",
      "longitud": 14
    },
    {
      "componente_id": "[data-testid='btn-search']",
      "componente_descripcion": "Botón Buscar del panel de filtros",
      "tipo_ayuda": "A",
      "texto": "Busca facturas en el período seleccionado",
      "criterio_origen": "AC-023-01",
      "longitud": 42
    },
    {
      "componente_id": "[data-testid='date-range-error']",
      "componente_descripcion": "Mensaje de error por rango excesivo",
      "tipo_ayuda": "B",
      "texto": "El rango no puede superar 365 días. Ajuste las fechas.",
      "criterio_origen": "AC-023-02",
      "longitud": 54
    },
    {
      "componente_id": "[data-testid='empty-state']",
      "componente_descripcion": "Estado vacío del listado de facturas",
      "tipo_ayuda": "C",
      "texto": "No se encontraron facturas para el período seleccionado. Pulse Ampliar búsqueda para ver otros períodos.",
      "criterio_origen": "AC-023-03",
      "longitud": 108
    },
    {
      "componente_id": "#filter-panel-info",
      "componente_descripcion": "Nota informativa del panel de filtros",
      "tipo_ayuda": "E",
      "texto": "Solo se muestran facturas del ejercicio fiscal en curso. El rango máximo de búsqueda es de 365 días.",
      "criterio_origen": "REQ-023-reglas_negocio",
      "longitud": 100
    }
  ]
}
```

---

### Prompt 4 — Capítulo de introducción a un módulo (épica)

```
A partir de la descripción de la épica, los actores que intervienen 
y las funciones que incluye, genera el capítulo de introducción al 
módulo para el manual de usuario.

ÉPICA:
{{epica_yaml}}

HISTORIAS DEL MÓDULO (resumen):
{{lista_historias_resumen}}

ACTORES DEL GLOSARIO RELEVANTES:
{{actores_glosario}}

ESTRUCTURA REQUERIDA:

## [Nombre del módulo]

**¿Para qué sirve este módulo?**
[2-3 párrafos. Explica qué proceso de negocio cubre el módulo, 
qué problema resuelve para la organización y qué puede hacer el 
usuario con él. Derivado del campo `objetivo` de la épica 
y de los `objetivo_negocio` de sus historias principales.]

**¿Quién trabaja con este módulo?**
[Tabla con dos columnas: Rol / Qué puede hacer. 
Derivada del glosario de actores y sus `permisos_clave`.]

**Funciones disponibles**
[Lista numerada de las funciones del módulo con una frase descriptiva 
cada una. Una función por historia validada en el módulo. 
Incluir referencia a la sección del manual donde se documenta cada una.]

**Antes de empezar**
[Lista de requisitos previos para el usuario: acceso, permisos, 
datos necesarios. Derivada de las `precondiciones` más frecuentes 
en los criterios de aceptación y de las `reglas_globales` del glosario.]
```

---

### Prompt 5 — Glosario del módulo para el usuario final

```
A partir del glosario estructurado del proyecto (sección de entidades 
del módulo indicado), genera el glosario orientado al usuario final 
para incluir como apéndice del manual.

GLOSARIO TÉCNICO DE ENTRADA:
{{glosario_entidades_modulo_yaml}}

REGLAS DE TRANSFORMACIÓN:
1. Usa el `nombre_oficial` como término de entrada, nunca un sinónimo.
2. Transforma la `descripcion` técnica del glosario en una definición 
   comprensible para un usuario sin conocimientos técnicos.
3. Para cada entidad con estados definidos, incluye una tabla de estados 
   solo si el usuario necesita distinguirlos para operar correctamente.
4. Omite los campos técnicos (tipo de dato, formato, regex). 
   Incluye solo la información que ayuda al usuario a entender qué es 
   ese elemento y cómo se comporta.
5. Los `atributos_clave` solo se mencionan si el usuario los ve directamente 
   en la interfaz (nunca IDs internos, hashes ni campos técnicos).

Genera el JSON de salida:
{
  "tipo": "glosario_usuario",
  "modulo": "{{epica_id}}",
  "terminos": [
    {
      "termino": "...",
      "definicion": "...",
      "estados": [
        {"nombre": "...", "descripcion_usuario": "..."}
      ],
      "nota_uso": "..."
    }
  ]
}
```

**Ejemplo de output para la entidad Factura:**

```json
{
  "termino": "Factura",
  "definicion": "Documento que registra una compra realizada a un proveedor. En este módulo, las facturas son siempre documentos recibidos de proveedores, no documentos emitidos a clientes.",
  "estados": [
    {
      "nombre": "Pendiente",
      "descripcion_usuario": "La factura ha sido registrada en el sistema pero aún no ha sido revisada."
    },
    {
      "nombre": "En revisión",
      "descripcion_usuario": "El gestor de facturación está verificando que la factura es correcta."
    },
    {
      "nombre": "Aprobada",
      "descripcion_usuario": "La factura ha sido validada y está pendiente de pago."
    },
    {
      "nombre": "Rechazada",
      "descripcion_usuario": "La factura no ha sido aceptada. Se ha registrado el motivo del rechazo."
    },
    {
      "nombre": "Pagada",
      "descripcion_usuario": "El pago ha sido registrado en el sistema."
    },
    {
      "nombre": "Archivada",
      "descripcion_usuario": "La factura está en el archivo histórico. Solo puede consultarse, no modificarse."
    }
  ],
  "nota_uso": "Las facturas superiores a 10.000 € requieren la aprobación del Responsable financiero antes de procesarse para pago."
}
```

---

## Validación de terminología: el prompt supervisor

La coherencia terminológica en la documentación de usuario es tan crítica como en los requisitos. Un manual que usa "cliente", "usuario", "cuenta" y "usuario registrado" para referirse al mismo actor confunde más que aclara.

El pipeline incluye un paso de validación de terminología que revisa cada documento generado antes de la aprobación:

```
Revisa el documento de usuario final generado y verifica que:

1. Todos los actores mencionados usan el nombre oficial del glosario.
   Detecta cualquier aparición de sinónimos no oficiales.

2. Todas las entidades mencionadas usan el nombre oficial del glosario.

3. Los mensajes de error reproducidos en el documento coinciden 
   literalmente con los definidos en los criterios de aceptación 
   (campo `entonces`). Cualquier paráfrasis es un error.

4. Los valores de límites y restricciones mencionados (365 días, 
   100 registros, 10.000 €) coinciden con los definidos en el 
   YAML del requisito.

DOCUMENTO A REVISAR:
{{documento_markdown}}

GLOSARIO DE REFERENCIA:
{{glosario_yaml}}

CRITERIOS DE ACEPTACIÓN DE REFERENCIA:
{{criterios_ac_yaml}}

Genera el informe de validación:
{
  "resultado": "APROBADO | APROBADO_CON_ADVERTENCIAS | BLOQUEADO",
  "problemas": [
    {
      "tipo": "terminologia | mensaje_incorrecto | valor_incorrecto",
      "ubicacion": "...",
      "texto_actual": "...",
      "texto_correcto": "...",
      "severidad": "BLOQUEANTE | ADVERTENCIA"
    }
  ]
}
```

---

## Integración en el orquestador

El pipeline de documentación se añade al orquestador principal como un paso opcional (`s10_documentacion`) que se activa mediante el flag `--docs`:

```bash
# Generar artefactos Jira + documentación de usuario en un único comando
python orchestrator.py --req REQ-023 --docs

# Generar solo la documentación (el pipeline de Jira ya se ejecutó antes)
python orchestrator.py --req REQ-023 --solo-docs --tipo manual

# Generar las release notes para el sprint completado
python orchestrator.py --sprint SPRINT-04 --docs --tipo release-notes

# Modo dry-run: generar documentación sin publicarla
python orchestrator.py --epica EP-04 --docs --dry-run
```

El paso `s10_documentacion` se ejecuta siempre después de `s9_push_jira` y antes de finalizar el run. No es bloqueante: si falla, el pipeline reporta la advertencia pero los artefactos Jira ya están creados.

```python
# Fragmento del orquestador para el paso de documentación
# (se añade al bloque de pasos existente)

# ══════════════════════════════════════════════════════
# PASO 10 — Generación de documentación de usuario (opcional)
# ══════════════════════════════════════════════════════
paso = "s10_documentacion"
if not config.generar_docs:
    run = gestor.omitir_paso(
        run, paso, "Flag --docs no activado."
    )
else:
    _log_paso(10, "Generando documentación de usuario")
    run = gestor.iniciar_paso(run, paso)
    try:
        resultado_docs = await generar_documentacion_usuario(
            requisito=requisito,
            historia=run.artefactos_generados.get("historia", {}),
            test_cases=run.test_cases_generados or [],
            glosario=glosario,
            config=config,
            tipos=config.tipos_doc  # ["manual", "ayuda_en_linea"]
        )
        # Guardar en la carpeta de outputs del proyecto
        _guardar_documentacion(resultado_docs, run.requisito_id, config)
        run = gestor.completar_paso(run, paso, {
            "documentos_generados": len(resultado_docs),
            "tipos": config.tipos_doc
        })
        _log_ok(f"{len(resultado_docs)} documentos generados")
    except Exception as e:
        # La documentación no bloquea el pipeline principal
        log.warning(f"  ⚠ Documentación falló: {e}")
        run = gestor.omitir_paso(run, paso, str(e))
```

---

## Destinos de publicación

El JSON o Markdown generado puede publicarse en múltiples destinos sin modificar el pipeline de generación. El destino se configura mediante variables de entorno en el archivo `.env`:

```bash
# Publicar en Confluence como páginas hijas de la épica
DOCS_DESTINO=confluence
CONFLUENCE_ESPACIO=MANUAL
CONFLUENCE_PAGINA_RAIZ=EP-04

# Publicar como archivos Markdown en el repositorio Git
DOCS_DESTINO=git
DOCS_GIT_PATH=docs/usuario/

# Publicar como JSON en el sistema de ayuda en línea del frontend
DOCS_DESTINO=api
DOCS_API_ENDPOINT=https://help.empresa.com/api/v1/content

# Publicar en los tres destinos simultáneamente
DOCS_DESTINO=confluence,git,api
```

El conector de Confluence reutiliza el cliente base del punto 10 del modelo operativo. El conector de Git usa la misma integración CI/CD del orquestador. El conector de API es una llamada REST simple con el JSON de ayuda en línea.

---

## Ciclo de vida: cuándo regenerar la documentación

La documentación de usuario tiene el mismo problema de sincronización que los artefactos Jira: cuando un requisito cambia, la documentación queda desactualizada. El sistema de detección de impacto de cambios del modelo operativo resuelve este problema con la misma arquitectura que ya resuelve el impacto sobre historias y test cases.

El analizador de impacto amplía su análisis para incluir los documentos de usuario como nodos del grafo de trazabilidad. Cuando detecta que un cambio en un requisito afecta a la documentación existente, lo incluye en el informe de impacto y en el plan de acción generado por el LLM:

```
Artefactos afectados por el cambio en REQ-023 (365 días → 90 días):

Historia US-047        → Regenerar         [INMEDIATO]
Test case TC-023-02    → Regenerar         [INMEDIATO]
Test case TC-023-06    → Revisar           [PRÓXIMA ITERACIÓN]
Manual Cap. 3, §3.1    → Regenerar         [INMEDIATO]
  — El texto "365 días" aparece en 3 lugares del manual
Release notes Sprint 4 → Añadir nota de cambio [PRÓXIMA RELEASE]
Ayuda en línea #filter-panel-info → Regenerar  [INMEDIATO]
  — El texto del tooltip menciona "365 días"
```

Esta trazabilidad es posible porque en el momento de generar cada documento, el pipeline registra en el grafo la arista `documento → requisito` con tipo de relación `generado_desde`. El campo de contenido del nodo incluye los valores numéricos y textos literales del requisito que aparecen en el documento, que son los que el analizador usa para detectar si un cambio los afecta.

---

## Qué no hace este pipeline (todavía)

**Capturas de pantalla y elementos visuales.** El pipeline genera texto y estructura. Los diagramas, capturas de pantalla y vídeos explicativos siguen siendo trabajo manual. Para proyectos con un ciclo de diseño maduro en Figma, es posible enriquecer automáticamente los documentos con los enlaces a los frames relevantes del prototipo usando la integración de la API de Figma, pero requiere un paso adicional de configuración.

**Traducción a otros idiomas.** El pipeline genera documentación en el idioma del glosario (español en el caso del modelo operativo de referencia). La traducción automática es técnicamente posible como paso adicional, pero requiere un proceso de revisión humana específico porque los términos del glosario tienen equivalencias que no siempre coinciden con la traducción literal.

**Documentación de procesos cross-módulo.** Las guías de usuario que cubren flujos de trabajo que cruzan varios módulos (por ejemplo, el proceso completo de recepción, revisión y pago de una factura que involucra a EP-05, EP-06 y EP-07) no se generan automáticamente desde un único requisito. Requieren un prompt de síntesis que agregue múltiples historias en un flujo narrativo coherente.

**Personalización por perfil de usuario.** El pipeline genera documentación para el rol definido en el campo `actor` del requisito. Un portal de ayuda que muestre contenido diferente según si el usuario autenticado es gestor de facturación o responsable financiero requiere una capa adicional de filtrado por rol que no está incluida en el pipeline base.

---

## Métricas de calidad de la documentación generada

El gobierno del modelo (punto 12 del modelo operativo) añade las siguientes métricas específicas de documentación al dashboard semanal:

| Métrica | Objetivo | Señal de alarma |
|---|---|---|
| Tasa de aprobación directa de documentos | >85% | Caída de >10 puntos en dos semanas |
| Documentos con términos no oficiales detectados | <5% | >15% en cualquier semana |
| Mensajes de error que coinciden literalmente con los AC | 100% | Cualquier discrepancia |
| Documentos regenerados automáticamente tras un cambio de requisito | >90% | <70% |
| Tiempo desde merge de historia hasta documentación publicada | <2 horas | >8 horas |

La métrica más importante es la última: la rapidez con la que la documentación refleja la realidad del sistema es lo que hace que los usuarios confíen en ella. Un sistema que actualiza automáticamente la documentación en menos de dos horas tras cada entrega transforma la percepción del equipo de documentación de carga a activo.

---

## Resumen

El pipeline de generación de documentación de usuario no es un componente nuevo del modelo operativo. Es la aplicación más directa de lo que ya está construido: los mismos requisitos YAML, el mismo glosario, los mismos criterios de aceptación y el mismo grafo de trazabilidad que alimentan el pipeline de Jira y el de test cases contienen toda la información necesaria para producir manuales de usuario, release notes y ayuda en línea contextual de calidad.

La diferencia entre el pipeline de documentación y los de artefactos Jira no es técnica sino de audiencia. El sistema de prompts cambia el destinatario (el usuario final en lugar del desarrollador o el QA), el tono (segunda persona imperativa en lugar de técnico-descriptivo) y la granularidad (una sección del manual por historia en lugar de una historia por requisito). El resto —el chunking, el RAG, la validación de terminología, el gate de aprobación, el registro en el grafo de trazabilidad y la detección de impacto de cambios— funciona exactamente igual.

El resultado es que el coste marginal de mantener la documentación de usuario actualizada en un proyecto que ya usa el modelo operativo es prácticamente cero. El trabajo de estructurar el requisito correctamente, que ya se hace para generar los artefactos Jira, produce automáticamente la documentación del usuario como subproducto.
