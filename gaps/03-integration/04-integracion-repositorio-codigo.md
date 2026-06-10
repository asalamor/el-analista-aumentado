# Integración con repositorio de código

## El problema que resuelve

La trazabilidad del modelo operativo, tal como está construida en el punto 9, llega hasta las historias de usuario y los test cases. Desde el punto de vista del analista y del product owner, esa trazabilidad es suficiente para gobernar el backlog. Desde el punto de vista del equipo técnico y de la auditoría, no lo es: la cadena que va del requisito de negocio al código que lo implementa tiene un eslabón roto entre las tareas de Jira y los commits del repositorio.

Ese eslabón roto tiene consecuencias concretas. Cuando aparece un bug en producción, el equipo no puede trazar rápidamente qué requisito de negocio introdujo el comportamiento defectuoso. Cuando se revisa un pull request, el revisor no tiene acceso inmediato al criterio de aceptación que la historia debería satisfacer. Cuando la dirección pregunta si una épica está completamente implementada, la respuesta requiere consultar manualmente Jira, el repositorio y los resultados de QA por separado.

La integración con el repositorio de código cierra ese eslabón. Vincula automáticamente los commits y pull requests con las historias y tareas de Jira o ADO, sin depender de que el desarrollador recuerde escribir la referencia en el mensaje del commit. Actualiza el grafo de trazabilidad del punto 9 con cada cambio de código, de forma que la cadena completa requisito → historia → tarea → commit → test queda visible en tiempo real para cualquier miembro del equipo.

---

## Estrategia de vinculación: explícita e inferida

La vinculación entre código y work items puede ocurrir de dos formas con diferente nivel de fiabilidad.

La **vinculación explícita** se produce cuando el desarrollador incluye la referencia al issue en el mensaje del commit o en el título del pull request. Es la más precisa pero depende de disciplina del equipo. La referencia puede tener múltiples formatos según la convención de la organización.

La **vinculación inferida** se produce cuando el mensaje del commit no incluye referencia explícita. El sistema analiza el texto del mensaje usando el LLM y lo cruza semánticamente con las historias abiertas del sprint activo para inferir a cuál pertenece. Es menos precisa pero garantiza trazabilidad incluso cuando el desarrollador olvida la referencia.

El sistema usa siempre la vinculación explícita cuando existe, y complementa con inferencia solo para los commits sin referencia. Los vínculos inferidos se presentan diferenciados en el grafo de trazabilidad con un nivel de confianza que refleja la certeza de la inferencia.

```
Commit / Pull Request
        │
        ├── ¿Contiene referencia explícita? ─────────────────────────────
        │   (PROJ-123, #123, REQ-023, fixes #123, closes FACT-47)        │
        │                                                                 ▼
        │                                               Vinculación directa
        │                                               Confianza: 1.0
        │
        └── Sin referencia explícita ───────────────────────────────────
                │
                ▼
        Análisis semántico del mensaje
        contra historias del sprint activo
                │
                ├── Similitud ≥ 0.80 → Vinculación inferida (alta confianza)
                ├── Similitud 0.65-0.79 → Vinculación inferida (media confianza)
                └── Similitud < 0.65 → Commit no vinculado (alerta)
```

---

## Arquitectura de la integración

```
Repositorio de código
(GitHub / GitLab / Azure Repos / Bitbucket)
        │
        ├── Webhook push / PR events ────────────────────────────────────
        │   (en tiempo real al hacer push o abrir PR)                    │
        │                                                                 ▼
        │                                               [Receptor de webhooks]
        │                                               Parsea el evento y
        │                                               extrae metadatos
        │
        ├── GitHub Actions / GitLab CI ──────────────────────────────────
        │   (en el pipeline de CI/CD)                                    │
        │                                                                 ▼
        │                                               [Step de trazabilidad]
        │                                               Se ejecuta como paso
        │                                               del pipeline CI/CD
        │
        └── Polling periódico ──────────────────────────────────────────
            (para repositorios sin webhooks configurables)               │
                                                                         ▼
                                                         [Poller de commits]
                                                         Consulta la API cada
                                                         N minutos
        │
        ▼
[Analizador de commits]
Extrae referencias explícitas o infiere
la vinculación semánticamente
        │
        ├── Actualiza el grafo de trazabilidad del punto 9
        ├── Actualiza el estado del work item en Jira/ADO
        ├── Publica comentario en el PR con el contexto funcional
        └── Detecta commits que no están vinculados a ningún trabajo planificado
```

---

## Configuración y cliente base

El sistema soporta los cuatro repositorios más frecuentes con un cliente base unificado que abstrae las diferencias de API.

```python
# config_repos.py

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RepoConfig:
    proveedor: str = os.getenv("REPO_PROVEEDOR", "github")
    # github │ gitlab │ azure_repos │ bitbucket

    base_url: str = os.getenv("REPO_BASE_URL", "https://api.github.com")
    # GitHub:       https://api.github.com
    # GitLab Cloud: https://gitlab.com/api/v4
    # GitLab Self:  https://tu-gitlab.com/api/v4
    # Azure Repos:  https://dev.azure.com/{org}
    # Bitbucket:    https://api.bitbucket.org/2.0

    token: str = os.getenv("REPO_TOKEN", "")
    # GitHub:       Personal Access Token o GitHub App token
    # GitLab:       Personal Access Token o Project Access Token
    # Azure Repos:  PAT (mismo que ADO del punto de integración ADO)
    # Bitbucket:    App password o OAuth token

    organizacion: str = os.getenv("REPO_ORG", "")
    repositorio: str = os.getenv("REPO_NAME", "")
    rama_principal: str = os.getenv("REPO_MAIN_BRANCH", "main")

    # Convenciones de referencia a issues en mensajes de commit
    # El sistema detecta automáticamente estas variantes
    patrones_referencia: list[str] = field(default_factory=lambda: [
        r"(?i)(?:fixes?|closes?|resolves?|refs?|references?)\s+#?(\w+-\d+|\d+)",
        r"#(\d+)",
        r"\b([A-Z]+-\d+)\b",             # JIRA-123, FACT-47
        r"\bREQ-(\d{3})\b",              # REQ-023
        r"\bUS-(\d{3})\b",               # US-047
    ])

    # Rama de trabajo que indica que un commit está en progreso activo
    prefijos_rama_feature: list[str] = field(default_factory=lambda: [
        "feature/", "feat/", "fix/", "bugfix/",
        "hotfix/", "story/", "us/", "task/"
    ])

    webhook_secret: str = os.getenv("REPO_WEBHOOK_SECRET", "")
    # Secreto para verificar la autenticidad de los webhooks

    def validar(self) -> list[str]:
        errores = []
        if not self.token:
            errores.append("REPO_TOKEN no configurado")
        if not self.organizacion:
            errores.append("REPO_ORG no configurada")
        if not self.repositorio:
            errores.append("REPO_NAME no configurado")
        if self.proveedor not in (
            "github", "gitlab", "azure_repos", "bitbucket"
        ):
            errores.append(
                f"REPO_PROVEEDOR '{self.proveedor}' no válido"
            )
        return errores
```

