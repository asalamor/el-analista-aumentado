# Fase 5. Reverse shadowing  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 5

La **Fase 5. Reverse shadowing** tiene como objetivo que el equipo entrante pase de observar la operación a **ejecutarla bajo supervisión** del equipo saliente.

En la Fase 4, el equipo entrante observaba cómo el equipo saliente gestionaba incidencias, despliegues, procesos batch, escalados, monitorización y comunicación. En esta fase se invierte el rol:

> El equipo entrante opera; el equipo saliente observa, supervisa, corrige y valida.

Esta fase es una de las más críticas de toda la transición porque permite comprobar si el conocimiento transferido es realmente operativo. No basta con que el equipo entrante haya asistido a sesiones o leído documentación. Debe demostrar que puede actuar con criterio ante situaciones reales o simuladas.

El reverse shadowing permite validar:

- Si el equipo entrante entiende los procedimientos.
- Si sabe usar las herramientas.
- Si sabe diagnosticar incidencias.
- Si sabe cuándo escalar.
- Si puede seguir runbooks.
- Si puede ejecutar despliegues supervisados.
- Si puede validar procesos batch.
- Si puede comunicarse correctamente con negocio y operación.
- Si distingue entre incidencias técnicas, funcionales y mixtas.
- Si conoce sus límites de autonomía.
- Si el equipo saliente puede retirarse progresivamente sin poner en riesgo el servicio.

En una aseguradora, esta fase debe tratarse con especial cuidado, ya que muchas operaciones tienen impacto directo en emisión, recibos, siniestros, documentación contractual, mediadores, reporting, cumplimiento normativo, datos personales y continuidad del servicio.

---

## 2. Resultado esperado de la Fase 5

Al finalizar esta fase, el equipo entrante debe haber demostrado capacidad práctica para operar bajo supervisión.

Los resultados esperados son:

- Incidencias gestionadas por el equipo entrante con supervisión.
- Diagnósticos técnicos realizados por el equipo entrante.
- Diagnósticos funcionales-técnicos realizados con apoyo limitado.
- Despliegues ejecutados o coordinados por el equipo entrante con supervisión.
- Procesos batch revisados, validados o reprocesados bajo control.
- Escalados realizados correctamente.
- Comunicaciones operativas preparadas o emitidas correctamente.
- Runbooks utilizados y corregidos.
- Gaps restantes identificados.
- Riesgos operativos actualizados.
- Evidencias de autonomía por aplicación o dominio.
- Criterios de asunción progresiva preparados para la Fase 6.

El objetivo no es que el equipo entrante actúe sin ningún error, sino que demuestre capacidad de operar de forma controlada, segura, trazable y con criterio de escalado.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **3 a 6 semanas**.

Puede ser menor si:

- La Fase 4 ha sido muy completa.
- Los runbooks están maduros.
- Las aplicaciones críticas son pocas.
- El equipo entrante ya tiene experiencia previa en tecnologías similares.
- El equipo saliente supervisa activamente.
- Hay suficientes casos reales para practicar.

Puede alargarse si:

- Hay muchas aplicaciones críticas.
- Los gaps operativos siguen siendo relevantes.
- Los procedimientos no están suficientemente probados.
- Hay pocos eventos reales.
- Hay procesos batch con ventanas muy concretas.
- Existen sistemas legacy.
- Los despliegues son delicados o manuales.
- El equipo entrante necesita más práctica.
- El equipo saliente detecta errores de criterio.
- El cliente exige evidencias fuertes antes de autorizar la asunción.

---


---

# 4. Alineamiento ITIL específico de la Fase 5

## 4.1 Sentido de la Fase 5 desde ITIL

Desde la perspectiva de ITIL, la Fase 5 representa una validación práctica de la capacidad operativa del equipo entrante antes de transferirle responsabilidad principal sobre el servicio.

En esta fase, el foco deja de estar únicamente en la transferencia de conocimiento y pasa a estar en la **demostración controlada de competencia operativa**. El equipo entrante debe probar, con evidencias, que puede ejecutar los procesos de gestión del servicio bajo supervisión y dentro de los límites autorizados.

La fase se alinea especialmente con las prácticas ITIL relacionadas con:

- Gestión de incidencias.
- Gestión de problemas.
- Gestión de cambios.
- Gestión de releases.
- Gestión de despliegues.
- Gestión del conocimiento.
- Gestión de niveles de servicio.
- Gestión de proveedores.
- Monitorización y gestión de eventos.
- Seguridad de la información.
- Gestión de configuración del servicio.
- Validación de la preparación operativa.
- Mejora continua.

El objetivo es confirmar que la operación futura no dependerá únicamente de documentación o de conocimiento teórico, sino de una capacidad real, observada y evaluada.

## 4.2 Prácticas ITIL aplicables

| Práctica ITIL | Aplicación en la Fase 5 |
|---|---|
| **Incident Management** | Validar que el equipo entrante puede clasificar, diagnosticar, resolver, escalar y cerrar incidencias bajo supervisión. |
| **Problem Management** | Identificar problemas recurrentes, causas raíz pendientes, workarounds y acciones estructurales derivadas de las incidencias gestionadas. |
| **Change Enablement** | Comprobar que los cambios y despliegues se ejecutan con autorización, control de riesgo, evidencias y criterios de rollback. |
| **Release Management** | Verificar que el equipo entrante entiende versiones, releases, artefactos, ventanas y validaciones post-release. |
| **Deployment Management** | Validar la capacidad de ejecutar o coordinar despliegues supervisados en entornos autorizados. |
| **Knowledge Management** | Comprobar que el equipo usa, corrige y mejora runbooks, guías de diagnóstico y base de conocimiento durante la ejecución real. |
| **Service Level Management** | Evaluar si el equipo opera teniendo en cuenta SLAs, prioridades, severidades, tiempos de respuesta y tiempos de resolución. |
| **Monitoring and Event Management** | Validar la capacidad de interpretar alertas, dashboards, eventos y señales de degradación. |
| **Supplier Management** | Comprobar la capacidad de escalar correctamente a proveedores externos cuando la incidencia, cambio o integración lo requiere. |
| **Information Security Management** | Verificar que se respetan permisos, datos sensibles, accesos a producción, secretos y restricciones de seguridad. |
| **Service Configuration Management** | Confirmar que las acciones se realizan sobre los componentes, servicios, entornos y versiones correctas. |
| **Continual Improvement** | Transformar errores, dudas y desviaciones en acciones de mejora, refuerzo documental o automatización. |

## 4.3 Enfoque ITIL de validación operativa

La Fase 5 debe funcionar como un control previo a la asunción progresiva del servicio. Por ello, cada actividad ejecutada por el equipo entrante debe dejar una evidencia trazable.

No debe evaluarse únicamente si la actividad terminó bien, sino también:

- Si se siguió el proceso correcto.
- Si se entendió el impacto de negocio.
- Si se respetaron los niveles de servicio.
- Si se usaron las herramientas adecuadas.
- Si se consultaron los elementos de configuración correctos.
- Si se aplicó el runbook correspondiente.
- Si se escaló en el momento adecuado.
- Si se protegieron datos sensibles.
- Si se documentó suficientemente la actuación.
- Si el aprendizaje se incorporó a la base de conocimiento.

## 4.4 Evidencias ITIL esperadas

| Evidencia | Finalidad |
|---|---|
| Tickets gestionados por el equipo entrante | Demostrar capacidad real en el flujo ITSM. |
| Evaluaciones de diagnóstico | Comprobar criterio técnico y funcional. |
| Actividades de cambio supervisadas | Validar cumplimiento de Change Enablement. |
| Despliegues supervisados | Validar capacidad de Deployment Management. |
| Validaciones postdespliegue | Confirmar cierre controlado del cambio. |
| Ejecuciones o validaciones batch | Confirmar capacidad sobre procesos operativos críticos. |
| Comunicaciones supervisadas | Validar claridad, destinatarios, tono y protección de información. |
| Escalados a terceros o áreas internas | Verificar rutas reales de soporte. |
| Runbooks actualizados | Convertir ejecución real en conocimiento reutilizable. |
| Matriz de autonomía | Medir preparación por aplicación, dominio o actividad. |
| Registro de gaps de reverse shadowing | Identificar carencias antes de Fase 6. |
| Registro de problemas recurrentes | Separar incidencias aisladas de problemas estructurales. |
| Registro de mejora continua | Derivar mejoras tras errores, dudas o ineficiencias. |

