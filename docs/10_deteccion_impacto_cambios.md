# Punto 8 — Detección de impacto de cambios

La detección de impacto de cambios es donde el sistema deja de ser reactivo y se vuelve proactivo. Sin ella, un cambio en un requisito validado se propaga silenciosamente a artefactos ya generados que nadie actualiza. Con ella, el sistema alerta exactamente de qué está roto y qué hay que regenerar antes de que llegue al sprint.

---

## El problema que resuelve

En el flujo tradicional, cuando el negocio cambia un requisito ya validado ocurren tres cosas malas en paralelo:

- Las historias Jira generadas desde ese requisito quedan desactualizadas sin que nadie lo sepa.
- Los test cases siguen verificando el comportamiento anterior.
- Los desarrolladores que ya leyeron la historia trabajan sobre una versión que ya no es la correcta.

El coste de un cambio no detectado crece exponencialmente con el tiempo:

| Momento de detección | Coste relativo |
|---|---|
| En el momento del cambio | 1 |
| En el refinamiento del sprint | 5 |
| En QA | 20 |
| En producción | 100 |

El sistema de detección de impacto actúa en el momento del cambio, cuando el coste es mínimo.

---

## Taxonomía de cambios y su impacto

No todos los cambios tienen el mismo alcance. El sistema necesita clasificarlos para determinar qué regenerar y con qué urgencia.

```
CAMBIOS EN UN REQUISITO
│
├── TIPO A: Cambios de comportamiento (impacto alto)
│   ├── Modificación de un criterio de aceptación
│   ├── Adición o eliminación de un flujo de excepción
│   ├── Cambio en una regla de negocio
│   └── Cambio en datos de entrada/salida (tipo, formato, rango)
│
├── TIPO B: Cambios de alcance (impacto medio)
│   ├── Cambio de épica (el requisito se mueve de módulo)
│   ├── Cambio de actor principal
│   ├── Cambio de prioridad (puede afectar al sprint)
│   └── División de un requisito en dos (split)
│
├── TIPO C: Cambios administrativos (impacto bajo)
│   ├── Cambio de estado (borrador → en-revision)
│   ├── Cambio de analista responsable
│   ├── Corrección ortográfica en descripción
│   └── Actualización de metadatos de origen
│
└── TIPO D: Cambios de deprecación (impacto estructural)
    ├── Requisito reemplazado por otro
    ├── Requisito eliminado del alcance
    └── Fusión de dos requisitos en uno
```

Esta taxonomía determina el árbol de decisión del sistema: qué analizar, qué alertar y qué regenerar automáticamente versus qué requiere decisión humana.

---

## Arquitectura del pipeline de detección de impacto

### Fase 1 — Motor de diff semántico

El primer paso es comparar la versión anterior y la nueva del requisito campo a campo. No es un diff de texto plano: necesita entender si un cambio es semánticamente significativo, no solo sintácticamente diferente.

