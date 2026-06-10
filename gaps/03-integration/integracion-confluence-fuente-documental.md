# Integración con Confluence como fuente documental

## El problema que resuelve

El pipeline descrito en el modelo operativo asume que el analista trabaja directamente con archivos YAML en Git o en Confluence con la plantilla estructurada del punto 1. Esa asunción es correcta para proyectos que adoptan el modelo desde cero. No lo es para la realidad más frecuente: organizaciones donde el conocimiento funcional ya vive en cientos de páginas de Confluence redactadas en prosa, con tablas de requisitos en formato libre, actas de reunión, documentos de visión y especificaciones funcionales heredadas.

En ese contexto, el analista tiene dos opciones. La primera es reescribir el contenido existente en la plantilla YAML antes de poder usar el pipeline, lo que supone semanas de trabajo de transformación que no producen valor funcional nuevo. La segunda es ignorar el conocimiento existente y empezar desde cero, perdiendo el contexto acumulado del proyecto.

La integración con Confluence como fuente documental ofrece una tercera opción: leer las páginas directamente, extraer la información estructurada que contienen usando el LLM como intérprete, y producir YAMLs de requisito borradores que el analista revisa y valida en lugar de escribir desde cero. El analista sigue siendo el propietario del requisito, pero el tiempo de creación se reduce drásticamente porque parte de un borrador generado desde la documentación existente en lugar de una plantilla vacía.

El mismo mecanismo sirve para mantener el repositorio sincronizado cuando el contenido de Confluence se actualiza: el sistema detecta cambios en las páginas vinculadas a requisitos y alerta al analista antes de que la divergencia entre la documentación y el pipeline sea demasiado grande para reconciliar.

---

## Arquitectura de la integración

La integración tiene tres modos de operación con propósitos distintos que comparten la misma infraestructura de lectura pero divergen en el procesamiento posterior.

```
Página de Confluence
        │
        ▼
[Lector] Extracción de contenido via REST API
        │
        ├──[Modo 1: Transformación]──────────────────────────────────
        │   LLM interpreta la página y genera YAML borrador
        │   Analista revisa y valida → entra al pipeline normal
        │
        ├──[Modo 2: Enriquecimiento de contexto RAG]─────────────────
        │   El contenido se indexa en el vector store del punto 7
        │   El pipeline lo recupera como contexto al generar artefactos
        │
        └──[Modo 3: Vigilancia de cambios]──────────────────────────
            Webhook de Confluence detecta actualizaciones de páginas
            vinculadas a requisitos → alerta al analista
```

---

## Autenticación y cliente base

Confluence Cloud y Confluence Server/Data Center usan APIs distintas. El cliente base abstrae esa diferencia para que el resto del código sea independiente del tipo de instalación.

```python
# cliente_confluence.py

import requests
import base64
import os
import time
import logging
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger("pipeline.confluence")


@dataclass
class ConfluenceConfig:
    tipo: str = os.getenv("CONFLUENCE_TIPO", "cloud")
    # cloud        → Confluence Cloud (Atlassian)
    # server       → Confluence Server o Data Center (on-premise)

    base_url: str = os.getenv("CONFLUENCE_BASE_URL", "")
    # Cloud:  https://tu-empresa.atlassian.net/wiki
    # Server: https://confluence.tu-empresa.com

    user_email: str = os.getenv("CONFLUENCE_USER_EMAIL", "")
    # Cloud: dirección de correo del usuario
    # Server: nombre de usuario

    api_token: str = os.getenv("CONFLUENCE_API_TOKEN", "")
    # Cloud:  Personal Access Token generado en id.atlassian.com
    # Server: Personal Access Token generado en el perfil de usuario

    espacio_principal: str = os.getenv("CONFLUENCE_SPACE_KEY", "")
    # Clave del espacio donde vive la documentación funcional
    # Ejemplo: "FACT", "PROJ", "DOC"

    pagina_raiz_requisitos: Optional[str] = os.getenv(
        "CONFLUENCE_ROOT_PAGE_ID", None
    )
    # ID de la página raíz bajo la cual se organizan los requisitos
    # Si se especifica, la búsqueda se restringe a este subárbol

    max_reintentos: int = 3
    pausa_entre_llamadas_ms: int = 300
    timeout_segundos: int = 30

    def validar(self) -> list[str]:
        errores = []
        if not self.base_url:
            errores.append("CONFLUENCE_BASE_URL no configurada")
        if not self.user_email:
            errores.append("CONFLUENCE_USER_EMAIL no configurada")
        if not self.api_token:
            errores.append("CONFLUENCE_API_TOKEN no configurada")
        if self.tipo not in ("cloud", "server"):
            errores.append(
                f"CONFLUENCE_TIPO '{self.tipo}' no válido. "
                f"Valores: cloud │ server"
            )
        return errores


class ClienteConfluence:
    """
    Cliente base para la REST API de Confluence.
    Soporta Cloud y Server/Data Center con la misma interfaz.
    """

    def __init__(self, config: ConfluenceConfig):
        self.config = config
        self.session = requests.Session()

        # Autenticación Basic con email:token (Cloud) o user:token (Server)
        credencial = base64.b64encode(
            f"{config.user_email}:{config.api_token}".encode("ascii")
        ).decode("ascii")

        self.session.headers.update({
            "Authorization": f"Basic {credencial}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        self._ultima_llamada = 0.0

    @property
    def _api_base(self) -> str:
        """URL base de la API según el tipo de instalación."""
        if self.config.tipo == "cloud":
            return f"{self.config.base_url}/rest/api"
        else:
            return f"{self.config.base_url}/rest/api"
        # La ruta es la misma; la diferencia está en la autenticación
        # y en algunos campos de la respuesta

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
        endpoint: str,
        params: dict = None,
        payload: dict = None
    ) -> dict:
        url = f"{self._api_base}/{endpoint}"
        intentos = 0

        while intentos < self.config.max_reintentos:
            self._respetar_rate_limit()
            try:
                response = self.session.request(
                    method=metodo,
                    url=url,
                    params=params,
                    json=payload,
                    timeout=self.config.timeout_segundos
                )

                if response.status_code == 429:
                    espera = int(
                        response.headers.get("Retry-After", 60)
                    )
                    log.warning(
                        f"Rate limit Confluence. Esperando {espera}s."
                    )
                    time.sleep(espera)
                    intentos += 1
                    continue

                if response.status_code >= 500:
                    espera = (2 ** intentos) * 2
                    log.warning(
                        f"Error {response.status_code} Confluence. "
                        f"Reintento {intentos + 1} en {espera}s."
                    )
                    time.sleep(espera)
                    intentos += 1
                    continue

                if response.status_code == 404:
                    return {}

                response.raise_for_status()
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

## Lector de páginas

El lector extrae el contenido de una página en múltiples formatos. El formato más útil para el pipeline es el **storage format** (HTML interno de Confluence), que preserva la estructura de tablas, cabeceras y macros, y el **texto plano**, que el LLM puede procesar directamente sin ruido de etiquetas HTML.

```python
# lector_confluence.py

