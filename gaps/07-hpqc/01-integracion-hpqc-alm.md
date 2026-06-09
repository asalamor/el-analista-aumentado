# Integración técnica con HP Quality Center / ALM

## Por qué HPQC/ALM requiere un tratamiento específico

La integración con HP Quality Center (también conocido como Micro Focus ALM o OpenText ALM/Quality Center) es funcionalmente equivalente a la integración con Xray o Zephyr descrita en el punto 10 del modelo, pero operativamente más compleja por tres razones estructurales que determinan toda la arquitectura del conector.

**Primera razón: el modelo de datos de ALM no es plano.** ALM organiza los test cases en una jerarquía de carpetas dentro del módulo Test Plan (Subject), y cada test case pertenece a exactamente una carpeta. El pipeline genera test cases vinculados a criterios de aceptación y a historias, pero ALM no tiene una noción nativa de "historia de usuario": hay que diseñar explícitamente la correspondencia entre la estructura del pipeline y la jerarquía de Subject.

**Segunda razón: ALM tiene dos APIs coexistentes con capacidades distintas.** La API REST (disponible desde ALM 11.5x) cubre la mayoría de operaciones de creación y consulta, pero algunas operaciones avanzadas como la creación de test sets o la asignación de configuraciones de ejecución siguen requiriendo la API OTA (Open Test Architecture, basada en COM/ActiveX). El conector debe decidir qué API usar para cada operación, y esa decisión depende de la versión instalada en cada organización.

**Tercera razón: la autenticación de ALM es stateful.** A diferencia de Jira, que acepta autenticación HTTP Basic o Bearer token en cada petición, ALM requiere una sesión de login que devuelve cookies de sesión que deben mantenerse vivas y renovarse periódicamente. Esto impone requisitos de diseño en el cliente HTTP que no están presentes en el conector de Jira del punto 10.

---

## Arquitectura del conector ALM

El conector se diseña con cuatro capas independientes que pueden evolucionar por separado:

```
Pipeline AI (JSON de test cases)
         │
         ▼
┌─────────────────────────────────┐
│  CAPA 1 — Transformador         │
│  JSON pipeline → Modelo ALM     │
│  (mapeo de campos y jerarquía)  │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  CAPA 2 — Gestor de sesión      │
│  Login, cookies, renovación,    │
│  logout y manejo de errores     │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  CAPA 3 — Cliente REST ALM      │
│  CRUD de entidades: Test,       │
│  Test Step, Test Set, Run       │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  CAPA 4 — Gestor de trazabilidad│
│  Registro en el grafo del       │
│  punto 9 con las referencias ALM│
└─────────────────────────────────┘
```

---

## Fase 1 — Estructura de carpetas en ALM (Subject)

La decisión sobre cómo organizar los test cases en ALM es la más importante de toda la integración. Una vez creada la jerarquía y populada con cientos de test cases, cambiarla tiene un coste muy alto. Esta decisión debe tomarse antes de la primera ejecución del conector.

La estructura recomendada refleja la jerarquía del pipeline (Épica → Requisito → Historia → Criterio de aceptación) y permite navegar desde un test case en ALM hasta el requisito que lo originó sin necesidad de consultar el repositorio YAML:

```
Subject/
└── [PROYECTO]
    └── [EP-04] Gestión de Facturación
        └── [REQ-023] Filtrar facturas por rango de fechas
            ├── Funcionales positivos
            │   └── TC-023-01 Filtrado válido devuelve resultados ordenados
            ├── Negativos y errores
            │   ├── TC-023-02 Rango superior a 365 días muestra error
            │   ├── TC-023-03 Búsqueda sin fecha de inicio muestra campo obligatorio
            │   ├── TC-023-04 Usuario sin permisos no puede acceder al módulo
            │   └── TC-023-05 Búsqueda sin resultados muestra estado vacío
            └── Contorno (boundary values)
                ├── TC-023-06 Rango exacto de 365 días es aceptado
                ├── TC-023-07 Rango de 366 días es rechazado
                ├── TC-023-08 Rango de un solo día es aceptado
                └── TC-023-09 Fecha fin anterior a fecha inicio es rechazada
```

Esta estructura tiene tres ventajas operativas. Permite filtrar en ALM todos los test cases de una épica o de un requisito sin necesidad de etiquetas o campos personalizados adicionales. Facilita la identificación visual de qué test cases están automatizados y cuáles son manuales (se puede crear una subcarpeta por tipo si el equipo lo prefiere). Y alinea la vista del QA en ALM con la vista del analista en Jira, reduciendo la fricción cognitiva entre herramientas.

### Nomenclatura de las carpetas

La nomenclatura debe ser estable y única para que el conector pueda localizar carpetas existentes sin ambigüedad. Las reglas son:

- El nombre de la carpeta de épica incluye el ID entre corchetes: `[EP-04] Gestión de Facturación`
- El nombre de la carpeta de requisito incluye el ID entre corchetes: `[REQ-023] Filtrar facturas por rango de fechas`
- Las subcarpetas de tipo son fijas: `Funcionales positivos`, `Negativos y errores`, `Contorno`
- El nombre del test case usa el ID como prefijo: `TC-023-01 Filtrado válido...`

El ID entre corchetes es la clave de idempotencia: el conector busca en ALM si existe una carpeta que contenga `[EP-04]` antes de intentar crearla, lo que garantiza que las re-ejecuciones no generan carpetas duplicadas.

---

## Fase 2 — Mapeo de campos entre el pipeline y ALM

