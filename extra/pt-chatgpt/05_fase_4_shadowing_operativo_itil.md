# Fase 4. Shadowing operativo  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 4

La **Fase 4. Shadowing operativo** tiene como objetivo que el equipo entrante observe al equipo saliente mientras este ejecuta la operación real del servicio.

Hasta este punto, el equipo entrante ha recibido información de contexto, inventario, conocimiento funcional y conocimiento técnico. Sin embargo, todavía existe una diferencia importante entre **saber cómo debería funcionar el servicio** y **ver cómo se opera realmente**.

El shadowing permite observar:

- Cómo se gestionan incidencias reales.
- Cómo se diagnostican errores.
- Cómo se consultan logs y monitorización.
- Cómo se ejecutan despliegues.
- Cómo se toman decisiones bajo presión.
- Cómo se escalan problemas.
- Cómo se comunican impactos.
- Cómo se ejecutan procesos batch.
- Cómo se realizan validaciones funcionales.
- Cómo se usan workarounds.
- Qué conocimiento tácito utiliza el equipo saliente.
- Qué diferencias existen entre documentación y práctica real.

Esta fase es especialmente importante en entornos aseguradores, donde muchas operaciones críticas no son puramente técnicas, sino técnico-funcionales: emisión, recibos, renovaciones, siniestros, documentación contractual, integraciones bancarias, firma electrónica, mediadores, reporting y procesos batch.

---

## 2. Resultado esperado de la Fase 4

Al finalizar esta fase, el equipo entrante debe haber observado suficientes situaciones reales o simuladas como para comprender cómo se opera el servicio en la práctica.

Los resultados esperados son:

- Incidencias reales observadas y documentadas.
- Despliegues observados y contrastados contra runbooks.
- Procesos batch críticos observados.
- Procedimientos de escalado entendidos.
- Monitorización y alertas revisadas en contexto real.
- Búsquedas de logs y diagnóstico capturadas.
- Workarounds documentados.
- Conocimiento tácito convertido en runbooks, checklists o entradas de base de conocimiento.
- Diferencias entre documentación y operación real identificadas.
- Gaps operativos registrados y priorizados.
- Riesgos actualizados en el RAID log.
- Preparación suficiente para pasar a la Fase 5, reverse shadowing.
- Evidencias ITIL de incidencias, eventos, problemas, cambios, despliegues y escalados observados.
- Runbooks y base de conocimiento actualizados con estado de validación operativo.
- Registro de problemas recurrentes, workarounds y oportunidades de mejora continua.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **3 a 6 semanas**.

Puede ser menor si:

- Hay pocas aplicaciones críticas.
- La operación está muy documentada.
- El volumen de incidencias es suficiente para observar casos relevantes.
- Hay despliegues frecuentes.
- El equipo saliente tiene buena disponibilidad.
- Los procesos batch son simples.

Puede alargarse si:

- Hay muchas aplicaciones críticas.
- Existen pocos eventos reales durante la ventana de shadowing.
- Los despliegues son poco frecuentes.
- Los procesos batch críticos tienen ventanas concretas.
- Hay guardias o incidencias fuera de horario.
- Existen sistemas legacy.
- Hay dependencias con terceros.
- La operación real difiere de la documentación.
- Hay baja colaboración o disponibilidad del equipo saliente.


---

# 1. Alineamiento ITIL específico de la Fase 4

La Fase 4 se alinea de forma directa con las prácticas ITIL relacionadas con la operación real del servicio. En esta fase el conocimiento deja de ser principalmente documental o explicativo y pasa a contrastarse con la ejecución diaria: tickets, incidencias, alertas, despliegues, escalados, comunicaciones, procesos batch, workarounds y decisiones operativas.

El objetivo ITIL de esta fase es validar cómo se ejecutan en la práctica los procesos de gestión del servicio y convertir esa observación en conocimiento operativo reutilizable. Por tanto, el shadowing no debe tratarse como una asistencia pasiva a reuniones, sino como una actividad formal de verificación operativa.

## 4.1 Prácticas ITIL relacionadas

| Práctica ITIL | Aplicación en esta fase |
|---|---|
| **Incident Management** | Observación de la gestión real de incidencias, desde la detección hasta el cierre. |
| **Monitoring and Event Management** | Revisión de alertas, dashboards, eventos, umbrales, falsos positivos y canales de notificación. |
| **Problem Management** | Identificación de problemas recurrentes, causas raíz, workarounds y deuda operativa. |
| **Knowledge Management** | Conversión del conocimiento tácito observado en runbooks, KB, checklists y guías de diagnóstico. |
| **Service Desk** | Comprensión del flujo real de tickets, clasificación, priorización, comunicación y cierre. |
| **Service Level Management** | Observación del impacto de las incidencias y cambios sobre SLAs, OLAs y compromisos operativos. |
| **Change Enablement** | Observación de cambios, despliegues, hotfixes, aprobaciones y validaciones. |
| **Release Management** | Observación de releases planificadas, paquetes desplegados, evidencias y comunicación asociada. |
| **Deployment Management** | Observación de la ejecución real de despliegues y rollback. |
| **Supplier Management** | Observación de escalados a terceros, proveedores críticos, bancos, firma, documental o comunicaciones. |
| **Information Security Management** | Control de evidencias, accesos, datos sensibles, certificados, secretos y restricciones de producción. |
| **Continual Improvement** | Identificación de mejoras operativas, automatizaciones, ajustes de monitorización y documentación pendiente. |

## 4.2 Objetivo ITIL de la fase

Desde la perspectiva ITIL, esta fase debe demostrar que el equipo entrante entiende cómo se opera realmente el servicio y cómo se ejecutan los procesos de gestión en situaciones reales.

La fase deberá aportar evidencias sobre:

- Cómo se detectan incidencias y eventos.
- Cómo se clasifican y priorizan tickets.
- Cómo se gestionan severidades y SLAs.
- Cómo se diagnostican incidencias técnicas y funcionales.
- Cómo se aplican workarounds.
- Cómo se escalan problemas a otros equipos o proveedores.
- Cómo se comunican impactos a negocio, usuarios o dirección.
- Cómo se ejecutan cambios y despliegues.
- Cómo se monitoriza el servicio tras una intervención.
- Cómo se capturan lecciones aprendidas.
- Cómo se actualiza la base de conocimiento.

## 4.3 Evidencias ITIL esperadas

| Evidencia | Práctica ITIL relacionada | Propósito |
|---|---|---|
| Actas de observación de incidencias | Incident Management | Demostrar comprensión del ciclo de vida de la incidencia. |
| Registro de eventos y alertas observadas | Monitoring and Event Management | Identificar cómo se detectan y gestionan eventos. |
| Matriz de problemas recurrentes | Problem Management | Separar síntomas repetidos de causas estructurales. |
| Runbooks actualizados | Knowledge Management | Convertir observación en procedimiento operativo. |
| Entradas de base de conocimiento | Knowledge Management | Documentar errores frecuentes, workarounds y diagnóstico. |
| Actas de despliegue observado | Change Enablement / Deployment Management | Validar cómo se ejecutan cambios reales. |
| Registro de escalados | Supplier Management / Service Desk | Confirmar rutas reales de soporte y proveedores. |
| Evidencias de comunicación | Service Level Management | Entender comunicación de impacto, SLA y seguimiento. |
| RAID log actualizado | Risk Management / Continual Improvement | Incorporar riesgos operativos reales. |
| Registro de mejoras operativas | Continual Improvement | Capturar oportunidades de mejora derivadas del shadowing. |

