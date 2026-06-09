# Fase 3. Transferencia técnica profunda  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 3

La **Fase 3. Transferencia técnica profunda** tiene como objetivo que el equipo entrante adquiera el conocimiento técnico necesario para mantener, diagnosticar, modificar, desplegar y operar las aplicaciones incluidas en el contrato.

En las fases anteriores se ha construido el inventario y se ha comprendido el funcionamiento documental y funcional del ecosistema. En esta fase se debe bajar al detalle técnico:

- Arquitectura.
- Código fuente.
- Frameworks.
- Configuración.
- Repositorios.
- Pipelines.
- Despliegues.
- Bases de datos.
- Integraciones.
- Seguridad.
- Monitorización.
- Logs.
- Batch.
- Infraestructura.
- Dependencias.
- Procedimientos de recuperación.
- Deuda técnica.
- Riesgos operativos.

El objetivo no es convertir al equipo entrante en experto absoluto de todos los sistemas desde el primer día, sino lograr que pueda:

- Entender cómo están construidas las aplicaciones.
- Localizar el código y los componentes relevantes.
- Diagnosticar incidencias técnicas.
- Relacionar errores técnicos con procesos funcionales.
- Compilar y desplegar en entornos no productivos.
- Entender cómo se despliega en producción.
- Saber dónde mirar logs, métricas y alertas.
- Conocer los puntos críticos de datos, integraciones y seguridad.
- Prepararse para el shadowing operativo de la Fase 4.

---

## 2. Resultado esperado de la Fase 3

Al finalizar esta fase, el equipo debe disponer de:

- Un **mapa de arquitectura técnica validado**.
- Un **conocimiento razonable de los componentes principales**.
- Una **matriz aplicación / componente / tecnología / repositorio / pipeline**.
- Una **guía de build y ejecución por aplicación**.
- Una **guía de despliegue y rollback por aplicación crítica**.
- Un **inventario validado de configuraciones por entorno**.
- Una **matriz de bases de datos, esquemas, tablas críticas y lógica en BD**.
- Una **matriz técnica de integraciones**.
- Una **guía de monitorización, logs y diagnóstico**.
- Una **identificación de procesos batch y procedimientos de reproceso**.
- Una **identificación de secretos, certificados y cuentas técnicas**.
- Un **registro de deuda técnica y riesgos técnicos**.
- Una **lista de gaps técnicos priorizados**.
- Un conjunto de **runbooks técnicos iniciales**.
- Una lista de **casos técnicos que deberán observarse en shadowing**.
- Un **registro técnico de configuración** alineado con la mini-CMDB de transición.
- Una **matriz de trazabilidad código / artefacto / despliegue / cambio / servicio**.
- Un **catálogo inicial de problemas técnicos recurrentes y workarounds**.
- Una **evaluación de preparación operativa técnica** para pasar a shadowing.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **4 a 8 semanas**.

Puede ser menor si:

- Las aplicaciones son modernas y están bien documentadas.
- Los repositorios están ordenados.
- Los pipelines son reproducibles.
- Hay buena cobertura de tests.
- Los entornos son consistentes.
- La observabilidad está madura.
- El proveedor saliente colabora activamente.

Puede alargarse si:

- Hay sistemas legacy.
- Hay código sin documentación.
- Hay despliegues manuales.
- Hay lógica de negocio en base de datos.
- Existen múltiples tecnologías.
- Los entornos no son equivalentes.
- Las integraciones externas son complejas.
- Hay procesos batch críticos.
- No existe trazabilidad entre código, artefacto y producción.
- Hay dependencia de expertos concretos.
- Hay requisitos fuertes de seguridad, auditoría o cumplimiento.

---


# 4. Alineamiento ITIL específico de la Fase 3

## 4.1 Sentido ITIL de esta fase

Desde la perspectiva de ITIL, la Fase 3 representa el momento en el que el conocimiento técnico deja de ser una explicación teórica y empieza a convertirse en **capacidad operativa verificable**.

Esta fase debe permitir que el equipo entrante entienda los elementos técnicos que soportan el servicio, su relación con los procesos de negocio, sus dependencias, sus riesgos y los mecanismos necesarios para mantenerlos bajo control durante la operación ordinaria.

Por tanto, la transferencia técnica profunda se alinea especialmente con las prácticas ITIL orientadas a:

- Conocer y controlar la configuración del servicio.
- Comprender la arquitectura y las plataformas que lo soportan.
- Asegurar la capacidad de desplegar, revertir y validar cambios.
- Preparar la gestión de incidencias y problemas técnicos.
- Garantizar seguridad, continuidad, observabilidad y trazabilidad.
- Generar runbooks y conocimiento accionable para la operación.

## 4.2 Prácticas ITIL relacionadas

| Práctica ITIL | Aplicación en la Fase 3 |
|---|---|
| **Architecture Management** | Comprensión de arquitectura global, dominios técnicos, plataformas, patrones, integraciones y decisiones históricas. |
| **Service Configuration Management** | Relación entre servicios, aplicaciones, componentes, entornos, bases de datos, integraciones, jobs y elementos de configuración. |
| **IT Asset Management** | Identificación de activos tecnológicos, licencias, certificados, cuentas técnicas, herramientas, servidores, plataformas y componentes relevantes. |
| **Deployment Management** | Comprensión de cómo se despliegan los componentes en cada entorno y qué evidencias se generan. |
| **Release Management** | Identificación de versiones, artefactos, ramas, tags, paquetes y relación entre release, cambio y despliegue. |
| **Change Enablement** | Revisión de controles, aprobaciones, CAB, ventanas, validaciones pre/post y trazabilidad de cambios técnicos. |
| **Incident Management** | Preparación para diagnosticar incidencias técnicas mediante logs, alertas, dashboards, errores frecuentes y runbooks. |
| **Problem Management** | Identificación de problemas recurrentes, deuda técnica, causas raíz probables, workarounds y riesgos estructurales. |
| **Monitoring and Event Management** | Revisión de monitorización, alertas, eventos, correlación, dashboards y procedimientos de respuesta. |
| **Information Security Management** | Revisión de accesos, secretos, certificados, cuentas técnicas, datos sensibles, logs y controles de seguridad. |
| **Service Continuity Management** | Revisión de backup, restore, DR, RTO, RPO, contingencias y recuperación. |
| **Knowledge Management** | Conversión del conocimiento técnico en guías, runbooks, matrices, troubleshooting y base de conocimiento operativa. |
| **Continual Improvement** | Registro de mejoras técnicas, automatización, observabilidad, documentación, reducción de deuda y estabilización futura. |

## 4.3 Resultado ITIL esperado

Al finalizar esta fase, el equipo entrante no solo debe haber recibido explicaciones técnicas, sino disponer de evidencias suficientes de que puede empezar a participar en la operación real del servicio.

Esto implica que:

- Los elementos técnicos relevantes están identificados y relacionados con servicios de negocio.
- Los componentes críticos tienen propietario, documentación mínima y estado de validación.
- Los procedimientos de build, despliegue, rollback, diagnóstico y recuperación están documentados o tienen gaps explícitos.
- Los riesgos técnicos están registrados y priorizados.
- Los elementos de configuración relevantes están vinculados a la mini-CMDB o registro de configuración de transición.
- Los runbooks técnicos iniciales son suficientemente accionables para ser utilizados durante shadowing.
- Los casos de shadowing se han definido a partir de riesgos reales, criticidad y operación observada.

## 4.4 Evidencias ITIL esperadas

| Evidencia | Finalidad |
|---|---|
| Diagrama de arquitectura validado | Confirmar comprensión del ecosistema técnico. |
| Matriz servicio / aplicación / componente | Vincular configuración técnica con servicio de negocio. |
| Registro de configuración técnica | Alimentar la mini-CMDB de transición. |
| Matriz de repositorios, ramas, tags y artefactos | Asegurar trazabilidad entre código y producción. |
| Guías de build y ejecución | Comprobar reproducibilidad técnica. |
| Matriz de configuración por entorno | Identificar diferencias, parámetros críticos y secretos. |
| Runbooks de despliegue y rollback | Preparar operación de cambios y releases. |
| Matriz de observabilidad | Preparar gestión de eventos e incidencias. |
| Catálogo de alertas y errores frecuentes | Preparar diagnóstico operativo. |
| Matriz de secretos y certificados | Controlar riesgos de seguridad y caducidad. |
| Matriz de backup, restore, RTO y RPO | Preparar continuidad y recuperación. |
| Registro de deuda técnica y problemas recurrentes | Alimentar Problem Management y mejora continua. |
| Casos de shadowing técnico | Preparar observación operativa de Fase 4. |

## 4.5 Relación con fases anteriores y posteriores

La Fase 3 consume información de las fases anteriores y genera insumos críticos para las siguientes:

| Origen / destino | Relación |
|---|---|
| Fase 1. Descubrimiento e inventario | Aporta inventario, criticidad, componentes, entornos, repositorios, BBDD e integraciones. |
| Fase 2. Transferencia funcional | Aporta procesos, reglas, documentos, incidencias funcionales y preguntas técnicas derivadas. |
| Fase 4. Shadowing operativo | Recibe casos a observar, runbooks iniciales, riesgos técnicos y procedimientos que deben contrastarse en operación real. |
| Fase 5. Reverse shadowing | Utilizará los runbooks y guías técnicas para que el equipo entrante opere bajo supervisión. |
| Fase 6. Asunción progresiva | Usará los criterios de preparación técnica para decidir qué aplicaciones pueden asumirse. |

## 4.6 Principio de preparación operativa técnica

La Fase 3 debe cerrarse con una pregunta de control:

