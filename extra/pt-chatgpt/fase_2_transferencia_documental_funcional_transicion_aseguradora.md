# Fase 2. Transferencia documental y funcional  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 2

La **Fase 2. Transferencia documental y funcional** tiene como objetivo que el equipo entrante comprenda en profundidad **qué hacen las aplicaciones desde el punto de vista de negocio**, qué procesos aseguradores soportan, qué reglas funcionales son críticas y qué documentación existe para operar y mantener correctamente el servicio.

Esta fase debe convertir el inventario construido en la Fase 1 en conocimiento funcional accionable.

No basta con saber que existe una aplicación llamada, por ejemplo, “Sistema de Recibos” o “Portal de Mediadores”. El equipo debe entender:

- Qué proceso de negocio soporta.
- Qué usuarios la utilizan.
- Qué productos de seguros se ven afectados.
- Qué reglas funcionales aplica.
- Qué datos son críticos.
- Qué documentación genera.
- Qué integraciones funcionales tiene.
- Qué incidencias funcionales son recurrentes.
- Qué excepciones operativas existen.
- Qué conocimiento está documentado y cuál reside solo en personas.
- Qué impacto tendría un error funcional.

En una aseguradora, esta fase es especialmente importante porque muchas incidencias no son puramente técnicas. Pueden deberse a reglas de negocio, parametrizaciones, estados de póliza, recibos, siniestros, documentación contractual, criterios de suscripción, normativa o integraciones con terceros.

---

## 2. Resultado esperado de la Fase 2

Al finalizar esta fase, el equipo debe disponer de:

- Un **mapa funcional de aplicaciones por dominio de negocio**.
- Una **visión clara de los procesos aseguradores críticos**.
- Una **matriz aplicación / proceso / producto / usuario**.
- Una **matriz de documentación funcional existente y pendiente**.
- Una **identificación de reglas de negocio críticas**.
- Una **identificación de parametrizaciones funcionales relevantes**.
- Una **lista de excepciones operativas y casuísticas especiales**.
- Una **relación de incidencias funcionales recurrentes**.
- Una **base inicial de conocimiento funcional**.
- Una **lista de gaps funcionales priorizados**.
- Una **validación inicial con negocio o responsables funcionales**.
- Una **preparación adecuada para la transferencia técnica profunda de la Fase 3**.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **3 a 6 semanas**.

Puede ser menor si:

- Existe documentación funcional completa y actualizada.
- Los procesos están bien modelados.
- Hay Product Owners disponibles.
- Las aplicaciones tienen bajo acoplamiento funcional.
- Los productos aseguradores soportados son pocos.

Puede alargarse si:

- Hay muchos ramos o productos.
- Existen sistemas legacy con reglas no documentadas.
- La documentación está desactualizada.
- El conocimiento reside en personas concretas.
- Hay muchos procesos batch funcionales.
- Las reglas de negocio están distribuidas entre código, tablas, parametrización y procedimientos.
- Existen obligaciones regulatorias complejas.
- Hay alto impacto en cliente, mediadores, cobros o siniestros.

---

# 4. Principios de trabajo de la Fase 2

## 4.1 Primero entender el negocio, después la aplicación

La transferencia funcional debe comenzar por los procesos de negocio, no por las pantallas o componentes técnicos.

Ejemplo:

- Primero entender el proceso de **emisión de una póliza**.
- Después identificar qué aplicaciones participan.
- Después revisar qué reglas se aplican.
- Después revisar pantallas, servicios, documentos, datos e integraciones.

## 4.2 Distinguir documentación existente de conocimiento validado

Un documento funcional puede existir, pero estar incompleto, obsoleto o no reflejar la operación real.

Estados recomendados para documentación funcional:

| Estado | Significado |
|---|---|
| Localizada | Se ha encontrado documentación, pero no revisada. |
| En revisión | Se está contrastando con expertos o negocio. |
| Validada | El contenido ha sido revisado y aceptado. |
| Obsoleta | No refleja la situación actual. |
| Parcial | Cubre solo una parte del proceso. |
| Inexistente | No se ha localizado documentación. |
| Sustituida por operación real | La documentación no existe y el conocimiento se captura mediante sesiones, tickets y práctica. |

## 4.3 Capturar reglas, excepciones y decisiones

En entornos aseguradores, muchas reglas críticas aparecen como excepciones:

- “Este producto solo se puede emitir por mediadores autorizados.”
- “Este tipo de suplemento no permite cambio retroactivo.”
- “Si el tomador es distinto del asegurado, se genera documentación adicional.”
- “Los recibos devueltos se reprocesan solo en determinadas ventanas.”
- “La renovación se bloquea si falta documentación contractual.”
- “Los siniestros de cierto ramo requieren validación manual.”
- “Determinados documentos deben conservarse durante un período mínimo.”

Estas reglas deben quedar registradas, aunque no exista documento formal previo.

## 4.4 No limitar la transferencia a pantallas

La funcionalidad de una aseguradora suele residir en varios niveles:

- Pantallas.
- APIs.
- Procesos batch.
- Reglas de parametrización.
- Tablas maestras.
- Workflows.
- Estados.
- Documentos.
- Comunicaciones.
- Validaciones.
- Integraciones con terceros.
- Procesos manuales de negocio.
- Procedimientos operativos.
- Reporting.

## 4.5 Validar con negocio siempre que sea posible

El equipo saliente puede conocer el sistema, pero negocio debe validar:

- Criticidad.
- Reglas funcionales.
- Procesos reales.
- Excepciones.
- Impacto de incidencias.
- Prioridad de transferencia.
- Documentación contractual.
- Operativas manuales.

---

# 5. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Preparación de transferencia funcional | Agenda, dominios, documentos y responsables funcionales. |
| Semana 1-2 | Revisión documental funcional | Identificación de documentación válida, parcial u obsoleta. |
| Semana 2-4 | Sesiones funcionales por dominio | Comprensión de procesos, reglas y excepciones. |
| Semana 3-5 | Análisis de tickets, incidencias y casos reales | Conocimiento funcional basado en operación real. |
| Semana 4-5 | Construcción de mapas funcionales | Matrices aplicación/proceso/producto/usuario. |
| Semana 5-6 | Validación con negocio y cierre de gaps | Aceptación funcional inicial y backlog de gaps. |