El test case generado por el pipeline en el punto 5 tiene una estructura YAML/JSON bien definida. ALM tiene su propio modelo de entidades con campos obligatorios, opcionales y campos personalizados (User Defined Fields) que varían según la configuración de cada instancia. La tabla de mapeo es el contrato entre ambos sistemas.

### Mapeo de la entidad Test (test case)

| Campo pipeline | Campo ALM | Tipo ALM | Notas |
|---|---|---|---|
| `id` | `user-03` (campo personalizado) | String | Campo personalizado recomendado: `Pipeline TC ID`. Clave de idempotencia. |
| `titulo` | `name` | String (255) | Campo nativo obligatorio |
| `tipo` | `user-04` (campo personalizado) | LookUp List | Valores: `Funcional positivo`, `Negativo validación`, `Negativo permiso`, `Negativo regla negocio`, `Contorno` |
| `prioridad` | `priority` | LookUp List | Mapeo: `critica`→`1-High`, `alta`→`2-Medium`, `media`→`3-Medium`, `baja`→`4-Low` |
| `criterio_origen` | `user-05` (campo personalizado) | String | Referencia al AC origen. Permite trazabilidad inversa. |
| `historia_origen` | `user-06` (campo personalizado) | String | Referencia a la historia de usuario en Jira |
| `requisito_origen` | `user-07` (campo personalizado) | String | Referencia al REQ del repositorio YAML |
| `automatizable` | `user-08` (campo personalizado) | Boolean (Y/N) | Indica si tiene script de automatización asociado |
| `precondiciones` | `description` (preámbulo) | Memo | Se añade como primera sección de la descripción |
| `resultado_final_esperado` | `description` (cierre) | Memo | Se añade como última sección de la descripción |

### Mapeo de los pasos (Test Steps)

Cada elemento del array `pasos` del pipeline se convierte en un paso de ALM. ALM gestiona los pasos como entidades hijas de la entidad Test, con su propia API:

| Campo pipeline | Campo ALM (Step) | Notas |
|---|---|---|
| `paso.numero` | `step-order` | Orden del paso dentro del test case |
| `paso.accion` | `name` | Descripción de la acción del paso |
| `paso.resultado_esperado` | `expected` | Resultado esperado del paso |
| — | `actual` | Se deja vacío en creación; se rellena durante la ejecución |

### Campos personalizados requeridos en ALM

Antes de ejecutar el conector por primera vez, el administrador de ALM debe crear estos campos en la entidad Test del dominio del proyecto:

```
Pipeline TC ID      → String, longitud 20, único por proyecto
TC Tipo             → LookUp List (crear lista con los 5 valores)
Criterio AC Origen  → String, longitud 30
Historia Origen     → String, longitud 20 (para el key de Jira)
Requisito Origen    → String, longitud 20
Automatizable       → Boolean (Y/N)
```

Sin estos campos, el conector no puede garantizar idempotencia ni mantener la trazabilidad bidireccional con el repositorio del pipeline.

---

## Fase 3 — Autenticación y gestión de sesión

La autenticación de ALM es el punto técnico más diferencial respecto a Jira. ALM usa un mecanismo de sesión en dos fases que debe implementarse correctamente para evitar fallos intermitentes en ejecuciones largas (por ejemplo, cuando se procesa una épica completa con decenas de test cases).

