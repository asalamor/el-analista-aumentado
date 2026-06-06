# 01 — Fases de la Transición

## Visión general

```
FASE 0          FASE 1           FASE 2           FASE 3          FASE 4
Arranque  ───►  Descubrimiento ► Transferencia ►  Operación  ►   Cierre
(1-2 sem)       (3-6 sem)        (4-8 sem)        supervisada     formal
                                                  (4-6 sem)       (1-2 sem)
```

---

## Fase 0 — Arranque y Preparación

**Duración estimada:** 1-2 semanas

### Objetivos

- Constituir formalmente el equipo de transición.
- Establecer los canales, herramientas y cadencias de comunicación.
- Obtener un inventario inicial de alto nivel de todas las aplicaciones en alcance.
- Firmar los acuerdos de confidencialidad y acceso necesarios.

### Actividades clave

- [ ] Nombrar el responsable de transición por cada parte (cliente/proveedor saliente/equipo entrante).
- [ ] Crear el repositorio/espacio de trabajo compartido (wiki, repo Git, Confluence, etc.).
- [ ] Celebrar la reunión de kick-off con todos los actores implicados.
- [ ] Recopilar el catálogo inicial de aplicaciones (nombre, tecnología, criticidad, equipo actual).
- [ ] Establecer el calendario de sesiones de transferencia.
- [ ] Revisar y firmar NDAs, acuerdos de nivel de servicio y contratos de soporte en transición.

### Criterios de salida (antes de pasar a Fase 1)

- [ ] Equipo de transición constituido y con roles asignados.
- [ ] Catálogo inicial de aplicaciones validado por el cliente.
- [ ] Herramientas y canales de comunicación operativos.
- [ ] Calendario de sesiones acordado y publicado.

---

## Fase 1 — Descubrimiento y Documentación

**Duración estimada:** 3-6 semanas

### Objetivos

- Comprender en profundidad el estado actual de cada aplicación.
- Identificar deuda técnica, zonas de riesgo y conocimiento tácito.
- Completar los checklists de descubrimiento (ver `02-checklists.md`).

### Actividades clave

- [ ] Sesiones de transferencia con cada equipo actual (grabarlas si es posible).
- [ ] Revisar toda la documentación existente y evaluar su calidad.
- [ ] Mapear arquitecturas, dependencias e integraciones.
- [ ] Inventariar todos los entornos, accesos y credenciales.
- [ ] Identificar los procesos críticos y sus ventanas de cambio.
- [ ] Documentar los procedimientos operativos que aún no estén escritos.
- [ ] Elaborar el mapa de contactos y escalado.

### Criterios de salida

- [ ] Checklists de descubrimiento completados al 90% o más.
- [ ] Gaps de documentación identificados y priorizados.
- [ ] Arquitectura de cada aplicación documentada y validada.
- [ ] Mapa de dependencias e integraciones completo.
- [ ] Primer borrador del runbook operativo por aplicación.

---

## Fase 2 — Transferencia Activa

**Duración estimada:** 4-8 semanas

### Objetivos

- Ejecutar la transferencia real del conocimiento mediante trabajo conjunto.
- Resolver los gaps de documentación identificados en Fase 1.
- Que el equipo entrante empiece a gestionar incidencias de baja/media criticidad con supervisión.

### Actividades clave

- [ ] Shadowing: el equipo entrante acompaña al equipo actual en sus operaciones diarias.
- [ ] Reverse shadowing: el equipo entrante toma el control y el equipo actual supervisa.
- [ ] Transferencia de accesos (siguiendo el procedimiento de seguridad acordado).
- [ ] Cerrar los gaps de documentación priorizados.
- [ ] Realizar simulacros de incidencias y procedimientos de emergencia.
- [ ] Transferir la gestión del backlog y los tickets activos.
- [ ] Validar los runbooks ejecutándolos paso a paso en entornos no productivos.

### Criterios de salida

- [ ] El equipo entrante ha gestionado al menos 2-3 incidencias reales de cada tipo (despliegue, incidencia, cambio).
- [ ] Runbooks validados en entorno de preproducción.
- [ ] Accesos de producción transferidos y verificados.
- [ ] Documentación al 100% en áreas críticas.
- [ ] Plan de contingencia acordado con el equipo saliente para la siguiente fase.

---

## Fase 3 — Operación Supervisada

**Duración estimada:** 4-6 semanas

### Objetivos

- El equipo entrante opera de forma autónoma con red de seguridad.
- El equipo saliente actúa como segundo nivel de soporte, no como primer respondedor.
- Validar la capacidad real del equipo entrante bajo condiciones productivas.

### Actividades clave

- [ ] El equipo entrante responde a todas las incidencias como primer nivel.
- [ ] El equipo saliente permanece disponible (SLA de respuesta acordado, ej: 4h en horario laboral).
- [ ] Reuniones semanales de revisión de incidencias y lecciones aprendidas.
- [ ] Identificar y resolver las dudas y gaps que emerjan en operación real.
- [ ] Actualizar la documentación con el conocimiento generado en esta fase.
- [ ] Monitorizar métricas de rendimiento y compararlas con la línea base histórica.

### Criterios de salida

- [ ] El equipo entrante ha operado autónomamente durante al menos 4 semanas.
- [ ] Ninguna incidencia crítica no resuelta por el equipo entrante de forma autónoma.
- [ ] Métricas operativas dentro de los rangos históricos aceptables.
- [ ] El equipo saliente ratifica que el equipo entrante está capacitado para operar solo.

---

## Fase 4 — Cierre Formal

**Duración estimada:** 1-2 semanas

### Objetivos

- Formalizar la finalización de la transición.
- Garantizar que no quedan cabos sueltos.
- Establecer el modelo de soporte post-transición si aplica.

### Actividades clave

- [ ] Revisión final de todos los checklists y criterios de aceptación.
- [ ] Retirada de accesos del equipo saliente (con registro auditado).
- [ ] Firma del acta de traspaso.
- [ ] Sesión de retrospectiva con todos los actores.
- [ ] Documentar lecciones aprendidas.
- [ ] Acordar el modelo de soporte residual (si el equipo saliente mantiene disponibilidad puntual).

### Criterios de salida

- [ ] Acta de traspaso firmada por ambas partes y por el cliente.
- [ ] Accesos del equipo saliente revocados y auditados.
- [ ] Repositorio de documentación entregado y accesible por el equipo entrante.
- [ ] Plan de soporte post-transición acordado (si aplica).
