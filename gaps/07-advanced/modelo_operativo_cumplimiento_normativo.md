# Requisitos de accesibilidad y cumplimiento normativo

Los requisitos normativos comparten un patrón que los hace especialmente problemáticos en el análisis funcional tradicional: nadie los pide explícitamente. El usuario de negocio solicita un formulario de alta de proveedores. No solicita que cumpla WCAG 2.1 AA, ni que tenga un aviso de privacidad conforme al artículo 13 del RGPD, ni que los datos personales recogidos estén registrados en el RAT antes de ir a producción. Esas obligaciones existen con independencia de que se pidan, y el coste de detectarlas tarde es desproporcionado: los criterios de accesibilidad descubiertos en QA implican refactorización del marcado semántico; los de privacidad descubiertos en producción pueden implicar sanciones.

El pipeline puede resolver esta asimetría. El analista captura lo que el negocio pide. El sistema detecta el contexto normativo y genera automáticamente los criterios de aceptación que las normas exigen, con el mismo formato verificable que cualquier criterio funcional.

Este punto desarrolla:

- La extensión del glosario con el catálogo de normas como contexto activo del pipeline.
- La extensión de la plantilla YAML con el campo `cumplimiento_normativo`.
- El prompt de detección normativa automática.
- Cómo los criterios de cumplimiento se integran en la generación de artefactos Jira, en los test cases y en la matriz de trazabilidad.
- El prompt de informe de cumplimiento normativo por épica o por sprint.
- Los límites del sistema: qué puede hacer la automatización y qué requiere criterio humano.

---

## Marcos normativos cubiertos

El modelo propuesto cubre tres marcos que afectan a la mayoría de organizaciones que desarrollan aplicaciones de gestión en el ámbito europeo.

**WCAG 2.1 nivel AA** (Web Content Accessibility Guidelines). Obligatorio para servicios digitales del sector público bajo la Directiva de Accesibilidad Web (2016/2102). Adoptado como estándar de calidad por muchas organizaciones privadas. Sus criterios son técnicos, deterministas y verificables con herramientas automatizadas como axe-core.

**RGPD** (Reglamento UE 2016/679). Aplica a todo tratamiento de datos personales de personas físicas en la UE. Sus implicaciones en los requisitos funcionales incluyen base jurídica, información al interesado, minimización de datos, derechos del interesado y seguridad del tratamiento.

**PSD2** (Directiva UE 2015/2366). Aplica a organizaciones que gestionan servicios de pago, cuentas de pago u operaciones de pago. Sus exigencias de autenticación reforzada (SCA), registros de auditoría y vinculación dinámica tienen traducción directa en criterios de aceptación funcionales.

El catálogo es extensible. La arquitectura propuesta permite añadir nuevos marcos (ISO 27001, HIPAA, NIS2, regulación específica de la Administración Pública) siguiendo el mismo patrón sin modificar los prompts de generación.

---

## Extensión del glosario: el catálogo de normas

El glosario estructurado del punto anterior es el lugar donde vive el conocimiento normativo del proyecto. Se añade una sección `normas` que el pipeline consulta durante la validación y la generación. Esta sección no reemplaza el asesoramiento legal: codifica los disparadores y los criterios más frecuentes para que el sistema pueda detectarlos sin que el analista los tenga que recordar.

