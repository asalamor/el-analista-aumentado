# Plan de transición tecnológica y transferencia de conocimiento  
## Mantenimiento del stack completo de aplicaciones de una compañía aseguradora

## 1. Objetivo del plan

El objetivo de la transición es que el nuevo equipo asuma de forma **segura, controlada y verificable** el mantenimiento completo del stack de aplicaciones de la aseguradora, minimizando riesgos operativos, técnicos, regulatorios y de continuidad de negocio.

La transición no debe limitarse a “recibir documentación”. Debe garantizar que el equipo entrante:

- Entiende el mapa funcional y técnico de las aplicaciones.
- Conoce los procesos críticos de negocio asegurador soportados.
- Tiene acceso controlado a entornos, repositorios, herramientas y documentación.
- Sabe operar incidencias, cambios, despliegues y recuperaciones.
- Ha realizado shadowing, reverse shadowing y pruebas de autonomía.
- Puede cumplir los SLAs acordados.
- Puede responder ante auditorías, incidencias críticas y eventos regulatorios.
- Dispone de un modelo de gobierno para operar tras el traspaso.

---

## 2. Alineamiento metodológico con ITIL

El presente plan de transición se alinea con las buenas prácticas de ITIL con el objetivo de asegurar que el traspaso del mantenimiento se gestione como una **transición formal del servicio**, y no únicamente como una transferencia documental o una sucesión de sesiones de conocimiento.

La finalidad de este alineamiento es reforzar el gobierno de la transición, asegurar la trazabilidad de las actividades realizadas, identificar riesgos, validar la preparación operativa del equipo entrante y garantizar que el servicio pueda ser mantenido, soportado, evolucionado y gobernado de forma autónoma tras el cierre del proceso.

Desde esta perspectiva, la transición deberá demostrar que el equipo entrante adquiere progresivamente la capacidad real de:

- Comprender el servicio desde el punto de vista funcional, técnico y operativo.
- Identificar las aplicaciones, componentes, integraciones, entornos y dependencias críticas.
- Acceder a los repositorios, herramientas, entornos y documentación necesarios.
- Gestionar incidencias, problemas, cambios, despliegues y escalados.
- Conocer los niveles de servicio, acuerdos operativos y mecanismos de soporte.
- Coordinarse con proveedores, terceros y áreas internas implicadas.
- Utilizar y mantener una base de conocimiento operativa.
- Asumir la responsabilidad del mantenimiento sin dependencia crítica del equipo saliente.

El uso de ITIL en este plan no pretende introducir una carga metodológica innecesaria, sino aportar un marco de control, visibilidad y aceptación que permita convertir el traspaso en una transferencia verificable de la capacidad operativa del servicio.

### 2.1 Prácticas ITIL consideradas

El plan incorpora, de forma pragmática, prácticas ITIL relacionadas con:

| Práctica ITIL | Aplicación en la transición |
|---|---|
| **Knowledge Management** | Captura, revisión, validación y mantenimiento de la base de conocimiento. |
| **Service Configuration Management** | Inventario de servicios, aplicaciones, componentes, entornos, integraciones y dependencias. |
| **IT Asset Management** | Identificación de activos tecnológicos, herramientas, licencias, certificados y contratos relevantes. |
| **Change Enablement** | Control de cambios durante la transición y preparación del modelo de cambios futuro. |
| **Release Management** | Comprensión del calendario de versiones, ventanas de despliegue y coordinación de releases. |
| **Deployment Management** | Validación de procedimientos de despliegue, rollback y evidencias postdespliegue. |
| **Incident Management** | Observación y ejecución de la gestión real de incidencias durante shadowing y reverse shadowing. |
| **Problem Management** | Identificación de problemas recurrentes, causas raíz, workarounds y deuda operativa. |
| **Service Level Management** | Revisión de SLAs, OLAs, indicadores, expectativas y cumplimiento durante la transición. |
| **Supplier Management** | Identificación de proveedores, terceros, contratos, contactos, SLAs y escalados. |
| **Monitoring and Event Management** | Revisión de herramientas, dashboards, alertas, eventos y procedimientos de respuesta. |
| **Information Security Management** | Control de accesos, permisos, secretos, certificados, trazabilidad y cumplimiento. |
| **Service Continuity Management** | Revisión de backup, recuperación, DRP, RTO, RPO y escenarios de contingencia. |
| **Continual Improvement** | Generación de un backlog de mejora continua tras la estabilización. |

### 2.2 Principio de aplicación

ITIL se utilizará como marco de gobierno y control, no como una metodología rígida. Su aplicación será proporcional a la criticidad, complejidad y madurez del servicio transferido.

Cada fase del plan incluirá, cuando aplique:

- Prácticas ITIL relacionadas.
- Evidencias esperadas.
- Criterios de salida verificables.
- Riesgos específicos.
- Relación con la operación futura del servicio.

---

## 3. Principios rectores de la transición

Antes de entrar en fases, conviene fijar algunos principios.

| Principio | Aplicación práctica |
|---|---|
| **No asumir conocimiento no validado** | Todo conocimiento recibido debe contrastarse con código, tickets, logs, documentación o ejecución práctica. |
| **Trazabilidad completa** | Cada aplicación, servicio, API, job, batch, base de datos o dependencia debe tener propietario, documentación mínima y estado de transición. |
| **Acceso controlado y auditado** | Ningún acceso debe concederse sin registro, aprobación, finalidad y caducidad cuando proceda. |
| **Aprendizaje por operación real** | El equipo entrante debe participar en incidencias, despliegues, análisis y cambios reales. |
| **Especial atención a procesos críticos de seguros** | Cotización, emisión, suplementos, renovaciones, recibos, siniestros, mediadores, cumplimiento y reporting regulatorio. |
| **Criterios de salida objetivos** | Cada fase debe cerrar con evidencias, no con percepciones. |
| **Plan de reversibilidad** | Durante la transición debe existir capacidad de escalado al equipo saliente. |
| **Documentación viva** | La documentación debe actualizarse durante la transición y pasar a ser mantenida por el equipo entrante. |

---

## 4. Fases del proceso de transición

### Vista general

| Fase | Nombre | Duración orientativa | Objetivo principal |
|---|---:|---:|---|
| 0 | Preparación y arranque | 1 semana | Establecer gobierno, alcance inicial, calendario y mecanismos de control. |
| 1 | Descubrimiento e inventario | 2-4 semanas | Identificar aplicaciones, dependencias, documentación, equipos y criticidad. |
| 2 | Transferencia documental y funcional | 3-6 semanas | Comprender procesos de negocio, documentación funcional y operación habitual. |
| 3 | Transferencia técnica profunda | 4-8 semanas | Entender arquitectura, código, datos, integraciones, despliegues y operación técnica. |
| 4 | Shadowing operativo | 3-6 semanas | Observar al equipo saliente gestionando incidencias, cambios y despliegues. |
| 5 | Reverse shadowing | 3-6 semanas | El equipo entrante opera; el saliente supervisa y corrige. |
| 6 | Asunción progresiva del servicio | 2-6 semanas | Tomar responsabilidad por bloques, aplicaciones o dominios funcionales. |
| 7 | Cierre y estabilización post-transición | 4-8 semanas | Validar autonomía, corregir huecos y cerrar formalmente la transición. |

Las duraciones dependen del número de aplicaciones, criticidad, deuda técnica, documentación existente, disponibilidad de expertos y complejidad regulatoria.

### Mapa general de fases y prácticas ITIL relacionadas

| Fase | Prácticas ITIL relacionadas | Evidencia principal esperada |
|---|---|---|
| Fase 0. Preparación y arranque | Relationship Management, Supplier Management, Risk Management, Service Level Management, Continual Improvement | Charter de transición, modelo de gobierno, alcance, riesgos iniciales y criterios de aceptación. |
| Fase 1. Descubrimiento e inventario | Service Configuration Management, IT Asset Management, Architecture Management, Information Security Management | Inventario de servicios, aplicaciones, activos, entornos, integraciones y dependencias. |
| Fase 2. Transferencia documental y funcional | Knowledge Management, Business Analysis, Service Desk, Service Level Management | Base documental funcional revisada, clasificada y validada. |
| Fase 3. Transferencia técnica profunda | Architecture Management, Infrastructure and Platform Management, Deployment Management, Release Management, Information Security Management, Service Continuity Management | Arquitectura, entornos, despliegues, seguridad, continuidad y operación técnica validadas. |
| Fase 4. Shadowing operativo | Incident Management, Monitoring and Event Management, Problem Management, Knowledge Management | Registro de observación operativa, incidencias, alertas, escalados y lecciones aprendidas. |
| Fase 5. Reverse shadowing | Service Validation, Incident Management, Problem Management, Knowledge Management, Service Level Management | Evidencias de ejecución supervisada por parte del equipo entrante. |
| Fase 6. Asunción progresiva del servicio | Change Enablement, Incident Management, Problem Management, Release Management, Deployment Management, Service Level Management, Supplier Management | Servicios asumidos por oleadas, SLAs monitorizados y riesgos controlados. |
| Fase 7. Cierre y estabilización post-transición | Continual Improvement, Problem Management, Measurement and Reporting, Service Level Management, Knowledge Management, Risk Management | Acta de cierre, riesgos residuales, backlog de mejora continua y estabilización BAU. |

