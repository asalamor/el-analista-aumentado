# Integración con herramientas de modelado BPMN

## El problema que resuelve

El Event Storming del punto 3 del modelo operativo es la técnica recomendada para descubrir el dominio funcional desde cero. Pero muchas organizaciones ya tienen su dominio documentado: no en Confluence ni en Word, sino en diagramas de proceso. BPMN en Bizagi o Camunda, diagramas de flujo en Lucidchart, notaciones propias en herramientas de arquitectura empresarial. Ese conocimiento existe, tiene estructura, y tiene un nivel de fidelidad funcional mayor que la mayoría de documentos narrativos porque fue revisado y aprobado por el área de negocio en su momento.

El problema es que ese conocimiento vive desconectado del pipeline. El analista lee el diagrama en la pantalla, lo interpreta mentalmente, y escribe el requisito YAML desde cero, perdiendo la trazabilidad entre el proceso modelado y el requisito generado. Si el proceso cambia en el modelo BPMN, nadie detecta automáticamente que los requisitos derivados de él han quedado desactualizados.

La integración con herramientas de modelado BPMN resuelve eso en dos direcciones. En la dirección de entrada, lee los modelos de proceso y extrae de ellos los elementos que la plantilla YAML necesita: actores, eventos, flujos, condiciones, reglas de negocio y excepciones, todos ya identificados en el diagrama con un nivel de detalle que un documento narrativo raramente iguala. En la dirección de salida, cuando el pipeline genera una historia de usuario o una épica, puede devolver al modelo BPMN una anotación que vincula el elemento de proceso con el artefacto Jira o ADO que lo implementa, cerrando el ciclo de trazabilidad.

---

## Qué información contiene un modelo BPMN que el pipeline puede aprovechar

Antes de diseñar la integración, es necesario entender qué elementos de un modelo BPMN tienen correspondencia directa con los campos de la plantilla YAML del punto 1. No todos los elementos son igualmente útiles: algunos son puramente representacionales, otros contienen semántica funcional que el pipeline puede transformar directamente.

```
ELEMENTO BPMN              → CAMPO YAML                 NOTAS
─────────────────────────────────────────────────────────────────────
Pool / Lane                → actor                      El lane identifica el rol
                                                        que ejecuta las tareas
Start Event               → evento_disparador           El evento que inicia el proceso
Task / User Task           → titulo + descripcion        Las tareas son los candidatos
                                                        a requisitos individuales
Service Task               → notas_implementacion       Indica integración técnica
                                                        no funcionalidad de usuario
Gateway (Exclusive XOR)    → flujos_alternativos +       Cada rama del gateway es un
                             excepciones                flujo alternativo o de error
Gateway (Parallel AND)     → dependencias               Las ramas paralelas implican
                                                        tareas que deben completarse
                                                        simultáneamente
End Event                  → resultado esperado          El estado final del proceso
Intermediate Event         → evento_disparador de        Un evento intermedio puede
                             un requisito nuevo          originar un requisito propio
Message Flow               → integraciones_externas     El flujo de mensajes entre
                             + datos_entrada/salida      pools indica integración
Data Object / Data Store   → datos_entrada/salida       Los objetos de dato describen
                                                        la información que fluye
Text Annotation            → reglas_negocio             Las anotaciones contienen
                                                        restricciones y condiciones
Boundary Event             → excepciones                Los eventos de límite son
                                                        exactamente los flujos de error
Subprocess                 → epica candidata            Un subproceso es candidato
                                                        a convertirse en una épica
```

Esta correspondencia no es perfecta. Un modelo BPMN bien elaborado puede contener toda la información que el pipeline necesita. Un modelo de alto nivel o de comunicación ejecutiva puede contener solo los flujos principales sin las condiciones ni las excepciones. El transformador debe gestionar ambos casos.

---

## Formatos de intercambio soportados

Las tres herramientas del mercado más frecuentes exponen sus modelos en formatos distintos, aunque todas soportan el estándar BPMN 2.0 XML como formato de exportación común.

```
HERRAMIENTA     FORMATO NATIVO        EXPORTACIÓN BPMN      API DISPONIBLE
──────────────────────────────────────────────────────────────────────────
Bizagi          .biz (propietario)    BPMN 2.0 XML (.bpmn)  REST API (Bizagi Studio)
Camunda         BPMN 2.0 XML          BPMN 2.0 XML (.bpmn)  REST API (Camunda Platform)
Lucidchart      .lucid (propietario)  BPMN 2.0 XML +         REST API (Lucidchart API)
                                      Visio (.vsdx) +
                                      PNG/SVG
draw.io         XML propietario       BPMN 2.0 XML (.xml)   Sin API REST (archivo local)
Miro            Propietario           Sin exportación BPMN  REST API (solo contenido
                                      estándar              de sticky notes y shapes)
```

La estrategia recomendada es implementar el lector sobre BPMN 2.0 XML estándar, que todas las herramientas pueden exportar, y añadir conectores específicos por herramienta solo para las capacidades que el estándar no cubre: acceso a la API en tiempo real, recuperación de versiones anteriores y escritura de anotaciones de trazabilidad de vuelta al modelo.

---

## Arquitectura de la integración

```
Modelo BPMN
(Bizagi / Camunda / Lucidchart / draw.io)
        │
        ├── Exportación BPMN 2.0 XML  ──────────────────────────────────
        │   (manual o automática via API)                               │
        │                                                               ▼
        │                                               [Lector BPMN 2.0 XML]
        │                                               Parsea el XML y extrae
        │                                               elementos semánticos
        │
        ├── API Camunda ──────────────────────────────────────────────────
        │   (deploy, consulta de definiciones)                          │
        │                                                               ▼
        │                                               [Conector Camunda]
        │                                               Acceso en tiempo real
        │                                               a definiciones de proceso
        │
        └── API Lucidchart ─────────────────────────────────────────────
            (lectura de documentos)                                     │
                                                                        ▼
                                                        [Conector Lucidchart]
                                                        Lectura de diagramas
                                                        y anotaciones
        │
        ▼
[Transformador BPMN → YAML]
Convierte elementos BPMN en campos de la plantilla
usando el LLM para la semántica no estructurada
        │
        ├── YAMLs borrador → revisión analista → pipeline normal
        │
        ├── Indexación en vector store RAG
        │   (el proceso como contexto de los requisitos)
        │
        └── Trazabilidad inversa: YAML → anotación en el modelo BPMN
```

---

## Lector BPMN 2.0 XML

El lector parsea el formato estándar BPMN 2.0 XML y extrae todos los elementos semánticos relevantes en una estructura de datos normalizada. El XML de BPMN 2.0 tiene un namespace bien definido que permite una extracción determinista sin ambigüedades.

