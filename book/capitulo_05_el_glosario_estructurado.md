# Capítulo 5. El glosario estructurado

*La terminología que no se gobierna, divide al equipo.*

---

Era la segunda reunión de refinamiento del sprint y Carlos llevaba diez minutos en silencio, mirando la historia que tenía en pantalla. La historia decía «el cliente podrá consultar sus facturas pendientes». El desarrollador preguntó qué era exactamente un cliente en ese contexto. Ana López, desde finanzas, respondió que un cliente era cualquier empresa que tuviera crédito activo. María García, desde desarrollo, señaló que en el sistema había una tabla llamada «usuarios» y otra llamada «cuentas», y que ninguna se llamaba «clientes». David Sanz añadió que él había entendido que «cliente» se refería a los contactos externos del CRM.

Cuatro personas. Cuatro definiciones distintas del mismo término. Y una historia que llevaba dos semanas en el backlog sin que nadie hubiera detectado el problema.

Carlos cerró el portátil. Tenía que hablar de algo que ninguno de ellos había construido todavía: un glosario. No una lista de definiciones en un documento Word que nadie consulta, sino una fuente de autoridad terminológica que el pipeline de IA pudiera usar como contexto en cada llamada, y que el validador automático pudiera cruzar con el texto de cada requisito antes de que llegara al sprint.

Ese glosario es el tema de este capítulo.

---

**En este capítulo aprenderás a:**

- Entender por qué el glosario es el componente más subestimado del modelo y el que más impacto tiene en la calidad del output del pipeline.
- Diseñar la estructura de un glosario AI-ready con actores, entidades, acciones, eventos y reglas globales.
- Construir el glosario desde cero usando los documentos existentes de tu organización, sin partir de una hoja en blanco.
- Inyectar el glosario como contexto en el pipeline de forma eficiente, sin desperdiciar tokens.
- Gobernar el glosario para que no se degrade con el tiempo.

---

## Por qué el glosario cambia las reglas del juego

En un proyecto tradicional, el glosario es un documento de referencia que alguien crea al inicio del proyecto con buenas intenciones y que nadie consulta a partir del segundo sprint. Si aparece una duda terminológica, la resuelve la persona más veterana del equipo, que da la definición correcta de memoria. Si esa persona está de vacaciones, el desarrollador adivina.

En un modelo AI-ready, el glosario tiene un papel radicalmente distinto: es contexto activo que se inyecta en cada llamada al pipeline de generación y validación. No es un documento que la gente consulta cuando tiene dudas. Es un archivo que la IA lee antes de escribir cualquier línea.

Eso cambia todo. Porque si el glosario dice que el término oficial es «gestor de facturación» y el analista escribe «operador financiero» en un requisito, el validador lo detecta antes de que el requisito entre al pipeline. Y si llega al pipeline, la historia generada usará «gestor de facturación» en todos sus campos, no el sinónimo que usó el analista.

> 💡 **El glosario hace tres cosas simultáneamente**
>
> **Normalización terminológica:** cuando el requisito dice «cliente» y el glosario dice que el término oficial es «usuario autenticado», la historia generada usa «usuario autenticado» en todos sus campos. Sin que el analista tenga que recordarlo.
>
> **Desambiguación semántica:** el término «pedido» puede significar cosas distintas en el módulo de ventas y en el de logística. El glosario le dice a la IA cuál es la definición vigente en cada contexto.
>
> **Detección de inconsistencias:** el validador automático cruza el vocabulario del requisito contra el glosario y marca los sinónimos no oficiales como un problema antes de que entren al pipeline.

En Meridian, el problema de la reunión de Carlos no era que el equipo fuera impreciso. Era que no existía ninguna fuente de autoridad a la que remitirse. Cuando el glosario existe y está bien construido, la respuesta a «¿qué es un cliente?» no la da la persona más veterana de la sala: la da el documento, que fue validado con el negocio en su momento y registrado como decisión.

---

## Anatomía del glosario AI-ready

