# Fase 7. Cierre y estabilización post-transición  
## Plan detallado para la transición tecnológica y transferencia de conocimiento en una aseguradora

## 1. Propósito de la Fase 7

La **Fase 7. Cierre y estabilización post-transición** tiene como objetivo confirmar que la transición se ha completado correctamente, que el equipo entrante opera de forma autónoma y que el servicio ha pasado de un modo de transición a un modo estable de operación ordinaria, o **BAU**.

Esta fase no debe verse como un trámite administrativo. Es el momento de validar con evidencias que:

- El equipo entrante ha asumido la responsabilidad principal.
- El servicio se mantiene estable.
- Los SLAs se cumplen.
- Las aplicaciones críticas están bajo control.
- Los riesgos residuales están documentados y aceptados.
- Los gaps críticos están cerrados o tienen plan aprobado.
- La documentación operativa está consolidada.
- El equipo saliente puede retirarse de forma ordenada.
- El modelo BAU está activo.
- Existe un plan de mejora continua.

En una aseguradora, esta fase es especialmente relevante porque el cierre no debe comprometer procesos críticos como emisión, recibos, siniestros, renovaciones, documentación contractual, integraciones bancarias, reporting financiero, reporting regulatorio, protección de datos, continuidad de servicio y auditoría.

El objetivo final es que el cliente pueda aceptar formalmente que el traspaso se ha completado con éxito.

---

## 2. Resultado esperado de la Fase 7

Al finalizar esta fase, debe existir una aceptación formal de la transición y un modelo estable de operación.

Los resultados esperados son:

- Transición cerrada formalmente.
- Servicio en modo BAU.
- Equipo entrante operando de forma autónoma.
- Soporte saliente retirado o reducido a un mecanismo residual claramente definido.
- SLAs y métricas bajo control.
- Runbooks y documentación consolidados.
- Gaps críticos cerrados o aceptados con plan.
- Riesgos residuales aceptados formalmente.
- Evidencias de aceptación archivadas.
- Modelo de gobierno BAU activo.
- Plan de mejora continua definido.
- Lecciones aprendidas documentadas.
- Informe final de transición aprobado.
- Prácticas ITIL de operación BAU activas y con responsables asignados.
- Registro de problemas recurrentes creado o integrado en la herramienta ITSM.
- Backlog de mejora continua priorizado y aceptado por el modelo de gobierno BAU.
- Mini-CMDB o inventario de configuración actualizado con el estado final del servicio.
- Proveedores externos traspasados al modelo de soporte ordinario.

---

## 3. Duración estimada

La duración recomendada para esta fase es de **4 a 8 semanas**.

Puede ser menor si:

- La Fase 6 ha sido estable.
- Los SLAs se han mantenido.
- La dependencia del equipo saliente es baja.
- No hay gaps críticos abiertos.
- El cliente tiene criterios de aceptación claros.
- La documentación está consolidada.
- No hay hitos de negocio o regulatorios próximos.

Puede alargarse si:

- Persisten riesgos residuales altos.
- Hay aplicaciones críticas con restricciones.
- El equipo saliente sigue interviniendo con frecuencia.
- Hay incidencias relevantes durante la estabilización.
- Hay procesos batch complejos aún en observación.
- Hay auditorías o cierres próximos.
- Negocio no percibe suficiente estabilidad.
- Los SLAs muestran degradación.
- La documentación requiere cierre adicional.
- Hay desacuerdo sobre la aceptación final.

---

---

# 4. Alineamiento ITIL específico de la Fase 7

## 4.1 Sentido ITIL de esta fase

Desde la perspectiva ITIL, la Fase 7 representa el paso definitivo desde una transición controlada hacia una operación ordinaria estable, gobernada y orientada a la mejora continua.

El cierre no debe entenderse únicamente como una aceptación administrativa, sino como la confirmación de que el servicio puede operar bajo un modelo BAU con prácticas activas de gestión de incidencias, problemas, cambios, niveles de servicio, configuración, conocimiento, proveedores, seguridad, continuidad y mejora continua.

La fase debe demostrar que el equipo entrante no solo ha recibido el servicio, sino que ya lo gestiona como un servicio IT gobernado.

## 4.2 Prácticas ITIL relacionadas

| Práctica ITIL | Aplicación en esta fase |
|---|---|
| **Service Level Management** | Confirmar cumplimiento de SLAs, SLOs y calidad del servicio durante la estabilización. |
| **Incident Management** | Validar que las incidencias se gestionan de forma ordinaria por el equipo entrante. |
| **Problem Management** | Convertir incidencias recurrentes en problemas gestionados con causa raíz, workaround y plan de resolución. |
| **Change Enablement** | Confirmar que los cambios y despliegues ya se gestionan bajo el proceso BAU. |
| **Release Management** | Asegurar que versiones, despliegues y evidencias quedan trazadas en operación ordinaria. |
| **Deployment Management** | Confirmar que los procedimientos de despliegue y rollback son utilizables en BAU. |
| **Knowledge Management** | Integrar runbooks, KB, lecciones aprendidas y documentación viva en el modelo operativo. |
| **Service Configuration Management** | Validar que el inventario, relaciones y elementos de configuración quedan mantenidos tras el cierre. |
| **IT Asset Management** | Regularizar activos, licencias, herramientas, certificados y responsabilidades heredadas. |
| **Supplier Management** | Confirmar que los proveedores externos tienen contactos, SLAs, escalados y responsabilidades transferidas. |
| **Information Security Management** | Regularizar accesos, secretos, certificados, evidencias de auditoría y retirada del equipo saliente. |
| **Service Continuity Management** | Confirmar que backup, restore, DRP, RTO y RPO quedan entendidos y gobernados en BAU. |
| **Monitoring and Event Management** | Consolidar dashboards, alertas, umbrales, guardias y respuesta ante eventos. |
| **Measurement and Reporting** | Establecer reporting ordinario del servicio tras la transición. |
| **Continual Improvement** | Convertir deuda, riesgos no bloqueantes y oportunidades en un backlog priorizado de mejora continua. |

## 4.3 Objetivo ITIL de la fase

El objetivo ITIL de la Fase 7 es confirmar que la transición ha generado una **capacidad operativa sostenible**, no solo una transferencia puntual de conocimiento.

Para ello, la fase debe dejar evidencias de que:

- El servicio opera bajo modelo BAU.
- Las prácticas de gestión del servicio están activas.
- Los SLAs y métricas se monitorizan.
- Las incidencias se gestionan por el equipo entrante.
- Los problemas recurrentes tienen tratamiento formal.
- Los cambios y despliegues siguen el proceso establecido.
- La documentación tiene propietario y ciclo de mantenimiento.
- Los proveedores están integrados en el modelo de soporte.
- Los riesgos residuales están aceptados o mitigados.
- La mejora continua queda activada.

## 4.4 Evidencias ITIL esperadas

| Evidencia | Práctica ITIL relacionada |
|---|---|
| Panel de estabilización y SLAs | Service Level Management / Measurement and Reporting |
| Registro de incidencias BAU | Incident Management |
| Registro de problemas recurrentes | Problem Management |
| Registro de cambios y despliegues BAU | Change Enablement / Release / Deployment |
| Base de conocimiento consolidada | Knowledge Management |
| Inventario y mini-CMDB actualizados | Service Configuration Management |
| Matriz final de proveedores | Supplier Management |
| Matriz final de accesos y retirada saliente | Information Security Management |
| Riesgos residuales aceptados | Risk Management / Continual Improvement |
| Backlog de mejora continua | Continual Improvement |
| Acta de aceptación final | Governance / Service Level Management |
| Informe final de transición | Measurement and Reporting |