---

# 6. Actividad 1. Preparar la transferencia funcional

## 6.1 Objetivo

Definir qué dominios funcionales se van a revisar, con qué expertos, en qué orden y con qué documentación de partida.

## 6.2 Entradas necesarias

- Inventario consolidado de aplicaciones de la Fase 1.
- Matriz aplicación / dominio funcional.
- Matriz de criticidad.
- Matriz de stakeholders.
- Matriz de documentación existente.
- Tickets históricos clasificados.
- Propuesta de oleadas.
- Lista de aplicaciones críticas.
- Lista de gaps documentales ya identificados.

## 6.3 Dominios funcionales recomendados

| Dominio | Motivo de revisión |
|---|---|
| Cotización | Afecta a prima, elegibilidad, reglas de producto y experiencia comercial. |
| Emisión | Proceso contractual crítico; errores pueden afectar a validez documental. |
| Cartera / pólizas | Modificaciones, suplementos, anulaciones y estados contractuales. |
| Renovaciones | Alto impacto económico, operativo y reputacional. |
| Recibos y cobros | Impacto financiero, contable, cliente y bancario. |
| Siniestros | Proceso crítico para cliente, reservas, pagos y cumplimiento. |
| Mediadores | Canal comercial clave; impacto directo en distribución. |
| Clientes / autoservicio | Impacto en experiencia cliente y privacidad. |
| Documental | Condiciones, anexos, comunicaciones, firma y custodia. |
| Comunicaciones | Notificaciones obligatorias, emails, SMS, cartas. |
| Cumplimiento | GDPR, consentimientos, auditoría, trazabilidad. |
| Reporting | Información financiera, regulatoria y operativa. |
| Contabilidad | Asientos, cierres, conciliaciones. |
| Data Warehouse / BI | Explotación de datos y reporting corporativo. |

## 6.4 Acciones concretas

- Confirmar dominios funcionales incluidos en el alcance.
- Asignar aplicaciones a dominios.
- Identificar responsables funcionales por dominio.
- Identificar expertos del equipo saliente.
- Identificar usuarios clave o representantes de negocio.
- Preparar calendario de sesiones.
- Solicitar documentación funcional previa.
- Preparar preguntas por dominio.
- Crear plantilla de acta funcional.
- Crear matriz de reglas de negocio.
- Crear matriz de procesos.
- Crear backlog inicial de gaps funcionales.

## 6.5 Entregables

- Calendario de sesiones funcionales.
- Mapa inicial de dominios.
- Matriz aplicación / dominio / experto funcional.
- Lista de documentación a revisar.
- Plantilla de acta funcional.
- Plantilla de reglas de negocio.
- Backlog de gaps funcionales inicial.

---

# 7. Actividad 2. Revisar la documentación funcional existente

## 7.1 Objetivo

Localizar, clasificar y evaluar la documentación funcional disponible.

## 7.2 Tipos de documentación a localizar

| Tipo de documentación | Ejemplos |
|---|---|
| Requisitos funcionales | Documentos de análisis, especificaciones, épicas, historias de usuario. |
| Manuales de usuario | Guías operativas, manuales de backoffice, manuales de mediadores. |
| Documentación de producto | Condiciones, coberturas, reglas de suscripción, tarifas. |
| Flujos de proceso | BPMN, diagramas, flujos de pantalla, procesos operativos. |
| Casos de uso | Alta de póliza, apertura de siniestro, emisión de recibo. |
| Reglas de negocio | Validaciones, excepciones, estados, cálculos, límites. |
| Catálogo de productos | Ramos, modalidades, garantías, coberturas, capitales. |
| Catálogo documental | Plantillas, documentos generados, condiciones, anexos. |
| Catálogo de comunicaciones | Emails, SMS, cartas, notificaciones. |
| Documentación de parametrización | Tablas maestras, reglas configurables, valores por producto. |
| Documentación de incidencias | Workarounds funcionales, errores frecuentes. |
| Documentación regulatoria | GDPR, auditoría, retención, obligaciones sectoriales. |
| Documentación de pruebas | Casos de prueba funcionales, UAT, evidencias de aceptación. |

## 7.3 Matriz de revisión documental

| Aplicación | Documento | Tipo | Fecha | Propietario | Estado | Cobertura | Observaciones |
|---|---|---|---|---|---|---|---|
|  | Manual emisión | Manual usuario |  |  | Validado / Obsoleto / Parcial | Alta / Media / Baja |  |
|  | Reglas recibos | Reglas negocio |  |  |  |  |  |
|  | Flujo siniestros | Proceso |  |  |  |  |  |

## 7.4 Criterios para evaluar documentación

| Criterio | Pregunta |
|---|---|
| Vigencia | ¿Refleja la versión actual del sistema? |
| Cobertura | ¿Cubre todo el proceso o solo una parte? |
| Nivel de detalle | ¿Permite entender reglas y excepciones? |
| Trazabilidad | ¿Está relacionada con aplicaciones, tickets o releases? |
| Propietario | ¿Hay alguien responsable de mantenerla? |
| Uso real | ¿La usan negocio, soporte o desarrollo? |
| Calidad | ¿Es clara, consistente y accionable? |
| Evidencia | ¿Ha sido validada con ejecución real o expertos? |

## 7.5 Acciones concretas

- Crear inventario documental funcional.
- Clasificar documentos por aplicación y dominio.
- Marcar documentos obsoletos.
- Marcar documentos sin propietario.
- Identificar documentos críticos inexistentes.
- Identificar inconsistencias entre documentos.
- Contrastar documentos con tickets recientes.
- Contrastar documentos con sesiones funcionales.
- Registrar gaps documentales.
- Priorizar documentación crítica pendiente.

## 7.6 Gaps documentales frecuentes

| Gap | Riesgo |
|---|---|
| No hay documentación de reglas de negocio | El soporte depende de expertos concretos. |
| Manuales obsoletos | Se aplican procedimientos incorrectos. |
| No hay catálogo documental | Riesgo contractual o regulatorio. |
| No hay documentación de parametrización | Riesgo en cambios de producto o tarifas. |
| No hay flujos de proceso | Dificultad para entender impactos. |
| No hay trazabilidad con sistemas | No se sabe qué aplicación implementa cada proceso. |
| No hay documentación de excepciones | Incidencias recurrentes mal gestionadas. |