```python
# lector_bpmn.py

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional


# Namespaces del estándar BPMN 2.0
NS = {
    "bpmn":  "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi":"http://www.omg.org/spec/BPMN/20100524/DI",
    "dc":    "http://www.omg.org/spec/DD/20100524/DC",
    "di":    "http://www.omg.org/spec/DD/20100524/DI",
    "camunda":"http://camunda.org/schema/1.0/bpmn",
    "bizagi":"http://www.bizagi.com/definitions/1.0"
}


@dataclass
class ElementoBPMN:
    id: str
    tipo: str
    nombre: str
    documentacion: str = ""
    lane: str = ""           # Lane (actor/rol) al que pertenece
    pool: str = ""           # Pool (participante/sistema) al que pertenece
    entrantes: list[str] = field(default_factory=list)   # IDs de flujos entrantes
    salientes: list[str] = field(default_factory=list)   # IDs de flujos salientes
    propiedades: dict = field(default_factory=dict)      # Propiedades extendidas


@dataclass
class FlujoBPMN:
    id: str
    tipo: str               # sequenceFlow │ messageFlow
    nombre: str             # Condición o nombre del flujo
    origen_id: str
    destino_id: str
    condicion: str = ""     # Expresión de condición en gateways


@dataclass
class ModeloProceso:
    id: str
    nombre: str
    herramienta: str        # bizagi │ camunda │ lucidchart │ drawio │ generico
    version: str
    # Elementos del modelo
    pools: list[dict]
    lanes: list[dict]
    tareas: list[ElementoBPMN]
    eventos_inicio: list[ElementoBPMN]
    eventos_fin: list[ElementoBPMN]
    eventos_intermedios: list[ElementoBPMN]
    gateways: list[ElementoBPMN]
    subprocesos: list[ElementoBPMN]
    flujos: list[FlujoBPMN]
    anotaciones: list[dict]
    objetos_datos: list[dict]
    # Mapa de IDs para navegación
    elementos_por_id: dict


class LectorBPMN:
    """
    Parsea archivos BPMN 2.0 XML y extrae los elementos semánticos
    en una estructura de datos normalizada e independiente de la
    herramienta de origen.
    """

    def leer_archivo(self, ruta: str) -> ModeloProceso:
        """Lee un archivo BPMN 2.0 XML desde disco."""
        with open(ruta, encoding="utf-8") as f:
            contenido = f.read()
        return self.leer_xml(contenido)

    def leer_xml(self, xml_contenido: str) -> ModeloProceso:
        """
        Parsea el XML de BPMN 2.0 y extrae todos los elementos.
        Detecta automáticamente la herramienta de origen por los
        namespaces y atributos presentes.
        """
        # Manejar archivos con y sin declaración de namespace
        try:
            root = ET.fromstring(xml_contenido)
        except ET.ParseError:
            # Intentar limpiar el XML antes de parsear
            xml_limpio = self._limpiar_xml(xml_contenido)
            root = ET.fromstring(xml_limpio)

        herramienta = self._detectar_herramienta(root)

        # Buscar el elemento definitions (raíz estándar de BPMN 2.0)
        definitions = root
        if "definitions" not in root.tag.lower():
            definitions = root.find(
                ".//{http://www.omg.org/spec/BPMN/20100524/MODEL}definitions"
            ) or root

        # Extraer el proceso principal
        proceso_elem = (
            definitions.find(f"{{{NS['bpmn']}}}process") or
            definitions.find(".//process")
        )

        nombre_proceso = (
            definitions.get("name") or
            (proceso_elem.get("name") if proceso_elem is not None else "") or
            "Proceso sin nombre"
        )

        proceso_id = (
            definitions.get("id") or
            (proceso_elem.get("id") if proceso_elem is not None else "PROC-001")
        )

        # Extraer todos los elementos
        pools = self._extraer_pools(definitions)
        lanes = self._extraer_lanes(proceso_elem or definitions)
        mapa_lanes = {l["id"]: l["nombre"] for l in lanes}
        mapa_pools = {p["id"]: p["nombre"] for p in pools}

        tareas = self._extraer_tareas(
            proceso_elem or definitions, mapa_lanes, mapa_pools
        )
        eventos_inicio = self._extraer_eventos(
            proceso_elem or definitions, "startEvent",
            mapa_lanes, mapa_pools
        )
        eventos_fin = self._extraer_eventos(
            proceso_elem or definitions, "endEvent",
            mapa_lanes, mapa_pools
        )
        eventos_intermedios = self._extraer_eventos(
            proceso_elem or definitions, "intermediateCatchEvent",
            mapa_lanes, mapa_pools
        ) + self._extraer_eventos(
            proceso_elem or definitions, "intermediateThrowEvent",
            mapa_lanes, mapa_pools
        )
        gateways = self._extraer_gateways(
            proceso_elem or definitions, mapa_lanes, mapa_pools
        )
        subprocesos = self._extraer_subprocesos(
            proceso_elem or definitions, mapa_lanes, mapa_pools
        )
        flujos = self._extraer_flujos(proceso_elem or definitions)
        anotaciones = self._extraer_anotaciones(proceso_elem or definitions)
        objetos_datos = self._extraer_objetos_datos(proceso_elem or definitions)

        # Construir mapa de IDs
        todos_elementos = (
            tareas + eventos_inicio + eventos_fin +
            eventos_intermedios + gateways + subprocesos
        )
        elementos_por_id = {e.id: e for e in todos_elementos}

        # Enriquecer elementos con sus conexiones
        for flujo in flujos:
            if flujo.origen_id in elementos_por_id:
                elementos_por_id[flujo.origen_id].salientes.append(flujo.destino_id)
            if flujo.destino_id in elementos_por_id:
                elementos_por_id[flujo.destino_id].entrantes.append(flujo.origen_id)

        return ModeloProceso(
            id=proceso_id,
            nombre=nombre_proceso,
            herramienta=herramienta,
            version=definitions.get("exporter", "desconocida"),
            pools=pools,
            lanes=lanes,
            tareas=tareas,
            eventos_inicio=eventos_inicio,
            eventos_fin=eventos_fin,
            eventos_intermedios=eventos_intermedios,
            gateways=gateways,
            subprocesos=subprocesos,
            flujos=flujos,
            anotaciones=anotaciones,
            objetos_datos=objetos_datos,
            elementos_por_id=elementos_por_id
        )

    def _detectar_herramienta(self, root: ET.Element) -> str:
        """Detecta la herramienta que exportó el BPMN por los atributos."""
        exportador = root.get("exporter", "").lower()
        namespace_str = str(root.tag).lower()

        if "bizagi" in exportador or "bizagi" in namespace_str:
            return "bizagi"
        if "camunda" in exportador or "camunda" in str(root.attrib):
            return "camunda"
        if "lucidchart" in exportador:
            return "lucidchart"
        if "draw.io" in exportador or "diagrams.net" in exportador:
            return "drawio"
        return "generico"

    def _extraer_pools(self, root: ET.Element) -> list[dict]:
        pools = []
        for pool in root.iter():
            if "collaboration" in pool.tag.lower():
                for participant in pool:
                    if "participant" in participant.tag.lower():
                        pools.append({
                            "id": participant.get("id", ""),
                            "nombre": participant.get("name", ""),
                            "proceso_ref": participant.get("processRef", "")
                        })
        return pools

    def _extraer_lanes(self, proceso: ET.Element) -> list[dict]:
        lanes = []
        if proceso is None:
            return lanes
        for elem in proceso.iter():
            if "lane" in elem.tag.lower() and "laneSet" not in elem.tag:
                lanes.append({
                    "id": elem.get("id", ""),
                    "nombre": elem.get("name", ""),
                    "elementos": [
                        ref.text for ref in elem
                        if "flowNodeRef" in ref.tag and ref.text
                    ]
                })
        return lanes

    def _extraer_tareas(
        self,
        proceso: ET.Element,
        mapa_lanes: dict,
        mapa_pools: dict
    ) -> list[ElementoBPMN]:
        """
        Extrae todos los tipos de tarea: task, userTask, serviceTask,
        manualTask, sendTask, receiveTask, businessRuleTask, scriptTask.
        """
        tareas = []
        tipos_tarea = {
            "task", "usertask", "servicetask", "manualtask",
            "sendtask", "receivetask", "businessruletask", "scripttask",
            "callactivity"
        }

        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local in tipos_tarea:
                doc = self._extraer_documentacion(elem)
                tareas.append(ElementoBPMN(
                    id=elem.get("id", ""),
                    tipo=tag_local,
                    nombre=elem.get("name", "").strip(),
                    documentacion=doc,
                    lane=self._buscar_lane(elem.get("id", ""), mapa_lanes, proceso),
                    propiedades=self._extraer_propiedades_extendidas(elem)
                ))

        return tareas

    def _extraer_eventos(
        self,
        proceso: ET.Element,
        tipo_evento: str,
        mapa_lanes: dict,
        mapa_pools: dict
    ) -> list[ElementoBPMN]:
        eventos = []
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag_local.lower() == tipo_evento.lower():
                doc = self._extraer_documentacion(elem)
                # Extraer el tipo de evento (message, timer, error, etc.)
                subtipo = self._detectar_subtipo_evento(elem)
                eventos.append(ElementoBPMN(
                    id=elem.get("id", ""),
                    tipo=f"{tipo_evento}:{subtipo}",
                    nombre=elem.get("name", "").strip(),
                    documentacion=doc,
                    lane=self._buscar_lane(elem.get("id", ""), mapa_lanes, proceso),
                    propiedades={"subtipo": subtipo}
                ))
        return eventos

    def _extraer_gateways(
        self,
        proceso: ET.Element,
        mapa_lanes: dict,
        mapa_pools: dict
    ) -> list[ElementoBPMN]:
        gateways = []
        tipos_gateway = {
            "exclusivegateway", "inclusivegateway",
            "parallelgateway", "eventbasedgateway",
            "complexgateway"
        }
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local in tipos_gateway:
                gateways.append(ElementoBPMN(
                    id=elem.get("id", ""),
                    tipo=tag_local,
                    nombre=elem.get("name", "").strip(),
                    documentacion=self._extraer_documentacion(elem),
                    lane=self._buscar_lane(elem.get("id", ""), mapa_lanes, proceso),
                    propiedades={
                        "es_convergente": self._es_convergente(
                            elem.get("id", ""), proceso
                        )
                    }
                ))
        return gateways

    def _extraer_subprocesos(
        self,
        proceso: ET.Element,
        mapa_lanes: dict,
        mapa_pools: dict
    ) -> list[ElementoBPMN]:
        subprocesos = []
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local in ("subprocess", "adhocsubprocess"):
                subprocesos.append(ElementoBPMN(
                    id=elem.get("id", ""),
                    tipo="subprocess",
                    nombre=elem.get("name", "").strip(),
                    documentacion=self._extraer_documentacion(elem),
                    lane=self._buscar_lane(elem.get("id", ""), mapa_lanes, proceso)
                ))
        return subprocesos

    def _extraer_flujos(self, proceso: ET.Element) -> list[FlujoBPMN]:
        flujos = []
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local in ("sequenceflow", "messageflow"):
                condicion = ""
                for child in elem:
                    if "conditionExpression" in child.tag and child.text:
                        condicion = child.text.strip()
                flujos.append(FlujoBPMN(
                    id=elem.get("id", ""),
                    tipo=tag_local,
                    nombre=elem.get("name", "").strip(),
                    origen_id=elem.get("sourceRef", ""),
                    destino_id=elem.get("targetRef", ""),
                    condicion=condicion
                ))
        return flujos

    def _extraer_anotaciones(self, proceso: ET.Element) -> list[dict]:
        anotaciones = []
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local == "textannotation":
                texto_elem = None
                for child in elem:
                    if "text" in child.tag.lower():
                        texto_elem = child
                        break
                texto = (
                    texto_elem.text.strip()
                    if texto_elem is not None and texto_elem.text
                    else elem.get("text", "")
                )
                if texto:
                    # Buscar el elemento al que está asociada la anotación
                    elemento_asociado = self._buscar_elemento_anotado(
                        elem.get("id", ""), proceso
                    )
                    anotaciones.append({
                        "id": elem.get("id", ""),
                        "texto": texto,
                        "elemento_asociado": elemento_asociado
                    })
        return anotaciones

    def _extraer_objetos_datos(self, proceso: ET.Element) -> list[dict]:
        objetos = []
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local in ("dataobject", "datastore", "datastorereference",
                             "dataobjectreference"):
                objetos.append({
                    "id": elem.get("id", ""),
                    "nombre": elem.get("name", "").strip(),
                    "tipo": tag_local
                })
        return objetos

    def _extraer_documentacion(self, elem: ET.Element) -> str:
        """Extrae el texto del elemento documentation de un nodo BPMN."""
        for child in elem:
            if "documentation" in child.tag.lower() and child.text:
                return child.text.strip()
        return ""

    def _extraer_propiedades_extendidas(self, elem: ET.Element) -> dict:
        """
        Extrae propiedades extendidas específicas de herramienta
        (Camunda properties, Bizagi extensions, etc.).
        """
        props = {}
        for child in elem:
            tag_local = child.tag.split("}")[-1].lower() if "}" in child.tag else child.tag.lower()
            if tag_local in ("extensionelements", "properties"):
                for prop in child.iter():
                    nombre = prop.get("name") or prop.get("id", "")
                    valor = prop.get("value") or prop.text
                    if nombre and valor:
                        props[nombre] = valor
        return props

    def _detectar_subtipo_evento(self, elem: ET.Element) -> str:
        """Detecta el subtipo de evento (message, timer, error, signal, etc.)."""
        for child in elem:
            tag_lower = child.tag.split("}")[-1].lower() if "}" in child.tag else child.tag.lower()
            for subtipo in ["message", "timer", "error", "signal",
                           "escalation", "compensation", "cancel", "terminate"]:
                if subtipo in tag_lower:
                    return subtipo
        return "none"

    def _buscar_lane(
        self,
        elemento_id: str,
        mapa_lanes: dict,
        proceso: ET.Element
    ) -> str:
        """Busca en qué lane está un elemento dado su ID."""
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local == "lane":
                nombre_lane = elem.get("name", "")
                for ref in elem:
                    if "flowNodeRef" in ref.tag and ref.text == elemento_id:
                        return nombre_lane
        return ""

    def _es_convergente(
        self,
        gateway_id: str,
        proceso: ET.Element
    ) -> bool:
        """Determina si un gateway es convergente (join) o divergente (split)."""
        entrantes = sum(
            1 for elem in proceso.iter()
            if ("sequenceflow" in (elem.tag.split("}")[-1].lower()
                if "}" in elem.tag else elem.tag.lower()))
            and elem.get("targetRef") == gateway_id
        )
        return entrantes > 1

    def _buscar_elemento_anotado(
        self,
        anotacion_id: str,
        proceso: ET.Element
    ) -> Optional[str]:
        """Busca el ID del elemento al que está asociada una anotación."""
        for elem in proceso.iter():
            tag_local = elem.tag.split("}")[-1].lower() if "}" in elem.tag else elem.tag.lower()
            if tag_local == "association":
                if elem.get("sourceRef") == anotacion_id:
                    return elem.get("targetRef")
                if elem.get("targetRef") == anotacion_id:
                    return elem.get("sourceRef")
        return None

    def _limpiar_xml(self, xml: str) -> str:
        """Limpieza básica de XML malformado."""
        import re
        # Eliminar BOM si existe
        xml = xml.lstrip("\ufeff")
        # Normalizar codificación en la declaración
        xml = re.sub(
            r'<\?xml[^>]*\?>',
            '<?xml version="1.0" encoding="utf-8"?>',
            xml
        )
        return xml
```

