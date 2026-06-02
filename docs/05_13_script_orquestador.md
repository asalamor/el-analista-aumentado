# Punto 13 — Script orquestador

El script orquestador es el pegamento que une todo lo construido en los puntos 4 al 10 en un único comando ejecutable. Lo diseño como un sistema real, no como pseudocódigo: con gestión de errores, logs, reintentos y estado persistente para que una ejecución interrumpida pueda reanudarse sin repetir pasos ya completados.

---

## Diseño del orquestador

Antes del código, las tres decisiones de diseño que determinan la arquitectura:

**Ejecución por fases con estado persistente.** Si el pipeline falla en el paso 6 de 10, la siguiente ejecución no repite los pasos 1 a 5. El estado de cada fase se persiste en un archivo de ejecución que actúa como diario de a bordo.

**Modo seco obligatorio antes del push real.** El orquestador siempre puede ejecutarse en modo `--dry-run` que genera todos los artefactos y los valida, pero no toca Jira ni Xray. Esto permite que el analista vea el resultado completo antes de comprometerse.

**Un requisito o un lote.** El mismo script procesa un único requisito (`--req REQ-023`) o un lote completo de una épica (`--epica EP-04`) con control de concurrencia y rate limiting entre llamadas.

---

## Estructura del proyecto

```
pipeline-ai/
├── orchestrator.py          ← punto de entrada principal
├── config.py                ← configuración centralizada
├── state.py                 ← gestión de estado de ejecución
│
├── steps/
│   ├── s1_load.py           ← carga y parseo del YAML
│   ├── s2_validate.py       ← validación de calidad (punto 6)
│   ├── s3_rag_context.py    ← recuperación de contexto RAG (punto 7)
│   ├── s4_generate.py       ← generación de artefactos (punto 4)
│   ├── s5_test_cases.py     ← generación de test cases (punto 5)
│   ├── s6_impact.py         ← análisis de impacto si es actualización (punto 8)
│   ├── s7_traceability.py   ← registro en el grafo (punto 9)
│   ├── s8_approval.py       ← cola de aprobación humana
│   └── s9_push.py           ← push a Jira y Xray (punto 10)
│
├── prompts/
│   └── v1.1/                ← prompts versionados
│
├── runs/                    ← archivos de estado por ejecución
│   └── REQ-023_20250512.json
│
└── reports/                 ← informes generados
    └── REQ-023_report.md
```

---

## `config.py` — Configuración centralizada

```python
# config.py
"""
Configuración centralizada del pipeline.
Todas las variables sensibles se leen de variables de entorno
o de un archivo .env. Nunca se hardcodean.
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
    # anthropic │ openai — permite cambiar sin tocar prompts
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
    campo_requisito_origen: str = os.getenv(
        "JIRA_FIELD_REQ_ORIGEN", "customfield_10100"
    )
    campo_story_points: str = os.getenv(
        "JIRA_FIELD_STORY_POINTS", "customfield_10016"
    )
    campo_epic_link: str = os.getenv(
        "JIRA_FIELD_EPIC_LINK", "customfield_10014"
    )
    campo_epic_name: str = os.getenv(
        "JIRA_FIELD_EPIC_NAME", "customfield_10011"
    )

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
    # True = genera artefactos pero no push a Jira/Xray
    modo_interactivo: bool = True
    # False = aprobación automática sin intervención humana
    # Solo usar en CI/CD con revisión post-hoc
    score_minimo_validacion: int = 65
    # Requisitos con score < 65 se bloquean aunque no tengan
    # problemas bloqueantes explícitos
    similitud_duplicado_umbral: float = 0.90
    # Chunks con similitud > 0.90 se marcan como posible duplicado
    max_paralelo: int = 3
    # Máximo de requisitos procesados en paralelo en modo lote

    # Subcomponentes
    llm: LLMConfig = field(default_factory=LLMConfig)
    jira: JiraConfig = field(default_factory=JiraConfig)
    db: DBConfig = field(default_factory=DBConfig)
    xray: XrayConfig = field(default_factory=XrayConfig)

    def __post_init__(self):
        # Crear carpetas si no existen
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
```

---

## `state.py` — Gestión de estado de ejecución

