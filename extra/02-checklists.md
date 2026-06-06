# 02 — Checklists de Transferencia por Área

> **Instrucciones de uso:** Cada checklist debe completarse por aplicación o por conjunto de aplicaciones cuando compartan infraestructura. Registrar fecha, responsable y observaciones para cada ítem.

---

## A. Inventario General de Aplicaciones

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| A1 | Nombre oficial y alias de la aplicación | ⬜ | | |
| A2 | Descripción funcional (qué hace y para quién) | ⬜ | | |
| A3 | Criticidad del negocio (Alta / Media / Baja) | ⬜ | | |
| A4 | Número de usuarios y perfil de uso | ⬜ | | |
| A5 | Horario de operación y ventanas de mantenimiento | ⬜ | | |
| A6 | Propietario funcional en la aseguradora | ⬜ | | |
| A7 | Equipo actual responsable del mantenimiento | ⬜ | | |
| A8 | Fecha de última actualización significativa | ⬜ | | |
| A9 | Roadmap previsto (si existe) | ⬜ | | |
| A10 | Aplicaciones relacionadas o dependientes | ⬜ | | |

---

## B. Arquitectura Técnica y Dependencias

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| B1 | Diagrama de arquitectura actualizado | ⬜ | | |
| B2 | Stack tecnológico completo (lenguajes, frameworks, versiones) | ⬜ | | |
| B3 | Diagrama de dependencias entre componentes internos | ⬜ | | |
| B4 | Mapa de integraciones con sistemas externos | ⬜ | | |
| B5 | Librerías y dependencias de terceros (con versiones) | ⬜ | | |
| B6 | Deuda técnica identificada y documentada | ⬜ | | |
| B7 | Decisiones de arquitectura relevantes (ADRs si existen) | ⬜ | | |
| B8 | Patrones de comunicación (síncrono/asíncrono, colas, eventos) | ⬜ | | |
| B9 | Volúmenes de datos y transacciones (baseline) | ⬜ | | |
| B10 | Restricciones técnicas o limitaciones conocidas | ⬜ | | |

---

## C. Entornos

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| C1 | Inventario completo de entornos (dev, pre, pro, DR, etc.) | ⬜ | | |
| C2 | Diagrama de red de cada entorno | ⬜ | | |
| C3 | Especificaciones de hardware/cloud de cada entorno | ⬜ | | |
| C4 | Diferencias significativas entre entornos documentadas | ⬜ | | |
| C5 | Procedimiento de aprovisionamiento de entornos | ⬜ | | |
| C6 | Variables de entorno y configuraciones por entorno | ⬜ | | |
| C7 | IPs, hostnames, FQDNs y puertos relevantes | ⬜ | | |
| C8 | Certificados SSL/TLS (ubicación, fecha de expiración, renovación) | ⬜ | | |
| C9 | Firewalls, grupos de seguridad y reglas de red | ⬜ | | |
| C10 | Procedimiento de acceso a cada entorno | ⬜ | | |

---

## D. Accesos, Credenciales y Gestión de Secretos

> ⚠️ **CRÍTICO:** Nunca transferir credenciales por email o canales no cifrados.

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| D1 | Inventario de cuentas de servicio y usuarios técnicos | ⬜ | | |
| D2 | Gestor de secretos utilizado (Vault, AWS Secrets Manager, etc.) | ⬜ | | |
| D3 | Procedimiento de rotación de credenciales | ⬜ | | |
| D4 | Accesos a sistemas cloud (AWS, Azure, GCP) | ⬜ | | |
| D5 | Accesos VPN y bastiones SSH | ⬜ | | |
| D6 | Credenciales de bases de datos (por entorno) | ⬜ | | |
| D7 | Tokens y API keys de terceros | ⬜ | | |
| D8 | Certificados digitales y claves privadas | ⬜ | | |
| D9 | Accesos a herramientas de monitorización y alertas | ⬜ | | |
| D10 | Política de gestión de accesos (IAM, RBAC) documentada | ⬜ | | |
| D11 | Cuentas de emergencia / break-glass | ⬜ | | |
| D12 | Registro auditado de todos los accesos transferidos | ⬜ | | |

---

## E. Repositorios de Código Fuente y Control de Versiones

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| E1 | Listado completo de repositorios | ⬜ | | |
| E2 | Acceso con permisos adecuados al equipo entrante | ⬜ | | |
| E3 | Estrategia de branching documentada | ⬜ | | |
| E4 | Convenciones de commits y nomenclatura | ⬜ | | |
| E5 | README actualizado en cada repositorio | ⬜ | | |
| E6 | Instrucciones de setup local del entorno de desarrollo | ⬜ | | |
| E7 | Repositorios de IaC (Terraform, Ansible, etc.) identificados | ⬜ | | |
| E8 | Repositorios de configuración separados del código | ⬜ | | |
| E9 | Política de protección de ramas (branch protection rules) | ⬜ | | |
| E10 | Submodules o dependencias internas entre repos | ⬜ | | |