```python
import requests
import time
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class ALMConfig:
    base_url: str          # https://alm.empresa.com/qcbin
    dominio: str           # EMPRESA
    proyecto: str          # PROYECTO_X
    usuario: str           # usuario@empresa.com
    password: str          # desde variable de entorno, nunca hardcodeado
    timeout_segundos: int = 30
    max_reintentos: int = 3
    renovar_sesion_cada_minutos: int = 25
    # ALM invalida sesiones tras 30 min de inactividad.
    # Renovar cada 25 para mantener margen de seguridad.


class GestorSesionALM:
    """
    Gestiona el ciclo de vida de la sesión HTTP con ALM.
    ALM requiere:
      1. POST a /authentication-point/authenticate con credenciales Basic
         → devuelve cookie LWSSO_COOKIE_KEY
      2. POST a /rest/site-session
         → devuelve cookies QCSession y XSRF-TOKEN
      3. Mantener ambas cookies en todas las peticiones posteriores
      4. Añadir cabecera X-XSRF-TOKEN con el valor de la cookie XSRF-TOKEN
    """

    def __init__(self, config: ALMConfig):
        self.config = config
        self.session = requests.Session()
        self._sesion_iniciada = False
        self._ultima_actividad = 0
        self._base_api = (
            f"{config.base_url}/rest/domains/{config.dominio}"
            f"/projects/{config.proyecto}"
        )

    def iniciar_sesion(self):
        """
        Ejecuta el handshake de autenticación de dos fases de ALM.
        Debe llamarse antes de cualquier operación sobre la API.
        """
        # FASE 1: Autenticación con credenciales
        url_auth = f"{self.config.base_url}/authentication-point/authenticate"
        respuesta = self.session.post(
            url_auth,
            auth=(self.config.usuario, self.config.password),
            timeout=self.config.timeout_segundos
        )

        if respuesta.status_code != 200:
            raise RuntimeError(
                f"Error de autenticación ALM: HTTP {respuesta.status_code}. "
                f"Verificar credenciales y URL base."
            )

        # LWSSO_COOKIE_KEY queda en self.session.cookies automáticamente

        # FASE 2: Iniciar sesión de proyecto
        url_sesion = f"{self.config.base_url}/rest/site-session"
        respuesta2 = self.session.post(
            url_sesion,
            timeout=self.config.timeout_segundos
        )

        if respuesta2.status_code not in (200, 201):
            raise RuntimeError(
                f"Error iniciando sesión de proyecto ALM: "
                f"HTTP {respuesta2.status_code}"
            )

        # Añadir XSRF-TOKEN a las cabeceras por defecto de la sesión
        xsrf_token = self.session.cookies.get("XSRF-TOKEN")
        if xsrf_token:
            self.session.headers.update({"X-XSRF-TOKEN": xsrf_token})

        self._sesion_iniciada = True
        self._ultima_actividad = time.time()
        logger.info(
            f"Sesión ALM iniciada: {self.config.dominio}/{self.config.proyecto}"
        )

    def cerrar_sesion(self):
        """Cierra la sesión correctamente para liberar recursos en ALM."""
        if not self._sesion_iniciada:
            return
        try:
            self.session.delete(
                f"{self.config.base_url}/rest/site-session",
                timeout=self.config.timeout_segundos
            )
            self.session.get(
                f"{self.config.base_url}/authentication-point/logout",
                timeout=self.config.timeout_segundos
            )
        except Exception as e:
            logger.warning(f"Error al cerrar sesión ALM: {e}")
        finally:
            self._sesion_iniciada = False
            logger.info("Sesión ALM cerrada")

    def _verificar_y_renovar_sesion(self):
        """
        Verifica si la sesión está próxima a expirar y la renueva.
        Se llama automáticamente antes de cada operación.
        """
        if not self._sesion_iniciada:
            self.iniciar_sesion()
            return

        minutos_transcurridos = (
            time.time() - self._ultima_actividad
        ) / 60

        if minutos_transcurridos >= self.config.renovar_sesion_cada_minutos:
            logger.info(
                f"Renovando sesión ALM tras {minutos_transcurridos:.1f} min"
            )
            # ALM permite renovar sin re-autenticarse con un POST vacío
            respuesta = self.session.post(
                f"{self.config.base_url}/rest/site-session",
                timeout=self.config.timeout_segundos
            )
            if respuesta.status_code not in (200, 201):
                # Si la renovación falla, reiniciar sesión completa
                logger.warning(
                    "Renovación falló. Reiniciando sesión completa."
                )
                self.cerrar_sesion()
                self.iniciar_sesion()
            else:
                self._ultima_actividad = time.time()

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        self._verificar_y_renovar_sesion()
        self._ultima_actividad = time.time()
        return self.session.get(
            f"{self._base_api}/{endpoint}",
            params=params,
            timeout=self.config.timeout_segundos
        )

    def post(self, endpoint: str, payload: dict) -> requests.Response:
        self._verificar_y_renovar_sesion()
        self._ultima_actividad = time.time()
        return self.session.post(
            f"{self._base_api}/{endpoint}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout_segundos
        )

    def put(self, endpoint: str, payload: dict) -> requests.Response:
        self._verificar_y_renovar_sesion()
        self._ultima_actividad = time.time()
        return self.session.put(
            f"{self._base_api}/{endpoint}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.config.timeout_segundos
        )

    def __enter__(self):
        self.iniciar_sesion()
        return self

    def __exit__(self, *args):
        self.cerrar_sesion()
```

---

## Fase 4 — Gestión de la jerarquía de carpetas (Subject)

Antes de crear test cases, el conector debe verificar y crear si no existen las carpetas correspondientes en el Subject de ALM. Esta operación es idempotente: si la carpeta ya existe, la reutiliza.