> Si mañana se produce una incidencia técnica en una aplicación crítica, ¿el equipo entrante sabe dónde está el código, qué versión está desplegada, qué logs revisar, qué alertas consultar, qué integraciones validar, qué batch comprobar, qué workaround aplicar, a quién escalar y qué riesgos existen?

Si la respuesta no puede justificarse con evidencias, runbooks o procedimientos, la aplicación no debería considerarse técnicamente preparada para shadowing o reverse shadowing.

---

# 5. Principios de trabajo de la Fase 3

## 4.1 Trabajar desde la arquitectura hacia el detalle

La revisión técnica debe ir de lo general a lo específico:

1. Arquitectura global.
2. Aplicaciones y dominios.
3. Componentes.
4. Código.
5. Datos.
6. Integraciones.
7. Despliegue.
8. Operación.
9. Seguridad.
10. Recuperación.

## 4.2 Relacionar siempre técnica con negocio

En una aseguradora, un componente técnico rara vez es neutro. Debe conectarse con procesos de negocio.

Ejemplos:

| Componente técnico | Pregunta funcional asociada |
|---|---|
| API de cotización | ¿Qué productos calcula? ¿Qué reglas de tarifa aplica? |
| Batch de recibos | ¿Qué recibos genera? ¿Qué ocurre si falla? |
| Gestor documental | ¿Qué documentos contractuales produce? |
| Base de datos de siniestros | ¿Qué datos sensibles almacena? |
| Servicio de firma | ¿Qué contratos dependen de él? |
| Integración bancaria | ¿Qué impacto tiene en cobros e impagos? |

## 4.3 No dar por válido un procedimiento hasta ejecutarlo o observarlo

Un procedimiento técnico debe considerarse realmente aprendido solo cuando:

- Se ha explicado.
- Se ha documentado.
- Se ha contrastado con evidencias.
- Se ha ejecutado en entorno no productivo o se ha observado su ejecución.
- Se ha registrado qué hacer si falla.

## 4.4 Diferenciar conocimiento de lectura, operación y administración

No todos los miembros del equipo necesitan el mismo nivel de conocimiento.

| Nivel | Capacidad esperada |
|---|---|
| Lectura | Entender documentación, código, logs y arquitectura. |
| Diagnóstico | Investigar incidencias y localizar causa probable. |
| Operación | Ejecutar tareas habituales, reinicios, reprocesos, validaciones. |
| Cambio | Modificar código, configuración o parametrización. |
| Despliegue | Ejecutar o coordinar despliegues. |
| Administración | Gestionar permisos, plataformas, infraestructura o herramientas. |

## 4.5 Registrar deuda técnica sin convertir la transición en una refactorización

Durante la Fase 3 aparecerá deuda técnica. Debe registrarse, clasificarse y priorizarse, pero no debe mezclarse indiscriminadamente con la transición.

La transición busca primero asegurar continuidad. Las mejoras deben pasar a un plan posterior salvo que mitiguen un riesgo crítico.

---


## 5.6 Principios ITIL aplicados al conocimiento técnico

Además de los principios anteriores, durante la Fase 3 se aplicarán los siguientes criterios de control alineados con ITIL:

| Principio | Aplicación práctica |
|---|---|
| **Trazabilidad técnica** | Cada componente debe relacionarse con aplicación, servicio de negocio, entorno, repositorio, pipeline, BBDD, integración y responsable. |
| **Configuración controlada** | Los elementos técnicos relevantes deben alimentar el registro de configuración de transición o mini-CMDB. |
| **Evidencia antes que relato** | Ningún procedimiento se considerará validado solo por haber sido explicado. Debe existir documento, ejecución, observación o evidencia. |
| **Separación entre riesgo y mejora** | Los riesgos que comprometen la continuidad se gestionan en la transición; las mejoras deseables pasan al backlog de mejora continua. |
| **Preparación para incidencias** | La revisión técnica debe producir guías de diagnóstico, alertas, logs, errores frecuentes y rutas de escalado. |
| **Preparación para cambios** | La revisión de CI/CD, releases y despliegues debe permitir controlar cambios de forma segura. |
| **Seguridad por diseño operativo** | Accesos, secretos, certificados, datos sensibles y trazas deben revisarse desde la perspectiva de operación segura. |
| **Continuidad verificable** | Backup, restore, RTO, RPO y DR deben estar identificados, aunque su prueba formal se planifique posteriormente. |

# 6. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Revisión de arquitectura técnica global | Mapa técnico inicial validado. |
| Semana 1-2 | Revisión de componentes y repositorios | Matriz aplicación/componente/repositorio. |
| Semana 2-3 | Revisión de build, configuración y ejecución | Guías de build y configuración. |
| Semana 2-4 | Revisión de bases de datos y datos críticos | Matriz de BBDD, esquemas, tablas, lógica y riesgos. |
| Semana 3-5 | Revisión de integraciones técnicas | Matriz técnica de APIs, ficheros, colas y terceros. |
| Semana 4-6 | Revisión de CI/CD, despliegue y rollback | Runbooks de despliegue y rollback. |
| Semana 5-7 | Revisión de observabilidad, logs y operación | Guías de diagnóstico y monitorización. |
| Semana 6-8 | Revisión de seguridad, DR, batch y cierre de gaps | Riesgos técnicos, runbooks y preparación de shadowing. |

---

# 7. Actividad 1. Revisar arquitectura técnica global

## 6.1 Objetivo

Comprender la arquitectura técnica del ecosistema, sus plataformas, capas, dependencias y patrones de integración.

## 6.2 Preguntas clave

- ¿Cuál es la arquitectura global del stack?
- ¿Qué aplicaciones son frontales?
- ¿Qué aplicaciones son backend?
- ¿Qué servicios son compartidos?
- ¿Qué sistemas legacy participan?
- ¿Qué plataformas transversales existen?
- ¿Qué sistemas son síncronos y cuáles batch?
- ¿Qué aplicaciones tienen alta criticidad?
- ¿Qué componentes son single point of failure?
- ¿Qué aplicaciones son 24x7?
- ¿Qué sistemas tienen requisitos especiales de seguridad?
- ¿Qué sistemas tienen datos sensibles?
- ¿Qué dependencias externas son críticas?
- ¿Qué componentes no tienen alternativa?
- ¿Qué decisiones arquitectónicas históricas condicionan el mantenimiento?

## 6.3 Capas a revisar

| Capa | Elementos |
|---|---|
| Canal | Web pública, portal cliente, portal mediador, backoffice. |
| Presentación | Angular, React, ASP.NET, aplicaciones desktop, terminales internos. |
| Servicios | APIs REST, SOAP, microservicios, servicios monolíticos. |
| Negocio | Motores de reglas, lógica de producto, suscripción, siniestros, recibos. |
| Integración | ESB, API Gateway, colas, Kafka, MQ, SFTP, ficheros. |
| Datos | Bases relacionales, NoSQL, DWH, data marts, ficheros. |
| Documental | Gestor documental, plantillas, firma, custodia. |
| Batch | Planificadores, jobs, ETLs, procesos nocturnos. |
| Observabilidad | Monitorización, logs, alertas, trazas. |
| Seguridad | IAM, MFA, certificados, secretos, vault, PAM. |
| Infraestructura | Servidores, contenedores, Kubernetes, cloud, redes. |

## 6.4 Entregables

- Diagrama de arquitectura global.
- Diagrama de dominios técnicos.
- Diagrama de dependencias principales.
- Diagrama de flujos críticos.
- Lista de plataformas compartidas.
- Lista de componentes críticos.
- Lista de riesgos arquitectónicos.
- Lista de gaps técnicos iniciales.

## 6.5 Plantilla de resumen arquitectónico

| Elemento | Descripción |
|---|---|
| Patrón arquitectónico principal | Monolito, microservicios, SOA, legacy, híbrido. |
| Canales principales | Cliente, mediador, backoffice, batch, APIs. |
| Plataformas transversales | API Gateway, ESB, documental, IAM, monitorización. |
| Sistemas core | Pólizas, recibos, siniestros, clientes, contabilidad. |
| Integraciones críticas | Bancos, firma, comunicaciones, reporting, terceros. |
| Datos críticos | Clientes, pólizas, recibos, siniestros, salud, bancarios. |
| Riesgos | Obsolescencia, acoplamiento, SPOF, falta de documentación. |

---

# 8. Actividad 2. Revisar componentes técnicos por aplicación

## 7.1 Objetivo

Entender cómo está construida cada aplicación y qué componentes la forman.

## 7.2 Matriz aplicación / componente

| Aplicación | Componente | Tipo | Tecnología | Versión | Criticidad | Responsable | Observaciones |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | med-front | Frontend | Angular |  | Alta |  |  |
| Portal Mediadores | med-api | Backend | Java Spring |  | Alta |  |  |
| Recibos | rec-batch | Batch | Java / Shell |  | Crítica |  | Proceso nocturno. |
| Siniestros | sin-api | API | .NET |  | Alta |  |  |

## 7.3 Aspectos a revisar

- Tipo de componente.
- Tecnología.
- Versión.
- Framework.
- Estructura del proyecto.
- Dependencias internas.
- Dependencias externas.
- Librerías críticas.
- Parámetros de configuración.
- Gestión de errores.
- Gestión de logs.
- Mecanismos de seguridad.
- Tests existentes.
- Calidad de código.
- Acoplamientos.
- Obsolescencia.
- Propietario.

## 7.4 Preguntas clave

- ¿Qué hace este componente?
- ¿Qué proceso funcional soporta?
- ¿De qué otros componentes depende?
- ¿Quién lo consume?
- ¿Dónde se despliega?
- ¿Cómo se configura?
- ¿Cómo se arranca?
- ¿Cómo se para?
- ¿Dónde escribe logs?
- ¿Cómo se monitoriza?
- ¿Cómo se prueba?
- ¿Cómo se versiona?
- ¿Cómo se despliega?
- ¿Qué errores son frecuentes?
- ¿Qué parte es más delicada?
- ¿Qué conocimiento no está documentado?

