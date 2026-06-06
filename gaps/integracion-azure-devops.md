# Integración con Azure DevOps

## Por qué este punto merece desarrollo propio

El modelo operativo está construido con Jira como destino de artefactos porque es la herramienta más extendida en equipos de análisis funcional. Sin embargo, una parte significativa de organizaciones opera con el stack Microsoft: Azure DevOps como gestor de trabajo, Azure Repos como repositorio de código, y GitHub Copilot o Azure OpenAI Service como capa de IA. Para esas organizaciones, el modelo es completamente válido en su arquitectura conceptual, en la plantilla YAML, en el glosario, en los prompts de generación y en el pipeline de validación. Lo único que cambia es la capa de integración: el conector del punto 10 que empuja los artefactos generados al sistema de destino.

Este documento desarrolla esa capa de integración específicamente para Azure DevOps, manteniendo paridad funcional con la integración Jira documentada en el punto 10 del modelo y señalando explícitamente las diferencias conceptuales entre ambos sistemas que afectan al diseño del conector.

---

## Diferencias conceptuales entre Jira y Azure DevOps

Antes del código, es necesario entender cómo Azure DevOps modela el trabajo de forma diferente a Jira. Ignorar estas diferencias produce un conector que fuerza los conceptos de Jira sobre ADO, generando work items mal tipados y una jerarquía que el equipo no reconoce como suya.

### Jerarquía de work items

Azure DevOps usa un modelo jerárquico de tres niveles que varía según el proceso seleccionado al crear el proyecto. Los tres procesos disponibles son Agile, Scrum y CMMI, y cada uno nombra los tipos de work item de forma diferente aunque la estructura sea equivalente.

```
PROCESO AGILE               PROCESO SCRUM               PROCESO CMMI
─────────────────           ─────────────────           ─────────────────
Epic                        Epic                        Epic
  └── Feature               └── Feature                   └── Feature
        └── User Story            └── Product Backlog         └── Requirement
              └── Task                  Item (PBI)                  └── Task
                    └── (sin              └── Task                        └── (sin
                         subtask)               └── (sin                       subtask
                                                     subtask                   nativo)
                                                     nativo)
```

La equivalencia con los artefactos generados por el pipeline es la siguiente:

| Artefacto del pipeline | Jira | ADO (Agile) | ADO (Scrum) |
|---|---|---|---|
| Épica funcional | Epic | Epic | Epic |
| Módulo funcional | Epic padre | Feature | Feature |
| Historia de usuario | Story | User Story | Product Backlog Item |
| Tarea técnica | Task | Task | Task |
| Subtarea | Subtask | (no existe de forma nativa) | (no existe de forma nativa) |
| Test case | Xray/Zephyr | Test Case (nativo) | Test Case (nativo) |

Dos diferencias estructurales importantes:

**ADO tiene una capa adicional: la Feature.** Entre la épica y la historia existe el nivel Feature, que no tiene equivalente directo en la nomenclatura del modelo operativo. En la práctica, la Feature en ADO cumple el mismo rol que la épica funcional del pipeline, y la Epic en ADO agrupa Features de alto nivel. El conector debe crear la Feature como destino directo de las historias y reservar la Epic para agrupaciones de módulos relacionados.

**ADO no tiene subtareas nativas en los procesos Agile y Scrum.** Las tareas no pueden tener hijos en esos procesos. Las subtareas del pipeline se convierten en Tasks adicionales vinculadas a la historia padre, no a la tarea. Para los equipos que usan el proceso CMMI existe un tipo Subtask, pero es el menos frecuente en organizaciones de producto.

### El campo Area Path y el campo Iteration Path

ADO no tiene el concepto de componente de la misma forma que Jira. En su lugar, usa dos campos jerárquicos propios:

**Area Path** organiza el trabajo por equipo o dominio funcional. Equivale aproximadamente a los componentes de Jira. Un work item asignado a `Proyecto\Módulo Facturación` es visible para el equipo responsable de ese módulo.

**Iteration Path** (llamado Sprint en la interfaz) indica a qué sprint o iteración pertenece el work item. En Jira, el sprint se gestiona desde los campos de la board. En ADO, el Iteration Path es un campo de primer nivel del work item.

El conector debe mapear el campo `components` del JSON generado por el pipeline al Area Path correcto de ADO, y respetar el Iteration Path del equipo si el requisito lleva información de sprint.

### El sistema de vinculación entre work items

ADO usa un modelo de vínculos tipados entre work items que es más explícito que los issue links de Jira. Los tipos de vínculo más relevantes para el pipeline son:

| Tipo de vínculo | Dirección | Uso en el pipeline |
|---|---|---|
| `System.LinkTypes.Hierarchy-Forward` | padre → hijo | Conectar Feature → User Story → Task |
| `Microsoft.VSTS.Common.Affects-Forward` | A afecta a B | Dependencias entre tareas del mismo tipo |
| `Microsoft.VSTS.Common.TestedBy-Forward` | historia → test case | Vincular test cases a historias |
| `System.LinkTypes.Related` | bidireccional | Requisitos relacionados sin jerarquía |

La relación padre-hijo en ADO se establece mediante el campo `parent` al crear el work item, no mediante un vínculo explícito posterior. Esto significa que la historia debe crearse con referencia al ID de la Feature padre, y las tareas con referencia al ID de la historia. El orden de creación en el conector no es opcional: primero Feature, luego User Story, luego Tasks.

---

## Autenticación y cliente base

ADO usa dos mecanismos de autenticación. Para integraciones servidor-a-servidor como el pipeline, el recomendado es el Personal Access Token (PAT) con alcance limitado a Work Items (lectura y escritura) y Test Management (lectura y escritura). OAuth 2.0 con service principal es la alternativa para organizaciones con política de seguridad más estricta que prohíbe PATs personales.

```python
# config_ado.py

import os
from dataclasses import dataclass, field

@dataclass
class ADOConfig:
    organization: str = os.getenv("ADO_ORGANIZATION", "")
    # Nombre de la organización: https://dev.azure.com/{organization}

    project: str = os.getenv("ADO_PROJECT", "")
    # Nombre del proyecto dentro de la organización

    pat: str = os.getenv("ADO_PAT", "")
    # Personal Access Token con scopes:
    #   - Work Items: Read & Write
    #   - Test Management: Read & Write
    #   - Build: Read (para vinculación con pipelines CI/CD)

    proceso: str = os.getenv("ADO_PROCESO", "Agile")
    # Agile │ Scrum │ CMMI — determina los tipos de work item disponibles

    area_path_base: str = os.getenv("ADO_AREA_PATH", "")
    # Ejemplo: "MiProyecto\Backend"
    # Los work items se crean bajo este area path por defecto

    iteration_path_base: str = os.getenv("ADO_ITERATION_PATH", "")
    # Ejemplo: "MiProyecto\Sprint 1"
    # Iteration path por defecto para work items sin sprint asignado

    api_version: str = "7.1"
    # Versión de la REST API. 7.1 es la más reciente y estable a mayo 2025

    max_reintentos: int = 3
    pausa_entre_llamadas_ms: int = 300

    # Mapeo de tipos de work item según el proceso
    @property
    def tipo_historia(self) -> str:
        return {
            "Agile": "User Story",
            "Scrum": "Product Backlog Item",
            "CMMI": "Requirement"
        }.get(self.proceso, "User Story")

    @property
    def tipo_feature(self) -> str:
        return "Feature"  # Igual en los tres procesos

    @property
    def tipo_epic(self) -> str:
        return "Epic"  # Igual en los tres procesos

    @property
    def tipo_tarea(self) -> str:
        return "Task"  # Igual en los tres procesos

    @property
    def tipo_test_case(self) -> str:
        return "Test Case"  # Nativo en ADO, igual en los tres procesos

    def base_url(self) -> str:
        return f"https://dev.azure.com/{self.organization}/{self.project}"

    def validar(self) -> list[str]:
        errores = []
        if not self.organization:
            errores.append("ADO_ORGANIZATION no configurada")
        if not self.project:
            errores.append("ADO_PROJECT no configurada")
        if not self.pat:
            errores.append("ADO_PAT no configurado")
        if self.proceso not in ("Agile", "Scrum", "CMMI"):
            errores.append(
                f"ADO_PROCESO '{self.proceso}' no válido. "
                f"Valores: Agile │ Scrum │ CMMI"
            )
        return errores
```