---

## Fase 0. Preparación y arranque

### Objetivos

- Acordar el alcance inicial de la transición.
- Identificar stakeholders.
- Definir el modelo de gobierno.
- Establecer herramientas de seguimiento.
- Definir criterios de éxito.
- Preparar calendario de sesiones con equipos salientes.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Kick-off ejecutivo | Alineamiento entre cliente, proveedor saliente y proveedor entrante. |
| Kick-off operativo | Identificación de equipos, aplicaciones, responsables y calendario inicial. |
| Definición del modelo de gobierno | Comités, reuniones, roles, cadencia y mecanismos de escalado. |
| Creación del backlog de transición | Lista inicial de tareas, entregables, riesgos y dependencias. |
| Definición de plantilla estándar de aplicación | Documento mínimo que debe completarse por cada aplicación. |
| Definición de repositorio documental | Espacio único para documentación, actas, decisiones, diagramas y evidencias. |

### Entregables

- Acta de kick-off.
- Matriz inicial de stakeholders.
- RACI de transición.
- Calendario de sesiones.
- Backlog de transición.
- Plantilla estándar de ficha de aplicación.
- Registro inicial de riesgos.
- Definición de criterios de aceptación.

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Relationship Management.
- Supplier Management.
- Risk Management.
- Service Level Management.
- Continual Improvement.

**Aplicación en la fase:**

Esta fase establece el marco de gobierno de la transición, define los interesados, delimita el alcance, identifica riesgos iniciales y fija las reglas de coordinación entre cliente, proveedor saliente, proveedor entrante y terceros.

**Evidencias ITIL esperadas:**

- Charter o acta de arranque de la transición.
- Alcance validado.
- Modelo de gobierno.
- Matriz inicial de stakeholders.
- RACI inicial.
- Registro inicial de riesgos.
- Criterios generales de aceptación.
- Calendario de sesiones y comités.

### Criterios de salida

La fase puede cerrarse cuando:

- Existe un listado inicial de aplicaciones o dominios.
- Están identificados los interlocutores principales.
- Hay calendario de sesiones acordado.
- Hay repositorio documental compartido.
- Hay modelo de gobierno aprobado.
- Hay backlog inicial de transición.

---

## Fase 1. Descubrimiento e inventario

### Objetivos

- Construir el mapa real del stack.
- Identificar aplicaciones, componentes, procesos batch, APIs, bases de datos e integraciones.
- Clasificar criticidad funcional, técnica y regulatoria.
- Detectar documentación inexistente, obsoleta o no fiable.
- Identificar riesgos tempranos.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Inventario de aplicaciones | Lista completa de aplicaciones y módulos. |
| Inventario de componentes técnicos | Servicios, microservicios, frontales, backends, jobs, colas, APIs. |
| Inventario de entornos | Desarrollo, integración, preproducción, producción, DR. |
| Inventario de bases de datos | Motores, esquemas, tablas críticas, jobs, volumetría. |
| Inventario de integraciones | Sistemas internos, externos, mediadores, bancos, reguladores, terceros. |
| Clasificación de criticidad | Alta, media, baja según negocio, operación y regulación. |
| Identificación de propietarios | Técnico, funcional, negocio, proveedor, operación. |
| Análisis de documentación existente | Estado: vigente, parcial, obsoleta, inexistente. |

### Ficha mínima por aplicación

Cada aplicación debe tener una ficha con, al menos:

| Campo | Descripción |
|---|---|
| Nombre de aplicación | Nombre oficial y nombres alternativos usados internamente. |
| Código o identificador | Código de inventario, CMDB o portfolio. |
| Dominio funcional | Vida, Autos, Hogar, Salud, Siniestros, Recibos, Mediadores, etc. |
| Descripción funcional | Qué proceso de negocio soporta. |
| Usuarios | Internos, mediadores, clientes, backoffice, call center, batch. |
| Criticidad | Alta, media, baja. |
| Ventana de uso | 24x7, horario laboral, cierres mensuales, campañas. |
| Responsable negocio | Persona o área. |
| Responsable técnico actual | Equipo saliente. |
| Responsable técnico entrante | Equipo asignado. |
| Tecnologías | Lenguajes, frameworks, servidores, bases de datos. |
| Repositorios | URLs o identificadores de repositorio. |
| Entornos | DEV, INT, UAT, PRE, PRO, DR. |
| Dependencias | Sistemas internos, externos, librerías, servicios compartidos. |
| Documentación | Links a funcional, técnica, operación, arquitectura. |
| SLAs | Disponibilidad, respuesta, resolución. |
| Riesgos conocidos | Obsolescencia, deuda técnica, dependencia de personas, falta de tests. |
| Estado de transición | No iniciado, en curso, validado, pendiente de gaps. |
| Estado de validación documental | No recibido, recibido, revisado, contrastado, probado, aceptado u obsoleto. |
| Estado de preparación operativa | Pendiente, parcial, preparado, asumido o bloqueado. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Service Configuration Management.
- IT Asset Management.
- Architecture Management.
- Information Security Management.

**Aplicación en la fase:**

Esta fase construye una visión mínima de configuración del servicio, equivalente a una mini-CMDB operativa. Permite conocer qué servicios, aplicaciones, activos, componentes, entornos, integraciones y proveedores forman parte del perímetro transferido.

**Evidencias ITIL esperadas:**

- Inventario de servicios de negocio.
- Inventario de aplicaciones.
- Inventario de componentes técnicos.
- Inventario de entornos.
- Inventario de integraciones.
- Inventario de proveedores.
- Matriz de dependencias.
- Clasificación de criticidad.
- Estado de documentación por aplicación.

### Criterios de salida

La fase puede cerrarse cuando:

- Existe inventario razonablemente completo.
- Cada aplicación tiene una criticidad asignada.
- Se han identificado aplicaciones huérfanas o con documentación insuficiente.
- Se conocen dependencias principales.
- Se ha priorizado el orden de transferencia.
- Se dispone de una matriz aplicación / responsable / estado.

---

## Fase 2. Transferencia documental y funcional

### Objetivos

- Entender qué hacen las aplicaciones desde el punto de vista de negocio.
- Identificar procesos aseguradores soportados.
- Entender reglas de negocio críticas.
- Localizar documentación funcional, manuales, especificaciones y decisiones históricas.
- Identificar conocimiento tácito no documentado.

### Áreas funcionales típicas en aseguradoras

| Área | Aspectos a revisar |
|---|---|
| Cotización | Tarificación, cuestionarios, reglas de elegibilidad, descuentos, promociones. |
| Emisión | Alta de pólizas, validaciones, documentación contractual, firma, pagos. |
| Suplementos | Modificaciones de pólizas, cambios de riesgo, capitales, garantías. |
| Renovaciones | Procesos automáticos, campañas, anulaciones, recargos, avisos. |
| Recibos y cobros | Domiciliaciones, impagos, recobros, SEPA, conciliación bancaria. |
| Siniestros | Apertura, tramitación, peritación, pagos, reservas, fraude. |
| Mediadores | Comisiones, cartera, emisión delegada, portales, reporting. |
| Clientes | Área privada, autoservicio, comunicaciones, consentimientos. |
| Cumplimiento | KYC, prevención fraude, protección de datos, trazabilidad. |
| Reporting | Informes regulatorios, financieros, operativos, cuadros de mando. |
| Documentación | Condiciones generales, particulares, precontractual, anexos, comunicaciones. |

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Sesiones funcionales por dominio | Comprensión del flujo completo de negocio. |
| Revisión de documentación funcional | Identificación de documentación válida y gaps. |
| Análisis de tickets históricos | Incidencias recurrentes, áreas problemáticas, reglas ocultas. |
| Revisión de procesos batch funcionales | Cierres diarios, mensuales, renovaciones, recibos, reporting. |
| Identificación de reglas críticas | Tarifas, validaciones, estados, excepciones. |
| Mapeo aplicación-proceso | Qué aplicaciones intervienen en cada proceso de negocio. |
| Identificación de picos operativos | Renovaciones masivas, cierres contables, campañas comerciales. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Knowledge Management.
- Business Analysis.
- Service Desk.
- Service Level Management.
- Relationship Management.

**Aplicación en la fase:**

Esta fase convierte la documentación funcional y el conocimiento tácito en una base de conocimiento útil para operar el servicio. El objetivo no es solo recopilar documentos, sino revisar su vigencia, contrastarlos con negocio y validar que permiten entender los procesos críticos.

**Evidencias ITIL esperadas:**

- Base documental funcional clasificada.
- Glosario funcional.
- Mapa aplicación-proceso.
- Catálogo de reglas de negocio críticas.
- Catálogo de incidencias frecuentes funcionales.
- Relación de documentación obsoleta o inexistente.
- Backlog de gaps funcionales.

### Criterios de salida

La fase puede cerrarse cuando:

- El equipo entrante puede explicar los procesos funcionales principales.
- Existen mapas aplicación-proceso.
- Están identificadas reglas críticas y puntos de riesgo.
- Se conocen incidencias recurrentes y su impacto.
- Hay un backlog de gaps funcionales.
- Negocio ha validado la comprensión funcional básica.

---

