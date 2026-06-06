# 03 — Riesgos y Estrategias de Mitigación

> Los riesgos están ordenados por **impacto potencial** (Alto / Medio / Bajo) y probabilidad estimada.

---

## Matriz de Riesgos

| ID | Riesgo | Impacto | Probabilidad | Prioridad |
|----|--------|---------|--------------|-----------|
| R01 | Conocimiento tácito no documentado | Alto | Alta | 🔴 Crítica |
| R02 | Pérdida de disponibilidad durante la transición | Alto | Media | 🔴 Crítica |
| R03 | Fuga o exposición de datos sensibles | Alto | Baja | 🔴 Crítica |
| R04 | Resistencia o falta de colaboración del equipo saliente | Alto | Media | 🟠 Alta |
| R05 | Documentación desactualizada o incompleta | Alto | Alta | 🟠 Alta |
| R06 | Incumplimiento de SLA durante la transición | Alto | Media | 🟠 Alta |
| R07 | Dependencias ocultas o no documentadas | Medio | Alta | 🟠 Alta |
| R08 | Rotación de personal clave durante la transición | Medio | Media | 🟠 Alta |
| R09 | Desfase entre entornos (pre vs pro) no detectado | Medio | Media | 🟡 Media |
| R10 | Licencias o contratos que no se pueden transferir | Medio | Baja | 🟡 Media |
| R11 | Falta de acceso a herramientas o entornos | Medio | Media | 🟡 Media |
| R12 | Deuda técnica más grave de lo esperada | Medio | Media | 🟡 Media |
| R13 | Cambios en el alcance durante la transición | Medio | Media | 🟡 Media |
| R14 | Problemas de integración con sistemas de terceros | Medio | Baja | 🟡 Media |
| R15 | Calendario de transición demasiado ajustado | Bajo | Media | 🟢 Baja |

---

## Detalle de Riesgos y Mitigaciones

### R01 — Conocimiento tácito no documentado

**Descripción:** El equipo actual opera con conocimiento implícito que nunca ha sido escrito: trucos de operación, comportamientos anómalos conocidos, decisiones históricas no registradas.

**Mitigaciones:**
- Grabar todas las sesiones de transferencia (con consentimiento).
- Usar sesiones de "brain dump" estructuradas con preguntas tipo: *"¿Qué es lo primero que harías si X fallara?"*
- Realizar sesiones de pair operation donde el equipo saliente opere en voz alta.
- Implementar un diario de operaciones compartido durante la Fase 2.
- Revisar el historial de incidencias para detectar patrones no documentados.

**Contingencia:** Si el equipo saliente abandona el proyecto antes de documentar este conocimiento, escalar al cliente para exigir un período adicional de disponibilidad.

---

### R02 — Pérdida de disponibilidad durante la transición

**Descripción:** Un error operativo del equipo entrante durante el período de transición puede causar una caída de servicio en producción.

**Mitigaciones:**
- No realizar cambios en producción sin supervisión del equipo saliente hasta la Fase 3.
- Mantener el equipo saliente como segundo nivel durante toda la Fase 3.
- Validar todos los runbooks en entornos no productivos antes de ejecutarlos en producción.
- Definir ventanas de cambio seguras y comunicarlas al negocio.
- Establecer un procedimiento de escalado de emergencia desde el primer día.

**Contingencia:** Plan de rollback preparado y validado para cada tipo de cambio. Contacto directo con el equipo saliente con SLA de respuesta acordado.

---

### R03 — Fuga o exposición de datos sensibles

**Descripción:** Durante el traspaso de accesos, credenciales o documentación pueden exponerse datos de asegurados o información confidencial.

**Mitigaciones:**
- Usar exclusivamente gestores de secretos para la transferencia de credenciales (nunca email).
- Auditar todos los accesos concedidos y revocarlos inmediatamente cuando ya no sean necesarios.
- Nunca utilizar datos de producción en entornos de desarrollo o pruebas sin anonimizar.
- Firmar NDA y cláusulas de protección de datos antes del inicio del traspaso.
- Revisión de seguridad del repositorio de documentación (no almacenar credenciales en texto plano).

**Contingencia:** Protocolo de gestión de brecha de seguridad activado. Notificación a la AEPD en menos de 72h si aplica (RGPD art. 33).

---

### R04 — Resistencia o falta de colaboración del equipo saliente

**Descripción:** El equipo que entrega puede no tener incentivos para colaborar activamente, especialmente si perciben la transición como una amenaza a su empleo.

**Mitigaciones:**
- Involucrar a la dirección del cliente para que respalde el proceso y exija colaboración.
- Establecer hitos de entrega contractuales con el equipo/empresa saliente vinculados al pago.
- Mostrar respeto y reconocimiento por el trabajo del equipo saliente en todas las interacciones.
- Identificar a los colaboradores más proactivos y construir una relación de confianza con ellos.
- Documentar cualquier falta de colaboración de forma formal y escalarla al cliente.

**Contingencia:** Solicitar al cliente que active cláusulas contractuales de obligación de transferencia. Ampliar el período de descubrimiento y recurrir a la documentación existente y al código fuente.

---

