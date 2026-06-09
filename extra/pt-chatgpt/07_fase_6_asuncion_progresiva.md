# Fase 6. Asunción progresiva del servicio  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 6

La **Fase 6. Asunción progresiva del servicio** tiene como objetivo transferir de forma controlada la responsabilidad operativa desde el equipo saliente hacia el equipo entrante.

En las fases anteriores el equipo entrante ha aprendido, observado y ejecutado bajo supervisión. En esta fase comienza la verdadera toma de control del servicio, pero no de forma abrupta, sino por **oleadas**, **dominios**, **aplicaciones**, **niveles de criticidad** o **tipos de actividad**.

La idea central es:

> El equipo entrante pasa a ser responsable principal de la operación, mientras el equipo saliente permanece disponible como soporte de segundo nivel, mentor o escalado temporal.

Esta fase es crítica porque el servicio ya no se está “ensayando”. El equipo entrante empieza a responder ante el cliente, los usuarios, negocio y operación. Por eso, la asunción debe ser progresiva, medible, reversible en algunos aspectos y basada en evidencias.

En una compañía aseguradora, la asunción progresiva debe proteger especialmente:

- Emisión de pólizas.
- Cotización.
- Recibos y cobros.
- Impagos y recobros.
- Renovaciones.
- Siniestros.
- Documentación contractual.
- Firma electrónica.
- Mediadores.
- Integraciones bancarias.
- Reporting financiero y regulatorio.
- Procesos batch.
- Datos personales y sensibles.
- Cumplimiento normativo.
- Continuidad del servicio.

---

## 2. Resultado esperado de la Fase 6

Al finalizar esta fase, el equipo entrante debe haber asumido progresivamente la responsabilidad principal de las aplicaciones, procesos o dominios acordados, cumpliendo los niveles de servicio definidos y con dependencia decreciente del equipo saliente.

Los resultados esperados son:

- Servicio asumido por oleadas.
- Responsabilidad operativa principal transferida al equipo entrante.
- SLAs y SLOs monitorizados durante la asunción.
- Incidencias gestionadas directamente por el equipo entrante.
- Despliegues, cambios y tareas recurrentes ejecutados con autonomía definida.
- Equipo saliente reducido a soporte puntual o escalado residual.
- Gaps críticos cerrados o con mitigación aprobada.
- Riesgos residuales documentados y aceptados.
- Matriz de autonomía consolidada.
- Modelo BAU inicial activado.
- Evidencias suficientes para preparar el cierre formal de la transición en la Fase 7.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **2 a 6 semanas**.

Puede ser menor si:

- La Fase 5 ha demostrado alta autonomía.
- El número de aplicaciones críticas es limitado.
- El equipo entrante ya gestiona tickets con solvencia.
- Los runbooks están maduros.
- Los SLAs se están cumpliendo.
- El equipo saliente apenas interviene.
- El cliente acepta una asunción rápida.

Puede alargarse si:

- Hay muchos dominios críticos.
- Existen procesos batch complejos.
- Hay aplicaciones legacy.
- Persisten gaps altos.
- El cliente exige evidencias adicionales.
- Hay picos de negocio próximos.
- Hay auditorías, cierres o campañas.
- El equipo saliente sigue siendo necesario en incidencias relevantes.
- Los SLAs se ven tensionados.
- Hay dudas sobre despliegues, rollback o reprocesos.

---

# 4. Principios de trabajo de la Fase 6

## 4.1 Asumir por oleadas, no de golpe

La toma de servicio debe realizarse por bloques controlados.

Posibles criterios de oleada:

- Por aplicación.
- Por dominio funcional.
- Por criticidad.
- Por tecnología.
- Por tipo de operación.
- Por horario.
- Por nivel de soporte.
- Por canal.
- Por proceso asegurador.

La asunción total de todo el stack en una única fecha solo debería hacerse si el entorno es pequeño, muy estable y con bajo riesgo. En stacks aseguradores complejos no es recomendable.

## 4.2 Responsabilidad principal con soporte residual

Durante esta fase, el equipo entrante debe figurar como responsable principal, pero el equipo saliente debe permanecer disponible para:

- Dudas no previstas.
- Incidencias críticas.
- Casos no observados.
- Procesos batch sensibles.
- Despliegues complejos.
- Integraciones externas delicadas.
- Validaciones de conocimiento.
- Escenarios de contingencia.

La diferencia respecto a la Fase 5 es que el equipo saliente ya no supervisa cada paso. Interviene bajo demanda, según reglas de escalado.

## 4.3 Control operativo reforzado

Durante la asunción progresiva conviene aumentar temporalmente el control:

- Reuniones operativas más frecuentes.
- Revisión diaria de incidencias.
- Seguimiento de SLAs.
- Revisión de alertas.
- Revisión de tickets escalados.
- Revisión de gaps.
- Revisión de riesgos.
- Comunicación frecuente con cliente.
- Registro de intervenciones del equipo saliente.

Este control reforzado no debe mantenerse indefinidamente. Sirve para estabilizar la transferencia de responsabilidad.

## 4.4 Medir dependencia real

No basta con decir que el equipo entrante ha asumido el servicio. Hay que medir cuánto depende todavía del equipo saliente.

Indicadores útiles:

- Número de escalados al equipo saliente.
- Motivo de cada escalado.
- Tiempo de respuesta del saliente.
- Criticidad de los casos escalados.
- Repetición de dudas.
- Actividades que aún no se ejecutan de forma autónoma.
- Aplicaciones con baja autonomía.
- Gaps que bloquean independencia.

## 4.5 No cerrar en falso

La Fase 6 no debe convertirse en una aceptación prematura por presión de calendario. Si una aplicación crítica sigue dependiendo del equipo saliente, debe reconocerse.

Puede haber asunción progresiva con restricciones, pero esas restricciones deben quedar documentadas.

Ejemplos:

- “El equipo entrante asume soporte L2, pero los reprocesos de remesas siguen requiriendo validación del equipo saliente durante dos semanas.”
- “La aplicación de siniestros pasa a BAU, salvo despliegues productivos, que requieren supervisión hasta completar un despliegue exitoso.”
- “El portal de mediadores se asume plenamente, con soporte saliente bajo demanda durante horario laboral.”

