# 06 — Recomendaciones Específicas para el Sector Asegurador

> El sector asegurador tiene características propias que hacen que el traspaso de aplicaciones sea especialmente delicado. Este documento recoge las consideraciones adicionales a tener en cuenta.

---

## 1. Marco Regulatorio y Normativo

### Normativas clave que pueden afectar a las aplicaciones

| Normativa | Ámbito | Implicaciones para el traspaso |
|-----------|--------|-------------------------------|
| **Reglamento General de Protección de Datos (RGPD / GDPR)** | Datos personales de asegurados | Actualizar el registro de tratamientos, revisar los contratos de encargo de tratamiento, asegurarse de que el equipo conoce las obligaciones de notificación de brechas (72h). |
| **LOSSEAR** (Ley de ordenación, supervisión y solvencia de entidades aseguradoras) | Regulación sectorial en España | Conocer las obligaciones de reporte a la DGSFP y las restricciones operativas. |
| **Solvencia II** | Requisitos de capital y gestión del riesgo | Los sistemas de reporting de Solvencia II son críticos y con calendarios inamovibles. Identificarlos y priorizarlos en el traspaso. |
| **DORA** (Digital Operational Resilience Act) | Resiliencia operativa digital (aplicable desde enero 2025) | Verificar que las aplicaciones cumplen los requisitos de resiliencia, gestión de incidentes TIC y riesgo de terceros. |
| **ENS** (Esquema Nacional de Seguridad) | Si la aseguradora opera con el sector público | Verificar la certificación vigente y las obligaciones de mantenimiento. |
| **PCI DSS** | Si se gestionan datos de pago | Identificar el alcance y las aplicaciones en scope. No realizar cambios sin seguir el proceso de gestión de cambios PCI. |

### Acciones recomendadas

- [ ] Identificar qué normativas afectan a cada aplicación en el inventario inicial.
- [ ] Revisar los contratos de encargo de tratamiento (DPA) y actualizarlos para incluir a tu empresa.
- [ ] Conocer el calendario de reportes regulatorios obligatorios (DGSFP, Banco de España) y asegurarse de que el equipo puede ejecutarlos.
- [ ] Revisar el último informe de auditoría interna o externa de cumplimiento.
- [ ] Identificar al DPO de la aseguradora y establecer canal de comunicación.

---

## 2. Criticidad Operativa y Ventanas de Cambio

### Períodos de alta criticidad en el sector asegurador

El sector asegurador tiene ciclos de negocio marcados que imponen restricciones a los cambios:

| Período | Motivo | Recomendación |
|---------|--------|---------------|
| **Cierre contable mensual/trimestral** | Procesos batch de cálculo y reporting críticos | Congelar cambios en aplicaciones de contabilidad y reporting los últimos 3 días del mes. |
| **Renovación masiva de pólizas** (típicamente enero y julio) | Alto volumen de operaciones, sistemas bajo máxima carga | Evitar despliegues en producción durante estos períodos. |
| **Reporting a DGSFP** (trimestral y anual) | Plazos regulatorios inamovibles | Conocer las fechas exactas; las incidencias en estos sistemas tienen máxima prioridad. |
| **Cálculo de Solvencia II** (trimestral) | Procesos complejos y sensibles | Mantener estabilidad de los sistemas implicados en las semanas previas al cierre. |
| **Campañas de suscripción** | Picos de carga en portales y sistemas de cotización | Monitorizar rendimiento activamente y tener capacidad de escalado preparada. |

### Recomendación

- [ ] Obtener el calendario anual de eventos críticos de negocio desde el inicio del traspaso.
- [ ] Planificar las fases de transición teniendo en cuenta estos períodos (nunca realizar el reverse shadowing durante un cierre contable).
- [ ] Documentar las ventanas de cambio aprobadas y comunicarlas al equipo.

---

## 3. Sensibilidad y Clasificación de los Datos

Las aplicaciones de una aseguradora manejan datos especialmente sensibles:

| Tipo de dato | Categoría RGPD | Ejemplos |
|--------------|----------------|---------|
| Datos de salud | **Categoría especial (art. 9)** | Historiales médicos, enfermedades preexistentes, siniestros de salud |
| Datos biométricos | **Categoría especial (art. 9)** | Si se usan para identificación |
| Datos de condena penal | **Categoría especial (art. 10)** | En seguros de RC o defensa jurídica |
| Datos financieros | Datos personales ordinarios de alta sensibilidad | Cuentas bancarias, historial de pagos |
| Datos de localización | Datos personales ordinarios | Seguros de automóvil telemáticos |

### Acciones recomendadas

