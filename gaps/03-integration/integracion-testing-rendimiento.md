# Integración con herramientas de testing de rendimiento

## El problema que resuelve

Los criterios de rendimiento en el modelo operativo tienen una ubicación definida. En la plantilla YAML del punto 1 viven en dos lugares: en el campo `tiempo_respuesta_max_ms` de los datos de salida, y en el campo `rendimiento` del bloque de restricciones no funcionales. En los criterios de aceptación, cuando el analista los documenta correctamente, aparecen como criterios de tipo `contorno` con datos concretos: tiempos máximos de respuesta, percentiles, número de usuarios concurrentes y volumen de datos.

El problema es el mismo que con los criterios funcionales antes de la automatización: alguien tiene que convertir esos criterios en scripts ejecutables. Un criterio que dice "el sistema debe responder en menos de 2 segundos para el percentil 95 con 100 usuarios concurrentes" termina siendo interpretado de formas distintas por el QA que escribe el script de JMeter y por el desarrollador que diseña la arquitectura. Si el criterio cambia en el requisito, el script no se actualiza automáticamente. Si el script falla en CI, no hay trazabilidad directa hacia el criterio de aceptación que está roto.

La integración con herramientas de testing de rendimiento cierra ese ciclo. Lee los criterios de rendimiento del YAML del requisito y los criterios de aceptación de tipo contorno, y genera scripts ejecutables para JMeter y k6 que verifican exactamente lo que el analista especificó, con los datos de prueba concretos y los umbrales correctos. Los scripts generados se registran en el grafo de trazabilidad del punto 9 vinculados al criterio de aceptación que los originó, de forma que cuando el pipeline detecta un cambio en ese criterio, sabe exactamente qué script debe regenerarse.

---

## Qué información del YAML origina los scripts de rendimiento

No todos los campos del requisito YAML son relevantes para el testing de rendimiento. El generador extrae sus inputs de cuatro fuentes específicas dentro de la plantilla.

```
FUENTE EN EL YAML                    → USÉ EN EL SCRIPT
─────────────────────────────────────────────────────────────────────────────
datos_salida.tiempo_respuesta_max_ms → Umbral de tiempo de respuesta (threshold)
datos_salida.max_registros           → Volumen de datos para las peticiones
datos_salida.formato                 → Tipo de petición HTTP y validación de respuesta

restricciones_no_funcionales:
  rendimiento                        → Texto libre con parámetros adicionales:
                                       percentil, usuarios concurrentes, ramp-up
  volumen_datos                      → Dataset de prueba en el entorno de staging

criterios_aceptacion (tipo: contorno):
  dado                               → Precondiciones y estado del entorno
  cuando                             → Configuración de la carga: N usuarios
  entonces                           → Umbral de tiempo + comportamiento esperado
  datos_ejemplo                      → Parámetros concretos de la prueba

datos_entrada:
  nombre, tipo, formato, rango       → Parámetros del request HTTP
  valores_enum                       → Valores para parametrizar el dataset
```

El generador parsea el texto libre del campo `rendimiento` buscando patrones reconocibles. Un texto como "< 2 segundos p95 con 100 usuarios concurrentes" se descompone en: umbral `2000ms`, percentil `p95`, usuarios `100`. Si el campo usa un formato diferente, el LLM actúa como intérprete y produce la estructura normalizada antes de generar el script.

---

## Arquitectura del generador

```
Requisito YAML validado
        │
        ▼
[Extractor de criterios de rendimiento]
Lee los campos relevantes del YAML y produce
una especificación de carga normalizada
        │
        ▼
[Intérprete LLM]
Convierte texto libre en parámetros estructurados
cuando los campos no siguen el formato estándar
        │
        ▼
[Constructor de escenarios de carga]
Diseña los escenarios: carga constante, ramp-up,
spike, soak, basados en los criterios del requisito
        │
        ├──[Generador JMeter]──────────────────────────────────────────
        │   Produce el archivo .jmx con todos los                     │
        │   elementos del plan de prueba                              ▼
        │                                               Script JMeter (.jmx)
        │
        └──[Generador k6]──────────────────────────────────────────────
            Produce el script JavaScript de k6                        │
            con thresholds y configuración de VUs                     ▼
                                                        Script k6 (.js)
        │
        ▼
[Registrador de trazabilidad]
Vincula cada script al criterio de aceptación
que lo originó en el grafo del punto 9
        │
        ▼
[Validador de umbrales en CI/CD]
Step de GitHub Actions / GitLab CI que ejecuta
el script y verifica los thresholds automáticamente
```

---

## Extractor de criterios de rendimiento

El extractor lee el YAML del requisito y produce una especificación de carga normalizada que los generadores de script consumen de forma determinista.

