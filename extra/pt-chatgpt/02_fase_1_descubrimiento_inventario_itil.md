# Fase 1. Descubrimiento e inventario  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 1

La **Fase 1. Descubrimiento e inventario** tiene como objetivo construir una visión inicial, fiable y trazable del ecosistema de aplicaciones, componentes, datos, integraciones, entornos, equipos y dependencias que forman parte del servicio que va a ser transferido.

Esta fase es crítica porque el equipo entrante no puede asumir el mantenimiento de un stack que no conoce o cuyo perímetro no está claramente delimitado.

El objetivo no es todavía dominar técnicamente cada aplicación, sino responder con suficiente rigor a estas preguntas:

- ¿Qué aplicaciones forman parte del contrato?
- ¿Qué procesos de negocio soporta cada aplicación?
- ¿Qué componentes técnicos existen?
- ¿Qué aplicaciones son críticas?
- ¿Qué dependencias internas y externas existen?
- ¿Qué entornos hay?
- ¿Dónde está el código?
- ¿Dónde está la documentación?
- ¿Qué bases de datos intervienen?
- ¿Qué integraciones existen?
- ¿Qué herramientas operativas se utilizan?
- ¿Qué equipos o personas conocen cada sistema?
- ¿Qué riesgos de conocimiento, documentación o continuidad aparecen desde el inicio?

---

## 2. Resultado esperado de la Fase 1

Al finalizar esta fase, el equipo debe disponer de:

- Un **inventario inicial validado de aplicaciones**.
- Una **matriz aplicación / dominio funcional / criticidad**.
- Una **matriz de componentes técnicos**.
- Una **matriz de dependencias internas y externas**.
- Un **mapa inicial de entornos**.
- Una **matriz de repositorios y pipelines**.
- Una **matriz inicial de bases de datos y esquemas**.
- Una **matriz de integraciones**.
- Una **matriz de documentación existente y gaps documentales**.
- Una **identificación de responsables técnicos, funcionales y operativos**.
- Una **clasificación inicial de criticidad y prioridad de transferencia**.
- Una **lista de riesgos y gaps detectados**.
- Una **propuesta de oleadas para las siguientes fases de transferencia**.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **2 a 4 semanas**.

Puede ser más corta si:

- El cliente dispone de una CMDB fiable.
- El inventario contractual está actualizado.
- La documentación técnica está centralizada.
- El proveedor saliente colabora activamente.
- El número de aplicaciones es reducido.

Puede alargarse si:

- Hay sistemas legacy.
- Hay múltiples proveedores.
- Existen aplicaciones sin propietario claro.
- La documentación está dispersa.
- Hay integraciones no inventariadas.
- Hay aplicaciones críticas con conocimiento concentrado en pocas personas.
- No existe una correspondencia clara entre contrato, CMDB, repositorios y operación real.



---

## 3.1 Alineamiento ITIL específico de la Fase 1

La Fase 1 se alinea especialmente con las prácticas ITIL orientadas a conocer, estructurar y controlar los elementos que forman parte de un servicio. En esta fase, el inventario no debe entenderse como una simple lista de aplicaciones, sino como la base inicial de la configuración del servicio que permitirá gobernar la transición y preparar la operación futura.

El objetivo ITIL de esta fase es construir una visión suficientemente fiable del servicio para responder a cuatro preguntas fundamentales:

- ¿Qué elementos forman parte del servicio?
- ¿Cómo se relacionan entre sí?
- ¿Quién es responsable de cada elemento?
- ¿Qué nivel de confianza tenemos sobre la información recopilada?

### Prácticas ITIL relacionadas

| Práctica ITIL | Aplicación en la Fase 1 |
|---|---|
| **Service Configuration Management** | Identificar servicios, aplicaciones, componentes, entornos, integraciones, bases de datos, relaciones y dependencias. |
| **IT Asset Management** | Localizar activos tecnológicos, licencias, herramientas, certificados, plataformas y componentes sujetos a control. |
| **Architecture Management** | Relacionar aplicaciones, componentes, plataformas, datos, flujos e integraciones dentro de una visión de arquitectura. |
| **Knowledge Management** | Clasificar la documentación existente, detectar gaps y establecer el estado de validación del conocimiento recibido. |
| **Information Security Management** | Identificar datos sensibles, accesos, credenciales, certificados, restricciones de entorno y riesgos de seguridad. |
| **Supplier Management** | Identificar proveedores, terceros, contratos, niveles de soporte y dependencias externas. |
| **Service Level Management** | Relacionar aplicaciones y servicios con SLAs, criticidad, impacto de negocio y prioridades de transferencia. |
| **Risk Management** | Registrar riesgos asociados a inventario incompleto, dependencias desconocidas, documentación obsoleta o falta de propietarios. |

### Resultado ITIL esperado

Al finalizar la fase, el equipo deberá disponer de una primera versión de un **Registro de Configuración del Servicio**, equivalente a una mini-CMDB operativa de transición.

Este registro no tiene que sustituir a la CMDB corporativa, pero sí debe permitir gestionar la transición con trazabilidad suficiente, relacionando:

- Servicios de negocio.
- Aplicaciones.
- Componentes técnicos.
- Entornos.
- Repositorios.
- Pipelines.
- Bases de datos.
- Integraciones.
- Proveedores.
- Responsables.
- Documentación.
- SLAs.
- Riesgos.
- Estado de validación.

### Evidencias ITIL esperadas

- Registro inicial de configuración del servicio.
- Matriz de relaciones servicio / aplicación / componente.
- Matriz de dependencias internas y externas.
- Matriz de activos tecnológicos relevantes.
- Inventario de documentación con estado de validación.
- Inventario de proveedores y terceros.
- Mapa inicial de servicios críticos.
- Relación entre criticidad, SLAs y prioridad de transferencia.
- RAID log actualizado con riesgos de configuración, activos, seguridad y proveedores.

### Criterio ITIL de éxito de la fase

La Fase 1 estará correctamente alineada con ITIL cuando el inventario permita comprender no solo qué aplicaciones existen, sino también qué servicios soportan, de qué componentes dependen, qué activos intervienen, qué terceros participan, qué riesgos existen y qué evidencias soportan cada dato registrado.


---

# 4. Principios de trabajo de la Fase 1

## 4.1 No confiar en una única fuente

El inventario no debe construirse únicamente a partir de una lista contractual o una CMDB. Debe contrastarse con varias fuentes:

- Contrato.
- CMDB.
- Repositorios.
- Herramienta ITSM.
- Monitorización.
- Pipelines.
- Bases de datos.
- Herramientas de despliegue.
- Documentación.
- Entrevistas.
- Logs.
- Calendarios batch.
- Proveedores externos.
- Equipos de negocio.

## 4.2 Separar “identificado” de “validado”

Una aplicación puede estar identificada pero no validada. Por ejemplo, puede aparecer en la CMDB, pero no tener repositorio conocido, responsable actual ni uso confirmado.

Estados recomendados:

| Estado | Significado |
|---|---|
| Identificado | Aparece en alguna fuente, pero no ha sido contrastado. |
| En análisis | Se está recopilando información. |
| Validado | Cliente, equipo saliente o evidencias operativas confirman su existencia y uso. |
| Dudoso | Hay indicios contradictorios o incompletos. |
| Fuera de alcance | Se confirma que no forma parte del contrato o transición. |
| Pendiente de decisión | No está claro si entra o no en el alcance. |

## 4.3 No confundir aplicación con componente

En entornos empresariales es habitual mezclar términos. Durante el inventario conviene distinguir:

| Concepto | Ejemplo |
|---|---|
| Aplicación | Portal de mediadores. |
| Módulo funcional | Alta de póliza, consulta de cartera, emisión de recibos. |
| Servicio técnico | API de cotización, servicio de documentos, servicio de clientes. |
| Componente | Front Angular, backend Java, job batch, cola, base de datos. |
| Plataforma | Middleware, bus de integración, gestor documental, motor de reglas. |
| Producto asegurador | Auto, hogar, vida, salud, empresas. |
| Proceso de negocio | Cotización, emisión, renovación, siniestro, cobro. |



## 4.5 Construir una mini-CMDB de transición

Desde esta fase debe empezar a construirse un registro mínimo de configuración del servicio. No es necesario que tenga la complejidad de una CMDB corporativa completa, pero sí debe permitir relacionar aplicaciones, componentes, entornos, repositorios, integraciones, datos, proveedores y responsables.

El valor de este registro no está en acumular información, sino en permitir tomar decisiones de transición con datos verificables.

Campos mínimos recomendados:

