# Punto 3 — Guía de Event Storming para analistas funcionales

El Event Storming es la pieza que falta en la base conceptual del modelo: es el método que permite capturar los requisitos en el workshop de forma que encajen directamente con la plantilla YAML y respeten el vocabulario del glosario desde el primer momento.

---

## Qué es y por qué es el punto de partida correcto

Event Storming es una técnica de descubrimiento colaborativo creada por Alberto Brandolini que permite mapear un dominio de negocio complejo en pocas horas, con todos los actores relevantes en la misma sala, usando solo post-its de colores y una superficie grande. No requiere conocimiento técnico previo: el usuario de negocio trabaja en su propio lenguaje y el analista estructura lo que emerge.

La razón por la que es el punto de partida correcto para este modelo es una sola: el Event Storming produce exactamente los elementos que necesita la plantilla YAML. Al final de un taller bien facilitado, el analista tiene identificados los eventos de negocio que se convierten en `evento_disparador`, los actores que se convierten en `actor`, los comandos que se convierten en el `cuando` de los criterios de aceptación, y las políticas que se convierten en `reglas_negocio`. La plantilla no es un formulario que se rellena después del workshop: es la traducción directa de lo que el Event Storming produce.

---

## Los tres niveles de Event Storming

No todos los workshops son iguales. Hay tres niveles de profundidad y el analista debe elegir el correcto según el objetivo:

**Big Picture Event Storming.** Para proyectos nuevos o módulos que nadie ha documentado antes. Dura entre cuatro y ocho horas. El objetivo es entender el dominio completo: qué ocurre, en qué orden, quién lo hace y dónde están los problemas. Produce el mapa completo de eventos que luego se agrupan en épicas.

**Process Level Event Storming.** Para módulos ya identificados que se van a implementar en el siguiente trimestre. Dura entre dos y cuatro horas. El objetivo es detallar un proceso concreto hasta el nivel de comandos, actores y políticas. Produce los requisitos listos para convertirse en YAML.

**Design Level Event Storming.** Para el equipo técnico, antes del desarrollo. Dura entre una y dos horas. El objetivo es diseñar los agregados y bounded contexts del sistema. Produce decisiones de arquitectura, no requisitos funcionales. Este nivel está fuera del alcance de esta guía.

Para la mayoría de los proyectos, el analista facilitará el Process Level porque el Big Picture ya se hizo al inicio del proyecto o al definir la hoja de ruta.

---

## Los elementos del lenguaje visual

El Event Storming usa un código de colores que todos los participantes deben conocer antes de empezar. Cinco minutos de explicación al inicio del taller son suficientes.

| COLOR | ELEMENTO | PREGUNTA QUE RESPONDE |
|---|---|---|
| Naranja | Evento de negocio <br>(pasado) | ¿Qué ha ocurrido? <br>"Factura recibida" <br>"Pedido confirmado" <br>"Usuario registrado" |
|  |  |  |
| Azul | Comando <br>(imperativo) | ¿Qué desencadena ese evento? <br>"Registrar factura" <br>"Confirmar pedido" <br>"Crear cuenta" |
|  |  |  |
| Amarillo <br>pálido | Actor <br>(persona/rol) | ¿Quién ejecuta el comando? <br>"Gestor de facturación" <br>"Cliente" <br>"Sistema externo" |
|  |  |  |
| Lila/morado | Política <br>(si...entonces) | ¿Qué regla de negocio provoca que <br>este evento dispare este comando? <br>"Si el importe supera 10.000€, <br>notificar al responsable" |
|  |  |  |
| Rosa | Punto de dolor <br>(problema) | ¿Qué no funciona bien aquí? <br>"No sabemos qué facturas están <br>pendientes sin revisar el email" |
|  |  |  |
| Verde | Vista/read model <br>(información) | ¿Qué información necesita el <br>actor para tomar la decisión? <br>"Listado de facturas pendientes" |
|  |  |  |
| Rojo | Pregunta abierta <br>(incertidumbre) | ¿Qué no sabemos todavía? <br>"¿Cuál es el plazo máximo de <br>revisión?" |