```yaml
# glosario.yaml — Sección normas
# Añadir al glosario del proyecto.
# El catálogo cubre los criterios más frecuentes, no todos.
# Ampliar con el área legal y el DPO al inicio del proyecto.

normas:
  - id: NORM-WCAG
    nombre_oficial: "WCAG 2.1 nivel AA"
    tipo: accesibilidad
    ambito: >
      Toda interfaz de usuario accesible vía navegador o aplicación móvil.
    obligatoriedad: >
      Obligatorio para servicios públicos digitales (Dir. 2016/2102 y RD 1112/2018).
      Recomendado como estándar de calidad para servicios privados.
    # Lista de criterios relevantes para aplicaciones de gestión empresarial.
    # Fuente: https://www.w3.org/TR/WCAG21/
    criterios_relevantes:
      - id: "1.1.1"
        nombre: "Contenido no textual"
        descripcion: >
          Todo contenido no textual tiene una alternativa textual equivalente.
        # Palabras clave en el requisito que activan este criterio
        activado_por: ["imagen", "icono funcional", "gráfico", "diagrama", "logo"]
        plantilla_ac: >
          El componente {{elemento}} tiene atributo alt descriptivo o aria-label
          que comunica su función. Las imágenes decorativas tienen alt vacío.
        herramienta_verificacion: "axe-core, WAVE"

      - id: "1.3.1"
        nombre: "Información y relaciones"
        descripcion: >
          La estructura, relaciones y significado pueden determinarse
          programáticamente o están disponibles en texto.
        activado_por: ["formulario", "tabla", "lista", "encabezado", "campo de entrada",
                       "sección", "grupo de campos"]
        plantilla_ac: >
          Los campos del formulario {{elemento}} tienen etiquetas asociadas
          mediante <label for> o aria-label/aria-labelledby.
          Los encabezados de tabla tienen <th scope>.
        herramienta_verificacion: "axe-core, revisión manual con NVDA"

      - id: "1.4.3"
        nombre: "Contraste mínimo"
        descripcion: >
          El texto y las imágenes de texto tienen contraste de al menos
          4.5:1 (texto normal) o 3:1 (texto grande, ≥18pt o ≥14pt negrita).
        activado_por: ["texto", "botón", "enlace", "mensaje de estado",
                       "etiqueta", "placeholder"]
        plantilla_ac: >
          El ratio de contraste del texto en {{elemento}} es ≥ 4.5:1
          frente al fondo en todos los estados (normal, hover, deshabilitado).
        herramienta_verificacion: "Colour Contrast Analyser, axe-core"

      - id: "2.1.1"
        nombre: "Teclado"
        descripcion: >
          Toda la funcionalidad está disponible desde un teclado sin requerir
          tiempos específicos de pulsación de tecla individual.
        activado_por: ["formulario", "modal", "menú", "control interactivo",
                       "acción", "wizard", "drag and drop"]
        plantilla_ac: >
          La acción {{elemento}} puede completarse íntegramente usando solo
          el teclado (Tab para navegar, Enter/Espacio para activar, Escape para cerrar).
        herramienta_verificacion: "Prueba manual de navegación por teclado"

      - id: "2.4.3"
        nombre: "Orden del foco"
        descripcion: >
          Los componentes reciben el foco en un orden que preserva
          el significado y la operabilidad.
        activado_por: ["modal", "wizard", "formulario de varios pasos",
                       "panel lateral", "drawer"]
        plantilla_ac: >
          El orden de tabulación en {{elemento}} es lógico y coherente
          con el flujo visual. Al abrir un modal, el foco se mueve al modal.
          Al cerrarlo, el foco regresa al elemento que lo abrió.
        herramienta_verificacion: "Prueba manual con teclado"

      - id: "3.3.1"
        nombre: "Identificación de errores"
        descripcion: >
          Si se detecta un error de entrada, el elemento erróneo se identifica
          y el error se describe al usuario en texto.
        activado_por: ["formulario", "campo de entrada", "validación", "error"]
        plantilla_ac: >
          Cuando {{elemento}} tiene un error de validación, el mensaje de error
          identifica el campo afectado por su nombre y describe qué se debe corregir.
          El mensaje es perceptible por lectores de pantalla (role=alert o aria-live).
        herramienta_verificacion: "Prueba manual con NVDA, axe-core"

      - id: "4.1.2"
        nombre: "Nombre, función, valor"
        descripcion: >
          Para todos los componentes de interfaz, el nombre y la función
          pueden determinarse programáticamente.
        activado_por: ["botón", "campo de entrada", "control personalizado",
                       "widget", "componente interactivo"]
        plantilla_ac: >
          El componente {{elemento}} tiene rol ARIA correcto, nombre accesible
          (visible o via aria-label) y estado comunicado programáticamente
          (aria-expanded, aria-checked, aria-disabled según corresponda).
        herramienta_verificacion: "axe-core, Accessibility Insights"

  - id: NORM-RGPD
    nombre_oficial: "RGPD — Reglamento (UE) 2016/679"
    tipo: privacidad_datos
    ambito: "Todo tratamiento de datos personales de personas físicas en la UE."
    obligatoriedad: >
      Obligatorio. Sanciones de hasta 20M€ o el 4% del volumen de negocio global anual.
    criterios_relevantes:
      - id: "Art6"
        nombre: "Base jurídica del tratamiento"
        descripcion: >
          El tratamiento solo es lícito si existe al menos una base jurídica:
          consentimiento, contrato, obligación legal, interés vital,
          misión de interés público o interés legítimo.
        activado_por: ["dato personal", "dato de contacto", "NIF persona física",
                       "nombre persona física", "dirección", "email", "teléfono",
                       "IP", "cookie de seguimiento"]
        plantilla_ac: >
          El sistema no permite almacenar {{dato}} sin que exista base jurídica
          documentada y aprobada por el DPO en el Registro de Actividades de Tratamiento.
        herramienta_verificacion: "Revisión documental (RAT)"

      - id: "Art13"
        nombre: "Información al interesado"
        descripcion: >
          Cuando se recaben datos directamente del interesado, se le debe informar
          de la finalidad, base jurídica, destinatarios y sus derechos
          en el momento de la recogida.
        activado_por: ["formulario de registro", "alta de usuario",
                       "formulario de contacto", "recogida de datos personales"]
        plantilla_ac: >
          El formulario {{elemento}} muestra el aviso de privacidad antes de
          que el usuario pueda enviar los datos. El aviso incluye finalidad,
          base jurídica y enlace a la política de privacidad completa.
          El formulario no puede enviarse sin que el aviso sea visible.
        herramienta_verificacion: "Revisión manual de la interfaz"

      - id: "Art17"
        nombre: "Derecho de supresión"
        descripcion: >
          El interesado tiene derecho a obtener la supresión de sus datos personales
          cuando ya no sean necesarios, retire el consentimiento u otros supuestos.
          Plazo de respuesta: sin dilación indebida, máximo 30 días.
        activado_por: ["perfil de usuario", "datos de contacto almacenados",
                       "histórico de actividad personal", "cuenta de usuario"]
        plantilla_ac: >
          El sistema proporciona un mecanismo para que {{interesado}} solicite
          la supresión de sus datos. La solicitud queda registrada con fecha.
          El sistema responde en el plazo máximo de 30 días naturales.
        herramienta_verificacion: "Prueba funcional del flujo de supresión"

      - id: "Art25"
        nombre: "Privacidad desde el diseño y por defecto"
        descripcion: >
          El responsable aplica medidas técnicas para garantizar que, por defecto,
          solo sean objeto de tratamiento los datos necesarios para cada fin específico.
        activado_por: ["formulario", "campo de entrada", "exportación de datos",
                       "informe con datos personales"]
        plantilla_ac: >
          El formulario/sistema {{elemento}} recoge únicamente los campos
          necesarios para la finalidad declarada. No existen campos opcionales
          que recojan más datos de los justificados por dicha finalidad.
        herramienta_verificacion: "Revisión del formulario + auditoría de red (DevTools)"

      - id: "Art30"
        nombre: "Registro de actividades de tratamiento (RAT)"
        descripcion: >
          El responsable mantiene un registro de los tratamientos efectuados
          bajo su responsabilidad, actualizado antes de la puesta en producción.
        activado_por: ["nuevo tratamiento de datos personales",
                       "nueva finalidad de tratamiento existente",
                       "nuevo módulo con datos personales"]
        plantilla_ac: >
          El nuevo tratamiento de {{datos}} con finalidad {{finalidad}} está
          dado de alta en el RAT y aprobado por el DPO antes del despliegue
          a producción.
        herramienta_verificacion: "Revisión documental (RAT)"

      - id: "Art32"
        nombre: "Seguridad del tratamiento"
        descripcion: >
          Medidas técnicas apropiadas para garantizar confidencialidad, integridad,
          disponibilidad y resiliencia: seudonimización, cifrado, capacidad de recuperación.
        activado_por: ["datos de salud", "datos financieros sensibles",
                       "contraseña", "token de autenticación",
                       "número de tarjeta", "datos de categoría especial"]
        plantilla_ac: >
          Los datos de {{categoría}} se almacenan cifrados en reposo (AES-256 o superior)
          y en tránsito (TLS 1.3 o superior). Las claves de cifrado no se almacenan
          junto a los datos cifrados.
        herramienta_verificacion: "Revisión de arquitectura, prueba de seguridad"

  - id: NORM-PSD2
    nombre_oficial: "PSD2 — Directiva (UE) 2015/2366"
    tipo: servicios_pago
    ambito: >
      Organizaciones que presten servicios de pago, gestionen cuentas de pago
      o inicien operaciones de pago en la UE. Verificar con el área legal
      si aplica antes de activar esta sección en el glosario.
    obligatoriedad: >
      Obligatorio para entidades de pago autorizadas y sus proveedores de servicios.
    criterios_relevantes:
      - id: "Art97-SCA"
        nombre: "Autenticación reforzada de clientes (SCA)"
        descripcion: >
          Los proveedores aplican SCA al acceder a cuentas de pago en línea,
          al iniciar operaciones de pago electrónico y al realizar acciones
          a distancia con riesgo de fraude.
          SCA requiere al menos dos factores independientes de: algo que el usuario
          sabe (PIN, contraseña), algo que posee (dispositivo, token),
          algo que es (biometría).
        activado_por: ["operación de pago", "acceso a cuenta de pago",
                       "autorización de pago", "transferencia",
                       "domiciliación", "cargo en cuenta"]
        plantilla_ac: >
          La operación {{elemento}} requiere autenticación con al menos dos factores
          independientes antes de ejecutarse. El sistema rechaza el intento
          si se supera el número máximo de intentos fallidos configurado.
        herramienta_verificacion: "Prueba funcional del flujo de autenticación"

      - id: "RTS-Art22-AuditLog"
        nombre: "Registro de auditoría de operaciones"
        descripcion: >
          Las operaciones de pago y las solicitudes de autenticación quedan
          registradas con los datos necesarios para investigar incidentes:
          timestamp, identidad del ordenante, importe, canal y resultado.
          El registro debe ser inmutable.
        activado_por: ["operación de pago", "autorización de pago",
                       "rechazo de pago", "sesión de pago",
                       "callback de pago", "notificación de pago"]
        plantilla_ac: >
          Cada operación {{elemento}} genera un registro de auditoría inmutable
          con los campos: timestamp_utc, id_usuario, importe, moneda,
          id_beneficiario, canal_acceso y resultado (APROBADO/RECHAZADO/PENDIENTE).
          El registro no puede modificarse ni eliminarse una vez creado.
        herramienta_verificacion: "Revisión del esquema de BD, prueba de integridad del log"

      - id: "RTS-Art4-VinculacionDinamica"
        nombre: "Vinculación dinámica"
        descripcion: >
          Para operaciones de pago remotas, el código de autenticación debe ser
          específico para el importe y el beneficiario. El usuario debe ser
          consciente de ambos antes de autenticar.
        activado_por: ["confirmación de pago", "autorización de transferencia",
                       "pantalla de confirmación de operación de pago"]
        plantilla_ac: >
          La pantalla de confirmación de {{elemento}} muestra el importe y
          el beneficiario antes de solicitar el factor de autenticación.
          El código de autenticación generado es único para esa combinación
          concreta de importe y beneficiario. Una modificación del importe
          o el beneficiario invalida el código anterior.
        herramienta_verificacion: "Prueba funcional: modificar importe tras generar código"

      - id: "Art96-Incidentes"
        nombre: "Notificación de incidentes de seguridad"
        descripcion: >
          Los proveedores notifican a la autoridad competente los incidentes
          de seguridad graves sin dilación.
        activado_por: ["fallo de autenticación masivo", "acceso no autorizado a cuenta",
                       "brecha de datos de pago", "interrupción del servicio de pago"]
        plantilla_ac: >
          El sistema registra y clasifica los eventos de seguridad en {{elemento}}
          con suficiente detalle (timestamp, tipo de evento, impacto estimado)
          para evaluar si superan el umbral de notificación a la autoridad
          competente (Banco de España / BCE según aplique).
        herramienta_verificacion: "Revisión del sistema de logging, simulación de incidente"
```