import re
from dataclasses import dataclass, field
from typing import Optional
from html.parser import HTMLParser


@dataclass
class ContenidoPagina:
    id: str
    titulo: str
    espacio: str
    url: str
    version: int
    fecha_modificacion: str
    autor_ultima_modificacion: str
    # Formatos del contenido
    storage_html: str           # HTML interno de Confluence
    texto_plano: str            # Texto limpio sin etiquetas
    tablas: list[dict]          # Tablas extraídas con estructura
    secciones: list[dict]       # Secciones por cabecera H1/H2/H3
    etiquetas: list[str]        # Labels de la página
    paginas_hijas: list[str]    # IDs de páginas hijas
    paginas_enlazadas: list[str]# IDs de páginas enlazadas internamente


class LectorConfluence:
    """
    Lee y estructura el contenido de páginas de Confluence
    en formatos procesables por el pipeline.
    """

    def __init__(self, cliente: ClienteConfluence):
        self.cliente = cliente

    def leer_pagina(self, page_id: str) -> Optional[ContenidoPagina]:
        """
        Lee una página por su ID y extrae todo el contenido
        en los formatos necesarios para el pipeline.
        """
        # Solicitar la página con expansiones necesarias
        datos = self.cliente.get(
            f"content/{page_id}",
            params={
                "expand": (
                    "body.storage,"      # Contenido HTML interno
                    "body.view,"         # HTML renderizado
                    "version,"           # Número de versión
                    "metadata.labels,"   # Etiquetas
                    "children.page,"     # Páginas hijas
                    "space"              # Información del espacio
                )
            }
        )

        if not datos:
            log.warning(f"Página {page_id} no encontrada o sin acceso")
            return None

        storage_html = datos.get("body", {}).get("storage", {}).get("value", "")

        # Extraer componentes estructurados
        texto_plano = self._extraer_texto_plano(storage_html)
        tablas = self._extraer_tablas(storage_html)
        secciones = self._extraer_secciones(storage_html)
        etiquetas = [
            label["name"]
            for label in datos.get(
                "metadata", {}
            ).get("labels", {}).get("results", [])
        ]
        paginas_hijas = [
            child["id"]
            for child in datos.get(
                "children", {}
            ).get("page", {}).get("results", [])
        ]
        paginas_enlazadas = self._extraer_enlaces_internos(
            storage_html, self.cliente.config.espacio_principal
        )

        # Construir URL de la página
        url = (
            f"{self.cliente.config.base_url}"
            f"{datos.get('_links', {}).get('webui', '')}"
        )

        # Información de versión y autoría
        version_info = datos.get("version", {})

        return ContenidoPagina(
            id=datos.get("id", page_id),
            titulo=datos.get("title", ""),
            espacio=datos.get("space", {}).get("key", ""),
            url=url,
            version=version_info.get("number", 0),
            fecha_modificacion=version_info.get("when", ""),
            autor_ultima_modificacion=version_info.get(
                "by", {}
            ).get("displayName", ""),
            storage_html=storage_html,
            texto_plano=texto_plano,
            tablas=tablas,
            secciones=secciones,
            etiquetas=etiquetas,
            paginas_hijas=paginas_hijas,
            paginas_enlazadas=paginas_enlazadas
        )

    def buscar_paginas(
        self,
        query: str,
        espacio: str = None,
        etiqueta: str = None,
        padre_id: str = None,
        max_resultados: int = 25
    ) -> list[dict]:
        """
        Busca páginas usando CQL (Confluence Query Language).
        Retorna metadatos básicos sin el contenido completo.
        """
        clausulas = ['type = "page"']

        if espacio:
            clausulas.append(f'space = "{espacio}"')
        elif self.cliente.config.espacio_principal:
            clausulas.append(
                f'space = "{self.cliente.config.espacio_principal}"'
            )

        if etiqueta:
            clausulas.append(f'label = "{etiqueta}"')

        if padre_id:
            clausulas.append(f'ancestor = "{padre_id}"')

        if query:
            clausulas.append(f'text ~ "{query}"')

        cql = " AND ".join(clausulas)

        resultado = self.cliente.get(
            "content/search",
            params={
                "cql": cql,
                "limit": max_resultados,
                "expand": "version,metadata.labels,space"
            }
        )

        return resultado.get("results", [])

    def leer_subárbol(
        self,
        pagina_raiz_id: str,
        profundidad_max: int = 3
    ) -> list[ContenidoPagina]:
        """
        Lee recursivamente una página y todas sus páginas hijas
        hasta la profundidad indicada. Útil para procesar secciones
        completas de documentación funcional.
        """
        paginas = []
        visitadas = set()

        def _leer_recursivo(page_id: str, nivel: int):
            if nivel > profundidad_max:
                return
            if page_id in visitadas:
                return
            visitadas.add(page_id)

            pagina = self.leer_pagina(page_id)
            if pagina:
                paginas.append(pagina)
                for hijo_id in pagina.paginas_hijas:
                    _leer_recursivo(hijo_id, nivel + 1)

        _leer_recursivo(pagina_raiz_id, 0)
        return paginas

    # ── Métodos de extracción de contenido ────────────────────────

    def _extraer_texto_plano(self, html: str) -> str:
        """
        Extrae texto plano del HTML de Confluence eliminando todas
        las etiquetas pero preservando la estructura de párrafos
        y la información de las celdas de tabla.
        """
        if not html:
            return ""

        class ExtractorTexto(HTMLParser):
            def __init__(self):
                super().__init__()
                self.textos = []
                self.en_tabla = False
                self.celda_actual = []
                self.fila_actual = []
                self.tabla_actual = []
                self._skip_tags = {"script", "style", "ac:parameter"}
                self._skip = False

            def handle_starttag(self, tag, attrs):
                if tag in self._skip_tags:
                    self._skip = True
                if tag == "table":
                    self.en_tabla = True
                    self.tabla_actual = []
                if tag in ("td", "th"):
                    self.celda_actual = []
                if tag == "tr":
                    self.fila_actual = []
                if tag in ("p", "h1", "h2", "h3", "h4", "li", "br"):
                    self.textos.append("\n")

            def handle_endtag(self, tag):
                if tag in self._skip_tags:
                    self._skip = False
                if tag in ("td", "th"):
                    texto_celda = "".join(self.celda_actual).strip()
                    self.fila_actual.append(texto_celda)
                    self.celda_actual = []
                if tag == "tr":
                    if self.fila_actual:
                        self.tabla_actual.append(self.fila_actual)
                        self.textos.append(" | ".join(self.fila_actual) + "\n")
                    self.fila_actual = []
                if tag == "table":
                    self.en_tabla = False
                    self.textos.append("\n")

            def handle_data(self, data):
                if self._skip:
                    return
                texto = data.strip()
                if texto:
                    if self.en_tabla and self.fila_actual is not None:
                        self.celda_actual.append(texto)
                    else:
                        self.textos.append(texto + " ")

        extractor = ExtractorTexto()
        extractor.feed(html)
        texto = "".join(extractor.textos)

        # Limpiar espacios múltiples y líneas vacías consecutivas
        texto = re.sub(r' +', ' ', texto)
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        return texto.strip()

    def _extraer_tablas(self, html: str) -> list[dict]:
        """
        Extrae las tablas del HTML de Confluence como estructuras
        de datos con cabecera y filas. Crucial para documentos
        funcionales que usan tablas de requisitos.
        """
        tablas = []
        patron_tabla = re.compile(
            r'<table[^>]*>(.*?)</table>',
            re.DOTALL | re.IGNORECASE
        )
        patron_fila = re.compile(
            r'<tr[^>]*>(.*?)</tr>',
            re.DOTALL | re.IGNORECASE
        )
        patron_celda = re.compile(
            r'<t[dh][^>]*>(.*?)</t[dh]>',
            re.DOTALL | re.IGNORECASE
        )

        for match_tabla in patron_tabla.finditer(html):
            contenido_tabla = match_tabla.group(1)
            filas = []

            for i, match_fila in enumerate(
                patron_fila.finditer(contenido_tabla)
            ):
                celdas = [
                    self._limpiar_html(celda.group(1))
                    for celda in patron_celda.finditer(match_fila.group(1))
                ]
                if celdas:
                    filas.append(celdas)

            if filas:
                tablas.append({
                    "cabecera": filas[0] if filas else [],
                    "filas": filas[1:] if len(filas) > 1 else [],
                    "n_columnas": len(filas[0]) if filas else 0,
                    "n_filas": len(filas) - 1 if len(filas) > 1 else 0
                })

        return tablas

    def _extraer_secciones(self, html: str) -> list[dict]:
        """
        Divide el contenido en secciones por cabeceras H1/H2/H3.
        Cada sección contiene su título, nivel y el texto que le sigue.
        """
        secciones = []
        patron = re.compile(
            r'<(h[123])[^>]*>(.*?)</\1>(.*?)(?=<h[123]|$)',
            re.DOTALL | re.IGNORECASE
        )

        for match in patron.finditer(html):
            nivel = int(match.group(1)[1])
            titulo = self._limpiar_html(match.group(2))
            contenido = self._extraer_texto_plano(match.group(3))

            if titulo.strip():
                secciones.append({
                    "nivel": nivel,
                    "titulo": titulo.strip(),
                    "contenido": contenido.strip()
                })

        return secciones

    def _extraer_enlaces_internos(
        self,
        html: str,
        espacio: str
    ) -> list[str]:
        """
        Extrae los IDs de páginas de Confluence enlazadas internamente.
        Útil para detectar dependencias documentales entre páginas.
        """
        ids = []
        # Formato de enlace interno en storage format de Confluence
        patron = re.compile(
            r'<ac:link><ri:page[^/]*/?>',
            re.IGNORECASE
        )
        patron_id = re.compile(r'ri:content-title="([^"]+)"')

        for match in patron_id.finditer(html):
            titulo_enlazado = match.group(1)
            if titulo_enlazado:
                ids.append(titulo_enlazado)

        return ids

    def _limpiar_html(self, html: str) -> str:
        """Elimina etiquetas HTML dejando solo el texto."""
        return re.sub(r'<[^>]+>', '', html).strip()
