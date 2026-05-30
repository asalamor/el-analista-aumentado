# Punto 2 — Glosario estructurado

## Por qué el glosario es diferente en un contexto AI-ready

En un proyecto tradicional, el glosario es un documento de referencia que la gente consulta cuando tiene dudas. Útil, pero pasivo.

En un modelo AI-ready, el glosario es **contexto activo**: se inyecta como parte del system prompt en cada llamada al pipeline. La IA lo usa para tres cosas distintas simultáneamente.

La primera es **normalización terminológica**: cuando el requisito dice "cliente" y el glosario dice que el término oficial es "usuario autenticado", la historia generada usa "usuario autenticado", no "cliente". Así todas las historias del proyecto comparten el mismo vocabulario sin que el analista tenga que recordarlo.

La segunda es **desambiguación semántica**: el término "pedido" puede significar cosas distintas en el módulo de ventas y en el módulo de logística. El glosario le dice a la IA cuál es la definición vigente en cada contexto del proyecto.

La tercera es **detección de inconsistencias**: el validador del punto 6 cruza el vocabulario del requisito contra el glosario. Si encuentra sinónimos no oficiales, los marca como problema antes de que entren al pipeline.

---

## Anatomía del glosario estructurado

Un glosario AI-ready no es una lista de definiciones en Word. Tiene estructura semántica explícita con campos que la IA puede procesar de forma determinista.