## 4.4 Diferencia entre shadowing operativo e ITIL operativo

El shadowing no debe limitarse a “ver trabajar” al equipo saliente. Debe permitir verificar cómo se comportan realmente las prácticas ITIL que sostienen el servicio.

| Observación tradicional | Observación alineada con ITIL |
|---|---|
| Ver cómo se resuelve una incidencia. | Entender detección, clasificación, impacto, SLA, diagnóstico, escalado, comunicación, resolución y cierre. |
| Ver un despliegue. | Entender cambio, aprobación, release, despliegue, validación, rollback, evidencias y cierre. |
| Ver una alerta. | Entender evento, umbral, severidad, falso positivo, acción esperada y relación con runbook. |
| Escuchar una explicación informal. | Convertir el conocimiento tácito en KB, checklist, runbook o problema conocido. |
| Revisar un ticket. | Identificar si debe generar problema, mejora, workaround o actualización documental. |

## 4.5 Relación con la preparación para reverse shadowing

La Fase 4 debe generar la base objetiva para decidir qué aplicaciones, procesos o actividades pueden pasar a reverse shadowing.

Desde una perspectiva ITIL, una aplicación o dominio estará preparado para reverse shadowing cuando el equipo entrante haya observado, comprendido y documentado suficientemente:

- Flujo de tickets.
- Incidencias frecuentes.
- Alertas y eventos relevantes.
- Procedimientos de diagnóstico.
- Escalados.
- Workarounds.
- Cambios y despliegues.
- Validaciones funcionales y técnicas.
- Riesgos operativos.
- Límites de actuación.

---

# 2. Principios de trabajo de la Fase 4

## 4.1 Observar sin interferir

Durante el shadowing, el equipo entrante observa, pregunta y documenta, pero no asume todavía la responsabilidad principal de operar.

La regla general es:

> El equipo saliente opera; el equipo entrante observa, registra y pregunta.

Esto evita introducir riesgo operativo prematuro.

## 4.2 Observar la realidad, no solo el procedimiento formal

El objetivo no es comprobar si el equipo saliente sigue el procedimiento escrito, sino entender cómo se opera realmente el servicio.

Deben capturarse:

- Pasos formales.
- Pasos informales.
- Decisiones no documentadas.
- Validaciones manuales.
- Herramientas realmente usadas.
- Contactos reales de escalado.
- Workarounds.
- Comprobaciones de experiencia.
- Señales de alerta que no aparecen en documentación.

## 4.3 Convertir observación en conocimiento accionable

Cada observación debe acabar en algún artefacto:

- Runbook actualizado.
- Checklist.
- Entrada de base de conocimiento.
- Matriz de incidencias frecuentes.
- Matriz de escalado.
- Procedimiento de diagnóstico.
- Gap.
- Riesgo.
- Acción de mejora.
- Caso candidato para reverse shadowing.

Observar sin documentar no transfiere conocimiento.

## 4.4 Priorizar casos críticos

No todo lo que se observa tiene el mismo valor. Deben priorizarse situaciones relacionadas con:

- Producción.
- Cliente final.
- Mediadores.
- Emisión de pólizas.
- Recibos y cobros.
- Siniestros.
- Renovaciones.
- Documentación contractual.
- Integraciones bancarias.
- Firma electrónica.
- Reporting regulatorio.
- Procesos batch.
- Seguridad.
- Recuperación.
- SLAs.

## 4.5 Mantener seguridad operativa

El shadowing no debe poner en riesgo el servicio.

Por tanto:

- El equipo entrante no debe ejecutar acciones productivas sin autorización.
- Las sesiones de observación deben respetar protocolos de seguridad.
- No deben compartirse secretos en claro.
- No deben grabarse sesiones con datos sensibles sin autorización.
- No deben copiarse datos productivos fuera de herramientas autorizadas.
- La observación de producción debe seguir controles de acceso.
- Las evidencias deben anonimizarse si contienen datos sensibles.

---

# 3. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Preparar plan de shadowing | Casos, responsables, calendario y criterios de observación. |
| Semana 1-2 | Observar operación diaria y gestión de tickets | Comprender dinámica real de soporte. |
| Semana 2-4 | Observar incidencias, diagnóstico y escalados | Capturar procedimientos reales y conocimiento tácito. |
| Semana 2-5 | Observar despliegues y cambios | Validar runbooks de despliegue y rollback. |
| Semana 3-5 | Observar procesos batch y cierres | Documentar ejecución, fallos, validaciones y reprocesos. |
| Semana 4-6 | Consolidar aprendizajes y actualizar documentación | Runbooks, KB, gaps, riesgos y preparación de reverse shadowing. |

---

# 4. Actividad 1. Preparar el plan de shadowing

## 6.1 Objetivo

Definir qué actividades deben observarse, con qué responsables, en qué fechas y con qué criterios de captura.

## 6.2 Entradas necesarias

- Inventario de aplicaciones críticas.
- Matriz de criticidad.
- Matriz de procesos funcionales.
- Matriz técnica de componentes.
- Runbooks iniciales de Fase 3.
- Matriz de incidencias recurrentes.
- Matriz de procesos batch.
- Matriz de despliegues.
- Matriz de integraciones.
- Catálogo de alertas.
- RAID log.
- Gaps funcionales y técnicos pendientes.

## 6.3 Tipos de actividades a observar

| Tipo de actividad | Ejemplos |
|---|---|
| Gestión de incidencias | P1, P2, incidencias recurrentes, incidencias funcionales. |
| Diagnóstico técnico | Logs, APM, BBDD, colas, integraciones. |
| Diagnóstico funcional | Estados de póliza, recibo, siniestro, documento. |
| Despliegues | Releases, hotfixes, cambios de configuración. |
| Rollback | Reversión de versión, desactivación funcional, contingencia. |
| Batch | Ejecución, fallo, reinicio, reproceso, validación. |
| Monitorización | Alertas, dashboards, falsos positivos, umbrales. |
| Escalado | Interno, cliente, proveedor tercero, comité de crisis. |
| Comunicación | Avisos a negocio, usuarios, dirección, mesa de servicio. |
| Seguridad | Certificados, accesos, secretos, incidentes de seguridad. |
| DR / recuperación | Restore, contingencia, validación de backups. |

## 6.4 Matriz de planificación de shadowing

