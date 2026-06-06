# Notificaciones y bandeja de entrada del analista

## El problema que resuelve este componente

El pipeline genera valor en dos direcciones: hacia Jira (artefactos) y hacia el analista (información). La segunda dirección es la que más frecuentemente se descuida. Un sistema que produce alertas sin criterio convierte la bandeja de entrada en ruido y el analista en alguien que aprende a ignorarla. Un sistema que no produce alertas cuando debería deja que los problemas lleguen al sprint sin aviso.

El objetivo de este componente no es informar de todo lo que ocurre. Es hacer que el analista actúe en el momento correcto sobre el problema correcto, sin que tenga que monitorizar activamente el estado del pipeline.

La diferencia entre un sistema de notificaciones bien diseñado y uno mal diseñado no está en la tecnología: está en la decisión de qué merece interrumpir a una persona.

---

## Taxonomía de eventos notificables

Antes de construir cualquier canal de notificación, hay que clasificar todos los eventos que el pipeline puede generar según dos dimensiones: urgencia (¿cuándo debe saber el analista esto?) y acción requerida (¿qué debe hacer el analista con esta información?).

Esta clasificación determina el canal, el formato y si el evento merece notificación en absoluto.

```
EVENTOS DEL PIPELINE
│
├── TIER 1 — Acción inmediata requerida (interrumpen el trabajo)
│   ├── Artefactos pendientes de aprobación en la cola
│   ├── Validación bloqueada en requisito en estado 'en-revision'
│   ├── Impacto de cambio detectado con nivel CRITICO
│   │   (hay issues en el sprint activo afectados)
│   └── Fallo del pipeline en un paso bloqueante
│       (el run quedó interrumpido y no se puede reanudar solo)
│
├── TIER 2 — Revisión antes del próximo sprint (no interrumpen)
│   ├── Impacto de cambio con nivel ALTO
│   │   (artefactos afectados fuera del sprint activo)
│   ├── Validación aprobada con advertencias
│   │   (el pipeline continuó pero hay campos incompletos)
│   ├── Duplicado probable detectado por RAG
│   │   (similitud > 0.90 con un requisito existente)
│   ├── Glosario sin actualizar en más de 30 días
│   └── Requisito en estado 'borrador' sin actividad en 14 días
│
├── TIER 3 — Información periódica (resúmenes, no alertas)
│   ├── Resumen semanal del estado de la cola de aprobación
│   ├── Auditoría semanal del repositorio de requisitos
│   ├── Métricas de calidad del pipeline (tasa de aprobación directa)
│   └── Matriz de trazabilidad generada para una épica
│
└── NO NOTIFICAR (registrar en log, no enviar al analista)
    ├── Re-indexación del RAG completada
    ├── Push a Jira exitoso (el analista ya aprobó, no necesita confirmación)
    ├── Impacto de cambio con nivel BAJO o NINGUNO
    ├── Cambios de estado administrativos en requisitos
    │   (borrador → en-revision, cambio de analista, actualización de metadatos)
    └── Resultados de ejecución de test cases (van al QA lead, no al analista)
```

La regla más importante del diseño de notificaciones es que **los eventos de Tier 3 nunca deben llegar como interrupciones**. Son resúmenes periódicos con cadencia fija. El analista los consulta cuando quiere; el sistema no los empuja en tiempo real.

---

## Arquitectura del sistema de notificaciones

El sistema tiene tres capas que operan de forma independiente y pueden activarse gradualmente:

```
PIPELINE (genera eventos)
        │
        ▼
CLASIFICADOR DE EVENTOS
(decide tier, canal y destinatario)
        │
        ├──► TIER 1 ──► Canal inmediato (Slack / Teams / email)
        │
        ├──► TIER 2 ──► Cola de bandeja de entrada
        │                       │
        │               ┌───────▼───────────┐
        │               │  BANDEJA DE ENTRADA│
        │               │  del analista      │
        │               │  (interfaz web o   │
        │               │   Confluence)      │
        │               └───────────────────┘
        │
        ├──► TIER 3 ──► Scheduler periódico
        │               (lunes 8:00 resumen semanal)
        │
        └──► NO NOTIF ──► Log de sistema (sin envío)
```

---

## El clasificador de eventos

El clasificador es el componente central. Recibe el evento del pipeline y determina qué hacer con él. Funciona como un conjunto de reglas evaluadas en orden, con la primera coincidencia ganando.