```python
# cliente_ado.py

import requests
import base64
import time
import logging
from typing import Optional

log = logging.getLogger("pipeline.ado")


class ClienteADO:
    """
    Cliente base para la REST API de Azure DevOps.
    Gestiona autenticación PAT, rate limiting y reintentos.
    """

    def __init__(self, config: ADOConfig):
        self.config = config
        self.session = requests.Session()

        # ADO usa Basic Auth con el PAT como contraseña
        # El usuario puede ser cualquier cadena; por convención se usa vacío
        credencial = base64.b64encode(
            f":{config.pat}".encode("ascii")
        ).decode("ascii")
        self.session.headers.update({
            "Authorization": f"Basic {credencial}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        self._ultima_llamada = 0.0

    @property
    def _url_wit(self) -> str:
        """URL base para la Work Items Tracking API."""
        return (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit"
        )

    @property
    def _url_test(self) -> str:
        """URL base para la Test Management API."""
        return (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/test"
        )

    def _respetar_rate_limit(self):
        ahora = time.time() * 1000
        diferencia = ahora - self._ultima_llamada
        pausa = self.config.pausa_entre_llamadas_ms
        if diferencia < pausa:
            time.sleep((pausa - diferencia) / 1000)
        self._ultima_llamada = time.time() * 1000

    def _llamar(
        self,
        metodo: str,
        url: str,
        payload=None,
        params: dict = None,
        content_type: str = "application/json"
    ) -> dict:
        """
        Ejecuta una llamada HTTP con reintentos y backoff exponencial.
        ADO devuelve 429 con cabecera Retry-After cuando se supera el límite.
        """
        # ADO usa content-type especial para PATCH de work items
        headers = {}
        if content_type == "json-patch":
            headers["Content-Type"] = (
                "application/json-patch+json"
            )

        intentos = 0
        while intentos < self.config.max_reintentos:
            self._respetar_rate_limit()
            try:
                response = self.session.request(
                    method=metodo,
                    url=url,
                    json=payload,
                    params={
                        **(params or {}),
                        "api-version": self.config.api_version
                    },
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 429:
                    espera = int(
                        response.headers.get("Retry-After", 60)
                    )
                    log.warning(f"Rate limit ADO. Esperando {espera}s.")
                    time.sleep(espera)
                    intentos += 1
                    continue

                if response.status_code >= 500:
                    espera = (2 ** intentos) * 2
                    log.warning(
                        f"Error {response.status_code} ADO. "
                        f"Reintento {intentos + 1} en {espera}s."
                    )
                    time.sleep(espera)
                    intentos += 1
                    continue

                if response.status_code >= 400:
                    log.error(
                        f"Error {response.status_code} en {metodo} {url}: "
                        f"{response.text}"
                    )
                    response.raise_for_status()

                if response.status_code == 204:
                    return {}

                return response.json()

            except requests.exceptions.Timeout:
                intentos += 1
                if intentos >= self.config.max_reintentos:
                    raise RuntimeError(
                        f"Timeout en {metodo} {url} "
                        f"tras {self.config.max_reintentos} intentos"
                    )
                time.sleep(2 ** intentos)

        raise RuntimeError(
            f"Máximo de reintentos alcanzado para {metodo} {url}"
        )

    def get(self, endpoint: str, params: dict = None) -> dict:
        return self._llamar("GET", endpoint, params=params)

    def post(self, endpoint: str, payload) -> dict:
        return self._llamar("POST", endpoint, payload=payload)

    def patch_wit(self, url: str, operaciones: list) -> dict:
        """
        PATCH especial para actualizar work items.
        ADO requiere JSON Patch (RFC 6902) para actualizaciones de work items.
        """
        return self._llamar(
            "PATCH", url, payload=operaciones,
            content_type="json-patch"
        )
```

---

## Constructor de payloads para ADO

ADO usa un formato de creación y actualización de work items diferente a Jira. Los work items se crean mediante una operación PATCH con un array de operaciones JSON Patch, donde cada campo es una operación `add` sobre su ruta específica.

