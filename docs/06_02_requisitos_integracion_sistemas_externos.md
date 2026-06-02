# Gestión de Requisitos de Integración con Sistemas Externos

> Complemento al Modelo Operativo de Análisis Funcional AI-Ready  
> Versión 1.0 · Encaja con los puntos 1–12 del modelo operativo

---

## Por qué los requisitos de integración necesitan su propio flujo

En el modelo operativo base, los prompts y la plantilla YAML están optimizados para requisitos funcionales donde el sistema construye comportamiento nuevo de principio a fin. Los requisitos de integración tienen una naturaleza diferente que rompe ese supuesto en cuatro puntos concretos.

El comportamiento esperado **no depende solo del equipo**. Una parte crítica del resultado la determina el sistema externo: su contrato de API, su modelo de datos, sus tiempos de respuesta, sus códigos de error y sus políticas de cambio. Todo eso puede cambiar sin previo aviso.

La **incertidumbre es estructural**, no excepcional. En un requisito funcional estándar, la ambigüedad es un defecto de análisis que hay que eliminar. En un requisito de integración, parte de la incertidumbre no puede eliminarse hasta que el equipo técnico estudia el sistema externo. El proceso debe acomodar esa incertidumbre en lugar de fingir que no existe.

El **análisis precede a la definición**. Antes de escribir los criterios de aceptación, hay que conocer el contrato de API. Si no existe documentación oficial, hay que descubrirlo mediante un spike técnico. La plantilla de requisito estándar asume que los datos de entrada y salida ya se conocen; aquí esa suposición falla sistemáticamente.

Los **flujos de error son el núcleo**, no el margen. En un requisito funcional, los flujos de excepción suelen ser el 20% del trabajo. En una integración, el manejo de timeouts, errores de red, respuestas inesperadas y fallos parciales es el 60% del trabajo real y la fuente de la mayoría de los bugs en producción.

---

## Taxonomía de integraciones

Antes de aplicar el flujo, hay que clasificar el tipo de integración. El tratamiento no es igual para todos los casos.

```
INTEGRACIONES
│
├── SÍNCRONAS (el sistema espera la respuesta en tiempo real)
│   ├── API REST / GraphQL     → Request-response, contrato OpenAPI/GraphQL
│   ├── SOAP / Web Services    → WSDL, tipos fuertemente tipados
│   └── RPC (gRPC, Thrift)    → Protobuf, esquemas binarios
│
├── ASÍNCRONAS (el sistema no espera, reacciona a eventos)
│   ├── Mensajería (Kafka, RabbitMQ, SQS)  → Esquema de mensaje, topic/cola
│   ├── Webhooks recibidos     → El externo nos notifica, nosotros procesamos
│   └── Webhooks enviados      → Nosotros notificamos al externo
│
├── TRANSFERENCIA DE DATOS (batch, no tiempo real)
│   ├── SFTP / FTP             → Formato de fichero, frecuencia, protocolo
│   ├── EDI                    → Estándar (EDIFACT, X12), segmentos
│   └── Base de datos directa → Esquema compartido, vistas, stored procedures
│
└── DELEGACIÓN DE FUNCIONALIDAD (el externo ejecuta algo por nosotros)
    ├── Autenticación (OAuth2, SAML, LDAP)
    ├── Pagos (Stripe, Redsys, Adyen)
    └── Servicios de plataforma (envío de emails, SMS, firma digital)
```

La taxonomía importa porque determina qué artefactos de contrato necesita el analista antes de poder escribir el requisito, y qué tipos de prueba son relevantes.

---

## El flujo en cinco fases

A diferencia del flujo estándar del modelo operativo, los requisitos de integración pasan por una fase de descubrimiento técnico antes de llegar a la plantilla YAML. Sin ese descubrimiento, la plantilla se rellena con suposiciones que generan artefactos incorrectos.

```
FASE 0 — CLASIFICACIÓN Y VIABILIDAD          (analista + tech lead, 30 min)
         ¿Qué tipo de integración es?
         ¿Existe documentación oficial del sistema externo?
         ¿Hay un entorno de sandbox disponible?
                │
                ▼
FASE 1 — DESCUBRIMIENTO DEL CONTRATO          (tech lead + analista, variable)
         Obtener / generar el contrato de API
         Identificar operaciones relevantes para el requisito
         Mapear entidades externas al glosario interno
                │
                ▼
FASE 2 — ANÁLISIS DE INCERTIDUMBRE            (analista, 1-2h)
         Completar la plantilla de incertidumbre
         Abrir preguntas abiertas formales
         Decidir si el requisito puede avanzar o necesita un spike
                │
         ┌──────────────┐
         │              │
         ▼              ▼
    SPIKE TÉCNICO   CONTINÚA
    (si hay dudas   (si el contrato
    bloqueantes)     está claro)
         │              │
         └──────┬───────┘
                ▼
FASE 3 — REDACCIÓN DEL REQUISITO YAML         (analista, 2-4h)
         Plantilla extendida con bloque de integración
         Criterios de aceptación para flujos normales Y de error
         Datos de prueba con valores reales del sistema externo
                │
                ▼
FASE 4 — GENERACIÓN DE ARTEFACTOS             (pipeline AI)
         Prompts especializados para requisitos de integración
         Tareas técnicas con capa de integración explícita
         Test cases con mocks y casos de fallo del sistema externo
```

---

## Fase 0 — Clasificación y viabilidad

Esta conversación de 30 minutos entre el analista y el tech lead evita semanas de trabajo mal orientado.

Las preguntas que hay que responder son estas. Primero, ¿quién es el propietario del sistema externo? ¿Es un sistema interno de la misma organización, un proveedor con SLA contractual, o un servicio de terceros sin garantías? La respuesta determina el nivel de control que el equipo tiene sobre los cambios futuros del contrato y el nivel de defensividad que debe tener la implementación.

Segundo, ¿existe documentación oficial? Un contrato OpenAPI (Swagger), un WSDL, una colección Postman o un esquema de mensaje en Confluent Schema Registry son puntos de partida radicalmente distintos a "hay que preguntarle al equipo que lo hizo".

Tercero, ¿hay un entorno de sandbox o de pruebas? Sin sandbox, los test cases de integración real son imposibles en desarrollo y arriesgados en preprod. Esto afecta directamente a la estrategia de testing y a la generación de test cases del pipeline.

Cuarto, ¿tiene el sistema externo historial de cambios no controlados? Si el proveedor ha roto el contrato sin previo aviso en el pasado, el nivel de defensividad del diseño debe ser mayor: más validación de respuestas, versionado del cliente, circuit breaker más agresivo.

El resultado de esta conversación es una de estas tres decisiones:

```
DECISIÓN A: Proceder con la Fase 1
  → Hay documentación suficiente para iniciar el análisis del contrato

DECISIÓN B: Abrir un spike técnico antes de la Fase 1
  → No hay documentación o el sistema externo es desconocido para el equipo
  → El spike tiene tiempo box de 2-4 horas y produce el contrato mínimo viable

DECISIÓN C: Escalar a producto o a arquitectura
  → El sistema externo no tiene API documentada y no hay acceso a sus propietarios
  → No es posible definir el requisito hasta resolver la dependencia de información
```

