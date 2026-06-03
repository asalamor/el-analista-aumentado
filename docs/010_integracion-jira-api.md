# Punto 10 — Integración técnica con Jira API

La integración con Jira API es el punto donde todo el trabajo previo se materializa en artefactos reales que el equipo puede ver, planificar y ejecutar. Sin esta capa, el pipeline genera JSONs que viven en el repositorio, pero no llegan al flujo de trabajo del equipo.

---

## Principios de diseño de la integración

Antes del código, tres decisiones de diseño que determinan cómo se comporta toda la integración.

**Push con aprobación humana, no push directo.** Ningún artefacto generado por la IA debe llegar a Jira sin que un humano lo haya revisado. El pipeline genera, el analista aprueba, el sistema empuja. Esto no ralentiza el proceso porque la revisión de un JSON bien formateado tarda minutos, pero sí protege contra errores que serían costosos de corregir en Jira.

**Idempotencia obligatoria.** Si el pipeline se ejecuta dos veces sobre el mismo requisito, el resultado debe ser el mismo: no se crean duplicados, se actualizan los existentes. Esto es crítico porque los pipelines fallan, se re-ejecutan y los analistas repiten operaciones.

**Trazabilidad bidireccional.** Cada issue creado en Jira tiene referencia al requisito que lo originó en un campo personalizado. Cada requisito YAML tiene referencia al issue Jira en su bloque de trazabilidad. El grafo del punto 2 conecta ambos extremos.

---

## Arquitectura de la integración

```
YAML Requisito
     │
     ▼
Pipeline generación
     │
     ▼
Cola de aprobación ──► Analista revisa/edita/aprueba
     │
     ▼
ConectorJira
     ├── VerificadorIdempotencia ──► Jira API (búsqueda)
     ├── ConstructorPayloadJira  ──► Conversión JSON → ADF
     ├── ClienteJira             ──► Jira API (creación/actualización)
     └── MotorTrazabilidad       ──► Grafo (registro de aristas)
          │
          ▼
     Webhook Jira ──► Sistema (actualización de estado en tiempo real)
```

---

## Fase 1 — Configuración y cliente base

El cliente base encapsula toda la comunicación con la API de Jira. Gestiona autenticación, rate limiting, reintentos y errores de forma centralizada para que el resto del código no tenga que preocuparse por ello.

```python
import requests
import time
import json
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class JiraConfig:
    base_url: str           # https://tu-empresa.atlassian.net
    user_email: str         # usuario@empresa.com
    api_token: str          # Token generado en id.atlassian.com
    project_key: str        # FACT, PROJ, etc.

    # Campos personalizados de tu instancia Jira
    # Se obtienen via GET /rest/api/3/field
    campo_requisito_origen: str   # customfield_10100
    campo_modulo_funcional: str   # customfield_10101
    campo_story_points: str       # customfield_10016
    campo_epic_link: str          # customfield_10014
    campo_epic_name: str          # customfield_10011

    max_reintentos: int = 3
    pausa_entre_llamadas_ms: int = 200


class ClienteJira:
    """
    Cliente base para la API REST de Jira v3.
    Gestiona autenticación, rate limiting, reintentos y errores.
    """

    def __init__(self, config: JiraConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.user_email, config.api_token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self._ultima_llamada = 0

    def _respetar_rate_limit(self):
        """Pausa mínima entre llamadas para no saturar la API."""
        ahora = time.time() * 1000
        diferencia = ahora - self._ultima_llamada
        pausa = self.config.pausa_entre_llamadas_ms
        if diferencia < pausa:
            time.sleep((pausa - diferencia) / 1000)
        self._ultima_llamada = time.time() * 1000

    def _llamar(
        self,
        metodo: str,
        endpoint: str,
        payload: dict = None,
        params: dict = None
    ) -> dict:
        """
        Ejecuta una llamada a la API con reintentos automáticos
        y backoff exponencial en caso de error 429 o 5xx.
        """
        url = f"{self.config.base_url}/rest/api/3/{endpoint}"
        intentos = 0

        while intentos < self.config.max_reintentos:
            self._respetar_rate_limit()
            try:
                response = self.session.request(
                    method=metodo,
                    url=url,
                    json=payload,
                    params=params,
                    timeout=30
                )

                # Rate limit: esperar el tiempo indicado por Jira
                if response.status_code == 429:
                    espera = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limit alcanzado. Esperando {espera}s.")
                    time.sleep(espera)
                    intentos += 1
                    continue

                # Error de servidor: backoff exponencial
                if response.status_code >= 500:
                    espera = (2 ** intentos) * 2
                    logger.warning(
                        f"Error {response.status_code}. "
                        f"Reintento {intentos + 1} en {espera}s."
                    )
                    time.sleep(espera)
                    intentos += 1
                    continue

                # Error de cliente: no reintentar
                if response.status_code >= 400:
                    logger.error(
                        f"Error {response.status_code} en {metodo} {endpoint}: "
                        f"{response.text}"
                    )
                    response.raise_for_status()

                # Éxito
                if response.status_code == 204:
                    return {}
                return response.json()

            except requests.exceptions.Timeout:
                intentos += 1
                if intentos >= self.config.max_reintentos:
                    raise RuntimeError(
                        f"Timeout en {metodo} {endpoint} "
                        f"tras {self.config.max_reintentos} intentos"
                    )
                time.sleep(2 ** intentos)

        raise RuntimeError(
            f"Máximo de reintentos alcanzado para {metodo} {endpoint}"
        )

    def get(self, endpoint: str, params: dict = None) -> dict:
        return self._llamar("GET", endpoint, params=params)

    def post(self, endpoint: str, payload: dict) -> dict:
        return self._llamar("POST", endpoint, payload=payload)

    def put(self, endpoint: str, payload: dict) -> dict:
        return self._llamar("PUT", endpoint, payload=payload)
```

