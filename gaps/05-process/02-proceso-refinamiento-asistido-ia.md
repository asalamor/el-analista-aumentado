# Proceso de refinamiento asistido por IA

> **Contexto del modelo operativo:** Este documento desarrolla uno de los puntos pendientes identificados al cierre del modelo operativo. Se integra con la plantilla de requisito AI-ready (punto 1), el glosario estructurado (punto 2), el pipeline de validación (punto 6) y el grafo de trazabilidad (punto 9). Es el complemento natural a la guía de Event Storming (punto 3): si el Event Storming captura los requisitos desde cero, el refinamiento asistido los depura antes de que entren al sprint.

---

## El problema que resuelve

La ceremonia de refinamiento tiene un problema estructural que ningún proceso Agile resuelve bien: el analista y el equipo técnico dedican entre el 40% y el 60% del tiempo a hacer preguntas que deberían haberse respondido antes, y el 20% restante a descubrir que el requisito tiene dependencias o contradicciones con historias anteriores que nadie recuerda.

El resultado es una ceremonia de refinamiento que se alarga, que no cubre todo el backlog previsto, y donde las historias salen con criterios de aceptación incompletos porque el tiempo se agotó antes de llegar a los flujos de error.

La IA no puede facilitar el refinamiento en lugar del analista. Pero puede hacer tres cosas que transforman la calidad de la ceremonia:

**Preparación estructurada antes de entrar.** Analizar cada historia candidata al refinamiento, detectar sus gaps, y generar la lista de preguntas que el equipo necesita responder, ordenadas por impacto.

**Apoyo en tiempo real durante la sesión.** Responder preguntas sobre requisitos anteriores, detectar contradicciones con el backlog existente y sugerir criterios de aceptación mientras el equipo conversa.

**Cierre asistido al terminar.** Verificar que las historias salientes del refinamiento están completas, actualizar el repositorio y generar los artefactos que falten.

---

## Anatomía de una sesión de refinamiento asistida

La ceremonia tiene tres momentos diferenciados. La IA tiene un rol distinto en cada uno.

```
ANTES (24-48h antes de la sesión)
  │
  ├── Análisis automático de las historias candidatas
  ├── Generación de la agenda priorizada
  ├── Briefing individual para cada participante
  └── Detección de prerequisitos no resueltos
  
DURANTE (la sesión en sí)
  │
  ├── Panel de apoyo en tiempo real (silencioso hasta que se le consulta)
  ├── Sugerencia de preguntas cuando detecta gaps en la conversación
  ├── Consulta al repositorio RAG para contexto histórico
  ├── Generación de criterios de aceptación en directo
  └── Alerta de contradicciones con requisitos existentes
  
DESPUÉS (inmediatamente al terminar)
  │
  ├── Validación automática de las historias refinadas
  ├── Actualización del repositorio de requisitos
  ├── Generación de artefactos faltantes (test cases, tareas)
  └── Actualización del grafo de trazabilidad
```

---

## Fase previa — Preparación automática de la sesión

### Selección y análisis de historias candidatas

El punto de entrada es la consulta al backlog de Jira para recuperar las historias en estado candidato al refinamiento. El sistema las analiza contra el repositorio de requisitos y el vector store del punto 7 para producir un informe de preparación.