```python
# cliente_repo.py

import requests
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger("pipeline.repo")


@dataclass
class CommitInfo:
    sha: str
    mensaje: str
    autor: str
    email: str
    fecha: str
    rama: str
    url: str
    archivos_modificados: list[str]
    adiciones: int
    eliminaciones: int
    # Campos rellenados por el analizador
    referencias_explicitas: list[str] = None
    issue_inferido: Optional[str] = None
    confianza_inferencia: float = 0.0


@dataclass
class PRInfo:
    id: str
    titulo: str
    descripcion: str
    autor: str
    rama_origen: str
    rama_destino: str
    estado: str          # open │ merged │ closed
    url: str
    commits: list[str]   # SHAs de los commits del PR
    labels: list[str]
    reviewers: list[str]
    fecha_creacion: str
    fecha_merge: Optional[str]
    referencias_explicitas: list[str] = None


class ClienteRepoBase(ABC):
    """Interfaz común para todos los clientes de repositorio."""

    def __init__(self, config: RepoConfig):
        self.config = config
        self.session = requests.Session()
        self._configurar_auth()
        self._ultima_llamada = 0.0

    @abstractmethod
    def _configurar_auth(self):
        pass

    def _respetar_rate_limit(self, pausa_ms: int = 200):
        ahora = time.time() * 1000
        diferencia = ahora - self._ultima_llamada
        if diferencia < pausa_ms:
            time.sleep((pausa_ms - diferencia) / 1000)
        self._ultima_llamada = time.time() * 1000

    def _get(self, url: str, params: dict = None) -> dict:
        self._respetar_rate_limit()
        response = self.session.get(url, params=params, timeout=30)
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def obtener_commit(self, sha: str) -> Optional[CommitInfo]:
        pass

    @abstractmethod
    def obtener_commits_rama(
        self,
        rama: str,
        desde: str = None,
        hasta: str = None,
        max_commits: int = 50
    ) -> list[CommitInfo]:
        pass

    @abstractmethod
    def obtener_pr(self, pr_id: str) -> Optional[PRInfo]:
        pass

    @abstractmethod
    def publicar_comentario_pr(
        self,
        pr_id: str,
        comentario: str
    ) -> bool:
        pass

    @abstractmethod
    def obtener_commits_pr(self, pr_id: str) -> list[CommitInfo]:
        pass


class ClienteGitHub(ClienteRepoBase):
    """Cliente para la API REST de GitHub."""

    def _configurar_auth(self):
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        })
        self._base = (
            f"{self.config.base_url}/repos/"
            f"{self.config.organizacion}/{self.config.repositorio}"
        )

    def obtener_commit(self, sha: str) -> Optional[CommitInfo]:
        datos = self._get(f"{self._base}/commits/{sha}")
        if not datos:
            return None
        commit = datos.get("commit", {})
        stats = datos.get("stats", {})
        archivos = [f["filename"] for f in datos.get("files", [])]
        return CommitInfo(
            sha=datos.get("sha", sha),
            mensaje=commit.get("message", ""),
            autor=commit.get("author", {}).get("name", ""),
            email=commit.get("author", {}).get("email", ""),
            fecha=commit.get("author", {}).get("date", ""),
            rama=self.config.rama_principal,
            url=datos.get("html_url", ""),
            archivos_modificados=archivos,
            adiciones=stats.get("additions", 0),
            eliminaciones=stats.get("deletions", 0)
        )

    def obtener_commits_rama(
        self,
        rama: str,
        desde: str = None,
        hasta: str = None,
        max_commits: int = 50
    ) -> list[CommitInfo]:
        params = {"sha": rama, "per_page": min(max_commits, 100)}
        if desde:
            params["since"] = desde
        if hasta:
            params["until"] = hasta

        datos = self._get(f"{self._base}/commits", params)
        if not datos or not isinstance(datos, list):
            return []

        commits = []
        for item in datos[:max_commits]:
            commit = item.get("commit", {})
            commits.append(CommitInfo(
                sha=item.get("sha", ""),
                mensaje=commit.get("message", ""),
                autor=commit.get("author", {}).get("name", ""),
                email=commit.get("author", {}).get("email", ""),
                fecha=commit.get("author", {}).get("date", ""),
                rama=rama,
                url=item.get("html_url", ""),
                archivos_modificados=[],
                adiciones=0,
                eliminaciones=0
            ))
        return commits

    def obtener_pr(self, pr_id: str) -> Optional[PRInfo]:
        datos = self._get(f"{self._base}/pulls/{pr_id}")
        if not datos:
            return None
        return PRInfo(
            id=str(datos.get("number", pr_id)),
            titulo=datos.get("title", ""),
            descripcion=datos.get("body", "") or "",
            autor=datos.get("user", {}).get("login", ""),
            rama_origen=datos.get("head", {}).get("ref", ""),
            rama_destino=datos.get("base", {}).get("ref", ""),
            estado=datos.get("state", ""),
            url=datos.get("html_url", ""),
            commits=[],
            labels=[l["name"] for l in datos.get("labels", [])],
            reviewers=[
                r["login"]
                for r in datos.get("requested_reviewers", [])
            ],
            fecha_creacion=datos.get("created_at", ""),
            fecha_merge=datos.get("merged_at")
        )

    def obtener_commits_pr(self, pr_id: str) -> list[CommitInfo]:
        datos = self._get(f"{self._base}/pulls/{pr_id}/commits")
        if not datos or not isinstance(datos, list):
            return []
        commits = []
        for item in datos:
            commit = item.get("commit", {})
            commits.append(CommitInfo(
                sha=item.get("sha", ""),
                mensaje=commit.get("message", ""),
                autor=commit.get("author", {}).get("name", ""),
                email=commit.get("author", {}).get("email", ""),
                fecha=commit.get("author", {}).get("date", ""),
                rama="",
                url=item.get("html_url", ""),
                archivos_modificados=[],
                adiciones=0,
                eliminaciones=0
            ))
        return commits

    def publicar_comentario_pr(
        self,
        pr_id: str,
        comentario: str
    ) -> bool:
        try:
            response = self.session.post(
                f"{self._base}/issues/{pr_id}/comments",
                json={"body": comentario},
                timeout=30
            )
            response.raise_for_status()
            return True
        except Exception as e:
            log.warning(f"Error publicando comentario en PR #{pr_id}: {e}")
            return False


class ClienteGitLab(ClienteRepoBase):
    """Cliente para la API REST de GitLab."""

    def _configurar_auth(self):
        self.session.headers.update({
            "PRIVATE-TOKEN": self.config.token,
            "Content-Type": "application/json"
        })
        proyecto_encoded = (
            f"{self.config.organizacion}%2F{self.config.repositorio}"
        )
        self._base = (
            f"{self.config.base_url}/projects/{proyecto_encoded}"
        )

    def obtener_commit(self, sha: str) -> Optional[CommitInfo]:
        datos = self._get(f"{self._base}/repository/commits/{sha}")
        if not datos:
            return None
        return CommitInfo(
            sha=datos.get("id", sha),
            mensaje=datos.get("message", ""),
            autor=datos.get("author_name", ""),
            email=datos.get("author_email", ""),
            fecha=datos.get("authored_date", ""),
            rama=self.config.rama_principal,
            url=datos.get("web_url", ""),
            archivos_modificados=[],
            adiciones=datos.get("stats", {}).get("additions", 0),
            eliminaciones=datos.get("stats", {}).get("deletions", 0)
        )

    def obtener_commits_rama(
        self,
        rama: str,
        desde: str = None,
        hasta: str = None,
        max_commits: int = 50
    ) -> list[CommitInfo]:
        params = {"ref_name": rama, "per_page": min(max_commits, 100)}
        if desde:
            params["since"] = desde
        if hasta:
            params["until"] = hasta
        datos = self._get(
            f"{self._base}/repository/commits", params
        )
        if not datos or not isinstance(datos, list):
            return []
        return [
            CommitInfo(
                sha=item.get("id", ""),
                mensaje=item.get("message", ""),
                autor=item.get("author_name", ""),
                email=item.get("author_email", ""),
                fecha=item.get("authored_date", ""),
                rama=rama,
                url=item.get("web_url", ""),
                archivos_modificados=[],
                adiciones=0,
                eliminaciones=0
            )
            for item in datos[:max_commits]
        ]

    def obtener_pr(self, pr_id: str) -> Optional[PRInfo]:
        # GitLab los llama Merge Requests
        datos = self._get(
            f"{self._base}/merge_requests/{pr_id}"
        )
        if not datos:
            return None
        return PRInfo(
            id=str(datos.get("iid", pr_id)),
            titulo=datos.get("title", ""),
            descripcion=datos.get("description", "") or "",
            autor=datos.get("author", {}).get("name", ""),
            rama_origen=datos.get("source_branch", ""),
            rama_destino=datos.get("target_branch", ""),
            estado=datos.get("state", ""),
            url=datos.get("web_url", ""),
            commits=[],
            labels=datos.get("labels", []),
            reviewers=[
                r["name"]
                for r in datos.get("reviewers", [])
            ],
            fecha_creacion=datos.get("created_at", ""),
            fecha_merge=datos.get("merged_at")
        )

    def obtener_commits_pr(self, pr_id: str) -> list[CommitInfo]:
        datos = self._get(
            f"{self._base}/merge_requests/{pr_id}/commits"
        )
        if not datos or not isinstance(datos, list):
            return []
        return [
            CommitInfo(
                sha=item.get("id", ""),
                mensaje=item.get("message", ""),
                autor=item.get("author_name", ""),
                email=item.get("author_email", ""),
                fecha=item.get("authored_date", ""),
                rama="",
                url="",
                archivos_modificados=[],
                adiciones=0,
                eliminaciones=0
            )
            for item in datos
        ]

    def publicar_comentario_pr(
        self,
        pr_id: str,
        comentario: str
    ) -> bool:
        try:
            response = self.session.post(
                f"{self._base}/merge_requests/{pr_id}/notes",
                json={"body": comentario},
                timeout=30
            )
            response.raise_for_status()
            return True
        except Exception as e:
            log.warning(f"Error publicando nota en MR !{pr_id}: {e}")
            return False


def crear_cliente_repo(config: RepoConfig) -> ClienteRepoBase:
    """Factory que instancia el cliente correcto según el proveedor."""
    clientes = {
        "github":      ClienteGitHub,
        "gitlab":      ClienteGitLab,
    }
    clase = clientes.get(config.proveedor)
    if not clase:
        raise ValueError(
            f"Proveedor '{config.proveedor}' no soportado. "
            f"Disponibles: {list(clientes.keys())}"
        )
    return clase(config)
```