---

## Transformador BPMN → YAML

El transformador convierte el modelo de proceso extraído en borradores YAML. Combina análisis estructural del grafo de proceso con el LLM para interpretar la semántica de los elementos.

### Estrategia de granularidad

La pregunta central al transformar un proceso BPMN en requisitos es la granularidad: ¿cada tarea es un requisito? ¿cada subproceso es una épica? La respuesta depende del nivel del modelo.

```python
# transformador_bpmn.py

import json
import yaml
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class CandidatoRequisito:
    """
    Representa una tarea o conjunto de tareas del modelo BPMN
    que son candidatas a convertirse en uno o más requisitos YAML.
    """
    elementos: list[ElementoBPMN]
    actor: str
    evento_disparador: str
    flujos_alternativos: list[dict]
    flujos_error: list[dict]
    anotaciones_asociadas: list[str]
    objetos_datos_asociados: list[dict]
    tipo_origen: str    # tarea_individual │ secuencia_tareas │ subproceso


@dataclass
class ResultadoTransformacionBPMN:
    proceso_id: str
    proceso_nombre: str
    herramienta: str
    epicas_candidatas: list[dict]
    requisitos_generados: list[dict]
    estadisticas: dict
    advertencias: list[str]


class TransformadorBPMN:
    """
    Transforma modelos de proceso BPMN en borradores YAML del pipeline.
    Combina análisis estructural del grafo con LLM para la semántica.
    """

    def __init__(self, openai_client, glosario: dict):
        self.openai = openai_client
        self.glosario = glosario

    def transformar(
        self,
        modelo: ModeloProceso,
        nivel: str = "auto"
    ) -> ResultadoTransformacionBPMN:
        """
        Transforma el modelo BPMN completo en candidatos a épicas y requisitos.

        nivel: auto │ alto │ detallado
          auto      → detecta el nivel del modelo automáticamente
          alto       → un subproceso = una épica, no genera requisitos de tareas
          detallado  → cada user task = un requisito candidato
        """
        nivel_detectado = (
            self._detectar_nivel_modelo(modelo)
            if nivel == "auto" else nivel
        )

        advertencias = []

        # Paso 1: Identificar épicas candidatas desde subprocesos
        epicas_candidatas = self._identificar_epicas(modelo)

        # Paso 2: Identificar candidatos a requisito
        candidatos = self._identificar_candidatos(modelo, nivel_detectado)

        # Paso 3: Enriquecer cada candidato con contexto del grafo
        candidatos_enriquecidos = [
            self._enriquecer_candidato(c, modelo)
            for c in candidatos
        ]

        # Paso 4: Transformar cada candidato en YAML borrador con el LLM
        requisitos_generados = []
        for candidato in candidatos_enriquecidos:
            resultado = self._transformar_candidato(candidato, modelo)
            if resultado:
                requisitos_generados.append(resultado)
            else:
                advertencias.append(
                    f"No se pudo transformar el candidato "
                    f"'{candidato.elementos[0].nombre if candidato.elementos else 'sin nombre'}'"
                )

        # Detectar advertencias del modelo
        advertencias += self._detectar_advertencias_modelo(modelo)

        return ResultadoTransformacionBPMN(
            proceso_id=modelo.id,
            proceso_nombre=modelo.nombre,
            herramienta=modelo.herramienta,
            epicas_candidatas=epicas_candidatas,
            requisitos_generados=requisitos_generados,
            estadisticas={
                "nivel_detectado": nivel_detectado,
                "total_tareas": len(modelo.tareas),
                "total_candidatos": len(candidatos),
                "total_requisitos_generados": len(requisitos_generados),
                "total_epicas_candidatas": len(epicas_candidatas)
            },
            advertencias=advertencias
        )

    def _detectar_nivel_modelo(self, modelo: ModeloProceso) -> str:
        """
        Detecta si el modelo es de alto nivel (pocos elementos, mucha abstracción)
        o detallado (muchas tareas específicas con documentación).
        """
        n_tareas = len(modelo.tareas)
        n_user_tasks = sum(
            1 for t in modelo.tareas if "usertask" in t.tipo.lower()
        )
        n_subprocesos = len(modelo.subprocesos)
        n_con_doc = sum(
            1 for t in modelo.tareas if t.documentacion
        )
        pct_documentadas = (
            n_con_doc / n_tareas if n_tareas > 0 else 0
        )

        # Modelo detallado: muchas user tasks con documentación
        if n_user_tasks >= 5 and pct_documentadas >= 0.5:
            return "detallado"

        # Modelo de alto nivel: pocos elementos, predominan subprocesos
        if n_subprocesos >= 2 and n_tareas <= 10:
            return "alto"

        # Nivel intermedio: combinar ambas estrategias
        return "detallado"

    def _identificar_epicas(self, modelo: ModeloProceso) -> list[dict]:
        """
        Identifica candidatos a épicas:
        - Subprocesos del modelo
        - Lanes con muchas tareas (más de 5)
        - Pools externos (sistemas integrados)
        """
        epicas = []

        # Subprocesos como épicas
        for sp in modelo.subprocesos:
            epicas.append({
                "tipo_origen": "subproceso",
                "nombre_sugerido": sp.nombre,
                "descripcion": sp.documentacion or (
                    f"Módulo funcional correspondiente al subproceso "
                    f"'{sp.nombre}' del proceso '{modelo.nombre}'"
                ),
                "elemento_id": sp.id
            })

        # Lanes con muchas tareas
        tareas_por_lane = defaultdict(list)
        for tarea in modelo.tareas:
            if tarea.lane:
                tareas_por_lane[tarea.lane].append(tarea)

        for lane, tareas in tareas_por_lane.items():
            if len(tareas) >= 5 and not any(
                e["nombre_sugerido"] == lane for e in epicas
            ):
                epicas.append({
                    "tipo_origen": "lane",
                    "nombre_sugerido": f"Módulo {lane}",
                    "descripcion": (
                        f"Conjunto de funcionalidades del rol '{lane}' "
                        f"en el proceso '{modelo.nombre}'"
                    ),
                    "n_tareas": len(tareas)
                })

        return epicas

    def _identificar_candidatos(
        self,
        modelo: ModeloProceso,
        nivel: str
    ) -> list[CandidatoRequisito]:
        """
        Identifica los candidatos a requisito según el nivel del modelo.
        """
        candidatos = []

        if nivel == "alto":
            # Solo subprocesos como candidatos
            for sp in modelo.subprocesos:
                candidatos.append(CandidatoRequisito(
                    elementos=[sp],
                    actor=sp.lane or "Actor pendiente de definir",
                    evento_disparador="",
                    flujos_alternativos=[],
                    flujos_error=[],
                    anotaciones_asociadas=[],
                    objetos_datos_asociados=[],
                    tipo_origen="subproceso"
                ))
        else:
            # Nivel detallado: user tasks y tareas manuales como candidatos
            for tarea in modelo.tareas:
                # Excluir service tasks (son técnicas, no funcionales)
                if "servicetask" in tarea.tipo.lower():
                    continue
                # Excluir call activities sin documentación
                if "callactivity" in tarea.tipo.lower() and not tarea.documentacion:
                    continue

                candidatos.append(CandidatoRequisito(
                    elementos=[tarea],
                    actor=tarea.lane or "Actor pendiente de definir",
                    evento_disparador="",
                    flujos_alternativos=[],
                    flujos_error=[],
                    anotaciones_asociadas=[],
                    objetos_datos_asociados=[],
                    tipo_origen="tarea_individual"
                ))

        return candidatos

    def _enriquecer_candidato(
        self,
        candidato: CandidatoRequisito,
        modelo: ModeloProceso
    ) -> CandidatoRequisito:
        """
        Enriquece el candidato con información del grafo de proceso:
        evento disparador, flujos alternativos, excepciones y anotaciones.
        """
        elem_principal = candidato.elementos[0]

        # Evento disparador: buscar el evento de inicio que alcanza este elemento
        candidato.evento_disparador = self._encontrar_evento_disparador(
            elem_principal.id, modelo
        )

        # Flujos alternativos y de error: analizar gateways conectados
        flujos_alt, flujos_error = self._analizar_gateways_conectados(
            elem_principal.id, modelo
        )
        candidato.flujos_alternativos = flujos_alt
        candidato.flujos_error = flujos_error

        # Anotaciones asociadas al elemento
        candidato.anotaciones_asociadas = [
            a["texto"] for a in modelo.anotaciones
            if a.get("elemento_asociado") == elem_principal.id
        ]

        # Objetos de datos conectados
        candidato.objetos_datos_asociados = self._encontrar_datos_asociados(
            elem_principal.id, modelo
        )

        return candidato

    def _encontrar_evento_disparador(
        self,
        elemento_id: str,
        modelo: ModeloProceso
    ) -> str:
        """
        Navega el grafo hacia atrás para encontrar el evento de inicio
        más próximo que dispara la tarea dada.
        """
        visitados = set()
        cola = [elemento_id]

        while cola:
            actual_id = cola.pop(0)
            if actual_id in visitados:
                continue
            visitados.add(actual_id)

            elemento = modelo.elementos_por_id.get(actual_id)
            if not elemento:
                continue

            # Si es un evento de inicio, hemos encontrado el disparador
            if "startevent" in elemento.tipo.lower():
                return elemento.nombre or f"Inicio del proceso '{modelo.nombre}'"

            # Navegar hacia los elementos predecesores
            for pred_id in elemento.entrantes:
                pred_elem = modelo.elementos_por_id.get(pred_id)
                if pred_elem:
                    cola.append(pred_id)

        # Si no se encontró un evento de inicio directo
        return f"Ejecución del proceso '{modelo.nombre}'"

    def _analizar_gateways_conectados(
        self,
        elemento_id: str,
        modelo: ModeloProceso
    ) -> tuple[list[dict], list[dict]]:
        """
        Analiza los gateways conectados a un elemento para extraer
        flujos alternativos y flujos de error.
        """
        flujos_alt = []
        flujos_error = []

        elemento = modelo.elementos_por_id.get(elemento_id)
        if not elemento:
            return flujos_alt, flujos_error

        # Analizar gateways salientes (divergentes)
        for sucesor_id in elemento.salientes:
            sucesor = modelo.elementos_por_id.get(sucesor_id)
            if not sucesor:
                continue

            if "gateway" in sucesor.tipo.lower() and not sucesor.propiedades.get("es_convergente"):
                # Es un gateway divergente: extraer sus ramas como flujos alternativos
                for rama_id in sucesor.salientes:
                    # Buscar la condición del flujo hacia esta rama
                    condicion = next(
                        (f.condicion or f.nombre for f in modelo.flujos
                         if f.origen_id == sucesor_id and f.destino_id == rama_id),
                        ""
                    )
                    rama_elem = modelo.elementos_por_id.get(rama_id)
                    nombre_rama = rama_elem.nombre if rama_elem else rama_id

                    # Determinar si es flujo de error o alternativo
                    es_error = any(
                        kw in (condicion + nombre_rama).lower()
                        for kw in ["error", "excepción", "fallo", "rechazo",
                                  "cancelación", "timeout", "falla", "exception"]
                    )

                    if es_error:
                        flujos_error.append({
                            "condicion": condicion or nombre_rama,
                            "comportamiento": nombre_rama
                        })
                    else:
                        if condicion or nombre_rama:
                            flujos_alt.append({
                                "condicion": condicion or nombre_rama,
                                "nombre": nombre_rama
                            })

        # Boundary events (eventos de límite) son siempre flujos de error
        for evento in modelo.eventos_intermedios:
            if "boundary" in str(evento.propiedades).lower():
                if elemento_id in evento.propiedades.get("attachedTo", ""):
                    flujos_error.append({
                        "condicion": f"Evento de límite: {evento.nombre}",
                        "comportamiento": evento.nombre
                    })

        return flujos_alt, flujos_error

    def _encontrar_datos_asociados(
        self,
        elemento_id: str,
        modelo: ModeloProceso
    ) -> list[dict]:
        """Encuentra los objetos de datos conectados a un elemento."""
        datos = []
        for obj in modelo.objetos_datos:
            # Los data associations vinculan elementos con objetos de dato
            # En BPMN 2.0 se modelan como dataInputAssociation o dataOutputAssociation
            if obj.get("id") and elemento_id in str(obj):
                datos.append(obj)
        return datos

    def _transformar_candidato(
        self,
        candidato: CandidatoRequisito,
        modelo: ModeloProceso
    ) -> Optional[dict]:
        """
        Transforma un candidato en un YAML borrador usando el LLM.
        """
        elem = candidato.elementos[0]

        # Construir el contexto del candidato para el prompt
        contexto_candidato = self._construir_contexto_candidato(
            candidato, modelo
        )

        prompt = f"""
Eres un analista funcional senior. El siguiente fragmento proviene de un
modelo de proceso BPMN del proyecto y describe una tarea o funcionalidad
que debe implementarse en el sistema.

PROCESO ORIGEN: {modelo.nombre}
HERRAMIENTA: {modelo.herramienta}

ELEMENTO BPMN:
{contexto_candidato}

GLOSARIO DEL PROYECTO (usar estos términos exactos):
{self._glosario_compacto()}

Tu tarea es convertir este elemento BPMN en un requisito funcional
en formato YAML del proyecto.

INSTRUCCIONES:
1. El actor debe ser exactamente uno del glosario. Si el lane del BPMN
   usa un sinónimo, usa el nombre oficial del glosario.
2. El evento_disparador debe extraerse del evento de inicio identificado.
3. Los gateways divergentes se convierten en flujos_alternativos o excepciones.
4. Las anotaciones del BPMN se convierten en reglas_negocio.
5. Los objetos de datos se convierten en datos_entrada o datos_salida.
6. Marca con [PENDIENTE] cualquier campo que no puedas deducir del BPMN.
7. No inventes información que no esté en el modelo.

El YAML debe incluir el origen del requisito:
  origen:
    fuente_documental: "Proceso BPMN: {modelo.nombre}"
    elemento_bpmn_id: "{elem.id}"
    elemento_bpmn_tipo: "{elem.tipo}"
    herramienta: "{modelo.herramienta}"

Responde SOLO con JSON válido:
{{
  "yaml_borrador": "...",
  "confianza": 0.0-1.0,
  "campos_pendientes": [],
  "advertencias": []
}}
"""

        try:
            response = self.openai.chat.completions.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            texto = response.choices[0].message.content
            texto = texto.replace("```json", "").replace("```", "").strip()
            datos = json.loads(texto)

            # Validar que el YAML es parseable
            yaml_str = datos.get("yaml_borrador", "")
            yaml.safe_load(yaml_str)

            return {
                "elemento_id": elem.id,
                "elemento_nombre": elem.nombre,
                "yaml": yaml_str,
                "confianza": datos.get("confianza", 0.5),
                "campos_pendientes": datos.get("campos_pendientes", []),
                "advertencias": datos.get("advertencias", [])
            }

        except Exception as e:
            import logging
            logging.getLogger("pipeline.bpmn").warning(
                f"Error transformando elemento {elem.id}: {e}"
            )
            return None

    def _construir_contexto_candidato(
        self,
        candidato: CandidatoRequisito,
        modelo: ModeloProceso
    ) -> str:
        """
        Construye el bloque de texto que describe el candidato
        para el prompt del LLM.
        """
        elem = candidato.elementos[0]
        lineas = [
            f"Tipo de elemento: {elem.tipo}",
            f"Nombre: {elem.nombre}",
            f"Actor/Lane: {candidato.actor}",
            f"Evento disparador identificado: {candidato.evento_disparador}"
        ]

        if elem.documentacion:
            lineas.append(f"Documentación en el modelo: {elem.documentacion}")

        if candidato.anotaciones_asociadas:
            lineas.append(
                "Anotaciones/reglas en el modelo:\n" +
                "\n".join(f"  - {a}" for a in candidato.anotaciones_asociadas)
            )

        if candidato.flujos_alternativos:
            lineas.append(
                "Flujos alternativos identificados:\n" +
                "\n".join(
                    f"  - Si {f['condicion']}: {f['nombre']}"
                    for f in candidato.flujos_alternativos
                )
            )

        if candidato.flujos_error:
            lineas.append(
                "Flujos de error/excepción identificados:\n" +
                "\n".join(
                    f"  - Si {f['condicion']}: {f['comportamiento']}"
                    for f in candidato.flujos_error
                )
            )

        if candidato.objetos_datos_asociados:
            nombres_datos = [
                d.get("nombre", d.get("id", ""))
                for d in candidato.objetos_datos_asociados
            ]
            lineas.append(
                f"Datos involucrados: {', '.join(nombres_datos)}"
            )

        if elem.propiedades:
            props_relevantes = {
                k: v for k, v in elem.propiedades.items()
                if k not in ("es_convergente",) and v
            }
            if props_relevantes:
                lineas.append(
                    "Propiedades extendidas del modelo:\n" +
                    "\n".join(f"  {k}: {v}" for k, v in props_relevantes.items())
                )

        return "\n".join(lineas)

    def _detectar_advertencias_modelo(
        self,
        modelo: ModeloProceso
    ) -> list[str]:
        """
        Detecta problemas en el modelo BPMN que pueden afectar
        a la calidad de la transformación.
        """
        advertencias = []

        # Tareas sin nombre
        sin_nombre = [t for t in modelo.tareas if not t.nombre.strip()]
        if sin_nombre:
            advertencias.append(
                f"{len(sin_nombre)} tarea(s) sin nombre en el modelo. "
                f"Los requisitos derivados tendrán título [PENDIENTE]."
            )

        # Gateways sin condiciones en los flujos salientes
        for gw in modelo.gateways:
            if "exclusivegateway" in gw.tipo.lower():
                flujos_salientes = [
                    f for f in modelo.flujos
                    if f.origen_id == gw.id
                ]
                sin_condicion = [
                    f for f in flujos_salientes
                    if not f.condicion and not f.nombre
                ]
                if sin_condicion:
                    advertencias.append(
                        f"Gateway '{gw.nombre or gw.id}' tiene "
                        f"{len(sin_condicion)} flujo(s) saliente(s) sin condición. "
                        f"Los flujos alternativos generados estarán incompletos."
                    )

        # Modelo sin ninguna documentación en las tareas
        pct_doc = (
            sum(1 for t in modelo.tareas if t.documentacion) /
            len(modelo.tareas)
        ) if modelo.tareas else 0
        if pct_doc < 0.2 and len(modelo.tareas) > 3:
            advertencias.append(
                f"El modelo tiene poca documentación en las tareas "
                f"({pct_doc:.0%}). Los requisitos generados tendrán "
                f"muchos campos [PENDIENTE] y requerirán revisión extensa."
            )

        # Modelo de alto nivel sin subprocesos
        if len(modelo.tareas) > 20 and not modelo.subprocesos:
            advertencias.append(
                "El modelo tiene muchas tareas sin subprocesos. "
                "Considerar agruparlas en épicas manualmente antes de transformar."
            )

        return advertencias

    def _glosario_compacto(self) -> str:
        """Genera el bloque compacto del glosario para el prompt."""
        actores = self.glosario.get("actores", [])
        lineas = []
        for a in actores[:8]:
            sinonimos = a.get("sinonimos_no_oficiales", [])[:3]
            lineas.append(
                f"- '{a['nombre_oficial']}'"
                + (f" [NO: {', '.join(sinonimos)}]" if sinonimos else "")
            )
        return "Actores oficiales:\n" + "\n".join(lineas) if lineas else ""
```