```python
# refinement_preparation.py

import asyncio
from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class AnalisisHistoriaRefinamiento:
    historia_key: str
    titulo: str
    requisito_origen: str
    score_completitud: float       # 0-100, calculado por el validador del punto 6
    gaps_detectados: list[dict]    # Problemas que el equipo debe resolver
    preguntas_sugeridas: list[dict]# Preguntas ordenadas por impacto
    contexto_relacionado: list[dict]# Requisitos anteriores relevantes
    contradicciones: list[dict]    # Conflictos con el backlog existente
    dependencias_no_resueltas: list[str]
    complejidad_estimada: str      # simple │ moderada │ compleja │ muy_compleja
    tiempo_refinamiento_min: int   # Estimación de tiempo necesario en la sesión
    lista_para_sprint: bool        # Si puede entrar al sprint sin más trabajo


@dataclass
class AgendaRefinamiento:
    sprint_id: str
    fecha_sesion: str
    duracion_total_min: int
    historias: list[AnalisisHistoriaRefinamiento]
    historias_bloqueadas: list[dict]    # No pueden refinarse por prerequisitos
    historias_listas: list[dict]        # Ya están listas, no necesitan sesión
    tiempo_estimado_total_min: int
    puede_completarse_en_sesion: bool
    orden_recomendado: list[str]        # Keys en orden de prioridad


class PreparadorRefinamiento:
    """
    Analiza las historias candidatas al refinamiento y produce
    la agenda optimizada con el material de preparación para
    cada participante.
    """

    def __init__(
        self,
        cliente_jira,
        validador,          # Del punto 6
        motor_rag,          # Del punto 7
        openai_client,
        config
    ):
        self.jira = cliente_jira
        self.validador = validador
        self.rag = motor_rag
        self.openai = openai_client
        self.config = config

    async def preparar_sesion(
        self,
        sprint_id: str,
        duracion_sesion_min: int = 90
    ) -> AgendaRefinamiento:
        """
        Punto de entrada principal.
        Analiza todas las historias candidatas y produce la agenda.
        """

        # 1. Recuperar historias candidatas de Jira
        candidatas = self._obtener_historias_candidatas(sprint_id)

        if not candidatas:
            return self._agenda_vacia(sprint_id, duracion_sesion_min)

        # 2. Analizar cada historia en paralelo
        analisis = await asyncio.gather(*[
            self._analizar_historia(h) for h in candidatas
        ])

        # 3. Separar historias por estado
        listas = [a for a in analisis if a.lista_para_sprint]
        a_refinar = [a for a in analisis if not a.lista_para_sprint
                     and not a.dependencias_no_resueltas]
        bloqueadas = [a for a in analisis if a.dependencias_no_resueltas]

        # 4. Ordenar las que van a refinamiento por prioridad
        orden = self._ordenar_por_prioridad(a_refinar)

        # 5. Verificar si cabe en el tiempo de sesión
        tiempo_total = sum(a.tiempo_refinamiento_min for a in a_refinar)

        return AgendaRefinamiento(
            sprint_id=sprint_id,
            fecha_sesion="",  # Se rellena al publicar
            duracion_total_min=duracion_sesion_min,
            historias=a_refinar,
            historias_bloqueadas=[
                {
                    "key": a.historia_key,
                    "titulo": a.titulo,
                    "bloqueada_por": a.dependencias_no_resueltas
                }
                for a in bloqueadas
            ],
            historias_listas=[
                {
                    "key": a.historia_key,
                    "titulo": a.titulo,
                    "score": a.score_completitud
                }
                for a in listas
            ],
            tiempo_estimado_total_min=tiempo_total,
            puede_completarse_en_sesion=tiempo_total <= duracion_sesion_min,
            orden_recomendado=orden
        )

    def _obtener_historias_candidatas(self, sprint_id: str) -> list[dict]:
        """Recupera de Jira las historias marcadas para refinamiento."""
        resultado = self.jira.get(
            "search",
            params={
                "jql": (
                    f"project = {self.jira.config.project_key} "
                    f"AND sprint = {sprint_id} "
                    f"AND issuetype = Story "
                    f"AND status = 'Refinement'"
                ),
                "fields": (
                    "summary,description,priority,customfield_10016,"
                    f"{self.jira.config.campo_requisito_origen},"
                    f"{self.jira.config.campo_epic_link}"
                ),
                "maxResults": 20
            }
        )
        return resultado.get("issues", [])

    async def _analizar_historia(self, issue: dict) -> AnalisisHistoriaRefinamiento:
        """
        Análisis completo de una historia candidata.
        Combina validación estructural, búsqueda RAG y razonamiento LLM.
        """
        historia_key = issue["key"]
        titulo = issue["fields"]["summary"]
        req_id = issue["fields"].get(self.jira.config.campo_requisito_origen, "")

        # Cargar el YAML del requisito si existe
        yaml_requisito = self._cargar_yaml_requisito(req_id)

        # Validación de completitud (punto 6)
        if yaml_requisito:
            informe_val = await self.validador.ejecutar_completo(yaml_requisito)
            score = informe_val.get("puntuacion_global", {}).get("valor", 0)
            gaps = self._extraer_gaps_accionables(informe_val)
        else:
            score = 0.0
            gaps = [{"tipo": "sin_requisito", "descripcion":
                     "No se encontró el YAML del requisito origen. "
                     "El refinamiento partirá de la descripción de Jira."}]

        # Contexto relacionado del repositorio RAG (punto 7)
        contexto = await self._recuperar_contexto_rag(
            titulo, yaml_requisito, req_id
        )

        # Detección de contradicciones con el backlog
        contradicciones = await self._detectar_contradicciones(
            yaml_requisito, contexto
        )

        # Dependencias no resueltas
        dependencias_ko = self._verificar_dependencias(yaml_requisito)

        # Generación de preguntas con LLM
        preguntas = await self._generar_preguntas(
            titulo, yaml_requisito, gaps, contexto, contradicciones
        )

        # Estimación de complejidad y tiempo
        complejidad = self._estimar_complejidad(yaml_requisito, gaps, preguntas)
        tiempo_min = self._estimar_tiempo_refinamiento(complejidad, preguntas)

        lista_para_sprint = (
            score >= 80 and
            not gaps and
            not contradicciones and
            not dependencias_ko
        )

        return AnalisisHistoriaRefinamiento(
            historia_key=historia_key,
            titulo=titulo,
            requisito_origen=req_id,
            score_completitud=score,
            gaps_detectados=gaps,
            preguntas_sugeridas=preguntas,
            contexto_relacionado=contexto,
            contradicciones=contradicciones,
            dependencias_no_resueltas=dependencias_ko,
            complejidad_estimada=complejidad,
            tiempo_refinamiento_min=tiempo_min,
            lista_para_sprint=lista_para_sprint
        )

    async def _generar_preguntas(
        self,
        titulo: str,
        yaml_req: Optional[dict],
        gaps: list[dict],
        contexto: list[dict],
        contradicciones: list[dict]
    ) -> list[dict]:
        """
        Genera las preguntas que el equipo debe responder durante
        el refinamiento, ordenadas por impacto en la calidad del output.
        """

        contexto_str = "\n".join([
            f"- {c['requisito_id']}: {c['texto'][:200]}"
            for c in contexto[:5]
        ]) or "Sin requisitos relacionados en el repositorio."

        gaps_str = "\n".join([
            f"- [{g['severidad']}] {g['campo']}: {g['descripcion']}"
            for g in gaps[:8]
        ]) or "Sin gaps detectados."

        contradicciones_str = "\n".join([
            f"- {c['descripcion']}"
            for c in contradicciones[:3]
        ]) or "Sin contradicciones detectadas."

        yaml_str = json.dumps(yaml_req, ensure_ascii=False, indent=2) \
            if yaml_req else "Requisito no disponible en formato estructurado."

        prompt = f"""
Eres un Scrum Master y analista funcional senior preparando una sesión de refinamiento.
Analiza la siguiente historia de usuario y genera las preguntas que el equipo DEBE
responder durante el refinamiento para que la historia pueda entrar al sprint.

HISTORIA: {titulo}

REQUISITO YAML:
{yaml_str[:2000]}

GAPS DETECTADOS POR EL VALIDADOR:
{gaps_str}

CONTEXTO DE REQUISITOS ANTERIORES RELACIONADOS:
{contexto_str}

CONTRADICCIONES CON EL BACKLOG EXISTENTE:
{contradicciones_str}

REGLAS PARA LAS PREGUNTAS:
1. Cada pregunta debe ser accionable: su respuesta debe mejorar directamente
   un campo concreto de la historia (criterio AC, regla de negocio, dato de entrada).
2. Ordénalas por impacto: primero las que bloquean la estimación, luego las que
   afectan a los criterios de aceptación, luego las de detalle.
3. Máximo 8 preguntas. Si hay más gaps, prioriza los más críticos.
4. Las preguntas de contorno son obligatorias si hay campos numéricos o de fecha.
5. Incluye siempre al menos una pregunta sobre flujos de error.
6. Distingue quién debe responder cada pregunta: negocio │ técnico │ ambos.

Responde SOLO con este JSON, sin texto adicional:
{{
  "preguntas": [
    {{
      "orden": 1,
      "categoria": "estimacion │ criterio_ac │ regla_negocio │ dato_entrada │ flujo_error │ contorno │ dependencia",
      "pregunta": "[Pregunta concreta y directa]",
      "campo_que_completa": "[Campo del YAML que esta pregunta ayuda a completar]",
      "dirigida_a": "negocio │ tecnico │ ambos",
      "impacto_si_no_se_responde": "[Qué queda indefinido si nadie la responde]",
      "pista_de_respuesta": "[Contexto del repositorio que puede ayudar a responderla]"
    }}
  ]
}}
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(
                response.choices[0].message.content
            ).get("preguntas", [])
        except Exception:
            return []

    async def _recuperar_contexto_rag(
        self,
        titulo: str,
        yaml_req: Optional[dict],
        req_id: str
    ) -> list[dict]:
        """Recupera requisitos relacionados del vector store."""
        if not yaml_req:
            resultados = self.rag.buscar_por_similitud(
                query_texto=titulo,
                filtros={"estado": "validado"},
                top_k=5
            )
        else:
            resultados = await self.rag.recuperar_contexto_completo(yaml_req)
            resultados = resultados.get("funcionalidad_similar", [])

        return [
            {
                "requisito_id": r.metadatos.get("requisito_id", ""),
                "similitud": round(r.similitud, 2),
                "texto": r.texto[:300]
            }
            for r in resultados
            if r.metadatos.get("requisito_id") != req_id
        ]

    async def _detectar_contradicciones(
        self,
        yaml_req: Optional[dict],
        contexto: list[dict]
    ) -> list[dict]:
        """Detecta posibles contradicciones con requisitos del repositorio."""
        if not yaml_req or not contexto:
            return []

        reglas = yaml_req.get("reglas_negocio", [])
        if not reglas:
            return []

        # Solo buscar contradicciones si hay reglas de negocio definidas
        contradicciones = []
        for item in contexto:
            if item["similitud"] > 0.85:
                # Alta similitud: revisar si hay conflicto de reglas
                contradicciones.append({
                    "requisito_relacionado": item["requisito_id"],
                    "similitud": item["similitud"],
                    "descripcion": (
                        f"Alta similitud ({item['similitud']:.0%}) con "
                        f"{item['requisito_id']}. Verificar que las reglas "
                        f"de negocio no son contradictorias."
                    ),
                    "texto_relacionado": item["texto"][:200]
                })

        return contradicciones

    def _verificar_dependencias(
        self, yaml_req: Optional[dict]
    ) -> list[str]:
        """Verifica si las dependencias declaradas están resueltas."""
        if not yaml_req:
            return []
        deps = yaml_req.get("dependencias", {}).get("requisitos", [])
        ko = []
        for dep_id in deps:
            yaml_dep = self._cargar_yaml_requisito(dep_id)
            if not yaml_dep:
                ko.append(f"{dep_id} (no encontrado en el repositorio)")
            elif yaml_dep.get("estado") not in ("validado",):
                estado = yaml_dep.get("estado", "desconocido")
                ko.append(f"{dep_id} (estado: {estado}, no validado)")
        return ko

    def _extraer_gaps_accionables(self, informe_val: dict) -> list[dict]:
        """Extrae solo los gaps que el equipo puede resolver en la sesión."""
        gaps = []
        for problema in (
            informe_val.get("problemas_por_prioridad", {})
            .get("bloqueantes", []) +
            informe_val.get("problemas_por_prioridad", {})
            .get("advertencias", [])
        ):
            gaps.append({
                "severidad": problema.get("severidad", ""),
                "campo": problema.get("campo", ""),
                "descripcion": problema.get("problema", ""),
                "ejemplo_correcto": problema.get("ejemplo_correcto", "")
            })
        return gaps[:10]  # Máximo 10 para no saturar la sesión

    def _estimar_complejidad(
        self,
        yaml_req: Optional[dict],
        gaps: list[dict],
        preguntas: list[dict]
    ) -> str:
        if not yaml_req:
            return "muy_compleja"
        n_ac = len(yaml_req.get("criterios_aceptacion", []))
        n_reglas = len(yaml_req.get("reglas_negocio", []))
        n_deps = len(yaml_req.get("dependencias", {}).get("requisitos", []))
        n_bloqueantes = sum(1 for g in gaps if g["severidad"] == "BLOQUEANTE")
        score = n_ac + n_reglas * 1.5 + n_deps * 2 + n_bloqueantes * 3
        if score < 5:
            return "simple"
        if score < 10:
            return "moderada"
        if score < 18:
            return "compleja"
        return "muy_compleja"

    def _estimar_tiempo_refinamiento(
        self, complejidad: str, preguntas: list[dict]
    ) -> int:
        """Estimación de minutos necesarios en la sesión."""
        base = {"simple": 10, "moderada": 20, "compleja": 35, "muy_compleja": 50}
        extra_por_pregunta = 3
        return base.get(complejidad, 20) + len(preguntas) * extra_por_pregunta

    def _ordenar_por_prioridad(
        self, analisis: list[AnalisisHistoriaRefinamiento]
    ) -> list[str]:
        """
        Ordena las historias para maximizar el valor del tiempo de sesión.
        Prioridad: dependencias primero, luego complejidad ascendente,
        luego score descendente.
        """
        # Las simples van primero para dar victorias rápidas
        # Las muy complejas van al final o se parten
        orden_complejidad = {
            "simple": 0, "moderada": 1, "compleja": 2, "muy_compleja": 3
        }
        ordenadas = sorted(
            analisis,
            key=lambda a: (
                orden_complejidad.get(a.complejidad_estimada, 2),
                -a.score_completitud
            )
        )
        return [a.historia_key for a in ordenadas]

    def _cargar_yaml_requisito(self, req_id: str) -> Optional[dict]:
        """Carga el YAML del requisito desde el repositorio."""
        if not req_id:
            return None
        import yaml
        from pathlib import Path
        for ruta in Path(self.config.repo_requisitos).rglob(f"{req_id}.yaml"):
            with open(ruta, encoding="utf-8") as f:
                return yaml.safe_load(f)
        return None

    def _agenda_vacia(
        self, sprint_id: str, duracion: int
    ) -> AgendaRefinamiento:
        return AgendaRefinamiento(
            sprint_id=sprint_id,
            fecha_sesion="",
            duracion_total_min=duracion,
            historias=[],
            historias_bloqueadas=[],
            historias_listas=[],
            tiempo_estimado_total_min=0,
            puede_completarse_en_sesion=True,
            orden_recomendado=[]
        )
```