## 4.5 Criterio ITIL de éxito

La Fase 7 será exitosa desde el punto de vista ITIL cuando el servicio pueda demostrar que ha pasado de un estado transitorio a un modelo de gestión ordinaria, medible, gobernado y mejorable.

La aceptación final debe basarse en evidencias de operación real, no en percepciones de estabilidad.

# 5. Principios de trabajo de la Fase 7

## 4.1 Cerrar con evidencias, no con sensaciones

La transición no debe cerrarse porque “parece que ya está” o porque se ha agotado el plazo. Debe cerrarse porque existen evidencias objetivas.

Ejemplos de evidencias:

- Tickets gestionados por el equipo entrante.
- SLAs cumplidos durante el período de estabilización.
- Incidencias críticas resueltas sin dependencia saliente.
- Despliegues ejecutados correctamente.
- Procesos batch validados.
- Runbooks actualizados.
- Riesgos aceptados.
- Gaps cerrados.
- Comunicaciones realizadas.
- Actas de Go / No-Go.
- Informe final aprobado.

## 4.2 Distinguir cierre de transición y mejora continua

No todos los problemas técnicos deben resolverse antes de cerrar la transición.

Debe diferenciarse:

| Tipo de elemento | Tratamiento |
|---|---|
| Gap crítico de conocimiento | Debe cerrarse antes del cierre o contar con mitigación formal. |
| Riesgo operativo alto | Debe mitigarse o aceptarse formalmente. |
| Deuda técnica estructural | Puede pasar al plan de mejora continua. |
| Mejora de automatización | Puede planificarse post-transición. |
| Optimización de observabilidad | Puede pasar a backlog BAU si el riesgo está controlado. |
| Refactorización | Normalmente no bloquea cierre salvo riesgo crítico. |

La transición debe asegurar continuidad y autonomía. La transformación técnica puede continuar después.

## 4.3 Retirar al equipo saliente de forma ordenada

La retirada del equipo saliente debe ser planificada. No debe producirse un corte brusco sin confirmar:

- Qué soporte residual queda.
- Durante cuánto tiempo.
- En qué horario.
- Para qué tipos de casos.
- Con qué tiempos de respuesta.
- Por qué canal.
- Quién autoriza su intervención.
- Qué accesos conserva temporalmente.
- Cuándo se revocan accesos.
- Cómo se documentan las últimas dudas.

## 4.4 Consolidar BAU

La transición termina cuando el servicio deja de funcionar como proyecto de traspaso y pasa a funcionar como operación ordinaria.

Esto implica:

- Comités BAU definidos.
- Reporting BAU activo.
- Gestión de incidencias normalizada.
- Gestión de cambios normalizada.
- Gestión de problemas activa.
- Gestión del conocimiento integrada.
- SLAs monitorizados.
- Responsables permanentes asignados.
- Modelo de escalado estable.
- Proveedores externos correctamente integrados.
- Seguridad y accesos regularizados.

## 4.5 Mantener vigilancia reforzada durante estabilización

Aunque la responsabilidad esté asumida, conviene mantener una vigilancia reforzada durante unas semanas.

Esta vigilancia debe centrarse en:

- Incidencias P1/P2.
- SLAs en riesgo.
- Reaperturas.
- Incidencias recurrentes.
- Escalados al equipo saliente.
- Fallos batch.
- Fallos de despliegue.
- Procesos críticos de negocio.
- Alertas relevantes.
- Percepción de negocio.
- Riesgos regulatorios.

## 5.6 Convertir incidencias recurrentes en gestión de problemas

Desde una perspectiva ITIL, la estabilización no debe limitarse a resolver incidencias una a una. Si durante el cierre aparecen patrones repetidos, deben convertirse en problemas formales.

Esto implica:

- Registrar el problema.
- Identificar causa raíz si es posible.
- Documentar workaround.
- Asignar responsable.
- Priorizar solución definitiva.
- Relacionar el problema con incidencias previas.
- Incorporarlo al backlog BAU o de mejora continua.

## 5.7 Activar mejora continua como práctica, no como lista final

El plan de mejora continua no debe ser un anexo decorativo al informe final. Debe convertirse en un mecanismo operativo con responsable, priorización, seguimiento y reporting.

Las mejoras detectadas durante la transición deben clasificarse según su impacto en:

- Reducción de riesgo operativo.
- Mejora de SLAs.
- Reducción de incidencias recurrentes.
- Automatización.
- Seguridad.
- Observabilidad.
- Calidad técnica.
- Cumplimiento normativo.
- Reducción de dependencia personal.

---

# 6. Secuencia recomendada de trabajo

## Vista general

| Semana | Actividad principal | Resultado esperado |
|---|---|---|
| Semana 1 | Confirmar entrada en estabilización | Alcance, criterios, métricas y soporte residual definidos. |
| Semana 1-4 | Operar en BAU con vigilancia reforzada | Validar estabilidad, SLAs, autonomía y calidad. |
| Semana 2-5 | Cerrar gaps y riesgos residuales | Reducir pendientes críticos y formalizar aceptaciones. |
| Semana 3-6 | Consolidar documentación y evidencias | Preparar paquete de aceptación final. |
| Semana 4-7 | Retirar soporte saliente progresivamente | Reducir dependencia y regularizar accesos. |
| Semana 6-8 | Cerrar formalmente transición | Informe final, aceptación, lecciones aprendidas y mejora continua. |

---

# 7. Actividad 1. Confirmar el inicio de la estabilización

## 6.1 Objetivo

Validar que la Fase 6 ha concluido suficientemente y que el servicio puede entrar en una etapa de estabilización post-transición.

## 6.2 Entradas necesarias

- Decisión Go / No-Go de Fase 6.
- Matriz de oleadas completadas.
- Matriz de autonomía.
- Matriz de riesgos residuales.
- Matriz de gaps.
- Métricas de SLAs.
- Registro de escalados al equipo saliente.
- Runbooks actualizados.
- Modelo BAU inicial.
- Matriz de soporte residual.
- Calendario de eventos críticos de negocio.
- Calendario de auditorías, cierres o campañas.
- Feedback de cliente, negocio y operaciones.

## 6.3 Preguntas clave

- ¿Qué aplicaciones están plenamente asumidas?
- ¿Qué aplicaciones están asumidas con restricciones?
- ¿Qué aplicaciones no están completamente asumidas?
- ¿Qué riesgos residuales existen?
- ¿Qué gaps siguen abiertos?
- ¿Qué soporte saliente sigue siendo necesario?
- ¿Se han cumplido SLAs durante la asunción?
- ¿Hay incidencias recurrentes no resueltas?
- ¿Negocio percibe continuidad?
- ¿Mesa de servicio tiene claro el modelo?
- ¿El equipo entrante conoce sus responsabilidades?
- ¿Qué condiciones deben cumplirse para la aceptación final?

## 6.4 Entregables

- Acta de inicio de estabilización.
- Alcance de estabilización.
- Criterios de cierre final.
- Matriz de restricciones residuales.
- Plan de soporte saliente residual.
- Plan de vigilancia reforzada.
- Calendario de revisión de estabilización.

---

# 8. Actividad 2. Operar en BAU con vigilancia reforzada

## 7.1 Objetivo

Confirmar que el equipo entrante puede operar el servicio en condiciones reales y sostenidas.

## 7.2 Controles recomendados durante estabilización