---

## Conectores específicos por herramienta

### Conector Camunda Platform

Camunda expone una REST API completa que permite leer las definiciones de proceso sin necesidad de exportar el XML manualmente.

```python
# conector_camunda.py

import requests
from dataclasses import dataclass
import os


@dataclass
class CamundaConfig:
    base_url: str = os.getenv("CAMUNDA_URL", "http://localhost:8080")
    # Camunda Platform 7: http://host:port/engine-rest
    # Camunda Platform 8: endpoint de Zeebe gRPC (diferente API)
    user: str = os.getenv("CAMUNDA_USER", "demo")
    password: str = os.getenv("CAMUNDA_PASSWORD", "demo")
    motor: str = os.getenv("CAMUNDA_ENGINE", "default")


class ConectorCamunda:
    """
    Accede a la API REST de Camunda Platform 7 para leer
    definiciones de proceso en tiempo real.
    """

    def __init__(self, config: CamundaConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.user, config.password)
        self.session.headers.update({"Accept": "application/json"})

    @property
    def _url(self) -> str:
        return f"{self.config.base_url}/engine-rest"

    def listar_procesos(self) -> list[dict]:
        """Lista todas las definiciones de proceso activas."""
        response = self.session.get(
            f"{self._url}/process-definition",
            params={"latestVersion": "true", "active": "true"}
        )
        response.raise_for_status()
        return response.json()

    def obtener_xml(self, process_definition_id: str) -> str:
        """Obtiene el XML BPMN de una definición de proceso por su ID."""
        response = self.session.get(
            f"{self._url}/process-definition/{process_definition_id}/xml"
        )
        response.raise_for_status()
        return response.json().get("bpmn20Xml", "")

    def leer_proceso(
        self,
        process_definition_id: str,
        lector: LectorBPMN
    ) -> ModeloProceso:
        """
        Descarga y parsea una definición de proceso de Camunda
        en un ModeloProceso del pipeline.
        """
        xml = self.obtener_xml(process_definition_id)
        if not xml:
            raise ValueError(
                f"No se pudo obtener el XML del proceso {process_definition_id}"
            )
        modelo = lector.leer_xml(xml)
        modelo.herramienta = "camunda"
        return modelo
```