```

---

## Modo 1: Transformación de página a YAML borrador

El transformador es el componente más crítico de la integración. Usa el LLM para interpretar el contenido de la página de Confluence e inferir los campos de la plantilla YAML del punto 1. El resultado es un borrador que el analista revisa y valida, no un YAML listo para el pipeline.

### Estrategia de transformación

No todas las páginas de Confluence tienen la misma estructura. El transformador detecta el tipo de página antes de aplicar el prompt de extracción, para elegir la estrategia más adecuada.

```python
# transformador_confluence.py

import json
import yaml
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultadoTransformacion:
    pagina_id: str
    pagina_titulo: str
    tipo_detectado: str
    # Tipos: requisito_unico │ lista_requisitos │ especificacion_funcional │
    #        acta_reunion │ documento_vision │ no_procesable
    requisitos_generados: list[dict]    # YAMLs borrador generados
    confianza: float                    # 0-1, estimación del LLM
    campos_faltantes: list[str]         # Campos no encontrados en la página
    advertencias: list[str]
    requiere_revision_humana: bool


class TransformadorConfluence:
    """
    Transforma páginas de Confluence en borradores YAML
    usando el LLM como intérprete del contenido no estructurado.
    """

    UMBRAL_CONFIANZA_ALTA = 0.80
    # Por encima: el borrador puede revisarse rápidamente
    # Por debajo: requiere revisión detallada campo a campo

    def __init__(self, openai_client, glosario: dict):
        self.openai = openai_client
        self.glosario = glosario

    def transformar(
        self,
        pagina: ContenidoPagina
    ) -> ResultadoTransformacion:
        """
        Transforma una página de Confluence en uno o más borradores YAML.
        """
        # Detectar el tipo de página para elegir la estrategia
        tipo = self._detectar_tipo_pagina(pagina)

        if tipo == "no_procesable":
            return ResultadoTransformacion(
                pagina_id=pagina.id,
                pagina_titulo=pagina.titulo,
                tipo_detectado=tipo,
                requisitos_generados=[],
                confianza=0.0,
                campos_faltantes=[],
                advertencias=[
                    "La página no contiene contenido funcional procesable. "
                    "Puede ser una página de navegación, índice o documentación técnica."
                ],
                requiere_revision_humana=True
            )

        # Seleccionar la estrategia de extracción según el tipo
        if tipo == "lista_requisitos":
            return self._transformar_lista(pagina)
        elif tipo == "acta_reunion":
            return self._transformar_acta(pagina)
        else:
            # requisito_unico, especificacion_funcional, documento_vision
            return self._transformar_documento(pagina, tipo)

    def _detectar_tipo_pagina(self, pagina: ContenidoPagina) -> str:
        """
        Detecta el tipo de página para seleccionar la estrategia
        de transformación más adecuada. Usa heurísticas antes del LLM
        para evitar llamadas innecesarias a la API.
        """
        titulo = pagina.titulo.lower()
        etiquetas = [e.lower() for e in pagina.etiquetas]
        texto = pagina.texto_plano[:500].lower()

        # Heurísticas de tipo por etiqueta
        if "requisito" in etiquetas or "requirement" in etiquetas:
            return "requisito_unico"
        if "acta" in etiquetas or "meeting-notes" in etiquetas:
            return "acta_reunion"
        if "vision" in etiquetas or "roadmap" in etiquetas:
            return "documento_vision"

        # Heurísticas por título
        if any(p in titulo for p in ["acta", "reunión", "meeting", "notas"]):
            return "acta_reunion"
        if any(p in titulo for p in ["visión", "vision", "estrategia", "roadmap"]):
            return "documento_vision"
        if any(p in titulo for p in ["especificación", "funcional", "spec"]):
            return "especificacion_funcional"

        # Heurísticas por contenido: muchas tablas → posible lista de requisitos
        if len(pagina.tablas) >= 2:
            # Verificar si las tablas tienen cabeceras de requisito
            palabras_req = {
                "requisito", "requirement", "historia", "user story",
                "criterio", "aceptación", "actor", "descripción"
            }
            for tabla in pagina.tablas[:3]:
                cabecera_texto = " ".join(
                    c.lower() for c in tabla.get("cabecera", [])
                )
                if any(p in cabecera_texto for p in palabras_req):
                    return "lista_requisitos"

        # Si el texto es muy corto, probablemente no es procesable
        if len(pagina.texto_plano) < 200:
            return "no_procesable"

        # Por defecto: especificación funcional genérica
        return "especificacion_funcional"

    def _transformar_lista(
        self,
        pagina: ContenidoPagina
    ) -> ResultadoTransformacion:
        """
        Transforma páginas con listas o tablas de requisitos.
        Genera un YAML borrador por cada fila de requisito detectada.
        """
        # Preparar el contexto: usar las tablas extraídas
        tablas_texto = self._tablas_a_texto(pagina.tablas)

        prompt = f"""
Eres un analista funcional senior. La siguiente página de Confluence
contiene una lista o tabla de requisitos funcionales en formato no estructurado.

TÍTULO DE LA PÁGINA: {pagina.titulo}
URL: {pagina.url}

CONTENIDO DE LAS TABLAS:
{tablas_texto}

TEXTO ADICIONAL:
{pagina.texto_plano[:2000]}

GLOSARIO DEL PROYECTO (usar estos términos exactos):
{self._glosario_compacto()}

Tu tarea es extraer cada requisito identificable y convertirlo al formato
YAML del proyecto. Para cada requisito genera:

1. Un bloque YAML con los campos que puedas inferir del contenido
2. Marca con [PENDIENTE] los campos obligatorios que no puedas deducir
3. Usa el glosario para normalizar los términos

Para cada requisito genera:
- id: REQ-PENDIENTE (el analista asignará el ID definitivo)
- titulo: frase concisa sin verbos ambiguos
- actor: rol específico del glosario (o [PENDIENTE] si no se puede deducir)
- descripcion: qué necesita el usuario y por qué
- evento_disparador: qué activa este requisito
- criterios_aceptacion: al menos uno en formato dado/cuando/entonces
- excepciones: al menos una
- prioridad: must-have │ should-have │ could-have (deducir del contexto)
- epica: EP-PENDIENTE (el analista asignará)
- estado: borrador
- origen:
    fuente_documental: "{pagina.url}"
    pagina_confluence: "{pagina.id}"
    version_pagina: {pagina.version}

Al final del JSON incluye:
- confianza: número 0-1 que refleja tu certeza sobre la extracción
- campos_faltantes: lista de campos que no pudiste deducir
- advertencias: aspectos ambiguos o conflictivos detectados

Responde SOLO con JSON válido con esta estructura:
{{
  "requisitos": [
    {{
      "yaml_borrador": "... (YAML completo como string) ...",
      "confianza_requisito": 0.0-1.0
    }}
  ],
  "confianza_global": 0.0-1.0,
  "campos_faltantes": [],
  "advertencias": []
}}
"""
        return self._ejecutar_y_procesar(prompt, pagina, "lista_requisitos")

    def _transformar_documento(
        self,
        pagina: ContenidoPagina,
        tipo: str
    ) -> ResultadoTransformacion:
        """
        Transforma páginas de especificación funcional o documentos
        de visión en uno o varios YAMLs borrador.
        """
        # Dividir el contenido por secciones para no superar el límite de tokens
        contenido = self._preparar_contenido_para_llm(pagina)

        prompt = f"""
Eres un analista funcional senior con experiencia en ingeniería de requisitos.
La siguiente página de Confluence es una "{tipo.replace('_', ' ')}".

TÍTULO: {pagina.titulo}
URL: {pagina.url}

CONTENIDO:
{contenido}

GLOSARIO DEL PROYECTO:
{self._glosario_compacto()}

Tu tarea es extraer los requisitos funcionales que puedas identificar
en este documento y convertirlos al formato YAML del proyecto.

REGLAS DE EXTRACCIÓN:
1. Solo extrae requisitos funcionales concretos, no generalidades estratégicas
2. Un requisito = una funcionalidad = un evento de negocio
3. Si un párrafo mezcla varios requisitos, sepáralos en YAMLs distintos
4. Marca con [PENDIENTE] todo lo que no puedas deducir del texto
5. Usa siempre los términos del glosario para actores y entidades
6. No inventes información: si no está en el documento, marca como [PENDIENTE]

Para cada requisito identificado genera un YAML con todos los campos
de la plantilla estándar del proyecto, con origen:
  fuente_documental: "{pagina.url}"
  pagina_confluence: "{pagina.id}"
  version_pagina: {pagina.version}
  estado: borrador

Responde SOLO con JSON válido:
{{
  "requisitos": [
    {{
      "yaml_borrador": "...",
      "seccion_origen": "nombre de la sección del documento de donde se extrajo",
      "confianza_requisito": 0.0-1.0
    }}
  ],
  "confianza_global": 0.0-1.0,
  "campos_faltantes": [],
  "advertencias": [],
  "n_requisitos_posibles": 0
}}
"""
        return self._ejecutar_y_procesar(prompt, pagina, tipo)

    def _transformar_acta(
        self,
        pagina: ContenidoPagina
    ) -> ResultadoTransformacion:
        """
        Transforma actas de reunión en requisitos borrador.
        Las actas contienen compromisos y decisiones que a menudo
        no llegan al repositorio de requisitos.
        """
        prompt = f"""
Eres un analista funcional. La siguiente página de Confluence es un
acta de reunión o documento de notas.

TÍTULO: {pagina.titulo}
URL: {pagina.url}

CONTENIDO:
{pagina.texto_plano[:3000]}

Tu tarea es identificar los compromisos, decisiones y necesidades funcionales
que emergen de esta reunión y que podrían convertirse en requisitos.

CRITERIOS DE SELECCIÓN:
- Incluir: compromisos concretos del tipo "el sistema debe...", "se ha decidido que...",
  "el usuario necesita...", "acordamos implementar..."
- Excluir: opiniones, conversaciones, contexto de reunión, temas pendientes vagos

Para cada requisito potencial identificado, genera un YAML borrador marcando
claramente con [PENDIENTE] todo lo que necesite validación con el equipo.
El nivel de confianza debe ser bajo (0.3-0.6) ya que el origen es un acta.

Responde SOLO con JSON válido:
{{
  "requisitos": [
    {{
      "yaml_borrador": "...",
      "fragmento_origen": "texto exacto del acta del que se extrae",
      "confianza_requisito": 0.0-1.0
    }}
  ],
  "confianza_global": 0.0-1.0,
  "campos_faltantes": [],
  "advertencias": [
    "Los requisitos extraídos de actas requieren validación explícita con los asistentes"
  ]
}}
"""
        return self._ejecutar_y_procesar(prompt, pagina, "acta_reunion")

    def _ejecutar_y_procesar(
        self,
        prompt: str,
        pagina: ContenidoPagina,
        tipo: str
    ) -> ResultadoTransformacion:
        """
        Ejecuta el prompt y procesa la respuesta del LLM.
        """
        try:
            response = self.openai.chat.completions.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            texto = response.choices[0].message.content
            # Limpiar posibles bloques de código markdown
            texto = texto.replace("```json", "").replace("```", "").strip()
            datos = json.loads(texto)

            requisitos_generados = []
            for req_data in datos.get("requisitos", []):
                yaml_str = req_data.get("yaml_borrador", "")
                try:
                    # Validar que el YAML es parseable
                    yaml.safe_load(yaml_str)
                    requisitos_generados.append({
                        "yaml": yaml_str,
                        "confianza": req_data.get("confianza_requisito", 0.5),
                        "seccion_origen": req_data.get("seccion_origen", ""),
                        "fragmento_origen": req_data.get("fragmento_origen", "")
                    })
                except yaml.YAMLError as e:
                    log.warning(
                        f"YAML inválido en transformación de {pagina.id}: {e}"
                    )

            confianza_global = datos.get("confianza_global", 0.5)

            return ResultadoTransformacion(
                pagina_id=pagina.id,
                pagina_titulo=pagina.titulo,
                tipo_detectado=tipo,
                requisitos_generados=requisitos_generados,
                confianza=confianza_global,
                campos_faltantes=datos.get("campos_faltantes", []),
                advertencias=datos.get("advertencias", []),
                requiere_revision_humana=confianza_global < self.UMBRAL_CONFIANZA_ALTA
            )

        except json.JSONDecodeError as e:
            log.error(f"Error parseando respuesta LLM para {pagina.id}: {e}")
            return ResultadoTransformacion(
                pagina_id=pagina.id,
                pagina_titulo=pagina.titulo,
                tipo_detectado=tipo,
                requisitos_generados=[],
                confianza=0.0,
                campos_faltantes=["todos"],
                advertencias=[f"Error en la transformación: {e}"],
                requiere_revision_humana=True
            )

    def _preparar_contenido_para_llm(
        self,
        pagina: ContenidoPagina,
        max_chars: int = 4000
    ) -> str:
        """
        Prepara el contenido de la página para el prompt del LLM,
        priorizando las secciones más relevantes si el contenido
        supera el límite de caracteres.
        """
        if len(pagina.texto_plano) <= max_chars:
            return pagina.texto_plano

        # Si hay secciones, priorizar las que tienen palabras clave funcionales
        palabras_funcionales = {
            "requisito", "funcionalidad", "usuario", "sistema",
            "debe", "necesita", "criterio", "aceptación", "flujo",
            "proceso", "regla", "negocio", "actor"
        }

        secciones_priorizadas = []
        secciones_secundarias = []

        for seccion in pagina.secciones:
            texto_seccion = seccion["titulo"] + " " + seccion["contenido"]
            relevancia = sum(
                1 for p in palabras_funcionales
                if p in texto_seccion.lower()
            )
            if relevancia >= 2:
                secciones_priorizadas.append(seccion)
            else:
                secciones_secundarias.append(seccion)

        contenido = ""
        for seccion in secciones_priorizadas + secciones_secundarias:
            bloque = (
                f"\n## {seccion['titulo']}\n{seccion['contenido']}\n"
            )
            if len(contenido) + len(bloque) <= max_chars:
                contenido += bloque
            else:
                break

        # Añadir indicación de que el contenido está truncado
        if len(contenido) < len(pagina.texto_plano):
            contenido += (
                "\n[NOTA: Contenido parcial. "
                "El documento original tiene más secciones.]"
            )

        return contenido

    def _tablas_a_texto(self, tablas: list[dict]) -> str:
        """Convierte las tablas extraídas a texto estructurado para el prompt."""
        if not tablas:
            return "Sin tablas detectadas."

        resultado = []
        for i, tabla in enumerate(tablas, 1):
            resultado.append(f"\nTABLA {i}:")
            if tabla.get("cabecera"):
                resultado.append("Cabecera: " + " | ".join(tabla["cabecera"]))
            for fila in tabla.get("filas", []):
                resultado.append("  " + " | ".join(str(c) for c in fila))

        return "\n".join(resultado)

    def _glosario_compacto(self) -> str:
        """Genera el bloque compacto del glosario para el prompt."""
        actores = self.glosario.get("actores", [])
        entidades = self.glosario.get("entidades", [])

        lineas = []
        for a in actores[:5]:
            sinonimos = a.get("sinonimos_no_oficiales", [])
            lineas.append(
                f"Actor oficial: '{a['nombre_oficial']}' "
                f"[NO usar: {', '.join(sinonimos[:3])}]"
            )
        for e in entidades[:5]:
            sinonimos = e.get("sinonimos_no_oficiales", [])
            lineas.append(
                f"Entidad oficial: '{e['nombre_oficial']}' "
                f"[NO usar: {', '.join(sinonimos[:3])}]"
            )

        return "\n".join(lineas) if lineas else "Glosario no disponible."