---

## F. Pipelines de CI/CD y Herramientas de Despliegue

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| F1 | Herramientas de CI/CD utilizadas (Jenkins, GitLab CI, etc.) | ⬜ | | |
| F2 | Acceso a las herramientas CI/CD transferido | ⬜ | | |
| F3 | Documentación de cada pipeline (etapas, triggers, artefactos) | ⬜ | | |
| F4 | Procedimiento de despliegue a producción (paso a paso) | ⬜ | | |
| F5 | Procedimiento de rollback documentado y validado | ⬜ | | |
| F6 | Variables y secretos de los pipelines documentados | ⬜ | | |
| F7 | Registro de los últimos despliegues (histórico) | ⬜ | | |
| F8 | Tests automatizados existentes y cobertura | ⬜ | | |
| F9 | Gates de calidad y aprobaciones manuales requeridas | ⬜ | | |
| F10 | Herramientas de gestión de artefactos (Nexus, Artifactory, etc.) | ⬜ | | |

---

## G. Bases de Datos y Gestión de Datos

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| G1 | Inventario de bases de datos (tipo, versión, tamaño) | ⬜ | | |
| G2 | Modelo de datos o esquema actualizado | ⬜ | | |
| G3 | Procedimientos de migración y versionado de esquema | ⬜ | | |
| G4 | Procedimiento de backup y frecuencia | ⬜ | | |
| G5 | Procedimiento de restauración y RTO/RPO definidos | ⬜ | | |
| G6 | Jobs y procesos batch sobre BBDD documentados | ⬜ | | |
| G7 | Procedimientos de mantenimiento (vacuum, reindex, purga) | ⬜ | | |
| G8 | Datos de producción: clasificación y nivel de sensibilidad | ⬜ | | |
| G9 | Política de enmascaramiento/anonimización para entornos no prod | ⬜ | | |
| G10 | Conexiones y usuarios de BBDD por aplicación | ⬜ | | |
| G11 | Réplicas y estrategia de alta disponibilidad | ⬜ | | |

---

## H. Integraciones con Sistemas Externos y APIs de Terceros

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| H1 | Mapa completo de integraciones (entrada y salida) | ⬜ | | |
| H2 | Documentación de cada API consumida (contratos, versiones) | ⬜ | | |
| H3 | Documentación de cada API expuesta | ⬜ | | |
| H4 | Contactos técnicos de cada sistema externo integrado | ⬜ | | |
| H5 | SLAs de los sistemas externos de los que se depende | ⬜ | | |
| H6 | Procedimiento ante caída de sistemas externos (fallback) | ⬜ | | |
| H7 | Integraciones con organismos reguladores (DGS, Unespa, etc.) | ⬜ | | |
| H8 | Integraciones con entidades financieras o de pago | ⬜ | | |
| H9 | Entornos de sandbox/test de cada integración | ⬜ | | |
| H10 | Historial de incidencias relacionadas con integraciones | ⬜ | | |

---

## I. Monitorización, Alertas y Gestión de Logs

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| I1 | Herramientas de monitorización (Datadog, Grafana, etc.) | ⬜ | | |
| I2 | Acceso a dashboards transferido | ⬜ | | |
| I3 | Catálogo de alertas activas con descripción y umbral | ⬜ | | |
| I4 | Procedimiento de actuación por tipo de alerta (runbooks) | ⬜ | | |
| I5 | Canales de notificación de alertas (PagerDuty, Slack, email) | ⬜ | | |
| I6 | Stack de logs (ELK, Splunk, CloudWatch, etc.) | ⬜ | | |
| I7 | Política de retención de logs | ⬜ | | |
| I8 | Línea base de métricas de rendimiento (CPU, memoria, latencia) | ⬜ | | |
| I9 | Dashboards de negocio / KPIs técnicos documentados | ⬜ | | |
| I10 | Procedimiento de on-call y rotaciones | ⬜ | | |

---

## J. Procedimientos de Backup y Recuperación ante Desastres

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| J1 | Plan de recuperación ante desastres (DRP) documentado | ⬜ | | |
| J2 | RTO y RPO definidos y validados por el negocio | ⬜ | | |
| J3 | Procedimientos de backup por sistema | ⬜ | | |
| J4 | Verificación periódica de backups (resultados del último test) | ⬜ | | |
| J5 | Entorno de DR disponible y documentado | ⬜ | | |
| J6 | Procedimiento de failover documentado y testado | ⬜ | | |
| J7 | Procedimiento de failback documentado | ⬜ | | |
| J8 | Contactos de emergencia internos y externos | ⬜ | | |
| J9 | Fecha del último simulacro de DR y resultado | ⬜ | | |
| J10 | Planificación del próximo simulacro de DR | ⬜ | | |