## 7.5 Entregables

- Matriz de componentes actualizada.
- Descripción técnica por componente.
- Relación componente/proceso funcional.
- Riesgos por componente.
- Gaps técnicos por componente.

---

# 9. Actividad 3. Revisar repositorios de código fuente

## 8.1 Objetivo

Garantizar que el equipo entrante sabe localizar, leer, compilar, versionar y modificar el código fuente.

## 8.2 Aspectos a revisar

| Área | Revisión |
|---|---|
| Plataforma | GitHub, GitLab, Bitbucket, Azure Repos, SVN. |
| Repositorio | URL, propietario, permisos, estructura. |
| Ramas | main, master, develop, release, hotfix. |
| Estrategia | Gitflow, trunk-based, ramas por versión. |
| Versionado | Tags, releases, convenciones. |
| Calidad | Pull requests, revisiones, linters, análisis estático. |
| Seguridad | Secretos en código, dependencias vulnerables. |
| Documentación | README, guía build, guía run, troubleshooting. |
| Dependencias | Maven, Gradle, npm, NuGet, pip, librerías internas. |
| Actividad | Último commit, frecuencia, autores. |

## 8.3 Preguntas clave

- ¿Qué repositorio corresponde a producción?
- ¿Qué rama representa producción?
- ¿Qué rama se usa para desarrollo?
- ¿Cómo se crean releases?
- ¿Hay tags por versión desplegada?
- ¿Cómo se gestionan hotfixes?
- ¿Quién aprueba pull requests?
- ¿Hay protección de ramas?
- ¿Hay dependencias internas?
- ¿Hay código generado?
- ¿Hay binarios fuera del repositorio?
- ¿Hay configuración fuera del repositorio?
- ¿Hay secretos accidentalmente incluidos?
- ¿Hay documentación para arrancar localmente?
- ¿Hay tests automatizados?

## 8.4 Matriz de repositorios

| Aplicación | Componente | Repositorio | Rama PRO | Estrategia ramas | Último commit | Responsable | Estado |
|---|---|---|---|---|---|---|---|
|  |  |  | main / master | Gitflow / trunk |  |  | Validado / Dudoso |

## 8.5 Acciones concretas

- Validar permisos de lectura.
- Validar permisos de escritura donde proceda.
- Clonar repositorios.
- Revisar estructura del proyecto.
- Revisar README.
- Identificar ramas vivas.
- Identificar tags.
- Identificar versión desplegada en producción.
- Identificar dependencias.
- Revisar configuración.
- Revisar tests.
- Revisar issues o documentación técnica.
- Registrar gaps.

## 8.6 Entregables

- Matriz repositorio/componente.
- Guía de ramas y releases.
- Guía de acceso a repositorios.
- Lista de repositorios huérfanos.
- Lista de aplicaciones sin repositorio claro.
- Lista de riesgos de versionado.

---

# 10. Actividad 4. Revisar build, ejecución local y configuración

## 9.1 Objetivo

Asegurar que el equipo entrante puede preparar un entorno de desarrollo o diagnóstico y generar artefactos de manera reproducible.

## 9.2 Aspectos a revisar

- Requisitos de sistema.
- Versión de lenguaje.
- Versión de framework.
- Gestor de dependencias.
- Comandos de build.
- Comandos de test.
- Comandos de ejecución local.
- Variables de entorno.
- Ficheros de configuración.
- Perfiles por entorno.
- Dependencias locales.
- Dependencias externas simuladas.
- Certificados necesarios.
- Configuración de IDE.
- Errores frecuentes de setup.

## 9.3 Plantilla de guía de build

```markdown
# Guía de build y ejecución

## Aplicación

- Nombre:
- Componente:
- Repositorio:
- Tecnología:
- Rama recomendada:

## Prerrequisitos

- Lenguaje / SDK:
- Gestor de dependencias:
- Herramientas:
- Accesos:
- VPN / red:

## Configuración

- Variables de entorno:
- Ficheros de configuración:
- Perfiles:
- Certificados:
- Dependencias externas:

## Build

```bash
comando de build
```

## Tests

```bash
comando de test
```

## Ejecución local

```bash
comando de ejecución
```

## Verificación

- URL:
- Health check:
- Logs:
- Prueba mínima:

## Problemas frecuentes

| Problema | Causa | Solución |
|---|---|---|
|  |  |  |
```

## 9.4 Preguntas clave

- ¿Puede compilarse el proyecto desde cero?
- ¿Qué versiones exactas se necesitan?
- ¿Hay dependencias privadas?
- ¿Dónde están las credenciales de dependencias?
- ¿Hay librerías internas?
- ¿Hay artefactos que no se pueden reconstruir?
- ¿Hay configuración manual?
- ¿Hay diferencias entre local, DEV, PRE y PRO?
- ¿Hay tests mínimos?
- ¿Qué prueba confirma que el componente arranca correctamente?

## 9.5 Gaps frecuentes

| Gap | Riesgo |
|---|---|
| No compila desde cero | Dependencia crítica del equipo saliente. |
| Dependencias privadas no documentadas | Bloqueo de desarrollo. |
| Configuración manual desconocida | Errores de entorno. |
| No hay datos de prueba | Imposibilidad de validar cambios. |
| No hay tests | Riesgo elevado en mantenimiento. |
| No hay README | Curva de aprendizaje mayor. |

---

# 11. Actividad 5. Revisar configuración por entorno

## 10.1 Objetivo

Entender qué cambia entre entornos y qué configuraciones son críticas.

## 10.2 Elementos de configuración

| Tipo | Ejemplos |
|---|---|
| Variables de entorno | URLs, flags, perfiles, timeouts. |
| Ficheros | application.yml, web.config, properties, XML. |
| Parámetros de servidor | pools, threads, memoria, rutas. |
| Conexiones | BBDD, colas, APIs, SFTP. |
| Seguridad | certificados, tokens, OAuth, claves. |
| Feature flags | Activación de funcionalidades. |
| Parámetros funcionales | Productos, reglas, plantillas, canales. |
| Configuración batch | Calendarios, rutas, dependencias. |

## 10.3 Matriz de configuración

| Aplicación | Entorno | Parámetro | Valor gestionado en | Responsable | Sensible | Observaciones |
|---|---|---|---|---|---|---|
|  | DEV | API_URL | Pipeline / fichero |  | No |  |
|  | PRO | DB_PASSWORD | Vault | Seguridad | Sí | No exponer valor. |
|  | PRE | FEATURE_X | Config server |  | No |  |

## 10.4 Preguntas clave

- ¿Dónde se guarda la configuración?
- ¿Está versionada?
- ¿Quién puede cambiarla?
- ¿Cómo se promueve entre entornos?
- ¿Qué parámetros son sensibles?
- ¿Qué parámetros afectan a negocio?
- ¿Qué parámetros cambian entre PRE y PRO?
- ¿Hay feature flags?
- ¿Hay parámetros hardcodeados?
- ¿Hay configuración en base de datos?
- ¿Hay configuración manual en servidores?

## 10.5 Riesgos frecuentes

| Riesgo | Mitigación |
|---|---|
| Configuración no versionada | Documentar y proponer control. |
| Parámetros hardcodeados | Registrar deuda técnica. |
| Diferencias PRE/PRO | Crear matriz de diferencias. |
| Secretos en ficheros | Migrar a gestor de secretos o registrar plan. |
| Cambios manuales sin trazabilidad | Revisar permisos y procedimiento. |

---

# 12. Actividad 6. Revisar bases de datos y lógica de datos

## 11.1 Objetivo

Entender la estructura de datos, la lógica implementada en base de datos y los riesgos asociados al tratamiento de información sensible.

## 11.2 Aspectos a revisar

- Motor de base de datos.
- Instancias.
- Esquemas.
- Tablas críticas.
- Relaciones principales.
- Vistas.
- Procedimientos almacenados.
- Packages.
- Triggers.
- Jobs.
- Secuencias.
- Índices críticos.
- Particionamiento.
- Volumetría.
- Crecimiento.
- Usuarios técnicos.
- Permisos.
- Backups.
- Replicación.
- Retención.
- Enmascaramiento.
- Auditoría.
- Datos sensibles.

## 11.3 Matriz técnica de bases de datos

| Aplicación | BD | Motor | Esquema | Tablas críticas | Lógica en BD | Datos sensibles | Responsable |
|---|---|---|---|---|---|---|---|
| Emisión | POL_DB | Oracle | POL | POLIZA, TOMADOR | Packages | Sí | DBA |
| Recibos | REC_DB | Oracle | REC | RECIBO, REMESA | Jobs / procedures | Sí | DBA |
| Siniestros | SIN_DB | SQL Server | SIN | EXPEDIENTE, PAGO | Procedures | Sí | DBA |

## 11.4 Preguntas clave

- ¿Qué tablas representan entidades de negocio críticas?
- ¿Dónde se guardan pólizas?
- ¿Dónde se guardan recibos?
- ¿Dónde se guardan siniestros?
- ¿Dónde se guardan clientes y beneficiarios?
- ¿Dónde se guardan datos bancarios?
- ¿Dónde puede haber datos de salud?
- ¿Qué lógica vive en stored procedures?
- ¿Qué procesos batch actualizan datos?
- ¿Qué integraciones escriben directamente?
- ¿Qué aplicaciones comparten tablas?
- ¿Cómo se versionan cambios de modelo?
- ¿Hay scripts manuales recurrentes?
- ¿Qué auditoría existe sobre cambios?
- ¿Cómo se restauran datos?
- ¿Qué datos se enmascaran en PRE?

## 11.5 Revisión de lógica en base de datos