```python
from dataclasses import dataclass, field
from typing import Any
import yaml
from openai import OpenAI

@dataclass
class CambioDetectado:
    campo: str
    valor_anterior: Any
    valor_nuevo: Any
    tipo_cambio: str          # A, B, C, D
    severidad: str            # bloqueante | advertencia | informativo
    descripcion: str          # Qué cambió en lenguaje natural
    impacto_estimado: str     # Qué artefactos pueden verse afectados


class MotorDiffSemantico:
    """
    Compara dos versiones de un requisito e identifica
    todos los cambios con su clasificación de impacto.
    """

    # Mapa de campos a tipo de cambio y severidad
    CLASIFICACION_CAMPOS = {
        # Tipo A — comportamiento (alto impacto)
        "criterios_aceptacion":     ("A", "bloqueante"),
        "reglas_negocio":           ("A", "bloqueante"),
        "excepciones":              ("A", "bloqueante"),
        "flujo_principal":          ("A", "bloqueante"),
        "flujos_alternativos":      ("A", "bloqueante"),
        "datos_entrada":            ("A", "bloqueante"),
        "datos_salida":             ("A", "bloqueante"),
        "definition_of_done":       ("A", "advertencia"),

        # Tipo B — alcance (impacto medio)
        "epica":                    ("B", "bloqueante"),
        "actor":                    ("B", "advertencia"),
        "actores_secundarios":      ("B", "advertencia"),
        "prioridad":                ("B", "advertencia"),
        "titulo":                   ("B", "advertencia"),
        "descripcion":              ("B", "informativo"),
        "evento_disparador":        ("B", "advertencia"),
        "objetivo_negocio":         ("B", "informativo"),
        "dependencias":             ("B", "advertencia"),

        # Tipo C — administrativo (sin impacto en artefactos)
        "estado":                   ("C", "informativo"),
        "version":                  ("C", "informativo"),
        "origen":                   ("C", "informativo"),
        "analista":                 ("C", "informativo"),
        "fecha_validacion":         ("C", "informativo"),
        "notas_implementacion":     ("C", "informativo"),

        # Tipo D — deprecación (impacto estructural)
        "sucesor":                  ("D", "bloqueante"),
    }

    def __init__(self, openai_client: OpenAI):
        self.openai = openai_client

    def calcular_diff(
        self,
        yaml_anterior: str,
        yaml_nuevo: str
    ) -> list[CambioDetectado]:
        """
        Compara dos versiones YAML de un requisito y retorna
        la lista de cambios detectados con su clasificación.
        """
        req_anterior = yaml.safe_load(yaml_anterior)
        req_nuevo = yaml.safe_load(yaml_nuevo)
        cambios = []

        # Detectar estado de deprecación antes de cualquier otra cosa
        if req_nuevo.get("estado") == "deprecado" and \
           req_anterior.get("estado") != "deprecado":
            cambios.append(CambioDetectado(
                campo="estado",
                valor_anterior=req_anterior.get("estado"),
                valor_nuevo="deprecado",
                tipo_cambio="D",
                severidad="bloqueante",
                descripcion=(
                    f"El requisito {req_nuevo['id']} ha sido deprecado. "
                    f"Sucesor: {req_nuevo.get('sucesor', 'no especificado')}"
                ),
                impacto_estimado=(
                    "Todos los artefactos generados desde este requisito "
                    "deben revisarse. Las historias Jira deben marcarse como "
                    "dependientes de la resolución del sucesor."
                )
            ))
            return cambios  # No analizar más si está deprecado

        # Analizar cada campo conocido
        todos_los_campos = set(
            list(req_anterior.keys()) + list(req_nuevo.keys())
        )

        for campo in todos_los_campos:
            val_anterior = req_anterior.get(campo)
            val_nuevo = req_nuevo.get(campo)

            if val_anterior == val_nuevo:
                continue

            tipo, severidad = self.CLASIFICACION_CAMPOS.get(
                campo, ("C", "informativo")
            )

            descripcion = self._describir_cambio(campo, val_anterior, val_nuevo)
            impacto = self._estimar_impacto(campo, val_anterior, val_nuevo, tipo)

            cambios.append(CambioDetectado(
                campo=campo,
                valor_anterior=val_anterior,
                valor_nuevo=val_nuevo,
                tipo_cambio=tipo,
                severidad=severidad,
                descripcion=descripcion,
                impacto_estimado=impacto
            ))

        # Ordenar por severidad: bloqueante primero
        orden_severidad = {"bloqueante": 0, "advertencia": 1, "informativo": 2}
        cambios.sort(key=lambda c: orden_severidad[c.severidad])

        return cambios
```

### Fase 2 — Analizador de impacto RAG

Con los cambios clasificados, el analizador consulta el vector store para identificar qué artefactos concretos del repositorio están afectados.