---

## Fase 1 — Descubrimiento del contrato

El contrato es el documento de autoridad que describe cómo se comunica el sistema externo. Puede llegar de múltiples fuentes con calidad muy diferente.

### Fuentes de contrato y cómo tratarlas

**Especificación OpenAPI (Swagger)**

La fuente más completa para APIs REST. Antes de usarla hay que hacer tres verificaciones. Primero, que la versión de la especificación corresponde a la versión del sistema externo en producción: es frecuente que la documentación esté desactualizada. Segundo, que los ejemplos de respuesta incluidos son reales, no ilustrativos. Tercero, que los campos marcados como opcionales en el esquema realmente lo son o si en la práctica siempre vienen.

```yaml
# Fragmento de lo que extrae el analista de un OpenAPI para el requisito
endpoint_relevante:
  path: /api/v2/invoices
  metodo: GET
  parametros_relevantes:
    - nombre: date_from
      tipo: string
      formato: ISO-8601
      requerido: true
      nota_analista: "La API acepta también DD/MM/YYYY pero devuelve error no documentado"
  respuesta_exitosa:
    codigo: 200
    campos_usados:
      - invoice_id       # string, siempre presente
      - invoice_date     # string ISO-8601, siempre presente
      - total_amount     # decimal con 2 decimales, siempre presente
      - status           # enum: PENDING, APPROVED, PAID, CANCELLED
      - supplier_ref     # string, OPCIONAL (ausente en facturas antiguas)
    campos_ignorados:
      - internal_id      # ID interno del proveedor, sin uso en nuestro sistema
      - audit_fields     # Metadatos de auditoría del proveedor
  codigos_error_documentados:
    - 400: "Parámetros inválidos (fecha mal formateada)"
    - 401: "Token expirado o inválido"
    - 429: "Rate limit: máx 100 peticiones/minuto"
    - 500: "Error interno del servidor externo"
  codigos_error_observados_no_documentados:
    - 503: "Ocurre en mantenimiento los domingos entre 2:00 y 4:00 AM"
```

**WSDL (servicios SOAP)**

Más verboso pero más preciso en tipos. El analista no necesita leer el XML directamente: basta con importar el WSDL en SoapUI o Postman y explorar las operaciones disponibles. Lo más importante es identificar qué operaciones del servicio corresponden al requisito y qué campos del esquema son obligatorios vs. opcionales, porque en SOAP los campos `nillable="false"` son obligatorios aunque no estén marcados como required explícitamente.

**Colección Postman o ejemplos de request/response**

Fuente habitual cuando la documentación formal no existe. El riesgo es que los ejemplos pueden estar desactualizados o ser casos felices que no muestran los campos opcionales ni los errores. Hay que complementarlos siempre con una sesión de pruebas reales contra el sandbox.

**Sin documentación disponible**

Cuando no hay documentación, el spike técnico usa estas técnicas en orden de preferencia: revisar el código fuente si el sistema externo es interno a la organización, capturar tráfico real con un proxy (Charles, mitmproxy) si hay un entorno donde ya funciona la integración, o preguntar al equipo propietario del sistema externo con una lista de preguntas específicas (no "¿cómo funciona?" sino "¿qué devuelve el campo X cuando Y?").

### Artefacto de contrato mínimo viable

Al final de la Fase 1, el analista produce este documento YAML que alimenta directamente la plantilla del requisito de integración y los prompts de generación:

```yaml
# contrato_api_[sistema_externo]_v1.yaml
sistema_externo:
  nombre: "ERP-SAP Financiero"
  propietario: "Departamento de Sistemas - Finanzas"
  contacto_tecnico: "sistemas-finanzas@empresa.com"
  version_api: "2.1.4"
  entorno_sandbox: "https://erp-sandbox.empresa.com/api/v2"
  entorno_produccion: "https://erp.empresa.com/api/v2"
  autenticacion:
    tipo: oauth2
    endpoint_token: "/auth/token"
    scopes_requeridos: ["invoices:read"]
    expiracion_token_segundos: 3600
    renovacion: automatica_con_refresh_token
  rate_limiting:
    max_peticiones_por_minuto: 100
    comportamiento_al_superar: "HTTP 429 con header Retry-After"
  sla_documentado:
    disponibilidad: "99.5% mensual"
    tiempo_respuesta_p95: "800ms"
    ventanas_mantenimiento: "Domingos 02:00-04:00 CET"

operaciones_relevantes:
  - id: OP-001
    nombre: "Obtener facturas por rango de fechas"
    endpoint: "GET /invoices"
    parametros:
      - nombre: date_from
        tipo: string
        formato: "YYYY-MM-DD"
        requerido: true
      - nombre: date_to
        tipo: string
        formato: "YYYY-MM-DD"
        requerido: true
      - nombre: page
        tipo: integer
        requerido: false
        valor_defecto: 1
      - nombre: page_size
        tipo: integer
        requerido: false
        valor_defecto: 50
        maximo: 200
    respuesta_exitosa:
      codigo_http: 200
      estructura:
        data: array_de_facturas
        pagination:
          total: integer
          page: integer
          page_size: integer
          has_more: boolean
      campos_factura:
        - nombre: invoice_id
          tipo: string
          siempre_presente: true
          mapeo_interno: id_factura
        - nombre: invoice_date
          tipo: string
          formato: ISO-8601
          siempre_presente: true
          mapeo_interno: fecha_factura
        - nombre: total_amount
          tipo: decimal
          precision: 2
          moneda: EUR
          siempre_presente: true
          mapeo_interno: importe_total
        - nombre: status
          tipo: enum
          valores: [PENDING, APPROVED, PAID, CANCELLED, DISPUTED]
          siempre_presente: true
          mapeo_interno: estado
          nota: "DISPUTED no existe en nuestro modelo. Tratar como PENDING."
        - nombre: supplier_ref
          tipo: string
          siempre_presente: false
          ausente_cuando: "Facturas anteriores a 2022-01-01"
          mapeo_interno: referencia_proveedor
    codigos_error:
      - codigo: 400
        descripcion: "Parámetros inválidos"
        cuerpo_ejemplo: '{"error": "INVALID_DATE_FORMAT", "message": "date_from must be YYYY-MM-DD"}'
        accion_sistema: "Mostrar error de validación al usuario. No reintentar."
      - codigo: 401
        descripcion: "Token inválido o expirado"
        cuerpo_ejemplo: '{"error": "UNAUTHORIZED"}'
        accion_sistema: "Renovar token y reintentar una vez. Si vuelve a fallar, mostrar error."
      - codigo: 429
        descripcion: "Rate limit superado"
        header_relevante: "Retry-After: N"
        accion_sistema: "Esperar N segundos y reintentar. Máximo 3 reintentos."
      - codigo: 500
        descripcion: "Error interno del sistema externo"
        accion_sistema: "Registrar en log. Mostrar error genérico al usuario. No reintentar automáticamente."
      - codigo: 503
        descripcion: "Servicio no disponible (mantenimiento)"
        accion_sistema: "Mostrar mensaje 'El servicio no está disponible temporalmente'. No reintentar."
    comportamientos_no_documentados:
      - "Si date_from es posterior a date_to, devuelve 200 con array vacío (no 400)"
      - "Si el rango supera 365 días, devuelve 200 con los primeros 200 resultados sin aviso de truncamiento"
      - "El campo total_amount puede ser negativo en facturas de abono"
    comportamientos_a_validar_en_sandbox:
      - "Comportamiento con rango vacío de resultados"
      - "Comportamiento en ventana de mantenimiento (esperar al domingo)"
```

