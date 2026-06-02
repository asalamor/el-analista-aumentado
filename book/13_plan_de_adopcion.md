# Capítulo 13. Plan de adopción

Carlos guarda el terminal y mira el reloj: las 17:23 del martes. Hace exactamente tres semanas, en esa misma hora, estaba copiando campos de un documento Word a Jira mientras el equipo esperaba las historias para el sprint del jueves. Hoy ha procesado REQ-023 en cuarenta y siete segundos, ha revisado el JSON durante tres minutos y ha aprobado los artefactos con una sola tecla.

Pero Carlos es una persona. El equipo de Meridian tiene cuatro analistas, un product owner, dos QA leads y doce desarrolladores. Y en el pasillo, mientras espera el ascensor, David le pregunta algo que sabe que lleva semanas cocinándose: "¿Cuándo lo ponemos en marcha para todos?"

Esa pregunta —cuándo y cómo hacer que el sistema funcione para un equipo real, no solo para el analista que lo construyó— es el tema de este capítulo.

---

## En este capítulo

- Por qué la tecnología es la parte fácil y la adopción es el verdadero reto.
- El plan de cuatro fases para implantar el sistema de forma gradual, con valor visible en las primeras dos semanas.
- Cómo gestionar las resistencias específicas de cada perfil: analistas funcionales, usuarios de negocio, equipo técnico y dirección.
- Los materiales de comunicación y formación que han funcionado en la práctica.
- Las métricas que demuestran el impacto antes de que nadie lo pida.

---

## El problema que nadie nombra en los proyectos de transformación

Meridian no es la primera organización que construye algo así. La historia de los proyectos de automatización en empresas medianas tiene un patrón reconocible: un equipo técnico entusiasta construye un sistema que funciona, hace una demostración interna, recibe aplausos, y tres meses después el sistema está apagado porque "es demasiado complicado" o "no encaja con nuestro proceso".

La tecnología no era el problema. El problema era que nadie había gestionado el cambio con el mismo rigor con el que se gestionó el desarrollo.

Este capítulo existe porque el sistema que has construido en los Capítulos 4 a 12 puede tener el mismo destino si la adopción se deja al azar. Y también existe porque, cuando la adopción se gestiona bien, los resultados son sorprendentemente rápidos.

> 💡 **Idea clave**
>
> El objetivo de la adopción no es que todo el equipo use el sistema desde el primer día. Es que cada persona que lo usa sienta que su trabajo mejora, y que esa percepción se propague sola.

---

## Por qué la gente resiste (y tiene razón en hacerlo)

Antes de diseñar el plan, conviene entender las resistencias reales. No son irracionales. Cada perfil tiene motivos legítimos para desconfiar.

**Los analistas funcionales** tienen miedo a dos cosas que no siempre dicen en voz alta. La primera es el miedo a la sustitución: si la IA puede generar las historias, ¿para qué me necesitan a mí? La segunda es el miedo al juicio: el sistema va a leer mis requisitos y va a decirme que están mal. Eso duele.

**Los usuarios de negocio** tienen una resistencia diferente: ya tienen demasiadas reuniones y demasiadas herramientas. Cualquier cambio en el proceso de captura de requisitos se percibe como trabajo adicional, aunque no lo sea.

**El equipo técnico** desconfía de los artefactos generados por IA porque ha visto antes historias mal escritas llegar al sprint. La pregunta implícita es: ¿el sistema va a generar más basura más rápido?

**La dirección** tiene la resistencia más pragmática de todas: el coste de cambiar un proceso que, aunque imperfecto, funciona. La pregunta es simple: ¿cuánto va a costar esto y qué vamos a ganar?

Cada una de estas resistencias tiene una respuesta concreta. El plan de adopción es, en gran medida, la secuencia en la que se dan esas respuestas.

---

## Los cuatro principios que guían el plan

Antes de entrar en las fases, cuatro principios que determinan todas las decisiones del plan:

**Valor visible antes que proceso correcto.** El equipo necesita ver un beneficio concreto en las primeras dos semanas. Si las primeras semanas son de configuración y formación sin output tangible, la resistencia se instala.