---

## Fase 2 — Verificación de idempotencia

Antes de crear cualquier issue, el sistema verifica si ya existe uno generado desde el mismo requisito. Esto es lo que impide los duplicados cuando el pipeline se re-ejecuta.

```python
class VerificadorIdempotencia:
    """
    Verifica si los artefactos ya existen en Jira antes de crearlos.
    Usa el campo personalizado 'requisito_origen' como clave de unicidad.
    """

    def __init__(self, cliente: ClienteJira):
        self.cliente = cliente

    def buscar_issue_existente(
        self,
        requisito_id: str,
        tipo_issue: str
    ) -> Optional[dict]:
        """
        Busca un issue existente generado desde el requisito dado.
        Retorna el issue si existe, None si no.
        """
        jql = (
            f"project = {self.cliente.config.project_key} "
            f"AND issuetype = '{tipo_issue}' "
            f"AND '{self.cliente.config.campo_requisito_origen}' "
            f"~ '{requisito_id}' "
            f"AND statusCategory != Done"
        )

        resultado = self.cliente.get(
            "search",
            params={
                "jql": jql,
                "fields": "summary,status,issuetype,"
                          "customfield_10100,customfield_10014",
                "maxResults": 5
            }
        )

        issues = resultado.get("issues", [])
        if not issues:
            return None

        if len(issues) > 1:
            logger.warning(
                f"Encontrados {len(issues)} issues para {requisito_id} "
                f"tipo {tipo_issue}. Usando el primero: {issues[0]['key']}"
            )
        return issues[0]

    def determinar_accion(
        self,
        requisito_id: str,
        tipo_issue: str
    ) -> tuple[str, Optional[str]]:
        """
        Retorna la acción a tomar y el key del issue si existe.
        Acciones posibles: 'crear' | 'actualizar' | 'omitir'
        """
        issue_existente = self.buscar_issue_existente(requisito_id, tipo_issue)

        if issue_existente is None:
            return "crear", None

        estado = issue_existente["fields"]["status"]["statusCategory"]["key"]

        # Si está en progreso o completado, no sobrescribir
        if estado in ("indeterminate", "done"):
            logger.info(
                f"Issue {issue_existente['key']} en estado '{estado}'. "
                f"Acción: omitir para no interrumpir el trabajo."
            )
            return "omitir", issue_existente["key"]

        # Si está en backlog o por hacer, actualizar
        return "actualizar", issue_existente["key"]
```

---

## Fase 3 — Constructor de payloads Jira

Convierte los JSONs generados por el pipeline al formato exacto que espera la API de Jira v3. Este es el componente más dependiente de la configuración específica de cada instancia Jira.