```python
@dataclass
class ArtefactoAfectado:
    tipo: str            # historia | test_case | requisito | jira_issue
    id: str
    titulo: str
    razon_impacto: str   # Por qué está afectado
    accion_recomendada: str
    urgencia: str        # inmediata | proxima_iteracion | monitorizar
    similitud: float     # Score de similitud con el cambio


class AnalizadorImpactoRAG:
    """
    Usa el vector store para identificar todos los artefactos
    afectados por un conjunto de cambios.
    """

    def __init__(self, motor_rag, db_jira_config: dict):
        self.rag = motor_rag
        self.jira_config = db_jira_config

    async def analizar(
        self,
        requisito_id: str,
        cambios: list[CambioDetectado],
        yaml_nuevo: dict
    ) -> dict:
        """
        Punto de entrada principal del análisis de impacto.
        Orquesta todos los sub-análisis y produce el informe consolidado.
        """
        cambios_tipo_a = [c for c in cambios if c.tipo_cambio == "A"]
        cambios_tipo_b = [c for c in cambios if c.tipo_cambio == "B"]
        cambios_tipo_d = [c for c in cambios if c.tipo_cambio == "D"]

        if not (cambios_tipo_a or cambios_tipo_b or cambios_tipo_d):
            return self._informe_sin_impacto(requisito_id, cambios)

        resultados = await asyncio.gather(
            self._analizar_historias_afectadas(requisito_id, cambios_tipo_a + cambios_tipo_b),
            self._analizar_test_cases_afectados(requisito_id, cambios_tipo_a),
            self._analizar_requisitos_dependientes(requisito_id, cambios_tipo_a + cambios_tipo_b),
            self._analizar_issues_jira(requisito_id),
            self._analizar_sprint_impacto(requisito_id)
        )

        (
            historias_afectadas,
            test_cases_afectados,
            requisitos_dependientes,
            issues_jira,
            impacto_sprint
        ) = resultados

        plan_accion = await self._generar_plan_accion(
            requisito_id, cambios, historias_afectadas,
            test_cases_afectados, requisitos_dependientes, yaml_nuevo
        )

        return self._ensamblar_informe(
            requisito_id=requisito_id,
            cambios=cambios,
            historias_afectadas=historias_afectadas,
            test_cases_afectados=test_cases_afectados,
            requisitos_dependientes=requisitos_dependientes,
            issues_jira=issues_jira,
            impacto_sprint=impacto_sprint,
            plan_accion=plan_accion
        )
```

### Fase 3 — Generación del plan de acción con LLM

Con todos los artefactos afectados identificados, el LLM genera un plan de acción específico y ordenado:

```python
async def _generar_plan_accion(
    self,
    requisito_id: str,
    cambios: list[CambioDetectado],
    historias_afectadas: list[ArtefactoAfectado],
    test_cases_afectados: list[ArtefactoAfectado],
    requisitos_dependientes: list[ArtefactoAfectado],
    yaml_nuevo: dict
) -> dict:

    prompt = f"""
    Eres un gestor de proyectos Agile senior. Se ha detectado un cambio en el
    requisito {requisito_id} ({yaml_nuevo.get('titulo', '')}).

    Genera un plan de acción concreto y ordenado en JSON:
    {{
      "resumen_ejecutivo": "...",
      "nivel_riesgo_global": "critico | alto | medio | bajo",
      "justificacion_riesgo": "...",
      "acciones": [
        {{
          "orden": 1,
          "tipo": "notificar | regenerar | revisar | decidir | monitorizar",
          "descripcion": "...",
          "responsable": "analista | product_owner | tech_lead | qa_lead | equipo",
          "plazo": "inmediato | antes_del_siguiente_sprint | proxima_iteracion",
          "artefactos_involucrados": ["..."],
          "como_hacerlo": "..."
        }}
      ],
      "decision_requerida": {{
        "necesaria": true | false,
        "pregunta": "...",
        "opciones": ["Opción A", "Opción B"],
        "impacto_de_no_decidir": "..."
      }},
      "comunicacion_recomendada": {{
        "notificar_a": ["product_owner", "tech_lead", "qa_lead"],
        "mensaje_resumen": "..."
      }}
    }}
    """

    response = self.rag.repo.openai.chat.completions.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)
```

### Fase 4 — Informe consolidado de impacto

El informe final es el documento que recibe el analista. Debe ser accionable en menos de 5 minutos de lectura.