| Bloque | Campos recomendados |
|---|---|
| Identificación | ID de servicio, nombre de aplicación, alias, código corporativo, estado de alcance. |
| Negocio | Servicio de negocio, dominio funcional, proceso soportado, criticidad, responsable de negocio. |
| Técnica | Componentes, tecnologías, repositorios, pipelines, bases de datos, entornos. |
| Operación | ITSM, monitorización, logs, alertas, runbooks, guardias, SLAs. |
| Seguridad | Datos sensibles, accesos requeridos, certificados, secretos, restricciones. |
| Proveedores | Terceros, contratos, soporte, contactos, SLAs externos. |
| Validación | Fuente del dato, evidencia, nivel de confianza, estado de validación, fecha de revisión. |


## 4.4 Registrar gaps desde el primer día

Todo hueco de información debe registrarse como gap, no dejarse para “cuando haya tiempo”.

Ejemplos de gaps:

- Aplicación sin responsable.
- Repositorio desconocido.
- Documentación obsoleta.
- Pipeline no identificado.
- Integración externa sin contrato localizado.
- Base de datos sin modelo conocido.
- Job batch crítico sin runbook.
- Aplicación en producción no incluida en la CMDB.
- Componente desplegado pero sin código localizado.

---

# 5. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Recopilación de fuentes e inventario bruto | Primera lista consolidada de aplicaciones y componentes. |
| Semana 1-2 | Contraste con equipos y herramientas | Depuración de duplicados, alias y elementos dudosos. |
| Semana 2 | Clasificación funcional y técnica | Aplicaciones vinculadas a dominios, procesos y tecnologías. |
| Semana 2-3 | Identificación de dependencias | Matrices de integraciones, datos, entornos, repositorios y proveedores. |
| Semana 3 | Clasificación de criticidad | Priorización inicial por impacto negocio, técnico y regulatorio. |
| Semana 3-4 | Validación y cierre de inventario inicial | Inventario base aprobado para pasar a transferencia profunda. |

---

# 6. Actividad 1. Recopilar fuentes de información

## 6.1 Objetivo

Obtener todas las fuentes disponibles que puedan ayudar a reconstruir el mapa real del servicio.

## 6.2 Fuentes recomendadas

| Fuente | Información que puede aportar | Responsable habitual |
|---|---|---|
| Contrato / anexo de servicio | Alcance formal, SLAs, exclusiones, responsabilidades. | Cliente / gestión contractual. |
| CMDB | Aplicaciones, servidores, responsables, criticidad. | Operaciones / ITSM. |
| Portfolio de aplicaciones | Nombre funcional, área propietaria, estado. | Arquitectura / PMO. |
| ITSM | Incidencias, cambios, problemas, peticiones, responsables reales. | Service Manager. |
| Repositorios Git | Código fuente, actividad, tecnologías, ramas. | Líder técnico. |
| Herramientas CI/CD | Pipelines, despliegues, artefactos, entornos. | DevOps / arquitectura. |
| Herramientas de monitorización | Aplicaciones activas, hosts, servicios, alertas. | Operaciones. |
| Herramientas de logs | Componentes activos, errores recurrentes, trazabilidad. | Operaciones / soporte. |
| Bases de datos | Esquemas, conexiones, jobs, usuarios técnicos. | DBA. |
| Calendario batch | Procesos programados, dependencias, ventanas. | Operaciones batch. |
| Documentación funcional | Procesos de negocio, reglas, productos, usuarios. | Negocio / analistas. |
| Documentación técnica | Arquitectura, despliegues, integraciones. | Equipo saliente. |
| Inventario de proveedores | Terceros, contratos, soporte, SLAs. | Compras / gestión proveedores. |
| Seguridad / IAM | Accesos, cuentas técnicas, secretos, certificados. | Seguridad. |
| Auditoría / compliance | Sistemas regulados, evidencias, controles. | Auditoría / cumplimiento. |

## 6.3 Acciones concretas

- Solicitar al cliente el inventario contractual.
- Solicitar exportación de la CMDB.
- Solicitar listado de aplicaciones del portfolio corporativo.
- Solicitar extracción de tickets de los últimos 12-24 meses.
- Solicitar listado de repositorios relacionados.
- Solicitar listado de pipelines y jobs de despliegue.
- Solicitar listado de entornos y servidores.
- Solicitar listado de bases de datos y esquemas.
- Solicitar listado de APIs, colas, ficheros e integraciones.
- Solicitar listado de proveedores tecnológicos y funcionales.
- Solicitar documentación técnica y funcional existente.
- Solicitar calendario de procesos batch.
- Solicitar matriz de criticidad existente, si la hay.
- Solicitar matriz de contactos técnicos y funcionales.

## 6.4 Evidencias esperadas

- Ficheros exportados.
- Links a herramientas.
- Capturas o listados.
- Actas de entrega.
- Referencias a documentos existentes.
- Identificación del propietario de cada fuente.

## 6.5 Riesgos frecuentes

| Riesgo | Mitigación |
|---|---|
| Fuentes contradictorias | Mantener trazabilidad de origen y validar con expertos. |
| CMDB obsoleta | Contrastar con monitorización, ITSM y repositorios. |
| Repositorios sin correspondencia con aplicaciones | Crear mapeo manual y resolver alias. |
| Aplicaciones no incluidas en contrato pero operadas de facto | Registrar como pendiente de decisión. |
| Listados incompletos | Cruzar fuentes y escalar gaps. |

---

# 7. Actividad 2. Construir el inventario bruto

## 7.1 Objetivo

Crear una primera lista amplia de posibles aplicaciones, servicios y componentes, sin depurar todavía, para no perder elementos relevantes.

## 7.2 Técnica recomendada

Partir de una tabla única donde se consoliden todos los elementos encontrados en las distintas fuentes.

## 7.3 Campos mínimos del inventario bruto

| Campo | Descripción |
|---|---|
| ID provisional | Identificador interno de inventario. |
| Nombre encontrado | Nombre tal como aparece en la fuente. |
| Alias | Otros nombres conocidos. |
| Tipo | Aplicación, servicio, job, API, BD, componente, herramienta. |
| Fuente | Contrato, CMDB, Git, ITSM, monitorización, entrevista, etc. |
| Evidencia | Link, captura, exportación o referencia. |
| Dominio funcional preliminar | Pólizas, recibos, siniestros, mediadores, etc. |
| Tecnología preliminar | Java, .NET, Angular, COBOL, Oracle, etc. |
| Responsable conocido | Persona o equipo identificado. |
| Estado | Identificado, dudoso, duplicado, pendiente, fuera de alcance. |
| Observaciones | Comentarios iniciales. |

## 7.4 Ejemplo de inventario bruto

| ID | Nombre encontrado | Tipo | Fuente | Dominio preliminar | Estado | Observaciones |
|---|---|---|---|---|---|---|
| INV-001 | Portal Mediadores | Aplicación | Contrato | Mediadores | Identificado | Confirmar repositorio. |
| INV-002 | med-front | Componente | Git | Mediadores | Identificado | Posible frontend del portal. |
| INV-003 | API-Cotizacion | API | Jenkins | Cotización | Identificado | Aparece en pipeline. |
| INV-004 | REC_BATCH_01 | Job batch | Calendario batch | Recibos | Identificado | Revisar criticidad. |
| INV-005 | SiniestrosWeb | Aplicación | ITSM | Siniestros | Dudoso | No aparece en contrato. |

## 7.5 Acciones concretas

- Consolidar todos los nombres encontrados.
- No eliminar duplicados todavía.
- Marcar la fuente de cada elemento.
- Marcar elementos con nombres similares.
- Identificar componentes sin aplicación padre.
- Identificar aplicaciones sin componentes asociados.
- Identificar aplicaciones con tickets pero sin documentación.
- Identificar repositorios sin aplicación asociada.
- Identificar pipelines sin aplicación asociada.
- Identificar sistemas con alertas pero no inventariados.
- Identificar proveedores o integraciones sin aplicación asociada.



## 7.6 Enfoque ITIL: registro inicial de configuración

El inventario bruto debe prepararse pensando en su evolución hacia un registro de configuración del servicio. Para ello, cada elemento identificado debe conservar la relación con su fuente original y con las evidencias que justifican su inclusión.

Campos adicionales recomendados desde el punto de vista ITIL:

| Campo | Descripción |
|---|---|
| Servicio de negocio asociado | Servicio funcional que se ve soportado por el elemento. |
| CI relacionado | Elemento de configuración relacionado, si existe en CMDB. |
| Activo relacionado | Activo tecnológico o licencia asociada, si aplica. |
| Propietario del dato | Persona o equipo que confirma la información. |
| Nivel de confianza | Alto, medio o bajo según la calidad de la evidencia. |
| Fecha de última validación | Fecha en la que se revisó o confirmó el dato. |
| Relación con SLA | SLA, OLA o nivel de criticidad asociado. |
| Riesgo asociado | Riesgo registrado en el RAID log, si aplica. |