Especial atención a:

- Cálculo de primas.
- Generación de recibos.
- Cambios de estado.
- Renovaciones.
- Liquidaciones.
- Comisiones.
- Reservas de siniestros.
- Pagos.
- Conciliaciones.
- Reporting.
- Procesos de regularización.
- Correcciones manuales.

## 11.6 Entregables

- Matriz técnica de BBDD.
- Diagrama lógico simplificado.
- Lista de tablas críticas.
- Lista de procedimientos críticos.
- Lista de jobs en base de datos.
- Lista de datos sensibles.
- Riesgos de datos y BD.
- Gaps de documentación de datos.

---

# 13. Actividad 7. Revisar integraciones técnicas

## 12.1 Objetivo

Entender cómo se comunican los sistemas, qué protocolos usan, qué datos intercambian, cómo se autentican y cómo se gestionan fallos.

## 12.2 Tipos de integración

| Tipo | Elementos a revisar |
|---|---|
| REST | Endpoints, contratos, autenticación, errores, timeouts. |
| SOAP | WSDL, namespaces, certificados, errores. |
| Ficheros | Rutas, formatos, frecuencia, codificación, control de errores. |
| Mensajería | Colas, topics, consumidores, reintentos, DLQ. |
| Batch | Secuencia, dependencias, ventanas, reprocesos. |
| Base de datos | Lecturas/escrituras compartidas, permisos, riesgos. |
| Terceros | Contrato, SLA, soporte, certificados, entornos de prueba. |

## 12.3 Matriz técnica de integraciones

| Origen | Destino | Tipo | Protocolo | Autenticación | Datos | Frecuencia | Criticidad | Fallos / reproceso |
|---|---|---|---|---|---|---|---|---|
| Emisión | Gestor documental | API | REST | OAuth | Datos póliza | Online | Crítica | Reintento / cola |
| Recibos | Banco | Fichero | SFTP | Certificado | Remesas | Diario | Crítica | Reenvío controlado |
| Siniestros | Peritación | API | SOAP | Certificado | Expediente | Online | Alta | Manual / soporte tercero |

## 12.4 Preguntas clave

- ¿Cuál es el contrato técnico?
- ¿Dónde está documentado?
- ¿Qué sistema inicia la comunicación?
- ¿Es síncrona o asíncrona?
- ¿Qué datos se envían?
- ¿Contiene datos personales?
- ¿Cómo se autentica?
- ¿Qué certificados usa?
- ¿Cuándo caducan?
- ¿Qué timeouts existen?
- ¿Qué errores son habituales?
- ¿Hay reintentos?
- ¿Hay DLQ o cola de errores?
- ¿Cómo se reprocesa?
- ¿Cómo se monitoriza?
- ¿Quién da soporte al sistema destino?
- ¿Hay entorno de pruebas del tercero?

## 12.5 Integraciones críticas típicas en seguros

- Bancos.
- Pasarelas de pago.
- Firma electrónica.
- Gestor documental.
- Mediadores.
- Corredores.
- Sistemas de scoring.
- Sistemas antifraude.
- Peritación.
- Comunicaciones email/SMS.
- Sistemas contables.
- Reporting regulatorio.
- Data Warehouse.
- Sistemas legacy core.
- Sistemas de autenticación corporativa.

## 12.6 Entregables

- Matriz técnica de integraciones.
- Contratos API localizados.
- Inventario de ficheros.
- Inventario de colas/topics.
- Inventario de certificados.
- Procedimientos de reproceso.
- Riesgos por integración.
- Gaps de integración.

---

# 14. Actividad 8. Revisar procesos batch, jobs y planificadores

## 13.1 Objetivo

Entender los procesos no interactivos que soportan operaciones críticas, especialmente recibos, renovaciones, reporting, cierres y conciliaciones.

## 13.2 Tipos de procesos batch

| Tipo | Ejemplos |
|---|---|
| Emisión diferida | Altas masivas, regularizaciones. |
| Renovaciones | Renovación de cartera, generación de avisos. |
| Recibos | Emisión de recibos, remesas, impagos, recobros. |
| Siniestros | Pagos, reservas, cierres, conciliaciones. |
| Documental | Generación masiva de documentos. |
| Comunicaciones | Emails, SMS, cartas. |
| Reporting | DWH, informes financieros, regulatorios. |
| Contabilidad | Asientos, cierres, conciliaciones. |
| Limpieza / retención | Depuración, anonimización, archivado. |

## 13.3 Matriz batch

| Job | Aplicación | Planificador | Frecuencia | Ventana | Dependencias | Criticidad | Reproceso | Responsable |
|---|---|---|---|---|---|---|---|---|
| REC_GENERA | Recibos | Control-M | Diario | Nocturna | Pólizas emitidas | Crítica | Sí | Batch Ops |
| REN_CARTERA | Renovaciones | Control-M | Mensual | Nocturna | Tarifas vigentes | Crítica | Parcial |  |
| DWH_LOAD | Reporting | ETL | Diario | Madrugada | Core sistemas | Alta | Sí | BI |

## 13.4 Preguntas clave

- ¿Qué jobs existen?
- ¿Qué proceso funcional soportan?
- ¿Quién los planifica?
- ¿Dónde se ejecutan?
- ¿Qué dependencias tienen?
- ¿Qué ocurre si fallan?
- ¿Hay alertas?
- ¿Dónde están los logs?
- ¿Cómo se reinician?
- ¿Cómo se reprocesan?
- ¿Qué validaciones funcionales hay al terminar?
- ¿Qué ventanas de negocio tienen?
- ¿Qué jobs son críticos para cierres?
- ¿Qué jobs son críticos para bancos?
- ¿Qué jobs son críticos para reporting regulatorio?

## 13.5 Entregables

- Calendario batch.
- Matriz de jobs.
- Secuencia de dependencias.
- Runbooks de reproceso.
- Lista de jobs críticos.
- Lista de alertas batch.
- Riesgos de batch.

---

# 15. Actividad 9. Revisar CI/CD, despliegues y rollback

## 14.1 Objetivo

Entender cómo se construyen, validan y despliegan las aplicaciones, y cómo se revierte un cambio fallido.

## 14.2 Aspectos a revisar

- Herramienta CI/CD.
- Pipeline de build.
- Pipeline de test.
- Pipeline de análisis de calidad.
- Pipeline de seguridad.
- Pipeline de despliegue.
- Artefactos generados.
- Repositorio de artefactos.
- Promoción entre entornos.
- Aprobaciones.
- Ventanas de despliegue.
- Despliegue manual.
- Scripts.
- Configuración.
- Variables.
- Secretos.
- Rollback.
- Validación postdespliegue.
- Comunicación a negocio.
- Gestión de cambios.

## 14.3 Matriz de despliegue

| Aplicación | Componente | Pipeline | Artefacto | Entornos | Aprobación | Rollback | Validación postdespliegue |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | Front |  |  | DEV/PRE/PRO | Sí | Versión anterior | Smoke test |
| Recibos | Batch |  |  | PRE/PRO | Sí | Script anterior | Validación job |
| Emisión | API |  |  | DEV/PRE/PRO | Sí | Redeploy tag | Health check |

## 14.4 Preguntas clave

- ¿Cómo se genera el artefacto?
- ¿Dónde se almacena?
- ¿Cómo se despliega en DEV?
- ¿Cómo se despliega en PRE?
- ¿Cómo se despliega en PRO?
- ¿Quién aprueba?
- ¿Qué evidencias se requieren?
- ¿Qué validaciones se hacen antes?
- ¿Qué validaciones se hacen después?
- ¿Cómo se identifica la versión desplegada?
- ¿Cómo se revierte?
- ¿Cuánto tarda un rollback?
- ¿Qué despliegues son manuales?
- ¿Qué errores son frecuentes?
- ¿Qué cambios requieren parada?
- ¿Qué cambios requieren comunicación a negocio?
- ¿Qué cambios requieren CAB?

## 14.5 Plantilla de runbook de despliegue

```markdown
# Runbook de despliegue

## Aplicación

- Nombre:
- Componente:
- Entorno:
- Responsable:
- Ventana de despliegue:

## Prerrequisitos

- Ticket de cambio:
- Rama / tag:
- Artefacto:
- Aprobaciones:
- Backup previo:
- Comunicación:

## Pasos de despliegue

1.
2.
3.

## Validaciones previas

- 
- 

## Validaciones posteriores

- Health check:
- Logs:
- Smoke test:
- Validación funcional:
- Monitorización:

## Rollback

1.
2.
3.

## Criterios de éxito

## Criterios de rollback

## Contactos de escalado

## Evidencias
```

## 14.6 Entregables

- Matriz CI/CD.
- Runbooks de despliegue.
- Procedimientos de rollback.
- Lista de despliegues manuales.
- Lista de riesgos de despliegue.
- Validaciones postdespliegue.
- Gaps de automatización.

---

# 16. Actividad 10. Revisar monitorización, logs y diagnóstico

## 15.1 Objetivo

Capacitar al equipo entrante para detectar y diagnosticar incidencias técnicas y funcionales.

## 15.2 Elementos a revisar

- Herramientas APM.
- Dashboards.
- Alertas.
- Umbrales.
- Logs de aplicación.
- Logs de servidor.
- Logs de integración.
- Logs batch.
- Trazas distribuidas.
- Correlation ID.
- Métricas técnicas.
- Métricas funcionales.
- Retención de logs.
- Alertas recurrentes.
- Falsos positivos.
- Runbooks asociados.

## 15.3 Matriz de observabilidad

| Aplicación | Herramienta | Dashboard | Logs | Alertas | Correlation ID | Runbook | Responsable |
|---|---|---|---|---|---|---|---|
| Portal Mediadores | Dynatrace |  | Splunk | Sí | Sí | Parcial | Operaciones |
| Recibos | Control-M |  | Ficheros / Splunk | Sí | No aplica | Sí | Batch Ops |
| Siniestros | Grafana |  | ELK | Sí | Parcial | No |  |