Un glosario AI-ready no es una lista de definiciones en Word ni una tabla en Confluence con dos columnas. Tiene estructura semántica explícita organizada en cinco tipos de elemento: actores, entidades, acciones, eventos y reglas globales. Cada tipo tiene un propósito distinto y la IA los procesa de formas diferentes.

### Actores: los roles que ejecutan las acciones

Un actor es el rol específico que ejecuta una acción en el sistema. No es una persona: es un rol que puede ser desempeñado por distintas personas. La distinción es importante porque los permisos, los flujos y las restricciones se definen sobre roles, no sobre individuos.

El error más frecuente es definir actores demasiado genéricos. Si el sistema tiene tres tipos de usuario con comportamientos distintos, son tres actores distintos en el glosario. «El usuario» no sirve. La IA no puede generar permisos correctos ni el desarrollador puede implementar restricciones de acceso con un actor tan ambiguo.

| ❌ Incorrecto | ✅ Correcto |
|---|---|
| el usuario | Gestor de facturación |
| el cliente | Usuario autenticado con rol consultor_externo |
| el administrador | Administrador del sistema (acceso completo a configuración) |

Para cada actor, el glosario documenta cuatro cosas: el nombre oficial, los sinónimos no permitidos, una descripción de sus responsabilidades y sus permisos clave sobre el sistema. Esta información es lo que permite a la IA generar historias con el actor correcto y al validador detectar cuando se usa un sinónimo no oficial.

En Meridian, el proceso de alineación terminológica reveló que el equipo usaba «gestor», «operador financiero» y «usuario de facturación» para referirse exactamente al mismo rol. Desde que el glosario existe, hay un único término oficial y el pipeline genera siempre el mismo nombre en todas las historias del módulo.

### Entidades: los objetos de negocio sobre los que se opera

Una entidad es el objeto de negocio sobre el que actúan los actores. En el módulo de facturación de Meridian, las entidades principales son «Factura» y «Proveedor». El glosario documenta para cada entidad sus atributos clave, los estados por los que puede pasar y las reglas de transición entre estados.

Los estados y sus transiciones son especialmente valiosos para el pipeline. Cuando la IA conoce el ciclo de vida completo de una entidad, puede generar criterios de aceptación que cubren todas las transiciones de estado posibles, no solo el flujo feliz. Y el equipo de QA recibe test cases que verifican que una factura no puede pasar directamente de «pendiente» a «pagada» sin pasar por «aprobada».

> 💡 **El modelo de estados es la pieza más valiosa del glosario**
>
> Cuando el glosario tiene documentados los estados de una entidad y sus transiciones permitidas, el pipeline puede generar automáticamente criterios de aceptación para cada transición. Y el validador puede detectar si un requisito propone una transición que el modelo de estados no permite.
>
> Sin el modelo de estados, la IA genera historias que asumen que cualquier estado puede pasar a cualquier otro. En producción, eso se traduce en bugs de lógica de negocio que son difíciles de reproducir y costosos de diagnosticar.

El ejemplo de la entidad «Factura» en Meridian ilustra bien la diferencia entre una entidad bien y mal documentada. La versión mal documentada dice: «Una factura tiene un número, una fecha y un importe». La versión bien documentada incluye los seis estados posibles, las transiciones permitidas entre ellos, quién puede ejecutar cada transición y qué condiciones deben cumplirse.

### Acciones: los verbos que describen lo que hacen los actores

Las acciones son los verbos del dominio. Definirlas en el glosario evita que el mismo concepto aparezca con diez verbos distintos en documentos distintos. En Meridian, el proceso de auditoría terminológica encontró «buscar», «consultar», «listar», «filtrar» y «visualizar» usados de forma intercambiable para referirse a operaciones que en realidad tienen semánticas distintas.