---

## Analizador de commits

El analizador combina extracción de referencias explícitas con inferencia semántica para producir el vínculo entre cada commit y su work item correspondiente.

```python
# analizador_commits.py

import re
import logging
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger("pipeline.repo")


@dataclass
class VinculoCommit:
    sha: str
    issue_key: str
    tipo_vinculo: str       # explicito │ inferido_rama │ inferido_semantico
    confianza: float        # 1.0 explícito, 0.5-0.9 inferido
    metodo_deteccion: str   # Descripción del método usado
    rama: str


class AnalizadorCommits:
    """
    Analiza mensajes de commit y nombres de rama para establecer
    vínculos con work items de Jira o ADO.
    Combina extracción de patrones con inferencia semántica RAG.
    """

    def __init__(
        self,
        config: RepoConfig,
        repositorio_rag,
        openai_client
    ):
        self.config = config
        self.rag = repositorio_rag
        self.openai = openai_client

        # Compilar patrones de referencia
        self._patrones = [
            re.compile(p) for p in config.patrones_referencia
        ]

    def analizar_commit(
        self,
        commit: CommitInfo,
        issues_sprint_activo: list[dict]
    ) -> VinculoCommit:
        """
        Analiza un commit e intenta vincularlo a un work item.
        Prioriza referencias explícitas sobre inferencia.
        """
        # 1. Buscar referencias explícitas en el mensaje
        referencias = self._extraer_referencias_explicitas(commit.mensaje)

        if referencias:
            issue_key = self._resolver_referencia(
                referencias[0], issues_sprint_activo
            )
            if issue_key:
                commit.referencias_explicitas = referencias
                return VinculoCommit(
                    sha=commit.sha,
                    issue_key=issue_key,
                    tipo_vinculo="explicito",
                    confianza=1.0,
                    metodo_deteccion=(
                        f"Referencia explícita en mensaje: "
                        f"'{referencias[0]}'"
                    ),
                    rama=commit.rama
                )

        # 2. Inferir desde el nombre de la rama
        issue_desde_rama = self._extraer_issue_de_rama(commit.rama)
        if issue_desde_rama:
            issue_key = self._resolver_referencia(
                issue_desde_rama, issues_sprint_activo
            )
            if issue_key:
                return VinculoCommit(
                    sha=commit.sha,
                    issue_key=issue_key,
                    tipo_vinculo="inferido_rama",
                    confianza=0.90,
                    metodo_deteccion=(
                        f"Referencia en nombre de rama: '{commit.rama}'"
                    ),
                    rama=commit.rama
                )

        # 3. Inferencia semántica si hay issues del sprint activo
        if issues_sprint_activo and commit.mensaje.strip():
            vinculo_semantico = self._inferir_semanticamente(
                commit, issues_sprint_activo
            )
            if vinculo_semantico:
                commit.issue_inferido = vinculo_semantico.issue_key
                commit.confianza_inferencia = vinculo_semantico.confianza
                return vinculo_semantico

        # 4. Sin vínculo encontrado
        return VinculoCommit(
            sha=commit.sha,
            issue_key="",
            tipo_vinculo="sin_vinculo",
            confianza=0.0,
            metodo_deteccion="No se encontró referencia ni similitud suficiente",
            rama=commit.rama
        )

    def _extraer_referencias_explicitas(
        self,
        mensaje: str
    ) -> list[str]:
        """
        Extrae todas las referencias a issues del mensaje de commit.
        Aplica todos los patrones configurados.
        """
        referencias = []
        for patron in self._patrones:
            for match in patron.finditer(mensaje):
                ref = match.group(1) if match.lastindex else match.group(0)
                ref = ref.strip()
                if ref and ref not in referencias:
                    referencias.append(ref)
        return referencias

    def _extraer_issue_de_rama(self, nombre_rama: str) -> Optional[str]:
        """
        Extrae la referencia a un issue del nombre de la rama.
        Soporta convenciones como:
          feature/FACT-47-filtrar-facturas
          feat/123-nueva-funcionalidad
          fix/US-047
        """
        if not nombre_rama:
            return None

        # Eliminar el prefijo de tipo de rama
        rama_sin_prefijo = nombre_rama
        for prefijo in self.config.prefijos_rama_feature:
            if nombre_rama.startswith(prefijo):
                rama_sin_prefijo = nombre_rama[len(prefijo):]
                break

        # Buscar patrones de issue en el nombre limpio
        for patron in self._patrones:
            match = patron.search(rama_sin_prefijo)
            if match:
                return match.group(1) if match.lastindex else match.group(0)

        return None

    def _resolver_referencia(
        self,
        referencia: str,
        issues_sprint: list[dict]
    ) -> Optional[str]:
        """
        Normaliza una referencia extraída al formato estándar del issue.
        Si es un número sin prefijo, intenta resolverlo contra los issues
        del sprint activo.
        """
        referencia = referencia.strip().upper()

        # Si ya tiene formato de issue key (FACT-47, US-047), usar directamente
        if re.match(r'^[A-Z]+-\d+$', referencia):
            return referencia

        # Si es solo un número, buscar en los issues del sprint
        if re.match(r'^\d+$', referencia):
            numero = int(referencia)
            for issue in issues_sprint:
                key = issue.get("key", "")
                if key.endswith(f"-{numero}"):
                    return key

        return referencia if referencia else None

    def _inferir_semanticamente(
        self,
        commit: CommitInfo,
        issues_sprint: list[dict]
    ) -> Optional[VinculoCommit]:
        """
        Infiere el issue al que pertenece un commit usando similitud
        semántica entre el mensaje del commit y los títulos/descripciones
        de los issues del sprint activo.
        """
        if not issues_sprint:
            return None

        # Construir el texto de búsqueda combinando mensaje y archivos
        archivos_relevantes = [
            f for f in commit.archivos_modificados
            if not any(
                f.endswith(ext)
                for ext in [".lock", ".min.js", ".map", ".svg"]
            )
        ][:5]

        texto_busqueda = commit.mensaje
        if archivos_relevantes:
            texto_busqueda += " " + " ".join(archivos_relevantes)

        # Buscar en el vector store contra las historias del sprint
        resultados = self.rag.buscar_por_similitud(
            query_texto=texto_busqueda,
            filtros={"chunk_tipo": "identidad_requisito"},
            top_k=3
        )

        if not resultados:
            return None

        mejor = resultados[0]

        # Filtrar por umbral mínimo de confianza
        UMBRAL_INFERENCIA_ALTA = 0.80
        UMBRAL_INFERENCIA_MEDIA = 0.65

        if mejor.similitud < UMBRAL_INFERENCIA_MEDIA:
            return None

        # Obtener el issue key del requisito más similar
        req_id = mejor.metadatos.get("requisito_id", "")

        # Buscar el issue de Jira/ADO correspondiente al requisito
        issue_key = self._buscar_issue_de_requisito(req_id, issues_sprint)

        if not issue_key:
            return None

        confianza = mejor.similitud
        nivel = (
            "alta" if confianza >= UMBRAL_INFERENCIA_ALTA
            else "media"
        )

        return VinculoCommit(
            sha=commit.sha,
            issue_key=issue_key,
            tipo_vinculo="inferido_semantico",
            confianza=round(confianza, 2),
            metodo_deteccion=(
                f"Similitud semántica {nivel} ({confianza:.0%}) "
                f"con '{mejor.texto[:60]}...'"
            ),
            rama=commit.rama
        )

    def _buscar_issue_de_requisito(
        self,
        req_id: str,
        issues_sprint: list[dict]
    ) -> Optional[str]:
        """
        Busca el issue de Jira/ADO asociado a un requisito en el
        grafo de trazabilidad.
        """
        import psycopg2
        try:
            with psycopg2.connect(
                **self.rag.db_config
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT n.id
                        FROM nodos_trazabilidad n
                        JOIN aristas_trazabilidad a
                          ON a.destino_id = n.id
                        WHERE a.origen_id = %s
                          AND a.tipo_relacion = 'vincula'
                          AND n.tipo IN ('issue_jira', 'historia')
                          AND n.activo = TRUE
                        LIMIT 1
                    """, (req_id,))
                    fila = cur.fetchone()
                    return fila[0] if fila else None
        except Exception:
            return None
```