| ID | Caso a observar | Aplicación / dominio | Tipo | Criticidad | Responsable saliente | Observador entrante | Fecha prevista | Estado |
|---|---|---|---|---|---|---|---|---|
| SH-001 | Gestión incidencia recibos | Recibos | Incidencia | Crítica |  |  |  | Planificado |
| SH-002 | Despliegue API emisión | Emisión | Despliegue | Alta |  |  |  | Planificado |
| SH-003 | Ejecución batch renovaciones | Renovaciones | Batch | Crítica |  |  |  | Planificado |
| SH-004 | Revisión alertas portal mediadores | Mediadores | Monitorización | Alta |  |  |  | Planificado |

## 6.5 Preguntas clave

- ¿Qué casos son obligatorios antes de pasar a reverse shadowing?
- ¿Qué casos pueden ser simulados si no ocurren de forma natural?
- ¿Qué incidencias recurrentes deberían observarse?
- ¿Qué despliegues están previstos?
- ¿Qué procesos batch críticos se ejecutan durante la ventana de shadowing?
- ¿Qué expertos salientes deben participar?
- ¿Qué miembros del equipo entrante deben observar cada caso?
- ¿Qué evidencias se deben capturar?
- ¿Qué restricciones de seguridad aplican?
- ¿Qué actividades requieren autorización del cliente?

## 6.6 Entregables

- Plan de shadowing.
- Calendario de observación.
- Matriz de casos.
- Lista de observadores.
- Lista de responsables salientes.
- Plantilla de observación.
- Criterios de evidencia.
- Reglas de seguridad para observación.

---

# 5. Actividad 2. Observar la operación diaria del servicio

## 7.1 Objetivo

Comprender cómo se gestiona el servicio en el día a día: entrada de tickets, priorización, asignación, coordinación, comunicación y seguimiento.

## 7.2 Aspectos a observar

- Herramienta ITSM utilizada.
- Bandejas de entrada.
- Clasificación de tickets.
- Severidades.
- Priorización.
- Asignación a grupos.
- Revisión diaria de pendientes.
- Reuniones operativas.
- Comunicación con negocio.
- Comunicación con usuarios.
- Gestión de SLAs.
- Cambios de prioridad.
- Escalados.
- Cierre de tickets.
- Documentación de resolución.
- Relación entre incidencias, problemas y cambios.

## 7.3 Preguntas clave

- ¿Cómo entra una incidencia?
- ¿Quién la clasifica?
- ¿Cómo se decide la severidad?
- ¿Quién asigna el ticket?
- ¿Qué criterios se usan para priorizar?
- ¿Cómo se identifica impacto funcional?
- ¿Cómo se relaciona con SLA?
- ¿Cuándo se escala?
- ¿Quién comunica a negocio?
- ¿Qué información mínima debe tener un ticket?
- ¿Qué errores de clasificación son habituales?
- ¿Qué tickets se tratan fuera de herramienta?
- ¿Qué casos generan war room o comité de crisis?
- ¿Cómo se documenta la resolución?
- ¿Cómo se evitan reaperturas?

## 7.4 Plantilla de observación de operación diaria

| Elemento observado | Descripción | Evidencia | Gap / riesgo | Acción |
|---|---|---|---|---|
| Entrada de tickets |  |  |  |  |
| Priorización |  |  |  |  |
| Escalado |  |  |  |  |
| Comunicación |  |  |  |  |
| Cierre |  |  |  |  |

## 7.5 Resultado esperado

- Comprensión del flujo real de tickets.
- Identificación de roles operativos.
- Identificación de criterios reales de severidad.
- Identificación de comunicaciones clave.
- Identificación de gaps en ITSM.
- Actualización de runbooks de soporte.

---

# 6. Actividad 3. Observar gestión de incidencias reales

## 8.1 Objetivo

Ver cómo el equipo saliente diagnostica, contiene, resuelve y comunica incidencias reales.

## 8.2 Tipos de incidencias a observar

| Tipo | Ejemplo |
|---|---|
| Técnica | Error de aplicación, caída de servicio, timeout, memoria, conexión. |
| Funcional | Póliza bloqueada, recibo no generado, documento incorrecto. |
| Integración | Error con banco, firma, documental, mediador, tercero. |
| Batch | Job fallido, proceso incompleto, fichero no generado. |
| Datos | Estado inconsistente, registro duplicado, error de parametrización. |
| Seguridad | Acceso denegado, certificado caducado, credencial fallida. |
| Rendimiento | Lentitud, saturación, bloqueo, degradación. |

## 8.3 Qué observar durante una incidencia

- Detección inicial.
- Fuente de alerta.
- Clasificación.
- Confirmación de impacto.
- Consulta de logs.
- Consulta de monitorización.
- Consulta de BBDD.
- Revisión funcional.
- Identificación de causa probable.
- Contención.
- Workaround.
- Escalado.
- Comunicación.
- Resolución.
- Validación técnica.
- Validación funcional.
- Cierre.
- Lecciones aprendidas.

## 8.4 Preguntas clave

- ¿Cómo se detectó la incidencia?
- ¿Quién la detectó?
- ¿Cómo se confirmó impacto?
- ¿Qué se miró primero?
- ¿Qué dashboard se usó?
- ¿Qué logs se consultaron?
- ¿Qué búsqueda fue útil?
- ¿Qué tabla o dato se revisó?
- ¿Qué integración se verificó?
- ¿Qué hipótesis se descartaron?
- ¿Qué acción contuvo el impacto?
- ¿Qué workaround se aplicó?
- ¿Quién decidió escalar?
- ¿Quién validó la resolución?
- ¿Cómo se comunicó?
- ¿Qué debería quedar documentado?

## 8.5 Plantilla de observación de incidencia

```markdown
# Observación de incidencia

## Datos básicos

- ID de ticket:
- Fecha:
- Aplicación:
- Proceso afectado:
- Severidad:
- Observador entrante:
- Responsable saliente:
- Estado final:

## Descripción de la incidencia

## Detección

- Fuente:
- Alerta:
- Usuario / negocio:
- Monitorización:

## Impacto

- Usuarios afectados:
- Proceso afectado:
- Impacto cliente:
- Impacto económico:
- Impacto regulatorio:
- SLA:

## Diagnóstico observado

1.
2.
3.

## Herramientas utilizadas

- ITSM:
- Logs:
- Monitorización:
- BBDD:
- Otros:

## Causa probable / causa raíz

## Acción de contención

## Resolución

## Validación posterior

## Comunicación realizada

## Workaround identificado

## Conocimiento tácito capturado

## Gaps detectados

## Riesgos detectados

## Acciones posteriores
```

## 8.6 Resultado esperado

- Incidencias documentadas como casos de aprendizaje.
- Mejora de guías de diagnóstico.
- Workarounds identificados.
- Errores frecuentes registrados.
- Gaps y riesgos actualizados.
- Casos candidatos para reverse shadowing.

---

# 7. Actividad 4. Observar diagnóstico técnico

## 9.1 Objetivo

Aprender cómo el equipo saliente investiga técnicamente un problema.

## 9.2 Herramientas habituales