## 4.5 Relación con el modelo de servicio

Cada actividad de reverse shadowing debe relacionarse, siempre que sea posible, con:

- Servicio de negocio afectado.
- Aplicación o componente implicado.
- Elemento de configuración relacionado.
- Proceso ITIL ejecutado.
- SLA u OLA aplicable.
- Riesgo operativo asociado.
- Evidencia generada.
- Nivel de autonomía demostrado.

Esto permite que la decisión de pasar a Fase 6 no sea genérica, sino específica por servicio, aplicación, proceso o tipo de actividad.

# 6. Principios de trabajo de la Fase 5

## 4.1 Operar con supervisión explícita

El reverse shadowing no significa que el equipo entrante opere en solitario. Significa que opera con un marco de supervisión definido.

Antes de iniciar la fase debe estar claro:

- Qué puede hacer el equipo entrante.
- Qué no puede hacer.
- Qué requiere aprobación previa.
- Qué requiere presencia del equipo saliente.
- Qué requiere autorización del cliente.
- Qué debe escalarse inmediatamente.
- Qué evidencias deben quedar registradas.

## 4.2 Progresividad

No todas las actividades deben delegarse al equipo entrante al mismo tiempo.

La progresión recomendada es:

1. Diagnóstico en entornos no productivos.
2. Diagnóstico en producción con acceso de lectura.
3. Gestión de tickets de baja criticidad.
4. Gestión de incidencias conocidas.
5. Validaciones postdespliegue.
6. Ejecución de tareas recurrentes.
7. Coordinación de despliegues no productivos.
8. Participación en despliegues productivos.
9. Gestión de incidencias de criticidad media.
10. Gestión supervisada de incidencias críticas.
11. Ejecución supervisada de reprocesos.
12. Preparación para asunción por oleadas.

## 4.3 Seguridad antes que velocidad

El equipo entrante debe operar con prudencia. La prioridad no es resolver rápido a cualquier precio, sino resolver correctamente, documentar, escalar cuando proceda y proteger el servicio.

La velocidad llegará con la práctica. En reverse shadowing se mide especialmente:

- Calidad del diagnóstico.
- Uso correcto de procedimientos.
- Capacidad para pedir ayuda a tiempo.
- Comunicación clara.
- Trazabilidad.
- Control del riesgo.

## 4.4 El error controlado es parte del aprendizaje

Pueden aparecer errores de interpretación o ejecución. Lo importante es que ocurran en un entorno supervisado y se transformen en aprendizaje.

Los errores deben tratarse como señales de mejora:

- Falta de claridad del runbook.
- Gap de formación.
- Acceso insuficiente.
- Procedimiento ambiguo.
- Dependencia no identificada.
- Criterio de escalado no interiorizado.
- Validación funcional incompleta.

No deben utilizarse para culpabilizar al equipo entrante, sino para reforzar la transición.

## 4.5 Evidencias por encima de percepciones

La decisión de pasar a Fase 6 no debe basarse en frases como “parece que ya lo controlan”. Debe basarse en evidencias:

- Tickets gestionados.
- Actas de reverse shadowing.
- Despliegues supervisados.
- Validaciones realizadas.
- Runbooks usados.
- Errores corregidos.
- Gaps cerrados.
- Evaluaciones del equipo saliente.
- Aceptación del cliente.

---

# 6. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Preparar plan de reverse shadowing | Actividades autorizadas, límites, responsables y criterios. |
| Semana 1-2 | Operar tickets e incidencias de baja/media criticidad | Validar flujo operativo básico. |
| Semana 2-4 | Gestionar incidencias conocidas y recurrentes | Validar diagnóstico y uso de runbooks. |
| Semana 2-5 | Ejecutar tareas recurrentes y validaciones | Validar capacidad operativa diaria. |
| Semana 3-5 | Participar en despliegues y cambios supervisados | Validar despliegue, rollback y comunicación. |
| Semana 3-6 | Ejecutar o validar batch supervisado | Validar operación de procesos críticos. |
| Semana 5-6 | Evaluar autonomía por aplicación o dominio | Preparar asunción progresiva de Fase 6. |

---

# 7. Actividad 1. Preparar el plan de reverse shadowing

## 6.1 Objetivo

Definir qué actividades va a ejecutar el equipo entrante, bajo qué supervisión, con qué límites y con qué criterios de evaluación.

## 6.2 Entradas necesarias

- Plan de shadowing ejecutado.
- Matriz de casos observados.
- Runbooks actualizados.
- Guías de diagnóstico.
- Matriz de escalado.
- Matriz de accesos.
- Matriz de aplicaciones críticas.
- Matriz de procesos batch.
- Runbooks de despliegue.
- Procedimientos de rollback.
- Base de conocimiento operativa.
- Gaps pendientes.
- RAID log actualizado.
- Decisión Go / No-Go de Fase 4.

## 6.3 Tipos de actividades candidatas

| Tipo de actividad | Ejemplos |
|---|---|
| Gestión de tickets | Clasificación, análisis inicial, resolución, cierre. |
| Diagnóstico técnico | Logs, APM, BBDD, colas, integraciones. |
| Diagnóstico funcional | Estados de póliza, recibo, siniestro, documento. |
| Incidencias recurrentes | Casos conocidos con workaround documentado. |
| Validaciones | Postdespliegue, batch, integraciones, datos. |
| Tareas recurrentes | Revisión de alertas, comprobaciones diarias, controles. |
| Despliegues | DEV, PRE, UAT, producción con supervisión. |
| Batch | Seguimiento, validación, reinicio, reproceso supervisado. |
| Escalados | Comunicación con L3, negocio, proveedor, operaciones. |
| Comunicación | Actualizaciones de incidencia, informe de estado, cierre. |

## 6.4 Niveles de autorización

| Nivel | Descripción | Ejemplo |
|---|---|---|
| Nivel 1. Observación activa | El entrante propone acciones, pero el saliente ejecuta. | Diagnóstico inicial de incidencia crítica. |
| Nivel 2. Ejecución guiada | El entrante ejecuta paso a paso con supervisión directa. | Revisión de logs, validación de estado. |
| Nivel 3. Ejecución supervisada | El entrante ejecuta; el saliente observa e interviene si es necesario. | Resolución de incidencia recurrente. |
| Nivel 4. Ejecución autónoma controlada | El entrante ejecuta y el saliente revisa a posteriori. | Ticket de baja criticidad. |
| Nivel 5. Preparado para asunción | El entrante puede operar en Fase 6 con soporte bajo demanda. | Aplicación de baja/media criticidad. |

## 6.5 Matriz de planificación

| ID | Actividad | Aplicación / dominio | Tipo | Nivel autorización | Responsable entrante | Supervisor saliente | Fecha | Estado |
|---|---|---|---|---|---|---|---|---|
| RS-001 | Resolver ticket recurrente | Portal mediadores | Incidencia | Nivel 3 |  |  |  | Planificado |
| RS-002 | Validar batch recibos | Recibos | Batch | Nivel 2 |  |  |  | Planificado |
| RS-003 | Ejecutar despliegue PRE | Emisión | Despliegue | Nivel 3 |  |  |  | Planificado |
| RS-004 | Preparar comunicación incidencia | Siniestros | Comunicación | Nivel 2 |  |  |  | Planificado |

## 6.6 Entregables