```python
# notificador/clasificador.py
"""
Clasifica los eventos del pipeline y determina:
  - Si deben notificarse
  - A quién
  - Por qué canal
  - Con qué urgencia

El orden de las reglas importa: la primera que coincide gana.
No evaluamos todas las reglas para cada evento.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Tier(str, Enum):
    UNO   = "1"   # Acción inmediata
    DOS   = "2"   # Revisión antes del sprint
    TRES  = "3"   # Resumen periódico
    NADA  = "0"   # No notificar


class Canal(str, Enum):
    INMEDIATO  = "inmediato"   # Slack / Teams en tiempo real
    BANDEJA    = "bandeja"     # Bandeja de entrada del analista
    RESUMEN    = "resumen"     # Incluir en el resumen semanal
    LOG        = "log"         # Solo registro interno


@dataclass
class DecisionNotificacion:
    tier:        Tier
    canal:       Canal
    destinatario: str    # "analista" | "champion" | "product_owner" | "qa_lead"
    asunto:      str     # Una línea, máx. 80 caracteres
    cuerpo:      str     # El mensaje completo
    accion:      Optional[str]  # La única acción que se pide al destinatario
    url_accion:  Optional[str]  # URL directa a donde tomar la acción


# Tabla de reglas ordenadas por prioridad
# Cada regla tiene: condición → decisión
REGLAS_CLASIFICACION = [

    # ── TIER 1: Acción inmediata ─────────────────────────────────────────────

    {
        "evento": "aprobacion_pendiente",
        "condicion": lambda e: e.get("tiempo_en_cola_minutos", 0) == 0,
        # Notificar al instante cuando llega a la cola, no cuando lleva tiempo
        "tier": Tier.UNO,
        "canal": Canal.INMEDIATO,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"⏳ Artefactos listos para revisar — {e['requisito_id']}"
        ),
        "accion": "Revisar y aprobar (o rechazar) los artefactos generados",
    },
    {
        "evento": "validacion_bloqueada",
        "condicion": lambda e: e.get("tiene_bloqueantes", False),
        "tier": Tier.UNO,
        "canal": Canal.INMEDIATO,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"🚫 Requisito bloqueado — {e['requisito_id']} "
            f"({e.get('num_bloqueantes', '?')} problema(s))"
        ),
        "accion": "Corregir los campos marcados como BLOQUEANTE en el informe",
    },
    {
        "evento": "impacto_cambio",
        "condicion": lambda e: e.get("nivel_urgencia") == "CRITICO",
        # CRITICO = hay issues en el sprint activo afectados
        "tier": Tier.UNO,
        "canal": Canal.INMEDIATO,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"🔴 Cambio crítico en {e['requisito_id']} "
            f"— hay {e.get('issues_en_sprint', 0)} issue(s) en sprint activo"
        ),
        "accion": "Notificar al equipo de desarrollo antes de que continúe el trabajo",
    },
    {
        "evento": "pipeline_fallo_bloqueante",
        "condicion": lambda e: e.get("paso_fallido") not in (
            "s3_rag_contexto",   # El RAG no es bloqueante
            "s7_registro_trazabilidad",  # La trazabilidad tampoco
            "s9b_push_xray",     # Xray tampoco
        ),
        "tier": Tier.UNO,
        "canal": Canal.INMEDIATO,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"💥 Pipeline detenido — {e['requisito_id']} "
            f"(paso: {e.get('paso_fallido', '?')})"
        ),
        "accion": "Revisar el error y reanudar con --desde o crear los artefactos manualmente",
    },

    # ── TIER 2: Revisión antes del sprint ────────────────────────────────────

    {
        "evento": "impacto_cambio",
        "condicion": lambda e: e.get("nivel_urgencia") == "ALTO",
        "tier": Tier.DOS,
        "canal": Canal.BANDEJA,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"🟡 Cambio con impacto en {e['requisito_id']} "
            f"— {e.get('total_afectados', 0)} artefacto(s) a revisar"
        ),
        "accion": "Revisar los artefactos afectados antes del próximo refinamiento",
    },
    {
        "evento": "validacion_aprobada_con_advertencias",
        "condicion": lambda e: len(e.get("advertencias", [])) > 0,
        "tier": Tier.DOS,
        "canal": Canal.BANDEJA,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"⚠️ {e['requisito_id']} aprobado con {len(e['advertencias'])} "
            f"advertencia(s) — revisar antes del sprint"
        ),
        "accion": "Completar los campos marcados como ADVERTENCIA antes del refinamiento",
    },
    {
        "evento": "duplicado_probable",
        "condicion": lambda e: e.get("similitud_maxima", 0) >= 0.90,
        "tier": Tier.DOS,
        "canal": Canal.BANDEJA,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"🔁 Posible duplicado — {e['requisito_id']} "
            f"similar a {e.get('requisito_similar', '?')} "
            f"({int(e.get('similitud_maxima', 0) * 100)}%)"
        ),
        "accion": "Verificar si este requisito es realmente distinto al existente",
    },
    {
        "evento": "glosario_desactualizado",
        "condicion": lambda e: e.get("dias_sin_actualizar", 0) >= 30,
        "tier": Tier.DOS,
        "canal": Canal.BANDEJA,
        "destinatario": "champion",
        "generar_asunto": lambda e: (
            f"📖 Glosario sin actualizar desde hace "
            f"{e.get('dias_sin_actualizar', '?')} días"
        ),
        "accion": "Revisar si han aparecido términos nuevos en los últimos requisitos",
    },
    {
        "evento": "requisito_inactivo",
        "condicion": lambda e: (
            e.get("estado") == "borrador" and
            e.get("dias_sin_cambios", 0) >= 14
        ),
        "tier": Tier.DOS,
        "canal": Canal.BANDEJA,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: (
            f"💤 {e['requisito_id']} lleva {e['dias_sin_cambios']} días "
            f"en borrador sin actividad"
        ),
        "accion": "Retomar el requisito, bloquearlo o marcarlo como descartado",
    },

    # ── TIER 3: Resumen periódico (nunca interrumpen) ────────────────────────

    {
        "evento": "resumen_semanal",
        "condicion": lambda e: True,
        "tier": Tier.TRES,
        "canal": Canal.RESUMEN,
        "destinatario": "analista_responsable",
        "generar_asunto": lambda e: "📊 Resumen semanal del pipeline",
        "accion": None,  # No hay una acción específica; es solo información
    },
    {
        "evento": "auditoria_repositorio",
        "condicion": lambda e: True,
        "tier": Tier.TRES,
        "canal": Canal.RESUMEN,
        "destinatario": "champion",
        "generar_asunto": lambda e: "🔍 Auditoría semanal del repositorio",
        "accion": None,
    },

    # ── NO NOTIFICAR ─────────────────────────────────────────────────────────

    {
        "evento": "reindexacion_rag",
        "condicion": lambda e: True,
        "tier": Tier.NADA,
        "canal": Canal.LOG,
        "destinatario": "sistema",
        "generar_asunto": lambda e: "",
        "accion": None,
    },
    {
        "evento": "push_jira_exitoso",
        "condicion": lambda e: True,
        # El analista ya aprobó. No necesita saber que el push fue bien.
        # Si fue mal, el pipeline ya lo habría notificado como fallo bloqueante.
        "tier": Tier.NADA,
        "canal": Canal.LOG,
        "destinatario": "sistema",
        "generar_asunto": lambda e: "",
        "accion": None,
    },
    {
        "evento": "impacto_cambio",
        "condicion": lambda e: e.get("nivel_urgencia") in ("BAJO", "NINGUNO"),
        "tier": Tier.NADA,
        "canal": Canal.LOG,
        "destinatario": "sistema",
        "generar_asunto": lambda e: "",
        "accion": None,
    },
]


def clasificar_evento(tipo_evento: str, datos_evento: dict) -> DecisionNotificacion:
    """
    Clasifica un evento del pipeline y retorna la decisión de notificación.
    La primera regla que coincide con el tipo de evento y su condición gana.
    Si ninguna regla coincide, el evento se registra solo en el log.
    """
    for regla in REGLAS_CLASIFICACION:
        if regla["evento"] != tipo_evento:
            continue
        try:
            if not regla["condicion"](datos_evento):
                continue
        except Exception:
            continue

        asunto = regla["generar_asunto"](datos_evento)
        return DecisionNotificacion(
            tier=regla["tier"],
            canal=regla["canal"],
            destinatario=regla["destinatario"],
            asunto=asunto,
            cuerpo="",          # Lo construye el formateador en el siguiente paso
            accion=regla.get("accion"),
            url_accion=None,    # Lo resuelve el despachador con el contexto de entorno
        )

    # Ninguna regla coincidió: solo log
    return DecisionNotificacion(
        tier=Tier.NADA,
        canal=Canal.LOG,
        destinatario="sistema",
        asunto=f"[LOG] Evento sin regla de clasificación: {tipo_evento}",
        cuerpo=str(datos_evento),
        accion=None,
        url_accion=None,
    )
```