Esto permitirá que la Fase 1 no genere únicamente una hoja de cálculo de inventario, sino una base de gobierno para la transición y la operación futura.


---

# 8. Actividad 3. Depurar duplicados, alias y relaciones

## 8.1 Objetivo

Convertir el inventario bruto en un inventario comprensible y útil, resolviendo duplicados, nombres alternativos y relaciones aplicación-componente.

## 8.2 Problemas habituales

| Problema | Ejemplo |
|---|---|
| Una aplicación con varios nombres | “Portal Mediadores”, “MediadoresWeb”, “MEDPORTAL”. |
| Un repositorio por componente | `med-front`, `med-api`, `med-batch`. |
| Un nombre técnico que no coincide con el funcional | `pol-core-srv` soporta emisión de pólizas. |
| Aplicación antigua con nombre histórico | “Sistema Nuevo” que ya tiene 15 años. |
| Componentes compartidos | Servicio documental usado por emisión, siniestros y recibos. |
| Aplicaciones retiradas pero aún referenciadas | Aparecen en CMDB pero no tienen actividad real. |
| Aplicaciones activas no inventariadas | Aparecen en logs, ITSM o monitorización. |

## 8.3 Acciones concretas

- Agrupar nombres que representen la misma aplicación.
- Definir nombre canónico.
- Registrar alias.
- Asociar componentes a aplicación padre.
- Asociar APIs a dominios o aplicaciones consumidoras.
- Asociar jobs batch a procesos de negocio.
- Asociar bases de datos a aplicaciones.
- Marcar elementos retirados o dudosos.
- Registrar decisiones de consolidación.
- Validar agrupaciones con equipo saliente y cliente.

## 8.4 Plantilla de resolución de alias

| Nombre canónico | Alias | Fuente del alias | Confirmado por | Observaciones |
|---|---|---|---|---|
| Portal Mediadores | MEDPORTAL | Git | Equipo saliente | Front y backend separados. |
| Portal Mediadores | MediadoresWeb | ITSM | Service Manager | Nombre usado en tickets. |
| Recibos Batch | REC_BATCH_01 | Operación | Operaciones batch | Job nocturno crítico. |

---

# 9. Actividad 4. Clasificar aplicaciones por dominio funcional

## 9.1 Objetivo

Relacionar cada aplicación con los procesos de negocio asegurador que soporta.

Esto permite priorizar correctamente y preparar la transferencia funcional de la Fase 2.

## 9.2 Dominios funcionales recomendados

| Dominio | Ejemplos de procesos |
|---|---|
| Cotización | Simulación, tarificación, descuentos, elegibilidad. |
| Emisión | Alta de póliza, contratación, firma, documentación. |
| Cartera / pólizas | Consulta, modificación, suplementos, anulaciones. |
| Renovaciones | Renovación automática, campañas, actualización de primas. |
| Recibos y cobros | Emisión de recibos, domiciliación, impagos, recobros. |
| Siniestros | Apertura, tramitación, pagos, reservas, peritación. |
| Mediadores | Portal, comisiones, cartera, emisión delegada. |
| Clientes | Área privada, autoservicio, comunicaciones. |
| Documental | Generación, custodia y recuperación de documentos. |
| Comunicaciones | Email, SMS, notificaciones, cartas. |
| Cumplimiento | Consentimientos, KYC, privacidad, auditoría. |
| Reporting | BI, reporting regulatorio, reporting financiero. |
| Contabilidad | Asientos, cierres, conciliaciones. |
| Integración | Bus, APIs transversales, colas, ficheros. |
| Seguridad | Identidad, autenticación, autorización. |

## 9.3 Matriz aplicación / dominio

| Aplicación | Dominio principal | Dominios secundarios | Proceso crítico | Responsable negocio |
|---|---|---|---|---|
| Portal Mediadores | Mediadores | Cotización, emisión | Alta de póliza por mediador |  |
| Motor de tarificación | Cotización | Productos, pricing | Cálculo de prima |  |
| Sistema de recibos | Recibos | Contabilidad, bancos | Emisión y cobro |  |
| Gestor documental | Documental | Emisión, siniestros | Generación contractual |  |
| Sistema de siniestros | Siniestros | Pagos, peritación | Tramitación siniestro |  |

## 9.4 Preguntas clave

- ¿Qué proceso de negocio se detiene si esta aplicación falla?
- ¿Qué usuarios se ven afectados?
- ¿Afecta a cliente final, mediador o backoffice?
- ¿Afecta a emisión de pólizas?
- ¿Afecta a cobros?
- ¿Afecta a siniestros?
- ¿Genera documentación contractual?
- ¿Tiene impacto contable?
- ¿Tiene impacto regulatorio?
- ¿Es usada en cierres diarios, mensuales o anuales?

---

# 10. Actividad 5. Clasificar componentes técnicos

## 10.1 Objetivo

Identificar los componentes que forman cada aplicación y las tecnologías usadas.

## 10.2 Tipos de componentes

| Tipo | Ejemplos |
|---|---|
| Frontend | Angular, React, Vue, ASP.NET MVC. |
| Backend | Java, .NET, Node.js, COBOL, Spring Boot, Web API. |
| API | REST, SOAP, GraphQL. |
| Batch | Jobs Java, scripts, ETL, procedimientos almacenados. |
| Base de datos | Oracle, SQL Server, DB2, PostgreSQL, MongoDB. |
| Mensajería | Kafka, MQ, RabbitMQ, colas propietarias. |
| Documental | Gestor documental, plantillas, repositorio de documentos. |
| Reporting | ETL, DWH, Power BI, MicroStrategy, Cognos. |
| Middleware | ESB, API Gateway, bus de integración. |
| Infraestructura | Servidores, contenedores, Kubernetes, OpenShift, IIS, Tomcat. |

## 10.3 Matriz aplicación / componente

| Aplicación | Componente | Tipo | Tecnología | Repositorio | Pipeline | Entorno |
|---|---|---|---|---|---|---|
| Portal Mediadores | med-front | Frontend | Angular |  |  | DEV/PRE/PRO |
| Portal Mediadores | med-api | Backend | Java Spring |  |  | DEV/PRE/PRO |
| Recibos | rec-batch | Batch | Java / Shell |  |  | PRO |
| Siniestros | siniestros-db | BD | Oracle | N/A | N/A | PRE/PRO |

## 10.4 Acciones concretas

- Revisar repositorios.
- Revisar pipelines.
- Revisar despliegues activos.
- Revisar CMDB.
- Revisar monitorización.
- Revisar documentación técnica.
- Entrevistar a técnicos salientes.
- Asociar cada componente a una aplicación.
- Marcar componentes compartidos.
- Marcar componentes sin propietario.
- Marcar tecnologías obsoletas o fuera de soporte.

---

# 11. Actividad 6. Inventariar entornos

## 11.1 Objetivo

Identificar los entornos disponibles y entender su uso, restricciones y diferencias.

## 11.2 Entornos habituales

| Entorno | Uso |
|---|---|
| Local | Desarrollo individual. |
| DEV | Desarrollo compartido. |
| INT | Integración técnica. |
| QA | Pruebas técnicas. |
| UAT | Validación funcional por negocio. |
| PRE | Preproducción, similar a producción. |
| PRO | Producción. |
| DR | Recuperación ante desastre. |
| Sandbox | Pruebas aisladas o proveedores. |

## 11.3 Matriz de entornos

| Aplicación | Entorno | URL / host | Tecnología | Datos | Acceso requerido | Responsable | Observaciones |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | DEV |  | Angular/Java | Sintéticos | Sí |  |  |
| Portal Mediadores | PRE |  | Angular/Java | Enmascarados | Sí |  |  |
| Portal Mediadores | PRO |  | Angular/Java | Reales | Lectura logs |  | Acceso restringido. |
| Recibos Batch | PRO |  | Batch | Reales | Operación |  | Ventana nocturna. |

## 11.4 Aspectos a revisar

- Qué entornos existen realmente.
- Qué entornos están activos.
- Qué entornos están desactualizados.
- Qué datos contiene cada entorno.
- Si PRE es equivalente a PRO.
- Quién puede desplegar en cada entorno.
- Qué restricciones existen.
- Qué ventanas de disponibilidad hay.
- Qué dependencias externas están simuladas.
- Qué integraciones reales existen en PRE.
- Qué entornos tienen datos personales.
- Qué herramientas se usan para acceder.
- Qué VPN, bastiones o PAM son necesarios.

