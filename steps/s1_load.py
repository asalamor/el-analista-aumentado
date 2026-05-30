# steps/s1_load.py
"""Paso 1 — Carga y parseo del YAML de requisito."""

import yaml
from typing import Union


def cargar_requisito(yaml_content: Union[str, bytes]) -> dict:
    """
    Parsea el contenido YAML del requisito y valida la estructura mínima.
    Lanza ValueError si el YAML no es válido o le falta el campo 'id'.
    """
    try:
        requisito = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML inválido: {e}")

    if not isinstance(requisito, dict):
        raise ValueError("El YAML no contiene un objeto de requisito válido.")

    if not requisito.get("id"):
        raise ValueError("El requisito no tiene campo 'id'.")

    return requisito