### Generación del briefing por participante

Cada participante recibe un briefing adaptado a su rol. El desarrollador recibe las preguntas técnicas y las dependencias. El representante de negocio recibe las preguntas de reglas y criterios. El analista recibe el cuadro completo.

```python
# refinement_briefing_generator.py

class GeneradorBriefingParticipante:
    """
    Genera el material de preparación individual para cada participante
    de la sesión de refinamiento, adaptado a su rol.
    """

    FILTROS_POR_ROL = {
        "negocio": ["criterio_ac", "regla_negocio", "flujo_error"],
        "tecnico": ["estimacion", "dato_entrada", "dependencia", "contorno"],
        "analista": None,   # Recibe todo
        "qa": ["criterio_ac", "flujo_error", "contorno"]
    }

    def generar_para_rol(
        self,
        agenda: "AgendaRefinamiento",
        rol: str,
        nombre: str
    ) -> str:
        """Genera el briefing en Markdown para un participante específico."""

        filtro = self.FILTROS_POR_ROL.get(rol)
        md = f"# Briefing de refinamiento — {nombre}\n\n"
        md += f"**Rol:** {rol.capitalize()}\n"
        md += f"**Sesión:** {agenda.fecha_sesion}\n"
        md += f"**Duración prevista:** {agenda.duracion_total_min} minutos\n\n"

        if not agenda.puede_completarse_en_sesion:
            md += (
                "> ⚠ **Aviso:** El backlog candidato supera el tiempo disponible. "
                f"Se priorizarán las primeras {agenda.duracion_total_min // 20} historias "
                f"y el resto quedará para la siguiente sesión.\n\n"
            )

        md += "---\n\n"

        for historia in agenda.historias:
            md += f"## {historia.historia_key} — {historia.titulo}\n\n"
            md += f"**Complejidad estimada:** {historia.complejidad_estimada.replace('_', ' ').capitalize()}\n"
            md += f"**Tiempo en sesión:** ~{historia.tiempo_refinamiento_min} minutos\n"
            md += f"**Completitud actual:** {historia.score_completitud:.0f}/100\n\n"

            # Contexto de requisitos anteriores relacionados
            if historia.contexto_relacionado:
                md += "### Contexto del repositorio\n\n"
                md += "Historias anteriores relacionadas que pueden servir de referencia:\n\n"
                for ctx in historia.contexto_relacionado[:3]:
                    md += (
                        f"- **{ctx['requisito_id']}** "
                        f"(similitud {ctx['similitud']:.0%}): "
                        f"{ctx['texto'][:150]}...\n"
                    )
                md += "\n"

            # Contradicciones detectadas
            if historia.contradicciones:
                md += "### ⚠ Posibles contradicciones con el backlog\n\n"
                for c in historia.contradicciones:
                    md += f"- {c['descripcion']}\n"
                md += "\n"

            # Preguntas filtradas por rol
            preguntas_filtradas = [
                p for p in historia.preguntas_sugeridas
                if filtro is None or p.get("categoria") in filtro
            ]

            if preguntas_filtradas:
                md += "### Preguntas a responder en la sesión\n\n"
                for p in preguntas_filtradas:
                    icono = "🔴" if p.get("categoria") == "estimacion" else "🟡"
                    md += f"{icono} **{p['pregunta']}**\n"
                    md += f"   *Campo que completa: `{p.get('campo_que_completa', '')}`*\n"
                    if p.get("pista_de_respuesta"):
                        md += f"   *Pista: {p['pista_de_respuesta']}*\n"
                    md += f"   *Si no se responde: {p.get('impacto_si_no_se_responde', '')}*\n\n"

            md += "---\n\n"

        # Historias bloqueadas: solo para analista
        if rol == "analista" and agenda.historias_bloqueadas:
            md += "## Historias bloqueadas (no entran a esta sesión)\n\n"
            for h in agenda.historias_bloqueadas:
                md += f"- **{h['key']}** {h['titulo']}\n"
                for dep in h["bloqueada_por"]:
                    md += f"  - Bloqueada por: {dep}\n"
            md += "\n"

        return md
```