---

## Receptor de webhooks

El receptor procesa los eventos de push y pull request en tiempo real, sin necesidad de polling.

```python
# webhook_repo.py

import hmac
import hashlib
import json
import logging
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException

log = logging.getLogger("pipeline.repo")
app = FastAPI(title="Webhook Repositorio → Trazabilidad")


def _verificar_firma_github(
    payload_bytes: bytes,
    firma: str,
    secreto: str
) -> bool:
    """Verifica la firma HMAC-SHA256 de GitHub."""
    if not firma or not secreto:
        return True  # Sin secreto configurado, omitir verificación
    mac = hmac.new(
        secreto.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256
    )
    firma_esperada = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(firma_esperada, firma)


def _verificar_firma_gitlab(
    token: str,
    secreto: str
) -> bool:
    """Verifica el token secreto de GitLab."""
    if not secreto:
        return True
    return hmac.compare_digest(token, secreto)


@app.post("/webhook/github")
async def recibir_webhook_github(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Recibe eventos de GitHub (push, pull_request).
    Configurar en: Repo Settings → Webhooks → Add webhook.
    Content type: application/json
    Events: Push, Pull requests
    """
    payload_bytes = await request.body()
    firma = request.headers.get("X-Hub-Signature-256", "")

    if not _verificar_firma_github(
        payload_bytes, firma, config_repo.webhook_secret
    ):
        raise HTTPException(status_code=401, detail="Firma inválida")

    payload = json.loads(payload_bytes)
    evento = request.headers.get("X-GitHub-Event", "")

    if evento == "push":
        background_tasks.add_task(
            _procesar_push_github, payload
        )
    elif evento == "pull_request":
        background_tasks.add_task(
            _procesar_pr_github, payload
        )

    return {"status": "aceptado", "evento": evento}


@app.post("/webhook/gitlab")
async def recibir_webhook_gitlab(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Recibe eventos de GitLab (Push Hook, Merge Request Hook).
    Configurar en: Project Settings → Webhooks.
    Events: Push events, Merge request events
    """
    token = request.headers.get("X-Gitlab-Token", "")
    if not _verificar_firma_gitlab(token, config_repo.webhook_secret):
        raise HTTPException(status_code=401, detail="Token inválido")

    payload = await request.json()
    evento = request.headers.get("X-Gitlab-Event", "")

    if evento == "Push Hook":
        background_tasks.add_task(
            _procesar_push_gitlab, payload
        )
    elif evento == "Merge Request Hook":
        background_tasks.add_task(
            _procesar_mr_gitlab, payload
        )

    return {"status": "aceptado", "evento": evento}


async def _procesar_push_github(payload: dict):
    """Procesa un evento push de GitHub."""
    rama = payload.get("ref", "").replace("refs/heads/", "")
    commits_raw = payload.get("commits", [])

    if not commits_raw:
        return

    issues_sprint = _obtener_issues_sprint_activo()

    for commit_raw in commits_raw:
        commit = CommitInfo(
            sha=commit_raw.get("id", ""),
            mensaje=commit_raw.get("message", ""),
            autor=commit_raw.get("author", {}).get("name", ""),
            email=commit_raw.get("author", {}).get("email", ""),
            fecha=commit_raw.get("timestamp", ""),
            rama=rama,
            url=commit_raw.get("url", ""),
            archivos_modificados=(
                commit_raw.get("added", []) +
                commit_raw.get("modified", []) +
                commit_raw.get("removed", [])
            ),
            adiciones=0,
            eliminaciones=0
        )

        await _procesar_commit(commit, issues_sprint)


async def _procesar_push_gitlab(payload: dict):
    """Procesa un evento push de GitLab."""
    rama = payload.get("ref", "").replace("refs/heads/", "")
    commits_raw = payload.get("commits", [])

    if not commits_raw:
        return

    issues_sprint = _obtener_issues_sprint_activo()

    for commit_raw in commits_raw:
        commit = CommitInfo(
            sha=commit_raw.get("id", ""),
            mensaje=commit_raw.get("message", ""),
            autor=commit_raw.get("author", {}).get("name", ""),
            email=commit_raw.get("author", {}).get("email", ""),
            fecha=commit_raw.get("timestamp", ""),
            rama=rama,
            url=commit_raw.get("url", ""),
            archivos_modificados=(
                commit_raw.get("added", []) +
                commit_raw.get("modified", []) +
                commit_raw.get("removed", [])
            ),
            adiciones=0,
            eliminaciones=0
        )

        await _procesar_commit(commit, issues_sprint)


async def _procesar_commit(
    commit: CommitInfo,
    issues_sprint: list[dict]
):
    """
    Lógica central de procesamiento de un commit individual.
    Analiza el vínculo, actualiza la trazabilidad y Jira/ADO.
    """
    vinculo = analizador.analizar_commit(commit, issues_sprint)

    if vinculo.tipo_vinculo == "sin_vinculo":
        log.warning(
            f"Commit sin vincular: {commit.sha[:8]} "
            f"'{commit.mensaje[:60]}'"
        )
        _registrar_commit_no_vinculado(commit)
        return

    # Registrar el nodo del commit en el grafo de trazabilidad
    motor_trazabilidad.registrar_nodo(Nodo(
        id=f"COMMIT::{commit.sha[:12]}",
        tipo="commit",
        titulo=commit.mensaje[:100],
        estado="merged" if commit.rama == config_repo.rama_principal else "en_rama",
        metadatos={
            "sha": commit.sha,
            "rama": commit.rama,
            "autor": commit.autor,
            "email": commit.email,
            "fecha": commit.fecha,
            "url": commit.url,
            "archivos": commit.archivos_modificados[:10],
            "adiciones": commit.adiciones,
            "eliminaciones": commit.eliminaciones
        }
    ))

    # Registrar la arista commit → issue
    motor_trazabilidad.registrar_arista(Arista(
        origen_id=f"COMMIT::{commit.sha[:12]}",
        destino_id=vinculo.issue_key,
        tipo_relacion="implementa",
        confianza=vinculo.confianza,
        origen_relacion=f"webhook_{config_repo.proveedor}",
        metadatos={
            "tipo_vinculo": vinculo.tipo_vinculo,
            "metodo_deteccion": vinculo.metodo_deteccion
        }
    ))

    # Actualizar el work item en Jira/ADO con el commit
    _actualizar_issue_con_commit(vinculo.issue_key, commit, vinculo)

    log.info(
        f"Commit {commit.sha[:8]} vinculado a {vinculo.issue_key} "
        f"({vinculo.tipo_vinculo}, {vinculo.confianza:.0%})"
    )


async def _procesar_pr_github(payload: dict):
    """Procesa eventos de pull request de GitHub."""
    accion = payload.get("action", "")
    pr_data = payload.get("pull_request", {})

    if accion not in ("opened", "reopened", "closed", "ready_for_review"):
        return

    pr = PRInfo(
        id=str(pr_data.get("number", "")),
        titulo=pr_data.get("title", ""),
        descripcion=pr_data.get("body", "") or "",
        autor=pr_data.get("user", {}).get("login", ""),
        rama_origen=pr_data.get("head", {}).get("ref", ""),
        rama_destino=pr_data.get("base", {}).get("ref", ""),
        estado=pr_data.get("state", ""),
        url=pr_data.get("html_url", ""),
        commits=[],
        labels=[l["name"] for l in pr_data.get("labels", [])],
        reviewers=[
            r["login"]
            for r in pr_data.get("requested_reviewers", [])
        ],
        fecha_creacion=pr_data.get("created_at", ""),
        fecha_merge=pr_data.get("merged_at")
    )

    await _procesar_pr(pr, accion)


async def _procesar_mr_gitlab(payload: dict):
    """Procesa eventos de merge request de GitLab."""
    attrs = payload.get("object_attributes", {})
    accion = attrs.get("action", "")

    if accion not in ("open", "reopen", "merge", "close"):
        return

    pr = PRInfo(
        id=str(attrs.get("iid", "")),
        titulo=attrs.get("title", ""),
        descripcion=attrs.get("description", "") or "",
        autor=payload.get("user", {}).get("name", ""),
        rama_origen=attrs.get("source_branch", ""),
        rama_destino=attrs.get("target_branch", ""),
        estado=attrs.get("state", ""),
        url=attrs.get("url", ""),
        commits=[],
        labels=attrs.get("labels", []),
        reviewers=[],
        fecha_creacion=attrs.get("created_at", ""),
        fecha_merge=attrs.get("merged_at")
    )

    accion_norm = {
        "open": "opened", "reopen": "reopened",
        "merge": "closed", "close": "closed"
    }.get(accion, accion)

    await _procesar_pr(pr, accion_norm)


async def _procesar_pr(pr: PRInfo, accion: str):
    """
    Lógica central de procesamiento de un PR/MR.
    Al abrirse: publica el contexto funcional como comentario.
    Al mergearse: actualiza la trazabilidad con todos sus commits.
    """
    issues_sprint = _obtener_issues_sprint_activo()

    # Extraer referencias del título y descripción del PR
    referencias = analizador._extraer_referencias_explicitas(
        f"{pr.titulo} {pr.descripcion}"
    )

    # Inferir desde el nombre de la rama si no hay referencias
    if not referencias:
        ref_rama = analizador._extraer_issue_de_rama(pr.rama_origen)
        if ref_rama:
            referencias = [ref_rama]

    issue_key = (
        analizador._resolver_referencia(referencias[0], issues_sprint)
        if referencias else None
    )

    pr.referencias_explicitas = referencias

    if accion in ("opened", "ready_for_review") and issue_key:
        # Publicar el contexto funcional como comentario en el PR
        comentario = _generar_comentario_contexto_funcional(
            pr, issue_key
        )
        cliente_repo.publicar_comentario_pr(pr.id, comentario)

    if accion == "closed" and pr.estado in ("merged", "closed"):
        # Registrar el nodo del PR en el grafo
        motor_trazabilidad.registrar_nodo(Nodo(
            id=f"PR::{pr.id}",
            tipo="pull_request",
            titulo=pr.titulo,
            estado="merged" if pr.fecha_merge else "closed",
            metadatos={
                "rama_origen": pr.rama_origen,
                "rama_destino": pr.rama_destino,
                "autor": pr.autor,
                "url": pr.url,
                "fecha_merge": pr.fecha_merge
            }
        ))

        if issue_key:
            motor_trazabilidad.registrar_arista(Arista(
                origen_id=f"PR::{pr.id}",
                destino_id=issue_key,
                tipo_relacion="implementa",
                confianza=1.0 if referencias else 0.85,
                origen_relacion=f"webhook_{config_repo.proveedor}"
            ))

        log.info(
            f"PR #{pr.id} mergeado: "
            f"{'vinculado a ' + issue_key if issue_key else 'sin vincular'}"
        )
```