```yaml
# glosario.yaml
# Documento de autoridad terminológica del proyecto
# Gobierno: el analista líder actualiza, el product owner aprueba
# Versión: 1.0 — Fecha: 2025-05-06

metadata:
  proyecto: ""
  version: "1.0"
  propietario: ""           # Quién aprueba cambios
  fecha_ultima_revision: "" # YYYY-MM-DD
  proxima_revision: ""      # Fecha de revisión periódica programada

actores:
  # Los actores son los roles que aparecen en las historias de usuario.
  # Cada actor tiene un nombre oficial único. Todos los demás son sinónimos no permitidos.
  - id: ACT-001
    nombre_oficial: "Gestor de facturación"
    descripcion: >
      Empleado del área financiera con acceso completo al módulo de facturación.
      Puede consultar, filtrar, exportar y archivar facturas. No puede emitir
      ni anular facturas sin aprobación del Responsable financiero.
    sinonimos_no_oficiales:
      - "usuario de facturación"
      - "operador financiero"
      - "gestor"
    permisos_clave:
      - "Consultar facturas"
      - "Filtrar y exportar facturas"
      - "Archivar facturas"
    sistemas_que_usa:
      - "Módulo de Facturación"
      - "Módulo de Reporting"
    notas: >
      Distinguir del Responsable financiero, que tiene permisos adicionales
      de aprobación y anulación.

  - id: ACT-002
    nombre_oficial: "Responsable financiero"
    descripcion: >
      Directivo del área financiera con permisos de aprobación sobre operaciones
      iniciadas por el Gestor de facturación. Recibe notificaciones automáticas
      cuando se supera el umbral de importe definido en la configuración.
    sinonimos_no_oficiales:
      - "director financiero"
      - "aprobador"
      - "validador"
    permisos_clave:
      - "Aprobar y rechazar facturas"
      - "Anular facturas emitidas"
      - "Configurar umbrales de aprobación"
    sistemas_que_usa:
      - "Módulo de Facturación"
      - "Módulo de Aprobaciones"
    notas: ""

entidades:
  # Las entidades son los objetos de negocio sobre los que operan los actores.
  # Cada entidad tiene un nombre oficial, sus atributos clave y sus estados posibles.
  - id: ENT-001
    nombre_oficial: "Factura"
    descripcion: >
      Documento fiscal que registra una transacción comercial entre la organización
      y un proveedor o cliente. En el contexto de este proyecto, factura hace siempre
      referencia a facturas recibidas de proveedores, no a facturas emitidas a clientes.
    sinonimos_no_oficiales:
      - "albarán"       # INCORRECTO: el albarán es un documento de entrega, no fiscal
      - "recibo"        # INCORRECTO: el recibo es el justificante de pago
      - "documento"     # AMBIGUO: demasiado genérico
    atributos_clave:
      - nombre: "id_factura"
        tipo: string
        descripcion: "Identificador único. Formato: FACT-YYYYNNNNN"
      - nombre: "fecha_factura"
        tipo: date
        descripcion: "Fecha de emisión del documento por el proveedor. ISO-8601."
      - nombre: "fecha_recepcion"
        tipo: date
        descripcion: "Fecha en que la organización recibe la factura. Puede diferir de fecha_factura."
      - nombre: "importe_total"
        tipo: decimal
        descripcion: "Importe total con impuestos incluidos. Moneda: EUR."
      - nombre: "estado"
        tipo: enum
        valores: ["pendiente", "en-revision", "aprobada", "rechazada", "pagada", "archivada"]
      - nombre: "proveedor"
        tipo: referencia
        entidad_referenciada: ENT-002
    estados:
      - nombre: "pendiente"
        descripcion: "Factura recibida, pendiente de revisión"
        transiciones_permitidas: ["en-revision", "rechazada"]
      - nombre: "en-revision"
        descripcion: "Factura en proceso de validación por el gestor"
        transiciones_permitidas: ["aprobada", "rechazada"]
      - nombre: "aprobada"
        descripcion: "Factura validada, pendiente de pago"
        transiciones_permitidas: ["pagada"]
      - nombre: "rechazada"
        descripcion: "Factura no aceptada. Requiere nota de rechazo."
        transiciones_permitidas: ["pendiente"]
      - nombre: "pagada"
        descripcion: "Pago registrado en el sistema"
        transiciones_permitidas: ["archivada"]
      - nombre: "archivada"
        descripcion: "Factura en archivo histórico. Solo lectura."
        transiciones_permitidas: []
    reglas_negocio_asociadas:
      - "Una factura solo puede archivarse si está en estado pagada"
      - "El rechazo requiere siempre una nota de motivo de al menos 20 caracteres"
      - "Las facturas superiores a 10.000€ requieren aprobación del Responsable financiero"

  - id: ENT-002
    nombre_oficial: "Proveedor"
    descripcion: >
      Persona jurídica o física que emite facturas a la organización.
      En el módulo de facturación, el proveedor es siempre una entidad
      ya registrada en el sistema. No se pueden registrar facturas de
      proveedores no existentes en el catálogo.
    sinonimos_no_oficiales:
      - "vendedor"
      - "suministrador"
      - "acreedor"
    atributos_clave:
      - nombre: "id_proveedor"
        tipo: string
        descripcion: "Identificador interno. Formato: PROV-NNNNN"
      - nombre: "razon_social"
        tipo: string
      - nombre: "cif"
        tipo: string
        descripcion: "Identificador fiscal. Validación: formato NIF/CIF español"
      - nombre: "activo"
        tipo: boolean
        descripcion: "Solo los proveedores activos pueden asociarse a nuevas facturas"
    notas: >
      Distinguir de 'cliente', que es la entidad a la que la organización emite facturas.
      En este proyecto, el módulo de clientes es un sistema separado fuera del alcance.

acciones:
  # Las acciones son los verbos que describen lo que los actores hacen con las entidades.
  # Definirlas evita que el mismo concepto aparezca con diez verbos distintos.
  - id: ACC-001
    verbo_oficial: "filtrar"
    descripcion: >
      Reducir el conjunto de registros visibles aplicando uno o más criterios
      sobre los atributos de las entidades. El filtrado no elimina registros,
      solo restringe los visibles en la sesión actual.
    sinonimos_no_oficiales:
      - "buscar"      # buscar implica texto libre; filtrar implica criterios estructurados
      - "consultar"   # consultar es más amplio; filtrar es una operación específica
      - "listar"      # listar es mostrar sin criterios; filtrar implica criterios aplicados
    contexto_de_uso: "Módulo de Facturación, Módulo de Reporting"
    ejemplo_correcto: >
      "El gestor de facturación filtra las facturas por rango de fechas
       y estado para preparar el cierre mensual."

  - id: ACC-002
    verbo_oficial: "exportar"
    descripcion: >
      Generar un archivo descargable con el contenido de un listado o conjunto
      de registros. La exportación no modifica los registros del sistema.
      Formatos soportados: CSV, XLSX, PDF.
    sinonimos_no_oficiales:
      - "descargar"
      - "extraer"
      - "sacar"
    contexto_de_uso: "Cualquier módulo con listados paginados"
    nota_importante: >
      'Exportar' y 'reportar' son acciones distintas. Exportar genera un archivo
      con datos en bruto. Reportar genera un documento con formato y agregaciones.

eventos:
  # Los eventos son los hechos de negocio que desencadenan comportamientos.
  # Vienen del Event Storming y son la fuente de los eventos_disparador en los requisitos.
  - id: EVT-001
    nombre_oficial: "Factura recibida"
    descripcion: >
      Evento que ocurre cuando la organización recibe una nueva factura de un proveedor,
      ya sea por correo electrónico, por integración EDI o por carga manual en el sistema.
    disparado_por:
      - "Integración automática con el buzón de facturas"
      - "Carga manual por parte del Gestor de facturación"
      - "Integración EDI con proveedores homologados"
    consecuencias:
      - "Se crea un registro de Factura en estado 'pendiente'"
      - "Se notifica al Gestor de facturación asignado"
      - "Se inicia el contador de SLA de revisión (72h laborables)"
    modulo: "EP-04 Gestión de Facturación"

  - id: EVT-002
    nombre_oficial: "Factura aprobada"
    descripcion: >
      Evento que ocurre cuando el Gestor de facturación (o el Responsable financiero
      para importes superiores al umbral) valida una factura pendiente de revisión.
    disparado_por:
      - "Acción manual de aprobación por el Gestor de facturación"
      - "Acción manual de aprobación por el Responsable financiero"
    consecuencias:
      - "La factura pasa a estado 'aprobada'"
      - "Se programa el pago según las condiciones del proveedor"
      - "Se notifica al área de tesorería"
    modulo: "EP-04 Gestión de Facturación"

reglas_globales:
  # Restricciones que aplican a todo el proyecto, no a un módulo específico.
  # Se inyectan en todos los prompts del pipeline.
  - id: RG-001
    descripcion: >
      Todos los datos personales se tratan según el RGPD.
      Ningún requisito puede contemplar el almacenamiento de datos personales
      sin que exista una base legal documentada y aprobada por el DPO.
    afecta_a: "todos los módulos"

  - id: RG-002
    descripcion: >
      El sistema opera en zona horaria Europe/Madrid.
      Todas las fechas y horas se almacenan en UTC y se muestran convertidas
      a la zona horaria del usuario según su configuración de perfil.
    afecta_a: "todos los módulos con campos de fecha o datetime"

  - id: RG-003
    descripcion: >
      El acceso a cualquier módulo requiere autenticación activa.
      Una sesión inactiva durante más de 30 minutos se cierra automáticamente.
      El usuario es redirigido a la pantalla de login con el mensaje
      'Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.'
    afecta_a: "todos los módulos"

abreviaturas:
  # Siglas y acrónimos usados en el proyecto. La IA las expande al generar artefactos.
  - sigla: "AC"
    expansion: "Criterio de Aceptación (Acceptance Criterion)"
  - sigla: "EP"
    expansion: "Épica"
  - sigla: "REQ"
    expansion: "Requisito"
  - sigla: "US"
    expansion: "Historia de Usuario (User Story)"
  - sigla: "TC"
    expansion: "Caso de Prueba (Test Case)"
  - sigla: "DoD"
    expansion: "Definición de Terminado (Definition of Done)"
  - sigla: "NFR"
    expansion: "Requisito No Funcional (Non-Functional Requirement)"
  - sigla: "SLA"
    expansion: "Acuerdo de Nivel de Servicio (Service Level Agreement)"
```