---

## Fase durante la sesión — Apoyo en tiempo real

### Arquitectura del panel de apoyo

El panel de apoyo es una interfaz web ligera que el facilitador (el analista) tiene visible en una pantalla secundaria o en una ventana minimizada durante la sesión. No interrumpe la dinámica del grupo: el facilitador lo consulta cuando lo necesita, no responde automáticamente en voz alta.

El panel tiene tres modos de operación que el facilitador selecciona según el momento de la sesión:

**Modo escucha:** el sistema analiza la conversación en tiempo real (transcripción de audio o notas rápidas del facilitador) y prepara sugerencias sin mostrarlas todavía.

**Modo sugerencia:** el sistema muestra proactivamente las preguntas pendientes de respuesta cuando detecta que la conversación avanza sin haberlas cubierto.

**Modo consulta:** el facilitador hace preguntas directas al sistema y recibe respuestas en tiempo real ("¿Tenemos algún requisito anterior que haya resuelto este caso?").

```python
# refinement_realtime_assistant.py

import asyncio
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class SugerenciaEnTiempoReal:
    tipo: str               # pregunta │ contradiccion │ criterio_ac │ alerta
    contenido: str          # El texto de la sugerencia
    urgencia: str           # alta │ media │ baja
    campo_relacionado: str  # Campo del YAML que se está trabajando
    origen: str             # De dónde viene la sugerencia
    timestamp: str


class AsistenteRefinamientoRealtime:
    """
    Asistente en tiempo real durante la sesión de refinamiento.
    Se integra con el panel del facilitador vía WebSocket para
    latencia mínima (<2 segundos desde la entrada hasta la sugerencia).
    """

    INDICADORES_GAP_EN_CONVERSACION = [
        # Frases que indican que el equipo está dejando algo sin definir
        "lo vemos después",
        "eso ya lo sabemos",
        "es obvio",
        "como siempre",
        "igual que antes",
        "no hace falta especificarlo",
        "el desarrollador ya sabe",
        "ya lo decidiremos",
        "depende",
        "en principio sí",
        "más o menos"
    ]

    INDICADORES_FLUJO_ERROR_NO_CUBIERTO = [
        "cuando funciona bien",
        "en el caso normal",
        "el flujo estándar",
        "el camino feliz"
        # Si aparecen estos sin que después aparezca "qué pasa si" o "error",
        # probablemente los flujos de error no se están cubriendo
    ]

    def __init__(
        self,
        historia_en_curso: "AnalisisHistoriaRefinamiento",
        motor_rag,
        openai_client,
        glosario: dict
    ):
        self.historia = historia_en_curso
        self.rag = motor_rag
        self.openai = openai_client
        self.glosario = glosario
        self.preguntas_respondidas: set[int] = set()
        self.criterios_ac_generados: list[dict] = []
        self.transcripcion_acumulada: list[str] = []
        self.alertas_enviadas: set[str] = set()

    async def procesar_fragmento_conversacion(
        self, texto: str
    ) -> list[SugerenciaEnTiempoReal]:
        """
        Procesa un fragmento de la conversación (transcripción de 30-60 segundos)
        y retorna las sugerencias relevantes para el facilitador.
        """
        self.transcripcion_acumulada.append(texto)
        texto_completo = " ".join(self.transcripcion_acumulada[-5:])  # Últimos 5 fragmentos

        sugerencias = []

        # Detectar indicadores de gap sin resolver
        gaps_detectados = self._detectar_indicadores_gap(texto)
        if gaps_detectados:
            sugerencia = await self._generar_sugerencia_gap(
                texto, gaps_detectados
            )
            if sugerencia:
                sugerencias.append(sugerencia)

        # Verificar si las preguntas del briefing se están respondiendo
        preguntas_sin_cubrir = self._identificar_preguntas_sin_cubrir(texto_completo)
        if preguntas_sin_cubrir:
            sugerencias.extend([
                SugerenciaEnTiempoReal(
                    tipo="pregunta",
                    contenido=(
                        f"Pregunta pendiente: **{p['pregunta']}**\n"
                        f"*Impacto si no se responde: {p['impacto_si_no_se_responde']}*"
                    ),
                    urgencia="alta" if p.get("categoria") == "estimacion" else "media",
                    campo_relacionado=p.get("campo_que_completa", ""),
                    origen="briefing_previo",
                    timestamp=datetime.now().isoformat()
                )
                for p in preguntas_sin_cubrir[:2]  # Máximo 2 a la vez
            ])

        # Detectar si se menciona un criterio de aceptación que podemos capturar
        criterio_detectado = await self._detectar_criterio_ac(texto)
        if criterio_detectado:
            sugerencias.append(criterio_detectado)

        # Detectar posibles contradicciones con el repositorio
        contradiccion = await self._verificar_contradiccion_rag(texto)
        if contradiccion:
            sugerencias.append(contradiccion)

        return sugerencias

    def _detectar_indicadores_gap(self, texto: str) -> list[str]:
        """Detecta frases que indican que algo queda sin definir."""
        texto_lower = texto.lower()
        return [
            indicador for indicador in self.INDICADORES_GAP_EN_CONVERSACION
            if indicador in texto_lower
        ]

    async def _generar_sugerencia_gap(
        self, texto: str, indicadores: list[str]
    ) -> Optional[SugerenciaEnTiempoReal]:
        """
        Cuando detecta indicadores de ambigüedad, genera una pregunta
        específica basada en el contexto de la conversación.
        """
        # Evitar repetir alertas idénticas
        clave = "|".join(sorted(indicadores))
        if clave in self.alertas_enviadas:
            return None
        self.alertas_enviadas.add(clave)

        prompt = f"""
El equipo de refinamiento está discutiendo la siguiente historia:
"{self.historia.titulo}"

En la última intervención se detectaron estas expresiones que indican
que algo puede estar quedando sin definir:
{', '.join(f'"{i}"' for i in indicadores)}

Texto de la conversación:
"{texto}"

Genera UNA pregunta concisa (máximo 20 palabras) que el facilitador
puede hacer para concretar lo que está quedando ambiguo.
La pregunta debe ser en lenguaje de negocio, sin tecnicismos.
Responde SOLO con la pregunta, sin explicación.
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=60,
            messages=[{"role": "user", "content": prompt}]
        )

        pregunta = response.choices[0].message.content.strip()
        if not pregunta:
            return None

        return SugerenciaEnTiempoReal(
            tipo="pregunta",
            contenido=f"💬 {pregunta}",
            urgencia="media",
            campo_relacionado="criterios_aceptacion",
            origen="detector_ambiguedad",
            timestamp=datetime.now().isoformat()
        )

    def _identificar_preguntas_sin_cubrir(
        self, texto_conversacion: str
    ) -> list[dict]:
        """
        Comprueba cuáles de las preguntas del briefing no han sido
        abordadas aún en la conversación, basándose en palabras clave.
        """
        texto_lower = texto_conversacion.lower()
        sin_cubrir = []

        for i, pregunta in enumerate(self.historia.preguntas_sugeridas):
            if i in self.preguntas_respondidas:
                continue

            # Comprobar si el tema de la pregunta ha aparecido en la conversación
            campo = pregunta.get("campo_que_completa", "").lower()
            palabras_clave = campo.replace("_", " ").split()

            if not any(palabra in texto_lower for palabra in palabras_clave):
                sin_cubrir.append(pregunta)

        return sin_cubrir

    async def _detectar_criterio_ac(
        self, texto: str
    ) -> Optional[SugerenciaEnTiempoReal]:
        """
        Detecta si en la conversación se está articulando implícitamente
        un criterio de aceptación y lo captura en formato Dado/Cuando/Entonces.
        """
        # Solo activar si hay estructura condicional en el texto
        indicadores_ac = ["si ", "cuando ", "en caso de ", "siempre que ", "debe "]
        texto_lower = texto.lower()
        if not any(ind in texto_lower for ind in indicadores_ac):
            return None

        prompt = f"""
El equipo está discutiendo la historia: "{self.historia.titulo}"

En la conversación se dijo: "{texto}"

¿Se puede extraer de esto un criterio de aceptación en formato Dado/Cuando/Entonces?
Si sí, extráelo. Si no, responde "NO".

Responde en uno de estos dos formatos:

Formato SÍ:
DADO: [contexto]
CUANDO: [acción]
ENTONCES: [resultado esperado]

Formato NO:
NO
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

        contenido = response.choices[0].message.content.strip()
        if contenido.startswith("NO"):
            return None

        return SugerenciaEnTiempoReal(
            tipo="criterio_ac",
            contenido=(
                f"✅ Criterio detectado en la conversación:\n\n"
                f"```\n{contenido}\n```\n\n"
                f"*¿Lo añadimos como criterio de aceptación?*"
            ),
            urgencia="alta",
            campo_relacionado="criterios_aceptacion",
            origen="detector_criterio_ac",
            timestamp=datetime.now().isoformat()
        )

    async def _verificar_contradiccion_rag(
        self, texto: str
    ) -> Optional[SugerenciaEnTiempoReal]:
        """
        Busca en el repositorio si algo de lo que se está diciendo
        contradice un requisito ya validado.
        """
        if len(texto.split()) < 10:
            return None  # Texto demasiado corto para buscar

        resultados = self.rag.buscar_por_similitud(
            query_texto=texto,
            filtros={
                "chunk_tipo": "reglas_negocio",
                "estado": "validado"
            },
            top_k=3
        )

        for r in resultados:
            if (r.similitud > 0.87 and
                    r.metadatos.get("requisito_id") != self.historia.requisito_origen):
                clave = f"contradiccion_{r.chunk_id}"
                if clave in self.alertas_enviadas:
                    continue
                self.alertas_enviadas.add(clave)

                return SugerenciaEnTiempoReal(
                    tipo="contradiccion",
                    contenido=(
                        f"⚠ Posible contradicción con **{r.metadatos.get('requisito_id')}**\n\n"
                        f"Ese requisito establece: *{r.texto[:250]}*\n\n"
                        f"¿Estáis definiendo algo diferente o es coherente con esto?"
                    ),
                    urgencia="alta",
                    campo_relacionado="reglas_negocio",
                    origen="rag_contradiccion",
                    timestamp=datetime.now().isoformat()
                )
        return None

    def marcar_pregunta_respondida(self, indice_pregunta: int):
        """El facilitador marca una pregunta como respondida."""
        self.preguntas_respondidas.add(indice_pregunta)

    def registrar_criterio_ac_aprobado(self, criterio: dict):
        """El facilitador aprueba un criterio AC capturado por el asistente."""
        self.criterios_ac_generados.append(criterio)

    def resumen_sesion_hasta_ahora(self) -> dict:
        """Estado actual de la historia tras la conversación hasta este punto."""
        return {
            "historia_key": self.historia.historia_key,
            "preguntas_totales": len(self.historia.preguntas_sugeridas),
            "preguntas_respondidas": len(self.preguntas_respondidas),
            "criterios_ac_capturados": len(self.criterios_ac_generados),
            "porcentaje_completitud_sesion": round(
                len(self.preguntas_respondidas) /
                max(len(self.historia.preguntas_sugeridas), 1) * 100
            ),
            "criterios_generados": self.criterios_ac_generados
        }
```

