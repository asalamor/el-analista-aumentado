# Capítulo — Requisitos de accesibilidad y cumplimiento normativo

> **Nota de edición:** Este capítulo se sitúa en la Parte III del libro, después del Capítulo 12 (El orquestador) y antes del Capítulo 13 (Plan de adopción). Se puede publicar como capítulo independiente o como apéndice avanzado según la decisión editorial final. El hilo conductor de Meridian y el módulo EP-04 se mantienen intactos.

---

## En este capítulo

- Por qué los requisitos normativos son los que más frecuentemente se omiten y los más caros de corregir tarde.
- Cómo el pipeline detecta automáticamente cuándo un requisito activa obligaciones de WCAG 2.1 AA, RGPD o PSD2.
- Cómo generar criterios de aceptación de cumplimiento normativo que son verificables y que el equipo de QA puede ejecutar sin ser abogados ni expertos en accesibilidad.
- Cómo integrar estas capas en el YAML de requisito, en los prompts del pipeline y en la matriz de trazabilidad.

---

Carlos lleva tres sprints corrigiendo lo mismo. No son bugs de lógica de negocio ni de integración. Son errores que el equipo no vio venir: un formulario que no puede manejarse solo con teclado, un campo de importe sin etiqueta accesible, un log de auditoría de transacciones financieras que no se estaba generando. Cada corrección llega con su correspondiente deuda: horas de refactorización, conversaciones incómodas con el área legal y, en el caso del log de auditoría, una revisión urgente del equipo de seguridad antes de que el módulo llegara a producción.

Lo que Carlos no sabía al definir los requisitos es que cada uno de esos tres errores tenía una norma detrás que lo hacía obligatorio. No opcional. No recomendable. Obligatorio. WCAG 2.1 nivel AA para el formulario y el campo de importe. PSD2 y su Artículo 97 para el log de auditoría de operaciones de pago. Ninguno de los tres había activado una alerta en el pipeline porque el pipeline no sabía buscarlos.

Este capítulo resuelve ese problema. No convierte al analista en abogado ni en experto en accesibilidad. Lo que hace es enseñar al pipeline a reconocer cuándo un requisito tiene implicaciones normativas, generar automáticamente los criterios de aceptación que esas normas exigen, y dejar una traza que cualquier auditor puede seguir.

---

## El problema de los requisitos normativos invisibles

Hay un patrón que se repite en casi todos los proyectos de software en sectores regulados: los requisitos funcionales se definen con detalle, los requisitos técnicos se discuten en el refinamiento, y los requisitos normativos aparecen cuando alguien del área legal o de compliance los menciona en una reunión tardía o, peor, cuando un auditor los señala.

La razón no es negligencia. Es que los requisitos normativos tienen una característica que los hace difíciles de capturar en el flujo natural del análisis funcional: no los pide nadie explícitamente.

Ana López no va a entrar en una reunión de requisitos y decir "necesito que el formulario de alta de proveedor cumpla con el criterio de éxito 1.3.1 de WCAG 2.1 sobre información y relaciones". Lo que Ana va a decir es "necesito un formulario para dar de alta nuevos proveedores". El requisito normativo que acompaña a ese formulario está implícito en el contexto regulatorio de la organización, no en la solicitud de la usuaria de negocio.

Esa asimetría es la que el pipeline puede resolver. El analista captura lo que pide el negocio. El sistema detecta el contexto normativo y genera los criterios que la norma exige.

### Las tres normas que más frecuentemente se omiten

El modelo propuesto en este capítulo cubre tres marcos normativos que afectan a la mayoría de organizaciones que leen este libro.

**WCAG 2.1 nivel AA** (Web Content Accessibility Guidelines). El estándar internacional de accesibilidad para contenido web y aplicaciones. En la Unión Europea, la Directiva de Accesibilidad Web (2016/2102) lo hace obligatorio para organismos del sector público. La Ley General de Derechos de las Personas con Discapacidad lo extiende a servicios digitales relevantes en España. Muchas organizaciones privadas lo adoptan voluntariamente como estándar de calidad o por exigencia de sus clientes empresariales.

**RGPD** (Reglamento General de Protección de Datos, Reglamento UE 2016/679). Aplica a cualquier tratamiento de datos personales de personas físicas en la Unión Europea, independientemente de dónde esté establecida la organización que los trata. Sus implicaciones en los requisitos funcionales son amplias: desde el consentimiento hasta el derecho de supresión, pasando por la minimización de datos, la limitación del plazo de conservación y la notificación de brechas.

**PSD2** (Payment Services Directive 2, Directiva UE 2015/2366, transpuesta en España como Ley 18/2018). Aplica a cualquier organización que gestione servicios de pago, cuentas de pago o inicie operaciones de pago. Sus exigencias de autenticación reforzada (SCA), registros de auditoría y gestión de incidentes tienen traducción directa en requisitos funcionales que con frecuencia se definen incompletos o directamente se omiten.

> **💡 Idea clave:** Las tres normas comparten una característica que las hace especialmente compatibles con el pipeline: sus exigencias son concretas, verificables y reproducibles. No son principios abstractos. Son condiciones que pueden expresarse en formato Dado/Cuando/Entonces y ejecutarse en un test.

---

## La capa normativa en el modelo de datos