## 11.5 Gaps frecuentes

| Gap | Riesgo |
|---|---|
| No existe entorno PRE fiable | Cambios no probados adecuadamente. |
| DEV no reproduce incidencias | Diagnóstico lento. |
| Datos no anonimizados | Riesgo GDPR. |
| Integraciones simuladas sin documentación | Falsos positivos en pruebas. |
| Producción inaccesible para diagnóstico | Dependencia del equipo saliente. |
| Entornos con versiones distintas | Incidencias por diferencias de configuración. |

---

# 12. Actividad 7. Inventariar repositorios y control de versiones

## 12.1 Objetivo

Identificar dónde reside el código fuente, cómo se versiona y qué repositorios corresponden a cada aplicación o componente.

## 12.2 Campos recomendados

| Campo | Descripción |
|---|---|
| Aplicación | Aplicación asociada. |
| Componente | Front, backend, batch, librería, infraestructura. |
| Repositorio | URL o identificador. |
| Plataforma | GitHub, GitLab, Bitbucket, Azure Repos, SVN. |
| Rama principal | main, master, develop, trunk. |
| Estrategia de ramas | Gitflow, trunk-based, release branches. |
| Último commit | Fecha de actividad. |
| Responsable | Equipo propietario. |
| Permisos requeridos | Lectura, escritura, aprobación. |
| Estado | Validado, pendiente, dudoso. |

## 12.3 Acciones concretas

- Solicitar listado completo de repositorios.
- Cruzar repositorios con aplicaciones.
- Identificar repositorios huérfanos.
- Identificar aplicaciones sin repositorio.
- Revisar fecha de última actividad.
- Revisar README y documentación técnica.
- Revisar estructura de ramas.
- Identificar tags o releases.
- Identificar librerías compartidas.
- Identificar repositorios de infraestructura como código.
- Identificar repositorios de configuración.
- Registrar permisos necesarios.

## 12.4 Preguntas clave

- ¿El código de producción está en este repositorio?
- ¿Qué rama corresponde a producción?
- ¿Cómo se identifica la versión desplegada?
- ¿Hay tags por release?
- ¿Hay ramas antiguas aún en uso?
- ¿Hay código generado o binarios fuera del repositorio?
- ¿Hay dependencias internas en otros repositorios?
- ¿Hay secretos o credenciales en el código?
- ¿Hay documentación de build y despliegue?
- ¿Quién aprueba cambios?

---

# 13. Actividad 8. Inventariar pipelines y despliegues

## 13.1 Objetivo

Identificar cómo se construyen, empaquetan y despliegan las aplicaciones.

## 13.2 Matriz de pipelines

| Aplicación | Componente | Herramienta CI/CD | Pipeline | Entornos destino | Trigger | Aprobaciones | Rollback |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | med-api | Jenkins | build-med-api | DEV/PRE/PRO | Manual / commit | Sí | Pendiente |
| Portal Mediadores | med-front | Azure DevOps | deploy-med-front | DEV/PRE/PRO | Manual | Sí | Documentado |
| Recibos | rec-batch | Control-M / Jenkins | rec-batch-deploy | PRO | Manual | Sí | No claro |

## 13.3 Aspectos a revisar

- Herramienta CI/CD utilizada.
- Relación pipeline-repositorio.
- Relación pipeline-entorno.
- Triggers automáticos o manuales.
- Gates de calidad.
- Tests automatizados.
- Análisis estático.
- Análisis de seguridad.
- Variables de entorno.
- Secretos.
- Artefactos generados.
- Repositorio de artefactos.
- Aprobaciones.
- Despliegue azul/verde, canary o tradicional.
- Rollback.
- Histórico de despliegues.
- Despliegues fallidos.

## 13.4 Gaps frecuentes

| Gap | Riesgo |
|---|---|
| Despliegue manual no documentado | Dependencia de personas. |
| Pipeline sin rollback | Mayor riesgo ante errores. |
| Variables no trazadas | Incidencias por configuración. |
| Secretos en pipeline sin control | Riesgo de seguridad. |
| No hay relación commit-release | Difícil diagnosticar producción. |
| Pipelines antiguos sin propietario | Riesgo operativo. |

---

# 14. Actividad 9. Inventariar bases de datos y datos

## 14.1 Objetivo

Identificar las bases de datos, esquemas, tablas críticas, procedimientos, jobs y datos sensibles asociados a las aplicaciones.

## 14.2 Matriz aplicación / base de datos

| Aplicación | Base de datos | Motor | Esquema | Tipo de datos | Criticidad | Responsable | Observaciones |
|---|---|---|---|---|---|---|---|
| Emisión | POL_DB | Oracle | POLIZAS | Pólizas, clientes | Alta | DBA | Datos personales. |
| Recibos | REC_DB | Oracle | RECIBOS | Recibos, cobros | Alta | DBA | Integración bancaria. |
| Siniestros | SIN_DB | SQL Server | SIN | Siniestros | Alta | DBA | Puede contener datos sensibles. |

## 14.3 Elementos a identificar

- Motor de base de datos.
- Instancia.
- Esquema.
- Tablas críticas.
- Procedimientos almacenados.
- Triggers.
- Jobs.
- Vistas.
- Usuarios técnicos.
- Aplicaciones consumidoras.
- Datos personales.
- Datos especialmente sensibles.
- Volumetría.
- Política de retención.
- Backups.
- Restore.
- Réplicas.
- Enmascaramiento en entornos no productivos.

## 14.4 Preguntas clave

- ¿Qué tablas contienen pólizas?
- ¿Qué tablas contienen recibos?
- ¿Qué tablas contienen siniestros?
- ¿Qué tablas contienen datos personales?
- ¿Qué tablas contienen datos bancarios?
- ¿Qué tablas contienen datos de salud?
- ¿Qué procedimientos ejecutan lógica de negocio?
- ¿Hay lógica crítica en stored procedures?
- ¿Qué procesos batch escriben en la base de datos?
- ¿Cómo se versionan los cambios de modelo?
- ¿Qué aplicaciones comparten esquema?
- ¿Quién puede ejecutar scripts en producción?

## 14.5 Riesgos específicos

| Riesgo | Mitigación |
|---|---|
| Lógica de negocio oculta en BD | Revisar packages, procedures, triggers y jobs. |
| Datos sensibles sin clasificación | Involucrar DPO y seguridad. |
| Esquemas compartidos | Mapear consumidores y dependencias. |
| Cambios manuales en producción | Revisar procedimientos y auditoría. |
| Falta de versionado de scripts | Proponer control con herramienta o repositorio. |

---

# 15. Actividad 10. Inventariar integraciones

## 15.1 Objetivo

Identificar todas las comunicaciones entre aplicaciones, sistemas internos, terceros, proveedores, bancos, reguladores y plataformas corporativas.

## 15.2 Tipos de integración

| Tipo | Ejemplos |
|---|---|
| API REST | Consulta de cliente, cotización, emisión. |
| SOAP | Servicios legacy o de terceros. |
| Ficheros | SFTP, CSV, XML, ficheros bancarios. |
| Mensajería | MQ, Kafka, colas internas. |
| Batch | Intercambios nocturnos. |
| Base de datos compartida | Lectura o escritura directa entre sistemas. |
| Webhooks | Notificaciones de terceros. |
| Servicios documentales | Generación o custodia de documentos. |
| Plataformas externas | Firma, pagos, SMS, email, scoring, antifraude. |

## 15.3 Matriz de integraciones

| Sistema origen | Sistema destino | Tipo | Datos intercambiados | Frecuencia | Criticidad | Responsable | Observaciones |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | API Cotización | REST | Datos de riesgo | Online | Alta |  |  |
| Emisión | Gestor documental | API | Documentos póliza | Online | Alta |  |  |
| Recibos | Banco | Fichero SFTP | Remesas | Diario | Alta |  | Formato SEPA. |
| Siniestros | Proveedor peritación | API | Expediente siniestro | Online | Media |  | Tercero externo. |

## 15.4 Preguntas clave

- ¿Qué sistemas consume esta aplicación?
- ¿Qué sistemas consumen esta aplicación?
- ¿Qué datos se intercambian?
- ¿La integración es síncrona o asíncrona?
- ¿Es online o batch?
- ¿Qué ocurre si falla?
- ¿Hay reintentos?
- ¿Hay reproceso?
- ¿Dónde se monitoriza?
- ¿Quién es el propietario del sistema destino?
- ¿Hay contrato o SLA con el tercero?
- ¿Hay certificados o credenciales?
- ¿Cuándo caducan?
- ¿Existen entornos de prueba del tercero?
- ¿Hay datos personales en la integración?