## 15.4 Preguntas clave

- ¿Cómo se detecta que la aplicación está caída?
- ¿Qué alertas existen?
- ¿Qué alertas son críticas?
- ¿Qué alertas generan ruido?
- ¿Quién recibe las alertas?
- ¿Dónde se consultan logs?
- ¿Cómo se filtra por operación?
- ¿Existe correlation ID?
- ¿Cómo se sigue una operación entre sistemas?
- ¿Cómo se diagnostica una integración caída?
- ¿Cómo se diagnostica un batch fallido?
- ¿Qué dashboards usa el equipo saliente?
- ¿Qué métricas mira primero?
- ¿Qué errores son habituales?
- ¿Qué logs contienen datos personales?
- ¿Cuánto tiempo se conservan logs?

## 15.5 Guía mínima de diagnóstico

Para cada aplicación crítica debe existir una guía con:

- Síntomas habituales.
- Alertas asociadas.
- Dashboard principal.
- Logs principales.
- Búsquedas útiles.
- Errores frecuentes.
- Relación error/causa probable.
- Validaciones funcionales.
- Validaciones técnicas.
- Escalado.
- Workaround.
- Cuándo activar incidencia mayor.

## 15.6 Entregables

- Matriz de observabilidad.
- Guías de diagnóstico.
- Dashboards identificados.
- Catálogo de alertas.
- Búsquedas de logs útiles.
- Lista de falsos positivos.
- Riesgos de observabilidad.
- Gaps de monitorización.

---

# 17. Actividad 11. Revisar seguridad técnica, accesos, secretos y certificados

## 16.1 Objetivo

Entender cómo se protegen los sistemas, cómo se gestionan accesos técnicos, secretos, certificados y cuentas de servicio.

## 16.2 Aspectos a revisar

- Autenticación.
- Autorización.
- Roles.
- Accesos a entornos.
- Accesos a producción.
- Cuentas técnicas.
- Cuentas de servicio.
- MFA.
- PAM.
- VPN.
- Bastiones.
- Secretos.
- Vault.
- Certificados.
- API keys.
- Tokens.
- Rotación.
- Caducidades.
- Auditoría.
- Segregación de funciones.
- Datos personales.
- Datos especialmente sensibles.

## 16.3 Matriz de secretos y certificados

> Esta matriz no debe contener valores secretos. Solo debe registrar metadatos, responsables y caducidades.

| Aplicación | Tipo | Uso | Ubicación segura | Responsable | Caducidad | Criticidad | Observaciones |
|---|---|---|---|---|---|---|---|
| Emisión | Certificado | Firma integración | Vault | Seguridad |  | Alta |  |
| Recibos | Credencial SFTP | Banco | Vault | Seguridad |  | Crítica |  |
| Portal | OAuth client | Login | IAM | IAM |  | Alta |  |

## 16.4 Preguntas clave

- ¿Qué mecanismos de autenticación usa la aplicación?
- ¿Cómo se autorizan usuarios?
- ¿Qué roles existen?
- ¿Qué cuentas técnicas existen?
- ¿Qué secretos usa la aplicación?
- ¿Dónde se almacenan?
- ¿Quién puede leerlos?
- ¿Quién puede rotarlos?
- ¿Cuándo caducan certificados?
- ¿Hay alertas de caducidad?
- ¿Hay secretos en código o pipeline?
- ¿Cómo se accede a producción?
- ¿Hay segregación de funciones?
- ¿Qué datos sensibles trata la aplicación?
- ¿Qué logs pueden contener datos personales?
- ¿Qué evidencias requiere auditoría?

## 16.5 Riesgos frecuentes

| Riesgo | Mitigación |
|---|---|
| Secretos en código | Registrar riesgo, retirar y rotar. |
| Certificados sin control de caducidad | Crear calendario y alertas. |
| Cuentas compartidas | Migrar a cuentas nominales o controladas. |
| Accesos excesivos | Revisar mínimo privilegio. |
| Falta de auditoría | Escalar a seguridad/compliance. |
| Logs con datos sensibles | Revisar mascarado y retención. |

---

# 18. Actividad 12. Revisar backup, restore y recuperación

## 17.1 Objetivo

Conocer los mecanismos de respaldo, restauración y recuperación ante desastres.

## 17.2 Aspectos a revisar

- Política de backup.
- Frecuencia.
- Tipo de backup.
- Sistemas cubiertos.
- Bases de datos cubiertas.
- Configuración respaldada.
- Documentos respaldados.
- Retención.
- Cifrado.
- Pruebas de restore.
- RTO.
- RPO.
- DRP.
- BCP.
- Secuencia de recuperación.
- Responsables.
- Dependencias.
- Evidencias de pruebas.

## 17.3 Matriz de recuperación

| Aplicación | Elemento | Backup | Frecuencia | RPO | RTO | Restore probado | Responsable |
|---|---|---|---|---|---|---|---|
| Emisión | BD pólizas | Sí | Diario / incremental |  |  |  | DBA |
| Documental | Repositorio documentos | Sí |  |  |  |  | Infra |
| Recibos | BD recibos | Sí |  |  |  |  | DBA |

## 17.4 Preguntas clave

- ¿Qué se respalda?
- ¿Qué no se respalda?
- ¿Cada cuánto?
- ¿Dónde se guarda?
- ¿Está cifrado?
- ¿Quién puede restaurar?
- ¿Cuándo se probó el último restore?
- ¿Cuál es el RTO?
- ¿Cuál es el RPO?
- ¿Existe DR?
- ¿Cuál es el orden de recuperación?
- ¿Qué dependencias externas afectan?
- ¿Qué ocurre con documentos contractuales?
- ¿Qué ocurre con datos de recibos o siniestros?
- ¿Qué evidencias se requieren para auditoría?

## 17.5 Entregables

- Matriz backup/restore.
- Procedimientos de recuperación.
- Evidencias de pruebas existentes.
- Lista de gaps DR.
- Lista de riesgos de continuidad.
- Preguntas pendientes para operaciones/infraestructura.

---

# 19. Actividad 13. Revisar deuda técnica, obsolescencia y riesgos

## 18.1 Objetivo

Identificar riesgos técnicos que puedan afectar a la operación futura del servicio.

## 18.2 Tipos de deuda técnica

| Tipo | Ejemplos |
|---|---|
| Obsolescencia | Framework fuera de soporte, servidor antiguo, versión legacy. |
| Acoplamiento | Dependencias directas entre sistemas sin contrato claro. |
| Código | Código sin tests, duplicado, sin modularidad. |
| Despliegue | Manual, no reproducible, sin rollback. |
| Datos | Modelo no documentado, lógica en BD, datos duplicados. |
| Seguridad | Secretos en código, cuentas compartidas, certificados sin control. |
| Observabilidad | Sin logs útiles, sin alertas, sin dashboards. |
| Documentación | Sin runbook, sin arquitectura, sin guía de diagnóstico. |
| Personas | Conocimiento en una única persona. |
| Integraciones | Terceros sin entorno de pruebas o sin SLA claro. |

## 18.3 Matriz de riesgos técnicos

| ID | Aplicación | Riesgo | Tipo | Impacto | Probabilidad | Mitigación | Prioridad |
|---|---|---|---|---|---|---|---|
| RT-001 | Recibos | Batch crítico sin runbook | Operación | Alto | Alta | Documentar y observar ejecución | Alta |
| RT-002 | Emisión | Rollback no probado | Despliegue | Alto | Media | Ejecutar prueba en PRE | Alta |
| RT-003 | Portal | Framework fuera de soporte | Obsolescencia | Medio | Alta | Plan de actualización | Media |

## 18.4 Priorización

Priorizar riesgos que afecten a:

- Producción.
- Cliente final.
- Emisión.
- Recibos.
- Siniestros.
- Documentación contractual.
- Datos personales.
- Cumplimiento.
- Disponibilidad.
- Recuperación.
- Despliegues.
- Integraciones externas críticas.

## 18.5 Entregables

- Registro de deuda técnica.
- Registro de riesgos técnicos.
- Recomendaciones de mitigación.
- Quick wins técnicos.
- Riesgos que deben escalarse al comité.
- Riesgos que bloquean shadowing o reverse shadowing.

---

# 20. Actividad 14. Crear runbooks técnicos iniciales

## 19.1 Objetivo

Consolidar el conocimiento técnico necesario para operar cada aplicación crítica.

## 19.2 Runbook mínimo por aplicación crítica

```markdown
# Runbook técnico

## Identificación

- Aplicación:
- Código:
- Dominio funcional:
- Criticidad:
- Responsable técnico:
- Responsable funcional:
- Estado:

## Arquitectura resumida

## Componentes

| Componente | Tipo | Tecnología | Repositorio | Entorno |
|---|---|---|---|---|

## Repositorios

## Build

## Configuración

## Entornos

## Bases de datos

## Integraciones

## Procesos batch

## Despliegue

## Rollback

## Monitorización

## Logs

## Alertas

## Diagnóstico rápido

| Síntoma | Validación | Posible causa | Acción |
|---|---|---|---|

## Incidencias técnicas frecuentes

## Workarounds

## Backup y recuperación

## Seguridad

## Contactos de escalado

## Riesgos conocidos

## Gaps pendientes

## Evidencias de validación
```

## 19.3 Reglas para crear runbooks útiles

- Deben ser accionables.
- Deben indicar dónde mirar.
- Deben incluir comandos si procede.
- Deben evitar información secreta.
- Deben tener responsable.
- Deben tener fecha de revisión.
- Deben separar producción de no producción.
- Deben incluir criterios de escalado.
- Deben incluir validaciones funcionales mínimas.
- Deben actualizarse tras shadowing y reverse shadowing.