Antes de construir los prompts, hace falta extender la arquitectura de datos del pipeline para que pueda razonar sobre obligaciones normativas. Esto implica dos adiciones al modelo existente.

### Extensión del glosario: el catálogo de normas

El glosario estructurado del Capítulo 5 es el lugar natural donde vive el conocimiento normativo del proyecto. Se añade una sección `normas` que el pipeline consultará durante la validación y la generación.

```yaml
# glosario.yaml — Sección de normas (añadir al glosario existente de Meridian)

normas:
  - id: NORM-WCAG
    nombre_oficial: "WCAG 2.1 nivel AA"
    tipo: accesibilidad
    ambito: "Toda interfaz de usuario accesible vía navegador o aplicación móvil"
    obligatoriedad: "Obligatorio para servicios públicos digitales (Dir. 2016/2102).
      Recomendado como estándar de calidad para servicios privados."
    # Los criterios de éxito más frecuentes en aplicaciones de gestión.
    # No es la lista completa de WCAG 2.1 AA — es la lista relevante
    # para el contexto de Meridian. Ampliar según el tipo de proyecto.
    criterios_relevantes:
      - id: "1.1.1"
        nombre: "Contenido no textual"
        descripcion: "Todo contenido no textual tiene una alternativa textual."
        activado_por: ["imagen", "icono funcional", "gráfico", "diagrama"]
        criterio_ac_tipo: "El componente <X> tiene atributo alt o aria-label descriptivo"
      - id: "1.3.1"
        nombre: "Información y relaciones"
        descripcion: >
          La estructura, relaciones y significado del contenido pueden
          determinarse programáticamente o están disponibles en texto.
        activado_por: ["formulario", "tabla", "lista", "encabezado", "campo de entrada"]
        criterio_ac_tipo: "Los campos del formulario <X> tienen etiquetas asociadas programáticamente"
      - id: "1.4.3"
        nombre: "Contraste mínimo"
        descripcion: >
          El texto y las imágenes de texto tienen una relación de contraste
          de al menos 4.5:1 (texto normal) o 3:1 (texto grande).
        activado_por: ["texto", "botón", "enlace", "mensaje de estado"]
        criterio_ac_tipo: "El ratio de contraste del texto en <X> es >= 4.5:1"
      - id: "2.1.1"
        nombre: "Teclado"
        descripcion: >
          Toda la funcionalidad está disponible desde un teclado sin requerir
          tiempos específicos de pulsación de tecla.
        activado_por: ["formulario", "modal", "menú", "control interactivo", "acción"]
        criterio_ac_tipo: "La acción <X> puede completarse usando solo el teclado"
      - id: "2.4.3"
        nombre: "Orden del foco"
        descripcion: >
          Si una página web puede navegarse de forma secuencial y las secuencias
          de navegación afectan al significado u operación, los componentes
          reciben el foco en un orden que preserva el significado y la operabilidad.
        activado_por: ["modal", "wizard", "formulario de varios pasos"]
        criterio_ac_tipo: "El orden de tabulación en <X> es lógico y coherente con el flujo visual"
      - id: "3.3.1"
        nombre: "Identificación de errores"
        descripcion: >
          Si se detecta automáticamente un error de entrada, el elemento erróneo
          se identifica y el error se describe al usuario en texto.
        activado_por: ["formulario", "campo de entrada", "validación"]
        criterio_ac_tipo: "Los mensajes de error en <X> identifican el campo afectado y describen el problema"
      - id: "4.1.2"
        nombre: "Nombre, función, valor"
        descripcion: >
          Para todos los componentes de interfaz de usuario, el nombre y la función
          pueden determinarse programáticamente.
        activado_por: ["botón", "campo de entrada", "control personalizado", "widget"]
        criterio_ac_tipo: "El componente <X> tiene rol ARIA correcto y nombre accesible"

  - id: NORM-RGPD
    nombre_oficial: "RGPD — Reglamento (UE) 2016/679"
    tipo: privacidad_datos
    ambito: "Todo tratamiento de datos personales de personas físicas en la UE"
    obligatoriedad: "Obligatorio. Sanciones de hasta 20M€ o el 4% del volumen de negocio global."
    criterios_relevantes:
      - id: "Art6"
        nombre: "Base jurídica del tratamiento"
        descripcion: >
          El tratamiento solo es lícito si existe al menos una base jurídica:
          consentimiento, contrato, obligación legal, interés vital,
          misión de interés público o interés legítimo.
        activado_por: ["dato personal", "dato de contacto", "NIF", "CIF persona física",
                       "dirección", "email", "teléfono", "nombre"]
        criterio_ac_tipo: >
          El sistema no permite almacenar <dato> sin que exista base jurídica
          documentada y aprobada por el DPO
      - id: "Art13"
        nombre: "Información al interesado"
        descripcion: >
          Cuando se recaben datos personales directamente del interesado,
          se le debe informar de la finalidad, base jurídica, destinatarios
          y derechos en el momento de la recogida.
        activado_por: ["formulario de registro", "alta de usuario", "alta de proveedor persona física",
                       "recogida de datos de contacto"]
        criterio_ac_tipo: >
          El formulario <X> muestra el aviso de privacidad antes de enviar datos
          e incluye enlace a la política de privacidad completa
      - id: "Art17"
        nombre: "Derecho de supresión"
        descripcion: >
          El interesado tiene derecho a obtener la supresión de sus datos
          personales cuando ya no sean necesarios, retire el consentimiento,
          se oponga al tratamiento u otros supuestos.
        activado_por: ["perfil de usuario", "datos de contacto", "datos personales almacenados"]
        criterio_ac_tipo: >
          El sistema permite solicitar la supresión de datos del <interesado>
          y responde en el plazo máximo de 30 días
      - id: "Art25"
        nombre: "Privacidad desde el diseño y por defecto"
        descripcion: >
          El responsable del tratamiento aplica las medidas técnicas apropiadas
          para garantizar que, por defecto, solo sean objeto de tratamiento
          los datos personales necesarios para cada fin.
        activado_por: ["formulario", "campo de entrada", "dato personal", "exportación de datos"]
        criterio_ac_tipo: >
          El formulario/sistema <X> recoge únicamente los campos necesarios
          para la finalidad declarada; no hay campos opcionales que recojan
          más datos de los necesarios
      - id: "Art30"
        nombre: "Registro de actividades de tratamiento"
        descripcion: >
          El responsable y el encargado del tratamiento mantienen un registro
          de las actividades de tratamiento efectuadas bajo su responsabilidad.
        activado_por: ["nuevo tratamiento de datos personales", "nueva finalidad de tratamiento"]
        criterio_ac_tipo: >
          El nuevo tratamiento de <datos> con finalidad <X> está registrado
          en el RAT antes de la puesta en producción
      - id: "Art32"
        nombre: "Seguridad del tratamiento"
        descripcion: >
          Medidas técnicas y organizativas apropiadas para garantizar un nivel
          de seguridad adecuado al riesgo: seudonimización, cifrado, garantías
          de confidencialidad, integridad, disponibilidad y resiliencia.
        activado_por: ["datos de salud", "datos financieros", "datos de identidad",
                       "contraseña", "token", "datos sensibles"]
        criterio_ac_tipo: >
          Los datos de <categoría> se almacenan cifrados en reposo
          y en tránsito con protocolos actuales (AES-256, TLS 1.3 o superior)

  - id: NORM-PSD2
    nombre_oficial: "PSD2 — Directiva (UE) 2015/2366"
    tipo: servicios_pago
    ambito: >
      Toda organización que preste servicios de pago, gestione cuentas de pago
      o inicie operaciones de pago en la UE.
    obligatoriedad: >
      Obligatorio para entidades de pago autorizadas y sus proveedores de servicios.
      Verificar con el área legal si aplica a la organización.
    criterios_relevantes:
      - id: "Art97"
        nombre: "Autenticación reforzada de clientes (SCA)"
        descripcion: >
          Los proveedores de servicios de pago aplican SCA cuando el ordenante
          accede a su cuenta de pago en línea, inicia una operación de pago
          electrónico o realiza cualquier acción a distancia que pueda implicar
          riesgo de fraude.
          SCA requiere al menos dos factores independientes de: algo que el usuario
          sabe, algo que posee, algo que es.
        activado_por: ["operación de pago", "acceso a cuenta de pago", "autorización de pago",
                       "transferencia", "domiciliación", "cargo"]
        criterio_ac_tipo: >
          La operación <X> requiere autenticación con al menos dos factores
          independientes antes de ejecutarse
      - id: "Art96"
        nombre: "Notificación de incidentes de seguridad"
        descripcion: >
          Los proveedores de servicios de pago notifican a la autoridad competente
          los incidentes de seguridad graves sin dilación.
        activado_por: ["fallo de autenticación", "acceso no autorizado", "brecha de datos de pago"]
        criterio_ac_tipo: >
          El sistema registra y clasifica los eventos de seguridad en <X>
          con suficiente detalle para evaluar el umbral de notificación a la autoridad
      - id: "RTS-SCA-Art22"
        nombre: "Registro de auditoría de operaciones"
        descripcion: >
          Las operaciones de pago y las solicitudes de autenticación deben quedar
          registradas con los datos necesarios para investigar incidentes:
          timestamp, identidad del ordenante, importe, canal, resultado.
        activado_por: ["operación de pago", "autorización", "rechazo de pago",
                       "sesión de pago", "callback de pago"]
        criterio_ac_tipo: >
          Cada operación de pago en <X> genera un registro de auditoría
          inmutable con: timestamp UTC, id_usuario, importe, moneda, resultado
          y canal de acceso
      - id: "RTS-SCA-Art4"
        nombre: "Vinculación dinámica"
        descripcion: >
          Para las operaciones de pago remotas, el código de autenticación
          debe ser específico para el importe y el beneficiario de la operación.
          El usuario debe ser consciente del importe y el beneficiario.
        activado_por: ["confirmación de pago", "autorización de transferencia"]
        criterio_ac_tipo: >
          La pantalla de confirmación de <X> muestra importe y beneficiario
          antes de solicitar el factor de autenticación, y el código generado
          es único para esa combinación de importe y beneficiario
```