---

# 5. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Preparar plan de asunción por oleadas | Alcance, calendario, criterios y restricciones. |
| Semana 1-2 | Activar primera oleada | Equipo entrante asume aplicaciones o tareas de menor riesgo. |
| Semana 2-4 | Asumir dominios o aplicaciones críticas con control reforzado | Validar SLAs, escalados y autonomía. |
| Semana 3-5 | Reducir intervención del equipo saliente | Medir dependencia y cerrar gaps. |
| Semana 4-6 | Consolidar operación BAU inicial | Normalizar rutinas, reporting y responsabilidades. |
| Final | Evaluar preparación para cierre y estabilización | Decisión Go / No-Go hacia Fase 7. |

---

# 6. Actividad 1. Definir el plan de asunción progresiva

## 6.1 Objetivo

Establecer qué aplicaciones, dominios o actividades serán asumidas, en qué orden, con qué restricciones y con qué criterios de éxito.

## 6.2 Entradas necesarias

- Matriz de autonomía de Fase 5.
- Decisiones Go / No-Go por aplicación o dominio.
- Matriz de criticidad.
- Matriz de riesgos.
- Gaps pendientes.
- Runbooks actualizados.
- SLAs y SLOs.
- Matriz de escalado.
- Matriz de accesos.
- Calendario de negocio.
- Calendario de despliegues.
- Calendario batch.
- Disponibilidad del equipo saliente.
- Restricciones del cliente.

## 6.3 Criterios para definir oleadas

| Criterio | Pregunta |
|---|---|
| Criticidad | ¿Qué impacto tendría un fallo? |
| Autonomía demostrada | ¿Qué nivel alcanzó el equipo entrante en Fase 5? |
| Complejidad técnica | ¿Es una aplicación simple o muy acoplada? |
| Complejidad funcional | ¿Tiene muchas reglas de negocio o excepciones? |
| Incidencias históricas | ¿Genera muchos tickets? |
| Dependencia saliente | ¿Sigue requiriendo experto saliente? |
| Procesos batch | ¿Tiene jobs críticos? |
| Integraciones | ¿Depende de terceros o sistemas críticos? |
| Datos sensibles | ¿Trata datos personales o especialmente sensibles? |
| Calendario de negocio | ¿Hay picos, cierres, campañas o auditorías? |

## 6.4 Modelos de asunción posibles

### Modelo por aplicación

Útil cuando las aplicaciones son relativamente independientes.

Ejemplo:

1. Portal interno auxiliar.
2. Portal de mediadores.
3. Aplicación documental.
4. Sistema de emisión.
5. Sistema de recibos.
6. Sistema de siniestros.

### Modelo por dominio funcional

Útil cuando varias aplicaciones intervienen en un proceso de negocio.

Ejemplo:

1. Consulta y soporte de mediadores.
2. Cotización.
3. Emisión.
4. Recibos.
5. Siniestros.
6. Reporting.

### Modelo por tipo de actividad

Útil cuando se quiere asumir gradualmente responsabilidades.

Ejemplo:

1. Monitorización y tickets.
2. Diagnóstico L2.
3. Tareas recurrentes.
4. Despliegues no productivos.
5. Despliegues productivos.
6. Reprocesos batch.
7. Guardia completa.

### Modelo por criticidad

Útil para reducir riesgo progresivamente.

Ejemplo:

1. Aplicaciones baja criticidad.
2. Aplicaciones media criticidad.
3. Aplicaciones alta criticidad.
4. Aplicaciones críticas.

### Modelo mixto

En la práctica, suele ser el más recomendable. Combina aplicación, dominio, criticidad y tipo de actividad.

## 6.5 Matriz de plan de oleadas

| Oleada | Alcance | Tipo | Criticidad | Fecha inicio | Fecha fin | Restricciones | Criterio de éxito |
|---|---|---|---|---|---|---|---|
| Oleada 1 | Aplicaciones auxiliares | Aplicación | Baja / Media |  |  | Soporte saliente bajo demanda | 1 semana sin escalados críticos |
| Oleada 2 | Portal mediadores | Dominio | Alta |  |  | Escalado saliente para integraciones | SLAs cumplidos |
| Oleada 3 | Emisión y documental | Dominio | Crítica |  |  | Supervisión en despliegues | Sin P1 atribuibles a transición |
| Oleada 4 | Recibos y batch | Dominio | Crítica |  |  | Reprocesos con doble validación | Batch completado correctamente |

## 6.6 Entregables

- Plan de asunción progresiva.
- Matriz de oleadas.
- Restricciones por oleada.
- Criterios de éxito por oleada.
- Calendario de asunción.
- Matriz de soporte residual del equipo saliente.
- Plan de comunicación al cliente y negocio.

---

# 7. Actividad 2. Definir el modelo de responsabilidad durante la asunción

## 7.1 Objetivo

Clarificar quién es responsable de qué durante la Fase 6.

La ambigüedad en esta fase es peligrosa. Debe estar claro si una actividad la ejecuta el equipo entrante, el saliente, operaciones, infraestructura, seguridad, negocio o un proveedor externo.

## 7.2 Modelo recomendado

| Tipo de responsabilidad | Equipo entrante | Equipo saliente | Cliente / otros |
|---|---|---|---|
| Gestión diaria de tickets | Responsable principal | Soporte bajo demanda | Seguimiento |
| Diagnóstico L2 | Responsable principal | Apoyo en casos complejos |  |
| Diagnóstico L3 especializado | Según aplicación | Apoyo temporal | Arquitectura / proveedor |
| Despliegues no productivos | Responsable principal | Consultado si aplica |  |
| Despliegues productivos | Responsable o corresponsable | Apoyo temporal | Aprobación cliente |
| Batch crítico | Responsable progresivo | Apoyo / validación temporal | Operaciones / negocio |
| Reprocesos sensibles | Responsable condicionado | Validación temporal | Autorización negocio |
| Comunicación a negocio | Responsable / Service Manager | Consultado | Cliente valida protocolo |
| Escalado a terceros | Responsable progresivo | Apoyo si conoce proveedor | Proveedor externo |
| Seguridad / secretos | No administra salvo autorización | Consultado si conoce | Seguridad / IAM |
| Cierre de gaps | Responsable | Consultado | Cliente prioriza |

