# steps/s9_push.py
"""
Paso 9 — Push a Jira API y Xray.
Usa el ConectorJira del punto 10 para crear todos los artefactos
aprobados en el proyecto Jira y los test cases en Xray/Zephyr.
Ver implementación completa en: jira/conector_jira.py
"""

from config import PipelineConfig


async def push_a_jira(
    artefactos: dict,
    requisito_id: str,
    config: PipelineConfig
) -> dict:
    """
    Crea o actualiza los artefactos en Jira usando el ConectorJira.
    Implementa idempotencia: no crea duplicados si el requisito
    ya tiene issues vinculados.
    """
    try:
        from jira.conector_jira import ConectorJira
        from trazabilidad.motor_trazabilidad import MotorTrazabilidad

        motor_traz = MotorTrazabilidad(config.db.to_dict())
        conector = ConectorJira(config.jira, motor_traz)

        resultado = conector.procesar_requisito_completo({
            "requisito_id": requisito_id,
            **artefactos
        })

        return {
            "exito": resultado.exito,
            "epica_key":    resultado.epica_key,
            "historia_key": resultado.historia_key,
            "tareas_keys":  resultado.tareas_keys,
            "errores":      resultado.errores,
            "advertencias": resultado.advertencias,
            "acciones":     resultado.acciones_realizadas
        }

    except ImportError as e:
        return {
            "exito": False,
            "errores": [f"Módulo de Jira no disponible: {e}"],
            "nota": "Revisa jira/conector_jira.py y las credenciales en .env"
        }
    except Exception as e:
        return {
            "exito": False,
            "errores": [str(e)]
        }


async def push_a_xray(
    test_cases: list,
    historia_key: str,
    requisito_id: str,
    config: PipelineConfig
) -> dict:
    """
    Importa los test cases generados a Xray vinculándolos
    a la historia de usuario correspondiente.
    """
    if not test_cases:
        return {"test_cases_creados": 0, "nota": "Sin test cases que importar"}

    try:
        from jira.conector_xray import ConectorXray

        conector = ConectorXray(config.jira)
        keys = conector.crear_test_cases(test_cases, historia_key, requisito_id)

        return {
            "test_cases_creados": len(keys),
            "keys_creados": keys
        }

    except ImportError as e:
        return {
            "test_cases_creados": 0,
            "errores": [f"Módulo Xray no disponible: {e}"],
            "nota": "Revisa jira/conector_xray.py y las credenciales Xray en .env"
        }
    except Exception as e:
        return {
            "test_cases_creados": 0,
            "errores": [str(e)]
        }