- [ ] Mapear qué tipos de datos maneja cada aplicación.
- [ ] Verificar que los entornos de desarrollo y preproducción usan datos anonimizados o sintéticos (nunca datos reales de producción sin anonimizar).
- [ ] Revisar que los logs no registran datos personales en texto plano.
- [ ] Confirmar que las copias de seguridad están cifradas.
- [ ] Verificar que las integraciones con terceros tienen contratos DPA en vigor.

---

## 4. Sistemas de Alta Criticidad Habituales en Aseguradoras

Identificar si alguna de las aplicaciones en alcance corresponde a estas categorías y tratarlos con prioridad máxima:

| Sistema | Descripción | Riesgo en el traspaso |
|---------|-------------|----------------------|
| **Core de pólizas** | Gestión del ciclo de vida de pólizas (emisión, renovación, cancelación) | Caída = paralización del negocio. Sin operación no supervisada hasta Fase 3 avanzada. |
| **Sistema de siniestros** | Gestión de apertura, tramitación y liquidación de siniestros | Datos altamente sensibles. Procesos complejos con muchas reglas de negocio tácitas. |
| **Motor de cálculo de primas** | Tarificación y cotización | Errores pueden resultar en pérdidas económicas significativas. Validar con actuarios. |
| **Sistemas de reporting regulatorio** | Reporting a DGSFP, Banco de España, Solvencia II | Plazos inamovibles. Prioridad máxima en la transferencia. |
| **Portal del asegurado / mediador** | Acceso de clientes y red de distribución | Alta visibilidad. Los fallos impactan directamente en la experiencia del cliente. |
| **Sistemas de contabilidad** | Integración con ERPs, conciliación, cierre contable | Ventanas de cambio muy restringidas. |
| **Sistemas de recobros** | Recuperación de siniestros pagados | Reglas de negocio muy específicas del sector. |

---

## 5. Red de Distribución y Mediadores

- Las aseguradoras operan con redes de mediadores (agentes, corredores, bancaseguros) que interactúan con los sistemas. Identificar estas integraciones es crítico.
- Los cambios en los sistemas de mediadores pueden requerir comunicación y homologación previa con la red comercial.
- Identificar si existen acuerdos de nivel de servicio específicos con mediadores.

---

## 6. Gestión de Incidencias en Contexto Asegurador

- Una incidencia en el sistema de siniestros puede tener implicaciones legales si impide la tramitación dentro de los plazos legales establecidos.
- Los plazos de resolución de siniestros están regulados (Ley 50/1980 del Contrato de Seguro). Conocer estas obligaciones.
- En caso de incidencia grave, puede ser necesario notificar a la DGSFP.
- Establecer un protocolo específico de comunicación con el cliente (aseguradora) ante incidencias de alto impacto.

---

## 7. Checklist Adicional Específico del Sector

| # | Ítem | Estado | Responsable |
|---|------|--------|-------------|
| S1 | Calendario de reportes regulatorios obtenido y documentado | ⬜ | |
| S2 | Contacto en DGSFP identificado (si aplica) | ⬜ | |
| S3 | Contratos DPA actualizados con la empresa entrante | ⬜ | |
| S4 | Datos de producción anonimizados en entornos no productivos | ⬜ | |
| S5 | Ventanas de cambio aprobadas por el negocio documentadas | ⬜ | |
| S6 | Sistemas de reporting regulatorio priorizados en el plan | ⬜ | |
| S7 | Core de pólizas y siniestros identificados como aplicaciones críticas | ⬜ | |
| S8 | Integración con red de mediadores documentada | ⬜ | |
| S9 | Plazos legales de tramitación de siniestros conocidos por el equipo | ⬜ | |
| S10 | Protocolo de notificación a regulador ante incidencia grave | ⬜ | |
| S11 | Requisitos DORA revisados y aplicados al plan de transición | ⬜ | |
| S12 | Última auditoría actuarial de los sistemas de cálculo revisada | ⬜ | |

---

## 8. Recomendaciones Finales

1. **Involucra al equipo actuarial** desde el principio si hay sistemas de cálculo de primas o reservas. El conocimiento del negocio asegurador en estas áreas es muy específico.

2. **No subestimes la complejidad del modelo de datos**. Las bases de datos de pólizas y siniestros son históricamente complejas, con décadas de evolución y reglas de negocio embebidas en el esquema.

3. **Los procesos batch nocturnos son invisibles pero críticos**. Asegúrate de documentar todos los jobs programados, su frecuencia, dependencias y consecuencias de su fallo.

4. **Establece una relación directa con el negocio**, no solo con TI. En el sector asegurador, muchas reglas de negocio las conocen los técnicos de seguros, no el equipo de desarrollo.

5. **Prepárate para auditorías**. Es probable que durante o después del traspaso haya una auditoría interna o regulatoria. El equipo debe estar preparado para documentar y justificar todos los cambios realizados.