| Acción oficial | Sinónimos no permitidos | Distinción importante |
|---|---|---|
| filtrar | buscar, consultar, listar | Filtrar implica criterios estructurados. Buscar implica texto libre. Son operaciones distintas. |
| exportar | descargar, extraer, sacar | Exportar genera un archivo. Reportar genera un documento formateado. No son sinónimos. |
| aprobar | validar, confirmar, autorizar | En Meridian, aprobar es una acción con flujo de escalado para importes > 10.000 €. Los sinónimos no llevan esa connotación. |
| archivar | eliminar, borrar, inactivar | Archivar conserva el registro en solo lectura. Eliminar lo destruye. La diferencia tiene implicaciones legales en un contexto financiero. |

Cuando el pipeline conoce estas distinciones, genera historias con el verbo preciso. Cuando el validador las conoce, detecta si un requisito usa «buscar» donde debería decir «filtrar» y alerta al analista antes de que la ambigüedad llegue al desarrollo.

### Eventos: los hechos de negocio que desencadenan comportamientos

Los eventos vienen directamente del Event Storming que describimos en el capítulo siguiente. Son los hechos que han ocurrido en el sistema y que desencadenan otros comportamientos. «Factura recibida», «Factura aprobada», «Pago ejecutado» son eventos del dominio de Meridian.

El glosario documenta para cada evento quién lo desencadena, qué consecuencias tiene y a qué módulo pertenece. Esta información es la que conecta el mapa del Event Storming con los campos `evento_disparador` de la plantilla YAML que vimos en el capítulo anterior. Cuando el glosario tiene los eventos bien definidos, el analista no tiene que inventar la descripción del evento disparador: existe en el glosario y puede referenciarlo directamente.

### Reglas globales: las restricciones que aplican a todo el proyecto

Las reglas globales son restricciones que no pertenecen a un módulo específico sino a todo el sistema. En Meridian, hay tres reglas globales que aplican a cualquier requisito de cualquier módulo: la zona horaria del sistema es Europe/Madrid con almacenamiento en UTC, las sesiones expiran tras treinta minutos de inactividad, y todos los datos personales se tratan según el RGPD.

Estas reglas se inyectan en todos los prompts del pipeline, siempre. No requieren que el analista las recuerde ni las incluya en cada requisito. La IA las tiene en cuenta automáticamente al generar los artefactos.

> 🛠️ **En la práctica: las reglas globales son las más difíciles de documentar**
>
> Las reglas de negocio específicas de un módulo son fáciles de identificar: emergen en los workshops con los usuarios. Las reglas globales son más elusivas porque nadie las menciona explícitamente: están tan asumidas que nadie las dice en voz alta.
>
> La forma más efectiva de identificarlas es preguntar en el taller: «¿Hay algo que sea cierto para absolutamente todo lo que hace el sistema, independientemente del módulo?». Las respuestas suelen revelar exactamente las reglas que nadie había documentado nunca.

---

## El glosario de Meridian: un ejemplo real

Para hacer concreto lo anterior, veamos el fragmento del glosario de Meridian correspondiente al módulo de Facturación. Este es el mismo glosario que Carlos Ruiz construyó tras la reunión que abrió este capítulo. No está completo, pero ilustra el nivel de detalle que hace que el pipeline funcione correctamente.

