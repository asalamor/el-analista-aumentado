# Inventario completo de puntos pendientes identificados

Al completar el modelo operativo principal, se identificaron los siguientes puntos adicionales que complementan el análisis:

### Gaps técnicos del pipeline

- **Prompts para requisitos no funcionales (NFR)** — estructura diferente, genera spike técnicos y criterios de benchmark
- **Gestión de requisitos de integración con sistemas externos** — flujo específico con contratos de API e incertidumbre
- **Pipeline de generación de épicas desde cero** — desde el mapa de Event Storming
- **Manejo de requisitos deprecados o divididos** — split y fusión de requisitos
- **Gestión de versiones de un mismo requisito en sprints distintos** — implementación parcial

### Gaps en la capa de inteligencia

- **Fine-tuning o few-shot learning con ejemplos propios** — usar artefactos aprobados históricos como referencia
- **Detección automática de requisitos candidatos a épica nueva** — cuando no encajan en épicas existentes
- **Análisis de cobertura de negocio** — cruzar requisitos con objetivos de negocio declarados

### Gaps de integración

- **Integración con Azure DevOps** — alternativa a Jira para organizaciones con stack Microsoft
- **Integración con Confluence como fuente documental** — leer páginas directamente sin transformación manual
- **Integración con herramientas de modelado BPMN** — Bizagi, Camunda, Lucidchart
- **Integración con repositorio de código** — vincular commits automáticamente con historias Jira
- **Integración con herramientas de testing de rendimiento** — scripts JMeter/k6 desde criterios de rendimiento

### Gaps de proceso

- **Flujo de gestión de cambios de alcance mid-sprint** — cambio a historia en desarrollo
- **Proceso de refinamiento asistido por IA** — preguntas en tiempo real durante la ceremonia
- **Gestión del backlog de épicas no priorizadas** — consistencia para estimación de capacidad
- **Proceso de cierre de sprint y actualización de trazabilidad** — historias no completadas

## Gaps de gobierno

- **Métricas de ROI para la dirección** — valor monetario de las métricas técnicas
- **Política de privacidad y seguridad de datos** — qué enviar a APIs externas en proyectos regulados
- **Proceso de auditoría externa** — ISO 9001, CMMI, SOC 2
- **Escalabilidad a múltiples proyectos simultáneos** — glosario y RAG multi-proyecto

### Gaps de experiencia de usuario

- **Interfaz de analista para el pipeline** — interfaz web accesible sin conocimientos técnicos
- **Plugin de Confluence o extensión del navegador** — integración nativa sin salir de Confluence
- **Notificaciones y bandeja de entrada del analista** — alertas sin ruido excesivo

### Gaps de casos de uso avanzados

- **Análisis funcional de migraciones** — equivalencia con sistema legado
- **Requisitos de accesibilidad y cumplimiento normativo** — WCAG, RGPD, PSD2 automáticos
- **Generación de documentación de usuario final** — manuales, release notes, ayuda en línea

---

## Priorización de los puntos pendientes

De todos los puntos identificados, los que más valor aportarían al modelo actual, en orden de prioridad:

1. **Script orquestador** — cierra el ciclo completo
2. **Interfaz de analista** — hace el sistema accesible sin código
3. **Modelo de ROI para dirección** — justifica la inversión con números
4. **Política de privacidad y datos** — desbloqueante para proyectos regulados
5. **Integración con Azure DevOps** — amplía el alcance a organizaciones con ese stack