---

# 8. Actividad 3. Realizar sesiones funcionales por dominio

## 8.1 Objetivo

Capturar conocimiento funcional directamente de expertos salientes, responsables de negocio y usuarios clave.

## 8.2 Tipos de sesiones

| Tipo de sesión | Objetivo |
|---|---|
| Sesión de proceso extremo a extremo | Entender un flujo completo de negocio. |
| Sesión de aplicación | Entender qué hace una aplicación concreta. |
| Sesión de producto | Entender reglas asociadas a un producto asegurador. |
| Sesión de excepciones | Capturar casuísticas no documentadas. |
| Sesión de incidencias recurrentes | Entender errores habituales y workarounds. |
| Sesión documental | Revisar documentos generados y obligaciones. |
| Sesión de parametrización | Revisar tablas, reglas configurables y mantenimiento funcional. |
| Sesión de reporting | Entender informes, cierres y métricas. |

## 8.3 Agenda recomendada para una sesión funcional

| Bloque | Duración | Contenido |
|---|---:|---|
| Contexto | 5-10 min | Aplicación, proceso, producto o dominio a revisar. |
| Flujo principal | 20-30 min | Paso a paso del proceso normal. |
| Sistemas implicados | 10-15 min | Aplicaciones, integraciones y datos utilizados. |
| Reglas de negocio | 20-30 min | Validaciones, cálculos, estados, límites y excepciones. |
| Documentación | 10-15 min | Documentos, comunicaciones, evidencias y trazabilidad. |
| Incidencias frecuentes | 15-20 min | Problemas habituales y resolución funcional. |
| Gaps y dudas | 10-15 min | Pendientes, riesgos, acciones y responsables. |

## 8.4 Preguntas generales para cualquier sesión

- ¿Cuál es el objetivo funcional de este proceso?
- ¿Qué usuario o canal lo inicia?
- ¿Qué aplicaciones intervienen?
- ¿Qué datos mínimos son necesarios?
- ¿Qué validaciones se aplican?
- ¿Qué estados existen?
- ¿Qué documentos se generan?
- ¿Qué comunicaciones se envían?
- ¿Qué integraciones se invocan?
- ¿Qué ocurre si una integración falla?
- ¿Qué excepciones son habituales?
- ¿Qué incidencias se repiten?
- ¿Qué decisiones manuales existen?
- ¿Qué reglas están parametrizadas?
- ¿Qué reglas están en código?
- ¿Qué reglas están en base de datos?
- ¿Qué reglas no están documentadas?
- ¿Qué impacto tiene un fallo?
- ¿Qué alternativa manual existe?
- ¿Quién valida funcionalmente los cambios?
- ¿Qué documentación se considera fuente de verdad?

## 8.5 Evidencias a capturar

- Acta de sesión.
- Diagramas o flujos.
- Pantallazos si están permitidos.
- Links a documentos.
- Referencias a tickets.
- Ejemplos de casos reales.
- Reglas de negocio.
- Excepciones.
- Decisiones.
- Dudas abiertas.
- Acciones asignadas.
- Gaps funcionales.

---

# 9. Actividad 4. Mapear procesos funcionales extremo a extremo

## 9.1 Objetivo

Entender los procesos aseguradores completos, no solo la parte que ejecuta una aplicación concreta.

## 9.2 Procesos prioritarios

| Proceso | Motivo |
|---|---|
| Cotización | Inicio comercial, cálculo de prima, elegibilidad. |
| Emisión | Formalización contractual, documentos, firma y alta. |
| Suplementos | Cambios en pólizas vigentes. |
| Renovaciones | Continuidad de cartera y generación de recibos. |
| Recibos y cobros | Impacto financiero y cliente. |
| Impagos y recobros | Riesgo económico y operacional. |
| Anulación de póliza | Impacto contractual y contable. |
| Siniestros | Servicio crítico para cliente y provisiones. |
| Pagos de siniestros | Impacto económico, controles y fraude. |
| Comisiones de mediadores | Relación comercial y contabilidad. |
| Reporting regulatorio | Cumplimiento y auditoría. |
| Generación documental | Evidencia contractual y legal. |

## 9.3 Plantilla de proceso funcional

```markdown
# Proceso funcional

## Identificación

- Nombre del proceso:
- Dominio:
- Aplicaciones implicadas:
- Usuarios:
- Criticidad:
- Responsable de negocio:
- Responsable funcional:
- Responsable técnico:

## Objetivo del proceso

## Disparador

¿Qué evento inicia el proceso?

## Flujo principal

1.
2.
3.

## Variantes del proceso

## Excepciones

## Reglas de negocio

| ID | Regla | Tipo | Fuente | Responsable | Observaciones |
|---|---|---|---|---|---|
| RN-001 |  | Validación / Cálculo / Estado / Documento |  |  |  |

## Estados funcionales

| Estado | Significado | Estado anterior | Estado siguiente | Observaciones |
|---|---|---|---|---|

## Datos utilizados

| Dato | Origen | Uso | Sensibilidad | Observaciones |
|---|---|---|---|---|

## Documentos generados

| Documento | Momento | Obligatorio | Destinatario | Custodia |
|---|---|---|---|---|

## Integraciones

| Sistema | Tipo | Momento | Qué intercambia | Qué ocurre si falla |
|---|---|---|---|---|

## Incidencias frecuentes

| Incidencia | Causa habitual | Workaround | Escalado |
|---|---|---|---|

## Alternativa manual

## Riesgos

## Gaps pendientes
```

## 9.4 Resultado esperado

- Procesos principales documentados.
- Aplicaciones vinculadas a cada paso.
- Reglas críticas identificadas.
- Excepciones registradas.
- Impactos funcionales entendidos.
- Gaps pendientes priorizados.

---

# 10. Actividad 5. Identificar reglas de negocio críticas

## 10.1 Objetivo

Capturar las reglas que determinan el comportamiento funcional de las aplicaciones.

## 10.2 Tipos de reglas