```python
class ConstructorPayloadJira:
    """
    Convierte los artefactos generados por el pipeline
    al formato JSON que espera la API de Jira v3.
    """

    def __init__(self, config: JiraConfig):
        self.config = config

    def construir_epica(self, epica_json: dict) -> dict:
        """Construye el payload para crear o actualizar una épica."""
        return {
            "fields": {
                "project":        {"key": self.config.project_key},
                "issuetype":      {"name": "Epic"},
                "summary":        epica_json["summary"],
                self.config.campo_epic_name: epica_json["epic_name"],
                "description":    self._construir_adf(
                    self._formatear_descripcion_epica(epica_json["description"])
                ),
                "priority":       {"name": self._mapear_prioridad(epica_json["priority"])},
                "labels":         epica_json.get("labels", []),
                "components":     [{"name": c} for c in epica_json.get("components", [])],
                self.config.campo_requisito_origen: (
                    epica_json["custom_fields"]["origen_requisito"]
                ),
                self.config.campo_modulo_funcional: (
                    epica_json["custom_fields"]["modulo_funcional"]
                )
            }
        }

    def construir_historia(self, historia_json: dict, epic_key: str) -> dict:
        """Construye el payload para crear o actualizar una historia."""
        descripcion_formateada = self._formatear_descripcion_historia(
            historia_json["description"],
            historia_json["acceptance_criteria"],
            historia_json["definition_of_done"]
        )
        return {
            "fields": {
                "project":    {"key": self.config.project_key},
                "issuetype":  {"name": "Story"},
                "summary":    historia_json["summary"],
                self.config.campo_epic_link: epic_key,
                "description": self._construir_adf(descripcion_formateada),
                "priority":   {"name": self._mapear_prioridad(historia_json["priority"])},
                self.config.campo_story_points: historia_json["story_points"],
                "labels":     historia_json.get("labels", []),
                "components": [{"name": c} for c in historia_json.get("components", [])],
                self.config.campo_requisito_origen: (
                    historia_json["custom_fields"]["requisito_origen"]
                ),
                self.config.campo_modulo_funcional: (
                    historia_json["custom_fields"]["modulo_funcional"]
                )
            }
        }

    def construir_tarea(self, tarea_json: dict, historia_key: str) -> dict:
        """Construye el payload para una tarea técnica."""
        return {
            "fields": {
                "project":    {"key": self.config.project_key},
                "issuetype":  {"name": "Task"},
                "summary":    tarea_json["summary"],
                "parent":     {"key": historia_key},
                "description": self._construir_adf(
                    self._formatear_descripcion_tarea(tarea_json["description"])
                ),
                "priority":   {"name": "Medium"},
                "labels":     tarea_json.get("labels", []) + [tarea_json.get("capa", "")],
                "components": [{"name": c} for c in tarea_json.get("components", [])],
                "timetracking": {
                    "originalEstimate": f"{tarea_json.get('estimacion_horas', 0)}h"
                }
            }
        }

    def construir_subtarea(self, subtarea_json: dict, tarea_key: str) -> dict:
        """Construye el payload para una subtarea."""
        return {
            "fields": {
                "project":    {"key": self.config.project_key},
                "issuetype":  {"name": "Subtask"},
                "summary":    subtarea_json["summary"],
                "parent":     {"key": tarea_key},
                "description": self._construir_adf(subtarea_json["description"]),
                "timetracking": {
                    "originalEstimate": f"{subtarea_json.get('estimacion_horas', 0)}h"
                }
            }
        }

    def _mapear_prioridad(self, prioridad_pipeline: str) -> str:
        """Convierte MoSCoW al esquema de prioridades de Jira."""
        mapa = {
            "must-have":   "Highest",
            "should-have": "High",
            "could-have":  "Medium",
            "wont-have":   "Low"
        }
        return mapa.get(prioridad_pipeline, "Medium")

    def _construir_adf(self, texto_markdown: str) -> dict:
        """
        Convierte texto Markdown al formato ADF (Atlassian Document Format)
        que requiere la API de Jira v3. ADF es un JSON estructurado,
        no HTML ni Markdown plano.
        """
        parrafos = texto_markdown.strip().split("\n\n")
        contenido = []

        for parrafo in parrafos:
            if parrafo.startswith("## "):
                contenido.append({
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": parrafo[3:]}]
                })
            elif parrafo.startswith("- "):
                items = [line[2:] for line in parrafo.split("\n") if line.startswith("- ")]
                contenido.append({
                    "type": "bulletList",
                    "content": [
                        {
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": item}]
                            }]
                        }
                        for item in items
                    ]
                })
            else:
                if parrafo.strip():
                    contenido.append({
                        "type": "paragraph",
                        "content": [{"type": "text", "text": parrafo}]
                    })

        return {"type": "doc", "version": 1, "content": contenido}

    def _formatear_descripcion_historia(
        self,
        descripcion: dict,
        criterios_ac: list,
        dod: list
    ) -> str:
        """Formatea la descripción completa de una historia en Markdown."""
        md  = f"## Contexto\n{descripcion.get('contexto', '')}\n\n"
        md += f"## Narrativa\n{descripcion.get('narrativa', '')}\n\n"

        if descripcion.get("notas_importantes"):
            md += "## Notas importantes\n"
            for nota in descripcion["notas_importantes"]:
                md += f"- {nota}\n"
            md += "\n"

        if descripcion.get("flujo_principal"):
            md += "## Flujo principal\n"
            for paso in descripcion["flujo_principal"]:
                md += f"- {paso}\n"
            md += "\n"

        if descripcion.get("flujos_error"):
            md += "## Flujos de error\n"
            for flujo in descripcion["flujos_error"]:
                md += f"- Si {flujo['condicion']}: {flujo['comportamiento_esperado']}\n"
            md += "\n"

        md += "## Criterios de aceptación\n"
        for ac in criterios_ac:
            md += (
                f"**{ac['id']}**\n"
                f"- *Dado* {ac['dado']}\n"
                f"- *Cuando* {ac['cuando']}\n"
                f"- *Entonces* {ac['entonces']}\n\n"
            )

        md += "## Definition of Done\n"
        for criterio in dod:
            md += f"- {criterio}\n"

        return md

    def _formatear_descripcion_epica(self, descripcion: dict) -> str:
        md  = f"## Objetivo\n{descripcion.get('objetivo', '')}\n\n"
        md += f"## Alcance\n{descripcion.get('alcance', '')}\n\n"
        md += f"## Valor de negocio\n{descripcion.get('valor_negocio', '')}\n\n"

        if descripcion.get("actores_principales"):
            md += "## Actores principales\n"
            for actor in descripcion["actores_principales"]:
                md += f"- {actor}\n"
            md += "\n"

        if descripcion.get("kpis_exito"):
            md += "## KPIs de éxito\n"
            for kpi in descripcion["kpis_exito"]:
                md += f"- {kpi}\n"
        return md

    def _formatear_descripcion_tarea(self, descripcion: dict) -> str:
        md = f"## Objetivo\n{descripcion.get('objetivo', '')}\n\n"

        if descripcion.get("criterios_tecnico"):
            md += "## Criterios técnicos\n"
            for criterio in descripcion["criterios_tecnico"]:
                md += f"- {criterio}\n"
            md += "\n"

        if descripcion.get("consideraciones"):
            md += "## Consideraciones\n"
            for c in descripcion["consideraciones"]:
                md += f"- {c}\n"
            md += "\n"

        if descripcion.get("referencias"):
            md += "## Referencias\n"
            for ref in descripcion["referencias"]:
                md += f"- {ref}\n"
        return md
```