### Modo consulta directa — El facilitador pregunta al sistema

El facilitador puede hacer consultas directas al sistema en cualquier momento de la sesión. Estas consultas van al contexto del RAG más el LLM y tienen un tiempo de respuesta objetivo de menos de 3 segundos.

```python
# refinement_query_handler.py

class ManejadorConsultasRefinamiento:
    """
    Gestiona las consultas directas que el facilitador hace al sistema
    durante la sesión. Diseñado para respuestas en <3 segundos.
    """

    TIPOS_CONSULTA = {
        "historico": [
            "¿tenemos algún requisito anterior",
            "¿cómo lo hicimos antes",
            "¿hay algo similar",
            "¿existe ya algo que"
        ],
        "criterio_ac": [
            "¿cómo quedaría el criterio",
            "¿cómo se redactaría",
            "dame un ejemplo de criterio",
            "¿cómo verificamos que"
        ],
        "contorno": [
            "¿qué pasa si el valor es cero",
            "¿qué pasa con el máximo",
            "¿y si no hay datos",
            "¿qué pasa en el límite",
            "¿qué pasa si está vacío"
        ],
        "estimacion": [
            "¿cuánto crees que llevaría",
            "¿es muy complejo",
            "¿merece la pena partirlo"
        ]
    }

    def __init__(
        self,
        historia_en_curso: "AnalisisHistoriaRefinamiento",
        motor_rag,
        openai_client,
        glosario: dict
    ):
        self.historia = historia_en_curso
        self.rag = motor_rag
        self.openai = openai_client
        self.glosario = glosario

    async def responder(self, consulta: str) -> dict:
        """
        Punto de entrada para consultas del facilitador.
        Detecta el tipo de consulta y enruta al handler específico.
        """
        tipo = self._detectar_tipo(consulta)

        if tipo == "historico":
            return await self._responder_historico(consulta)
        if tipo == "criterio_ac":
            return await self._responder_criterio_ac(consulta)
        if tipo == "contorno":
            return await self._responder_contorno(consulta)
        if tipo == "estimacion":
            return await self._responder_estimacion(consulta)

        # Consulta genérica
        return await self._responder_generica(consulta)

    def _detectar_tipo(self, consulta: str) -> str:
        consulta_lower = consulta.lower()
        for tipo, patrones in self.TIPOS_CONSULTA.items():
            if any(p in consulta_lower for p in patrones):
                return tipo
        return "generica"

    async def _responder_historico(self, consulta: str) -> dict:
        """Busca en el repositorio RAG y retorna los requisitos más relevantes."""
        resultados = self.rag.buscar_por_similitud(
            query_texto=consulta,
            filtros={"estado": "validado"},
            top_k=4
        )

        if not resultados:
            return {
                "tipo": "historico",
                "respuesta": "No encontré requisitos anteriores directamente relacionados.",
                "fuentes": []
            }

        fuentes = [
            {
                "id": r.metadatos.get("requisito_id"),
                "similitud": f"{r.similitud:.0%}",
                "extracto": r.texto[:300]
            }
            for r in resultados
        ]

        prompt = f"""
El facilitador de una sesión de refinamiento pregunta: "{consulta}"

Contexto de la historia actual: {self.historia.titulo}

Estos son los requisitos anteriores más relevantes del repositorio:
{chr(10).join(f"[{f['id']} - {f['similitud']}] {f['extracto']}" for f in fuentes)}

Responde en 3-4 frases máximo, indicando qué hay en el repositorio que
sea relevante para la pregunta del facilitador. Sé directo y específico.
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "tipo": "historico",
            "respuesta": response.choices[0].message.content.strip(),
            "fuentes": fuentes[:3]
        }

    async def _responder_criterio_ac(self, consulta: str) -> dict:
        """Genera un criterio de aceptación basándose en la conversación."""
        prompt = f"""
Historia en refinamiento: "{self.historia.titulo}"
Contexto de la conversación: "{consulta}"

Genera un criterio de aceptación completo en formato Dado/Cuando/Entonces.
El criterio debe ser:
- Verificable con una prueba concreta (PASS/FAIL)
- Específico (sin "adecuado", "correcto", "rápido")
- Con datos concretos de ejemplo cuando sea posible

Formato de respuesta:
**Dado:** [estado inicial]
**Cuando:** [una acción concreta]
**Entonces:** [resultado observable y medible]

**Datos de ejemplo:**
- [campo]: [valor concreto]
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "tipo": "criterio_ac",
            "respuesta": response.choices[0].message.content.strip(),
            "accion_disponible": "aprobar_y_añadir"  # El facilitador puede aprobarlo directamente
        }

    async def _responder_contorno(self, consulta: str) -> dict:
        """
        Responde preguntas sobre casos de contorno.
        Identifica el campo numérico o de fecha implicado y
        genera los cuatro casos límite estándar.
        """
        datos_entrada = (
            self.historia.preguntas_sugeridas[0].get("pista_de_respuesta", "")
            if self.historia.preguntas_sugeridas else ""
        )

        prompt = f"""
Historia: "{self.historia.titulo}"
Pregunta del facilitador: "{consulta}"
Contexto adicional: {datos_entrada}

El equipo está preguntando por casos de contorno.
Identifica el campo o restricción sobre el que preguntan y genera
los cuatro casos límite estándar:
1. Valor en el límite inferior exacto → debe funcionar
2. Valor un paso por debajo del límite inferior → debe fallar
3. Valor en el límite superior exacto → debe funcionar
4. Valor un paso por encima del límite superior → debe fallar

Si no hay límite inferior claro, indica el caso del valor mínimo posible.
Usa datos concretos. Responde de forma concisa, en formato de lista.
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "tipo": "contorno",
            "respuesta": response.choices[0].message.content.strip(),
            "nota": "Estos casos deben añadirse como criterios AC o anotarse para los test cases."
        }

    async def _responder_estimacion(self, consulta: str) -> dict:
        """
        Responde preguntas sobre estimación de complejidad,
        incluyendo si la historia debe partirse.
        """
        n_ac = len(self.historia.preguntas_sugeridas)
        complejidad = self.historia.complejidad_estimada
        n_gaps = len(self.historia.gaps_detectados)

        respuesta = (
            f"Con {n_ac} preguntas pendientes y complejidad **{complejidad}**, "
        )

        if complejidad == "muy_compleja" or n_gaps > 5:
            respuesta += (
                "recomendaría considerar partirla. Una historia muy compleja "
                "que no está clara en el refinamiento suele bloquearse en el sprint. "
                "¿Hay una parte que se pueda entregar independientemente de la otra?"
            )
        elif complejidad in ("compleja",):
            respuesta += (
                "puede entrar al sprint si resolvéis las preguntas principales "
                f"(quedan ~{n_gaps} gaps pendientes). Si no da tiempo hoy, "
                "puede quedar para el siguiente refinamiento."
            )
        else:
            respuesta += (
                "la historia tiene tamaño razonable. Si respondéis las "
                "preguntas pendientes en los próximos minutos, puede estar "
                "lista para el sprint."
            )

        return {
            "tipo": "estimacion",
            "respuesta": respuesta,
            "datos": {
                "complejidad": complejidad,
                "preguntas_pendientes": n_ac,
                "gaps_detectados": n_gaps
            }
        }

    async def _responder_generica(self, consulta: str) -> dict:
        """Responde consultas no clasificadas usando RAG + LLM."""
        contexto_rag = self.rag.buscar_por_similitud(
            query_texto=consulta,
            filtros={"estado": "validado"},
            top_k=3
        )

        contexto_str = "\n".join([
            f"[{r.metadatos.get('requisito_id')}]: {r.texto[:200]}"
            for r in contexto_rag
        ]) if contexto_rag else "Sin contexto relevante en el repositorio."

        prompt = f"""
Eres el asistente de una sesión de refinamiento Agile.
Historia en discusión: "{self.historia.titulo}"
El facilitador pregunta: "{consulta}"

Contexto del repositorio de requisitos:
{contexto_str}

Responde de forma concisa (máximo 4 frases). Si no tienes información
suficiente, dilo claramente en lugar de inventar.
        """

        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "tipo": "generica",
            "respuesta": response.choices[0].message.content.strip()
        }
```