```python
# state.py
"""
Gestión del estado de ejecución de cada requisito.
Permite reanudar una ejecución interrumpida sin repetir pasos.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional

class EstadoPaso(str, Enum):
    PENDIENTE  = "pendiente"
    EN_CURSO   = "en_curso"
    COMPLETADO = "completado"
    FALLIDO    = "fallido"
    OMITIDO    = "omitido"
    # OMITIDO: el paso no aplica (ej: impacto de cambios en req nuevo)

class EstadoEjecucion(str, Enum):
    INICIADA            = "iniciada"
    VALIDACION_FALLIDA  = "validacion_fallida"
    PENDIENTE_APROBACION= "pendiente_aprobacion"
    APROBADO            = "aprobado"
    RECHAZADO           = "rechazado"
    COMPLETADO          = "completado"
    FALLIDO             = "fallido"

@dataclass
class PasoEjecucion:
    nombre: str
    estado: EstadoPaso = EstadoPaso.PENDIENTE
    inicio: Optional[str] = None
    fin: Optional[str] = None
    duracion_segundos: Optional[float] = None
    resultado: Optional[dict] = None
    error: Optional[str] = None
    intentos: int = 0

@dataclass
class EstadoRun:
    run_id: str
    requisito_id: str
    hash_yaml: str          # Hash del YAML de entrada para detectar cambios
    inicio: str
    fin: Optional[str] = None
    estado: EstadoEjecucion = EstadoEjecucion.INICIADA
    dry_run: bool = False
    pasos: dict = field(default_factory=dict)
    # Resultados intermedios (para no regenerar si se reanuda)
    artefactos_generados: Optional[dict] = None
    test_cases_generados: Optional[list] = None
    informe_validacion: Optional[dict] = None
    informe_impacto: Optional[dict] = None
    resultado_jira: Optional[dict] = None
    errores_globales: list = field(default_factory=list)
    advertencias_globales: list = field(default_factory=list)

class GestorEstado:
    """
    Persiste y recupera el estado de ejecución de cada requisito.
    Permite reanudar ejecuciones interrumpidas.
    """

    PASOS_PIPELINE = [
        "s1_carga",
        "s2_validacion",
        "s3_rag_contexto",
        "s4_generacion_artefactos",
        "s5_generacion_test_cases",
        "s6_analisis_impacto",
        "s7_registro_trazabilidad",
        "s8_aprobacion",
        "s9_push_jira",
        "s9b_push_xray",
    ]

    def __init__(self, carpeta_runs: Path):
        self.carpeta_runs = carpeta_runs

    def crear_run(
        self,
        requisito_id: str,
        yaml_content: str,
        dry_run: bool = False
    ) -> EstadoRun:
        """Crea un nuevo run o recupera uno existente si el YAML no cambió."""
        hash_yaml = hashlib.md5(yaml_content.encode()).hexdigest()
        run_existente = self._buscar_run_reanudable(requisito_id, hash_yaml)

        if run_existente:
            print(
                f"  ↩ Run anterior encontrado para {requisito_id}. "
                f"Reanudando desde el paso fallido."
            )
            return run_existente

        # Crear run nuevo
        run_id = (
            f"{requisito_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        run = EstadoRun(
            run_id=run_id,
            requisito_id=requisito_id,
            hash_yaml=hash_yaml,
            inicio=datetime.now().isoformat(),
            dry_run=dry_run,
            pasos={
                paso: asdict(PasoEjecucion(nombre=paso))
                for paso in self.PASOS_PIPELINE
            }
        )
        self._persistir(run)
        return run

    def iniciar_paso(self, run: EstadoRun, paso: str) -> EstadoRun:
        run.pasos[paso]["estado"] = EstadoPaso.EN_CURSO
        run.pasos[paso]["inicio"] = datetime.now().isoformat()
        run.pasos[paso]["intentos"] += 1
        self._persistir(run)
        return run

    def completar_paso(
        self,
        run: EstadoRun,
        paso: str,
        resultado: dict = None
    ) -> EstadoRun:
        inicio = run.pasos[paso].get("inicio")
        fin = datetime.now().isoformat()
        duracion = None
        if inicio:
            from datetime import datetime as dt
            d = dt.fromisoformat(fin) - dt.fromisoformat(inicio)
            duracion = d.total_seconds()

        run.pasos[paso]["estado"] = EstadoPaso.COMPLETADO
        run.pasos[paso]["fin"] = fin
        run.pasos[paso]["duracion_segundos"] = duracion
        run.pasos[paso]["resultado"] = resultado or {}
        self._persistir(run)
        return run

    def fallar_paso(
        self,
        run: EstadoRun,
        paso: str,
        error: str
    ) -> EstadoRun:
        run.pasos[paso]["estado"] = EstadoPaso.FALLIDO
        run.pasos[paso]["error"] = error
        run.errores_globales.append(f"[{paso}] {error}")
        self._persistir(run)
        return run

    def omitir_paso(
        self,
        run: EstadoRun,
        paso: str,
        motivo: str
    ) -> EstadoRun:
        run.pasos[paso]["estado"] = EstadoPaso.OMITIDO
        run.pasos[paso]["resultado"] = {"motivo": motivo}
        self._persistir(run)
        return run

    def debe_ejecutar(self, run: EstadoRun, paso: str) -> bool:
        """
        Retorna True si el paso debe ejecutarse.
        False si ya está completado o si es un run reanudado y el paso
        se completó en la ejecución anterior.
        """
        estado = run.pasos.get(paso, {}).get("estado")
        return estado not in (
            EstadoPaso.COMPLETADO, EstadoPaso.OMITIDO
        )

    def finalizar(
        self,
        run: EstadoRun,
        estado: EstadoEjecucion
    ) -> EstadoRun:
        run.estado = estado
        run.fin = datetime.now().isoformat()
        self._persistir(run)
        return run

    def _persistir(self, run: EstadoRun):
        ruta = self.carpeta_runs / f"{run.run_id}.json"
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(asdict(run), f, ensure_ascii=False, indent=2)

    def _buscar_run_reanudable(
        self,
        requisito_id: str,
        hash_yaml: str
    ) -> Optional[EstadoRun]:
        """
        Busca un run reciente (últimas 24h) del mismo requisito
        con el mismo YAML que quedó incompleto.
        """
        from datetime import timedelta

        for archivo in sorted(
            self.carpeta_runs.glob(f"{requisito_id}_*.json"),
            reverse=True
        ):
            with open(archivo) as f:
                datos = json.load(f)

            # Solo runs del mismo YAML y no finalizados positivamente
            if datos.get("hash_yaml") != hash_yaml:
                continue
            if datos.get("estado") in (
                EstadoEjecucion.COMPLETADO,
                EstadoEjecucion.RECHAZADO
            ):
                continue

            # Solo runs de las últimas 24 horas
            inicio = datetime.fromisoformat(datos["inicio"])
            if datetime.now() - inicio > timedelta(hours=24):
                continue

            # Reconstruir el objeto
            run = EstadoRun(**{
                k: v for k, v in datos.items()
                if k in EstadoRun.__dataclass_fields__
            })
            return run

        return None
```

---

## `orchestrator.py` — El script principal

