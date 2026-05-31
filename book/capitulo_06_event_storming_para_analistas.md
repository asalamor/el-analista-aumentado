# Capítulo 6. Event Storming para analistas

*El conocimiento del negocio existe. El problema es que nadie lo ha articulado todavía.*

---

Carlos llegó a la sala con un rotulador negro, un rollo de papel de embalar y seis bloques de post-its de colores. Ana López lo miró con curiosidad. «¿No traes el portátil?», preguntó. «Hoy no», dijo Carlos. «Hoy lo hacemos con las manos.»

Llevaban tres semanas intentando arrancar la definición funcional del nuevo módulo de gestión de pagos a proveedores. Las reuniones de requisitos habían producido cuarenta páginas de notas, tres documentos Word parcialmente contradictorios y la sensación colectiva de que cuanto más hablaban, menos entendían. El problema no era que Ana no supiera explicar su proceso. El problema era que el formato de la reunión —alguien pregunta, alguien responde, alguien toma notas— no era el adecuado para capturar un proceso tan interconectado como ese.

Carlos pegó el papel en la pared. Destapó el rotulador. Y dijo la frase que siempre usa para empezar: «Escribid en post-its naranjas todo lo que ocurre en este proceso. Un evento por post-it. En pasado. No os coordinéis.»

Lo que ocurrió en las dos horas siguientes transformó las cuarenta páginas de notas en un mapa que todo el equipo podía leer, discutir y validar. Y al salir de la sala, Carlos tenía exactamente la materia prima que necesitaba para rellenar la plantilla YAML del capítulo anterior.

Eso es el Event Storming. Y ese es el tema de este capítulo.

---

**En este capítulo aprenderás a:**

- Entender qué es el Event Storming y por qué es la técnica de descubrimiento más eficaz para proyectos donde se va a usar el pipeline de IA.
- Preparar y facilitar un taller de Event Storming de nivel Process Level con usuarios de negocio no técnicos.
- Usar el código de colores del Event Storming para producir exactamente los elementos que necesita la plantilla YAML.
- Traducir el mapa resultante del taller a los campos del requisito AI-ready sin perder información.
- Evitar los cinco errores más frecuentes del facilitador novel.

---

## Qué es el Event Storming y por qué es el punto de partida correcto

Event Storming es una técnica de descubrimiento colaborativo creada por Alberto Brandolini que permite mapear un dominio de negocio complejo en pocas horas, con todos los actores relevantes en la misma sala, usando solo post-its de colores y una superficie grande. No requiere conocimiento técnico previo. El usuario de negocio trabaja en su propio lenguaje. El analista estructura lo que emerge.

La razón por la que es el punto de partida correcto para este modelo no es que sea una técnica elegante o moderna. Es una razón muy práctica: el Event Storming produce exactamente los elementos que necesita la plantilla YAML que describimos en el Capítulo 4.

Al final de un taller bien facilitado, el analista tiene sobre la mesa los eventos de negocio que se convierten en el campo `evento_disparador` de cada requisito, los actores que se convierten en el campo `actor`, los comandos que se convierten en el `cuando` de los criterios de aceptación, y las políticas que se convierten en `reglas_negocio`. La plantilla no es un formulario que se rellena después del workshop: es la traducción directa de lo que el Event Storming produce.

> 💡 **El Event Storming como puente entre el negocio y el pipeline**
>
> La mayoría de técnicas de captura de requisitos producen texto narrativo que el analista tiene que estructurar después. El Event Storming produce directamente los elementos semánticos —eventos, actores, comandos, políticas— que el pipeline de IA necesita para generar artefactos de calidad. El trabajo de traducción al YAML se reduce drásticamente porque ambas cosas hablan el mismo lenguaje.

Hay una segunda razón, igual de práctica: el Event Storming involucra a los usuarios de negocio de una forma que las reuniones de requisitos tradicionales no consiguen. En una reunión convencional, la persona más habladora domina la conversación y el conocimiento de los demás queda oculto. En un Event Storming, todos escriben simultáneamente y en silencio durante la primera fase. El conocimiento de la persona más callada tiene el mismo peso que el de la más locuaz.

---

## Los tres niveles del Event Storming

No todos los talleres son iguales. Hay tres niveles de profundidad y el analista debe elegir el correcto según el objetivo de la sesión.