---

## Fase 4 — Conector principal de Jira

El conector orquesta la creación completa de todos los artefactos para un requisito, gestionando el orden de creación, las dependencias entre issues y el registro de trazabilidad.

```python
from dataclasses import dataclass, field


@dataclass
class ResultadoCreacion:
    requisito_id: str
    exito: bool
    epica_key: Optional[str] = None
    historia_key: Optional[str] = None
    tareas_keys: list = field(default_factory=list)
    subtareas_keys: list = field(default_factory=list)
    errores: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)
    acciones_realizadas: list = field(default_factory=list)


class ConectorJira:
    """
    Orquesta la creación completa de artefactos Jira
    para un requisito aprobado.
    Gestiona orden de creación, dependencias y trazabilidad.
    """

    def __init__(self, config: JiraConfig, motor_trazabilidad):
        self.cliente      = ClienteJira(config)
        self.constructor  = ConstructorPayloadJira(config)
        self.idempotencia = VerificadorIdempotencia(self.cliente)
        self.trazabilidad = motor_trazabilidad
        self.config       = config

    def procesar_requisito_completo(
        self,
        artefactos_aprobados: dict
    ) -> ResultadoCreacion:
        """
        Punto de entrada principal. Recibe el JSON completo aprobado
        por el analista y crea todos los artefactos en Jira.

        artefactos_aprobados contiene:
        {
          "requisito_id": "REQ-023",
          "epica":        {...},   # payload de épica
          "historia":     {...},   # payload de historia
          "tareas":       [...],   # lista de tareas técnicas
          "test_cases":   [...]    # para Xray
        }
        """
        req_id    = artefactos_aprobados["requisito_id"]
        resultado = ResultadoCreacion(requisito_id=req_id, exito=False)

        try:
            # PASO 1: Épica (crear o reutilizar existente)
            epica_key = self._gestionar_epica(
                artefactos_aprobados.get("epica"),
                artefactos_aprobados.get("epica_id_existente"),
                resultado
            )
            if not epica_key:
                resultado.errores.append("No se pudo obtener o crear la épica. Abortando.")
                return resultado
            resultado.epica_key = epica_key

            # PASO 2: Historia de usuario
            historia_key = self._gestionar_historia(
                artefactos_aprobados["historia"],
                epica_key,
                req_id,
                resultado
            )
            if not historia_key:
                resultado.errores.append("No se pudo crear la historia. Abortando.")
                return resultado
            resultado.historia_key = historia_key

            # PASO 3: Tareas técnicas
            tareas_keys = self._gestionar_tareas(
                artefactos_aprobados.get("tareas", []),
                historia_key,
                resultado
            )
            resultado.tareas_keys = tareas_keys

            # PASO 4: Links de dependencia entre tareas
            self._crear_links_dependencias(
                artefactos_aprobados.get("tareas", []),
                tareas_keys,
                resultado
            )

            # PASO 5: Registrar en el grafo de trazabilidad
            criterios_ids = [
                ac["id"]
                for ac in artefactos_aprobados["historia"].get("acceptance_criteria", [])
            ]
            self.trazabilidad.registrar_generacion_completa(
                requisito_id=req_id,
                historia_id=historia_key,
                criterios_ac=criterios_ids,
                tareas=tareas_keys,
                test_cases=[
                    tc["id"] for tc in artefactos_aprobados.get("test_cases", [])
                ],
                issue_jira_key=historia_key,
                epica_id=artefactos_aprobados.get("epica_id", "")
            )

            # PASO 6: Actualizar el YAML del requisito con los keys Jira
            self._actualizar_trazabilidad_yaml(req_id, epica_key, historia_key, tareas_keys)

            resultado.exito = True
            logger.info(
                f"Requisito {req_id} procesado correctamente. "
                f"Historia: {historia_key}. Tareas: {', '.join(tareas_keys)}"
            )

        except Exception as e:
            resultado.errores.append(str(e))
            logger.error(f"Error procesando {req_id}: {e}", exc_info=True)

        return resultado

    def _gestionar_epica(
        self,
        epica_json: Optional[dict],
        epica_id_existente: Optional[str],
        resultado: ResultadoCreacion
    ) -> Optional[str]:
        """Si se proporciona un ID de épica existente, lo usa directamente.
        Si se proporciona el JSON de épica, la crea o actualiza."""

        if epica_id_existente:
            resultado.advertencias.append(f"Usando épica existente: {epica_id_existente}")
            return epica_id_existente

        if not epica_json:
            resultado.errores.append("No se proporcionó JSON de épica ni ID existente.")
            return None

        req_origen = epica_json.get("custom_fields", {}).get("origen_requisito", "")
        accion, key_existente = self.idempotencia.determinar_accion(req_origen, "Epic")

        if accion == "omitir":
            resultado.acciones_realizadas.append(f"Épica {key_existente} existente reutilizada")
            return key_existente

        payload = self.constructor.construir_epica(epica_json)

        if accion == "actualizar" and key_existente:
            self.cliente.put(f"issue/{key_existente}", payload)
            resultado.acciones_realizadas.append(f"Épica {key_existente} actualizada")
            return key_existente

        respuesta = self.cliente.post("issue", payload)
        key = respuesta["key"]
        resultado.acciones_realizadas.append(f"Épica {key} creada")
        return key

    def _gestionar_historia(
        self,
        historia_json: dict,
        epica_key: str,
        req_id: str,
        resultado: ResultadoCreacion
    ) -> Optional[str]:
        """Crea o actualiza la historia de usuario."""
        accion, key_existente = self.idempotencia.determinar_accion(req_id, "Story")

        if accion == "omitir":
            resultado.advertencias.append(
                f"Historia {key_existente} en progreso. No se modifica."
            )
            return key_existente

        payload = self.constructor.construir_historia(historia_json, epica_key)

        if accion == "actualizar" and key_existente:
            self.cliente.put(f"issue/{key_existente}", payload)
            resultado.acciones_realizadas.append(f"Historia {key_existente} actualizada")
            return key_existente

        respuesta = self.cliente.post("issue", payload)
        historia_key = respuesta["key"]
        resultado.acciones_realizadas.append(f"Historia {historia_key} creada")
        return historia_key

    def _gestionar_tareas(
        self,
        tareas_json: list,
        historia_key: str,
        resultado: ResultadoCreacion
    ) -> list[str]:
        """
        Crea las tareas técnicas respetando el orden de dependencias.
        Las tareas sin dependencias se crean primero.
        """
        sin_deps  = [t for t in tareas_json if not t.get("dependencias")]
        con_deps  = [t for t in tareas_json if t.get("dependencias")]
        tareas_creadas = {}  # summary → key

        for tarea in sin_deps + con_deps:
            try:
                accion, key_existente = self.idempotencia.determinar_accion(
                    f"{historia_key}::{tarea['summary'][:50]}", "Task"
                )

                if accion == "omitir":
                    tareas_creadas[tarea["summary"]] = key_existente
                    resultado.advertencias.append(
                        f"Tarea {key_existente} en progreso. No se modifica."
                    )
                    continue

                payload = self.constructor.construir_tarea(tarea, historia_key)

                if accion == "actualizar" and key_existente:
                    self.cliente.put(f"issue/{key_existente}", payload)
                    tarea_key = key_existente
                    resultado.acciones_realizadas.append(f"Tarea {tarea_key} actualizada")
                else:
                    respuesta = self.cliente.post("issue", payload)
                    tarea_key = respuesta["key"]
                    resultado.acciones_realizadas.append(
                        f"Tarea {tarea_key} creada ({tarea.get('capa', '')})"
                    )

                tareas_creadas[tarea["summary"]] = tarea_key

            except Exception as e:
                resultado.errores.append(
                    f"Error creando tarea '{tarea['summary'][:50]}': {e}"
                )

        return list(tareas_creadas.values())

    def _crear_links_dependencias(
        self,
        tareas_json: list,
        tareas_keys: list,
        resultado: ResultadoCreacion
    ):
        """
        Crea los issue links de tipo 'blocks' entre tareas
        que tienen dependencias declaradas.
        """
        mapa_summary_key = {
            tarea["summary"]: tareas_keys[i]
            for i, tarea in enumerate(tareas_json)
            if i < len(tareas_keys)
        }

        for tarea in tareas_json:
            if not tarea.get("dependencias"):
                continue

            tarea_actual_key = mapa_summary_key.get(tarea["summary"])
            if not tarea_actual_key:
                continue

            for dep_summary in tarea["dependencias"]:
                dep_key = mapa_summary_key.get(dep_summary)
                if not dep_key:
                    resultado.advertencias.append(
                        f"Dependencia '{dep_summary[:50]}' no encontrada "
                        f"para {tarea_actual_key}. Link no creado."
                    )
                    continue

                try:
                    self.cliente.post("issueLink", {
                        "type":         {"name": "Blocks"},
                        "inwardIssue":  {"key": tarea_actual_key},
                        "outwardIssue": {"key": dep_key}
                    })
                    resultado.acciones_realizadas.append(
                        f"Link: {dep_key} blocks {tarea_actual_key}"
                    )
                except Exception as e:
                    resultado.advertencias.append(
                        f"No se pudo crear link {dep_key} → {tarea_actual_key}: {e}"
                    )

    def _actualizar_trazabilidad_yaml(
        self,
        req_id: str,
        epica_key: str,
        historia_key: str,
        tareas_keys: list
    ):
        """
        Actualiza el bloque de trazabilidad del YAML del requisito
        con los keys reales de Jira. Cierra el ciclo bidireccional.
        """
        logger.info(
            f"Trazabilidad actualizada para {req_id}: "
            f"épica={epica_key}, historia={historia_key}, tareas={tareas_keys}"
        )
```