---

## La bandeja de entrada del analista

La bandeja de entrada no es el correo electrónico. Es una vista centralizada de todos los eventos de Tier 2 pendientes de atención, ordenados por prioridad y agrupados por requisito.

La razón de tener una bandeja separada del correo o de Slack es que los eventos de Tier 2 no requieren respuesta inmediata pero tampoco deben perderse. Si llegan a Slack se mezclan con conversaciones de equipo y se olvidan. Si llegan al correo se entierran bajo otras notificaciones. La bandeja de entrada es el lugar donde el analista va cuando tiene tiempo de revisar el estado del pipeline, no cuando Slack le interrumpe.

### Opciones de implementación

Hay tres niveles de complejidad, adoptables gradualmente según la madurez del equipo:

**Nivel 1 — Confluence como bandeja (recomendado para el piloto)**

Una página de Confluence con una macro que renderiza la tabla de eventos pendientes consultando la base de datos del pipeline. El analista la visita una vez al día. Es la opción más sencilla y la que menos infraestructura requiere.

**Nivel 2 — Canal de Slack dedicado**

Un canal `#pipeline-ai-bandeja` donde solo llegan los eventos de Tier 2 formateados como mensajes con botones de acción. El analista lo revisa cuando quiere, sin que sea su canal principal de comunicación.

**Nivel 3 — Interfaz web del pipeline**

La interfaz web del orquestador incluye una sección de bandeja de entrada con filtros, ordenación y acciones directas. Es el nivel más completo pero requiere más desarrollo inicial.

### Estructura de la tabla de bandeja (Nivel 1)

```sql
-- notificaciones/bandeja_entrada.sql
-- Tabla que almacena los eventos de Tier 2 pendientes de atención
-- Los eventos de Tier 1 no pasan por aquí: van directo al canal inmediato
-- Los eventos de Tier 3 tampoco: se generan en el scheduler, no se almacenan

CREATE TABLE bandeja_entrada (
    id              SERIAL PRIMARY KEY,
    tipo_evento     TEXT NOT NULL,
    requisito_id    TEXT,               -- NULL para eventos de proyecto (glosario, etc.)
    analista_id     TEXT NOT NULL,      -- A quién va dirigido
    asunto          TEXT NOT NULL,
    datos_evento    JSONB NOT NULL,     -- Datos completos del evento para renderizar
    accion          TEXT,               -- La acción requerida en lenguaje natural
    url_accion      TEXT,               -- URL directa (Confluence, Jira, interfaz web)
    prioridad       INTEGER DEFAULT 50, -- 0-100; mayor número = mayor prioridad
    leido           BOOLEAN DEFAULT FALSE,
    resuelto        BOOLEAN DEFAULT FALSE,
    fecha_creacion  TIMESTAMP DEFAULT NOW(),
    fecha_limite    TIMESTAMP,          -- NULL = sin límite; si hay sprint, la fecha de inicio
    fecha_leido     TIMESTAMP,
    fecha_resuelto  TIMESTAMP
);

-- Índice para consultar la bandeja de un analista ordenada por prioridad
CREATE INDEX idx_bandeja_analista_pendiente
    ON bandeja_entrada (analista_id, resuelto, prioridad DESC, fecha_creacion DESC)
    WHERE resuelto = FALSE;

-- Índice para limpiar eventos antiguos ya resueltos
CREATE INDEX idx_bandeja_resuelto_fecha
    ON bandeja_entrada (fecha_resuelto)
    WHERE resuelto = TRUE;
```