---

## Fase 2 — Análisis de incertidumbre

Con el contrato en mano, el analista completa la plantilla de incertidumbre antes de escribir el requisito. Este paso es el que diferencia a un analista experto de uno junior en integraciones: saber qué no se sabe es tan importante como saber lo que se sabe.

### Plantilla de análisis de incertidumbre

```yaml
# analisis_incertidumbre_[REQ-ID].yaml

certezas:                  # Lo que se sabe con seguridad
  - "El endpoint GET /invoices existe y responde en el sandbox"
  - "Los campos invoice_id, invoice_date, total_amount y status siempre están presentes"
  - "La autenticación es OAuth2 con token renovable"
  - "El rate limit es 100 peticiones/minuto con header Retry-After"

incertidumbres_menores:    # Lo que no se sabe pero no bloquea el análisis
  # Requieren respuesta antes del refinamiento, no antes de escribir el requisito
  - id: IM-01
    pregunta: "¿El campo supplier_ref estará siempre presente para facturas futuras?"
    impacto: "Si no, hay que manejar la ausencia en el mapeo interno"
    responsable_respuesta: "sistemas-finanzas@empresa.com"
    plazo: "2025-05-20"
    decision_provisional: "Tratar como opcional. Si falta, dejar referencia_proveedor en blanco."

  - id: IM-02
    pregunta: "¿Puede total_amount ser cero (facturas de servicio sin coste)?"
    impacto: "Afecta a validaciones en el listado y posiblemente al flujo de aprobación"
    responsable_respuesta: "Ana López, Dir. Financiera"
    plazo: "2025-05-20"
    decision_provisional: "Asumir que sí puede ser cero y mostrarlo como €0,00"

incertidumbres_bloqueantes: # Lo que no se sabe y SÍ bloquea la escritura correcta del requisito
  # Si alguna existe, el requisito no puede pasar a validado hasta resolverse
  - id: IB-01
    pregunta: >
      El sistema externo devuelve facturas con status DISPUTED que no existe en
      nuestro modelo de datos. ¿Debemos mostrarlo como PENDING, crear un nuevo
      estado en nuestro sistema, o filtrar estas facturas?
    impacto: >
      Afecta al modelo de datos, al mapeo de estados y a los criterios de aceptación
      de filtrado. Sin esta respuesta, cualquier AC sobre estados será incorrecto.
    responsable_respuesta: "Product Owner + Ana López"
    plazo: "2025-05-15"
    estado: pendiente

riesgos_contractuales:     # Comportamientos del sistema externo que pueden cambiar
  - riesgo: >
      El comportamiento no documentado de devolver 200 con array vacío para rangos
      invertidos puede cambiar a 400 en una actualización futura del sistema externo.
    probabilidad: media
    impacto: alto
    mitigacion: >
      Implementar validación client-side del rango antes de llamar al API,
      de forma que nunca enviemos una petición con date_from > date_to.

  - riesgo: >
      El rate limit de 100 peticiones/minuto puede ser insuficiente si el volumen
      de consultas de los gestores crece. El proveedor no documenta si ese límite
      es por usuario o por organización.
    probabilidad: baja
    impacto: medio
    mitigacion: >
      Implementar caché de resultados con TTL de 5 minutos para peticiones idénticas.
      Monitorizar el consumo de rate limit desde el día de despliegue.

decision_spike:
  necesario: false
  # Si fuera true:
  # objetivo: "Verificar el comportamiento con status DISPUTED en el sandbox"
  # duracion_time_box: "4 horas"
  # responsable: "Tech lead backend"
  # criterio_exito: "Documento de comportamiento observado con capturas de tráfico"
```

---

## Fase 3 — La plantilla YAML extendida para integraciones

La plantilla base del modelo operativo se extiende con un bloque de integración que encapsula todo el conocimiento del contrato. El analista no necesita que el desarrollador lea el contrato por separado: toda la información relevante está en el YAML del requisito.