**Big Picture Event Storming.** Para proyectos nuevos o módulos que nadie ha documentado antes. Dura entre cuatro y ocho horas. El objetivo es entender el dominio completo: qué ocurre, en qué orden, quién lo hace y dónde están los problemas. Produce el mapa completo de eventos que luego se agrupan en épicas. Es el punto de partida cuando no existe ninguna documentación previa.

**Process Level Event Storming.** Para módulos ya identificados que se van a implementar en el próximo trimestre. Dura entre dos y cuatro horas. El objetivo es detallar un proceso concreto hasta el nivel de comandos, actores y políticas. Produce los requisitos listos para convertirse en YAML. Este es el nivel que usará el analista funcional en la mayoría de sus proyectos.

**Design Level Event Storming.** Para el equipo técnico, antes del desarrollo. El objetivo es diseñar los agregados y los contextos delimitados del sistema. Produce decisiones de arquitectura, no requisitos funcionales. Está fuera del alcance de este capítulo.

Para la mayoría de los proyectos, el analista facilitará el **Process Level** porque el Big Picture ya se hizo al inicio del proyecto o al definir la hoja de ruta. Todo lo que sigue en este capítulo se refiere a ese nivel.

---

## El código de colores: el lenguaje visual del taller

El Event Storming usa un código de colores que todos los participantes deben conocer antes de empezar. Cinco minutos de explicación al inicio del taller son suficientes. No hace falta que los participantes memoricen nada: el código estará visible en la sala durante toda la sesión.

| Color | Elemento | Pregunta que responde | Ejemplo en Meridian |
|---|---|---|---|
| 🟠 Naranja | Evento de negocio | ¿Qué ha ocurrido? (en pasado) | «Factura recibida» |
| 🔵 Azul | Comando | ¿Qué desencadena ese evento? <br>(en imperativo) | «Registrar factura» |
| 🟡 Amarillo pálido | Actor | ¿Quién ejecuta el comando? | «Gestor de facturación» |
| 🟣 Lila / morado | Política | ¿Qué regla provoca que este evento <br>dispare este comando? | «Si importe > 10.000€, notificar <br>al Responsable financiero» |
| 🩷 Rosa | Punto de dolor | ¿Qué no funciona bien aquí? | «No sabemos qué facturas están <br>pendientes sin revisar el correo» |
| 🟢 Verde | Vista / read model | ¿Qué información necesita <br>el actor para decidir? | «Listado de facturas pendientes <br>con importe y proveedor» |
| 🔴 Rojo | Pregunta abierta | ¿Qué no sabemos todavía? | «¿Cuál es el plazo máximo de revisión?» |

La regla de oro del código de colores es que los post-its naranjas son la espina dorsal del taller. Todo lo demás se construye alrededor de ellos. Si el facilitador nota que el grupo está poniendo pocos post-its naranjas, hay que parar y redirigir.

> ⚠️ **El error del facilitador novel: mezclar colores desde el principio**
>
> La tentación en los primeros talleres es pedir a los participantes que escriban todos los colores a la vez. El resultado es un caos ingobernable. El taller funciona en fases: primero solo naranjas, luego azules, luego amarillos, etc. Cada color en su momento y sobre la base del anterior.

---

## Preparación del taller

La calidad del workshop depende en un setenta por ciento de la preparación. Un taller mal preparado produce mapas confusos que el analista no puede traducir a requisitos. Estos son los elementos que hay que tener listos antes de que llegue el primer participante.

### El espacio

Una pared o superficie continua de al menos cuatro metros de longitud. El rollo de papel de embalar pegado a la pared funciona perfectamente y es la solución más económica. Si el taller es remoto, Miro o FigJam con una plantilla de Event Storming preconfigurada. En remoto, todos los participantes deben tener cámara encendida y acceso de edición al tablero.

El espacio no es un detalle menor. Un Event Storming en una sala pequeña con participantes apretados alrededor de una mesa no funciona. El movimiento físico —levantarse, caminar hacia la pared, pegar un post-it, alejarse para ver el conjunto— es parte del proceso cognitivo. Cuando el espacio lo impide, el pensamiento se vuelve más estrecho.

### Los materiales

Post-its de los siete colores del código visual, rotuladores negros gruesos para que la letra se lea desde lejos, y cinta de carrocero para delimitar zonas del lienzo. Nunca usar bolígrafo: la letra no se ve desde más de un metro. Nunca usar post-its pequeños: es imposible leerlos en el mapa completo.