### Conector Lucidchart

```python
# conector_lucidchart.py

import requests
from dataclasses import dataclass
import os


@dataclass
class LucidchartConfig:
    api_token: str = os.getenv("LUCIDCHART_API_TOKEN", "")
    # OAuth 2.0 token generado en developer.lucid.co


class ConectorLucidchart:
    """
    Accede a la API REST de Lucidchart para leer documentos
    que contienen diagramas BPMN.
    """

    BASE_URL = "https://api.lucid.co"

    def __init__(self, config: LucidchartConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_token}",
            "Accept": "application/json",
            "Lucid-Api-Version": "1"
        })

    def listar_documentos(
        self,
        product: str = "lucidchart"
    ) -> list[dict]:
        """Lista los documentos de Lucidchart accesibles."""
        response = self.session.get(
            f"{self.BASE_URL}/documents",
            params={"product": product}
        )
        response.raise_for_status()
        return response.json().get("documents", [])

    def exportar_bpmn(self, document_id: str) -> str:
        """
        Exporta un documento de Lucidchart como BPMN 2.0 XML.
        Requiere que el documento contenga un diagrama compatible.
        """
        response = self.session.post(
            f"{self.BASE_URL}/documents/{document_id}/export",
            json={
                "format": "bpmn",
                "allPages": True
            }
        )
        response.raise_for_status()
        datos = response.json()
        # El export es asíncrono; esperar el resultado
        job_id = datos.get("jobId")
        return self._esperar_export(job_id) if job_id else ""

    def _esperar_export(
        self,
        job_id: str,
        max_intentos: int = 10
    ) -> str:
        """Polling hasta que el export esté disponible."""
        import time
        for _ in range(max_intentos):
            time.sleep(2)
            response = self.session.get(
                f"{self.BASE_URL}/exports/{job_id}"
            )
            datos = response.json()
            estado = datos.get("status")
            if estado == "complete":
                url_descarga = datos.get("downloadUrl", "")
                if url_descarga:
                    contenido = requests.get(url_descarga)
                    return contenido.text
                return ""
            if estado == "failed":
                raise RuntimeError(
                    f"Export de Lucidchart fallido: {datos.get('error')}"
                )
        raise TimeoutError(
            f"Export de Lucidchart no completado tras {max_intentos} intentos"
        )
```