```python
# constructor_payload_ado.py

from dataclasses import dataclass
from typing import Optional


class ConstructorPayloadADO:
    """
    Convierte los artefactos generados por el pipeline al formato
    de operaciones JSON Patch que requiere la API de Azure DevOps.
    """

    def __init__(self, config: ADOConfig):
        self.config = config

    def _op(self, path: str, value) -> dict:
        """Construye una operación JSON Patch de tipo 'add'."""
        return {"op": "add", "path": path, "value": value}

    def _campo(self, nombre: str, valor) -> dict:
        """Operación para un campo estándar de work item."""
        return self._op(f"/fields/{nombre}", valor)

    def _relacion(
        self,
        tipo: str,
        url_destino: str,
        atributos: dict = None
    ) -> dict:
        """Operación para añadir una relación entre work items."""
        return self._op("/relations/-", {
            "rel": tipo,
            "url": url_destino,
            "attributes": atributos or {}
        })

    # ── ÉPICA ──────────────────────────────────────────────────────

    def construir_epic(self, epica_json: dict) -> list[dict]:
        """
        Construye las operaciones JSON Patch para crear una Epic en ADO.
        En ADO, la Epic agrupa Features de alto nivel (módulos completos).
        """
        desc = epica_json.get("description", {})
        descripcion_html = self._markdown_a_html(
            self._formatear_descripcion_epica(desc)
        )

        operaciones = [
            self._campo("System.Title", epica_json["summary"]),
            self._campo("System.Description", descripcion_html),
            self._campo(
                "System.AreaPath",
                self._area_path(epica_json.get("components", []))
            ),
            self._campo(
                "Microsoft.VSTS.Common.Priority",
                self._mapear_prioridad_numero(epica_json.get("priority", ""))
            ),
            self._campo(
                "System.Tags",
                "; ".join(epica_json.get("labels", []))
            ),
            # Campo personalizado: ID del requisito origen
            self._campo(
                "Custom.RequisitoOrigen",
                epica_json.get("custom_fields", {}).get(
                    "origen_requisito", ""
                )
            ),
        ]

        return operaciones

    # ── FEATURE ─────────────────────────────────────────────────────

    def construir_feature(
        self,
        epica_json: dict,
        epic_id: int
    ) -> list[dict]:
        """
        Construye las operaciones para crear una Feature en ADO.
        La Feature es el equivalente directo de la épica del pipeline:
        agrupa las historias de un módulo funcional.
        El epic_id es el ID numérico de la Epic padre ya creada en ADO.
        """
        desc = epica_json.get("description", {})
        descripcion_html = self._markdown_a_html(
            self._formatear_descripcion_epica(desc)
        )

        url_epic = (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems/{epic_id}"
        )

        operaciones = [
            self._campo("System.Title", epica_json.get("epic_name", epica_json["summary"])),
            self._campo("System.Description", descripcion_html),
            self._campo(
                "System.AreaPath",
                self._area_path(epica_json.get("components", []))
            ),
            self._campo(
                "Microsoft.VSTS.Common.Priority",
                self._mapear_prioridad_numero(epica_json.get("priority", ""))
            ),
            self._campo(
                "System.Tags",
                "; ".join(epica_json.get("labels", []))
            ),
            self._campo(
                "Custom.ModuloFuncional",
                epica_json.get("custom_fields", {}).get("modulo_funcional", "")
            ),
            # Relación padre: Epic → Feature
            self._relacion(
                "System.LinkTypes.Hierarchy-Reverse",
                url_epic,
                {"comment": "Épica funcional padre"}
            )
        ]

        return operaciones

    # ── HISTORIA DE USUARIO ─────────────────────────────────────────

    def construir_historia(
        self,
        historia_json: dict,
        feature_id: int
    ) -> list[dict]:
        """
        Construye las operaciones para crear una User Story (o PBI) en ADO.
        feature_id es el ID numérico de la Feature padre.
        """
        descripcion_html = self._markdown_a_html(
            self._formatear_descripcion_historia(
                historia_json.get("description", {}),
                historia_json.get("acceptance_criteria", []),
                historia_json.get("definition_of_done", [])
            )
        )

        # Los criterios de aceptación van también en el campo nativo de ADO
        ac_texto = self._formatear_ac_para_ado(
            historia_json.get("acceptance_criteria", [])
        )

        url_feature = (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems/{feature_id}"
        )

        operaciones = [
            self._campo("System.Title", historia_json["summary"]),
            self._campo("System.Description", descripcion_html),
            # Campo nativo de ADO para criterios de aceptación
            self._campo(
                "Microsoft.VSTS.Common.AcceptanceCriteria",
                ac_texto
            ),
            self._campo(
                "System.AreaPath",
                self._area_path(historia_json.get("components", []))
            ),
            self._campo(
                "System.IterationPath",
                self.config.iteration_path_base
            ),
            self._campo(
                "Microsoft.VSTS.Common.Priority",
                self._mapear_prioridad_numero(historia_json.get("priority", ""))
            ),
            # Story Points: en ADO el campo se llama Story Points en Agile,
            # Effort en Scrum y Size en CMMI
            self._campo(
                self._campo_story_points(),
                historia_json.get("story_points")
            ),
            self._campo(
                "System.Tags",
                "; ".join(historia_json.get("labels", []))
            ),
            self._campo(
                "Custom.RequisitoOrigen",
                historia_json.get("custom_fields", {}).get(
                    "requisito_origen", ""
                )
            ),
            self._campo(
                "Custom.ModuloFuncional",
                historia_json.get("custom_fields", {}).get(
                    "modulo_funcional", ""
                )
            ),
            # Relación padre: Feature → User Story
            self._relacion(
                "System.LinkTypes.Hierarchy-Reverse",
                url_feature,
                {"comment": "Feature funcional padre"}
            )
        ]

        return operaciones

    # ── TAREA TÉCNICA ───────────────────────────────────────────────

    def construir_tarea(
        self,
        tarea_json: dict,
        historia_id: int
    ) -> list[dict]:
        """
        Construye las operaciones para crear una Task en ADO.
        historia_id es el ID numérico de la User Story padre.
        En ADO (Agile/Scrum), las Tasks son hijas de las historias,
        no existen subtareas anidadas.
        """
        descripcion_html = self._markdown_a_html(
            self._formatear_descripcion_tarea(tarea_json.get("description", {}))
        )

        url_historia = (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems/{historia_id}"
        )

        horas_estimadas = tarea_json.get("estimacion_horas", 0)

        operaciones = [
            self._campo("System.Title", tarea_json["summary"]),
            self._campo("System.Description", descripcion_html),
            self._campo(
                "System.AreaPath",
                self._area_path(tarea_json.get("components", []))
            ),
            self._campo(
                "System.IterationPath",
                self.config.iteration_path_base
            ),
            # Estimación en horas: campo nativo de ADO para Tasks
            self._campo(
                "Microsoft.VSTS.Scheduling.OriginalEstimate",
                horas_estimadas
            ),
            self._campo(
                "Microsoft.VSTS.Scheduling.RemainingWork",
                horas_estimadas
            ),
            self._campo(
                "System.Tags",
                "; ".join(
                    tarea_json.get("labels", []) +
                    [tarea_json.get("capa", "")]
                )
            ),
            # Relación padre: User Story → Task
            self._relacion(
                "System.LinkTypes.Hierarchy-Reverse",
                url_historia,
                {"comment": f"Historia padre — capa {tarea_json.get('capa', '')}"}
            )
        ]

        return operaciones

    # ── TEST CASE ───────────────────────────────────────────────────

    def construir_test_case(
        self,
        tc: dict,
        historia_id: int
    ) -> list[dict]:
        """
        Construye las operaciones para crear un Test Case en ADO.
        ADO tiene soporte nativo de test cases: el tipo 'Test Case'
        tiene campos específicos para pasos, datos de prueba y resultados.
        Los pasos se almacenan en formato XML en el campo Steps.
        """
        pasos_xml = self._pasos_a_xml(tc.get("pasos", []))
        precondiciones_html = self._markdown_a_html(
            "\n".join(f"- {p}" for p in tc.get("precondiciones", []))
        )

        url_historia = (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems/{historia_id}"
        )

        operaciones = [
            self._campo("System.Title", tc["titulo"]),
            # Campo nativo de ADO para los pasos del test case
            self._campo("Microsoft.VSTS.TCM.Steps", pasos_xml),
            self._campo(
                "Microsoft.VSTS.TCM.LocalDataSource",
                self._datos_prueba_a_xml(tc.get("datos_prueba", {}))
            ),
            self._campo(
                "System.Description",
                precondiciones_html
            ),
            self._campo(
                "Microsoft.VSTS.Common.Priority",
                self._mapear_prioridad_numero(tc.get("prioridad", "media"))
            ),
            self._campo(
                "System.AreaPath",
                self.config.area_path_base
            ),
            self._campo(
                "System.Tags",
                "; ".join([
                    tc.get("tipo", ""),
                    tc.get("criterio_origen", ""),
                    tc.get("requisito_origen", "")
                ])
            ),
            self._campo("Custom.CriterioOrigen", tc.get("criterio_origen", "")),
            self._campo("Custom.RequisitoOrigen", tc.get("requisito_origen", "")),
            # Vínculo Tested By: historia → test case
            self._relacion(
                "Microsoft.VSTS.Common.TestedBy-Reverse",
                url_historia,
                {"comment": "Historia verificada por este test case"}
            )
        ]

        return operaciones

    # ── VINCULACIÓN DE DEPENDENCIAS ─────────────────────────────────

    def construir_dependencia(
        self,
        id_origen: int,
        id_destino: int,
        comentario: str = ""
    ) -> dict:
        """
        Construye el payload para crear un vínculo de dependencia
        entre dos Tasks mediante la API de work item updates.
        En ADO, las dependencias entre tasks usan el tipo
        'Microsoft.VSTS.Common.Affects-Forward'.
        """
        url_destino = (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems/{id_destino}"
        )
        return [
            self._relacion(
                "Microsoft.VSTS.Common.Affects-Forward",
                url_destino,
                {"comment": comentario or "Dependencia técnica"}
            )
        ]

    # ── HELPERS DE FORMATO ──────────────────────────────────────────

    def _campo_story_points(self) -> str:
        return {
            "Agile": "Microsoft.VSTS.Scheduling.StoryPoints",
            "Scrum": "Microsoft.VSTS.Scheduling.Effort",
            "CMMI":  "Microsoft.VSTS.Scheduling.Size"
        }.get(self.config.proceso, "Microsoft.VSTS.Scheduling.StoryPoints")

    def _mapear_prioridad_numero(self, prioridad_pipeline: str) -> int:
        """
        ADO usa prioridad numérica del 1 (más alta) al 4 (más baja).
        """
        return {
            "Highest":     1,
            "High":        2,
            "Medium":      3,
            "Low":         4,
            "must-have":   1,
            "should-have": 2,
            "could-have":  3,
            "wont-have":   4,
            "critica":     1,
            "alta":        2,
            "media":       3,
            "baja":        4
        }.get(prioridad_pipeline, 3)

    def _area_path(self, components: list) -> str:
        """
        Construye el Area Path a partir del primer componente.
        Si no hay componentes, usa el área base de la configuración.
        """
        if not components:
            return self.config.area_path_base
        # Convención: el nombre del componente se añade como subnivel
        componente = components[0].replace("-", " ").title()
        base = self.config.area_path_base or self.config.project
        return f"{base}\\{componente}"

    def _pasos_a_xml(self, pasos: list) -> str:
        """
        Convierte los pasos del test case al formato XML que requiere
        el campo Microsoft.VSTS.TCM.Steps de ADO.
        """
        if not pasos:
            return "<steps />"

        items_xml = []
        for i, paso in enumerate(pasos, 1):
            accion = paso.get("accion", "").replace("<", "&lt;").replace(">", "&gt;")
            resultado = paso.get("resultado_esperado", "").replace("<", "&lt;").replace(">", "&gt;")
            items_xml.append(
                f'<step id="{i}" type="ValidateStep">'
                f'<parameterizedString isformatted="true">{accion}</parameterizedString>'
                f'<parameterizedString isformatted="true">{resultado}</parameterizedString>'
                f'<description />'
                f'</step>'
            )

        return f'<steps id="0" last="{len(pasos)}">' + "".join(items_xml) + "</steps>"

    def _datos_prueba_a_xml(self, datos: dict) -> str:
        """
        Convierte los datos de prueba al formato XML de LocalDataSource de ADO.
        Permite parametrizar los test cases con datos concretos.
        """
        if not datos:
            return ""

        columnas = "".join(
            f'<Column Name="{k}" />' for k in datos.keys()
        )
        fila = "".join(
            f'<Parameter Name="{k}" Value="{v}" />'
            for k, v in datos.items()
        )
        return (
            f'<ArrayOfKeyValueOfstringstring>'
            f'<KeyValueOfstringstring>'
            f'<Key>Data</Key>'
            f'<Value>{fila}</Value>'
            f'</KeyValueOfstringstring>'
            f'</ArrayOfKeyValueOfstringstring>'
        )

    def _formatear_ac_para_ado(self, criterios: list) -> str:
        """
        Formatea los criterios de aceptación para el campo nativo de ADO.
        ADO acepta HTML en este campo.
        """
        if not criterios:
            return ""
        partes = []
        for ac in criterios:
            partes.append(
                f"<p><strong>{ac.get('id', '')}</strong></p>"
                f"<p><em>Dado</em> {ac.get('dado', '')}</p>"
                f"<p><em>Cuando</em> {ac.get('cuando', '')}</p>"
                f"<p><em>Entonces</em> {ac.get('entonces', '')}</p>"
                f"<hr/>"
            )
        return "".join(partes)

    def _markdown_a_html(self, texto: str) -> str:
        """
        Conversión básica de Markdown a HTML para los campos de ADO.
        ADO renderiza HTML en los campos de descripción.
        Para proyectos con descripciones complejas, usar la librería
        'markdown' (pip install markdown) para conversión completa.
        """
        if not texto:
            return ""
        import re
        # Cabeceras
        texto = re.sub(r'^## (.+)$', r'<h2>\1</h2>', texto, flags=re.MULTILINE)
        texto = re.sub(r'^### (.+)$', r'<h3>\1</h3>', texto, flags=re.MULTILINE)
        # Negrita
        texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
        # Listas
        texto = re.sub(r'^- (.+)$', r'<li>\1</li>', texto, flags=re.MULTILINE)
        texto = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', texto, flags=re.DOTALL)
        # Párrafos
        parrafos = texto.split('\n\n')
        resultado = []
        for p in parrafos:
            p = p.strip()
            if p and not p.startswith('<'):
                p = f'<p>{p}</p>'
            resultado.append(p)
        return "\n".join(resultado)

    def _formatear_descripcion_epica(self, desc: dict) -> str:
        lineas = [f"## Objetivo\n{desc.get('objetivo', '')}"]
        if desc.get("alcance"):
            lineas.append(f"## Alcance\n{desc.get('alcance', '')}")
        if desc.get("valor_negocio"):
            lineas.append(f"## Valor de negocio\n{desc.get('valor_negocio', '')}")
        if desc.get("actores_principales"):
            actores = "\n".join(f"- {a}" for a in desc["actores_principales"])
            lineas.append(f"## Actores principales\n{actores}")
        if desc.get("kpis_exito"):
            kpis = "\n".join(f"- {k}" for k in desc["kpis_exito"])
            lineas.append(f"## KPIs de éxito\n{kpis}")
        return "\n\n".join(lineas)

    def _formatear_descripcion_historia(
        self,
        desc: dict,
        criterios: list,
        dod: list
    ) -> str:
        lineas = [f"## Contexto\n{desc.get('contexto', '')}"]
        lineas.append(f"## Narrativa\n{desc.get('narrativa', '')}")
        if desc.get("notas_importantes"):
            notas = "\n".join(f"- {n}" for n in desc["notas_importantes"])
            lineas.append(f"## Notas importantes\n{notas}")
        if desc.get("flujo_principal"):
            pasos = "\n".join(desc["flujo_principal"])
            lineas.append(f"## Flujo principal\n{pasos}")
        if desc.get("flujos_error"):
            errores = "\n".join(
                f"- Si {f['condicion']}: {f['comportamiento_esperado']}"
                for f in desc["flujos_error"]
            )
            lineas.append(f"## Flujos de error\n{errores}")
        if dod:
            dod_texto = "\n".join(f"- {d}" for d in dod)
            lineas.append(f"## Definition of Done\n{dod_texto}")
        return "\n\n".join(lineas)

    def _formatear_descripcion_tarea(self, desc: dict) -> str:
        lineas = [f"## Objetivo\n{desc.get('objetivo', '')}"]
        if desc.get("criterios_tecnico"):
            criterios = "\n".join(f"- {c}" for c in desc["criterios_tecnico"])
            lineas.append(f"## Criterios técnicos\n{criterios}")
        if desc.get("consideraciones"):
            cons = "\n".join(f"- {c}" for c in desc["consideraciones"])
            lineas.append(f"## Consideraciones\n{cons}")
        if desc.get("referencias"):
            refs = "\n".join(f"- {r}" for r in desc["referencias"])
            lineas.append(f"## Referencias\n{refs}")
        return "\n\n".join(lineas)
```