### El grupo

El grupo ideal tiene entre seis y diez personas. Más pequeño y falta perspectiva. Más grande y es ingobernable. Los perfiles imprescindibles son al menos dos usuarios de negocio que conozcan el proceso en profundidad, el product owner o quien toma decisiones de alcance, y el analista que facilitará.

Opcionales pero recomendables: un desarrollador senior para detectar restricciones técnicas relevantes y un representante de QA para hacer preguntas sobre los casos de error. No invitar a directivos que no participan en el proceso: su presencia inhibe a los usuarios de negocio.

### El brief previo

Dos días antes del taller, el analista envía un mensaje de no más de diez líneas que explica el objetivo de la sesión, el proceso que se va a mapear y el resultado esperado. Nada más. Si se comparte demasiado contexto previo, los participantes llegan con ideas preconcebidas que bloquean el descubrimiento.

```
Hola a todos,

El próximo martes haremos una sesión de tres horas para mapear juntos
el proceso de aprobación y pago de facturas de proveedor, desde que
recibimos la factura hasta que se registra el pago.

El objetivo es identificar qué ocurre exactamente en ese proceso, quién
hace qué y dónde están los problemas actuales.

No hace falta preparar nada. Solo vuestro conocimiento del proceso.

Nos vemos el martes a las 10:00 en la sala Proyecto.
```

---

## El flujo del taller paso a paso

Un taller de Process Level bien estructurado dura tres horas. Esta es la distribución que funciona en la práctica, con los tiempos exactos para un facilitador que lo hace por primera vez.

### Fase 1 — Introducción y caos creativo (40 minutos)

**Primeros diez minutos: explicar el código de colores.** El facilitador explica el sistema de colores con un ejemplo real del dominio del proyecto, no con un ejemplo genérico. En Meridian, Carlos no explica que «los post-its naranjas son eventos»: dice «escribid cosas como "Factura recibida" o "Pago ejecutado" —cosas que ocurren en el proceso de gestión de facturas».

**Treinta minutos: caos creativo.** El facilitador lanza la primera instrucción: «Escribid en post-its naranjas todo lo que ocurre en este proceso. Un evento por post-it. Usad el pasado. No os coordinéis entre vosotros todavía.»

Los participantes escriben en silencio durante veinte minutos. El resultado es un caos de post-its naranjes distribuidos aleatoriamente por el lienzo. Eso es exactamente lo que debe ocurrir. El caos inicial es la señal de que el grupo está volcando su conocimiento sin filtros.

El facilitador no participa en la escritura durante esta fase. Su rol es observar, asegurarse de que todos escriben —los más callados necesitan a veces un empujón suave— y capturar en un cuaderno privado las primeras señales de conflicto: dos personas que escriben el mismo evento con nombres distintos, eventos que nadie escribe pero que el facilitador sabe que existen, zonas del proceso donde nadie pone post-its.

> 🛠️ **En la práctica: qué hacer con los participantes que no escriben**
>
> En casi todos los grupos hay una o dos personas que miran el lienzo sin escribir, esperando a ver qué hacen los demás. La intervención más eficaz no es pedirles que participen en voz alta —eso los presiona— sino acercarse y preguntarles en voz baja: «¿Qué es lo primero que pasa cuando llega una factura?». La respuesta suele ser el post-it que desbloqueará a esa persona durante el resto del taller.

### Fase 2 — Línea de tiempo (20 minutos)

El facilitador pide al grupo que ordene los eventos en el eje horizontal de izquierda a derecha siguiendo el orden temporal. La instrucción exacta es: «Moved los post-its para que el flujo se lea de izquierda a derecha. Lo que ocurre primero va a la izquierda.»

Esta fase es donde emergen los primeros conflictos productivos. Dos personas intentan poner el mismo evento en momentos distintos de la línea porque tienen perspectivas diferentes del proceso. El facilitador no resuelve el conflicto: lo señala con un post-it rojo de pregunta abierta y continúa. Los conflictos se resuelven con las personas correctas, no con el grupo completo en caliente.

El resultado al final de esta fase es una línea de eventos naranjes ordenada cronológicamente con algunos huecos —eventos que faltan— y algunos grupos densos donde el proceso está bien conocido.

### Fase 3 — Añadir contexto (40 minutos)