{% raw %}
```python
import json

class GestorCarpetasALM:
    """
    Gestiona la creación y localización de carpetas en el Subject
    del módulo Test Plan de ALM.
    """

    # Subcarpetas fijas por tipo de test case
    SUBCARPETAS_TIPO = [
        "Funcionales positivos",
        "Negativos y errores",
        "Contorno"
    ]

    def __init__(self, sesion: GestorSesionALM):
        self.sesion = sesion
        # Caché local para evitar peticiones repetidas al mismo Subject
        self._cache_carpetas: dict[str, int] = {}

    def obtener_o_crear_carpeta_requisito(
        self,
        epica_id: str,
        epica_titulo: str,
        req_id: str,
        req_titulo: str
    ) -> dict[str, int]:
        """
        Garantiza que existe la jerarquía completa de carpetas para un requisito:
        Subject → [Proyecto] → [EP-xx] Épica → [REQ-xxx] Requisito → [Tipo]

        Retorna un diccionario {tipo: id_carpeta} para cada subcarpeta de tipo.
        """
        # Clave de caché para este requisito
        clave = f"{epica_id}::{req_id}"
        if clave in self._cache_carpetas:
            return self._cache_carpetas[clave]

        # Asegurar carpeta de épica
        nombre_carpeta_epica = f"[{epica_id}] {self._truncar(epica_titulo, 80)}"
        id_epica = self._obtener_o_crear_carpeta(
            nombre=nombre_carpeta_epica,
            id_padre=self._obtener_id_raiz_proyecto()
        )

        # Asegurar carpeta de requisito dentro de la épica
        nombre_carpeta_req = f"[{req_id}] {self._truncar(req_titulo, 80)}"
        id_req = self._obtener_o_crear_carpeta(
            nombre=nombre_carpeta_req,
            id_padre=id_epica
        )

        # Asegurar subcarpetas por tipo
        ids_por_tipo = {}
        for nombre_tipo in self.SUBCARPETAS_TIPO:
            id_tipo = self._obtener_o_crear_carpeta(
                nombre=nombre_tipo,
                id_padre=id_req
            )
            ids_por_tipo[nombre_tipo] = id_tipo

        self._cache_carpetas[clave] = ids_por_tipo
        return ids_por_tipo

    def _obtener_id_raiz_proyecto(self) -> int:
        """Obtiene el ID de la carpeta raíz del proyecto en ALM."""
        respuesta = self.sesion.get(
            "test-folders",
            params={
                "query": "{name['Subject']}",
                "fields": "id,name"
            }
        )
        respuesta.raise_for_status()
        entidades = respuesta.json().get("entities", [])
        if not entidades:
            raise RuntimeError(
                "No se encontró la carpeta Subject raíz en ALM. "
                "Verificar configuración del proyecto."
            )
        return int(entidades[0]["Fields"][0]["values"][0]["value"])

    def _obtener_o_crear_carpeta(self, nombre: str, id_padre: int) -> int:
        """
        Busca una carpeta por nombre dentro de un padre dado.
        Si no existe, la crea.
        La búsqueda usa el ID del padre para evitar colisiones de nombres
        entre ramas distintas del árbol.
        """
        # Buscar carpeta existente
        respuesta = self.sesion.get(
            "test-folders",
            params={
                "query": f"{{parent-id[{id_padre}];name['{self._escapar_query(nombre)}']}}",
                "fields": "id,name"
            }
        )
        respuesta.raise_for_status()
        entidades = respuesta.json().get("entities", [])

        if entidades:
            id_carpeta = int(
                self._extraer_campo(entidades[0], "id")
            )
            logger.debug(f"Carpeta existente: '{nombre}' (id={id_carpeta})")
            return id_carpeta

        # Crear carpeta nueva
        payload = {
            "Fields": [
                {"Name": "name", "values": [{"value": nombre}]},
                {"Name": "parent-id", "values": [{"value": str(id_padre)}]}
            ]
        }
        respuesta_creacion = self.sesion.post("test-folders", payload)
        respuesta_creacion.raise_for_status()
        id_nuevo = int(
            self._extraer_campo(
                respuesta_creacion.json(), "id"
            )
        )
        logger.info(
            f"Carpeta creada: '{nombre}' (id={id_nuevo}, padre={id_padre})"
        )
        return id_nuevo

    @staticmethod
    def _truncar(texto: str, max_chars: int) -> str:
        return texto[:max_chars] if len(texto) > max_chars else texto

    @staticmethod
    def _escapar_query(texto: str) -> str:
        """Escapa caracteres especiales para las queries de ALM."""
        return texto.replace("'", "\\'").replace("[", "\\[").replace("]", "\\]")

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                if valores:
                    return valores[0].get("value", "")
        return ""
```
{% endraw %}

---

## Fase 5 — Transformador: JSON del pipeline → Entidades ALM

El transformador es el componente que convierte el JSON generado por los prompts del punto 5 al formato de entidades que espera la API REST de ALM.