| Control | Frecuencia | Objetivo |
|---|---:|---|
| Revisión de tickets | Diaria | Detectar desviaciones tempranas. |
| Revisión de SLAs | Diaria o semanal | Confirmar cumplimiento contractual. |
| Revisión de incidencias críticas | Inmediata | Controlar impacto. |
| Revisión de reabiertos | Semanal | Medir calidad de resolución. |
| Revisión de escalados al saliente | Semanal | Medir dependencia residual. |
| Revisión de batch | Diaria / según calendario | Validar procesos críticos. |
| Revisión de cambios | Semanal | Controlar riesgo de despliegue. |
| Revisión de riesgos | Semanal | Mantener RAID log actualizado. |
| Revisión con negocio | Semanal o quincenal | Medir percepción de continuidad. |
| Comité BAU reforzado | Semanal | Gobernar estabilización. |

## 7.3 Métricas recomendadas

| Métrica | Objetivo |
|---|---|
| Cumplimiento SLA | Validar calidad de servicio. |
| MTTA | Medir rapidez de atención. |
| MTTR | Medir rapidez de resolución. |
| Tickets reabiertos | Medir calidad de solución. |
| Incidencias P1/P2 | Medir estabilidad. |
| Escalados al saliente | Medir autonomía real. |
| Incidencias recurrentes | Identificar problemas estructurales. |
| Cambios fallidos | Medir madurez de despliegue. |
| Batch fallidos | Controlar procesos críticos. |
| Alertas no atendidas | Medir capacidad operativa. |
| Tickets fuera de SLA | Identificar riesgo contractual. |
| Satisfacción de negocio | Medir confianza funcional. |

## 7.4 Panel de estabilización

| Indicador | Semana 1 | Semana 2 | Semana 3 | Semana 4 | Tendencia | Estado |
|---|---:|---:|---:|---:|---|---|
| Tickets recibidos |  |  |  |  | ↑ / ↓ / = | Verde / Ámbar / Rojo |
| SLA cumplido |  |  |  |  |  |  |
| MTTR |  |  |  |  |  |  |
| Reabiertos |  |  |  |  |  |  |
| Incidencias P1/P2 |  |  |  |  |  |  |
| Escalados saliente |  |  |  |  |  |  |
| Cambios fallidos |  |  |  |  |  |  |
| Batch fallidos |  |  |  |  |  |  |

## 7.5 Resultado esperado

- Operación estable durante varias semanas.
- SLAs bajo control.
- Disminución de dependencia saliente.
- Incidencias recurrentes identificadas.
- Confianza del cliente reforzada.
- Evidencia suficiente para aceptación.

---

# 9. Actividad 3. Cerrar gaps pendientes

## 8.1 Objetivo

Resolver, mitigar o aceptar formalmente los gaps identificados durante la transición.

## 8.2 Tipos de gaps

| Tipo | Ejemplo |
|---|---|
| Funcional | Regla de negocio no completamente validada. |
| Técnico | Componente poco conocido. |
| Operativo | Runbook incompleto. |
| Acceso | Permiso pendiente o excesivo. |
| Seguridad | Certificado o secreto pendiente de regularizar. |
| Datos | Modelo o tabla crítica sin documentación suficiente. |
| Integración | Tercero sin circuito de soporte claro. |
| Batch | Reproceso no practicado. |
| Despliegue | Rollback no validado. |
| Documental | Documento contractual sin trazabilidad suficiente. |

## 8.3 Tratamiento de gaps

| Criticidad | Tratamiento |
|---|---|
| Crítica | Debe cerrarse antes de aceptación final o tener mitigación aprobada por sponsor. |
| Alta | Debe cerrarse o contar con plan fechado y responsable. |
| Media | Puede pasar a backlog BAU con seguimiento. |
| Baja | Puede pasar a mejora continua. |

## 8.4 Matriz de gaps de cierre

| ID | Gap | Aplicación | Criticidad | Tratamiento | Responsable | Fecha | Estado | Aceptación |
|---|---|---|---|---|---|---|---|---|
| GC-001 | Runbook reproceso incompleto | Recibos | Alta | Completar y validar |  |  | Abierto |  |
| GC-002 | Integración tercero sin SLA claro | Firma | Media | Pasar a BAU |  |  | En curso | Cliente |
| GC-003 | Rollback no probado | Emisión | Alta | Simulación PRE |  |  | Pendiente |  |

## 8.5 Resultado esperado

- Gaps críticos cerrados.
- Gaps altos mitigados.
- Gaps medios y bajos planificados.
- Riesgos asociados aceptados o trasladados a BAU.
- Sin pendientes ocultos.

---

# 10. Actividad 4. Gestionar riesgos residuales

## 9.1 Objetivo

Asegurar que todos los riesgos que permanecen tras la transición están identificados, mitigados, aceptados o trasladados a mejora continua.

## 9.2 Categorías de riesgo residual

| Categoría | Ejemplo |
|---|---|
| Conocimiento | Experto único aún necesario en caso concreto. |
| Operación | Procedimiento poco frecuente no practicado. |
| Técnico | Tecnología obsoleta. |
| Seguridad | Certificado pendiente de renovación. |
| Datos | Trazabilidad parcial en una entidad crítica. |
| Integración | Dependencia externa con SLA débil. |
| Cumplimiento | Evidencia de auditoría pendiente. |
| Continuidad | Restore no probado recientemente. |
| Despliegue | Rollback no ejecutado en producción. |
| Batch | Reproceso no observado en caso real. |

## 9.3 Tratamiento recomendado

| Nivel de riesgo | Tratamiento |
|---|---|
| Crítico | Bloquea cierre salvo aceptación ejecutiva formal. |
| Alto | Requiere mitigación concreta y seguimiento. |
| Medio | Puede pasar a BAU con responsable y fecha. |
| Bajo | Puede pasar a backlog de mejora continua. |

## 9.4 Matriz de riesgos residuales de cierre

| ID | Riesgo | Aplicación / dominio | Impacto | Probabilidad | Mitigación | Decisión | Responsable |
|---|---|---|---|---|---|---|---|
| RR-001 | Reproceso de remesas poco practicado | Recibos | Alto | Media | Doble validación durante 1 mes | Aceptado condicionado |  |
| RR-002 | Framework fuera de soporte | Portal | Medio | Alta | Plan de actualización | Mejora continua |  |
| RR-003 | Restore no probado en últimos 12 meses | Documental | Alto | Baja | Solicitar prueba DR | BAU prioritario |  |

## 9.5 Resultado esperado

- Riesgos residuales transparentes.
- Aceptación formal de riesgos relevantes.
- Planes de mitigación definidos.
- Riesgos transferidos a BAU o mejora continua.

---

# 11. Actividad 5. Consolidar documentación final

## 10.1 Objetivo

Asegurar que la documentación necesaria para operar el servicio queda completa, accesible, validada y con responsables de mantenimiento.

## 10.2 Documentación mínima a consolidar

| Documento | Objetivo |
|---|---|
| Inventario de aplicaciones | Conocer alcance real del servicio. |
| Matriz de criticidad | Priorizar soporte y riesgos. |
| Mapa funcional | Relacionar aplicaciones y procesos de negocio. |
| Mapa técnico | Entender arquitectura y dependencias. |
| Matriz de entornos | Conocer DEV, PRE, PRO, DR y restricciones. |
| Matriz de repositorios | Localizar código y ramas. |
| Matriz CI/CD | Conocer pipelines, despliegues y artefactos. |
| Matriz de BBDD | Conocer datos, esquemas y lógica crítica. |
| Matriz de integraciones | Conocer sistemas internos, terceros y APIs. |
| Matriz de accesos | Controlar permisos y responsabilidades. |
| Matriz de secretos/certificados | Controlar caducidades y responsables. |
| Runbooks técnicos | Operar y diagnosticar aplicaciones. |
| Runbooks funcionales | Entender procesos y reglas. |
| Runbooks batch | Gestionar procesos críticos y reprocesos. |
| Runbooks de despliegue | Ejecutar cambios y rollback. |
| Catálogo de alertas | Saber responder a monitorización. |
| Matriz de escalado | Saber a quién acudir. |
| Base de conocimiento | Incidencias frecuentes y workarounds. |
| Criterios de aceptación | Evidencias de transición completada. |