### Consulta de la bandeja activa de un analista

```python
# notificador/bandeja.py

def obtener_bandeja(analista_id: str, db) -> list[dict]:
    """
    Retorna todos los eventos pendientes de un analista,
    ordenados por prioridad descendente y luego por fecha de creación.

    Los eventos resueltos no aparecen.
    Los eventos leídos aparecen con menor peso visual pero siguen presentes
    hasta que se resuelven — leer no es resolver.
    """
    with db.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                tipo_evento,
                requisito_id,
                asunto,
                accion,
                url_accion,
                prioridad,
                leido,
                fecha_creacion,
                fecha_limite,
                EXTRACT(EPOCH FROM (NOW() - fecha_creacion)) / 3600
                    AS horas_desde_creacion,
                datos_evento
            FROM bandeja_entrada
            WHERE analista_id = %s
              AND resuelto = FALSE
            ORDER BY
                prioridad DESC,
                fecha_creacion DESC
            LIMIT 50   -- La bandeja no debería nunca superar 50 items activos
                       -- Si lo supera, hay un problema de gobernanza, no de la bandeja
        """, (analista_id,))

        columnas = [desc[0] for desc in cur.description]
        return [dict(zip(columnas, fila)) for fila in cur.fetchall()]


def marcar_resuelto(evento_id: int, analista_id: str, db):
    """
    Marca un evento como resuelto. El analista declara que ha tomado la acción.
    No valida que la acción se haya tomado realmente — esa responsabilidad
    es del analista, no del sistema.
    """
    with db.cursor() as cur:
        cur.execute("""
            UPDATE bandeja_entrada
            SET resuelto = TRUE,
                fecha_resuelto = NOW()
            WHERE id = %s
              AND analista_id = %s  -- Un analista solo puede resolver sus propios eventos
        """, (evento_id, analista_id))
        db.commit()


def calcular_prioridad(tipo_evento: str, datos_evento: dict) -> int:
    """
    Calcula la prioridad de un evento en la bandeja (0-100).
    Se usa para ordenar los eventos cuando el analista abre la bandeja.
    Un evento con prioridad 100 aparece siempre el primero.

    La prioridad no determina si se notifica (eso lo hace el clasificador)
    sino en qué orden el analista los ve cuando tiene tiempo de revisarlos.
    """
    base = {
        "impacto_cambio":                   80,
        "duplicado_probable":               70,
        "validacion_aprobada_con_advertencias": 60,
        "requisito_inactivo":               40,
        "glosario_desactualizado":          30,
    }.get(tipo_evento, 50)

    # Ajustes según el contexto del evento
    ajuste = 0

    # Si hay un sprint próximo, los eventos de impacto suben de prioridad
    if datos_evento.get("hay_sprint_en_menos_de_7_dias"):
        ajuste += 15

    # Si el requisito ya tiene historia en Jira, el impacto es más urgente
    if datos_evento.get("tiene_historia_en_jira"):
        ajuste += 10

    # Si lleva más de 3 días en la bandeja sin que el analista lo haya leído, sube
    horas = datos_evento.get("horas_desde_creacion", 0)
    if horas > 72:
        ajuste += 10

    return min(100, base + ajuste)
```

---

## Formatos de notificación por canal

### Canal inmediato — mensaje de Slack / Teams

El mensaje debe poderse leer en diez segundos y dejar claro sin ambigüedad qué tiene que hacer el analista. Sin preámbulos, sin resúmenes del contexto que el analista no pidió.

El formato tiene tres partes fijas: **qué pasó** (una frase), **dónde actuar** (un enlace directo), **qué hacer** (una sola instrucción).