| Tipo de regla | Ejemplos |
|---|---|
| Validación | Campos obligatorios, formato, coherencia de fechas. |
| Elegibilidad | Riesgos aceptados o rechazados. |
| Tarificación | Cálculo de prima, descuentos, recargos. |
| Suscripción | Límites, autorizaciones, revisión manual. |
| Estados | Transiciones permitidas de póliza, recibo o siniestro. |
| Documental | Documentos obligatorios según producto o canal. |
| Comunicaciones | Avisos, cartas, emails, SMS. |
| Cobro | Reglas de emisión de recibos, impagos, recobros. |
| Siniestros | Apertura, reserva, pago, cierre, fraude. |
| Mediadores | Permisos, comisiones, cartera, emisión delegada. |
| Regulatoria | Retención, consentimiento, auditoría, trazabilidad. |
| Contable | Devengo, asientos, cierres, conciliación. |

## 10.3 Matriz de reglas de negocio

| ID | Aplicación | Proceso | Regla | Tipo | Fuente | Implementación | Criticidad | Responsable |
|---|---|---|---|---|---|---|---|---|
| RN-001 | Emisión | Alta póliza | Validar tomador y asegurado | Validación | Documento funcional | Código / BD / Parametrización | Alta |  |
| RN-002 | Recibos | Cobro | Reintento tras devolución | Cobro | Operación real | Batch / Parametrización | Alta |  |
| RN-003 | Siniestros | Pago | Requiere autorización según importe | Siniestro | Negocio | Workflow | Crítica |  |

## 10.4 Preguntas clave

- ¿Dónde está implementada la regla?
- ¿Está en código, parametrización, base de datos, motor de reglas o proceso manual?
- ¿Quién puede modificarla?
- ¿Cómo se prueba?
- ¿Cómo se aprueba?
- ¿Qué ocurre si se aplica mal?
- ¿Tiene impacto contractual?
- ¿Tiene impacto económico?
- ¿Tiene impacto regulatorio?
- ¿Qué productos afecta?
- ¿Qué canales afecta?
- ¿Desde cuándo está vigente?
- ¿Hay excepciones?
- ¿Está documentada?

## 10.5 Riesgos frecuentes

| Riesgo | Mitigación |
|---|---|
| Reglas no documentadas | Capturarlas en sesiones y validarlas con negocio. |
| Reglas dispersas | Registrar ubicación: código, BD, parametrización, manual. |
| Reglas modificadas manualmente | Revisar controles, permisos y trazabilidad. |
| Reglas críticas sin pruebas | Priorizar casos de prueba funcionales. |
| Reglas obsoletas aún activas | Validar con negocio y analizar impacto. |

---

# 11. Actividad 6. Revisar parametrización funcional

## 11.1 Objetivo

Identificar qué comportamiento funcional depende de parámetros modificables y cómo se gestionan.

## 11.2 Parametrizaciones típicas en seguros

| Área | Ejemplos |
|---|---|
| Producto | Garantías, coberturas, modalidades, capitales. |
| Tarificación | Tarifas, factores, descuentos, recargos, promociones. |
| Suscripción | Límites, reglas de aceptación, autorizaciones. |
| Documentación | Plantillas, textos, anexos, versiones. |
| Comunicaciones | Plantillas email/SMS/carta, destinatarios. |
| Mediadores | Comisiones, permisos, campañas, canales. |
| Recibos | Frecuencias de pago, reintentos, bancos, remesas. |
| Siniestros | Tipologías, reservas, autorizaciones, peritos. |
| Reporting | Códigos, agrupaciones, reglas de extracción. |
| Cumplimiento | Consentimientos, textos legales, retención. |

## 11.3 Preguntas clave

- ¿Qué parámetros existen?
- ¿Dónde se mantienen?
- ¿Quién puede modificarlos?
- ¿Hay interfaz de administración?
- ¿Se modifican directamente en base de datos?
- ¿Existe workflow de aprobación?
- ¿Hay histórico de cambios?
- ¿Se pueden versionar?
- ¿Hay validación previa en PRE?
- ¿Qué parámetros son críticos?
- ¿Qué parámetros afectan a documentación contractual?
- ¿Qué parámetros afectan a importes?
- ¿Qué parámetros afectan a cumplimiento?

## 11.4 Matriz de parametrización

| Parámetro / tabla | Aplicación | Proceso | Uso | Modificación | Responsable | Criticidad | Control |
|---|---|---|---|---|---|---|---|
| Tabla tarifas | Cotización | Cálculo prima | Factores de tarifa | Pantalla admin / BD | Producto | Crítica | Validación negocio |
| Plantillas documentos | Documental | Emisión | Condiciones particulares | Gestor documental | Negocio / Legal | Crítica | Aprobación legal |
| Reintentos cobro | Recibos | Impagos | Número de reintentos | Parametrización | Operaciones | Alta | Comité cambios |

---

# 12. Actividad 7. Revisar documentación contractual y comunicaciones

## 12.1 Objetivo

Identificar qué documentos y comunicaciones se generan, cuándo, para quién y con qué obligación funcional o legal.

## 12.2 Documentos habituales

| Tipo | Ejemplos |
|---|---|
| Precontractual | IPID, información previa, cuestionarios. |
| Contractual | Condiciones particulares, generales, especiales. |
| Suplementos | Anexos, modificaciones, actualizaciones. |
| Renovaciones | Avisos, nuevas condiciones, recibos. |
| Recibos | Avisos de cobro, devolución, recobro. |
| Siniestros | Comunicaciones de apertura, resolución, pago. |
| Consentimientos | Protección de datos, comunicaciones comerciales. |
| Mediadores | Liquidaciones, comisiones, comunicaciones comerciales. |

## 12.3 Matriz documental

| Documento | Proceso | Aplicación origen | Generador | Obligatorio | Destinatario | Custodia | Criticidad |
|---|---|---|---|---|---|---|---|
| Condiciones particulares | Emisión | Emisión | Gestor documental | Sí | Cliente | Repositorio documental | Crítica |
| Aviso de renovación | Renovación | Renovaciones | Comunicaciones | Sí | Cliente | Documental / histórico | Alta |
| Comunicación siniestro | Siniestros | Siniestros | Comunicaciones | Según caso | Cliente | Expediente | Alta |

## 12.4 Preguntas clave

