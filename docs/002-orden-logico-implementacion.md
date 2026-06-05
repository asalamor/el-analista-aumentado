# Orden lógico de implementación del modelo operativo

Basándome en lo que ya tienes como base estratégica, el orden lógico sería este — de lo más fundacional a lo más avanzado:

---

## Antes de tocar tecnología

**1. Taller de plantillas**
Diseñar juntos la plantilla YAML definitiva adaptada a tu organización, con los campos obligatorios, opcionales y los vocabularios controlados propios de tu negocio.

**2. Glosario estructurado**
Cómo construirlo, quién lo gobierna y cómo se inyecta como contexto en cada llamada a la IA para garantizar coherencia terminológica.

**3. Guía de Event Storming para analistas**
Cómo facilitar el workshop, qué artefactos producir y cómo pasar de post-its a requisitos estructurados sin perder información.

---

## El núcleo técnico del pipeline

**4. Prompts de generación de artefactos Jira**
Los prompts concretos y testeados para transformar un YAML de requisito en épicas, historias, tareas técnicas y subtareas. Con ejemplos reales y variantes según tipo de requisito.

**5. Generación automática de test cases**
Cómo construir el pipeline que convierte criterios de aceptación en casos de prueba, qué formato de salida genera y cómo se integra con Xray o Zephyr.

**6. Validación automática de calidad de requisitos**
El checklist que la IA ejecuta sobre cada requisito antes de que entre al pipeline — detección de ambigüedad, campos vacíos, conflictos con otros requisitos.

---

## La capa de inteligencia avanzada

**7. Arquitectura RAG para el repositorio de requisitos**
Cómo indexar todos los documentos funcionales, qué embeddings usar, y cómo la IA consulta el histórico antes de generar para evitar duplicidades y detectar contradicciones.

**8. Detección de impacto de cambios**
Cuando un requisito cambia, cómo la IA identifica automáticamente qué historias, tareas y test cases se ven afectados.

**9. Matriz de trazabilidad automática**
Generación y mantenimiento continuo de la traza completa Req → US → TC → Jira → código.

---

## Implantación y gobierno

**10. Integración técnica con Jira API**
Cómo construir el conector que empuja los artefactos generados a Jira, con el flujo de aprobación humana intermedia.

**11. Script orquestador**
El flujo Python ejecutable que une en un único comando los pipelines de los puntos 4 al 10, desde el YAML hasta Jira y Xray.

**12. Plan de formación y adopción**
Materiales concretos para analistas y usuarios de negocio, estructura del piloto, métricas de éxito de las primeras semanas.

**13. Gobierno del modelo**
Cómo gestionar la evolución de los prompts, quién los valida, cómo se mide la calidad de los artefactos generados y cuándo escalar la autonomía de la IA.

---

### [Puntos adicionales identificados posteriormente](../gaps/inventario-puntos-adicionales)

---

## Recomendación de inicio

Mi recomendación concreta es empezar por el **punto 1 y el 4** en paralelo: la plantilla te da la materia prima, y los prompts de generación te permiten ver resultados tangibles rápido. Nada acelera más la adopción que mostrar un requisito real de tu organización convertido en artefactos Jira en tiempo real.

---

A continuación: [Modelo Operativo AI-Ready — Documentación Completa.](./003-modelo-operativo.md)

---