## Fase 3. Transferencia técnica profunda

### Objetivos

- Entender arquitectura, código, datos, integraciones, despliegues y operación.
- Preparar al equipo para resolver incidencias y ejecutar cambios.
- Validar accesos y herramientas.
- Identificar riesgos técnicos críticos.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Revisión de arquitectura | Diagramas actualizados de alto y bajo nivel. |
| Revisión de código | Estructura, módulos, patrones, deuda técnica, puntos críticos. |
| Revisión de repositorios | Branching, versionado, permisos, dependencias. |
| Revisión de CI/CD | Pipelines, despliegues, gates, rollback. |
| Revisión de bases de datos | Modelo lógico, físico, jobs, volumetría, backups. |
| Revisión de integraciones | APIs, colas, ficheros, terceros, certificados. |
| Revisión de observabilidad | Logs, métricas, alertas, dashboards. |
| Revisión de seguridad | Secretos, usuarios técnicos, certificados, hardening. |
| Revisión de DRP | Backup, restore, RTO, RPO, pruebas realizadas. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Architecture Management.
- Infrastructure and Platform Management.
- Deployment Management.
- Release Management.
- Information Security Management.
- Service Continuity Management.

**Aplicación en la fase:**

Esta fase valida la arquitectura real del servicio, los componentes técnicos que lo soportan, los procedimientos de despliegue, los mecanismos de seguridad, la continuidad, las integraciones y los riesgos técnicos asociados.

**Evidencias ITIL esperadas:**

- Diagramas de arquitectura validados.
- Procedimientos de build, despliegue y rollback.
- Inventario de repositorios y pipelines.
- Inventario de certificados, secretos y usuarios técnicos.
- Mapa de logs, métricas, dashboards y alertas.
- Procedimientos de backup, restore y contingencia.
- Riesgos técnicos críticos registrados.

### Criterios de salida

La fase puede cerrarse cuando:

- Hay diagramas técnicos validados.
- El equipo entrante puede compilar, desplegar y diagnosticar aplicaciones en entornos no productivos.
- Los accesos necesarios están disponibles y probados.
- Se conocen procedimientos de despliegue y rollback.
- Se conocen mecanismos de monitorización y logs.
- Se han identificado riesgos técnicos críticos.
- Existe documentación mínima operativa por aplicación.

---

## Fase 4. Shadowing operativo

### Objetivos

- Observar cómo trabaja el equipo saliente.
- Entender la gestión real de incidencias, cambios, despliegues y escalados.
- Capturar procedimientos no documentados.
- Validar el comportamiento real de las aplicaciones frente a la teoría.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Asistencia a guardias o soporte | Entender dinámica real de operación. |
| Observación de incidencias reales | Diagnóstico, comunicación, resolución y cierre. |
| Observación de despliegues | Secuencia, validaciones, rollback, comunicaciones. |
| Revisión de tickets recientes | Casuística real. |
| Participación en comités operativos | Conocer prioridades y escalados. |
| Registro de conocimiento tácito | Procedimientos, trucos, excepciones, personas clave. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Incident Management.
- Monitoring and Event Management.
- Problem Management.
- Service Desk.
- Knowledge Management.

**Aplicación en la fase:**

Esta fase permite observar cómo se gestiona realmente el servicio: entrada de incidencias, clasificación, priorización, diagnóstico, escalado, comunicación, resolución, cierre y aprendizaje posterior. También permite contrastar la documentación con la operación real.

**Evidencias ITIL esperadas:**

- Registro de incidencias observadas.
- Registro de alertas y eventos revisados.
- Escalados realizados.
- Workarounds aplicados.
- Patrones de incidencias recurrentes.
- Procedimientos no documentados detectados.
- Lecciones aprendidas.
- Actualizaciones de runbooks.

### Criterios de salida

La fase puede cerrarse cuando:

- El equipo entrante ha observado suficientes casos reales.
- Se han documentado procedimientos no escritos.
- Se han identificado patrones de incidencias.
- Se conocen rutas de escalado.
- Se han validado procedimientos de despliegue y soporte.
- El equipo entrante está preparado para operar bajo supervisión.

---

## Fase 5. Reverse shadowing

### Objetivos

- El equipo entrante ejecuta la operación.
- El equipo saliente observa, corrige y valida.
- Se comprueba la autonomía práctica.
- Se detectan gaps antes de la asunción formal.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Gestión de incidencias por el equipo entrante | Validar diagnóstico y resolución. |
| Ejecución de despliegues supervisados | Validar capacidad operativa. |
| Resolución de consultas funcionales | Validar comprensión de negocio. |
| Ejecución de tareas recurrentes | Jobs, validaciones, reporting, controles. |
| Simulacros de escenarios críticos | Caída, rollback, degradación, error batch. |
| Revisión post-ejecución | Lecciones aprendidas y gaps. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Service Validation.
- Incident Management.
- Problem Management.
- Knowledge Management.
- Service Level Management.

**Aplicación en la fase:**

Esta fase actúa como prueba de preparación operativa. El equipo entrante ejecuta tareas reales o simuladas bajo supervisión del equipo saliente, demostrando que puede diagnosticar, resolver, escalar, documentar y comunicar de forma adecuada.

**Evidencias ITIL esperadas:**

- Incidencias gestionadas por el equipo entrante.
- Diagnósticos realizados.
- Escalados ejecutados.
- Despliegues o tareas recurrentes ejecutadas bajo supervisión.
- Feedback del equipo saliente.
- Gaps detectados y plan de cierre.
- Evidencia de actualización de documentación.

### Criterios de salida

La fase puede cerrarse cuando:

- El equipo entrante ha resuelto incidencias reales o simuladas.
- Ha ejecutado despliegues supervisados.
- Ha operado procedimientos recurrentes.
- Ha demostrado capacidad de análisis funcional y técnico.
- Los gaps críticos están cerrados o tienen plan aprobado.
- El equipo saliente valida la capacidad operativa mínima.

---

## Fase 6. Asunción progresiva del servicio

### Objetivos

- Transferir responsabilidad por bloques.
- Reducir dependencia del equipo saliente.
- Medir desempeño real del equipo entrante.
- Mantener escalado temporal para situaciones críticas.

### Modelos posibles de asunción

| Modelo | Cuándo usarlo |
|---|---|
| Por aplicación | Cuando las aplicaciones son independientes. |
| Por dominio funcional | Cuando hay procesos de negocio integrados, por ejemplo pólizas, siniestros o recibos. |
| Por criticidad | Primero aplicaciones de baja/media criticidad, después críticas. |
| Por tipo de operación | Primero soporte L2, luego despliegues, luego guardias, luego cambios evolutivos. |
| Por tecnología | Útil si el stack es heterogéneo: Java, .NET, Cobol, Angular, batch, mainframe, etc. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Change Enablement.
- Incident Management.
- Problem Management.
- Release Management.
- Deployment Management.
- Service Level Management.
- Supplier Management.

**Aplicación en la fase:**

Esta fase transfiere gradualmente la responsabilidad operativa al equipo entrante, manteniendo control sobre incidencias, cambios, despliegues, niveles de servicio, proveedores, riesgos y mecanismos de escalado temporal.

**Evidencias ITIL esperadas:**

- Matriz de asunción por aplicación, dominio o servicio.
- Servicios asumidos por oleadas.
- SLAs monitorizados durante la asunción.
- Cambios y despliegues gestionados por el equipo entrante.
- Incidencias gestionadas de forma principal por el equipo entrante.
- Riesgos actualizados.
- Decisiones de asunción documentadas.

### Criterios de salida

La fase puede cerrarse cuando:

- El equipo entrante opera de forma principal.
- El equipo saliente solo interviene bajo demanda.
- Los SLAs se cumplen durante un período acordado.
- No existen gaps críticos sin plan.
- La documentación operativa está bajo control del equipo entrante.
- El cliente acepta la asunción progresiva.

---

## Fase 7. Cierre y estabilización post-transición

### Objetivos

- Confirmar autonomía plena.
- Cerrar formalmente la transición.
- Consolidar documentación.
- Pasar a modo BAU, es decir, operación ordinaria.
- Definir plan de mejora continua.

### Actividades clave

| Actividad | Resultado esperado |
|---|---|
| Revisión final de evidencias | Confirmar cumplimiento de criterios de aceptación. |
| Cierre de gaps | Resolver o planificar pendientes. |
| Retirada ordenada del equipo saliente | Reducir o finalizar soporte. |
| Informe final de transición | Estado, riesgos, recomendaciones, deuda técnica. |
| Plan de estabilización | Seguimiento durante primeras semanas de operación autónoma. |
| Plan de mejora continua | Automatización, documentación, observabilidad, deuda técnica. |

### Alineamiento ITIL de la fase

**Prácticas ITIL relacionadas:**

- Continual Improvement.
- Problem Management.
- Measurement and Reporting.
- Service Level Management.
- Knowledge Management.
- Risk Management.

**Aplicación en la fase:**

Esta fase consolida la operación, valida el cumplimiento de niveles de servicio, cierra riesgos de transición, formaliza lecciones aprendidas y genera un backlog de mejora continua para la etapa BAU.

**Evidencias ITIL esperadas:**