```python
# extractor_criterios_rendimiento.py

import re
import yaml
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EspecificacionCarga:
    """
    Representación normalizada de los criterios de rendimiento
    extraídos de un requisito YAML. Es el input de ambos generadores.
    """
    requisito_id: str
    criterio_ac_id: str         # ID del criterio AC de origen
    endpoint: str               # URL o ruta del endpoint a probar
    metodo_http: str            # GET │ POST │ PUT │ DELETE │ PATCH
    # Umbrales de rendimiento
    tiempo_respuesta_p50_ms: Optional[int]
    tiempo_respuesta_p90_ms: Optional[int]
    tiempo_respuesta_p95_ms: Optional[int]
    tiempo_respuesta_p99_ms: Optional[int]
    tiempo_respuesta_max_ms: Optional[int]
    tasa_error_max_pct: float           # Porcentaje máximo de errores permitido
    # Configuración de carga
    usuarios_concurrentes: int
    ramp_up_segundos: int               # Tiempo para alcanzar carga máxima
    duracion_prueba_segundos: int       # Duración total del test
    # Configuración de datos
    parametros_request: list[dict]      # Campos del request con sus tipos y rangos
    cuerpo_request: Optional[dict]      # Body para POST/PUT
    cabeceras_http: dict
    codigo_respuesta_esperado: int
    validaciones_respuesta: list[str]   # Expresiones para validar el body
    # Datos de prueba
    dataset_parametrizado: list[dict]   # Filas de datos para parametrizar
    volumen_datos_bd: str               # Descripción del dataset en BD
    # Metadatos
    nombre_escenario: str
    descripcion: str
    tipo_escenario: str     # baseline │ carga │ estres │ spike │ soak


class ExtractorCriteriosRendimiento:
    """
    Extrae y normaliza los criterios de rendimiento de un requisito YAML.
    """

    # Patrones para parsear texto libre de rendimiento
    PATRON_TIEMPO = re.compile(
        r'[<≤]\s*(\d+(?:\.\d+)?)\s*(s|seg|segundo|segundos|ms|miliseg)',
        re.IGNORECASE
    )
    PATRON_PERCENTIL = re.compile(
        r'p(\d{2})\b|percentil\s*(\d{2})\b',
        re.IGNORECASE
    )
    PATRON_USUARIOS = re.compile(
        r'(\d+)\s*(?:usuario|user|vu|virtual user)s?\s*concurrente',
        re.IGNORECASE
    )
    PATRON_RAMPUP = re.compile(
        r'ramp.?up[:\s]+(\d+)\s*(?:s|seg|segundo|segundos|min|minuto)',
        re.IGNORECASE
    )
    PATRON_DURACION = re.compile(
        r'duraci[oó]n[:\s]+(\d+)\s*(?:s|seg|segundo|segundos|min|minuto)',
        re.IGNORECASE
    )

    def extraer(self, yaml_path: str) -> list[EspecificacionCarga]:
        """
        Lee un YAML de requisito y extrae todas las especificaciones
        de carga que contiene. Puede producir múltiples especificaciones
        si el requisito tiene varios criterios de rendimiento.
        """
        with open(yaml_path, encoding="utf-8") as f:
            req = yaml.safe_load(f)

        if not req:
            return []

        especificaciones = []

        # Extraer del campo restricciones_no_funcionales.rendimiento
        restriccion_rend = (
            req.get("restricciones_no_funcionales", {})
            .get("rendimiento", "")
        )

        # Extraer de los criterios de aceptación de tipo contorno
        criterios_contorno = [
            ac for ac in req.get("criterios_aceptacion", [])
            if ac.get("tipo") in ("contorno", "rendimiento")
            or self._es_criterio_rendimiento(ac)
        ]

        # Extraer del campo datos_salida
        tiempo_max = req.get("datos_salida", {}).get(
            "tiempo_respuesta_max_ms"
        )

        if criterios_contorno:
            for ac in criterios_contorno:
                spec = self._extraer_de_criterio(
                    ac, req, restriccion_rend, tiempo_max
                )
                if spec:
                    especificaciones.append(spec)
        elif restriccion_rend or tiempo_max:
            # Sin criterios de contorno explícitos, generar spec desde
            # el campo de restricciones
            spec = self._extraer_de_restriccion(
                req, restriccion_rend, tiempo_max
            )
            if spec:
                especificaciones.append(spec)

        return especificaciones

    def _es_criterio_rendimiento(self, ac: dict) -> bool:
        """
        Detecta si un criterio de aceptación es de rendimiento aunque
        no esté etiquetado como 'contorno' o 'rendimiento'.
        """
        texto = " ".join([
            ac.get("dado", ""),
            ac.get("cuando", ""),
            ac.get("entonces", "")
        ]).lower()

        palabras_rendimiento = {
            "segundo", "ms", "milisegundo", "tiempo", "respuesta",
            "concurrente", "usuario", "carga", "rendimiento",
            "latencia", "throughput", "p95", "p99", "percentil"
        }
        return any(p in texto for p in palabras_rendimiento)

    def _extraer_de_criterio(
        self,
        ac: dict,
        req: dict,
        restriccion_global: str,
        tiempo_max_global: Optional[int]
    ) -> Optional[EspecificacionCarga]:
        """
        Extrae una especificación de carga desde un criterio de aceptación.
        """
        entonces = ac.get("entonces", "")
        cuando = ac.get("cuando", "")
        datos = ac.get("datos_ejemplo", {})

        # Parsear tiempo de respuesta del criterio
        tiempo_ms = self._parsear_tiempo_ms(entonces) or tiempo_max_global
        percentil = self._parsear_percentil(entonces) or 95

        # Parsear usuarios concurrentes del criterio o del cuando
        usuarios = (
            self._parsear_usuarios(cuando) or
            self._parsear_usuarios(restriccion_global) or
            50
        )

        if not tiempo_ms:
            return None

        # Inferir endpoint desde datos_entrada y eventos
        endpoint = self._inferir_endpoint(req)
        metodo = self._inferir_metodo(req)

        # Construir dataset desde datos_ejemplo del criterio
        dataset = []
        if datos:
            dataset.append({
                k: str(v) for k, v in datos.items()
                if v is not None
            })

        # Completar con valores desde datos_entrada del requisito
        parametros = self._extraer_parametros_request(req)

        return EspecificacionCarga(
            requisito_id=req.get("id", ""),
            criterio_ac_id=ac.get("id", ""),
            endpoint=endpoint,
            metodo_http=metodo,
            tiempo_respuesta_p50_ms=None,
            tiempo_respuesta_p90_ms=(
                tiempo_ms if percentil == 90 else None
            ),
            tiempo_respuesta_p95_ms=(
                tiempo_ms if percentil == 95 else None
            ),
            tiempo_respuesta_p99_ms=(
                tiempo_ms if percentil == 99 else None
            ),
            tiempo_respuesta_max_ms=tiempo_ms,
            tasa_error_max_pct=1.0,
            usuarios_concurrentes=usuarios,
            ramp_up_segundos=self._calcular_ramp_up(usuarios),
            duracion_prueba_segundos=self._calcular_duracion(restriccion_global),
            parametros_request=parametros,
            cuerpo_request=self._inferir_body(req),
            cabeceras_http={"Content-Type": "application/json"},
            codigo_respuesta_esperado=200,
            validaciones_respuesta=self._extraer_validaciones(entonces),
            dataset_parametrizado=dataset,
            volumen_datos_bd=(
                req.get("restricciones_no_funcionales", {})
                .get("volumen_datos", "")
            ),
            nombre_escenario=(
                f"{req.get('id', 'REQ')}_{ac.get('id', 'AC')}_rendimiento"
            ),
            descripcion=(
                f"Test de rendimiento generado desde {ac.get('id', '')} "
                f"del requisito {req.get('id', '')}. "
                f"Criterio: {entonces[:100]}"
            ),
            tipo_escenario="carga"
        )

    def _extraer_de_restriccion(
        self,
        req: dict,
        restriccion: str,
        tiempo_max: Optional[int]
    ) -> Optional[EspecificacionCarga]:
        """
        Extrae una especificación desde el campo restricciones_no_funcionales
        cuando no hay criterios de aceptación de rendimiento explícitos.
        """
        tiempo_ms = (
            self._parsear_tiempo_ms(restriccion) or tiempo_max
        )
        if not tiempo_ms:
            return None

        usuarios = self._parsear_usuarios(restriccion) or 50
        percentil = self._parsear_percentil(restriccion) or 95

        return EspecificacionCarga(
            requisito_id=req.get("id", ""),
            criterio_ac_id=f"{req.get('id', '')}_NFR_rendimiento",
            endpoint=self._inferir_endpoint(req),
            metodo_http=self._inferir_metodo(req),
            tiempo_respuesta_p50_ms=None,
            tiempo_respuesta_p90_ms=(
                tiempo_ms if percentil == 90 else None
            ),
            tiempo_respuesta_p95_ms=(
                tiempo_ms if percentil == 95 else None
            ),
            tiempo_respuesta_p99_ms=(
                tiempo_ms if percentil == 99 else None
            ),
            tiempo_respuesta_max_ms=tiempo_ms,
            tasa_error_max_pct=1.0,
            usuarios_concurrentes=usuarios,
            ramp_up_segundos=self._calcular_ramp_up(usuarios),
            duracion_prueba_segundos=self._calcular_duracion(restriccion),
            parametros_request=self._extraer_parametros_request(req),
            cuerpo_request=self._inferir_body(req),
            cabeceras_http={"Content-Type": "application/json"},
            codigo_respuesta_esperado=200,
            validaciones_respuesta=[],
            dataset_parametrizado=[],
            volumen_datos_bd=(
                req.get("restricciones_no_funcionales", {})
                .get("volumen_datos", "")
            ),
            nombre_escenario=f"{req.get('id', 'REQ')}_rendimiento_nfr",
            descripcion=(
                f"Test de rendimiento NFR del requisito {req.get('id', '')}. "
                f"Restricción: {restriccion[:100]}"
            ),
            tipo_escenario="baseline"
        )

    def _parsear_tiempo_ms(self, texto: str) -> Optional[int]:
        """Extrae el tiempo de respuesta en ms de un texto."""
        if not texto:
            return None
        match = self.PATRON_TIEMPO.search(texto)
        if not match:
            return None
        valor = float(match.group(1))
        unidad = match.group(2).lower()
        if unidad.startswith("ms") or unidad.startswith("mili"):
            return int(valor)
        # Convertir segundos a ms
        return int(valor * 1000)

    def _parsear_percentil(self, texto: str) -> Optional[int]:
        """Extrae el percentil de un texto."""
        if not texto:
            return None
        match = self.PATRON_PERCENTIL.search(texto)
        if not match:
            return None
        return int(match.group(1) or match.group(2))

    def _parsear_usuarios(self, texto: str) -> Optional[int]:
        """Extrae el número de usuarios concurrentes de un texto."""
        if not texto:
            return None
        match = self.PATRON_USUARIOS.search(texto)
        return int(match.group(1)) if match else None

    def _calcular_ramp_up(self, usuarios: int) -> int:
        """
        Calcula el tiempo de ramp-up recomendado según el número de usuarios.
        Regla general: 1 segundo por cada 10 usuarios, mínimo 30s.
        """
        return max(30, (usuarios // 10) * 10)

    def _calcular_duracion(self, restriccion: str) -> int:
        """Extrae la duración del test o usa un valor por defecto."""
        if not restriccion:
            return 300  # 5 minutos por defecto
        match = self.PATRON_DURACION.search(restriccion)
        if not match:
            return 300
        valor = int(match.group(1))
        # Si la unidad es minutos, convertir
        if "min" in restriccion[match.start():match.end() + 5].lower():
            return valor * 60
        return valor

    def _inferir_endpoint(self, req: dict) -> str:
        """
        Infiere la URL del endpoint desde el evento disparador y el título.
        El analista debe revisar y completar si el endpoint no es deducible.
        """
        titulo = req.get("titulo", "").lower()
        epica = req.get("epica", "").lower()

        # Intentar inferir desde palabras clave en el título
        if "factura" in titulo:
            if "filtrar" in titulo or "listar" in titulo or "buscar" in titulo:
                return "/api/v1/facturas"
            if "aprobar" in titulo:
                return "/api/v1/facturas/{id}/aprobar"
            if "exportar" in titulo:
                return "/api/v1/facturas/exportar"
            return "/api/v1/facturas"

        # Endpoint genérico como fallback
        return f"/api/v1/{epica.replace('ep-', '').replace('-', '/')}/[PENDIENTE]"

    def _inferir_metodo(self, req: dict) -> str:
        """Infiere el método HTTP desde el título y tipo de operación."""
        titulo = req.get("titulo", "").lower()
        palabras_get = {
            "filtrar", "listar", "buscar", "consultar",
            "obtener", "ver", "mostrar", "exportar"
        }
        palabras_post = {
            "crear", "registrar", "añadir", "enviar",
            "generar", "importar"
        }
        palabras_put = {
            "actualizar", "modificar", "editar", "cambiar"
        }
        palabras_delete = {"eliminar", "borrar", "archivar"}

        for palabra in palabras_get:
            if palabra in titulo:
                return "GET"
        for palabra in palabras_post:
            if palabra in titulo:
                return "POST"
        for palabra in palabras_put:
            if palabra in titulo:
                return "PUT"
        for palabra in palabras_delete:
            if palabra in titulo:
                return "DELETE"

        return "GET"

    def _extraer_parametros_request(self, req: dict) -> list[dict]:
        """Extrae los parámetros del request desde datos_entrada."""
        params = []
        for dato in req.get("datos_entrada", []):
            params.append({
                "nombre": dato.get("nombre", ""),
                "tipo": dato.get("tipo", "string"),
                "requerido": dato.get("requerido", True),
                "formato": dato.get("formato", ""),
                "rango_min": dato.get("rango", {}).get("min"),
                "rango_max": dato.get("rango", {}).get("max"),
                "valores_enum": dato.get("valores_enum", []),
                "valor_defecto": dato.get("valor_defecto")
            })
        return params

    def _inferir_body(self, req: dict) -> Optional[dict]:
        """Construye el body del request para métodos POST/PUT."""
        metodo = self._inferir_metodo(req)
        if metodo not in ("POST", "PUT", "PATCH"):
            return None

        body = {}
        for dato in req.get("datos_entrada", []):
            nombre = dato.get("nombre", "")
            tipo = dato.get("tipo", "string")
            if dato.get("valor_defecto") is not None:
                body[nombre] = dato["valor_defecto"]
            elif tipo == "string":
                body[nombre] = f"valor_prueba_{nombre}"
            elif tipo == "integer":
                body[nombre] = dato.get("rango", {}).get("min", 1)
            elif tipo == "date":
                body[nombre] = "2024-01-01"
            elif tipo == "boolean":
                body[nombre] = True
        return body if body else None

    def _extraer_validaciones(self, entonces: str) -> list[str]:
        """
        Extrae validaciones de respuesta del campo 'entonces'
        del criterio de aceptación.
        """
        validaciones = []
        entonces_lower = entonces.lower()

        if "ordenad" in entonces_lower:
            validaciones.append("response_body_contains_ordered_results")
        if "paginad" in entonces_lower or "página" in entonces_lower:
            validaciones.append("response_body_has_pagination")
        if "contador" in entonces_lower or "total" in entonces_lower:
            validaciones.append("response_body_has_total_count")
        if "mensaje" in entonces_lower:
            validaciones.append("response_body_has_message")

        return validaciones
```