---

## Verificación de idempotencia en ADO

ADO no tiene un lenguaje de consulta tan flexible como el JQL de Jira, pero ofrece la WIQL (Work Item Query Language) para buscar work items por sus campos. La idempotencia se implementa buscando work items existentes que tengan el campo personalizado `Custom.RequisitoOrigen` igual al ID del requisito en proceso.

```python
class VerificadorIdempotenciaADO:
    """
    Verifica si los work items ya existen en ADO antes de crearlos.
    Usa WIQL para buscar por el campo personalizado RequisitoOrigen.
    """

    def __init__(self, cliente: ClienteADO):
        self.cliente = cliente

    def buscar_work_item_existente(
        self,
        requisito_id: str,
        tipo_work_item: str
    ) -> Optional[dict]:
        """
        Busca un work item existente del tipo dado para el requisito.
        Retorna el work item si existe, None si no.
        """
        wiql = {
            "query": f"""
                SELECT [System.Id], [System.Title], [System.State],
                       [Custom.RequisitoOrigen]
                FROM WorkItems
                WHERE [System.TeamProject] = '{self.cliente.config.project}'
                  AND [System.WorkItemType] = '{tipo_work_item}'
                  AND [Custom.RequisitoOrigen] = '{requisito_id}'
                  AND [System.State] <> 'Closed'
                ORDER BY [System.CreatedDate] DESC
            """
        }

        url = (
            f"https://dev.azure.com/{self.cliente.config.organization}/"
            f"{self.cliente.config.project}/_apis/wit/wiql"
        )

        try:
            resultado = self.cliente.post(url, wiql)
            work_items = resultado.get("workItems", [])

            if not work_items:
                return None

            # Recuperar el detalle del primer resultado
            wi_id = work_items[0]["id"]
            url_detalle = (
                f"https://dev.azure.com/{self.cliente.config.organization}/"
                f"_apis/wit/workItems/{wi_id}"
            )
            return self.cliente.get(url_detalle)

        except Exception as e:
            log.warning(f"Error en búsqueda WIQL: {e}. Tratando como nuevo.")
            return None

    def determinar_accion(
        self,
        requisito_id: str,
        tipo_work_item: str
    ) -> tuple[str, Optional[int]]:
        """
        Retorna la acción a tomar y el ID del work item si existe.
        Acciones: 'crear' │ 'actualizar' │ 'omitir'
        """
        wi_existente = self.buscar_work_item_existente(
            requisito_id, tipo_work_item
        )

        if wi_existente is None:
            return "crear", None

        estado = wi_existente.get("fields", {}).get("System.State", "")
        wi_id = wi_existente.get("id")

        # No modificar work items en estados activos de desarrollo
        estados_no_modificar = {"Active", "In Progress", "Resolved", "Closed", "Done"}
        if estado in estados_no_modificar:
            log.info(
                f"Work item {wi_id} en estado '{estado}'. "
                f"No se modifica para no interrumpir el trabajo."
            )
            return "omitir", wi_id

        return "actualizar", wi_id
```