**El analista como protagonista, no como receptor.** El analista no es el usuario final del sistema: es el experto que lo supervisa y lo mejora. Ese reencuadre cambia completamente la dinámica de adopción.

**El usuario de negocio no debe notar el cambio.** El proceso con el usuario de negocio debe parecer una ligera evolución del anterior. Los cambios profundos ocurren entre bastidores.

**Métricas desde el día uno.** Sin métricas no hay argumento para continuar cuando aparezcan las primeras fricciones. Las métricas también motivan al equipo cuando muestran mejora real.

---

## El plan en cuatro fases

El roadmap de implantación que introdujimos en el Capítulo 3 tiene cuatro fases. En este capítulo lo convertimos en un plan de acción concreto con actividades, responsables y criterios de avance.

### Fase 0 — Preparación silenciosa (semanas 1 y 2)

Esta fase ocurre sin comunicar nada al equipo todavía. El objetivo es tener todo listo para que la demo de la Fase 1 sea impactante con datos reales del propio proyecto.

**Actividad 1: Seleccionar el proyecto piloto.**

El piloto no debe ser el proyecto más grande ni el más estratégico. Debe cumplir tres condiciones: hay un analista receptivo al cambio, el módulo funcional está acotado (entre diez y veinte requisitos), y el backlog tiene algunos problemas conocidos de ambigüedad que el sistema pueda resolver de forma visible.

En Meridian, el módulo EP-04 de Gestión de Facturación fue la elección obvia: Carlos lo conocía bien, Ana López había pedido mejoras en el proceso de cierre mensual, y todos sabían que US-041 y US-043 habían llegado al sprint con problemas. Un módulo con historia de dolor reciente es el mejor candidato para un piloto.

**Actividad 2: Medir la línea base.**

Durante dos semanas, sin cambiar nada en el proceso actual, medir estas métricas:

| Métrica | Cómo medirla | Valor en Meridian |
|---|---|---|
| Tiempo desde reunión de requisitos hasta historias en Jira | El analista cronometra tres requisitos reales | 110 minutos de media |
| Porcentaje de historias que llegan al sprint con cambios de alcance | Revisar retrospectivas de los últimos tres sprints | 28% |
| Bugs clasificados como "ambigüedad funcional" | Filtrar en Jira por campo de causa raíz | 4 de los últimos 15 bugs |
| Porcentaje de historias con criterios de aceptación documentados | Auditar las últimas 30 historias cerradas | 61% |

Estos números van a ser el argumento más poderoso del plan. Cuando en la Fase 3 la tasa de ambigüedad funcional baje a 1 de cada 15 bugs, ese contraste habla solo.

> ⚠️ **Error frecuente**
>
> Muchos equipos saltan la medición de línea base porque parece trabajo extra antes de empezar. Es un error que cuesta caro: sin datos del antes, no hay manera de demostrar el impacto del después. Invertir dos horas en medir bien el estado actual ahorra semanas de conversaciones difíciles con la dirección en el futuro.

**Actividad 3: Construir el dataset de demostración.**

Antes de cualquier formación, el responsable técnico toma tres o cuatro requisitos reales del proyecto piloto, los transforma al formato YAML y los pasa por el pipeline completo con `--dry-run`. El resultado —historias, tareas técnicas y test cases generados con el vocabulario real del proyecto— es el material de la demo de la Fase 1.

Nada convence más que ver el propio trabajo transformado. Un requisito que el equipo reconoce, convertido en artefactos que el equipo habría tardado dos horas en crear manualmente, genera en cuarenta y siete segundos.

**Actividad 4: Identificar al champion.**

El champion es la persona que más rápido va a adoptar el sistema y que tiene credibilidad con el resto del equipo. No tiene por qué ser el analista más senior. Suele ser el más curioso tecnológicamente o el que más ha sufrido los problemas que el sistema resuelve.