```yaml
# glosario.yaml — Módulo EP-04 Gestión de Facturación
# Propietario: Carlos Ruiz (analista líder)
# Validado con: Ana López (Dir. Financiera) — 2025-05-10

actores:
  - id: ACT-001
    nombre_oficial: "Gestor de facturación"
    descripcion: >
      Empleado del área financiera con acceso completo al módulo de
      facturación. Puede consultar, filtrar, exportar y archivar
      facturas. No puede aprobar facturas superiores a 10.000€.
    sinonimos_no_oficiales:
      - "operador financiero"
      - "usuario de facturación"
      - "gestor"       # demasiado genérico
    permisos_clave:
      - "Consultar y filtrar facturas"
      - "Exportar listados a CSV y XLSX"
      - "Archivar facturas en estado pagada"

  - id: ACT-002
    nombre_oficial: "Responsable financiero"
    descripcion: >
      Directivo con permisos de aprobación sobre facturas superiores
      a 10.000€ y sobre operaciones de anulación.
    sinonimos_no_oficiales:
      - "director financiero"
      - "aprobador"
    permisos_clave:
      - "Aprobar y rechazar facturas (sin límite de importe)"
      - "Anular facturas emitidas"

entidades:
  - id: ENT-001
    nombre_oficial: "Factura"
    descripcion: >
      Documento fiscal recibido de un proveedor. En este proyecto,
      "factura" siempre se refiere a facturas recibidas, nunca emitidas.
    sinonimos_no_oficiales:
      - "albarán"    # INCORRECTO: el albarán es un documento de entrega
      - "recibo"     # INCORRECTO: el recibo es el justificante de pago
      - "documento"  # AMBIGUO: demasiado genérico
    atributos_clave:
      - { nombre: id_factura,    tipo: string,  descripcion: "Formato: FACT-YYYYNNNNN" }
      - { nombre: fecha_factura, tipo: date,    descripcion: "Fecha de emisión. ISO-8601" }
      - { nombre: importe_total, tipo: decimal, descripcion: "Con impuestos. Moneda: EUR" }
      - { nombre: estado,        tipo: enum,
          valores: [pendiente, en-revision, aprobada, rechazada, pagada, archivada] }
    estados:
      - nombre: pendiente
        transiciones_permitidas: [en-revision, rechazada]
      - nombre: en-revision
        transiciones_permitidas: [aprobada, rechazada]
      - nombre: aprobada
        transiciones_permitidas: [pagada]
      - nombre: rechazada
        transiciones_permitidas: [pendiente]   # puede reiniciarse el proceso
      - nombre: pagada
        transiciones_permitidas: [archivada]
      - nombre: archivada
        transiciones_permitidas: []             # estado final, solo lectura
    reglas_negocio_asociadas:
      - "Facturas > 10.000€ requieren aprobación del Responsable financiero"
      - "El rechazo requiere siempre una nota de motivo (mínimo 20 caracteres)"

acciones:
  - id: ACC-001
    verbo_oficial: "filtrar"
    descripcion: >
      Reducir el conjunto de registros visibles aplicando uno o más criterios
      sobre los atributos de las entidades. El filtrado no elimina registros,
      solo restringe los visibles en la sesión actual.
    sinonimos_no_oficiales:
      - "buscar"     # buscar implica texto libre; filtrar implica criterios estructurados
      - "consultar"  # consultar es más amplio; filtrar es una operación específica
      - "listar"     # listar es mostrar sin criterios; filtrar implica criterios aplicados

  - id: ACC-002
    verbo_oficial: "exportar"
    descripcion: >
      Generar un archivo descargable con el contenido de un listado.
      La exportación no modifica los registros del sistema.
      Formatos soportados: CSV, XLSX, PDF.
    sinonimos_no_oficiales:
      - "descargar"
      - "extraer"

eventos:
  - id: EVT-001
    nombre_oficial: "Factura recibida"
    descripcion: >
      Evento que ocurre cuando la organización recibe una nueva factura
      de un proveedor, ya sea por correo, integración EDI o carga manual.
    consecuencias:
      - "Se crea un registro de Factura en estado 'pendiente'"
      - "Se notifica al Gestor de facturación asignado"
      - "Se inicia el contador de SLA de revisión (72h laborables)"

  - id: EVT-002
    nombre_oficial: "Factura aprobada"
    descripcion: >
      Evento que ocurre cuando el Gestor de facturación (o el Responsable
      financiero para importes superiores al umbral) valida una factura.
    consecuencias:
      - "La factura pasa a estado 'aprobada'"
      - "Se programa el pago según las condiciones del proveedor"
      - "Se notifica al área de tesorería"

reglas_globales:
  - id: RG-001
    descripcion: >
      Zona horaria Europe/Madrid. Almacenamiento en UTC.
      Mostrar convertido a la zona horaria del usuario.
  - id: RG-002
    descripcion: >
      Sesión expira tras 30 minutos de inactividad.
      Redirección a login con mensaje de aviso.
  - id: RG-003
    descripcion: >
      Datos personales tratados según RGPD.
      Base legal requerida para cualquier campo de datos personales.
```

