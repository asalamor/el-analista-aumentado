# Pipeline AI — Análisis Funcional AI-Ready

Modelo operativo completo para automatizar la generación de artefactos Agile
mediante Inteligencia Artificial, desde la captura de requisitos hasta
la trazabilidad en producción.

---

## Contenido del repositorio

```
pipeline-ai/
│
├── orchestrator.py          ← Punto de entrada principal del pipeline
├── config.py                ← Configuración centralizada
├── state.py                 ← Gestión de estado de ejecución (reanudación)
├── glosario.yaml            ← Glosario de términos del proyecto
├── requirements.txt         ← Dependencias Python
├── .env.example             ← Plantilla de variables de entorno
│
├── steps/                   ← Pasos del pipeline
│   ├── s1_load.py           ← Carga y parseo del YAML
│   ├── s2_validate.py       ← Validación automática de calidad
│   ├── s3_rag_context.py    ← Recuperación de contexto RAG
│   ├── s4_generate.py       ← Generación de artefactos Jira
│   ├── s5_test_cases.py     ← Generación de test cases
│   ├── s6_impact.py         ← Análisis de impacto de cambios
│   ├── s7_traceability.py   ← Registro en el grafo de trazabilidad
│   ├── s8_approval.py       ← Aprobación humana interactiva
│   └── s9_push.py           ← Push a Jira y Xray
│
├── rag/
│   └── repositorio_rag.py   ← Motor de indexación y consulta vectorial
│
├── trazabilidad/
│   └── motor_trazabilidad.py ← Grafo de trazabilidad (nodos y aristas)
│
├── jira/
│   ├── conector_jira.py     ← Cliente Jira API v3 con idempotencia
│   └── conector_xray.py     ← Importación de test cases a Xray
│
├── sql/
│   └── schema.sql           ← Esquema PostgreSQL completo (RAG + trazabilidad)
│
├── prompts/
│   └── v1.1/                ← Prompts versionados del pipeline
│       ├── p1_epica.txt
│       ├── p2_historia.txt
│       ├── p3_tareas.txt
│       └── stack_tecnologico.txt
│
├── templates/
│   └── requisito.template.yaml  ← Plantilla base AI-ready
│
├── requisitos/
│   └── EP-04/
│       └── REQ-023.yaml     ← Ejemplo completo de requisito
│
├── docs/                    ← Documentación del modelo operativo
│
├── runs/                    ← Estado de ejecuciones (auto-generado)
└── reports/                 ← Informes de ejecución (auto-generado)
```

---

## Instalación rápida

### 1. Prerrequisitos

- Python 3.11+
- PostgreSQL 14+ con extensión `pgvector`
- Cuenta Anthropic con API key
- Proyecto Jira con API token

### 2. Clonar e instalar dependencias

```bash
git clone https://github.com/tu-empresa/pipeline-ai.git
cd pipeline-ai
python -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores reales
```

### 4. Inicializar la base de datos

```bash
psql -U postgres -c "CREATE DATABASE pipeline_ai;"
psql -U postgres -c "CREATE USER pipeline WITH PASSWORD 'tu-password';"
psql -U postgres -c "GRANT ALL ON DATABASE pipeline_ai TO pipeline;"
psql -U pipeline -d pipeline_ai -f sql/schema.sql
```

### 5. Verificar la instalación

```bash
python orchestrator.py --req REQ-023 --dry-run
```

Si todo está correctamente configurado, verás el pipeline ejecutarse sobre
el requisito de ejemplo y generar los artefactos en modo dry-run.

---

## Uso básico

### Procesar un requisito individual

```bash
# Modo dry-run (no push a Jira)
python orchestrator.py --req REQ-023 --dry-run

# Modo producción (push a Jira con aprobación interactiva)
python orchestrator.py --req REQ-023

# Sin aprobación interactiva (para CI/CD)
python orchestrator.py --req REQ-023 --sin-aprobacion

# Reanudar desde un paso específico
python orchestrator.py --req REQ-023 --desde s4_generacion_artefactos
```

### Procesar una épica completa

```bash
# Todos los requisitos de EP-04, de 2 en 2
python orchestrator.py --epica EP-04 --paralelo 2

# Dry-run de la épica completa
python orchestrator.py --epica EP-04 --dry-run --sin-aprobacion
```

### Pasos disponibles para `--desde`

```
s1_carga
s2_validacion
s3_rag_contexto
s4_generacion_artefactos
s5_generacion_test_cases
s6_analisis_impacto
s7_registro_trazabilidad
s8_aprobacion
s9_push_jira
s9b_push_xray
```

---

## Flujo del pipeline