## 7.3 RACI específico de asunción

| Actividad | Entrante | Saliente | Cliente | Operaciones | Negocio |
|---|---|---|---|---|---|
| Recepción de ticket | R | C | I | C | I |
| Diagnóstico inicial | R | C | I | C |  |
| Resolución estándar | R | C | I | C |  |
| Incidencia crítica | R | C | A | C | C |
| Reproceso batch crítico | R | C | A | C | C |
| Despliegue productivo | R | C | A | C | I |
| Comunicación a negocio | R | C | A | I | I |
| Aceptación de riesgo residual | C | C | A | C | C |

Leyenda:

- **R** = Responsible.
- **A** = Accountable.
- **C** = Consulted.
- **I** = Informed.

## 7.4 Preguntas clave

- ¿Quién recibe la incidencia?
- ¿Quién decide severidad?
- ¿Quién comunica?
- ¿Quién ejecuta?
- ¿Quién valida?
- ¿Quién aprueba un reproceso?
- ¿Quién decide rollback?
- ¿Quién contacta con terceros?
- ¿Cuándo se consulta al saliente?
- ¿Cuándo se escala al cliente?
- ¿Quién acepta riesgos residuales?

## 7.5 Entregables

- RACI de asunción progresiva.
- Modelo de responsabilidad temporal.
- Matriz de actividades condicionadas.
- Reglas de escalado al equipo saliente.
- Reglas de comunicación.

---

# 8. Actividad 3. Activar la primera oleada

## 8.1 Objetivo

Iniciar la asunción real del servicio con un primer conjunto de aplicaciones, dominios o actividades de riesgo controlado.

La primera oleada debe seleccionarse cuidadosamente. Debe permitir validar el modelo de operación sin exponer innecesariamente procesos críticos.

## 8.2 Criterios para la primera oleada

Conviene elegir aplicaciones o actividades que cumplan varias de estas condiciones:

- Autonomía alta demostrada en Fase 5.
- Baja o media criticidad.
- Runbooks maduros.
- Pocas integraciones críticas.
- Baja complejidad batch.
- SLAs razonables.
- Bajo impacto regulatorio.
- Equipo entrante cómodo con diagnóstico.
- Soporte saliente disponible.
- Posibilidad de revertir o escalar.

## 8.3 Actividades de arranque de oleada

- Comunicar inicio de oleada.
- Confirmar responsables.
- Confirmar restricciones.
- Confirmar escalado saliente.
- Confirmar SLAs.
- Confirmar herramientas.
- Confirmar accesos.
- Revisar runbooks.
- Revisar gaps abiertos.
- Activar seguimiento diario.
- Registrar fecha y hora de asunción.
- Informar a mesa de servicio.
- Informar a operaciones.
- Informar a negocio si aplica.

## 8.4 Checklist de activación de oleada

| Criterio | Estado |
|---|---|
| Alcance definido | Pendiente / En curso / Validado |
| Responsable entrante asignado |  |
| Soporte saliente asignado |  |
| Runbooks disponibles |  |
| Accesos verificados |  |
| Matriz de escalado actualizada |  |
| SLAs confirmados |  |
| Gaps críticos cerrados |  |
| Riesgos residuales aceptados |  |
| Comunicación enviada |  |
| Seguimiento activado |  |

## 8.5 Resultado esperado

- Primera oleada en operación principal por equipo entrante.
- Modelo de asunción probado.
- Incidencias y escalados monitorizados.
- Ajustes iniciales identificados.

---

# 9. Actividad 4. Operar con control reforzado

## 9.1 Objetivo

Gestionar la operación real durante la asunción con un nivel de seguimiento superior al BAU normal.

## 9.2 Controles recomendados

| Control | Frecuencia | Objetivo |
|---|---:|---|
| Revisión de tickets | Diaria | Detectar bloqueos, errores o mala clasificación. |
| Revisión de SLAs | Diaria | Evitar incumplimientos durante la transición. |
| Revisión de escalados al saliente | Diaria | Medir dependencia residual. |
| Revisión de incidencias críticas | Inmediata | Controlar impacto. |
| Revisión de gaps | 2-3 veces por semana | Acelerar cierre de pendientes. |
| Revisión de riesgos | Semanal | Actualizar RAID log. |
| Comité operativo | Semanal | Tomar decisiones y ajustar oleadas. |
| Comunicación a cliente | Semanal o según criticidad | Mantener confianza y visibilidad. |

## 9.3 Métricas clave durante la asunción

| Métrica | Qué mide |
|---|---|
| Nº tickets gestionados por entrante | Volumen real asumido. |
| % tickets resueltos sin saliente | Autonomía. |
| Nº escalados al saliente | Dependencia residual. |
| Motivo de escalado | Gaps o complejidad restante. |
| MTTR | Tiempo medio de resolución. |
| Cumplimiento SLA | Calidad de servicio. |
| Incidencias reabiertas | Calidad de resolución. |
| Incidencias críticas | Estabilidad. |
| Cambios fallidos | Riesgo de despliegue. |
| Batch completados correctamente | Estabilidad operativa. |
| Gaps críticos abiertos | Riesgo de continuidad. |

## 9.4 Matriz de seguimiento diario

| Fecha | Aplicación | Tickets abiertos | Tickets cerrados | Escalados al saliente | SLA en riesgo | Incidencias críticas | Observaciones |
|---|---|---:|---:|---:|---:|---:|---|
|  |  |  |  |  |  |  |  |

## 9.5 Resultado esperado

- Operación controlada.
- Riesgos detectados pronto.
- Dependencia saliente medida.
- Confianza del cliente reforzada.
- Ajustes rápidos antes de ampliar oleadas.

---

# 10. Actividad 5. Gestionar incidencias durante la asunción

## 10.1 Objetivo

Asegurar que las incidencias gestionadas durante la asunción se resuelven correctamente, se documentan y sirven para validar autonomía.

## 10.2 Flujo recomendado

1. Entrada de incidencia.
2. Clasificación por equipo entrante.
3. Confirmación de severidad.
4. Diagnóstico inicial.
5. Revisión de runbook.
6. Acción de contención.
7. Escalado si procede.
8. Resolución.
9. Validación técnica.
10. Validación funcional.
11. Comunicación.
12. Cierre.
13. Revisión postincidencia si aplica.
14. Actualización de documentación.