- ¿Qué documento se genera?
- ¿En qué momento del proceso?
- ¿Es obligatorio?
- ¿Quién lo recibe?
- ¿Dónde se custodia?
- ¿Qué plantilla se usa?
- ¿Cómo se versiona la plantilla?
- ¿Quién aprueba cambios en el texto?
- ¿Cómo se acredita la entrega?
- ¿Qué ocurre si no se genera?
- ¿Qué aplicación genera el documento?
- ¿Qué datos alimentan el documento?
- ¿Hay documentos firmados?
- ¿Hay integración con firma electrónica?
- ¿Hay impacto GDPR?

## 12.5 Riesgos frecuentes

| Riesgo | Mitigación |
|---|---|
| Documento incorrecto | Validar plantillas, datos y reglas con legal/negocio. |
| Documento no generado | Monitorizar procesos y registrar incidencias. |
| Falta de custodia | Identificar repositorio documental y retención. |
| Texto legal obsoleto | Validar con legal/compliance. |
| Falta de trazabilidad de entrega | Revisar evidencias y logs. |

---

# 13. Actividad 8. Analizar tickets históricos desde perspectiva funcional

## 13.1 Objetivo

Extraer conocimiento funcional real a partir de incidencias, problemas, cambios y peticiones históricas.

## 13.2 Qué buscar en los tickets

- Incidencias recurrentes.
- Dudas funcionales frecuentes.
- Errores de parametrización.
- Errores de documentos.
- Errores de cálculo de prima.
- Errores de recibos.
- Errores de estados.
- Casos de siniestros mal tramitados.
- Problemas de mediadores.
- Cambios urgentes solicitados por negocio.
- Workarounds manuales.
- Tickets escalados siempre a la misma persona.
- Tickets con impacto cliente.
- Tickets con impacto regulatorio.
- Tickets relacionados con cierres contables.
- Tickets relacionados con integraciones externas.

## 13.3 Matriz de incidencias funcionales recurrentes

| Aplicación | Proceso | Incidencia recurrente | Causa habitual | Workaround | Impacto | Responsable |
|---|---|---|---|---|---|---|
| Recibos | Cobro | Recibo no generado | Parametrización producto | Reproceso batch | Alto |  |
| Emisión | Documentación | Documento incompleto | Datos origen incorrectos | Regenerar documento | Crítico |  |
| Siniestros | Pago | Pago bloqueado | Estado inconsistente | Corrección manual | Alto |  |

## 13.4 Preguntas clave

- ¿Qué incidencias tienen causa funcional?
- ¿Qué incidencias se repiten?
- ¿Qué procesos generan más consultas?
- ¿Qué aplicaciones requieren más conocimiento de negocio?
- ¿Qué workarounds se aplican?
- ¿Están documentados esos workarounds?
- ¿Quién sabe resolver esas incidencias?
- ¿Hay incidencias que deberían convertirse en problemas?
- ¿Hay cambios funcionales que no están documentados?
- ¿Qué tickets revelan reglas de negocio ocultas?

## 13.5 Resultado esperado

- Lista de incidencias funcionales recurrentes.
- Workarounds documentados.
- Reglas ocultas identificadas.
- Gaps funcionales priorizados.
- Riesgos incorporados al RAID log.
- Casos reales para usar en shadowing y reverse shadowing.

---

# 14. Actividad 9. Construir base de conocimiento funcional

## 14.1 Objetivo

Crear un repositorio práctico de conocimiento funcional que permita al equipo entrante resolver dudas e incidencias.

## 14.2 Contenido recomendado

| Sección | Contenido |
|---|---|
| Glosario funcional | Términos de seguros y términos internos. |
| Procesos | Flujos extremo a extremo. |
| Aplicaciones | Qué hace cada aplicación desde negocio. |
| Productos | Ramos, modalidades, garantías, coberturas. |
| Reglas de negocio | Validaciones, cálculos, estados y excepciones. |
| Estados | Estados de póliza, recibo, siniestro, documento. |
| Documentos | Documentos generados, plantillas y custodia. |
| Incidencias frecuentes | Diagnóstico funcional y workaround. |
| Parametrización | Parámetros críticos y responsables. |
| Contactos | Responsables funcionales y escalado. |
| Preguntas frecuentes | Dudas habituales del soporte. |

## 14.3 Ejemplo de entrada de conocimiento

```markdown
# KB-FUNC-001. Recibo no generado tras emisión

## Proceso afectado

Emisión / Recibos

## Síntoma

La póliza aparece emitida, pero no se genera el primer recibo.

## Posibles causas funcionales

- Producto sin configuración de forma de pago.
- Fecha de efecto fuera de ventana.
- Error en datos bancarios.
- Estado de póliza incompleto.
- Error en integración con sistema de recibos.

## Validaciones iniciales

1. Revisar estado de póliza.
2. Revisar forma de pago.
3. Revisar datos bancarios.
4. Revisar si el producto genera recibo inmediato o diferido.
5. Revisar ejecución del batch de recibos.

## Workaround conocido

Pendiente de validar con equipo saliente.

## Escalado

- Responsable funcional:
- Responsable técnico:
- Operaciones batch:

## Tickets relacionados

- INC-XXXX
- INC-YYYY
```

## 14.4 Buenas prácticas

- Usar formato breve y accionable.
- Relacionar entradas con tickets reales.
- Mantener propietario de cada entrada.
- Marcar estado: borrador, validado, obsoleto.
- Revisar periódicamente.
- Integrar con ITSM si es posible.
- Priorizar casos frecuentes o críticos.

---

# 15. Actividad 10. Identificar gaps funcionales

## 15.1 Objetivo

Registrar todo conocimiento funcional incompleto, dudoso o no validado.

## 15.2 Tipos de gaps funcionales

| Tipo de gap | Ejemplo |
|---|---|
| Documental | No existe documento del proceso de renovación. |
| Regla de negocio | No está documentado cómo se calcula un recargo. |
| Parametrización | Nadie sabe quién mantiene una tabla. |
| Proceso | No está claro cómo se reprocesa un recibo. |
| Excepción | No están documentados casos especiales de emisión. |
| Producto | No se conoce la lógica específica de un ramo. |
| Documental contractual | No se sabe qué plantilla aplica a un producto. |
| Operativo | Workaround conocido solo por una persona. |
| Validación | Negocio no ha confirmado el flujo. |
| Trazabilidad | No se sabe qué aplicación ejecuta una regla. |