---

## Cómo se inyecta el glosario en el pipeline

El glosario no se pasa completo en cada llamada. Un glosario de proyecto maduro puede tener 200 términos y consumir demasiados tokens. La estrategia es una **inyección selectiva por contexto**:

```python
def construir_contexto_glosario(requisito_yaml, glosario_completo):
    """
    Extrae solo los términos del glosario relevantes para el requisito.
    Reduce el consumo de tokens en un 70-80% respecto a inyectar el glosario completo.
    """
    terminos_relevantes = {
        "actores": [],
        "entidades": [],
        "acciones": [],
        "eventos": [],
        "reglas_globales": glosario_completo["reglas_globales"],  # Siempre se inyectan
        "abreviaturas": glosario_completo["abreviaturas"]          # Siempre se inyectan
    }

    # Extraer texto completo del requisito para buscar menciones
    texto_requisito = extraer_texto_completo(requisito_yaml)

    # Buscar actores mencionados (nombre oficial o sinónimo)
    for actor in glosario_completo["actores"]:
        todos_los_nombres = [actor["nombre_oficial"]] + actor["sinonimos_no_oficiales"]
        if any(nombre.lower() in texto_requisito.lower() for nombre in todos_los_nombres):
            terminos_relevantes["actores"].append(actor)

    # Buscar entidades mencionadas
    for entidad in glosario_completo["entidades"]:
        todos_los_nombres = [entidad["nombre_oficial"]] + entidad["sinonimos_no_oficiales"]
        if any(nombre.lower() in texto_requisito.lower() for nombre in todos_los_nombres):
            terminos_relevantes["entidades"].append(entidad)

    # Buscar acciones mencionadas
    for accion in glosario_completo["acciones"]:
        todos_los_verbos = [accion["verbo_oficial"]] + accion["sinonimos_no_oficiales"]
        if any(verbo.lower() in texto_requisito.lower() for verbo in todos_los_verbos):
            terminos_relevantes["acciones"].append(accion)

    return terminos_relevantes
```