- Acta de cierre de transición.
- Informe final de evidencias.
- Riesgos residuales aceptados o planificados.
- Backlog de mejora continua.
- KPIs de transición y estabilización.
- Documentación final validada.
- Plan de estabilización post-transición.

### Criterios de salida

La transición puede darse por cerrada cuando:

- Hay aceptación formal del cliente.
- El equipo entrante opera autónomamente.
- Los SLAs se cumplen.
- La documentación mínima está completa.
- Los accesos están regularizados.
- Los riesgos residuales están aceptados.
- Hay plan de mejora post-transición.

---

# 5. Checklist detallado por área

## 5.1 Inventario y documentación de aplicaciones

| Ítem | Preguntas clave | Evidencia esperada | Estado |
|---|---|---|---|
| Inventario completo | ¿Qué aplicaciones forman parte del contrato? | Lista validada por cliente. | Pendiente / En curso / Validado |
| Nombre oficial y alias | ¿Se usan distintos nombres para la misma aplicación? | Ficha de aplicación. |  |
| Propietario funcional | ¿Quién decide funcionalmente sobre la aplicación? | Contacto registrado. |  |
| Propietario técnico | ¿Quién conoce el código y la operación? | Contacto registrado. |  |
| Criticidad | ¿Qué impacto tiene una caída? | Clasificación alta/media/baja. |  |
| Usuarios | ¿Quién usa la aplicación? | Internos, clientes, mediadores, terceros. |  |
| Documentación funcional | ¿Existe y está actualizada? | Link y fecha de revisión. |  |
| Documentación técnica | ¿Existe arquitectura, despliegue, operación? | Link y fecha de revisión. |  |
| Manuales operativos | ¿Hay runbooks? | Runbook por aplicación. |  |
| Histórico de cambios | ¿Dónde se consultan evolutivos y decisiones? | Jira, ALM, Confluence, SharePoint, Git. |  |
| Obsolescencia | ¿Hay componentes fuera de soporte? | Informe de riesgos técnicos. |  |

---

## 5.2 Arquitectura técnica y dependencias

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Diagrama de alto nivel | ¿Cómo encaja la aplicación en el ecosistema? | Diagrama validado. |
| Diagrama de componentes | ¿Qué servicios, módulos y procesos la componen? | Diagrama técnico. |
| Flujo de datos | ¿Qué datos entran, se transforman y salen? | Diagrama de flujo. |
| Dependencias internas | ¿Qué otros sistemas necesita? | Matriz de dependencias. |
| Dependencias externas | ¿Qué proveedores o servicios externos usa? | Lista de terceros. |
| Protocolos | ¿REST, SOAP, MQ, SFTP, batch, eventos? | Inventario técnico. |
| Certificados | ¿Qué certificados usa y cuándo caducan? | Registro de certificados. |
| Librerías críticas | ¿Qué librerías son sensibles u obsoletas? | SBOM o inventario de dependencias. |
| Jobs y procesos batch | ¿Qué procesos programados existen? | Calendario batch. |
| Single points of failure | ¿Qué componentes no tienen redundancia? | Registro de riesgos. |

---

## 5.3 Entornos

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Desarrollo | ¿Existe entorno local o compartido? | Guía de configuración. |
| Integración | ¿Dónde se integran cambios? | URL, accesos, despliegue. |
| UAT / Preproducción | ¿Quién valida? ¿Con qué datos? | Procedimiento de validación. |
| Producción | ¿Quién accede y bajo qué controles? | Matriz de accesos. |
| DR / Contingencia | ¿Existe entorno de recuperación? | Documentación DR. |
| Paridad de entornos | ¿PRE se parece realmente a PRO? | Análisis de diferencias. |
| Datos de prueba | ¿Son anonimizados? | Evidencia de anonimización. |
| Configuración | ¿Dónde están las variables por entorno? | Inventario de configuración. |
| Ventanas de despliegue | ¿Cuándo se puede desplegar? | Calendario operativo. |
| Restricciones | ¿Hay congelaciones por cierre, campañas o auditorías? | Calendario de restricciones. |

---

## 5.4 Accesos, credenciales y gestión de secretos

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Usuarios nominales | ¿Cada persona tiene usuario propio? | Matriz de usuarios. |
| Usuarios técnicos | ¿Qué cuentas de servicio existen? | Inventario de cuentas técnicas. |
| Privilegios | ¿Se aplica mínimo privilegio? | Matriz rol/permiso. |
| MFA | ¿Está activado donde corresponde? | Evidencia de configuración. |
| Secretos | ¿Dónde se guardan contraseñas, tokens y claves? | Vault, Key Vault, Secrets Manager, etc. |
| Rotación | ¿Cada cuánto se rotan secretos? | Procedimiento documentado. |
| Caducidades | ¿Qué certificados o claves caducan pronto? | Calendario de vencimientos. |
| Acceso a producción | ¿Quién puede acceder y cómo se audita? | Procedimiento de acceso PRO. |
| Baja de accesos salientes | ¿Cuándo se revocan los accesos del proveedor anterior? | Plan de retirada. |
| Segregación de funciones | ¿Quien desarrolla puede desplegar en PRO? | Modelo de control aprobado. |

---

## 5.5 Repositorios de código fuente y control de versiones

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Repositorios identificados | ¿Dónde está todo el código? | Lista de repositorios. |
| Branching model | ¿Gitflow, trunk-based, ramas por release? | Documento de estrategia. |
| Tags y releases | ¿Cómo se identifica lo desplegado? | Convención documentada. |
| Permisos | ¿Quién puede leer, escribir, aprobar? | Matriz de permisos. |
| Pull requests | ¿Hay revisión obligatoria? | Política de repositorio. |
| Hooks y calidad | ¿Hay linters, tests, análisis estático? | Configuración visible. |
| Dependencias | ¿Cómo se gestionan librerías? | Maven, npm, NuGet, Gradle, etc. |
| Artefactos binarios | ¿Dónde se almacenan? | Nexus, Artifactory, registry. |
| Código huérfano | ¿Hay repos sin propietario? | Registro de deuda. |
| Documentación técnica en repo | ¿README, build, run, deploy? | README actualizado. |

---

## 5.6 Pipelines de CI/CD y herramientas de despliegue

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Herramienta CI/CD | ¿Jenkins, GitLab, GitHub Actions, Azure DevOps, Bamboo? | Inventario. |
| Pipelines por aplicación | ¿Existe pipeline para build, test y deploy? | Link a pipeline. |
| Variables | ¿Dónde se gestionan variables de entorno? | Configuración documentada. |
| Secretos en pipeline | ¿Están protegidos? | Evidencia de uso de vault/secret store. |
| Gates de calidad | ¿Hay tests, análisis estático, seguridad? | Configuración del pipeline. |
| Aprobaciones | ¿Quién aprueba despliegues? | Flujo de aprobación. |
| Rollback | ¿Cómo se vuelve atrás? | Procedimiento probado. |
| Versionado de artefactos | ¿Qué versión se despliega? | Trazabilidad commit-release. |
| Despliegue manual | ¿Qué partes siguen siendo manuales? | Runbook. |
| Ventanas y congelaciones | ¿Cuándo se despliega? | Calendario. |

---

## 5.7 Bases de datos y gestión de datos

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Motores | ¿Oracle, SQL Server, DB2, PostgreSQL, MongoDB, etc.? | Inventario. |
| Esquemas | ¿Qué esquemas son usados por cada aplicación? | Matriz app/esquema. |
| Modelo de datos | ¿Existe modelo lógico o físico? | Diagramas o documentación. |
| Tablas críticas | ¿Dónde están pólizas, recibos, siniestros, clientes? | Catálogo de datos. |
| Jobs DB | ¿Hay procedimientos, triggers, packages? | Inventario técnico. |
| Volumetría | ¿Tamaño, crecimiento, particiones? | Métricas actuales. |
| Retención | ¿Cuánto tiempo se conservan datos? | Política de retención. |
| Datos personales | ¿Qué datos son sensibles? | Clasificación de datos. |
| Anonimización | ¿Los entornos no productivos usan datos reales? | Evidencia de enmascaramiento. |
| Migraciones | ¿Cómo se versionan cambios de BD? | Liquibase, Flyway, scripts controlados. |
| Backups | ¿Frecuencia, tipo, prueba de restore? | Procedimiento y evidencias. |

---

## 5.8 Integraciones con sistemas externos y APIs de terceros

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Sistemas internos | ¿Qué sistemas corporativos se consumen? | Matriz de integración. |
| Terceros | ¿Qué proveedores externos intervienen? | Lista de proveedores. |
| APIs | ¿REST, SOAP, GraphQL? | Contratos OpenAPI/WSDL. |
| Ficheros | ¿SFTP, carpetas compartidas, formatos? | Especificación de ficheros. |
| Mensajería | ¿MQ, Kafka, colas propietarias? | Topología y topics/colas. |
| Autenticación | ¿OAuth, certificados, API keys, basic auth? | Documentación de seguridad. |
| Límites | ¿Hay rate limits o ventanas horarias? | Acuerdos técnicos. |
| Errores | ¿Qué códigos de error son frecuentes? | Catálogo de errores. |
| Reprocesos | ¿Cómo se reprocesan mensajes o ficheros fallidos? | Runbook. |
| Monitorización | ¿Cómo se detecta una integración caída? | Alertas y dashboards. |