### Extensión del Bloque 1 del requisito: el campo `cumplimiento_normativo`

Cuando el analista detecta que un requisito tiene implicaciones normativas, las documenta en el Bloque 1 del YAML. Si no las detecta, el pipeline las infiere y las añade como advertencia en el informe de validación.

```yaml
# Extensión del Bloque 1 — Identidad del requisito
# Añadir a la plantilla base del Capítulo 4

cumplimiento_normativo:
  # La IA rellena este campo automáticamente durante la validación.
  # El analista puede completarlo antes si lo conoce de antemano.
  # Si está vacío, el validador analiza el requisito y propone los marcos aplicables.
  normas_aplicables: []
  # Ejemplo para un requisito de formulario con datos personales:
  # normas_aplicables:
  #   - norma: NORM-WCAG
  #     criterios: ["1.3.1", "2.1.1", "3.3.1", "4.1.2"]
  #     motivo: "El formulario recoge datos de contacto del proveedor"
  #   - norma: NORM-RGPD
  #     criterios: ["Art6", "Art13", "Art25"]
  #     motivo: "Se recogen datos personales de persona física (nombre, email, teléfono)"
  evidencia_requerida: ""
  # Qué documentación debe existir antes de la puesta en producción:
  # "DIA aprobada por el DPO", "entrada en el RAT", "informe de accesibilidad", etc.
  revision_legal_requerida: false
  # true si el área legal debe revisar antes de validar el requisito
```