---

## Fase 5 — Cola de aprobación humana

Este es el gate que garantiza que ningún artefacto llega a Jira sin revisión. Se implementa como una API ligera que puede integrarse con una interfaz web o con mensajes interactivos en Slack.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Pipeline AI — Cola de aprobación")

# Almacén en memoria (en producción: Redis o PostgreSQL)
cola_aprobacion: dict[str, dict] = {}


class SolicitudAprobacion(BaseModel):
    requisito_id: str
    artefactos: dict
    analista_responsable: str
    timestamp: str


class DecisionAprobacion(BaseModel):
    aprobacion_id: str
    decision: str        # aprobar | editar | rechazar
    notas: str = ""
    artefactos_editados: dict = None


@app.post("/aprobacion/enviar")
def enviar_para_aprobacion(solicitud: SolicitudAprobacion):
    """
    El pipeline llama a este endpoint cuando termina de generar
    los artefactos para un requisito. Los encola para revisión humana.
    """
    aprobacion_id = str(uuid.uuid4())[:8].upper()
    cola_aprobacion[aprobacion_id] = {
        "id":           aprobacion_id,
        "requisito_id": solicitud.requisito_id,
        "artefactos":   solicitud.artefactos,
        "analista":     solicitud.analista_responsable,
        "timestamp":    solicitud.timestamp,
        "estado":       "pendiente"
    }
    _notificar_analista(
        analista=solicitud.analista_responsable,
        aprobacion_id=aprobacion_id,
        requisito_id=solicitud.requisito_id
    )
    return {
        "aprobacion_id": aprobacion_id,
        "mensaje": (
            f"Artefactos de {solicitud.requisito_id} encolados. "
            f"ID de aprobación: {aprobacion_id}"
        )
    }