## 10.3 Criterios de escalado al equipo saliente

Debe escalarse al equipo saliente cuando:

- La incidencia afecta a aplicación crítica y no existe runbook suficiente.
- Hay riesgo de impacto en cliente final.
- Hay riesgo económico.
- Hay riesgo regulatorio.
- Afecta a emisión, recibos, siniestros o documentación contractual.
- Requiere reproceso no practicado.
- Requiere rollback no ejecutado por el entrante.
- Hay inconsistencia de datos.
- Hay integración externa no dominada.
- Se superan umbrales de tiempo definidos.
- El equipo entrante no puede formular una hipótesis razonable.
- El cliente lo solicita.

## 10.4 Matriz de incidencias en asunción

| Ticket | Aplicación | Severidad | Resuelto por entrante | Escalado saliente | Motivo escalado | SLA cumplido | Aprendizaje |
|---|---|---|---|---|---|---|---|
|  |  | P1 / P2 / P3 | Sí / No | Sí / No |  | Sí / No |  |

## 10.5 Resultado esperado

- Incidencias resueltas por el equipo entrante.
- Escalados controlados.
- SLAs mantenidos.
- Aprendizajes incorporados.
- Autonomía validada progresivamente.

---

# 11. Actividad 6. Asumir despliegues y cambios de forma progresiva

## 11.1 Objetivo

Pasar gradualmente de despliegues supervisados a despliegues asumidos por el equipo entrante, manteniendo controles de riesgo.

## 11.2 Progresión recomendada

| Nivel | Actividad |
|---|---|
| 1 | El entrante prepara despliegue y el saliente ejecuta. |
| 2 | El entrante ejecuta en DEV/PRE y el saliente observa. |
| 3 | El entrante ejecuta despliegues no productivos autónomamente. |
| 4 | El entrante participa en producción con apoyo saliente. |
| 5 | El entrante ejecuta producción con soporte saliente bajo demanda. |
| 6 | El entrante ejecuta producción dentro de BAU. |

## 11.3 Condiciones para asumir despliegues productivos

Antes de asumir despliegues productivos debe existir:

- Runbook de despliegue validado.
- Procedimiento de rollback.
- Identificación clara de versión.
- Artefacto trazable.
- Aprobación de cambio.
- Validaciones predespliegue.
- Validaciones postdespliegue.
- Comunicación preparada.
- Monitorización posterior.
- Contactos de escalado.
- Evidencias de despliegues supervisados previos.

## 11.4 Matriz de cambios durante asunción

| Cambio | Aplicación | Tipo | Entorno | Ejecuta | Apoya saliente | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
|  |  | Release / Hotfix / Config | PRE / PRO | Entrante | Sí / No | Correcto / Fallido |  |

## 11.5 Resultado esperado

- Cambios asumidos de forma progresiva.
- Riesgo de despliegue controlado.
- Rollback conocido.
- Evidencias de capacidad de cambio.
- Restricciones para Fase 7 reducidas.

---

# 12. Actividad 7. Asumir procesos batch y tareas sensibles

## 12.1 Objetivo

Transferir progresivamente la responsabilidad sobre procesos batch, validaciones recurrentes, reprocesos y tareas sensibles.

## 12.2 Procesos sensibles en aseguradoras

| Proceso | Riesgo |
|---|---|
| Generación de recibos | Duplicidades, impagos, impacto económico. |
| Remesas bancarias | Errores bancarios, rechazos, descuadres. |
| Renovaciones | Importe incorrecto, pérdida de cartera, reclamaciones. |
| Comisiones de mediadores | Conflictos comerciales, errores contables. |
| Reporting financiero | Descuadres, cierres erróneos. |
| Reporting regulatorio | Riesgo de incumplimiento. |
| Siniestros | Pagos, reservas, estados incorrectos. |
| Documentación masiva | Documentos contractuales incorrectos. |
| Carga DWH | Informes erróneos, decisiones equivocadas. |

## 12.3 Progresión recomendada para batch

1. Monitorización por el equipo entrante.
2. Validación de salida por el equipo entrante.
3. Diagnóstico de fallos con apoyo saliente.
4. Reproceso propuesto por entrante y ejecutado por saliente.
5. Reproceso ejecutado por entrante con validación saliente.
6. Reproceso ejecutado por entrante con autorización cliente/negocio.
7. Operación BAU del batch.

## 12.4 Condiciones para asumir reprocesos

Antes de asumir reprocesos debe existir:

- Runbook validado.
- Criterio claro de cuándo reprocesar.
- Criterio claro de cuándo no reprocesar.
- Validación previa.
- Validación posterior.
- Responsable funcional.
- Autorización requerida.
- Evidencia de ejecución.
- Plan de contención.
- Riesgo de duplicidad controlado.

## 12.5 Matriz de batch asumidos

| Proceso batch | Dominio | Frecuencia | Nivel asumido | Restricciones | Responsable entrante | Apoyo saliente |
|---|---|---|---|---|---|---|
| Generación recibos | Recibos | Diario | Validación / Reproceso | Requiere autorización |  | Sí |
| Renovaciones | Renovaciones | Mensual | Monitorización | No reproceso sin negocio |  | Sí |
| Carga DWH | Reporting | Diario | Operación completa |  |  | Bajo demanda |

## 12.6 Resultado esperado

- Procesos batch asumidos con restricciones claras.
- Reprocesos críticos controlados.
- Validaciones funcionales incorporadas.
- Riesgo financiero y regulatorio mitigado.

---

# 13. Actividad 8. Reducir gradualmente la dependencia del equipo saliente

## 13.1 Objetivo

Pasar de un soporte saliente frecuente a un soporte excepcional y finalmente prescindible.

## 13.2 Tipos de dependencia

| Tipo | Ejemplo |
|---|---|
| Técnica | Solo el saliente entiende un componente. |
| Funcional | Solo el saliente conoce una regla. |
| Operativa | Solo el saliente sabe ejecutar un procedimiento. |
| Histórica | Solo el saliente conoce una decisión pasada. |
| Relacional | Solo el saliente conoce al proveedor externo. |
| De acceso | Solo el saliente tiene permisos. |
| De criterio | El entrante pregunta siempre antes de actuar. |