---

## Extensión de la plantilla YAML: el campo `cumplimiento_normativo`

Se añade al Bloque 1 de la plantilla de requisito del punto anterior. Si el analista conoce las implicaciones normativas en el momento de la escritura, las documenta aquí. Si no, el campo queda vacío y el prompt de detección lo rellena durante la validación.

```yaml
# Extensión del Bloque 1 — Identidad del requisito
# Añadir a la plantilla base.

cumplimiento_normativo:
  # Si se deja vacío, el validador analiza el requisito y propone
  # los marcos aplicables basándose en el catálogo de normas del glosario.
  # El analista revisa la propuesta y la aprueba, ajusta o rechaza.
  normas_aplicables: []
  # Formato cuando se rellena:
  # normas_aplicables:
  #   - norma: NORM-WCAG
  #     criterios: ["1.3.1", "2.1.1", "3.3.1"]
  #     motivo: "El requisito describe un formulario interactivo"
  #   - norma: NORM-RGPD
  #     criterios: ["Art6", "Art13", "Art25"]
  #     motivo: "Se recogen nombre y email de una persona física"

  evidencia_requerida: ""
  # Documentación que debe existir ANTES de la puesta en producción.
  # Ejemplos:
  # "Alta en el RAT aprobada por el DPO"
  # "Informe de accesibilidad con axe-core sin errores AA"
  # "Evaluación de Impacto en Protección de Datos (EIPD) completada"

  revision_legal_requerida: false
  # true si el área legal o el DPO deben revisar antes de que el requisito
  # entre en el pipeline de generación de artefactos.

  estado_cumplimiento: pendiente
  # Valores: pendiente | en_revision | aprobado | bloqueado
  # Solo pasa a 'aprobado' cuando todas las evidencias_requeridas están completas.
```

---

## El prompt de detección normativa

Se ejecuta como parte del pipeline de validación (punto 6 del modelo operativo), inmediatamente después de la validación semántica. No bloquea el pipeline, pero añade los criterios de cumplimiento detectados al JSON de la historia generada y marca `revision_legal_requerida: true` cuando es necesario.

> 📋 **Prompt de IA — Detección normativa automática**

```
Eres un especialista en cumplimiento normativo para aplicaciones de software.
Tu función es analizar requisitos funcionales, detectar qué marcos normativos
son aplicables y generar los criterios de aceptación de cumplimiento
en el mismo formato Dado/Cuando/Entonces que los criterios funcionales.

REGLAS ESTRICTAS:
1. Solo activa una norma si el requisito contiene al menos un disparador
   de los definidos en el catálogo de normas. No actives normas por precaución
   genérica ni por heurísticas propias no documentadas en el catálogo.
2. Los criterios de aceptación de cumplimiento deben ser verificables
   mediante una prueba concreta. Si no pueden responderse con PASS/FAIL,
   no los incluyas.
3. Si el campo cumplimiento_normativo ya tiene contenido, amplíalo con lo
   que falta. No elimines lo que el analista ya ha documentado.
4. Si la norma requiere una acción organizativa fuera del código
   (aprobación del DPO, entrada en el RAT, revisión de contratos),
   indícalo en evidencia_requerida, no como criterio de aceptación técnico.
5. Distingue entre criterios verificables automáticamente (herramienta)
   y criterios que requieren prueba manual o revisión documental.
6. El output es siempre JSON válido. Sin texto fuera del JSON.

CATÁLOGO DE NORMAS DEL PROYECTO:
{{normas_seccion_glosario}}

REQUISITO A ANALIZAR:
{{requisito_yaml}}

Genera:
{
  "deteccion_normativa": {
    "requisito_id": "{{req_id}}",
    "normas_detectadas": [
      {
        "norma_id": "NORM-WCAG",
        "criterios_aplicables": ["1.3.1", "2.1.1"],
        "motivo_deteccion": "[Por qué se activa: qué disparador se encontró]",
        "disparadores_encontrados": ["[texto o campo del requisito que activó la norma]"]
      }
    ],
    "criterios_ac_cumplimiento": [
      {
        "id": "AC-{{req_id}}-NORM-01",
        "norma": "NORM-WCAG",
        "articulo_criterio": "1.3.1",
        "titulo": "[Qué verifica este criterio en una frase]",
        "dado": "[Estado previo relevante para la verificación]",
        "cuando": "[Acción de verificación concreta]",
        "entonces": "[Comportamiento requerido por la norma, observable y verificable]",
        "tipo_verificacion": "automatizada | manual | documental",
        "herramienta_verificacion": "[axe-core | WAVE | NVDA | revisión manual | revisión documental]"
      }
    ],
    "actualizacion_campo_cumplimiento": {
      "normas_aplicables": [],
      "evidencia_requerida": "[Documentación obligatoria antes de producción, o cadena vacía]",
      "revision_legal_requerida": false
    },
    "alertas": [
      "[Advertencia sobre implicaciones normativas ambiguas o que requieren criterio humano]"
    ]
  }
}
```

### Ejemplo de output para un requisito de formulario con datos personales

**Requisito de entrada (fragmento):**

```yaml
id: REQ-041
titulo: "Dar de alta un nuevo proveedor en el sistema"
actor: "Gestor de facturación"
descripcion: >
  El gestor necesita registrar nuevos proveedores. El formulario recoge:
  razón social, CIF, dirección fiscal, email de contacto y nombre del
  responsable de facturación.
datos_entrada:
  - nombre: razon_social
    tipo: string
    requerido: true
  - nombre: cif
    tipo: string
    requerido: true
  - nombre: email_contacto
    tipo: string
    requerido: false
  - nombre: nombre_responsable
    tipo: string
    requerido: false
    descripcion: "Nombre de la persona de contacto para facturación"
```

**Output del prompt:**