> ⚠️ **El error más frecuente: definiciones circulares**
>
> «Una factura es un documento de facturación.» Esta definición no le dice nada a la IA que pueda usar para generar artefactos correctos. La definición debe decir qué es la entidad, para qué sirve y en qué se distingue de conceptos similares.
>
> **Mal:** «Un proveedor es una entidad proveedora de bienes o servicios.»
>
> **Bien:** «Persona jurídica o física que emite facturas a la organización. En este módulo, el proveedor debe existir en el catálogo antes de que pueda asociarse a una factura nueva. No confundir con cliente, que es la entidad a la que la organización emite facturas —módulo separado, fuera de alcance en este proyecto—.»

---

## Cómo se inyecta el glosario en el pipeline

El glosario no se vuelca completo en cada llamada al pipeline. Un glosario maduro puede tener doscientos términos, y pasar todos al contexto del LLM consumiría demasiados tokens y degradaría la calidad de la respuesta. La estrategia es la inyección selectiva: antes de cada llamada, el sistema extrae solo los términos del glosario relevantes para el requisito que se está procesando.

La lógica es sencilla: si el requisito menciona «factura» (o cualquiera de sus sinónimos), se inyecta la definición completa de la entidad Factura. Si menciona «gestor de facturación» (o cualquier sinónimo), se inyecta la definición del actor. Las reglas globales y las abreviaturas se inyectan siempre, en todos los requisitos, porque son contexto transversal.

> 📋 **Prompt — Bloque de glosario inyectado en el sistema**
>
> Este es el formato compacto que el sistema inyecta antes de cada llamada de generación. Ocupa aproximadamente 300 tokens frente a los 2.000–3.000 del YAML completo. La diferencia escala significativamente cuando se procesan requisitos en lote.
>
> ```
> ═══════════════════════════════════════════════
> GLOSARIO APLICABLE A ESTE REQUISITO
> ═══════════════════════════════════════════════
> ACTORES OFICIALES (usar el nombre exacto siempre):
> ▸ "Gestor de facturación" [NO: usuario, operador, gestor]
>   → Empleado financiero. Puede filtrar y exportar facturas.
>   → NO puede aprobar facturas superiores a 10.000€.
>
> ▸ "Responsable financiero" [NO: director, aprobador]
>   → Aprueba facturas y configura umbrales de importe.
>
> ENTIDADES OFICIALES:
> ▸ "Factura" [NO: albarán, recibo, documento]
>   → Documento fiscal de proveedor.
>   → Estados: pendiente → en-revision → aprobada → pagada → archivada
>   → Regla: importes > 10.000€ requieren Responsable financiero.
>
> ACCIONES OFICIALES:
> ▸ "filtrar" [NO: buscar, consultar, listar]
>   → Reducir registros visibles por criterios estructurados.
>
> REGLAS GLOBALES (aplican a todos los requisitos):
> ▸ Zona horaria Europe/Madrid. Almacenamiento en UTC.
> ▸ Sesión expira tras 30 min. → redirección a login.
> ▸ Datos personales: tratamiento según RGPD.
> ═══════════════════════════════════════════════
> ```

Este bloque es lo que el pipeline pasa como contexto de sistema antes de llamar al LLM con el requisito. Con él, la IA sabe exactamente qué términos son oficiales, cuáles están prohibidos y qué restricciones aplican, sin necesidad de deducirlo del texto del requisito.

---

## Cómo construir el glosario desde cero

El glosario no se construye en una sala de reuniones con el equipo técnico. Se extrae de donde vive el conocimiento real: en los documentos existentes y en las conversaciones con el negocio. El proceso tiene cuatro pasos que, en total, requieren entre cuatro y seis horas distribuidas en una semana.

### Paso 1 — Minería de documentos existentes (1-2 horas)

