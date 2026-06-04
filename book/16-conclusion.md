# Conclusión

---

Es martes por la tarde. Carlos Ruiz tiene Jira abierto en una pantalla y el terminal en la otra.

Hace exactamente dieciocho meses, esta escena significaba dos horas por delante: copiar campos de un documento Word a formularios de Jira, inventar criterios de aceptación que nadie había validado, crear test cases que cubrían el flujo feliz y dejaban los flujos de error para que los descubriera alguien en producción. Un trabajo que Carlos hacía bien —siempre lo había hecho bien— pero que le dejaba con la sensación de que su valor no estaba ahí.

Hoy la escena es diferente. Carlos escribe en el terminal:

```
python orchestrator.py --req REQ-041
```

Cuarenta y siete segundos después, tiene una historia de usuario, cuatro tareas técnicas distribuidas por capa y nueve test cases listos para revisión. Revisa el output durante cuatro minutos, aprueba, y el pipeline empuja todo a Jira.

Las dos horas de antes se han convertido en cinco minutos. Las otras una hora y cincuenta y cinco minutos las dedica ahora a la reunión de esta tarde con Ana López, donde van a hablar del nuevo módulo de conciliación de pagos. Una conversación real sobre un problema de negocio real, sin la presión de tener que traducir después todo lo que Ana diga en campos de un formulario mientras intenta recordar lo que ha dicho.

---

## Lo que ha cambiado, y lo que no

El pipeline ha cambiado muchas cosas en Meridian. El tiempo de ciclo funcional. La cobertura de los test cases. El número de bugs que llegan a producción con causa raíz en un requisito ambiguo. La duración del planning poker. La confianza de Lucía al cerrar un sprint sabiendo qué se ha probado y por qué.

Pero hay algo que no ha cambiado, y que nunca cambiará: el trabajo de análisis funcional sigue requiriendo a alguien que entienda el negocio, que haga las preguntas correctas, que detecte la contradicción que el usuario de negocio no ha articulado todavía, que sienta cuándo un requisito parece completo pero esconde una decisión que nadie ha tomado.

Ese trabajo es el de Carlos. El pipeline no lo hace. Lo que hace el pipeline es devolvérselo.

Durante años, el análisis funcional convirtió a los analistas en secretarios de lujo: personas con capacidad de comprensión estratégica dedicando la mitad de su jornada a rellenar formularios. El pipeline invierte esa ecuación. La IA hace el trabajo de secretaría; el analista hace el trabajo de análisis.

Es un cambio simple de enunciar y difícil de implantar. Este libro ha intentado describir exactamente cómo hacerlo.

---

## El camino que hemos recorrido juntos

La Parte I partió de un diagnóstico incómodo: el proceso de análisis funcional en la mayoría de organizaciones Agile está roto de una forma que nadie nombra en voz alta. No roto de forma espectacular —los sprints avanzan, los productos se entregan, los proyectos terminan— sino roto de forma silenciosa: demasiado tiempo en trabajo mecánico, demasiada ambigüedad que llega al sprint sin ser detectada, demasiados bugs cuya causa raíz es un requisito que nadie revisó con suficiente atención.

El capítulo 2 desmitificó lo que la IA puede y no puede hacer en este contexto. No puede entender el negocio. No puede detectar lo que el usuario de negocio no ha dicho. No puede compensar un requisito mal capturado. Pero puede transformar un requisito bien estructurado en artefactos consistentes con una velocidad y una exhaustividad que ningún analista puede igualar trabajando manualmente. Esa combinación —el analista captura, la IA transforma— es la que funciona.

La Parte II construyó las tres piezas fundacionales del sistema: la plantilla de requisito AI-ready con sus cinco bloques, el glosario estructurado como contrato terminológico activo del pipeline, y el Event Storming como técnica de captura que produce directamente los elementos que la plantilla necesita. Estas tres piezas son la base sobre la que descansa todo lo demás. Sin ellas, los prompts más sofisticados del mundo generan artefactos inconsistentes.

La Parte III construyó el pipeline completo: la validación automática que detecta ambigüedades antes de que lleguen al sprint, la generación de artefactos Jira en cuatro llamadas encadenadas, la generación de test cases que cubre flujos positivos, negativos y de contorno, la arquitectura RAG que da al pipeline memoria del repositorio, la trazabilidad automática que responde en cuarenta segundos preguntas que antes llevaban dos horas, y el orquestador que une todo en un único comando ejecutable.

La Parte IV tradujo el sistema técnico al sistema humano: cómo llevar el pipeline a un equipo real sin que la resistencia al cambio lo aborte antes de que produzca valor, cómo gobernarlo para que no se degrade silenciosamente, y cómo medir su impacto con la honestidad suficiente para que el argumento sea creíble ante la dirección.