Con la línea de tiempo estable, el facilitador añade las otras capas del modelo en un orden específico. El orden importa: cada capa enriquece la anterior sin interferir con ella.

**Comandos (azul).** Para cada evento naranja, el grupo identifica qué comando lo causó. La pregunta es: «¿Qué acción provocó que ocurriera este evento?» El comando se escribe en azul y se coloca justo antes del evento que causa. «Factura recibida» viene precedido del comando «Registrar factura en el sistema».

**Actores (amarillo).** Para cada comando, ¿quién lo ejecuta? El actor se coloca sobre el comando. Aquí es donde el glosario cobra valor: si el grupo empieza a usar «cliente», «usuario» y «comprador» para referirse a la misma persona, el facilitador interviene con el término oficial del glosario que construimos en el capítulo anterior.

**Políticas (lila).** Entre eventos y comandos, ¿hay alguna regla de negocio que determina qué ocurre? La política se escribe en lila y se coloca entre el evento que la activa y el comando que desencadena. «Si el importe supera los 10.000€, notificar al Responsable financiero» es una política que conecta el evento «Factura recibida» con el comando «Escalar a aprobación superior».

**Puntos de dolor (rosa).** El facilitador pregunta activamente: «¿Dónde os duele este proceso? ¿Qué es lento, confuso o propenso a errores?» Los puntos de dolor se convierten en el `objetivo_negocio` de los requisitos: explican por qué existe la necesidad de cambio. Sin ellos, los requisitos tienen estructura pero no tienen propósito de negocio visible.

**Preguntas abiertas (rojo).** Todo lo que el grupo no sabe todavía. Cada pregunta roja es un riesgo para el proyecto que necesita respuesta antes de que el analista pueda completar el requisito. «¿Cuál es el plazo máximo para aprobar una factura?» es una pregunta roja típica en Meridian.

> 💡 **Las políticas son el origen de las reglas de negocio**
>
> En la plantilla YAML, el campo `reglas_negocio` es uno de los más difíciles de rellenar porque las reglas de negocio rara vez se verbalizan de forma explícita: están en la cabeza de las personas que llevan años haciendo el proceso. El Event Storming las hace aflorar de forma natural porque el formato «si X ocurre, entonces Y» es exactamente cómo las políticas se expresan en el taller.

### Fase 4 — Identificar límites de dominio (15 minutos)

Con el mapa completo, el facilitador pide al grupo que identifique las zonas naturales del proceso: agrupaciones de eventos que tienen cohesión entre sí y que están separadas de otras agrupaciones. Estas zonas son las futuras épicas.

El facilitador dibuja líneas verticales con cinta de carrocero separando las zonas y el grupo les da un nombre. Ese nombre es el nombre de la épica y va al glosario como un término oficial. En Meridian, el mapa del módulo de pagos produjo tres épicas: «Recepción de facturas», «Revisión y aprobación» y «Proceso de pago».

```
│← EP-05 Recepción ──────────┤← EP-06 Revisión ──────────────┤← EP-07 Pago ─────────→│
│                            │                               │                       │
│ Factura recibida ────────→ │ Revisión iniciada ──────────→ │ Pago programado ────→ │
│ Proveedor notificado       │ Factura aprobada              │ Pago ejecutado        │
│                            │ Factura rechazada             │ Proveedor notificado  │
│                            │                               │                       │
│ Actor: Sistema             │ Actor: Gestor facturación     │ Actor: Tesorería      │
│ Actor: Proveedor           │ Actor: Resp. financiero       │ Actor: Sistema banco  │
```

### Fase 5 — Captura estructurada (30 minutos)

Esta es la fase que diferencia un Event Storming orientado al pipeline de uno convencional. Mientras el mapa todavía está visible y el grupo sigue en la sala, el analista traduce los elementos del mapa a los campos de la plantilla YAML en tiempo real.

La ventaja de hacerlo con el grupo presente es que las dudas se resuelven en el momento. El analista lee en voz alta lo que está escribiendo y el grupo confirma o corrige. Esto elimina la ambigüedad que se introduce cuando el analista transcribe el mapa en solitario horas o días después.

La tabla de traducción es siempre la misma:

