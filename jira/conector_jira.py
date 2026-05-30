# jira/conector_jira.py
"""
Conector principal de Jira API.
Gestiona la creación idempotente de épicas, historias,
tareas técnicas y links de dependencia.

Punto 10 del modelo operativo AI-ready.
"""

import json
import time
import logging
import requests
from dataclasses import dataclass, field
from typing import Optional

log = logging.getLogger("jira_conector")


@dataclass
class ResultadoCreacion:
    requisito_id: str
    exito: bool = False
    epica_key: Optional[str] = None
    historia_key: Optional[str] = None
    tareas_keys: list = field(default_factory=list)
    errores: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)
    acciones_realizadas: list = field(default_factory=list)


class ClienteJira:
    """Cliente base para la API REST de Jira v3."""

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.user_email, config.api_token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self._ultima_llamada = 0

    def _respetar_rate_limit(self):
        ahora = time.time() * 1000
        diferencia = ahora - self._ultima_llamada
        pausa = self.config.pausa_entre_llamadas_ms if hasattr(self.config, 'pausa_entre_llamadas_ms') else 200
        if diferencia < pausa:
            time.sleep((pausa - diferencia) / 1000)
        self._ultima_llamada = time.time() * 1000

    def _llamar(self, metodo: str, endpoint: str, payload=None, params=None) -> dict:
        url = f"{self.config.base_url}/rest/api/3/{endpoint}"
        max_reintentos = 3

        for intento in range(max_reintentos):
            self._respetar_rate_limit()
            try:
                response = self.session.request(
                    method=metodo, url=url, json=payload,
                    params=params, timeout=30
                )
                if response.status_code == 429:
                    espera = int(response.headers.get("Retry-After", 60))
                    log.warning(f"Rate limit. Esperando {espera}s.")
                    time.sleep(espera)
                    continue
                if response.status_code >= 500:
                    time.sleep(2 ** intento * 2)
                    continue
                if response.status_code >= 400:
                    log.error(f"Error {response.status_code}: {response.text[:200]}")
                    response.raise_for_status()
                if response.status_code == 204:
                    return {}
                return response.json()
            except requests.exceptions.Timeout:
                if intento >= max_reintentos - 1:
                    raise

        raise RuntimeError(f"Máximo de reintentos para {metodo} {endpoint}")

    def get(self, endpoint: str, params=None) -> dict:
        return self._llamar("GET", endpoint, params=params)

    def post(self, endpoint: str, payload: dict) -> dict:
        return self._llamar("POST", endpoint, payload=payload)

    def put(self, endpoint: str, payload: dict) -> dict:
        return self._llamar("PUT", endpoint, payload=payload)


class VerificadorIdempotencia:
    """Verifica si los artefactos ya existen en Jira."""

    def __init__(self, cliente: ClienteJira):
        self.cliente = cliente

    def buscar_issue_existente(self, requisito_id: str, tipo_issue: str) -> Optional[dict]:
        jql = (
            f"project = {self.cliente.config.project_key} "
            f"AND issuetype = '{tipo_issue}' "
            f"AND '{self.cliente.config.campo_requisito_origen}' ~ '{requisito_id}' "
            f"AND statusCategory != Done"
        )
        resultado = self.cliente.get("search", params={
            "jql": jql,
            "fields": "summary,status,issuetype",
            "maxResults": 5
        })
        issues = resultado.get("issues", [])
        return issues[0] if issues else None

    def determinar_accion(self, requisito_id: str, tipo_issue: str) -> tuple[str, Optional[str]]:
        issue = self.buscar_issue_existente(requisito_id, tipo_issue)
        if issue is None:
            return "crear", None
        estado = issue["fields"]["status"]["statusCategory"]["key"]
        if estado in ("indeterminate", "done"):
            return "omitir", issue["key"]
        return "actualizar", issue["key"]