---

## El prompt de detección normativa

Este prompt se ejecuta como parte del paso de validación del Capítulo 7, justo después de la validación semántica. Analiza el contenido del requisito, lo cruza contra el catálogo de normas del glosario y determina qué marcos normativos aplican y por qué.

> 📋 **Prompt de IA — Detección normativa automática**
>
> ```
> Eres un especialista en cumplimiento normativo para aplicaciones de software
> en el sector financiero europeo. Tu función es analizar requisitos funcionales
> y detectar qué marcos normativos son aplicables, qué criterios concretos
> activan y qué criterios de aceptación de cumplimiento deben añadirse.
>
> REGLAS:
> 1. Solo señala una norma como aplicable si el requisito activa explícitamente
>    uno de los disparadores definidos en el catálogo de normas.
>    No actives normas por precaución genérica.
> 2. Para cada norma aplicable, genera los criterios de aceptación de cumplimiento
>    en formato Dado/Cuando/Entonces, igual que los criterios funcionales.
>    Los criterios de cumplimiento son verificables y ejecutables en un test.
> 3. Si un campo `cumplimiento_normativo` ya existe en el requisito,
>    amplíalo con lo que falta. No elimines lo que ya está.
> 4. Si la norma requiere acción fuera del pipeline (revisión legal, entrada en RAT,
>    aprobación del DPO), añádelo en `evidencia_requerida`.
> 5. El output es siempre JSON válido. Sin texto fuera del JSON.
>
> CATÁLOGO DE NORMAS DEL PROYECTO:
> {{normas_glosario}}
>
> REQUISITO A ANALIZAR:
> {{requisito_yaml}}
>
> Genera:
> {
>   "normas_detectadas": [
>     {
>       "norma_id": "NORM-WCAG",
>       "criterios_aplicables": ["1.3.1", "2.1.1"],
>       "motivo_deteccion": "[Por qué se activa esta norma en este requisito]",
>       "disparadores_encontrados": ["[campo o elemento que activa la norma]"]
>     }
>   ],
>   "criterios_ac_cumplimiento": [
>     {
>       "id": "AC-{{req_id}}-NORM-01",
>       "norma": "NORM-WCAG",
>       "criterio_wcag_rgpd_psd2": "1.3.1",
>       "titulo": "[Qué verifica este criterio de cumplimiento]",
>       "dado": "[Estado previo relevante para la verificación normativa]",
>       "cuando": "[Acción que activa la verificación]",
>       "entonces": "[Comportamiento requerido por la norma, observable y verificable]",
>       "herramienta_verificacion": "[axe-core, WAVE, prueba manual con lector de pantalla, etc.]"
>     }
>   ],
>   "evidencia_requerida": "[Documentación obligatoria antes de producción, o vacío]",
>   "revision_legal_requerida": true,
>   "alertas": [
>     "[Advertencia sobre implicaciones normativas que el analista debe conocer]"
>   ]
> }
> ```

### Ejemplo de detección aplicado a Meridian

Meridian está extendiendo el módulo EP-04 con un formulario de alta de nuevos proveedores. El analista, Carlos, ha definido el requisito REQ-041 con los campos habituales de la plantilla, sin entrar en detalle normativo. El pipeline analiza el requisito y devuelve lo siguiente.

**Requisito de entrada (fragmento relevante):**

```yaml
id: REQ-041
titulo: "Dar de alta un nuevo proveedor en el sistema"
actor: "Gestor de facturación"
descripcion: >
  El gestor de facturación necesita poder registrar nuevos proveedores en el sistema
  antes de asociarles facturas. El formulario recoge los datos identificativos
  del proveedor: razón social, CIF, dirección fiscal, email de contacto,
  teléfono y nombre del responsable de facturación.
datos_entrada:
  - nombre: razon_social
    tipo: string
    requerido: true
  - nombre: cif
    tipo: string
    requerido: true
    descripcion: "NIF o CIF del proveedor"
  - nombre: email_contacto
    tipo: string
    requerido: false
  - nombre: nombre_responsable
    tipo: string
    requerido: false
    descripcion: "Nombre de la persona de contacto para facturación"
```

**Output del prompt de detección:**