## 13.3 Cómo medir dependencia

| Indicador | Interpretación |
|---|---|
| Escalados frecuentes por la misma causa | Gap no resuelto. |
| Dudas repetidas | Formación o documentación insuficiente. |
| Necesidad de validación saliente en casos estándar | Autonomía incompleta. |
| Escalado por falta de acceso | Problema de habilitación. |
| Escalado por temor a actuar | Falta de confianza o límites mal definidos. |
| Escalado por integración concreta | Dependencia técnica o de proveedor. |

## 13.4 Matriz de dependencia saliente

| Aplicación | Caso | Motivo de dependencia | Frecuencia | Acción para reducir | Responsable | Fecha |
|---|---|---|---|---|---|---|
| Recibos | Reproceso remesas | Riesgo duplicidad | Alta | Simulacro + runbook |  |  |
| Emisión | Rollback | Falta práctica | Media | Despliegue PRE |  |  |
| Mediadores | Proveedor externo | Contacto histórico | Baja | Actualizar matriz proveedor |  |  |

## 13.5 Estrategias para reducir dependencia

- Repetir reverse shadowing en casos concretos.
- Actualizar runbooks.
- Crear guías de decisión.
- Crear matrices de escalado.
- Transferir contactos de proveedores.
- Completar accesos.
- Realizar simulacros.
- Documentar reglas.
- Crear checklists de autorización.
- Revisar casos con expertos salientes.
- Convertir preguntas repetidas en FAQs.

## 13.6 Resultado esperado

- Menos escalados al equipo saliente.
- Mayor autonomía del equipo entrante.
- Dependencias restantes identificadas.
- Plan de eliminación de dependencia.

---

# 14. Actividad 9. Estabilizar el modelo BAU inicial

## 14.1 Objetivo

Pasar gradualmente de modo transición a modo operación ordinaria o BAU.

BAU significa **Business As Usual**, es decir, el funcionamiento normal del servicio una vez que la transición deja de ser el foco principal.

## 14.2 Elementos del modelo BAU

| Elemento | Descripción |
|---|---|
| Modelo de soporte | L1, L2, L3, escalado, guardias. |
| ITSM | Gestión de incidencias, problemas, cambios y peticiones. |
| SLAs | Niveles de servicio contractuales. |
| Reporting | Informes de servicio. |
| Gobierno | Comités operativos y ejecutivos. |
| Gestión de cambios | CAB, despliegues, ventanas, aprobaciones. |
| Gestión de problemas | RCA, problem management, acciones preventivas. |
| Gestión del conocimiento | Runbooks, KB, documentación viva. |
| Monitorización | Dashboards, alertas, on-call. |
| Gestión de proveedores | Contactos, SLAs, escalados. |
| Seguridad | Accesos, auditoría, secretos, cumplimiento. |
| Mejora continua | Deuda técnica, automatización, observabilidad. |

## 14.3 Preguntas clave

- ¿Quién atiende cada tipo de ticket?
- ¿Cómo se escala a L3?
- ¿Quién comunica a negocio?
- ¿Quién aprueba cambios?
- ¿Quién participa en CAB?
- ¿Quién revisa SLAs?
- ¿Quién mantiene runbooks?
- ¿Quién actualiza la base de conocimiento?
- ¿Quién revisa alertas?
- ¿Quién gestiona proveedores?
- ¿Qué comités se mantienen tras transición?
- ¿Qué reporting se enviará al cliente?
- ¿Qué riesgos pasan a mejora continua?

## 14.4 Matriz BAU inicial

| Área | Responsable BAU | Herramienta | Frecuencia | Observaciones |
|---|---|---|---|---|
| Incidencias | Service Manager | ITSM | Diario |  |
| Cambios | Change Manager / Líder técnico | ITSM / CAB | Semanal |  |
| Problemas | Service Manager | ITSM | Quincenal |  |
| SLAs | Service Manager | Reporting | Mensual |  |
| Runbooks | Equipo técnico | Wiki / Git | Continua |  |
| Proveedores | Service Manager | Matriz proveedores | Según necesidad |  |
| Seguridad | Seguridad / IAM | Herramientas corporativas | Mensual |  |

## 14.5 Resultado esperado

- Modelo BAU inicial operativo.
- Roles de soporte clarificados.
- Reporting de servicio activo.
- Gestión de conocimiento incorporada a operación.
- Menor dependencia de estructuras de transición.

---

# 15. Actividad 10. Gestionar comunicación durante la asunción

## 15.1 Objetivo

Mantener informados al cliente, negocio, operaciones y equipos implicados sobre el avance de la asunción progresiva, riesgos y cambios de responsabilidad.

## 15.2 Audiencias

| Audiencia | Información necesaria |
|---|---|
| Dirección cliente | Estado general, riesgos, hitos, decisiones. |
| IT cliente | Avance por aplicación, SLAs, gaps, escalados. |
| Negocio | Impacto en procesos, canales de soporte, cambios relevantes. |
| Mesa de servicio | Nuevo responsable, grupos de asignación, escalado. |
| Operaciones | Alertas, guardias, procedimientos, contactos. |
| Seguridad | Accesos, secretos, restricciones, auditoría. |
| Proveedor saliente | Alcance de soporte residual y disponibilidad. |
| Proveedores externos | Nuevo canal de contacto si aplica. |

## 15.3 Mensajes clave

- Qué se asume.
- Desde cuándo.
- Quién es responsable.
- Cómo se escala.
- Qué cambia para usuarios o negocio.
- Qué no cambia.
- Qué restricciones temporales existen.
- Qué riesgos residuales están controlados.
- Qué canal usar para incidencias.
- Cuándo será la siguiente revisión.

## 15.4 Plantilla de comunicación de inicio de oleada

```markdown
# Inicio de oleada de asunción progresiva

## Alcance

A partir de [fecha], el equipo entrante asumirá la responsabilidad principal sobre:

- Aplicaciones:
- Procesos:
- Tipos de actividad:

## Modelo de soporte

- Responsable principal:
- Soporte residual:
- Escalado:
- Horario:

## Restricciones temporales

- 
- 

## Canales

- ITSM:
- Contacto operativo:
- Escalado:

## Seguimiento

- Frecuencia:
- Próxima revisión:

## Observaciones
```