---

## Trazabilidad inversa: pipeline → modelo BPMN

Una vez que el pipeline genera los artefactos Jira o ADO, puede anotar el modelo BPMN original vinculando cada elemento del proceso con el issue que lo implementa. Esta trazabilidad inversa cierra el ciclo: el arquitecto de procesos puede abrir el modelo en Camunda o Bizagi y ver directamente qué historias implementan cada tarea.

```python
# anotador_bpmn.py

class AnotadorBPMN:
    """
    Escribe anotaciones de trazabilidad de vuelta al modelo BPMN.
    Vincula elementos del proceso con los artefactos generados en Jira/ADO.
    """

    def anotar_en_camunda(
        self,
        proceso_id: str,
        elemento_id: str,
        requisito_id: str,
        issue_key: str,
        conector_camunda: ConectorCamunda
    ) -> bool:
        """
        Añade una variable de proceso en Camunda que vincula
        el elemento con el artefacto generado.
        Usa el mecanismo de extensiones de Camunda para no modificar
        el BPMN estándar.
        """
        try:
            # Camunda permite añadir variables a nivel de instancia de proceso.
            # Para anotaciones de modelado, usar la API de user tasks
            # o los comentarios de la tarea si está activa.
            # En proyectos donde el proceso no está en ejecución, la
            # trazabilidad se gestiona en el repositorio del pipeline,
            # no en el modelo mismo.
            payload = {
                "variables": {
                    f"pipeline_req_{elemento_id}": {
                        "value": f"{requisito_id}:{issue_key}",
                        "type": "String"
                    }
                }
            }
            # Registrar en el repositorio de trazabilidad local
            self._registrar_vinculo_local(
                proceso_id, elemento_id, requisito_id, issue_key
            )
            return True
        except Exception as e:
            import logging
            logging.getLogger("pipeline.bpmn").warning(
                f"No se pudo anotar en Camunda: {e}"
            )
            return False

    def generar_xml_anotado(
        self,
        xml_original: str,
        vinculos: list[dict]
    ) -> str:
        """
        Genera una versión del XML BPMN con anotaciones de trazabilidad
        añadidas como TextAnnotations al diagrama.
        Útil para herramientas que no tienen API de escritura (draw.io, Bizagi).
        """
        import xml.etree.ElementTree as ET

        ET.register_namespace("bpmn", NS["bpmn"])
        ET.register_namespace("bpmndi", NS["bpmndi"])

        root = ET.fromstring(xml_original)
        proceso = root.find(
            f"{{{NS['bpmn']}}}process"
        ) or root.find(".//process")

        if proceso is None:
            return xml_original

        for vinculo in vinculos:
            elemento_id = vinculo.get("elemento_id", "")
            issue_key = vinculo.get("issue_key", "")
            requisito_id = vinculo.get("requisito_id", "")

            if not elemento_id or not issue_key:
                continue

            # Crear TextAnnotation con la trazabilidad
            annotation_id = f"pipeline_trace_{elemento_id}"
            annotation = ET.SubElement(
                proceso,
                f"{{{NS['bpmn']}}}textAnnotation",
                {"id": annotation_id}
            )
            texto_elem = ET.SubElement(
                annotation,
                f"{{{NS['bpmn']}}}text"
            )
            texto_elem.text = (
                f"Pipeline: {requisito_id} → {issue_key}"
            )

            # Association entre el elemento y la anotación
            assoc_id = f"pipeline_assoc_{elemento_id}"
            ET.SubElement(
                proceso,
                f"{{{NS['bpmn']}}}association",
                {
                    "id": assoc_id,
                    "sourceRef": elemento_id,
                    "targetRef": annotation_id
                }
            )

        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    def _registrar_vinculo_local(
        self,
        proceso_id: str,
        elemento_id: str,
        requisito_id: str,
        issue_key: str
    ):
        """
        Registra el vínculo en el grafo de trazabilidad del punto 9.
        """
        import logging
        logging.getLogger("pipeline.bpmn").info(
            f"Vínculo BPMN registrado: "
            f"proceso={proceso_id} elemento={elemento_id} "
            f"req={requisito_id} issue={issue_key}"
        )
```