```json
{
  "normas_detectadas": [
    {
      "norma_id": "NORM-RGPD",
      "criterios_aplicables": ["Art6", "Art13", "Art25", "Art30"],
      "motivo_deteccion": "El formulario recoge datos personales de personas físicas:
        'nombre_responsable' y 'email_contacto' son datos de una persona física
        identificable. Aunque el proveedor sea una persona jurídica, el responsable
        de facturación es una persona física cuyos datos se tratan.",
      "disparadores_encontrados": ["nombre_responsable", "email_contacto", "formulario de alta"]
    },
    {
      "norma_id": "NORM-WCAG",
      "criterios_aplicables": ["1.3.1", "2.1.1", "3.3.1", "4.1.2"],
      "motivo_deteccion": "El requisito describe un formulario interactivo con
        campos de entrada. Todos los criterios de accesibilidad relacionados
        con formularios son aplicables.",
      "disparadores_encontrados": ["formulario", "campo de entrada", "acción de registro"]
    }
  ],
  "criterios_ac_cumplimiento": [
    {
      "id": "AC-041-NORM-01",
      "norma": "NORM-RGPD",
      "criterio_wcag_rgpd_psd2": "Art13",
      "titulo": "El formulario de alta muestra el aviso de privacidad antes del envío",
      "dado": "El gestor de facturación está rellenando el formulario de alta de proveedor",
      "cuando": "Antes de poder enviar el formulario",
      "entonces": "Se muestra un aviso de privacidad que indica finalidad del tratamiento,
        base jurídica, responsable del tratamiento y enlace a la política completa.
        El formulario no puede enviarse sin que el aviso sea visible.",
      "herramienta_verificacion": "Revisión manual del formulario en la interfaz"
    },
    {
      "id": "AC-041-NORM-02",
      "norma": "NORM-RGPD",
      "criterio_wcag_rgpd_psd2": "Art25",
      "titulo": "El formulario no recoge más datos de los necesarios para la finalidad",
      "dado": "El formulario de alta de proveedor está disponible en el sistema",
      "cuando": "Se revisan los campos del formulario",
      "entonces": "Los únicos campos del formulario son los definidos en el requisito.
        No hay campos ocultos ni campos adicionales que no estén justificados
        por la finalidad de identificación del proveedor.",
      "herramienta_verificacion": "Revisión del código del formulario + auditoría de red"
    },
    {
      "id": "AC-041-NORM-03",
      "norma": "NORM-WCAG",
      "criterio_wcag_rgpd_psd2": "1.3.1",
      "titulo": "Los campos del formulario tienen etiquetas asociadas programáticamente",
      "dado": "El formulario de alta de proveedor está cargado en el navegador",
      "cuando": "Se inspeccionan los campos con una herramienta de accesibilidad",
      "entonces": "Cada campo de entrada tiene un elemento label asociado mediante
        el atributo 'for' o está encapsulado en el label. Los campos sin label
        visible tienen un atributo aria-label o aria-labelledby.",
      "herramienta_verificacion": "axe-core en modo automatizado + NVDA con Chrome"
    },
    {
      "id": "AC-041-NORM-04",
      "norma": "NORM-WCAG",
      "criterio_wcag_rgpd_psd2": "2.1.1",
      "titulo": "El formulario completo puede enviarse usando solo el teclado",
      "dado": "El gestor de facturación accede al formulario de alta sin usar el ratón",
      "cuando": "Navega por todos los campos con la tecla Tab y envía el formulario con Enter",
      "entonces": "Todos los campos reciben el foco en el orden visual lógico.
        El formulario se envía correctamente sin requerir el uso del ratón en ningún paso.",
      "herramienta_verificacion": "Prueba manual de navegación por teclado"
    },
    {
      "id": "AC-041-NORM-05",
      "norma": "NORM-WCAG",
      "criterio_wcag_rgpd_psd2": "3.3.1",
      "titulo": "Los errores de validación identifican el campo afectado y describen el problema",
      "dado": "El gestor de facturación envía el formulario con el campo 'CIF' vacío",
      "cuando": "El sistema procesa la validación",
      "entonces": "Aparece un mensaje de error que identifica el campo CIF de forma explícita
        (no solo un error genérico) y describe qué debe introducirse.
        El mensaje de error es perceptible tanto visualmente como para lectores de pantalla.",
      "herramienta_verificacion": "Prueba manual de validación + axe-core"
    }
  ],
  "evidencia_requerida": "Alta del tratamiento 'Datos de contacto de responsables de proveedor'
    en el Registro de Actividades de Tratamiento (RAT) aprobada por el DPO antes de la puesta
    en producción. Solicitar a dpo@meridian.es con el modelo de formulario adjunto.",
  "revision_legal_requerida": true,
  "alertas": [
    "El campo 'nombre_responsable' recoge datos de una persona física. Aunque el proveedor
     sea una entidad jurídica, este campo activa obligaciones RGPD. Confirmar con el DPO
     si se requiere base jurídica específica o si queda amparado por el contrato con el proveedor.",
    "Si el campo 'email_contacto' se usará para comunicaciones comerciales, se requiere
     consentimiento explícito adicional (LSSI-CE Art. 21). Confirmar con el área de marketing
     si existe esa intención de uso."
  ]
}
```

> **⚠️ Error frecuente:** Tratar los criterios de accesibilidad como criterios opcionales que "ya se verán en QA". En la práctica, un criterio de accesibilidad descubierto en QA requiere cambios en el marcado HTML, en los componentes del design system y a veces en el diseño visual. El coste de detectarlo en el requisito es cero. El coste de detectarlo en QA puede ser días de refactorización.