---

## Generador de scripts JMeter

JMeter usa un formato XML propietario (`.jmx`) con una estructura jerárquica de elementos. El generador produce un plan de prueba completo con gestión de cookies, cabeceras, dataset parametrizado y assertions de tiempo.

```python
# generador_jmeter.py

import xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass
from pathlib import Path
import json


class GeneradorJMeter:
    """
    Genera planes de prueba JMeter (.jmx) desde especificaciones
    de carga normalizadas.
    Produce planes listos para ejecutarse con:
      jmeter -n -t plan.jmx -l resultados.jtl -e -o report/
    """

    def generar(
        self,
        spec: EspecificacionCarga,
        ruta_salida: str
    ) -> str:
        """
        Genera el archivo .jmx completo y lo guarda en disco.
        Retorna la ruta del archivo generado.
        """
        root = self._crear_test_plan(spec)
        xml_str = self._formatear_xml(root)

        ruta = Path(ruta_salida) / f"{spec.nombre_escenario}.jmx"
        ruta.write_text(xml_str, encoding="utf-8")
        return str(ruta)

    def _crear_test_plan(self, spec: EspecificacionCarga) -> ET.Element:
        """Construye el árbol XML del plan de prueba JMeter."""

        # Raíz: jmeterTestPlan
        root = ET.Element("jmeterTestPlan", {
            "version": "1.2",
            "properties": "5.0",
            "jmeter": "5.6"
        })

        # HashTree raíz
        hash_tree_root = ET.SubElement(root, "hashTree")

        # TestPlan
        test_plan = ET.SubElement(hash_tree_root, "TestPlan", {
            "guiclass":    "TestPlanGui",
            "testclass":   "TestPlan",
            "testname":    spec.nombre_escenario,
            "enabled":     "true"
        })
        self._add_string_prop(test_plan, "TestPlan.comments", spec.descripcion)
        self._add_bool_prop(test_plan, "TestPlan.functional_mode", False)
        self._add_bool_prop(test_plan, "TestPlan.tearDown_on_shutdown", True)
        self._add_bool_prop(test_plan, "TestPlan.serialize_threadgroups", False)
        ET.SubElement(test_plan, "elementProp", {
            "name":       "TestPlan.user_defined_variables",
            "elementType":"Arguments",
            "guiclass":   "ArgumentsPanel",
            "testclass":  "Arguments",
            "testname":   "User Defined Variables"
        })

        hash_tree_plan = ET.SubElement(hash_tree_root, "hashTree")

        # Variables de usuario para parametrización
        self._agregar_variables_usuario(hash_tree_plan, spec)

        # HTTP Request Defaults (configuración base del servidor)
        self._agregar_http_defaults(hash_tree_plan, spec)

        # HTTP Cookie Manager
        self._agregar_cookie_manager(hash_tree_plan)

        # HTTP Header Manager
        self._agregar_header_manager(hash_tree_plan, spec)

        # CSV Dataset si hay datos parametrizados
        if spec.dataset_parametrizado:
            self._agregar_csv_dataset(hash_tree_plan, spec)

        # Thread Group principal (escenario de carga)
        self._agregar_thread_group(hash_tree_plan, spec, "carga")

        # Thread Group de spike si aplica
        if spec.tipo_escenario in ("estres", "spike"):
            self._agregar_thread_group(hash_tree_plan, spec, "spike")

        # Listeners de resultados
        self._agregar_listeners(hash_tree_plan, spec)

        return root

    def _agregar_variables_usuario(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade variables de usuario para parametrizar el plan."""
        args = ET.SubElement(parent, "Arguments", {
            "guiclass":  "ArgumentsPanel",
            "testclass": "Arguments",
            "testname":  "Variables de usuario",
            "enabled":   "true"
        })
        coll = ET.SubElement(args, "collectionProp", {
            "name": "Arguments.arguments"
        })

        variables = {
            "BASE_URL":               self._extraer_base_url(spec.endpoint),
            "ENDPOINT":               self._extraer_path(spec.endpoint),
            "TIEMPO_MAX_MS":          str(spec.tiempo_respuesta_max_ms or 2000),
            "TASA_ERROR_MAX":         str(spec.tasa_error_max_pct),
            "USUARIOS_CONCURRENTES":  str(spec.usuarios_concurrentes),
            "RAMP_UP_SEGUNDOS":       str(spec.ramp_up_segundos),
            "DURACION_SEGUNDOS":      str(spec.duracion_prueba_segundos),
        }

        # Añadir parámetros del request como variables
        for param in spec.parametros_request:
            nombre = param.get("nombre", "")
            valor = str(
                param.get("valor_defecto") or
                self._valor_por_tipo(param)
            )
            variables[f"PARAM_{nombre.upper()}"] = valor

        for nombre, valor in variables.items():
            elem = ET.SubElement(coll, "elementProp", {
                "name":        nombre,
                "elementType": "Argument"
            })
            self._add_string_prop(elem, "Argument.name", nombre)
            self._add_string_prop(elem, "Argument.value", valor)
            self._add_string_prop(elem, "Argument.metadata", "=")

        ET.SubElement(parent, "hashTree")

    def _agregar_http_defaults(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade el elemento HTTP Request Defaults."""
        defaults = ET.SubElement(parent, "ConfigTestElement", {
            "guiclass":  "HttpDefaultsGui",
            "testclass": "ConfigTestElement",
            "testname":  "HTTP Request Defaults",
            "enabled":   "true"
        })
        self._add_string_prop(defaults, "HTTPSampler.domain", "${BASE_URL}")
        self._add_string_prop(defaults, "HTTPSampler.port", "443")
        self._add_string_prop(defaults, "HTTPSampler.protocol", "https")
        self._add_string_prop(defaults, "HTTPSampler.contentEncoding", "UTF-8")
        self._add_string_prop(defaults, "HTTPSampler.connect_timeout", "5000")
        self._add_string_prop(defaults, "HTTPSampler.response_timeout", "30000")
        ET.SubElement(parent, "hashTree")

    def _agregar_cookie_manager(self, parent: ET.Element):
        """Añade el gestor de cookies."""
        cm = ET.SubElement(parent, "CookieManager", {
            "guiclass":  "CookiePanel",
            "testclass": "CookieManager",
            "testname":  "HTTP Cookie Manager",
            "enabled":   "true"
        })
        self._add_bool_prop(cm, "CookieManager.clearEachIteration", True)
        ET.SubElement(parent, "hashTree")

    def _agregar_header_manager(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade el gestor de cabeceras HTTP."""
        hm = ET.SubElement(parent, "HeaderManager", {
            "guiclass":  "HeaderPanel",
            "testclass": "HeaderManager",
            "testname":  "HTTP Header Manager",
            "enabled":   "true"
        })
        coll = ET.SubElement(hm, "collectionProp", {
            "name": "HeaderManager.headers"
        })
        for nombre, valor in spec.cabeceras_http.items():
            elem = ET.SubElement(coll, "elementProp", {
                "name":        nombre,
                "elementType": "Header"
            })
            self._add_string_prop(elem, "Header.name", nombre)
            self._add_string_prop(elem, "Header.value", valor)
        ET.SubElement(parent, "hashTree")

    def _agregar_csv_dataset(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade el CSV Data Set Config para parametrización."""
        csv = ET.SubElement(parent, "CSVDataSet", {
            "guiclass":  "TestBeanGUI",
            "testclass": "CSVDataSet",
            "testname":  f"Dataset - {spec.requisito_id}",
            "enabled":   "true"
        })
        self._add_string_prop(
            csv, "filename",
            f"datasets/{spec.nombre_escenario}_datos.csv"
        )
        self._add_string_prop(
            csv, "variableNames",
            ",".join(spec.dataset_parametrizado[0].keys())
            if spec.dataset_parametrizado else ""
        )
        self._add_string_prop(csv, "delimiter", ",")
        self._add_string_prop(csv, "fileEncoding", "UTF-8")
        self._add_bool_prop(csv, "ignoreFirstLine", True)
        self._add_bool_prop(csv, "recycle", True)
        self._add_bool_prop(csv, "stopThread", False)
        self._add_string_prop(csv, "shareMode", "shareMode.all")
        ET.SubElement(parent, "hashTree")

    def _agregar_thread_group(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga,
        tipo: str
    ):
        """
        Añade un Thread Group con el escenario de carga configurado.
        tipo: 'carga' (normal) o 'spike' (pico de carga)
        """
        if tipo == "spike":
            usuarios = spec.usuarios_concurrentes * 3
            ramp_up = 10
            duracion = 120
            nombre = f"{spec.nombre_escenario}_spike"
        else:
            usuarios = spec.usuarios_concurrentes
            ramp_up = spec.ramp_up_segundos
            duracion = spec.duracion_prueba_segundos
            nombre = spec.nombre_escenario

        tg = ET.SubElement(parent, "ThreadGroup", {
            "guiclass":  "ThreadGroupGui",
            "testclass": "ThreadGroup",
            "testname":  nombre,
            "enabled":   "true"
        })
        self._add_string_prop(
            tg, "ThreadGroup.on_sample_error", "continue"
        )

        # Scheduler
        scheduler = ET.SubElement(tg, "elementProp", {
            "name":        "ThreadGroup.main_controller",
            "elementType": "LoopController",
            "guiclass":    "LoopControlPanel",
            "testclass":   "LoopController",
            "testname":    "Loop Controller"
        })
        self._add_bool_prop(scheduler, "LoopController.continue_forever", True)
        self._add_string_prop(scheduler, "LoopController.loops", "-1")

        self._add_string_prop(tg, "ThreadGroup.num_threads", str(usuarios))
        self._add_string_prop(tg, "ThreadGroup.ramp_time", str(ramp_up))
        self._add_bool_prop(tg, "ThreadGroup.scheduler", True)
        self._add_string_prop(tg, "ThreadGroup.duration", str(duracion))
        self._add_string_prop(tg, "ThreadGroup.delay", "0")

        hash_tree_tg = ET.SubElement(parent, "hashTree")

        # HTTP Request Sampler
        self._agregar_http_sampler(hash_tree_tg, spec)

        # Response Time Assertion
        self._agregar_assertion_tiempo(hash_tree_tg, spec)

        # Response Code Assertion
        self._agregar_assertion_codigo(hash_tree_tg, spec)

        # Assertions de body si hay validaciones
        for validacion in spec.validaciones_respuesta:
            self._agregar_assertion_body(hash_tree_tg, validacion)

    def _agregar_http_sampler(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade el HTTP Request Sampler."""
        sampler = ET.SubElement(parent, "HTTPSamplerProxy", {
            "guiclass":  "HttpTestSampleGui",
            "testclass": "HTTPSamplerProxy",
            "testname":  f"{spec.metodo_http} {spec.endpoint}",
            "enabled":   "true"
        })

        self._add_string_prop(sampler, "HTTPSampler.method", spec.metodo_http)
        self._add_string_prop(
            sampler, "HTTPSampler.path",
            self._construir_path_con_params(spec)
        )
        self._add_bool_prop(sampler, "HTTPSampler.follow_redirects", True)
        self._add_bool_prop(sampler, "HTTPSampler.auto_redirects", False)
        self._add_bool_prop(sampler, "HTTPSampler.use_keepalive", True)
        self._add_bool_prop(sampler, "HTTPSampler.DO_MULTIPART_POST", False)

        # Body para POST/PUT
        if spec.cuerpo_request:
            self._add_bool_prop(sampler, "HTTPSampler.postBodyRaw", True)
            args_prop = ET.SubElement(sampler, "elementProp", {
                "name":        "HTTPsampler.Arguments",
                "elementType": "Arguments"
            })
            coll = ET.SubElement(args_prop, "collectionProp", {
                "name": "Arguments.arguments"
            })
            elem = ET.SubElement(coll, "elementProp", {
                "name":        "",
                "elementType": "HTTPArgument"
            })
            self._add_bool_prop(elem, "HTTPArgument.always_encode", False)
            self._add_string_prop(
                elem, "Argument.value",
                json.dumps(spec.cuerpo_request, ensure_ascii=False)
            )
            self._add_string_prop(elem, "Argument.metadata", "=")
        else:
            ET.SubElement(sampler, "elementProp", {
                "name":        "HTTPsampler.Arguments",
                "elementType": "Arguments",
                "guiclass":    "HTTPArgumentsPanel",
                "testclass":   "Arguments",
                "testname":    "User Defined Variables"
            })

        ET.SubElement(parent, "hashTree")

    def _agregar_assertion_tiempo(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade la assertion de tiempo de respuesta máximo."""
        assertion = ET.SubElement(parent, "DurationAssertion", {
            "guiclass":  "DurationAssertionGui",
            "testclass": "DurationAssertion",
            "testname":  (
                f"Tiempo respuesta ≤ {spec.tiempo_respuesta_max_ms}ms"
            ),
            "enabled":   "true"
        })
        self._add_string_prop(
            assertion, "DurationAssertion.duration",
            str(spec.tiempo_respuesta_max_ms or 2000)
        )
        ET.SubElement(parent, "hashTree")

    def _agregar_assertion_codigo(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade la assertion de código de respuesta HTTP."""
        assertion = ET.SubElement(parent, "ResponseAssertion", {
            "guiclass":  "AssertionGui",
            "testclass": "ResponseAssertion",
            "testname":  f"Código HTTP = {spec.codigo_respuesta_esperado}",
            "enabled":   "true"
        })
        coll = ET.SubElement(assertion, "collectionProp", {
            "name": "Asserion.test_strings"
        })
        elem = ET.SubElement(coll, "stringProp", {
            "name": "49586"
        })
        elem.text = str(spec.codigo_respuesta_esperado)
        self._add_string_prop(assertion, "Assertion.test_field", "Assertion.response_code")
        self._add_bool_prop(assertion, "Assertion.assume_success", False)
        self._add_int_prop(assertion, "Assertion.test_type", 8)
        ET.SubElement(parent, "hashTree")

    def _agregar_assertion_body(
        self,
        parent: ET.Element,
        validacion: str
    ):
        """Añade assertion de contenido del body."""
        assertion = ET.SubElement(parent, "ResponseAssertion", {
            "guiclass":  "AssertionGui",
            "testclass": "ResponseAssertion",
            "testname":  f"Validación: {validacion}",
            "enabled":   "true"
        })
        # Usar el nombre de la validación como patrón básico
        # El analista puede refinarlo después de revisar el script
        patrones = {
            "response_body_has_pagination": '"total"',
            "response_body_has_total_count": '"total"',
            "response_body_has_message":     '"message"',
        }
        patron = patrones.get(validacion, validacion)
        coll = ET.SubElement(assertion, "collectionProp", {
            "name": "Asserion.test_strings"
        })
        elem = ET.SubElement(coll, "stringProp", {"name": "49586"})
        elem.text = patron
        self._add_string_prop(
            assertion, "Assertion.test_field", "Assertion.response_data"
        )
        self._add_bool_prop(assertion, "Assertion.assume_success", False)
        self._add_int_prop(assertion, "Assertion.test_type", 2)
        ET.SubElement(parent, "hashTree")

    def _agregar_listeners(
        self,
        parent: ET.Element,
        spec: EspecificacionCarga
    ):
        """Añade listeners de resultados: Summary Report y Backend Listener."""
        # Summary Report (para ejecución local)
        sr = ET.SubElement(parent, "ResultCollector", {
            "guiclass":  "SummaryReport",
            "testclass": "ResultCollector",
            "testname":  "Summary Report",
            "enabled":   "true"
        })
        self._add_bool_prop(sr, "ResultCollector.error_logging", False)
        objprop = ET.SubElement(sr, "objProp")
        name_elem = ET.SubElement(objprop, "name")
        name_elem.text = "saveConfig"
        value_elem = ET.SubElement(objprop, "value", {
            "class": "SampleSaveConfiguration"
        })
        self._add_bool_prop(value_elem, "time", True)
        self._add_bool_prop(value_elem, "latency", True)
        self._add_bool_prop(value_elem, "timestamp", True)
        self._add_bool_prop(value_elem, "success", True)
        self._add_bool_prop(value_elem, "responseCode", True)
        self._add_string_prop(
            sr, "filename",
            f"resultados/{spec.nombre_escenario}.jtl"
        )
        ET.SubElement(parent, "hashTree")

        # Backend Listener para integración con Grafana/InfluxDB (opcional)
        bl = ET.SubElement(parent, "BackendListener", {
            "guiclass":  "BackendListenerGui",
            "testclass": "BackendListener",
            "testname":  "Backend Listener (Grafana/InfluxDB)",
            "enabled":   "false"  # Desactivado por defecto
        })
        self._add_string_prop(
            bl, "classname",
            "org.apache.jmeter.visualizers.backend.influxdb.InfluxdbBackendListenerClient"
        )
        ET.SubElement(parent, "hashTree")

    # ── Helpers de generación XML ──────────────────────────────────

    def _add_string_prop(
        self,
        parent: ET.Element,
        name: str,
        value: str
    ):
        elem = ET.SubElement(parent, "stringProp", {"name": name})
        elem.text = value

    def _add_bool_prop(
        self,
        parent: ET.Element,
        name: str,
        value: bool
    ):
        elem = ET.SubElement(parent, "boolProp", {"name": name})
        elem.text = str(value).lower()

    def _add_int_prop(
        self,
        parent: ET.Element,
        name: str,
        value: int
    ):
        elem = ET.SubElement(parent, "intProp", {"name": name})
        elem.text = str(value)

    def _extraer_base_url(self, endpoint: str) -> str:
        """Extrae la base URL del endpoint."""
        import os
        return os.environ.get("PERF_BASE_URL", "staging.tu-empresa.com")

    def _extraer_path(self, endpoint: str) -> str:
        """Extrae solo el path del endpoint."""
        if endpoint.startswith("http"):
            from urllib.parse import urlparse
            return urlparse(endpoint).path
        return endpoint

    def _construir_path_con_params(self, spec: EspecificacionCarga) -> str:
        """Construye el path con parámetros de query string si es GET."""
        path = self._extraer_path(spec.endpoint)
        if spec.metodo_http != "GET":
            return path
        params = [
            p for p in spec.parametros_request if p.get("requerido", True)
        ]
        if not params:
            return path
        query = "&".join(
            f"{p['nombre']}=${{{p['nombre'].upper()}}}"
            for p in params
        )
        return f"{path}?{query}"

    def _valor_por_tipo(self, param: dict) -> str:
        """Genera un valor de prueba según el tipo del parámetro."""
        tipo = param.get("tipo", "string")
        valores = {
            "string":   "valor_prueba",
            "integer":  str(param.get("rango_min") or 1),
            "decimal":  "1.0",
            "date":     "2024-01-01",
            "datetime": "2024-01-01T00:00:00Z",
            "boolean":  "true"
        }
        if param.get("valores_enum"):
            return str(param["valores_enum"][0])
        return valores.get(tipo, "valor_prueba")

    def _formatear_xml(self, root: ET.Element) -> str:
        """Formatea el XML con indentación legible."""
        xml_str = ET.tostring(root, encoding="unicode", xml_declaration=False)
        dom = minidom.parseString(xml_str)
        pretty = dom.toprettyxml(indent="  ", encoding=None)
        # Añadir declaración XML con codificación
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(
            pretty.split("\n")[1:]
        )

    def generar_csv_dataset(
        self,
        spec: EspecificacionCarga,
        ruta_salida: str
    ) -> Optional[str]:
        """Genera el archivo CSV con los datos de prueba parametrizados."""
        if not spec.dataset_parametrizado:
            return None

        import csv
        ruta = Path(ruta_salida) / "datasets" / f"{spec.nombre_escenario}_datos.csv"
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=spec.dataset_parametrizado[0].keys()
            )
            writer.writeheader()
            writer.writerows(spec.dataset_parametrizado)

        return str(ruta)
```