```python
class TransformadorALM:
    """
    Convierte los test cases del pipeline AI al formato de entidades ALM.
    """

    # Mapeo de prioridades pipeline → valores ALM
    MAPA_PRIORIDAD = {
        "critica": "1-High",
        "alta":    "2-Medium",
        "media":   "3-Medium",
        "baja":    "4-Low"
    }

    # Mapeo de tipo de TC → subcarpeta ALM
    MAPA_TIPO_A_CARPETA = {
        "funcional_positivo":      "Funcionales positivos",
        "negativo_validacion":     "Negativos y errores",
        "negativo_permiso":        "Negativos y errores",
        "negativo_regla_negocio":  "Negativos y errores",
        "negativo_concurrencia":   "Negativos y errores",
        "negativo_sistema":        "Negativos y errores",
        "contorno":                "Contorno"
    }

    def tc_a_entidad_alm(
        self,
        tc: dict,
        id_carpeta: int
    ) -> dict:
        """
        Convierte un test case del pipeline a la estructura de entidad ALM.
        El resultado es el payload para POST /tests.
        """
        descripcion = self._construir_descripcion(tc)

        return {
            "Fields": [
                # Campos nativos de ALM
                {
                    "Name": "name",
                    "values": [{"value": tc["titulo"][:255]}]
                },
                {
                    "Name": "parent-id",
                    "values": [{"value": str(id_carpeta)}]
                },
                {
                    "Name": "priority",
                    "values": [{
                        "value": self.MAPA_PRIORIDAD.get(
                            tc.get("prioridad", "media"), "3-Medium"
                        )
                    }]
                },
                {
                    "Name": "description",
                    "values": [{"value": descripcion}]
                },
                {
                    "Name": "status",
                    "values": [{"value": "Ready"}]
                },
                # Campos personalizados (nombres reales dependen de la config de ALM)
                {
                    "Name": "user-03",  # Pipeline TC ID
                    "values": [{"value": tc["id"]}]
                },
                {
                    "Name": "user-04",  # TC Tipo
                    "values": [{"value": tc.get("tipo", "")}]
                },
                {
                    "Name": "user-05",  # Criterio AC Origen
                    "values": [{"value": tc.get("criterio_origen", "")}]
                },
                {
                    "Name": "user-06",  # Historia Origen (Jira key)
                    "values": [{"value": tc.get("historia_origen", "")}]
                },
                {
                    "Name": "user-07",  # Requisito Origen
                    "values": [{"value": tc.get("requisito_origen", "")}]
                },
                {
                    "Name": "user-08",  # Automatizable
                    "values": [{"value": "Y" if tc.get("automatizable") else "N"}]
                }
            ]
        }

    def pasos_a_entidades_alm(self, tc: dict) -> list[dict]:
        """
        Convierte los pasos del test case a la lista de entidades DesignStep de ALM.
        """
        pasos = []

        # Paso 0 implícito: precondiciones como primer paso especial
        if tc.get("precondiciones"):
            texto_precs = "\n".join(
                f"{i+1}. {p}"
                for i, p in enumerate(tc["precondiciones"])
            )
            pasos.append({
                "Fields": [
                    {
                        "Name": "name",
                        "values": [{"value": "PRECONDICIONES"}]
                    },
                    {
                        "Name": "description",
                        "values": [{"value": texto_precs}]
                    },
                    {
                        "Name": "expected",
                        "values": [{"value": "Sistema en el estado descrito"}]
                    },
                    {
                        "Name": "step-order",
                        "values": [{"value": "1"}]
                    }
                ]
            })

        # Pasos del test case
        for paso in tc.get("pasos", []):
            numero = paso["numero"] + 1  # +1 porque el paso 1 son precondiciones
            pasos.append({
                "Fields": [
                    {
                        "Name": "name",
                        "values": [{"value": str(paso["accion"])[:500]}]
                    },
                    {
                        "Name": "description",
                        "values": [{"value": str(paso["accion"])}]
                    },
                    {
                        "Name": "expected",
                        "values": [{"value": str(paso["resultado_esperado"])}]
                    },
                    {
                        "Name": "step-order",
                        "values": [{"value": str(numero)}]
                    }
                ]
            })

        return pasos

    def _construir_descripcion(self, tc: dict) -> str:
        """
        Construye el texto de descripción del test case en ALM.
        ALM soporta HTML básico en el campo description.
        """
        partes = []

        if tc.get("precondiciones"):
            partes.append("<b>PRECONDICIONES:</b>")
            for prec in tc["precondiciones"]:
                partes.append(f"&bull; {prec}")

        if tc.get("datos_prueba"):
            partes.append("<br/><b>DATOS DE PRUEBA:</b>")
            for campo, valor in tc["datos_prueba"].items():
                partes.append(f"&bull; {campo} = {valor}")

        if tc.get("resultado_final_esperado"):
            partes.append("<br/><b>RESULTADO FINAL ESPERADO:</b>")
            partes.append(tc["resultado_final_esperado"])

        if tc.get("notas_automatizacion"):
            partes.append("<br/><b>NOTAS DE AUTOMATIZACIÓN:</b>")
            partes.append(tc["notas_automatizacion"])

        return "<br/>".join(partes)
```

---

## Fase 6 — Conector principal ALM

El conector principal orquesta las fases anteriores en el orden correcto: verificar idempotencia, crear o actualizar la carpeta, crear el test case y crear sus pasos. Se integra como el paso `s9b_push_alm` del orquestador del script principal.

