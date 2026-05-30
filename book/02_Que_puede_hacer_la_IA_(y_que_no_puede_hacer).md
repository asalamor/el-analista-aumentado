# Capítulo 2. Qué puede hacer la IA (y qué no puede hacer)

---

*En este capítulo aprenderás:*
- *Cómo funcionan los modelos de lenguaje explicado sin matemáticas, en términos que un analista funcional puede usar para trabajar con ellos de forma eficaz*
- *Qué hace bien la IA en el contexto del análisis funcional, y por qué*
- *Qué no hace bien todavía, y cómo diseñar el proceso para que esas limitaciones no se conviertan en errores*
- *Por qué el requisito es el punto de partida del sistema, y no la IA*

---

## La pregunta de María

Dos semanas después de que David Sanz anunciara en la reunión de equipo que Meridian iba a implantar un sistema de IA para el análisis funcional, María García se acercó a Carlos Ruiz con una pregunta directa.

"¿Esto nos va a reemplazar?"

Carlos tardó un momento en responder, no porque no supiera la respuesta, sino porque quería darle la correcta en lugar de la tranquilizadora.

"No", dijo. "Pero va a cambiar lo que hacemos. Y para entender cómo va a cambiar, necesitas entender qué puede hacer esta herramienta y qué no puede hacer. Porque si no lo entiendes, o te asusta más de lo que debes o confías más de lo que debes. Los dos errores son caros."

Esa conversación es el punto de partida de este capítulo. Antes de tocar ninguna plantilla, ningún prompt y ninguna línea de código, necesitamos entender con precisión qué herramienta estamos usando. No a nivel técnico —no necesitas saber cómo se entrena un modelo de lenguaje para usarlo bien—, pero sí a nivel funcional: qué puede hacer, qué no puede hacer, y por qué.

---

## Qué es un modelo de lenguaje, sin matemáticas

Un modelo de lenguaje grande —un LLM, por sus siglas en inglés— es un sistema entrenado sobre cantidades enormes de texto para aprender los patrones del lenguaje: qué palabras suelen aparecer juntas, qué estructuras son habituales en determinados contextos, cómo se construye un argumento, cómo se formula una pregunta técnica, cómo se redacta una historia de usuario.

La metáfora más útil que conozco para un analista funcional es esta: imagina un colaborador que ha leído millones de documentos de todo tipo —requisitos, historias de usuario, especificaciones técnicas, manuales, código, libros, artículos— y ha interiorizado los patrones de todos ellos. Cuando le pides que genere una historia de usuario a partir de un requisito, no "entiende" el requisito en el sentido en que lo entendería una persona. Lo que hace es identificar el patrón de transformación que existe entre los requisitos y las historias de usuario que ha visto, y lo aplica a tu requisito concreto.

Esto explica dos cosas a la vez: por qué los LLMs son extraordinariamente buenos en tareas de transformación estructurada —tomar algo con una forma y producir algo con otra forma distinta— y por qué fallan de maneras específicas y predecibles cuando el input no tiene la estructura que el modelo necesita para aplicar ese patrón.

No es inteligencia en el sentido humano. Es reconocimiento de patrones a una escala y una velocidad que ningún humano puede igualar. Y en el contexto del análisis funcional, ese reconocimiento de patrones es exactamente lo que necesitamos para automatizar el trabajo mecánico.

> 💡 **Idea clave**
>
> Un modelo de lenguaje no "entiende" tu requisito: reconoce el patrón de tu requisito y lo transforma siguiendo los patrones que ha aprendido de millones de ejemplos similares. Esta distinción no es filosófica: tiene consecuencias prácticas directas sobre cómo debes escribir los requisitos y qué puedes esperar del output.

---

## Lo que la IA hace bien en este contexto

Hay cuatro capacidades de los modelos de lenguaje actuales que son especialmente relevantes para el análisis funcional. Las cuatro están en la base del sistema que construiremos en este libro.

### Transformar estructura en estructura

Esta es la capacidad más importante para nuestro caso de uso. Un LLM bien configurado puede tomar un requisito escrito en el formato de cinco bloques que describe el Capítulo 4 y producir una historia de usuario en formato Jira, con criterios de aceptación en Dado/Cuando/Entonces, flujo principal, flujos de error y estimación en story points. No porque "entienda" la funcionalidad, sino porque ha visto tantos ejemplos de esa transformación que puede aplicarla con consistencia y precisión.