```json
{
  "deteccion_normativa": {
    "requisito_id": "REQ-041",
    "normas_detectadas": [
      {
        "norma_id": "NORM-RGPD",
        "criterios_aplicables": ["Art6", "Art13", "Art25", "Art30"],
        "motivo_deteccion": "Los campos 'nombre_responsable' y 'email_contacto'
          son datos personales de una persona física identificable.
          Aunque el proveedor sea una persona jurídica, el responsable de
          facturación es una persona física cuyos datos se tratan.",
        "disparadores_encontrados": ["nombre_responsable", "email_contacto",
                                     "formulario de alta"]
      },
      {
        "norma_id": "NORM-WCAG",
        "criterios_aplicables": ["1.3.1", "2.1.1", "3.3.1", "4.1.2"],
        "motivo_deteccion": "El requisito describe un formulario interactivo
          con campos de entrada.",
        "disparadores_encontrados": ["formulario", "campo de entrada"]
      }
    ],
    "criterios_ac_cumplimiento": [
      {
        "id": "AC-041-NORM-01",
        "norma": "NORM-RGPD",
        "articulo_criterio": "Art13",
        "titulo": "El formulario muestra el aviso de privacidad antes del envío",
        "dado": "El gestor ha rellenado el formulario de alta de proveedor",
        "cuando": "Intenta enviar el formulario",
        "entonces": "Se muestra un aviso de privacidad con finalidad del
          tratamiento, base jurídica y enlace a la política completa.
          El formulario no puede enviarse hasta que el aviso sea visible.",
        "tipo_verificacion": "manual",
        "herramienta_verificacion": "Revisión manual de la interfaz"
      },
      {
        "id": "AC-041-NORM-02",
        "norma": "NORM-RGPD",
        "articulo_criterio": "Art25",
        "titulo": "El formulario no recoge más campos de los necesarios",
        "dado": "El formulario de alta de proveedor está disponible",
        "cuando": "Se inspeccionan los campos del formulario y el tráfico de red",
        "entonces": "Los únicos campos del formulario son los definidos en el
          requisito. No hay campos ocultos ni envíos adicionales de datos
          no justificados por la finalidad de alta de proveedor.",
        "tipo_verificacion": "manual",
        "herramienta_verificacion": "Revisión de código + DevTools (Network)"
      },
      {
        "id": "AC-041-NORM-03",
        "norma": "NORM-WCAG",
        "articulo_criterio": "1.3.1",
        "titulo": "Los campos tienen etiquetas asociadas programáticamente",
        "dado": "El formulario de alta está cargado en el navegador",
        "cuando": "Se ejecuta axe-core sobre la página del formulario",
        "entonces": "axe-core no reporta errores de nivel AA relacionados
          con etiquetas de formulario. Cada campo tiene <label for> o
          aria-label/aria-labelledby asociado.",
        "tipo_verificacion": "automatizada",
        "herramienta_verificacion": "axe-core"
      },
      {
        "id": "AC-041-NORM-04",
        "norma": "NORM-WCAG",
        "articulo_criterio": "2.1.1",
        "titulo": "El formulario puede enviarse usando solo el teclado",
        "dado": "El gestor accede al formulario sin usar el ratón",
        "cuando": "Navega por todos los campos con Tab y envía con Enter",
        "entonces": "Todos los campos reciben el foco en el orden visual lógico.
          El formulario se envía correctamente sin requerir el ratón en ningún paso.",
        "tipo_verificacion": "manual",
        "herramienta_verificacion": "Prueba manual de navegación por teclado"
      },
      {
        "id": "AC-041-NORM-05",
        "norma": "NORM-WCAG",
        "articulo_criterio": "3.3.1",
        "titulo": "Los errores de validación identifican el campo e indican qué corregir",
        "dado": "El gestor envía el formulario con el campo CIF vacío",
        "cuando": "El sistema procesa la validación",
        "entonces": "Aparece un mensaje de error que identifica el campo CIF
          de forma explícita y describe qué debe introducirse. El mensaje
          es perceptible por lectores de pantalla (role=alert o aria-live).",
        "tipo_verificacion": "manual",
        "herramienta_verificacion": "Prueba manual de validación + NVDA"
      }
    ],
    "actualizacion_campo_cumplimiento": {
      "normas_aplicables": [
        {
          "norma": "NORM-RGPD",
          "criterios": ["Art6", "Art13", "Art25", "Art30"],
          "motivo": "El formulario recoge datos personales del responsable de facturación del proveedor"
        },
        {
          "norma": "NORM-WCAG",
          "criterios": ["1.3.1", "2.1.1", "3.3.1", "4.1.2"],
          "motivo": "El requisito describe un formulario interactivo"
        }
      ],
      "evidencia_requerida": "Alta del tratamiento 'Datos de contacto de responsables
        de proveedor' en el RAT aprobada por el DPO antes del despliegue a producción.",
      "revision_legal_requerida": true
    },
    "alertas": [
      "Si el campo 'email_contacto' se usará para comunicaciones comerciales,
       se requiere consentimiento explícito adicional (LSSI-CE Art. 21).
       Confirmar con el área legal si existe esa intención de uso.",
      "El tratamiento del campo 'nombre_responsable' puede estar amparado por
       el interés legítimo del contrato con el proveedor (Art6.1.b RGPD),
       pero el DPO debe confirmarlo antes de producción."
    ]
  }
}
```

---

## Integración en el pipeline existente

### En la generación de artefactos Jira (Prompt 2)

Los criterios de cumplimiento generados por el prompt de detección se añaden a la lista `acceptance_criteria` de la historia. En Jira son criterios de aceptación estándar, con la única diferencia de que llevan el campo `norma` que permite filtrarlos y reportarlos de forma independiente.

El Prompt 2 del pipeline de generación de artefactos recibe los criterios normativos como parte del contexto:

```
CRITERIOS DE CUMPLIMIENTO NORMATIVO DETECTADOS:
{{criterios_ac_cumplimiento}}

Añade estos criterios a la lista acceptance_criteria de la historia.
No los fusiones con los criterios funcionales: cada criterio normativo
mantiene su campo 'norma' y 'herramienta_verificacion'.
Incluye en definition_of_done el criterio:
"Todos los criterios de aceptación de cumplimiento normativo verificados
y documentados en Xray con su tipo de verificación."
```

### En las tareas técnicas (Prompt 3)

El Prompt 3 recibe los criterios normativos como contexto adicional e infiere qué trabajo técnico implican por capa tecnológica:

```
CONTEXTO ADICIONAL — CRITERIOS NORMATIVOS:
Este requisito tiene criterios de aceptación de cumplimiento que implican
trabajo técnico diferenciado. Genera tareas técnicas específicas para:

- Criterios WCAG: capa frontend. Tareas de marcado semántico, atributos ARIA,
  gestión del foco y verificación con axe-core. Planificar en el mismo sprint
  que la tarea de implementación del componente, no después.
- Criterios RGPD (Art13, aviso de privacidad): capa frontend.
- Criterios RGPD (Art32, cifrado): capa backend y base de datos.
- Criterios RGPD (Art30, RAT): no genera tarea técnica. Añadir como
  dependencia bloqueante al despliegue a producción.
- Criterios PSD2 (log de auditoría): capa backend y base de datos.
  El log debe ser inmutable: no se puede UPDATE ni DELETE sobre él.
- Criterios PSD2 (SCA): capa backend y frontend.

Las tareas normativas llevan los labels: ["cumplimiento", "norma-WCAG"/
"norma-RGPD"/"norma-PSD2"] para facilitar el filtrado en Jira.

CRITERIOS NORMATIVOS:
{{criterios_ac_cumplimiento}}
```

### En los test cases (Prompt de test cases positivos y negativos)