```

---

## Modo 2: Indexación en el vector store RAG

Las páginas de Confluence que no se transforman en YAMLs pueden indexarse directamente en el vector store del punto 7 como contexto documental. Esto permite que el pipeline recupere información de los documentos existentes al generar artefactos, sin necesidad de transformarlos completamente.

```python
# indexador_confluence_rag.py

import hashlib
import json
import psycopg2


class IndexadorConfluenceRAG:
    """
    Indexa páginas de Confluence en el vector store del pipeline RAG
    como contexto documental complementario a los requisitos YAML.
    """

    CHUNK_MAX_CHARS = 800
    # Tamaño máximo de cada chunk para mantener coherencia semántica
    # sin desperdiciar tokens en recuperaciones irrelevantes

    def __init__(self, repositorio_rag):
        self.rag = repositorio_rag

    def indexar_pagina(
        self,
        pagina: ContenidoPagina,
        tipo_contenido: str = "documentacion_funcional"
    ) -> dict:
        """
        Indexa una página de Confluence dividida en chunks semánticos.
        Cada sección de la página se indexa como un chunk independiente.
        """
        chunks_indexados = 0
        chunks_omitidos = 0

        # Chunk 1: resumen de la página completa
        resumen_texto = (
            f"Página de Confluence: {pagina.titulo}\n"
            f"Espacio: {pagina.espacio}\n"
            f"URL: {pagina.url}\n"
            f"Etiquetas: {', '.join(pagina.etiquetas)}\n"
            f"Contenido resumido: {pagina.texto_plano[:400]}"
        )
        self._indexar_chunk(
            chunk_id=f"CONFLUENCE::{pagina.id}::resumen",
            texto=resumen_texto,
            metadatos={
                "tipo": tipo_contenido,
                "subtipo": "resumen_pagina",
                "pagina_id": pagina.id,
                "pagina_titulo": pagina.titulo,
                "espacio": pagina.espacio,
                "url": pagina.url,
                "version": pagina.version,
                "fecha_modificacion": pagina.fecha_modificacion
            }
        )
        chunks_indexados += 1

        # Chunk por sección: cada sección de la página como chunk propio
        for i, seccion in enumerate(pagina.secciones):
            contenido_seccion = seccion.get("contenido", "")
            if len(contenido_seccion) < 50:
                # Secciones muy cortas no aportan contexto útil
                chunks_omitidos += 1
                continue

            # Dividir secciones largas en sub-chunks
            sub_chunks = self._dividir_en_chunks(contenido_seccion)

            for j, sub_chunk in enumerate(sub_chunks):
                texto_chunk = (
                    f"De la página '{pagina.titulo}', "
                    f"sección '{seccion['titulo']}':\n{sub_chunk}"
                )
                self._indexar_chunk(
                    chunk_id=(
                        f"CONFLUENCE::{pagina.id}::s{i}::c{j}"
                    ),
                    texto=texto_chunk,
                    metadatos={
                        "tipo": tipo_contenido,
                        "subtipo": "seccion",
                        "pagina_id": pagina.id,
                        "pagina_titulo": pagina.titulo,
                        "seccion_titulo": seccion["titulo"],
                        "seccion_nivel": seccion["nivel"],
                        "espacio": pagina.espacio,
                        "url": pagina.url,
                        "version": pagina.version
                    }
                )
                chunks_indexados += 1

        # Chunks de tablas: indexar cada tabla como contexto de datos
        for i, tabla in enumerate(pagina.tablas):
            if not tabla.get("filas"):
                continue

            texto_tabla = self._tabla_a_texto_natural(
                tabla, pagina.titulo
            )
            if len(texto_tabla) > 50:
                self._indexar_chunk(
                    chunk_id=f"CONFLUENCE::{pagina.id}::tabla{i}",
                    texto=texto_tabla,
                    metadatos={
                        "tipo": tipo_contenido,
                        "subtipo": "tabla",
                        "pagina_id": pagina.id,
                        "pagina_titulo": pagina.titulo,
                        "espacio": pagina.espacio,
                        "url": pagina.url,
                        "n_filas": tabla["n_filas"],
                        "n_columnas": tabla["n_columnas"]
                    }
                )
                chunks_indexados += 1

        return {
            "pagina_id": pagina.id,
            "chunks_indexados": chunks_indexados,
            "chunks_omitidos": chunks_omitidos
        }

    def _indexar_chunk(
        self,
        chunk_id: str,
        texto: str,
        metadatos: dict
    ):
        """Indexa un chunk individual en el vector store."""
        hash_contenido = hashlib.md5(texto.encode()).hexdigest()
        embedding = self.rag.embeder_texto(texto)

        with psycopg2.connect(**self.rag.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO chunks_requisitos
                        (id, texto, tipo, embedding, metadatos, hash_contenido)
                    VALUES (%s, %s, %s, %s::vector, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        texto          = EXCLUDED.texto,
                        embedding      = EXCLUDED.embedding,
                        metadatos      = EXCLUDED.metadatos,
                        hash_contenido = EXCLUDED.hash_contenido,
                        fecha_indexado = NOW(),
                        activo         = TRUE
                    WHERE chunks_requisitos.hash_contenido != EXCLUDED.hash_contenido
                """, (
                    chunk_id,
                    texto,
                    metadatos.get("tipo", "documentacion_funcional"),
                    embedding,
                    json.dumps(metadatos),
                    hash_contenido
                ))
            conn.commit()

    def _dividir_en_chunks(self, texto: str) -> list[str]:
        """
        Divide un texto largo en chunks respetando párrafos completos.
        """
        if len(texto) <= self.CHUNK_MAX_CHARS:
            return [texto]

        parrafos = texto.split("\n\n")
        chunks = []
        chunk_actual = ""

        for parrafo in parrafos:
            if len(chunk_actual) + len(parrafo) <= self.CHUNK_MAX_CHARS:
                chunk_actual += parrafo + "\n\n"
            else:
                if chunk_actual:
                    chunks.append(chunk_actual.strip())
                chunk_actual = parrafo + "\n\n"

        if chunk_actual.strip():
            chunks.append(chunk_actual.strip())

        return chunks if chunks else [texto[:self.CHUNK_MAX_CHARS]]

    def _tabla_a_texto_natural(
        self,
        tabla: dict,
        titulo_pagina: str
    ) -> str:
        """
        Convierte una tabla a texto natural para mejorar
        la recuperación semántica.
        """
        cabecera = tabla.get("cabecera", [])
        filas = tabla.get("filas", [])

        if not cabecera or not filas:
            return ""

        lineas = [f"Tabla de '{titulo_pagina}' con columnas: {', '.join(cabecera)}"]
        for fila in filas[:10]:  # Máximo 10 filas por chunk de tabla
            if len(fila) == len(cabecera):
                pares = [
                    f"{cabecera[i]}: {fila[i]}"
                    for i in range(len(cabecera))
                    if fila[i]
                ]
                lineas.append(" | ".join(pares))

        return "\n".join(lineas)
```

---

## Modo 3: Vigilancia de cambios mediante webhook

Confluence puede notificar cambios en páginas mediante webhooks. El receptor actualiza el estado de sincronización en el repositorio y alerta al analista cuando una página vinculada a un requisito ha sido modificada.

```python
# webhook_confluence.py

from fastapi import FastAPI, Request, BackgroundTasks
import yaml
import os

app = FastAPI(title="Webhook Confluence → Pipeline")


@app.post("/webhook/confluence")
async def recibir_evento_confluence(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Confluence llama a este endpoint cuando ocurren eventos en páginas.
    Configurar en: Confluence Admin → Webhooks.

    Eventos a suscribir:
      - page_updated
      - page_created
      - page_deleted
      - page_trashed
    """
    payload = await request.json()
    evento = payload.get("event", "")
    pagina_datos = payload.get("page", {})
    pagina_id = str(pagina_datos.get("id", ""))
    pagina_titulo = pagina_datos.get("title", "")
    pagina_version = pagina_datos.get("version", {}).get("number", 0)
    autor = pagina_datos.get("version", {}).get(
        "by", {}
    ).get("displayName", "desconocido")

    if not pagina_id:
        return {"status": "ignorado", "motivo": "Sin ID de página"}

    if evento == "page_updated":
        background_tasks.add_task(
            _procesar_actualizacion_pagina,
            pagina_id, pagina_titulo, pagina_version, autor
        )
        return {"status": "procesando", "pagina_id": pagina_id}

    if evento in ("page_deleted", "page_trashed"):
        background_tasks.add_task(
            _procesar_eliminacion_pagina,
            pagina_id, pagina_titulo
        )
        return {"status": "procesando_eliminacion", "pagina_id": pagina_id}

    return {"status": "ignorado", "evento": evento}


async def _procesar_actualizacion_pagina(
    pagina_id: str,
    pagina_titulo: str,
    nueva_version: int,
    autor: str
):
    """
    Procesa la actualización de una página de Confluence.
    Busca requisitos vinculados a esa página y genera alertas.
    """
    requisitos_vinculados = _buscar_requisitos_por_pagina(pagina_id)

    if not requisitos_vinculados:
        # Re-indexar la página en el RAG aunque no tenga requisitos vinculados
        # por si el contenido nuevo es relevante para futuros requisitos
        log.info(
            f"Página {pagina_id} actualizada sin requisitos vinculados. "
            f"Re-indexando en RAG."
        )
        return

    # Generar alerta para cada requisito vinculado
    for req_id in requisitos_vinculados:
        alerta = {
            "tipo": "pagina_confluence_actualizada",
            "requisito_id": req_id,
            "pagina_id": pagina_id,
            "pagina_titulo": pagina_titulo,
            "nueva_version": nueva_version,
            "autor_cambio": autor,
            "mensaje": (
                f"La página de Confluence '{pagina_titulo}' vinculada al "
                f"requisito {req_id} ha sido actualizada a la versión "
                f"{nueva_version} por {autor}. Revisar si el requisito "
                f"necesita actualización."
            ),
            "accion_recomendada": (
                "Comparar el contenido actualizado de la página con el "
                "YAML del requisito y actualizar los campos afectados."
            )
        }

        # Notificar por el canal configurado (Slack, email, etc.)
        _notificar_alerta_confluence(alerta)

        # Registrar en el log de gobierno
        log.warning(
            f"ALERTA CONFLUENCE: {alerta['mensaje']}"
        )


async def _procesar_eliminacion_pagina(
    pagina_id: str,
    pagina_titulo: str
):
    """Procesa la eliminación de una página vinculada a requisitos."""
    requisitos_vinculados = _buscar_requisitos_por_pagina(pagina_id)

    for req_id in requisitos_vinculados:
        alerta = {
            "tipo": "pagina_confluence_eliminada",
            "requisito_id": req_id,
            "pagina_id": pagina_id,
            "pagina_titulo": pagina_titulo,
            "mensaje": (
                f"La página de Confluence '{pagina_titulo}' vinculada al "
                f"requisito {req_id} ha sido eliminada. La fuente documental "
                f"del requisito ya no está disponible."
            ),
            "accion_recomendada": (
                "Verificar si el requisito tiene suficiente contexto en "
                "el YAML o si necesita una nueva fuente documental."
            )
        }
        _notificar_alerta_confluence(alerta)

    # Desactivar los chunks de la página eliminada en el vector store
    import psycopg2
    with psycopg2.connect(**os.environ.get("DB_CONFIG", {})) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE chunks_requisitos
                SET activo = FALSE
                WHERE metadatos->>'pagina_id' = %s
            """, (pagina_id,))
        conn.commit()


def _buscar_requisitos_por_pagina(pagina_id: str) -> list[str]:
    """
    Busca en el repositorio los requisitos que declaran la página
    dada como fuente documental en el campo origen.
    """
    req_ids = []
    ruta_requisitos = os.environ.get("REPO_REQUISITOS", "./requisitos")

    for root, _, files in os.walk(ruta_requisitos):
        for archivo in files:
            if not archivo.endswith(".yaml"):
                continue
            try:
                with open(os.path.join(root, archivo)) as f:
                    req = yaml.safe_load(f)
                if not req:
                    continue
                pagina_origen = (
                    req.get("origen", {}).get("pagina_confluence", "")
                )
                if str(pagina_origen) == str(pagina_id):
                    req_ids.append(req.get("id", ""))
            except Exception:
                continue

    return [r for r in req_ids if r]


def _notificar_alerta_confluence(alerta: dict):
    """Envía la alerta por el canal configurado."""
    log.info(
        f"Notificación Confluence: {alerta['tipo']} "
        f"para {alerta.get('requisito_id', 'desconocido')}"
    )
    # En producción: webhook Slack, email o mensaje en Teams
```

---

## Comando de línea de operación

Los tres modos se exponen como subcomandos del orquestador del punto 13, manteniendo la misma interfaz de línea de comandos que el resto del pipeline.

```bash
# Modo 1: Transformar una página concreta en YAML borrador
python orchestrator.py \
  --confluence-transform \
  --page-id 123456789 \
  --output ./borradores/

# Transformar todas las páginas bajo una página raíz
python orchestrator.py \
  --confluence-transform \
  --page-id 123456789 \
  --recursive \
  --depth 2 \
  --output ./borradores/

# Transformar páginas con una etiqueta específica
python orchestrator.py \
  --confluence-transform \
  --label "especificacion-funcional" \
  --space FACT \
  --output ./borradores/

# Modo 2: Indexar una página o subárbol en el RAG
python orchestrator.py \
  --confluence-index \
  --page-id 123456789

python orchestrator.py \
  --confluence-index \
  --space FACT \
  --label "documentacion-funcional"

# Modo 3: Verificar el estado de sincronización de las páginas vinculadas
python orchestrator.py \
  --confluence-sync-check
```

La salida de la transformación en consola:

```
══════════════════════════════════════════════════════════
  TRANSFORMACIÓN CONFLUENCE → YAML
  Página: "Especificación funcional - Módulo Facturación"
  ID: 123456789 · Versión: 14
══════════════════════════════════════════════════════════

  [1] Leyendo página y extrayendo contenido...
      ✓ 3.421 caracteres · 2 tablas · 8 secciones

  [2] Detectando tipo de página...
      ✓ Tipo: especificacion_funcional

  [3] Transformando con IA...
      ✓ 6 requisitos identificados
      ✓ Confianza global: 71%

  RESULTADO POR REQUISITO:
  ──────────────────────────────────────────────────────
  Req 1  87% conf  Filtrar facturas por rango de fechas
         Campos pendientes: epica, id
  Req 2  74% conf  Exportar listado de facturas a CSV
         Campos pendientes: epica, id, excepciones
  Req 3  65% conf  Configurar columnas visibles en listado
         Campos pendientes: epica, id, criterios_aceptacion
  Req 4  58% conf  [REVISIÓN MANUAL] Gestión de permisos
         Campos pendientes: actor, epica, id, criterios_aceptacion
  Req 5  71% conf  Archivar facturas del ejercicio anterior
         Campos pendientes: epica, id
  Req 6  82% conf  Aprobar factura con importe superior al umbral
         Campos pendientes: epica, id
  ──────────────────────────────────────────────────────

  ⚠ 2 advertencias:
    → La sección "Rendimiento" mezcla NFRs con requisitos funcionales
    → El término "operador" no está en el glosario (posible sinónimo de "Gestor de facturación")

  Borradores guardados en: ./borradores/pagina-123456789/
    REQ-BORRADOR-001.yaml
    REQ-BORRADOR-002.yaml
    REQ-BORRADOR-003.yaml
    REQ-BORRADOR-004.yaml  [REVISIÓN MANUAL REQUERIDA]
    REQ-BORRADOR-005.yaml
    REQ-BORRADOR-006.yaml

══════════════════════════════════════════════════════════
  Tiempo total: 18.3s
══════════════════════════════════════════════════════════
```

---

## Limitaciones y gestión de expectativas

**La transformación no es sustituto del análisis funcional.** Los YAMLs generados son borradores que el analista debe revisar con el mismo rigor que aplicaría a cualquier requisito antes de que entre al pipeline. La confianza que reporta el LLM es una estimación interna, no una garantía de correctitud funcional. Un YAML con 90% de confianza puede tener el actor incorrecto si el documento usa un término no oficial que el glosario no ha registrado todavía.

**El contenido no estructurado genera ambigüedad estructural.** Los documentos de Confluence escritos en prosa libre son ambiguos por diseño: el mismo párrafo puede interpretarse como un requisito, como una regla de negocio o como el contexto de un requisito. El LLM elige una interpretación, pero el analista debe verificar que la elección es correcta para cada caso.

**Las páginas con mucho contenido se truncan.** El límite de tokens del LLM impone un máximo de contenido procesable en cada llamada. El transformador aplica una estrategia de priorización de secciones funcionales, pero puede perder información relevante en páginas muy largas. Para documentos extensos, el enfoque recomendado es transformar sección por sección usando `--recursive` con profundidad 1, no procesar la página completa de una vez.

**El webhook requiere acceso de red entrante.** El receptor de webhooks de Confluence necesita ser accesible desde los servidores de Atlassian Cloud o desde la instalación on-premise. En organizaciones con redes muy restrictivas, la alternativa es el modo de polling: verificar periódicamente si las páginas vinculadas a requisitos han sido modificadas comparando la versión almacenada en el origen del requisito con la versión actual de la página.

**La indexación RAG es complementaria, no sustitutiva.** Los chunks de páginas de Confluence en el vector store aportan contexto documental, pero tienen menor precisión que los chunks de requisitos YAML porque su estructura es menos determinista. El pipeline los pondera con menor peso que los requisitos validados en las consultas de recuperación de contexto del punto 7.