---

## Comentario automático de contexto funcional en el PR

Cuando se abre un pull request vinculado a un issue, el sistema publica automáticamente un comentario con el contexto funcional: los criterios de aceptación de la historia, las reglas de negocio relevantes y los test cases que deben pasar. Esto elimina la necesidad de que el revisor navegue entre Jira y el repositorio para entender qué debe validar.

```python
# generador_comentario_pr.py

def _generar_comentario_contexto_funcional(
    pr: PRInfo,
    issue_key: str
) -> str:
    """
    Genera el comentario de contexto funcional que se publica
    en el PR al abrirse. Recupera la información del grafo
    de trazabilidad y del repositorio de requisitos.
    """
    # Recuperar la traza completa del issue
    traza = consultor_trazabilidad.traza_completa_requisito(
        _obtener_req_id_de_issue(issue_key)
    )

    historia = traza.get("historias", [{}])[0] if traza.get("historias") else {}
    criterios = traza.get("criterios_aceptacion", [])
    test_cases = traza.get("test_cases", [])

    n_tc_pasados = sum(
        1 for tc in test_cases if tc.get("estado") == "pasado"
    )
    n_tc_total = len(test_cases)

    # Construir el comentario en Markdown
    comentario = f"""## 🔗 Contexto funcional — {issue_key}

**Historia:** {historia.get('titulo', issue_key)}

### Criterios de aceptación

"""
    if criterios:
        for ac in criterios[:5]:
            comentario += (
                f"**{ac.get('id', '')}**\n"
                f"- **Dado** {ac.get('dado', '')}\n"
                f"- **Cuando** {ac.get('cuando', '')}\n"
                f"- **Entonces** {ac.get('entonces', '')}\n\n"
            )
    else:
        comentario += "_No se encontraron criterios de aceptación en el repositorio._\n\n"

    comentario += f"""### Estado de test cases

"""
    if test_cases:
        estado_icono = (
            "✅" if n_tc_pasados == n_tc_total and n_tc_total > 0
            else "⚠️" if n_tc_pasados > 0
            else "❌"
        )
        comentario += (
            f"{estado_icono} **{n_tc_pasados}/{n_tc_total}** "
            f"test cases pasando\n\n"
        )
        for tc in test_cases[:5]:
            icono_tc = {
                "pasado": "✅", "fallido": "❌", "pendiente": "⏸"
            }.get(tc.get("estado", ""), "⏸")
            comentario += f"{icono_tc} {tc.get('titulo', tc.get('id', ''))}\n"
    else:
        comentario += "⏸ Sin test cases registrados en el pipeline.\n\n"

    comentario += f"""
---
_Generado automáticamente por el pipeline de análisis funcional._
_[Ver requisito completo]({_obtener_url_issue(issue_key)})_
"""
    return comentario
```