Carlos fue el champion de Meridian no porque fuera el mejor analista, sino porque era el más cansado de copiar campos entre sistemas. Esa motivación personal es más potente que cualquier incentivo externo.

El champion recibe formación técnica completa antes que nadie y se convierte en el referente interno durante los primeros meses. Su tiempo estimado es de tres a cuatro horas semanales, no más.

---

### Fase 1 — Demo y enganche (semanas 3 y 4)

El objetivo de esta fase es una sola cosa: que el equipo *quiera* usar el sistema. No que lo entienda completamente. No que confíe plenamente en él. Solo que quiera probarlo.

#### La sesión de demo (90 minutos)

La demo tiene una estructura diseñada para maximizar el impacto antes de explicar nada técnico.

**Apertura con el dolor conocido (10 min).** Empezar con una pregunta directa: "¿Cuánto tiempo tardáis en pasar de una reunión de requisitos a las historias en Jira?" Dejar que el equipo responda. Normalmente la respuesta es entre uno y tres días. Luego: "¿Cuántas veces habéis llegado al sprint con una historia que tuvo que cambiar porque el requisito era ambiguo?" Más respuestas incómodas.

No añadir nada todavía. El equipo ha articulado el problema que el sistema resuelve.

**La transformación en directo (30 min).** Tomar uno de los requisitos del dataset preparado en la Fase 0, uno que el equipo reconozca, y ejecutar el pipeline en directo:

```bash
# El comando que Carlos ejecuta en la demo, con el equipo mirando
python orchestrator.py --req REQ-023 --dry-run
```

La pantalla muestra los nueve pasos, los artefactos generados y el output final. En menos de un minuto aparecen la historia, las cuatro tareas técnicas y los nueve test cases. El silencio que sigue a ese momento vale más que cualquier presentación.

**La conversación honesta (20 min).** No vender el sistema como perfecto. Mostrar los errores que comete: los campos que a veces genera con información incompleta, los casos donde el glosario no está bien definido y la IA usa un término incorrecto, los criterios de aceptación que el analista tiene que reescribir antes de aprobar.

Esta honestidad construye más confianza que una demo perfecta. El equipo sabe que estás mostrando la realidad.

**El rol del analista en el nuevo proceso (20 min).** Este es el momento más importante de la sesión. La pregunta de María García del Capítulo 2 —"¿esto nos va a reemplazar?"— va a estar en la cabeza de todos aunque nadie la diga en voz alta.

La respuesta concreta: la IA hace el trabajo mecánico (rellenar campos, formatear, generar la estructura), el analista hace el trabajo de valor (entender el negocio, validar que el output es correcto, detectar lo que la IA no puede ver).

La metáfora que Carlos usa en Meridian es la del copiloto de avión: el copiloto no sustituye al piloto, hace el trabajo de monitorización y ejecución rutinaria para que el piloto pueda concentrarse en las decisiones difíciles. El analista pasa de copiar datos entre sistemas a tomar decisiones funcionales con información más completa y más tiempo.

**Preguntas sin filtro (10 min).** Dejar espacio real para las preguntas incómodas. Estas son las más frecuentes y las respuestas que funcionan:

| Pregunta | Respuesta honesta |
|---|---|
| "¿Esto nos va a reemplazar?" | No. Va a eliminar la parte más aburrida de tu trabajo. La parte que requiere juicio experto sigue siendo tuya. |
| "¿Qué pasa si la IA genera algo incorrecto?" | Por eso existe el gate de aprobación. Nada llega a Jira sin que tú lo hayas revisado. |
| "¿Cuánto tiempo me va a llevar aprender esto?" | La sesión práctica de mañana es suficiente para empezar. En dos semanas lo usarás con fluidez. |
| "¿Y si el negocio no quiere cambiar?" | El negocio no cambia nada. La plantilla estructurada la rellena el analista después de la reunión, no el usuario de negocio. |

> 🛠️ **En la práctica**
>
> En Meridian, la pregunta que más silenció la sala no fue ninguna de esas cuatro. Fue David Sanz, el product owner, quien preguntó: "¿Podemos hacer que los criterios de aceptación lleguen al planning ya listos para votar?" Esa pregunta, salida espontáneamente del equipo, fue el mejor argumento de adopción. Cuando el equipo empieza a imaginar cómo usarlo, la demo ha funcionado.