La clave operativa es que la transformación funciona bien cuando la estructura del input es clara y la estructura del output está bien definida. Cuando el input es ambiguo o el output no está especificado con precisión, la calidad cae drásticamente. Más sobre esto en la sección de limitaciones.

### Seguir instrucciones estructuradas complejas

Los modelos de lenguaje de última generación son notablemente buenos siguiendo instrucciones largas y complejas con múltiples condiciones. Puedes pedirle a un LLM que genere una historia de usuario usando el vocabulario exacto del glosario del proyecto, respetando las restricciones de formato de tu organización, añadiendo el campo personalizado que Jira requiere, y alertando si detecta alguna ambigüedad en el input. Todo en la misma llamada. Y lo hará consistentemente, sin olvidarse de ninguna instrucción, sin variar el comportamiento según el día de la semana o el nivel de fatiga.

Esta capacidad es la que hace posible el sistema de validación automática del Capítulo 7: un prompt que aplica un checklist de quince criterios de calidad a cada requisito, sin excepciones, sin olvidos, y produciendo un informe estructurado con los problemas encontrados y cómo corregirlos.

### Ser consistente a escala

Un analista funcional que procesa veinte requisitos en una semana aplica su criterio de forma ligeramente distinta en el primero y en el último. Está más concentrado por la mañana, más cansado a última hora del viernes, más riguroso cuando el proyecto es nuevo y más permisivo cuando lleva meses con el mismo backlog. Eso es humano y comprensible, pero tiene un coste en la consistencia de los artefactos.

Un LLM aplica exactamente las mismas instrucciones al requisito número uno y al número doscientos. El criterio de validación es idéntico para una historia del sprint 1 y para una del sprint 15. La terminología del glosario se respeta igual en enero y en septiembre. A escala, esa consistencia produce una homogeneidad en los artefactos que es muy difícil de lograr con proceso manual, por riguroso que sea el equipo.

### Recuperar y conectar información dispersa

Cuando el sistema RAG que describe el Capítulo 10 está activo, el LLM trabaja con acceso al repositorio completo de requisitos del proyecto. Esto le permite hacer algo que un analista individual raramente hace por falta de tiempo: antes de generar una nueva historia, revisar si existe ya una historia similar, verificar si las reglas de negocio del nuevo requisito son consistentes con las de los requisitos aprobados en los últimos tres meses, y detectar si algún criterio de aceptación nuevo contradice uno ya validado.

Esta capacidad no es perfecta —tiene sus propios errores y limitaciones, que discutiremos— pero a escala de proyectos medianos y grandes produce una coherencia entre requisitos que es prácticamente imposible de mantener manualmente.

---

## Lo que la IA no hace bien

Aquí está la parte del capítulo que más importa para evitar los errores más caros. Las limitaciones de los LLMs en el contexto del análisis funcional son específicas y predecibles. Conocerlas de antemano permite diseñar el proceso para compensarlas.

### No inventa lo que no está

Si el requisito no especifica qué debe ocurrir cuando el rango de fechas supera 365 días, el LLM no va a inventar el comportamiento correcto. Va a hacer una de tres cosas: inventar algo plausible pero incorrecto, marcar el campo como pendiente, o generar un criterio de aceptación vacío. Las tres son problemáticas, pero la primera es la más peligrosa porque produce un artefacto que parece completo sin serlo.

Este comportamiento tiene un nombre en el ecosistema de IA: alucinación. Los LLMs generan texto fluido y confiante incluso cuando la información que necesitan para ser correctos no está disponible. En el contexto del análisis funcional, una alucinación no es una curiosidad técnica: es un criterio de aceptación inventado que llega al sprint, se implementa y genera un bug que nadie esperaba porque nadie lo definió.

La solución a este problema no es desconfiar de la IA: es estructurar el requisito de forma que no haya lagunas que la IA tenga que rellenar inventando. El sistema de validación del Capítulo 7 existe precisamente para detectar esas lagunas antes de que el requisito entre al pipeline de generación.

> ⚠️ **Error frecuente**
>
> El error más caro al empezar a usar LLMs en análisis funcional es asumir que el modelo "completará" la información que falta en el requisito de forma correcta. No lo hará de forma fiable. Si el input tiene lagunas, el output tendrá errores. La validación antes de la generación no es opcional: es lo que separa un pipeline útil de uno peligroso.