```yaml
# REQ-025.yaml
# BLOQUE 1 — IDENTIDAD (igual que la plantilla base)
id: REQ-025
titulo: "Recuperar facturas de proveedor desde ERP externo por rango de fechas"
version: "1.0"
estado: en-revision
epica: EP-04
modulo: "Gestión de Facturación"
origen:
  solicitante: "Ana López"
  area: "Dirección Financiera"
  fecha_solicitud: "2025-05-10"
  referencia: "ACTA-2025-041"
fecha_creacion: "2025-05-12"
analista: "Carlos Ruiz"
prioridad: must-have

# BLOQUE 2 — CONTEXTO DE NEGOCIO (igual que la plantilla base)
actor: "Gestor de facturación"
evento_disparador: >
  El gestor de facturación necesita consultar el listado de facturas
  de proveedores para el proceso de cierre contable mensual.
objetivo_negocio: >
  Eliminar la necesidad de acceder directamente al ERP externo para
  consultar facturas, centralizando la información en el módulo de
  facturación interno. El proceso actual requiere alternar entre dos
  sistemas, lo que produce errores de transcripción y consume
  aproximadamente 45 minutos adicionales por cierre mensual.
descripcion: >
  El sistema debe recuperar del ERP externo (SAP Financiero) las facturas
  de proveedores correspondientes a un rango de fechas, mapear los datos
  al modelo interno y mostrarlas en el listado de facturas del módulo.
  La consulta es de solo lectura: el sistema no modifica datos en el ERP.
reglas_negocio:
  - "El rango máximo de consulta es de 365 días (restricción de rendimiento)"
  - "Solo se recuperan facturas del ejercicio fiscal en curso"
  - "Las facturas con estado DISPUTED en el ERP se tratan como PENDING internamente"
  - "Las facturas con importe cero o negativo se recuperan y muestran normalmente"

# BLOQUE 3 — COMPORTAMIENTO ESPERADO
flujo_principal:
  - paso: 1
    actor: "Gestor de facturación"
    accion: "Introduce fecha_inicio y fecha_fin en el panel de filtros y pulsa Buscar"
    resultado: "El sistema valida el rango y construye la petición al ERP"
  - paso: 2
    actor: "sistema"
    accion: "Llama al endpoint GET /invoices del ERP con el rango de fechas"
    resultado: "El ERP responde con la lista de facturas del período"
  - paso: 3
    actor: "sistema"
    accion: "Mapea los campos del ERP al modelo interno y aplica la transformación de estados"
    resultado: "Las facturas están disponibles en el formato del módulo interno"
  - paso: 4
    actor: "sistema"
    accion: "Muestra las facturas en el listado ordenadas por fecha descendente"
    resultado: "El gestor ve el listado con el contador de resultados"

flujos_alternativos:
  - condicion: "El ERP devuelve múltiples páginas (más de 200 facturas)"
    pasos:
      - paso: 1
        actor: "sistema"
        accion: "Detecta que has_more es true en la respuesta"
        resultado: "Realiza peticiones adicionales con paginación hasta obtener todos los resultados"
      - paso: 2
        actor: "sistema"
        accion: "Combina todas las páginas y aplica el mapeo completo"
        resultado: "El gestor ve el listado completo con el total real de registros"

excepciones:
  - condicion: "El ERP devuelve error 401 (token expirado)"
    comportamiento: >
      El sistema renueva automáticamente el token OAuth2 y reintenta la petición
      una vez. Si el segundo intento también falla con 401, muestra el mensaje:
      'Error de autenticación con el sistema externo. Contacte con el equipo de sistemas.'
  - condicion: "El ERP devuelve error 429 (rate limit)"
    comportamiento: >
      El sistema espera los segundos indicados en el header Retry-After y reintenta
      automáticamente hasta 3 veces. Si tras 3 reintentos sigue fallando, muestra:
      'El sistema externo está recibiendo demasiadas peticiones. Inténtelo en unos minutos.'
  - condicion: "El ERP devuelve error 500 o 503"
    comportamiento: >
      El sistema no reintenta automáticamente. Registra el error en el log de integraciones
      con el código de respuesta, el timestamp y el rango de fechas solicitado.
      Muestra al gestor: 'El servicio de facturas no está disponible temporalmente.
      Inténtelo de nuevo más tarde.'
  - condicion: "El ERP no responde en menos de 10 segundos (timeout)"
    comportamiento: >
      El sistema cancela la petición, registra el timeout en el log de integraciones
      y muestra el mismo mensaje que para los errores 500/503.
  - condicion: "El ERP responde 200 pero el array de datos está vacío"
    comportamiento: >
      El sistema muestra el estado vacío estándar del módulo de facturas con el texto
      'No se encontraron facturas en el sistema externo para el período seleccionado.'

criterios_aceptacion:
  - id: AC-025-01
    titulo: "Consulta exitosa devuelve facturas correctamente mapeadas"
    dado: >
      El gestor está autenticado con rol gestor_facturacion, el ERP externo
      está disponible, y existen facturas en el período 2024-01-01 a 2024-03-31
    cuando: >
      Introduce fecha_inicio=2024-01-01, fecha_fin=2024-03-31 y pulsa Buscar
    entonces: >
      El listado muestra las facturas del período con los campos id_factura,
      fecha_factura, importe_total (en euros con 2 decimales), estado y
      referencia_proveedor (en blanco si no viene en la respuesta del ERP).
      Los resultados aparecen en menos de 5 segundos para conjuntos de hasta
      500 facturas. El contador muestra el número total de facturas recuperadas.
    tipo: positivo
    datos_ejemplo:
      fecha_inicio: "2024-01-01"
      fecha_fin: "2024-03-31"
      invoice_id_erp: "INV-2024-00123"
      invoice_date_erp: "2024-01-15T00:00:00Z"
      total_amount_erp: 1250.50
      status_erp: "APPROVED"
      id_factura_esperado: "INV-2024-00123"
      fecha_factura_esperada: "2024-01-15"
      importe_total_esperado: 1250.50
      estado_esperado: "aprobada"

  - id: AC-025-02
    titulo: "Facturas con estado DISPUTED se tratan como PENDING"
    dado: >
      El ERP devuelve al menos una factura con status=DISPUTED en el período consultado
    cuando: >
      El sistema procesa la respuesta del ERP y mapea los estados
    entonces: >
      Las facturas con status=DISPUTED en el ERP aparecen con estado 'pendiente'
      en el módulo interno. No aparece ninguna factura con estado 'disputed'
      o similar en el listado.
    tipo: positivo
    datos_ejemplo:
      status_erp: "DISPUTED"
      estado_interno_esperado: "pendiente"

  - id: AC-025-03
    titulo: "Error de comunicación con el ERP muestra mensaje informativo"
    dado: >
      El ERP externo devuelve un error HTTP 500 o no responde en 10 segundos
    cuando: >
      El gestor ejecuta una búsqueda válida
    entonces: >
      El sistema no muestra datos parciales ni un estado vacío genérico.
      Muestra el mensaje exacto: 'El servicio de facturas no está disponible
      temporalmente. Inténtelo de nuevo más tarde.'
      El error queda registrado en el log de integraciones con el timestamp
      y los parámetros de la petición fallida.
    tipo: negativo
    datos_ejemplo:
      codigo_respuesta_erp: 500

  - id: AC-025-04
    titulo: "Token expirado se renueva automáticamente sin impacto al usuario"
    dado: >
      El token OAuth2 actual está expirado cuando el gestor ejecuta la búsqueda
    cuando: >
      El sistema recibe un error 401 del ERP en el primer intento
    entonces: >
      El sistema renueva el token de forma transparente al usuario y reintenta
      la petición. El gestor recibe los resultados normalmente sin ver ningún
      mensaje de error de autenticación. El tiempo total de respuesta no supera
      los 8 segundos (5s base + 3s adicionales por la renovación del token).
    tipo: positivo

  - id: AC-025-05
    titulo: "Rate limit del ERP provoca reintento automático"
    dado: >
      El ERP devuelve HTTP 429 con header Retry-After: 30
    cuando: >
      El sistema recibe la respuesta 429 en el primer intento
    entonces: >
      El sistema espera 30 segundos y reintenta automáticamente la petición.
      Si el reintento tiene éxito, el gestor ve los resultados normalmente.
      El gestor no ve ningún mensaje de error durante la espera
      (puede mostrarse un indicador de carga).
    tipo: positivo

definition_of_done:
  - "Todos los criterios de aceptación superan las pruebas de regresión"
  - "Prueba de integración real contra el ERP sandbox con dataset representativo"
  - "Log de integraciones verificado para los casos de error documentados"
  - "Tiempo de respuesta validado en staging con carga realista"
  - "Circuit breaker configurado y probado"

# BLOQUE 4 — DATOS
datos_entrada:
  - nombre: fecha_inicio
    tipo: date
    requerido: true
    formato: YYYY-MM-DD
  - nombre: fecha_fin
    tipo: date
    requerido: true
    formato: YYYY-MM-DD

datos_salida:
  campos:
    - id_factura
    - fecha_factura
    - importe_total
    - estado
    - referencia_proveedor
  formato: pantalla
  paginacion:
    aplica: true
    tamanyo_pagina_defecto: 50
    max_registros: null    # Sin límite impuesto por nuestro sistema
  orden_defecto: "fecha_factura DESC"
  tiempo_respuesta_max_ms: 5000

# BLOQUE 5 — METADATOS TÉCNICOS + BLOQUE DE INTEGRACIÓN (extensión)
componentes_afectados:
  - "api-facturacion"
  - "frontend-facturas"
  - "cliente-erp-externo"
  - "bd-cache-facturas"

integracion_externa:
  sistema: "ERP-SAP Financiero"
  tipo: API-REST
  contrato_referencia: "contrato_api_erp_sap_v1.yaml"
  operacion_principal: "GET /invoices"
  autenticacion: "OAuth2 client_credentials"
  patron_resiliencia:
    retry:
      activo: true
      max_intentos: 3
      codigos_a_reintentar: [429, 503]
      backoff: exponencial
      max_espera_segundos: 60
    circuit_breaker:
      activo: true
      umbral_errores_pct: 50
      ventana_segundos: 60
      tiempo_recuperacion_segundos: 30
    timeout:
      conexion_ms: 3000
      lectura_ms: 10000
    cache:
      activo: true
      ttl_segundos: 300
      clave: "facturas:{fecha_inicio}:{fecha_fin}:{pagina}"
  mapeo_estados:
    PENDING: "pendiente"
    APPROVED: "aprobada"
    PAID: "pagada"
    CANCELLED: "rechazada"
    DISPUTED: "pendiente"    # Tratamiento provisional hasta IB-01 resuelto
  incertidumbres_pendientes:
    - ref: IB-01
      descripcion: "Tratamiento definitivo del estado DISPUTED"
      bloquea_desarrollo: false
      decision_provisional: "Mapear a pendiente"

restricciones_no_funcionales:
  rendimiento: >
    La respuesta debe estar disponible en menos de 5 segundos para conjuntos
    de hasta 500 facturas. Para conjuntos mayores, mostrar indicador de progreso.
  seguridad: >
    Las credenciales OAuth2 nunca se transmiten al frontend ni se incluyen en logs.
    El token de acceso se almacena en memoria del servidor, nunca en base de datos.
  disponibilidad: >
    El módulo de facturación debe seguir funcionando aunque el ERP esté caído
    mostrando el mensaje de error apropiado. El ERP no disponible no debe
    provocar errores 500 en nuestro sistema.
  volumen_datos: >
    Se estima un máximo de 2.000 facturas por consulta mensual estándar.
    El sistema debe manejar hasta 10.000 facturas en consultas de rango anual.

trazabilidad:
  historias_generadas: []
  test_cases_generados: []
  jira_issues: []
```