---

## Las tres cosas que el libro no ha dicho, pero debería decir

Hay tres cosas que no aparecen en ningún capítulo y que merecen un lugar aquí.

**La primera es que el sistema falla.** Falla más de lo que los ejemplos del libro sugieren. REQ-039 y el incidente de «conciliación» del capítulo 14 son reales, pero son la punta del iceberg. Los primeros meses hay más fallos de los que se muestran en el libro: prompts que generan estimaciones incorrectas, glosarios con huecos que la IA rellena con su propio criterio, test cases que cubren el criterio de aceptación pero ignoran un caso de contorno obvio. El sistema mejora con el tiempo y con el uso, pero el punto de partida es más rugoso de lo que sugiere la narrativa lineal de Meridian.

La implicación práctica es esta: el gate de aprobación humana no es un paso burocrático que se elimina cuando el sistema madura. Es la garantía estructural de que ningún error del pipeline llega al sprint sin que alguien lo haya visto. Esa garantía vale más que cualquier optimización de velocidad.

**La segunda es que la implantación es más lenta de lo que parece.** El roadmap de cuatro fases del capítulo 3 describe lo que ocurre cuando todo va bien. En la práctica, hay semanas donde el champion está ausente y el sistema funciona en modo piloto automático sin que nadie lo revise. Hay sprints donde la presión del proyecto hace que los analistas creen los issues manualmente porque «no hay tiempo para el pipeline». Hay momentos donde un argumento de dirección amenaza con cancelar el proyecto antes de que haya producido suficiente valor visible.

La implantación real es irregular, con retrocesos y aceleraciones. Lo que hace que finalmente funcione no es el roadmap perfecto sino la persistencia del champion y el respaldo de al menos una persona en la dirección que cree en el proyecto cuando los demás dudan.

**La tercera es que el analista que usa bien este sistema es más valioso, no menos.** El miedo que expresó María García en el capítulo 2 —«¿esto nos va a reemplazar?»— es comprensible pero está mal orientado. La automatización del trabajo mecánico no reduce el valor del analista funcional: lo desplaza hacia el trabajo que siempre debió hacer y que la presión del trabajo mecánico le impedía hacer bien. El analista que domina el sistema del libro es alguien que entiende el negocio, facilita workshops de Event Storming, detecta ambigüedades antes de que lleguen al sprint y gobierna un pipeline que amplifica su trabajo. Eso no es alguien prescindible; es alguien más difícil de reemplazar que antes.

---

## Lo que sigue

El sistema descrito en este libro es el estado del arte en junio de 2025. En dieciocho meses, algunas piezas habrán evolucionado: los modelos de lenguaje serán más capaces, las integraciones con Jira y Confluence serán más directas, y habrá herramientas que automaticen pasos que hoy requieren código personalizado.

Lo que no habrá cambiado es el problema de fondo: el análisis funcional seguirá siendo la disciplina que determina si un sprint produce valor o produce retrabajo. Y la solución de fondo tampoco habrá cambiado: requisitos bien estructurados, un vocabulario compartido, y un equipo que distingue el trabajo que solo pueden hacer ellos del trabajo que puede hacer una máquina.

Ese es el núcleo del modelo. Todo lo demás —los prompts, el YAML, el vector store, el orquestador— son la implementación de ese principio. Las implementaciones cambian; el principio no.

---

## De vuelta al martes por la tarde

Carlos cierra el terminal. Quedan quince minutos para la reunión con Ana López.

Abre el cuaderno donde lleva anotados los tiempos desde el primer día. Mira la última línea: «Mes 18. Tasa de aprobación directa: 91%. Bugs funcionales en producción: 16 (−52% vs. línea base). NPS interno: 8,3.»

Cierra el cuaderno.

Lo que más le importa de esos números no es lo que dicen sobre el pipeline. Es lo que dicen sobre el equipo. Sobre María García, que ahora llega al refinamiento sin miedo. Sobre Lucía, que cierra los sprints con confianza. Sobre Ana López, que en la última reunión llegó con tres preguntas preparadas sobre el comportamiento esperado del sistema en lugar de una descripción genérica de lo que necesitaba.

Sobre David Sanz, que dijo en la última retrospectiva la frase que Carlos tiene subrayada en el cuaderno: «Antes el pipeline era la herramienta de Carlos. Ahora es parte de cómo trabajamos.»

Eso es lo que significa que el sistema haya funcionado. No el ROI del 520%. No la reducción del tiempo de ciclo. No los cuarenta y siete segundos.

Que el equipo no pueda imaginar trabajar sin él.

Carlos recoge el cuaderno, cierra el portátil y va a la reunión con Ana.

Esta vez, las cosas son diferentes.

---

*Fin*