---

| COLOR | ELEMENTO | PREGUNTA QUE RESPONDE |
|---|---|---|
| Naranja | Evento de negocio <br>(pasado) | ¿Qué ha ocurrido? <br>"Factura recibida" ,"Pedido confirmado" ,"Usuario registrado" |
|  |  |  |
| Azul | Comando <br>(imperativo) | ¿Qué desencadena ese evento? <br>"Registrar factura" ,"Confirmar pedido" ,"Crear cuenta" |
|  |  |  |
| Amarillo <br>pálido | Actor <br>(persona/rol) | ¿Quién ejecuta el comando? <br>"Gestor de facturación" ,"Cliente" ,"Sistema externo" |
|  |  |  |
| Lila/morado | Política <br>(si...entonces) | ¿Qué regla de negocio provoca que este evento dispare este comando? <br>"Si el importe supera 10.000€, notificar al responsable" |
|  |  |  |
| Rosa | Punto de dolor <br>(problema) | ¿Qué no funciona bien aquí? <br>"No sabemos qué facturas están pendientes sin revisar el email" |
|  |  |  |
| Verde | Vista/read model <br>(información) | ¿Qué información necesita el actor para tomar la decisión? <br>"Listado de facturas pendientes" |
|  |  |  |
| Rojo | Pregunta abierta <br>(incertidumbre) | ¿Qué no sabemos todavía? <br>"¿Cuál es el plazo máximo de revisión?" |

---

| Color | Elemento | Pregunta que responde | Ejemplo |
|---|---|---|---|
| 🟠 Naranja | Evento de negocio (pasado) | ¿Qué ha ocurrido? | "Factura recibida", "Pedido confirmado" |
| 🔵 Azul | Comando (imperativo) | ¿Qué desencadena ese evento? | "Registrar factura", "Confirmar pedido" |
| 🟡 Amarillo pálido | Actor (persona/rol) | ¿Quién ejecuta el comando? | "Gestor de facturación", "Cliente" |
| 🟣 Lila/morado | Política (si…entonces) | ¿Qué regla de negocio provoca que este evento dispare este comando? | "Si el importe supera 10.000€, notificar al responsable" |
| 🩷 Rosa | Punto de dolor (problema) | ¿Qué no funciona bien aquí? | "No sabemos qué facturas están pendientes sin revisar el email" |
| 🟢 Verde | Vista/read model (información) | ¿Qué información necesita el actor para tomar la decisión? | "Listado de facturas pendientes" |
| 🔴 Rojo | Pregunta abierta (incertidumbre) | ¿Qué no sabemos todavía? | "¿Cuál es el plazo máximo de revisión?" |

---

## Preparación del taller

La calidad del workshop depende en un 70% de la preparación. Un taller mal preparado produce mapas confusos que el analista no puede traducir a requisitos.

**Quién debe estar en la sala.** El grupo ideal tiene entre seis y diez personas. Más pequeño y falta perspectiva. Más grande y el grupo es ingobernable. Los perfiles imprescindibles son: al menos dos usuarios de negocio que conozcan el proceso en profundidad, el product owner o quien toma decisiones de alcance, y el analista que facilitará. Opcionales pero recomendables: un desarrollador senior para detectar restricciones técnicas relevantes y un representante de QA para hacer preguntas sobre los casos de error.

**El espacio.** Una pared o superficie continua de al menos cuatro metros de longitud. El rollo de papel de embalar pegado a la pared funciona perfectamente. Si es remoto, Miro o FigJam con una plantilla de Event Storming pre-configurada. La clave en remoto es que todos los participantes tengan cámara encendida y acceso de edición al tablero.

**El material.** Post-its de los colores del código visual, rotuladores negros gruesos para que la letra se lea desde lejos, y cinta de carrocero para delimitar zonas del lienzo. Nunca usar bolígrafo: la letra no se ve.