class ConstructorPayloadJira:
    """Convierte los artefactos generados al formato de la API Jira v3."""

    def __init__(self, config):
        self.config = config

    def construir_historia(self, historia_json: dict, epic_key: str) -> dict:
        return {
            "fields": {
                "project": {"key": self.config.project_key},
                "issuetype": {"name": "Story"},
                "summary": historia_json.get("summary", "Historia sin título"),
                self.config.campo_epic_link: epic_key,
                "description": self._texto_a_adf(
                    self._formatear_historia(historia_json)
                ),
                "priority": {"name": self._mapear_prioridad(historia_json.get("priority", ""))},
                self.config.campo_story_points: historia_json.get("story_points", 3),
                "labels": historia_json.get("labels", []),
                "components": [{"name": c} for c in historia_json.get("components", [])],
                self.config.campo_requisito_origen: (
                    historia_json.get("custom_fields", {}).get("requisito_origen", "")
                ),
            }
        }

    def construir_tarea(self, tarea_json: dict, historia_key: str) -> dict:
        return {
            "fields": {
                "project": {"key": self.config.project_key},
                "issuetype": {"name": "Task"},
                "summary": tarea_json.get("summary", "Tarea sin título"),
                "parent": {"key": historia_key},
                "description": self._texto_a_adf(
                    self._formatear_tarea(tarea_json.get("description", {}))
                ),
                "labels": tarea_json.get("labels", []),
                "components": [{"name": c} for c in tarea_json.get("components", [])],
                "timetracking": {
                    "originalEstimate": f"{tarea_json.get('estimacion_horas', 0)}h"
                }
            }
        }

    def _mapear_prioridad(self, prioridad: str) -> str:
        return {
            "must-have": "Highest", "should-have": "High",
            "could-have": "Medium", "wont-have": "Low"
        }.get(prioridad, "Medium")

    def _formatear_historia(self, h: dict) -> str:
        desc = h.get("description", {})
        md = f"## Contexto\n{desc.get('contexto', '')}\n\n"
        md += f"## Narrativa\n{desc.get('narrativa', '')}\n\n"
        acs = h.get("acceptance_criteria", [])
        if acs:
            md += "## Criterios de aceptación\n"
            for ac in acs:
                md += (f"**{ac.get('id','')}**\n"
                       f"- *Dado* {ac.get('dado','')}\n"
                       f"- *Cuando* {ac.get('cuando','')}\n"
                       f"- *Entonces* {ac.get('entonces','')}\n\n")
        dod = h.get("definition_of_done", [])
        if dod:
            md += "## Definition of Done\n" + "\n".join(f"- {d}" for d in dod)
        return md

    def _formatear_tarea(self, desc: dict) -> str:
        md = f"## Objetivo\n{desc.get('objetivo', '')}\n\n"
        criterios = desc.get("criterios_tecnico", [])
        if criterios:
            md += "## Criterios técnicos\n" + "\n".join(f"- {c}" for c in criterios)
        return md

    def _texto_a_adf(self, texto: str) -> dict:
        """Convierte Markdown básico a Atlassian Document Format."""
        parrafos = texto.strip().split("\n\n")
        contenido = []
        for p in parrafos:
            if p.startswith("## "):
                contenido.append({
                    "type": "heading", "attrs": {"level": 2},
                    "content": [{"type": "text", "text": p[3:]}]
                })
            elif p.startswith("- "):
                items = [l[2:] for l in p.split("\n") if l.startswith("- ")]
                contenido.append({
                    "type": "bulletList",
                    "content": [
                        {"type": "listItem", "content": [
                            {"type": "paragraph", "content": [{"type": "text", "text": i}]}
                        ]}
                        for i in items
                    ]
                })
            elif p.strip():
                contenido.append({
                    "type": "paragraph",
                    "content": [{"type": "text", "text": p}]
                })
        return {"type": "doc", "version": 1, "content": contenido}