---

## Fase posterior a la sesión — Cierre asistido

### Validación y actualización automática

Al terminar el refinamiento de cada historia, el sistema ejecuta un cierre en cuatro pasos sin intervención del facilitador.

```python
# refinement_closure.py

import yaml
from pathlib import Path
from datetime import datetime


class CierreSesionRefinamiento:
    """
    Ejecuta el cierre automático de la sesión de refinamiento:
    valida las historias refinadas, actualiza el repositorio
    y genera los artefactos faltantes.
    """

    def __init__(
        self,
        validador,
        motor_pipeline,
        motor_trazabilidad,
        conector_jira,
        config
    ):
        self.validador = validador
        self.pipeline = motor_pipeline
        self.trazabilidad = motor_trazabilidad
        self.jira = conector_jira
        self.config = config

    async def cerrar_historia(
        self,
        historia_key: str,
        asistente: "AsistenteRefinamientoRealtime",
        notas_sesion: str = ""
    ) -> dict:
        """
        Punto de entrada tras terminar el refinamiento de una historia.
        Consolida todo lo capturado durante la sesión.
        """
        resumen = asistente.resumen_sesion_hasta_ahora()
        resultado = {
            "historia_key": historia_key,
            "acciones": [],
            "advertencias": [],
            "lista_para_sprint": False
        }

        # 1. Incorporar los criterios AC capturados al YAML del requisito
        if asistente.criterios_ac_generados:
            actualizado = await self._incorporar_criterios_al_yaml(
                asistente.historia.requisito_origen,
                asistente.criterios_ac_generados
            )
            if actualizado:
                resultado["acciones"].append(
                    f"{len(asistente.criterios_ac_generados)} criterios AC "
                    f"incorporados al YAML de {asistente.historia.requisito_origen}"
                )

        # 2. Ejecutar validación sobre el YAML actualizado
        yaml_actualizado = self._cargar_yaml(asistente.historia.requisito_origen)
        if yaml_actualizado:
            informe_val = await self.validador.ejecutar_completo(yaml_actualizado)
            score_final = informe_val.get(
                "puntuacion_global", {}
            ).get("valor", 0)
            veredicto = informe_val.get("veredicto_final", "")

            resultado["score_final"] = score_final
            resultado["veredicto"] = veredicto

            if veredicto == "BLOQUEADO":
                resultado["advertencias"].append(
                    f"Score {score_final}/100. La historia todavía tiene "
                    f"gaps bloqueantes. No puede entrar al sprint sin más trabajo."
                )
                resultado["lista_para_sprint"] = False
            elif veredicto == "APROBADO_CON_ADVERTENCIAS":
                resultado["advertencias"].append(
                    f"Score {score_final}/100. Historia aprobada con advertencias. "
                    f"Puede entrar al sprint pero revisa las advertencias antes del planning."
                )
                resultado["lista_para_sprint"] = True
            else:
                resultado["lista_para_sprint"] = True
                resultado["acciones"].append(
                    f"Historia validada: score {score_final}/100. Lista para el sprint."
                )

        # 3. Añadir notas de la sesión como comentario en Jira
        if notas_sesion or resumen["criterios_ac_capturados"] > 0:
            comentario = self._generar_comentario_cierre(resumen, notas_sesion)
            self.jira.cliente.post(
                f"issue/{historia_key}/comment",
                payload={
                    "body": self.jira.constructor._construir_adf(comentario)
                }
            )
            resultado["acciones"].append(
                f"Notas de refinamiento añadidas en {historia_key}"
            )

        # 4. Mover la historia al estado correcto en Jira
        nuevo_estado = (
            "Ready for Sprint" if resultado["lista_para_sprint"]
            else "Needs More Work"
        )
        self._transicionar_estado_jira(historia_key, nuevo_estado)
        resultado["acciones"].append(
            f"Historia movida a '{nuevo_estado}' en Jira"
        )

        # 5. Si está lista, pre-generar test cases base para el QA
        if resultado["lista_para_sprint"] and yaml_actualizado:
            n_tc = await self._pregenerar_test_cases(
                yaml_actualizado, historia_key
            )
            if n_tc > 0:
                resultado["acciones"].append(
                    f"{n_tc} test cases base pre-generados y disponibles en Xray"
                )

        return resultado

    async def _incorporar_criterios_al_yaml(
        self,
        req_id: str,
        criterios_nuevos: list[dict]
    ) -> bool:
        """Añade los criterios capturados en sesión al YAML del requisito."""
        ruta = self._encontrar_yaml(req_id)
        if not ruta:
            return False

        with open(ruta, encoding="utf-8") as f:
            req = yaml.safe_load(f)

        criterios_existentes = req.get("criterios_aceptacion", [])
        indice_siguiente = len(criterios_existentes) + 1

        for criterio in criterios_nuevos:
            nuevo_ac = {
                "id": f"AC-{req_id.replace('REQ-', '')}-{indice_siguiente:02d}",
                "titulo": criterio.get("titulo", "Criterio capturado en refinamiento"),
                "dado": criterio.get("dado", ""),
                "cuando": criterio.get("cuando", ""),
                "entonces": criterio.get("entonces", ""),
                "tipo": "positivo",
                "origen": "refinamiento_sesion",
                "fecha_captura": datetime.now().strftime("%Y-%m-%d")
            }
            criterios_existentes.append(nuevo_ac)
            indice_siguiente += 1

        req["criterios_aceptacion"] = criterios_existentes
        req["fecha_ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d")

        with open(ruta, "w", encoding="utf-8") as f:
            yaml.dump(req, f, allow_unicode=True, sort_keys=False)

        return True

    async def _pregenerar_test_cases(
        self, yaml_req: dict, historia_key: str
    ) -> int:
        """Pre-genera los test cases base para que el QA los revise."""
        try:
            resultado = await self.pipeline.generar_test_cases_desde_requisito(
                yaml_req=yaml_req,
                historia_key=historia_key,
                modo="base_only"  # Solo los casos principales, no contornos
            )
            return len(resultado)
        except Exception:
            return 0

    def _generar_comentario_cierre(
        self, resumen: dict, notas: str
    ) -> str:
        md = "## Refinamiento completado\n\n"
        md += f"**Preguntas abordadas:** {resumen['preguntas_respondidas']} "
        md += f"de {resumen['preguntas_totales']}\n"
        md += f"**Criterios AC capturados:** {resumen['criterios_ac_capturados']}\n"
        md += f"**Completitud al cierre:** {resumen['porcentaje_completitud_sesion']}%\n\n"

        if resumen["criterios_generados"]:
            md += "### Criterios de aceptación añadidos en la sesión\n\n"
            for ac in resumen["criterios_generados"]:
                md += (
                    f"**{ac.get('id', 'AC')}:**\n"
                    f"- *Dado:* {ac.get('dado', '')}\n"
                    f"- *Cuando:* {ac.get('cuando', '')}\n"
                    f"- *Entonces:* {ac.get('entonces', '')}\n\n"
                )

        if notas:
            md += f"### Notas del facilitador\n\n{notas}\n"

        return md

    def _transicionar_estado_jira(self, historia_key: str, nuevo_estado: str):
        """Mueve la historia al estado correspondiente mediante la API de transiciones."""
        transiciones = self.jira.cliente.get(
            f"issue/{historia_key}/transitions"
        ).get("transitions", [])

        transicion = next(
            (t for t in transiciones if t["name"] == nuevo_estado), None
        )
        if transicion:
            self.jira.cliente.post(
                f"issue/{historia_key}/transitions",
                payload={"transition": {"id": transicion["id"]}}
            )

    def _cargar_yaml(self, req_id: str) -> Optional[dict]:
        ruta = self._encontrar_yaml(req_id)
        if not ruta:
            return None
        with open(ruta, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _encontrar_yaml(self, req_id: str) -> Optional[Path]:
        if not req_id:
            return None
        for ruta in Path(self.config.repo_requisitos).rglob(f"{req_id}.yaml"):
            return ruta
        return None
```