| Área | Herramientas posibles |
|---|---|
| ITSM | ServiceNow, Jira Service Management, Remedy. |
| Logs | Splunk, ELK, OpenSearch, ficheros locales. |
| APM | Dynatrace, AppDynamics, New Relic, Application Insights. |
| Métricas | Grafana, Prometheus, CloudWatch, Azure Monitor. |
| BBDD | SQL Developer, SSMS, DBeaver, herramientas corporativas. |
| Batch | Control-M, Autosys, Jenkins, planificadores internos. |
| CI/CD | Jenkins, Azure DevOps, GitLab, GitHub Actions. |
| Infraestructura | Kubernetes, OpenShift, servidores, consolas cloud. |
| Integraciones | API Gateway, ESB, colas, Kafka, MQ. |

## 9.3 Qué capturar

- Búsquedas de logs útiles.
- Dashboards usados.
- Métricas relevantes.
- Consultas SQL frecuentes.
- Health checks.
- Comandos de diagnóstico.
- Errores conocidos.
- Correlation IDs.
- Validaciones de integración.
- Validaciones batch.
- Criterios para distinguir falso positivo de alerta real.
- Indicadores de degradación.
- Señales tempranas de problema.

## 9.4 Matriz de diagnóstico

| Síntoma | Herramienta | Qué revisar | Señal esperada | Causa probable | Acción |
|---|---|---|---|---|---|
| Error 500 | Logs aplicación | Stacktrace / correlation ID | Excepción servicio | Error backend | Revisar API |
| Recibo no generado | BBDD / batch | Estado póliza y job | Job incompleto | Batch fallido | Reproceso |
| Documento no emitido | Logs documental | Petición a gestor | Error plantilla | Datos incompletos | Regenerar |
| Timeout | APM | Latencia integración | Pico de respuesta | Tercero lento | Escalar proveedor |

## 9.5 Resultado esperado

- Guías de diagnóstico enriquecidas.
- Búsquedas útiles documentadas.
- Dashboards relevantes identificados.
- Consultas y validaciones frecuentes registradas.
- Mejora de runbooks técnicos.

---

# 8. Actividad 5. Observar incidencias funcionales-técnicas

## 10.1 Objetivo

Capturar cómo se resuelven incidencias que combinan lógica funcional y análisis técnico.

En seguros, muchas incidencias tienen esta naturaleza híbrida. No basta con mirar logs; hay que entender estados, productos, documentos, recibos, reglas, fechas, parametrización y procesos.

## 10.2 Casos típicos

| Proceso | Incidencia |
|---|---|
| Emisión | Póliza emitida sin documento correcto. |
| Cotización | Prima incorrecta o descuento no aplicado. |
| Recibos | Recibo no generado, duplicado o devuelto. |
| Renovaciones | Póliza no renovada o renovada con importe incorrecto. |
| Siniestros | Expediente bloqueado o pago no autorizado. |
| Mediadores | Operación no visible en portal. |
| Documental | Documento contractual no generado o generado con datos incorrectos. |
| Firma | Firma no completada o callback no recibido. |
| Reporting | Datos descuadrados frente a sistema origen. |

## 10.3 Qué observar

- Cómo se identifica el proceso afectado.
- Qué estado funcional se revisa.
- Qué datos se consultan.
- Qué reglas aplican.
- Qué parametrización se valida.
- Qué integración participa.
- Qué workaround existe.
- Quién valida funcionalmente.
- Qué riesgo contractual o económico existe.
- Cómo se documenta el caso.

## 10.4 Preguntas clave

- ¿Qué estado funcional debería tener el registro?
- ¿Qué estado tiene realmente?
- ¿Qué regla debería haberse aplicado?
- ¿Dónde se implementa esa regla?
- ¿Qué datos alimentan el proceso?
- ¿Qué documento o recibo debería haberse generado?
- ¿Qué validación funcional confirma la resolución?
- ¿Cuándo debe intervenir negocio?
- ¿Qué casos no se deben corregir manualmente?
- ¿Qué correcciones requieren aprobación?

## 10.5 Resultado esperado

- Casos funcionales-técnicos documentados.
- Reglas de diagnóstico funcional incorporadas.
- Validaciones de negocio identificadas.
- Riesgos de corrección manual registrados.
- Runbooks enriquecidos con visión funcional.

---

# 9. Actividad 6. Observar despliegues y cambios

## 11.1 Objetivo

Ver cómo se ejecutan realmente los despliegues y cambios, desde la preparación hasta la validación posterior.

## 11.2 Tipos de despliegues a observar

| Tipo | Ejemplo |
|---|---|
| Release planificada | Nueva versión de aplicación. |
| Hotfix | Corrección urgente de producción. |
| Cambio de configuración | Variable, parámetro, feature flag. |
| Cambio batch | Script, job, planificación. |
| Cambio de BBDD | Script SQL, procedimiento, índice. |
| Cambio documental | Plantilla, texto, generación documental. |
| Cambio de integración | Endpoint, certificado, contrato API. |

## 11.3 Qué observar

- Ticket de cambio.
- Aprobaciones.
- Rama o tag.
- Artefacto.
- Pipeline.
- Variables.
- Ventana.
- Comunicación previa.
- Backup previo.
- Validaciones predespliegue.
- Ejecución.
- Validaciones postdespliegue.
- Smoke test.
- Validación funcional.
- Monitorización posterior.
- Criterios de rollback.
- Evidencias.
- Cierre del cambio.

## 11.4 Preguntas clave

- ¿Qué debe estar aprobado antes de desplegar?
- ¿Cómo se sabe qué versión se despliega?
- ¿Quién ejecuta el despliegue?
- ¿Quién observa?
- ¿Quién valida?
- ¿Qué puede fallar?
- ¿Qué se mira durante el despliegue?
- ¿Qué se mira después?
- ¿Cuánto tiempo se monitoriza?
- ¿Qué criterio activa rollback?
- ¿Quién decide rollback?
- ¿Qué evidencia se guarda?
- ¿Qué comunicación se envía?

## 11.5 Plantilla de observación de despliegue

```markdown
# Observación de despliegue

## Datos básicos

- Aplicación:
- Componente:
- Entorno:
- Fecha:
- Tipo de cambio:
- Ticket de cambio:
- Responsable saliente:
- Observador entrante:

## Preparación

- Rama / tag:
- Artefacto:
- Aprobaciones:
- Backup:
- Comunicación:
- Ventana:

## Ejecución observada

1.
2.
3.

## Validaciones previas

## Validaciones posteriores

## Monitorización posterior

## Criterios de éxito

## Criterios de rollback

## ¿Se ejecutó rollback?

## Evidencias

## Gaps detectados

## Mejoras al runbook

## Acciones
```

## 11.6 Resultado esperado

- Runbooks de despliegue validados o corregidos.
- Procedimientos reales documentados.
- Validaciones postdespliegue capturadas.
- Criterios de rollback clarificados.
- Riesgos de despliegue actualizados.

---

