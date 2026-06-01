# Modelo Operativo AI-Ready — Documentación Completa

Documento de referencia que recoge los doce componentes del modelo operativo
para la transformación del análisis funcional mediante Inteligencia Artificial.

---

## Índice

1. [Plantilla de requisito AI-ready](#1-plantilla-de-requisito-ai-ready)
2. [Glosario estructurado](#2-glosario-estructurado)
3. [Guía de Event Storming](#3-guía-de-event-storming)
4. [Prompts de generación de artefactos Jira](#4-prompts-de-generación-de-artefactos-jira)
5. [Generación automática de test cases](#5-generación-automática-de-test-cases)
6. [Validación automática de calidad](#6-validación-automática-de-calidad)
7. [Arquitectura RAG](#7-arquitectura-rag)
8. [Detección de impacto de cambios](#8-detección-de-impacto-de-cambios)
9. [Matriz de trazabilidad automática](#9-matriz-de-trazabilidad-automática)
10. [Integración con Jira API](#10-integración-con-jira-api)
11. [Plan de formación y adopción](#11-plan-de-formación-y-adopción)
12. [Gobierno del modelo](#12-gobierno-del-modelo)

---

## 1. Plantilla de requisito AI-ready

### Estructura de cinco bloques

La plantilla tiene cinco bloques con responsabilidades distintas:

| Bloque | Propósito | Rellena |
|---|---|---|
| 1. Identidad | Identificar, versionar y enrutar el requisito | Analista |
| 2. Contexto de negocio | El "por qué" para generar historias con valor real | Analista |
| 3. Comportamiento esperado | Fuente principal de test cases | Analista |
| 4. Datos | Tipos y rangos para casos de contorno | Analista + Técnico |
| 5. Metadatos técnicos | Contexto para tareas técnicas | Equipo técnico |

### Campos obligatorios (bloquean el pipeline si faltan)

- `id`, `titulo`, `epica`, `estado`, `actor`
- `descripcion` (mínimo 30 palabras)
- `evento_disparador`
- `criterios_aceptacion` (mínimo 1, con dado/cuando/entonces)
- `excepciones` (mínimo 1)
- `prioridad`

### Plantilla en uso

Ver: `templates/requisito.template.yaml`

Ejemplo completo: `requisitos/EP-04/REQ-023.yaml`

---

## 2. Glosario estructurado

### Estructura del glosario

El glosario define cuatro categorías de términos:

- **Actores**: roles que aparecen en las historias de usuario
- **Entidades**: objetos de negocio con sus atributos y estados
- **Acciones**: verbos oficiales para describir operaciones
- **Eventos**: hechos de negocio del Event Storming

### Cómo se usa en el pipeline

Se inyecta como contexto en cada llamada al LLM:
- Normaliza la terminología en los artefactos generados
- Detecta sinónimos no oficiales en la validación de consistencia
- Proporciona las reglas globales del proyecto a todos los prompts

### Gobierno del glosario

- **Propietario único**: el analista líder del proyecto
- **Proceso de cambio**: propuesta → revisión con negocio → aprobación → commit
- **Revisión periódica**: cada 2 sprints + al inicio de cada nueva épica

Ver: `glosario.yaml`

---

## 3. Guía de Event Storming

### Los tres niveles

| Nivel | Duración | Objetivo | Output |
|---|---|---|---|
| Big Picture | 4-8h | Entender el dominio completo | Mapa de épicas |
| Process Level | 2-4h | Detallar un proceso concreto | Requisitos YAML |
| Design Level | 1-2h | Diseñar agregados técnicos | Decisiones de arquitectura |

### Código de colores

| Color | Elemento | Pregunta |
|---|---|---|
| Naranja | Evento de negocio | ¿Qué ha ocurrido? |
| Azul | Comando | ¿Qué desencadena ese evento? |
| Amarillo | Actor | ¿Quién ejecuta el comando? |
| Lila | Política | ¿Qué regla activa este comando? |
| Rosa | Punto de dolor | ¿Qué no funciona bien aquí? |
| Verde | Vista/read model | ¿Qué información necesita el actor? |
| Rojo | Pregunta abierta | ¿Qué no sabemos todavía? |

### Traducción taller → YAML

| Elemento del taller | Campo del requisito |
|---|---|
| Evento naranja | `evento_disparador` |
| Comando azul | `cuando` (en el criterio AC) |
| Actor amarillo | `actor` |
| Política lila | `reglas_negocio` |
| Punto de dolor rosa | `objetivo_negocio` |
| Vista verde | `datos_salida` |
| Pregunta roja | Incertidumbre a resolver antes del requisito |

---

## 4. Prompts de generación de artefactos Jira

### Arquitectura del pipeline de prompts

```
YAML de requisito validado
        │
        ▼
[Prompt 1] → Épica (si no existe)
        │
        ▼
[Prompt 2] → Historia de usuario + criterios AC
        │
        ▼
[Prompt 3] → Tareas técnicas (por capa tecnológica)
        │
        ▼
[Prompt 4] → Subtareas (para tareas > 8h)
        │
        ▼
JSON → Revisión humana → Jira API
```

### Principios de los prompts

- **System prompt base**: define el rol, las reglas y el glosario. Se inyecta en todas las llamadas.
- **Temperatura baja** (0.1): outputs deterministas y estructurados
- **JSON puro**: sin texto antes ni después del JSON
- **Alertas de calidad**: el LLM marca en `alertas_calidad` las ambigüedades detectadas

### Prompts disponibles

Ver: `prompts/v1.1/`

---

## 5. Generación automática de test cases

### Pipeline de generación

```
Historia de usuario
        │
        ├── [Prompt 1] → Casos funcionales (flujo feliz)
        ├── [Prompt 2] → Casos negativos y de error
        ├── [Prompt 3] → Casos de contorno (boundary values)
        ├── [Prompt 4] → Scripts Gherkin (Cucumber/Behave)
        └── [Prompt 5] → Matriz de cobertura AC↔TC
```

### Tipos de test cases generados

| Tipo | Descripción | Origen |
|---|---|---|
| `funcional_positivo` | Flujo feliz verificable | Criterios AC positivos |
| `negativo_validacion` | Campo obligatorio vacío | Datos de entrada |
| `negativo_permiso` | Usuario sin permiso | Actor + permisos |
| `negativo_regla_negocio` | Violación de regla | `reglas_negocio` |
| `negativo_sistema` | Servicio no disponible | `excepciones` |
| `contorno` | Valores límite | `datos_entrada` con rangos |

### Integración con Xray/Zephyr

Los test cases se importan automáticamente via API.
Los scripts Gherkin se importan como test cases de tipo Cucumber.

---

## 6. Validación automática de calidad

### Cuatro fases de validación

| Fase | Qué verifica | Bloquea si |
|---|---|---|
| Estructural | Campos obligatorios, formatos | Falta campo obligatorio |
| Semántica | Ambigüedad, verificabilidad, atomicidad | Criterio AC no verificable |
| Consistencia | Glosario, contradicciones entre requisitos | Término no oficial en campo clave |
| Completitud | Flujos de error, datos, contornos | Sin ninguna excepción documentada |

### Niveles de problema

- **BLOQUEANTE**: impide la generación. El requisito no entra al pipeline.
- **ADVERTENCIA**: degrada la calidad pero no bloquea.
- **SUGERENCIA**: mejora opcional.

### Los 15 problemas más frecuentes

1. Verbos ambiguos en el título (gestionar, administrar)
2. Criterios de rendimiento no cuantificados ("rápido", "eficiente")
3. Criterio AC con múltiples condiciones en el "entonces"
4. Actor no especificado o genérico ("el usuario")
5. Sin flujo de error documentado
6. Datos de entrada sin tipo ni formato
7. Sinónimos del glosario mezclados
8. Requisito que mezcla dos funcionalidades
9. Contradicción con otro requisito del módulo
10. Criterio "el sistema funciona correctamente"
11. Regla de negocio sin criterio AC asociado
12. Campo "excepciones" vacío
13. Casos de contorno no documentados
14. Condición implícita ("si es necesario", "cuando proceda")
15. Dependencia de otro requisito no documentada

---

## 7. Arquitectura RAG

### Componentes

- **Chunking semántico**: cada bloque funcional del requisito se indexa como un chunk independiente
- **Vector store**: pgvector con índice HNSW, 1536 dimensiones (text-embedding-3-large)
- **Motor de consulta**: 5 consultas paralelas especializadas por tipo de contexto
- **Re-ranking**: deduplicación y filtrado por score de similitud mínimo (0.72)

### Tipos de chunks

| Tipo | Contenido | Se recupera cuando |
|---|---|---|
| `identidad_requisito` | ID, título, actor, descripción | Siempre (funcionalidad similar) |
| `reglas_negocio` | Lista de reglas del requisito | Se generan reglas nuevas |
| `criterio_aceptacion` | Un AC completo | Se generan ACs (detección duplicados) |
| `datos_interfaz` | Campos de entrada y salida | Se definen datos de un requisito |
| `flujos_error` | Excepciones documentadas | Se documentan excepciones |

### Pipeline de indexación

Los requisitos se indexan automáticamente al cambiar a estado `en-revision` o `validado`
mediante webhook de Confluence o al hacer commit en Git.

---

## 8. Detección de impacto de cambios

### Taxonomía de cambios

| Tipo | Campos | Impacto | Acción |
|---|---|---|---|
| A — Comportamiento | criterios_ac, reglas_negocio, excepciones, datos | Alto | Regenerar artefactos |
| B — Alcance | epica, actor, prioridad, titulo | Medio | Revisar antes del sprint |
| C — Administrativo | estado, version, analista | Ninguno | Re-indexar silencioso |
| D — Deprecación | estado=deprecado | Estructural | Convocar sesión de decisión |

### Plan de acción automático

Cuando se detecta un cambio Tipo A o B, el sistema:
1. Identifica los artefactos afectados via RAG
2. Verifica si hay issues en el sprint activo via Jira API
3. Genera un plan de acción priorizado via LLM
4. Notifica al equipo por Slack/Teams con nivel de urgencia

---

## 9. Matriz de trazabilidad automática

### Modelo de datos (grafo dirigido)

```
Requisito ──genera──► Historia ──genera──► Criterio AC
    │                    │                      │
    │               descompone               deriva_de
    │                    │                      │
    ▼                    ▼                      ▼
  Épica            Tarea técnica          Test Case
                        │                      │
                   implementa               verifica
                        │                      │
                        ▼                      ▼
                   Issue Jira            Ejecución TC
                        │
                    implementa
                        │
                        ▼
                     Commit
```

### Consultas disponibles

- `traza_completa_requisito(req_id)`: cadena descendente completa
- `origen_de_test_case(tc_id)`: cadena ascendente hasta el requisito
- `test_cases_de_componente(componente)`: TCs a ejecutar si se modifica el componente
- `gaps_de_trazabilidad(epica_id)`: requisitos/historias sin cobertura
- `cobertura_sprint(sprint_id)`: estado de cobertura del sprint activo

---

## 10. Integración con Jira API

### Flujo de integración

```
Artefactos JSON aprobados
        │
        ▼
[Cola de aprobación] → Revisión humana
        │
        ▼
[VerificadorIdempotencia] → ¿Ya existe este issue?
        │
        ▼
[ConstructorPayloadJira] → JSON en formato ADF v3
        │
        ▼
[ClienteJira] → POST/PUT /rest/api/3/issue
        │
        ▼
[WebhookReceiver] → Jira notifica cambios → actualiza grafo
```

### Idempotencia

Antes de crear cualquier issue, el sistema verifica si ya existe
uno generado desde el mismo requisito usando el campo personalizado
`campo_requisito_origen`. Si existe y está en progreso, no lo modifica.

### Webhook receiver

Jira notifica al sistema cuando cambia el estado de un issue.
El sistema actualiza el nodo correspondiente en el grafo de trazabilidad.

---

## 11. Plan de formación y adopción

### Cuatro fases

| Fase | Duración | Objetivo | KPI |
|---|---|---|---|
| 0. Preparación | Semanas 1-2 | Configurar entorno, medir línea base | Métricas base documentadas |
| 1. Demo y enganche | Semanas 3-4 | El equipo quiere usar el sistema | Asistencia >80% a la demo |
| 2. Piloto asistido | Meses 2-3 | 1 analista, 1 proyecto, resultados medibles | Reducción >50% tiempo de ciclo |
| 3. Expansión | Meses 4-6 | Todo el equipo, caso de éxito presentado | Frecuencia uso >90% |
| 4. Autonomía | Mes 7+ | Pipeline autónomo, gobierno activo | Tasa aprobación directa >80% |

### Métricas de adopción

- Tiempo de ciclo funcional (reunión → historias en Jira)
- Tasa de aprobación directa del pipeline
- Frecuencia de uso voluntario
- Bugs por ambigüedad funcional en producción
- Satisfacción del analista (encuesta trimestral)

### Materiales disponibles

- Guía rápida del analista (1 página)
- Guía para usuarios de negocio ("Cómo dar buenos requisitos")
- Contrato de artefactos para el equipo técnico y QA

---

## 12. Gobierno del modelo

### Los cinco pilares

| Pilar | Herramienta | Cadencia |
|---|---|---|
| Observabilidad | Dashboard de métricas + alertas automáticas | Semanal |
| Gestión de prompts | Versionado Git + evaluador automático | Por cambio |
| Calidad del repositorio | Auditoría automática del repositorio | Semanal |
| Estructura de decisión | Comité de gobierno | Mensual (45 min) |
| Gestión del riesgo | Catálogo de riesgos + planes de contingencia | Revisión trimestral |

### Proceso de cambio de un prompt

1. **Proponer**: crear `prompts/vX.Y-draft/` con el prompt modificado y el motivo
2. **Evaluar**: ejecutar `evaluar_prompts.py` sobre el dataset de referencia (20 requisitos)
3. **Aprobar**: el champion (mejoras menores) o el comité (cambios de lógica)
4. **Desplegar**: renombrar a `prompts/vX.Y/` y actualizar `config.py`

### Roles de gobierno

| Rol | Responsabilidad | Tiempo/semana |
|---|---|---|
| Champion del pipeline | Prompts, métricas, soporte al equipo | 3-4h |
| Responsable técnico | Infraestructura, cambios de arquitectura | 2-3h |
| Comité de gobierno | Decisiones estratégicas, roadmap | 45 min/mes |
| Propietario del glosario | Vocabulario del proyecto | 1-2h |

### Señales de alerta automáticas

- Tasa de aprobación directa < 60% → alerta crítica
- Score medio del repositorio < 60 → alerta alta
- Glosario sin actualización > 30 días → alerta media
- Bugs por ambigüedad +30% respecto al mes anterior → alerta alta

---

## Apéndice: Glosario del modelo operativo

| Término | Definición |
|---|---|
| AC | Criterio de Aceptación (Acceptance Criterion) |
| ADF | Atlassian Document Format (formato de descripción en Jira API v3) |
| BDD | Behaviour Driven Development — metodología que usa Gherkin |
| Chunk | Fragmento de texto indexado como unidad en el vector store |
| DoD | Definition of Done — criterios de completitud de una historia |
| Embedding | Representación numérica del significado semántico de un texto |
| Épica | Agrupación de historias relacionadas por módulo funcional |
| Event Storming | Técnica de descubrimiento colaborativo de dominios de negocio |
| Gherkin | Lenguaje de escritura de criterios AC: Dado/Cuando/Entonces |
| HNSW | Hierarchical Navigable Small World — algoritmo de índice vectorial |
| MoSCoW | Priorización: Must/Should/Could/Won't have |
| NFR | Non-Functional Requirement — requisito no funcional |
| pgvector | Extensión de PostgreSQL para almacenamiento y búsqueda vectorial |
| Pipeline | Secuencia de pasos automatizados que procesa un requisito |
| RAG | Retrieval-Augmented Generation — IA con acceso a repositorio propio |
| Run | Instancia de ejecución del pipeline sobre un requisito específico |
| Trazabilidad | Capacidad de navegar desde cualquier artefacto hasta su origen |
| Vector store | Base de datos optimizada para búsqueda por similitud semántica |