### No detecta contradicciones sutiles sin contexto

Un LLM puede detectar contradicciones obvias dentro de un único requisito: si el mismo documento dice en un párrafo que solo los gestores pueden exportar facturas y en otro que cualquier usuario puede hacerlo, el modelo lo detectará. Pero no puede detectar de forma fiable contradicciones entre un requisito nuevo y otro aprobado hace cuatro meses que está en un documento diferente que el modelo no ha visto.

Este es exactamente el problema que resuelve la arquitectura RAG del Capítulo 10: dar al modelo acceso al repositorio histórico antes de generar, para que pueda cruzar el nuevo requisito contra los aprobados anteriormente. Pero incluso con RAG, la detección de contradicciones sutiles requiere supervisión humana. El sistema puede alertar de posibles conflictos; decidir si son conflictos reales es trabajo del analista.

### No puede sustituir el juicio experto sobre el negocio

El LLM no sabe qué importa para el negocio de Meridian. No sabe que el módulo de facturación tiene un SLA contractual con los proveedores que afecta a los tiempos de respuesta de la búsqueda. No sabe que el Responsable Financiero tiene una regla no escrita de no delegar la aprobación de facturas superiores a diez mil euros. No sabe que el equipo de desarrollo tuvo problemas en el sprint anterior con la paginación y que cualquier nuevo requisito que la involucre necesita tratamiento especial.

Todo ese conocimiento tácito vive en la cabeza de Carlos. Y mientras no esté escrito en algún lugar que el sistema pueda leer —en el glosario, en los comentarios del requisito, en las reglas de negocio globales—, el LLM no puede usarlo.

Esta limitación es, paradójicamente, una de las razones por las que el modelo mejora con el uso. Cada vez que el equipo documenta una regla de negocio que antes estaba implícita, cada vez que el glosario se actualiza con un nuevo término, cada vez que un criterio de aceptación captura un comportamiento de error que antes nadie escribía, el sistema tiene más contexto correcto para trabajar. La calidad del output crece con la calidad del repositorio.

### No trabaja bien con requisitos vagos

Este es el punto más importante del capítulo, y el que conecta directamente con el trabajo de los capítulos siguientes.

Un LLM produce outputs de calidad proporcional a la calidad del input. Con un requisito vago —"el sistema debe permitir al usuario gestionar sus facturas de forma eficiente"— el modelo generará una historia vaga, criterios de aceptación vagos y test cases que no verifican nada concreto. Técnicamente correcto en forma, funcionalmente inútil en fondo.

Esto no es un defecto del modelo: es una consecuencia directa de cómo funciona. El modelo transforma el patrón de tu input en el patrón de tu output. Si el input no tiene estructura, el output no puede tenerla.

La paradoja es que el LLM puede ayudarte a escribir mejores requisitos —puede detectar cuándo un requisito está incompleto, puede sugerir campos que faltan, puede reformular criterios ambiguos— pero solo si el input tiene suficiente estructura para que el modelo sepa qué buscar. Un blank canvas no funciona.

> 💡 **Idea clave**
>
> La calidad del output del pipeline es directamente proporcional a la calidad del input. Esto no es una limitación técnica superable: es una consecuencia matemática de cómo funcionan los modelos de lenguaje. Invertir en la calidad del requisito no es trabajo previo al pipeline: es parte integral del pipeline.

---

## El experimento del requisito vago

Para hacer tangible la diferencia entre trabajar con la IA con un requisito vago y con uno estructurado, hagamos el experimento que Carlos hizo en Meridian antes de convencer a David de implantar el sistema.

Carlos tomó el requisito original de Ana para el filtrado de facturas, tal y como llegó de la reunión:

> *"Los gestores de facturación necesitan poder buscar facturas por fechas para agilizar el trabajo del cierre mensual."*

Y lo pasó directamente al modelo de lenguaje con la instrucción de generar una historia de usuario lista para Jira.

El resultado fue este:

---

**Historia generada desde el requisito vago:**

*Como gestor de facturación, quiero poder buscar facturas por fechas para agilizar el trabajo del cierre mensual.*