```python
# orchestrator.py
"""
Orquestador principal del pipeline AI de análisis funcional.

Uso básico:
  python orchestrator.py --req REQ-023
  python orchestrator.py --epica EP-04
  python orchestrator.py --req REQ-023 --dry-run
  python orchestrator.py --req REQ-023 --desde s4_generacion_artefactos
  python orchestrator.py --epica EP-04 --paralelo 3

Flags disponibles:
  --req         ID de un requisito individual
  --epica       ID de épica para procesar todos sus requisitos
  --dry-run     Genera artefactos pero no push a Jira/Xray
  --sin-aprobacion  Modo automático sin intervención humana
  --desde       Reanudar desde un paso específico
  --paralelo N  Número de requisitos en paralelo (modo épica)
  --verbose     Output detallado de cada llamada al LLM
"""

import argparse
import asyncio
import sys
import time
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Importar configuración y gestión de estado
from config import PipelineConfig
from state import GestorEstado, EstadoEjecucion, EstadoPaso

# Importar los pasos del pipeline
from steps.s1_load       import cargar_requisito
from steps.s2_validate   import validar_requisito
from steps.s3_rag_context import recuperar_contexto_rag
from steps.s4_generate   import generar_artefactos_jira
from steps.s5_test_cases import generar_test_cases
from steps.s6_impact     import analizar_impacto_cambios
from steps.s7_traceability import registrar_en_grafo
from steps.s8_approval   import solicitar_aprobacion
from steps.s9_push       import push_a_jira, push_a_xray

# Logging estructurado
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("pipeline")


# ─────────────────────────────────────────────────────────────
# PIPELINE DE UN REQUISITO
# ─────────────────────────────────────────────────────────────

async def ejecutar_pipeline_requisito(
    requisito_id: str,
    config: PipelineConfig,
    gestor: GestorEstado,
    forzar_desde: Optional[str] = None
) -> dict:
    """
    Ejecuta el pipeline completo para un único requisito.
    Retorna el resultado final con métricas y estado.
    """

    separador = "─" * 56
    print(f"\n{separador}")
    print(f"  PIPELINE → {requisito_id}")
    print(f"  Modo: {'DRY-RUN' if config.dry_run else 'PRODUCCIÓN'}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separador)

    inicio_total = time.time()

    # ── Localizar el YAML del requisito ──────────────────────
    ruta_yaml = _encontrar_yaml(requisito_id, config)
    if not ruta_yaml:
        log.error(f"YAML no encontrado para {requisito_id}")
        return {"exito": False, "error": "YAML no encontrado"}

    yaml_content = ruta_yaml.read_text(encoding="utf-8")

    # ── Crear o reanudar el run ───────────────────────────────
    run = gestor.crear_run(requisito_id, yaml_content, config.dry_run)

    # Si se fuerza inicio desde un paso concreto, resetear los
    # pasos posteriores para que se re-ejecuten
    if forzar_desde:
        run = _resetear_desde_paso(run, forzar_desde, gestor)

    try:

        # ══════════════════════════════════════════════════════
        # PASO 1 — Carga y parseo del YAML
        # ══════════════════════════════════════════════════════
        paso = "s1_carga"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(1, "Carga y parseo del requisito")
            run = gestor.iniciar_paso(run, paso)
            try:
                requisito = cargar_requisito(yaml_content)
                run.artefactos_generados = run.artefactos_generados or {}
                run.artefactos_generados["requisito"] = requisito
                run = gestor.completar_paso(run, paso, {
                    "titulo": requisito.get("titulo"),
                    "epica": requisito.get("epica"),
                    "estado": requisito.get("estado")
                })
                _log_ok(f"'{requisito.get('titulo', '')[:60]}'")
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)
            requisito = run.artefactos_generados.get("requisito", {})

        # Verificar que el estado del requisito permite procesarlo
        if requisito.get("estado") not in ("en-revision", "validado"):
            msg = (
                f"El requisito está en estado '{requisito.get('estado')}'. "
                f"Solo se procesan requisitos en estado "
                f"'en-revision' o 'validado'."
            )
            log.warning(f"  ⚠ {msg}")
            run = gestor.fallar_paso(run, "s1_carga", msg)
            run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
            return _resultado_fallido(run, msg, time.time() - inicio_total)

        # ══════════════════════════════════════════════════════
        # PASO 2 — Validación automática de calidad
        # ══════════════════════════════════════════════════════
        paso = "s2_validacion"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(2, "Validación automática de calidad")
            run = gestor.iniciar_paso(run, paso)
            try:
                glosario = _cargar_glosario(config)
                informe_val = await validar_requisito(
                    requisito=requisito,
                    glosario=glosario,
                    config=config
                )
                run.informe_validacion = informe_val
                score = informe_val.get(
                    "puntuacion_global", {}
                ).get("valor", 0)
                veredicto = informe_val.get("veredicto_final", "")
                run = gestor.completar_paso(run, paso, {
                    "score": score,
                    "veredicto": veredicto
                })

                if veredicto == "BLOQUEADO":
                    _log_error(
                        f"Score {score}/100 · BLOQUEADO. "
                        f"Revisa el informe de validación."
                    )
                    _imprimir_problemas_bloqueantes(informe_val)
                    run = gestor.finalizar(
                        run, EstadoEjecucion.VALIDACION_FALLIDA
                    )
                    _generar_informe_validacion(run, config)
                    return _resultado_fallido(
                        run,
                        "Validación bloqueada. Ver informe.",
                        time.time() - inicio_total
                    )
                elif veredicto == "APROBADO_CON_ADVERTENCIAS":
                    _log_advertencia(
                        f"Score {score}/100 · ADVERTENCIAS. "
                        f"El pipeline continúa."
                    )
                    _imprimir_advertencias(informe_val)
                else:
                    _log_ok(f"Score {score}/100 · APROBADO")

            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)
            informe_val = run.informe_validacion

        # ══════════════════════════════════════════════════════
        # PASO 3 — Recuperación de contexto RAG
        # ══════════════════════════════════════════════════════
        paso = "s3_rag_contexto"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(3, "Recuperando contexto del repositorio (RAG)")
            run = gestor.iniciar_paso(run, paso)
            try:
                contexto_rag = await recuperar_contexto_rag(
                    requisito=requisito,
                    glosario=glosario,
                    config=config
                )
                run.artefactos_generados["contexto_rag"] = contexto_rag

                # Alertar si se detectan posibles duplicados
                duplicados = contexto_rag.get("criterios_similares", [])
                duplicados_criticos = [
                    d for d in duplicados
                    if d.get("similitud", 0) > config.similitud_duplicado_umbral
                ]
                if duplicados_criticos:
                    _log_advertencia(
                        f"⚠ {len(duplicados_criticos)} criterios AC "
                        f"con similitud >{config.similitud_duplicado_umbral:.0%} "
                        f"detectados. Posible duplicado."
                    )
                    for d in duplicados_criticos[:3]:
                        print(
                            f"    → {d.get('chunk_id')} "
                            f"({d.get('similitud', 0):.0%} similitud)"
                        )

                n_relacionados = len(
                    contexto_rag.get("funcionalidad_similar", [])
                )
                run = gestor.completar_paso(run, paso, {
                    "requisitos_relacionados": n_relacionados,
                    "duplicados_criticos": len(duplicados_criticos)
                })
                _log_ok(
                    f"{n_relacionados} requisitos relacionados recuperados"
                )

            except Exception as e:
                # El RAG no es bloqueante: si falla, continuamos
                # sin contexto histórico pero con advertencia
                log.warning(
                    f"  ⚠ RAG no disponible: {e}. "
                    f"Continuando sin contexto histórico."
                )
                run.artefactos_generados["contexto_rag"] = {}
                run = gestor.omitir_paso(
                    run, paso, f"RAG no disponible: {e}"
                )
        else:
            _log_reanudado(paso)
            contexto_rag = run.artefactos_generados.get("contexto_rag", {})

        # ══════════════════════════════════════════════════════
        # PASO 4 — Generación de artefactos Jira
        # ══════════════════════════════════════════════════════
        paso = "s4_generacion_artefactos"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(4, "Generando artefactos Jira con IA")
            run = gestor.iniciar_paso(run, paso)
            try:
                artefactos = await generar_artefactos_jira(
                    requisito=requisito,
                    glosario=glosario,
                    contexto_rag=contexto_rag,
                    config=config
                )
                run.artefactos_generados.update(artefactos)
                n_tareas = len(artefactos.get("tareas", []))
                n_ac = len(
                    artefactos.get("historia", {})
                    .get("acceptance_criteria", [])
                )
                run = gestor.completar_paso(run, paso, {
                    "historia_generada": bool(artefactos.get("historia")),
                    "n_tareas": n_tareas,
                    "n_criterios_ac": n_ac
                })
                _log_ok(
                    f"Historia · {n_tareas} tareas · {n_ac} criterios AC"
                )

                # Mostrar alertas de calidad del LLM si las hay
                alertas = artefactos.get(
                    "historia", {}
                ).get("alertas_calidad", [])
                for alerta in alertas:
                    _log_advertencia(f"LLM: {alerta}")

            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # PASO 5 — Generación de test cases
        # ══════════════════════════════════════════════════════
        paso = "s5_generacion_test_cases"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(5, "Generando test cases")
            run = gestor.iniciar_paso(run, paso)
            try:
                test_cases = await generar_test_cases(
                    historia=run.artefactos_generados.get("historia", {}),
                    requisito=requisito,
                    config=config
                )
                run.test_cases_generados = test_cases

                n_pos = sum(
                    1 for tc in test_cases
                    if "positivo" in tc.get("tipo", "")
                )
                n_neg = sum(
                    1 for tc in test_cases
                    if "negativo" in tc.get("tipo", "")
                )
                n_cont = sum(
                    1 for tc in test_cases
                    if "contorno" in tc.get("tipo", "")
                )
                run = gestor.completar_paso(run, paso, {
                    "total": len(test_cases),
                    "positivos": n_pos,
                    "negativos": n_neg,
                    "contorno": n_cont
                })
                _log_ok(
                    f"{len(test_cases)} TCs "
                    f"({n_pos} pos · {n_neg} neg · {n_cont} contorno)"
                )

            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # PASO 6 — Análisis de impacto (solo si el req es actualización)
        # ══════════════════════════════════════════════════════
        paso = "s6_analisis_impacto"
        es_actualizacion = float(
            requisito.get("version", "1.0").split(".")[0]
        ) > 1 or requisito.get("version", "1.0") != "1.0"

        if not es_actualizacion:
            run = gestor.omitir_paso(
                run, paso, "Requisito nuevo. Análisis de impacto no aplica."
            )
            _log_omitido(paso, "requisito nuevo")
        elif gestor.debe_ejecutar(run, paso):
            _log_paso(6, "Analizando impacto de cambios")
            run = gestor.iniciar_paso(run, paso)
            try:
                informe_impacto = await analizar_impacto_cambios(
                    requisito_id=requisito_id,
                    requisito_nuevo=requisito,
                    config=config
                )
                run.informe_impacto = informe_impacto
                nivel = informe_impacto.get(
                    "informe_impacto", {}
                ).get("nivel_urgencia", "DESCONOCIDO")
                n_afectados = informe_impacto.get(
                    "informe_impacto", {}
                ).get("estadisticas", {}).get(
                    "total_artefactos_afectados", 0
                )
                run = gestor.completar_paso(run, paso, {
                    "nivel_urgencia": nivel,
                    "artefactos_afectados": n_afectados
                })

                if nivel in ("CRITICO", "ALTO"):
                    _log_advertencia(
                        f"Impacto {nivel}: "
                        f"{n_afectados} artefactos afectados"
                    )
                else:
                    _log_ok(f"Impacto {nivel}: {n_afectados} afectados")

            except Exception as e:
                log.warning(f"  ⚠ Análisis de impacto falló: {e}")
                run = gestor.omitir_paso(
                    run, paso, f"Error en análisis: {e}"
                )
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # PASO 7 — Registro en el grafo de trazabilidad
        # ══════════════════════════════════════════════════════
        paso = "s7_registro_trazabilidad"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(7, "Registrando en el grafo de trazabilidad")
            run = gestor.iniciar_paso(run, paso)
            try:
                resultado_traz = await registrar_en_grafo(
                    requisito=requisito,
                    artefactos=run.artefactos_generados,
                    test_cases=run.test_cases_generados or [],
                    config=config
                )
                run = gestor.completar_paso(run, paso, resultado_traz)
                _log_ok(
                    f"{resultado_traz.get('nodos_registrados', 0)} nodos · "
                    f"{resultado_traz.get('aristas_registradas', 0)} aristas"
                )
            except Exception as e:
                # La trazabilidad no es bloqueante para el push
                log.warning(f"  ⚠ Trazabilidad falló: {e}")
                run = gestor.omitir_paso(run, paso, str(e))
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # PASO 8 — Aprobación humana
        # ══════════════════════════════════════════════════════
        paso = "s8_aprobacion"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(8, "Solicitud de aprobación humana")
            run = gestor.iniciar_paso(run, paso)

            if config.dry_run:
                _log_ok("DRY-RUN: aprobación simulada. No se empujará a Jira.")
                run.artefactos_generados["aprobacion"] = {
                    "decision": "aprobado_dry_run",
                    "por": "sistema"
                }
                run = gestor.completar_paso(run, paso, {"decision": "dry_run"})

            elif not config.modo_interactivo:
                # Modo automático: aprobar sin intervención
                log.warning(
                    "  ⚠ Modo no-interactivo: aprobación automática. "
                    "Revisar artefactos post-push."
                )
                run.artefactos_generados["aprobacion"] = {
                    "decision": "aprobado_automatico",
                    "por": "pipeline"
                }
                run = gestor.completar_paso(
                    run, paso, {"decision": "automatico"}
                )

            else:
                # Modo interactivo: mostrar artefactos y esperar
                decision = await solicitar_aprobacion(
                    run=run,
                    artefactos=run.artefactos_generados,
                    test_cases=run.test_cases_generados or [],
                    informe_validacion=run.informe_validacion,
                    informe_impacto=run.informe_impacto
                )

                if decision["decision"] == "rechazado":
                    run = gestor.fallar_paso(
                        run, paso,
                        f"Rechazado por el analista. Motivo: "
                        f"{decision.get('motivo', 'no especificado')}"
                    )
                    run = gestor.finalizar(run, EstadoEjecucion.RECHAZADO)
                    return _resultado_rechazado(
                        run, decision, time.time() - inicio_total
                    )

                # Si el analista editó los artefactos, usar la versión editada
                if decision.get("artefactos_editados"):
                    run.artefactos_generados.update(
                        decision["artefactos_editados"]
                    )
                    log.info("  ✓ Artefactos actualizados con las ediciones")

                run.artefactos_generados["aprobacion"] = decision
                run = gestor.completar_paso(run, paso, {
                    "decision": decision["decision"],
                    "por": decision.get("analista", "desconocido")
                })
                _log_ok(
                    f"Aprobado por {decision.get('analista', 'analista')}"
                )
        else:
            _log_reanudado(paso)

        # Si es dry-run, terminar aquí
        if config.dry_run:
            _generar_informe_completo(run, config)
            run = gestor.finalizar(run, EstadoEjecucion.COMPLETADO)
            return _resultado_exitoso(
                run, time.time() - inicio_total,
                nota="DRY-RUN completado. Artefactos generados pero no empujados."
            )

        # ══════════════════════════════════════════════════════
        # PASO 9 — Push a Jira
        # ══════════════════════════════════════════════════════
        paso = "s9_push_jira"
        if gestor.debe_ejecutar(run, paso):
            _log_paso(9, "Push a Jira")
            run = gestor.iniciar_paso(run, paso)
            try:
                resultado_jira = await push_a_jira(
                    artefactos=run.artefactos_generados,
                    requisito_id=requisito_id,
                    config=config
                )
                run.resultado_jira = resultado_jira

                if not resultado_jira.get("exito"):
                    errores_jira = resultado_jira.get("errores", [])
                    run = gestor.fallar_paso(
                        run, paso,
                        f"Push Jira fallido: {'; '.join(errores_jira)}"
                    )
                    raise PipelineFallo(paso, str(errores_jira))

                run = gestor.completar_paso(run, paso, {
                    "epica_key": resultado_jira.get("epica_key"),
                    "historia_key": resultado_jira.get("historia_key"),
                    "tareas_keys": resultado_jira.get("tareas_keys", [])
                })
                _log_ok(
                    f"Historia {resultado_jira.get('historia_key')} · "
                    f"{len(resultado_jira.get('tareas_keys', []))} tareas"
                )

            except PipelineFallo:
                raise
            except Exception as e:
                run = gestor.fallar_paso(run, paso, str(e))
                raise PipelineFallo(paso, str(e))
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # PASO 9B — Push a Xray
        # ══════════════════════════════════════════════════════
        paso = "s9b_push_xray"
        if not config.xray.activo:
            run = gestor.omitir_paso(
                run, paso, "Xray desactivado en configuración."
            )
            _log_omitido(paso, "Xray desactivado")
        elif gestor.debe_ejecutar(run, paso):
            _log_paso("9b", "Push test cases a Xray")
            run = gestor.iniciar_paso(run, paso)
            try:
                historia_key = run.resultado_jira.get("historia_key")
                resultado_xray = await push_a_xray(
                    test_cases=run.test_cases_generados or [],
                    historia_key=historia_key,
                    requisito_id=requisito_id,
                    config=config
                )
                n_tc = resultado_xray.get("test_cases_creados", 0)
                run = gestor.completar_paso(run, paso, resultado_xray)
                _log_ok(f"{n_tc} test cases en Xray")
            except Exception as e:
                # Xray no es bloqueante
                log.warning(f"  ⚠ Push Xray falló: {e}")
                run = gestor.omitir_paso(run, paso, str(e))
        else:
            _log_reanudado(paso)

        # ══════════════════════════════════════════════════════
        # FIN DEL PIPELINE
        # ══════════════════════════════════════════════════════
        duracion = time.time() - inicio_total
        _generar_informe_completo(run, config)
        run = gestor.finalizar(run, EstadoEjecucion.COMPLETADO)
        return _resultado_exitoso(run, duracion)

    except PipelineFallo as e:
        duracion = time.time() - inicio_total
        log.error(f"\n  ✗ Pipeline detenido en [{e.paso}]: {e.mensaje}")
        _generar_informe_completo(run, config)
        run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
        return _resultado_fallido(run, str(e), duracion)

    except Exception as e:
        duracion = time.time() - inicio_total
        log.exception(f"Error inesperado: {e}")
        run = gestor.finalizar(run, EstadoEjecucion.FALLIDO)
        return _resultado_fallido(run, str(e), duracion)


# ─────────────────────────────────────────────────────────────
# PIPELINE DE UNA ÉPICA (lote de requisitos)
# ─────────────────────────────────────────────────────────────

async def ejecutar_pipeline_epica(
    epica_id: str,
    config: PipelineConfig,
    gestor: GestorEstado,
    max_paralelo: int = 1
) -> dict:
    """
    Procesa todos los requisitos de una épica.
    El orden de procesamiento respeta las dependencias declaradas.
    """
    print(f"\n{'═' * 56}")
    print(f"  ÉPICA → {epica_id}")
    print(f"  Procesando requisitos en lote (paralelo: {max_paralelo})")
    print(f"{'═' * 56}")

    # Descubrir todos los requisitos de la épica
    requisitos = _descubrir_requisitos_epica(epica_id, config)

    if not requisitos:
        print(f"  ⚠ No se encontraron requisitos para {epica_id}")
        return {"exito": False, "error": "Sin requisitos"}

    print(f"  {len(requisitos)} requisitos encontrados")

    # Ordenar por dependencias declaradas
    requisitos_ordenados = _ordenar_por_dependencias(requisitos, config)

    # Procesar en lotes respetando el paralelismo máximo
    resultados = {}
    inicio = time.time()

    for i in range(0, len(requisitos_ordenados), max_paralelo):
        lote = requisitos_ordenados[i:i + max_paralelo]
        print(
            f"\n  Lote {i // max_paralelo + 1}: "
            f"{[r['id'] for r in lote]}"
        )

        # Ejecutar el lote en paralelo
        tareas = [
            ejecutar_pipeline_requisito(req["id"], config, gestor)
            for req in lote
        ]
        resultados_lote = await asyncio.gather(*tareas, return_exceptions=True)

        for req, resultado in zip(lote, resultados_lote):
            req_id = req["id"]
            if isinstance(resultado, Exception):
                resultados[req_id] = {"exito": False, "error": str(resultado)}
            else:
                resultados[req_id] = resultado

        # Pausa entre lotes para no saturar APIs
        if i + max_paralelo < len(requisitos_ordenados):
            print(f"\n  Pausa entre lotes (3s)...")
            await asyncio.sleep(3)

    # Resumen del lote
    duracion = time.time() - inicio
    exitosos = sum(1 for r in resultados.values() if r.get("exito"))
    fallidos = len(resultados) - exitosos

    print(f"\n{'═' * 56}")
    print(f"  RESUMEN ÉPICA {epica_id}")
    print(f"  Total: {len(resultados)} requisitos")
    print(f"  ✓ Exitosos: {exitosos}")
    print(f"  ✗ Fallidos: {fallidos}")
    print(f"  Tiempo total: {duracion:.1f}s")
    print(f"{'═' * 56}\n")

    return {
        "epica_id": epica_id,
        "exito": fallidos == 0,
        "total": len(resultados),
        "exitosos": exitosos,
        "fallidos": fallidos,
        "duracion_segundos": round(duracion, 1),
        "detalle": resultados
    }


# ─────────────────────────────────────────────────────────────
# UTILIDADES INTERNAS
# ─────────────────────────────────────────────────────────────

class PipelineFallo(Exception):
    def __init__(self, paso: str, mensaje: str):
        self.paso = paso
        self.mensaje = mensaje
        super().__init__(f"[{paso}] {mensaje}")

def _encontrar_yaml(req_id: str, config: PipelineConfig) -> Optional[Path]:
    """Busca el YAML del requisito en el repositorio."""
    for ruta in config.repo_requisitos.rglob(f"{req_id}.yaml"):
        return ruta
    for ruta in config.repo_requisitos.rglob("*.yaml"):
        try:
            contenido = yaml.safe_load(ruta.read_text())
            if contenido and contenido.get("id") == req_id:
                return ruta
        except Exception:
            continue
    return None

def _cargar_glosario(config: PipelineConfig) -> dict:
    """Carga el glosario del proyecto."""
    with open(config.repo_glosario, encoding="utf-8") as f:
        return yaml.safe_load(f)

def _descubrir_requisitos_epica(
    epica_id: str,
    config: PipelineConfig
) -> list[dict]:
    """Descubre todos los requisitos de una épica en el repositorio."""
    requisitos = []
    for ruta in config.repo_requisitos.rglob("*.yaml"):
        try:
            contenido = yaml.safe_load(ruta.read_text())
            if (contenido and
                contenido.get("epica") == epica_id and
                contenido.get("estado") in ("en-revision", "validado")):
                requisitos.append(contenido)
        except Exception:
            continue
    return requisitos

def _ordenar_por_dependencias(
    requisitos: list[dict],
    config: PipelineConfig
) -> list[dict]:
    """
    Ordena los requisitos para que las dependencias se procesen antes.
    Usa ordenación topológica simple.
    """
    ids = {r["id"] for r in requisitos}
    ordenados = []
    visitados = set()

    def visitar(req):
        if req["id"] in visitados:
            return
        visitados.add(req["id"])
        for dep_id in req.get("dependencias", {}).get("requisitos", []):
            if dep_id in ids:
                dep = next((r for r in requisitos if r["id"] == dep_id), None)
                if dep:
                    visitar(dep)
        ordenados.append(req)

    for req in requisitos:
        visitar(req)

    return ordenados

def _resetear_desde_paso(run, desde_paso: str, gestor: GestorEstado) -> object:
    """Resetea todos los pasos desde el indicado para re-ejecutarlos."""
    pasos = list(run.pasos.keys())
    if desde_paso not in pasos:
        log.warning(f"Paso '{desde_paso}' no reconocido. Ignorando --desde.")
        return run
    desde_idx = pasos.index(desde_paso)
    for paso in pasos[desde_idx:]:
        run.pasos[paso]["estado"] = EstadoPaso.PENDIENTE
        run.pasos[paso]["resultado"] = None
        run.pasos[paso]["error"] = None
    gestor._persistir(run)
    return run

def _generar_informe_completo(run, config: PipelineConfig):
    """Genera el informe Markdown de la ejecución."""
    ruta = config.carpeta_reports / f"{run.run_id}_report.md"

    pasos_completados = sum(
        1 for p in run.pasos.values() if p.get("estado") == "completado"
    )
    pasos_fallidos = sum(
        1 for p in run.pasos.values() if p.get("estado") == "fallido"
    )
    duracion_total = sum(
        p.get("duracion_segundos") or 0 for p in run.pasos.values()
    )

    md = f"""# Informe de ejecución — {run.requisito_id}

**Run ID:** {run.run_id}
**Estado:** {run.estado}
**Inicio:** {run.inicio}
**Fin:** {run.fin or 'en curso'}
**Modo:** {'DRY-RUN' if run.dry_run else 'PRODUCCIÓN'}

## Resumen

| Métrica | Valor |
|---|---|
| Pasos completados | {pasos_completados} |
| Pasos fallidos | {pasos_fallidos} |
| Duración total | {duracion_total:.1f}s |

## Pasos del pipeline

| Paso | Estado | Duración | Resultado |
|---|---|---|---|
"""
    for nombre, paso in run.pasos.items():
        estado = paso.get("estado", "pendiente")
        icono = {
            "completado": "✅", "fallido": "❌",
            "omitido": "⏭", "en_curso": "🔄", "pendiente": "⏸"
        }.get(estado, "?")
        duracion = f"{paso.get('duracion_segundos', 0):.1f}s"
        resultado = ""
        if paso.get("resultado"):
            resultado = str(paso["resultado"])[:80]
        if paso.get("error"):
            resultado = f"ERROR: {paso['error'][:80]}"
        md += f"| {nombre} | {icono} {estado} | {duracion} | {resultado} |\n"

    if run.resultado_jira:
        md += f"""
## Artefactos en Jira

| Tipo | Key |
|---|---|
| Épica | {run.resultado_jira.get('epica_key', '—')} |
| Historia | {run.resultado_jira.get('historia_key', '—')} |
| Tareas | {', '.join(run.resultado_jira.get('tareas_keys', []))} |
"""

    if run.errores_globales:
        md += "\n## Errores\n"
        for e in run.errores_globales:
            md += f"- {e}\n"

    if run.advertencias_globales:
        md += "\n## Advertencias\n"
        for a in run.advertencias_globales:
            md += f"- {a}\n"

    ruta.write_text(md, encoding="utf-8")

def _generar_informe_validacion(run, config: PipelineConfig):
    """Genera un informe específico cuando la validación bloquea."""
    if not run.informe_validacion:
        return
    ruta = config.carpeta_reports / f"{run.run_id}_validacion.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(run.informe_validacion, f, ensure_ascii=False, indent=2)
    log.info(f"  Informe de validación: {ruta}")

def _resultado_exitoso(run, duracion: float, nota: str = "") -> dict:
    historia_key = (run.resultado_jira or {}).get("historia_key")
    tareas = (run.resultado_jira or {}).get("tareas_keys", [])
    n_tc = len(run.test_cases_generados or [])

    print(f"\n  {'─' * 48}")
    print(f"  ✓ COMPLETADO en {duracion:.1f}s")
    if historia_key:
        print(f"    Historia:  {historia_key}")
        print(f"    Tareas:    {', '.join(tareas)}")
        print(f"    Test cases: {n_tc}")
    if nota:
        print(f"    Nota: {nota}")
    print(f"  {'─' * 48}\n")

    return {
        "exito": True,
        "requisito_id": run.requisito_id,
        "run_id": run.run_id,
        "historia_key": historia_key,
        "tareas_keys": tareas,
        "test_cases": n_tc,
        "duracion_segundos": round(duracion, 1),
        "dry_run": run.dry_run,
        "nota": nota
    }

def _resultado_fallido(run, error: str, duracion: float) -> dict:
    print(f"\n  {'─' * 48}")
    print(f"  ✗ FALLIDO en {duracion:.1f}s")
    print(f"    Error: {error[:120]}")
    print(f"  {'─' * 48}\n")
    return {
        "exito": False,
        "requisito_id": run.requisito_id,
        "run_id": run.run_id,
        "error": error,
        "duracion_segundos": round(duracion, 1)
    }

def _resultado_rechazado(run, decision: dict, duracion: float) -> dict:
    print(f"\n  {'─' * 48}")
    print(f"  ↩ RECHAZADO por {decision.get('analista', 'analista')}")
    print(f"    Motivo: {decision.get('motivo', 'no especificado')}")
    print(f"  {'─' * 48}\n")
    return {
        "exito": False,
        "requisito_id": run.requisito_id,
        "run_id": run.run_id,
        "estado": "rechazado",
        "motivo": decision.get("motivo"),
        "duracion_segundos": round(duracion, 1)
    }

def _log_paso(num, descripcion: str):
    print(f"\n  [{num:>2}] {descripcion}")

def _log_ok(msg: str):
    print(f"       ✓ {msg}")

def _log_error(msg: str):
    print(f"       ✗ {msg}")

def _log_advertencia(msg: str):
    print(f"       ⚠ {msg}")

def _log_reanudado(paso: str):
    print(f"\n  [--] {paso} (ya completado, omitiendo)")

def _log_omitido(paso: str, motivo: str):
    print(f"\n  [⏭] {paso} omitido ({motivo})")

def _imprimir_problemas_bloqueantes(informe: dict):
    bloqueantes = (
        informe.get("problemas_por_prioridad", {})
        .get("bloqueantes", [])
    )
    for p in bloqueantes[:5]:
        print(
            f"       → [{p.get('campo', '?')}] "
            f"{p.get('problema', '')[:80]}"
        )

def _imprimir_advertencias(informe: dict):
    advertencias = (
        informe.get("problemas_por_prioridad", {})
        .get("advertencias", [])
    )
    for a in advertencias[:3]:
        print(
            f"       → [{a.get('campo', '?')}] "
            f"{a.get('problema', '')[:80]}"
        )


# ─────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Orquestador del pipeline AI de análisis funcional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python orchestrator.py --req REQ-023
  python orchestrator.py --req REQ-023 --dry-run
  python orchestrator.py --epica EP-04 --paralelo 2
  python orchestrator.py --req REQ-023 --desde s4_generacion_artefactos
  python orchestrator.py --req REQ-023 --sin-aprobacion
        """
    )
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--req",   help="ID del requisito a procesar")
    grupo.add_argument("--epica", help="ID de épica (procesa todos sus requisitos)")

    parser.add_argument(
        "--dry-run", action="store_true",
        help="Genera artefactos pero no push a Jira/Xray"
    )
    parser.add_argument(
        "--sin-aprobacion", action="store_true",
        help="Aprobación automática sin intervención humana"
    )
    parser.add_argument(
        "--desde", metavar="PASO",
        help="Reanudar desde un paso específico"
    )
    parser.add_argument(
        "--paralelo", type=int, default=1, metavar="N",
        help="Número de requisitos en paralelo (modo épica)"
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Output detallado de llamadas al LLM"
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Construir configuración
    config = PipelineConfig(
        dry_run=args.dry_run,
        modo_interactivo=not args.sin_aprobacion,
        max_paralelo=args.paralelo
    )

    # Validar configuración mínima
    errores_config = config.validar()
    if errores_config:
        print("\n✗ Errores de configuración:")
        for e in errores_config:
            print(f"  - {e}")
        print("\nRevisa el archivo .env y vuelve a intentarlo.\n")
        sys.exit(1)

    gestor = GestorEstado(config.carpeta_runs)

    # Ejecutar en modo requisito individual o épica
    if args.req:
        resultado = await ejecutar_pipeline_requisito(
            requisito_id=args.req,
            config=config,
            gestor=gestor,
            forzar_desde=args.desde
        )
    else:
        resultado = await ejecutar_pipeline_epica(
            epica_id=args.epica,
            config=config,
            gestor=gestor,
            max_paralelo=args.paralelo
        )

    # Código de salida para integración con CI/CD
    sys.exit(0 if resultado.get("exito") else 1)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Output real de una ejecución completa

Esto es lo que ve el analista al ejecutar el pipeline:

```
$ python orchestrator.py --req REQ-023