---

## Integración en el orquestador principal

El refinamiento asistido se integra como un comando adicional del orquestador del punto 12, con su propia interfaz de línea de comandos.

```python
# En orchestrator.py, añadir el subcomando 'refinement':

# python orchestrator.py refinement --sprint SP-42 --preparar
# python orchestrator.py refinement --sprint SP-42 --sesion
# python orchestrator.py refinement --historia FACT-47 --cerrar

@app.command("refinement")
async def comando_refinamiento(args):

    if args.preparar:
        # Modo pre-sesión: generar agenda y briefings
        preparador = PreparadorRefinamiento(
            cliente_jira=conector_jira.cliente,
            validador=validador,
            motor_rag=motor_rag,
            openai_client=openai_client,
            config=config
        )
        agenda = await preparador.preparar_sesion(
            sprint_id=args.sprint,
            duracion_sesion_min=args.duracion or 90
        )
        _publicar_agenda(agenda, config)
        _generar_briefings_por_rol(agenda, config)
        print(f"✓ Agenda generada: {len(agenda.historias)} historias")
        print(f"  Tiempo estimado: {agenda.tiempo_estimado_total_min} min")
        if not agenda.puede_completarse_en_sesion:
            print(f"  ⚠ No cabe todo en {agenda.duracion_total_min} min")

    elif args.cerrar:
        # Modo post-historia: cerrar y actualizar el repositorio
        cierre = CierreSesionRefinamiento(
            validador=validador,
            motor_pipeline=motor_pipeline,
            motor_trazabilidad=motor_trazabilidad,
            conector_jira=conector_jira,
            config=config
        )
        resultado = await cierre.cerrar_historia(
            historia_key=args.historia,
            asistente=_recuperar_asistente_sesion(args.historia),
            notas_sesion=args.notas or ""
        )
        _imprimir_resultado_cierre(resultado)
```