```python
from dataclasses import dataclass, field

@dataclass
class ResultadoPushALM:
    requisito_id: str
    exito: bool
    test_cases_creados: list[str] = field(default_factory=list)
    test_cases_actualizados: list[str] = field(default_factory=list)
    test_cases_omitidos: list[str] = field(default_factory=list)
    errores: list[str] = field(default_factory=list)
    ids_alm: dict[str, int] = field(default_factory=dict)
    # Mapa tc_id → id_entidad_ALM para el registro de trazabilidad


class ConectorALM:
    """
    Conector principal. Empuja test cases generados por el pipeline
    al módulo Test Plan de ALM, gestionando idempotencia y trazabilidad.
    """

    def __init__(self, config: ALMConfig, motor_trazabilidad=None):
        self.config = config
        self.trazabilidad = motor_trazabilidad
        self.transformador = TransformadorALM()

    def push_test_cases_requisito(
        self,
        test_cases: list[dict],
        requisito: dict,
        historia_jira_key: str
    ) -> ResultadoPushALM:
        """
        Punto de entrada principal del conector.
        Procesa todos los test cases de un requisito en una única sesión ALM.
        """
        req_id = requisito["id"]
        resultado = ResultadoPushALM(requisito_id=req_id, exito=False)

        with GestorSesionALM(self.config) as sesion:
            gestor_carpetas = GestorCarpetasALM(sesion)

            # PASO 1: Asegurar jerarquía de carpetas
            try:
                ids_carpetas = gestor_carpetas.obtener_o_crear_carpeta_requisito(
                    epica_id=requisito.get("epica", "EP-00"),
                    epica_titulo=requisito.get("modulo", "Módulo sin nombre"),
                    req_id=req_id,
                    req_titulo=requisito.get("titulo", req_id)
                )
            except Exception as e:
                resultado.errores.append(f"Error creando carpetas: {e}")
                return resultado

            # PASO 2: Procesar cada test case
            for tc in test_cases:
                try:
                    # Añadir referencia a la historia Jira
                    tc["historia_origen"] = historia_jira_key

                    # Determinar carpeta destino según tipo
                    nombre_subcarpeta = self.transformador.MAPA_TIPO_A_CARPETA.get(
                        tc.get("tipo", "funcional_positivo"),
                        "Funcionales positivos"
                    )
                    id_carpeta = ids_carpetas.get(
                        nombre_subcarpeta,
                        list(ids_carpetas.values())[0]
                    )

                    # Verificar idempotencia
                    accion, id_existente = self._verificar_idempotencia(
                        sesion, tc["id"]
                    )

                    if accion == "omitir":
                        resultado.test_cases_omitidos.append(tc["id"])
                        resultado.ids_alm[tc["id"]] = id_existente
                        logger.info(
                            f"TC {tc['id']} existe en ALM (id={id_existente}). "
                            f"Omitiendo."
                        )
                        continue

                    # Construir payload
                    payload_tc = self.transformador.tc_a_entidad_alm(tc, id_carpeta)

                    if accion == "actualizar" and id_existente:
                        # Actualizar test case existente
                        respuesta = sesion.put(
                            f"tests/{id_existente}",
                            payload_tc
                        )
                        respuesta.raise_for_status()
                        id_alm = id_existente
                        resultado.test_cases_actualizados.append(tc["id"])
                        logger.info(f"TC {tc['id']} actualizado en ALM (id={id_alm})")

                    else:
                        # Crear test case nuevo
                        respuesta = sesion.post("tests", payload_tc)
                        respuesta.raise_for_status()
                        id_alm = int(
                            self._extraer_campo(respuesta.json(), "id")
                        )
                        resultado.test_cases_creados.append(tc["id"])
                        logger.info(f"TC {tc['id']} creado en ALM (id={id_alm})")

                    resultado.ids_alm[tc["id"]] = id_alm

                    # Crear pasos del test case
                    self._crear_pasos(sesion, id_alm, tc)

                    # Registrar en el grafo de trazabilidad
                    if self.trazabilidad and id_alm:
                        self._registrar_trazabilidad(
                            tc_id=tc["id"],
                            id_alm=id_alm,
                            historia_jira_key=historia_jira_key,
                            req_id=req_id
                        )

                except Exception as e:
                    error_msg = f"Error procesando {tc.get('id', '?')}: {e}"
                    resultado.errores.append(error_msg)
                    logger.error(error_msg, exc_info=True)

        resultado.exito = len(resultado.errores) == 0
        return resultado

    def _verificar_idempotencia(
        self,
        sesion: GestorSesionALM,
        tc_id: str
    ) -> tuple[str, Optional[int]]:
        """
        Verifica si el test case ya existe en ALM usando el Pipeline TC ID.
        Retorna ('crear', None), ('actualizar', id) u ('omitir', id).
        """
        respuesta = sesion.get(
            "tests",
            params={
                "query": f"{{user-03['{tc_id}']}}",
                "fields": "id,name,status"
            }
        )

        if respuesta.status_code != 200:
            return "crear", None

        entidades = respuesta.json().get("entities", [])
        if not entidades:
            return "crear", None

        id_existente = int(self._extraer_campo(entidades[0], "id"))
        estado = self._extraer_campo(entidades[0], "status")

        # Si está en ejecución activa, no modificar
        if estado in ("Running", "In Progress"):
            return "omitir", id_existente

        return "actualizar", id_existente

    def _crear_pasos(
        self,
        sesion: GestorSesionALM,
        id_test: int,
        tc: dict
    ):
        """
        Crea los pasos del test case en ALM.
        Los pasos anteriores se eliminan y se recrean para garantizar
        consistencia cuando se actualiza un TC existente.
        """
        # Eliminar pasos existentes si es una actualización
        respuesta_pasos = sesion.get(f"tests/{id_test}/design-steps")
        if respuesta_pasos.status_code == 200:
            pasos_existentes = respuesta_pasos.json().get("entities", [])
            for paso in pasos_existentes:
                id_paso = self._extraer_campo(paso, "id")
                if id_paso:
                    sesion.session.delete(
                        f"{sesion._base_api}/tests/{id_test}"
                        f"/design-steps/{id_paso}",
                        timeout=sesion.config.timeout_segundos
                    )

        # Crear nuevos pasos
        pasos_alm = self.transformador.pasos_a_entidades_alm(tc)
        for payload_paso in pasos_alm:
            respuesta = sesion.post(
                f"tests/{id_test}/design-steps",
                payload_paso
            )
            if respuesta.status_code not in (200, 201):
                logger.warning(
                    f"Error creando paso en TC ALM id={id_test}: "
                    f"HTTP {respuesta.status_code}"
                )

    def _registrar_trazabilidad(
        self,
        tc_id: str,
        id_alm: int,
        historia_jira_key: str,
        req_id: str
    ):
        """Registra el vínculo TC pipeline ↔ entidad ALM en el grafo."""
        try:
            from state import Nodo, Arista
            self.trazabilidad.registrar_nodo(Nodo(
                id=f"ALM-{id_alm}",
                tipo="test_case_alm",
                titulo=tc_id,
                estado="Ready",
                metadatos={
                    "alm_id": id_alm,
                    "pipeline_tc_id": tc_id,
                    "historia_jira": historia_jira_key,
                    "requisito_origen": req_id
                }
            ))
            self.trazabilidad.registrar_arista(Arista(
                origen_id=tc_id,
                destino_id=f"ALM-{id_alm}",
                tipo_relacion="vincula",
                origen_relacion="push_alm"
            ))
        except Exception as e:
            logger.warning(f"Error registrando trazabilidad ALM: {e}")

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                if valores:
                    return valores[0].get("value", "")
        return ""
```

---

## Fase 7 — Sincronización inversa: resultados de ejecución ALM → grafo de trazabilidad

La integración no es solo de entrada (pipeline → ALM). Los resultados de ejecución de los test cases en ALM deben fluir de vuelta al grafo de trazabilidad del punto 9, de forma que la matriz de trazabilidad del punto 9 refleje el último estado de ejecución real, no solo el estado de creación.

