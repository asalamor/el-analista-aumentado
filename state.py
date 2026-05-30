"""
state.py — Gestión del estado de ejecución de cada requisito.
Permite reanudar una ejecución interrumpida sin repetir pasos ya completados.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class EstadoPaso(str, Enum):
    PENDIENTE  = "pendiente"
    EN_CURSO   = "en_curso"
    COMPLETADO = "completado"
    FALLIDO    = "fallido"
    OMITIDO    = "omitido"


class EstadoEjecucion(str, Enum):
    INICIADA             = "iniciada"
    VALIDACION_FALLIDA   = "validacion_fallida"
    PENDIENTE_APROBACION = "pendiente_aprobacion"
    APROBADO             = "aprobado"
    RECHAZADO            = "rechazado"
    COMPLETADO           = "completado"
    FALLIDO              = "fallido"


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
    hash_yaml: str
    inicio: str
    fin: Optional[str] = None
    estado: EstadoEjecucion = EstadoEjecucion.INICIADA
    dry_run: bool = False
    pasos: dict = field(default_factory=dict)
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
    Permite reanudar ejecuciones interrumpidas sin repetir pasos completados.
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

    def crear_run(self, requisito_id: str, yaml_content: str, dry_run: bool = False) -> EstadoRun:
        """Crea un nuevo run o recupera uno existente si el YAML no cambió."""
        hash_yaml = hashlib.md5(yaml_content.encode()).hexdigest()
        run_existente = self._buscar_run_reanudable(requisito_id, hash_yaml)

        if run_existente:
            print(f"  ↩ Run anterior encontrado para {requisito_id}. Reanudando.")
            return run_existente

        run_id = f"{requisito_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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

    def completar_paso(self, run: EstadoRun, paso: str, resultado: dict = None) -> EstadoRun:
        inicio = run.pasos[paso].get("inicio")
        fin = datetime.now().isoformat()
        duracion = None
        if inicio:
            d = datetime.fromisoformat(fin) - datetime.fromisoformat(inicio)
            duracion = d.total_seconds()

        run.pasos[paso]["estado"] = EstadoPaso.COMPLETADO
        run.pasos[paso]["fin"] = fin
        run.pasos[paso]["duracion_segundos"] = duracion
        run.pasos[paso]["resultado"] = resultado or {}
        self._persistir(run)
        return run

    def fallar_paso(self, run: EstadoRun, paso: str, error: str) -> EstadoRun:
        run.pasos[paso]["estado"] = EstadoPaso.FALLIDO
        run.pasos[paso]["error"] = error
        run.errores_globales.append(f"[{paso}] {error}")
        self._persistir(run)
        return run

    def omitir_paso(self, run: EstadoRun, paso: str, motivo: str) -> EstadoRun:
        run.pasos[paso]["estado"] = EstadoPaso.OMITIDO
        run.pasos[paso]["resultado"] = {"motivo": motivo}
        self._persistir(run)
        return run

    def debe_ejecutar(self, run: EstadoRun, paso: str) -> bool:
        estado = run.pasos.get(paso, {}).get("estado")
        return estado not in (EstadoPaso.COMPLETADO, EstadoPaso.OMITIDO)

    def finalizar(self, run: EstadoRun, estado: EstadoEjecucion) -> EstadoRun:
        run.estado = estado
        run.fin = datetime.now().isoformat()
        self._persistir(run)
        return run

    def _persistir(self, run: EstadoRun):
        ruta = self.carpeta_runs / f"{run.run_id}.json"
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(asdict(run), f, ensure_ascii=False, indent=2)

    def _buscar_run_reanudable(self, requisito_id: str, hash_yaml: str) -> Optional[EstadoRun]:
        for archivo in sorted(self.carpeta_runs.glob(f"{requisito_id}_*.json"), reverse=True):
            with open(archivo) as f:
                datos = json.load(f)

            if datos.get("hash_yaml") != hash_yaml:
                continue
            if datos.get("estado") in (EstadoEjecucion.COMPLETADO, EstadoEjecucion.RECHAZADO):
                continue

            inicio = datetime.fromisoformat(datos["inicio"])
            if datetime.now() - inicio > timedelta(hours=24):
                continue

            run = EstadoRun(**{k: v for k, v in datos.items() if k in EstadoRun.__dataclass_fields__})
            return run

        return None