- Plan de reverse shadowing.
- Matriz de actividades autorizadas.
- Matriz de niveles de autorización.
- Lista de supervisores salientes.
- Lista de responsables entrantes.
- Criterios de evaluación.
- Criterios de parada.
- Plantillas de registro.
- Calendario de ejecución.

---

# 8. Actividad 2. Gestionar tickets bajo supervisión

## 7.1 Objetivo

Validar que el equipo entrante sabe trabajar dentro del flujo ITSM real: clasificar, analizar, resolver, documentar y cerrar tickets.

## 7.2 Actividades a ejecutar

- Revisar bandeja de entrada.
- Clasificar tickets.
- Confirmar severidad.
- Identificar aplicación afectada.
- Identificar proceso funcional afectado.
- Revisar documentación existente.
- Consultar logs o datos si procede.
- Proponer diagnóstico.
- Proponer acción.
- Ejecutar acción autorizada.
- Validar resolución.
- Documentar ticket.
- Cerrar o escalar.

## 7.3 Qué debe supervisar el equipo saliente

- Si la clasificación es correcta.
- Si la severidad está bien asignada.
- Si el diagnóstico es razonable.
- Si se consultan las herramientas adecuadas.
- Si se siguen los runbooks.
- Si se escala a tiempo.
- Si la resolución es segura.
- Si la documentación del ticket es suficiente.
- Si se cumplen SLAs.
- Si se evita introducir riesgo.

## 7.4 Preguntas clave

- ¿El equipo entrante entiende el ticket?
- ¿Ha identificado correctamente aplicación y proceso?
- ¿Ha diferenciado síntoma de causa?
- ¿Ha consultado la documentación adecuada?
- ¿Ha usado bien logs, monitorización o BBDD?
- ¿Ha aplicado el workaround correcto?
- ¿Ha pedido ayuda cuando debía?
- ¿Ha documentado correctamente?
- ¿Ha informado a quien correspondía?
- ¿Ha dejado evidencia suficiente?

## 7.5 Plantilla de evaluación de ticket

| Campo | Valor |
|---|---|
| ID ticket |  |
| Aplicación |  |
| Proceso |  |
| Severidad |  |
| Responsable entrante |  |
| Supervisor saliente |  |
| Diagnóstico correcto | Sí / No / Parcial |
| Runbook usado | Sí / No |
| Escalado correcto | Sí / No / N/A |
| Resolución correcta | Sí / No / Parcial |
| Documentación suficiente | Sí / No / Parcial |
| Observaciones |  |
| Gaps detectados |  |
| Resultado | Apto / Requiere refuerzo |

## 7.6 Resultado esperado

- Tickets gestionados por el equipo entrante.
- Evaluación de desempeño operativo.
- Gaps de conocimiento detectados.
- Runbooks ajustados.
- Evidencias para aceptación de autonomía.

---

# 9. Actividad 3. Realizar diagnóstico técnico supervisado

## 8.1 Objetivo

Comprobar que el equipo entrante sabe diagnosticar problemas técnicos usando las herramientas reales de operación.

## 8.2 Casos adecuados

- Error 500.
- Timeout de integración.
- Caída de servicio.
- Lentitud.
- Error de autenticación.
- Error de conexión a BBDD.
- Cola acumulada.
- Job fallido.
- Error en pipeline.
- Error de configuración.
- Alerta de monitorización.
- Problema de certificado.

## 8.3 Pasos esperados

1. Confirmar síntoma.
2. Confirmar alcance.
3. Identificar aplicación y componente.
4. Revisar dashboards.
5. Revisar logs.
6. Buscar correlation ID si existe.
7. Revisar estado de integraciones.
8. Revisar estado de BBDD o colas.
9. Formular hipótesis.
10. Descartar causas.
11. Proponer acción.
12. Escalar si procede.
13. Documentar diagnóstico.

## 8.4 Matriz de evaluación técnica

| Criterio | Evaluación | Observaciones |
|---|---|---|
| Identifica síntoma real | Correcto / Parcial / Incorrecto |  |
| Usa herramientas adecuadas | Correcto / Parcial / Incorrecto |  |
| Interpreta logs | Correcto / Parcial / Incorrecto |  |
| Formula hipótesis | Correcto / Parcial / Incorrecto |  |
| Descarta causas | Correcto / Parcial / Incorrecto |  |
| Identifica riesgo | Correcto / Parcial / Incorrecto |  |
| Propone acción segura | Correcto / Parcial / Incorrecto |  |
| Escala correctamente | Correcto / Parcial / Incorrecto |  |
| Documenta diagnóstico | Correcto / Parcial / Incorrecto |  |

## 8.5 Resultado esperado

- Diagnósticos técnicos ejecutados por el equipo entrante.
- Validación de uso de herramientas.
- Identificación de necesidades de formación.
- Mejora de guías de diagnóstico.
- Mayor confianza para operar en Fase 6.

---

# 10. Actividad 4. Realizar diagnóstico funcional-técnico supervisado

## 9.1 Objetivo

Validar que el equipo entrante puede resolver o encaminar incidencias que combinan lógica funcional y técnica.

## 9.2 Casos típicos

| Dominio | Caso |
|---|---|
| Emisión | Póliza bloqueada o emitida con error documental. |
| Cotización | Prima incorrecta o regla no aplicada. |
| Recibos | Recibo no generado, duplicado o devuelto. |
| Renovaciones | Póliza no renovada correctamente. |
| Siniestros | Expediente bloqueado, reserva errónea o pago no autorizado. |
| Documental | Documento contractual incorrecto o no generado. |
| Firma | Firma no completada o callback no recibido. |
| Mediadores | Operación no visible o permiso incorrecto. |
| Reporting | Descuadre entre origen y DWH. |

## 9.3 Pasos esperados

1. Identificar proceso de negocio afectado.
2. Identificar estado funcional esperado.
3. Identificar estado real.
4. Revisar reglas de negocio aplicables.
5. Revisar parametrización.
6. Revisar datos.
7. Revisar integraciones.
8. Revisar logs.
9. Confirmar impacto.
10. Proponer acción técnica o funcional.
11. Validar con negocio si procede.
12. Documentar resolución.

## 9.4 Preguntas que debe hacerse el equipo entrante

- ¿Qué proceso se ha visto afectado?
- ¿Qué debería haber ocurrido funcionalmente?
- ¿Qué ha ocurrido realmente?
- ¿Qué regla aplica?
- ¿Dónde se implementa esa regla?
- ¿Qué dato está condicionando el resultado?
- ¿Qué documento, recibo, póliza o siniestro está afectado?
- ¿Hay impacto contractual?
- ¿Hay impacto económico?
- ¿Hay impacto regulatorio?
- ¿Quién debe validar la corrección?
- ¿La corrección puede hacerse manualmente?
- ¿Requiere autorización?

## 9.5 Resultado esperado

- Capacidad de análisis mixto validada.
- Mejora de runbooks funcionales-técnicos.
- Identificación de límites de autonomía.
- Criterios de escalado funcional reforzados.

---

# 11. Actividad 5. Ejecutar tareas recurrentes supervisadas

## 10.1 Objetivo

Comprobar que el equipo entrante puede realizar actividades habituales de operación sin depender constantemente del equipo saliente.

## 10.2 Tareas candidatas

| Tipo | Ejemplo |
|---|---|
| Revisión diaria | Comprobar alertas, jobs, tickets pendientes. |
| Validación batch | Revisar salida de procesos nocturnos. |
| Validación integración | Comprobar ficheros, colas o APIs. |
| Control documental | Verificar generación de documentos. |
| Control recibos | Comprobar remesas, recibos, devoluciones. |
| Control reporting | Revisar cargas DWH o cuadres. |
| Mantenimiento menor | Reinicio autorizado, limpieza controlada, revisión de colas. |
| Revisión de certificados | Comprobar caducidades. |
| Revisión de SLAs | Comprobar tickets próximos a incumplimiento. |

## 10.3 Matriz de tareas recurrentes