## 15.3 Matriz de gaps funcionales

| ID | Aplicación | Proceso | Gap | Tipo | Criticidad | Responsable | Acción | Estado |
|---|---|---|---|---|---|---|---|---|
| GF-001 | Recibos | Impagos | No documentado el reproceso de recibos devueltos | Proceso | Alta |  | Sesión con operaciones | Abierto |
| GF-002 | Emisión | Documentación | No está claro qué plantilla aplica por producto | Documental | Crítica |  | Validar con legal/negocio | Abierto |
| GF-003 | Cotización | Tarificación | Reglas de descuento no documentadas | Regla | Alta |  | Revisar parametrización | Abierto |

## 15.4 Priorización de gaps

Priorizar primero gaps que afecten a:

- Cliente final.
- Mediadores.
- Emisión.
- Cobros.
- Siniestros.
- Documentación contractual.
- Cumplimiento normativo.
- Datos sensibles.
- Reporting financiero o regulatorio.
- Procesos sin alternativa manual.
- Procesos con alta recurrencia de incidencias.

---

# 16. Actividad 11. Validar conocimiento funcional con negocio

## 16.1 Objetivo

Confirmar que la interpretación funcional capturada por el equipo entrante es correcta.

## 16.2 Qué debe validar negocio

- Procesos principales.
- Criticidad.
- Reglas de negocio.
- Excepciones.
- Impacto de fallos.
- Documentación contractual.
- Comunicaciones obligatorias.
- Alternativas manuales.
- Prioridad de gaps.
- Aplicaciones críticas.
- Puntos de dolor actuales.

## 16.3 Formato recomendado de validación

| Elemento | Responsable validación | Evidencia |
|---|---|---|
| Proceso emisión | Product Owner emisión | Acta de validación |
| Reglas de recibos | Responsable cobros | Acta / documento revisado |
| Documentos contractuales | Legal / negocio | Validación documental |
| Criticidad siniestros | Responsable siniestros | Matriz criticidad |
| Workarounds funcionales | Operaciones negocio | Base de conocimiento |

## 16.4 Preguntas clave para negocio

- ¿El flujo descrito refleja la operación real?
- ¿Faltan excepciones importantes?
- ¿La criticidad asignada es correcta?
- ¿Qué errores serían más graves?
- ¿Qué reglas no pueden fallar?
- ¿Qué procesos no tienen alternativa manual?
- ¿Qué períodos del año son más sensibles?
- ¿Qué documentación debe ser especialmente controlada?
- ¿Qué problemas funcionales son más frecuentes?
- ¿Qué aplicaciones generan más fricción para usuarios o mediadores?

## 16.5 Resultado esperado

- Procesos validados.
- Reglas críticas confirmadas.
- Gaps priorizados.
- Riesgos actualizados.
- Base funcional inicial aceptada.
- Preparación para transferencia técnica profunda.

---

# 17. Actividad 12. Preparar la transición hacia la Fase 3

## 17.1 Objetivo

Convertir el conocimiento funcional capturado en insumos concretos para la transferencia técnica profunda.

## 17.2 Qué debe trasladarse a la Fase 3

| Elemento funcional | Uso en Fase 3 |
|---|---|
| Procesos críticos | Priorizar revisión técnica. |
| Reglas de negocio | Localizar implementación en código, BD o parametrización. |
| Documentos generados | Revisar motores documentales, plantillas e integraciones. |
| Incidencias recurrentes | Revisar logs, código, jobs, errores y monitorización. |
| Workarounds | Convertir en runbooks técnicos. |
| Integraciones funcionales | Revisar contratos técnicos, APIs, colas, ficheros. |
| Gaps funcionales | Buscar evidencia técnica o documentación adicional. |
| Procesos batch | Revisar planificación, logs, dependencias y reprocesos. |
| Datos críticos | Revisar modelos, tablas, trazabilidad y sensibilidad. |

## 17.3 Preguntas para preparar sesiones técnicas

- ¿Dónde está implementada esta regla?
- ¿Qué servicio ejecuta esta validación?
- ¿Qué tabla guarda este estado?
- ¿Qué job genera este documento?
- ¿Qué integración envía esta comunicación?
- ¿Qué sistema calcula esta prima?
- ¿Qué proceso genera el recibo?
- ¿Qué logs permiten diagnosticar esta incidencia?
- ¿Qué componente controla esta parametrización?
- ¿Qué pipeline despliega este módulo?

---

# 18. Entregables de la Fase 2

## 18.1 Entregables principales

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Mapa funcional por dominio | Relación de dominios, procesos y aplicaciones. | Líder funcional |
| Matriz aplicación / proceso | Qué procesos soporta cada aplicación. | Líder funcional |
| Matriz aplicación / producto | Qué productos o ramos afecta cada aplicación. | Líder funcional + negocio |
| Matriz de reglas de negocio | Reglas críticas identificadas y clasificadas. | Líder funcional |
| Matriz de parametrización | Parámetros funcionales críticos. | Líder funcional + técnico |
| Catálogo documental | Documentos generados por proceso y aplicación. | Negocio / legal / funcional |
| Catálogo de comunicaciones | Emails, SMS, cartas y notificaciones. | Negocio / funcional |
| Matriz de incidencias funcionales | Incidencias recurrentes, causas y workarounds. | Service Manager + funcional |
| Base de conocimiento funcional | Entradas prácticas para soporte y mantenimiento. | Líder funcional |
| Matriz de gaps funcionales | Huecos documentales o de conocimiento. | Transition Manager |
| Actas de sesiones funcionales | Evidencia de transferencia. | Transition Manager |
| Validación de negocio | Confirmación de procesos y criticidad. | Negocio |

---

# 19. Plantillas útiles de la Fase 2

## 19.1 Matriz aplicación / proceso / producto

| Aplicación | Proceso | Producto / ramo | Usuario | Criticidad | Responsable negocio | Observaciones |
|---|---|---|---|---|---|---|
|  | Emisión | Autos | Backoffice / mediador | Alta |  |  |
|  | Recibos | Multirramo | Batch / operaciones | Crítica |  |  |
|  | Siniestros | Hogar | Tramitador | Alta |  |  |

