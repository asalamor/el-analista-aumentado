"""
config.py — Configuración centralizada del pipeline AI funcional.
Todas las variables sensibles se leen de variables de entorno o de .env
Nunca se hardcodean valores sensibles en el código.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent


@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "anthropic")
    # anthropic | openai — permite cambiar sin tocar prompts
    model: str = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    max_tokens: int = 4096
    temperatura: float = 0.1
    # Temperatura baja para outputs deterministas y estructurados
    max_reintentos: int = 3
    pausa_entre_llamadas_ms: int = 500


@dataclass
class JiraConfig:
    base_url: str = os.getenv("JIRA_BASE_URL", "")
    user_email: str = os.getenv("JIRA_USER_EMAIL", "")
    api_token: str = os.getenv("JIRA_API_TOKEN", "")
    project_key: str = os.getenv("JIRA_PROJECT_KEY", "")
    campo_requisito_origen: str = os.getenv("JIRA_FIELD_REQ_ORIGEN", "customfield_10100")
    campo_modulo_funcional: str = os.getenv("JIRA_FIELD_MODULO", "customfield_10101")
    campo_story_points: str = os.getenv("JIRA_FIELD_STORY_POINTS", "customfield_10016")
    campo_epic_link: str = os.getenv("JIRA_FIELD_EPIC_LINK", "customfield_10014")
    campo_epic_name: str = os.getenv("JIRA_FIELD_EPIC_NAME", "customfield_10011")


@dataclass
class DBConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    name: str = os.getenv("DB_NAME", "pipeline_ai")
    user: str = os.getenv("DB_USER", "pipeline")
    password: str = os.getenv("DB_PASSWORD", "")

    def to_dict(self):
        return {
            "host": self.host, "port": self.port,
            "dbname": self.name, "user": self.user,
            "password": self.password
        }


@dataclass
class XrayConfig:
    base_url: str = os.getenv("XRAY_BASE_URL", "")
    client_id: str = os.getenv("XRAY_CLIENT_ID", "")
    client_secret: str = os.getenv("XRAY_CLIENT_SECRET", "")
    activo: bool = os.getenv("XRAY_ACTIVO", "true").lower() == "true"


@dataclass
class PipelineConfig:
    # Rutas del proyecto
    repo_requisitos: Path = BASE_DIR / "requisitos"
    repo_glosario: Path = BASE_DIR / "glosario.yaml"
    repo_prompts: Path = BASE_DIR / "prompts" / "v1.1"
    carpeta_runs: Path = BASE_DIR / "runs"
    carpeta_reports: Path = BASE_DIR / "reports"

    # Comportamiento del pipeline
    dry_run: bool = False
    modo_interactivo: bool = True
    score_minimo_validacion: int = 65
    similitud_duplicado_umbral: float = 0.90
    max_paralelo: int = 3

    # Subcomponentes
    llm: LLMConfig = field(default_factory=LLMConfig)
    jira: JiraConfig = field(default_factory=JiraConfig)
    db: DBConfig = field(default_factory=DBConfig)
    xray: XrayConfig = field(default_factory=XrayConfig)

    def __post_init__(self):
        self.carpeta_runs.mkdir(exist_ok=True)
        self.carpeta_reports.mkdir(exist_ok=True)

    def validar(self) -> list[str]:
        """Verifica que la configuración mínima está presente."""
        errores = []
        if not self.llm.api_key:
            errores.append("ANTHROPIC_API_KEY no configurada")
        if not self.dry_run:
            if not self.jira.base_url:
                errores.append("JIRA_BASE_URL no configurada")
            if not self.jira.api_token:
                errores.append("JIRA_API_TOKEN no configurada")
        if not self.repo_glosario.exists():
            errores.append(f"Glosario no encontrado: {self.repo_glosario}")
        return errores