Antes de hablar con nadie, el analista dedica una o dos horas a revisar los últimos cinco a diez documentos funcionales del equipo buscando inconsistencias terminológicas. El indicador más claro es encontrar el mismo concepto con nombres distintos en documentos distintos.

El resultado típico de este ejercicio es sorprendente incluso para equipos veteranos. En Meridian, la auditoría reveló que el concepto equivalente a «factura» aparecía como «factura», «documento fiscal», «documento de proveedor» y «factura de compra» en cuatro documentos distintos del mismo proyecto. Ninguno de los analistas era consciente de la inconsistencia porque cada uno había trabajado en módulos distintos.

El patrón que buscamos en esa revisión es siempre el mismo:

```
APARECE SIEMPRE (pero con nombres distintos):
  - El mismo objeto de negocio llamado de tres formas diferentes
  - El mismo rol con dos nombres que nadie distingue

APARECE A VECES (según quién redactó el documento):
  - Verbos que deberían ser sinónimos pero se usan indistintamente

NUNCA APARECE (pero todo el mundo lo asume):
  - Las restricciones tan obvias que nadie escribe
  - Los estados intermedios de las entidades principales
```

### Paso 2 — Taller de alineación terminológica (2 horas)

Una sesión con negocio, analistas y técnicos donde se presentan las inconsistencias encontradas y el grupo decide el término oficial para cada concepto. La regla es que el término oficial lo elige el negocio, no el técnico. Si el negocio llama «factura» a lo que el sistema llama «invoice», el término oficial es «factura».

La dinámica más eficaz es mostrar pares de términos y hacer una única pregunta: «¿Son lo mismo o son cosas distintas?». Si son lo mismo, uno es sinónimo no oficial del otro y el grupo decide cuál es el término canónico. Si son distintos, ambos entran en el glosario con sus definiciones propias.

> 🛠️ **En la práctica: los debates son el output más valioso del taller**
>
> Cuando dos personas del grupo no se ponen de acuerdo sobre si dos términos son lo mismo, eso no es un problema del taller: es el taller haciendo su trabajo. Esa desalineación existía antes del taller; el taller simplemente la hace visible.
>
> No intentes resolver el debate en la sala si no hay consenso. Registra la pregunta abierta, asigna un responsable de resolverla con el área de negocio correcta y continúa. Un taller que termina con diez preguntas abiertas bien identificadas es más valioso que uno que termina con diez definiciones acordadas sin rigor.

### Paso 3 — Definición de atributos y estados (1-2 horas por entidad principal)

Para cada entidad identificada, el analista entrevista al usuario de negocio con un guión de preguntas fijas que producen directamente los campos del glosario. No es una conversación abierta: es una entrevista estructurada que sigue siempre el mismo orden.

| Pregunta de la entrevista | Campo del glosario que produce |
|---|---|
| ¿Qué información tiene siempre una [entidad]? | `atributos_clave → requerido: true` |
| ¿Qué información puede o no puede tener? | `atributos_clave → requerido: false` |
| ¿En qué situaciones puede estar una [entidad]? | `estados` (listado) |
| ¿Cuándo pasa de un estado a otro? ¿Quién lo decide? | `estados → transiciones_permitidas` |
| ¿Puede una [entidad] volver a un estado anterior? | Transiciones de retorno en el modelo de estados |
| ¿Qué cosas no puede hacer el sistema con una [entidad] según las reglas del negocio? | `reglas_negocio_asociadas` |

### Paso 4 — Revisión y aprobación formal

El glosario completo se presenta al product owner o responsable de negocio para aprobación. Esta aprobación no es un trámite: es el acto que convierte el glosario en un documento de autoridad. Cuando en el futuro haya discusión sobre un término durante el desarrollo, el glosario resuelve la disputa sin necesidad de convocar una reunión.

La diferencia entre un glosario aprobado formalmente y uno que «todo el mundo usa porque parece razonable» se manifiesta en el momento en que alguien cuestiona una definición. Si hay un registro de aprobación, la discusión termina. Si no lo hay, empieza una reunión que dura una hora y no llega a ninguna conclusión.