## 19.2 Matriz de reglas de negocio

| ID | Dominio | Aplicación | Proceso | Regla | Tipo | Fuente | Implementación | Criticidad | Estado |
|---|---|---|---|---|---|---|---|---|---|
| RN-001 |  |  |  |  | Validación / Cálculo / Estado / Documento |  | Código / BD / Parametrización / Manual |  | Borrador / Validada |

## 19.3 Matriz de documentación funcional

| Aplicación | Proceso | Documento | Tipo | Propietario | Estado | Fecha revisión | Gap |
|---|---|---|---|---|---|---|---|
|  |  |  | Manual / Requisito / Flujo / Producto |  | Localizado / Validado / Obsoleto / Parcial |  |  |

## 19.4 Matriz de excepciones funcionales

| ID | Proceso | Excepción | Condición | Tratamiento | Responsable | Riesgo |
|---|---|---|---|---|---|---|
| EX-001 | Emisión | Tomador distinto de asegurado | Según producto | Documentación adicional |  | Error contractual |
| EX-002 | Recibos | Devolución bancaria | Recibo impagado | Reintento / recobro |  | Impacto económico |

## 19.5 Matriz de workarounds

| ID | Aplicación | Incidencia | Workaround | Quién lo ejecuta | Riesgo | Estado |
|---|---|---|---|---|---|---|
| WK-001 |  |  |  |  |  | Validado / Pendiente |

---

# 20. Checklist operativo de Fase 2

## 20.1 Preparación

- [ ] Confirmar dominios funcionales.
- [ ] Confirmar aplicaciones por dominio.
- [ ] Identificar responsables de negocio.
- [ ] Identificar expertos funcionales salientes.
- [ ] Identificar usuarios clave.
- [ ] Preparar calendario de sesiones.
- [ ] Recopilar documentación funcional.
- [ ] Preparar plantillas.
- [ ] Crear matriz de procesos.
- [ ] Crear matriz de reglas.
- [ ] Crear matriz de gaps funcionales.

## 20.2 Revisión documental

- [ ] Localizar requisitos funcionales.
- [ ] Localizar manuales de usuario.
- [ ] Localizar documentación de producto.
- [ ] Localizar flujos de proceso.
- [ ] Localizar reglas de negocio.
- [ ] Localizar catálogo documental.
- [ ] Localizar catálogo de comunicaciones.
- [ ] Localizar documentación de parametrización.
- [ ] Localizar casos de prueba funcional.
- [ ] Clasificar estado documental.
- [ ] Registrar documentos obsoletos.
- [ ] Registrar documentos inexistentes.
- [ ] Registrar gaps documentales.

## 20.3 Sesiones funcionales

- [ ] Realizar sesión de cotización.
- [ ] Realizar sesión de emisión.
- [ ] Realizar sesión de cartera / pólizas.
- [ ] Realizar sesión de suplementos.
- [ ] Realizar sesión de renovaciones.
- [ ] Realizar sesión de recibos y cobros.
- [ ] Realizar sesión de impagos y recobros.
- [ ] Realizar sesión de siniestros.
- [ ] Realizar sesión de mediadores.
- [ ] Realizar sesión de documentación contractual.
- [ ] Realizar sesión de comunicaciones.
- [ ] Realizar sesión de reporting.
- [ ] Realizar sesión de cumplimiento.
- [ ] Registrar actas.
- [ ] Registrar dudas abiertas.
- [ ] Registrar acciones.
- [ ] Registrar riesgos.

## 20.4 Procesos y reglas

- [ ] Documentar procesos extremo a extremo.
- [ ] Identificar disparadores de proceso.
- [ ] Identificar usuarios y canales.
- [ ] Identificar estados funcionales.
- [ ] Identificar reglas de validación.
- [ ] Identificar reglas de cálculo.
- [ ] Identificar reglas documentales.
- [ ] Identificar reglas de cobro.
- [ ] Identificar reglas de siniestros.
- [ ] Identificar reglas regulatorias.
- [ ] Identificar excepciones.
- [ ] Identificar alternativas manuales.
- [ ] Validar reglas críticas con negocio.

## 20.5 Parametrización

- [ ] Identificar parámetros de producto.
- [ ] Identificar parámetros de tarificación.
- [ ] Identificar parámetros de suscripción.
- [ ] Identificar parámetros documentales.
- [ ] Identificar parámetros de comunicaciones.
- [ ] Identificar parámetros de mediadores.
- [ ] Identificar parámetros de recibos.
- [ ] Identificar parámetros de siniestros.
- [ ] Identificar responsables de parametrización.
- [ ] Identificar controles de cambio.
- [ ] Registrar riesgos.

## 20.6 Documentación contractual y comunicaciones

- [ ] Identificar documentos precontractuales.
- [ ] Identificar documentos contractuales.
- [ ] Identificar suplementos y anexos.
- [ ] Identificar comunicaciones de renovación.
- [ ] Identificar comunicaciones de recibos.
- [ ] Identificar comunicaciones de siniestros.
- [ ] Identificar consentimientos.
- [ ] Identificar plantillas.
- [ ] Identificar custodia documental.
- [ ] Identificar trazabilidad de entrega.
- [ ] Validar con legal/compliance cuando proceda.

## 20.7 Tickets e incidencias

- [ ] Revisar tickets funcionales recurrentes.
- [ ] Identificar problemas por proceso.
- [ ] Identificar workarounds.
- [ ] Identificar expertos recurrentes.
- [ ] Identificar incidencias con impacto cliente.
- [ ] Identificar incidencias con impacto regulatorio.
- [ ] Identificar cambios urgentes de negocio.
- [ ] Incorporar hallazgos a la base de conocimiento.
- [ ] Actualizar RAID log.

## 20.8 Validación

- [ ] Validar procesos con negocio.
- [ ] Validar criticidad.
- [ ] Validar reglas críticas.
- [ ] Validar documentación contractual.
- [ ] Validar excepciones.
- [ ] Validar workarounds.
- [ ] Validar gaps prioritarios.
- [ ] Obtener actas de validación.
- [ ] Preparar insumos para Fase 3.