```
YAML de requisito
     │
     ▼
[s1] Carga y parseo del YAML
     │
     ▼
[s2] Validación automática de calidad
     │ (bloqueante si hay errores BLOQUEANTES)
     ▼
[s3] Recuperación de contexto RAG
     │ (no bloqueante)
     ▼
[s4] Generación de artefactos Jira (LLM)
     │ Épica + Historia + Tareas técnicas
     ▼
[s5] Generación de test cases (LLM)
     │ Positivos + Negativos + Contorno + Gherkin
     ▼
[s6] Análisis de impacto (solo si es actualización)
     │
     ▼
[s7] Registro en grafo de trazabilidad
     │
     ▼
[s8] Aprobación humana
     │ Aprobar / Editar / Rechazar
     ▼
[s9] Push a Jira API
     │
     ▼
[s9b] Push a Xray (test cases)
```

---

## Crear un nuevo requisito

1. Copia la plantilla base:
   ```bash
   cp templates/requisito.template.yaml requisitos/EP-XX/REQ-NNN.yaml
   ```

2. Rellena los campos obligatorios (marcados como `# OBLIGATORIO`).

3. Valida el requisito antes de ejecutar el pipeline completo:
   ```bash
   python orchestrator.py --req REQ-NNN --dry-run
   ```

4. Si la validación pasa, ejecuta el pipeline completo:
   ```bash
   python orchestrator.py --req REQ-NNN
   ```

---

## Actualizar el glosario

El glosario (`glosario.yaml`) define el vocabulario oficial del proyecto.
Se inyecta en todos los prompts del pipeline para garantizar coherencia.

Proceso de actualización:
1. Editar `glosario.yaml` añadiendo el nuevo término.
2. Incrementar la versión en el campo `metadata.version`.
3. Notificar al equipo (el glosario es un documento de autoridad compartido).

---

## Configuración de campos personalizados de Jira

Para obtener los IDs de los campos personalizados de tu instancia Jira:

```bash
curl -u tu-email@empresa.com:TU_API_TOKEN \
  https://tu-empresa.atlassian.net/rest/api/3/field \
  | python -m json.tool \
  | grep -A2 '"name": "Story Points"'
```

Actualiza los valores en `.env`:
```
JIRA_FIELD_STORY_POINTS=customfield_XXXXX
JIRA_FIELD_EPIC_LINK=customfield_XXXXX
JIRA_FIELD_EPIC_NAME=customfield_XXXXX
JIRA_FIELD_REQ_ORIGEN=customfield_XXXXX
```

---

## Governance y mantenimiento

### Versionado de prompts

Los prompts viven en `prompts/v1.1/`. Para proponer un cambio:

1. Crear carpeta `prompts/v1.2-draft/` con los prompts modificados.
2. Ejecutar evaluación comparativa:
   ```bash
   python gobierno/evaluar_prompts.py --desde v1.1 --hasta v1.2-draft
   ```
3. Revisar el informe comparativo y obtener aprobación del champion.
4. Si se aprueba, renombrar a `prompts/v1.2/` y actualizar `config.py`.

### Métricas del pipeline

Los informes de cada ejecución se guardan en `reports/`.
Para generar el dashboard semanal:

```bash
python gobierno/dashboard.py --semana 2025-W20
```

---

## Arquitectura técnica

| Componente | Tecnología | Propósito |
|---|---|---|
| LLM | Claude Sonnet (Anthropic) | Generación y validación de artefactos |
| Vector store | pgvector (PostgreSQL) | Índice semántico del repositorio RAG |
| Grafo trazabilidad | PostgreSQL | Nodos y aristas de artefactos |
| API Jira | REST v3 | Creación de épicas, historias, tareas |
| API Xray | REST v1 | Importación de test cases |
| CI/CD | GitHub Actions | Ejecución automática en push |

---

## Documentación adicional

Todos los puntos del modelo operativo están documentados en la carpeta `docs/`:

- `docs/01_01_taller_de_plantillas.md`
- `docs/01_02_glosario_estructurado.md`
- `docs/01_03_guia_event_storming.md`
- `docs/02_04_prompts_generacion_jira.md`
- `docs/02_05_generacion_test_cases.md`
- `docs/02_06_validacion_automatica_requisitos.md`
- `docs/03_07_arquitectura_rag_requisitos.md`
- `docs/03_08_deteccion_impacto_cambios.md`
- `docs/03_09_matriz_trazabilidad_automatica.md`
- `docs/04_10_integracion_jira_api.md`
- `docs/04_11_plan_formacion_adopcion.md`
- `docs/04_12_gobierno_del_modelo.md`

---

## Licencia

Uso interno. No distribuir fuera de la organización.