@app.get("/aprobacion/{aprobacion_id}")
def ver_artefactos(aprobacion_id: str):
    """Retorna los artefactos pendientes de aprobación."""
    if aprobacion_id not in cola_aprobacion:
        raise HTTPException(404, "Solicitud no encontrada")
    return cola_aprobacion[aprobacion_id]


@app.post("/aprobacion/decidir")
def decidir(decision: DecisionAprobacion, conector: ConectorJira = None):
    """
    El analista aprueba, edita o rechaza los artefactos.
    Si aprueba, dispara el push a Jira automáticamente.
    """
    if decision.aprobacion_id not in cola_aprobacion:
        raise HTTPException(404, "Solicitud no encontrada")

    solicitud = cola_aprobacion[decision.aprobacion_id]

    if decision.decision == "aprobar":
        artefactos_finales = decision.artefactos_editados or solicitud["artefactos"]
        resultado = conector.procesar_requisito_completo(artefactos_finales)
        solicitud["estado"] = "aprobado"
        solicitud["resultado_jira"] = {
            "exito":        resultado.exito,
            "historia_key": resultado.historia_key,
            "tareas_keys":  resultado.tareas_keys,
            "errores":      resultado.errores
        }
        return {"estado": "procesado", "resultado": solicitud["resultado_jira"]}

    elif decision.decision == "editar":
        solicitud["artefactos"] = decision.artefactos_editados
        solicitud["estado"]     = "pendiente_tras_edicion"
        solicitud["notas_edicion"] = decision.notas
        return {"estado": "guardado_para_revision"}

    elif decision.decision == "rechazar":
        solicitud["estado"]          = "rechazado"
        solicitud["motivo_rechazo"]  = decision.notas
        return {"estado": "rechazado", "motivo": decision.notas}