---

## Comando de línea de operación

```bash
# Transformar un archivo BPMN local en YAMLs borrador
python orchestrator.py \
  --bpmn-transform \
  --file ./procesos/gestion-facturas.bpmn \
  --nivel auto \
  --output ./borradores/

# Transformar desde Camunda por ID de proceso
python orchestrator.py \
  --bpmn-transform \
  --camunda-process-id invoice-approval-process:3:abc123 \
  --output ./borradores/

# Transformar desde Lucidchart por ID de documento
python orchestrator.py \
  --bpmn-transform \
  --lucidchart-doc-id abc-123-def \
  --output ./borradores/

# Indexar un modelo BPMN en el vector store RAG sin transformar
python orchestrator.py \
  --bpmn-index \
  --file ./procesos/gestion-facturas.bpmn

# Generar XML anotado con trazabilidad inversa
python orchestrator.py \
  --bpmn-annotate \
  --file ./procesos/gestion-facturas.bpmn \
  --output ./procesos/gestion-facturas-trazado.bpmn
```

Salida de la transformación en consola:

```
══════════════════════════════════════════════════════════
  TRANSFORMACIÓN BPMN → YAML
  Archivo: gestion-facturas.bpmn
  Herramienta detectada: camunda
  Proceso: Gestión y aprobación de facturas de proveedor
══════════════════════════════════════════════════════════

  [1] Parseando modelo BPMN...
      ✓ 3 pools · 4 lanes · 18 tareas · 6 gateways
      ✓ 2 subprocesos · 12 anotaciones · 8 objetos de datos

  [2] Detectando nivel del modelo...
      ✓ Nivel: detallado (78% de tareas documentadas)

  [3] Identificando candidatos...
      ✓ 2 épicas candidatas (subprocesos)
      ✓ 12 candidatos a requisito (excluyendo 6 service tasks)

  [4] Enriqueciendo candidatos con contexto del grafo...
      ✓ Eventos disparadores: 12/12 identificados
      ✓ Flujos alternativos: 8 flujos en 4 gateways
      ✓ Flujos de error: 5 boundary events

  [5] Transformando con IA...
      ✓ 12/12 requisitos transformados

  RESULTADO:
  ──────────────────────────────────────────────────────
  Épicas candidatas:
    EP-CAND-01  Recepción y registro de facturas
    EP-CAND-02  Aprobación y pago de facturas

  Requisitos (12):
    REQ-B-01  88%  Registrar factura recibida por correo
    REQ-B-02  82%  Validar datos de factura contra pedido
    REQ-B-03  79%  Aprobar factura estándar (≤10.000€)
    REQ-B-04  91%  Escalar aprobación a responsable financiero
    REQ-B-05  73%  Rechazar factura con nota de motivo
    REQ-B-06  85%  Programar pago según condiciones de proveedor
    REQ-B-07  68%  Notificar proveedor de rechazo        ⚠ revisar actor
    REQ-B-08  77%  Archivar factura pagada
    REQ-B-09  62%  Gestionar factura con discrepancia     ⚠ revisar
    REQ-B-10  84%  Consultar estado de factura por gestor
    REQ-B-11  71%  Exportar listado de facturas del período
    REQ-B-12  55%  Configurar umbrales de aprobación      ⚠ revisión manual
  ──────────────────────────────────────────────────────

  ⚠ 3 advertencias del modelo:
    → Gateway 'Decisión de aprobación' tiene 1 flujo sin condición
    → Tarea 'Notificar proveedor' usa el término 'proveedor externo'
      (sinónimo no oficial de 'Proveedor' en el glosario)
    → REQ-B-12 tiene confianza baja (55%): la tarea de configuración
      puede ser un NFR en lugar de un requisito funcional

  Borradores guardados en: ./borradores/gestion-facturas/
  Tiempo total: 34.7s
══════════════════════════════════════════════════════════
```