| Elemento del mapa | Campo de la plantilla YAML |
|---|---|
| Post-it naranja (evento) | `evento_disparador` |
| Post-it azul (comando) | `cuando` en el criterio de aceptación |
| Post-it amarillo (actor) | `actor` |
| Post-it lila (política) | `reglas_negocio` |
| Post-it rosa (punto de dolor) | `objetivo_negocio` |
| Post-it verde (vista) | `datos_salida` |
| Post-it rojo (pregunta abierta) | Incertidumbre a resolver antes de validar el requisito |
| Agrupación de eventos | `epica` |

### Cierre del taller (15 minutos)

Los últimos quince minutos son para tres cosas: leer en voz alta las preguntas abiertas identificadas y asignar un responsable y un plazo a cada una, confirmar los nombres de las épicas con el group, y fotografiar el mapa completo antes de que nadie mueva nada.

El analista no desmonta el mapa al terminar. Lo deja físicamente intacto al menos cuarenta y ocho horas o, si es en Miro, exporta una versión de alta resolución antes de archivar el tablero. El mapa sin el contexto de las conversaciones pierde el cuarenta por ciento de la información. Las fotografías son la copia de seguridad de ese contexto.

---

## De la captura del taller al YAML de requisito

La captura del taller no es el requisito final. Es la materia prima que el analista transforma en los días siguientes en requisitos YAML completos. La traducción sigue un patrón sistemático que, con práctica, tarda entre treinta y sesenta minutos por requisito.

Un evento de negocio no siempre es un requisito. A veces un evento es el resultado de otro requisito. La regla práctica es simple: si el evento requiere que el sistema haga algo activamente, es un requisito. Si el evento simplemente ocurre como consecuencia de otro, es el resultado esperado de ese requisito.

Un comando con su actor y sus políticas es el núcleo de un requisito. Veamos la traducción concreta con un ejemplo del taller de Meridian:

```
CAPTURA DEL TALLER:
  Evento:    "Factura aprobada"
  Comando:   "Aprobar factura"
  Actor:     "Gestor de facturación"
  Política:  "Importes > 10.000€ requieren aprobación del Responsable financiero"
  Dolor:     "No hay trazabilidad de quién aprobó qué y cuándo"
  Vista:     "Detalle de factura con histórico de cambios de estado"

YAML RESULTANTE (campos clave):
  actor: "Gestor de facturación"
  evento_disparador: >
    El gestor accede a una factura en estado 'en-revision'
    para aprobarla tras verificar su contenido.
  reglas_negocio:
    - "Facturas con importe > 10.000€ no pueden ser aprobadas por el Gestor
       de facturación. Requieren aprobación del Responsable financiero."
    - "La aprobación queda registrada con fecha, hora y usuario."
  objetivo_negocio: >
    Eliminar la falta de trazabilidad sobre quién aprueba cada factura,
    reduciendo el tiempo de auditoría interna de horas a minutos.
  criterios_aceptacion:
    - id: AC-XXX-01
      dado: >
        El gestor está en el detalle de una factura en estado 'en-revision'
        con importe igual o inferior a 10.000€.
      cuando: "Pulsa el botón 'Aprobar'."
      entonces: >
        La factura cambia a estado 'aprobada'. Se registra la aprobación
        con el nombre del gestor, la fecha y la hora.
    - id: AC-XXX-02
      dado: >
        El gestor está en el detalle de una factura en estado 'en-revision'
        con importe superior a 10.000€.
      cuando: "Pulsa el botón 'Aprobar'."
      entonces: >
        El sistema muestra el mensaje 'Esta factura requiere aprobación del
        Responsable financiero'. El estado de la factura no cambia.
```

La política se convierte en dos criterios de aceptación —el flujo normal y la excepción— porque el Event Storming reveló dos caminos distintos para la misma acción según el importe. Sin el Event Storming, esa distinción habría aparecido semanas después, durante el desarrollo o, peor, durante la prueba.

> 📋 **Prompt — Traducción de captura de taller a YAML**
>
> Una vez terminada la Fase 5 del taller, este prompt ayuda a completar los bloques 3 y 4 de la plantilla (comportamiento esperado y datos) a partir de la captura estructurada.
>
> ```
> A partir de la siguiente captura de taller de Event Storming,
> completa los bloques de criterios de aceptación y datos de la
> plantilla YAML del requisito.
>
> CAPTURA DEL TALLER:
> Evento: [evento naranja]
> Comando: [comando azul]
> Actor: [actor amarillo]
> Políticas: [políticas lilas]
> Punto de dolor: [post-it rosa]
> Vista necesaria: [post-it verde]
> Preguntas abiertas: [post-its rojos]
>
> GLOSARIO DEL PROYECTO:
> [glosario compacto del capítulo anterior]
>
> Genera los criterios de aceptación en formato Dado/Cuando/Entonces.
> Un criterio por cada flujo identificado (normal y excepciones).
> Usa exclusivamente los términos del glosario. Si hay preguntas
> abiertas sin respuesta, indícalas con [PENDIENTE: descripción].
> ```