---

## Conector principal para ADO

El conector orquesta la creación completa respetando el orden jerárquico obligatorio de ADO: Epic → Feature → User Story → Tasks → Test Cases.

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResultadoCreacionADO:
    requisito_id: str
    exito: bool
    epic_id: Optional[int] = None
    feature_id: Optional[int] = None
    historia_id: Optional[int] = None
    tareas_ids: list = field(default_factory=list)
    test_cases_ids: list = field(default_factory=list)
    errores: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)
    acciones_realizadas: list = field(default_factory=list)


class ConectorADO:
    """
    Orquesta la creación completa de work items en Azure DevOps
    para un requisito aprobado por el pipeline.
    """

    def __init__(
        self,
        config: ADOConfig,
        motor_trazabilidad
    ):
        self.cliente = ClienteADO(config)
        self.constructor = ConstructorPayloadADO(config)
        self.idempotencia = VerificadorIdempotenciaADO(self.cliente)
        self.trazabilidad = motor_trazabilidad
        self.config = config

    @property
    def _url_wit(self) -> str:
        return (
            f"https://dev.azure.com/{self.config.organization}/"
            f"{self.config.project}/_apis/wit/workItems"
        )

    def _url_crear(self, tipo: str) -> str:
        tipo_url = tipo.replace(" ", "%20")
        return f"{self._url_wit}/${tipo_url}"

    def _url_wi(self, wi_id: int) -> str:
        return (
            f"https://dev.azure.com/{self.config.organization}/"
            f"_apis/wit/workItems/{wi_id}"
        )

    def procesar_requisito_completo(
        self,
        artefactos_aprobados: dict
    ) -> ResultadoCreacionADO:
        """
        Punto de entrada principal. Crea todos los work items en ADO
        en el orden jerárquico requerido.
        """
        req_id = artefactos_aprobados["requisito_id"]
        resultado = ResultadoCreacionADO(
            requisito_id=req_id,
            exito=False
        )

        try:
            # PASO 1: Epic (crear o reutilizar)
            epic_id = self._gestionar_epic(
                artefactos_aprobados.get("epica"),
                artefactos_aprobados.get("epic_id_existente"),
                resultado
            )
            if not epic_id:
                resultado.errores.append("No se pudo obtener la Epic. Abortando.")
                return resultado
            resultado.epic_id = epic_id

            # PASO 2: Feature (equivalente a la épica del pipeline)
            feature_id = self._gestionar_feature(
                artefactos_aprobados.get("epica"),
                epic_id,
                req_id,
                resultado
            )
            if not feature_id:
                resultado.errores.append("No se pudo crear la Feature. Abortando.")
                return resultado
            resultado.feature_id = feature_id

            # PASO 3: User Story (o PBI en Scrum)
            historia_id = self._gestionar_historia(
                artefactos_aprobados["historia"],
                feature_id,
                req_id,
                resultado
            )
            if not historia_id:
                resultado.errores.append("No se pudo crear la historia. Abortando.")
                return resultado
            resultado.historia_id = historia_id

            # PASO 4: Tasks técnicas
            tareas_ids = self._gestionar_tareas(
                artefactos_aprobados.get("tareas", []),
                historia_id,
                resultado
            )
            resultado.tareas_ids = tareas_ids

            # PASO 5: Dependencias entre tasks
            self._crear_dependencias(
                artefactos_aprobados.get("tareas", []),
                tareas_ids,
                resultado
            )

            # PASO 6: Test Cases nativos de ADO
            tc_ids = self._gestionar_test_cases(
                artefactos_aprobados.get("test_cases", []),
                historia_id,
                resultado
            )
            resultado.test_cases_ids = tc_ids

            # PASO 7: Registrar en el grafo de trazabilidad
            self.trazabilidad.registrar_generacion_completa(
                requisito_id=req_id,
                historia_id=str(historia_id),
                criterios_ac=[
                    ac["id"]
                    for ac in artefactos_aprobados["historia"].get(
                        "acceptance_criteria", []
                    )
                ],
                tareas=[str(t) for t in tareas_ids],
                test_cases=[str(t) for t in tc_ids],
                issue_jira_key=str(historia_id),
                epica_id=artefactos_aprobados.get("epica_id", "")
            )

            resultado.exito = True
            log.info(
                f"Requisito {req_id} procesado en ADO. "
                f"Historia: #{historia_id}. "
                f"Tareas: {tareas_ids}"
            )

        except Exception as e:
            resultado.errores.append(str(e))
            log.error(f"Error procesando {req_id} en ADO: {e}", exc_info=True)

        return resultado

    def _gestionar_epic(
        self,
        epica_json: Optional[dict],
        epic_id_existente: Optional[int],
        resultado: ResultadoCreacionADO
    ) -> Optional[int]:
        if epic_id_existente:
            resultado.advertencias.append(
                f"Epic existente reutilizada: #{epic_id_existente}"
            )
            return epic_id_existente

        if not epica_json:
            resultado.errores.append("No se proporcionó JSON de épica ni ID existente.")
            return None

        req_origen = epica_json.get("custom_fields", {}).get("origen_requisito", "")
        accion, wi_id = self.idempotencia.determinar_accion(
            req_origen, self.config.tipo_epic
        )

        if accion == "omitir":
            resultado.acciones_realizadas.append(f"Epic #{wi_id} existente reutilizada")
            return wi_id

        operaciones = self.constructor.construir_epic(epica_json)

        if accion == "actualizar" and wi_id:
            self.cliente.patch_wit(self._url_wi(wi_id), operaciones)
            resultado.acciones_realizadas.append(f"Epic #{wi_id} actualizada")
            return wi_id

        respuesta = self.cliente.patch_wit(
            self._url_crear(self.config.tipo_epic), operaciones
        )
        nuevo_id = respuesta["id"]
        resultado.acciones_realizadas.append(f"Epic #{nuevo_id} creada")
        return nuevo_id

    def _gestionar_feature(
        self,
        epica_json: Optional[dict],
        epic_id: int,
        req_id: str,
        resultado: ResultadoCreacionADO
    ) -> Optional[int]:
        if not epica_json:
            return None

        accion, wi_id = self.idempotencia.determinar_accion(
            f"FEATURE::{epica_json.get('custom_fields', {}).get('modulo_funcional', req_id)}",
            self.config.tipo_feature
        )

        if accion == "omitir":
            resultado.acciones_realizadas.append(f"Feature #{wi_id} existente reutilizada")
            return wi_id

        operaciones = self.constructor.construir_feature(epica_json, epic_id)

        if accion == "actualizar" and wi_id:
            self.cliente.patch_wit(self._url_wi(wi_id), operaciones)
            resultado.acciones_realizadas.append(f"Feature #{wi_id} actualizada")
            return wi_id

        respuesta = self.cliente.patch_wit(
            self._url_crear(self.config.tipo_feature), operaciones
        )
        nuevo_id = respuesta["id"]
        resultado.acciones_realizadas.append(f"Feature #{nuevo_id} creada")
        return nuevo_id

    def _gestionar_historia(
        self,
        historia_json: dict,
        feature_id: int,
        req_id: str,
        resultado: ResultadoCreacionADO
    ) -> Optional[int]:
        accion, wi_id = self.idempotencia.determinar_accion(
            req_id, self.config.tipo_historia
        )

        if accion == "omitir":
            resultado.advertencias.append(
                f"Historia #{wi_id} en progreso. No se modifica."
            )
            return wi_id

        operaciones = self.constructor.construir_historia(historia_json, feature_id)

        if accion == "actualizar" and wi_id:
            self.cliente.patch_wit(self._url_wi(wi_id), operaciones)
            resultado.acciones_realizadas.append(f"Historia #{wi_id} actualizada")
            return wi_id

        respuesta = self.cliente.patch_wit(
            self._url_crear(self.config.tipo_historia), operaciones
        )
        nuevo_id = respuesta["id"]
        resultado.acciones_realizadas.append(f"Historia #{nuevo_id} creada")
        return nuevo_id

    def _gestionar_tareas(
        self,
        tareas_json: list,
        historia_id: int,
        resultado: ResultadoCreacionADO
    ) -> list[int]:
        tareas_ids = []
        for tarea in tareas_json:
            try:
                operaciones = self.constructor.construir_tarea(tarea, historia_id)
                respuesta = self.cliente.patch_wit(
                    self._url_crear(self.config.tipo_tarea), operaciones
                )
                wi_id = respuesta["id"]
                tareas_ids.append(wi_id)
                resultado.acciones_realizadas.append(
                    f"Task #{wi_id} creada ({tarea.get('capa', '')})"
                )
            except Exception as e:
                resultado.errores.append(
                    f"Error creando tarea '{tarea.get('summary', '')[:50]}': {e}"
                )
        return tareas_ids

    def _crear_dependencias(
        self,
        tareas_json: list,
        tareas_ids: list[int],
        resultado: ResultadoCreacionADO
    ):
        """
        Crea vínculos de dependencia entre Tasks usando
        Microsoft.VSTS.Common.Affects-Forward.
        """
        mapa_summary_id = {
            t.get("summary", ""): tareas_ids[i]
            for i, t in enumerate(tareas_json)
            if i < len(tareas_ids)
        }

        for tarea, tarea_id in zip(tareas_json, tareas_ids):
            for dep_summary in tarea.get("dependencias", []):
                dep_id = mapa_summary_id.get(dep_summary)
                if not dep_id:
                    resultado.advertencias.append(
                        f"Dependencia '{dep_summary[:50]}' no encontrada. "
                        f"Vínculo no creado."
                    )
                    continue
                try:
                    operaciones = self.constructor.construir_dependencia(
                        dep_id, tarea_id,
                        f"#{dep_id} debe completarse antes de #{tarea_id}"
                    )
                    self.cliente.patch_wit(self._url_wi(dep_id), operaciones)
                    resultado.acciones_realizadas.append(
                        f"Dependencia: #{dep_id} → #{tarea_id}"
                    )
                except Exception as e:
                    resultado.advertencias.append(
                        f"No se pudo crear dependencia #{dep_id}→#{tarea_id}: {e}"
                    )

    def _gestionar_test_cases(
        self,
        test_cases: list,
        historia_id: int,
        resultado: ResultadoCreacionADO
    ) -> list[int]:
        """
        Crea Test Cases nativos en ADO y los vincula a la historia
        mediante el tipo de relación TestedBy.
        """
        tc_ids = []
        for tc in test_cases:
            try:
                operaciones = self.constructor.construir_test_case(tc, historia_id)
                respuesta = self.cliente.patch_wit(
                    self._url_crear(self.config.tipo_test_case), operaciones
                )
                tc_id = respuesta["id"]
                tc_ids.append(tc_id)
                resultado.acciones_realizadas.append(
                    f"Test Case #{tc_id} creado"
                )
            except Exception as e:
                resultado.errores.append(
                    f"Error creando test case '{tc.get('titulo', '')[:50]}': {e}"
                )
        return tc_ids
