# 04 — Modelo de Gobierno de la Transición

---

## Estructura de Roles

### Por parte del equipo entrante (tu empresa)

| Rol | Responsabilidades |
|-----|------------------|
| **Líder de Transición** | Dirección del plan, interlocutor principal con cliente y equipo saliente, escalado de bloqueos, reporting ejecutivo. |
| **Técnico Líder por Aplicación** | Responsable de la transferencia técnica de una o varias aplicaciones. Coordina las sesiones, completa los checklists y valida la documentación. |
| **Responsable de Documentación** | Centraliza y mantiene el repositorio de documentación. Garantiza la calidad y trazabilidad de los entregables. |
| **Responsable de Seguridad** | Supervisa la transferencia de accesos y credenciales. Valida el cumplimiento normativo durante el traspaso. |

### Por parte del cliente (aseguradora)

| Rol | Responsabilidades |
|-----|------------------|
| **Sponsor Ejecutivo** | Aprueba el plan, desbloquea decisiones de alto nivel, acepta formalmente el cierre. |
| **Responsable de TI** | Interlocutor técnico principal del cliente. Gestiona los accesos internos y facilita la colaboración del equipo saliente. |
| **Propietarios Funcionales** | Validan la documentación funcional de cada aplicación y participan en la aceptación final. |

### Por parte del equipo saliente

| Rol | Responsabilidades |
|-----|------------------|
| **Responsable de Entrega** | Coordina la participación de su equipo, garantiza la disponibilidad de las personas clave en las sesiones. |
| **Técnicos de Aplicación** | Ejecutan las sesiones de transferencia, documentan el conocimiento tácito, supervisan el reverse shadowing. |

---

## Cadencia de Reuniones

### Comité de Dirección de Transición
- **Frecuencia:** Quincenal
- **Participantes:** Líder de Transición + Sponsor Ejecutivo cliente + Responsable equipo saliente
- **Objetivo:** Revisión del estado general del plan, resolución de bloqueos estratégicos, aprobación de cambios de alcance.
- **Entregable:** Acta de reunión con decisiones y próximos pasos.

### Reunión Operativa Semanal
- **Frecuencia:** Semanal
- **Participantes:** Técnicos Líderes + Responsable TI cliente + Responsable entrega equipo saliente
- **Objetivo:** Seguimiento del progreso de checklists, identificación de bloqueos operativos, revisión de riesgos.
- **Entregable:** Actualización del panel de seguimiento.

### Sesiones de Transferencia de Conocimiento
- **Frecuencia:** Según calendario acordado (recomendado: 2-3 por semana por aplicación en Fase 1-2)
- **Participantes:** Técnico Líder entrante + Técnico saliente de la aplicación
- **Objetivo:** Transferencia activa de conocimiento técnico y operativo.
- **Entregable:** Notas de sesión, documentación actualizada, checklist progresado.

### Retrospectiva de Fase
- **Frecuencia:** Al cierre de cada fase
- **Participantes:** Todos los actores implicados
- **Objetivo:** Evaluar el progreso, identificar mejoras para la siguiente fase, validar los criterios de salida.
- **Entregable:** Informe de cierre de fase.

---

## Herramientas Recomendadas

| Necesidad | Herramienta sugerida | Alternativa |
|-----------|---------------------|-------------|
| Repositorio de documentación | Confluence / Notion | GitHub Wiki / GitBook |
| Control de versiones y código | GitHub / GitLab | Bitbucket |
| Gestión de tareas y checklists | Jira / Linear | GitHub Projects / Notion |
| Comunicación diaria | Slack / Microsoft Teams | Google Chat |
| Videoconferencias y grabaciones | Google Meet / Zoom | Microsoft Teams |
| Gestión de secretos | HashiCorp Vault / AWS Secrets Manager | Bitwarden Teams |
| Seguimiento de riesgos | Jira / hoja de cálculo compartida | Notion |
| Firma de documentos | DocuSign | Adobe Sign |

---

## Panel de Seguimiento del Traspaso

> Mantener actualizado semanalmente. Publicar en el espacio compartido.

### Estado por Aplicación

| Aplicación | Fase actual | % Checklist | Riesgos abiertos | Próximo hito | Responsable |
|------------|-------------|-------------|-----------------|--------------|-------------|
| App 1 | Fase 1 | 45% | 2 | Sesión arquitectura (DD/MM) | | 
| App 2 | Fase 0 | 10% | 0 | Kick-off técnico (DD/MM) | |
| ... | | | | | |

### Semáforo de Estado General

| Área | Estado | Comentario |
|------|--------|------------|
| Documentación | 🟡 En progreso | Gaps en App 2 y App 4 |
| Accesos | 🔴 Bloqueado | Pendiente aprobación acceso producción |
| Sesiones de transferencia | 🟢 En plazo | |
| Riesgos | 🟡 Controlado | R04 en seguimiento activo |
| SLA | 🟢 Cumplido | |

---

## Protocolo de Escalado

```
Bloqueo operativo
      │
      ▼
Técnico Líder entrante ──► intenta resolver en 24h
      │
      │ No resuelto
      ▼
Reunión operativa semanal ──► equipo conjunto lo aborda
      │
      │ No resuelto en 48h
      ▼
Líder de Transición ──► escala al Responsable TI cliente
      │
      │ No resuelto en 48h
      ▼
Comité de Dirección ──► decisión ejecutiva
```

---

## Gestión de la Documentación

- Todo el conocimiento transferido debe quedar registrado en el repositorio central **antes de dar por cerrada la sesión correspondiente**.
- Los documentos deben versionarse en Git. Nunca en carpetas compartidas sin control de versiones.
- Nomenclatura de ficheros: `[APPID]-[AREA]-[descripcion].md` (ej: `SIPOL-ARQ-diagrama-componentes.md`)
- Cada documento debe incluir: fecha de creación, autor, fecha de última revisión y revisor.
- Los checklists completados se guardan con el estado de cada ítem y las observaciones pertinentes.

---

## Plantilla de Acta de Reunión

```markdown
## Acta — [Tipo de reunión] — [Fecha]

**Participantes:**
- Nombre (Rol, Empresa)

**Puntos tratados:**
1. 
2. 

**Decisiones tomadas:**
- 

**Acciones:**
| Acción | Responsable | Fecha límite |
|--------|-------------|--------------|
| | | |

**Próxima reunión:** [Fecha y hora]
```