```python
# notificador/formateadores.py

def formatear_slack_tier1(decision: DecisionNotificacion, datos: dict) -> dict:
    """
    Construye el payload de Slack para un evento de Tier 1.

    El formato usa Slack Block Kit para que el botón de acción
    sea clicable directamente desde el mensaje, sin copiar URLs.
    """

    # Iconos por tipo de evento para reconocimiento visual inmediato
    ICONOS = {
        "aprobacion_pendiente":     "⏳",
        "validacion_bloqueada":     "🚫",
        "impacto_cambio":           "🔴",
        "pipeline_fallo_bloqueante":"💥",
    }
    icono = ICONOS.get(datos.get("tipo_evento", ""), "⚠️")

    bloques = [
        # Bloque de cabecera: qué pasó
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{icono} *{decision.asunto}*"
            }
        },
        # Bloque de acción requerida: qué hacer (una sola frase)
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Acción:* {decision.accion}"
            }
        },
    ]

    # Botón de acción directa si hay URL
    if decision.url_accion:
        bloques.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Ir a revisar →"},
                    "style": "primary",
                    "url": decision.url_accion
                }
            ]
        })

    # Contexto adicional solo si es relevante para tomar la decisión
    # (no para dar información general que el analista ya tiene)
    contexto = _construir_contexto_relevante(datos)
    if contexto:
        bloques.append({
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": contexto}]
        })

    return {"blocks": bloques}


def _construir_contexto_relevante(datos: dict) -> str:
    """
    Construye la línea de contexto adicional del mensaje.
    Solo incluye información que el analista necesita para actuar,
    no un resumen general del estado del pipeline.
    """
    partes = []

    tipo = datos.get("tipo_evento")

    if tipo == "aprobacion_pendiente":
        historia = datos.get("historia_summary", "")[:60]
        n_tareas = datos.get("n_tareas", 0)
        n_tc = datos.get("n_test_cases", 0)
        if historia:
            partes.append(f"Historia: _{historia}_")
        if n_tareas:
            partes.append(f"{n_tareas} tareas · {n_tc} test cases")

    elif tipo == "validacion_bloqueada":
        n_bloq = datos.get("num_bloqueantes", 0)
        campo_principal = datos.get("campo_principal_bloqueante", "")
        if n_bloq:
            partes.append(f"{n_bloq} problema(s) bloqueante(s)")
        if campo_principal:
            partes.append(f"Campo principal: `{campo_principal}`")

    elif tipo == "impacto_cambio":
        issues = datos.get("issues_en_sprint", [])
        if issues:
            keys = ", ".join(i.get("key", "") for i in issues[:3])
            partes.append(f"Issues en sprint: {keys}")
        afectados = datos.get("total_afectados", 0)
        if afectados:
            partes.append(f"Artefactos afectados: {afectados}")

    elif tipo == "pipeline_fallo_bloqueante":
        paso = datos.get("paso_fallido", "")
        error = datos.get("error_resumen", "")[:80]
        if paso:
            partes.append(f"Paso: `{paso}`")
        if error:
            partes.append(f"Error: _{error}_")

    return "  ·  ".join(partes)
```

### Resumen semanal — email o Confluence

El resumen semanal se genera cada lunes a las 8:00 y contiene todo lo que no requirió atención inmediata durante la semana anterior. No es una lista de todo lo que ocurrió: es una vista del estado actual del pipeline con los gaps que necesitan atención.

```python
# notificador/resumen_semanal.py

def generar_resumen_semanal(analista_id: str, db, motor_trazabilidad) -> str:
    """
    Genera el resumen semanal en Markdown para publicar en Confluence
    o enviar por email.

    Contiene cuatro secciones fijas en orden de importancia:
    1. Bandeja de entrada pendiente (si hay items sin resolver)
    2. Estado del repositorio de requisitos
    3. Cobertura de trazabilidad de las épicas activas
    4. Una sola recomendación de acción para la semana
    """

    bandeja = obtener_bandeja(analista_id, db)
    pendientes = [b for b in bandeja if not b["leido"]]
    leidos_sin_resolver = [b for b in bandeja if b["leido"]]

    # Sección 1: Bandeja de entrada
    seccion_bandeja = _formatear_seccion_bandeja(pendientes, leidos_sin_resolver)

    # Sección 2: Estado del repositorio
    stats_repo = _calcular_stats_repositorio(analista_id, db)
    seccion_repo = _formatear_seccion_repositorio(stats_repo)

    # Sección 3: Cobertura de trazabilidad
    cobertura = _calcular_cobertura_epicas_activas(analista_id, motor_trazabilidad)
    seccion_trazabilidad = _formatear_seccion_trazabilidad(cobertura)

    # Sección 4: Una sola recomendación
    recomendacion = _generar_recomendacion_principal(
        pendientes, stats_repo, cobertura
    )

    return f"""# Resumen semanal del pipeline — {_fecha_lunes()}

_{analista_id}_

---

{seccion_bandeja}

{seccion_repo}

{seccion_trazabilidad}

---

## Esta semana, una sola cosa

{recomendacion}

---

_Generado automáticamente el {_fecha_lunes()} a las 08:00._
_Para desactivar este resumen o cambiar la cadencia: [Configuración del pipeline]_
"""


def _formatear_seccion_bandeja(
    pendientes: list[dict],
    leidos: list[dict]
) -> str:
    if not pendientes and not leidos:
        return "## Bandeja de entrada\n\n✅ Sin eventos pendientes de atención."

    md = "## Bandeja de entrada\n\n"

    if pendientes:
        md += f"**{len(pendientes)} evento(s) sin leer:**\n\n"
        for item in pendientes[:5]:  # Máximo 5 en el resumen
            md += (
                f"- **{item['asunto']}**  \n"
                f"  {item['accion']}  \n"
                f"  [Ver →]({item['url_accion']})\n\n"
            ) if item.get("url_accion") else (
                f"- **{item['asunto']}**  \n"
                f"  {item['accion']}\n\n"
            )
        if len(pendientes) > 5:
            md += f"_... y {len(pendientes) - 5} más en la bandeja_\n\n"

    if leidos:
        md += f"**{len(leidos)} evento(s) leído(s) pendientes de resolver:**\n\n"
        for item in leidos[:3]:
            md += f"- {item['asunto']}\n"
        md += "\n"

    return md


def _generar_recomendacion_principal(
    pendientes: list[dict],
    stats_repo: dict,
    cobertura: dict
) -> str:
    """
    Genera una sola recomendación concreta para la semana.
    La lógica de prioridad: impacto de cambio > gaps de cobertura > mantenimiento.
    """

    # Si hay un impacto de cambio sin atender, eso es lo más urgente
    impactos = [p for p in pendientes if p["tipo_evento"] == "impacto_cambio"]
    if impactos:
        req_id = impactos[0].get("requisito_id", "")
        return (
            f"Hay {len(impactos)} cambio(s) de requisito con impacto no atendido. "
            f"Empieza por **{req_id}** antes del refinamiento de esta semana."
        )

    # Si hay requisitos sin cobertura de test cases
    historias_sin_tc = cobertura.get("historias_sin_test_cases", [])
    if historias_sin_tc:
        return (
            f"**{len(historias_sin_tc)} historia(s)** no tienen test cases asociados. "
            f"Si alguna está comprometida en el sprint actual, ejecuta el pipeline "
            f"de test cases antes de que empiece el desarrollo."
        )

    # Si el score medio del repositorio ha bajado
    score = stats_repo.get("score_medio", 100)
    if score < 70:
        return (
            f"El score medio del repositorio ha bajado a **{score}/100**. "
            f"Dedica 30 minutos esta semana a revisar los requisitos con score < 60 "
            f"y corregir los campos más frecuentemente problemáticos."
        )

    # Si todo va bien, una nota de mantenimiento preventivo
    return (
        "El pipeline está en buen estado esta semana. "
        "Buen momento para revisar si el glosario recoge los términos nuevos "
        "que han aparecido en las últimas conversaciones con negocio."
    )
```