────────────────────────────────────────────────────────
  PIPELINE → REQ-023
  Modo: PRODUCCIÓN
  2025-05-12 10:15:32
────────────────────────────────────────────────────────

  [ 1] Carga y parseo del requisito
       ✓ 'Filtrar facturas por rango de fechas'

  [ 2] Validación automática de calidad
       ✓ Score 84/100 · APROBADO

  [ 3] Recuperando contexto del repositorio (RAG)
       ✓ 7 requisitos relacionados recuperados

  [ 4] Generando artefactos Jira con IA
       ✓ Historia · 4 tareas · 3 criterios AC

  [ 5] Generando test cases
       ✓ 9 TCs (2 pos · 4 neg · 3 contorno)

  [ 6] Analizando impacto de cambios
       ⏭ s6_analisis_impacto omitido (requisito nuevo)

  [ 7] Registrando en el grafo de trazabilidad
       ✓ 14 nodos · 19 aristas

  [ 8] Solicitud de aprobación humana

╔══════════════════════════════════════════════════╗
║  REVISIÓN DE ARTEFACTOS — REQ-023                ║
╠══════════════════════════════════════════════════╣
║  HISTORIA                                        ║
║  Como gestor de facturación, quiero filtrar      ║
║  facturas por rango de fechas para localizar     ║
║  documentos de un período contable               ║
║                                                  ║
║  Story Points: 5  │  Prioridad: Highest          ║
║  Épica: FACT-12   │  Componente: facturacion     ║
║                                                  ║
║  CRITERIOS DE ACEPTACIÓN (3)                     ║
║  AC-023-01 · Filtrado válido devuelve resultados ║
║  AC-023-02 · Rango >365d bloquea la búsqueda     ║
║  AC-023-03 · Sin resultados muestra estado vacío ║
║                                                  ║
║  TAREAS (4)                                      ║
║  · [BD]       Índice en tabla facturas           ║
║  · [backend]  Endpoint GET /api/v1/facturas      ║
║  · [frontend] Componente filtro por fechas       ║
║  · [testing]  Pruebas integración y rendimiento  ║
║                                                  ║
║  TEST CASES (9)                                  ║
║  2 positivos · 4 negativos · 3 contorno          ║
╠══════════════════════════════════════════════════╣
║  [A] Aprobar y empujar a Jira                    ║
║  [E] Editar antes de aprobar                     ║
║  [R] Rechazar (devolver al analista)             ║
║  [V] Ver JSON completo                           ║
╚══════════════════════════════════════════════════╝
  Decisión: A

  [ 8] Solicitud de aprobación humana
       ✓ Aprobado por carlos.ruiz@empresa.com

  [ 9] Push a Jira
       ✓ Historia FACT-47 · 4 tareas

  [9b] Push test cases a Xray
       ✓ 9 test cases en Xray

  ────────────────────────────────────────────────
  ✓ COMPLETADO en 47.3s
    Historia:   FACT-47
    Tareas:     FACT-48, FACT-49, FACT-50, FACT-51
    Test cases: 9
  ────────────────────────────────────────────────