| Tarea | Aplicación / dominio | Frecuencia | Runbook | Responsable entrante | Supervisor | Resultado |
|---|---|---|---|---|---|---|
| Revisión batch recibos | Recibos | Diaria | Sí |  |  | Correcto / Refuerzo |
| Control alertas portal | Mediadores | Diaria | Sí |  |  |  |
| Validación DWH | Reporting | Diaria | Parcial |  |  |  |

## 10.4 Resultado esperado

- Tareas recurrentes ejecutadas por el equipo entrante.
- Validación de autonomía básica.
- Runbooks corregidos.
- Identificación de tareas que pueden pasar a Fase 6.

---

# 12. Actividad 6. Ejecutar despliegues supervisados

## 11.1 Objetivo

Validar que el equipo entrante puede preparar, ejecutar, validar y documentar despliegues bajo supervisión.

## 11.2 Tipos de despliegues recomendados

La progresión recomendada es:

1. Despliegue en DEV.
2. Despliegue en entorno de integración.
3. Despliegue en UAT.
4. Despliegue en PRE.
5. Participación en despliegue productivo.
6. Ejecución supervisada de despliegue productivo, si el cliente lo autoriza.

## 11.3 Qué debe ejecutar el equipo entrante

- Revisar ticket de cambio.
- Confirmar rama, tag o versión.
- Confirmar artefacto.
- Revisar aprobaciones.
- Preparar comunicación.
- Ejecutar pipeline o coordinar ejecución.
- Verificar logs.
- Ejecutar smoke test.
- Solicitar validación funcional.
- Monitorizar postdespliegue.
- Documentar evidencias.
- Confirmar cierre.
- Identificar rollback si aplica.

## 11.4 Evaluación de despliegue supervisado

| Criterio | Evaluación | Observaciones |
|---|---|---|
| Preparación correcta | Sí / No / Parcial |  |
| Versión identificada | Sí / No / Parcial |  |
| Aprobaciones revisadas | Sí / No / Parcial |  |
| Ejecución correcta | Sí / No / Parcial |  |
| Validación técnica | Sí / No / Parcial |  |
| Validación funcional | Sí / No / Parcial |  |
| Monitorización posterior | Sí / No / Parcial |  |
| Criterio rollback conocido | Sí / No / Parcial |  |
| Evidencias registradas | Sí / No / Parcial |  |

## 11.5 Resultado esperado

- Despliegues ejecutados o coordinados por el equipo entrante.
- Procedimientos de despliegue validados.
- Criterios de rollback interiorizados.
- Capacidad de cambio medida.
- Evidencias para Fase 6.

---

# 13. Actividad 7. Ejecutar procesos batch o reprocesos supervisados

## 12.1 Objetivo

Validar que el equipo entrante puede monitorizar, validar y, cuando esté autorizado, ejecutar tareas relacionadas con procesos batch críticos.

## 12.2 Actividades posibles

- Revisar ejecución batch.
- Comprobar secuencia de jobs.
- Revisar logs.
- Validar salidas.
- Revisar ficheros generados.
- Comprobar número de registros procesados.
- Identificar errores.
- Proponer reintento.
- Ejecutar reproceso supervisado.
- Validar resultado funcional.
- Comunicar estado.

## 12.3 Especial precaución en seguros

Los reprocesos batch pueden tener impactos graves:

- Duplicidad de recibos.
- Duplicidad de remesas.
- Documentos duplicados.
- Estados inconsistentes de pólizas.
- Errores en renovaciones.
- Descuadres contables.
- Reporting incorrecto.
- Impacto en mediadores.
- Impacto en bancos.
- Impacto regulatorio.

Por eso, cualquier reproceso debe tener:

- Autorización.
- Criterio claro.
- Backup o punto de control si aplica.
- Validación previa.
- Validación posterior.
- Evidencia.
- Responsable funcional.
- Responsable técnico.
- Plan de reversión o contención.

## 12.4 Matriz de evaluación batch

| Criterio | Evaluación | Observaciones |
|---|---|---|
| Identifica job correcto | Sí / No / Parcial |  |
| Entiende dependencias | Sí / No / Parcial |  |
| Revisa logs correctos | Sí / No / Parcial |  |
| Interpreta salida | Sí / No / Parcial |  |
| Identifica impacto | Sí / No / Parcial |  |
| Solicita autorización | Sí / No / N/A |  |
| Ejecuta reproceso correctamente | Sí / No / N/A |  |
| Valida resultado | Sí / No / Parcial |  |
| Documenta evidencias | Sí / No / Parcial |  |

## 12.5 Resultado esperado

- Procesos batch validados por el equipo entrante.
- Reprocesos entendidos.
- Riesgos de batch controlados.
- Límites de autonomía definidos para Fase 6.

---

# 14. Actividad 8. Ejecutar escalados y comunicaciones supervisadas

## 13.1 Objetivo

Validar que el equipo entrante puede escalar y comunicar correctamente durante la operación.

## 13.2 Tipos de comunicación

| Tipo | Ejemplo |
|---|---|
| Comunicación a negocio | Aviso de incidencia, avance, resolución. |
| Comunicación a IT | Escalado a infraestructura, DBA, seguridad. |
| Comunicación a proveedor | Apertura de ticket a tercero. |
| Comunicación ejecutiva | Resumen de incidencia mayor. |
| Comunicación postdespliegue | Confirmación de éxito o rollback. |
| Comunicación de cierre | Causa, resolución, validación y acciones. |

## 13.3 Qué debe validar el equipo saliente

- Si el mensaje es claro.
- Si el impacto está bien descrito.
- Si la severidad es correcta.
- Si se evita alarmar innecesariamente.
- Si no se oculta información relevante.
- Si se informa a los destinatarios adecuados.
- Si se indican próximas actualizaciones.
- Si se respetan protocolos del cliente.
- Si se evita divulgar datos sensibles.
- Si se documenta en ITSM.

## 13.4 Plantilla de evaluación de comunicación

| Criterio | Evaluación | Observaciones |
|---|---|---|
| Claridad | Correcta / Parcial / Incorrecta |  |
| Impacto descrito | Correcto / Parcial / Incorrecto |  |
| Destinatarios adecuados | Sí / No / Parcial |  |
| Tono adecuado | Sí / No / Parcial |  |
| Próximos pasos indicados | Sí / No / Parcial |  |
| Datos sensibles protegidos | Sí / No |  |
| Registro en ITSM | Sí / No / Parcial |  |

## 13.5 Resultado esperado

- Comunicaciones supervisadas correctamente realizadas.
- Escalados validados.
- Plantillas ajustadas.
- Capacidad de interlocución operativa validada.

---

# 15. Actividad 9. Ejecutar simulacros controlados

## 14.1 Objetivo

Practicar escenarios críticos que no hayan ocurrido de forma natural durante la transición.

## 14.2 Casos candidatos

| Escenario | Objetivo |
|---|---|
| Caída de API crítica | Validar diagnóstico, escalado y comunicación. |
| Fallo de batch de recibos | Validar revisión, reproceso y control de impacto. |
| Error en generación documental | Validar análisis funcional-técnico. |
| Timeout con proveedor externo | Validar integración, escalado y workaround. |
| Despliegue fallido en PRE | Validar rollback. |
| Certificado próximo a caducar | Validar procedimiento de control. |
| Alerta crítica fuera de horario | Validar guardia y escalado. |
| Descuadre de reporting | Validar análisis de datos y comunicación. |

## 14.3 Reglas de simulacro

- Debe tener alcance claro.
- Debe estar autorizado.
- No debe poner en riesgo producción.
- Debe tener guion.
- Debe tener observadores.
- Debe tener criterios de éxito.
- Debe tener debrief posterior.
- Debe actualizar runbooks.
- Debe generar evidencias.

## 14.4 Plantilla de simulacro