---

## Generador de scripts k6

k6 es la alternativa moderna a JMeter: scripts en JavaScript, más ligeros y mejor integrados con CI/CD. El generador produce un script con thresholds declarativos, gestión de VUs y scenarios para múltiples perfiles de carga.

```python
# generador_k6.py

from pathlib import Path
import json


class GeneradorK6:
    """
    Genera scripts k6 (.js) desde especificaciones de carga normalizadas.
    Produce scripts listos para ejecutarse con:
      k6 run script.js
      k6 run --out influxdb=http://localhost:8086/k6 script.js
    """

    def generar(
        self,
        spec: EspecificacionCarga,
        ruta_salida: str
    ) -> str:
        """
        Genera el archivo .js de k6 y lo guarda en disco.
        Retorna la ruta del archivo generado.
        """
        script = self._construir_script(spec)
        ruta = Path(ruta_salida) / f"{spec.nombre_escenario}.js"
        ruta.write_text(script, encoding="utf-8")
        return str(ruta)

    def _construir_script(self, spec: EspecificacionCarga) -> str:
        """Construye el script k6 completo como string."""

        # Construir los thresholds
        thresholds = self._construir_thresholds(spec)

        # Construir los scenarios
        scenarios = self._construir_scenarios(spec)

        # Construir la función de setup (autenticación si aplica)
        setup_fn = self._construir_setup(spec)

        # Construir la función principal de petición
        request_fn = self._construir_request(spec)

        # Construir el dataset de prueba inline
        dataset = self._construir_dataset(spec)

        script = f"""/**
 * Script de test de rendimiento k6
 * Generado automáticamente por el pipeline de análisis funcional
 *
 * Requisito origen: {spec.requisito_id}
 * Criterio AC:      {spec.criterio_ac_id}
 * Descripción:      {spec.descripcion}
 *
 * Ejecución:
 *   k6 run {spec.nombre_escenario}.js
 *   k6 run --env BASE_URL=https://staging.tu-empresa.com {spec.nombre_escenario}.js
 *
 * Variables de entorno soportadas:
 *   BASE_URL    URL base del entorno a probar (default: staging)
 *   TOKEN       Token de autenticación Bearer (si aplica)
 *   VUS         Número de usuarios virtuales (sobreescribe el configurado)
 */

import http from 'k6/http';
import {{ check, sleep, group }} from 'k6';
import {{ Rate, Trend, Counter }} from 'k6/metrics';
import {{ SharedArray }} from 'k6/data';
import encoding from 'k6/encoding';

// ── Métricas personalizadas ─────────────────────────────────────────────────

const errorRate = new Rate('errores_tasa');
const tiempoRespuesta = new Trend('tiempo_respuesta_ms', true);
const peticionesExitosas = new Counter('peticiones_exitosas');

// ── Configuración ───────────────────────────────────────────────────────────

const BASE_URL = __ENV.BASE_URL || 'https://staging.tu-empresa.com';
const TOKEN    = __ENV.TOKEN    || '';

// Datos de prueba parametrizados
{dataset}

// ── Opciones del test ────────────────────────────────────────────────────────

export const options = {{
  // Thresholds: el test falla si se incumple alguno
  thresholds: {json.dumps(thresholds, indent=4, ensure_ascii=False)},

  // Scenarios: perfiles de carga
  scenarios: {json.dumps(scenarios, indent=4, ensure_ascii=False)},

  // Límite de ancho de banda para simular condiciones reales
  // Descomenta si necesitas limitar la red:
  // bandwidth: {{ rate: 1000000 }},
}};

// ── Setup: preparación del entorno ──────────────────────────────────────────

{setup_fn}

// ── Función principal ────────────────────────────────────────────────────────

{request_fn}

// ── Teardown: limpieza ───────────────────────────────────────────────────────

export function teardown(data) {{
  // Añadir lógica de limpieza si es necesario
  // Por ejemplo: eliminar datos de prueba creados en setup
}}
"""
        return script

    def _construir_thresholds(self, spec: EspecificacionCarga) -> dict:
        """Construye el objeto de thresholds de k6."""
        thresholds = {}

        # Threshold de tiempo de respuesta por percentil
        if spec.tiempo_respuesta_p95_ms:
            thresholds["http_req_duration"] = [
                f"p(95)<{spec.tiempo_respuesta_p95_ms}",
                f"p(99)<{int(spec.tiempo_respuesta_p95_ms * 1.5)}"
            ]
        elif spec.tiempo_respuesta_max_ms:
            thresholds["http_req_duration"] = [
                f"p(95)<{spec.tiempo_respuesta_max_ms}"
            ]

        if spec.tiempo_respuesta_p90_ms:
            thresholds["http_req_duration"] = thresholds.get(
                "http_req_duration", []
            ) + [f"p(90)<{spec.tiempo_respuesta_p90_ms}"]

        # Threshold de tasa de error
        thresholds["http_req_failed"] = [
            f"rate<{spec.tasa_error_max_pct / 100:.3f}"
        ]

        # Métricas personalizadas
        if spec.tiempo_respuesta_p95_ms:
            thresholds["tiempo_respuesta_ms"] = [
                f"p(95)<{spec.tiempo_respuesta_p95_ms}"
            ]
        thresholds["errores_tasa"] = [
            f"rate<{spec.tasa_error_max_pct / 100:.3f}"
        ]

        return thresholds

    def _construir_scenarios(self, spec: EspecificacionCarga) -> dict:
        """Construye los scenarios de k6 según el tipo de prueba."""
        scenarios = {}

        # Scenario de carga ramped (siempre presente)
        scenarios["carga_ramped"] = {
            "executor": "ramping-vus",
            "startVUs": 0,
            "stages": [
                {
                    "duration": f"{spec.ramp_up_segundos}s",
                    "target": spec.usuarios_concurrentes
                },
                {
                    "duration": f"{max(60, spec.duracion_prueba_segundos - spec.ramp_up_segundos * 2)}s",
                    "target": spec.usuarios_concurrentes
                },
                {
                    "duration": f"{spec.ramp_up_segundos}s",
                    "target": 0
                }
            ],
            "gracefulRampDown": "30s"
        }

        # Scenario de spike si es prueba de estrés
        if spec.tipo_escenario in ("estres", "spike"):
            scenarios["spike"] = {
                "executor": "ramping-vus",
                "startVUs": 0,
                "startTime": f"{spec.duracion_prueba_segundos + 60}s",
                "stages": [
                    {"duration": "10s", "target": spec.usuarios_concurrentes * 3},
                    {"duration": "60s", "target": spec.usuarios_concurrentes * 3},
                    {"duration": "10s", "target": 0}
                ]
            }

        # Scenario de soak (larga duración) para pruebas de estabilidad
        if spec.tipo_escenario == "soak":
            scenarios["soak"] = {
                "executor": "constant-vus",
                "vus": max(1, spec.usuarios_concurrentes // 2),
                "duration": "3600s",  # 1 hora
                "startTime": f"{spec.duracion_prueba_segundos + 120}s"
            }

        return scenarios

    def _construir_setup(self, spec: EspecificacionCarga) -> str:
        """Construye la función de setup para autenticación."""
        return """export function setup() {
  // Autenticación: descomentar y adaptar según el mecanismo del proyecto
  //
  // Opción 1: Bearer Token desde variable de entorno
  // return { token: TOKEN };
  //
  // Opción 2: Login con credenciales (obtener token dinámicamente)
  // const loginRes = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
  //   username: __ENV.TEST_USER || 'usuario_prueba@empresa.com',
  //   password: __ENV.TEST_PASS || 'password_prueba'
  // }), { headers: { 'Content-Type': 'application/json' } });
  //
  // check(loginRes, { 'login exitoso': (r) => r.status === 200 });
  // const token = loginRes.json('token');
  // return { token };
  //
  return {};
}"""

    def _construir_request(self, spec: EspecificacionCarga) -> str:
        """Construye la función default con la lógica del test."""

        # Construir cabeceras
        cabeceras_str = json.dumps({
            **spec.cabeceras_http,
            "Authorization": "Bearer ${TOKEN}"
        }, indent=6, ensure_ascii=False)

        # Construir la URL con parámetros
        if spec.metodo_http == "GET" and spec.parametros_request:
            params_requeridos = [
                p for p in spec.parametros_request
                if p.get("requerido", True)
            ]
            query_parts = []
            for p in params_requeridos:
                nombre = p.get("nombre", "")
                query_parts.append(f"{nombre}=${{params.{nombre}}}")
            query_str = "&".join(query_parts)
            url_expr = (
                f"`${{BASE_URL}}{spec.endpoint}?{query_str}`"
                if query_str else
                f"`${{BASE_URL}}{spec.endpoint}`"
            )
        else:
            url_expr = f"`${{BASE_URL}}{spec.endpoint}`"

        # Construir el body para POST/PUT
        if spec.cuerpo_request:
            body_str = json.dumps(spec.cuerpo_request, indent=6, ensure_ascii=False)
            body_expr = f"JSON.stringify({body_str})"
        else:
            body_expr = "null"

        # Construir los checks
        checks = self._construir_checks(spec)
        checks_str = json.dumps(checks, indent=8, ensure_ascii=False)

        # Selección de datos del dataset
        dataset_select = ""
        if spec.dataset_parametrizado:
            dataset_select = (
                "  // Seleccionar una fila del dataset parametrizado\n"
                "  const params = datos[Math.floor(Math.random() * datos.length)];"
            )

        return f"""export default function (data) {{
  // Recuperar token de autenticación del setup
  const token = data.token || TOKEN;

{dataset_select}

  // Configuración de la petición
  const cabeceras = {{
    'Content-Type': 'application/json',
    ...(token ? {{ 'Authorization': `Bearer ${{token}}` }} : {{}})
  }};

  group('{spec.nombre_escenario}', function () {{
    const inicio = Date.now();

    // Ejecutar la petición HTTP
    const respuesta = http.{spec.metodo_http.lower()}(
      {url_expr},
      {body_expr},
      {{ headers: cabeceras, tags: {{ requisito: '{spec.requisito_id}', ac: '{spec.criterio_ac_id}' }} }}
    );

    const duracion = Date.now() - inicio;

    // Registrar métricas personalizadas
    tiempoRespuesta.add(duracion);
    errorRate.add(respuesta.status >= 400);

    // Verificar criterios de aceptación de rendimiento
    const ok = check(respuesta, {checks_str});

    if (ok) {{
      peticionesExitosas.add(1);
    }}

    // Pausa entre iteraciones (think time)
    // Ajustar según el comportamiento real del usuario
    sleep(1);
  }});
}}"""

    def _construir_checks(self, spec: EspecificacionCarga) -> dict:
        """Construye el objeto de checks de k6."""
        checks = {
            f"HTTP {spec.codigo_respuesta_esperado}": (
                f"(r) => r.status === {spec.codigo_respuesta_esperado}"
            ),
            f"tiempo < {spec.tiempo_respuesta_max_ms or 2000}ms": (
                f"(r) => r.timings.duration < {spec.tiempo_respuesta_max_ms or 2000}"
            )
        }

        # Checks adicionales desde validaciones del criterio
        for validacion in spec.validaciones_respuesta:
            if "total" in validacion:
                checks["respuesta contiene total"] = (
                    "(r) => JSON.parse(r.body).total !== undefined"
                )
            if "pagination" in validacion:
                checks["respuesta paginada"] = (
                    "(r) => JSON.parse(r.body).page !== undefined"
                )
            if "message" in validacion:
                checks["respuesta tiene mensaje"] = (
                    "(r) => JSON.parse(r.body).message !== undefined"
                )

        return checks

    def _construir_dataset(self, spec: EspecificacionCarga) -> str:
        """Construye el dataset inline en el script."""
        if not spec.dataset_parametrizado:
            # Generar datos de prueba mínimos desde parámetros
            datos_minimos = {}
            for p in spec.parametros_request:
                nombre = p.get("nombre", "")
                if p.get("valores_enum"):
                    datos_minimos[nombre] = p["valores_enum"][0]
                elif p.get("valor_defecto") is not None:
                    datos_minimos[nombre] = p["valor_defecto"]

            if datos_minimos:
                return (
                    f"const datos = new SharedArray('datos', function() {{\n"
                    f"  return [{json.dumps(datos_minimos, ensure_ascii=False)}];\n"
                    f"}});"
                )
            return "const datos = [];"

        datos_json = json.dumps(
            spec.dataset_parametrizado, indent=2, ensure_ascii=False
        )
        return (
            f"const datos = new SharedArray('datos', function() {{\n"
            f"  return {datos_json};\n"
            f"}});"
        )
```