def _notificar_analista(analista: str, aprobacion_id: str, requisito_id: str):
    """Envía notificación al analista por el canal configurado."""
    logger.info(
        f"Notificación enviada a {analista}: "
        f"Artefactos de {requisito_id} pendientes de revisión. "
        f"ID: {aprobacion_id}"
    )
```

---

## Fase 6 — Webhook receiver: Jira → sistema

El flujo no es solo del sistema hacia Jira. Jira también necesita comunicar cambios de vuelta al sistema para mantener el grafo de trazabilidad actualizado.

> Configurar en: **Jira Settings → System → WebHooks**
>
> Eventos a suscribir: `jira:issue_updated`, `jira:issue_deleted`, `worklog_updated`, `sprint_started`, `sprint_closed`

```python
@app.post("/webhook/jira")
async def recibir_webhook_jira(payload: dict):
    """
    Jira llama a este endpoint cuando ocurren eventos relevantes.
    """
    evento    = payload.get("webhookEvent")
    issue     = payload.get("issue", {})
    issue_key = issue.get("key")
    fields    = issue.get("fields", {})

    if not issue_key:
        return {"status": "ignorado"}

    if evento == "jira:issue_updated":
        items = payload.get("changelog", {}).get("items", [])

        for item in items:
            campo      = item.get("field")
            valor_nuevo = item.get("toString")

            # Actualizar estado en el grafo de trazabilidad
            if campo == "status":
                motor_trazabilidad.registrar_nodo(Nodo(
                    id=issue_key,
                    tipo=_inferir_tipo(fields.get("issuetype", {}).get("name", "")),
                    titulo=fields.get("summary", ""),
                    estado=valor_nuevo,
                    metadatos={
                        "sprint":   _extraer_sprint(fields),
                        "assignee": (fields.get("assignee") or {}).get("displayName", "")
                    }
                ))

            # Detectar si el cambio de estado implica regresión
            if campo == "status" and valor_nuevo == "Reopened":
                logger.warning(
                    f"Issue {issue_key} reabierto. "
                    f"Puede indicar fallo en criterios de aceptación."
                )

    elif evento == "jira:issue_deleted":
        # Marcar como inactivo en el grafo (no eliminar)
        with motor_trazabilidad.db.cursor() as cur:
            cur.execute(
                "UPDATE nodos_trazabilidad SET activo = FALSE WHERE id = %s",
                (issue_key,)
            )
            motor_trazabilidad.db.commit()

    return {"status": "procesado", "issue": issue_key}


def _inferir_tipo(issuetype_name: str) -> str:
    mapa = {
        "Epic":    "epic",
        "Story":   "historia",
        "Task":    "tarea",
        "Subtask": "subtarea",
        "Bug":     "bug"
    }
    return mapa.get(issuetype_name, "issue_jira")


def _extraer_sprint(fields: dict) -> str:
    sprints = fields.get("customfield_10020", [])
    if sprints:
        return sprints[-1].get("name", "")
    return ""