```

---

## Campos personalizados en ADO

A diferencia de Jira, donde los campos personalizados se identifican por un ID de tipo `customfield_NNNNN` que varía por instancia, ADO permite crear campos con nombres explícitos bajo el espacio de nombres del proceso. Los campos que el pipeline necesita crear una sola vez en la configuración del proyecto son los siguientes.

```python
CAMPOS_PERSONALIZADOS_ADO = [
    {
        "referenceName": "Custom.RequisitoOrigen",
        "name": "Requisito Origen",
        "type": "string",
        "description": (
            "ID del requisito YAML que originó este work item. "
            "Formato: REQ-NNN. Campo de solo lectura para el equipo."
        ),
        "work_item_types": ["Epic", "Feature", "User Story",
                           "Product Backlog Item", "Task", "Test Case"]
    },
    {
        "referenceName": "Custom.ModuloFuncional",
        "name": "Módulo Funcional",
        "type": "string",
        "description": "ID de la épica funcional del repositorio. Formato: EP-NN.",
        "work_item_types": ["Feature", "User Story", "Product Backlog Item"]
    },
    {
        "referenceName": "Custom.CriterioOrigen",
        "name": "Criterio AC Origen",
        "type": "string",
        "description": (
            "ID del criterio de aceptación que originó este test case. "
            "Formato: AC-NNN-NN."
        ),
        "work_item_types": ["Test Case"]
    }
]
```

El script de inicialización que crea estos campos en el proyecto ADO se ejecuta una sola vez durante la Fase 0 del roadmap:

```python
def inicializar_campos_ado(config: ADOConfig):
    """
    Crea los campos personalizados necesarios en el proceso ADO.
    Debe ejecutarse una sola vez por proyecto.
    Requiere permisos de administrador del proceso.
    """
    cliente = ClienteADO(config)
    url_procesos = (
        f"https://dev.azure.com/{config.organization}/_apis/work/processes"
    )

    # Obtener el ID del proceso del proyecto
    procesos = cliente.get(url_procesos).get("value", [])
    proceso = next(
        (p for p in procesos if p.get("name") == config.proceso), None
    )
    if not proceso:
        raise ValueError(f"Proceso '{config.proceso}' no encontrado")

    proceso_id = proceso["typeId"]

    for campo in CAMPOS_PERSONALIZADOS_ADO:
        url_campo = (
            f"https://dev.azure.com/{config.organization}/_apis/work/"
            f"processes/{proceso_id}/fields"
        )
        try:
            cliente.post(url_campo, {
                "referenceName": campo["referenceName"],
                "name": campo["name"],
                "type": campo["type"],
                "description": campo["description"]
            })
            log.info(f"Campo '{campo['name']}' creado correctamente")
        except Exception as e:
            # El campo puede ya existir si se ejecutó antes
            log.warning(f"Campo '{campo['name']}': {e}")