---

## Orquestador del generador

El orquestador une los componentes y produce todos los artefactos en una única llamada, registrando la trazabilidad con los criterios de aceptación origen.

```python
# orquestador_rendimiento.py

from pathlib import Path
import logging

log = logging.getLogger("pipeline.rendimiento")


class OrquestadorTestingRendimiento:
    """
    Orquesta la generación completa de scripts de rendimiento
    para un requisito dado.
    """

    def __init__(
        self,
        motor_trazabilidad,
        openai_client=None
    ):
        self.trazabilidad = motor_trazabilidad
        self.extractor = ExtractorCriteriosRendimiento()
        self.generador_jmeter = GeneradorJMeter()
        self.generador_k6 = GeneradorK6()

    def generar_para_requisito(
        self,
        yaml_path: str,
        ruta_salida: str,
        herramientas: list[str] = None
    ) -> dict:
        """
        Genera los scripts de rendimiento para un requisito.
        herramientas: ['jmeter', 'k6'] o None (ambas)
        """
        herramientas = herramientas or ["jmeter", "k6"]
        Path(ruta_salida).mkdir(parents=True, exist_ok=True)

        log.info(f"Generando scripts de rendimiento para {yaml_path}")

        # Extraer especificaciones de carga
        especificaciones = self.extractor.extraer(yaml_path)

        if not especificaciones:
            return {
                "exito": False,
                "motivo": (
                    "No se encontraron criterios de rendimiento en el requisito. "
                    "Añadir el campo restricciones_no_funcionales.rendimiento "
                    "o criterios de aceptación de tipo 'contorno' con umbrales de tiempo."
                ),
                "scripts_generados": []
            }

        scripts_generados = []

        for spec in especificaciones:
            scripts_req = {"criterio_ac_id": spec.criterio_ac_id, "scripts": []}

            # Generar JMeter
            if "jmeter" in herramientas:
                ruta_jmx = self.generador_jmeter.generar(spec, ruta_salida)
                ruta_csv = self.generador_jmeter.generar_csv_dataset(
                    spec, ruta_salida
                )
                scripts_req["scripts"].append({
                    "herramienta": "jmeter",
                    "ruta": ruta_jmx,
                    "csv_dataset": ruta_csv
                })
                log.info(f"  ✓ JMeter: {ruta_jmx}")

            # Generar k6
            if "k6" in herramientas:
                ruta_k6 = self.generador_k6.generar(spec, ruta_salida)
                scripts_req["scripts"].append({
                    "herramienta": "k6",
                    "ruta": ruta_k6
                })
                log.info(f"  ✓ k6: {ruta_k6}")

            # Registrar en el grafo de trazabilidad
            for script_info in scripts_req["scripts"]:
                script_id = (
                    f"PERF_SCRIPT::{spec.criterio_ac_id}::"
                    f"{script_info['herramienta']}"
                )
                self.trazabilidad.registrar_nodo(Nodo(
                    id=script_id,
                    tipo="script_rendimiento",
                    titulo=spec.nombre_escenario,
                    estado="generado",
                    metadatos={
                        "herramienta": script_info["herramienta"],
                        "ruta": script_info["ruta"],
                        "requisito_id": spec.requisito_id,
                        "criterio_ac_id": spec.criterio_ac_id,
                        "umbral_p95_ms": spec.tiempo_respuesta_p95_ms,
                        "usuarios": spec.usuarios_concurrentes
                    }
                ))
                self.trazabilidad.registrar_arista(Arista(
                    origen_id=script_id,
                    destino_id=spec.criterio_ac_id,
                    tipo_relacion="verifica",
                    confianza=1.0,
                    origen_relacion="pipeline_rendimiento"
                ))

            scripts_generados.append(scripts_req)

        return {
            "exito": True,
            "requisito_id": especificaciones[0].requisito_id,
            "especificaciones_detectadas": len(especificaciones),
            "scripts_generados": scripts_generados
        }
```

