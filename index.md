# El analista aumentado

**Modelo operativo para transformar el análisis funcional con Inteligencia Artificial**

Este proyecto documenta y prototipa un modelo operativo completo para automatizar la generación de artefactos Agile mediante Inteligencia Artificial: desde la captura estructurada de requisitos hasta la creación de historias, tareas, test cases, análisis de impacto y trazabilidad en producción.

El objetivo no es sustituir al analista funcional, sino reducir el trabajo mecánico que consume tiempo —redacción repetitiva, creación manual de artefactos, duplicidad documental y mantenimiento de trazabilidad— para que el analista pueda dedicar más esfuerzo al trabajo de valor: entender el negocio, detectar ambigüedades, facilitar decisiones y mejorar la calidad funcional antes del desarrollo.

---

## Qué encontrará en este repositorio

El contenido está organizado en dos grandes bloques complementarios:

### 1. Modelo operativo

La carpeta [docs](#docs) contiene la documentación técnica y metodológica del modelo operativo.

Aquí se explica cómo capturar requisitos en formato AI-ready, cómo estructurar el glosario, cómo generar artefactos Jira, cómo producir casos de prueba, cómo construir una arquitectura RAG, cómo mantener la trazabilidad y cómo gobernar el modelo a lo largo del tiempo.

La carpeta [gaps](#gaps) contine puntos adicionales que complementan el análisis, identificados al completar el modelo operativo principal.

La página [resumen-ejecutivo.html](./resumen-ejecutivo.html) ofrece una vista ejecutiva en formato HTML para presentar el modelo a dirección o stakeholders.

### 2. Libro: *El analista aumentado*

La carpeta **book** contiene el libro en capítulos.

El libro presenta el mismo modelo desde una perspectiva narrativa y didáctica, usando un caso de uso recurrente: Empresa Meridian, el módulo de facturación y el requisito REQ-023, “Filtrar facturas por rango de fechas”.

---

## Visión rápida del modelo

El flujo de trabajo propuesto se basa en una idea sencilla:

> La IA no convierte requisitos vagos en buenos artefactos. Convierte requisitos bien estructurados en artefactos listos para revisión.

El modelo parte de requisitos escritos con estructura semántica explícita —YAML, criterios BDD, glosario controlado y reglas de negocio verificables— y los transforma mediante un pipeline de IA en:

* Épicas, historias de usuario, tareas técnicas y subtareas.
* Criterios de aceptación en formato Dado/Cuando/Entonces.
* Casos de prueba funcionales, negativos y de contorno.
* Scripts Gherkin para automatización.
* Matrices de trazabilidad.
* Análisis de impacto ante cambios.
* Registro de relaciones entre requisitos, historias, test cases, Jira y código.

La regla de gobierno principal es:

> **La IA propone; el humano aprueba.**

---
<a id="docs"></a>
## Índice del modelo operativo

### Base conceptual y documental

**1. [Modelo operativo de análisis funcional AI-ready](docs/00_01_modelo_operativo_analisis_funcional_ai_ready.md)**
   Visión inicial del cambio necesario en la captura de requisitos, estructura documental, metodología y proceso end-to-end.

**2. [Orden lógico de implementación](docs/00_02_orden_logico_implementacion.md)**
   Secuencia recomendada para construir el modelo desde las bases documentales hasta la automatización avanzada.

3. [Modelo operativo completo](docs/01_00_modelo_operativo_completo.md)
   Documento de referencia de los doce componentes principales del modelo.

### Fundación del modelo

4. [Taller de plantillas](docs/01_01_taller_de_plantillas.md)
   Diseño de la plantilla de requisito AI-ready y definición de campos obligatorios, recomendados y opcionales.

5. [Glosario estructurado](docs/01_02_glosario_estructurado.md)
   Cómo construir y gobernar el vocabulario oficial del proyecto para evitar inconsistencias terminológicas.

6. [Guía de Event Storming](docs/01_03_guia_event_storming.md)
   Técnica de descubrimiento para transformar conversaciones de negocio en eventos, comandos, actores y requisitos estructurados.

### Núcleo técnico del pipeline

7. [Prompts de generación de Jira](docs/02_04_prompts_generacion_jira.md)
   Prompts para transformar requisitos YAML en épicas, historias, tareas técnicas y subtareas.

8. [Generación automática de test cases](docs/02_05_generacion_test_cases.md)
   Pipeline para generar casos de prueba desde criterios de aceptación y reglas de negocio.

9. [Validación automática de requisitos](docs/02_06_validacion_automatica_requisitos.md)
    Validación de completitud, ambigüedad, contradicciones y calidad funcional antes de generar artefactos.

### Inteligencia avanzada y trazabilidad

10. [Arquitectura RAG para requisitos](docs/03_07_arquitectura_rag_requisitos.md)
    Diseño de la memoria semántica del pipeline para recuperar contexto del repositorio funcional.

11. [Detección de impacto de cambios](docs/03_08_deteccion_impacto_cambios.md)
    Cómo identificar historias, tareas y test cases afectados cuando cambia un requisito.

12. [Matriz de trazabilidad automática](docs/03_09_matriz_trazabilidad_automatica.md)
    Generación de trazabilidad entre requisitos, historias, test cases, Jira y código.

### Integración, adopción y gobierno

13. [Integración con Jira API](docs/04_10_integracion_jira_api.md)
    Conector para crear artefactos en Jira manteniendo control, idempotencia y aprobación humana.

14. [Script orquestador](docs/05_13_script_orquestador.md)
    Flujo ejecutable que une los pasos del pipeline desde el YAML hasta Jira y Xray.
    
15. [Plan de formación y adopción](docs/04_11_plan_formacion_adopcion.md)
    Estrategia de implantación gradual, gestión del cambio, formación y métricas de adopción.

16. [Gobierno del modelo](docs/04_12_gobierno_del_modelo.md)
    Gestión de prompts, calidad del repositorio, observabilidad, riesgos y estructura de decisión.

<a id="gaps"></a>
## Gaps que complementan el modelo

### Gaps técnicos del pipeline

- *[Pipeline AI-ready para requisitos no funcionales](docs/06_01_NFR_Pipeline_AI_Ready.md)* — estructura diferente, genera spike técnicos y criterios de benchmark
- *[Requisitos de integración con sistemas externos](docs/06_02_requisitos_integracion_sistemas_externos.md)* — flujo específico con contratos de API e incertidumbre
- *[Pipeline de épicas desde cero](docs/06_03_pipeline-epicas-desde-cero.md)* — desde el mapa de Event Storming
- *Manejo de requisitos deprecados o divididos* — split y fusión de requisitos
- *Gestión de versiones de un mismo requisito en sprints distintos* — implementación parcial

### Gaps en la capa de inteligencia

- *Fine-tuning o few-shot learning con ejemplos propios* — usar artefactos aprobados históricos como referencia
- *Detección automática de requisitos candidatos a épica nueva* — cuando no encajan en épicas existentes
- *Análisis de cobertura de negocio* — cruzar requisitos con objetivos de negocio declarados

### Gaps de integración

- *Integración con Azure DevOps* — alternativa a Jira para organizaciones con stack Microsoft
- *Integración con Confluence como fuente documental* — leer páginas directamente sin transformación manual
- *Integración con herramientas de modelado BPMN* — Bizagi, Camunda, Lucidchart
- *Integración con repositorio de código* — vincular commits automáticamente con historias Jira
- *Integración con herramientas de testing de rendimiento* — scripts JMeter/k6 desde criterios de rendimiento

### Gaps de proceso

- *Flujo de gestión de cambios de alcance mid-sprint* — cambio a historia en desarrollo
- *Proceso de refinamiento asistido por IA* — preguntas en tiempo real durante la ceremonia
- *Gestión del backlog de épicas no priorizadas* — consistencia para estimación de capacidad
- *Proceso de cierre de sprint y actualización de trazabilidad* — historias no completadas

### Gaps de gobierno

- *Métricas de ROI para la dirección* — valor monetario de las métricas técnicas
- *Política de privacidad y seguridad de datos* — qué enviar a APIs externas en proyectos regulados
- *Proceso de auditoría externa* — ISO 9001, CMMI, SOC 2
- *Escalabilidad a múltiples proyectos simultáneos* — glosario y RAG multi-proyecto

### Gaps de experiencia de usuario

- *[Interfaz de analista](docs/05_14_interfaz_analista_pipeline.md)* — interfaz web accesible sin conocimientos técnicos
- *Plugin de Confluence o extensión del navegador* — integración nativa sin salir de Confluence
- *Notificaciones y bandeja de entrada del analista* — alertas sin ruido excesivo

### Gaps de casos de uso avanzados

- *Análisis funcional de migraciones* — equivalencia con sistema legado
- *Requisitos de accesibilidad y cumplimiento normativo* — WCAG, RGPD, PSD2 automáticos
- *Generación de documentación de usuario final* — manuales, release notes, ayuda en línea

---

## Índice del libro

### Parte I — El problema y la oportunidad

1. [Introducción](book/00_introduccion.md)
   Presenta el problema, los perfiles de lector, el caso Meridian y la promesa del modelo.

2. [Capítulo 1. El análisis funcional en crisis silenciosa](book/01_el_analisis_funcional_en_crisis_silenciosa.md)
   Diagnóstico del problema: tiempo mecánico, ambigüedad, deuda funcional y coste de los defectos.

3. [Capítulo 2. Qué puede hacer la IA, y qué no puede hacer](book/02_que_puede_hacer_la_IA_%28y_que_no_puede_hacer%29.md)
   Explicación práctica de las capacidades y límites de los LLMs en análisis funcional.

4. [Capítulo 3. Visión del modelo operativo](book/03_vision_del_modelo_operativo.md)
   Mapa completo del sistema, componentes, flujo end-to-end y roadmap de implantación.

### Parte II — Preparar requisitos para IA

5. [Capítulo 4. El requisito AI-ready](book/04_el_requisito_AI-ready.md)
   Plantilla de cinco bloques para convertir un requisito en materia prima procesable por IA.

6. [Capítulo 5. El glosario estructurado](book/05_el_glosario_estructurado.md)
   El glosario como contrato terminológico activo del pipeline.

7. [Capítulo 6. Event Storming para analistas](book/06_event_storming_para_analistas.md)
   Cómo descubrir requisitos mediante eventos de negocio y convertirlos en YAML funcional.

### Parte III — Construir el pipeline

8. [Capítulo 7. Validación automática](book/07_validacion_automatica.md)
   Validación de calidad del requisito antes de generar artefactos.

9. [Capítulo 8. Generación de artefactos Jira](book/08_generacion_artefactos_jira.md)
   Conversión de requisitos en épicas, historias, tareas y subtareas.

10. [Capítulo 9. Generación automática de test cases](book/09_generacion_test_cases.md)
    Producción de casos de prueba funcionales, negativos, de contorno y Gherkin.

11. [Capítulo 10. Arquitectura RAG](book/10_arquitectura_rag.md)
    Memoria semántica del pipeline para recuperar requisitos relacionados y evitar contradicciones.

12. [Capítulo 11. Trazabilidad automática e impacto de cambios](book/11_trazabilidad_automatica_e_impacto_de_cambios.md)
    Grafo de trazabilidad y análisis automático de impacto.

13. [Capítulo 12. El orquestador](book/12_el_orquestador.md)
    Pipeline completo ejecutable, gestión de estado, configuración y ejecución por lotes.

### Parte IV — Implantar y sostener el modelo

14. [Capítulo 13. Plan de adopción](book/13_plan_de_adopcion.md)
    Implantación por fases, resistencias, demostraciones, formación y métricas de adopción.

15. [Capítulo 14. Gobierno del modelo](book/14_gobierno_del_modelo.md)
    Observabilidad, gestión de prompts, calidad del repositorio, gobierno y madurez del sistema.

---

## Estado actual del libro

El libro está en desarrollo. Actualmente están completados la introducción y los capítulos 1 a 14.

El siguiente capítulo previsto es:

* **Capítulo 15. Medición del impacto y ROI**

---

## Material técnico del repositorio

Además de la documentación, el repositorio contiene una implementación técnica del pipeline:

* [`orchestrator.py`](orchestrator.py): punto de entrada principal.
* [`config.py`](config.py): configuración centralizada.
* [`state.py`](state.py): gestión de estado y reanudación.
* [`glosario.yaml`](glosario.yaml): vocabulario oficial del proyecto.
* [`templates/`](templates/): plantillas base de requisitos.
* [`requisitos/EP-04/REQ-023.yaml`](requisitos/EP-04/REQ-023.yaml): requisito de ejemplo usado en el libro.
* [`steps/`](steps/): pasos del pipeline.
* [`rag/`](rag/): motor de recuperación semántica.
* [`trazabilidad/`](trazabilidad/): grafo de trazabilidad.
* [`jira/`](jira/): conectores con Jira y Xray.
* [`prompts/v1.1/`](prompts/v1.1/): prompts versionados.
* [`sql/schema.sql`](sql/schema.sql): esquema PostgreSQL para RAG y trazabilidad.
* [`gobierno/`](gobierno/): utilidades de gobierno, métricas y evaluación.

---

## Cómo leer este proyecto

### Si viene desde negocio, producto o dirección

Empiece por:

1. [Introducción](book/00_introduccion.md)
2. [Capítulo 1](book/01_el_analisis_funcional_en_crisis_silenciosa.md)
3. [Capítulo 3](book/03_vision_del_modelo_operativo.md)
4. [Plan de formación y adopción](docs/04_11_plan_formacion_adopcion.md)
5. [Gobierno del modelo](docs/04_12_gobierno_del_modelo.md)

### Si es analista funcional o Product Owner

Empiece por:

1. [Capítulo 4. El requisito AI-ready](book/04_el_requisito_AI-ready.md)
2. [Capítulo 5. El glosario estructurado](book/05_el_glosario_estructurado.md)
3. [Capítulo 6. Event Storming para analistas](book/06_event_storming_para_analistas.md)
4. [Validación automática de requisitos](docs/02_06_validacion_automatica_requisitos.md)
5. [Generación automática de test cases](docs/02_05_generacion_test_cases.md)

### Si es arquitecto, desarrollador senior o responsable técnico

Empiece por:

1. [Capítulo 8. Generación de artefactos Jira](book/08_generacion_artefactos_jira.md)
2. [Capítulo 10. Arquitectura RAG](book/10_arquitectura_rag.md)
3. [Capítulo 11. Trazabilidad automática e impacto de cambios](book/11_trazabilidad_automatica_e_impacto_de_cambios.md)
4. [Capítulo 12. El orquestador](book/12_el_orquestador.md)
5. [Integración con Jira API](docs/04_10_integracion_jira_api.md)

---

## Resumen ejecutivo

Este repositorio propone una forma práctica de introducir IA en el ciclo de vida del análisis funcional sin depender de promesas de automatización total.

El sistema se apoya en cuatro principios:

1. **Estructurar antes de automatizar.**
   La calidad del output depende de la calidad del requisito.

2. **Mantener al humano en el control.**
   La IA genera propuestas; el analista revisa, decide y aprueba.

3. **Crear trazabilidad desde el origen.**
   Cada requisito debe poder conectarse con sus historias, test cases, cambios y evidencias.

4. **Gobernar el modelo como un producto vivo.**
   Prompts, glosario, métricas y repositorio necesitan mantenimiento continuo.

La aspiración final es convertir el análisis funcional en una disciplina más precisa, más trazable y más escalable, sin perder el juicio experto que solo puede aportar el analista humano.

---

## Repositorio

Repositorio GitHub del proyecto:

https://github.com/asalamor/el-analista-aumentado