---

## Gobierno del glosario

El glosario tiene valor solo si se mantiene actualizado. Un glosario desactualizado es peor que no tenerlo, porque la IA genera artefactos incorrectos con confianza. No como el analista que adivina con duda, sino como el sistema que afirma con certeza.

El modelo de gobierno más ligero que funciona en la práctica tiene tres elementos: un propietario único, un proceso de cambio de tres pasos y una revisión periódica programada.

### Propietario único

El analista líder del proyecto es el único que puede hacer cambios en el glosario. Cualquier miembro del equipo puede proponer cambios, pero solo el propietario los aprueba y los aplica. Sin propietario único, el glosario se fragmenta en pocas semanas: cada analista añade los términos que necesita para su módulo sin coordinación, y el resultado es un documento lleno de sinónimos oficiales contradictorios.

### Proceso de cambio en tres pasos

Cuando alguien detecta un término que falta o una definición incorrecta, el proceso es siempre el mismo: primero se abre una incidencia con la propuesta y el motivo; el propietario la revisa con el área de negocio afectada; si se aprueba, se actualiza el glosario, se incrementa el número de versión menor y se notifica al equipo. Los cambios que afectan a términos usados en requisitos ya validados requieren revisar esos requisitos.

Este proceso parece burocrático para un documento tan técnico, pero la burocracia ligera es lo que distingue un glosario vivo de uno que muere de éxito: primero todo el mundo lo usa, luego todo el mundo lo modifica a su gusto, y el resultado es un documento que ya no es fuente de autoridad sino una colección de versiones contradictorias de la misma verdad.

### Revisión periódica

Cada dos sprints, el propietario dedica treinta minutos a revisar el glosario buscando términos que hayan aparecido en conversaciones recientes sin estar recogidos. Al inicio de cada nueva épica, se revisa el glosario completo con el negocio para añadir los términos específicos del nuevo módulo.

La señal de alarma más clara de que el glosario necesita revisión no es que alguien lo diga: es que el validador automático del pipeline empieza a detectar un número creciente de términos no oficiales en los requisitos. Cuando la tasa de detección de sinónimos no oficiales supera el veinte por ciento de los requisitos procesados, hay términos del dominio que no están en el glosario.

---

## Los diez errores que matan un glosario

Estos son los patrones más frecuentes que hacen que un glosario deje de funcionar a los tres meses. No son errores teóricos: son los que aparecen en casi todos los proyectos que intentan construir un glosario por primera vez.

1. **Definiciones circulares.** «Una factura es un documento de facturación.» No dice nada que la IA pueda usar. La definición debe decir qué es, para qué sirve y en qué se distingue de conceptos similares.

2. **Sinónimos no documentados.** Si el glosario dice que el término oficial es «usuario autenticado» pero no lista «cliente», «usuario registrado» y «cuenta» como sinónimos no permitidos, el validador no puede detectar cuando aparecen en un requisito.

3. **Actores demasiado genéricos.** Un actor llamado «usuario» no sirve. Si el sistema tiene tres tipos de usuario con comportamientos distintos, son tres actores distintos.

4. **Estados sin transiciones.** Documentar que una factura puede estar «pendiente», «aprobada» o «pagada» sin documentar quién puede hacer cada transición y bajo qué condiciones genera requisitos contradictorios en módulos distintos.

5. **Entidades sin atributos.** Una entidad sin atributos clave no puede generar casos de prueba con datos concretos. La IA inventa valores cuando no tiene referencia.

6. **Reglas de negocio en el glosario en lugar de en los requisitos.** El glosario documenta qué son las cosas. Las reglas sobre cómo funcionan van en los requisitos. Mezclar ambos hace el glosario inmanejable y duplica información que después se contradice.

7. **Glosario sin propietario.** En dos meses tiene trescientos términos contradictorios porque cada analista añadió los suyos sin coordinación.