---

## Integración en CI/CD

Los scripts generados se ejecutan automáticamente en el pipeline de CI/CD al mergearse un PR relacionado con el requisito.

### GitHub Actions

```yaml
# .github/workflows/performance-tests.yml

name: Tests de rendimiento

on:
  pull_request:
    types: [closed]
  workflow_dispatch:
    inputs:
      requisito_id:
        description: "ID del requisito a probar (ej: REQ-023)"
        required: true

jobs:
  performance-k6:
    if: |
      github.event.pull_request.merged == true ||
      github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Instalar k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg \
            --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] \
            https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update && sudo apt-get install k6

      - name: Identificar scripts de rendimiento del PR
        id: identificar
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          DB_HOST: ${{ secrets.DB_HOST }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          python orchestrator.py \
            --listar-scripts-rendimiento \
            --pr-id ${{ github.event.pull_request.number }} \
            --output scripts_a_ejecutar.json

      - name: Ejecutar tests k6
        env:
          BASE_URL: ${{ vars.STAGING_URL }}
          TOKEN:    ${{ secrets.STAGING_TOKEN }}
        run: |
          if [ -f scripts_a_ejecutar.json ]; then
            python -c "
          import json, subprocess, sys
          with open('scripts_a_ejecutar.json') as f:
              scripts = json.load(f)
          fallos = 0
          for script in scripts.get('k6', []):
              result = subprocess.run(
                  ['k6', 'run', '--out', 'json=results.json', script],
                  capture_output=True, text=True
              )
              print(result.stdout)
              if result.returncode != 0:
                  print(f'FALLO: {script}', file=sys.stderr)
                  fallos += 1
          sys.exit(1 if fallos > 0 else 0)
          "
          fi

      - name: Publicar resumen en el PR
        if: always() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            if (fs.existsSync('results.json')) {
              const body = `## 📊 Resultados de tests de rendimiento\n\n` +
                `Ver resultados detallados en los artefactos del workflow.`;
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body
              });
            }

      - name: Subir resultados
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: resultados-rendimiento
          path: results.json
          retention-days: 30