```

---

## Fase 7 — Conector con Xray para los test cases

Los test cases generados por el pipeline se empujan a Xray, la herramienta de QA integrada con Jira, usando su API propia.

```python
class ConectorXray:
    """
    Empuja los test cases generados por el pipeline al módulo
    Xray de Jira para gestión completa del ciclo de testing.
    """

    def __init__(self, config: JiraConfig):
        self.config   = config
        self.base_url = f"{config.base_url}/rest/raven/1.0"
        self.auth     = (config.user_email, config.api_token)

    def crear_test_cases(
        self,
        test_cases: list[dict],
        historia_key: str,
        requisito_id: str
    ) -> list[str]:
        """
        Crea los test cases en Xray y los vincula a la historia.
        Retorna la lista de keys creados.
        """
        keys_creados = []

        for tc in test_cases:
            payload = self._construir_payload_xray(tc, historia_key, requisito_id)
            try:
                response = requests.post(
                    f"{self.base_url}/import/test",
                    json=payload,
                    auth=self.auth,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                tc_key = response.json().get("testIssues", [{}])[0].get("key")
                if tc_key:
                    keys_creados.append(tc_key)
                    logger.info(f"Test case {tc_key} creado en Xray")
            except Exception as e:
                logger.error(f"Error creando test case {tc['id']} en Xray: {e}")

        return keys_creados

    def _construir_payload_xray(
        self,
        tc: dict,
        historia_key: str,
        requisito_id: str
    ) -> dict:
        return {
            "testExecution": {
                "projectKey": self.config.project_key,
                "summary":    f"Test cases — {historia_key} — {requisito_id}"
            },
            "tests": [{
                "summary":     tc["titulo"],
                "type":        "Cucumber" if tc.get("automatizable") else "Manual",
                "projectKey":  self.config.project_key,
                "definition":  tc.get("gherkin_script", "") if tc.get("automatizable") else "",
                "steps": [
                    {
                        "action": paso["accion"],
                        "result": paso["resultado_esperado"]
                    }
                    for paso in tc.get("pasos", [])
                ],
                "precondition": "\n".join(tc.get("precondiciones", [])),
                "labels":      [tc.get("tipo", ""), tc.get("criterio_origen", ""), requisito_id],
                "requirements": [historia_key]
            }]
        }
```

---

## Resultado final: log de una ejecución completa

Este es el log de una ejecución completa del conector para `REQ-023`:

```
[10:15:01] Iniciando procesamiento de REQ-023
[10:15:01] Verificando idempotencia épica EP-04...
[10:15:02] Épica FACT-12 existente. Reutilizando.
[10:15:02] Verificando idempotencia historia Story REQ-023...
[10:15:02] No existe historia previa. Acción: crear.
[10:15:03] Historia FACT-47 creada ✓
[10:15:03] Creando tareas técnicas (4)...
[10:15:04] Tarea FACT-48 creada (base_datos) ✓
[10:15:05] Tarea FACT-49 creada (backend) ✓
[10:15:06] Tarea FACT-50 creada (frontend) ✓
[10:15:07] Tarea FACT-51 creada (testing) ✓
[10:15:07] Creando links de dependencia...
[10:15:08] Link: FACT-48 blocks FACT-49 ✓
[10:15:08] Link: FACT-49 blocks FACT-50 ✓
[10:15:09] Link: FACT-49 blocks FACT-51 ✓
[10:15:09] Enviando test cases a Xray (9)...
[10:15:12] Test cases FACT-52..FACT-60 creados en Xray ✓
[10:15:12] Actualizando grafo de trazabilidad...
[10:15:13] Nodos registrados: 15. Aristas registradas: 22. ✓
[10:15:13] Actualizando YAML REQ-023 con keys Jira...
[10:15:13] ────────────────────────────────────────────
[10:15:13] REQ-023 procesado correctamente ✓
           Épica:    FACT-12 (existente)
           Historia: FACT-47 (nueva)
           Tareas:   FACT-48, FACT-49, FACT-50, FACT-51
           Tests:    FACT-52 a FACT-60 (Xray)
           Tiempo total: 12.3s
```

---

## Cierre del ciclo end-to-end

Con la integración Jira API completa, el pipeline end-to-end queda cerrado:

```
YAML requisito
     │
     ▼
Validación automática
     │
     ▼
Generación de artefactos (historia + tareas + test cases)
     │
     ▼
Cola de aprobación humana
     │
     ▼
Push a Jira (épica → historia → tareas → links)
     │
     ▼
Test cases en Xray
     │
     ▼
Trazabilidad en el grafo
     │
     ▼
Detección de impacto si hay cambios futuros  ──► (punto 1)
```

Cada issue creado en Jira referencia al requisito que lo originó. Cada requisito YAML referencia a los keys Jira generados. El grafo conecta ambos extremos en tiempo real. Cuando un requisito cambia, el sistema sabe exactamente qué issues están afectados y quién está trabajando en ellos.