# 10. Actividad 7. Observar procesos batch y reprocesos

## 12.1 Objetivo

Comprender cómo se ejecutan, monitorizan, validan y reprocesan procesos batch críticos.

En aseguradoras, los procesos batch suelen ser especialmente sensibles porque intervienen en:

- Renovaciones.
- Recibos.
- Remesas bancarias.
- Impagos.
- Recobros.
- Comisiones.
- Reporting.
- Contabilidad.
- Documentación masiva.
- Carga a Data Warehouse.
- Cierres diarios, mensuales o anuales.

## 12.2 Qué observar

- Planificador.
- Secuencia de jobs.
- Dependencias.
- Ventana de ejecución.
- Inputs.
- Outputs.
- Logs.
- Alertas.
- Validaciones.
- Reintentos.
- Reprocesos.
- Controles funcionales.
- Comunicación a negocio.
- Escalado.
- Criterios de parada.
- Criterios de continuidad.

## 12.3 Preguntas clave

- ¿Qué proceso funcional soporta el batch?
- ¿Qué ocurre si falla?
- ¿Qué jobs son predecesores?
- ¿Qué jobs son sucesores?
- ¿Qué ficheros genera?
- ¿Qué tablas actualiza?
- ¿Qué integraciones activa?
- ¿Qué validaciones se hacen al finalizar?
- ¿Cómo se detecta un fallo parcial?
- ¿Cuándo se reprocesa?
- ¿Cuándo no se debe reprocesar?
- ¿Quién autoriza un reproceso?
- ¿Qué impacto tiene en bancos, contabilidad o reporting?
- ¿Qué fechas son críticas?
- ¿Qué pasa en cierres mensuales o anuales?

## 12.4 Matriz de observación batch

| Job / cadena | Proceso | Ventana | Qué observar | Validación final | Reproceso | Riesgo |
|---|---|---|---|---|---|---|
| Generación recibos | Recibos | Nocturna | Logs, salidas, errores | Nº recibos generados | Sí | Duplicidad |
| Renovación cartera | Renovaciones | Mensual | Secuencia, tarifas | Pólizas renovadas | Parcial | Importe incorrecto |
| Carga DWH | Reporting | Madrugada | ETL, rechazos | Cuadres | Sí | Reporting erróneo |

## 12.5 Resultado esperado

- Runbooks batch validados.
- Secuencias batch documentadas.
- Validaciones funcionales identificadas.
- Reprocesos documentados.
- Riesgos de duplicidad o impacto financiero registrados.
- Casos de reverse shadowing preparados.

---

# 11. Actividad 8. Observar monitorización, alertas y guardias

## 13.1 Objetivo

Entender cómo se vigila el servicio y cómo se actúa ante alertas, especialmente fuera del horario ordinario.

## 13.2 Aspectos a observar

- Dashboards principales.
- Alertas críticas.
- Alertas informativas.
- Umbrales.
- Falsos positivos.
- Alertas recurrentes.
- Canales de notificación.
- Guardias.
- On-call.
- Escalado fuera de horario.
- Comunicación a negocio.
- Activación de crisis.
- Criterios de severidad.
- Tiempo de respuesta.
- Tiempo de resolución.

## 13.3 Preguntas clave

- ¿Qué alertas se miran primero?
- ¿Qué alertas son ruido?
- ¿Qué alertas nunca deben ignorarse?
- ¿Quién recibe las alertas?
- ¿Cómo se confirma impacto?
- ¿Cómo se escala fuera de horario?
- ¿Cuándo se despierta a un experto?
- ¿Cuándo se abre incidencia mayor?
- ¿Qué dashboards son realmente útiles?
- ¿Qué métricas anticipan problemas?
- ¿Qué alertas faltan?
- ¿Qué alertas deberían ajustarse?

## 13.4 Catálogo de alertas observadas

| Alerta | Aplicación | Severidad | Qué significa | Acción esperada | Falso positivo | Runbook |
|---|---|---|---|---|---|---|
|  |  | Crítica / Alta / Media |  |  | Sí / No |  |

## 13.5 Resultado esperado

- Catálogo de alertas enriquecido.
- Alertas críticas identificadas.
- Falsos positivos documentados.
- Procedimiento de guardia entendido.
- Escalados fuera de horario documentados.
- Gaps de monitorización registrados.

---

# 12. Actividad 9. Observar escalados y comunicación

## 14.1 Objetivo

Entender cómo se comunica y escala durante incidencias, despliegues, fallos batch o situaciones de crisis.

## 14.2 Tipos de escalado

| Tipo | Ejemplo |
|---|---|
| Técnico interno | De L2 a L3 o arquitectura. |
| Funcional | A Product Owner o responsable de negocio. |
| Operativo | A operaciones, infraestructura, DBA, batch. |
| Seguridad | A ciberseguridad, IAM, DPO. |
| Proveedor externo | Banco, firma, documental, comunicaciones. |
| Ejecutivo | Comité de crisis, dirección IT, sponsor. |
| Regulatorio | Compliance, legal, auditoría. |

## 14.3 Qué observar

- Quién decide escalar.
- Cuándo se escala.
- Por qué canal se escala.
- Qué información se proporciona.
- Qué tiempos se esperan.
- Qué responsables intervienen.
- Qué plantillas de comunicación se usan.
- Cómo se informa a negocio.
- Cómo se informa a usuarios.
- Cómo se declara una incidencia mayor.
- Cómo se cierra la comunicación.
- Qué evidencias se guardan.

## 14.4 Plantilla de comunicación de incidencia

```markdown
# Comunicación de incidencia

## Resumen

- Aplicación:
- Proceso afectado:
- Severidad:
- Inicio:
- Estado actual:

## Impacto

- Usuarios afectados:
- Impacto negocio:
- Impacto cliente:
- Impacto regulatorio:
- SLA:

## Acciones en curso

## Próxima actualización

## Responsable de seguimiento

## Contactos implicados
```

## 14.5 Resultado esperado

- Matriz de escalado validada.
- Canales reales de comunicación identificados.
- Plantillas de comunicación recopiladas.
- Criterios de incidencia mayor entendidos.
- Responsables de comunicación identificados.

---

# 13. Actividad 10. Capturar conocimiento tácito

## 15.1 Objetivo

Convertir observaciones informales y experiencia del equipo saliente en conocimiento utilizable por el equipo entrante.

## 15.2 Qué es conocimiento tácito en esta fase

| Tipo | Ejemplo |
|---|---|
| Heurística | “Cuando aparece este error, normalmente es la integración documental.” |
| Advertencia | “No reprocesar este fichero dos veces.” |
| Prioridad real | “Esta alerta parece menor, pero en cierre es crítica.” |
| Validación informal | “Después del batch siempre comprobamos este conteo.” |
| Dependencia personal | “Para este proveedor funciona mejor escalar por este contacto.” |
| Excepción | “Este producto tiene tratamiento distinto en renovaciones.” |
| Riesgo oculto | “El rollback existe, pero nunca se ha probado en producción.” |
| Atajo operativo | “Esta consulta permite saber si el proceso terminó bien.” |