```

---

## Salida del generador en consola

```
══════════════════════════════════════════════════════════
  GENERADOR DE TESTS DE RENDIMIENTO
  Requisito: REQ-023 — Filtrar facturas por rango de fechas
══════════════════════════════════════════════════════════

  [1] Extrayendo criterios de rendimiento...
      ✓ 2 especificaciones detectadas

  ESPECIFICACIÓN 1: AC-023-01 (tipo: carga)
    Endpoint:          GET /api/v1/facturas
    Tiempo máx (p95):  2.000ms
    Usuarios:          100 usuarios concurrentes
    Ramp-up:           60s → duración: 300s → ramp-down: 60s
    Parámetros:        fecha_inicio, fecha_fin
    Dataset:           1 fila de datos de ejemplo

  ESPECIFICACIÓN 2: AC-023-02 (tipo: baseline)
    Endpoint:          GET /api/v1/facturas
    Tiempo máx (p95):  2.000ms
    Usuarios:          50 usuarios concurrentes (NFR global)
    Parámetros:        fecha_inicio, fecha_fin (rango > 365 días)

  [2] Generando scripts JMeter...
      ✓ REQ-023_AC-023-01_rendimiento.jmx
      ✓ REQ-023_AC-023-01_rendimiento_datos.csv
      ✓ REQ-023_AC-023-02_rendimiento_nfr.jmx

  [3] Generando scripts k6...
      ✓ REQ-023_AC-023-01_rendimiento.js
      ✓ REQ-023_AC-023-02_rendimiento_nfr.js

  [4] Registrando trazabilidad...
      ✓ 4 nodos registrados en el grafo
      ✓ 4 aristas (verifica → criterio AC)

  Scripts guardados en: ./tests/rendimiento/REQ-023/