## 15.5 Integraciones especialmente sensibles en seguros

- Bancos y pasarelas de pago.
- Firma electrónica.
- Gestor documental.
- Mediadores y corredores.
- Plataformas de comunicación.
- Scoring o tarificación externa.
- Antifraude.
- Peritación.
- Servicios sanitarios o datos de salud.
- Reporting financiero.
- Reporting regulatorio.
- Sistemas contables.
- Data Warehouse.

---

# 16. Actividad 11. Inventariar monitorización, logs y operación

## 16.1 Objetivo

Saber cómo se detectan, diagnostican y gestionan los problemas en producción.

## 16.2 Matriz de observabilidad

| Aplicación | Herramienta monitorización | Herramienta logs | Dashboard | Alertas | Responsable | Observaciones |
|---|---|---|---|---|---|---|
| Portal Mediadores | Dynatrace | Splunk |  | Sí | Operaciones | Confirmar umbrales. |
| Recibos Batch | Control-M | Logs servidor |  | Parcial | Batch Ops | Alertas por fallo job. |
| Siniestros | Grafana | ELK |  | Sí | Operaciones |  |

## 16.3 Elementos a identificar

- Herramientas APM.
- Dashboards existentes.
- Alertas configuradas.
- Umbrales.
- Logs técnicos.
- Logs funcionales.
- Correlation IDs.
- Retención de logs.
- Procedimientos de consulta.
- Guardias.
- On-call.
- Escalado.
- Runbooks asociados a alertas.
- Incidencias recurrentes.
- Falsos positivos.

## 16.4 Preguntas clave

- ¿Cómo se sabe que la aplicación está caída?
- ¿Qué alertas existen?
- ¿Quién recibe las alertas?
- ¿Qué alertas son realmente útiles?
- ¿Dónde se ven los errores?
- ¿Cómo se traza una operación de negocio?
- ¿Se puede seguir una póliza, recibo o siniestro entre sistemas?
- ¿Durante cuánto tiempo se conservan los logs?
- ¿Los logs contienen datos personales?
- ¿Hay dashboards por proceso de negocio?
- ¿Hay procedimientos asociados a alertas?

---

# 17. Actividad 12. Analizar tickets históricos

## 17.1 Objetivo

Utilizar la historia real de incidencias, problemas y cambios para identificar aplicaciones críticas, puntos débiles y conocimiento tácito.

## 17.2 Extracciones recomendadas

Solicitar tickets de los últimos **12 a 24 meses**, filtrados por:

- Aplicación.
- Severidad.
- Tipo: incidencia, problema, cambio, petición.
- Estado.
- Fecha de apertura y cierre.
- Tiempo de resolución.
- Equipo asignado.
- Categoría.
- Causa raíz.
- Workaround.
- Reaperturas.
- Incidencias mayores.
- Cambios fallidos.

## 17.3 Métricas útiles

| Métrica | Utilidad |
|---|---|
| Nº incidencias por aplicación | Detectar sistemas problemáticos. |
| Nº incidencias críticas | Identificar riesgo operativo. |
| MTTR | Medir dificultad de resolución. |
| Tickets recurrentes | Detectar problemas no resueltos. |
| Cambios fallidos | Detectar riesgo de despliegue. |
| Reaperturas | Detectar baja calidad de resolución. |
| Incidencias por integración | Detectar dependencias débiles. |
| Incidencias por batch | Detectar procesos sensibles. |

## 17.4 Preguntas clave

- ¿Qué aplicaciones generan más incidencias?
- ¿Qué incidencias han sido críticas?
- ¿Qué problemas se repiten?
- ¿Qué workarounds se usan habitualmente?
- ¿Qué componentes tienen más errores?
- ¿Qué despliegues han fallado?
- ¿Qué terceros generan más problemas?
- ¿Qué incidencias requieren expertos concretos?
- ¿Qué tickets tienen impacto regulatorio?
- ¿Qué procesos de negocio han estado bloqueados?

## 17.5 Resultado esperado

- Ranking de aplicaciones por volumen de incidencias.
- Ranking de aplicaciones por severidad.
- Lista de incidencias recurrentes.
- Lista de workarounds.
- Lista de problemas abiertos.
- Riesgos incorporados al RAID log.
- Priorización ajustada con datos reales.

---

# 18. Actividad 13. Clasificar criticidad y prioridad

## 18.1 Objetivo

Asignar a cada aplicación una criticidad inicial y una prioridad de transferencia.

## 18.2 Dimensiones de criticidad

| Dimensión | Pregunta |
|---|---|
| Negocio | ¿Qué proceso se bloquea si falla? |
| Cliente | ¿Afecta al cliente final? |
| Mediador | ¿Afecta a la red comercial? |
| Económica | ¿Impacta en cobros, pagos, emisión o contabilidad? |
| Regulatoria | ¿Puede generar incumplimientos o sanciones? |
| Operativa | ¿Tiene alternativa manual? |
| Técnica | ¿Es compleja, obsoleta o inestable? |
| Datos | ¿Trata datos sensibles? |
| Dependencias | ¿Es nodo central para otros sistemas? |
| Histórica | ¿Tiene muchas incidencias? |

## 18.3 Escala recomendada

| Criticidad | Descripción |
|---|---|
| Crítica | Su caída bloquea procesos esenciales, afecta a clientes, dinero, regulación o continuidad. |
| Alta | Impacto relevante en negocio o servicio, aunque con cierta contención. |
| Media | Impacto limitado o con alternativa operativa. |
| Baja | Aplicación auxiliar, bajo impacto o uso reducido. |

## 18.4 Matriz de criticidad

| Aplicación | Negocio | Cliente | Económico | Regulatorio | Datos sensibles | Dependencias | Incidencias | Criticidad |
|---|---|---|---|---|---|---|---|---|
| Emisión pólizas | Alta | Alta | Alta | Alta | Media | Alta | Media | Crítica |
| Recibos | Alta | Media | Alta | Media | Alta | Alta | Alta | Crítica |
| Siniestros | Alta | Alta | Alta | Alta | Alta | Media | Media | Crítica |
| Portal interno auxiliar | Baja | Baja | Baja | Baja | Baja | Baja | Baja | Baja |

## 18.5 Prioridad de transferencia

La prioridad no depende solo de la criticidad. También influye la dificultad de transferir conocimiento.

| Factor | Efecto |
|---|---|
| Alta criticidad | Subir prioridad. |
| Falta de documentación | Subir prioridad. |
| Experto saliente con baja disponibilidad | Subir prioridad. |
| Alta complejidad técnica | Subir prioridad. |
| Muchas incidencias históricas | Subir prioridad. |
| Aplicación estable y bien documentada | Puede bajar prioridad. |
| Aplicación fuera de uso | Puede quedar pendiente de decisión. |

---

# 19. Actividad 14. Validar el inventario con los equipos

## 19.1 Objetivo

Revisar el inventario inicial con los equipos adecuados para corregir errores, confirmar dudas y obtener aceptación preliminar.

## 19.2 Sesiones recomendadas

| Sesión | Participantes | Objetivo |
|---|---|---|
| Validación con cliente IT | Cliente, entrante | Confirmar alcance técnico. |
| Validación con proveedor saliente | Saliente, entrante | Confirmar aplicaciones, componentes y responsables. |
| Validación con negocio | Product owners, funcionales | Confirmar procesos y criticidad. |
| Validación con operaciones | ITSM, monitorización, batch | Confirmar operación real. |
| Validación con seguridad | IAM, DPO, compliance | Confirmar datos sensibles y restricciones. |
| Validación con arquitectura | Arquitectos | Confirmar dependencias y plataformas. |

## 19.3 Preguntas de validación

- ¿Falta alguna aplicación?
- ¿Hay aplicaciones que realmente no estén en uso?
- ¿Hay aplicaciones fuera de alcance?
- ¿Los nombres canónicos son correctos?
- ¿Los alias están bien asociados?
- ¿Los responsables identificados son correctos?
- ¿La criticidad asignada es razonable?
- ¿Las dependencias principales están reflejadas?
- ¿Existen aplicaciones compartidas con otros contratos?
- ¿Hay procesos críticos no representados?
- ¿Qué elementos deben revisarse antes de pasar a la siguiente fase?

## 19.4 Resultado esperado

- Inventario corregido.
- Dudas registradas.
- Gaps actualizados.
- Riesgos actualizados.
- Aplicaciones priorizadas.
- Elementos fuera de alcance identificados.
- Elementos pendientes de decisión escalados.