---

## Fase 4 — Prompts especializados para integraciones

Los prompts del modelo operativo base necesitan modificadores específicos para los requisitos de integración. Estos modificadores se añaden al system prompt del Prompt 2 (generación de historia) y al Prompt 3 (generación de tareas técnicas).

### Modificador para el Prompt 2 — Historia de usuario de integración

```
CONTEXTO ADICIONAL — REQUISITO DE INTEGRACIÓN:

Este requisito implica integración con el sistema externo {{sistema_externo}}.

PRINCIPIOS OBLIGATORIOS para este tipo de requisito:

1. Los criterios de aceptación DEBEN incluir al menos:
   - Un criterio del flujo exitoso con datos concretos del sistema externo
   - Un criterio para cada código de error documentado relevante para el usuario
   - Un criterio para el timeout o fallo de comunicación
   - Un criterio para cualquier transformación de datos no trivial (mapeo de estados, conversión de tipos)

2. En la descripción de la historia, incluir una sección "Comportamiento ante fallos del sistema externo"
   que describa en lenguaje de negocio cómo experimenta el usuario cada tipo de fallo.

3. Las tareas técnicas DEBEN incluir:
   - Una tarea específica de tipo "integracion" para el cliente HTTP
   - Una tarea de tipo "testing" que cubra los mocks del sistema externo
   - Si hay circuit breaker: una tarea de tipo "infraestructura"

4. El campo "notas_importantes" de la historia debe incluir explícitamente:
   - Qué ocurre si el sistema externo no está disponible
   - Qué garantías ofrece el sistema sobre la consistencia de los datos

5. Las incertidumbres_pendientes del bloque de integración deben aparecer
   como notas en la historia con el prefijo [PENDIENTE DE DECISIÓN]:

CONTRATO DE API RELEVANTE:
{{contrato_api_yaml}}

INCERTIDUMBRES ABIERTAS:
{{incertidumbres_pendientes}}
```

### Modificador para el Prompt 3 — Tareas técnicas de integración

```
CONTEXTO ADICIONAL — DESCOMPOSICIÓN TÉCNICA DE INTEGRACIÓN:

Para este requisito de integración, la descomposición en tareas DEBE seguir
este patrón específico:

TAREA OBLIGATORIA 1 — Cliente de integración (capa: integracion)
  Implementar el cliente HTTP para {{sistema_externo}} con:
  - Autenticación: {{tipo_autenticacion}}
  - Retry logic: {{patron_retry}}
  - Circuit breaker: {{patron_circuit_breaker}}
  - Timeout: {{timeout_configuracion}}
  - Logging estructurado de todas las llamadas (sin incluir datos sensibles)
  
TAREA OBLIGATORIA 2 — Mapeo y transformación (capa: backend)
  Implementar el mapeo entre el modelo externo y el modelo interno:
  {{mapeo_estados}}
  Incluir validación de los campos opcionales y manejo de valores inesperados.
  
TAREA OBLIGATORIA 3 — Tests de integración con mocks (capa: testing)
  Implementar mock del sistema externo {{sistema_externo}} para los tests:
  - Escenario de respuesta exitosa con datos representativos
  - Escenario de error 401 → renovación de token → éxito
  - Escenario de error 429 → wait → reintento → éxito
  - Escenario de error 500 → mensaje de error al usuario
  - Escenario de timeout → mensaje de error al usuario
  - Escenario de respuesta con paginación (múltiples páginas)
  
TAREA CONDICIONAL — Cache (si cache.activo = true)
  Implementar cache con clave {{cache_clave}} y TTL {{ttl_segundos}} segundos.
  Incluir lógica de invalidación cuando aplique.

TAREA CONDICIONAL — Circuit breaker (si circuit_breaker.activo = true)
  Configurar y probar el circuit breaker:
  - Estado CLOSED: comportamiento normal
  - Estado OPEN: respuesta inmediata de error sin llamar al sistema externo
  - Estado HALF-OPEN: prueba de recuperación
```

### Modificador para los prompts de test cases de integración

```
CONTEXTO ADICIONAL — TEST CASES DE INTEGRACIÓN:

Para los test cases de este requisito de integración, seguir estas reglas adicionales:

CATEGORÍAS OBLIGATORIAS (además de las estándar):

CATEGORÍA F — Disponibilidad del sistema externo:
  Para cada código de error del sistema externo documentado, generar un test case que:
  - Describe el mock del sistema externo que simula ese error
  - Verifica el mensaje exacto que ve el usuario
  - Verifica que no se muestran datos parciales o incorrectos
  - Verifica que el error queda registrado en el log de integraciones

CATEGORÍA G — Transformaciones de datos:
  Para cada mapeo no trivial documentado en el contrato, generar un test case que:
  - Proporciona el valor original del sistema externo como dato de prueba
  - Verifica el valor transformado en el sistema interno
  - Especialmente importante para: mapeo de estados, conversión de tipos,
    normalización de fechas y manejo de campos opcionales ausentes

CATEGORÍA H — Resiliencia:
  Para cada patrón de resiliencia configurado (retry, circuit breaker, cache):
  - Test del comportamiento con el patrón activo
  - Test del comportamiento cuando el patrón se agota (todos los reintentos fallidos)

FORMATO DE MOCK EN LOS TEST CASES:
Cada test case de integración debe incluir el campo "mock_sistema_externo" que describe:
  - El endpoint mockeado
  - El código de respuesta simulado
  - El cuerpo de respuesta simulado (si aplica)
  - Cualquier header relevante (ej: Retry-After)
```