```python
def _ensamblar_informe(self, **kwargs) -> dict:
    cambios = kwargs["cambios"]
    impacto_sprint = kwargs["impacto_sprint"]
    plan_accion = kwargs["plan_accion"]

    tiene_bloqueantes = any(c.severidad == "bloqueante" for c in cambios)
    en_sprint_activo = impacto_sprint.get("tiene_issues_en_sprint_activo", False)

    return {
        "informe_impacto": {
            "requisito_id": kwargs["requisito_id"],
            "timestamp": datetime.now().isoformat(),
            "nivel_urgencia": (
                "CRITICO" if en_sprint_activo and tiene_bloqueantes else
                "ALTO"    if tiene_bloqueantes else
                "MEDIO"   if any(c.tipo_cambio == "B" for c in cambios) else
                "BAJO"
            ),
            "alerta_sprint": impacto_sprint.get("alerta"),
            "issues_en_sprint_activo": impacto_sprint.get("issues_en_sprint", []),
            "cambios_detectados": [...],
            "artefactos_afectados": {
                "historias": [...],
                "test_cases": [...],
                "requisitos_dependientes": [...],
                "issues_jira": kwargs["issues_jira"]
            },
            "plan_accion": plan_accion,
            "estadisticas": {
                "total_cambios": len(cambios),
                "cambios_bloqueantes": sum(1 for c in cambios if c.severidad == "bloqueante"),
                "total_artefactos_afectados": (
                    len(kwargs["historias_afectadas"]) +
                    len(kwargs["test_cases_afectados"]) +
                    len(kwargs["requisitos_dependientes"])
                ),
                "requiere_decision_po": plan_accion.get(
                    "decision_requerida", {}
                ).get("necesaria", False)
            }
        }
    }
```

---

## Ejemplo de informe real generado

Este es el aspecto del informe cuando un analista modifica el criterio `AC-023-01` de `REQ-023`:

```json
{
  "informe_impacto": {
    "requisito_id": "REQ-023",
    "timestamp": "2025-05-06T11:32:00Z",
    "nivel_urgencia": "CRITICO",

    "alerta_sprint": "⚠ HAY ISSUES EN EL SPRINT ACTIVO. El equipo puede estar trabajando sobre una versión desactualizada.",
    "issues_en_sprint_activo": [
      {
        "key": "FACT-47",
        "summary": "Como gestor de facturación, quiero filtrar facturas por rango de fechas",
        "status": "En progreso",
        "asignado_a": "María García"
      }
    ],

    "cambios_detectados": [
      {
        "campo": "criterios_aceptacion",
        "tipo": "A",
        "severidad": "bloqueante",
        "descripcion": "Criterios modificados: AC-023-01. El tiempo de respuesta máximo cambia de 2 segundos a 500ms.",
        "impacto_estimado": "Las historias de usuario y todos los test cases derivados de AC-023-01 quedan desactualizados."
      }
    ],

    "artefactos_afectados": {
      "historias": [
        {
          "id": "US-047",
          "razon": "Historia generada directamente desde REQ-023. Cambio en: criterios_aceptacion",
          "accion": "Regenerar historia automáticamente",
          "urgencia": "inmediata"
        }
      ],
      "test_cases": [
        {
          "id": "TC-023-01",
          "razon": "Test case generado desde AC-023-01 que ha sido modificado",
          "accion": "Regenerar test case desde el criterio actualizado",
          "urgencia": "inmediata"
        },
        {
          "id": "TC-023-06",
          "razon": "Test case de contorno relacionado con el rendimiento",
          "accion": "Revisar manualmente en Xray",
          "urgencia": "proxima_iteracion"
        }
      ],
      "requisitos_dependientes": [
        {
          "id": "REQ-024",
          "razon": "Declara dependencia explícita con REQ-023",
          "accion": "Verificar que sus criterios de aceptación siguen siendo coherentes"
        }
      ]
    },

    "plan_accion": {
      "resumen_ejecutivo": "El cambio en el tiempo de respuesta máximo de AC-023-01 (2s → 500ms) es bloqueante. Hay una historia en desarrollo activo que trabaja con el criterio anterior. Requiere decisión inmediata del Product Owner.",
      "nivel_riesgo_global": "critico",
      "acciones": [
        {
          "orden": 1,
          "tipo": "notificar",
          "descripcion": "Informar a María García y al Tech Lead del cambio antes de que continúe el desarrollo",
          "responsable": "analista",
          "plazo": "inmediato",
          "artefactos_involucrados": ["FACT-47"],
          "como_hacerlo": "Añadir comentario en FACT-47 referenciando este informe de impacto."
        },
        {
          "orden": 2,
          "tipo": "decidir",
          "descripcion": "El Product Owner debe confirmar si el nuevo umbral de 500ms aplica al sprint actual o al siguiente",
          "responsable": "product_owner",
          "plazo": "inmediato"
        },
        {
          "orden": 3,
          "tipo": "regenerar",
          "descripcion": "Regenerar la historia US-047 y el test case TC-023-01 con el nuevo criterio de 500ms",
          "responsable": "analista",
          "plazo": "antes_del_siguiente_sprint",
          "artefactos_involucrados": ["US-047", "TC-023-01"]
        }
      ],
      "decision_requerida": {
        "necesaria": true,
        "pregunta": "¿El nuevo umbral de 500ms aplica al sprint actual o al siguiente sprint?",
        "opciones": [
          "Sprint actual: pausar FACT-47 hasta redefinir la solución técnica",
          "Siguiente sprint: María García continúa con 2s, el cambio entra en el siguiente sprint"
        ],
        "impacto_de_no_decidir": "María García puede entregar una implementación de 2s que será rechazada en QA."
      },
      "comunicacion_recomendada": {
        "notificar_a": ["product_owner", "tech_lead", "qa_lead"],
        "mensaje_resumen": "⚠ Cambio bloqueante en REQ-023: el tiempo de respuesta máximo pasa de 2s a 500ms. Hay una historia en desarrollo activo (FACT-47). Necesitamos decisión del PO antes de EOD."
      }
    },

    "estadisticas": {
      "total_cambios": 1,
      "cambios_bloqueantes": 1,
      "total_artefactos_afectados": 4,
      "requiere_decision_po": true
    }
  }
}
```