```markdown
# Simulacro de reverse shadowing

## Escenario

## Objetivo

## Aplicación / dominio

## Participantes

- Equipo entrante:
- Supervisor saliente:
- Cliente:
- Observadores:

## Condiciones iniciales

## Guion del simulacro

1.
2.
3.

## Acciones esperadas

## Criterios de éxito

## Resultado

## Errores detectados

## Gaps

## Acciones de mejora

## Evidencias
```

## 14.5 Resultado esperado

- Escenarios críticos practicados.
- Preparación realista del equipo entrante.
- Runbooks validados bajo presión.
- Gaps corregidos antes de Fase 6.

---

# 16. Actividad 10. Medir autonomía del equipo entrante

## 15.1 Objetivo

Evaluar objetivamente el grado de autonomía del equipo entrante por aplicación, proceso o dominio.

## 15.2 Dimensiones de autonomía

| Dimensión | Pregunta |
|---|---|
| Funcional | ¿Entiende el proceso de negocio afectado? |
| Técnica | ¿Entiende componentes, logs, datos e integraciones? |
| Operativa | ¿Sigue correctamente el flujo ITSM? |
| Diagnóstico | ¿Formula hipótesis correctas? |
| Ejecución | ¿Ejecuta acciones seguras? |
| Comunicación | ¿Informa correctamente? |
| Escalado | ¿Pide ayuda a tiempo y a quien corresponde? |
| Documentación | ¿Registra evidencias y actualiza runbooks? |
| Riesgo | ¿Identifica impacto y límites? |
| Seguridad | ¿Respeta accesos, datos y secretos? |

## 15.3 Escala de autonomía

| Nivel | Descripción |
|---|---|
| 0. No preparado | No entiende o no puede operar el caso. |
| 1. Requiere guía completa | Puede ejecutar solo con instrucciones paso a paso. |
| 2. Requiere supervisión estrecha | Ejecuta, pero necesita validación constante. |
| 3. Supervisión ligera | Opera correctamente con revisión puntual. |
| 4. Autónomo controlado | Opera de forma autónoma en casos definidos. |
| 5. Autónomo | Puede operar y escalar con criterio en BAU. |

## 15.4 Matriz de autonomía

| Aplicación / dominio | Incidencias | Diagnóstico | Despliegues | Batch | Comunicación | Escalado | Nivel autonomía | Observaciones |
|---|---|---|---|---|---|---|---|---|
| Emisión | 3 | 3 | 2 | N/A | 3 | 3 | 3 | Reforzar rollback. |
| Recibos | 2 | 3 | 2 | 2 | 3 | 3 | 2 | Requiere más batch. |
| Portal mediadores | 4 | 4 | 3 | N/A | 4 | 4 | 4 | Candidato Fase 6. |

## 15.5 Resultado esperado

- Nivel de autonomía por aplicación.
- Identificación de dominios preparados.
- Identificación de dominios que requieren refuerzo.
- Evidencias para decisión de Fase 6.

---

# 17. Actividad 11. Gestionar feedback del equipo saliente

## 16.1 Objetivo

Obtener retroalimentación estructurada del equipo saliente sobre el desempeño del equipo entrante.

## 16.2 Qué feedback solicitar

- Fortalezas observadas.
- Errores recurrentes.
- Riesgos de autonomía.
- Actividades que ya pueden asumir.
- Actividades que aún no deben asumir.
- Runbooks que siguen siendo insuficientes.
- Gaps de conocimiento.
- Recomendaciones para Fase 6.
- Casos que deben repetirse.
- Aplicaciones que requieren más supervisión.

## 16.3 Plantilla de feedback

| Pregunta | Respuesta |
|---|---|
| ¿Qué ha ejecutado bien el equipo entrante? |  |
| ¿Dónde ha necesitado más ayuda? |  |
| ¿Qué errores o dudas se han repetido? |  |
| ¿Qué actividades puede asumir ya? |  |
| ¿Qué actividades no debería asumir todavía? |  |
| ¿Qué runbooks necesitan mejora? |  |
| ¿Qué riesgos siguen abiertos? |  |
| ¿Qué recomendáis antes de pasar a Fase 6? |  |

## 16.4 Buenas prácticas

- Pedir feedback concreto, no genérico.
- Basarlo en casos observados.
- Evitar que se convierta en juicio personal.
- Traducir feedback en acciones.
- Validar con evidencias.
- Registrar desacuerdos si los hay.
- Revisar feedback con el cliente.

## 16.5 Resultado esperado

- Evaluación objetiva del equipo saliente.
- Acciones de refuerzo.
- Evidencias para Go / No-Go.
- Mayor confianza para asunción progresiva.

---

# 18. Actividad 12. Corregir gaps antes de pasar a Fase 6

## 17.1 Objetivo

Cerrar o mitigar los gaps detectados durante la ejecución supervisada.

## 17.2 Tipos de gaps frecuentes

| Tipo | Ejemplo |
|---|---|
| Conocimiento | El equipo no entiende una regla funcional. |
| Acceso | Falta permiso para consultar logs o herramientas. |
| Procedimiento | Runbook ambiguo o incompleto. |
| Diagnóstico | No se sabe interpretar una alerta. |
| Técnico | No se conoce componente afectado. |
| Batch | No se entiende reproceso. |
| Despliegue | Rollback no interiorizado. |
| Comunicación | Mensaje a negocio incompleto. |
| Seguridad | Duda sobre tratamiento de datos sensibles. |
| Escalado | No se sabe a quién acudir. |

## 17.3 Matriz de gaps de reverse shadowing

| ID | Aplicación | Gap | Tipo | Criticidad | Acción | Responsable | Estado |
|---|---|---|---|---|---|---|---|
| GRS-001 | Recibos | Dudas en reproceso de remesas | Batch | Alta | Repetir simulacro |  | Abierto |
| GRS-002 | Emisión | Rollback no practicado | Despliegue | Alta | Simulación en PRE |  | Abierto |
| GRS-003 | Siniestros | Escalado funcional no claro | Escalado | Media | Actualizar matriz |  | En curso |

## 17.4 Criterios de tratamiento

| Criticidad del gap | Tratamiento |
|---|---|
| Crítico | Bloquea paso a Fase 6 para esa aplicación. |
| Alto | Debe cerrarse o tener mitigación formal. |
| Medio | Puede pasar con plan de acción y seguimiento. |
| Bajo | Puede incorporarse a mejora continua. |

## 17.5 Resultado esperado

- Gaps críticos cerrados.
- Gaps altos mitigados.
- Plan de acción para pendientes.
- Riesgos residuales aceptados si procede.

---

# 19. Actividad 13. Preparar el Go / No-Go hacia Fase 6

## 18.1 Objetivo

Decidir si una aplicación, dominio o bloque funcional puede pasar a asunción progresiva del servicio.

## 18.2 Participantes recomendados

- Sponsor o responsable cliente.
- Transition Manager.
- Service Manager.
- Líder técnico entrante.
- Líder funcional entrante.
- Equipo saliente.
- Operaciones.
- Seguridad si aplica.
- Negocio si el dominio es crítico.

## 18.3 Información a revisar

- Actividades ejecutadas.
- Tickets gestionados.
- Incidencias diagnosticadas.
- Despliegues supervisados.
- Batch supervisados.
- Simulacros realizados.
- Gaps abiertos.
- Riesgos.
- Feedback del equipo saliente.
- Matriz de autonomía.
- Estado de runbooks.
- Estado de accesos.
- SLAs durante la fase.
- Incidentes relevantes.
- Limitaciones de autonomía.

## 18.4 Decisiones posibles

| Decisión | Significado |
|---|---|
| Go | Puede pasar a Fase 6. |
| Go condicionado | Puede pasar con restricciones y plan de mitigación. |
| No-Go temporal | Requiere refuerzo antes de pasar. |
| No-Go | No está preparado y requiere replantear transferencia. |

## 18.5 Plantilla de decisión