8. **Términos técnicos mezclados con términos de negocio.** «JWT», «endpoint», «webhook» no son términos del glosario de negocio. Van en la documentación técnica. El glosario es para el lenguaje que usan negocio y analistas.

9. **No revisar el glosario al iniciar una nueva épica.** Cada módulo introduce términos nuevos. Si no se recogen a tiempo, los primeros requisitos del módulo usan vocabulario inventado que se propaga a todos los artefactos.

10. **Glosario en un formato que nadie consulta.** Si vive en un Word en una carpeta de red, nadie lo usa. Si está en Confluence enlazado desde la plantilla de requisito, se consulta constantemente.

---

## Lo que funciona en la práctica

La teoría del glosario es clara. La práctica tiene matices que dependen del contexto de cada equipo. Estos son los que aparecen más frecuentemente en las primeras semanas de implantación.

El glosario mínimo viable no necesita estar completo antes de empezar a usar el pipeline. Basta con tener documentados los actores principales y las entidades del módulo piloto. El glosario se completa progresivamente a medida que el pipeline detecta términos no oficiales en los requisitos. Cada detección es una señal de que falta un elemento, no un fallo del sistema.

En la práctica, el glosario más útil no es el más completo sino el más preciso. Veinte términos bien definidos con sus sinónimos no permitidos producen más valor que doscientos términos con definiciones de dos líneas que no distinguen conceptos similares. La profundidad importa más que la amplitud.

El taller de alineación terminológica no necesita durar dos horas si el equipo ya tiene documentación existente. En algunos proyectos, el analista puede construir un borrador del glosario en solitario a partir de los documentos existentes y presentarlo al negocio para validación en una sesión de cuarenta y cinco minutos. El taller completo es para proyectos sin documentación previa o con terminología muy inconsistente.

El glosario no solo sirve al pipeline. Sirve también al equipo técnico para nombrar correctamente las tablas y campos de la base de datos, al equipo de QA para escribir los tests con el vocabulario adecuado y a los usuarios de negocio para validar que el sistema usa los términos que ellos reconocen. Un glosario bien construido es, además del contexto de la IA, el documento de referencia del proyecto para todo el equipo. Eso lo hace especialmente fácil de vender: no es una herramienta para el pipeline, es una herramienta para todos.

---

## Tres puntos clave

**1.** El glosario no es una lista de definiciones: es el contrato terminológico del proyecto, y el pipeline de IA lo usa como contexto activo en cada llamada. Sin él, la IA genera artefactos técnicamente correctos pero terminológicamente inconsistentes entre sí.

**2.** Un glosario AI-ready tiene cinco tipos de elemento: actores, entidades, acciones, eventos y reglas globales. El modelo de estados de las entidades es la pieza más valiosa porque permite detectar transiciones imposibles antes de que lleguen al código.

**3.** El glosario mínimo viable —actores y entidades del módulo piloto con sus sinónimos no permitidos— es suficiente para empezar. La completitud llega con el uso: cada detección del validador automático de un término no oficial es una señal de que falta un elemento en el glosario.

---

> 💡 **Pregunta de reflexión para tu equipo**
>
> Si tu equipo tuviera que ponerse de acuerdo ahora mismo sobre qué es exactamente un «cliente» en vuestro sistema, ¿tardaríais menos de cinco minutos o necesitaríais una reunión? Si la respuesta es la segunda opción, tenéis un glosario pendiente de construir.

---

Con la plantilla del requisito AI-ready (Capítulo 4) y el glosario estructurado (este capítulo) tienes los dos cimientos que necesita el pipeline para funcionar. La plantilla define cómo se escribe cada requisito. El glosario define con qué vocabulario se escribe.

Pero ambos cimientos se construyen desde algún punto de partida. Ese punto de partida es el workshop de descubrimiento: la sesión con los usuarios de negocio donde se identifican los eventos del dominio, los actores, las reglas y los problemas que hay que resolver. El siguiente capítulo describe cómo facilitarlo.