---

## Control de ruido: las cuatro reglas de supresión

El mayor riesgo de un sistema de notificaciones es el ruido que hace que el analista lo ignore. Estas cuatro reglas de supresión garantizan que cada notificación enviada tiene sentido:

**Regla 1 — Cooldown por evento repetido.** Si el mismo tipo de evento sobre el mismo requisito ya ha sido notificado en las últimas 24 horas, no se vuelve a notificar. La segunda ocurrencia se registra en el log pero no genera un nuevo mensaje.

**Regla 2 — Agrupación en ventana de tiempo.** Si en menos de cinco minutos llegan tres o más eventos de Tier 2 del mismo requisito (por ejemplo, porque el analista modificó varios campos a la vez), se agrupan en una sola notificación de bandeja con el resumen de todos ellos.

**Regla 3 — Supresión por contexto de trabajo.** Si el analista está en el proceso activo de aprobar artefactos de un requisito (tiene la interfaz de aprobación abierta), los eventos de Tier 2 de ese mismo requisito se suprimen durante esa sesión. Ya tiene el contexto delante.

**Regla 4 — Silencio programable.** El analista puede marcar períodos de silencio (reuniones, vacaciones, foco en otra épica) durante los cuales solo llegan los eventos de Tier 1 de requisitos de su proyecto activo. Los Tier 2 se acumulan en la bandeja para cuando vuelva.

```python
# notificador/supresion.py

from datetime import datetime, timedelta
import json


class ControlSupresion:
    """
    Decide si un evento debe suprimirse antes de enviarlo.
    Consulta el historial reciente de notificaciones para evitar ruido.
    """

    COOLDOWN_TIER_1_HORAS = 4     # Un evento crítico puede repetirse cada 4h como máximo
    COOLDOWN_TIER_2_HORAS = 24    # Los eventos de revisión, una vez al día por tipo
    VENTANA_AGRUPACION_MINUTOS = 5

    def __init__(self, db):
        self.db = db

    def debe_suprimir(
        self,
        tipo_evento: str,
        requisito_id: str,
        analista_id: str,
        tier: str
    ) -> tuple[bool, str]:
        """
        Retorna (suprimir: bool, motivo: str).
        Si suprimir=True, el evento no se envía (pero sí se registra en el log).
        """

        # Verificar cooldown
        cooldown_horas = (
            self.COOLDOWN_TIER_1_HORAS if tier == "1"
            else self.COOLDOWN_TIER_2_HORAS
        )
        ultimo_envio = self._ultimo_envio(tipo_evento, requisito_id, analista_id)
        if ultimo_envio:
            tiempo_desde = datetime.now() - ultimo_envio
            if tiempo_desde < timedelta(hours=cooldown_horas):
                return True, f"Cooldown activo: {int(tiempo_desde.total_seconds() / 60)} min desde el último envío"

        # Verificar si el analista está en silencio programado
        if self._analista_en_silencio(analista_id) and tier != "1":
            return True, "Analista en período de silencio programado"

        return False, ""

    def _ultimo_envio(
        self,
        tipo_evento: str,
        requisito_id: str,
        analista_id: str
    ) -> datetime | None:
        """Retorna la fecha del último envío de este tipo de evento para este requisito."""
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT MAX(fecha_envio)
                FROM log_notificaciones
                WHERE tipo_evento  = %s
                  AND requisito_id = %s
                  AND analista_id  = %s
                  AND suprimido    = FALSE
            """, (tipo_evento, requisito_id, analista_id))
            resultado = cur.fetchone()
            return resultado[0] if resultado and resultado[0] else None

    def _analista_en_silencio(self, analista_id: str) -> bool:
        """Verifica si el analista ha programado un período de silencio activo ahora."""
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*)
                FROM silencio_programado
                WHERE analista_id = %s
                  AND inicio <= NOW()
                  AND fin    >= NOW()
            """, (analista_id,))
            return cur.fetchone()[0] > 0


class AgrupadorEventos:
    """
    Agrupa eventos de Tier 2 del mismo requisito que llegan en ventana corta
    para evitar que una cascada de cambios genere múltiples notificaciones.
    """

    def __init__(self, db):
        self.db = db

    def registrar_y_agrupar(
        self,
        tipo_evento: str,
        requisito_id: str,
        analista_id: str,
        datos: dict
    ) -> bool:
        """
        Registra el evento en el buffer de agrupación.
        Retorna True si debe enviarse ahora (primer evento de la ventana).
        Retorna False si debe suprimirse (ya hay eventos en la ventana activa).
        """
        ventana_inicio = datetime.now() - timedelta(
            minutes=ControlSupresion.VENTANA_AGRUPACION_MINUTOS
        )

        with self.db.cursor() as cur:
            # Contar eventos del mismo requisito en la ventana
            cur.execute("""
                SELECT COUNT(*)
                FROM buffer_agrupacion
                WHERE requisito_id = %s
                  AND analista_id  = %s
                  AND timestamp    >= %s
            """, (requisito_id, analista_id, ventana_inicio))

            n_en_ventana = cur.fetchone()[0]

            # Registrar este evento en el buffer
            cur.execute("""
                INSERT INTO buffer_agrupacion
                    (tipo_evento, requisito_id, analista_id, datos, timestamp)
                VALUES (%s, %s, %s, %s, NOW())
            """, (tipo_evento, requisito_id, analista_id, json.dumps(datos)))
            self.db.commit()

        # Primer evento de la ventana: enviar
        if n_en_ventana == 0:
            return True

        # Hay más eventos en la ventana: no enviar (el primero ya fue enviado)
        return False
```