## 15.5 Resultado esperado

- Cambios de responsabilidad claros.
- Menor confusión operativa.
- Cliente informado.
- Mesa de servicio alineada.
- Negocio protegido.

---

# 16. Actividad 11. Controlar SLAs, SLOs y calidad de servicio

## 16.1 Objetivo

Validar que la asunción progresiva no degrada la calidad del servicio.

## 16.2 Métricas recomendadas

| Métrica | Objetivo |
|---|---|
| Cumplimiento SLA | Confirmar calidad contractual. |
| MTTA | Medir tiempo de asignación o atención. |
| MTTR | Medir tiempo de resolución. |
| Tickets reabiertos | Medir calidad de resolución. |
| Incidencias P1/P2 | Controlar estabilidad. |
| Cambios fallidos | Medir calidad de despliegue. |
| Escalados al saliente | Medir dependencia. |
| Incidencias recurrentes | Identificar problemas no resueltos. |
| Alertas no atendidas | Medir capacidad operativa. |
| Batch fallidos | Controlar procesos críticos. |
| SLAs de proveedores | Controlar dependencias externas. |

## 16.3 Panel de control de asunción

| Indicador | Semana anterior | Semana actual | Tendencia | Estado | Comentario |
|---|---:|---:|---|---|---|
| Tickets recibidos |  |  | ↑ / ↓ / = | Verde / Ámbar / Rojo |  |
| SLA cumplido |  |  |  |  |  |
| MTTR |  |  |  |  |  |
| Escalados al saliente |  |  |  |  |  |
| Incidencias críticas |  |  |  |  |  |
| Cambios fallidos |  |  |  |  |  |
| Batch fallidos |  |  |  |  |  |

## 16.4 Criterios de alerta

Debe activarse revisión especial si:

- Se incumple un SLA crítico.
- Aumentan incidencias P1/P2.
- Se repite el mismo error.
- Aumentan escalados al saliente.
- Hay reabiertos frecuentes.
- Falla un batch crítico.
- Falla un despliegue.
- Negocio reporta pérdida de confianza.
- Aparece un riesgo regulatorio.
- Se detecta impacto en cliente final.

## 16.5 Resultado esperado

- Servicio bajo control.
- Evidencias de no degradación.
- Riesgos detectados temprano.
- Preparación objetiva para cierre.

---

# 17. Actividad 12. Gestionar riesgos residuales

## 17.1 Objetivo

Identificar, documentar, mitigar o aceptar formalmente los riesgos que siguen vivos durante la asunción.

## 17.2 Tipos de riesgos residuales

| Tipo | Ejemplo |
|---|---|
| Técnico | Rollback no probado en una aplicación. |
| Funcional | Regla compleja aún no validada por negocio. |
| Operativo | Reproceso batch requiere experto saliente. |
| Seguridad | Certificado próximo a caducar. |
| Datos | Modelo no completamente documentado. |
| Proveedor | Tercero con soporte poco claro. |
| Conocimiento | Experto único aún necesario. |
| Documentación | Runbook incompleto. |
| SLA | MTTR superior al esperado. |
| Regulatorio | Evidencias de auditoría pendientes. |

## 17.3 Matriz de riesgos residuales

| ID | Riesgo | Aplicación | Impacto | Probabilidad | Mitigación | Aceptado por | Fecha revisión |
|---|---|---|---|---|---|---|---|
| RR-001 | Reproceso recibos requiere validación saliente | Recibos | Alto | Media | Doble validación 2 semanas | Cliente |  |
| RR-002 | Rollback no probado en PRO | Emisión | Alto | Baja | Simulación PRE + restricción despliegue | Cliente |  |
| RR-003 | Documentación integración tercero incompleta | Firma | Medio | Media | Escalado proveedor documentado | Cliente |  |

## 17.4 Tratamiento recomendado

| Nivel de riesgo | Tratamiento |
|---|---|
| Crítico | No avanzar sin cierre o aceptación ejecutiva formal. |
| Alto | Mitigación obligatoria o restricción clara. |
| Medio | Plan de acción y seguimiento. |
| Bajo | Incorporar a mejora continua. |

## 17.5 Resultado esperado

- Riesgos residuales visibles.
- Mitigaciones claras.
- Aceptación formal cuando proceda.
- Sin riesgos críticos ocultos.

---

# 18. Actividad 13. Evaluar preparación para cierre y estabilización

## 18.1 Objetivo

Determinar si el servicio está suficientemente asumido como para pasar a la Fase 7.

## 18.2 Preguntas clave

- ¿Qué oleadas se han completado?
- ¿Qué aplicaciones están bajo responsabilidad principal del equipo entrante?
- ¿Qué actividades siguen condicionadas?
- ¿Se cumplen SLAs?
- ¿Se han reducido escalados al equipo saliente?
- ¿Qué gaps críticos siguen abiertos?
- ¿Qué riesgos residuales existen?
- ¿Negocio percibe continuidad?
- ¿Mesa de servicio tiene claro el modelo?
- ¿Operaciones tiene claros contactos y escalados?
- ¿Los runbooks están actualizados?
- ¿El cliente acepta pasar a estabilización?
- ¿Qué soporte saliente se mantiene en Fase 7?

## 18.3 Matriz de preparación para Fase 7

| Aplicación / dominio | Asumido | SLAs OK | Gaps críticos | Escalados saliente | Riesgo residual | Preparado Fase 7 |
|---|---|---|---|---|---|---|
| Portal mediadores | Sí | Sí | No | Bajo | Bajo | Sí |
| Emisión | Sí condicionado | Sí | No | Medio | Medio | Sí condicionado |
| Recibos | Parcial | Sí | Sí | Alto | Alto | No |
| Siniestros | Sí | Sí | No | Bajo | Medio | Sí |

## 18.4 Decisiones posibles

| Decisión | Significado |
|---|---|
| Go | Puede pasar a Fase 7. |
| Go condicionado | Puede pasar con restricciones y seguimiento especial. |
| No-Go parcial | Algunas aplicaciones deben permanecer en Fase 6. |
| No-Go | La asunción no está suficientemente consolidada. |