Esta sincronización se ejecuta de forma programada (por ejemplo, al final de cada jornada de testing o al cerrar un ciclo de pruebas) y no en tiempo real, porque ALM no tiene un sistema de webhooks equivalente al de Jira.

```python
class SincronizadorResultadosALM:
    """
    Lee los resultados de ejecución de ALM y actualiza el grafo
    de trazabilidad con el último estado de cada test case.
    """

    MAPA_ESTADO_ALM_A_PIPELINE = {
        "Passed":  "pasado",
        "Failed":  "fallido",
        "Blocked": "bloqueado",
        "N/A":     "no_aplica",
        "No Run":  "pendiente"
    }

    def __init__(self, sesion: GestorSesionALM, motor_trazabilidad):
        self.sesion = sesion
        self.trazabilidad = motor_trazabilidad

    def sincronizar_resultados_epica(self, epica_id: str) -> dict:
        """
        Recupera el último resultado de ejecución de todos los test cases
        de una épica en ALM y actualiza el grafo de trazabilidad.
        """
        resultados = {
            "epica_id": epica_id,
            "test_cases_sincronizados": 0,
            "pasados": 0,
            "fallidos": 0,
            "bloqueados": 0,
            "pendientes": 0
        }

        # Buscar test cases de la épica por el campo Pipeline TC ID
        # (el ID de los TCs tiene el prefijo del req que pertenece a la épica)
        respuesta = self.sesion.get(
            "tests",
            params={
                # Buscar todos los TCs cuyo Requisito Origen pertenece a la épica
                # Requiere el campo personalizado user-07 (Requisito Origen)
                "query": f"{{user-07['REQ-*']}}",
                "fields": "id,name,user-03,user-07,status",
                "page-size": 200
            }
        )

        if respuesta.status_code != 200:
            logger.error(
                f"Error consultando TCs en ALM para {epica_id}: "
                f"HTTP {respuesta.status_code}"
            )
            return resultados

        test_cases = respuesta.json().get("entities", [])

        for tc in test_cases:
            tc_pipeline_id = self._extraer_campo(tc, "user-03")
            id_alm = self._extraer_campo(tc, "id")

            if not tc_pipeline_id or not id_alm:
                continue

            # Obtener última ejecución del test case
            ultimo_estado = self._obtener_ultimo_resultado(int(id_alm))

            if not ultimo_estado:
                continue

            estado_pipeline = self.MAPA_ESTADO_ALM_A_PIPELINE.get(
                ultimo_estado, "pendiente"
            )

            # Actualizar nodo en el grafo
            try:
                self.trazabilidad.registrar_nodo(Nodo(
                    id=tc_pipeline_id,
                    tipo="test_case",
                    titulo=self._extraer_campo(tc, "name"),
                    estado=estado_pipeline,
                    metadatos={
                        "alm_id": int(id_alm),
                        "ultimo_estado_alm": ultimo_estado,
                        "fecha_sincronizacion": datetime.now().isoformat()
                    }
                ))
            except Exception as e:
                logger.warning(
                    f"Error actualizando trazabilidad TC {tc_pipeline_id}: {e}"
                )
                continue

            resultados["test_cases_sincronizados"] += 1
            contadores = {
                "pasado": "pasados",
                "fallido": "fallidos",
                "bloqueado": "bloqueados",
                "pendiente": "pendientes"
            }
            clave = contadores.get(estado_pipeline)
            if clave:
                resultados[clave] += 1

        return resultados

    def _obtener_ultimo_resultado(self, id_test: int) -> Optional[str]:
        """
        Consulta el último resultado de ejecución de un test case en ALM.
        Devuelve el estado (Passed, Failed, etc.) o None si no hay ejecuciones.
        """
        respuesta = self.sesion.get(
            f"tests/{id_test}/runs",
            params={
                "fields": "id,status,execution-date",
                "order-by": "{execution-date[DESC]}",
                "page-size": 1
            }
        )

        if respuesta.status_code != 200:
            return None

        runs = respuesta.json().get("entities", [])
        if not runs:
            return None

        return self._extraer_campo(runs[0], "status")

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                if valores:
                    return valores[0].get("value", "")
        return ""
```

---

## Fase 8 — Integración en el orquestador principal

El conector ALM se integra en el script orquestador del modelo como el paso `s9b_push_alm`, equivalente al `s9b_push_xray` pero para organizaciones que usan HPQC/ALM como herramienta de gestión de pruebas.

En el archivo `orchestrator.py`, dentro de la función `ejecutar_pipeline_requisito`:

```python
# ══════════════════════════════════════════════════════
# PASO 9B (variante) — Push test cases a HPQC/ALM
# ══════════════════════════════════════════════════════
paso = "s9b_push_alm"

if not config.alm.activo:
    run = gestor.omitir_paso(
        run, paso, "ALM desactivado en configuración."
    )
    _log_omitido(paso, "ALM desactivado")

elif gestor.debe_ejecutar(run, paso):
    _log_paso("9b", "Push test cases a HPQC/ALM")
    run = gestor.iniciar_paso(run, paso)
    try:
        historia_key = run.resultado_jira.get("historia_key")

        conector_alm = ConectorALM(
            config=config.alm,
            motor_trazabilidad=motor_trazabilidad
        )
        resultado_alm = conector_alm.push_test_cases_requisito(
            test_cases=run.test_cases_generados or [],
            requisito=requisito,
            historia_jira_key=historia_key
        )

        n_creados = len(resultado_alm.test_cases_creados)
        n_actualizados = len(resultado_alm.test_cases_actualizados)
        n_omitidos = len(resultado_alm.test_cases_omitidos)

        run = gestor.completar_paso(run, paso, {
            "creados": n_creados,
            "actualizados": n_actualizados,
            "omitidos": n_omitidos,
            "errores": resultado_alm.errores
        })

        _log_ok(
            f"{n_creados} creados · {n_actualizados} actualizados · "
            f"{n_omitidos} omitidos en ALM"
        )

        if resultado_alm.errores:
            for error in resultado_alm.errores:
                _log_advertencia(f"ALM: {error}")

    except Exception as e:
        # ALM no es bloqueante para el resto del pipeline
        log.warning(f"  ⚠ Push ALM falló: {e}")
        run = gestor.omitir_paso(run, paso, str(e))

else:
    _log_reanudado(paso)
```