class ConectorJira:
    """Orquesta la creación completa de artefactos Jira para un requisito aprobado."""

    def __init__(self, config, motor_trazabilidad):
        self.cliente       = ClienteJira(config)
        self.constructor   = ConstructorPayloadJira(config)
        self.idempotencia  = VerificadorIdempotencia(self.cliente)
        self.trazabilidad  = motor_trazabilidad
        self.config        = config

    def procesar_requisito_completo(self, artefactos_aprobados: dict) -> ResultadoCreacion:
        req_id = artefactos_aprobados["requisito_id"]
        resultado = ResultadoCreacion(requisito_id=req_id)

        try:
            # Épica
            epica_key = self._gestionar_epica(
                artefactos_aprobados.get("epica_id_existente"), resultado
            )
            if not epica_key:
                resultado.errores.append("No se pudo obtener la épica.")
                return resultado
            resultado.epica_key = epica_key

            # Historia
            historia_key = self._gestionar_historia(
                artefactos_aprobados.get("historia", {}),
                epica_key, req_id, resultado
            )
            if not historia_key:
                resultado.errores.append("No se pudo crear la historia.")
                return resultado
            resultado.historia_key = historia_key

            # Tareas
            tareas_keys = self._gestionar_tareas(
                artefactos_aprobados.get("tareas", []),
                historia_key, resultado
            )
            resultado.tareas_keys = tareas_keys

            # Links de dependencia
            self._crear_links_dependencias(
                artefactos_aprobados.get("tareas", []),
                tareas_keys, resultado
            )

            resultado.exito = True
            log.info(f"Requisito {req_id} procesado. Historia: {historia_key}")

        except Exception as e:
            resultado.errores.append(str(e))
            log.error(f"Error procesando {req_id}: {e}")

        return resultado

    def _gestionar_epica(self, epica_id_existente: Optional[str], resultado) -> Optional[str]:
        if epica_id_existente:
            resultado.advertencias.append(f"Usando épica existente: {epica_id_existente}")
            return epica_id_existente
        return None  # En producción: crear épica si no existe

    def _gestionar_historia(self, historia_json, epica_key, req_id, resultado) -> Optional[str]:
        accion, key_existente = self.idempotencia.determinar_accion(req_id, "Story")

        if accion == "omitir":
            resultado.advertencias.append(f"Historia {key_existente} en progreso. No se modifica.")
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

    def _gestionar_tareas(self, tareas_json, historia_key, resultado) -> list[str]:
        tareas_creadas = {}
        sin_deps = [t for t in tareas_json if not t.get("dependencias")]
        con_deps = [t for t in tareas_json if t.get("dependencias")]

        for tarea in sin_deps + con_deps:
            try:
                payload = self.constructor.construir_tarea(tarea, historia_key)
                respuesta = self.cliente.post("issue", payload)
                tarea_key = respuesta["key"]
                tareas_creadas[tarea["summary"]] = tarea_key
                resultado.acciones_realizadas.append(
                    f"Tarea {tarea_key} creada ({tarea.get('capa', '')})"
                )
            except Exception as e:
                resultado.errores.append(f"Error en tarea '{tarea.get('summary','')[:40]}': {e}")

        return list(tareas_creadas.values())

    def _crear_links_dependencias(self, tareas_json, tareas_keys, resultado):
        mapa = {}
        for i, tarea in enumerate(tareas_json):
            if i < len(tareas_keys):
                mapa[tarea["summary"]] = tareas_keys[i]

        for tarea in tareas_json:
            tarea_key = mapa.get(tarea["summary"])
            if not tarea_key:
                continue
            for dep_summary in tarea.get("dependencias", []):
                dep_key = mapa.get(dep_summary)
                if not dep_key:
                    resultado.advertencias.append(f"Dependencia '{dep_summary[:40]}' no encontrada")
                    continue
                try:
                    self.cliente.post("issueLink", {
                        "type": {"name": "Blocks"},
                        "inwardIssue": {"key": tarea_key},
                        "outwardIssue": {"key": dep_key}
                    })
                    resultado.acciones_realizadas.append(f"Link: {dep_key} blocks {tarea_key}")
                except Exception as e:
                    resultado.advertencias.append(f"Link {dep_key}→{tarea_key} falló: {e}")