## 18.5 Resultado esperado

- Decisión Go / No-Go hacia Fase 7.
- Aplicaciones plenamente asumidas.
- Aplicaciones condicionadas.
- Aplicaciones no preparadas.
- Plan de estabilización definido.

---

# 19. Entregables de la Fase 6

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Plan de asunción progresiva | Oleadas, calendario, criterios y restricciones. | Transition Manager |
| Matriz de oleadas | Alcance y estado por oleada. | Transition Manager |
| RACI de asunción | Responsabilidades durante la toma de servicio. | Service Manager |
| Matriz de soporte residual | Cuándo y cómo interviene el equipo saliente. | Transition Manager |
| Comunicaciones de oleada | Avisos a cliente, negocio y operación. | Service Manager |
| Panel de SLAs y métricas | Seguimiento de calidad durante asunción. | Service Manager |
| Matriz de escalados al saliente | Medición de dependencia residual. | Líder técnico / Service Manager |
| Matriz de riesgos residuales | Riesgos vivos y mitigaciones. | Transition Manager |
| Matriz de gaps de asunción | Pendientes detectados durante toma de servicio. | Transition Manager |
| Modelo BAU inicial | Roles, comités, reporting y operación ordinaria. | Service Manager |
| Actas de revisión de oleadas | Evidencia de avance y decisiones. | Transition Manager |
| Decisión Go / No-Go a Fase 7 | Validación formal de paso a estabilización. | Cliente + Transition Manager |

---

# 20. Plantillas útiles de la Fase 6

## 20.1 Matriz de estado de oleadas

| Oleada | Alcance | Fecha inicio | Estado | SLAs | Escalados saliente | Gaps | Decisión |
|---|---|---|---|---|---|---|---|
| Oleada 1 |  |  | En curso / Cerrada | OK / Riesgo | Alto / Medio / Bajo |  | Go / No-Go |
| Oleada 2 |  |  |  |  |  |  |  |

## 20.2 Matriz de actividades asumidas

| Aplicación | Actividad | Responsable entrante | Soporte saliente | Restricción | Estado |
|---|---|---|---|---|---|
|  | Tickets L2 |  | Bajo demanda |  | Asumido |
|  | Despliegues PRE |  | No |  | Asumido |
|  | Reprocesos batch |  | Sí | Autorización negocio | Condicionado |

## 20.3 Matriz de escalados al equipo saliente

| Fecha | Aplicación | Motivo | Criticidad | Resuelto por saliente | Acción para evitar repetición |
|---|---|---|---|---|---|
|  |  |  | Alta / Media / Baja | Sí / No |  |

## 20.4 Checklist de cierre de oleada

```markdown
# Checklist de cierre de oleada

## Alcance

- [ ] Aplicaciones incluidas confirmadas.
- [ ] Actividades asumidas confirmadas.
- [ ] Restricciones documentadas.

## Operación

- [ ] Tickets gestionados por equipo entrante.
- [ ] SLAs cumplidos.
- [ ] Incidencias críticas revisadas.
- [ ] Escalados al saliente analizados.
- [ ] Tareas recurrentes ejecutadas.
- [ ] Despliegues realizados si aplica.
- [ ] Batch validado si aplica.

## Documentación

- [ ] Runbooks actualizados.
- [ ] Matriz de escalado actualizada.
- [ ] KB actualizada.
- [ ] Gaps registrados.
- [ ] Riesgos residuales registrados.

## Decisión

- [ ] Go / No-Go realizado.
- [ ] Riesgos aceptados si aplica.
- [ ] Comunicación de cierre enviada.
```

## 20.5 Plantilla de informe semanal de asunción

```markdown
# Informe semanal de asunción progresiva

## Semana

## Estado general

- Verde / Ámbar / Rojo

## Oleadas activas

| Oleada | Estado | Comentario |
|---|---|---|

## Métricas

| Métrica | Valor | Tendencia | Comentario |
|---|---:|---|---|
| Tickets gestionados |  |  |  |
| SLA cumplido |  |  |  |
| Escalados al saliente |  |  |  |
| Incidencias críticas |  |  |  |
| Gaps críticos |  |  |  |

## Riesgos

## Gaps

## Decisiones requeridas

## Próximos pasos
```

---

# 21. Checklist operativo de Fase 6

## 21.1 Preparación

- [ ] Revisar matriz de autonomía de Fase 5.
- [ ] Revisar Go / No-Go de Fase 5.
- [ ] Definir oleadas.
- [ ] Definir criterios de éxito por oleada.
- [ ] Definir restricciones.
- [ ] Definir soporte residual del saliente.
- [ ] Definir RACI temporal.
- [ ] Confirmar accesos.
- [ ] Confirmar runbooks.
- [ ] Confirmar SLAs.
- [ ] Comunicar inicio de asunción.

## 21.2 Activación de oleadas

- [ ] Activar primera oleada.
- [ ] Informar a mesa de servicio.
- [ ] Informar a operaciones.
- [ ] Informar a negocio si aplica.
- [ ] Registrar fecha de inicio.
- [ ] Activar seguimiento diario.
- [ ] Monitorizar tickets.
- [ ] Monitorizar SLAs.
- [ ] Registrar escalados.
- [ ] Revisar gaps.

## 21.3 Operación

- [ ] Gestionar tickets por equipo entrante.
- [ ] Gestionar incidencias.
- [ ] Ejecutar tareas recurrentes.
- [ ] Ejecutar cambios autorizados.
- [ ] Revisar batch.
- [ ] Gestionar comunicaciones.
- [ ] Escalar según matriz.
- [ ] Actualizar documentación.
- [ ] Revisar riesgos.

## 21.4 Reducción de dependencia

- [ ] Medir escalados al saliente.
- [ ] Analizar causas.
- [ ] Cerrar gaps repetidos.
- [ ] Actualizar FAQs.
- [ ] Reforzar formación.
- [ ] Hacer simulacros adicionales si procede.
- [ ] Transferir contactos de terceros.
- [ ] Validar autonomía.

## 21.5 BAU inicial

- [ ] Activar modelo de soporte.
- [ ] Activar reporting de servicio.
- [ ] Activar gestión de problemas.
- [ ] Activar gestión de cambios.
- [ ] Activar mantenimiento de runbooks.
- [ ] Confirmar comités BAU.
- [ ] Confirmar responsables permanentes.
- [ ] Confirmar canales de comunicación.