## 10.3 Estados documentales finales

| Estado | Significado |
|---|---|
| Validado | Revisado y aceptado para BAU. |
| Validado con restricciones | Útil, pero con gaps conocidos. |
| Pendiente BAU | No bloquea cierre, pero requiere seguimiento. |
| Obsoleto | Sustituido o no fiable. |
| No requerido | Se confirma que no aplica. |

## 10.4 Matriz de documentación final

| Documento | Aplicación / dominio | Estado | Responsable mantenimiento | Última revisión | Próxima revisión |
|---|---|---|---|---|---|
| Runbook emisión | Emisión | Validado |  |  |  |
| Matriz batch recibos | Recibos | Validado con restricciones |  |  |  |
| Catálogo alertas | Global | Validado |  |  |  |

## 10.5 Buenas prácticas

- Evitar documentación sin propietario.
- Evitar duplicidades.
- Marcar claramente documentos obsoletos.
- Mantener una fuente de verdad.
- Definir periodicidad de revisión.
- Relacionar documentos con aplicaciones.
- Integrar documentación con ITSM cuando sea posible.
- Actualizar runbooks tras incidencias relevantes.
- Mantener trazabilidad de cambios documentales.

## 10.6 Resultado esperado

- Documentación consolidada.
- Responsables asignados.
- Estado documental claro.
- Base operativa lista para BAU.

---

# 12. Actividad 6. Validar accesos, seguridad y retirada del equipo saliente

## 11.1 Objetivo

Regularizar accesos tras la transición, asegurando que el equipo entrante tiene los permisos necesarios y que el equipo saliente conserva únicamente los accesos justificados o los pierde de forma controlada.

## 11.2 Acciones necesarias

- Revisar accesos del equipo entrante.
- Confirmar accesos a herramientas críticas.
- Confirmar accesos a ITSM.
- Confirmar accesos a repositorios.
- Confirmar accesos a CI/CD.
- Confirmar accesos a monitorización y logs.
- Confirmar accesos a entornos.
- Confirmar accesos a proveedores.
- Revisar cuentas técnicas.
- Revisar secretos.
- Revisar certificados.
- Revisar accesos del equipo saliente.
- Definir fecha de revocación.
- Revocar accesos no necesarios.
- Mantener accesos residuales solo si están aprobados.
- Registrar evidencias para auditoría.

## 11.3 Matriz de retirada de accesos salientes

| Persona / equipo | Herramienta | Tipo acceso | Motivo residual | Fecha revocación | Aprobador | Estado |
|---|---|---|---|---|---|---|
|  | Git | Lectura | Soporte residual |  |  | Pendiente |
|  | Producción | Lectura logs | No requerido |  |  | Revocado |
|  | ITSM | Consulta | Cierre tickets transición |  |  | Temporal |

## 11.4 Preguntas clave

- ¿Qué accesos del saliente siguen siendo necesarios?
- ¿Durante cuánto tiempo?
- ¿Para qué casos?
- ¿Quién aprueba?
- ¿Cómo se audita?
- ¿Qué accesos deben revocarse inmediatamente?
- ¿Hay cuentas compartidas?
- ¿Hay secretos que deban rotarse?
- ¿Hay certificados bajo responsabilidad del saliente?
- ¿Hay proveedores que siguen contactando al saliente?
- ¿Se han actualizado grupos de asignación?

## 11.5 Resultado esperado

- Accesos entrantes completos.
- Accesos salientes retirados o justificados.
- Secretos y certificados bajo control.
- Evidencias de seguridad disponibles.
- Riesgo de acceso residual mitigado.

---

# 13. Actividad 7. Formalizar el soporte residual del equipo saliente

## 12.1 Objetivo

Definir, si procede, un período limitado de soporte residual posterior a la transición.

## 12.2 Cuándo tiene sentido

Puede ser conveniente mantener soporte residual si:

- Hay aplicaciones críticas con eventos poco frecuentes.
- Hay procesos batch mensuales o anuales aún no ejecutados.
- Hay cierres contables próximos.
- Hay auditorías próximas.
- Hay sistemas legacy con riesgo residual.
- Hay integraciones externas delicadas.
- Hay reprocesos no practicados.
- Hay despliegues productivos aún no ejecutados por el entrante.

## 12.3 Elementos a definir

| Elemento | Descripción |
|---|---|
| Alcance | Aplicaciones o casos cubiertos. |
| Duración | Fecha inicio y fin. |
| Horario | Laboral, extendido, guardia. |
| Canal | ITSM, correo, teléfono, bridge. |
| SLA de respuesta | Tiempo de respuesta esperado. |
| Actividades incluidas | Consulta, validación, soporte experto. |
| Actividades excluidas | Operación ordinaria, tareas BAU. |
| Aprobador | Quién autoriza intervención. |
| Coste | Si aplica contractualmente. |
| Evidencia | Cómo se registra cada intervención. |

## 12.4 Matriz de soporte residual

| Aplicación / dominio | Caso cubierto | Duración | Canal | SLA respuesta | Aprobador | Observaciones |
|---|---|---|---|---|---|---|
| Recibos | Reproceso remesas | 1 mes | ITSM | 4h | Cliente | Solo incidencias altas |
| Renovaciones | Primer ciclo mensual | 1 ciclo | Comité operativo | 24h | Cliente | Revisión postciclo |
| Emisión | Rollback productivo | 2 despliegues | Bridge | Inmediato | Change Manager | Solo si se activa rollback |

## 12.5 Resultado esperado

- Soporte saliente residual definido.
- Sin dependencia informal.
- Sin accesos innecesarios.
- Sin ambigüedad de responsabilidad.
- Retirada final planificada.

---

# 14. Actividad 8. Obtener aceptación formal del cliente

## 13.1 Objetivo

Cerrar formalmente la transición mediante aceptación del cliente basada en evidencias.

## 13.2 Elementos a presentar

- Resumen del proceso de transición.
- Aplicaciones incluidas.
- Fases ejecutadas.
- Oleadas completadas.
- Evidencias de autonomía.
- SLAs durante estabilización.
- Incidencias relevantes.
- Gaps cerrados.
- Gaps pendientes.
- Riesgos residuales.
- Soporte residual si aplica.
- Documentación consolidada.
- Accesos regularizados.
- Modelo BAU.
- Plan de mejora continua.
- Lecciones aprendidas.

## 13.3 Criterios de aceptación final

| Criterio | Evidencia |
|---|---|
| Inventario validado | Matriz de aplicaciones. |
| Aplicaciones críticas cubiertas | Matriz de criticidad y runbooks. |
| Equipo entrante operando | Tickets, métricas, actas. |
| SLAs cumplidos | Reporting de servicio. |
| Documentación consolidada | Repositorio documental. |
| Accesos regularizados | Matriz de accesos. |
| Riesgos residuales aceptados | RAID log / acta. |
| Soporte saliente definido | Matriz de soporte residual. |
| Modelo BAU activo | Documento BAU. |
| Plan de mejora continua definido | Backlog priorizado. |

## 13.4 Plantilla de acta de aceptación