Los criterios normativos de tipo `automatizada` generan test cases ejecutables con el mismo pipeline del punto 5. Los de tipo `manual` generan test cases manuales en Xray. Los de tipo `documental` no generan test cases: generan una entrada en `evidencia_requerida` que bloquea el despliegue hasta que el documento exista.

```
CONTEXTO ADICIONAL — TEST CASES DE CUMPLIMIENTO:
Para los criterios con tipo_verificacion = "automatizada":
  - Generar test case ejecutable con los mismos campos que los test cases funcionales.
  - El campo 'automatizable' = true.
  - El campo 'framework_sugerido' = la herramienta indicada en herramienta_verificacion.

Para los criterios con tipo_verificacion = "manual":
  - Generar test case con pasos detallados para el QA.
  - El campo 'automatizable' = false.
  - Los pasos deben ser ejecutables sin conocimiento previo de la norma.

Para los criterios con tipo_verificacion = "documental":
  - No generar test case.
  - Añadir la evidencia a la sección evidencia_requerida del requisito.

CRITERIOS NORMATIVOS A PROCESAR:
{{criterios_ac_cumplimiento}}
```

### En el grafo de trazabilidad

El modelo de datos del punto 9 se extiende con dos nuevos tipos para dar visibilidad a los artefactos normativos sin modificar el esquema existente.

```sql
-- Extensión del esquema de trazabilidad (punto 9 del modelo operativo)
-- Los criterios normativos son nodos como cualquier otro artefacto.

-- Nuevo tipo de nodo: criterio_normativo
-- Se registra igual que cualquier otro nodo en nodos_trazabilidad
-- con tipo = 'criterio_normativo' y los metadatos de la norma.

-- Ejemplo de registro automático desde el pipeline:
INSERT INTO nodos_trazabilidad (id, tipo, titulo, estado, metadatos)
VALUES (
  'AC-041-NORM-01',
  'criterio_normativo',
  'RGPD Art13: Aviso de privacidad en el formulario de alta',
  'activo',
  '{
    "norma": "NORM-RGPD",
    "articulo": "Art13",
    "requisito_origen": "REQ-041",
    "tipo_verificacion": "manual",
    "evidencia_requerida": false
  }'
);

-- Nueva arista: verifica_cumplimiento
-- Conecta test cases con criterios normativos.
INSERT INTO aristas_trazabilidad
  (origen_id, destino_id, tipo_relacion, confianza, origen_relacion)
VALUES (
  'TC-041-NORM-01',        -- test case de cumplimiento
  'AC-041-NORM-01',        -- criterio normativo que verifica
  'verifica_cumplimiento', -- nuevo tipo de arista
  1.0,
  'pipeline_generacion'
);

-- Consulta de gaps normativos: criterios sin test case asociado
SELECT
  n.id              AS criterio_id,
  n.titulo          AS criterio_titulo,
  n.metadatos->>'norma'       AS norma,
  n.metadatos->>'articulo'    AS articulo
FROM nodos_trazabilidad n
WHERE n.tipo = 'criterio_normativo'
  AND n.activo = TRUE
  AND NOT EXISTS (
    SELECT 1 FROM aristas_trazabilidad a
    WHERE a.destino_id = n.id
      AND a.tipo_relacion = 'verifica_cumplimiento'
      AND a.activo = TRUE
  );

-- Consulta de cobertura normativa por norma
SELECT
  n.metadatos->>'norma'  AS norma,
  COUNT(*)               AS total_criterios,
  COUNT(a.origen_id)     AS criterios_con_test
FROM nodos_trazabilidad n
LEFT JOIN aristas_trazabilidad a
  ON a.destino_id = n.id
  AND a.tipo_relacion = 'verifica_cumplimiento'
  AND a.activo = TRUE
WHERE n.tipo = 'criterio_normativo'
  AND n.activo = TRUE
GROUP BY n.metadatos->>'norma';
```

---

## El prompt de informe de cumplimiento normativo

El informe se genera bajo demanda o automáticamente al cierre de cada sprint. Es el documento que el DPO, el área legal o un auditor externo necesita para verificar que los requisitos normativos se han definido, implementado y probado.

> 📋 **Prompt de IA — Informe de cumplimiento normativo**

```
A partir de los datos de trazabilidad de la épica o sprint indicado,
genera el informe de cumplimiento normativo.

El informe tiene dos audiencias distintas:
1. El equipo de desarrollo: qué gaps existen y qué hay que hacer antes del despliegue.
2. El DPO o auditor externo: evidencia de que el proceso incluye requisitos
   normativos desde la definición funcional.

DATOS DE TRAZABILIDAD:
{{datos_trazabilidad_normativa}}
(Resultado de la consulta de cobertura normativa sobre nodos_trazabilidad)

CATÁLOGO DE NORMAS DEL PROYECTO:
{{normas_glosario}}

Genera:
{
  "informe_cumplimiento": {
    "ambito": "{{epica_id}} | sprint-{{sprint_id}}",
    "fecha_generacion": "{{fecha}}",
    "resumen_ejecutivo": "[Estado del cumplimiento en 2-3 frases para el DPO o auditor]",
    "por_norma": [
      {
        "norma_id": "NORM-RGPD",
        "nombre": "RGPD — Reglamento (UE) 2016/679",
        "criterios_requeridos": 0,
        "criterios_con_ac": 0,
        "criterios_con_test": 0,
        "criterios_test_pasado": 0,
        "porcentaje_cobertura_test": "0%",
        "gaps_ac": ["[Criterio normativo sin criterio de aceptación documentado]"],
        "gaps_test": ["[Criterio con AC pero sin test case asociado]"],
        "evidencias_pendientes": ["[Documentación requerida antes de producción]"]
      }
    ],
    "semaforo_global": "verde | amarillo | rojo",
    "listo_para_produccion": true,
    "acciones_bloqueantes": [
      {
        "accion": "[Qué hay que hacer exactamente]",
        "responsable": "analista | DPO | legal | tech_lead | QA",
        "plazo": "[Cuándo debe estar resuelto para no bloquear el despliegue]",
        "referencia": "[ID de requisito o criterio al que aplica]"
      }
    ],
    "acciones_recomendadas": []
  }
}

SEMÁFORO:
- verde: cobertura_test ≥ 100% en todas las normas y sin evidencias pendientes
- amarillo: alguna norma con cobertura_test < 100% o evidencias pendientes
  no bloqueantes para el sprint actual
- rojo: alguna norma con criterios sin AC, evidencias bloqueantes pendientes,
  o criterios con test fallido en QA
```

### Ejemplo de informe de cumplimiento generado

El siguiente output corresponde al cierre del sprint en que se implementa el módulo EP-08 Alta y gestión de proveedores, con cuatro requisitos procesados, tres de los cuales tienen criterios RGPD y todos tienen criterios WCAG.