### R05 — Documentación desactualizada o incompleta

**Descripción:** La documentación existente no refleja el estado actual real de las aplicaciones.

**Mitigaciones:**
- Validar toda la documentación contrastándola con el sistema real (no asumir que es correcta).
- Priorizar la ejecución de runbooks en entornos no productivos para verificar su validez.
- Asignar responsables del equipo entrante para actualizar la documentación durante la Fase 2.
- Establecer como criterio de salida de cada fase que la documentación esté verificada.

**Contingencia:** Ampliar la Fase 1 y reasignar recursos para cerrar los gaps críticos antes de asumir operación.

---

### R06 — Incumplimiento de SLA durante la transición

**Descripción:** El período de transición puede elevar el riesgo operativo y derivar en incumplimientos de los SLAs contractuales.

**Mitigaciones:**
- Negociar con el cliente un período de gracia o SLAs reducidos durante la transición.
- Mantener al equipo saliente como soporte durante toda la Fase 3.
- Monitorizar activamente las métricas de SLA desde el primer día.
- Comunicar proactivamente cualquier riesgo de incumplimiento antes de que ocurra.

**Contingencia:** Protocolo de escalado rápido al equipo saliente ante cualquier incidencia que amenace el SLA. Comunicación transparente al cliente.

---

### R07 — Dependencias ocultas o no documentadas

**Descripción:** Aplicaciones con dependencias no conocidas (scripts legacy, servicios no inventariados, integraciones informales) que se descubren tras el traspaso.

**Mitigaciones:**
- Análisis de tráfico de red en producción para detectar comunicaciones no documentadas.
- Revisión del código fuente para identificar llamadas a servicios externos.
- Revisar logs de producción históricos en busca de patrones de comunicación.
- Preguntar explícitamente: *"¿Existe algún proceso o integración que solo funcione en producción?"*

**Contingencia:** Mantener disponible al equipo saliente como referencia técnica durante al menos 4 semanas tras el cierre formal.

---

### R08 — Rotación de personal clave durante la transición

**Descripción:** Una persona clave del equipo saliente o del equipo entrante abandona el proyecto durante la transición.

**Mitigaciones:**
- Asegurarse de que el conocimiento nunca reside en una sola persona (bus factor > 1).
- Documentar el conocimiento de forma continua, no al final.
- Identificar al menos dos personas del equipo entrante para cada área crítica.
- Establecer en contrato que el equipo saliente debe garantizar sustitución de personal clave.

**Contingencia:** Plan de continuidad activado. Ampliar el período de transición y renegociar con el cliente si es necesario.

---

### R09 — Desfase entre entornos no detectado

**Descripción:** El entorno de producción tiene configuraciones, datos o componentes que no existen en preproducción, haciendo que las validaciones previas no sean representativas.

**Mitigaciones:**
- Documentar y verificar explícitamente las diferencias entre entornos.
- Solicitar acceso de lectura a producción desde la Fase 1 para comparar configuraciones.
- Usar herramientas de IaC para garantizar paridad entre entornos.

---

### R10 — Licencias o contratos intransferibles

**Descripción:** Algunas licencias de software o contratos con proveedores pueden estar vinculados a la empresa saliente y no ser transferibles directamente.

**Mitigaciones:**
- Inventariar todas las licencias en la Fase 1 e identificar las que requieren gestión activa.
- Involucrar al departamento legal/compras del cliente para gestionar las transferencias.
- Identificar alternativas para software cuya licencia no sea transferible.

---

### R11 — Falta de acceso a herramientas o entornos

**Descripción:** El equipo entrante no puede obtener acceso a tiempo a sistemas críticos por burocracia, procesos de seguridad o falta de colaboración.

**Mitigaciones:**
- Solicitar accesos desde el primer día de la Fase 1, no esperar a la Fase 2.
- Escalar los bloqueos de acceso al responsable de TI del cliente inmediatamente.
- Mantener un registro de accesos solicitados vs. concedidos.

---

### R12 — Deuda técnica más grave de lo esperada

**Descripción:** El estado real del código o la infraestructura es peor de lo reflejado en la documentación o en la valoración inicial.

**Mitigaciones:**
- Realizar una revisión de código y arquitectura en la Fase 1 antes de comprometerse al plan de transición definitivo.
- Incluir en el contrato cláusulas que permitan renegociar el alcance si se detectan problemas graves.
- Documentar toda la deuda técnica encontrada y comunicarla formalmente al cliente.

---

### R13 — Cambios en el alcance durante la transición

**Descripción:** El cliente solicita incluir nuevas aplicaciones o cambios funcionales durante el período de transición, desestabilizando el plan.

**Mitigaciones:**
- Establecer un proceso formal de gestión de cambios de alcance desde el inicio.
- Comunicar claramente que los cambios de alcance pueden impactar el calendario y el coste.
- Congelar los cambios no críticos durante las fases más delicadas de la transición.

---

## Registro de Riesgos (plantilla)

| Fecha | ID Riesgo | Descripción | Estado | Acciones tomadas | Responsable |
|-------|-----------|-------------|--------|------------------|-------------|
| | | | Abierto / En seguimiento / Cerrado | | |