La configuración del conector ALM se añade a `config.py`:

```python
@dataclass
class ALMConfig:
    activo: bool = os.getenv("ALM_ACTIVO", "false").lower() == "true"
    base_url: str = os.getenv("ALM_BASE_URL", "")
    dominio: str  = os.getenv("ALM_DOMINIO", "")
    proyecto: str = os.getenv("ALM_PROYECTO", "")
    usuario: str  = os.getenv("ALM_USUARIO", "")
    password: str = os.getenv("ALM_PASSWORD", "")
    # Nombres de campos personalizados (configurables por instancia)
    campo_pipeline_tc_id: str = os.getenv("ALM_CAMPO_TC_ID",   "user-03")
    campo_tipo:           str = os.getenv("ALM_CAMPO_TIPO",    "user-04")
    campo_criterio_ac:    str = os.getenv("ALM_CAMPO_AC",      "user-05")
    campo_historia_jira:  str = os.getenv("ALM_CAMPO_HIST",    "user-06")
    campo_req_origen:     str = os.getenv("ALM_CAMPO_REQ",     "user-07")
    campo_automatizable:  str = os.getenv("ALM_CAMPO_AUTO",    "user-08")
    renovar_sesion_min:   int = int(os.getenv("ALM_RENOVAR_SESION", "25"))
```

---

## Comparativa con la integración Xray/Zephyr

Para organizaciones que tienen la opción de elegir entre herramientas, esta tabla resume las diferencias operativas entre las tres integraciones soportadas por el modelo:

| Dimensión | Xray (Jira) | Zephyr Scale | HPQC/ALM |
|---|---|---|---|
| Autenticación | Bearer token (stateless) | Bearer token (stateless) | Sesión con cookies (stateful) |
| Jerarquía de carpetas | Heredada de Jira | Propia (folders) | Subject tree propio |
| Idempotencia | Por campo personalizado | Por campo `tc-key` | Por campo personalizado |
| Webhooks (resultados) | Sí (nativo) | Sí (nativo) | No — requiere polling |
| Formato de pasos | JSON directo | JSON directo | Entidades hijas separadas |
| Complejidad de integración | Baja | Media | Alta |
| Requisito de administrador | Crear campos personalizados Jira | Crear campos Zephyr | Crear UDF en ALM + configuración |
| Versionado de test cases | Heredado de Jira | Propio | Propio (historial de versiones) |
| Idoneidad para proyectos regulados | Media | Media | Alta (trazabilidad, auditoría) |

La complejidad mayor de ALM no es un inconveniente en sí mismo: ALM aporta capacidades de gestión de pruebas, trazabilidad de requisitos propia y auditoría que las herramientas más ligeras no tienen. El conector descrito en este punto aprovecha esas capacidades sin imponer trabajo manual al analista.

---

## Lista de verificación antes de la primera ejecución

Antes de ejecutar el conector por primera vez en un proyecto, el administrador de ALM y el responsable técnico del pipeline deben completar estos pasos en orden:

**En ALM (administrador de ALM):**

- [ ] Crear los seis campos personalizados (UDF) en la entidad Test del dominio/proyecto
- [ ] Crear la lista de valores para el campo `TC Tipo` con los cinco valores del modelo
- [ ] Verificar que el usuario del conector tiene permisos de lectura y escritura en el módulo Test Plan
- [ ] Confirmar la versión de ALM instalada (determina disponibilidad de la API REST v2)
- [ ] Documentar los nombres reales de los campos personalizados creados (para el archivo `.env`)

**En el pipeline (responsable técnico):**

- [ ] Configurar las variables de entorno `ALM_*` en el archivo `.env`
- [ ] Ejecutar `python orchestrator.py --req REQ-TEST-001 --dry-run` para validar la transformación sin push
- [ ] Ejecutar `python orchestrator.py --req REQ-TEST-001` sobre un requisito de prueba en ALM de desarrollo
- [ ] Verificar en ALM que la jerarquía de carpetas, el test case y sus pasos se crearon correctamente
- [ ] Verificar que los campos personalizados tienen los valores correctos
- [ ] Ejecutar el sincronizador de resultados y verificar que el grafo de trazabilidad se actualiza
- [ ] Documentar los IDs reales de ALM en el grafo de trazabilidad para validar la trazabilidad bidireccional

---

*Punto A desarrollado como parte del Modelo Operativo — Análisis Funcional AI-Ready.*
*Referencia cruzada: Punto 5 (Generación de test cases), Punto 9 (Grafo de trazabilidad), Punto 10 (Integración Jira API), Punto B (Gobierno del ciclo de vida de pruebas en ALM).*