En aseguradoras es especialmente importante revisar integraciones con:

- Bancos.
- Pasarelas de pago.
- Mediadores y corredores.
- Plataformas documentales.
- Firma electrónica.
- Sistemas antifraude.
- Sistemas de scoring o tarificación.
- Servicios de comunicaciones: email, SMS, notificaciones.
- Reguladores o reporting supervisor.
- Sistemas contables y financieros.
- Sistemas de Data Warehouse / BI.
- Sistemas legacy o mainframe.

---

## 5.9 Monitorización, alertas y gestión de logs

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Herramientas | ¿Dynatrace, Splunk, ELK, Grafana, Prometheus, AppInsights? | Inventario. |
| Dashboards | ¿Existen dashboards por aplicación? | Links. |
| Alertas | ¿Qué alertas están configuradas? | Catálogo de alertas. |
| Umbrales | ¿Los umbrales son correctos? | Validación técnica. |
| Logs | ¿Dónde se consultan? | Guía de consulta. |
| Correlación | ¿Hay correlation ID entre sistemas? | Evidencia técnica. |
| Trazabilidad funcional | ¿Se puede seguir una póliza, recibo o siniestro? | Procedimiento de diagnóstico. |
| Retención de logs | ¿Cuánto tiempo se conservan? | Política definida. |
| Alert fatigue | ¿Hay demasiadas falsas alarmas? | Análisis de calidad. |
| On-call | ¿Quién recibe alertas fuera de horario? | Procedimiento de guardia. |

---

## 5.10 Backup y recuperación ante desastres

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Política de backup | ¿Qué se respalda y con qué frecuencia? | Documento aprobado. |
| RPO | ¿Cuánta pérdida de datos es tolerable? | Valor por sistema. |
| RTO | ¿En cuánto tiempo debe recuperarse? | Valor por sistema. |
| Restore probado | ¿Cuándo se probó la última restauración? | Evidencia de prueba. |
| DRP | ¿Existe plan de recuperación ante desastre? | Documento DRP. |
| BCP | ¿Existe continuidad de negocio? | Documento BCP. |
| Dependencias DR | ¿Terceros y sistemas externos participan? | Matriz de dependencias. |
| Simulacros | ¿Se hacen pruebas periódicas? | Actas de simulacro. |
| Orden de recuperación | ¿Qué sistemas se levantan primero? | Secuencia documentada. |
| Responsables | ¿Quién decide activar contingencia? | Matriz de escalado. |

---

## 5.11 SLAs, SLOs y métricas actuales

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| SLAs contractuales | ¿Qué niveles de servicio están comprometidos? | Contrato o anexo operativo. |
| SLOs internos | ¿Qué objetivos técnicos se monitorizan? | Catálogo de SLOs. |
| Disponibilidad | ¿Cuál es la disponibilidad real? | Histórico mensual. |
| Rendimiento | ¿Tiempos medios de respuesta? | Métricas APM. |
| Incidencias | ¿Volumen por severidad? | Histórico ITSM. |
| Tiempo de resolución | ¿MTTR por tipo de incidencia? | Informe operativo. |
| Tiempo de detección | ¿MTTD? | Informe de monitorización. |
| Cambios fallidos | ¿Qué porcentaje de despliegues falla? | Métrica DevOps. |
| Volumen batch | ¿Cuánto duran procesos críticos? | Histórico batch. |
| Picos de negocio | ¿Cuándo se tensionan los sistemas? | Calendario y métricas. |

---

## 5.12 Gestión de incidencias y tickets históricos

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Herramienta ITSM | ¿ServiceNow, Jira Service Management, Remedy, HP SM? | Acceso y documentación. |
| Tipología | ¿Incidente, problema, cambio, petición? | Catálogo. |
| Severidades | ¿Cómo se clasifican P1, P2, P3? | Procedimiento. |
| Histórico | ¿Qué incidencias se han repetido? | Extracción últimos 12-24 meses. |
| Problemas abiertos | ¿Hay problem records sin cerrar? | Lista priorizada. |
| Workarounds | ¿Qué soluciones temporales existen? | Base de conocimiento. |
| Escalado | ¿A quién se escala por tipo de problema? | Matriz de escalado. |
| Comunicación | ¿Cómo se informa a negocio y usuarios? | Plantillas. |
| Postmortems | ¿Se hacen análisis causa raíz? | Ejemplos. |
| Tickets regulatorios | ¿Hay incidencias reportables? | Registro específico. |

---

## 5.13 Documentación funcional y de negocio

Esta área es especialmente crítica en seguros porque muchas reglas no están en el código de forma evidente, sino en normativa, producto, contratos, anexos, decisiones históricas o prácticas operativas.

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Catálogo de productos | ¿Qué productos soporta cada aplicación? | Inventario producto/app. |
| Ramos | ¿Vida, no vida, salud, autos, hogar, empresas? | Clasificación. |
| Reglas de suscripción | ¿Qué riesgos se aceptan o rechazan? | Documentación funcional. |
| Reglas de tarificación | ¿Dónde están tarifas, descuentos y recargos? | Especificación o motor de reglas. |
| Estados de póliza | ¿Qué estados existen y qué implican? | Diagrama de estados. |
| Estados de recibo | ¿Emitido, cobrado, devuelto, anulado? | Diagrama de estados. |
| Estados de siniestro | ¿Abierto, pendiente, cerrado, reabierto? | Diagrama. |
| Documentación contractual | ¿Qué documentos se generan? | Catálogo documental. |
| Comunicaciones | ¿Qué cartas, emails o SMS se envían? | Catálogo de comunicaciones. |
| Reglas contables | ¿Qué procesos impactan contabilidad? | Mapa funcional. |
| Excepciones operativas | ¿Qué casos especiales existen? | Base de conocimiento. |

---

## 5.14 Cumplimiento normativo y regulatorio

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| GDPR | ¿Qué datos personales trata cada aplicación? | Registro de tratamientos. |
| Base legal | ¿Consentimiento, contrato, obligación legal? | Documentación DPO/legal. |
| Derechos ARSOPL | ¿Cómo se atienden acceso, rectificación, supresión, oposición, portabilidad, limitación? | Procedimiento. |
| Minimización | ¿Se recogen solo datos necesarios? | Revisión funcional. |
| Retención | ¿Cuándo se eliminan o anonimizan datos? | Política aplicada. |
| Auditoría | ¿Qué trazas deben conservarse? | Política de logging. |
| Segregación de funciones | ¿Hay controles de acceso adecuados? | Matriz SoD. |
| Cifrado | ¿Datos cifrados en tránsito y reposo? | Evidencias técnicas. |
| DORA / resiliencia | ¿Hay requisitos de resiliencia operacional digital? | Planes y evidencias. |
| Outsourcing | ¿El contrato exige controles específicos al proveedor? | Cláusulas y procedimientos. |
| Auditorías | ¿Qué auditorías están planificadas o abiertas? | Calendario de auditorías. |
| Incidentes de seguridad | ¿Cómo se notifican y escalan? | Procedimiento. |

---

## 5.15 Contratos con proveedores y licencias

| Ítem | Preguntas clave | Evidencia esperada |
|---|---|---|
| Proveedores críticos | ¿Qué terceros soportan sistemas clave? | Inventario. |
| Contratos vigentes | ¿Qué cubre cada contrato? | Resumen contractual. |
| SLAs de terceros | ¿Qué compromisos tienen? | Anexo de servicio. |
| Soporte | ¿Cómo se abre ticket al proveedor? | Procedimiento. |
| Licencias | ¿Qué software requiere licencia? | Inventario de licencias. |
| Caducidades | ¿Cuándo vencen contratos/licencias? | Calendario. |
| Costes | ¿Hay costes por uso, volumen o usuarios? | Modelo de costes. |
| Restricciones | ¿Hay limitaciones de uso o transferencia? | Revisión contractual. |
| Escalado proveedor | ¿Contactos técnicos/comerciales? | Matriz de contactos. |
| Software sin soporte | ¿Hay versiones EOL? | Registro de riesgos. |

---

## 5.16 Contactos clave y escalado

| Rol / contacto | Información necesaria |
|---|---|
| Responsable de negocio | Nombre, área, email, teléfono, horario, sustituto. |
| Product owner | Aplicaciones o productos bajo su responsabilidad. |
| Responsable técnico saliente | Dominio, nivel de conocimiento, disponibilidad. |
| Arquitecto | Sistemas cubiertos, decisiones pendientes. |
| Operaciones / Infraestructura | Servidores, redes, certificados, middleware. |
| Seguridad | Accesos, vulnerabilidades, incidentes. |
| DPO / legal | Protección de datos, auditorías, reporting. |
| Proveedores terceros | Soporte, escalado, SLAs. |
| Mesa de servicio | Canal de entrada, severidades, escalado. |
| Dirección cliente | Escalado ejecutivo. |

---

## 5.17 Preparación operativa alineada con ITIL

Esta checklist resume los elementos mínimos que permiten considerar que una aplicación o servicio está preparado para ser asumido desde una perspectiva ITIL.