#### La sesión práctica con analistas (120 minutos)

Dos días después de la demo, sesión de manos a la obra solo con los analistas. Sin directivos, sin usuarios de negocio. Solo el equipo técnico-funcional.

```
00:00 - 00:20  El champion explica el pipeline con sus palabras
               Objetivo: que el equipo se lo oiga explicar a un igual

00:20 - 00:50  Ejercicio individual
               Cada analista rellena un requisito real en la plantilla YAML
               Pasa el requisito por el validador
               Ve los errores detectados y los corrige

00:50 - 01:20  Ejercicio en parejas
               Una pareja ejecuta el pipeline sobre el requisito del ejercicio
               La otra pareja revisa el output y lo aprueba o rechaza con argumentos
               Rotar roles

01:20 - 01:40  Puesta en común
               ¿Qué os ha sorprendido positivamente?
               ¿Qué no funciona como esperabais?
               ¿Qué cambiaríais de la plantilla para vuestro contexto?

01:40 - 02:00  Configuración personal
               Cada analista configura su acceso a la herramienta
               El champion queda como punto de contacto para dudas
               Se acuerda la cadencia de revisión: 30 min semanales el primer mes
```

> ⚠️ **Error frecuente**
>
> La tentación es hacer esta sesión con toda la organización a la vez. Es el error más común y el más costoso. La formación en grupo produce la ilusión de adopción: todos asisten, todos asienten, nadie usa el sistema porque nadie se siente responsable individual. La adopción funciona persona a persona, con seguimiento individual.

---

### Fase 2 — Piloto asistido (meses 2 y 3)

Un analista —el champion— usa el sistema en su proyecto real con plena supervisión. El resto del equipo observa y aprende sin presión.

#### Qué cambia (y qué no cambia) en el proceso del analista

El analista no abandona su flujo de trabajo habitual. Lo extiende con tres pasos nuevos que se insertan en momentos naturales del proceso.

**Después de la reunión de requisitos (en lugar de abrir Word).** El analista abre la plantilla YAML en Confluence y rellena los bloques 1, 2 y 3 mientras la reunión está fresca. El tiempo no cambia: antes tardaba cuarenta y cinco minutos en escribir el documento Word. Ahora tarda cuarenta minutos en rellenar la plantilla estructurada.

**Antes de enviar el requisito a revisión.** Ejecuta el validador automático del Capítulo 7. Si hay errores bloqueantes, los corrige. Si hay advertencias, las anota. Esto reemplaza la revisión informal que antes hacía mentalmente o preguntando a un compañero.

**En lugar de crear manualmente los issues en Jira.** Aprueba el JSON generado por el pipeline y lo empuja a Jira. Este paso reemplaza entre treinta y noventa minutos de trabajo mecánico por cinco a diez minutos de revisión.

La suma de los tres cambios produce la reducción de tiempo que medimos: de ciento diez minutos a treinta y ocho en Meridian al final del segundo mes del piloto.

> 💡 **Idea clave**
>
> El sistema no cambia el trabajo del analista: cambia la proporción de su tiempo que se dedica a trabajo de valor. El tiempo total puede incluso ser parecido al principio. Lo que cambia es que esos cuarenta minutos producen mucho más que antes.

#### Protocolo de seguimiento semanal

El champion y el responsable técnico se reúnen treinta minutos cada semana con un guión fijo:

```
1. ¿Qué funcionó bien esta semana? (5 min)
   → Documentar para el caso de éxito

2. ¿Qué no funcionó o generó fricción? (10 min)
   → Categorizar: ¿problema de plantilla, de prompt, de glosario o de proceso?

3. ¿Qué ajuste concreto hacemos esta semana? (10 min)
   → Un solo ajuste por semana. No acumular.
   → Documentar el ajuste y el motivo.

4. ¿Qué le contamos al resto del equipo? (5 min)
   → Actualización de tres frases en el canal del equipo.
   → Sin tecnicismos. Sin hype.
```