## 15.3 Técnicas para capturarlo

- Pedir que el experto piense en voz alta mientras opera.
- Preguntar qué mira primero y por qué.
- Preguntar qué no haría nunca.
- Preguntar qué señales le preocupan.
- Pedir ejemplos de fallos pasados.
- Pedir recomendaciones para alguien nuevo.
- Revisar tickets reales.
- Observar validaciones posteriores.
- Documentar decisiones tomadas en caliente.
- Convertir intuiciones en reglas operativas.

## 15.4 Preguntas útiles

- ¿Qué te ha hecho mirar ahí primero?
- ¿Qué señal te indica que el problema va por ese camino?
- ¿Qué descartarías antes de escalar?
- ¿Qué error suele confundir a alguien nuevo?
- ¿Qué no se debe tocar sin validar antes?
- ¿Qué harías si esto ocurre fuera de horario?
- ¿Qué comprobarías después de aplicar el workaround?
- ¿Qué parte de esto no está en el runbook?
- ¿Qué recomendación añadirías para el equipo entrante?

## 15.5 Resultado esperado

- Reglas prácticas documentadas.
- Advertencias incorporadas a runbooks.
- Workarounds validados.
- Entradas de base de conocimiento.
- Riesgos invisibles convertidos en RAID log.
- Mejora de formación interna del equipo entrante.

---

# 14. Actividad 11. Consolidar aprendizajes y actualizar documentación

## 16.1 Objetivo

Transformar las observaciones de shadowing en documentación operativa validada.

## 16.2 Documentos a actualizar

- Runbooks técnicos.
- Runbooks funcionales.
- Guías de diagnóstico.
- Matriz de incidencias frecuentes.
- Matriz de errores conocidos.
- Matriz de escalado.
- Catálogo de alertas.
- Matriz batch.
- Procedimientos de reproceso.
- Runbooks de despliegue.
- Procedimientos de rollback.
- Base de conocimiento.
- RAID log.
- Backlog de gaps.
- Criterios para reverse shadowing.

## 16.3 Revisión posterior a cada observación

Después de cada caso observado, realizar una breve revisión:

| Pregunta | Objetivo |
|---|---|
| ¿Qué hemos aprendido? | Capturar aprendizaje principal. |
| ¿Qué no estaba documentado? | Identificar gap. |
| ¿Qué runbook debe actualizarse? | Convertir observación en procedimiento. |
| ¿Qué riesgo aparece? | Actualizar RAID log. |
| ¿Qué debemos practicar en reverse shadowing? | Preparar Fase 5. |
| ¿Qué duda queda abierta? | Asignar responsable. |

## 16.4 Resultado esperado

- Documentación operativa actualizada.
- Gaps reducidos.
- Runbooks más accionables.
- Riesgos mejor definidos.
- Equipo entrante preparado para operar bajo supervisión.

---

# 15. Actividad 12. Evaluar preparación para reverse shadowing

## 17.1 Objetivo

Determinar si el equipo entrante está preparado para pasar de observar a ejecutar bajo supervisión.

## 17.2 Criterios de preparación

| Criterio | Evidencia |
|---|---|
| Ha observado incidencias relevantes | Actas de observación. |
| Conoce el flujo ITSM | Guía de operación diaria. |
| Sabe consultar logs principales | Guía de diagnóstico. |
| Sabe usar dashboards clave | Matriz de observabilidad. |
| Conoce escalados | Matriz de escalado. |
| Ha observado despliegues | Actas de despliegue. |
| Conoce rollback | Runbook de rollback. |
| Ha observado batch crítico | Actas batch. |
| Conoce workarounds | Base de conocimiento. |
| Ha actualizado runbooks | Runbooks revisados. |
| Conoce gaps pendientes | Backlog actualizado. |
| Conoce límites de autonomía | Criterios definidos. |

## 17.3 Decisión Go / No-Go

Antes de iniciar Fase 5, se recomienda una reunión Go / No-Go.

### Participantes

- Transition Manager.
- Líder técnico entrante.
- Líder funcional entrante.
- Service Manager entrante.
- Equipo saliente.
- Cliente.
- Operaciones.
- Seguridad si aplica.

### Preguntas de decisión

- ¿Qué casos críticos se han observado?
- ¿Qué casos no se han podido observar?
- ¿Qué gaps bloquean el reverse shadowing?
- ¿Qué riesgos deben aceptarse?
- ¿Qué aplicaciones pueden pasar a reverse shadowing?
- ¿Qué aplicaciones necesitan más shadowing?
- ¿Qué límites tendrá el equipo entrante al operar?
- ¿Qué supervisión dará el equipo saliente?
- ¿Qué actividades quedan prohibidas sin autorización?

## 17.4 Resultado esperado

- Decisión Go / No-Go por aplicación o dominio.
- Lista de actividades autorizadas para reverse shadowing.
- Lista de actividades que requieren supervisión estricta.
- Gaps bloqueantes identificados.
- Plan de Fase 5 preparado.

---

# 16. Entregables de la Fase 4

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Plan de shadowing | Casos, calendario, responsables y observadores. | Transition Manager |
| Matriz de casos observados | Registro de actividades observadas. | Transition Manager |
| Actas de observación de incidencias | Evidencia de aprendizaje en incidencias reales. | Observadores entrantes |
| Actas de observación de despliegues | Evidencia de despliegues observados. | Líder técnico / DevOps |
| Actas de observación batch | Evidencia de procesos batch observados. | Operaciones / equipo entrante |
| Guías de diagnóstico actualizadas | Logs, dashboards, consultas, síntomas. | Equipo técnico entrante |
| Runbooks actualizados | Procedimientos operativos mejorados. | Equipo entrante |
| Matriz de escalado validada | Contactos, canales y criterios. | Service Manager |
| Catálogo de alertas revisado | Alertas útiles, críticas y falsos positivos. | Operaciones |
| Base de conocimiento operativa | Workarounds, errores frecuentes, recomendaciones. | Equipo entrante |
| Matriz de gaps operativos | Pendientes detectados durante shadowing. | Transition Manager |
| RAID log actualizado | Riesgos derivados de operación real. | Transition Manager |
| Evaluación Go / No-Go Fase 5 | Validación de preparación para reverse shadowing. | Cliente + Transition Manager |
| Registro de problemas recurrentes | Síntomas repetidos, causas raíz, workarounds y acciones de mejora. | Service Manager / líder técnico |
| Matriz de evidencias ITIL de shadowing | Relación de observaciones con prácticas ITIL y artefactos actualizados. | Transition Manager |
| Registro de mejoras operativas | Oportunidades de mejora detectadas en operación real. | Service Manager |

---

# 17. Plantillas útiles de la Fase 4

## 19.1 Matriz de casos observados