```markdown
# Decisión Go / No-Go hacia Fase 6

## Aplicación / dominio

## Resumen de reverse shadowing

## Evidencias revisadas

- Tickets:
- Incidencias:
- Despliegues:
- Batch:
- Simulacros:
- Runbooks:
- Gaps:
- Riesgos:

## Nivel de autonomía

## Riesgos residuales

## Restricciones propuestas

## Decisión

- Go / Go condicionado / No-Go temporal / No-Go

## Condiciones

## Acciones posteriores

## Responsables

## Fecha de revisión
```

## 18.6 Resultado esperado

- Decisión formal por aplicación o dominio.
- Alcance de asunción progresiva definido.
- Restricciones documentadas.
- Plan de mitigación si procede.
- Preparación de Fase 6.

---


---

# 20. Actividad 14. Registrar evidencias ITIL de ejecución supervisada

## 20.1 Objetivo

Asegurar que todas las actividades ejecutadas durante el reverse shadowing quedan registradas con el nivel de evidencia necesario para soportar la decisión de asunción progresiva de la Fase 6.

Esta actividad convierte la ejecución supervisada en una prueba objetiva de preparación operativa.

## 20.2 Evidencias mínimas por tipo de actividad

| Tipo de actividad | Evidencia mínima esperada |
|---|---|
| Ticket o incidencia | ID de ticket, diagnóstico, acción, validación, cierre, feedback del supervisor. |
| Diagnóstico técnico | Herramientas usadas, logs revisados, hipótesis, causa probable, acción propuesta. |
| Diagnóstico funcional-técnico | Proceso afectado, regla o dato revisado, impacto, validación funcional. |
| Despliegue | Ticket de cambio, versión, pipeline, aprobación, validación posterior, criterio de rollback. |
| Batch o reproceso | Job, ventana, logs, validaciones, autorización, resultado, impacto. |
| Escalado | Motivo, destinatario, canal, hora, respuesta, resultado. |
| Comunicación | Mensaje emitido, destinatarios, impacto descrito, próxima actualización, cierre. |
| Simulacro | Guion, participantes, resultado, errores, acciones de mejora. |

## 20.3 Matriz de evidencias ITIL de reverse shadowing

| ID | Servicio | Aplicación | Actividad | Práctica ITIL | SLA/OLA relacionado | Evidencia | Resultado | Nivel autonomía |
|---|---|---|---|---|---|---|---|---|
| EV-RS-001 |  |  | Ticket gestionado | Incident Management |  | Ticket / acta | Correcto / Refuerzo |  |
| EV-RS-002 |  |  | Despliegue supervisado | Change Enablement / Deployment Management |  | Cambio / pipeline / acta | Correcto / Refuerzo |  |
| EV-RS-003 |  |  | Batch validado | Monitoring and Event Management |  | Logs / checklist | Correcto / Refuerzo |  |

## 20.4 Criterios de calidad de la evidencia

Una evidencia se considerará válida cuando:

- Permita reconstruir qué ocurrió.
- Indique quién ejecutó y quién supervisó.
- Identifique aplicación, servicio y entorno.
- Refleje la acción realizada.
- Incluya validaciones posteriores.
- Indique si hubo desviaciones.
- Registre gaps o mejoras detectadas.
- No contenga secretos ni datos sensibles no autorizados.
- Esté ubicada en el repositorio documental definido.

## 20.5 Resultado esperado

- Evidencias homogéneas de ejecución supervisada.
- Trazabilidad entre actividades, prácticas ITIL y servicios.
- Base objetiva para la matriz de autonomía.
- Base objetiva para la decisión Go / No-Go hacia Fase 6.

# 21. Entregables de la Fase 5

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Plan de reverse shadowing | Actividades, responsables, supervisores y calendario. | Transition Manager |
| Matriz de actividades ejecutadas | Registro de tickets, diagnósticos, despliegues, batch y simulacros. | Transition Manager |
| Evaluaciones por actividad | Valoración del desempeño por caso. | Supervisores salientes |
| Matriz de autonomía | Nivel de autonomía por aplicación o dominio. | Service Manager / líder técnico |
| Actas de reverse shadowing | Evidencia de ejecución supervisada. | Equipo entrante |
| Runbooks actualizados | Ajustes derivados de ejecución real. | Equipo entrante |
| Guías de diagnóstico actualizadas | Mejoras por errores o dudas detectadas. | Equipo técnico |
| Matriz de gaps de reverse shadowing | Gaps encontrados durante ejecución. | Transition Manager |
| RAID log actualizado | Riesgos operativos residuales. | Transition Manager |
| Feedback del equipo saliente | Validación y recomendaciones. | Equipo saliente |
| Simulacros documentados | Evidencias de escenarios practicados. | Equipo entrante |
| Decisión Go / No-Go hacia Fase 6 | Aceptación por aplicación o dominio. | Cliente + Transition Manager |

---


## 21.1 Entregables ITIL adicionales

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Matriz de evidencias ITIL de reverse shadowing | Relación entre actividades ejecutadas, prácticas ITIL, servicio afectado, SLA/OLA y evidencia generada. | Transition Manager / Service Manager |
| Registro de problemas recurrentes | Incidencias repetidas, causas conocidas, workarounds y posibles problem records. | Service Manager / líder técnico |
| Registro de cambios ejecutados o supervisados | Cambios, releases, despliegues y validaciones realizados durante la fase. | Change Manager / DevOps |
| Registro de escalados a proveedores | Evidencia de escalados a terceros y tiempos de respuesta observados. | Service Manager |
| Evaluación de cumplimiento de SLAs durante reverse shadowing | Revisión de severidades, tiempos de respuesta y resolución durante las actividades ejecutadas. | Service Manager |
| Registro de mejora continua | Mejoras derivadas de errores, dudas, ineficiencias o gaps observados. | Transition Manager |

# 22. Plantillas útiles de la Fase 5

## 20.1 Matriz de actividades ejecutadas

| ID | Fecha | Aplicación | Tipo | Actividad | Responsable entrante | Supervisor saliente | Resultado | Evidencia |
|---|---|---|---|---|---|---|---|---|
| RS-001 |  |  | Ticket |  |  |  | Correcto / Refuerzo |  |
| RS-002 |  |  | Despliegue |  |  |  | Correcto / Refuerzo |  |
| RS-003 |  |  | Batch |  |  |  | Correcto / Refuerzo |  |

## 20.2 Matriz de errores de aprendizaje

| ID | Aplicación | Situación | Error / duda | Causa | Acción correctiva | Estado |
|---|---|---|---|---|---|---|
| EA-001 |  | Diagnóstico | No se revisó integración | Runbook incompleto | Actualizar guía | Cerrado |
| EA-002 |  | Comunicación | Impacto poco claro | Falta plantilla | Crear plantilla | En curso |

## 20.3 Matriz de límites de autonomía

| Aplicación | Actividad | Permitido en Fase 6 | Restricción | Escalado obligatorio |
|---|---|---|---|---|
| Recibos | Reproceso remesas | No / Condicionado | Requiere autorización negocio | Operaciones + negocio |
| Emisión | Despliegue PRE | Sí | Notificación previa | Líder técnico |
| Siniestros | Consulta logs | Sí | Solo lectura | L3 si error crítico |

## 20.4 Checklist de ejecución supervisada

```markdown
# Checklist de ejecución supervisada

## Antes de ejecutar

- [ ] Actividad autorizada.
- [ ] Supervisor asignado.
- [ ] Runbook disponible.
- [ ] Accesos confirmados.
- [ ] Impacto evaluado.
- [ ] Riesgos revisados.
- [ ] Plan de rollback o contención conocido.
- [ ] Comunicación preparada si aplica.

## Durante la ejecución

- [ ] Pasos seguidos según runbook.
- [ ] Evidencias capturadas.
- [ ] Logs revisados.
- [ ] Validaciones realizadas.
- [ ] Escalado si procede.
- [ ] Supervisor informado.
- [ ] Incidencias registradas.

## Después de ejecutar

- [ ] Validación técnica completada.
- [ ] Validación funcional completada.
- [ ] Ticket actualizado.
- [ ] Comunicación realizada si aplica.
- [ ] Runbook actualizado si procede.
- [ ] Gaps registrados.
- [ ] Feedback solicitado.
```