La regla del ajuste único por semana es importante. La tentación de hacer varios cambios a la vez impide saber cuál funcionó y cuál no.

#### Las métricas del piloto

Estas métricas se miden cada semana durante los dos primeros meses:

| Métrica | Línea base (Fase 0) | Objetivo semana 8 |
|---|---|---|
| Tiempo de creación de artefactos por requisito | 110 min | < 45 min |
| Errores detectados por el validador por requisito | Sin dato (primer sprint) | Tendencia descendente |
| Porcentaje de artefactos Jira aprobados sin ediciones | 0% (primer contacto) | > 80% |
| Historias que llegan al sprint sin cambios de alcance | 72% (Fase 0) | > 88% |

La métrica de "artefactos aprobados sin ediciones" merece atención especial. Al inicio del piloto, el champion edita muchos campos antes de aprobar: el sistema todavía no conoce el vocabulario específico de Meridian ni el estilo del equipo. A partir del requisito diez o quince, cuando el glosario está maduro y los prompts están calibrados, la tasa de aprobación directa supera el ochenta por ciento. Ese umbral es el momento en que el sistema deja de ser un experimento y pasa a ser una herramienta de producción.

---

### Fase 3 — Expansión (meses 4 a 6)

Con el caso de éxito documentado del piloto, la expansión es mucho más sencilla. El equipo ya tiene pruebas internas, no promesas de un proveedor externo.

#### Incorporación del resto de analistas

La secuencia no es "todos a la vez". Es persona a persona, en tres semanas:

**Semana 1.** El champion presenta el caso de éxito del piloto al resto de analistas. Treinta minutos, sin presentación formal. Solo números reales y anécdotas concretas: "Antes tardaba dos horas en crear los issues de Jira para un requisito complejo. Ahora tardo veinte minutos en revisar lo que genera el sistema."

**Semanas 2 y 3.** Cada analista tiene una sesión individual de noventa minutos con el champion. No con el responsable técnico: con el champion, un igual. Esta sesión replica el ejercicio práctico de la Fase 1 pero con los datos del proyecto específico de cada analista.

**Semanas 4 a 6.** Cada analista usa el sistema en un requisito real de su proyecto actual, con el champion disponible por Slack para preguntas. No hay presión de velocidad ni de perfección.

**Mes 5 y 6.** El sistema es el flujo estándar para todos los analistas. Las métricas se miden a nivel de equipo.

#### Incorporación de los usuarios de negocio

Los usuarios de negocio no reciben formación sobre el sistema. Lo que cambia para ellos es mínimo y se presenta como una mejora de las reuniones, no como un cambio de proceso:

| Antes | Ahora |
|---|---|
| Usuario: "Necesitamos poder gestionar las facturas mejor" | Usuario: "Necesitamos poder gestionar las facturas mejor" |
| Analista toma notas en Word durante la reunión | Analista guía la conversación con las preguntas de la plantilla |
| Días después: documento Word para revisión | Al final de la reunión: Carlos lee en voz alta los criterios capturados |
| Días después: segunda ronda de revisión | 1-2 horas después: resumen estructurado para validar |

El usuario de negocio percibe que la reunión es más productiva y que el analista hace mejores preguntas. No sabe que detrás hay una plantilla YAML y un pipeline de IA. Eso es exactamente lo que queremos.

La guía que Ana López recibe en Meridian no menciona ninguna herramienta. Se llama simplemente "Cómo comunicar lo que necesitas" y tiene tres secciones:

```
ANTES DE LA REUNIÓN
→ Piensa en el problema, no en la solución
  Bien:  "Perdemos tiempo buscando facturas antiguas"
  Menos: "Necesitamos un filtro de facturas con fechas"

EN LA REUNIÓN
→ Te haremos preguntas específicas. Son para entenderte mejor,
  no para complicar las cosas.

DESPUÉS DE LA REUNIÓN
→ Recibirás un resumen estructurado en 1-2 días para validar.
→ Una respuesta rápida evita semanas de retraso más adelante.
```