---

## La plantilla de captura durante el taller

El analista no puede rellenar la plantilla YAML completa mientras facilita. Necesita un formato de captura más ligero que registre los elementos esenciales sin interrumpir el flujo del taller. Este es el formato que funciona en la práctica:

```yaml
# CAPTURA DE TALLER — Event Storming
# Proyecto: EP-06 Revisión y aprobación de facturas
# Fecha: 2025-05-14
# Participantes: Ana López, Carlos Ruiz, María García, David Sanz

epicas_identificadas:
  - id_provisional: EP-05
    nombre: "Recepción de facturas"
    eventos: ["Factura recibida", "Proveedor notificado de recepción"]
  - id_provisional: EP-06
    nombre: "Revisión y aprobación de facturas"
    eventos: ["Revisión iniciada", "Factura aprobada", "Factura rechazada"]
  - id_provisional: EP-07
    nombre: "Proceso de pago"
    eventos: ["Pago programado", "Pago ejecutado", "Proveedor notificado de pago"]

eventos_identificados:
  - evento: "Factura aprobada"
    epica: EP-06
    actores: ["Gestor de facturación", "Responsable financiero"]
    comandos: ["Aprobar factura"]
    politicas:
      - "Importes > 10.000€ requieren aprobación del Responsable financiero"
      - "La aprobación queda registrada con usuario, fecha y hora"
    puntos_de_dolor:
      - "No hay trazabilidad de quién aprobó qué y cuándo"
    vistas_necesarias:
      - "Detalle de factura con histórico de cambios de estado"
    preguntas_abiertas:
      - pregunta: "¿Puede un gestor aprobar su propia factura?"
        responsable: "Ana López"
        plazo: "2025-05-17"

  - evento: "Factura rechazada"
    epica: EP-06
    actores: ["Gestor de facturación", "Responsable financiero"]
    comandos: ["Rechazar factura"]
    politicas:
      - "El rechazo requiere siempre una nota de motivo de al menos 20 caracteres"
    puntos_de_dolor:
      - "El proveedor no recibe notificación automática del rechazo"
    vistas_necesarias:
      - "Campo de texto libre para el motivo del rechazo"
    preguntas_abiertas:
      - pregunta: "¿Qué ocurre con la factura rechazada? ¿El proveedor puede re-enviarla?"
        responsable: "David Sanz"
        plazo: "2025-05-17"

preguntas_sin_resolver:
  - "¿Cuál es el SLA de revisión de una factura desde que se recibe?"
  - "¿Las facturas en divisas distintas al euro tienen un flujo diferente?"

terminos_nuevos_para_glosario:
  - "nota de rechazo"
  - "SLA de revisión"
  - "factura en divisa"
```

Esta captura es la que el analista convierte en requisitos YAML completos en los dos días siguientes al taller. Los campos `objetivo_negocio`, `descripcion`, `datos_entrada` y `datos_salida` se completan a partir de esta captura sin necesidad de convocar reuniones adicionales, salvo para resolver las preguntas abiertas identificadas.

---

## Los cinco errores del facilitador novel

Estos son los patrones que aparecen en casi todos los primeros talleres y que el facilitador puede evitar si los conoce de antemano.

**Error 1: Resolver los conflictos en lugar de registrarlos.** Cuando dos personas no se ponen de acuerdo sobre el orden de dos eventos o sobre quién hace qué, el facilitador novato intenta resolver el conflicto en el momento. El facilitador experto pone un post-it rojo de pregunta abierta y continúa. Los conflictos se resuelven con las personas correctas fuera del taller, no con el grupo completo en caliente.