══════════════════════════════════════════════════════════
  EJECUCIÓN RÁPIDA:
  k6 run tests/rendimiento/REQ-023/REQ-023_AC-023-01_rendimiento.js \
    --env BASE_URL=https://staging.empresa.com \
    --env TOKEN=<tu_token>

  jmeter -n \
    -t tests/rendimiento/REQ-023/REQ-023_AC-023-01_rendimiento.jmx \
    -l resultados/REQ-023.jtl -e -o report/
══════════════════════════════════════════════════════════
```

---

## Limitaciones y gestión de expectativas

**Los endpoints necesitan revisión manual en casi todos los casos.** La inferencia del endpoint desde el título del requisito funciona para casos frecuentes como filtrado o creación, pero falla en funcionalidades con nomenclatura no estándar o en APIs con versiones y rutas complejas. Cada script generado incluye el comentario `[PENDIENTE]` en el endpoint cuando la inferencia no es fiable, y el analista o el QA deben completarlo antes de la primera ejecución.

**El dataset parametrizado requiere datos reales del entorno de staging.** Los scripts generan un dataset mínimo desde los datos de ejemplo del criterio de aceptación, pero para una prueba de rendimiento significativa se necesita un volumen de datos representativo en la base de datos del entorno de prueba. El campo `volumen_datos_bd` del YAML del requisito es la referencia para que el equipo de QA prepare el entorno antes de ejecutar el test.

**Los umbrales de tiempo son el resultado del test, no la garantía.** Un threshold de 2.000ms en el script no significa que el sistema vaya a responder en menos de 2 segundos. Significa que el test fallará si no lo hace. Si el entorno de staging no está dimensionado de forma equivalente a producción, los resultados del test no son extrapolables. El pipeline asume que el equipo de infraestructura mantiene la equivalencia entre entornos.

**La autenticación requiere configuración manual.** El script generado incluye la infraestructura de autenticación comentada con las tres variantes más frecuentes (token estático, login dinámico, API key), pero el analista o el QA debe descomentar y adaptar la sección correspondiente al mecanismo de autenticación real del proyecto. Un script que no se autentica correctamente producirá fallos por 401 que enmascararán los problemas reales de rendimiento.

**JMeter y k6 miden cosas ligeramente diferentes.** JMeter incluye el tiempo de establecimiento de conexión TCP y TLS en el tiempo de respuesta por defecto. k6 separa el tiempo de conexión (`connecting`) del tiempo de espera de respuesta (`waiting`). Los umbrales del criterio de aceptación del requisito aplican al tiempo total de respuesta tal como lo experimenta el usuario, que corresponde a `http_req_duration` en k6 y a la métrica de tiempo del sampler en JMeter. Ambos scripts usan ese tiempo como referencia para los thresholds, lo que garantiza consistencia en la interpretación de los resultados.