#### Incorporación del equipo técnico y QA

El equipo técnico recibe una sesión específica de sesenta minutos con dos objetivos: cómo leer los artefactos generados para entender el contexto funcional completo, y cómo usar la matriz de trazabilidad del Capítulo 11 para navegar desde un bug hasta el requisito que lo originó.

Lucía, la QA lead de Meridian, recibe además una sesión de noventa minutos centrada en tres cosas: cómo revisar los test cases generados, qué criterios usar para aprobarlos o rechazarlos, y cómo integrar los scripts Gherkin generados con su framework de automatización.

La observación de Lucía al terminar esa sesión resume perfectamente la dinámica de adopción del equipo de testing: "El pipeline cubre el setenta por ciento que me requería tiempo, y yo me quedo con el treinta por ciento que requiere conocer el negocio. Es un buen reparto."

---

### Fase 4 — Autonomía supervisada (mes 7 en adelante)

En esta fase el sistema funciona con mínima intervención manual. El foco pasa de la adopción al gobierno —que veremos en el Capítulo 14—, pero quedan dos actividades propias de la adopción que no terminan nunca.

**Comunicación interna continua.** Los éxitos del sistema deben comunicarse de forma visible pero sin exagerar. El modelo que funciona en Meridian es una actualización cada dos semanas en el canal del equipo:

```
Semana 10: "El validador ha detectado 23 ambigüedades en los últimos
dos sprints antes de que llegaran al refinamiento. 7 habrían generado
cambios de alcance mid-sprint según el historial. Los números del
sistema están donde esperábamos que estuvieran."

Semana 14: "Primera sprint donde el 100% de las historias tenían
criterios de aceptación completos desde el inicio. El equipo de QA
reporta que el tiempo de diseño de tests ha bajado a la mitad."
```

Tres frases. Datos reales. Sin hype.

**Incorporación de nuevos miembros.** Cuando se incorpora alguien nuevo al equipo, recibe la sesión de noventa minutos con el champion en su primera semana. El sistema es parte del onboarding, no un extra que se aprende después.

---

## Los materiales de adopción

### Para analistas funcionales: la guía de referencia rápida

Un documento de una página que cabe en la pantalla sin scroll. No un manual: una referencia que se consulta en los primeros usos.

```
┌─────────────────────────────────────────────────────────────┐
│ GUÍA RÁPIDA — Pipeline AI Funcional                         │
│ Champion: [nombre] · Dudas: #canal-pipeline-ai              │
├─────────────────────────────────────────────────────────────┤
│ EL FLUJO EN 5 PASOS                                         │
│                                                             │
│ 1. RELLENAR la plantilla YAML tras la reunión               │
│    Campos mínimos: id, titulo, actor, descripcion,          │
│    evento_disparador, criterios_aceptacion (≥1), excepciones│
│                                                             │
│ 2. VALIDAR antes de cambiar estado a 'en-revision'          │
│    python orchestrator.py --req REQ-XXX --dry-run           │
│    Si hay BLOQUEANTEs → corregir antes de continuar         │
│    Si hay solo ADVERTENCIAS → documentar y continuar        │
│                                                             │
│ 3. GENERAR cuando estado = 'validado'                       │
│    python orchestrator.py --req REQ-XXX                     │
│    Tiempo estimado: 30-90 segundos                          │
│                                                             │
│ 4. REVISAR el JSON antes de aprobar (2 minutos)             │
│    □ ¿El actor es correcto?                                 │
│    □ ¿Los criterios reflejan lo que pidió el negocio?       │
│    □ ¿Las tareas técnicas tienen sentido?                   │
│    □ ¿La estimación de story points es razonable?           │
│                                                             │
│ 5. APROBAR para push a Jira                                 │
│    Seleccionar [A] en el gate de aprobación                 │
├─────────────────────────────────────────────────────────────┤
│ CUÁNDO RECHAZAR EL OUTPUT                                   │
│                                                             │
│ ✗ El actor no es el correcto o es demasiado genérico        │
│ ✗ Un criterio AC no es verificable                          │
│ ✗ Las tareas técnicas mezclan capas (front + back juntos)   │
│ ✗ La estimación es claramente incorrecta (>13 o <1)         │
│ ✗ Hay términos que no están en el glosario del proyecto     │
├─────────────────────────────────────────────────────────────┤
│ SI ALGO FALLA                                               │
│ 1. Captura el error                                         │
│ 2. Crea issue en el proyecto [pipeline-ai] con el REQ-ID    │
│ 3. Crea los artefactos manualmente como siempre             │
│    El pipeline es una ayuda, no un bloqueante               │
└─────────────────────────────────────────────────────────────┘
```