| Categoría | Pregunta clave | Evidencia esperada | Estado |
|---|---|---|---|
| Conocimiento funcional | ¿El equipo entrante entiende el proceso de negocio soportado? | Mapa funcional, reglas críticas y validación con negocio. | Pendiente / En curso / Validado |
| Conocimiento técnico | ¿El equipo entrante entiende arquitectura, código, datos e integraciones? | Diagramas, walkthrough técnico y documentación validada. |  |
| Configuración del servicio | ¿Están identificados los CIs principales? | Mini-CMDB o registro de configuración. |  |
| Gestión de incidencias | ¿Se conoce el proceso de diagnóstico, escalado, comunicación y cierre? | Runbook, tickets históricos y evidencias de shadowing. |  |
| Gestión de problemas | ¿Están identificados problemas recurrentes y workarounds? | Registro de problemas conocidos. |  |
| Gestión de cambios | ¿Se conoce cómo se solicitan, aprueban y ejecutan cambios? | Procedimiento de cambios y evidencias de cambios reales. |  |
| Releases y despliegues | ¿Se puede desplegar y revertir con seguridad? | Procedimiento de despliegue, rollback y evidencias. |  |
| Monitorización | ¿Se conocen dashboards, alertas, logs y eventos relevantes? | Catálogo de alertas y guía de diagnóstico. |  |
| Seguridad | ¿Accesos, secretos, certificados y permisos están controlados? | Matriz de accesos, inventario de secretos y certificados. |  |
| Proveedores | ¿Se conocen terceros, contratos, SLAs y escalados? | Registro de proveedores y contactos. |  |
| Niveles de servicio | ¿Se conocen SLAs, OLAs e indicadores de operación? | Catálogo de SLAs/OLAs y métricas actuales. |  |
| Continuidad | ¿Se conocen backup, restore, RTO, RPO y DRP? | Procedimientos y evidencias de pruebas. |  |
| Mejora continua | ¿Se han registrado oportunidades de mejora? | Backlog de mejora continua. |  |

---

# 6. Riesgos principales y estrategias de mitigación

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---:|---:|---|
| Inventario incompleto | Alto | Alta | Cruce de fuentes: CMDB, repositorios, ITSM, monitorización, entrevistas, pipelines y facturación. |
| Documentación obsoleta | Alto | Alta | Validar documentación contra código, despliegues, tickets y sesiones con expertos. |
| Dependencia de personas clave | Alto | Alta | Identificar SMEs, grabar sesiones si se permite, documentar procedimientos, hacer reverse shadowing. |
| Accesos incompletos o tardíos | Alto | Media | Plan de accesos desde fase 0, matriz por rol, seguimiento semanal. |
| Secretos mal gestionados | Alto | Media | Migrar a gestor de secretos, rotar credenciales, eliminar secretos en código. |
| Desconocimiento funcional | Alto | Alta | Sesiones por proceso de negocio, mapas funcionales, revisión de tickets y validación con negocio. |
| Incidencias críticas durante transición | Alto | Media | Modelo de soporte dual, war room, escalado claro, runbooks mínimos. |
| Despliegues no reproducibles | Alto | Media | Documentar CI/CD, realizar despliegues supervisados, probar rollback. |
| Falta de entornos equivalentes | Medio/Alto | Alta | Identificar diferencias PRE/PRO, ajustar validaciones y datos de prueba. |
| Dependencias externas no controladas | Alto | Media | Inventario de terceros, contactos, SLAs, certificados, contratos y procedimientos. |
| Datos sensibles en entornos no productivos | Alto | Media | Revisión GDPR, anonimización, controles de acceso. |
| Falta de trazabilidad regulatoria | Alto | Media | Revisar auditoría, logs, retención, evidencias y controles. |
| Deuda técnica severa | Medio/Alto | Alta | Registrar como riesgo, priorizar remediaciones críticas, no mezclar transición con grandes refactorizaciones salvo urgencia. |
| Conocimiento tácito no transferido | Alto | Alta | Shadowing, reverse shadowing, análisis de tickets, sesiones de preguntas abiertas. |
| Cambios de alcance durante transición | Medio | Alta | Backlog controlado, comité de cambios, priorización por criticidad. |
| Resistencia del proveedor saliente | Alto | Media | Gobierno contractual, actas, entregables claros, escalado ejecutivo. |
| Métricas de servicio no fiables | Medio | Media | Reconstruir baseline con ITSM, APM y logs. |
| Falta de aceptación clara | Alto | Media | Criterios de aceptación definidos desde el inicio y evidencias por aplicación. |
| Transición no alineada con procesos ITSM | Medio/Alto | Media | Mapear prácticas ITIL aplicables, integrar evidencias y validar criterios de salida por fase. |
| Cambios no controlados durante la transición | Alto | Media | Aplicar política específica de Change Enablement, registrar cambios y revisar impacto documental. |
| SLAs/OLAs no conocidos por el equipo entrante | Alto | Media | Incorporar Service Level Management desde fase 0 y validar catálogo de niveles de servicio. |
| Proveedores críticos sin modelo de escalado | Alto | Media | Crear registro de proveedores, contactos operativos, SLAs y canales de soporte. |

---

# 7. Modelo de gobierno de la transición

## 7.1 Roles principales

| Rol | Responsabilidades |
|---|---|
| Sponsor del cliente | Resolver bloqueos ejecutivos, validar objetivos y prioridades. |
| Responsable de transición cliente | Coordinar áreas internas, validar entregables, facilitar accesos. |
| Transition Manager proveedor entrante | Liderar el plan, seguimiento, riesgos, dependencias y reporting. |
| Líder técnico entrante | Coordinar transferencia técnica, arquitectura, repositorios, despliegues. |
| Líder funcional entrante | Coordinar transferencia funcional, procesos de negocio y reglas críticas. |
| Service Manager entrante | Preparar operación BAU, SLAs, ITSM, reporting y soporte. |
| Equipo saliente | Transferir conocimiento, validar reverse shadowing, entregar documentación. |
| Arquitectura cliente | Validar arquitectura, estándares, deuda técnica y roadmap. |
| Seguridad / IAM | Gestionar accesos, secretos, auditoría y cumplimiento. |
| DPO / Legal / Compliance | Validar GDPR, auditorías, normativa sectorial y outsourcing. |
| Operaciones / Infraestructura | Entornos, monitorización, backups, DR, despliegues. |
| Negocio | Validar procesos funcionales y criticidad. |

---

## 7.2 RACI resumido

| Actividad | Cliente | Proveedor saliente | Proveedor entrante |
|---|---|---|---|
| Definir alcance | A/R | C | C |
| Planificar transición | A | C | R |
| Entregar documentación | C | R | C |
| Validar documentación | A | C | R |
| Transferir conocimiento | C | R | R |
| Habilitar accesos | A/R | C | C |
| Inventariar aplicaciones | A | R | R |
| Documentar arquitectura | C | R | R |
| Ejecutar shadowing | C | R | R |
| Ejecutar reverse shadowing | C | C | R |
| Validar autonomía | A | C | R |
| Cerrar transición | A | C | R |

Leyenda:  

- **R** = Responsible, ejecuta.
- **A** = Accountable, responsable último.
- **C** = Consulted, consultado.

---

## 7.3 Reuniones recomendadas

| Reunión | Frecuencia | Participantes | Objetivo |
|---|---:|---|---|
| Comité ejecutivo de transición | Quincenal o mensual | Sponsors, dirección, responsables transición | Riesgos mayores, decisiones, bloqueos. |
| Comité operativo de transición | Semanal | Transition Manager, cliente, saliente, entrante | Seguimiento de plan, hitos, riesgos, dependencias. |
| Daily de transición | Diario o 3 veces/semana | Equipo operativo entrante y saliente | Coordinación de sesiones, dudas, incidencias. |
| Sesiones funcionales | Según plan | SMEs negocio, funcionales, equipo entrante | Transferencia por proceso. |
| Sesiones técnicas | Según plan | Técnicos salientes, entrantes, arquitectura | Transferencia técnica. |
| Revisión de accesos | Semanal | Seguridad, IAM, líderes técnicos | Seguimiento de permisos. |
| Revisión de riesgos | Semanal | Transition Manager y responsables | Actualizar riesgos y mitigaciones. |
| Go / No-Go por aplicación | Por hito | Cliente, saliente, entrante | Decidir avance a siguiente fase. |
| Cierre de transición | Final | Todos los responsables | Validación formal. |

---

## 7.4 Herramientas recomendadas

| Necesidad | Herramienta típica |
|---|---|
| Backlog de transición | Jira, Azure DevOps, Planner, Monday, ServiceNow. |
| Documentación | Confluence, SharePoint, Git, Markdown, Wiki corporativa. |
| Inventario / CMDB | ServiceNow CMDB, Excel controlado, herramienta corporativa. |
| Diagramas | Draw.io, Lucidchart, Visio, PlantUML, Mermaid. |
| Repositorios | GitHub Enterprise, GitLab, Bitbucket, Azure Repos. |
| CI/CD | Jenkins, Azure DevOps, GitHub Actions, GitLab CI, Bamboo. |
| ITSM | ServiceNow, Jira Service Management, Remedy. |
| Observabilidad | Dynatrace, Splunk, ELK, Grafana, Prometheus, AppInsights. |
| Riesgos y decisiones | RAID log: Risks, Assumptions, Issues, Dependencies. |
| Evidencias de aceptación | Carpeta de transición por aplicación. |