**Criterios de aceptación:**
- El sistema permite buscar facturas por fecha de inicio y fecha de fin.
- Los resultados se muestran en pantalla.
- La búsqueda es rápida y eficiente.

---

Técnicamente, tiene el formato correcto. Una historia, tres criterios. Pero ninguno de esos criterios es verificable. "Los resultados se muestran en pantalla" no define nada: ¿cuántos resultados? ¿en qué orden? ¿con qué campos? "La búsqueda es rápida y eficiente" es una opinión, no un criterio. Y no hay ninguna mención al rango máximo de 365 días, al comportamiento cuando no hay resultados, ni al mensaje de error cuando el rango es demasiado amplio, porque esa información no estaba en el requisito de entrada.

Luego Carlos tomó el mismo requisito, lo transformó en el formato de cinco bloques de la plantilla AI-ready, y pasó esa versión estructurada al mismo modelo con los mismos prompts.

El resultado fue lo que vimos en la Introducción: una historia con tres criterios de aceptación verificables, cuatro tareas técnicas descompuestas por capa, nueve test cases incluyendo los valores límite que nadie habría escrito manualmente, y trazabilidad completa registrada en el grafo.

La diferencia no está en el modelo. Está en el input.

| | Requisito vago | Requisito AI-ready |
|---|---|---|
| **Criterios de aceptación** | 3 criterios no verificables | 3 criterios verificables con datos concretos |
| **Flujos de error** | Ninguno | 2 flujos documentados |
| **Casos de contorno** | Ninguno | 4 casos (límite superior, inferior, exacto, negativo) |
| **Test cases generados** | 0 útiles | 9 ejecutables |
| **Tiempo de revisión humana** | 45 minutos (reescribir todo) | 10 minutos (revisar y aprobar) |
| **Issues en Jira** | Historia sin valor | Historia + 4 tareas listas para sprint |

Este experimento es el argumento más convincente para el proceso que describe este libro. No porque la IA sea mágica, sino porque la combinación de un requisito bien estructurado con un LLM bien configurado produce en segundos lo que un analista habría tardado horas en producir manualmente, y lo produce con una consistencia y una completitud que el trabajo manual raramente alcanza.

> 🛠️ **En la práctica**
>
> Antes de invertir tiempo en configurar el pipeline técnico, haz este experimento con tus propios requisitos. Toma un requisito reciente de tu proyecto —uno real, no uno de ejemplo—, pásalo al modelo tal como está, y observa el output. Luego estructura ese mismo requisito siguiendo los cinco bloques del Capítulo 4 y vuelve a pasarlo. La diferencia entre los dos outputs es la demostración más eficaz que puedes hacer ante tu equipo de por qué la estructura del requisito importa.

---

## El punto de partida es el requisito, no la IA

Hay una confusión habitual cuando los equipos empiezan a explorar la IA para el análisis funcional: asumir que la IA es el punto de partida del proceso, y que el resto se construye alrededor de ella. Esta confusión lleva a proyectos que empiezan por evaluar modelos, comparar proveedores y construir integraciones técnicas antes de haber definido qué estructura tendrán los requisitos que alimentarán esas integraciones.

El resultado es casi siempre el mismo: integraciones técnicamente correctas que producen outputs de baja calidad porque el input nunca se diseñó para ser procesado por IA.

El modelo de este libro está construido al revés. El punto de partida es el requisito. Antes de tocar ninguna API, antes de escribir ningún prompt, antes de configurar ninguna integración con Jira, hay que resolver dos preguntas:

¿Qué información debe contener un requisito para que el pipeline pueda generar artefactos correctos a partir de él?

¿Cómo debe estructurarse esa información para que el LLM pueda procesarla sin ambigüedad?

La respuesta a esas dos preguntas es la plantilla de cinco bloques del Capítulo 4 y el glosario estructurado del Capítulo 5. Solo cuando esas dos piezas están definidas tiene sentido construir los prompts del pipeline. Y solo cuando los prompts están validados con requisitos reales tiene sentido construir la integración técnica con Jira.

Este orden importa porque cambia dónde ocurren los errores. Si construyes la integración primero y el formato del requisito después, los errores de diseño del formato son caros de corregir porque ya tienes código que depende de él. Si construyes el formato primero, los errores se detectan antes de que haya código, y el coste de corregirlos es una conversación en lugar de una refactorización.