### Para el equipo técnico y QA: el contrato de artefactos

Una página que explica qué pueden esperar en los artefactos generados por el pipeline y cómo interpretarlos:

```
CÓMO LEER LOS ARTEFACTOS GENERADOS POR EL PIPELINE

HISTORIAS DE USUARIO
→ El campo 'Requisito Origen' siempre tiene el ID del REQ que originó
  la historia. Úsalo para consultar el YAML completo si necesitas
  más contexto que el que cabe en la historia.
→ Los criterios de aceptación en formato Dado/Cuando/Entonces son
  la fuente de verdad para los test cases. Si la implementación no
  cumple el 'Entonces', es un bug funcional, no una diferencia
  de interpretación.
→ Las tareas técnicas tienen el campo 'capa'. Los links 'blocks'
  entre tareas indican el orden recomendado de implementación.

TEST CASES (en Xray)
→ Los test cases con label 'automatizable' tienen un script Gherkin.
  Importarlo directamente al framework reduce el tiempo de scripting.
→ Los casos de contorno (label 'contorno') son los valores límite.
  No saltárselos aunque parezcan obvios.

CUANDO EL ARTEFACTO PARECE INCORRECTO
→ Antes de modificarlo en Jira, comenta con el prefijo [PIPELINE-FEEDBACK]
→ El champion revisa estos comentarios semanalmente para mejorar los prompts.
→ Modifica el artefacto en Jira para que el sprint no se bloquee.
```

---

## El argumento para la dirección

David Sanz necesita un argumento de negocio, no técnico. Este es el resumen de tres minutos que funciona en organizaciones como Meridian:

---

*Desde que un usuario de negocio nos da un requisito hasta que hay historias en Jira listas para el sprint, pasan entre 2 y 5 días de trabajo de análisis. De ese tiempo, aproximadamente el 60% es trabajo mecánico: redactar documentos, copiar información entre sistemas, crear manualmente épicas, historias y tareas en Jira.*

*Además, entre el 20% y el 30% de los bugs que llegan a producción tienen como causa raíz un requisito ambiguo o incompleto que nadie detectó a tiempo. En Meridian, eso representa aproximadamente 250.000 euros anuales entre trabajo mecánico y bugs funcionales.*

*Lo que proponemos es automatizar el 60% del trabajo mecánico con IA para que los analistas dediquen ese tiempo al trabajo de valor: entender el negocio, detectar ambigüedades y guiar al equipo. Añadimos también una capa de validación automática que detecta ambigüedades antes de que el requisito entre al sprint.*

*El impacto esperado en 6 meses: reducción del 60% en tiempo de creación de artefactos Jira, reducción del 40% en bugs por ambigüedad funcional, trazabilidad completa sin coste de mantenimiento manual.*

*El coste: dos meses de configuración y piloto con un analista, sin nuevas licencias de software en las fases iniciales, y sin cambios en el proceso visible para los usuarios de negocio.*

---

Los tres números que más impactan en la dirección son el porcentaje de reducción de tiempo, el porcentaje de reducción de bugs y la ausencia de cambios visibles para el negocio. La dirección no quiere gestionar la resistencia del negocio: si el proceso con el usuario es igual que antes, ese problema desaparece.

---

## Las cinco trampas de la adopción