---

## K. SLAs, SLOs y Métricas de Rendimiento

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| K1 | SLAs contractuales con la aseguradora por aplicación | ⬜ | | |
| K2 | SLOs internos definidos | ⬜ | | |
| K3 | Métricas históricas de disponibilidad (últimos 12 meses) | ⬜ | | |
| K4 | Histórico de incumplimientos de SLA y causas | ⬜ | | |
| K5 | Penalizaciones contractuales por incumplimiento | ⬜ | | |
| K6 | Procedimiento de reporte de SLA al cliente | ⬜ | | |
| K7 | Herramienta de seguimiento de SLA | ⬜ | | |

---

## L. Gestión de Incidencias y Tickets

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| L1 | Herramienta de ticketing utilizada (Jira, ServiceNow, etc.) | ⬜ | | |
| L2 | Acceso a la herramienta de ticketing transferido | ⬜ | | |
| L3 | Procedimiento de clasificación y priorización de incidencias | ⬜ | | |
| L4 | Procedimiento de escalado documentado | ⬜ | | |
| L5 | Histórico de incidencias críticas (postmortems) | ⬜ | | |
| L6 | Incidencias y tickets activos en el momento del traspaso | ⬜ | | |
| L7 | Bugs conocidos y workarounds documentados | ⬜ | | |
| L8 | Backlog de mejoras y deuda técnica priorizado | ⬜ | | |
| L9 | Proceso de gestión de cambios (CAB, change freeze, etc.) | ⬜ | | |
| L10 | Calendario de cambios planificados | ⬜ | | |

---

## M. Documentación Funcional y de Negocio

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| M1 | Manual funcional de la aplicación | ⬜ | | |
| M2 | Procesos de negocio soportados documentados | ⬜ | | |
| M3 | Glosario de términos del negocio asegurador | ⬜ | | |
| M4 | Reglas de negocio críticas documentadas | ⬜ | | |
| M5 | Usuarios clave del negocio identificados y contactados | ⬜ | | |
| M6 | Histórico de decisiones funcionales relevantes | ⬜ | | |
| M7 | Casos de uso y user stories principales | ⬜ | | |
| M8 | Informes y reporting generado por la aplicación | ⬜ | | |

---

## N. Cumplimiento Normativo y Regulatorio

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| N1 | Normativas aplicables identificadas (GDPR, LOSSEAR, Solvencia II, etc.) | ⬜ | | |
| N2 | Última auditoría de seguridad y resultado | ⬜ | | |
| N3 | Última auditoría de cumplimiento normativo y resultado | ⬜ | | |
| N4 | Certificaciones vigentes (ISO 27001, ENS, etc.) | ⬜ | | |
| N5 | Registro de actividades de tratamiento (RGPD) | ⬜ | | |
| N6 | DPO (Delegado de Protección de Datos) identificado | ⬜ | | |
| N7 | Evaluaciones de impacto (DPIA) realizadas | ⬜ | | |
| N8 | Procedimiento de gestión de brechas de seguridad | ⬜ | | |
| N9 | Obligaciones de reporte regulatorio (DGS, Banco de España) | ⬜ | | |
| N10 | Calendario de auditorías previstas | ⬜ | | |

---

## O. Contratos con Proveedores y Licencias

| # | Ítem | Estado | Responsable | Notas |
|---|------|--------|-------------|-------|
| O1 | Inventario de licencias de software (con fecha de expiración) | ⬜ | | |
| O2 | Contratos con proveedores cloud | ⬜ | | |
| O3 | Contratos de soporte con fabricantes | ⬜ | | |
| O4 | Herramientas open source utilizadas (licencias y versiones) | ⬜ | | |
| O5 | Procedimiento de renovación de licencias | ⬜ | | |
| O6 | Contactos comerciales de los proveedores principales | ⬜ | | |
| O7 | Software próximo a fin de vida (EOL) identificado | ⬜ | | |

---

## P. Contactos Clave y Escalado

| Rol | Nombre | Email | Teléfono | Disponibilidad |
|-----|--------|-------|----------|----------------|
| Responsable TI aseguradora | | | | |
| Propietario funcional app 1 | | | | |
| Responsable equipo saliente | | | | |
| Contacto soporte proveedor cloud | | | | |
| DPO aseguradora | | | | |
| Contacto regulatorio (DGS) | | | | |
| Responsable de seguridad (CISO) | | | | |
| Contacto de emergencia 24/7 | | | | |