| ID | Fecha | Aplicación | Tipo | Descripción | Observador | Experto saliente | Resultado | Gaps |
|---|---|---|---|---|---|---|---|---|
| SH-001 |  |  | Incidencia |  |  |  | Documentado |  |
| SH-002 |  |  | Despliegue |  |  |  | Documentado |  |
| SH-003 |  |  | Batch |  |  |  | Pendiente |  |

## 19.2 Matriz de conocimiento tácito

| ID | Aplicación | Situación | Conocimiento capturado | Tipo | Artefacto actualizado | Estado |
|---|---|---|---|---|---|---|
| KT-001 |  | Batch fallido | No reprocesar dos veces sin validar salida | Advertencia | Runbook batch | Validado |
| KT-002 |  | Error documental | Revisar plantilla antes que servicio | Heurística | Guía diagnóstico | Borrador |

## 19.3 Matriz de preparación para reverse shadowing

| Aplicación | Incidencias observadas | Despliegue observado | Batch observado | Runbook actualizado | Gaps bloqueantes | Preparada |
|---|---|---|---|---|---|---|
|  | Sí / No | Sí / No | Sí / No / N/A | Sí / No |  | Sí / No |

## 19.4 Checklist de observación rápida

```markdown
# Checklist de observación

## Antes de la actividad

- [ ] Caso identificado.
- [ ] Observador asignado.
- [ ] Experto saliente asignado.
- [ ] Permisos confirmados.
- [ ] Plantilla preparada.
- [ ] Restricciones de seguridad revisadas.

## Durante la actividad

- [ ] Pasos observados.
- [ ] Herramientas usadas.
- [ ] Decisiones capturadas.
- [ ] Logs / dashboards identificados.
- [ ] Validaciones registradas.
- [ ] Escalados registrados.
- [ ] Workarounds registrados.
- [ ] Gaps anotados.

## Después de la actividad

- [ ] Acta completada.
- [ ] Runbook actualizado.
- [ ] KB actualizada.
- [ ] RAID log actualizado.
- [ ] Acciones asignadas.
- [ ] Caso marcado como candidato para reverse shadowing.
```

---

# 18. Checklist operativo de Fase 4

## 20.1 Preparación

- [ ] Definir plan de shadowing.
- [ ] Identificar casos obligatorios.
- [ ] Identificar aplicaciones críticas.
- [ ] Identificar expertos salientes.
- [ ] Asignar observadores entrantes.
- [ ] Preparar calendario.
- [ ] Confirmar accesos.
- [ ] Confirmar restricciones de seguridad.
- [ ] Preparar plantillas.
- [ ] Acordar evidencias.

## 20.2 Operación diaria

- [ ] Observar flujo de tickets.
- [ ] Observar priorización.
- [ ] Observar clasificación de severidad.
- [ ] Observar asignación.
- [ ] Observar seguimiento de SLAs.
- [ ] Observar comunicación.
- [ ] Observar cierre de tickets.
- [ ] Documentar gaps.

## 20.3 Incidencias

- [ ] Observar incidencia técnica.
- [ ] Observar incidencia funcional.
- [ ] Observar incidencia de integración.
- [ ] Observar incidencia batch.
- [ ] Observar incidencia de datos.
- [ ] Observar degradación de rendimiento.
- [ ] Documentar diagnóstico.
- [ ] Documentar resolución.
- [ ] Documentar validación.
- [ ] Documentar comunicación.
- [ ] Actualizar runbooks.

## 20.4 Despliegues y cambios

- [ ] Observar despliegue planificado.
- [ ] Observar hotfix si ocurre.
- [ ] Observar cambio de configuración.
- [ ] Observar cambio de BBDD si aplica.
- [ ] Observar validaciones previas.
- [ ] Observar validaciones posteriores.
- [ ] Revisar criterios de rollback.
- [ ] Actualizar runbook de despliegue.
- [ ] Registrar riesgos.

## 20.5 Batch

- [ ] Observar batch de recibos.
- [ ] Observar batch de renovaciones.
- [ ] Observar batch de reporting.
- [ ] Observar batch documental si aplica.
- [ ] Observar logs.
- [ ] Observar alertas.
- [ ] Observar validaciones.
- [ ] Observar reproceso si ocurre.
- [ ] Documentar dependencias.
- [ ] Actualizar matriz batch.

## 20.6 Monitorización y guardias

- [ ] Observar dashboards.
- [ ] Observar alertas críticas.
- [ ] Observar alertas recurrentes.
- [ ] Identificar falsos positivos.
- [ ] Observar escalado fuera de horario si aplica.
- [ ] Revisar canales de alerta.
- [ ] Actualizar catálogo de alertas.
- [ ] Actualizar guía de guardia.

## 20.7 Escalado y comunicación

- [ ] Observar escalado técnico.
- [ ] Observar escalado funcional.
- [ ] Observar escalado a proveedor.
- [ ] Observar escalado ejecutivo si ocurre.
- [ ] Observar comunicación a negocio.
- [ ] Observar comunicación a usuarios.
- [ ] Recopilar plantillas.
- [ ] Actualizar matriz de escalado.

## 20.8 Cierre de fase

- [ ] Consolidar aprendizajes.
- [ ] Actualizar runbooks.
- [ ] Actualizar KB.
- [ ] Actualizar gaps.
- [ ] Actualizar RAID log.
- [ ] Evaluar preparación por aplicación.
- [ ] Celebrar Go / No-Go.
- [ ] Preparar plan de reverse shadowing.

---

# 19. Riesgos específicos de la Fase 4

| Riesgo | Impacto | Mitigación |
|---|---|---|
| No ocurren incidencias relevantes durante la ventana | No se observa operación crítica | Usar tickets históricos, simulacros o walkthroughs guiados. |
| El equipo saliente opera sin explicar | Se observa acción pero no razonamiento | Pedir pensamiento en voz alta y revisión posterior. |
| El equipo entrante no documenta bien | Se pierde conocimiento tácito | Usar plantillas obligatorias y revisión diaria. |
| Se observa solo operación simple | Falsa sensación de preparación | Priorizar casos críticos y escenarios complejos. |
| No se observan despliegues | No se valida capacidad de cambio | Planificar despliegues no productivos o walkthrough de despliegue real. |
| No se observa batch crítico | Riesgo en recibos, renovaciones o reporting | Ajustar calendario a ventanas batch. |
| Producción tiene restricciones de acceso | Observación limitada | Coordinar con seguridad y usar sesiones compartidas controladas. |
| Se capturan datos sensibles en evidencias | Riesgo GDPR | Anonimizar evidencias y seguir política de seguridad. |
| El equipo saliente oculta workarounds | Runbooks incompletos | Preguntar por casos reales y zonas de riesgo. |
| La documentación no se actualiza tras observar | Shadowing no genera valor | Establecer revisión posterior obligatoria. |
| Se pasa prematuramente a reverse shadowing | Riesgo operativo | Aplicar Go / No-Go por aplicación. |
| No se relacionan incidencias con problemas recurrentes | Se perpetúan causas raíz y workarounds | Registrar problem records candidatos y backlog de mejora. |
| No se observa impacto sobre SLAs | Se desconoce la presión real del servicio | Revisar SLA, severidad, tiempos y comunicación en cada caso observado. |
| Escalados a proveedores no documentados | Dependencia informal de contactos personales | Registrar Supplier Management: contacto, canal, SLA y evidencia. |
| Evidencias sin trazabilidad ITIL | Dificultad para demostrar preparación operativa | Usar matriz de evidencias ITIL de shadowing. |