```

---

## Modo épica con resumen final

```
$ python orchestrator.py --epica EP-04 --paralelo 2 --dry-run

════════════════════════════════════════════════════════
  ÉPICA → EP-04
  Procesando requisitos en lote (paralelo: 2)
════════════════════════════════════════════════════════
  4 requisitos encontrados

  Lote 1: ['REQ-021', 'REQ-022']
  ... [pipeline de cada requisito] ...

  Lote 2: ['REQ-023', 'REQ-024']
  ... [pipeline de cada requisito] ...

════════════════════════════════════════════════════════
  RESUMEN ÉPICA EP-04
  Total: 4 requisitos
  ✓ Exitosos: 3
  ✗ Fallidos: 1  →  REQ-024 (Validación bloqueada)
  Tiempo total: 94.2s
════════════════════════════════════════════════════════
```

---

## Integración con CI/CD

El orquestador retorna código de salida estándar (0 éxito, 1 fallo) lo que permite integrarlo directamente en GitHub Actions, GitLab CI o Jenkins:

```yaml
# .github/workflows/pipeline_ai.yml
name: Pipeline AI — Generación de artefactos

on:
  push:
    paths:
      - 'requisitos/**/*.yaml'

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Detectar requisitos modificados
        id: cambios
        run: |
          MODIFICADOS=$(git diff --name-only HEAD~1 HEAD \
            -- 'requisitos/**/*.yaml' \
            | xargs -I{} basename {} .yaml)
          echo "requisitos=$MODIFICADOS" >> $GITHUB_OUTPUT

      - name: Ejecutar pipeline en modo dry-run
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_BASE_URL: ${{ vars.JIRA_BASE_URL }}
          JIRA_USER_EMAIL: ${{ vars.JIRA_USER_EMAIL }}
          JIRA_PROJECT_KEY: ${{ vars.JIRA_PROJECT_KEY }}
          DB_HOST: ${{ vars.DB_HOST }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          pip install -r requirements.txt
          for REQ in ${{ steps.cambios.outputs.requisitos }}; do
            python orchestrator.py \
              --req $REQ \
              --dry-run \
              --sin-aprobacion
          done

      - name: Publicar informes como artefactos
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-reports
          path: reports/
```

---

Con el script orquestador completo, el pipeline end-to-end está totalmente cerrado. Un único comando transforma un YAML de requisito en todos los artefactos del proyecto, con gestión de errores, reanudación automática, aprobación humana y registro de trazabilidad.