---

# 21. Actividad 15. Preparar casos para shadowing operativo

## 20.1 Objetivo

Definir qué actividades reales debe observar el equipo entrante durante la Fase 4.

## 20.2 Casos candidatos

| Tipo de caso | Ejemplo |
|---|---|
| Incidencia técnica | Error 500 en portal, caída API, timeout integración. |
| Incidencia funcional-técnica | Recibo no generado, documento incorrecto, póliza bloqueada. |
| Despliegue | Release de API, frontend, batch o configuración. |
| Batch | Ejecución nocturna, fallo y reproceso. |
| Integración | Error con banco, firma, documental o tercero. |
| Monitorización | Alerta crítica, falso positivo, degradación. |
| Datos | Corrección controlada, consulta, validación de estado. |
| Seguridad | Renovación certificado, revisión acceso, secreto. |
| DR / restore | Simulacro o revisión de procedimiento. |

## 20.3 Matriz de casos para shadowing

| Caso | Aplicación | Tipo | Criticidad | Qué observar | Responsable saliente | Fecha prevista |
|---|---|---|---|---|---|---|
| Despliegue API emisión | Emisión | Despliegue | Alta | Pipeline, validaciones, rollback |  |  |
| Fallo batch recibos | Recibos | Batch | Crítica | Diagnóstico, logs, reproceso |  |  |
| Error documental | Documental | Incidencia | Alta | Trazabilidad, regeneración |  |  |

## 20.4 Resultado esperado

- Lista priorizada de casos de shadowing.
- Responsables salientes asignados.
- Fechas tentativas.
- Evidencias a capturar.
- Relación con runbooks.

---


# 22. Actividad 16. Validar preparación operativa técnica

## 22.1 Objetivo

Validar que el conocimiento técnico adquirido durante la Fase 3 es suficiente para que el equipo entrante pueda observar y participar con criterio en la operación real durante la Fase 4.

Esta actividad actúa como un **Operational Readiness Review técnico**. No pretende certificar autonomía plena, sino confirmar que existen las condiciones mínimas para avanzar hacia shadowing sin depender exclusivamente de explicaciones informales del equipo saliente.

## 22.2 Dimensiones de validación

| Dimensión | Pregunta de control |
|---|---|
| Arquitectura | ¿El equipo entiende cómo encaja la aplicación en el ecosistema? |
| Código | ¿El equipo sabe localizar el repositorio, ramas, versión productiva y puntos críticos? |
| Build | ¿Existe guía para compilar, probar o generar artefactos? |
| Configuración | ¿Están identificados parámetros por entorno, secretos y diferencias relevantes? |
| Datos | ¿Se conocen BBDD, esquemas, tablas críticas, lógica en BD y datos sensibles? |
| Integraciones | ¿Se conocen sistemas origen/destino, protocolos, errores, reprocesos y responsables? |
| Batch | ¿Están identificados jobs, secuencias, ventanas, logs, alertas y reprocesos? |
| Despliegue | ¿Se conoce el proceso de despliegue, aprobación, validación y rollback? |
| Observabilidad | ¿Se conocen dashboards, logs, alertas, búsquedas útiles y escalados? |
| Seguridad | ¿Se conocen accesos, cuentas técnicas, certificados, secretos y caducidades? |
| Continuidad | ¿Se conocen backup, restore, DR, RTO, RPO y responsables? |
| Riesgos | ¿Están registrados los gaps y riesgos técnicos que condicionan la operación? |

## 22.3 Checklist de readiness técnico por aplicación crítica

| Criterio | Estado | Evidencia | Observaciones |
|---|---|---|---|
| Arquitectura revisada | Pendiente / Parcial / Validado |  |  |
| Componentes identificados | Pendiente / Parcial / Validado |  |  |
| Repositorio y rama productiva identificados | Pendiente / Parcial / Validado |  |  |
| Build documentado o ejecutado | Pendiente / Parcial / Validado |  |  |
| Configuración por entorno identificada | Pendiente / Parcial / Validado |  |  |
| BBDD y tablas críticas identificadas | Pendiente / Parcial / Validado |  |  |
| Integraciones técnicas identificadas | Pendiente / Parcial / Validado |  |  |
| Jobs y batch críticos identificados | Pendiente / Parcial / Validado |  |  |
| Despliegue documentado | Pendiente / Parcial / Validado |  |  |
| Rollback documentado | Pendiente / Parcial / Validado |  |  |
| Logs y dashboards localizados | Pendiente / Parcial / Validado |  |  |
| Alertas críticas identificadas | Pendiente / Parcial / Validado |  |  |
| Secretos y certificados inventariados | Pendiente / Parcial / Validado |  |  |
| Backup/restore revisado | Pendiente / Parcial / Validado |  |  |
| Runbook técnico inicial creado | Pendiente / Parcial / Validado |  |  |
| Riesgos técnicos registrados | Pendiente / Parcial / Validado |  |  |
| Casos de shadowing definidos | Pendiente / Parcial / Validado |  |  |

## 22.4 Estados recomendados de preparación técnica

| Estado | Significado |
|---|---|
| No iniciado | No se ha revisado técnicamente la aplicación. |
| Identificado | Se conocen componentes principales, pero sin validación suficiente. |
| Documentado | Existe documentación técnica mínima, pero no contrastada. |
| Contrastado | La información ha sido revisada con expertos o evidencias. |
| Ejecutado / observado | Se ha ejecutado o observado el procedimiento en un entorno real o controlado. |
| Preparado para shadowing | Hay conocimiento suficiente para observar operación real con criterio. |
| Bloqueado | Existen gaps críticos que impiden avanzar con seguridad. |

## 22.5 Criterio de aceptación de readiness técnico

Una aplicación crítica podrá considerarse preparada para la Fase 4 cuando:

- Exista arquitectura mínima entendida y documentada.
- El equipo entrante conozca repositorios, ramas y versión productiva.
- Se conozcan despliegues, rollback, logs, alertas y escalados.
- Se hayan identificado BBDD, integraciones, batch y configuraciones críticas.
- Los accesos necesarios para observación y diagnóstico estén solicitados o disponibles.
- Los riesgos técnicos estén registrados.
- Existan casos concretos para observar durante shadowing.

---

# 23. Entregables de la Fase 3

## 21.1 Entregables principales

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Mapa de arquitectura técnica | Vista global y por dominio. | Arquitecto / líder técnico |
| Matriz aplicación-componente | Componentes, tecnologías y criticidad. | Líder técnico |
| Matriz de repositorios | Repos, ramas, permisos y estado. | Líder técnico |
| Guías de build | Cómo compilar y ejecutar componentes. | Equipo técnico entrante |
| Matriz de configuración | Configuración por entorno. | DevOps / líder técnico |
| Matriz de bases de datos | BD, esquemas, tablas, lógica, datos sensibles. | DBA / líder técnico |
| Matriz de integraciones técnicas | APIs, ficheros, colas, terceros. | Arquitectura / líder técnico |
| Matriz batch | Jobs, dependencias, ventanas y reprocesos. | Operaciones / líder técnico |
| Matriz CI/CD | Pipelines, artefactos, despliegues y rollback. | DevOps |
| Runbooks de despliegue | Procedimientos por aplicación crítica. | DevOps / equipo técnico |
| Matriz de observabilidad | Dashboards, logs, alertas y diagnóstico. | Operaciones |
| Matriz de secretos/certificados | Metadatos, responsables y caducidades. | Seguridad |
| Matriz backup/restore | RTO, RPO, restore y DR. | Infra / DBA |
| Registro de riesgos técnicos | Riesgos y deuda técnica priorizada. | Líder técnico |
| Runbooks técnicos iniciales | Guías operativas por aplicación crítica. | Equipo entrante |
| Casos para shadowing | Actividades a observar en Fase 4. | Transition Manager |

---


## 23.2 Entregables ITIL específicos

| Entregable ITIL | Descripción | Práctica ITIL relacionada |
|---|---|---|
| Registro técnico de configuración | Relación de servicios, aplicaciones, componentes, entornos, BBDD, integraciones, jobs y responsables. | Service Configuration Management |
| Matriz de trazabilidad técnica | Relación entre código, artefacto, release, despliegue, cambio y servicio afectado. | Release Management / Change Enablement |
| Registro de activos técnicos relevantes | Herramientas, plataformas, licencias, certificados, cuentas técnicas, servidores y componentes clave. | IT Asset Management |
| Catálogo técnico de errores frecuentes | Síntomas, logs, causas probables, validaciones y acciones iniciales. | Incident Management |
| Registro de problemas técnicos recurrentes | Problemas conocidos, causa raíz, workaround, impacto y solución recomendada. | Problem Management |
| Catálogo de alertas críticas | Alertas, umbrales, severidad, responsable, acción esperada y escalado. | Monitoring and Event Management |
| Matriz de preparación técnica | Estado de readiness técnico por aplicación crítica. | Service Validation / Knowledge Management |
| Backlog de mejoras técnicas | Mejoras de automatización, observabilidad, documentación, seguridad y reducción de deuda. | Continual Improvement |

## 23.3 Relación entre entregables técnicos y prácticas ITIL

| Área técnica | Entregable | Práctica ITIL principal |
|---|---|---|
| Arquitectura | Diagramas, dependencias y plataformas | Architecture Management |
| Componentes | Matriz aplicación-componente | Service Configuration Management |
| Repositorios | Matriz repositorio/rama/tag | Release Management |
| Build | Guías de build y ejecución | Knowledge Management |
| Configuración | Matriz de parámetros por entorno | Service Configuration Management |
| Despliegue | Runbook de despliegue y rollback | Deployment Management |
| Cambios | Evidencias, aprobaciones y CAB | Change Enablement |
| Observabilidad | Dashboards, logs y alertas | Monitoring and Event Management |
| Incidencias | Diagnóstico y errores frecuentes | Incident Management |
| Problemas | Deuda técnica y causa raíz | Problem Management |
| Seguridad | Secretos, certificados y accesos | Information Security Management |
| Continuidad | Backup, restore y DR | Service Continuity Management |