```json
{
  "informe_cumplimiento": {
    "ambito": "EP-08",
    "fecha_generacion": "2025-05-20T18:00:00Z",
    "resumen_ejecutivo": "La épica tiene cobertura completa de criterios de
      accesibilidad WCAG AA (12/12 test cases pasados en QA). Los criterios
      RGPD tienen cobertura técnica completa pero la entrada en el RAT del
      tratamiento 'Datos de contacto de responsables de proveedor' está
      pendiente de aprobación por el DPO. El módulo no debe desplegarse
      a producción hasta que esa evidencia esté completada.",
    "por_norma": [
      {
        "norma_id": "NORM-WCAG",
        "nombre": "WCAG 2.1 nivel AA",
        "criterios_requeridos": 12,
        "criterios_con_ac": 12,
        "criterios_con_test": 12,
        "criterios_test_pasado": 12,
        "porcentaje_cobertura_test": "100%",
        "gaps_ac": [],
        "gaps_test": [],
        "evidencias_pendientes": []
      },
      {
        "norma_id": "NORM-RGPD",
        "nombre": "RGPD — Reglamento (UE) 2016/679",
        "criterios_requeridos": 5,
        "criterios_con_ac": 5,
        "criterios_con_test": 4,
        "criterios_test_pasado": 4,
        "porcentaje_cobertura_test": "80%",
        "gaps_ac": [],
        "gaps_test": [],
        "evidencias_pendientes": [
          "Alta del tratamiento 'Datos de contacto de responsables de proveedor'
           en el RAT aprobada por el DPO. Referencia: REQ-041, AC-041-NORM-RAT.
           Contacto: dpo@organizacion.es"
        ]
      }
    ],
    "semaforo_global": "amarillo",
    "listo_para_produccion": false,
    "acciones_bloqueantes": [
      {
        "accion": "Obtener aprobación del DPO para la entrada en el RAT del
          tratamiento 'Datos de contacto de responsables de proveedor'.",
        "responsable": "analista",
        "plazo": "Antes del despliegue a producción de EP-08.",
        "referencia": "REQ-041 / AC-041-NORM-RAT"
      }
    ],
    "acciones_recomendadas": [
      {
        "accion": "Confirmar con el área legal si el uso del campo 'email_contacto'
          para comunicaciones comerciales está previsto. Si es así, añadir
          criterio de consentimiento explícito (LSSI-CE Art. 21).",
        "responsable": "analista",
        "plazo": "Antes de que el área de marketing solicite acceso al dato.",
        "referencia": "REQ-041 / alerta del prompt de detección"
      }
    ]
  }
}
```

---

## Cómo extender el catálogo a otras normas

El catálogo del glosario cubre los tres marcos más frecuentes, pero la arquitectura está diseñada para ser ampliada sin modificar los prompts de generación. La extensión sigue siempre el mismo patrón.

**Paso 1 — Identificar los criterios con traducción funcional.** No todos los artículos de una norma tienen traducción directa en requisitos de software. El filtro es: ¿puede expresarse este artículo como un comportamiento del sistema verificable con un test? Si la respuesta es no (por ejemplo, el artículo obliga a tener un DPO nombrado, que es una obligación organizativa), no entra en el catálogo como criterio de aceptación. Entra en `evidencia_requerida`.

**Paso 2 — Definir los `activado_por` con precisión.** Este es el campo más crítico del catálogo. Si los disparadores son demasiado genéricos, el sistema activa la norma en demasiados requisitos y genera ruido. Si son demasiado específicos, se pierden casos relevantes. La regla práctica es: los disparadores deben ser sustantivos o sintagmas nominales que aparecen con frecuencia en los requisitos de la organización, no categorías abstractas.

```yaml
# Ejemplo: extensión del catálogo con NIS2 (Directiva UE 2022/2555)
# para organizaciones clasificadas como entidades esenciales o importantes.

  - id: NORM-NIS2
    nombre_oficial: "NIS2 — Directiva (UE) 2022/2555"
    tipo: ciberseguridad
    ambito: >
      Entidades esenciales e importantes en sectores críticos:
      energía, transporte, banca, infraestructuras digitales, etc.
      Verificar con el área legal si la organización está en el ámbito de NIS2.
    obligatoriedad: >
      Obligatorio para entidades en ámbito. Sanciones de hasta 10M€ o
      el 2% del volumen de negocio global para entidades esenciales.
    criterios_relevantes:
      - id: "Art21-LogAuditoria"
        nombre: "Registro de eventos de seguridad"
        descripcion: >
          Las entidades implementan medidas para registrar eventos de seguridad
          con suficiente detalle para detectar y analizar incidentes.
        activado_por: ["autenticación", "autorización", "acceso a datos sensibles",
                       "operación con datos críticos", "cambio de configuración"]
        plantilla_ac: >
          El sistema registra los eventos de {{elemento}} con los campos:
          timestamp_utc, id_usuario, acción, resultado y dirección IP de origen.
          El log es inmutable y se retiene durante el período mínimo establecido
          en la política de seguridad.
        herramienta_verificacion: "Revisión del esquema de log, prueba de integridad"

      - id: "Art21-GestionIncidentes"
        nombre: "Capacidad de detección y respuesta a incidentes"
        descripcion: >
          Las entidades implementan procedimientos para detectar, analizar
          y responder a incidentes de ciberseguridad.
        activado_por: ["fallo de autenticación", "acceso no autorizado",
                       "anomalía en el uso del sistema"]
        plantilla_ac: >
          El sistema genera una alerta cuando se producen {{N}} intentos
          fallidos consecutivos de {{acción}} desde la misma dirección IP
          en un período de {{T}} minutos. La alerta queda registrada
          con los datos necesarios para el análisis forense.
        herramienta_verificacion: "Prueba funcional de generación de alertas"
```

**Paso 3 — Validar el catálogo con el DPO o el responsable legal.** Antes de activar una nueva sección del catálogo en producción, el responsable legal debe revisar que los criterios codificados son suficientes para el nivel de cumplimiento requerido y que no hay artículos críticos omitidos. Esta revisión se documenta como `evidencia_requerida` del propio catálogo.

**Paso 4 — Definir el propietario del catálogo en el sistema de gobierno.** Cada sección de norma tiene un propietario responsable de mantenerla actualizada cuando la norma evoluciona. El DPO es el propietario natural de la sección RGPD. El responsable de seguridad lo es de NIS2 y PSD2. El equipo de frontend puede co-propietario de WCAG junto a un perfil de accesibilidad.

---

## Integración en el orquestador (paso adicional del pipeline)

El prompt de detección normativa se inserta en el orquestador del Modelo Operativo como un paso de la validación, después del paso `s2_validacion` y antes de que el requisito entre en la generación de artefactos. El paso no es bloqueante por defecto: si la detección falla o el catálogo de normas no está disponible, el pipeline continúa con una advertencia.