---

# 20. Actividad 15. Proponer oleadas de transferencia

## 20.1 Objetivo

Agrupar aplicaciones o dominios en oleadas de trabajo para las fases posteriores.

## 20.2 Criterios para definir oleadas

- Criticidad.
- Dominio funcional.
- Dependencias entre aplicaciones.
- Disponibilidad de expertos.
- Complejidad técnica.
- Volumen de documentación.
- Riesgo regulatorio.
- Incidencias históricas.
- Ventanas de negocio.
- Hitos contractuales.
- Calendario de auditorías.
- Cierres contables o campañas.

## 20.3 Ejemplo de oleadas

| Oleada | Contenido | Motivo |
|---|---|---|
| Oleada 1 | Emisión, recibos, siniestros, documental | Procesos críticos de negocio. |
| Oleada 2 | Portal mediadores, cotización, firma | Impacto comercial y contractual. |
| Oleada 3 | Reporting, DWH, contabilidad | Impacto financiero y regulatorio. |
| Oleada 4 | Aplicaciones auxiliares | Menor criticidad. |
| Oleada 5 | Sistemas legacy específicos | Requieren expertos concretos. |

## 20.4 Resultado esperado

- Propuesta de oleadas.
- Justificación de cada oleada.
- Dependencias entre oleadas.
- Riesgos asociados.
- Calendario tentativo.
- Validación por cliente.



---

# 21. Actividad 16. Construir el registro mínimo de configuración del servicio

## 21.1 Objetivo

Consolidar la información recopilada durante la Fase 1 en un registro mínimo de configuración del servicio, alineado con las prácticas ITIL de Service Configuration Management e IT Asset Management.

Este registro será la base para controlar qué se transfiere, qué está validado, qué está pendiente y qué riesgos existen sobre cada servicio, aplicación o componente.

## 21.2 Diferencia entre inventario y registro de configuración

| Concepto | Finalidad |
|---|---|
| Inventario | Identificar qué elementos existen. |
| Registro de configuración | Relacionar los elementos entre sí, indicar responsables, evidencias, estado de validación, criticidad y dependencias. |

El inventario responde a la pregunta:

> ¿Qué hay?

El registro de configuración responde además a:

> ¿Cómo se relaciona, quién lo gobierna, qué evidencia lo soporta y qué riesgo tiene?

## 21.3 Modelo mínimo de registro de configuración

| Campo | Descripción |
|---|---|
| ID de configuración | Identificador único del elemento. |
| Tipo de elemento | Servicio, aplicación, componente, base de datos, integración, job, proveedor, herramienta. |
| Nombre canónico | Nombre acordado y validado. |
| Alias | Nombres alternativos encontrados. |
| Servicio de negocio | Servicio o proceso que soporta. |
| Aplicación padre | Aplicación a la que pertenece, si aplica. |
| Componente relacionado | Frontend, backend, batch, API, base de datos, cola, etc. |
| Entorno | DEV, INT, QA, UAT, PRE, PRO, DR. |
| Tecnología | Lenguaje, framework, plataforma o motor. |
| Responsable funcional | Área o persona responsable desde negocio. |
| Responsable técnico | Equipo o persona responsable técnicamente. |
| Responsable operativo | Equipo que soporta la operación. |
| Proveedor externo | Tercero implicado, si existe. |
| Criticidad | Crítica, alta, media o baja. |
| SLA / OLA asociado | Nivel de servicio aplicable. |
| Fuente del dato | Contrato, CMDB, ITSM, Git, monitorización, entrevista, etc. |
| Evidencia | Link, captura, exportación, ticket, documento o acta. |
| Nivel de confianza | Alto, medio o bajo. |
| Estado de validación | Identificado, en análisis, validado, dudoso, fuera de alcance, pendiente de decisión. |
| Riesgo asociado | ID del riesgo en RAID log, si aplica. |
| Fecha de revisión | Última fecha de validación del dato. |

## 21.4 Relaciones mínimas a documentar

| Relación | Ejemplo |
|---|---|
| Servicio - aplicación | Emisión de pólizas soportada por Portal Mediadores y API Emisión. |
| Aplicación - componente | Portal Mediadores compuesto por frontend Angular y backend Java. |
| Aplicación - base de datos | Sistema de recibos usa REC_DB. |
| Aplicación - integración | Emisión consume servicio de firma electrónica. |
| Aplicación - proveedor | Servicio de firma prestado por tercero externo. |
| Aplicación - entorno | Portal Mediadores desplegado en DEV, PRE y PRO. |
| Aplicación - SLA | Portal Mediadores sujeto a SLA de disponibilidad y resolución. |
| Componente - repositorio | med-api reside en repositorio Git correspondiente. |
| Componente - pipeline | med-api se despliega mediante pipeline Jenkins. |
| Componente - alerta | API Cotización tiene alertas en APM y logs en Splunk. |

## 21.5 Estados de validación recomendados

| Estado | Uso |
|---|---|
| Identificado | El elemento aparece en alguna fuente, pero no se ha contrastado. |
| En análisis | Se está revisando información y evidencias. |
| Validado | La información ha sido confirmada por fuente fiable o evidencia operativa. |
| Dudoso | Existen contradicciones o información incompleta. |
| Fuera de alcance | Se confirma que no forma parte del servicio transferido. |
| Pendiente de decisión | Requiere decisión contractual, técnica o de gobierno. |
| Obsoleto | Existe como referencia histórica, pero no está activo o ha sido sustituido. |

## 21.6 Uso durante las siguientes fases

El registro mínimo de configuración se utilizará en las fases posteriores para:

- Priorizar la transferencia funcional.
- Planificar sesiones técnicas.
- Identificar dependencias críticas.
- Gestionar riesgos y gaps.
- Validar accesos necesarios.
- Preparar shadowing y reverse shadowing.
- Comprobar readiness operativo.
- Soportar la aceptación formal por aplicación o servicio.


---

# 22. Entregables de la Fase 1

## 21.1 Entregables principales

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Inventario consolidado de aplicaciones | Lista depurada y validada de aplicaciones. | Líder técnico + Transition Manager |
| Matriz de componentes | Relación aplicación-componente-tecnología. | Líder técnico |
| Matriz funcional | Relación aplicación-dominio-proceso. | Líder funcional |
| Matriz de entornos | Entornos por aplicación y restricciones. | Líder técnico / infraestructura |
| Matriz de repositorios | Repositorios y ramas principales. | Líder técnico |
| Matriz de pipelines | CI/CD y despliegues identificados. | DevOps / líder técnico |
| Matriz de bases de datos | BD, esquemas, datos críticos. | DBA / líder técnico |
| Matriz de integraciones | Sistemas origen/destino y criticidad. | Arquitectura / líder técnico |
| Matriz de documentación | Documentos existentes y gaps. | Transition Manager |
| Matriz de stakeholders por aplicación | Responsables técnicos, funcionales y operativos. | Transition Manager |
| Clasificación de criticidad | Criticidad inicial por aplicación. | Cliente + entrante |
| Propuesta de oleadas | Plan de transferencia por bloques. | Transition Manager |
| RAID log actualizado | Riesgos, issues, assumptions y dependencias. | Transition Manager |



## 22.2 Entregables ITIL específicos

| Entregable | Descripción | Práctica ITIL relacionada | Responsable sugerido |
|---|---|---|---|
| Registro mínimo de configuración del servicio | Mini-CMDB de transición con servicios, aplicaciones, componentes, relaciones, evidencias y estados. | Service Configuration Management | Líder técnico + Service Manager |
| Mapa servicio / aplicación / componente | Relación entre servicios de negocio, aplicaciones y componentes técnicos. | Service Configuration Management / Architecture Management | Arquitectura + líder técnico |
| Inventario de activos tecnológicos | Herramientas, plataformas, licencias, certificados y componentes relevantes. | IT Asset Management | Líder técnico + cliente |
| Matriz de proveedores y terceros | Terceros, contratos, soporte, contactos, SLAs y dependencias. | Supplier Management | Service Manager + cliente |
| Clasificación de datos y sensibilidad | Identificación inicial de datos personales, bancarios, salud u otros datos sensibles. | Information Security Management | Seguridad + DPO + líder técnico |
| Relación de SLAs/OLAs por servicio | Niveles de servicio asociados a aplicaciones y procesos críticos. | Service Level Management | Service Manager |
| Matriz de nivel de confianza del inventario | Clasificación de la fiabilidad de cada dato inventariado. | Knowledge Management / Risk Management | Transition Manager |
| Riesgos de configuración y activos | Riesgos derivados de elementos no identificados, obsoletos, huérfanos o sin propietario. | Risk Management | Transition Manager |