**Error 2: Permitir que una persona domine el espacio.** En casi todos los grupos hay alguien que habla más que los demás. Si esa persona domina el taller, el mapa refleja su perspectiva, no la del proceso real. La técnica más eficaz es la escritura silenciosa de la Fase 1: todos producen post-its al mismo tiempo y en silencio, lo que iguala la participación. Si en fases posteriores una persona sigue dominando, el facilitador puede redirigir explícitamente: «¿Alguien que no haya hablado todavía tiene algo que añadir sobre este punto?»

**Error 3: Entrar en el detalle técnico demasiado pronto.** «¿Cómo se implementa esto?» es una pregunta que no tiene cabida en un Event Storming. Cuando aparece, el facilitador la registra en un post-it rojo y redirige la conversación: «Anotamos esa pregunta técnica para el equipo de desarrollo. Ahora nos centramos en qué debe ocurrir desde la perspectiva del negocio.»

**Error 4: No capturar durante el taller.** Algunos analistas confían en fotografiar el mapa al final y transcribirlo después. El problema es que el mapa sin el contexto de las conversaciones pierde el cuarenta por ciento de la información. Las discusiones, los matices, los «esto es así pero solo cuando...» son tan importantes como los post-its. La captura estructurada debe hacerse durante la Fase 5, con el grupo presente.

**Error 5: Usar el Event Storming para requisitos ya conocidos.** El Event Storming aporta más valor cuando existe incertidumbre sobre el dominio. Si el proceso ya está bien documentado y el equipo lo conoce en profundidad, un taller de requisitos más convencional es más eficiente. El Event Storming es la herramienta para descubrir lo que nadie ha articulado todavía, no para documentar lo que todos ya saben.

---

## Guía rápida para el día del taller

Esta es la referencia que el analista tiene delante durante el workshop. Una sola página, sin scrolling:

```
╔══════════════════════════════════════════════════════════════╗
║  EVENT STORMING — Guía rápida del facilitador                ║
╠══════════════════════════════════════════════════════════════╣
║  CÓDIGO DE COLORES                                           ║
║  Naranja  → Evento de negocio (pasado: "X ocurrió")          ║
║  Azul     → Comando (imperativo: "Hacer X")                  ║
║  Amarillo → Actor (quién ejecuta el comando)                 ║
║  Lila     → Política (si X entonces Y)                       ║
║  Rosa     → Punto de dolor / problema actual                 ║
║  Verde    → Vista / información necesaria                    ║
║  Rojo     → Pregunta abierta / incertidumbre                 ║
╠══════════════════════════════════════════════════════════════╣
║  FASES Y DURACIÓN (taller de 3h)                             ║
║  00:00  Introducción y código de colores         (10 min)    ║
║  00:10  Fase 1: Caos creativo — post-its naranja (30 min)    ║
║  00:40  Fase 2: Línea de tiempo                  (20 min)    ║
║  01:00  Fase 3: Añadir contexto (azul/lila/rosa) (40 min)    ║
║  01:40  Fase 4: Límites de dominio → épicas      (15 min)    ║
║  01:55  PAUSA                                    (10 min)    ║
║  02:05  Fase 5: Captura estructurada en YAML     (30 min)    ║
║  02:35  Cierre: preguntas abiertas y siguientes  (25 min)    ║
╠══════════════════════════════════════════════════════════════╣
║  TRADUCCIONES CLAVE                                          ║
║  Evento naranja   → evento_disparador del requisito          ║
║  Comando azul     → cuando (en el criterio AC)               ║
║  Actor amarillo   → actor del requisito                      ║
║  Política lila    → reglas_negocio del requisito             ║
║  Punto dolor rosa → objetivo_negocio del requisito           ║
║  Vista verde      → datos_salida del requisito               ║
║  Pregunta roja    → incertidumbre a resolver antes del req   ║
╠══════════════════════════════════════════════════════════════╣
║  FRASES DE FACILITACIÓN                                      ║
║  "¿Qué ocurrió antes de esto para que llegáramos aquí?"      ║
║  "¿Y qué pasa si esto no funciona como se espera?"           ║
║  "¿Quién necesita saber que esto ha ocurrido?"               ║
║  "¿Siempre ocurre así o hay casos en que es diferente?"      ║
║  "Anoto esa pregunta en rojo y continuamos."                 ║
╠══════════════════════════════════════════════════════════════╣
║  SEÑALES DE QUE EL TALLER VA BIEN                            ║
║  ✓ Hay debate sobre el orden de los eventos                  ║
║  ✓ Aparecen post-its rojos de preguntas                      ║
║  ✓ Alguien dice "esto no lo hacemos así, lo hacemos asá"     ║
║  ✓ El mapa tiene zonas densas y zonas vacías                 ║
║                                                              ║
║  SEÑALES DE ALERTA                                           ║
║  ✗ Una persona escribe el 80% de los post-its                ║
║  ✗ Nadie pone post-its en silencio                           ║
║  ✗ El grupo debate sobre implementación técnica              ║
║  ✗ El mapa es perfectamente uniforme (falta descubrimiento)  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Lo que funciona en la práctica

El Event Storming tiene una curva de aprendizaje como facilitador que no tiene como participante. Los participantes aprenden el sistema en diez minutos. El facilitador aprende a sacar partido del sistema en dos o tres talleres. Estos son los aprendizajes que acortan esa curva.

El silencio durante la escritura de la Fase 1 incomoda a muchos facilitadores novatos. Treinta minutos en silencio parece demasiado. Pero ese silencio es el que garantiza que el conocimiento de todos emerge, no solo el de los más extrovertidos. Si hay que romper el silencio para animar al grupo, hazlo individualmente y en voz baja, no interrumpiendo a todos.

Los talleres remotos funcionan sorprendentemente bien si todos tienen acceso de edición al tablero de Miro o FigJam y si la cámara está encendida. Lo que no funciona en remoto es la Fase 3 tal como se describe aquí: mover y reorganizar post-its en un tablero digital es más lento que en la pared física. La solución es dar más tiempo a esa fase —cincuenta minutos en lugar de cuarenta— y agrupar los colores en rondas separadas con instrucciones explícitas.

El taller no tiene que producir el mapa perfecto. Tiene que producir un mapa suficientemente bueno para que el analista pueda completar los requisitos sin necesidad de más de una o dos reuniones de seguimiento. Si el analista sale del taller con la captura YAML rellena para el ochenta por ciento de los eventos y con una lista clara de preguntas abiertas para el veinte por ciento restante, el taller fue un éxito.

El Event Storming no reemplaza todas las reuniones de requisitos. Es el punto de partida para módulos nuevos o poco documentados. Para módulos que ya tienen una base funcional documentada, el analista puede saltarse el Big Picture y empezar directamente con la plantilla YAML, usando el Process Level Event Storming solo para los flujos que tienen incertidumbre.

---

## Tres puntos clave

**1.** El Event Storming produce directamente los elementos que necesita la plantilla YAML: los eventos naranjas se convierten en `evento_disparador`, los actores en `actor`, las políticas lilas en `reglas_negocio` y los puntos de dolor rosas en `objetivo_negocio`. No es una técnica de descubrimiento genérica: está diseñada para alimentar el pipeline.

**2.** La calidad del taller depende en un setenta por ciento de la preparación: el espacio correcto, el grupo correcto y el brief previo correcto. El facilitador novel suele subestimar estos tres elementos y sobreestimar la importancia de su propio desempeño durante el taller.

**3.** La Fase 5 de captura estructurada —traducir el mapa al YAML con el grupo presente— es la pieza que distingue un Event Storming orientado al pipeline de uno convencional. Sin ella, el analista pierde el cuarenta por ciento del conocimiento generado en el taller.

---

> 💡 **Pregunta de reflexión para tu equipo**
>
> ¿Cuántas veces has salido de una reunión de requisitos con la sensación de que el equipo entendía cosas distintas y nadie lo había dicho en voz alta? El Event Storming hace que esas diferencias emerjan en el taller, donde cuestan minutos, en lugar de en el sprint, donde cuestan días.

---

Con los tres cimientos del modelo en su lugar —la plantilla AI-ready, el glosario estructurado y el Event Storming como técnica de captura— la base conceptual del libro está completa. El lector sabe cómo capturar el conocimiento del negocio, cómo estructurarlo en un formato que la IA puede procesar y cómo garantizar que el vocabulario es consistente en todo el repositorio.

La Parte III empieza donde termina la captura: con el requisito ya escrito en la plantilla YAML, listo para entrar al pipeline. El primer paso de ese pipeline no es la generación, sino la validación. Antes de que la IA genere una sola historia, el sistema verifica que el requisito está completo, que no es ambiguo y que no contradice ninguno de los que ya existen en el repositorio. Ese es el tema del siguiente capítulo.