---

## Configuración por analista

Cada analista puede ajustar su configuración de notificaciones sin tocar código. La configuración se almacena en la base de datos y el clasificador la consulta antes de tomar decisiones.

```yaml
# Perfil de notificaciones de un analista (guardado en tabla configuracion_analista)
# El analista edita esto desde la interfaz web del pipeline o desde Confluence

analista_id: carlos.ruiz@meridian.com

# Canales habilitados para eventos inmediatos (Tier 1)
canales_tier1:
  slack: true
  email: false       # Solo Slack para eventos críticos; el email es demasiado lento
  bandeja: true      # Los Tier 1 también van a la bandeja como registro

# Canales para eventos de revisión (Tier 2)
canales_tier2:
  slack: false       # No interrumpir por Tier 2
  email: false
  bandeja: true      # Solo bandeja de entrada

# Resumen semanal
resumen_semanal:
  activo: true
  dia: lunes
  hora: "08:00"
  canal: confluence  # confluence | email
  url_pagina_confluence: "https://meridian.atlassian.net/wiki/..."

# Épicas activas (solo notificar de estas épicas en modo silencio)
epicas_activas:
  - EP-04
  - EP-05

# Tipos de evento que quiero suprimir completamente
# (el analista tiene la autoridad de desactivar tipos que no le aportan valor)
tipos_suprimidos:
  - requisito_inactivo    # Carlos prefiere no recibir recordatorios de borradores

# Períodos de silencio recurrentes
silencio_recurrente:
  - tipo: diario
    inicio: "09:00"
    fin: "10:00"
    descripcion: "Daily standup y revisión de correo"
    # Durante este período, solo pasan eventos Tier 1 de sprint activo
```

---

## Métricas de salud del sistema de notificaciones

El sistema de notificaciones necesita sus propias métricas para detectar si está funcionando bien o si ha derivado hacia el ruido. Estas métricas se incluyen en el resumen semanal del champion, no del analista.

```
MÉTRICAS DE SALUD (revisión mensual del comité de gobierno)

Tasa de supresión:
  Porcentaje de eventos generados que se suprimen por cooldown.
  Si supera el 40%: el pipeline genera demasiados eventos del mismo tipo,
  probablemente porque algo en el proceso crea cascadas de cambios evitables.
  Si está por debajo del 5%: el cooldown puede ser demasiado largo.
  Objetivo: entre 10% y 30%.

Tasa de acción sobre Tier 1:
  Porcentaje de eventos de Tier 1 que resultan en una acción del analista
  (aprobar, rechazar, corregir) en menos de 4 horas hábiles.
  Si está por debajo del 80%: los analistas están ignorando las notificaciones críticas.
  Objetivo: >85%.

Tiempo de resolución de bandeja:
  Tiempo medio entre que un evento de Tier 2 llega a la bandeja y se marca como resuelto.
  Objetivo: <3 días laborables.
  Señal de alarma: >7 días (los analistas no revisan la bandeja regularmente).

Volumen diario de notificaciones por analista:
  Número de mensajes de canal inmediato que recibe un analista al día.
  Si supera 5: el sistema está generando demasiado ruido y el analista lo ignorará.
  Objetivo: 0-2 mensajes de Tier 1 al día en un proyecto maduro.

Tasa de silencio programado activo:
  Porcentaje del tiempo de trabajo en que un analista tiene silencio programado.
  Si supera el 50%: el analista está usando el silencio para evadir el sistema,
  no para proteger su foco. Señal de que el volumen de Tier 2 es excesivo.
  Objetivo: <30%.
```

---

## Integración con el orquestador