---

## Integración en GitHub Actions y GitLab CI

Para repositorios donde el webhook no es suficiente o se requiere trazabilidad en el pipeline de CI, el sistema ofrece un step reutilizable.

### GitHub Actions

```yaml
# .github/workflows/trazabilidad-pipeline.yml

name: Trazabilidad funcional

on:
  push:
    branches: [main, develop, "feature/**", "feat/**", "fix/**"]
  pull_request:
    types: [opened, ready_for_review, closed]

jobs:
  vincular-trazabilidad:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0    # Historial completo para análisis de commits

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependencias del pipeline
        run: pip install -r requirements-pipeline.txt

      - name: Vincular commits con issues
        env:
          REPO_TOKEN:        ${{ secrets.GITHUB_TOKEN }}
          REPO_PROVEEDOR:    github
          REPO_ORG:          ${{ github.repository_owner }}
          REPO_NAME:         ${{ github.event.repository.name }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          DB_HOST:           ${{ secrets.DB_HOST }}
          DB_PASSWORD:       ${{ secrets.DB_PASSWORD }}
          JIRA_BASE_URL:     ${{ vars.JIRA_BASE_URL }}
          JIRA_API_TOKEN:    ${{ secrets.JIRA_API_TOKEN }}
          JIRA_USER_EMAIL:   ${{ vars.JIRA_USER_EMAIL }}
        run: |
          if [ "${{ github.event_name }}" = "push" ]; then
            python orchestrator.py \
              --vincular-commits \
              --sha ${{ github.sha }} \
              --rama ${{ github.ref_name }}
          elif [ "${{ github.event_name }}" = "pull_request" ]; then
            python orchestrator.py \
              --vincular-pr \
              --pr-id ${{ github.event.pull_request.number }} \
              --accion ${{ github.event.action }}
          fi

      - name: Verificar cobertura de trazabilidad
        if: github.event_name == 'pull_request'
        run: |
          python orchestrator.py \
            --verificar-trazabilidad \
            --pr-id ${{ github.event.pull_request.number }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml (fragmento)

trazabilidad-funcional:
  stage: .pre
  image: python:3.11-slim
  script:
    - pip install -r requirements-pipeline.txt
    - |
      if [ "$CI_PIPELINE_SOURCE" = "push" ]; then
        python orchestrator.py \
          --vincular-commits \
          --sha $CI_COMMIT_SHA \
          --rama $CI_COMMIT_REF_NAME
      elif [ "$CI_PIPELINE_SOURCE" = "merge_request_event" ]; then
        python orchestrator.py \
          --vincular-pr \
          --pr-id $CI_MERGE_REQUEST_IID \
          --accion $CI_MERGE_REQUEST_EVENT_TYPE
      fi
  variables:
    REPO_PROVEEDOR: gitlab
    REPO_ORG: $CI_PROJECT_NAMESPACE
    REPO_NAME: $CI_PROJECT_NAME
  rules:
    - if: $CI_PIPELINE_SOURCE == "push"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: true  # La trazabilidad no debe bloquear el pipeline de CI
```