---

## Panel de facilitador — Especificación de la interfaz

El panel es una aplicación web ligera que se despliega localmente durante la sesión. Se diseña para funcionar en una pantalla secundaria con el facilitador mirándola de forma intermitente, no continua. El principio de diseño es que nada debe exigir atención del facilitador si no hay algo urgente.

```
┌────────────────────────────────────────────────────────────┐
│  REFINAMIENTO ASISTIDO — Sprint 42                         │
│  Historia actual: FACT-47 · ~20 min restantes              │
├────────────────────────────────────────────────────────────┤
│  PREGUNTAS PENDIENTES (4/7 respondidas)                    │
│                                                            │
│  🔴 ¿Cuál es el rango máximo de días permitido?            │
│     [Marcar respondida]                                    │
│                                                            │
│  🟡 ¿Qué pasa si no hay facturas en el período?            │
│     [Marcar respondida]                                    │
│                                                            │
│  🟡 ¿El filtro aplica solo al año fiscal actual?           │
│     [Marcar respondida]                                    │
├────────────────────────────────────────────────────────────┤
│  SUGERENCIAS DEL ASISTENTE                                 │
│                                                            │
│  💬 "¿Y si el rango seleccionado no tiene ninguna          │
│     factura? ¿Qué ve el usuario?"                          │
│     [Usar esta pregunta]  [Descartar]                      │
│                                                            │
│  ✅ Criterio detectado en la conversación:                  │
│     DADO: el gestor selecciona un rango válido             │
│     CUANDO: pulsa Buscar                                   │
│     ENTONCES: el listado se actualiza en <2 segundos       │
│     [Añadir al requisito]  [Editar]  [Descartar]           │
├────────────────────────────────────────────────────────────┤
│  CONSULTA DIRECTA                                          │
│  ┌──────────────────────────────────────────────┐  [▶]    │
│  │ ¿Tenemos algo similar en el módulo de pedidos│          │
│  └──────────────────────────────────────────────┘          │
├────────────────────────────────────────────────────────────┤
│  [Cerrar historia]  [Siguiente historia]  [Ver contexto]   │
└────────────────────────────────────────────────────────────┘
```

---

## Flujo completo de ejemplo — Una historia en refinamiento

Este ejemplo muestra cómo interactúan todos los componentes durante un refinamiento real de la historia FACT-47 (filtrado de facturas por fecha).

**24 horas antes de la sesión:**
El preparador detecta que FACT-47 tiene un score de 71/100. Genera 6 preguntas priorizadas. La primera pregunta es "¿Cuál es el rango máximo de días que puede seleccionarse?" porque el campo `reglas_negocio` tiene la regla de los 365 días definida pero el criterio AC que la verifica está ausente.

**Al inicio de la sesión:**
El analista abre el panel de apoyo con FACT-47 cargada. Las 6 preguntas aparecen ordenadas. El team lead de negocio y dos desarrolladores están en la sala.

**Minuto 5 de la discusión sobre FACT-47:**
Alguien dice "eso ya lo decidimos, era un año". El asistente detecta el indicador "ya lo decidimos" y sugiere: "¿El límite de 365 días está documentado o lo establecemos ahora?" El facilitador usa la pregunta. El representante de negocio confirma: 365 días.

**Minuto 8:**
Se está hablando del flujo de búsqueda. Alguien dice "cuando el gestor pulsa Buscar, el sistema muestra los resultados". El asistente detecta estructura de criterio AC y captura: *DADO: el gestor introduce un rango válido. CUANDO: pulsa Buscar. ENTONCES: el sistema muestra las facturas del período ordenadas por fecha descendente.* El facilitador lo aprueba con un clic.

**Minuto 12:**
El facilitador consulta directamente: "¿Tenemos algo parecido en el módulo de pedidos?" El asistente busca en el RAG y responde en 2 segundos: "Sí, REQ-015 en EP-02 define un filtrado por fecha similar con un límite de 180 días. Los criterios de error están en AC-015-03 y AC-015-04, que pueden servir de referencia."

**Minuto 18:**
El facilitador pregunta "¿cómo quedaría el criterio para el caso en que no hay resultados?" El asistente genera: *DADO: el gestor ejecuta una búsqueda válida. CUANDO: no existen facturas en el período. ENTONCES: se muestra el mensaje 'No se encontraron facturas' y el botón 'Ampliar búsqueda'.* El facilitador lo edita ligeramente y lo aprueba.

**Al cerrar FACT-47:**
El cierre automático incorpora los 3 criterios capturados al YAML. La validación da score 88/100. La historia pasa a "Ready for Sprint" en Jira. Se pre-generan 7 test cases base. El desarrollador recibe un comentario en FACT-47 con los criterios acordados.

**Tiempo total en la sesión: 20 minutos.** Sin el asistente, la misma historia habría necesitado entre 35 y 45 minutos, y habría salido sin los criterios de error documentados.

---

## Métricas de la ceremonia

El sistema registra automáticamente estas métricas para el dashboard de gobierno del punto 12:

| Métrica | Descripción | Señal de alarma |
|---|---|---|
| **Historias por hora de refinamiento** | Historias que salen listas por hora de sesión | <1.5 historias/hora indica sesiones ineficientes |
| **Preguntas respondidas vs generadas** | Porcentaje de las preguntas del briefing que se responden | <60% indica que el briefing no está siendo útil o las preguntas son demasiado genéricas |
| **Criterios AC capturados en sesión** | Criterios que no existían antes del refinamiento y se añaden durante | 0 durante varias sesiones indica que el análisis previo es muy completo o que el asistente no está detectando bien |
| **Delta de score pre/post refinamiento** | Mejora del score de validación entre el análisis previo y el cierre | <10 puntos de mejora indica que la sesión no está siendo productiva |
| **Historias que salen bloqueadas** | Historias que terminan el refinamiento sin poder entrar al sprint | >30% es señal de que las historias llegan al refinamiento demasiado inmaduras |
| **Tiempo de consulta directa** | Tiempo de respuesta del asistente a las preguntas del facilitador | >5 segundos interrumpe el flujo de la sesión |

---

## Relación con los demás componentes del modelo

Este flujo cierra un ciclo que los componentes existentes no cubren completamente. El **Event Storming del punto 3** captura los requisitos desde cero en un workshop de descubrimiento. La **plantilla del punto 1** y el **glosario del punto 2** los estructuran. El **validador del punto 6** los audita. Pero entre la auditoría y el sprint planning falta el refinamiento, que es donde los requisitos se convierten en historias listas para el desarrollo.

El asistente de refinamiento conecta directamente con el **RAG del punto 7** para responder preguntas sobre el historial del proyecto sin interrumpir la sesión. Los criterios capturados durante la sesión entran al **pipeline de generación del punto 4** para producir los test cases base antes del sprint. El grafo de **trazabilidad del punto 9** se actualiza automáticamente con los nuevos criterios al cerrar cada historia. Y las métricas de la ceremonia alimentan el **dashboard de gobierno del punto 12**.

El resultado práctico es que el refinamiento deja de ser una ceremonia donde el equipo descubre qué falta y se convierte en una ceremonia donde el equipo decide qué es mejor, porque los gaps ya están identificados y el contexto histórico está disponible en segundos.