El resultado se inyecta en el system prompt en este formato compacto:

```
GLOSARIO APLICABLE A ESTE REQUISITO:

ACTORES OFICIALES:
- "Gestor de facturación": empleado financiero con acceso completo al módulo.
  Sinónimos NO permitidos: usuario de facturación, operador financiero, gestor.

ENTIDADES OFICIALES:
- "Factura": documento fiscal de proveedor. Estados: pendiente → en-revision
  → aprobada → pagada → archivada.
  Sinónimos NO permitidos: albarán, recibo, documento.

ACCIONES OFICIALES:
- "filtrar": reducir registros visibles por criterios. Distinto de buscar (texto libre).
  Sinónimos NO permitidos: buscar, consultar, listar.

REGLAS GLOBALES (aplican siempre):
- Zona horaria: Europe/Madrid. Almacenamiento en UTC.
- Sesión expira tras 30 minutos de inactividad → redirección a login.
- Datos personales: tratamiento según RGPD. Base legal requerida.
```

Este bloque ocupa aproximadamente 300 tokens, frente a los 2.000-3.000 que ocuparía el YAML completo. La diferencia escala cuando se tienen 50 o 100 requisitos procesándose en batch.

---

## Cómo construir el glosario desde cero

El glosario no se diseña en una sala de reuniones con el equipo técnico. Se extrae de donde vive el conocimiento real: en los documentos existentes y en las conversaciones con el negocio. El proceso tiene cuatro pasos.

### Paso 1 — Minería de documentos existentes (1-2 horas)

Se analizan los últimos 5-10 documentos funcionales del equipo buscando inconsistencias terminológicas. El indicador más claro es encontrar el mismo concepto con nombres distintos en documentos distintos. Este paso se puede automatizar parcialmente:

```python
# Script de extracción de candidatos a glosario desde documentos existentes
from collections import Counter
import re

def extraer_candidatos_glosario(textos_documentos):
    """
    Extrae sustantivos frecuentes de un conjunto de documentos
    como candidatos a incluir en el glosario.
    """
    candidatos = Counter()

    for texto in textos_documentos:
        # Extraer sustantivos en mayúscula (probables términos de dominio)
        terminos = re.findall(r'\b[A-ZÁÉÍÓÚ][a-záéíóú]+(?:\s+[a-záéíóú]+)?\b', texto)
        candidatos.update(terminos)

    # Los más frecuentes son los mejores candidatos para el glosario
    return candidatos.most_common(50)
```