---

## Limitaciones y gestión de expectativas

**La calidad de la extracción depende del nivel de detalle del modelo.** Un modelo BPMN de comunicación ejecutiva, con tareas del tipo "Gestionar factura" o "Procesar solicitud", produce candidatos a requisito con muchos campos pendientes que el analista debe completar. Un modelo detallado con documentación en cada tarea y condiciones en cada gateway produce borradores de alta confianza que requieren revisión mínima. El indicador más fiable antes de la transformación es el porcentaje de tareas con documentación: por debajo del 30%, el resultado requerirá trabajo extenso de completado.

**Los service tasks y script tasks no generan requisitos funcionales.** Son tareas técnicas que el desarrollador implementará sin necesidad de una historia de usuario. El transformador los excluye por defecto, pero el analista debe revisar los borradores para verificar que ninguno relevante quedó fuera, especialmente en modelos donde las tareas de integración tienen nombres ambiguos.

**Los modelos de alto nivel necesitan Event Storming previo.** Si el modelo BPMN tiene menos de diez tareas y varios subprocesos sin detalle, la transformación produce épicas candidatas pero no requisitos accionables. En ese caso, el flujo recomendado es usar el modelo como entrada para un Event Storming focalizado en cada subproceso, no intentar extraer requisitos directamente del modelo de alto nivel.

**La trazabilidad inversa es de mejor esfuerzo en herramientas cerradas.** Camunda soporta anotaciones mediante su API de variables. Bizagi y draw.io requieren edición manual del XML o del archivo nativo. Lucidchart permite añadir texto a shapes mediante su API, pero no en formato BPMN estándar. Para organizaciones donde la trazabilidad inversa es un requisito de gobierno, Camunda es la única herramienta de las tres que la soporta de forma programática sin intervención manual.

**Los modelos con múltiples pools requieren atención especial.** Cuando el modelo tiene pools que representan sistemas externos, los message flows entre pools se convierten en requisitos de integración, no en requisitos funcionales de usuario. El transformador los detecta y los marca como candidatos a `integraciones_externas` en el YAML, pero el analista debe confirmar qué tipo de integración se requiere (API REST, evento, fichero) antes de que entren al pipeline de generación de tareas técnicas.