---

# 23. Plantillas útiles de la Fase 1

## 22.1 Inventario consolidado de aplicaciones

| ID | Aplicación | Alias | Dominio | Criticidad | Estado alcance | Responsable negocio | Responsable técnico | Estado inventario |
|---|---|---|---|---|---|---|---|---|
| APP-001 |  |  |  |  | Incluida / Dudosa / Excluida |  |  | Identificada / Validada |
| APP-002 |  |  |  |  |  |  |  |  |

## 22.2 Matriz de documentación

| Aplicación | Tipo documento | Link | Fecha | Propietario | Estado | Gap |
|---|---|---|---|---|---|---|
|  | Funcional |  |  |  | Vigente / Obsoleto / Dudoso |  |
|  | Técnica |  |  |  |  |  |
|  | Runbook |  |  |  |  |  |
|  | Arquitectura |  |  |  |  |  |

## 22.3 Matriz de gaps

| ID | Aplicación | Gap | Tipo | Criticidad | Responsable | Fecha objetivo | Estado |
|---|---|---|---|---|---|---|---|
| GAP-001 |  | No se conoce repositorio | Técnico | Alta |  |  | Abierto |
| GAP-002 |  | No existe documentación funcional | Funcional | Alta |  |  | Abierto |
| GAP-003 |  | Integración bancaria sin responsable | Integración | Crítica |  |  | Abierto |

## 22.4 Matriz de dependencias

| Aplicación origen | Aplicación destino | Tipo dependencia | Criticidad | Responsable destino | Estado | Observaciones |
|---|---|---|---|---|---|---|
|  |  | API / BD / Fichero / Cola / Batch | Alta / Media / Baja |  | Validada / Dudosa |  |



## 23.5 Registro mínimo de configuración del servicio

| ID Configuración | Tipo | Nombre canónico | Servicio de negocio | Aplicación padre | Tecnología | Entorno | Responsable | Criticidad | Fuente | Evidencia | Confianza | Estado validación | Riesgo asociado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CI-001 | Aplicación |  |  |  |  |  |  | Crítica / Alta / Media / Baja |  |  | Alta / Media / Baja | Identificado / Validado / Dudoso |  |
| CI-002 | Componente |  |  |  |  |  |  |  |  |  |  |  |  |

## 23.6 Matriz servicio / aplicación / componente

| Servicio de negocio | Proceso | Aplicación | Componente | Tipo | Criticidad | SLA / OLA | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
|  | Cotización / emisión / recibos / siniestros |  |  | Front / Backend / API / Batch / BD |  |  |  |  |

## 23.7 Matriz de nivel de confianza

| Dato inventariado | Fuente | Evidencia | Nivel de confianza | Motivo | Acción necesaria |
|---|---|---|---|---|---|
|  | CMDB / ITSM / Git / entrevista / monitorización |  | Alto / Medio / Bajo |  | Validar / completar / descartar |


---

# 24. Checklist operativo de Fase 1

## 23.1 Inventario general

- [ ] Recopilar inventario contractual.
- [ ] Recopilar CMDB.
- [ ] Recopilar portfolio de aplicaciones.
- [ ] Recopilar listado de repositorios.
- [ ] Recopilar listado de pipelines.
- [ ] Recopilar listado de entornos.
- [ ] Recopilar listado de bases de datos.
- [ ] Recopilar listado de integraciones.
- [ ] Recopilar listado de proveedores.
- [ ] Recopilar documentación funcional.
- [ ] Recopilar documentación técnica.
- [ ] Recopilar tickets históricos.
- [ ] Recopilar calendario batch.
- [ ] Crear inventario bruto.
- [ ] Depurar duplicados.
- [ ] Definir nombres canónicos.
- [ ] Registrar alias.
- [ ] Marcar aplicaciones dudosas.
- [ ] Marcar aplicaciones fuera de alcance.

## 23.2 Clasificación funcional

- [ ] Asignar dominio funcional.
- [ ] Identificar proceso de negocio principal.
- [ ] Identificar procesos secundarios.
- [ ] Identificar usuarios.
- [ ] Identificar impacto en cliente final.
- [ ] Identificar impacto en mediadores.
- [ ] Identificar impacto en backoffice.
- [ ] Identificar impacto en emisión.
- [ ] Identificar impacto en recibos.
- [ ] Identificar impacto en siniestros.
- [ ] Identificar impacto en reporting.
- [ ] Validar con negocio.

## 23.3 Clasificación técnica

- [ ] Identificar tecnología principal.
- [ ] Identificar frontend.
- [ ] Identificar backend.
- [ ] Identificar APIs.
- [ ] Identificar jobs batch.
- [ ] Identificar bases de datos.
- [ ] Identificar colas o mensajería.
- [ ] Identificar servicios compartidos.
- [ ] Identificar plataformas transversales.
- [ ] Identificar herramientas de despliegue.
- [ ] Identificar herramientas de monitorización.
- [ ] Identificar componentes legacy.
- [ ] Identificar componentes sin propietario.

## 23.4 Entornos

- [ ] Identificar DEV.
- [ ] Identificar INT.
- [ ] Identificar QA.
- [ ] Identificar UAT.
- [ ] Identificar PRE.
- [ ] Identificar PRO.
- [ ] Identificar DR.
- [ ] Identificar sandbox.
- [ ] Documentar diferencias entre entornos.
- [ ] Identificar datos usados por entorno.
- [ ] Identificar restricciones de acceso.
- [ ] Identificar responsables.

## 23.5 Repositorios y CI/CD

- [ ] Mapear aplicación-repositorio.
- [ ] Mapear componente-repositorio.
- [ ] Identificar ramas principales.
- [ ] Identificar tags y releases.
- [ ] Identificar repositorios huérfanos.
- [ ] Identificar aplicaciones sin repositorio.
- [ ] Mapear pipelines.
- [ ] Identificar despliegues manuales.
- [ ] Identificar aprobaciones.
- [ ] Identificar rollback.
- [ ] Identificar artefactos.
- [ ] Identificar secretos o variables críticas.

## 23.6 Bases de datos y datos

- [ ] Identificar motores.
- [ ] Identificar instancias.
- [ ] Identificar esquemas.
- [ ] Identificar tablas críticas.
- [ ] Identificar procedimientos.
- [ ] Identificar jobs.
- [ ] Identificar triggers.
- [ ] Identificar datos personales.
- [ ] Identificar datos sensibles.
- [ ] Identificar consumidores.
- [ ] Identificar backups.
- [ ] Identificar política de retención.
- [ ] Identificar gaps de documentación.

## 23.7 Integraciones

- [ ] Identificar APIs internas.
- [ ] Identificar APIs externas.
- [ ] Identificar integraciones por fichero.
- [ ] Identificar integraciones por cola.
- [ ] Identificar integraciones batch.
- [ ] Identificar bancos.
- [ ] Identificar firma electrónica.
- [ ] Identificar gestor documental.
- [ ] Identificar proveedores de comunicaciones.
- [ ] Identificar scoring o antifraude.
- [ ] Identificar reporting regulatorio.
- [ ] Identificar certificados.
- [ ] Identificar credenciales.
- [ ] Identificar reprocesos.

## 23.8 Criticidad y priorización

- [ ] Definir criterios de criticidad.
- [ ] Clasificar criticidad por aplicación.
- [ ] Clasificar riesgo técnico.
- [ ] Clasificar riesgo regulatorio.
- [ ] Clasificar riesgo por datos sensibles.
- [ ] Analizar incidencias históricas.
- [ ] Identificar aplicaciones críticas.
- [ ] Identificar aplicaciones de baja prioridad.
- [ ] Definir propuesta de oleadas.
- [ ] Validar priorización con cliente.



## 24.9 Checklist ITIL de configuración y activos

- [ ] Definir identificador único para cada elemento de configuración.
- [ ] Relacionar servicios de negocio con aplicaciones.
- [ ] Relacionar aplicaciones con componentes técnicos.
- [ ] Relacionar componentes con repositorios.
- [ ] Relacionar componentes con pipelines.
- [ ] Relacionar aplicaciones con bases de datos.
- [ ] Relacionar aplicaciones con integraciones.
- [ ] Relacionar aplicaciones con proveedores.
- [ ] Registrar SLAs u OLAs asociados.
- [ ] Registrar fuente y evidencia de cada dato crítico.
- [ ] Asignar nivel de confianza a los datos principales.
- [ ] Identificar elementos sin propietario.
- [ ] Identificar activos tecnológicos relevantes.
- [ ] Identificar licencias, certificados o componentes sujetos a caducidad.
- [ ] Identificar datos sensibles por aplicación o servicio.
- [ ] Registrar riesgos de configuración en el RAID log.
- [ ] Marcar elementos fuera de alcance o pendientes de decisión.
- [ ] Validar el registro mínimo de configuración con cliente y equipo saliente.