```python
# steps/s2b_deteccion_normativa.py
# Paso s2b: detección de obligaciones normativas.
# Se ejecuta después de s2_validacion y antes de s3_rag_contexto.
# No es bloqueante: si falla, el pipeline continúa con advertencia.

import json
import yaml
from pathlib import Path

async def detectar_obligaciones_normativas(
    requisito: dict,
    glosario: dict,
    config
) -> dict:
    """
    Analiza el requisito contra el catálogo de normas del glosario
    y devuelve los criterios de aceptación de cumplimiento detectados.

    Retorna un dict con:
      - criterios_ac_cumplimiento: lista de criterios en formato AC
      - actualizacion_campo_cumplimiento: campos a añadir al YAML
      - alertas: advertencias para el analista
      - normas_detectadas: resumen de normas activadas
    """

    # Si el glosario no tiene sección de normas, no hay nada que detectar.
    # No es un error: simplemente el proyecto no ha configurado el catálogo.
    if "normas" not in glosario or not glosario["normas"]:
        return {
            "criterios_ac_cumplimiento": [],
            "normas_detectadas": [],
            "alertas": ["El glosario no tiene sección 'normas'. "
                        "La detección normativa automática no está activa."],
            "actualizacion_campo_cumplimiento": {}
        }

    # Si el campo cumplimiento_normativo ya tiene normas_aplicables definidas
    # por el analista, el prompt amplía en lugar de reemplazar.
    ya_tiene_normas = bool(
        requisito.get("cumplimiento_normativo", {}).get("normas_aplicables")
    )

    # Cargar el prompt de detección desde el repositorio de prompts versionados.
    # El mismo mecanismo de versionado del punto 12 del Modelo Operativo.
    prompt_path = config.repo_prompts / "s2b_deteccion_normativa.txt"
    with open(prompt_path, encoding="utf-8") as f:
        prompt_template = f.read()

    # Inyección selectiva del catálogo de normas.
    # Solo se pasan las secciones normas y reglas_globales del glosario,
    # no el glosario completo. Reduce el consumo de tokens.
    normas_contexto = yaml.dump(
        {"normas": glosario["normas"]},
        allow_unicode=True,
        default_flow_style=False
    )

    prompt = prompt_template.replace(
        "{{normas_seccion_glosario}}", normas_contexto
    ).replace(
        "{{requisito_yaml}}", yaml.dump(
            requisito, allow_unicode=True, default_flow_style=False
        )
    )

    # Llamada al LLM con el mismo cliente configurado en el orquestador.
    # Temperatura 0.0 para máximo determinismo en la detección.
    respuesta = await config.llm_client.completar(
        prompt=prompt,
        temperatura=0.0,
        max_tokens=2048
    )

    try:
        resultado = json.loads(respuesta)
        deteccion = resultado.get("deteccion_normativa", {})

        # Si el requisito ya tenía normas definidas por el analista,
        # registrar que el sistema amplió (no reemplazó) el campo.
        if ya_tiene_normas:
            deteccion["_modo"] = "ampliacion"
        else:
            deteccion["_modo"] = "deteccion_inicial"

        return deteccion

    except json.JSONDecodeError as e:
        # Si el LLM no devuelve JSON válido, devolver resultado vacío
        # con advertencia. El pipeline continúa sin criterios normativos.
        return {
            "criterios_ac_cumplimiento": [],
            "normas_detectadas": [],
            "alertas": [f"El prompt de detección normativa no devolvió JSON válido: {e}. "
                        "Revisar el prompt en s2b_deteccion_normativa.txt."],
            "actualizacion_campo_cumplimiento": {}
        }
```

El paso se registra en el estado de ejecución del orquestador con la misma mecánica que el resto:

```python
# Fragmento del orchestrator.py — insertar después del bloque de s2_validacion

# ══════════════════════════════════════════════════════
# PASO 2b — Detección de obligaciones normativas
# ══════════════════════════════════════════════════════
paso = "s2b_deteccion_normativa"
if gestor.debe_ejecutar(run, paso):
    _log_paso("2b", "Detectando obligaciones normativas")
    run = gestor.iniciar_paso(run, paso)
    try:
        deteccion_normativa = await detectar_obligaciones_normativas(
            requisito=requisito,
            glosario=glosario,
            config=config
        )

        # Guardar los criterios en el estado del run para que
        # los pasos 4, 5 y 7 los consuman como contexto adicional.
        run.artefactos_generados["deteccion_normativa"] = deteccion_normativa

        n_normas = len(deteccion_normativa.get("normas_detectadas", []))
        n_criterios = len(deteccion_normativa.get("criterios_ac_cumplimiento", []))

        run = gestor.completar_paso(run, paso, {
            "normas_detectadas": n_normas,
            "criterios_normativa_generados": n_criterios
        })

        if n_criterios > 0:
            _log_ok(f"{n_normas} normas activas · {n_criterios} criterios de cumplimiento")
        else:
            _log_ok("Sin obligaciones normativas detectadas en este requisito")

        # Las alertas del prompt de detección se registran como
        # advertencias globales del run, no como bloqueantes.
        for alerta in deteccion_normativa.get("alertas", []):
            run.advertencias_globales.append(f"[normativa] {alerta}")
            _log_advertencia(alerta)

    except Exception as e:
        # El paso no es bloqueante. Si falla, el pipeline continúa
        # sin criterios normativos y registra la advertencia.
        log.warning(f"  ⚠ Detección normativa falló: {e}. Continuando sin criterios normativos.")
        run.artefactos_generados["deteccion_normativa"] = {
            "criterios_ac_cumplimiento": [],
            "normas_detectadas": [],
            "alertas": [str(e)]
        }
        run = gestor.omitir_paso(run, paso, f"Error no bloqueante: {e}")
else:
    _log_reanudado(paso)
```

La tabla de pasos del orquestador queda así con el nuevo paso insertado:

| Paso | Nombre | Bloqueante | Aplica a |
|---|---|---|---|
| s1 | Carga y parseo del YAML | Sí | Siempre |
| s2 | Validación automática de calidad | Sí | Siempre |
| **s2b** | **Detección de obligaciones normativas** | **No** | **Si el glosario tiene sección `normas`** |
| s3 | Recuperación de contexto RAG | No | Siempre |
| s4 | Generación de artefactos Jira | Sí | Siempre |
| s5 | Generación de test cases | Sí | Siempre |
| s6 | Análisis de impacto de cambios | No | Solo si es actualización |
| s7 | Registro en el grafo de trazabilidad | No | Siempre |
| s8 | Gate de aprobación humana | Sí | Siempre |
| s9 | Push a Jira | Sí | Si no es dry-run |
| s9b | Push a Xray | No | Si Xray está activo |

---

## Errores frecuentes al implantar esta capa

Los errores que se repiten en la mayoría de proyectos cuando se añade la detección normativa al pipeline, ordenados por impacto:

**Catálogo demasiado genérico en los `activado_por`.** Si los disparadores son palabras tan amplias como "dato" o "interfaz", el sistema activa normas en prácticamente todos los requisitos y el analista empieza a ignorar las alertas. El catálogo pierde credibilidad en dos semanas. La regla es que cada disparador debe ser suficientemente específico para que su presencia en un requisito sea un indicador real de la obligación normativa.

**Tratar los criterios normativos como criterios de segunda clase.** El error más común en el refinamiento: el equipo revisa los criterios funcionales con detalle y aprueba los normativos "de pasada" sin verificar que son ejecutables. Un criterio de tipo "el sistema cifra los datos" sin especificar el algoritmo, el alcance y cómo se verifica no es un criterio de aceptación: es una intención. El prompt lo detectará con el validador semántico del punto 6, pero si el analista lo aprueba en el gate sin revisarlo, el error pasa al sprint.

**Separar los criterios normativos de los funcionales en Jira.** Algunos equipos crean issues separados para los criterios de accesibilidad ("historia de accesibilidad de X") desvinculados de la historia funcional. El resultado es que la historia funcional se cierra como completada y la de accesibilidad queda en el backlog indefinidamente porque nadie la planifica. Los criterios normativos deben vivir como criterios de aceptación dentro de la misma historia que el requisito funcional, no en historias separadas.

**Confundir `evidencia_requerida` con un criterio de aceptación.** La entrada en el RAT, la aprobación de una EIPD o la firma de un contrato de encargo de tratamiento son condiciones previas al despliegue, no comportamientos del sistema verificables en un test. El pipeline los gestiona como `evidencia_requerida` precisamente porque son de naturaleza distinta. Intentar convertirlos en criterios de aceptación técnicos produce criterios que ningún test puede ejecutar.

**No asignar propietario al catálogo de normas.** WCAG publica versiones nuevas. El RGPD recibe interpretaciones de las autoridades de control. PSD2 está siendo sustituida por PSD3 en el horizonte regulatorio europeo. Un catálogo sin propietario queda desactualizado silenciosamente, y el sistema genera criterios que ya no son suficientes o que ya no aplican. La cadencia de revisión mínima recomendada es trimestral o al inicio de cada nueva épica que active una norma del catálogo.