**El brief previo.** Dos días antes del taller, el analista envía un mensaje de no más de diez líneas que explica el objetivo del workshop, el proceso que se va a mapear y el resultado esperado. No más. Si se comparte demasiado contexto previo, los participantes llegan con ideas preconcebidas que bloquean el descubrimiento.

> **Ejemplo de brief previo:**
>
> Hola a todos,
>
> El próximo martes haremos una sesión de 3 horas para mapear juntos el proceso de gestión de facturas de proveedor, desde que recibimos una factura hasta que se paga. El objetivo es identificar qué ocurre exactamente en ese proceso, quién hace qué y dónde están los problemas actuales.
>
> No hace falta preparar nada. Solo vuestro conocimiento del proceso.
>
> Nos vemos el martes a las 10:00 en la sala Proyecto.

---

## El flujo del taller paso a paso

### Fase 1 — Caos creativo (30-45 minutos)

El facilitador explica el código de colores en cinco minutos y lanza la primera instrucción: *"Escribid todos los eventos que ocurren en este proceso. Un post-it naranja por evento. Usad el pasado. No os coordinéis entre vosotros todavía."*

Los participantes escriben en silencio durante 15-20 minutos. El resultado es un caos de post-its naranjas distribuidos aleatoriamente por el lienzo. Eso es exactamente lo que debe ocurrir. El caos inicial es la señal de que el grupo está volcando su conocimiento sin filtros.

El analista no participa en la escritura durante esta fase. Su rol es observar, asegurarse de que todos escriben (los más callados necesitan a veces un empujón suave) y capturar en un cuaderno privado las primeras señales de conflicto: dos personas que escriben el mismo evento con nombres distintos, eventos que nadie escribe pero que el analista sabe que existen, zonas del proceso donde nadie pone post-its.

**Qué hace la IA en esta fase.** Si el taller es presencial, nada todavía. Si es remoto en Miro, el analista puede tener preparado un prompt para transcribir los post-its al final de la fase y detectar duplicados automáticamente.

### Fase 2 — Línea de tiempo (20-30 minutos)

El facilitador pide al grupo que ordene los eventos en el eje horizontal de izquierda a derecha siguiendo el orden temporal. La instrucción exacta es: *"Moved los post-its para que el flujo se lea de izquierda a derecha. Lo que ocurre primero va a la izquierda."*

Esta fase es donde emergen los primeros conflictos productivos. Dos personas intentan poner el mismo evento en momentos distintos de la línea porque tienen perspectivas diferentes del proceso. El facilitador no resuelve el conflicto: lo señala con un post-it rojo de pregunta abierta y continúa. Las preguntas abiertas se resuelven al final del taller o en una sesión posterior.

El resultado al final de esta fase es una línea de eventos naranjas ordenada cronológicamente con algunos huecos (eventos que faltan) y algunos grupos densos (zonas del proceso bien conocidas).

### Fase 3 — Añadir contexto (30-40 minutos)

Con la línea de tiempo estable, el facilitador añade las otras capas del modelo en este orden:

**Comandos (azul).** Para cada evento naranja, el grupo identifica qué comando lo causó. La pregunta es: *"¿Qué acción provocó que ocurriera este evento?"* El comando se escribe en azul y se coloca justo antes del evento que causa.

**Actores (amarillo).** Para cada comando, ¿quién lo ejecuta? El actor se coloca sobre el comando. Aquí es donde el glosario cobra valor: si el grupo empieza a usar "cliente", "usuario" y "comprador" para referirse a la misma persona, el analista interviene con el término oficial del glosario.

**Políticas (lila).** Entre eventos y comandos, ¿hay alguna regla de negocio que determina qué ocurre? La política se escribe en lila y se coloca entre el evento que la activa y el comando que desencadena. Las políticas son el origen directo de las reglas de negocio de los requisitos.