---

# 20. Criterios de salida de la Fase 4

## 22.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Plan de shadowing ejecutado | Matriz de casos | Pendiente / En curso / Validado |
| Operación diaria observada | Actas / checklist |  |
| Incidencias observadas | Actas de incidencia |  |
| Diagnóstico técnico observado | Guías actualizadas |  |
| Incidencias funcionales-técnicas observadas | Casos documentados |  |
| Despliegues observados | Actas de despliegue |  |
| Procesos batch observados | Actas batch |  |
| Monitorización y alertas observadas | Catálogo actualizado |  |
| Escalados observados | Matriz de escalado |  |
| Comunicación observada | Plantillas / actas |  |
| Conocimiento tácito capturado | KB / runbooks |  |
| Runbooks actualizados | Runbooks revisados |  |
| Gaps operativos registrados | Backlog actualizado |  |
| Riesgos actualizados | RAID log |  |
| Preparación para reverse shadowing evaluada | Matriz de preparación |  |
| Go / No-Go realizado | Acta de decisión |  |
| Problemas recurrentes identificados | Registro de problemas / problem candidates |  |
| Evidencias ITIL consolidadas | Matriz de evidencias ITIL |  |
| Mejoras operativas registradas | Registro de mejora continua |  |
| Impacto sobre SLAs observado | Tickets, actas y reportes |  |

## 22.2 Criterio de salida recomendado

La Fase 4 puede considerarse cerrada cuando:

> El equipo entrante ha observado suficientes situaciones operativas reales o simuladas, ha capturado conocimiento tácito relevante, ha actualizado runbooks y guías de diagnóstico, entiende los flujos de incidencia, despliegue, batch, monitorización y escalado, y cuenta con validación suficiente para empezar a operar bajo supervisión en la Fase 5.


## 25.3 Gate ITIL de salida de la Fase 4

Antes de pasar a Fase 5, debe celebrarse un gate de salida específico para confirmar que el shadowing ha generado evidencias suficientes de operación real.

| Dimensión | Pregunta de control | Evidencia mínima |
|---|---|---|
| Incidencias | ¿El equipo entrante ha observado el ciclo completo de gestión de incidencias? | Actas de observación y tickets. |
| Eventos | ¿Se han observado alertas, dashboards y respuesta operativa? | Catálogo de alertas actualizado. |
| Problemas | ¿Se han identificado incidencias recurrentes y workarounds? | Registro de problemas recurrentes. |
| Conocimiento | ¿Los aprendizajes se han incorporado a runbooks o KB? | Runbooks y base de conocimiento actualizados. |
| Cambios | ¿Se han observado despliegues o cambios relevantes? | Actas de despliegue y runbooks revisados. |
| Escalado | ¿Se conocen escalados internos, externos y ejecutivos? | Matriz de escalado validada. |
| Seguridad | ¿Las evidencias cumplen las restricciones de seguridad y privacidad? | Validación de Seguridad / Compliance si aplica. |
| SLAs | ¿Se entiende cómo se miden y gestionan los SLAs durante incidencias? | Tickets, reportes y actas. |
| Readiness | ¿Existen casos adecuados para reverse shadowing? | Matriz de preparación Fase 5. |

La decisión del gate podrá ser:

- **Go**: la aplicación o dominio puede pasar a reverse shadowing.
- **Go condicionado**: puede pasar, pero con límites, supervisión reforzada o gaps abiertos con plan.
- **No-Go**: requiere más shadowing o resolución de bloqueos antes de operar bajo supervisión.


---

# 21. Recomendaciones prácticas para liderar la Fase 4

## 23.1 Recomendaciones de enfoque

- No convertir el shadowing en una reunión pasiva.
- Pedir al experto saliente que explique qué piensa mientras opera.
- Documentar inmediatamente después de cada observación.
- Priorizar calidad de casos sobre cantidad de reuniones.
- Usar tickets históricos si no aparecen incidencias reales.
- Observar tanto la parte técnica como la comunicación.
- Observar validaciones posteriores, no solo la resolución.
- Preguntar qué podría haber salido mal.
- Preguntar qué no está en el runbook.
- Preguntar qué haría el experto si estuviera solo de guardia.
- Convertir cada aprendizaje en artefacto.
- Preparar desde el principio la Fase 5.

## 23.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- El equipo entrante observa pero no entiende.
- El equipo saliente ejecuta demasiado rápido sin explicar.
- Las actas son superficiales.
- No se actualizan runbooks.
- Todo queda como “pendiente”.
- No se observan casos críticos.
- No se habla de rollback.
- No se habla de reprocesos.
- No se habla de errores pasados.
- No se documentan workarounds.
- No se identifican criterios de escalado.
- No se valida con negocio cuando procede.
- El equipo entrante cree estar preparado pero no puede explicar el diagnóstico.

## 23.3 Buenas prácticas

- Usar plantillas homogéneas.
- Crear una sesión breve de debrief tras cada observación.
- Mantener una matriz de conocimiento tácito.
- Grabar sesiones solo si está permitido.
- Separar datos sensibles de evidencias.
- Hacer revisión semanal de aprendizajes.
- Actualizar el RAID log semanalmente.
- Validar runbooks con el equipo saliente.
- Clasificar casos observados por criticidad.
- Definir casos mínimos por aplicación crítica.

---

# 22. Resumen ejecutivo de la Fase 4

La Fase 4 es el puente entre la transferencia teórica y la operación real.

Su valor está en que el equipo entrante deja de recibir explicaciones y empieza a ver cómo se comporta el servicio en situaciones reales:

1. Cómo se detectan incidencias.
2. Cómo se diagnostican.
3. Qué herramientas se usan realmente.
4. Qué logs y dashboards son útiles.
5. Cómo se decide escalar.
6. Cómo se comunica a negocio.
7. Cómo se ejecutan despliegues.
8. Cómo se valida después de un cambio.
9. Cómo se tratan procesos batch.
10. Cómo se aplican workarounds.
11. Qué conocimiento no estaba documentado.
12. Qué riesgos deben controlarse antes de operar.

La Fase 4 no debe cerrarse por haber asistido a reuniones, sino por haber capturado conocimiento operativo real y haberlo convertido en documentación accionable. Desde la perspectiva ITIL, debe dejar evidencias claras de gestión de incidencias, eventos, problemas, cambios, escalados, conocimiento operativo y mejora continua.

El objetivo final es que el equipo entrante esté preparado para pasar de observar a operar bajo supervisión en la Fase 5, minimizando el riesgo para producción, negocio, clientes, mediadores y cumplimiento regulatorio.

---