### Paso 2 — Workshop de alineación terminológica (2 horas)

Una sesión con negocio, analistas y técnicos donde se presentan las inconsistencias encontradas y el grupo decide el término oficial para cada concepto. La regla es que el término oficial lo elige el negocio, no el técnico.

La dinámica más eficaz es mostrar pares de términos y preguntar: "¿Son lo mismo o son cosas distintas?" Si son lo mismo, uno es sinónimo no oficial del otro. Si son distintos, ambos entran en el glosario con sus definiciones propias.

### Paso 3 — Definición de atributos y estados (1-2 horas por entidad principal)

Para cada entidad identificada, el analista entrevista al usuario de negocio con este guión de preguntas:

```
1. ¿Qué información tiene siempre una [entidad]?
2. ¿Qué información puede o no puede tener?
3. ¿En qué situaciones puede estar una [entidad]? (estados)
4. ¿Cuándo pasa de un estado a otro? ¿Quién lo decide?
5. ¿Puede una [entidad] volver a un estado anterior?
6. ¿Qué cosas no puede hacer el sistema con una [entidad] según las reglas del negocio?
```

Las respuestas a estas preguntas generan directamente los campos `atributos_clave`, `estados` y `reglas_negocio_asociadas` del glosario.

### Paso 4 — Revisión y aprobación formal

El glosario completo se presenta al product owner o responsable de negocio para aprobación. Esta aprobación convierte el glosario en un documento de autoridad: cuando haya discusión sobre un término durante el desarrollo, el glosario resuelve la disputa sin necesidad de convocar una reunión.

---

## Gobierno del glosario

El glosario tiene valor solo si se mantiene. Un glosario desactualizado es peor que no tenerlo porque la IA genera artefactos incorrectos con confianza.

El modelo de gobierno más ligero que funciona en la práctica es este:

**Propietario único.** El analista líder del proyecto es el único que puede hacer cambios en el glosario. Cualquier miembro del equipo puede proponer cambios, pero solo el propietario los aprueba y los aplica. Sin propietario único, el glosario se fragmenta.

**Proceso de cambio en tres pasos.** Cuando alguien detecta un término que falta o una definición incorrecta: primero abre una incidencia en Confluence o Jira con la propuesta; el propietario la revisa con el área de negocio afectada; si se aprueba, se actualiza el glosario, se incrementa la versión menor y se notifica al equipo. Los cambios que afectan a términos usados en requisitos ya validados requieren revisar esos requisitos.

**Revisión periódica.** Cada dos sprints, el propietario revisa el glosario durante 30 minutos buscando términos que hayan aparecido en conversaciones recientes sin estar recogidos. Al inicio de cada nueva épica, se revisa el glosario completo con el negocio para añadir los términos específicos del nuevo módulo.

**Versionado.** El glosario vive en Git junto a los requisitos. Cada cambio es un commit con mensaje descriptivo. El pipeline de validación usa siempre la versión etiquetada como estable, no la rama de desarrollo.

---

## Los diez errores más frecuentes al construir el glosario

**Definiciones circulares.** "Una factura es un documento de facturación." No dice nada que la IA pueda usar. La definición debe decir qué es, para qué sirve y en qué se distingue de conceptos similares.

**Sinónimos no documentados.** Si el glosario dice que el término oficial es "usuario autenticado" pero no lista "cliente", "usuario registrado" y "cuenta" como sinónimos no oficiales, el validador no puede detectar cuando aparecen en un requisito.

**Actores demasiado genéricos.** Un actor llamado "usuario" no sirve. Si el sistema tiene tres tipos de usuario con comportamientos distintos, son tres actores distintos en el glosario.

**Estados sin transiciones.** Documentar que una factura puede estar "pendiente", "aprobada" o "pagada" sin documentar quién puede hacer cada transición y bajo qué condiciones genera requisitos contradictorios en módulos distintos.

**Entidades sin atributos.** Una entidad sin atributos clave no puede generar casos de prueba con datos concretos. La IA inventa valores cuando no tiene referencia.