---

## Dashboard de trazabilidad de código

El grafo de trazabilidad del punto 9, enriquecido con los commits, permite responder preguntas que antes requerían inspección manual.

```python
# dashboard_trazabilidad_codigo.py

class DashboardTrazabilidadCodigo:
    """
    Genera métricas de trazabilidad entre el código y los work items.
    """

    def __init__(self, consultor_trazabilidad):
        self.consultor = consultor_trazabilidad

    def cobertura_de_codigo_por_sprint(self, sprint_id: str) -> dict:
        """
        Para cada historia del sprint, calcula si tiene commits asociados.
        Responde: ¿qué historias comprometidas no tienen código todavía?
        """
        cobertura_sprint = self.consultor.cobertura_sprint(sprint_id)
        historias = cobertura_sprint.get("historias", [])

        resultado = []
        for historia in historias:
            us_id = historia.get("historia_id", "")
            n_commits = self._contar_commits_de_historia(us_id)
            n_prs = self._contar_prs_de_historia(us_id)

            resultado.append({
                **historia,
                "commits_asociados": n_commits,
                "prs_asociados": n_prs,
                "tiene_codigo": n_commits > 0,
                "semaforo_codigo": (
                    "🟢" if n_prs > 0 and historia.get("estado_historia") == "Done"
                    else "🟡" if n_commits > 0
                    else "🔴"
                )
            })

        historias_sin_codigo = [
            h for h in resultado
            if not h["tiene_codigo"]
            and h.get("estado_historia") in ("In Progress", "Active")
        ]

        return {
            "sprint_id": sprint_id,
            "historias": resultado,
            "historias_sin_codigo": historias_sin_codigo,
            "alerta": (
                f"⚠ {len(historias_sin_codigo)} historia(s) en progreso "
                f"sin commits asociados."
                if historias_sin_codigo else None
            )
        }

    def commits_sin_vincular(self, rama: str = None) -> dict:
        """
        Lista los commits que no están vinculados a ningún work item.
        Son candidatos a scope creep o a referencias olvidadas.
        """
        import psycopg2
        with psycopg2.connect(**self.consultor.db.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT n.id, n.titulo, n.metadatos->>'fecha' AS fecha,
                           n.metadatos->>'autor' AS autor,
                           n.metadatos->>'rama' AS rama
                    FROM nodos_trazabilidad n
                    WHERE n.tipo = 'commit'
                      AND n.activo = TRUE
                      AND NOT EXISTS (
                        SELECT 1 FROM aristas_trazabilidad a
                        WHERE a.origen_id = n.id
                          AND a.tipo_relacion = 'implementa'
                          AND a.activo = TRUE
                      )
                    ORDER BY n.metadatos->>'fecha' DESC
                    LIMIT 50
                """)
                filas = cur.fetchall()

        commits = [
            {
                "commit_id": f[0],
                "mensaje": f[1],
                "fecha": f[2],
                "autor": f[3],
                "rama": f[4]
            }
            for f in filas
        ]

        return {
            "total_sin_vincular": len(commits),
            "commits": commits,
            "recomendacion": (
                "Revisar los commits sin vincular para detectar "
                "trabajo no planificado o referencias olvidadas."
                if commits else "Todos los commits están vinculados."
            )
        }

    def _contar_commits_de_historia(self, historia_id: str) -> int:
        import psycopg2
        with psycopg2.connect(**self.consultor.db.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM nodos_trazabilidad n
                    JOIN aristas_trazabilidad a ON a.origen_id = n.id
                    WHERE n.tipo = 'commit'
                      AND a.destino_id = %s
                      AND a.tipo_relacion = 'implementa'
                      AND n.activo = TRUE
                      AND a.activo = TRUE
                """, (historia_id,))
                return cur.fetchone()[0] or 0

    def _contar_prs_de_historia(self, historia_id: str) -> int:
        import psycopg2
        with psycopg2.connect(**self.consultor.db.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM nodos_trazabilidad n
                    JOIN aristas_trazabilidad a ON a.origen_id = n.id
                    WHERE n.tipo = 'pull_request'
                      AND a.destino_id = %s
                      AND a.tipo_relacion = 'implementa'
                      AND n.activo = TRUE
                      AND a.activo = TRUE
                """, (historia_id,))
                return cur.fetchone()[0] or 0
```