Después de observar varios procesos de adopción similares, estos son los patrones que hacen fracasar las iniciativas:

**Trampa 1: Empezar con el proyecto más importante.** El primer proyecto siempre tiene más fricción de la esperada. Si ese proyecto es crítico, cualquier problema en el pipeline se convierte en un argumento para abandonar la iniciativa. El piloto debe ser prescindible.

**Trampa 2: Automatizar antes de que la plantilla esté madura.** Si los analistas empiezan a usar el sistema y los resultados del pipeline son pobres porque la plantilla está incompleta o el glosario es escueto, la primera impresión es negativa y es muy difícil recuperarla. La plantilla y el glosario deben estar validados con datos reales antes de mostrar el pipeline al equipo.

**Trampa 3: No comunicar los resultados internamente.** Los éxitos del piloto deben comunicarse de forma visible. Si los resultados no se comunican, el esfuerzo del piloto es invisible y no genera el impulso necesario para la Fase 3.

**Trampa 4: Tratar el pipeline como un producto terminado.** El pipeline va a generar output incorrecto en casos que nadie anticipó. Si el equipo espera perfección y encuentra errores, la reacción es de rechazo. Si entiende que el pipeline es una herramienta en evolución que mejora con su feedback, los errores se convierten en contribuciones al sistema.

**Trampa 5: Formar a todos a la vez.** Como dijimos antes: la adopción funciona persona a persona. No en grupo.

---

## Lo que funciona en la práctica

En Meridian, el momento de inflexión no fue la demo ni la sesión práctica. Fue la primera vez que María García llegó al planning con los criterios de aceptación ya en el tablero, impresos desde Jira, y el equipo pudo votar story points en ocho minutos en lugar de veinte.

Nadie había pedido eso explícitamente. Era una consecuencia natural de que los criterios llegaran bien formados al sprint. Pero ese momento —concreto, visible, experimentado por todo el equipo— fue el que convirtió el sistema de "el experimento de Carlos" a "nuestra forma de trabajar".

La formación más eficaz no es un curso de prompt engineering. Es una sesión práctica de dos horas donde el analista ve cómo su propio requisito se transforma automáticamente en tres historias, dos tareas técnicas y seis casos de prueba. Esa demostración vale más que cualquier presentación estratégica.

El usuario de negocio que más resistencia inicial mostró en Meridian fue Ana López. Su preocupación no era el proceso de captura; era que "la IA no puede entender las reglas del negocio financiero tan bien como nosotros". Tenía razón. Pero cuando vio que el sistema detectó automáticamente que el criterio "el sistema debe ser rápido" no era verificable y le propuso sustituirlo por "el sistema debe devolver resultados en menos de 2 segundos para conjuntos de hasta 10.000 registros", cambió de posición. No porque la IA entendiera el negocio, sino porque le ayudaba a articular lo que ella ya sabía pero no había expresado con la precisión necesaria.

---

## Tres puntos clave

1. La resistencia al cambio es legítima y tiene respuestas concretas para cada perfil. El plan de adopción es, en gran medida, la secuencia en la que se dan esas respuestas.

2. El valor debe ser visible antes de que el proceso sea perfecto. Un requisito real del equipo transformado en artefactos en cuarenta y siete segundos vale más que cualquier presentación estratégica.

3. La adopción que dura no es la que se implanta de golpe, sino la que avanza persona a persona, con métricas reales, comunicación honesta y espacio para que el equipo contribuya a mejorar el sistema.

---

## Pregunta de reflexión para el equipo

¿Cuál es el analista de tu equipo que más ha sufrido el trabajo mecánico en los últimos seis meses? ¿Por qué no es él el champion del piloto?

---

*El sistema ya está adoptado. El equipo lo usa. Las métricas mejoran. Pero ¿qué ocurre cuando el pipeline empieza a degradarse silenciosamente? ¿Quién detecta que los prompts ya no producen el mismo output que hace seis meses? ¿Quién decide cuándo escalar la autonomía de la IA? Esas preguntas son el territorio del siguiente capítulo.*