---

## Ejemplo completo: test cases generados para REQ-025

Este es el output del pipeline para los criterios de aceptación del requisito anterior.

```yaml
test_cases:
  # ── CATEGORÍA: Flujo exitoso ───────────────────────────────────────
  - id: TC-025-01
    titulo: "Consulta exitosa al ERP devuelve facturas correctamente mapeadas"
    tipo: funcional_positivo
    criterio_origen: AC-025-01
    historia_origen: US-052
    prioridad: critica
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
      - "Token OAuth2 válido disponible"
      - "ERP sandbox disponible y con datos de prueba cargados"
    mock_sistema_externo:
      endpoint: "GET /invoices?date_from=2024-01-01&date_to=2024-03-31&page=1&page_size=50"
      codigo_respuesta: 200
      cuerpo_respuesta:
        data:
          - invoice_id: "INV-2024-00123"
            invoice_date: "2024-01-15T00:00:00Z"
            total_amount: 1250.50
            status: "APPROVED"
            supplier_ref: "PROV-SAP-001"
        pagination:
          total: 1
          page: 1
          page_size: 50
          has_more: false
    datos_prueba:
      fecha_inicio: "2024-01-01"
      fecha_fin: "2024-03-31"
    pasos:
      - numero: 1
        accion: "Navegar a /facturas, introducir fecha_inicio=2024-01-01 y fecha_fin=2024-03-31"
        resultado_esperado: "Los campos muestran las fechas introducidas"
      - numero: 2
        accion: "Pulsar el botón Buscar"
        resultado_esperado: "Aparece indicador de carga"
      - numero: 3
        accion: "Esperar la respuesta"
        resultado_esperado: >
          En menos de 5 segundos aparece el listado con la factura INV-2024-00123.
          El campo id_factura muestra 'INV-2024-00123'.
          El campo fecha_factura muestra '15/01/2024'.
          El campo importe_total muestra '1.250,50 €'.
          El campo estado muestra 'aprobada' (no 'APPROVED').
          El campo referencia_proveedor muestra 'PROV-SAP-001'.
          El contador muestra '1 factura encontrada'.
    automatizable: true

  # ── CATEGORÍA: Transformación de datos ────────────────────────────
  - id: TC-025-02
    titulo: "Factura con estado DISPUTED del ERP se muestra como pendiente"
    tipo: funcional_positivo
    criterio_origen: AC-025-02
    historia_origen: US-052
    prioridad: alta
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
      - "ERP sandbox con factura en estado DISPUTED disponible"
    mock_sistema_externo:
      endpoint: "GET /invoices"
      codigo_respuesta: 200
      cuerpo_respuesta:
        data:
          - invoice_id: "INV-2024-00456"
            invoice_date: "2024-02-10T00:00:00Z"
            total_amount: 890.00
            status: "DISPUTED"
        pagination:
          total: 1
          page: 1
          page_size: 50
          has_more: false
    pasos:
      - numero: 1
        accion: "Ejecutar búsqueda válida que incluya la factura INV-2024-00456"
        resultado_esperado: "El listado carga correctamente"
      - numero: 2
        accion: "Localizar la factura INV-2024-00456 en el listado"
        resultado_esperado: >
          La factura aparece con estado 'pendiente', no con 'DISPUTED' ni
          'disputada' ni ningún otro valor. No hay mensaje de error ni aviso especial.
    automatizable: true
    comportamiento_incorrecto_habitual: >
      El desarrollador muestra el valor crudo del ERP ('DISPUTED') porque no
      implementó el mapeo para ese valor, o genera un error al recibir un
      estado desconocido.

  # ── CATEGORÍA: Errores del sistema externo ────────────────────────
  - id: TC-025-03
    titulo: "Error 500 del ERP muestra mensaje informativo sin datos parciales"
    tipo: negativo_sistema_externo
    criterio_origen: AC-025-03
    historia_origen: US-052
    prioridad: critica
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
    mock_sistema_externo:
      endpoint: "GET /invoices"
      codigo_respuesta: 500
      cuerpo_respuesta:
        error: "INTERNAL_SERVER_ERROR"
        message: "An unexpected error occurred"
    pasos:
      - numero: 1
        accion: "Ejecutar una búsqueda válida"
        resultado_esperado: "El sistema llama al ERP y recibe el error 500"
      - numero: 2
        accion: "Observar la respuesta del sistema"
        resultado_esperado: >
          El listado NO muestra ninguna factura ni estado vacío genérico.
          Aparece el mensaje exacto: 'El servicio de facturas no está disponible
          temporalmente. Inténtelo de nuevo más tarde.'
          No hay rastro del error interno (500, stack trace, mensaje del ERP)
          en la pantalla del usuario.
      - numero: 3
        accion: "Verificar el log de integraciones"
        resultado_esperado: >
          Existe una entrada de log con: timestamp, código de respuesta (500),
          endpoint llamado, parámetros de la petición (sin datos sensibles).
    automatizable: true
    comportamiento_incorrecto_habitual: >
      El sistema muestra un estado vacío genérico haciendo creer al usuario
      que no hay facturas, cuando en realidad el ERP no respondió.
      O bien muestra el mensaje de error técnico del ERP directamente.

  - id: TC-025-04
    titulo: "Timeout del ERP (>10s) muestra mismo mensaje que error 500"
    tipo: negativo_sistema_externo
    criterio_origen: AC-025-03
    historia_origen: US-052
    prioridad: alta
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
    mock_sistema_externo:
      endpoint: "GET /invoices"
      comportamiento: "no_response"
      delay_ms: 11000
    pasos:
      - numero: 1
        accion: "Ejecutar una búsqueda válida"
        resultado_esperado: "El indicador de carga aparece"
      - numero: 2
        accion: "Esperar 10 segundos sin recibir respuesta del ERP"
        resultado_esperado: >
          El sistema cancela la petición tras 10 segundos.
          Aparece el mensaje: 'El servicio de facturas no está disponible
          temporalmente. Inténtelo de nuevo más tarde.'
          El tiempo total desde la búsqueda hasta el mensaje es de
          entre 10 y 12 segundos.
    automatizable: true

  # ── CATEGORÍA: Resiliencia ─────────────────────────────────────────
  - id: TC-025-05
    titulo: "Token expirado se renueva automáticamente y la búsqueda tiene éxito"
    tipo: resiliencia
    criterio_origen: AC-025-04
    historia_origen: US-052
    prioridad: alta
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
      - "Token OAuth2 expirado en el servidor (manipulado para el test)"
    mock_sistema_externo:
      secuencia:
        - endpoint: "GET /invoices"
          codigo_respuesta: 401
          cuerpo: '{"error": "UNAUTHORIZED"}'
        - endpoint: "POST /auth/token"
          codigo_respuesta: 200
          cuerpo: '{"access_token": "nuevo_token_xyz", "expires_in": 3600}'
        - endpoint: "GET /invoices"
          codigo_respuesta: 200
          cuerpo: "respuesta_normal_con_facturas"
    pasos:
      - numero: 1
        accion: "Ejecutar una búsqueda válida con el token expirado"
        resultado_esperado: "El indicador de carga aparece normalmente"
      - numero: 2
        accion: "Esperar la respuesta (incluye renovación de token)"
        resultado_esperado: >
          En menos de 8 segundos el listado muestra las facturas correctamente.
          El usuario no ve ningún mensaje de error de autenticación.
          No hay interrupciones visibles en la experiencia.
    automatizable: true

  - id: TC-025-06
    titulo: "Rate limit con Retry-After provoca espera automática y éxito"
    tipo: resiliencia
    criterio_origen: AC-025-05
    historia_origen: US-052
    prioridad: alta
    precondiciones:
      - "Usuario autenticado con rol gestor_facturacion"
    mock_sistema_externo:
      secuencia:
        - endpoint: "GET /invoices"
          codigo_respuesta: 429
          headers:
            Retry-After: "5"
        - endpoint: "GET /invoices"
          codigo_respuesta: 200
          cuerpo: "respuesta_normal_con_facturas"
    pasos:
      - numero: 1
        accion: "Ejecutar una búsqueda válida"
        resultado_esperado: "El indicador de carga permanece visible"
      - numero: 2
        accion: "Esperar 6 segundos (5s de espera + procesamiento)"
        resultado_esperado: >
          El listado muestra las facturas correctamente.
          No aparece ningún mensaje de error.
          El indicador de carga estuvo visible durante los 5+ segundos de espera.
    automatizable: true
```