---

## 7.5 Gobierno ITIL de la transición

Además del gobierno general del proyecto, se recomienda incorporar una capa de gobierno ITIL orientada a asegurar que la transición preserva la continuidad y calidad del servicio.

| Elemento de gobierno | Aplicación práctica |
|---|---|
| Gestión del conocimiento | Revisar el estado de documentación, runbooks, FAQs, decisiones y lecciones aprendidas. |
| Gestión de configuración | Mantener actualizado el inventario de servicios, aplicaciones, CIs, entornos e integraciones. |
| Gestión de cambios | Revisar cambios relevantes durante la transición y su impacto sobre documentación, operación y riesgos. |
| Gestión de incidencias | Analizar incidencias observadas y gestionadas por el equipo entrante durante shadowing y reverse shadowing. |
| Gestión de problemas | Registrar causas recurrentes, workarounds y deuda operativa. |
| Gestión de niveles de servicio | Monitorizar SLAs y OLAs durante transición, asunción progresiva y estabilización. |
| Gestión de proveedores | Revisar dependencias con terceros, escalados y contratos relevantes. |
| Mejora continua | Consolidar oportunidades de mejora detectadas durante la transición. |

Este gobierno debe apoyarse en evidencias y no solo en percepciones. Cada decisión de avance entre fases debe quedar soportada por entregables revisados, riesgos actualizados y criterios de salida aceptados.

---

# 8. Artefactos operativos recomendados

Para que la transición sea gestionable, conviene crear un conjunto estándar de artefactos.

## 8.1 Matriz de aplicaciones

Columnas recomendadas:

- Código aplicación.
- Nombre.
- Dominio funcional.
- Criticidad.
- Tecnología.
- Responsable saliente.
- Responsable entrante.
- Responsable negocio.
- Repositorio.
- Entornos.
- Base de datos.
- Integraciones principales.
- Documentación funcional.
- Documentación técnica.
- Estado de accesos.
- Estado de transferencia funcional.
- Estado de transferencia técnica.
- Estado de shadowing.
- Estado de reverse shadowing.
- Riesgos abiertos.
- Estado final.

---

## 8.2 RAID log

| Tipo | Descripción | Impacto | Responsable | Fecha objetivo | Estado |
|---|---|---:|---|---|---|
| Risk | Riesgo potencial. | Alto/Medio/Bajo | Nombre | Fecha | Abierto |
| Assumption | Supuesto pendiente de validar. | Alto/Medio/Bajo | Nombre | Fecha | En validación |
| Issue | Problema ya ocurrido. | Alto/Medio/Bajo | Nombre | Fecha | En curso |
| Dependency | Dependencia externa. | Alto/Medio/Bajo | Nombre | Fecha | Pendiente |

---

## 8.3 Runbook mínimo por aplicación

Cada aplicación crítica debería tener un runbook con:

- Descripción funcional.
- Arquitectura resumida.
- URLs y endpoints.
- Entornos.
- Repositorios.
- Procedimiento de build.
- Procedimiento de despliegue.
- Procedimiento de rollback.
- Logs principales.
- Dashboards.
- Alertas.
- Jobs y procesos batch.
- Dependencias.
- Incidencias frecuentes.
- Workarounds conocidos.
- Contactos de escalado.
- Procedimiento de recuperación.
- Riesgos conocidos.

---

## 8.4 Matriz de criticidad

| Criterio | Bajo | Medio | Alto | Crítico |
|---|---|---|---|---|
| Impacto cliente | Sin impacto externo | Impacto limitado | Impacto a muchos clientes | Bloqueo generalizado |
| Impacto económico | Bajo | Moderado | Alto | Muy alto |
| Impacto regulatorio | Nulo | Bajo | Alto | Reportable / sancionable |
| Disponibilidad requerida | Horario laboral | Ampliado | 24x5 | 24x7 |
| Alternativa manual | Existe fácilmente | Existe con esfuerzo | Muy limitada | No existe |
| Dependencias | Aislada | Algunas | Muchas | Nodo central |

---

## 8.5 Registro mínimo de configuración del servicio

Este registro actúa como una mini-CMDB operativa para la transición. No pretende sustituir a la CMDB corporativa, pero sí asegurar que el equipo entrante dispone de una visión fiable de los elementos relevantes del servicio.

| Campo | Descripción |
|---|---|
| Código de servicio | Identificador único del servicio o dominio. |
| Servicio de negocio | Servicio funcional soportado. |
| Aplicación o componente | Aplicación, módulo, microservicio, batch o componente técnico. |
| Criticidad | Baja, media, alta o crítica. |
| Tecnología | Stack tecnológico principal. |
| Entorno | DEV, INT, UAT, PRE, PRO, DR. |
| Repositorio | Ubicación del código fuente o artefactos. |
| Base de datos | BBDD, esquema o repositorio de datos asociado. |
| Integraciones | Sistemas internos o externos conectados. |
| Jobs | Procesos batch o planificados. |
| Monitorización | Herramientas, dashboards y alertas asociadas. |
| Responsable funcional | Área o persona responsable. |
| Responsable técnico | Equipo o persona responsable. |
| Proveedor | Tercero implicado, si aplica. |
| Documentación asociada | Enlaces a documentación funcional, técnica y operativa. |
| Riesgos conocidos | Riesgos técnicos, funcionales, regulatorios u operativos. |
| Estado de validación | Pendiente, revisado, validado, asumido o bloqueado. |

## 8.6 Registro de mejora continua

Durante todo el proceso de transición se deberá alimentar un registro de mejora continua que permita separar la asunción del servicio de las acciones posteriores de estabilización, automatización y optimización.

| ID | Mejora | Origen | Beneficio esperado | Prioridad | Esfuerzo | Responsable | Estado |
|---|---|---|---|---|---|---|---|
| MC-001 |  | Shadowing / Incidencia / Riesgo / Cliente / Auditoría |  | Alta / Media / Baja | Bajo / Medio / Alto |  | Propuesta / Aprobada / En curso / Implantada |

---

# 9. Criterios de aceptación final

La aceptación final debe basarse en evidencias. Conviene establecer criterios por aplicación y criterios globales.

## 9.1 Criterios por aplicación

Una aplicación se puede considerar transferida cuando:

| Criterio | Evidencia |
|---|---|
| Inventario completo | Ficha de aplicación completada y validada. |
| Documentación funcional mínima | Procesos, reglas críticas y usuarios documentados. |
| Documentación técnica mínima | Arquitectura, componentes, dependencias y despliegue documentados. |
| Accesos disponibles | Equipo entrante tiene accesos necesarios y auditados. |
| Repositorio validado | Código localizado, permisos correctos y estrategia de ramas entendida. |
| Build reproducible | El equipo entrante puede compilar o generar artefactos. |
| Despliegue conocido | Procedimiento probado en entorno no productivo o supervisado. |
| Rollback conocido | Procedimiento documentado y, si es posible, probado. |
| Logs localizados | Equipo sabe diagnosticar errores básicos. |
| Monitorización conocida | Dashboards y alertas identificados. |
| Datos conocidos | BD, tablas críticas y procedimientos identificados. |
| Integraciones conocidas | Sistemas consumidores/proveedores documentados. |
| Incidencias frecuentes conocidas | Workarounds y causas habituales documentadas. |
| Shadowing realizado | Evidencia de sesiones observadas. |
| Reverse shadowing realizado | Evidencia de operación por equipo entrante. |
| Riesgos documentados | Riesgos residuales aceptados o con plan. |

---

## 9.2 Criterios globales de transición

La transición completa puede aceptarse cuando:

- El inventario de aplicaciones está validado.
- El 100% de aplicaciones críticas tiene runbook mínimo.
- El 100% de aplicaciones críticas tiene responsable entrante asignado.
- Los accesos operativos están concedidos y auditados.
- Los accesos del proveedor saliente tienen plan de retirada.
- El equipo entrante ha gestionado incidencias reales o simuladas.
- El equipo entrante ha ejecutado despliegues supervisados.
- Los SLAs se han mantenido durante el período de transición o estabilización.
- Los riesgos críticos están cerrados o aceptados formalmente.
- Los procesos de escalado están documentados.
- Los contactos clave están actualizados.
- La documentación está centralizada.
- Hay modelo BAU definido tras la transición.
- El cliente firma aceptación formal.
- Existe evidencia de preparación operativa alineada con ITIL.
- Se ha validado el registro mínimo de configuración del servicio.
- Se ha consolidado un backlog de mejora continua.
- Se han identificado riesgos residuales y aceptaciones explícitas.

---

# 10. Recomendaciones específicas para el sector asegurador

## 10.1 Priorizar por criticidad de negocio asegurador

No todas las aplicaciones tienen el mismo riesgo. Conviene priorizar las que soportan:

1. Emisión de pólizas.
2. Cotización y tarificación.
3. Cobros y recibos.
4. Siniestros.
5. Renovaciones.
6. Documentación contractual.
7. Firma electrónica.
8. Mediadores y canales de venta.
9. Reporting financiero o regulatorio.
10. Data Warehouse con información crítica de negocio.

---

## 10.2 Validar especialmente la documentación contractual