```markdown
# Acta de aceptación de transición

## Datos generales

- Cliente:
- Servicio:
- Fecha:
- Participantes:

## Alcance aceptado

## Fases ejecutadas

## Evidencias revisadas

- Inventario:
- Runbooks:
- SLAs:
- Tickets:
- Despliegues:
- Batch:
- Riesgos:
- Gaps:
- Accesos:
- BAU:

## Riesgos residuales aceptados

## Gaps trasladados a BAU

## Soporte residual acordado

## Decisión

- Aceptado / Aceptado con condiciones / No aceptado

## Condiciones si aplica

## Firmas / aprobaciones
```

## 13.5 Resultado esperado

- Aceptación formal del cliente.
- Cierre contractual u operativo de transición.
- Condiciones documentadas si existen.
- Paso definitivo a BAU.

---

# 15. Actividad 9. Elaborar informe final de transición

## 14.1 Objetivo

Documentar de forma ejecutiva y operativa el resultado completo de la transición.

## 14.2 Estructura recomendada

```markdown
# Informe final de transición

## 1. Resumen ejecutivo

## 2. Alcance de la transición

## 3. Fases ejecutadas

## 4. Aplicaciones y dominios transferidos

## 5. Evidencias de transferencia

## 6. Estado de documentación

## 7. Estado de accesos

## 8. Estado de SLAs y métricas

## 9. Incidencias relevantes durante la transición

## 10. Riesgos cerrados

## 11. Riesgos residuales

## 12. Gaps cerrados

## 13. Gaps pendientes trasladados a BAU

## 14. Soporte residual del equipo saliente

## 15. Modelo BAU

## 16. Lecciones aprendidas

## 17. Recomendaciones de mejora continua

## 18. Anexos
```

## 14.3 Audiencias del informe

| Audiencia | Necesidad |
|---|---|
| Dirección cliente | Estado, riesgos, aceptación y próximos pasos. |
| IT cliente | Detalle operativo y técnico. |
| Negocio | Continuidad, impacto y canales. |
| Auditoría | Evidencias, accesos, riesgos, cumplimiento. |
| Equipo entrante | Base para BAU. |
| Equipo saliente | Cierre de responsabilidades. |

## 14.4 Resultado esperado

- Informe final aprobado.
- Evidencias consolidadas.
- Base histórica de la transición.
- Material de referencia para auditorías y mejora continua.

---

# 16. Actividad 10. Realizar sesión de lecciones aprendidas

## 15.1 Objetivo

Identificar qué ha funcionado, qué no, qué debe mejorarse y qué aprendizajes deben incorporarse al modelo BAU y a futuras transiciones.

## 15.2 Participantes recomendados

- Transition Manager.
- Service Manager.
- Líder técnico.
- Líder funcional.
- Representantes del equipo entrante.
- Representantes del equipo saliente si procede.
- Cliente IT.
- Negocio.
- Operaciones.
- Seguridad.
- PMO o calidad si aplica.

## 15.3 Preguntas clave

- ¿Qué funcionó especialmente bien?
- ¿Qué dificultó la transición?
- ¿Qué se descubrió tarde?
- ¿Qué debería haberse pedido antes?
- ¿Qué documentación fue más útil?
- ¿Qué documentación faltó?
- ¿Qué sesiones generaron más valor?
- ¿Qué riesgos se materializaron?
- ¿Qué gaps se repitieron?
- ¿Qué mejoraríamos en el modelo de gobierno?
- ¿Qué mejoraríamos en shadowing?
- ¿Qué mejoraríamos en reverse shadowing?
- ¿Qué debe incorporarse a BAU?
- ¿Qué aprendizajes aplican a futuras transiciones?

## 15.4 Matriz de lecciones aprendidas

| ID | Lección | Categoría | Impacto | Recomendación | Responsable | Aplicar en |
|---|---|---|---|---|---|---|
| LA-001 | Los accesos se solicitaron tarde | Accesos | Alto | Iniciar matriz IAM en Fase 0 |  | Futuras transiciones |
| LA-002 | Shadowing batch fue crítico | Operación | Alto | Planificar por calendario batch |  | BAU / futuras transiciones |
| LA-003 | Runbooks mejoraron tras casos reales | Conocimiento | Medio | Revisar runbooks tras incidencias |  | BAU |

## 15.5 Resultado esperado

- Lecciones aprendidas documentadas.
- Mejoras incorporadas a BAU.
- Recomendaciones para futuras transiciones.
- Cierre maduro del proceso.

---

# 17. Actividad 11. Definir plan de mejora continua

## 16.1 Objetivo

Convertir los hallazgos de la transición en un backlog ordenado de mejora continua.

La transición habrá revelado deuda técnica, gaps de observabilidad, automatización pendiente, documentación mejorable, procesos manuales y riesgos que no bloquean el cierre, pero que deben gestionarse.

## 16.2 Categorías de mejora

| Categoría | Ejemplos |
|---|---|
| Automatización | Despliegues, validaciones, reprocesos, controles. |
| Observabilidad | Dashboards, alertas, trazas, correlation ID. |
| Documentación | Runbooks, KB, diagramas, glosario. |
| Calidad | Tests, análisis estático, cobertura. |
| Seguridad | Rotación secretos, MFA, reducción permisos. |
| Datos | Catálogo, trazabilidad, calidad, anonimización. |
| Batch | Reprocesos, alertas, validaciones automáticas. |
| Integraciones | Contratos API, monitorización, circuitos de soporte. |
| Deuda técnica | Versiones obsoletas, refactorización, desacoplamiento. |
| Operación | Gestión de problemas, RCA, reducción recurrencias. |
| Cumplimiento | Evidencias, retención, auditoría, controles. |

## 16.3 Priorización de mejora continua

| Criterio | Peso |
|---|---:|
| Reducción de riesgo operativo | Alto |
| Impacto en cliente o mediador | Alto |
| Impacto regulatorio | Alto |
| Reducción de incidencias recurrentes | Alto |
| Reducción de dependencia personal | Alto |
| Mejora de SLAs | Medio/Alto |
| Facilidad de implementación | Medio |
| Coste | Medio |
| Alineamiento con roadmap cliente | Medio |

## 16.4 Backlog de mejora continua

| ID | Mejora | Categoría | Beneficio | Prioridad | Responsable | Horizonte |
|---|---|---|---|---|---|---|
| MC-001 | Automatizar validación batch recibos | Batch | Reducir riesgo financiero | Alta |  | 1-3 meses |
| MC-002 | Mejorar alertas documental | Observabilidad | Detectar fallos antes | Alta |  | 1-3 meses |
| MC-003 | Actualizar framework portal | Deuda técnica | Reducir obsolescencia | Media |  | 3-6 meses |
| MC-004 | Crear tests regresión emisión | Calidad | Reducir errores en cambios | Alta |  | 1-3 meses |

## 16.5 Resultado esperado

- Backlog de mejora continua priorizado.
- Responsables asignados.
- Riesgos no bloqueantes trasladados a BAU.
- Plan de evolución posterior a la transición.

---

# 18. Actividad 12. Integrar la gestión del conocimiento en BAU

## 17.1 Objetivo

Evitar que la documentación creada durante la transición quede obsoleta al poco tiempo.

## 17.2 Reglas de mantenimiento documental

- Todo runbook debe tener propietario.
- Todo documento debe tener fecha de revisión.
- Las incidencias relevantes deben actualizar la KB.
- Los cambios relevantes deben actualizar diagramas.
- Los nuevos gaps deben entrar al backlog BAU.
- Las lecciones aprendidas deben incorporarse a procedimientos.
- Los documentos obsoletos deben marcarse o retirarse.
- La documentación debe revisarse periódicamente.
- La base de conocimiento debe integrarse con ITSM si es posible.