## 21.6 Cierre de fase

- [ ] Evaluar todas las oleadas.
- [ ] Revisar SLAs.
- [ ] Revisar riesgos residuales.
- [ ] Revisar gaps abiertos.
- [ ] Revisar dependencia saliente.
- [ ] Preparar Go / No-Go a Fase 7.
- [ ] Definir plan de estabilización.
- [ ] Comunicar resultado.

---

# 22. Riesgos específicos de la Fase 6

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Asunción demasiado rápida | Incidencias o incumplimiento SLA | Oleadas progresivas y Go / No-Go por dominio. |
| Ambigüedad de responsabilidad | Tickets mal asignados o retrasos | RACI claro y comunicación a mesa de servicio. |
| Dependencia oculta del equipo saliente | Falsa autonomía | Medir escalados y motivos. |
| Gaps críticos no cerrados | Riesgo operativo | Bloquear oleada o aceptar formalmente riesgo. |
| SLAs degradados | Pérdida de confianza cliente | Control diario y refuerzo temporal. |
| Reprocesos batch sin control | Impacto financiero o contable | Doble validación y restricciones. |
| Despliegues sin madurez suficiente | Fallos productivos | Restricciones y apoyo saliente temporal. |
| Negocio no informado | Confusión y pérdida de confianza | Comunicación por oleada. |
| Mesa de servicio no alineada | Tickets mal canalizados | Actualizar grupos y procedimientos ITSM. |
| Saliente se retira antes de tiempo | Pérdida de apoyo crítico | Matriz de soporte residual acordada. |
| Saliente interviene demasiado | No se consolida autonomía | Limitar intervención a criterios definidos. |
| Riesgos residuales no aceptados | Cierre débil | Registro formal y aceptación cliente. |

---

# 23. Criterios de salida de la Fase 6

## 23.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Plan de asunción definido | Plan de oleadas | Pendiente / En curso / Validado |
| Oleadas ejecutadas | Matriz de oleadas |  |
| Responsabilidad principal transferida | RACI / comunicaciones |  |
| Tickets gestionados por entrante | ITSM / informes |  |
| SLAs cumplidos | Panel de servicio |  |
| Escalados al saliente reducidos | Matriz de escalados |  |
| Gaps críticos cerrados o mitigados | Matriz de gaps |  |
| Riesgos residuales documentados | RAID log |  |
| Runbooks actualizados | Repositorio documental |  |
| Modelo BAU inicial activado | Documento BAU |  |
| Mesa de servicio alineada | Comunicación / ITSM |  |
| Negocio informado | Comunicaciones |  |
| Soporte residual definido para Fase 7 | Matriz soporte residual |  |
| Go / No-Go hacia Fase 7 realizado | Acta de decisión |  |

## 23.2 Criterio de salida recomendado

La Fase 6 puede considerarse cerrada cuando:

> El equipo entrante ha asumido la responsabilidad principal de las aplicaciones, dominios o actividades acordadas, opera con cumplimiento de SLAs, mantiene una dependencia residual controlada del equipo saliente, tiene gaps críticos cerrados o mitigados, riesgos residuales documentados y un modelo BAU inicial activo, lo que permite pasar a la Fase 7 de cierre y estabilización.

---

# 24. Recomendaciones prácticas para liderar la Fase 6

## 24.1 Recomendaciones de enfoque

- No asumir todo el servicio de golpe.
- Usar oleadas pequeñas y controlables.
- Empezar por lo que tenga autonomía demostrada.
- Mantener seguimiento diario al principio.
- Medir dependencia real del saliente.
- No confundir ausencia de incidencias con madurez.
- Revisar calidad de resolución, no solo cantidad de tickets.
- Mantener comunicación frecuente con cliente.
- Documentar restricciones sin ocultarlas.
- Controlar especialmente batch, recibos, siniestros y documentación contractual.
- Evitar que el equipo saliente siga operando por costumbre.
- Evitar retirar al equipo saliente antes de tiempo.
- Preparar desde esta fase la estabilización BAU.

## 24.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- Los tickets siguen yendo al equipo saliente.
- El equipo entrante escala todo por inseguridad.
- El equipo entrante no escala cuando debería.
- La mesa de servicio no sabe a quién asignar.
- Negocio sigue contactando con el equipo saliente.
- Los SLAs empiezan a degradarse.
- Los runbooks no se actualizan.
- Se repiten dudas ya resueltas.
- Aparecen incidencias por mala clasificación.
- Hay reprocesos no autorizados.
- No se registran riesgos residuales.
- Se avanza por calendario, no por evidencia.

## 24.3 Buenas prácticas

- Definir oleadas con criterios claros.
- Comunicar cada cambio de responsabilidad.
- Mantener un panel visible de métricas.
- Revisar diariamente escalados al saliente.
- Convertir cada escalado repetido en acción.
- Mantener el RAID log vivo.
- Cerrar cada oleada formalmente.
- Validar autonomía por dominio.
- Acordar soporte residual explícito.
- Pasar a BAU solo cuando haya evidencias suficientes.

---

# 25. Resumen ejecutivo de la Fase 6

La Fase 6 es el paso desde la ejecución supervisada hacia la responsabilidad real.

Su valor está en transferir el servicio sin salto al vacío. El equipo entrante asume progresivamente, el equipo saliente reduce su intervención y el cliente observa que la continuidad del servicio se mantiene.

La fase debe demostrar:

1. Que el equipo entrante puede operar como responsable principal.
2. Que los SLAs se mantienen.
3. Que los tickets se gestionan correctamente.
4. Que los escalados al equipo saliente disminuyen.
5. Que los procesos críticos están controlados.
6. Que los runbooks son utilizables.
7. Que los riesgos residuales son visibles.
8. Que negocio y operaciones saben a quién acudir.
9. Que el modelo BAU empieza a funcionar.
10. Que la transición puede avanzar hacia cierre y estabilización.

La Fase 6 no debe cerrarse porque haya llegado la fecha prevista, sino porque la responsabilidad se ha transferido con evidencias y el servicio se mantiene estable.

---
