# 05 — Criterios de Aceptación Final

> El traspaso se considera **completado con éxito** únicamente cuando se cumplen todos los criterios marcados como obligatorios (🔴) y al menos el 90% de los recomendados (🟡).

---

## 1. Documentación

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| D1 | Existe documentación técnica actualizada y verificada para el 100% de las aplicaciones en alcance | 🔴 Obligatorio | Técnico Líder + cliente | ⬜ |
| D2 | Todos los runbooks operativos han sido ejecutados al menos una vez por el equipo entrante en entorno no productivo | 🔴 Obligatorio | Técnico Líder | ⬜ |
| D3 | El repositorio de documentación es accesible únicamente por el equipo entrante y el cliente (accesos del equipo saliente revocados) | 🔴 Obligatorio | Responsable Seguridad | ⬜ |
| D4 | Los diagramas de arquitectura están actualizados y reflejan el estado real de producción | 🔴 Obligatorio | Técnico Líder | ⬜ |
| D5 | El plan de recuperación ante desastres (DRP) está documentado y ha sido validado mediante simulacro | 🟡 Recomendado | Técnico Líder + cliente | ⬜ |
| D6 | Los documentos tienen control de versiones en Git con historial de cambios | 🟡 Recomendado | Responsable Documentación | ⬜ |

---

## 2. Capacitación del Equipo

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| C1 | El equipo entrante ha gestionado de forma autónoma al menos una incidencia de cada nivel de criticidad (baja, media, alta) en cada aplicación crítica | 🔴 Obligatorio | Líder de Transición | ⬜ |
| C2 | Al menos dos personas del equipo entrante conocen cada aplicación crítica (bus factor ≥ 2) | 🔴 Obligatorio | Líder de Transición | ⬜ |
| C3 | El equipo entrante ha ejecutado al menos un despliegue completo a producción con supervisión en cada aplicación | 🔴 Obligatorio | Técnico Líder | ⬜ |
| C4 | El equipo entrante conoce y ha ejecutado el procedimiento de rollback de cada aplicación | 🔴 Obligatorio | Técnico Líder | ⬜ |
| C5 | El equipo entrante ha participado en al menos una sesión de on-call nocturna o de fin de semana supervisada | 🟡 Recomendado | Líder de Transición | ⬜ |
| C6 | El equipo entrante conoce y puede interactuar con todos los contactos clave del cliente y proveedores | 🟡 Recomendado | Líder de Transición | ⬜ |

---

## 3. Accesos e Infraestructura

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| A1 | El equipo entrante tiene acceso operativo completo a todos los entornos (dev, pre, pro) de todas las aplicaciones | 🔴 Obligatorio | Responsable Seguridad | ⬜ |
| A2 | Todos los accesos del equipo saliente han sido revocados y el proceso está auditado | 🔴 Obligatorio | Responsable Seguridad + cliente | ⬜ |
| A3 | Las credenciales y secretos han sido rotados tras el traspaso | 🔴 Obligatorio | Responsable Seguridad | ⬜ |
| A4 | El equipo entrante gestiona los certificados SSL/TLS (conoce fechas de expiración y proceso de renovación) | 🔴 Obligatorio | Técnico Líder | ⬜ |
| A5 | El acceso a los sistemas de monitorización y alertas está operativo para el equipo entrante | 🔴 Obligatorio | Técnico Líder | ⬜ |
| A6 | Los pipelines de CI/CD están bajo el control del equipo entrante | 🔴 Obligatorio | Técnico Líder | ⬜ |

---

## 4. Operación y SLA

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| O1 | Las métricas de disponibilidad durante la Fase 3 se han mantenido dentro de los rangos históricos aceptables | 🔴 Obligatorio | Líder de Transición + cliente | ⬜ |
| O2 | No existe ninguna incidencia crítica abierta en el momento del cierre | 🔴 Obligatorio | Responsable TI cliente | ⬜ |
| O3 | El backlog de incidencias y tickets ha sido formalmente transferido y el equipo entrante lo conoce | 🔴 Obligatorio | Técnico Líder | ⬜ |
| O4 | El equipo entrante conoce y ha aplicado el proceso de gestión de cambios (CAB, change freeze, etc.) | 🔴 Obligatorio | Técnico Líder | ⬜ |
| O5 | Las métricas de SLA del período de transición han sido revisadas y aceptadas por el cliente | 🔴 Obligatorio | Líder de Transición + cliente | ⬜ |
| O6 | El equipo entrante ha preparado y enviado al menos un informe de SLA al cliente | 🟡 Recomendado | Líder de Transición | ⬜ |

---

## 5. Cumplimiento y Seguridad

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| S1 | El equipo entrante conoce todas las normativas aplicables y sus obligaciones | 🔴 Obligatorio | Responsable Seguridad | ⬜ |
| S2 | El registro de actividades de tratamiento (RGPD) ha sido actualizado para reflejar el nuevo responsable del mantenimiento | 🔴 Obligatorio | DPO cliente | ⬜ |
| S3 | Las certificaciones vigentes (ISO 27001, ENS, etc.) han sido revisadas y se conoce el proceso para mantenerlas | 🟡 Recomendado | Responsable Seguridad | ⬜ |
| S4 | El procedimiento de gestión de brechas de seguridad es conocido por el equipo entrante | 🔴 Obligatorio | Responsable Seguridad | ⬜ |
| S5 | El calendario de auditorías previstas es conocido por el equipo entrante | 🟡 Recomendado | Responsable Seguridad | ⬜ |

---

## 6. Cierre Formal

| # | Criterio | Tipo | Validado por | Estado |
|---|----------|------|--------------|--------|
| F1 | El acta de traspaso ha sido firmada por el Líder de Transición, el Sponsor Ejecutivo del cliente y el Responsable del equipo saliente | 🔴 Obligatorio | Todas las partes | ⬜ |
| F2 | El informe de lecciones aprendidas ha sido redactado y compartido | 🟡 Recomendado | Líder de Transición | ⬜ |
| F3 | El modelo de soporte post-transición (si aplica) está acordado y documentado | 🔴 Obligatorio | Líder de Transición + cliente | ⬜ |
| F4 | Se ha celebrado la reunión de retrospectiva final con todos los actores | 🟡 Recomendado | Líder de Transición | ⬜ |

---

## Resumen de Aceptación

```
Total criterios obligatorios (🔴):   ___  /  ___  cumplidos
Total criterios recomendados (🟡):   ___  /  ___  cumplidos (mínimo 90%)

¿Traspaso completado con éxito?   □ SÍ   □ NO — Pendiente: _______________

Fecha de validación: _______________
Firmado por:
  - Líder de Transición: _______________________
  - Responsable TI cliente: ____________________
  - Responsable equipo saliente: _______________
```