---

## Integración en el pipeline existente

Los criterios de cumplimiento normativo generados por el prompt de detección se integran en el pipeline del Capítulo 8 (generación de artefactos Jira) de tres formas.

### En la historia de usuario

Los criterios `AC-XXX-NORM-NN` se añaden a la lista de `acceptance_criteria` de la historia generada por el Prompt 2. En Jira aparecen como criterios de aceptación estándar, indistinguibles de los criterios funcionales, con la única diferencia de que llevan el campo `norma` que permite filtrarlos y reportarlos de forma independiente.

```yaml
# Fragmento de la historia generada para REQ-041
acceptance_criteria:
  # Criterios funcionales (generados por Prompt 2)
  - id: AC-041-01
    dado: "El gestor accede al formulario de alta de proveedor"
    cuando: "Introduce todos los campos obligatorios y pulsa Guardar"
    entonces: "El proveedor queda registrado y aparece en el listado de proveedores activos"
  # Criterios de cumplimiento (añadidos por el prompt de detección normativa)
  - id: AC-041-NORM-01
    norma: "RGPD Art13"
    dado: "El gestor está rellenando el formulario de alta de proveedor"
    cuando: "Antes de poder enviar el formulario"
    entonces: "Se muestra un aviso de privacidad con finalidad, base jurídica y enlace a política"
    herramienta_verificacion: "Revisión manual"
  - id: AC-041-NORM-03
    norma: "WCAG 1.3.1"
    dado: "El formulario de alta está cargado en el navegador"
    cuando: "Se inspeccionan los campos con axe-core"
    entonces: "Cada campo tiene label asociado programáticamente o aria-label/aria-labelledby"
    herramienta_verificacion: "axe-core automatizado"
```

### En las tareas técnicas

El Prompt 3 del Capítulo 8 recibe los criterios normativos como contexto adicional y genera tareas específicas de implementación. La instrucción de contexto adicional para cumplimiento normativo que se añade al Prompt 3 es la siguiente.

> 📋 **Prompt de IA — Variante para cumplimiento normativo en tareas técnicas**
>
> ```
> CONTEXTO ADICIONAL — CUMPLIMIENTO NORMATIVO:
> Este requisito tiene criterios de aceptación de cumplimiento normativo que
> implican trabajo técnico específico no cubierto por los criterios funcionales.
>
> CRITERIOS NORMATIVOS DETECTADOS:
> {{criterios_ac_cumplimiento}}
>
> Para cada criterio normativo, añade una tarea técnica específica si implica
> trabajo técnico diferenciado:
> - WCAG: tareas de marcado semántico, ARIA, contraste y navegación por teclado.
>   Capa: frontend. Asignar al mismo sprint que la tarea de implementación del componente.
> - RGPD: tareas de integración con el RAT, aviso de privacidad, cifrado de campos sensibles.
>   Capa: según el tipo (frontend para el aviso, backend/BD para cifrado y RAT).
> - PSD2: tareas de registro de auditoría inmutable, SCA, vinculación dinámica.
>   Capa: backend y BD.
>
> Las tareas normativas NO son opcionales. Marcarlas con label: ["cumplimiento",
> "norma-WCAG"/"norma-RGPD"/"norma-PSD2"] para facilitar el seguimiento.
> ```

El resultado para REQ-041 de Meridian genera, además de las tareas funcionales habituales, tareas como estas:

```json
{
  "issue_type": "Task",
  "summary": "Implementar marcado semántico y etiquetas ARIA en el formulario de alta de proveedor",
  "capa": "frontend",
  "parent_story": "FACT-63",
  "description": {
    "objetivo": "Garantizar que todos los campos del formulario de alta de proveedor tienen
      etiquetas asociadas programáticamente (criterio WCAG 1.3.1) y que el formulario
      es completamente operable con teclado (criterio 2.1.1). Los mensajes de error
      identifican el campo afectado y son perceptibles por lectores de pantalla (3.3.1).",
    "criterios_tecnico": [
      "Todos los inputs tienen <label for> o aria-label/aria-labelledby asociado",
      "El formulario puede enviarse completo usando solo Tab y Enter",
      "Los mensajes de error usan role='alert' o aria-live para lectores de pantalla",
      "La verificación con axe-core no genera errores de nivel AA"
    ],
    "consideraciones": [
      "Reutilizar los componentes accesibles del design system si están disponibles",
      "Si no existe componente accesible para el campo CIF, crearlo en esta tarea"
    ],
    "referencias": ["WCAG 2.1 criterios 1.3.1, 2.1.1, 3.3.1, 4.1.2", "Design system: InputField"]
  },
  "estimacion_horas": 4,
  "labels": ["frontend", "cumplimiento", "norma-WCAG", "facturacion"]
}
```

### En la trazabilidad

El grafo del Capítulo 11 añade un tipo de nodo `criterio_normativo` y un tipo de arista `verifica_cumplimiento` que conecta los criterios normativos con los test cases que los ejecutan.