## 17.3 Matriz de mantenimiento de conocimiento

| Artefacto | Propietario | Frecuencia revisión | Evento que obliga a actualizar |
|---|---|---|---|
| Runbook aplicación | Líder técnico | Trimestral | Incidencia crítica / cambio mayor |
| Guía batch | Operaciones | Mensual | Fallo batch / cambio calendario |
| Matriz escalado | Service Manager | Mensual | Cambio de equipo / proveedor |
| Catálogo alertas | Operaciones | Trimestral | Nueva alerta / falso positivo |
| Base de conocimiento | Equipo soporte | Continua | Incidencia recurrente |

## 17.4 Resultado esperado

- Conocimiento integrado en la operación.
- Documentación viva.
- Menor riesgo de degradación posterior.
- Capacidad de aprendizaje continuo.

---

---

# 19. Actividad 13. Consolidar el control ITIL del servicio en BAU

## 19.1 Objetivo

Confirmar que, tras el cierre de la transición, el servicio queda integrado en un modelo ordinario de gestión ITIL y no depende de mecanismos excepcionales de proyecto.

## 19.2 Prácticas a confirmar

| Práctica | Pregunta de validación | Evidencia esperada |
|---|---|---|
| Incident Management | ¿El equipo entrante gestiona incidencias en el flujo ITSM ordinario? | Tickets, SLAs, cierres, comunicaciones. |
| Problem Management | ¿Las recurrencias tienen problem record, workaround o acción preventiva? | Registro de problemas. |
| Change Enablement | ¿Los cambios siguen el flujo BAU de aprobación y control? | Tickets de cambio, CAB, aprobaciones. |
| Release / Deployment | ¿Versiones, despliegues y rollback tienen trazabilidad? | Registro de releases y evidencias. |
| Service Level Management | ¿Los SLAs se miden y reportan regularmente? | Panel de servicio. |
| Knowledge Management | ¿Runbooks y KB tienen propietario y ciclo de revisión? | Matriz documental final. |
| Service Configuration Management | ¿Aplicaciones, componentes y dependencias quedan actualizados? | Inventario / mini-CMDB. |
| Supplier Management | ¿Proveedores y terceros están traspasados al modelo de soporte? | Matriz de proveedores. |
| Information Security Management | ¿Accesos, secretos y certificados están regularizados? | Matriz de accesos, evidencias IAM. |
| Continual Improvement | ¿Existe backlog priorizado de mejoras? | Registro de mejora continua. |

## 19.3 Matriz de control ITIL BAU

| Área ITIL | Responsable BAU | Herramienta / repositorio | Frecuencia revisión | Estado | Observaciones |
|---|---|---|---|---|---|
| Incidencias | Service Manager | ITSM | Diario / semanal | Pendiente / Activo / Validado |  |
| Problemas | Service Manager | ITSM / backlog | Quincenal / mensual |  |  |
| Cambios | Change Manager | ITSM / CAB | Semanal |  |  |
| Releases | Líder técnico | CI/CD / ITSM | Por release |  |  |
| Conocimiento | Líder técnico / funcional | Wiki / KB | Continua |  |  |
| Configuración | Service Manager / Arquitectura | CMDB / inventario | Mensual |  |  |
| Proveedores | Service Manager | Matriz proveedores | Mensual |  |  |
| Seguridad | Seguridad / IAM | IAM / evidencias | Mensual |  |  |
| Mejora continua | Service Manager | Backlog BAU | Mensual |  |  |

## 19.4 Resultado esperado

- Prácticas BAU activas.
- Responsables asignados.
- Herramientas identificadas.
- Frecuencias de revisión definidas.
- Modelo operativo sostenible tras la transición.

---

# 20. Actividad 14. Transferir hallazgos a Problem Management y Continual Improvement

## 20.1 Objetivo

Evitar que los hallazgos de la transición se pierdan al cerrar el proyecto, transformándolos en registros operativos gestionables dentro del modelo BAU.

## 20.2 Clasificación de hallazgos

| Hallazgo | Tratamiento ITIL |
|---|---|
| Incidencia recurrente | Problem Management. |
| Workaround habitual | Knowledge Management + Problem Management. |
| Deuda técnica no bloqueante | Continual Improvement. |
| Falta de automatización | Continual Improvement. |
| Alerta insuficiente | Monitoring and Event Management + Continual Improvement. |
| Riesgo de proveedor | Supplier Management. |
| Acceso o permiso pendiente | Information Security Management. |
| Configuración no inventariada | Service Configuration Management. |
| Falta de evidencia de DR | Service Continuity Management. |

## 20.3 Registro de problemas post-transición

| ID | Problema | Incidencias relacionadas | Causa conocida | Workaround | Responsable | Prioridad | Estado |
|---|---|---|---|---|---|---|---|
| PRB-001 |  |  | Conocida / Pendiente |  |  | Alta / Media / Baja | Abierto |
| PRB-002 |  |  |  |  |  |  |  |

## 20.4 Registro de mejora continua post-transición

| ID | Mejora | Origen | Práctica ITIL relacionada | Beneficio esperado | Prioridad | Responsable | Horizonte |
|---|---|---|---|---|---|---|---|
| MC-001 |  | Transición / Incidencia / Riesgo / Auditoría | Continual Improvement |  | Alta / Media / Baja |  | 1-3 meses |
| MC-002 |  |  |  |  |  |  |  |

## 20.5 Resultado esperado

- Problemas recurrentes formalizados.
- Workarounds integrados en la KB.
- Mejoras priorizadas.
- Riesgos no bloqueantes trasladados a BAU.
- Gobierno de mejora continua activado.

# 21. Entregables de la Fase 7

| Entregable | Descripción | Responsable sugerido |
|---|---|---|
| Acta de inicio de estabilización | Confirma entrada en fase post-transición. | Transition Manager |
| Plan de estabilización | Duración, controles, métricas y responsables. | Service Manager |
| Panel de métricas de estabilización | SLAs, tickets, escalados, incidencias, batch. | Service Manager |
| Matriz final de gaps | Gaps cerrados, mitigados o trasladados a BAU. | Transition Manager |
| Matriz de riesgos residuales | Riesgos aceptados y mitigaciones. | Transition Manager |
| Repositorio documental consolidado | Documentación validada para BAU. | Líder técnico / funcional |
| Matriz de accesos final | Accesos entrantes y retirada saliente. | Seguridad / IAM |
| Matriz de soporte residual saliente | Alcance, duración y condiciones. | Transition Manager |
| Acta de aceptación final | Aceptación formal del cliente. | Cliente + Transition Manager |
| Informe final de transición | Resumen ejecutivo y operativo. | Transition Manager |
| Lecciones aprendidas | Aprendizajes y recomendaciones. | Todos |
| Backlog de mejora continua | Acciones post-transición. | Service Manager |
| Modelo BAU definitivo | Gobierno, roles, reporting y operación. | Service Manager |
| Matriz de control ITIL BAU | Prácticas activas, responsables, herramientas y frecuencia de revisión. | Service Manager |
| Registro de problemas post-transición | Incidencias recurrentes formalizadas como problemas. | Service Manager |
| Registro de cambios/releases BAU | Evidencias de que cambios y despliegues quedan integrados en operación ordinaria. | Change Manager / líder técnico |
| Registro de proveedores traspasados | Terceros, contactos, SLAs y escalados operativos. | Service Manager |
| Inventario / mini-CMDB final | Servicios, aplicaciones, componentes y dependencias actualizadas. | Service Manager / arquitectura |