```

---

## Webhook receiver: ADO → sistema de trazabilidad

ADO permite configurar Service Hooks que notifican a un endpoint externo cuando ocurren eventos en los work items. El webhook receiver actualiza el grafo de trazabilidad del punto 9 con los cambios de estado en tiempo real.

```python
# webhook_ado.py

from fastapi import FastAPI, Request
import hmac, hashlib

app = FastAPI(title="Webhook ADO → Trazabilidad")

EVENTOS_RELEVANTES = {
    "workitem.updated",
    "workitem.deleted",
    "workitem.commented"
}

@app.post("/webhook/ado")
async def recibir_webhook_ado(request: Request):
    """
    ADO llama a este endpoint cuando ocurren eventos en work items.
    Configurar en: ADO Project Settings → Service Hooks → Web Hooks.

    Eventos a suscribir:
      - Work item updated
      - Work item deleted
    """
    payload = await request.json()
    evento = payload.get("eventType", "")

    if evento not in EVENTOS_RELEVANTES:
        return {"status": "ignorado", "evento": evento}

    recurso = payload.get("resource", {})
    wi_id = str(recurso.get("workItemId") or
                recurso.get("id", ""))
    wi_tipo = (
        recurso.get("fields", {})
        .get("System.WorkItemType", {})
        .get("newValue", "")
    )

    if evento == "workitem.updated":
        campos_cambiados = recurso.get("fields", {})

        # Actualizar estado en el grafo
        nuevo_estado = (
            campos_cambiados.get("System.State", {})
            .get("newValue")
        )
        if nuevo_estado and wi_id:
            motor_trazabilidad.registrar_nodo(Nodo(
                id=wi_id,
                tipo=_inferir_tipo_ado(wi_tipo),
                titulo=(
                    campos_cambiados.get("System.Title", {})
                    .get("newValue", "")
                ),
                estado=nuevo_estado,
                metadatos={
                    "sprint": (
                        campos_cambiados.get("System.IterationPath", {})
                        .get("newValue", "")
                    ),
                    "asignado_a": (
                        campos_cambiados.get("System.AssignedTo", {})
                        .get("newValue", {})
                        .get("displayName", "")
                        if isinstance(
                            campos_cambiados.get("System.AssignedTo", {})
                            .get("newValue"), dict
                        ) else ""
                    )
                }
            ))

        # Detectar reaperturas (regresión)
        if nuevo_estado == "Active" and (
            campos_cambiados.get("System.State", {})
            .get("oldValue") in ("Resolved", "Closed")
        ):
            log.warning(
                f"Work item #{wi_id} reabierto. "
                f"Posible fallo en criterios de aceptación."
            )

    elif evento == "workitem.deleted":
        with motor_trazabilidad.db.cursor() as cur:
            cur.execute(
                "UPDATE nodos_trazabilidad SET activo = FALSE WHERE id = %s",
                (wi_id,)
            )
            motor_trazabilidad.db.commit()

    return {"status": "procesado", "wi_id": wi_id}


def _inferir_tipo_ado(wi_tipo: str) -> str:
    return {
        "Epic":                "epic",
        "Feature":             "epic",
        "User Story":          "historia",
        "Product Backlog Item":"historia",
        "Requirement":         "historia",
        "Task":                "tarea",
        "Test Case":           "test_case",
        "Bug":                 "bug"
    }.get(wi_tipo, "issue_ado")