---

# 21. Riesgos específicos de la Fase 2

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Negocio no participa | Se captura una visión técnica incompleta | Escalar al sponsor y explicar impacto en aceptación. |
| Documentación funcional obsoleta | El equipo aprende procesos incorrectos | Contrastar con expertos, tickets y operación real. |
| Reglas críticas no documentadas | Riesgo de errores en mantenimiento | Crear matriz de reglas y validar con negocio. |
| Excepciones no capturadas | Incidencias mal resueltas | Realizar sesiones específicas de casuísticas especiales. |
| Parametrización desconocida | Riesgo en cambios de producto o tarifa | Identificar tablas, responsables y controles. |
| Documentos contractuales mal entendidos | Riesgo legal o reputacional | Involucrar legal, negocio y cumplimiento. |
| Incidencias funcionales tratadas como técnicas | Resolución lenta o incorrecta | Analizar tickets históricos con enfoque funcional. |
| Conocimiento concentrado en una persona | Dependencia futura | Capturar sesiones, actas, KB y validaciones. |
| Procesos batch funcionales ignorados | Riesgo en recibos, renovaciones o reporting | Revisar calendario batch y cierres. |
| Falta de trazabilidad aplicación-proceso | Dificultad para diagnosticar impactos | Crear matriz aplicación/proceso/producto. |
| No se identifican alternativas manuales | Mala gestión de contingencias | Documentar procedimientos manuales y límites. |
| No se validan reglas con negocio | Riesgo de interpretación incorrecta | Formalizar sesiones de validación. |

---

# 22. Criterios de salida de la Fase 2

## 22.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Dominios funcionales confirmados | Mapa funcional | Pendiente / En curso / Validado |
| Aplicaciones asignadas a procesos | Matriz aplicación/proceso |  |
| Productos o ramos identificados | Matriz aplicación/producto |  |
| Documentación funcional localizada | Matriz documental |  |
| Estado documental clasificado | Matriz documental actualizada |  |
| Sesiones funcionales realizadas | Actas de sesión |  |
| Procesos críticos documentados | Flujos funcionales |  |
| Reglas de negocio identificadas | Matriz de reglas |  |
| Excepciones documentadas | Matriz de excepciones |  |
| Parametrización funcional identificada | Matriz de parametrización |  |
| Documentos contractuales identificados | Catálogo documental |  |
| Comunicaciones identificadas | Catálogo de comunicaciones |  |
| Tickets funcionales analizados | Informe / matriz de incidencias |  |
| Workarounds registrados | Base de conocimiento |  |
| Gaps funcionales registrados | Matriz de gaps |  |
| Riesgos funcionales actualizados | RAID log |  |
| Validación de negocio realizada | Actas de validación |  |
| Insumos para Fase 3 preparados | Preguntas y prioridades técnicas |  |

## 22.2 Criterio de salida recomendado

La Fase 2 puede considerarse cerrada cuando:

> El equipo entrante entiende los procesos funcionales principales, las aplicaciones que los soportan, las reglas de negocio críticas, las excepciones, la documentación contractual, las incidencias funcionales recurrentes y los gaps pendientes, con validación suficiente de negocio para iniciar la transferencia técnica profunda de la Fase 3.

---

# 23. Recomendaciones prácticas para liderar la Fase 2

## 23.1 Recomendaciones de enfoque

- Organizar las sesiones por proceso de negocio, no solo por aplicación.
- Priorizar emisión, recibos, siniestros, renovaciones, documental y reporting.
- Usar casos reales para validar el entendimiento.
- Preguntar siempre por excepciones.
- Preguntar siempre por workarounds.
- Registrar reglas aunque parezcan evidentes.
- No asumir que una regla está en código; puede estar en parametrización o en operación manual.
- Contrastar documentación con tickets recientes.
- Involucrar a negocio en la validación.
- Convertir dudas funcionales en gaps con responsable y fecha.
- Preparar preguntas técnicas derivadas para la Fase 3.

## 23.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- Nadie sabe explicar por qué se aplica una regla.
- Una regla crítica no está documentada.
- Una regla crítica solo la conoce una persona.
- Un documento contractual se genera sin que nadie conozca la plantilla origen.
- Las incidencias funcionales se resuelven con correcciones manuales no documentadas.
- No se sabe quién aprueba cambios de parametrización.
- No existe catálogo de comunicaciones.
- No existe trazabilidad entre proceso, aplicación y documento.
- Negocio y equipo saliente describen procesos distintos.
- Los tickets históricos contradicen la documentación.
- Existen procesos con datos sensibles sin validación de cumplimiento.

## 23.3 Buenas prácticas

- Mantener una matriz viva de reglas.
- Mantener una matriz viva de gaps.
- Crear un glosario funcional.
- Documentar procesos con diagramas simples.
- Asociar reglas a procesos y aplicaciones.
- Asociar incidencias recurrentes a procesos.
- Identificar propietario de cada regla crítica.
- Validar documentos contractuales con legal o negocio.
- Preparar casos funcionales para shadowing posterior.
- Crear una base de conocimiento práctica desde el inicio.

---

# 24. Resumen ejecutivo de la Fase 2

La Fase 2 permite pasar de un inventario técnico-funcional a una comprensión real de los procesos de negocio que soporta el stack de aplicaciones.

El resultado deseado es que el equipo entrante pueda explicar:

1. **Qué procesos de negocio soporta cada aplicación.**
2. **Qué productos, ramos, usuarios y canales están afectados.**
3. **Qué reglas de negocio son críticas.**
4. **Qué documentación contractual y comunicaciones se generan.**
5. **Qué parametrizaciones condicionan el comportamiento funcional.**
6. **Qué incidencias funcionales se repiten.**
7. **Qué workarounds existen.**
8. **Qué gaps funcionales siguen abiertos.**
9. **Qué debe investigarse técnicamente en la Fase 3.**
10. **Qué riesgos funcionales pueden afectar a la continuidad del servicio.**

La Fase 2 no debe cerrarse solo porque se hayan celebrado reuniones. Debe cerrarse cuando el equipo entrante haya transformado esas reuniones en conocimiento funcional documentado, validado y utilizable.

---