# 24. Plantillas útiles de la Fase 3

## 22.1 Matriz técnica consolidada

| Aplicación | Componente | Tecnología | Repositorio | Pipeline | BBDD | Integraciones | Logs | Criticidad | Gaps |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |

## 22.2 Matriz de gaps técnicos

| ID | Aplicación | Gap | Tipo | Criticidad | Responsable | Acción | Fecha objetivo | Estado |
|---|---|---|---|---|---|---|---|---|
| GT-001 |  | No hay rollback documentado | Despliegue | Alta |  | Documentar y validar |  | Abierto |
| GT-002 |  | No se puede compilar localmente | Build | Alta |  | Sesión técnica |  | Abierto |

## 22.3 Matriz de errores frecuentes

| Aplicación | Síntoma | Log / alerta | Causa probable | Validación | Acción |
|---|---|---|---|---|---|
|  | Error 500 |  | Timeout integración | Revisar endpoint | Escalar / reintentar |
|  | Batch fallido |  | Datos inconsistentes | Revisar input | Reproceso |

## 22.4 Matriz de dependencias técnicas

| Aplicación | Depende de | Tipo | Criticidad | Qué ocurre si falla | Monitorización | Escalado |
|---|---|---|---|---|---|---|
|  | Banco | SFTP | Crítica | No se envían remesas | Alerta batch | Proveedor banco |
|  | Documental | API | Alta | No se generan contratos | APM | Equipo documental |

---


## 24.5 Registro técnico de configuración del servicio

| Servicio | Aplicación | Componente | Tipo CI | Entorno | Tecnología | Responsable | Dependencias | Estado validación | Riesgo asociado |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  | Aplicación / API / Batch / BD / Cola / Servidor / Certificado | DEV / PRE / PRO |  |  |  | Identificado / Contrastado / Validado |  |

## 24.6 Matriz de trazabilidad release / cambio / despliegue

| Aplicación | Componente | Repositorio | Rama / tag | Artefacto | Cambio asociado | Entorno | Fecha despliegue | Validación | Rollback |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  | CHG- | DEV / PRE / PRO |  | Pendiente / OK / KO | Documentado / No documentado |

## 24.7 Registro de problemas técnicos recurrentes

| ID | Aplicación | Problema | Síntoma | Causa raíz conocida | Workaround | Impacto | Acción recomendada | Estado |
|---|---|---|---|---|---|---|---|---|
| PRB-T-001 |  |  |  | Conocida / Pendiente |  | Alto / Medio / Bajo |  | Abierto / En análisis / Mitigado |

## 24.8 Catálogo de alertas críticas

| Aplicación | Alerta | Herramienta | Severidad | Umbral | Acción inicial | Escalado | Runbook |
|---|---|---|---|---|---|---|---|
|  |  | Dynatrace / Splunk / Grafana / Control-M | Crítica / Alta / Media |  |  |  |  |

## 24.9 Registro de mejoras técnicas

| ID | Aplicación | Mejora | Origen | Beneficio esperado | Prioridad | Esfuerzo | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| MT-001 |  |  | Riesgo / Gap / Incidencia / Shadowing |  | Alta / Media / Baja | Bajo / Medio / Alto |  | Propuesta / Aprobada / En curso |

# 25. Checklist operativo de Fase 3

## 23.1 Arquitectura

- [ ] Revisar arquitectura global.
- [ ] Revisar diagramas existentes.
- [ ] Crear diagramas faltantes.
- [ ] Identificar capas.
- [ ] Identificar plataformas compartidas.
- [ ] Identificar sistemas core.
- [ ] Identificar sistemas legacy.
- [ ] Identificar single points of failure.
- [ ] Identificar dependencias críticas.
- [ ] Validar arquitectura con expertos.

## 23.2 Componentes y código

- [ ] Identificar componentes por aplicación.
- [ ] Identificar tecnologías.
- [ ] Identificar versiones.
- [ ] Identificar frameworks.
- [ ] Revisar estructura de código.
- [ ] Revisar dependencias.
- [ ] Revisar librerías internas.
- [ ] Revisar tests.
- [ ] Revisar gestión de errores.
- [ ] Revisar logs.
- [ ] Revisar deuda técnica.
- [ ] Registrar gaps.

## 23.3 Repositorios

- [ ] Validar repositorios.
- [ ] Validar permisos.
- [ ] Clonar repositorios.
- [ ] Identificar ramas.
- [ ] Identificar tags.
- [ ] Identificar versión productiva.
- [ ] Revisar README.
- [ ] Revisar estrategia de ramas.
- [ ] Revisar pull requests.
- [ ] Revisar protección de ramas.
- [ ] Revisar secretos en código.
- [ ] Registrar riesgos.

## 23.4 Build y configuración

- [ ] Identificar prerrequisitos.
- [ ] Identificar SDKs.
- [ ] Identificar gestores de dependencias.
- [ ] Ejecutar build en entorno controlado.
- [ ] Ejecutar tests si existen.
- [ ] Ejecutar aplicación local o en DEV si aplica.
- [ ] Documentar comandos.
- [ ] Identificar variables.
- [ ] Identificar perfiles.
- [ ] Identificar certificados.
- [ ] Identificar diferencias de entorno.
- [ ] Registrar problemas.

## 23.5 Bases de datos

- [ ] Identificar motores.
- [ ] Identificar instancias.
- [ ] Identificar esquemas.
- [ ] Identificar tablas críticas.
- [ ] Identificar procedimientos.
- [ ] Identificar triggers.
- [ ] Identificar jobs.
- [ ] Identificar usuarios técnicos.
- [ ] Identificar datos sensibles.
- [ ] Identificar backups.
- [ ] Identificar restore.
- [ ] Revisar cambios de modelo.
- [ ] Registrar riesgos.

## 23.6 Integraciones

- [ ] Identificar APIs REST.
- [ ] Identificar SOAP.
- [ ] Identificar ficheros.
- [ ] Identificar colas.
- [ ] Identificar topics.
- [ ] Identificar integraciones batch.
- [ ] Identificar terceros.
- [ ] Identificar autenticación.
- [ ] Identificar certificados.
- [ ] Identificar timeouts.
- [ ] Identificar errores frecuentes.
- [ ] Identificar reprocesos.
- [ ] Registrar gaps.

## 23.7 Batch

- [ ] Identificar planificador.
- [ ] Identificar jobs.
- [ ] Identificar secuencias.
- [ ] Identificar dependencias.
- [ ] Identificar ventanas.
- [ ] Identificar logs.
- [ ] Identificar alertas.
- [ ] Identificar validaciones.
- [ ] Identificar reprocesos.
- [ ] Identificar responsables.
- [ ] Documentar jobs críticos.

## 23.8 CI/CD y despliegue

- [ ] Identificar pipelines.
- [ ] Identificar artefactos.
- [ ] Identificar repositorio de artefactos.
- [ ] Identificar triggers.
- [ ] Identificar gates.
- [ ] Identificar aprobaciones.
- [ ] Identificar despliegues manuales.
- [ ] Identificar validaciones pre.
- [ ] Identificar validaciones post.
- [ ] Identificar rollback.
- [ ] Documentar runbooks.
- [ ] Registrar riesgos.

## 23.9 Observabilidad

- [ ] Identificar APM.
- [ ] Identificar dashboards.
- [ ] Identificar logs.
- [ ] Identificar alertas.
- [ ] Identificar umbrales.
- [ ] Identificar correlation ID.
- [ ] Identificar búsquedas útiles.
- [ ] Identificar falsos positivos.
- [ ] Identificar alertas críticas.
- [ ] Documentar guías de diagnóstico.
- [ ] Registrar gaps.

## 23.10 Seguridad y continuidad

- [ ] Identificar mecanismos de autenticación.
- [ ] Identificar roles.
- [ ] Identificar cuentas técnicas.
- [ ] Identificar secretos.
- [ ] Identificar certificados.
- [ ] Identificar caducidades.
- [ ] Identificar accesos PRO.
- [ ] Identificar PAM/VPN/bastión.
- [ ] Identificar backups.
- [ ] Identificar RTO/RPO.
- [ ] Identificar restore.
- [ ] Identificar DR.
- [ ] Registrar riesgos.

---


## 25.11 Checklist ITIL de Fase 3

- [ ] Relacionar componentes técnicos con servicios de negocio.
- [ ] Identificar elementos de configuración técnicos relevantes.
- [ ] Alimentar o actualizar la mini-CMDB de transición.
- [ ] Confirmar propietarios técnicos por componente crítico.
- [ ] Identificar activos técnicos relevantes.
- [ ] Revisar trazabilidad código / artefacto / release / despliegue.
- [ ] Identificar cambios técnicos recientes y cambios previstos durante la transición.
- [ ] Confirmar si los despliegues siguen proceso formal de cambio.
- [ ] Identificar procedimientos de validación postdespliegue.
- [ ] Identificar procedimientos de rollback.
- [ ] Crear catálogo inicial de alertas críticas.
- [ ] Crear guía de diagnóstico para aplicaciones críticas.
- [ ] Registrar problemas técnicos recurrentes.
- [ ] Registrar workarounds técnicos conocidos.
- [ ] Revisar riesgos de seguridad técnica.
- [ ] Revisar riesgos de continuidad técnica.
- [ ] Crear matriz de readiness técnico por aplicación crítica.
- [ ] Definir casos técnicos prioritarios para shadowing.
- [ ] Registrar mejoras técnicas para backlog de mejora continua.