---

## Integración con el workflow del equipo

El informe no vive solo en un JSON. Se integra en los canales donde el equipo ya trabaja:

```python
class NotificadorImpacto:
    """
    Distribuye el informe de impacto por los canales configurados.
    """

    async def notificar(self, informe: dict, config: dict):
        nivel = informe["informe_impacto"]["nivel_urgencia"]

        # Siempre: comentario en Confluence sobre el requisito
        await self._comentar_en_confluence(informe, config)

        # Si hay issues en sprint: comentario en cada issue Jira
        if informe["informe_impacto"].get("issues_en_sprint_activo"):
            await self._comentar_en_issues_jira(informe, config)

        # Si es CRITICO o ALTO: mensaje en Slack/Teams
        if nivel in ("CRITICO", "ALTO"):
            await self._notificar_slack(informe, config)

        # Si requiere decisión del PO: crear issue de tipo Decision en Jira
        decision = informe["informe_impacto"]["plan_accion"].get("decision_requerida", {})
        if decision.get("necesaria"):
            await self._crear_issue_decision(informe, config)
```

---

## Casos de uso que el sistema resuelve automáticamente

**Cambio de regla de negocio global.** Si cambia una regla que aplica a 15 requisitos del mismo módulo, el sistema identifica los 15, genera un informe de impacto consolidado y los ordena por urgencia según si tienen issues en sprint activo. El analista ve exactamente qué tiene que revisar y en qué orden.

**División de un requisito en dos.** Cuando un requisito se parte en `REQ-023a` y `REQ-023b`, el sistema detecta que `REQ-023` pasa a estado deprecado con sucesor, desactiva sus chunks del vector store, re-indexa los dos nuevos y genera un informe que lista todos los artefactos que referenciaban al original para actualizar su trazabilidad.

**Cambio de actor.** Si el actor principal de un requisito cambia de "Gestor de facturación" a "Responsable financiero", el sistema identifica todas las historias que implementan permisos para el primer actor y alerta al Tech Lead para que revise la implementación de autorización.

**Cambio silencioso en datos de entrada.** Si alguien cambia el tipo de un campo de `string` a `integer` sin documentar el impacto, el sistema detecta el cambio de datos de entrada (Tipo A), identifica los test cases con datos de prueba de tipo string y los marca como potencialmente obsoletos.