**Puntos de dolor (rosa).** El facilitador pregunta activamente: *"¿Dónde os duele este proceso? ¿Qué es lento, confuso o propenso a errores?"* Los puntos de dolor se convierten en el `objetivo_negocio` de los requisitos: explican por qué existe la necesidad de cambio.

**Preguntas abiertas (rojo).** Todo lo que el grupo no sabe todavía. Cada pregunta roja es un riesgo para el proyecto que necesita respuesta antes de que el analista pueda redactar el requisito.

### Fase 4 — Identificar límites de dominio (15-20 minutos)

Con el mapa completo, el facilitador pide al grupo que identifique las zonas naturales del proceso: agrupaciones de eventos que tienen cohesión entre sí y que están separadas de otras agrupaciones. Estas zonas son las futuras épicas.

El facilitador dibuja líneas verticales con cinta de carrocero separando las zonas y el grupo les da un nombre. Ese nombre es el nombre de la épica y va al glosario como un término oficial.

**Ejemplo de mapa resultante (simplificado):**

```
│← EP-03 Recepción ───────┤← EP-04 Revisión ──────────┤← EP-05 Pago ───────────→│
│                         │                            │                         │
│ [Factura recibida] ──→  │ [Revisión iniciada] ────→  │ [Pago programado] ───→  │
│ [Proveedor notificado]  │ [Factura aprobada]         │ [Pago ejecutado]        │
│                         │ [Factura rechazada]        │ [Proveedor notificado]  │
│                         │                            │                         │
│ Actor: Sistema          │ Actor: Gestor facturación  │ Actor: Tesorería        │
│ Actor: Proveedor        │ Actor: Resp. financiero    │ Actor: Sistema banco    │
```

### Fase 5 — Captura estructurada (20-30 minutos)

Esta fase la lidera el analista, no el facilitador (pueden ser la misma persona o no). Mientras el mapa todavía está visible y el grupo sigue en la sala, el analista traduce los elementos del mapa a los campos de la plantilla YAML en tiempo real.

La ventaja de hacerlo mientras el grupo está presente es que las dudas se resuelven inmediatamente. El analista lee en voz alta lo que está escribiendo y el grupo confirma o corrige.

**Traducción de elementos del mapa a campos YAML:**

| Elemento del mapa | Campo YAML |
|---|---|
| Evento naranja | `evento_disparador` |
| Comando azul | `cuando` (en el criterio AC) |
| Actor amarillo | `actor` |
| Política lila | `reglas_negocio` |
| Punto de dolor rosa | `objetivo_negocio` |
| Vista verde | `datos_salida` |
| Pregunta roja | Incertidumbre a resolver antes del requisito |
| Agrupación de eventos | `epica` |

---

## Plantilla de captura durante el taller

El analista usa esta plantilla en tiempo real durante la Fase 5. Es deliberadamente simple para no ralentizar la captura:

```yaml
# CAPTURA DE TALLER — Event Storming
# Proyecto: _______________  Fecha: ___________
# Participantes: _______________

eventos_identificados:
  - evento: "Factura recibida"
    epica_candidata: "EP-04 Gestión de Facturación"
    actores_involucrados: ["Proveedor", "Sistema de correo"]
    comandos_que_lo_causan: ["Registrar factura en el sistema"]
    politicas_asociadas:
      - "Si el importe supera 10.000€, asignar al Responsable financiero"
    puntos_de_dolor:
      - "Actualmente se registra manualmente copiando datos del email"
    preguntas_abiertas:
      - "¿Cuál es el plazo máximo para registrar una factura recibida?"
    vistas_necesarias:
      - "Bandeja de facturas pendientes de registro"

  - evento: "Factura aprobada"
    epica_candidata: "EP-04 Gestión de Facturación"
    actores_involucrados: ["Gestor de facturación", "Responsable financiero"]
    comandos_que_lo_causan: ["Aprobar factura"]
    politicas_asociadas:
      - "Solo facturas del ejercicio fiscal en curso pueden aprobarse"
      - "Importes >10.000€ requieren aprobación del Responsable financiero"
    puntos_de_dolor:
      - "No hay trazabilidad de quién aprobó qué y cuándo"
    preguntas_abiertas:
      - "¿Puede un gestor aprobar su propia factura?"
    vistas_necesarias:
      - "Detalle de factura con histórico de cambios"

preguntas_sin_resolver:
  - pregunta: "¿Cuál es el plazo máximo de revisión de una factura?"
    impacto: "Define el SLA y los criterios de escalado automático"
    responsable_respuesta: "Ana López (Dirección Financiera)"
    plazo_respuesta: "2025-05-15"

epicas_identificadas:
  - id_provisional: "EP-03"
    nombre: "Recepción de facturas"
    eventos_incluidos: ["Factura recibida", "Proveedor notificado"]
  - id_provisional: "EP-04"
    nombre: "Gestión y revisión de facturas"
    eventos_incluidos: ["Revisión iniciada", "Factura aprobada", "Factura rechazada"]
  - id_provisional: "EP-05"
    nombre: "Proceso de pago"
    eventos_incluidos: ["Pago programado", "Pago ejecutado", "Proveedor notificado de pago"]
```

---

## De la captura del taller al YAML de requisito

La captura del taller no es el requisito final. Es la materia prima que el analista transforma en los días siguientes en requisitos YAML completos. La traducción sigue este patrón sistemático:

**Un evento de negocio no siempre es un requisito.** A veces un evento es el resultado de otro requisito. La regla práctica es: si el evento requiere que el sistema haga algo activamente, es un requisito. Si el evento simplemente ocurre como consecuencia de otro, es el resultado esperado de ese requisito.

**Un comando con su actor y sus políticas es el núcleo de un requisito.** El comando se convierte en el `evento_disparador`. El actor se convierte en el `actor`. Cada política se convierte en una `regla_negocio`. La vista necesaria se convierte en los `datos_salida`.

**Los criterios de aceptación se construyen desde los flujos.** El flujo normal (comando → evento) produce el criterio positivo. Las políticas producen criterios adicionales. Los puntos de dolor producen los casos de error y las excepciones.

**Ejemplo de traducción:**

```
CAPTURA DEL TALLER:
  Evento:    "Factura aprobada"
  Comando:   "Aprobar factura"
  Actor:     "Gestor de facturación"
  Política:  "Importes >10.000€ requieren Responsable financiero"
  Dolor:     "No hay trazabilidad de quién aprobó"
  Vista:     "Detalle de factura con histórico"

YAML RESULTANTE:
  actor: "Gestor de facturación"
  evento_disparador: >
    El gestor accede a una factura en estado 'en-revision'
    para aprobarla tras verificar que es correcta
  reglas_negocio:
    - "Facturas con importe >10.000€ no pueden ser aprobadas
       por el Gestor de facturación. Requieren Responsable financiero."
    - "La aprobación queda registrada con fecha, hora y usuario."
  criterios_aceptacion:
    - id: AC-XXX-01
      dado: >
        El gestor está en el detalle de una factura
        en estado 'en-revision' con importe ≤10.000€
      cuando: "Pulsa el botón 'Aprobar'"
      entonces: >
        La factura cambia a estado 'aprobada'.
        Se registra la aprobación con el nombre del gestor,
        la fecha y la hora. El Responsable financiero no recibe notificación.
    - id: AC-XXX-02
      dado: >
        El gestor está en el detalle de una factura
        en estado 'en-revision' con importe >10.000€
      cuando: "Pulsa el botón 'Aprobar'"
      entonces: >
        El sistema muestra el mensaje 'Esta factura requiere
        aprobación del Responsable financiero'. El estado
        de la factura no cambia.
```

---

## Los cinco errores más frecuentes del facilitador novel