---


## 22.5 Registro de problemas recurrentes

| ID | Servicio | Aplicación | Incidencia recurrente | Causa conocida | Workaround | ¿Requiere problem record? | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| PR-RS-001 |  |  |  |  |  | Sí / No |  | Abierto / En análisis / Cerrado |

## 22.6 Registro de cambios y despliegues supervisados

| ID cambio | Aplicación | Tipo | Entorno | Versión / artefacto | Aprobación | Validación post | Rollback conocido | Resultado |
|---|---|---|---|---|---|---|---|---|
| CH-RS-001 |  | Release / Hotfix / Configuración |  |  | Sí / No | Sí / No | Sí / No | Correcto / Refuerzo |

## 22.7 Registro de mejora continua

| ID | Origen | Mejora propuesta | Beneficio esperado | Prioridad | Responsable | Estado |
|---|---|---|---|---|---|---|
| MC-RS-001 | Ticket / Despliegue / Batch / Simulacro |  | Reducción de riesgo / tiempo / dependencia | Alta / Media / Baja |  | Propuesta / Aprobada / En curso |

# 23. Checklist operativo de Fase 5

## 21.1 Preparación

- [ ] Revisar cierre de Fase 4.
- [ ] Definir actividades autorizadas.
- [ ] Definir niveles de autorización.
- [ ] Asignar supervisores salientes.
- [ ] Asignar responsables entrantes.
- [ ] Confirmar accesos.
- [ ] Confirmar runbooks.
- [ ] Definir criterios de evaluación.
- [ ] Definir criterios de parada.
- [ ] Preparar calendario.
- [ ] Preparar plantillas.

## 21.2 Tickets e incidencias

- [ ] Gestionar tickets de baja criticidad.
- [ ] Gestionar tickets de media criticidad.
- [ ] Diagnosticar incidencias recurrentes.
- [ ] Diagnosticar incidencias funcionales-técnicas.
- [ ] Documentar resolución.
- [ ] Validar cierre con supervisor.
- [ ] Registrar gaps.

## 21.3 Diagnóstico

- [ ] Consultar logs.
- [ ] Usar dashboards.
- [ ] Revisar APM.
- [ ] Revisar BBDD si aplica.
- [ ] Revisar integraciones.
- [ ] Formular hipótesis.
- [ ] Proponer acción.
- [ ] Escalar si procede.
- [ ] Documentar diagnóstico.

## 21.4 Despliegues

- [ ] Ejecutar despliegue en DEV.
- [ ] Ejecutar despliegue en PRE.
- [ ] Participar en despliegue productivo.
- [ ] Revisar ticket de cambio.
- [ ] Confirmar artefacto.
- [ ] Ejecutar validaciones previas.
- [ ] Ejecutar validaciones posteriores.
- [ ] Revisar rollback.
- [ ] Documentar evidencias.

## 21.5 Batch

- [ ] Revisar ejecución batch.
- [ ] Validar logs.
- [ ] Validar salidas.
- [ ] Identificar errores.
- [ ] Proponer reproceso.
- [ ] Ejecutar reproceso supervisado si aplica.
- [ ] Validar resultado.
- [ ] Documentar evidencias.

## 21.6 Comunicación y escalado

- [ ] Preparar comunicación de incidencia.
- [ ] Realizar escalado técnico.
- [ ] Realizar escalado funcional.
- [ ] Realizar escalado a proveedor.
- [ ] Actualizar ticket.
- [ ] Comunicar resolución.
- [ ] Validar tono y destinatarios.

## 21.7 Evaluación y cierre

- [ ] Solicitar feedback del equipo saliente.
- [ ] Actualizar matriz de autonomía.
- [ ] Actualizar runbooks.
- [ ] Actualizar gaps.
- [ ] Actualizar RAID log.
- [ ] Preparar Go / No-Go.
- [ ] Definir restricciones para Fase 6.
- [ ] Formalizar decisión.

---


## 23.8 Checklist ITIL de reverse shadowing

- [ ] Cada actividad ejecutada está vinculada a un servicio, aplicación o dominio.
- [ ] Cada actividad tiene supervisor saliente identificado.
- [ ] Cada actividad tiene evidencia registrada.
- [ ] Los tickets gestionados respetan el flujo ITSM.
- [ ] Las severidades se han asignado correctamente.
- [ ] Los SLAs/OLAs se han tenido en cuenta durante la ejecución.
- [ ] Los cambios ejecutados cuentan con aprobación y evidencias.
- [ ] Los despliegues supervisados tienen validación posterior.
- [ ] Los criterios de rollback son conocidos cuando aplica.
- [ ] Los reprocesos batch cuentan con autorización y validación funcional.
- [ ] Los escalados a proveedores quedan registrados.
- [ ] Los problemas recurrentes se han identificado.
- [ ] Los workarounds usados están documentados.
- [ ] La base de conocimiento ha sido actualizada.
- [ ] Los riesgos residuales se han incorporado al RAID log.
- [ ] Las mejoras detectadas se han incorporado al registro de mejora continua.
- [ ] La matriz de autonomía está soportada por evidencias.
- [ ] La decisión Go / No-Go está vinculada a criterios objetivos.

# 24. Riesgos específicos de la Fase 5

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El equipo entrante opera sin supervisión suficiente | Riesgo productivo | Definir niveles de autorización y supervisores. |
| Se delegan actividades demasiado críticas demasiado pronto | Incidencia grave | Progresividad y Go / No-Go por actividad. |
| El equipo entrante no escala a tiempo | Mayor impacto operativo | Reforzar criterios de escalado y simulacros. |
| El equipo saliente interviene demasiado pronto | No se valida autonomía real | Permitir ejecución supervisada antes de corregir. |
| El equipo saliente no interviene cuando debe | Riesgo de error | Definir criterios de parada. |
| Runbooks ambiguos | Ejecución incorrecta | Actualizar tras cada caso. |
| Falta de accesos | Bloqueo operativo | Validar accesos antes de actividades. |
| Falta de casos reales | Baja evidencia de autonomía | Usar simulacros y tickets históricos. |
| Despliegue sin rollback claro | Riesgo alto | No autorizar hasta documentar rollback. |
| Reproceso batch incorrecto | Duplicidades o descuadres | Supervisión estricta y autorización funcional. |
| Comunicación deficiente | Confusión con negocio o cliente | Plantillas y revisión previa. |
| Evaluación subjetiva | Aceptación débil | Matriz de autonomía y evidencias. |
| Tickets gestionados sin relación con SLAs | No se valida capacidad real de servicio | Asociar cada ticket a severidad, prioridad y SLA/OLA aplicable. |
| Cambios ejecutados sin evidencias suficientes | Riesgo de auditoría y baja trazabilidad | Registrar ticket de cambio, aprobación, versión, validaciones y cierre. |
| Incidencias recurrentes no convertidas en problemas | Se perpetúan fallos estructurales | Crear registro de problemas recurrentes y proponer problem records. |
| Escalados a proveedores no probados | Riesgo en incidencias reales futuras | Ejecutar o simular escalados a terceros críticos. |
| Se mide autonomía global sin separar servicios | Falsa sensación de preparación | Evaluar autonomía por aplicación, dominio, actividad y criticidad. |

---

# 25. Criterios de salida de la Fase 5