```

---

## Integración con Azure Test Plans

ADO incluye Azure Test Plans como módulo nativo de gestión de pruebas, sin necesidad de herramientas externas como Xray o Zephyr. El pipeline aprovecha esta integración para organizar los test cases generados dentro de un Test Plan estructurado por épica y sprint.

```python
class ConectorAzureTestPlans:
    """
    Gestiona la creación y organización de test cases en Azure Test Plans.
    Estructura: Test Plan (por épica) → Test Suite (por historia) → Test Cases
    """

    def __init__(self, cliente: ClienteADO):
        self.cliente = cliente

    def _url_test(self) -> str:
        return (
            f"https://dev.azure.com/{self.cliente.config.organization}/"
            f"{self.cliente.config.project}/_apis/test"
        )

    def obtener_o_crear_plan(self, epica_nombre: str) -> int:
        """Obtiene o crea el Test Plan para la épica."""
        url = f"{self._url_test()}/plans"
        planes = self.cliente.get(url).get("value", [])

        plan_existente = next(
            (p for p in planes if p.get("name") == f"QA - {epica_nombre}"),
            None
        )
        if plan_existente:
            return plan_existente["id"]

        nuevo_plan = self.cliente.post(url, {
            "name": f"QA - {epica_nombre}",
            "area": {"name": self.cliente.config.area_path_base},
            "iteration": self.cliente.config.iteration_path_base
        })
        return nuevo_plan["id"]

    def obtener_o_crear_suite(
        self,
        plan_id: int,
        historia_id: int,
        historia_titulo: str
    ) -> int:
        """Crea un Test Suite estático para la historia dentro del plan."""
        url = f"{self._url_test()}/plans/{plan_id}/suites"
        suites = self.cliente.get(url).get("value", [])

        suite_existente = next(
            (s for s in suites
             if str(historia_id) in s.get("name", "")),
            None
        )
        if suite_existente:
            return suite_existente["id"]

        nueva_suite = self.cliente.post(url, {
            "suiteType": "StaticTestSuite",
            "name": f"#{historia_id} - {historia_titulo[:60]}"
        })
        return nueva_suite["id"]

    def añadir_test_cases_a_suite(
        self,
        plan_id: int,
        suite_id: int,
        tc_ids: list[int]
    ) -> bool:
        """Añade los test cases creados al suite correspondiente."""
        if not tc_ids:
            return True

        url = (
            f"{self._url_test()}/plans/{plan_id}/"
            f"suites/{suite_id}/testcases/"
            + ",".join(str(tc_id) for tc_id in tc_ids)
        )
        try:
            self.cliente.post(url, {})
            return True
        except Exception as e:
            log.warning(f"Error añadiendo TCs al suite: {e}")
            return False
```

---

## Configuración del orquestador para ADO

El orquestador del punto 13 detecta automáticamente si el proyecto usa Jira o ADO a partir de la variable de entorno `PIPELINE_DESTINO`. Cuando el destino es ADO, sustituye el `ConectorJira` por el `ConectorADO` en los pasos s9_push y s9b_push_xray.

```python
# Fragmento de orchestrator.py — inicialización del conector destino

import os

def _crear_conector_destino(config, motor_trazabilidad):
    """
    Instancia el conector correcto según el sistema de destino configurado.
    Variable de entorno PIPELINE_DESTINO: 'jira' │ 'ado'
    """
    destino = os.getenv("PIPELINE_DESTINO", "jira").lower()

    if destino == "ado":
        from config_ado import ADOConfig
        from conector_ado import ConectorADO

        ado_config = ADOConfig()
        errores = ado_config.validar()
        if errores:
            raise ValueError(
                f"Configuración ADO inválida: {'; '.join(errores)}"
            )
        return ConectorADO(ado_config, motor_trazabilidad), "ado"

    else:
        from config import JiraConfig
        from conector_jira import ConectorJira

        jira_config = JiraConfig()
        return ConectorJira(jira_config, motor_trazabilidad), "jira"
```

El log de salida del orquestador cuando el destino es ADO:

```
────────────────────────────────────────────────────────
  PIPELINE → REQ-023
  Modo: PRODUCCIÓN · Destino: Azure DevOps
  2025-05-12 10:15:32
────────────────────────────────────────────────────────

  [ 1] Carga y parseo del requisito
       ✓ 'Filtrar facturas por rango de fechas'

  [ 2] Validación automática de calidad
       ✓ Score 84/100 · APROBADO

  [ 3] Recuperando contexto del repositorio (RAG)
       ✓ 7 requisitos relacionados recuperados

  [ 4] Generando artefactos con IA
       ✓ Historia · 4 tareas · 3 criterios AC

  [ 5] Generando test cases
       ✓ 9 TCs (2 pos · 4 neg · 3 contorno)

  [ 8] Aprobado por carlos.ruiz@empresa.com

  [ 9] Push a Azure DevOps
       ✓ Epic #1234 (existente)
       ✓ Feature #1289 creada
       ✓ User Story #1290 creada
       ✓ Tasks #1291, #1292, #1293, #1294 creadas
       ✓ Dependencias vinculadas

  [9b] Test Cases en Azure Test Plans
       ✓ Plan 'QA - Gestión de Facturación' (existente)
       ✓ Suite '#1290 - Filtrar facturas por rango de fechas' creada
       ✓ 9 Test Cases añadidos al suite

  ────────────────────────────────────────────────────
  ✓ COMPLETADO en 52.1s
    Feature:    #1289
    Historia:   #1290
    Tareas:     #1291, #1292, #1293, #1294
    Test Cases: 9 (Azure Test Plans)
  ────────────────────────────────────────────────────
```

---

## Diferencias operativas respecto a la integración Jira

Estas son las diferencias prácticas que el analista y el champion deben conocer al operar con ADO como destino, más allá de las diferencias técnicas del conector.

**La jerarquía es más rígida.** En Jira, una historia puede existir sin épica y añadirse después. En ADO, la relación padre-hijo es estricta y el orden de creación importa. Si el pipeline falla al crear la Feature, la historia no puede crearse hasta que la Feature exista. El orquestador gestiona esto con su sistema de estado persistente, pero el analista debe saber que un fallo en la Feature bloquea el resto del árbol.

**Los test cases son ciudadanos de primera clase.** En Jira, los test cases requieren una extensión de terceros (Xray, Zephyr). En ADO, el tipo Test Case existe de forma nativa y está profundamente integrado con Azure Test Plans, Azure Pipelines (para ejecución automática) y los informes de calidad del proyecto. Los test cases generados por el pipeline son directamente ejecutables desde la interfaz de ADO sin ninguna configuración adicional.

**El campo Iteration Path debe mantenerse.** En Jira, el sprint se asigna desde la board y el analista no necesita pensar en él al crear la historia. En ADO, el Iteration Path es un campo del work item que se puede dejar en el nivel del proyecto si no se conoce el sprint en el momento de la creación, pero que debe actualizarse antes del sprint planning. El pipeline crea los work items con el `iteration_path_base` de la configuración; el equipo los mueve al sprint correcto en el planning.

**Las queries WIQL son más limitadas que JQL.** La búsqueda de work items existentes para la idempotencia usa WIQL, que es menos expresiva que JQL para campos personalizados de tipo texto. Si el campo `Custom.RequisitoOrigen` no está indexado en el proyecto, las queries pueden ser lentas en repositorios con más de 5.000 work items. La solución es usar la búsqueda por etiquetas como alternativa: el pipeline añade la etiqueta `req:{req_id}` a todos los work items, y la query WIQL filtra por esa etiqueta, que sí está indexada.

---

## Relación con el resto del modelo

La integración ADO es un sustituto completo de la integración Jira del punto 10. Todos los demás componentes del modelo, desde la plantilla YAML del punto 1 hasta el gobierno del punto 12, funcionan sin cambios cuando el destino es ADO.

El grafo de trazabilidad del punto 9 almacena los IDs de work items de ADO en los nodos con el mismo esquema que los issues de Jira. Las consultas de cobertura, los análisis de impacto del punto 8 y la detección de candidatos a épica nueva del punto de gaps funcionan con independencia del sistema de destino, porque operan sobre el grafo interno, no sobre la API externa.

El único componente que requiere adaptación cuando se cambia de Jira a ADO es el webhook receiver, que procesa los eventos de actualización de work items en el formato específico de cada plataforma. El modelo incluye ambas implementaciones y el orquestador activa la correcta según la variable `PIPELINE_DESTINO`.