**Resolver los conflictos en lugar de registrarlos.** Cuando dos personas no se ponen de acuerdo sobre el orden de dos eventos o sobre quién hace qué, el facilitador novato intenta resolver el conflicto en el momento. El facilitador experto pone un post-it rojo de pregunta abierta y continúa. Los conflictos se resuelven con las personas correctas, no con el grupo completo.

**Permitir que una persona domine el espacio.** En casi todos los grupos hay alguien que habla más que los demás. Si esa persona domina el taller, el mapa refleja su perspectiva, no la del proceso real. La técnica más eficaz es la escritura silenciosa de la Fase 1: todos producen post-its al mismo tiempo y en silencio, lo que iguala la participación.

**Entrar en el detalle técnico demasiado pronto.** *"¿Cómo se implementa esto?"* es una pregunta que no tiene cabida en un Event Storming. Cuando aparece, el facilitador la registra en un post-it rojo y redirige la conversación: *"Anotamos esa pregunta técnica para el equipo de desarrollo. Ahora mismo nos centramos en qué debe ocurrir desde la perspectiva del negocio."*

**No capturar durante el taller.** Algunos analistas confían en fotografiar el mapa al final y transcribirlo después. El problema es que el mapa sin el contexto de las conversaciones pierde el 40% de la información. Las discusiones, los matices, los "esto es así pero solo cuando..." son tan importantes como los post-its. La captura estructurada debe hacerse durante la Fase 5, con el grupo presente.

**Usar el Event Storming para requisitos ya conocidos.** El Event Storming aporta más valor cuando existe incertidumbre sobre el dominio. Si el proceso ya está bien documentado y el equipo lo conoce en profundidad, un taller de requisitos más convencional es más eficiente. El Event Storming es la herramienta para descubrir lo que nadie ha articulado todavía, no para documentar lo que todos ya saben.

---

## Guía de referencia rápida para el día del taller

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
║  01:40  Fase 4: Límites de dominio → épicas      (20 min)    ║
║  02:00  PAUSA                                    (10 min)    ║
║  02:10  Fase 5: Captura estructurada en YAML     (30 min)    ║
║  02:40  Cierre: preguntas abiertas y siguientes  (20 min)    ║
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
║  "Anoto esa pregunta en rojo y continuamos"                  ║
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

## Qué entrega el taller al repositorio documental

Al terminar el taller, el analista tiene estos entregables listos para entrar al repositorio:

**El mapa fotográfico.** Fotografías de alta resolución del lienzo físico o exportación del tablero digital. Se archivan como evidencia del proceso de descubrimiento, no como documentación operativa.

**La captura YAML del taller.** El archivo de captura relleno durante la Fase 5. No es un requisito completo todavía: es la materia prima que el analista completará en los días siguientes añadiendo los bloques 3, 4 y 5 de la plantilla (comportamiento, datos y metadatos técnicos).

**El registro de preguntas abiertas.** Lista de todos los post-its rojos del taller con el responsable de respuesta y el plazo. Estos bloqueos deben resolverse antes de que el requisito pueda pasar a estado `validado`.

**El borrador del glosario ampliado.** Todos los términos nuevos que aparecieron en el taller y que no estaban en el glosario. El propietario del glosario los revisa con el área de negocio en los dos días siguientes al taller.

**El esquema de épicas.** La propuesta de agrupación de épicas derivada de la Fase 4. El product owner la revisa y aprueba antes de que el analista empiece a asignar los requisitos.

Con estos cinco entregables, el analista tiene todo lo necesario para completar los requisitos YAML en un plazo de uno a tres días laborables, sin necesidad de convocar reuniones adicionales salvo para resolver las preguntas abiertas identificadas.

---

*Con esto, los tres puntos de la base conceptual del modelo están completos: la plantilla de requisito AI-ready, el glosario estructurado y la guía de Event Storming para analistas. La base sobre la que se sustenta todo el pipeline técnico está íntegramente documentada.*