## 23.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Plan de reverse shadowing ejecutado | Matriz de actividades | Pendiente / En curso / Validado |
| Tickets gestionados por equipo entrante | Tickets / actas |  |
| Incidencias diagnosticadas | Evaluaciones |  |
| Incidencias funcionales-técnicas gestionadas | Casos documentados |  |
| Tareas recurrentes ejecutadas | Checklists |  |
| Despliegues supervisados realizados | Actas / evidencias |  |
| Batch o reprocesos supervisados | Actas batch |  |
| Escalados realizados correctamente | Tickets / comunicaciones |  |
| Comunicaciones supervisadas | Plantillas / actas |  |
| Simulacros realizados si aplica | Actas simulacro |  |
| Runbooks actualizados | Repositorio documental |  |
| Gaps críticos cerrados | Matriz de gaps |  |
| Riesgos residuales documentados | RAID log |  |
| Feedback del equipo saliente recogido | Plantilla feedback |  |
| Matriz de autonomía completada | Matriz autonomía |  |
| Go / No-Go hacia Fase 6 realizado | Acta de decisión |  |
| Evidencias ITIL registradas | Matriz de evidencias ITIL |  |
| SLAs/OLAs revisados durante ejecución | Informe o revisión de tickets |  |
| Cambios y despliegues trazados | Registro de cambios/despliegues supervisados |  |
| Problemas recurrentes identificados | Registro de problemas recurrentes |  |
| Mejoras operativas registradas | Registro de mejora continua |  |
| Límites de autonomía documentados | Matriz de límites de autonomía |  |

## 23.2 Criterio de salida recomendado

La Fase 5 puede considerarse cerrada cuando:

> El equipo entrante ha demostrado, mediante ejecución supervisada y evidencias objetivas, que puede gestionar tickets, diagnosticar incidencias, usar herramientas, ejecutar tareas recurrentes, participar en despliegues, validar procesos batch, escalar correctamente, comunicar con criterio y operar determinadas aplicaciones o dominios con un nivel de autonomía suficiente para iniciar la asunción progresiva del servicio en la Fase 6.

---


## 25.3 Gate ITIL de salida de Fase 5

La salida de la Fase 5 debe formalizarse mediante un gate de validación operativa. Este gate no debe aprobar únicamente el cierre de la fase, sino determinar qué servicios, aplicaciones, dominios o actividades pueden pasar a asunción progresiva en la Fase 6.

| Dimensión | Pregunta de control | Evidencia |
|---|---|---|
| Incidencias | ¿El equipo entrante ha gestionado tickets representativos bajo supervisión? | Tickets, actas, evaluaciones. |
| Diagnóstico | ¿Ha demostrado criterio técnico y funcional? | Matrices de evaluación. |
| Cambios | ¿Ha participado en cambios o despliegues con control? | Registros de cambio, despliegue y validación. |
| Batch | ¿Ha validado o ejecutado procesos batch autorizados? | Actas batch, logs, checklist. |
| SLAs | ¿Ha operado considerando prioridad, severidad y tiempos? | Revisión de tickets y SLAs. |
| Escalado | ¿Ha escalado correctamente a equipos internos o terceros? | Tickets, comunicaciones, matriz de escalado. |
| Seguridad | ¿Ha respetado accesos, datos sensibles y restricciones? | Evidencias de ejecución y revisión de seguridad. |
| Conocimiento | ¿Ha usado y actualizado runbooks y KB? | Runbooks y base de conocimiento actualizados. |
| Riesgo | ¿Los riesgos residuales están aceptados o mitigados? | RAID log actualizado. |
| Autonomía | ¿Existe nivel de autonomía suficiente por aplicación o dominio? | Matriz de autonomía. |

### Decisiones posibles del gate

| Decisión | Uso recomendado |
|---|---|
| **Go** | El servicio, aplicación o actividad puede pasar a Fase 6 sin restricciones relevantes. |
| **Go condicionado** | Puede pasar a Fase 6 con restricciones, supervisión temporal o mitigaciones concretas. |
| **No-Go temporal** | Requiere repetir reverse shadowing, cerrar gaps o reforzar conocimiento antes de avanzar. |
| **No-Go** | No existe preparación suficiente y debe replantearse la transferencia del ámbito afectado. |

### Criterio ITIL de salida

La Fase 5 podrá considerarse superada cuando exista evidencia objetiva de que el equipo entrante puede ejecutar los procesos operativos definidos bajo control, respetando procedimientos, SLAs, criterios de cambio, seguridad, escalado y documentación, y cuando los riesgos residuales estén formalmente aceptados o mitigados.

# 26. Recomendaciones prácticas para liderar la Fase 5

## 24.1 Recomendaciones de enfoque

- No pasar a ejecución sin límites claros.
- Empezar por actividades de menor riesgo.
- Usar niveles de autorización.
- Definir criterios de parada.
- Exigir evidencias.
- Permitir errores controlados.
- Hacer debrief después de cada actividad relevante.
- Pedir feedback concreto al equipo saliente.
- No confundir confianza con autonomía demostrada.
- Medir autonomía por aplicación, no de forma global.
- Separar actividades preparadas de actividades aún no autorizadas.
- Documentar restricciones para Fase 6.

## 24.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- El equipo entrante no sabe por dónde empezar un diagnóstico.
- Consulta herramientas sin criterio.
- No entiende impacto funcional.
- No identifica cuándo escalar.
- Ejecuta pasos sin entender consecuencias.
- No documenta evidencias.
- No actualiza tickets.
- No comunica adecuadamente.
- No sabe validar después de actuar.
- Depende excesivamente del experto saliente.
- El equipo saliente corrige constantemente.
- Hay errores repetidos en casos similares.
- Se intenta pasar a Fase 6 sin matriz de autonomía.

## 24.3 Buenas prácticas

- Evaluar cada caso inmediatamente después.
- Registrar tanto aciertos como gaps.
- Convertir errores en mejoras de runbook.
- Mantener una matriz de autonomía visible.
- Validar autonomía con casos reales y simulados.
- No autorizar reprocesos críticos sin doble validación.
- Mantener al cliente informado de avances y límites.
- Usar Go / No-Go por aplicación o dominio.
- Evitar una aceptación final genérica.
- Asegurar que el equipo entrante conoce sus límites.

---

# 27. Resumen ejecutivo de la Fase 5

La Fase 5 es el momento en el que la transición deja de ser transferencia de conocimiento y se convierte en **demostración de capacidad operativa**.

El equipo entrante debe pasar de decir “sabemos cómo se hace” a demostrar:

1. Que sabe recibir y clasificar tickets.
2. Que sabe diagnosticar incidencias.
3. Que sabe consultar logs y monitorización.
4. Que sabe entender impacto funcional.
5. Que sabe usar runbooks.
6. Que sabe ejecutar tareas recurrentes.
7. Que sabe participar en despliegues.
8. Que entiende rollback y validaciones.
9. Que sabe revisar procesos batch.
10. Que sabe escalar a tiempo.
11. Que sabe comunicar correctamente.
12. Que sabe documentar evidencias.
13. Que conoce sus límites de autonomía.

La Fase 5 no debe cerrarse por sensación de confianza, sino por evidencias. Su resultado debe ser una matriz clara de qué aplicaciones, procesos o dominios pueden pasar a asunción progresiva en la Fase 6, bajo qué restricciones y con qué riesgos residuales.

El objetivo final es iniciar la Fase 6 con una transición segura, progresiva y basada en capacidad demostrada, no en suposiciones.


Desde el punto de vista ITIL, esta fase constituye el principal mecanismo de validación previa a la transferencia de responsabilidad. Permite comprobar que el equipo entrante no solo conoce el servicio, sino que puede operar los procesos de gestión del servicio con trazabilidad, control de riesgo, respeto de SLAs, uso correcto de herramientas, escalado adecuado y mejora continua.

Por tanto, la Fase 5 debe cerrarse con una decisión formal basada en evidencias, no en percepciones. La matriz de autonomía, el registro de actividades ejecutadas, las evaluaciones del equipo saliente, los tickets gestionados, los cambios supervisados, los runbooks actualizados y el RAID log deben constituir la base objetiva para decidir el paso a la asunción progresiva del servicio.


---