---

## Métricas de calidad de la integración

Las métricas que indican si la integración está funcionando correctamente se miden semanalmente como parte de la auditoría del punto 12.

**Tasa de vinculación.** Porcentaje de commits en ramas de feature que tienen vínculo con un work item, ya sea explícito o inferido con confianza alta. El objetivo es superior al 90% en el tercer mes. Una tasa inferior al 75% indica que el equipo de desarrollo no está siguiendo la convención de referencias o que el sistema de inferencia necesita recalibración.

**Distribución de tipos de vínculo.** Proporción de vínculos explícitos frente a inferidos. Un porcentaje elevado de vínculos inferidos (superior al 40%) indica que la convención de referencias no está adoptada. El champion debe reforzar la convención en la retrospectiva del sprint.

**Precisión de la inferencia.** Porcentaje de vínculos inferidos que el desarrollador confirma como correctos cuando se le consulta. Se mide mediante una encuesta mensual corta o mediante el análisis de correcciones manuales en Jira. El objetivo es superior al 80%.

**Commits sin vincular en rama principal.** Número de commits en la rama principal sin vínculo a ningún work item. Cualquier número superior a cero merece revisión: puede indicar commits de mantenimiento legítimos o trabajo no planificado que debería haberse registrado.

**Tiempo desde commit hasta actualización de Jira.** Latencia entre el push del commit y la actualización del estado del work item en Jira. Con webhooks configurados correctamente debe ser inferior a 30 segundos. Un valor consistentemente superior indica problemas de infraestructura o saturación del receptor de webhooks.

---

## Limitaciones y gestión de expectativas

**La inferencia semántica tiene falsos positivos.** Un commit que dice "mejorar rendimiento del módulo de facturación" puede vincularse incorrectamente a cualquiera de las historias activas del módulo de facturación si el mensaje no es suficientemente específico. Los falsos positivos de la inferencia son menos dañinos que los commits no vinculados porque al menos existe una pista de contexto, pero deben revisarse cuando se detectan discrepancias entre el estado del work item y el código que se supone que lo implementa.

**Los commits de mantenimiento y refactoring son legítimamente no vinculables.** Un commit que actualiza dependencias, corrige un typo en documentación o refactoriza sin cambio funcional no debería vincularse a ninguna historia de usuario. El sistema los detectará como sin vincular, lo que puede generar falso ruido en la métrica de tasa de vinculación. La solución es añadir prefijos de exclusión en la configuración: commits que empiezan por `chore:`, `docs:`, `refactor:`, `style:` o `ci:` se excluyen del análisis de vinculación.

**El comentario de contexto en el PR requiere permisos de escritura.** En organizaciones con políticas de seguridad estrictas sobre los tokens de acceso, el token usado para publicar comentarios debe tener permisos de escritura en issues/pull requests. Si solo está disponible un token de lectura, el sistema puede funcionar en modo silencioso: registra la trazabilidad en el grafo pero no publica el comentario en el PR.

**Azure Repos usa una API diferente a GitHub y GitLab.** El conector para Azure Repos se implementa como extensión del cliente ADO del punto de integración con Azure DevOps, no como un cliente de repositorio independiente, porque Azure Repos y Azure Boards comparten la misma autenticación PAT y la misma base URL. Para organizaciones con stack Microsoft completo, la integración de commits con work items está parcialmente disponible de forma nativa en Azure DevOps sin necesidad del pipeline, mediante la configuración de branch policies que exigen referencia a work items en los commits. El pipeline añade sobre eso la inferencia semántica y la actualización del grafo de trazabilidad interno.