# 26. Riesgos específicos de la Fase 3

| Riesgo | Impacto | Mitigación |
|---|---|---|
| No se puede compilar el código | Bloqueo para mantenimiento | Sesión técnica específica, documentar dependencias y entorno. |
| No hay trazabilidad versión-producción | Dificultad de diagnóstico y rollback | Identificar tags, artefactos y despliegues reales. |
| Despliegue manual no documentado | Alto riesgo operativo | Crear runbook y observar despliegue en shadowing. |
| Rollback inexistente o no probado | Riesgo ante cambios fallidos | Documentar y probar en PRE si es posible. |
| Lógica crítica en base de datos | Riesgo de cambios no controlados | Inventariar procedures, triggers y jobs. |
| Integraciones externas sin contrato técnico | Fallos difíciles de resolver | Localizar documentación, contactos y SLAs. |
| Procesos batch sin runbook | Riesgo en cierres, recibos o reporting | Documentar secuencia, logs y reproceso. |
| Observabilidad insuficiente | Diagnóstico lento | Crear guías de logs y proponer mejoras. |
| Secretos mal gestionados | Riesgo de seguridad | Revisar vault, rotación y permisos. |
| Certificados sin control | Riesgo de caída por caducidad | Crear calendario de caducidades. |
| Datos sensibles en logs | Riesgo GDPR | Revisar mascarado, retención y acceso. |
| Dependencia de experto saliente | Riesgo de continuidad | Capturar sesiones y validar con práctica. |
| Entornos no equivalentes | Pruebas poco fiables | Documentar diferencias y ajustar validaciones. |
| Deuda técnica severa | Riesgo futuro | Registrar, priorizar y separar de transición. |

---



## 26.1 Riesgos ITIL adicionales

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Elementos de configuración no relacionados con servicio de negocio | Dificulta priorizar incidencias y cambios | Mantener matriz servicio / aplicación / componente. |
| Activos técnicos sin propietario | Riesgo de soporte y escalado | Asignar responsable temporal y registrar gap. |
| Cambios técnicos durante la transición sin visibilidad | Riesgo de aprender información obsoleta | Revisar calendario de cambios y releases semanalmente. |
| No existe relación entre cambio, release, artefacto y despliegue | Dificultad de auditoría y rollback | Crear matriz de trazabilidad release / cambio / despliegue. |
| Alertas críticas sin runbook | Respuesta inconsistente ante eventos | Crear catálogo de alertas y acción inicial. |
| Problemas recurrentes tratados como incidencias aisladas | Repetición de fallos y pérdida de conocimiento | Crear registro de problemas técnicos recurrentes. |
| Riesgos técnicos no conectados con mejora continua | Se pierden oportunidades de estabilización | Trasladar deuda y mejoras al backlog de mejora continua. |

# 27. Criterios de salida de la Fase 3

## 25.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Arquitectura técnica revisada | Diagramas y actas | Pendiente / En curso / Validado |
| Componentes identificados | Matriz aplicación-componente |  |
| Repositorios validados | Matriz de repositorios |  |
| Estrategia de ramas entendida | Documento de versionado |  |
| Build documentado | Guías de build |  |
| Configuración por entorno identificada | Matriz de configuración |  |
| Bases de datos revisadas | Matriz de BBDD |  |
| Lógica en BD identificada | Lista de procedures/triggers/jobs |  |
| Integraciones técnicas revisadas | Matriz de integraciones |  |
| Procesos batch identificados | Matriz batch |  |
| CI/CD revisado | Matriz de pipelines |  |
| Despliegues documentados | Runbooks de despliegue |  |
| Rollback documentado | Procedimiento de rollback |  |
| Monitorización revisada | Matriz de observabilidad |  |
| Logs y diagnóstico documentados | Guías de diagnóstico |  |
| Seguridad técnica revisada | Matriz secretos/certificados/accesos |  |
| Backup/restore revisado | Matriz de recuperación |  |
| Riesgos técnicos registrados | RAID log / matriz riesgos |  |
| Runbooks técnicos iniciales creados | Runbooks por aplicación crítica |  |
| Casos de shadowing definidos | Matriz de casos Fase 4 |  |

## 25.2 Criterio de salida recomendado

La Fase 3 puede considerarse cerrada cuando:

> El equipo entrante dispone del conocimiento técnico mínimo validado para entender la arquitectura, localizar y compilar código, revisar configuración, diagnosticar incidencias, comprender datos e integraciones, conocer despliegues y rollback, consultar logs y monitorización, identificar riesgos técnicos y participar con criterio en el shadowing operativo de la Fase 4.

---


## 27.3 Gate ITIL de salida de la Fase 3

La salida de la Fase 3 deberá validarse mediante un gate específico de preparación técnica.

| Dimensión | Criterio de aceptación | Evidencia |
|---|---|---|
| Configuración | Los componentes críticos están identificados y relacionados con servicios de negocio | Registro técnico de configuración |
| Arquitectura | La arquitectura técnica global y por dominio está entendida | Diagramas y actas de revisión |
| Release | Se conoce la versión productiva y su trazabilidad con repositorio y artefacto | Matriz release / artefacto / despliegue |
| Despliegue | Los procedimientos de despliegue y rollback están documentados o tienen gap registrado | Runbook de despliegue y matriz de gaps |
| Incidencias | El equipo sabe dónde diagnosticar errores técnicos habituales | Guías de diagnóstico y catálogo de errores |
| Problemas | Los problemas recurrentes y deuda técnica están registrados | Registro de problemas técnicos y deuda |
| Monitorización | Las alertas y dashboards críticos están identificados | Catálogo de alertas y matriz de observabilidad |
| Seguridad | Secretos, certificados, accesos y datos sensibles están identificados | Matriz de secretos/certificados/accesos |
| Continuidad | Backup, restore, RTO, RPO y DR están revisados | Matriz de recuperación |
| Conocimiento | Runbooks técnicos iniciales disponibles para aplicaciones críticas | Runbooks técnicos |
| Shadowing | Casos técnicos definidos para observación en Fase 4 | Matriz de casos de shadowing |

La Fase 3 no debería cerrarse si existen gaps críticos que impidan diagnosticar, escalar, desplegar, revertir o recuperar una aplicación crítica con un nivel mínimo de seguridad operativa.

# 28. Recomendaciones prácticas para liderar la Fase 3

## 26.1 Recomendaciones de enfoque

- Priorizar aplicaciones críticas.
- Usar la Fase 2 para orientar las preguntas técnicas.
- Revisar primero arquitectura y dependencias.
- No perderse demasiado pronto en detalles de código.
- Exigir evidencias: repos, pipelines, logs, despliegues, tickets.
- Intentar compilar al menos los componentes críticos.
- Documentar diferencias entre entornos.
- Revisar rollback antes de asumir despliegues.
- Revisar batch con especial detalle.
- Revisar integraciones externas con contactos y procedimientos.
- Revisar datos sensibles con seguridad y DPO.
- Convertir cada gap técnico en tarea.
- Convertir cada riesgo técnico en RAID log.
- Preparar casos concretos para shadowing.

## 26.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- Nadie sabe qué versión está en producción.
- Nadie sabe cómo hacer rollback.
- Solo una persona sabe desplegar.
- El código no compila.
- Hay binarios fuera de repositorio.
- Hay scripts manuales no versionados.
- Hay jobs críticos sin documentación.
- Hay integraciones con terceros sin contrato técnico.
- No hay logs suficientes para diagnosticar.
- No hay alertas para procesos críticos.
- Hay datos sensibles en logs.
- Hay certificados próximos a caducar sin responsable.
- PRE y PRO son muy diferentes.
- La base de datos contiene lógica crítica no documentada.
- Los pipelines tienen secretos visibles.
- El proveedor saliente resuelve incidencias “de memoria”.

## 26.3 Buenas prácticas

- Crear diagramas simples aunque no sean perfectos.
- Mantener matrices vivas y trazables.
- Anotar siempre fuente y nivel de confianza.
- Documentar comandos útiles.
- Documentar búsquedas de logs.
- Documentar errores frecuentes.
- Documentar runbooks por aplicación crítica.
- Relacionar componentes técnicos con procesos funcionales.
- Separar gaps bloqueantes de mejoras deseables.
- Mantener un backlog técnico de transición.
- Preparar shadowing con casos concretos.

---

# 29. Resumen ejecutivo de la Fase 3

La Fase 3 convierte el conocimiento funcional e inventarial de las fases anteriores en capacidad técnica real.

El resultado deseado es que el equipo entrante pueda explicar y utilizar:

1. **La arquitectura técnica global.**
2. **Los componentes de cada aplicación crítica.**
3. **Los repositorios, ramas, versiones y artefactos.**
4. **El proceso de build y configuración.**
5. **Las bases de datos, tablas y lógica crítica.**
6. **Las integraciones técnicas y sus mecanismos de fallo.**
7. **Los procesos batch y sus reprocesos.**
8. **Los pipelines, despliegues y rollback.**
9. **Los logs, dashboards y alertas.**
10. **Los secretos, certificados y accesos técnicos.**
11. **Los mecanismos de backup, restore y DR.**
12. **Los riesgos técnicos que condicionan la operación.**
13. **Los casos que deben observarse en la Fase 4.**
14. **El estado de configuración, activos, riesgos, alertas, problemas y readiness técnico alineado con ITIL.**

La Fase 3 no debe cerrarse solo porque se hayan explicado los sistemas. Debe cerrarse cuando el equipo entrante tenga conocimiento técnico documentado, contrastado con evidencias y suficiente para empezar a observar y participar en la operación real.

---