---

## Gestión de la incertidumbre residual en Jira

Cuando el requisito tiene incertidumbres menores que no bloquean el desarrollo pero sí pueden afectar a detalles de implementación, estas se representan en Jira como tareas de tipo Spike vinculadas a la historia.

La historia generada por el pipeline incluye en su descripción una sección específica:

```
## Incertidumbres conocidas y decisiones provisionales

⚠ [PENDIENTE DE DECISIÓN — IB-01]
El estado DISPUTED del ERP no tiene equivalente en nuestro modelo de datos.
Decisión provisional: mapear a "pendiente" hasta que el equipo de negocio
confirme el tratamiento definitivo.
Contacto para resolución: Product Owner + Ana López (Dirección Financiera)
Plazo: 2025-05-15
Impacto si cambia: actualizar el mapeo de estados en el cliente ERP
y regenerar los test cases TC-025-02 y TC-025-06.

ℹ [DECISIÓN PROVISIONAL — IM-01]
El campo supplier_ref puede estar ausente en facturas antiguas.
Tratamiento: dejar referencia_proveedor en blanco si el campo no viene.
Esta decisión no requiere validación adicional a menos que el negocio indique lo contrario.
```

---

## Arquitectura documental para integraciones

Los requisitos de integración amplían la arquitectura documental del modelo operativo con dos nuevas carpetas:

```
repositorio-funcional/
│
├── contratos-api/                     # Nuevo: contratos de sistemas externos
│   ├── erp-sap-financiero/
│   │   ├── contrato_v1.yaml           # Contrato en vigor
│   │   ├── contrato_v2-draft.yaml     # Próxima versión (si aplica)
│   │   ├── changelog.md               # Historial de cambios del contrato
│   │   └── sandbox-config.yaml        # Configuración de entorno de pruebas
│   └── pasarela-pagos/
│       └── ...
│
├── analisis-incertidumbre/            # Nuevo: plantillas por requisito
│   ├── REQ-025-incertidumbre.yaml
│   └── ...
│
├── requisitos/
│   └── EP-04/
│       ├── REQ-023.yaml               # Requisito funcional estándar
│       └── REQ-025.yaml               # Requisito de integración (plantilla extendida)
│
└── pipelines/
    ├── validate-requisitos.py
    ├── generate-jira-issues.py
    ├── generate-test-cases.py
    └── validate-contrato-api.py       # Nuevo: verifica que el contrato sigue vigente
```

### Script de validación de contratos

La vigencia del contrato de API debe verificarse periódicamente porque el sistema externo puede cambiar sin que el equipo lo sepa. Este script forma parte del pipeline de validación:

```python
# validate-contrato-api.py
"""
Verifica que el contrato de API documentado sigue siendo válido
comparando la especificación guardada con la versión actual del sistema externo.
Se ejecuta: manualmente antes de iniciar una nueva épica de integración
            y automáticamente en el pipeline CI cada lunes.
"""

import yaml
import requests
import json
from datetime import datetime

def validar_contrato(ruta_contrato: str, config: dict) -> dict:
    """
    Compara el contrato guardado con el estado actual del sistema externo.
    No verifica la lógica de negocio, solo la disponibilidad de endpoints
    y la estructura de respuesta de los campos críticos.
    """
    with open(ruta_contrato) as f:
        contrato = yaml.safe_load(f)

    resultado = {
        "contrato": ruta_contrato,
        "fecha_verificacion": datetime.now().isoformat(),
        "sistema": contrato["sistema_externo"]["nombre"],
        "operaciones_verificadas": [],
        "discrepancias": [],
        "estado": "VALIDO"
    }

    token = obtener_token(contrato["sistema_externo"], config)

    for operacion in contrato.get("operaciones_relevantes", []):
        if operacion.get("metodo", "GET") != "GET":
            # Solo verificar operaciones de lectura para no generar efectos secundarios
            continue

        verificacion = verificar_operacion(
            operacion=operacion,
            base_url=contrato["sistema_externo"]["entorno_sandbox"],
            token=token
        )
        resultado["operaciones_verificadas"].append(verificacion)

        if verificacion.get("discrepancias"):
            resultado["discrepancias"].extend(verificacion["discrepancias"])
            resultado["estado"] = "DISCREPANCIAS_DETECTADAS"

    return resultado

def verificar_operacion(operacion: dict, base_url: str, token: str) -> dict:
    """
    Llama al endpoint con parámetros mínimos de prueba y verifica
    que los campos críticos siguen presentes en la respuesta.
    """
    # Construir la petición con valores de prueba seguros
    params_prueba = {
        p["nombre"]: p.get("valor_prueba_por_defecto", _valor_por_defecto(p["tipo"]))
        for p in operacion.get("parametros", [])
        if p.get("requerido", False)
    }

    try:
        response = requests.get(
            f"{base_url}{operacion['endpoint']}",
            params=params_prueba,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        verificacion = {
            "operacion": operacion["id"],
            "endpoint": operacion["endpoint"],
            "codigo_respuesta": response.status_code,
            "discrepancias": []
        }

        if response.status_code != operacion["respuesta_exitosa"]["codigo_http"]:
            verificacion["discrepancias"].append({
                "tipo": "codigo_respuesta_inesperado",
                "esperado": operacion["respuesta_exitosa"]["codigo_http"],
                "obtenido": response.status_code,
                "severidad": "bloqueante"
            })
            return verificacion

        # Verificar que los campos marcados como siempre_presente siguen estándolo
        if response.status_code == 200:
            try:
                datos = response.json()
                primer_elemento = datos.get("data", [{}])[0] if datos.get("data") else {}

                for campo in operacion["respuesta_exitosa"].get("campos_factura", []):
                    if campo.get("siempre_presente") and campo["nombre"] not in primer_elemento:
                        verificacion["discrepancias"].append({
                            "tipo": "campo_critico_ausente",
                            "campo": campo["nombre"],
                            "mapeo_interno": campo.get("mapeo_interno"),
                            "severidad": "bloqueante",
                            "mensaje": f"El campo '{campo['nombre']}' ya no está presente en la respuesta"
                        })
            except Exception:
                pass  # No hay datos de muestra para verificar, solo disponibilidad

        return verificacion

    except requests.exceptions.Timeout:
        return {
            "operacion": operacion["id"],
            "endpoint": operacion["endpoint"],
            "discrepancias": [{
                "tipo": "timeout",
                "mensaje": "El sistema externo no respondió en 10 segundos",
                "severidad": "bloqueante"
            }]
        }

def _valor_por_defecto(tipo: str) -> str:
    defaults = {
        "string": "test",
        "integer": "1",
        "date": "2024-01-01",
        "boolean": "true"
    }
    return defaults.get(tipo, "test")
```