---

# 25. Riesgos específicos de la Fase 1

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Inventario incompleto | Se dejan sistemas sin transición | Cruzar contrato, CMDB, ITSM, Git, CI/CD, monitorización y entrevistas. |
| Duplicidad de nombres | Confusión en responsabilidades | Definir nombre canónico y alias. |
| Aplicaciones fuera de contrato pero operadas | Riesgo contractual y operativo | Registrar como pendiente de decisión y escalar. |
| Componentes sin propietario | Riesgo de soporte futuro | Asignar responsable temporal y registrar gap. |
| Documentación obsoleta | Transferencia incorrecta | Marcar estado documental y validar con evidencias. |
| Dependencias no identificadas | Incidencias por impacto cruzado | Construir matriz de dependencias. |
| Integraciones externas ocultas | Riesgo de caída o incumplimiento | Revisar logs, contratos, certificados y tickets. |
| Datos sensibles no detectados | Riesgo GDPR y auditoría | Involucrar seguridad, DPO y responsables de datos. |
| Criticidad mal asignada | Priorización incorrecta | Validar con negocio, operaciones y métricas históricas. |
| Proveedor saliente minimiza complejidad | Subestimación de esfuerzo | Contrastar con tickets, código, pipelines y operación real. |
| Aplicaciones legacy sin documentación | Riesgo alto de conocimiento tácito | Priorizar sesiones con expertos y shadowing temprano. |
| No se identifican procesos batch | Riesgo en cierres y procesos nocturnos | Revisar calendario batch y herramientas de operación. |



## 25.1 Riesgos ITIL específicos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Registro de configuración incompleto | La transición se basa en una visión parcial del servicio | Cruzar fuentes, asignar nivel de confianza y revisar semanalmente elementos dudosos. |
| Elementos de configuración sin relación con servicios | Dificulta priorizar por valor de negocio | Relacionar cada aplicación con servicio, proceso y criticidad. |
| Activos tecnológicos no identificados | Riesgo de soporte, licencias o caducidades no controladas | Crear inventario de activos, licencias, certificados y herramientas críticas. |
| SLAs no asociados a aplicaciones | No se puede medir impacto real ni readiness operativo | Relacionar cada servicio/aplicación con SLA, OLA o expectativa operativa. |
| Proveedores no incorporados al inventario | Riesgo de escalado fallido ante incidencias | Añadir matriz de proveedores, contactos, contratos y procedimientos de soporte. |
| Fuentes sin trazabilidad | No se puede auditar ni validar la información | Registrar fuente, evidencia, propietario del dato y fecha de validación. |
| Nivel de confianza no explícito | Se tratan como válidos datos que aún son dudosos | Clasificar cada dato crítico con confianza alta, media o baja. |


---

# 26. Criterios de salida de la Fase 1

## 25.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Inventario bruto creado | Tabla consolidada | Pendiente / En curso / Validado |
| Duplicados y alias depurados | Matriz de alias |  |
| Inventario consolidado creado | Matriz de aplicaciones |  |
| Aplicaciones clasificadas por dominio | Matriz funcional |  |
| Componentes técnicos identificados | Matriz de componentes |  |
| Entornos identificados | Matriz de entornos |  |
| Repositorios identificados | Matriz de repositorios |  |
| Pipelines identificados | Matriz CI/CD |  |
| Bases de datos identificadas | Matriz de BBDD |  |
| Integraciones principales identificadas | Matriz de integraciones |  |
| Documentación existente localizada | Matriz documental |  |
| Gaps documentales registrados | Matriz de gaps |  |
| Responsables identificados | Matriz de stakeholders por aplicación |  |
| Tickets históricos revisados | Informe o extracción ITSM |  |
| Criticidad inicial asignada | Matriz de criticidad |  |
| Riesgos actualizados | RAID log |  |
| Propuesta de oleadas creada | Plan de oleadas |  |
| Validación inicial realizada | Acta de validación |  |
| Registro mínimo de configuración creado | Mini-CMDB de transición |  |
| Servicios relacionados con aplicaciones | Matriz servicio/aplicación/componente |  |
| Activos tecnológicos identificados | Inventario de activos |  |
| Proveedores críticos identificados | Matriz de proveedores |  |
| SLAs/OLAs asociados a servicios críticos | Matriz de niveles de servicio |  |
| Nivel de confianza asignado a datos críticos | Matriz de confianza |  |
| Riesgos de configuración registrados | RAID log actualizado |  |

## 25.2 Criterio de salida recomendado

La Fase 1 puede considerarse cerrada cuando:

> Existe un inventario consolidado, trazable y validado inicialmente de las aplicaciones, componentes, entornos, repositorios, datos, integraciones, documentación, responsables, criticidad, activos, proveedores, SLAs y relaciones de configuración, suficiente para planificar las fases de transferencia funcional y técnica en oleadas priorizadas.

Desde el punto de vista ITIL, la fase debe cerrar con una primera versión del registro mínimo de configuración del servicio, con fuentes, evidencias, nivel de confianza y riesgos asociados.

---

# 27. Recomendaciones prácticas para liderar la Fase 1

## 26.1 Recomendaciones de enfoque

- No intentar conseguir un inventario perfecto desde el primer día.
- Trabajar con versiones sucesivas del inventario.
- Registrar siempre la fuente de cada dato.
- Diferenciar información confirmada de información pendiente.
- Revisar aplicaciones críticas antes que auxiliares.
- Cruzar datos de herramientas con entrevistas.
- No aceptar “esto no falla nunca” sin revisar tickets.
- No aceptar “eso ya no se usa” sin revisar monitorización o logs.
- Involucrar negocio para validar criticidad.
- Involucrar seguridad para datos sensibles.
- Involucrar operaciones para validar producción real.
- Involucrar arquitectura para validar dependencias.

## 26.2 Señales de alerta

Durante la Fase 1, deben preocupar especialmente estas señales:

- Nadie sabe quién es el responsable de una aplicación.
- Una aplicación tiene tickets recientes pero no aparece en contrato.
- Un repositorio no tiene commits recientes pero la aplicación está activa.
- Una aplicación crítica no tiene documentación.
- Un proceso batch crítico depende de una persona concreta.
- PRE no se parece a PRO.
- Las integraciones externas no tienen propietario.
- Hay datos reales en entornos no productivos.
- No hay trazabilidad entre commit, build y despliegue.
- No se sabe cómo hacer rollback.
- La criticidad técnica y la criticidad de negocio no coinciden.
- Existen sistemas legacy con baja disponibilidad de expertos.

## 26.3 Buenas prácticas

- Crear un identificador único por aplicación.
- Mantener alias para evitar confusiones.
- Crear una columna “fuente” en todas las matrices.
- Crear una columna “nivel de confianza” en los datos.
- Usar estados claros: identificado, validado, dudoso, fuera de alcance.
- Revisar semanalmente los gaps.
- Escalar pronto los elementos dudosos de alcance.
- Priorizar por impacto, no por facilidad.
- Convertir hallazgos en tareas del backlog.
- Convertir riesgos en entradas del RAID log.
- Preparar desde esta fase las sesiones de Fase 2 y Fase 3.

---

# 28. Resumen ejecutivo de la Fase 1

La Fase 1 transforma una visión contractual o parcial del servicio en un mapa operativo inicial del ecosistema real.

El resultado deseado es pasar a las siguientes fases con:

1. **Aplicaciones identificadas y depuradas.**
2. **Alias y duplicados resueltos.**
3. **Dominios funcionales asignados.**
4. **Componentes técnicos identificados.**
5. **Entornos conocidos.**
6. **Repositorios y pipelines localizados.**
7. **Bases de datos e integraciones inventariadas.**
8. **Documentación existente clasificada.**
9. **Responsables identificados.**
10. **Criticidad inicial asignada.**
11. **Riesgos y gaps registrados.**
12. **Oleadas de transferencia propuestas.**
13. **Registro mínimo de configuración del servicio creado.**
14. **Relaciones servicio / aplicación / componente documentadas.**
15. **Nivel de confianza y evidencia asociados a los datos críticos.**

La Fase 1 no busca que el equipo entrante sepa todavía operar cada aplicación, pero sí que sepa **qué existe, qué falta, qué es crítico y en qué orden debe profundizar**.

---