En seguros, un error técnico puede tener consecuencias contractuales. Hay que revisar:

- Condiciones particulares.
- Condiciones generales.
- Condiciones especiales.
- Documentación precontractual.
- Cuestionarios de salud, riesgo o suscripción.
- IPID u otros documentos informativos.
- Consentimientos.
- Comunicaciones obligatorias.
- Versionado documental.
- Trazabilidad de qué documento se entregó a qué cliente y cuándo.

---

## 10.3 Controlar cambios en reglas de negocio

Las reglas de negocio pueden estar en lugares diferentes:

- Código.
- Base de datos.
- Motor de reglas.
- Tablas paramétricas.
- Excel cargados manualmente.
- Aplicaciones legacy.
- Procedimientos almacenados.
- Ficheros de configuración.
- Servicios externos de tarificación.

Durante la transición es crítico identificar:

- Quién puede modificar reglas.
- Cómo se aprueban.
- Cómo se prueban.
- Cómo se despliegan.
- Cómo se auditan.
- Cómo se revierte un cambio erróneo.

---

## 10.4 Revisar procesos batch y cierres

En aseguradoras, muchos procesos críticos son batch:

- Emisión masiva.
- Renovaciones.
- Generación de recibos.
- Remesas bancarias.
- Conciliación.
- Comisiones de mediadores.
- Reporting contable.
- Reporting regulatorio.
- Generación documental masiva.
- Carga a Data Warehouse.
- Procesos antifraude.

Para cada batch crítico debe existir:

- Calendario.
- Dependencias.
- Duración esperada.
- Logs.
- Alertas.
- Procedimiento de reinicio.
- Procedimiento de reproceso.
- Validaciones funcionales.
- Contacto de negocio.
- Impacto si falla.

---

## 10.5 GDPR y datos sensibles

Debe tratarse con especial cuidado:

- Datos identificativos.
- Datos de contacto.
- Datos bancarios.
- Datos de salud.
- Datos de beneficiarios.
- Datos de siniestros.
- Datos de menores.
- Datos financieros.
- Documentos adjuntos.
- Grabaciones o comunicaciones.

Recomendaciones:

- No usar datos productivos en entornos no productivos salvo autorización y enmascaramiento.
- Revisar permisos por rol.
- Controlar exportaciones a Excel, ficheros o herramientas de soporte.
- Auditar accesos a datos sensibles.
- Verificar retención de logs y documentos.
- Confirmar procedimientos ante brechas de seguridad.
- Revisar integraciones con terceros que procesen datos personales.

---

## 10.6 Trazabilidad de decisiones e incidencias

En seguros es importante poder reconstruir:

- Qué se cotizó.
- Qué tarifa se aplicó.
- Qué versión de producto estaba vigente.
- Qué documentación se entregó.
- Qué consentimiento dio el cliente.
- Qué usuario hizo una modificación.
- Qué sistema generó una comunicación.
- Qué cálculo produjo un recibo, prima, comisión o indemnización.
- Qué versión de código estaba desplegada.

Esta trazabilidad debe revisarse durante la transición.

---

## 10.7 Atención a sistemas legacy

Es frecuente que el stack asegurador combine aplicaciones modernas con sistemas legacy. Hay que prestar especial atención a:

- Mainframe.
- COBOL.
- Bases jerárquicas o propietarias.
- Procesos batch antiguos.
- Integraciones por fichero.
- Jobs con dependencias manuales.
- Conocimiento concentrado en pocas personas.
- Falta de entornos equivalentes.
- Documentación incompleta.

En estos casos, el shadowing y reverse shadowing son más importantes que la documentación formal.

---

# 11. Plan de trabajo práctico para las primeras semanas

## Semana 1: Arranque

- Kick-off ejecutivo.
- Kick-off operativo.
- Crear backlog de transición.
- Crear matriz de aplicaciones.
- Definir plantilla de ficha de aplicación.
- Definir RAID log.
- Definir calendario de sesiones.
- Solicitar accesos iniciales.
- Identificar aplicaciones críticas.

## Semanas 2-4: Inventario y priorización

- Completar inventario inicial.
- Clasificar criticidad.
- Mapear responsables.
- Revisar documentación existente.
- Identificar gaps.
- Priorizar aplicaciones críticas.
- Iniciar sesiones funcionales.
- Iniciar sesiones técnicas de alto nivel.

## Semanas 5-8: Transferencia funcional y técnica

- Profundizar por dominio.
- Revisar código, repositorios y pipelines.
- Revisar bases de datos e integraciones.
- Revisar monitorización y logs.
- Documentar runbooks.
- Revisar incidencias históricas.
- Validar accesos.
- Identificar riesgos críticos.

## Semanas 9-12: Shadowing

- Observar incidencias reales.
- Observar despliegues.
- Observar procesos batch.
- Participar en comités operativos.
- Documentar procedimientos tácitos.
- Actualizar runbooks.
- Ejecutar simulacros controlados.

## Semanas 13-16: Reverse shadowing

- Gestionar incidencias bajo supervisión.
- Ejecutar despliegues supervisados.
- Resolver consultas funcionales.
- Ejecutar tareas recurrentes.
- Probar rollback o recuperación donde sea viable.
- Validar autonomía por aplicación.

## Semanas 17 en adelante: Asunción y estabilización

- Asumir aplicaciones por oleadas.
- Medir cumplimiento de SLAs.
- Cerrar gaps críticos.
- Formalizar aceptación.
- Retirar soporte saliente gradualmente.
- Consolidar operación BAU.
- Lanzar plan de mejora continua.

---

# 12. Indicadores de seguimiento de la transición

| Indicador | Objetivo |
|---|---|
| % aplicaciones inventariadas | Medir avance de descubrimiento. |
| % aplicaciones con criticidad asignada | Priorizar correctamente. |
| % aplicaciones con ficha completa | Control documental. |
| % aplicaciones con runbook validado | Preparación operativa. |
| % accesos concedidos | Reducir bloqueos operativos. |
| % sesiones realizadas vs planificadas | Control de transferencia. |
| Nº gaps abiertos por criticidad | Gestión de riesgos. |
| Nº riesgos críticos abiertos | Seguimiento ejecutivo. |
| Nº incidencias observadas | Calidad del shadowing. |
| Nº incidencias gestionadas por equipo entrante | Autonomía real. |
| Nº despliegues supervisados ejecutados | Capacidad de cambio. |
| Cumplimiento SLA durante transición | Calidad de servicio. |
| % aplicaciones aceptadas | Progreso hacia cierre. |
| % aplicaciones con preparación operativa validada | Asegurar readiness antes de asunción. |
| % aplicaciones con registro de configuración completo | Controlar cobertura de mini-CMDB. |
| Nº problemas recurrentes identificados | Alimentar Problem Management. |
| Nº mejoras registradas | Activar mejora continua post-transición. |
| % proveedores críticos con escalado validado | Reducir riesgo de dependencia externa. |

---

# 13. Decisiones importantes que conviene tomar pronto

| Decisión | Por qué es importante |
|---|---|
| Orden de transición | Evita dispersión y permite concentrarse en lo crítico. |
| Nivel mínimo de documentación | Evita discusiones subjetivas sobre “suficiente conocimiento”. |
| Modelo de acceso a producción | Reduce riesgos de seguridad y auditoría. |
| Modelo de guardias | Define responsabilidad real ante incidencias. |
| Estrategia de soporte dual | Evita vacío operativo entre proveedor saliente y entrante. |
| Criterios de aceptación | Permite cerrar formalmente sin ambigüedad. |
| Herramienta única de seguimiento | Evita pérdida de información. |
| Tratamiento de deuda técnica | Separa transición de transformación. |
| Gestión de cambios durante transición | Evita introducir riesgo adicional. |
| Plan de comunicación con negocio | Reduce incertidumbre y mejora confianza. |
| Prácticas ITIL mínimas a aplicar | Evita sobredimensionar la metodología y fija el nivel de control esperado. |
| Gate de salida por fase | Permite avanzar solo cuando existan evidencias suficientes. |
| Modelo de mejora continua post-transición | Asegura que los hallazgos no bloqueantes se gestionan tras la estabilización. |

---

# 14. Recomendación final de enfoque

Para que la transición sea segura, no la plantearía como un simple proyecto documental, sino como una **asunción progresiva de capacidad operativa**, gobernada con criterios ITIL, evidencias verificables y mejora continua.

El enfoque más fiable sería:

1. **Inventariar y clasificar.**
2. **Entender funcionalmente el negocio.**
3. **Entender técnicamente las aplicaciones.**
4. **Observar operación real.**
5. **Operar bajo supervisión.**
6. **Asumir por oleadas.**
7. **Cerrar con evidencias.**
8. **Validar preparación operativa alineada con ITIL.**
9. **Estabilizar y mejorar.**

La clave no es recibir muchos documentos, sino poder responder afirmativamente a esta pregunta:

> “Si mañana se produce una incidencia crítica en una aplicación relevante para emisión, cobros, siniestros o reporting regulatorio, ¿nuestro equipo sabe diagnosticarla, escalarla, comunicarla, resolverla o contenerla dentro de los SLAs comprometidos?”

Cuando la respuesta sea sí, con evidencias, la transición estará realmente completada.