**Reglas de negocio en el glosario en lugar de en los requisitos.** El glosario documenta qué son las cosas. Las reglas sobre cómo funcionan van en los requisitos. Si mezclas ambos, el glosario se vuelve inmanejable y las reglas se duplican.

**Glosario que crece sin propietario.** En dos meses tiene 300 términos contradictorios entre sí porque cada analista añadió los suyos sin coordinación.

**Términos técnicos mezclados con términos de negocio.** "JWT", "endpoint", "webhook" no son términos del glosario de negocio. Van en la documentación técnica. El glosario es para el lenguaje que usan negocio y analistas.

**No revisar el glosario al iniciar una nueva épica.** Cada módulo nuevo introduce términos nuevos. Si no se recogen a tiempo, los primeros requisitos del módulo usan vocabulario inventado que se propaga a todos los artefactos.

**Glosario en un formato que nadie consulta.** Si vive en un Word compartido en una carpeta de red, nadie lo usa. Si está integrado en Confluence como referencia enlazada desde la plantilla de requisito, se consulta constantemente.

---

## Formato de inyección compacta para los prompts

Cuando el glosario se inyecta en los prompts de generación y validación, no se vuelca en YAML completo. Se usa este formato compacto que la IA procesa eficientemente:

```
═══════════════════════════════════════════════
GLOSARIO DEL PROYECTO — TÉRMINOS APLICABLES
═══════════════════════════════════════════════

ACTORES (usar el nombre oficial siempre):
▸ "Gestor de facturación" [NO: usuario, operador, gestor]
  → Empleado financiero. Puede filtrar, exportar y archivar facturas.
  → NO puede aprobar facturas superiores a 10.000€.

▸ "Responsable financiero" [NO: director, aprobador, validador]
  → Directivo financiero. Aprueba facturas y configura umbrales.

ENTIDADES (atributos y estados clave):
▸ "Factura" [NO: albarán, recibo, documento]
  → Estados: pendiente→en-revision→aprobada→pagada→archivada
  → Atributos clave: id_factura, fecha_factura, importe_total, estado, proveedor
  → Regla: importes >10.000€ requieren aprobación de Responsable financiero

▸ "Proveedor" [NO: vendedor, suministrador, acreedor]
  → Solo proveedores activos pueden asociarse a nuevas facturas

ACCIONES (usar el verbo oficial):
▸ "filtrar" [NO: buscar, consultar, listar]
  → Reducir registros visibles por criterios estructurados

▸ "exportar" [NO: descargar, extraer]
  → Generar archivo descargable. Formatos: CSV, XLSX, PDF

REGLAS GLOBALES (aplican a todo el proyecto):
▸ Zona horaria: Europe/Madrid. Almacenamiento en UTC.
▸ Sesión expira tras 30 min de inactividad → redirección a login.
▸ Datos personales: tratamiento según RGPD. Base legal requerida.
═══════════════════════════════════════════════
```

Este bloque ocupa aproximadamente 300 tokens frente a los 2.000-3.000 que ocuparía el YAML completo. La diferencia escala cuando se tienen 50 o 100 requisitos procesándose en batch.

---

## Métricas de madurez del glosario

Para saber si el glosario está cumpliendo su función, estas son las métricas que se pueden medir en el pipeline:

**Tasa de detección de sinónimos no oficiales.** Porcentaje de requisitos en los que el validador detecta al menos un término no oficial del glosario. Al inicio de un proyecto es normal que sea alto (30-50%). Debe caer por debajo del 10% tras dos meses de uso.

**Cobertura de actores.** Porcentaje de actores que aparecen en los requisitos y que están definidos en el glosario. Debe ser del 100%. Cualquier actor no definido es un riesgo de implementación incorrecta de permisos.

**Cobertura de entidades.** Porcentaje de entidades mencionadas en los requisitos que tienen sus estados y atributos documentados en el glosario. El objetivo es 100% para las entidades del dominio principal.

**Frecuencia de actualización.** Número de cambios al glosario por sprint. Demasiados cambios (más de 5 por sprint) indican que el glosario se construyó demasiado deprisa sin validación real con el negocio. Ningún cambio durante varios sprints seguidos indica que probablemente hay términos nuevos que no se están recogiendo.
