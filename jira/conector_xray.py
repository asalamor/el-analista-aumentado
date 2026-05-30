# jira/conector_xray.py
"""
Conector con Xray para importación de test cases.
Integra los test cases generados por el pipeline con
el módulo de gestión de pruebas de Jira.
"""

import requests
import logging

log = logging.getLogger("xray_conector")


class ConectorXray:
    """Importa test cases generados al módulo Xray de Jira."""

    def __init__(self, jira_config):
        self.config   = jira_config
        self.base_url = f"{jira_config.base_url}/rest/raven/1.0"
        self.auth     = (jira_config.user_email, jira_config.api_token)

    def crear_test_cases(
        self,
        test_cases: list[dict],
        historia_key: str,
        requisito_id: str
    ) -> list[str]:
        """Crea los test cases en Xray vinculados a la historia."""
        keys_creados = []

        for tc in test_cases:
            payload = self._construir_payload(tc, historia_key, requisito_id)
            try:
                response = requests.post(
                    f"{self.base_url}/import/test",
                    json=payload,
                    auth=self.auth,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                response.raise_for_status()
                datos = response.json()
                tc_key = datos.get("testIssues", [{}])[0].get("key")
                if tc_key:
                    keys_creados.append(tc_key)
                    log.info(f"Test case {tc_key} creado en Xray")
            except Exception as e:
                log.error(f"Error creando TC {tc.get('id','?')}: {e}")

        return keys_creados

    def _construir_payload(
        self,
        tc: dict,
        historia_key: str,
        requisito_id: str
    ) -> dict:
        return {
            "testExecution": {
                "projectKey": self.config.project_key,
                "summary": f"Test cases — {historia_key} — {requisito_id}"
            },
            "tests": [{
                "summary": tc.get("titulo", ""),
                "type": "Cucumber" if tc.get("automatizable") else "Manual",
                "projectKey": self.config.project_key,
                "definition": tc.get("gherkin_script", ""),
                "steps": [
                    {
                        "action": paso.get("accion", ""),
                        "result": paso.get("resultado_esperado", "")
                    }
                    for paso in tc.get("pasos", [])
                ],
                "precondition": "\n".join(tc.get("precondiciones", [])),
                "labels": [
                    tc.get("tipo", ""),
                    tc.get("criterio_origen", ""),
                    requisito_id
                ],
                "requirements": [historia_key]
            }]
        }