El sistema de notificaciones se engancha al orquestador como un middleware que se ejecuta al finalizar cada paso del pipeline. No es un sistema separado que monitoriza desde fuera: es parte del flujo de ejecución.

```python
# orchestrator.py — fragmento de integración
# (añadir en cada paso relevante del pipeline existente)

from notificador.clasificador import clasificar_evento
from notificador.supresion import ControlSupresion, AgrupadorEventos
from notificador.despachador import Despachador

class OrquestadorConNotificaciones:
    """
    Extiende el orquestador del Cap. 12 con el sistema de notificaciones.
    Solo se añaden las llamadas al notificador en los puntos de decisión;
    el flujo principal del pipeline no cambia.
    """

    def __init__(self, config, db):
        self.supresion  = ControlSupresion(db)
        self.agrupador  = AgrupadorEventos(db)
        self.despachador = Despachador(config, db)

    def notificar_si_procede(
        self,
        tipo_evento: str,
        datos_evento: dict,
        analista_id: str
    ):
        """
        Punto de entrada único para notificaciones desde el orquestador.
        El orquestador llama a este método; el resto lo gestiona el notificador.
        """

        # Paso 1: Clasificar el evento
        decision = clasificar_evento(tipo_evento, datos_evento)

        # Si no hay que notificar, solo registrar en el log y salir
        if decision.tier == "0":
            self._registrar_log(tipo_evento, datos_evento, "no_notificar", "")
            return

        # Paso 2: Verificar supresión
        suprimir, motivo = self.supresion.debe_suprimir(
            tipo_evento=tipo_evento,
            requisito_id=datos_evento.get("requisito_id", ""),
            analista_id=analista_id,
            tier=decision.tier.value
        )
        if suprimir:
            self._registrar_log(tipo_evento, datos_evento, "suprimido", motivo)
            return

        # Paso 3: Verificar agrupación (solo para Tier 2)
        if decision.tier == "2":
            debe_enviar = self.agrupador.registrar_y_agrupar(
                tipo_evento=tipo_evento,
                requisito_id=datos_evento.get("requisito_id", ""),
                analista_id=analista_id,
                datos=datos_evento
            )
            if not debe_enviar:
                self._registrar_log(tipo_evento, datos_evento, "agrupado", "")
                return

        # Paso 4: Resolver URL de acción directa
        decision.url_accion = self._resolver_url_accion(tipo_evento, datos_evento)

        # Paso 5: Despachar por el canal correspondiente
        self.despachador.enviar(decision, datos_evento, analista_id)
        self._registrar_log(tipo_evento, datos_evento, "enviado", decision.canal.value)

    def _resolver_url_accion(self, tipo_evento: str, datos: dict) -> str | None:
        """Construye la URL directa donde el analista debe actuar."""
        base = datos.get("pipeline_base_url", "http://pipeline-ai.interno")
        req_id = datos.get("requisito_id", "")

        urls = {
            "aprobacion_pendiente":     f"{base}/aprobacion/{datos.get('aprobacion_id', '')}",
            "validacion_bloqueada":     f"{base}/requisitos/{req_id}/validacion",
            "impacto_cambio":           f"{base}/requisitos/{req_id}/impacto",
            "pipeline_fallo_bloqueante":f"{base}/runs/{datos.get('run_id', '')}",
            "duplicado_probable":       f"{base}/requisitos/{req_id}/similares",
            "validacion_aprobada_con_advertencias": f"{base}/requisitos/{req_id}/advertencias",
        }
        return urls.get(tipo_evento)

    def _registrar_log(
        self,
        tipo_evento: str,
        datos: dict,
        accion: str,
        detalle: str
    ):
        """Registra en el log interno todas las decisiones del notificador."""
        pass  # Implementación en el gestor de logs del orquestador
```

---

## Errores habituales al diseñar el sistema de notificaciones

**Notificar confirmaciones de acciones que el analista ya tomó.** El error más frecuente: cuando el analista aprueba los artefactos y el sistema le notifica que el push a Jira fue exitoso. El analista ya sabe que aprobó. Si el push falla, sí debe notificarse. Si tiene éxito, no.

**Notificar por canal inmediato eventos que no requieren respuesta inmediata.** Un duplicado probable no es urgente. Un requisito en borrador inactivo tampoco. Llegar al Slack del analista con esos eventos destruye la credibilidad del canal para cuando llegue un evento realmente crítico.

**No resolver la URL de acción directa.** Un mensaje que dice "hay un problema en REQ-023, revísalo" sin un enlace directo obliga al analista a abrir el pipeline, buscar el requisito y navegar hasta el informe. Ese fricción de diez segundos es suficiente para que el analista diga "lo veo luego" y lo olvide.

**Configuración uniforme para todos.** Un analista que gestiona tres épicas en paralelo necesita una configuración de notificaciones distinta al que gestiona una. No forzar la misma configuración por defecto para todos desde el día uno.

**Olvidar el canal de silencio.** Sin un mecanismo de silencio programable, el analista que tiene una semana de reuniones intensas recibe notificaciones que no puede atender, se estresa y empieza a desactivar el sistema completo en lugar de desactivar un período.

**No medir el ruido.** Sin las métricas de salud del sistema de notificaciones, no hay forma de saber si el analista está ignorando el canal hasta que alguien lo menciona en la retrospectiva. Medir el tiempo de respuesta a eventos de Tier 1 desde el primer mes.