> 💡 **Idea clave**
>
> La IA no es el punto de partida del sistema: es el motor que procesa la materia prima que el analista produce. Diseñar bien esa materia prima —el requisito estructurado— es la inversión con mayor retorno de todo el proceso. Un prompt mediocre sobre un requisito excelente produce mejores resultados que un prompt excelente sobre un requisito mediocre.

---

## Una nota sobre los modelos disponibles

Este libro usa Claude de Anthropic como modelo de referencia para todos los prompts y ejemplos. Todos los outputs que aparecen en los capítulos siguientes son resultados reales obtenidos con Claude ejecutando los prompts del Apéndice B sobre requisitos del proyecto Meridian.

Esto no significa que Claude sea la única opción ni necesariamente la mejor para tu contexto. GPT-4o de OpenAI produce resultados comparables con los mismos prompts y ajustes menores. Gemini de Google tiene capacidades similares para tareas de análisis estructurado. El mercado de modelos de lenguaje evoluciona con rapidez y las diferencias entre los principales proveedores son menores hoy de lo que eran hace un año.

Lo que sí importa en la elección del modelo para este caso de uso es una capacidad específica: la capacidad de seguir instrucciones estructuradas largas y complejas de forma consistente, produciendo siempre JSON válido como output. No todos los modelos la tienen en el mismo grado, y es la capacidad sobre la que descansa todo el pipeline. En el momento de escribir este libro, Claude y GPT-4o tienen el mejor rendimiento en esta dimensión concreta para el volumen y tipo de instrucciones que usa el pipeline.

La arquitectura del sistema está diseñada para que el modelo sea intercambiable: una sola variable de configuración determina qué proveedor se usa, y los prompts funcionan con ajustes menores en cualquiera de los principales modelos del mercado. Si mañana aparece un modelo que supera a los actuales en este tipo de tareas, cambiar el pipeline para usarlo es cuestión de minutos.

---

## Lo que funciona en la práctica

La pregunta que con más frecuencia hacen los analistas que se acercan a estas herramientas por primera vez no es técnica. Es esta: ¿puedo fiarme del output?

La respuesta correcta no es sí ni no. Es: puedes fiarte del output cuando el input es correcto y el proceso tiene un gate de revisión humana. No puedes fiarte del output si asumes que el modelo siempre hace lo correcto sin supervisión.

La forma más rápida de desarrollar la confianza correcta —ni excesiva ni insuficiente— es usar el sistema durante dos semanas sobre requisitos reales con el gate de aprobación activo. Revisar cada output antes de que llegue a Jira. Anotar los tipos de errores que aparecen. Identificar en qué campos el modelo es consistentemente bueno y en cuáles necesita más supervisión.

Lo que invariablemente ocurre en esas dos semanas es que los analistas descubren que los errores del modelo son predecibles: siempre falla en los mismos tipos de casos, con los mismos tipos de lagunas en el input. Esa predictibilidad es útil porque permite diseñar el checklist de validación —que es exactamente lo que hace el Capítulo 7— para detectar esos casos antes de que entren al pipeline.

La confianza en el sistema no es ciega: es calibrada. Y se calibra con uso real sobre problemas reales.

---

*Los tres puntos clave de este capítulo:*

1. Un modelo de lenguaje transforma patrones de input en patrones de output. Es extraordinariamente bueno en tareas de transformación estructurada, seguimiento de instrucciones complejas y consistencia a escala. No es un sistema de razonamiento: no inventa lo que no está, no detecta contradicciones sin contexto, y produce outputs de calidad proporcional a la calidad del input.

2. La limitación más importante para el análisis funcional es la sensibilidad al input: un requisito vago produce artefactos vagos e inutilizables. Un requisito estructurado produce artefactos correctos, completos y listos para revisión. Esta no es una limitación superable: es la razón por la que el diseño del requisito es la parte más importante del sistema.

3. El punto de partida del sistema es el requisito, no la IA. Diseñar primero el formato del requisito y después el pipeline que lo procesa es el orden correcto. Invertirlo lleva a integraciones técnicamente correctas que producen outputs de baja calidad.

---

*Pregunta para llevar a tu próxima reunión de equipo:*

Si tomamos un requisito real de nuestro backlog y lo pasamos a un modelo de lenguaje tal como está, ¿qué nos dice el output sobre la calidad del requisito de entrada?