---

# 22. Plantillas útiles de la Fase 7

## 19.1 Checklist de aceptación final

| Criterio | Evidencia | Estado | Observaciones |
|---|---|---|---|
| Inventario validado | Matriz aplicaciones | Pendiente / Validado |  |
| Aplicaciones críticas con runbook | Runbooks |  |  |
| SLAs cumplidos en estabilización | Panel métricas |  |  |
| Equipo entrante opera autónomamente | ITSM / actas |  |  |
| Escalados saliente bajo control | Matriz escalados |  |  |
| Gaps críticos cerrados | Matriz gaps |  |  |
| Riesgos residuales aceptados | RAID log |  |  |
| Accesos regularizados | Matriz accesos |  |  |
| Modelo BAU activo | Documento BAU |  |  |
| Soporte residual definido | Matriz soporte |  |  |
| Informe final preparado | Informe |  |  |
| Aceptación formal firmada | Acta aceptación |  |  |

## 19.2 Matriz de cierre de transición

| Área | Estado | Evidencia | Responsable | Pendiente |
|---|---|---|---|---|
| Gobierno |  |  |  |  |
| Inventario |  |  |  |  |
| Funcional |  |  |  |  |
| Técnico |  |  |  |  |
| Operación |  |  |  |  |
| Seguridad |  |  |  |  |
| Datos |  |  |  |  |
| Integraciones |  |  |  |  |
| Batch |  |  |  |  |
| BAU |  |  |  |  |

## 19.3 Informe de estabilización semanal

```markdown
# Informe semanal de estabilización

## Semana

## Estado general

- Verde / Ámbar / Rojo

## Métricas principales

| Métrica | Valor | Tendencia | Comentario |
|---|---:|---|---|
| SLA cumplido |  |  |  |
| Tickets recibidos |  |  |  |
| MTTR |  |  |  |
| Reabiertos |  |  |  |
| Incidencias P1/P2 |  |  |  |
| Escalados saliente |  |  |  |
| Batch fallidos |  |  |  |

## Incidencias relevantes

## Riesgos

## Gaps

## Acciones

## Decisiones requeridas

## Próximos pasos
```

## 19.4 Plantilla de cierre de soporte saliente

```markdown
# Cierre de soporte saliente

## Alcance

## Accesos a retirar

| Persona / equipo | Herramienta | Fecha retirada | Responsable |
|---|---|---|---|

## Soporte residual si aplica

| Caso | Canal | Duración | SLA | Aprobador |
|---|---|---|---|---|

## Riesgos

## Confirmación de retirada

## Evidencias

## Aprobación
```

---


## 22.5 Matriz de aceptación ITIL final

| Práctica ITIL | Criterio de aceptación | Evidencia | Estado | Responsable |
|---|---|---|---|---|
| Incident Management | Incidencias gestionadas por equipo entrante en BAU | ITSM / informes | Pendiente / Validado | Service Manager |
| Problem Management | Problemas recurrentes registrados o trasladados a BAU | Registro de problemas |  | Service Manager |
| Change Enablement | Cambios gestionados por proceso ordinario | Tickets de cambio / CAB |  | Change Manager |
| Release / Deployment | Despliegues y rollback trazados | Registro de releases / runbooks |  | Líder técnico |
| Service Level Management | SLAs monitorizados y reportados | Panel de servicio |  | Service Manager |
| Knowledge Management | KB y runbooks con propietario | Matriz documental |  | Líder técnico / funcional |
| Configuration Management | Inventario / CMDB actualizado | Registro de configuración |  | Arquitectura / Service Manager |
| Supplier Management | Proveedores traspasados | Matriz proveedores |  | Service Manager |
| Information Security | Accesos regularizados | Matriz IAM / evidencias |  | Seguridad / IAM |
| Continual Improvement | Backlog de mejora continua activo | Backlog BAU |  | Service Manager |

## 22.6 Registro final de proveedores traspasados

| Proveedor | Servicio | Aplicaciones afectadas | Contacto operativo | Canal soporte | SLA | Responsable BAU | Estado traspaso |
|---|---|---|---|---|---|---|---|
|  |  |  |  | ITSM / portal / email |  |  | Pendiente / Validado |

## 22.7 Registro final de cambios y releases BAU

| ID cambio/release | Aplicación | Tipo | Fecha | Responsable | Evidencia | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
|  |  | Release / hotfix / configuración |  |  |  | Correcto / Fallido / Rollback |  |

# 23. Checklist operativo de Fase 7

## 20.1 Inicio de estabilización

- [ ] Revisar cierre de Fase 6.
- [ ] Confirmar alcance estabilización.
- [ ] Confirmar criterios de cierre.
- [ ] Confirmar métricas.
- [ ] Confirmar soporte residual.
- [ ] Confirmar restricciones.
- [ ] Confirmar calendario.
- [ ] Comunicar inicio de estabilización.

## 20.2 Operación estabilizada

- [ ] Revisar tickets diariamente.
- [ ] Revisar SLAs.
- [ ] Revisar incidencias críticas.
- [ ] Revisar reabiertos.
- [ ] Revisar batch.
- [ ] Revisar cambios.
- [ ] Revisar escalados al saliente.
- [ ] Revisar percepción de negocio.
- [ ] Actualizar panel de estabilización.

## 20.3 Gaps y riesgos

- [ ] Revisar gaps críticos.
- [ ] Cerrar gaps pendientes.
- [ ] Mitigar gaps altos.
- [ ] Trasladar gaps medios/bajos a BAU.
- [ ] Revisar riesgos residuales.
- [ ] Obtener aceptación de riesgos.
- [ ] Actualizar RAID log.
- [ ] Comunicar riesgos relevantes.

## 20.4 Documentación

- [ ] Consolidar inventario.
- [ ] Consolidar runbooks técnicos.
- [ ] Consolidar runbooks funcionales.
- [ ] Consolidar runbooks batch.
- [ ] Consolidar despliegues y rollback.
- [ ] Consolidar matriz de escalado.
- [ ] Consolidar catálogo de alertas.
- [ ] Consolidar matriz de accesos.
- [ ] Asignar propietarios documentales.
- [ ] Definir revisión periódica.

## 20.5 Seguridad y accesos

- [ ] Validar accesos entrantes.
- [ ] Revisar accesos salientes.
- [ ] Revocar accesos no necesarios.
- [ ] Revisar cuentas técnicas.
- [ ] Revisar secretos.
- [ ] Revisar certificados.
- [ ] Registrar evidencias.
- [ ] Confirmar cumplimiento con seguridad/IAM.

## 20.6 Aceptación y cierre

- [ ] Preparar informe final.
- [ ] Preparar paquete de evidencias.
- [ ] Preparar acta de aceptación.
- [ ] Revisar con cliente.
- [ ] Registrar condiciones si existen.
- [ ] Obtener aceptación formal.
- [ ] Comunicar cierre.
- [ ] Activar mejora continua.
- [ ] Cerrar transición.

---


## 23.7 Checklist ITIL de cierre y estabilización