```sql
-- Extensión del esquema del Capítulo 11 para trazabilidad normativa

-- Los criterios normativos son nodos del grafo como cualquier otro artefacto
INSERT INTO nodos_trazabilidad (id, tipo, titulo, estado, metadatos)
VALUES (
  'AC-041-NORM-01',
  'criterio_normativo',                          -- nuevo tipo
  'RGPD Art13: Aviso de privacidad en el formulario de alta',
  'activo',
  '{"norma": "NORM-RGPD", "articulo": "Art13", "requisito_origen": "REQ-041"}'
);

-- Los test cases que verifican cumplimiento se vinculan con tipo de arista específico
INSERT INTO aristas_trazabilidad (origen_id, destino_id, tipo_relacion, confianza, origen_relacion)
VALUES (
  'TC-041-NORM-01',           -- test case de cumplimiento
  'AC-041-NORM-01',           -- criterio normativo que verifica
  'verifica_cumplimiento',    -- nuevo tipo de arista
  1.0,
  'pipeline_generacion'
);
```

Esta extensión del grafo permite responder a preguntas como "¿cuántos criterios RGPD están cubiertos por test cases?" o "¿qué historias del sprint tienen criterios de accesibilidad pendientes de verificar?" sin necesidad de revisar manualmente Jira o Xray.

---

## El informe de cumplimiento normativo

Con el grafo extendido, el sistema puede generar un informe de cumplimiento normativo por épica o por sprint. Este informe es el documento que el área legal, el DPO o un auditor externo necesita para verificar que los requisitos normativos se han definido, implementado y probado.

> 📋 **Prompt de IA — Informe de cumplimiento normativo**
>
> ```
> A partir de la matriz de trazabilidad de la épica {{epica_id}},
> genera el informe de cumplimiento normativo.
>
> DATOS DE TRAZABILIDAD:
> {{matriz_trazabilidad_json}}
>
> CATÁLOGO DE NORMAS APLICABLES AL PROYECTO:
> {{normas_glosario}}
>
> Genera un informe JSON con esta estructura:
>
> {
>   "informe_cumplimiento": {
>     "epica_id": "{{epica_id}}",
>     "fecha": "{{fecha}}",
>     "resumen_ejecutivo": "[Estado del cumplimiento en 2-3 frases para el DPO o auditor]",
>     "por_norma": [
>       {
>         "norma": "NORM-RGPD",
>         "criterios_requeridos": N,
>         "criterios_con_ac": N,
>         "criterios_con_test": N,
>         "criterios_test_pasado": N,
>         "porcentaje_cobertura": "N%",
>         "gaps": ["[Criterio normativo sin cobertura de test]"],
>         "evidencias_pendientes": ["[Documentación requerida antes de producción]"]
>       }
>     ],
>     "semaforo_global": "verde | amarillo | rojo",
>     "listo_para_produccion": true,
>     "acciones_requeridas": [
>       {
>         "urgencia": "bloqueante | recomendada",
>         "accion": "[Qué hay que hacer]",
>         "responsable": "analista | DPO | legal | tech_lead",
>         "plazo": "[Cuándo debe estar resuelto]"
>       }
>     ]
>   }
> }
> ```

### El informe real de Meridian al cierre del Sprint 8

Al cierre del sprint en que se implementa REQ-041, el sistema genera automáticamente el informe de cumplimiento para la épica EP-08 (Alta y gestión de proveedores). David Sanz lo recibe junto al resumen habitual del sprint.

```
INFORME DE CUMPLIMIENTO — EP-08 Alta y gestión de proveedores
Fecha: cierre Sprint 8

Resumen ejecutivo: La épica tiene cobertura completa de criterios de accesibilidad
WCAG AA (8/8 test cases pasados). Los criterios RGPD tienen cobertura parcial:
el aviso de privacidad está implementado y verificado, pero la entrada en el RAT
sigue pendiente de aprobación por el DPO. El sistema no debe pasar a producción
hasta que esa acción esté completada.

Por norma:
  NORM-WCAG: 8 criterios / 8 con AC / 8 con test / 8 pasados → 100% ✅
  NORM-RGPD: 4 criterios / 4 con AC / 4 con test / 3 pasados → 75% ⚠️
    Gap: AC-041-NORM-RAT (entrada en RAT) no tiene test pasado porque
         la acción es organizativa, no técnica. Pendiente de aprobación del DPO.

Semáforo global: AMARILLO
Listo para producción: NO

Acciones requeridas:
  [BLOQUEANTE] Obtener aprobación del DPO para la entrada en el RAT.
  Responsable: Carlos Ruiz (analista). Plazo: antes del despliegue a producción.
  Contacto: dpo@meridian.es. Referencia: REQ-041, tratamiento 'Datos contacto proveedor'.
```

La primera vez que Carlos ve ese informe tiene una reacción que resume bien el valor del sistema: "Nunca antes habíamos tenido esta conversación antes de ir a producción."

---

## Lo que el sistema no puede hacer

Ser honesto sobre las limitaciones de este componente es tan importante como describir sus capacidades.

**No sustituye al DPO ni al asesor legal.** El sistema detecta qué normas son aplicables basándose en patrones en el texto del requisito. No interpreta la norma en casos fronterizos, no valora el riesgo del tratamiento y no puede determinar si una base jurídica concreta es suficiente para un tratamiento específico. Esas decisiones requieren un profesional.

**La detección no es exhaustiva.** El catálogo de normas del glosario cubre los criterios más frecuentes, no todos. Un requisito puede activar obligaciones normativas que el catálogo no contempla. El sistema reduce el riesgo de omisión, no lo elimina.