---

## Errores más frecuentes en requisitos de integración

Estos patrones aparecen sistemáticamente en proyectos que no tienen un flujo específico para integraciones. El validador del pipeline (punto 6 del modelo operativo) debe incluir estas reglas adicionales para los requisitos con bloque `integracion_externa`.

**Flujos de error del sistema externo documentados como "N/A"** o simplemente ausentes. El analista escribe solo el flujo feliz asumiendo que el sistema externo siempre funciona. El resultado es que el desarrollador implementa el manejo de errores según su criterio, produciendo mensajes inconsistentes, estados vacíos confusos y bugs silenciosos cuando el sistema externo falla.

**Criterios de aceptación que no son testables sin el sistema externo real**. Un criterio que dice "el sistema devuelve las facturas del ERP" no puede verificarse sin acceso al ERP. Los test cases deben estar diseñados con mocks que simulen el comportamiento del sistema externo, no dependiendo de su disponibilidad.

**Datos de entrada y salida copiados directamente del contrato externo sin mapeo**. El analista escribe `invoice_id` y `total_amount` en el requisito porque así los llama el ERP, pero el sistema interno los llama `id_factura` e `importe_total`. El equipo de desarrollo trabaja con terminología mezclada, produciendo código inconsistente.

**No documentar los comportamientos no documentados del sistema externo**. Si se descubre que el ERP devuelve 200 con array vacío para rangos invertidos en lugar del esperado 400, eso debe quedar en el contrato y en el requisito. Si no se documenta, el siguiente analista o desarrollador que trabaje con ese sistema asume un comportamiento que no es real.

**Tiempo de respuesta del sistema externo ignorado**. El requisito define el tiempo de respuesta de la pantalla sin tener en cuenta que el sistema externo tiene su propio SLA. Si el ERP tarda 800ms en responder y el requisito exige 1 segundo de tiempo de respuesta total, hay un problema de diseño que nadie detecta hasta llegar a producción.

**Incertidumbres no explicitadas que se convierten en decisiones silenciosas**. El analista no sabe cómo tratar el estado DISPUTED y no lo documenta. El desarrollador implementa algo razonable pero incorrecto. El bug llega a producción cuando el negocio ve por primera vez una factura en ese estado.

---

## Integración con el glosario del modelo operativo

Los contratos de API introducen terminología del sistema externo que debe integrarse en el glosario del proyecto con cuidado. La regla es que el glosario siempre contiene el término oficial del dominio de negocio, no el nombre técnico del campo externo.

```yaml
# Extensión del glosario para la integración con el ERP

entidades:
  - id: ENT-003
    nombre_oficial: "Factura"    # Ya existe en el glosario
    mapeo_sistemas_externos:     # Nuevo campo en la entidad
      - sistema: "ERP-SAP Financiero"
        nombre_en_sistema: "invoice"
        campos:
          id_factura: invoice_id
          fecha_factura: invoice_date
          importe_total: total_amount
          estado: status
          referencia_proveedor: supplier_ref
        transformaciones:
          estado:
            PENDING: pendiente
            APPROVED: aprobada
            PAID: pagada
            CANCELLED: rechazada
            DISPUTED: pendiente    # Decisión provisional IB-01
        notas: >
          Los campos de fecha del ERP vienen en formato ISO-8601 con timezone UTC.
          Convertir a date local (Europe/Madrid) antes de persistir o mostrar.
          El campo total_amount puede ser negativo (facturas de abono).
```

Esta extensión permite que la IA, al generar artefactos para requisitos de integración, utilice el término interno correcto en las historias y el término externo correcto en las tareas técnicas, sin que el analista tenga que especificarlo explícitamente en cada requisito.

---

## Checklist de validación específico para integraciones

Este checklist se añade al validador automático del punto 6 del modelo operativo cuando el requisito contiene el campo `integracion_externa`.

```yaml
checklist_validacion_integracion:

  contrato_disponible:
    descripcion: "Existe un archivo de contrato referenciado y accesible"
    severidad: BLOQUEANTE
    regla: "contrato_referencia existe en /contratos-api/"

  operacion_identificada:
    descripcion: "La operacion_principal del contrato está identificada"
    severidad: BLOQUEANTE
    regla: "operacion_principal no está vacía"

  flujos_error_cubiertos:
    descripcion: >
      Por cada código de error documentado en el contrato, existe al menos
      una excepción documentada en el requisito
    severidad: BLOQUEANTE
    regla: "len(excepciones) >= len(codigos_error_contrato)"

  timeout_documentado:
    descripcion: "El comportamiento ante timeout está documentado en las excepciones"
    severidad: BLOQUEANTE
    regla: "existe excepcion con 'timeout' o 'no responde' en condicion"

  mapeo_campos_completo:
    descripcion: >
      Todos los campos marcados como siempre_presente en el contrato
      tienen su correspondencia en datos_salida del requisito
    severidad: BLOQUEANTE

  patron_resiliencia_definido:
    descripcion: "Se ha definido al menos la política de timeout y el comportamiento ante error 500"
    severidad: BLOQUEANTE

  incertidumbres_bloqueantes_resueltas:
    descripcion: "No existen incertidumbres_bloqueantes en estado 'pendiente'"
    severidad: BLOQUEANTE
    regla: "todas las IB tienen estado != 'pendiente'"

  sandbox_disponible:
    descripcion: "Existe un entorno de sandbox para pruebas de integración"
    severidad: ADVERTENCIA
    accion_si_falta: >
      Documentar cómo se probarán los test cases de integración
      si no hay sandbox disponible (mocks, grabaciones de tráfico, etc.)

  tiempo_respuesta_realista:
    descripcion: >
      El tiempo de respuesta máximo definido en el requisito es mayor que
      el SLA p95 del sistema externo más un margen de 20%
    severidad: ADVERTENCIA
```

---

> Este documento complementa los puntos 1–12 del Modelo Operativo de Análisis Funcional AI-Ready.
> Se integra con: plantilla YAML base (punto 1), glosario estructurado (punto 2),
> prompts de generación de artefactos Jira (punto 4), generación de test cases (punto 5),
> validación automática (punto 6) y arquitectura documental (punto 11).