- [ ] Incident Management activo en BAU.
- [ ] Problem Management activado para recurrencias detectadas.
- [ ] Change Enablement funcionando para cambios ordinarios.
- [ ] Release y Deployment Management con evidencias de versiones y despliegues.
- [ ] Service Level Management con panel de SLAs y reporting.
- [ ] Knowledge Management integrado en la operación.
- [ ] Service Configuration Management actualizado con inventario final.
- [ ] IT Asset Management revisado para herramientas, licencias y certificados.
- [ ] Supplier Management actualizado con terceros y escalados.
- [ ] Information Security Management validado con accesos, secretos y retirada saliente.
- [ ] Service Continuity Management revisado para backup, restore y DR.
- [ ] Monitoring and Event Management validado con alertas y dashboards.
- [ ] Measurement and Reporting definido para BAU.
- [ ] Continual Improvement activado con backlog priorizado.
- [ ] Acta de aceptación final vinculada a evidencias ITIL.

# 24. Riesgos específicos de la Fase 7

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Cerrar sin evidencias suficientes | Falsa aceptación | Checklist de aceptación y paquete de evidencias. |
| Riesgos residuales no aceptados | Conflictos posteriores | RAID log final y aceptación formal. |
| Gaps críticos trasladados indebidamente a BAU | Riesgo operativo | Criterios claros de criticidad. |
| Soporte saliente retirado demasiado pronto | Pérdida de conocimiento residual | Matriz de soporte residual. |
| Soporte saliente mantenido indefinidamente | Dependencia persistente | Fecha de fin y condiciones claras. |
| Accesos salientes no revocados | Riesgo de seguridad | Plan formal de retirada. |
| Documentación queda obsoleta | Degradación del conocimiento | Propietarios y revisión periódica. |
| SLAs se degradan tras cierre | Pérdida de confianza | Vigilancia reforzada y reporting BAU. |
| Negocio no acepta percepción de estabilidad | Fricción operativa | Revisiones con negocio y comunicación. |
| Mejoras no se priorizan | Deuda técnica acumulada | Backlog de mejora continua. |
| Auditoría solicita evidencias no preparadas | Riesgo de cumplimiento | Paquete documental y trazabilidad. |
| No se capturan lecciones aprendidas | Repetición de errores | Sesión formal de retrospectiva. |
| Incidencias recurrentes no se transforman en problemas | Persistencia de fallos y degradación del servicio | Activar Problem Management con problem records, RCA y workarounds. |
| Cambios post-transición no siguen el proceso BAU | Riesgo de despliegues no controlados | Validar Change Enablement y CAB antes del cierre. |
| Proveedores no quedan integrados en soporte BAU | Escalados lentos o pérdida de contactos críticos | Matriz final de proveedores y prueba de canales de soporte. |
| Mini-CMDB o inventario final no se mantiene | Pérdida progresiva de control del servicio | Asignar propietario y frecuencia de revisión. |
| Mejora continua queda sin gobierno | Deuda técnica y operativa sin seguimiento | Crear backlog priorizado con responsable y reporting. |

---

# 25. Criterios de salida de la Fase 7

## 22.1 Checklist de salida

| Criterio | Evidencia | Estado |
|---|---|---|
| Servicio en BAU | Modelo BAU activo | Pendiente / En curso / Validado |
| Equipo entrante opera autónomamente | Tickets / métricas |  |
| SLAs cumplidos | Panel estabilización |  |
| Incidencias críticas controladas | ITSM / informes |  |
| Escalados al saliente reducidos | Matriz escalados |  |
| Soporte residual definido o cerrado | Matriz soporte |  |
| Gaps críticos cerrados | Matriz gaps |  |
| Riesgos residuales aceptados | RAID log final |  |
| Documentación consolidada | Repositorio documental |  |
| Accesos regularizados | Matriz accesos |  |
| Informe final aprobado | Informe final |  |
| Acta de aceptación firmada | Acta aceptación |  |
| Lecciones aprendidas documentadas | Registro LA |  |
| Backlog mejora continua creado | Backlog BAU |  |
| Registro de problemas recurrentes creado | Problem records / backlog problemas |  |
| Cambios y releases integrados en BAU | ITSM / CAB / evidencias despliegue |  |
| Proveedores traspasados al soporte ordinario | Matriz proveedores |  |
| Inventario / mini-CMDB actualizado | Registro configuración |  |
| Comunicación de cierre enviada | Comunicación formal |  |

## 22.2 Criterio de salida recomendado

La Fase 7 puede considerarse cerrada cuando:

> El servicio opera en modo BAU bajo responsabilidad del equipo entrante, los SLAs se mantienen bajo control, los gaps críticos están cerrados o formalmente mitigados, los riesgos residuales están aceptados, la documentación y los accesos están consolidados, el soporte saliente está retirado o limitado formalmente, y el cliente ha emitido aceptación formal de la transición.

---

# 26. Recomendaciones prácticas para liderar la Fase 7

## 23.1 Recomendaciones de enfoque

- No tratar el cierre como trámite administrativo.
- Exigir evidencias objetivas.
- Mantener vigilancia reforzada durante varias semanas.
- Separar claramente transición y mejora continua.
- No ocultar riesgos residuales.
- No aceptar gaps críticos sin mitigación.
- Regularizar accesos antes del cierre.
- Definir soporte saliente residual con fecha y alcance.
- Involucrar a negocio en la percepción de estabilidad.
- Preparar un informe final claro y honesto.
- Documentar lecciones aprendidas.
- Pasar mejoras a backlog BAU con prioridad.

## 23.2 Señales de alerta

Deben preocupar especialmente estas situaciones:

- El cierre se empuja solo por calendario.
- No hay paquete de evidencias.
- El equipo saliente sigue resolviendo casos clave.
- No se sabe qué riesgos quedan vivos.
- Los gaps se trasladan a BAU sin priorización.
- No se han revocado accesos.
- Negocio sigue contactando al equipo saliente.
- Mesa de servicio sigue asignando mal tickets.
- Los runbooks no tienen propietario.
- No existe plan de mejora continua.
- El cliente no ha revisado criterios de aceptación.
- El informe final maquilla problemas.

## 23.3 Buenas prácticas

- Cerrar por aplicación o dominio si el cierre global es complejo.
- Usar una matriz de aceptación.
- Mantener transparencia sobre restricciones.
- Formalizar aceptación con condiciones si es necesario.
- Dejar trazabilidad completa de decisiones.
- Comunicar claramente el paso a BAU.
- Revisar métricas antes de retirar soporte saliente.
- Convertir aprendizaje en mejora continua.
- Archivar evidencias de forma útil para auditoría.
- Celebrar el cierre, pero mantener disciplina operativa.

---

# 27. Resumen ejecutivo de la Fase 7

La Fase 7 es el cierre real de la transición. Su objetivo no es únicamente firmar un acta, sino confirmar que el servicio está estable, que el equipo entrante opera con autonomía y que la organización puede funcionar sin depender del equipo saliente.

Esta fase debe demostrar:

1. Que el servicio está en BAU.
2. Que el equipo entrante es responsable principal.
3. Que los SLAs se cumplen.
4. Que las aplicaciones críticas están cubiertas.
5. Que los gaps críticos están cerrados o mitigados.
6. Que los riesgos residuales están aceptados.
7. Que la documentación está consolidada.
8. Que los accesos están regularizados.
9. Que el soporte saliente está retirado o limitado.
10. Que el cliente acepta formalmente la transición.
11. Que existe un plan de mejora continua.
12. Que las lecciones aprendidas se han capturado.
13. Que las prácticas ITIL quedan activas dentro del modelo BAU.
14. Que los problemas recurrentes tienen tratamiento formal.
15. Que la mejora continua cuenta con backlog, responsable y seguimiento.

La Fase 7 no debe cerrar el aprendizaje. Debe cerrar la transición y abrir una etapa de mejora continua, donde el conocimiento recibido se mantenga vivo, el servicio se estabilice y el equipo entrante evolucione desde la continuidad hacia la excelencia operativa.

---