**Los criterios de accesibilidad generados son de nivel AA.** Nivel AAA de WCAG y requisitos sectoriales adicionales (como los específicos de los servicios de la Administración Pública española) requieren ajustes manuales al catálogo.

**El razonamiento sobre PSD2 asume que la organización es entidad de pago.** Si la organización actúa únicamente como comercio (sin gestionar cuentas de pago ni iniciar operaciones), muchos criterios de PSD2 no aplican. El analista debe confirmar el alcance con el área legal antes de activar la sección PSD2 en el glosario.

> **🛠️ En la práctica:** En Meridian, Carlos acordó con el DPO una reunión mensual de 30 minutos para revisar los informes de cumplimiento del mes y validar las entradas en el RAT generadas por el pipeline. Lo que antes era una conversación tardía y tensa ("esto ya está en producción y no hemos hecho la Evaluación de Impacto") se convirtió en una revisión rutinaria de documentos ya generados. El DPO de Meridian usó el informe de cumplimiento del pipeline en la primera auditoría de RGPD posterior como evidencia del proceso de privacidad desde el diseño.

---

## Lo que funciona en la práctica

La integración de la capa normativa en el pipeline tiene tres efectos que van más allá del cumplimiento estricto.

**Acelera las conversaciones con el área legal.** Cuando Carlos lleva un informe de cumplimiento automáticamente generado a la reunión con el DPO, la conversación cambia de naturaleza. No es "¿hemos pensado en la privacidad?" sino "el sistema detectó estos cuatro criterios, los tres primeros están cubiertos, ¿este cuarto requiere base jurídica adicional?". El tiempo de la reunión se invierte en la decisión, no en el inventario.

**Hace visible el trabajo de accesibilidad.** Antes del pipeline, los criterios de accesibilidad no aparecían en Jira y por tanto no existían para el proceso de planificación. Ahora son tareas con estimación, responsable y criterio de completitud, igual que cualquier tarea técnica. Eso tiene un efecto colateral inesperado: el equipo de frontend empieza a diseñar pensando en accesibilidad desde el principio, no como un paso final de revisión.

**Crea una cultura de cumplimiento preventivo.** El primer sprint en que el informe bloquea un despliegue a producción por una entrada de RAT pendiente genera algo de fricción. El segundo sprint, Carlos incluye la solicitud al DPO en su checklist de finalización de requisito, al mismo nivel que la estimación de story points. Al tercer sprint, el DPO tiene los documentos antes de que Carlos los pida.

---

## Tres puntos clave

El cumplimiento normativo es técnico, no solo legal. WCAG, RGPD y PSD2 tienen requisitos que se pueden expresar en Dado/Cuando/Entonces y verificar en un test, igual que cualquier criterio funcional. El pipeline los trata exactamente igual.

La detección automática no elimina la responsabilidad del analista, pero sí elimina la omisión por desconocimiento. El sistema señala lo que la norma exige; el analista y el área legal validan que la interpretación es correcta para el caso concreto.

El informe de cumplimiento es un artefacto de gobierno, no solo de desarrollo. Es el documento que conecta el trabajo del sprint con las obligaciones legales de la organización, y que permite a cualquier auditor reconstruir el rastro desde el requisito hasta el test pasado.

---

## Pregunta de reflexión para el equipo

¿Cuántos de los requisitos actualmente en el backlog de vuestro proyecto recogen datos personales de personas físicas sin que el DPO haya sido informado del tratamiento?

---

## Apéndice del capítulo: catálogo mínimo de reglas de detección

Para equipos que quieran extender el catálogo de normas más allá de los ejemplos de Meridian, esta tabla resume los disparadores más frecuentes por tipo de elemento de interfaz.

| Elemento de requisito | WCAG aplicable | RGPD aplicable | PSD2 aplicable |
|---|---|---|---|
| Formulario con campos de entrada | 1.3.1, 2.1.1, 3.3.1, 4.1.2 | Art25 (minimización) | — |
| Campo que recoge nombre, email o teléfono de persona física | — | Art6, Art13, Art25, Art30 | — |
| Campo de contraseña o token | — | Art32 (seguridad) | Art97 si es pago |
| Imagen o icono funcional | 1.1.1, 4.1.2 | — | — |
| Tabla de datos | 1.3.1 | — | — |
| Modal o diálogo | 2.1.1, 2.4.3, 4.1.2 | — | — |
| Mensaje de estado o notificación | 1.4.1, 4.1.3 | — | — |
| Exportación de datos personales | — | Art25, Art32 | — |
| Acción de eliminación de usuario o datos | — | Art17 | — |
| Operación de pago o autorización | — | — | Art97 (SCA), RTS Art22 (log), RTS Art4 (vinculación) |
| Confirmación de transferencia | — | — | RTS Art4 |
| Log o registro de actividad de pago | — | — | RTS Art22 |
| Sesión de usuario con tiempo de expiración | 2.2.1 | — | — |
| Datos de salud o categorías especiales | — | Art9 (categorías especiales) | — |

> **💡 Idea clave:** Este catálogo no es un sustituto del asesoramiento legal. Es una red de captura para las implicaciones normativas más frecuentes que el análisis funcional habitual deja pasar. El DPO y el área legal son los que validan que la interpretación es correcta para el contexto específico de cada organización.