**Activar PSD2 sin confirmar el ámbito.** La sección PSD2 del catálogo genera criterios muy específicos (SCA obligatoria, registros de auditoría inmutables, vinculación dinámica) que implican trabajo de arquitectura significativo. Si la organización no está en el ámbito de PSD2 como entidad de pago, ese trabajo es innecesario. Confirmar el ámbito con el área legal antes de activar la sección es el paso previo no negociable.

---

## Roadmap de implantación de la capa normativa

La capa normativa no se implanta a la vez que el resto del pipeline. Se incorpora de forma incremental una vez que el pipeline base está estabilizado, siguiendo las fases del roadmap del Modelo Operativo.

| Fase | Cuándo | Qué se implanta | Resultado esperado |
|---|---|---|---|
| **0 — Catálogo mínimo** | Al inicio del proyecto, antes del primer requisito | Sección `normas` del glosario con solo los marcos que aplican. Validar con DPO y área legal. | El catálogo existe y está aprobado. No está conectado al pipeline todavía. |
| **1 — Detección asistida** | Fase 1 del roadmap general (meses 2-3) | El paso s2b está activo pero en modo informativo: genera las detecciones y las muestra al analista en el gate de aprobación, pero no las añade automáticamente a los criterios AC. | El analista ve las detecciones, las valida manualmente y las copia a la historia. Calibración del catálogo con datos reales del proyecto. |
| **2 — Detección automática** | Fase 2 del roadmap general (meses 4-6) | Los criterios normativos detectados se añaden automáticamente a los criterios AC de la historia generada. El analista los revisa en el gate. Los test cases normativos se generan con el mismo pipeline del punto 5. | El pipeline genera criterios normativos sin intervención del analista. La revisión en el gate toma 3-5 minutos adicionales. |
| **3 — Informe y trazabilidad** | Fase 3 del roadmap general (meses 7-9) | El grafo de trazabilidad incluye nodos `criterio_normativo`. El informe de cumplimiento se genera automáticamente al cierre de sprint. El gate de despliegue verifica `listo_para_produccion`. | El informe de cumplimiento es un artefacto automático que el DPO puede consultar en tiempo real. Los despliegues a producción tienen un gate normativo formal. |
| **4 — Gobierno continuo** | Ongoing | Revisión trimestral del catálogo. Métricas de cumplimiento en el dashboard semanal. Propietario del catálogo asignado. | El catálogo se mantiene actualizado. Las actualizaciones normativas se propagan al pipeline de forma controlada. |

---

## Catálogo de disparadores por tipo de elemento de interfaz

Esta tabla es la referencia rápida para el analista y para ajustar el catálogo del glosario. La IA la consulta implícitamente a través del campo `activado_por` de cada criterio, pero es útil tenerla disponible como guía de escritura de requisitos.

| Elemento descrito en el requisito | WCAG aplicable | RGPD aplicable | PSD2 aplicable |
|---|---|---|---|
| Formulario con campos de entrada | 1.3.1, 2.1.1, 3.3.1, 4.1.2 | Art25 (minimización) | — |
| Campo que recoge nombre, email o teléfono de persona física | — | Art6, Art13, Art25, Art30 | — |
| Campo de contraseña, token o credencial | — | Art32 (seguridad) | Art97 si es pago |
| Imagen o icono con función operativa | 1.1.1, 4.1.2 | — | — |
| Tabla de datos | 1.3.1 | — | — |
| Modal, drawer o diálogo | 2.1.1, 2.4.3, 4.1.2 | — | — |
| Mensaje de estado, alerta o notificación | 1.4.1, 4.1.3 | — | — |
| Exportación de datos personales | — | Art25, Art32 | — |
| Acción de eliminación de usuario o datos | — | Art17 | — |
| Operación de pago o autorización | — | — | Art97-SCA, RTS-Art22, RTS-Art4 |
| Confirmación de transferencia o cargo | — | — | RTS-Art4 (vinculación dinámica) |
| Registro o log de actividad de pago | — | — | RTS-Art22 (auditoría inmutable) |
| Sesión con expiración por inactividad | 2.2.1 | — | — |
| Datos de categoría especial (salud, origen racial, etc.) | — | Art9 | — |
| Nuevo módulo con cualquier dato personal | — | Art30 (RAT) | — |

---

## Límites del sistema

**No sustituye al DPO ni al asesor legal.** El sistema detecta qué normas son aplicables a partir de patrones en el texto del requisito. No interpreta la norma en casos fronterizos, no valora el riesgo del tratamiento y no puede determinar si una base jurídica concreta es suficiente para un tratamiento específico. Esas decisiones requieren un profesional.

**La detección no es exhaustiva.** El catálogo del glosario cubre los criterios más frecuentes para el contexto definido. Un requisito puede activar obligaciones normativas que el catálogo no contempla. El sistema reduce el riesgo de omisión, no lo elimina. El catálogo debe revisarse al inicio de cada nuevo módulo funcional con el DPO y el área legal.

**Los criterios WCAG generados son de nivel AA.** Los requisitos de nivel AAA y los específicos de la Administración Pública española (Real Decreto 1112/2018 y UNE-EN 301 549) requieren ajustes manuales al catálogo.

**PSD2 asume que la organización es entidad de pago o proveedor de servicios de pago.** Si la organización actúa únicamente como comercio (sin gestionar cuentas de pago ni iniciar operaciones propias), muchos criterios de PSD2 no aplican en el mismo grado. Confirmar el alcance con el área legal antes de activar la sección PSD2 en el glosario.

**Los criterios de tipo `documental` no son verificables con test cases.** La entrada en el RAT, la aprobación del DPO o la realización de una EIPD son acciones organizativas que el pipeline identifica y registra como `evidencia_requerida`, pero que un test de QA no puede verificar. El gate de despliegue a producción debe incluir la comprobación manual de que esas evidencias existen.

---

## Integración con el proceso de gobierno (punto 12)

El cumplimiento normativo tiene su propio ciclo de vida en el sistema de gobierno. Tres adiciones al modelo del punto 12:

**El catálogo de normas es un artefacto gobernado.** Igual que el glosario de términos de negocio, el catálogo de normas tiene un propietario (el DPO o el responsable legal), un proceso de cambio documentado y una cadencia de revisión. Las actualizaciones normativas (nuevas directivas, cambios en los estándares WCAG, jurisprudencia relevante) deben traducirse en actualizaciones del catálogo.

**La métrica de cobertura normativa entra en el dashboard semanal.** Junto a las métricas de calidad del output del punto 12, se añaden:

```yaml
metricas_cumplimiento:
  # Porcentaje de requisitos con datos personales que tienen
  # criterios RGPD documentados.
  cobertura_rgpd: 0.0         # Objetivo: 100%

  # Porcentaje de requisitos con interfaz de usuario que tienen
  # criterios WCAG documentados.
  cobertura_wcag: 0.0         # Objetivo: 100%

  # Número de despliegues bloqueados en el último mes
  # por evidencias normativas pendientes.
  bloqueos_por_cumplimiento: 0  # Señal de alarma: >2 por mes

  # Porcentaje de criterios normativos con test case pasado
  # sobre el total de criterios normativos definidos.
  tasa_verificacion_normativa: 0.0  # Objetivo: >90%
```

**El informe de cumplimiento normativo se genera automáticamente al cierre de sprint** como parte del proceso de retrospectiva. No requiere intervención manual: el script orquestador lo añade como paso opcional configurable en el archivo de configuración del pipeline.
