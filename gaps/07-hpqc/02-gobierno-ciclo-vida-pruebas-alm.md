# Gobierno del ciclo de vida de pruebas en ALM

## Qué es el gobierno del ciclo de vida de pruebas y por qué es diferente del gobierno del pipeline

El Punto A describe cómo el pipeline empuja test cases a ALM. El Punto B describe qué ocurre después: cómo se organizan esos test cases a lo largo del tiempo, quién puede modificarlos y bajo qué condiciones, cómo se planifican y ejecutan los ciclos de pruebas, cómo se sincronizan los resultados con el resto del modelo, y cómo se decide cuándo un conjunto de test cases está suficientemente cubierto para autorizar una entrega.

La diferencia conceptual clave es esta: el Punto A es trabajo de implantación, que se ejecuta una vez y se mantiene con esfuerzo mínimo. El Punto B es trabajo continuo, que ocurre en cada sprint, en cada release y cada vez que un requisito cambia. Sin el Punto B, los test cases generados por el pipeline se convierten en un repositorio estático que nadie mantiene y que pierde valor rápidamente.

El gobierno del ciclo de vida en ALM tiene cinco dimensiones que este punto desarrolla en orden:

```
┌─────────────────────────────────────────────────────────────────┐
│  DIMENSIÓN 1 — Organización y mantenimiento del repositorio     │
│  Quién puede tocar qué y bajo qué proceso                       │
├─────────────────────────────────────────────────────────────────┤
│  DIMENSIÓN 2 — Planificación de ciclos de pruebas               │
│  Test Sets, Test Plans y su relación con sprints y releases     │
├─────────────────────────────────────────────────────────────────┤
│  DIMENSIÓN 3 — Ejecución y seguimiento                          │
│  Cómo se ejecutan, qué se registra y cómo se escalan defectos   │
├─────────────────────────────────────────────────────────────────┤
│  DIMENSIÓN 4 — Sincronización con el resto del modelo           │
│  Resultados ALM → grafo de trazabilidad → matriz de cobertura   │
├─────────────────────────────────────────────────────────────────┤
│  DIMENSIÓN 5 — Criterios de salida (exit criteria)              │
│  Cuándo se autoriza una release desde la perspectiva de QA      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dimensión 1 — Organización y mantenimiento del repositorio de test cases en ALM

### El problema de la propiedad dual

Los test cases generados por el pipeline tienen dos propietarios con intereses distintos. El analista funcional es el autor conceptual: es quien valida que el test case verifica correctamente el criterio de aceptación del requisito. El QA engineer es el ejecutor operativo: es quien lo ejecuta, lo mantiene actualizado cuando cambia el entorno y lo automatiza cuando el equipo lo decide.

Esta dualidad de propiedad es la fuente del error más frecuente en proyectos que implantan generación automática de test cases: el analista genera los test cases, los empuja a ALM y considera que su trabajo ha terminado. El QA engineer los recibe, detecta que algunos no son ejecutables tal cual están (les faltan datos de prueba concretos del entorno, referencias a usuarios de prueba reales, URLs de entorno específico) y los corrige sin comunicárselo al analista. Cuando el pipeline regenera los test cases por un cambio en el requisito, sobrescribe las correcciones del QA sin que nadie lo sepa.

El modelo de gobierno resuelve esto con una regla simple y un proceso de tres pasos.

**La regla:** los test cases en ALM tienen dos zonas de contenido con propietarios distintos. La zona funcional (título, tipo, criterio AC origen, pasos lógicos derivados de los criterios de aceptación) es propiedad del pipeline y del analista. La zona operativa (datos de prueba específicos del entorno, usuarios de prueba reales, scripts de automatización, notas de ejecución) es propiedad del QA engineer.

**El proceso de tres pasos para modificaciones:**

```
Paso 1 — Detección del cambio necesario
  El QA engineer detecta que un test case necesita modificación.
  Abre una incidencia en Jira de tipo "QA Feedback" con:
    - ID del TC en ALM
    - ID del requisito origen (user-07)
    - Descripción del cambio necesario
    - Clasificación: ¿es un error en el criterio AC (zona funcional)
      o una adaptación al entorno (zona operativa)?

Paso 2 — Decisión según la zona afectada
  Si zona operativa → el QA engineer modifica directamente en ALM
    sin necesidad de aprobación. Documenta el cambio en el campo
    "Notas de QA" del test case.
  Si zona funcional → el analista revisa el criterio AC en el YAML
    del requisito, lo corrige si procede y re-ejecuta el pipeline
    para regenerar el test case. El QA engineer no modifica la
    zona funcional directamente en ALM.

Paso 3 — Actualización de la trazabilidad
  En ambos casos, el responsable del cambio actualiza el campo
  "Fecha última revisión" del test case en ALM.
  El sincronizador del Punto A actualiza el grafo en la siguiente
  ejecución programada.
```

### Nomenclatura y estado del repositorio

El repositorio de ALM debe mantener una nomenclatura coherente con el pipeline para que la búsqueda y el filtrado sean efectivos. Las reglas de nomenclatura definidas en el Punto A (IDs entre corchetes, subcarpetas por tipo) se complementan con estas convenciones de estado:

| Estado en ALM | Significado en el modelo | Quién lo asigna |
|---|---|---|
| `Design` | TC generado por el pipeline, pendiente de revisión QA | Pipeline automáticamente |
| `Ready` | TC revisado y validado por QA para ejecución | QA engineer |
| `Repair` | TC que necesita corrección antes de poder ejecutarse | QA engineer al detectar un problema |
| `Obsolete` | TC generado desde un criterio AC que ya no existe | Sistema (detección de impacto del punto 8) |

El estado `Design` es el estado inicial de todos los test cases creados por el pipeline. Ningún test case en estado `Design` debe incluirse en un Test Set de ejecución. La transición de `Design` a `Ready` es la señal de que el QA engineer ha revisado el test case y lo considera ejecutable en el entorno actual.

### Proceso de revisión QA de test cases generados

La revisión QA de los test cases es el paso que más valor aporta en las primeras semanas de implantación, porque es donde el QA engineer calibra la calidad del output del pipeline y proporciona feedback al champion para mejorar los prompts.

La revisión de un test case generado tiene un guión de siete comprobaciones:

```
CHECKLIST DE REVISIÓN QA — Test case generado por pipeline AI

□ 1. COMPLETITUD FUNCIONAL
     ¿Están todos los pasos necesarios para llegar al estado descrito en el "Dado"?
     ¿El paso de autenticación está incluido si el sistema requiere login?
     ¿El orden de los pasos es ejecutable sin saltos implícitos?

□ 2. VERIFICABILIDAD DEL RESULTADO ESPERADO
     ¿El resultado esperado de cada paso es observable en la interfaz
     o en la respuesta de la API?
     ¿Describe algo concreto o algo subjetivo ("funciona correctamente")?

□ 3. DATOS DE PRUEBA
     ¿Los datos del campo "datos_prueba" del TC existen en el entorno de pruebas?
     ¿Los usuarios de prueba referenciados tienen el rol correcto en el entorno?
     ¿Las fechas de ejemplo son válidas para el año en curso?

□ 4. DEPENDENCIAS DE ENTORNO
     ¿El test case depende de datos creados por otro test case?
     Si es así, ¿está documentado el TC del que depende?
     ¿Podría ejecutarse de forma aislada con datos propios?

□ 5. AUTOMATIZABILIDAD
     ¿El campo "automatizable" del TC coincide con la valoración del QA engineer?
     Si está marcado como automatizable, ¿los selectores CSS/XPath del campo
     "notas_automatizacion" son correctos en el entorno actual?

□ 6. COHERENCIA CON EL COMPORTAMIENTO REAL DEL SISTEMA
     Si el sistema ya existe (proyecto de mantenimiento), ¿el resultado
     esperado coincide con el comportamiento actual del sistema en los
     casos en que no hay cambio funcional?

□ 7. COBERTURA DE CONTORNO
     ¿Los valores en "datos_prueba" de los TCs de contorno están en el
     límite exacto, no aproximado?
     ¿El TC de contorno superior prueba el valor límite exacto Y el valor
     límite + 1 en TCs separados?
```

La revisión de un test case generado por el pipeline tarda entre 3 y 8 minutos si el requisito está bien definido. Si tarda más, suele indicar que el requisito tiene ambigüedades que el pipeline no pudo resolver, lo que es feedback valioso para el validador del punto 6.

---

## Dimensión 2 — Planificación de ciclos de pruebas en ALM

### Estructura de Test Sets y Test Labs

ALM organiza la ejecución de pruebas en el módulo Test Lab, que contiene Test Sets (conjuntos de ejecución) agrupados en carpetas. La estructura de Test Lab es paralela a la estructura de Test Plan, pero refleja el cuándo y el contexto de ejecución, no solo el qué.

La estructura recomendada de Test Lab refleja la cadencia del proyecto:

```
Test Lab/
└── [PROYECTO]
    ├── Sprints/
    │   ├── Sprint 01 — 2025-01-13 / 2025-01-24
    │   │   ├── REGRESIÓN — EP-04 Facturación
    │   │   │   ├── Funcionales críticos
    │   │   │   └── Contorno crítico
    │   │   └── NUEVAS HISTORIAS — Sprint 01
    │   │       ├── US-045 Exportar facturas
    │   │       └── US-047 Filtrar facturas por fecha
    │   └── Sprint 02 — 2025-01-27 / 2025-02-07
    │       └── ...
    └── Releases/
        ├── Release 1.0 — 2025-03-31
        │   ├── REGRESIÓN COMPLETA
        │   ├── SMOKE TEST
        │   └── UAT — Gestión de Facturación
        └── Release 1.1 — 2025-06-30
            └── ...
```

Esta estructura tiene una regla importante: **los Test Sets de sprint contienen solo los test cases de las historias comprometidas en ese sprint más los test cases de regresión de los módulos afectados**. Los Test Sets de release contienen la suite de regresión completa más los test cases de UAT.

### Generación automática de Test Sets desde el pipeline

El pipeline puede generar automáticamente el esqueleto del Test Set de un sprint en ALM cuando el product owner cierra la planificación del sprint. Este es el proceso:

{% raw %}
```python
class GeneradorTestSetSprint:
    """
    Genera automáticamente el Test Set de un sprint en ALM
    basándose en las historias comprometidas en Jira y los
    test cases disponibles en el repositorio de ALM.
    """

    def __init__(self, sesion: GestorSesionALM, cliente_jira):
        self.sesion = sesion
        self.jira = cliente_jira

    def generar_test_set_sprint(
        self,
        sprint_id: str,
        sprint_nombre: str,
        sprint_fecha_inicio: str,
        sprint_fecha_fin: str
    ) -> dict:
        """
        Orquesta la creación del Test Set del sprint en ALM.
        """
        resultado = {
            "sprint_id": sprint_id,
            "test_sets_creados": [],
            "test_cases_incluidos": 0,
            "advertencias": []
        }

        # PASO 1: Obtener historias comprometidas del sprint desde Jira
        historias = self._obtener_historias_sprint(sprint_id)
        if not historias:
            resultado["advertencias"].append(
                f"No se encontraron historias en el sprint {sprint_id}"
            )
            return resultado

        # PASO 2: Para cada historia, obtener los TCs disponibles en ALM
        tcs_nuevas_historias = []
        tcs_regresion = []
        modulos_afectados = set()

        for historia in historias:
            req_id = historia.get("requisito_origen")
            if not req_id:
                continue

            modulos_afectados.add(historia.get("epica", ""))

            # TCs de las nuevas historias (estado Ready)
            tcs_historia = self._obtener_tcs_requisito_alm(
                req_id=req_id,
                solo_listos=True
            )
            tcs_nuevas_historias.extend(tcs_historia)

            if not tcs_historia:
                resultado["advertencias"].append(
                    f"Historia {historia.get('key')} ({req_id}) "
                    f"no tiene TCs en estado Ready en ALM"
                )

        # PASO 3: TCs de regresión de módulos afectados (prioridad crítica/alta)
        for epica_id in modulos_afectados:
            if not epica_id:
                continue
            tcs_modulo = self._obtener_tcs_regresion_modulo(
                epica_id=epica_id,
                prioridades=["1-High", "2-Medium"]
            )
            tcs_regresion.extend(tcs_modulo)

        # PASO 4: Crear carpeta del sprint en Test Lab
        id_carpeta_sprint = self._crear_carpeta_sprint(
            sprint_nombre=sprint_nombre,
            fecha_inicio=sprint_fecha_inicio,
            fecha_fin=sprint_fecha_fin
        )

        # PASO 5: Crear Test Set de nuevas historias
        if tcs_nuevas_historias:
            id_ts_nuevas = self._crear_test_set(
                nombre=f"NUEVAS HISTORIAS — {sprint_nombre}",
                id_carpeta=id_carpeta_sprint,
                lista_tcs=tcs_nuevas_historias
            )
            resultado["test_sets_creados"].append({
                "nombre": f"NUEVAS HISTORIAS — {sprint_nombre}",
                "id_alm": id_ts_nuevas,
                "num_tcs": len(tcs_nuevas_historias)
            })
            resultado["test_cases_incluidos"] += len(tcs_nuevas_historias)

        # PASO 6: Crear Test Set de regresión
        if tcs_regresion:
            # Deduplicar TCs que pueden aparecer en múltiples módulos
            tcs_regresion_unicos = list({
                tc["id_alm"]: tc for tc in tcs_regresion
            }.values())

            id_ts_regresion = self._crear_test_set(
                nombre=f"REGRESIÓN — {sprint_nombre}",
                id_carpeta=id_carpeta_sprint,
                lista_tcs=tcs_regresion_unicos
            )
            resultado["test_sets_creados"].append({
                "nombre": f"REGRESIÓN — {sprint_nombre}",
                "id_alm": id_ts_regresion,
                "num_tcs": len(tcs_regresion_unicos)
            })
            resultado["test_cases_incluidos"] += len(tcs_regresion_unicos)

        return resultado

    def _obtener_historias_sprint(self, sprint_id: str) -> list[dict]:
        """Consulta las historias comprometidas en el sprint desde Jira."""
        resultado = self.jira.get(
            "search",
            params={
                "jql": (
                    f"sprint = {sprint_id} "
                    f"AND issuetype = Story "
                    f"AND statusCategory != Done"
                ),
                "fields": (
                    "summary,customfield_10100,"  # requisito_origen
                    "customfield_10014,status"    # epic_link
                ),
                "maxResults": 100
            }
        )
        issues = resultado.get("issues", [])
        return [
            {
                "key": i["key"],
                "titulo": i["fields"]["summary"],
                "requisito_origen": (
                    i["fields"].get("customfield_10100", "")
                ),
                "epica": i["fields"].get("customfield_10014", "")
            }
            for i in issues
        ]

    def _obtener_tcs_requisito_alm(
        self,
        req_id: str,
        solo_listos: bool = True
    ) -> list[dict]:
        """Obtiene los TCs de un requisito desde ALM."""
        filtro_estado = ";status['Ready']" if solo_listos else ""
        respuesta = self.sesion.get(
            "tests",
            params={
                "query": f"{{user-07['{req_id}']{filtro_estado}}}",
                "fields": "id,name,priority,user-03,user-04",
                "page-size": 100
            }
        )
        if respuesta.status_code != 200:
            return []

        entidades = respuesta.json().get("entities", [])
        return [
            {
                "id_alm": int(self._extraer_campo(e, "id")),
                "nombre": self._extraer_campo(e, "name"),
                "prioridad": self._extraer_campo(e, "priority"),
                "tc_pipeline_id": self._extraer_campo(e, "user-03"),
                "tipo": self._extraer_campo(e, "user-04")
            }
            for e in entidades
        ]

    def _obtener_tcs_regresion_modulo(
        self,
        epica_id: str,
        prioridades: list[str]
    ) -> list[dict]:
        """
        Obtiene los TCs de regresión de un módulo completo.
        Solo incluye TCs en estado Ready y de prioridad alta/crítica.
        """
        prioridades_query = ";".join(
            f"priority['{p}']" for p in prioridades
        )
        # La consulta usa la estructura de carpetas del Subject
        # Buscar por nombre de carpeta que contenga el epica_id
        respuesta = self.sesion.get(
            "tests",
            params={
                "query": (
                    f"{{parent-name['[{epica_id}]*'];"
                    f"status['Ready'];"
                    f"{prioridades_query}}}"
                ),
                "fields": "id,name,priority,user-03",
                "page-size": 200
            }
        )
        if respuesta.status_code != 200:
            return []

        entidades = respuesta.json().get("entities", [])
        return [
            {
                "id_alm": int(self._extraer_campo(e, "id")),
                "nombre": self._extraer_campo(e, "name"),
                "prioridad": self._extraer_campo(e, "priority"),
                "tc_pipeline_id": self._extraer_campo(e, "user-03")
            }
            for e in entidades
        ]

    def _crear_carpeta_sprint(
        self,
        sprint_nombre: str,
        fecha_inicio: str,
        fecha_fin: str
    ) -> int:
        """Crea la carpeta del sprint en Test Lab si no existe."""
        nombre_carpeta = (
            f"{sprint_nombre} — {fecha_inicio} / {fecha_fin}"
        )
        # Obtener o crear carpeta Sprints
        id_sprints = self._obtener_o_crear_carpeta_lab(
            "Sprints", self._obtener_id_raiz_lab()
        )
        return self._obtener_o_crear_carpeta_lab(nombre_carpeta, id_sprints)

    def _crear_test_set(
        self,
        nombre: str,
        id_carpeta: int,
        lista_tcs: list[dict]
    ) -> int:
        """Crea un Test Set en ALM y le añade los TCs indicados."""
        # Crear el Test Set
        payload_ts = {
            "Fields": [
                {"Name": "name", "values": [{"value": nombre}]},
                {"Name": "parent-id", "values": [{"value": str(id_carpeta)}]},
                {"Name": "status", "values": [{"value": "Open"}]}
            ]
        }
        respuesta = self.sesion.post("test-sets", payload_ts)
        respuesta.raise_for_status()
        id_ts = int(self._extraer_campo(respuesta.json(), "id"))

        # Añadir TCs al Test Set
        for tc in lista_tcs:
            payload_instancia = {
                "Fields": [
                    {
                        "Name": "test-id",
                        "values": [{"value": str(tc["id_alm"])}]
                    },
                    {
                        "Name": "cycle-id",
                        "values": [{"value": str(id_ts)}]
                    }
                ]
            }
            self.sesion.post("test-instances", payload_instancia)

        return id_ts

    def _obtener_id_raiz_lab(self) -> int:
        """Obtiene el ID de la carpeta raíz de Test Lab."""
        respuesta = self.sesion.get(
            "test-set-folders",
            params={"query": "{name['Root']}", "fields": "id"}
        )
        respuesta.raise_for_status()
        entidades = respuesta.json().get("entities", [])
        if not entidades:
            raise RuntimeError("No se encontró la carpeta Root de Test Lab")
        return int(self._extraer_campo(entidades[0], "id"))

    def _obtener_o_crear_carpeta_lab(
        self, nombre: str, id_padre: int
    ) -> int:
        """Obtiene o crea una carpeta en Test Lab."""
        respuesta = self.sesion.get(
            "test-set-folders",
            params={
                "query": (
                    f"{{parent-id[{id_padre}];"
                    f"name['{nombre[:100]}']}}"
                ),
                "fields": "id"
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        if entidades:
            return int(self._extraer_campo(entidades[0], "id"))

        payload = {
            "Fields": [
                {"Name": "name", "values": [{"value": nombre[:255]}]},
                {"Name": "parent-id", "values": [{"value": str(id_padre)}]}
            ]
        }
        resp = self.sesion.post("test-set-folders", payload)
        resp.raise_for_status()
        return int(self._extraer_campo(resp.json(), "id"))

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                return valores[0].get("value", "") if valores else ""
        return ""
```
{% endraw %}

### Cadencia de creación de Test Sets

La creación de Test Sets sigue la cadencia del proyecto y no debe ser ad hoc. Las reglas son:

**Test Set de sprint:** se genera automáticamente el día de la planificación del sprint, una vez que el product owner confirma las historias comprometidas. Se ejecuta el comando `python orchestrator.py --generar-test-set --sprint SPRINT-15`.

**Test Set de regresión de release:** se genera manualmente dos semanas antes de la fecha de release, incluyendo todos los TCs en estado `Ready` de todos los módulos afectados por la release, ordenados por prioridad.

**Test Set de smoke test:** se mantiene permanentemente en ALM con los 15-20 TCs más críticos del sistema. Se actualiza cuando cambian los criterios de aceptación de los requisitos más críticos. Se ejecuta en cada despliegue a cualquier entorno, incluyendo desarrollo.

---

## Dimensión 3 — Ejecución y seguimiento en ALM

### Protocolo de ejecución de test cases

La ejecución de test cases en ALM sigue un protocolo que garantiza que los resultados son comparables entre ejecutores y entre ciclos. Sin protocolo, dos QA engineers pueden ejecutar el mismo test case y registrar resultados diferentes para el mismo comportamiento del sistema, lo que invalida las métricas de cobertura.

**Reglas de ejecución:**

```
PROTOCOLO DE EJECUCIÓN — Test cases pipeline AI en ALM

ANTES DE EMPEZAR:
  □ Verificar que el entorno de pruebas está en estado conocido
    (datos de referencia cargados, servicios activos, caché limpia)
  □ Verificar que el TC está en estado "Ready"
    (si está en "Design", no ejecutar — notificar al analista)
  □ Leer el TC completo antes de ejecutar el primer paso
    (los errores más frecuentes son por no leer las precondiciones)

DURANTE LA EJECUCIÓN:
  □ Ejecutar exactamente la acción descrita en cada paso
    (no interpretar; si la acción no es clara, registrar como Blocked)
  □ Registrar el resultado real en el campo "Actual" de cada paso
    (aunque sea correcto; un campo vacío no es evidencia de PASS)
  □ Adjuntar screenshot al primer paso que no coincida con el esperado
  □ No continuar ejecutando pasos cuando un resultado crítico falla
    (marcar el TC como Failed y registrar en qué paso falló)

AL REGISTRAR EL RESULTADO:
  □ Passed: TODOS los pasos tienen resultado real = resultado esperado
  □ Failed: AL MENOS UN paso crítico no coincide
    → Crear defecto en ALM vinculado al TC y al paso fallido
    → Notificar al desarrollador asignado a la historia en Jira
  □ Blocked: No se puede ejecutar por dependencia externa
    → Documentar qué dependencia lo bloquea en el campo Actual
    → No crear defecto; crear una incidencia de tipo "Impedimento"
  □ N/A: El TC no aplica en este ciclo por cambio de alcance
    → Documentar el motivo en el campo Actual
    → Notificar al analista para que evalúe si el TC debe marcarse
      como Obsolete en el repositorio
```

### Gestión de defectos vinculados a test cases

Cuando un test case falla, el defecto creado en ALM debe vincularse automáticamente al test case, al requisito y a la historia de Jira. Este vínculo es lo que permite responder en segundos a preguntas como "¿qué requisitos tienen defectos abiertos?" o "¿cuántos bugs de este sprint son por ambigüedad funcional?".

```python
class GestorDefectosALM:
    """
    Gestiona la creación y vinculación de defectos en ALM
    cuando un test case falla durante la ejecución.
    """

    def __init__(self, sesion: GestorSesionALM, cliente_jira=None):
        self.sesion = sesion
        self.jira = cliente_jira

    def crear_defecto_desde_fallo(
        self,
        id_test: int,
        id_run: int,
        id_paso_fallido: int,
        descripcion_fallo: str,
        severidad: str = "3-Medium",
        tc_metadata: dict = None
    ) -> dict:
        """
        Crea un defecto en ALM vinculado al TC fallido y
        opcionalmente crea un bug en Jira vinculado al defecto ALM.
        """
        tc_metadata = tc_metadata or {}

        # Construir la descripción del defecto con contexto completo
        descripcion = self._construir_descripcion_defecto(
            id_test=id_test,
            id_run=id_run,
            id_paso_fallido=id_paso_fallido,
            descripcion_fallo=descripcion_fallo,
            tc_metadata=tc_metadata
        )

        # Crear el defecto en ALM
        payload_defecto = {
            "Fields": [
                {
                    "Name": "summary",
                    "values": [{"value": (
                        f"[TC {tc_metadata.get('tc_pipeline_id', id_test)}] "
                        f"{descripcion_fallo[:200]}"
                    )}]
                },
                {
                    "Name": "severity",
                    "values": [{"value": severidad}]
                },
                {
                    "Name": "description",
                    "values": [{"value": descripcion}]
                },
                {
                    "Name": "status",
                    "values": [{"value": "New"}]
                },
                {
                    "Name": "detected-in-rel",
                    "values": [{"value": tc_metadata.get("release", "")}]
                },
                # Campos de trazabilidad (personalizados)
                {
                    "Name": "user-10",  # Pipeline TC ID
                    "values": [{"value": tc_metadata.get("tc_pipeline_id", "")}]
                },
                {
                    "Name": "user-11",  # Requisito Origen
                    "values": [{"value": tc_metadata.get("req_origen", "")}]
                },
                {
                    "Name": "user-12",  # Historia Jira
                    "values": [{"value": tc_metadata.get("historia_jira", "")}]
                }
            ]
        }

        respuesta = self.sesion.post("defects", payload_defecto)
        respuesta.raise_for_status()
        id_defecto = int(self._extraer_campo(respuesta.json(), "id"))

        # Vincular el defecto al run del TC
        self._vincular_defecto_a_run(id_defecto, id_run)

        resultado = {
            "id_defecto_alm": id_defecto,
            "jira_bug_key": None
        }

        # Crear bug en Jira si el cliente Jira está disponible
        if self.jira and tc_metadata.get("historia_jira"):
            jira_bug_key = self._crear_bug_jira(
                id_defecto=id_defecto,
                descripcion_fallo=descripcion_fallo,
                tc_metadata=tc_metadata
            )
            resultado["jira_bug_key"] = jira_bug_key

            # Actualizar el defecto ALM con la referencia al bug Jira
            if jira_bug_key:
                self.sesion.put(
                    f"defects/{id_defecto}",
                    {"Fields": [
                        {
                            "Name": "user-13",  # Bug Jira Key
                            "values": [{"value": jira_bug_key}]
                        }
                    ]}
                )

        return resultado

    def _construir_descripcion_defecto(
        self,
        id_test: int,
        id_run: int,
        id_paso_fallido: int,
        descripcion_fallo: str,
        tc_metadata: dict
    ) -> str:
        """Construye la descripción HTML del defecto con trazabilidad completa."""
        return (
            f"<b>CONTEXTO DE LA INCIDENCIA:</b><br/>"
            f"Test Case ALM: {id_test}<br/>"
            f"Pipeline TC ID: {tc_metadata.get('tc_pipeline_id', 'N/A')}<br/>"
            f"Criterio AC Origen: {tc_metadata.get('criterio_ac', 'N/A')}<br/>"
            f"Requisito Origen: {tc_metadata.get('req_origen', 'N/A')}<br/>"
            f"Historia Jira: {tc_metadata.get('historia_jira', 'N/A')}<br/>"
            f"Run ID: {id_run}<br/>"
            f"Paso donde falló: {id_paso_fallido}<br/>"
            f"<br/><b>DESCRIPCIÓN DEL FALLO:</b><br/>"
            f"{descripcion_fallo}<br/>"
            f"<br/><b>PASOS PARA REPRODUCIR:</b><br/>"
            f"Ver Test Case {id_test} en ALM Test Plan.<br/>"
        )

    def _vincular_defecto_a_run(self, id_defecto: int, id_run: int):
        """Vincula el defecto al run del test case en ALM."""
        try:
            payload = {
                "Fields": [
                    {
                        "Name": "defect-id",
                        "values": [{"value": str(id_defecto)}]
                    }
                ]
            }
            self.sesion.post(f"runs/{id_run}/defect-links", payload)
        except Exception as e:
            logger.warning(f"No se pudo vincular defecto {id_defecto} al run {id_run}: {e}")

    def _crear_bug_jira(
        self,
        id_defecto: int,
        descripcion_fallo: str,
        tc_metadata: dict
    ) -> Optional[str]:
        """Crea el bug correspondiente en Jira y lo vincula a la historia."""
        try:
            payload_bug = {
                "fields": {
                    "project": {"key": self.jira.config.project_key},
                    "issuetype": {"name": "Bug"},
                    "summary": (
                        f"[{tc_metadata.get('tc_pipeline_id', '?')}] "
                        f"{descripcion_fallo[:200]}"
                    ),
                    "description": {
                        "type": "doc", "version": 1,
                        "content": [{
                            "type": "paragraph",
                            "content": [{
                                "type": "text",
                                "text": (
                                    f"Defecto detectado durante la ejecución "
                                    f"del test case {tc_metadata.get('tc_pipeline_id')}.\n"
                                    f"Defecto ALM ID: {id_defecto}\n"
                                    f"Criterio AC: {tc_metadata.get('criterio_ac', 'N/A')}\n"
                                    f"Requisito: {tc_metadata.get('req_origen', 'N/A')}\n\n"
                                    f"Descripción: {descripcion_fallo}"
                                )
                            }]
                        }]
                    },
                    "priority": {"name": "High"},
                    "labels": [
                        "bug-qa", "pipeline-ai",
                        tc_metadata.get("req_origen", "")
                    ]
                }
            }

            respuesta = self.jira.post("issue", payload_bug)
            bug_key = respuesta.get("key")

            # Vincular el bug a la historia de usuario origen
            if bug_key and tc_metadata.get("historia_jira"):
                self.jira.post("issueLink", {
                    "type": {"name": "is caused by"},
                    "inwardIssue": {"key": bug_key},
                    "outwardIssue": {"key": tc_metadata["historia_jira"]}
                })

            return bug_key
        except Exception as e:
            logger.warning(f"Error creando bug en Jira: {e}")
            return None

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                return valores[0].get("value", "") if valores else ""
        return ""
```

---

## Dimensión 4 — Sincronización ALM → grafo de trazabilidad → matriz de cobertura

### El ciclo completo de trazabilidad

El grafo de trazabilidad del punto 9 del modelo recibe información de tres fuentes: el pipeline de generación (al crear artefactos), la integración Jira (al actualizar issues) y ALM (al ejecutar test cases). La sincronización de ALM es la que cierra el ciclo completo:

```
Requisito YAML
    │
    ├── genera ──► Historia Jira (FACT-47)
    │                   │
    │                   ├── descompone ──► Tarea backend (FACT-48)
    │                   │                     │
    │                   │                     └── implementa ──► commit abc123
    │                   │
    │                   └── genera ──► Criterio AC (AC-023-01)
    │                                       │
    │                                       └── origina ──► TC pipeline (TC-023-01)
    │                                                           │
    │                                                           └── vincula ──► TC ALM (id=4821)
    │                                                                               │
    │                                                                               └── tiene_resultado ──► Run (Passed)
    │                                                                                                           │
    │                                                                                                           └── genera ──► Defecto ALM (id=392)
    │                                                                                                                               │
    │                                                                                                                               └── vincula ──► Bug Jira (FACT-89)
```

Este grafo completo permite responder en tiempo real a preguntas que en un proceso manual tardan horas: "¿qué defectos abiertos en Jira están relacionados con el requisito REQ-023?", "¿qué commits están asociados a las historias que tienen TCs fallidos?", "¿qué porcentaje de los criterios de aceptación del sprint actual tienen al menos un run Passed?"

### Proceso de sincronización programada

La sincronización entre ALM y el grafo de trazabilidad se ejecuta en tres momentos distintos con propósitos distintos:

{% raw %}
```python
class OrquestadorSincronizacionALM:
    """
    Orquesta los tres tipos de sincronización ALM → trazabilidad:
    - Diaria: actualiza estados de ejecución del día
    - Por sprint: consolida métricas al cerrar un sprint
    - Por release: genera el informe completo de cobertura para go/no-go
    """

    def __init__(
        self,
        config_alm: ALMConfig,
        motor_trazabilidad,
        notificador=None
    ):
        self.config_alm = config_alm
        self.trazabilidad = motor_trazabilidad
        self.notificador = notificador

    def sincronizacion_diaria(self, proyecto: str) -> dict:
        """
        Ejecutar cada noche a las 22:00.
        Actualiza el estado de todos los TCs ejecutados durante el día.
        """
        with GestorSesionALM(self.config_alm) as sesion:
            sincronizador = SincronizadorResultadosALM(
                sesion, self.trazabilidad
            )

            # Obtener TCs con runs del día de hoy
            hoy = datetime.now().strftime("%Y-%m-%d")
            tcs_ejecutados_hoy = self._obtener_tcs_ejecutados_desde(
                sesion, fecha_desde=hoy
            )

            resultados = {
                "fecha": hoy,
                "tcs_actualizados": 0,
                "fallidos_nuevos": [],
                "pasados_nuevos": []
            }

            for tc_id_alm, estado_nuevo in tcs_ejecutados_hoy.items():
                # Obtener estado anterior del grafo
                estado_anterior = self._obtener_estado_anterior(tc_id_alm)
                estado_pipeline = SincronizadorResultadosALM \
                    .MAPA_ESTADO_ALM_A_PIPELINE.get(estado_nuevo, "pendiente")

                # Actualizar el grafo
                self.trazabilidad.registrar_nodo(Nodo(
                    id=f"ALM-{tc_id_alm}",
                    tipo="test_case_alm",
                    titulo="",
                    estado=estado_pipeline,
                    metadatos={
                        "alm_id": tc_id_alm,
                        "ultimo_estado_alm": estado_nuevo,
                        "fecha_sincronizacion": datetime.now().isoformat()
                    }
                ))
                resultados["tcs_actualizados"] += 1

                # Detectar cambios de estado relevantes
                if estado_nuevo == "Failed" and estado_anterior != "Failed":
                    resultados["fallidos_nuevos"].append(tc_id_alm)

                if estado_nuevo == "Passed" and estado_anterior == "Failed":
                    resultados["pasados_nuevos"].append(tc_id_alm)

            # Notificar si hay nuevos fallos
            if resultados["fallidos_nuevos"] and self.notificador:
                self.notificador.enviar(
                    severidad="alta",
                    titulo=(
                        f"⚠ {len(resultados['fallidos_nuevos'])} nuevos "
                        f"TCs fallidos en ALM"
                    ),
                    descripcion=(
                        f"TCs que fallaron hoy: "
                        f"{resultados['fallidos_nuevos'][:10]}"
                    ),
                    destinatarios=["qa_lead", "tech_lead"]
                )

            return resultados

    def sincronizacion_cierre_sprint(
        self,
        sprint_id: str,
        sprint_nombre: str
    ) -> dict:
        """
        Ejecutar al cierre de cada sprint.
        Genera el informe de cobertura del sprint y lo publica.
        """
        with GestorSesionALM(self.config_alm) as sesion:
            # Obtener todos los TCs del Test Set del sprint
            id_test_set = self._buscar_test_set_sprint(sesion, sprint_nombre)
            if not id_test_set:
                return {
                    "error": f"No se encontró Test Set para {sprint_nombre}"
                }

            metricas = self._calcular_metricas_test_set(sesion, id_test_set)
            informe = self._generar_informe_sprint(sprint_id, sprint_nombre, metricas)

            # Publicar en el grafo de trazabilidad como nodo de sprint
            self.trazabilidad.registrar_nodo(Nodo(
                id=f"SPRINT-{sprint_id}",
                tipo="sprint",
                titulo=sprint_nombre,
                estado="cerrado",
                metadatos={
                    "metricas_qa": metricas,
                    "fecha_cierre": datetime.now().isoformat()
                }
            ))

            return informe

    def informe_cobertura_release(
        self,
        release_id: str,
        release_nombre: str
    ) -> dict:
        """
        Genera el informe completo de cobertura para la decisión go/no-go
        de una release. Incluye todos los módulos afectados.
        """
        with GestorSesionALM(self.config_alm) as sesion:
            id_test_set_release = self._buscar_test_set_release(
                sesion, release_nombre
            )
            metricas_release = self._calcular_metricas_test_set(
                sesion, id_test_set_release
            )

            # Obtener defectos abiertos vinculados a la release
            defectos_abiertos = self._obtener_defectos_abiertos_release(
                sesion, release_id
            )

            informe = {
                "release_id": release_id,
                "release_nombre": release_nombre,
                "fecha_informe": datetime.now().isoformat(),
                "metricas_ejecucion": metricas_release,
                "defectos_abiertos": defectos_abiertos,
                "semaforo_go_no_go": self._calcular_semaforo(
                    metricas_release, defectos_abiertos
                ),
                "criterios_salida": self._evaluar_criterios_salida(
                    metricas_release, defectos_abiertos
                )
            }

            return informe

    def _calcular_metricas_test_set(
        self,
        sesion: GestorSesionALM,
        id_test_set: int
    ) -> dict:
        """Calcula las métricas de ejecución de un Test Set."""
        respuesta = sesion.get(
            "test-instances",
            params={
                "query": f"{{cycle-id[{id_test_set}]}}",
                "fields": "id,status,test-id",
                "page-size": 500
            }
        )
        instancias = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        total = len(instancias)
        contadores = {
            "Passed": 0, "Failed": 0,
            "Blocked": 0, "N/A": 0, "No Run": 0
        }

        for inst in instancias:
            estado = self._extraer_campo(inst, "status")
            if estado in contadores:
                contadores[estado] += 1

        ejecutados = total - contadores["No Run"]
        pasados = contadores["Passed"]

        return {
            "total_tcs": total,
            "ejecutados": ejecutados,
            "pasados": pasados,
            "fallidos": contadores["Failed"],
            "bloqueados": contadores["Blocked"],
            "no_aplica": contadores["N/A"],
            "pendientes": contadores["No Run"],
            "porcentaje_ejecucion": round(ejecutados / total * 100) if total else 0,
            "porcentaje_passed": round(pasados / ejecutados * 100) if ejecutados else 0
        }

    def _calcular_semaforo(
        self,
        metricas: dict,
        defectos_abiertos: list
    ) -> str:
        """Calcula el semáforo go/no-go basado en métricas y defectos."""
        defectos_criticos = sum(
            1 for d in defectos_abiertos
            if d.get("severidad") in ("1-Critical", "2-High")
        )
        pct_passed = metricas.get("porcentaje_passed", 0)
        pct_ejecucion = metricas.get("porcentaje_ejecucion", 0)

        if defectos_criticos > 0 or pct_passed < 85:
            return "ROJO"
        if pct_passed < 95 or pct_ejecucion < 95:
            return "AMARILLO"
        return "VERDE"

    def _obtener_tcs_ejecutados_desde(
        self, sesion: GestorSesionALM, fecha_desde: str
    ) -> dict[int, str]:
        """
        Obtiene los TCs que tienen algún run desde la fecha indicada.
        Retorna un diccionario {id_test: ultimo_estado}.
        """
        respuesta = sesion.get(
            "runs",
            params={
                "query": f"{{execution-date[>= '{fecha_desde}']}}",
                "fields": "id,test-id,status,execution-date",
                "order-by": "{execution-date[DESC]}",
                "page-size": 500
            }
        )
        if respuesta.status_code != 200:
            return {}

        runs = respuesta.json().get("entities", [])
        # Keeper solo el último run por test (el primero al estar ordenado DESC)
        tcs_estado = {}
        for run in runs:
            id_test = self._extraer_campo(run, "test-id")
            if id_test and id_test not in tcs_estado:
                tcs_estado[int(id_test)] = self._extraer_campo(run, "status")
        return tcs_estado

    def _obtener_estado_anterior(self, tc_id_alm: int) -> str:
        """Obtiene el estado actual del TC en el grafo de trazabilidad."""
        try:
            with self.trazabilidad.db.cursor() as cur:
                cur.execute(
                    "SELECT estado FROM nodos_trazabilidad WHERE id = %s",
                    (f"ALM-{tc_id_alm}",)
                )
                fila = cur.fetchone()
                return fila[0] if fila else "pendiente"
        except Exception:
            return "pendiente"

    def _buscar_test_set_sprint(
        self, sesion: GestorSesionALM, sprint_nombre: str
    ) -> Optional[int]:
        """Busca el ID del Test Set de un sprint en ALM."""
        respuesta = sesion.get(
            "test-sets",
            params={
                "query": f"{{name['*{sprint_nombre}*']}}",
                "fields": "id,name"
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []
        if not entidades:
            return None
        return int(self._extraer_campo(entidades[0], "id"))

    def _buscar_test_set_release(
        self, sesion: GestorSesionALM, release_nombre: str
    ) -> Optional[int]:
        """Busca el Test Set de regresión completa de una release."""
        respuesta = sesion.get(
            "test-sets",
            params={
                "query": f"{{name['REGRESIÓN COMPLETA*{release_nombre}*']}}",
                "fields": "id,name"
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []
        return int(self._extraer_campo(entidades[0], "id")) if entidades else None

    def _obtener_defectos_abiertos_release(
        self, sesion: GestorSesionALM, release_id: str
    ) -> list[dict]:
        """Obtiene los defectos abiertos detectados en la release."""
        respuesta = sesion.get(
            "defects",
            params={
                "query": (
                    f"{{detected-in-rel['{release_id}'];"
                    f"status[!Closed;!Rejected]}}"
                ),
                "fields": "id,summary,severity,status",
                "page-size": 200
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []
        return [
            {
                "id": self._extraer_campo(e, "id"),
                "resumen": self._extraer_campo(e, "summary"),
                "severidad": self._extraer_campo(e, "severity"),
                "estado": self._extraer_campo(e, "status")
            }
            for e in entidades
        ]

    def _generar_informe_sprint(
        self,
        sprint_id: str,
        sprint_nombre: str,
        metricas: dict
    ) -> dict:
        """Genera el informe de cierre de sprint."""
        return {
            "sprint_id": sprint_id,
            "sprint_nombre": sprint_nombre,
            "fecha_cierre": datetime.now().isoformat(),
            "metricas": metricas,
            "semaforo": (
                "verde" if metricas.get("porcentaje_passed", 0) >= 95
                else "amarillo" if metricas.get("porcentaje_passed", 0) >= 85
                else "rojo"
            )
        }

    def _evaluar_criterios_salida(
        self,
        metricas: dict,
        defectos_abiertos: list
    ) -> list[dict]:
        """Evalúa cada criterio de salida y devuelve su estado."""
        # Ver Dimensión 5 para la definición completa de criterios
        defectos_criticos = sum(
            1 for d in defectos_abiertos
            if d.get("severidad") in ("1-Critical", "2-High")
        )
        return [
            {
                "criterio": "Sin defectos críticos o altos abiertos",
                "cumplido": defectos_criticos == 0,
                "valor": defectos_criticos,
                "umbral": 0
            },
            {
                "criterio": "Tasa de TCs Passed ≥ 95%",
                "cumplido": metricas.get("porcentaje_passed", 0) >= 95,
                "valor": metricas.get("porcentaje_passed", 0),
                "umbral": 95
            },
            {
                "criterio": "Tasa de ejecución ≥ 95%",
                "cumplido": metricas.get("porcentaje_ejecucion", 0) >= 95,
                "valor": metricas.get("porcentaje_ejecucion", 0),
                "umbral": 95
            },
            {
                "criterio": "TCs bloqueados ≤ 3%",
                "cumplido": (
                    metricas.get("bloqueados", 0) /
                    max(metricas.get("total_tcs", 1), 1) * 100
                ) <= 3,
                "valor": round(
                    metricas.get("bloqueados", 0) /
                    max(metricas.get("total_tcs", 1), 1) * 100, 1
                ),
                "umbral": 3
            }
        ]

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                return valores[0].get("value", "") if valores else ""
        return ""
```
{% endraw %}

---

## Dimensión 5 — Criterios de salida (exit criteria)

### El propósito de los criterios de salida en este modelo

Los criterios de salida son el contrato entre el equipo de QA y el product owner sobre cuándo un conjunto de funcionalidad está suficientemente verificado para entregarse. Sin criterios de salida explícitos, la decisión de release es subjetiva y varía según la presión del negocio en cada ciclo.

En el modelo AI-ready, los criterios de salida tienen una ventaja adicional respecto a los proyectos tradicionales: son evaluables automáticamente. El orquestador de sincronización calcula en tiempo real si los criterios se cumplen, sin necesidad de que el QA lead prepare un informe manual.

### Criterios de salida por nivel de entrega

Los criterios se estructuran en tres niveles con umbrales diferentes según el riesgo de la entrega:

```
CRITERIOS DE SALIDA — Modelo AI-Ready con ALM

NIVEL 1 — Fin de sprint (entrega a desarrollo/integración)
──────────────────────────────────────────────────────────
Obligatorios (bloquean la entrega si no se cumplen):
  ✓ Sin defectos de severidad Critical abiertos vinculados al sprint
  ✓ Tasa de TCs Passed en Test Set de nuevas historias ≥ 90%
  ✓ Todos los criterios de aceptación de prioridad Must Have
    tienen al menos un TC en estado Passed

Recomendados (se documenta si no se cumplen, pero no bloquean):
  ○ Tasa de TCs Passed en Test Set de regresión ≥ 95%
  ○ TCs en estado Blocked ≤ 5% del total
  ○ Todos los TCs de tipo "contorno" ejecutados al menos una vez

NIVEL 2 — Release candidate (entrega a preproducción / UAT)
──────────────────────────────────────────────────────────
Obligatorios:
  ✓ Sin defectos Critical ni High abiertos sin plan de resolución
  ✓ Tasa de TCs Passed en regresión completa ≥ 95%
  ✓ Tasa de ejecución del Test Set de release ≥ 95%
    (máximo 5% de TCs en estado No Run o Blocked)
  ✓ Todos los módulos afectados por la release tienen cobertura
    de criterios AC ≥ 85% (medido en el grafo de trazabilidad)
  ✓ El smoke test ejecuta y pasa al 100% en el entorno de release

Recomendados:
  ○ TCs automatizados del smoke test ejecutan sin intervención manual
  ○ Tiempo medio de ejecución del smoke test ≤ 15 minutos
  ○ Sin defectos Medium abiertos con antigüedad > 2 sprints

NIVEL 3 — Go-Live (entrega a producción)
──────────────────────────────────────────────────────────
Obligatorios:
  ✓ Todos los criterios del Nivel 2 cumplidos
  ✓ UAT firmado por el responsable de negocio de cada módulo
  ✓ Sin defectos Critical, High ni Medium abiertos sin cierre planificado
  ✓ El plan de rollback está documentado y validado
  ✓ El smoke test de producción está preparado y aprobado por el QA lead
```

### Dashboard de criterios de salida en tiempo real

El dashboard es el artefacto más visible del gobierno del ciclo de vida de pruebas: es lo que el product owner consulta para tomar la decisión de release sin necesidad de preguntar al QA lead.

```python
class DashboardCriteriosSalida:
    """
    Genera el dashboard de criterios de salida en tiempo real
    para la decisión go/no-go del product owner.
    """

    UMBRAL_NIVEL_1 = {
        "passed_nuevas_historias": 90,
        "defectos_critical": 0,
        "blocked_max_pct": 5
    }
    UMBRAL_NIVEL_2 = {
        "passed_regresion": 95,
        "ejecucion_minima": 95,
        "cobertura_ac": 85,
        "defectos_critical_high": 0
    }

    def __init__(self, orquestador: OrquestadorSincronizacionALM):
        self.orquestador = orquestador

    def generar_dashboard_markdown(
        self,
        nivel: int,
        release_id: str,
        sprint_id: str = None
    ) -> str:
        """Genera el dashboard en Markdown para publicar en Confluence."""

        if nivel == 1 and sprint_id:
            informe = self.orquestador.sincronizacion_cierre_sprint(
                sprint_id=sprint_id,
                sprint_nombre=sprint_id
            )
            return self._dashboard_nivel_1(informe)
        elif nivel in (2, 3):
            informe = self.orquestador.informe_cobertura_release(
                release_id=release_id,
                release_nombre=release_id
            )
            return self._dashboard_nivel_2_3(informe, nivel)
        else:
            return "# Error: nivel no reconocido"

    def _dashboard_nivel_1(self, informe: dict) -> str:
        m = informe.get("metricas", {})
        semaforo_emoji = {
            "verde": "🟢", "amarillo": "🟡", "rojo": "🔴"
        }.get(informe.get("semaforo", "rojo"), "🔴")

        return f"""# Dashboard QA — Cierre de Sprint
**Sprint:** {informe.get('sprint_nombre', 'N/A')}
**Fecha:** {informe.get('fecha_cierre', 'N/A')[:10]}
**Resultado:** {semaforo_emoji} {informe.get('semaforo', 'N/A').upper()}

## Métricas de ejecución

| Métrica | Valor | Umbral | Estado |
|---|---|---|---|
| TCs Passed (nuevas historias) | {m.get('porcentaje_passed', 0):.0f}% | ≥ 90% | {'✅' if m.get('porcentaje_passed', 0) >= 90 else '❌'} |
| Tasa de ejecución | {m.get('porcentaje_ejecucion', 0):.0f}% | ≥ 90% | {'✅' if m.get('porcentaje_ejecucion', 0) >= 90 else '❌'} |
| TCs fallidos | {m.get('fallidos', 0)} | 0 críticos | {'✅' if m.get('fallidos', 0) == 0 else '⚠'} |
| TCs bloqueados | {m.get('bloqueados', 0)} | ≤ 5% | {'✅' if (m.get('bloqueados', 0) / max(m.get('total_tcs', 1), 1) * 100) <= 5 else '⚠'} |

## Distribución de resultados

```
Total TCs del sprint:  {m.get('total_tcs', 0):>4}
  ✅ Passed:           {m.get('pasados', 0):>4}  ({m.get('porcentaje_passed', 0):.0f}%)
  ❌ Failed:           {m.get('fallidos', 0):>4}
  🚧 Blocked:         {m.get('bloqueados', 0):>4}
  ⏸ No Run:           {m.get('pendientes', 0):>4}
  ➖ N/A:             {m.get('no_aplica', 0):>4}
```

*Dashboard generado automáticamente por el pipeline AI.*
*Fuente de datos: ALM Test Lab — sincronización del {informe.get('fecha_cierre', '')[:10]}*
"""

    def _dashboard_nivel_2_3(self, informe: dict, nivel: int) -> str:
        m = informe.get("metricas_ejecucion", {})
        criterios = informe.get("criterios_salida", [])
        defectos = informe.get("defectos_abiertos", [])
        semaforo = informe.get("semaforo_go_no_go", "ROJO")

        semaforo_emoji = {
            "VERDE": "🟢 GO", "AMARILLO": "🟡 CONDICIONADO", "ROJO": "🔴 NO-GO"
        }.get(semaforo, "🔴 NO-GO")

        defectos_critical = [
            d for d in defectos if d.get("severidad") == "1-Critical"
        ]
        defectos_high = [
            d for d in defectos if d.get("severidad") == "2-High"
        ]
        defectos_medium = [
            d for d in defectos if d.get("severidad") == "3-Medium"
        ]

        filas_criterios = "\n".join(
            f"| {c['criterio']} | {c['valor']} | "
            f"{c['umbral']} | {'✅' if c['cumplido'] else '❌'} |"
            for c in criterios
        )

        filas_defectos = ""
        if defectos:
            filas_defectos = "\n## Defectos abiertos\n\n"
            filas_defectos += "| ID | Severidad | Estado | Resumen |\n"
            filas_defectos += "|---|---|---|---|\n"
            for d in sorted(defectos, key=lambda x: x.get("severidad", "")):
                filas_defectos += (
                    f"| {d['id']} | {d['severidad']} | "
                    f"{d['estado']} | {d['resumen'][:80]} |\n"
                )
        else:
            filas_defectos = "\n✅ **Sin defectos abiertos**\n"

        return f"""# Dashboard Go/No-Go — {"Release Candidate" if nivel == 2 else "Go-Live"}
**Release:** {informe.get('release_nombre', 'N/A')}
**Fecha informe:** {informe.get('fecha_informe', 'N/A')[:10]}

## {semaforo_emoji}

## Criterios de salida (Nivel {nivel})

| Criterio | Valor actual | Umbral | Estado |
|---|---|---|---|
{filas_criterios}

## Métricas de ejecución

| Métrica | Valor |
|---|---|
| Total TCs en scope | {m.get('total_tcs', 0)} |
| Ejecutados | {m.get('ejecutados', 0)} ({m.get('porcentaje_ejecucion', 0):.0f}%) |
| Passed | {m.get('pasados', 0)} ({m.get('porcentaje_passed', 0):.0f}% sobre ejecutados) |
| Failed | {m.get('fallidos', 0)} |
| Blocked | {m.get('bloqueados', 0)} |
| Pendientes (No Run) | {m.get('pendientes', 0)} |

## Resumen de defectos

| Severidad | Abiertos |
|---|---|
| 🔴 Critical | {len(defectos_critical)} |
| 🟠 High | {len(defectos_high)} |
| 🟡 Medium | {len(defectos_medium)} |
| Total | {len(defectos)} |
{filas_defectos}
---
*Dashboard generado automáticamente por el pipeline AI.*
*Fuente de datos: ALM + grafo de trazabilidad.*
*Última sincronización: {informe.get('fecha_informe', '')[:16]}*
"""
```

---

## Roles y responsabilidades en el gobierno de pruebas ALM

El gobierno del ciclo de vida en ALM tiene una distribución de responsabilidades distinta al gobierno del pipeline descrito en el punto 12 del modelo. Las responsabilidades de QA son operativas y continuas; las del analista y el champion son de supervisión y resolución de conflictos.

| Actividad | QA Engineer | QA Lead | Analista Funcional | Champion Pipeline |
|---|---|---|---|---|
| Revisar TCs en estado Design → Ready | ✓ Ejecuta | Supervisa | — | — |
| Modificar zona operativa de un TC | ✓ Ejecuta | Aprueba | — | — |
| Solicitar corrección de zona funcional | ✓ Detecta | — | ✓ Corrige | Coordina |
| Crear Test Sets de sprint | — | ✓ Ejecuta | — | — |
| Ejecutar TCs y registrar resultados | ✓ Ejecuta | Supervisa | — | — |
| Crear defectos en ALM y Jira | ✓ Ejecuta | Revisa | — | — |
| Evaluar criterios de salida | — | ✓ Valida | — | — |
| Presentar dashboard go/no-go al PO | — | ✓ Presenta | — | — |
| Sincronización diaria ALM → grafo | Automática | Revisa alertas | — | Mantiene script |
| Actualizar umbral de criterios de salida | — | Propone | Valida | Aprueba técnico |
| Auditoría trimestral del repositorio ALM | — | ✓ Ejecuta | — | Participa |

### Cadencia de reuniones de gobierno QA

El gobierno del ciclo de vida de pruebas se apoya en tres reuniones con cadencias distintas:

**Revisión diaria de estado de ejecución (10 minutos, asíncrona):** el QA lead revisa el dashboard automático generado por la sincronización nocturna. Si hay TCs fallidos nuevos, notifica al tech lead correspondiente. No hay reunión: es un proceso de lectura del dashboard publicado en Confluence.

**Revisión semanal de Test Sets y bloqueos (30 minutos):** QA lead, QA engineers y tech lead. Se revisan los TCs bloqueados de la semana, se identifican las causas (entorno, datos de prueba, dependencia de otro TC) y se asignan acciones de resolución. Se revisa también si los TCs recién llegados del pipeline están pasando correctamente a estado Ready.

**Revisión de criterios de salida pre-release (60 minutos):** QA lead, product owner, analista líder y responsable técnico. Se presenta el dashboard de Nivel 2 o Nivel 3, se discuten los criterios que no se cumplen y se toma la decisión go/no-go documentada. Si la decisión es no-go, se define el plan de remediación con fechas.

---

## Auditoría trimestral del repositorio ALM

Igual que el repositorio de requisitos del pipeline necesita auditoría periódica (punto 12 del modelo), el repositorio de test cases en ALM necesita una limpieza trimestral para evitar la acumulación de TCs obsoletos, duplicados o huérfanos (sin requisito origen válido).

{% raw %}
```python
class AuditorRepositorioALM:
    """
    Ejecuta la auditoría trimestral del repositorio de test cases en ALM.
    Identifica TCs obsoletos, sin ejecutar, huérfanos y duplicados.
    """

    def __init__(self, sesion: GestorSesionALM, motor_trazabilidad):
        self.sesion = sesion
        self.trazabilidad = motor_trazabilidad

    def ejecutar_auditoria_completa(self) -> dict:
        """Ejecuta todos los análisis y produce el informe de auditoría."""
        return {
            "fecha_auditoria": datetime.now().isoformat(),
            "tcs_obsoletos": self._detectar_tcs_obsoletos(),
            "tcs_sin_ejecutar_mas_de_2_sprints": self._detectar_tcs_sin_ejecucion(),
            "tcs_huerfanos": self._detectar_tcs_huerfanos(),
            "tcs_en_estado_design_mas_de_1_sprint": self._detectar_tcs_design_antiguos(),
            "duplicados_potenciales": self._detectar_duplicados()
        }

    def _detectar_tcs_obsoletos(self) -> list[dict]:
        """
        Detecta TCs cuyo criterio AC origen ya no existe en el repositorio
        de requisitos (porque el requisito fue modificado o deprecado).
        """
        # Consultar todos los TCs con su criterio AC origen (user-05)
        respuesta = self.sesion.get(
            "tests",
            params={
                "query": "{status[!Obsolete]}",
                "fields": "id,name,user-03,user-05,user-07",
                "page-size": 1000
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        obsoletos = []
        for e in entidades:
            ac_id = self._extraer_campo(e, "user-05")
            req_id = self._extraer_campo(e, "user-07")

            if not ac_id or not req_id:
                continue

            # Verificar en el grafo si el criterio AC todavía existe
            existe_ac = self._existe_en_grafo(ac_id)
            existe_req = self._existe_en_grafo(req_id)

            if not existe_ac or not existe_req:
                obsoletos.append({
                    "id_alm": self._extraer_campo(e, "id"),
                    "nombre": self._extraer_campo(e, "name"),
                    "tc_pipeline_id": self._extraer_campo(e, "user-03"),
                    "criterio_ac": ac_id,
                    "req_origen": req_id,
                    "motivo": (
                        "Criterio AC no existe en el grafo"
                        if not existe_ac
                        else "Requisito no existe en el grafo"
                    ),
                    "accion_recomendada": "Marcar como Obsolete en ALM"
                })
        return obsoletos

    def _detectar_tcs_sin_ejecucion(self) -> list[dict]:
        """
        Detecta TCs en estado Ready que no han sido ejecutados
        en más de dos sprints (aproximadamente 4 semanas).
        """
        from datetime import timedelta
        fecha_limite = (datetime.now() - timedelta(weeks=4)).strftime("%Y-%m-%d")

        respuesta = self.sesion.get(
            "tests",
            params={
                "query": f"{{status['Ready'];last-modified[< '{fecha_limite}']}}",
                "fields": "id,name,user-03,last-modified",
                "page-size": 500
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        sin_ejecucion = []
        for e in entidades:
            id_alm = self._extraer_campo(e, "id")
            # Verificar si tiene algún run
            respuesta_runs = self.sesion.get(
                f"tests/{id_alm}/runs",
                params={"fields": "id", "page-size": 1}
            )
            tiene_runs = bool(
                respuesta_runs.json().get("entities", [])
                if respuesta_runs.status_code == 200 else []
            )

            if not tiene_runs:
                sin_ejecucion.append({
                    "id_alm": id_alm,
                    "nombre": self._extraer_campo(e, "name"),
                    "tc_pipeline_id": self._extraer_campo(e, "user-03"),
                    "ultima_modificacion": self._extraer_campo(e, "last-modified"),
                    "accion_recomendada": (
                        "Incluir en el próximo Test Set de regresión "
                        "o evaluar si sigue siendo relevante"
                    )
                })
        return sin_ejecucion

    def _detectar_tcs_huerfanos(self) -> list[dict]:
        """
        Detecta TCs sin campo Pipeline TC ID (user-03) o
        sin referencia a requisito válido (user-07).
        Suelen ser TCs creados manualmente fuera del pipeline.
        """
        respuesta = self.sesion.get(
            "tests",
            params={
                "query": "{user-03['']}",  # Campo Pipeline TC ID vacío
                "fields": "id,name,parent-id",
                "page-size": 500
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        return [
            {
                "id_alm": self._extraer_campo(e, "id"),
                "nombre": self._extraer_campo(e, "name"),
                "carpeta_id": self._extraer_campo(e, "parent-id"),
                "accion_recomendada": (
                    "Añadir manualmente los campos Pipeline TC ID "
                    "y Requisito Origen, o migrar al proceso del pipeline"
                )
            }
            for e in entidades
        ]

    def _detectar_tcs_design_antiguos(self) -> list[dict]:
        """
        Detecta TCs en estado Design con más de un sprint de antigüedad.
        Indican TCs generados por el pipeline que nadie ha revisado.
        """
        from datetime import timedelta
        fecha_limite = (datetime.now() - timedelta(weeks=2)).strftime("%Y-%m-%d")

        respuesta = self.sesion.get(
            "tests",
            params={
                "query": f"{{status['Design'];creation-time[< '{fecha_limite}']}}",
                "fields": "id,name,user-03,user-07,creation-time",
                "page-size": 500
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        return [
            {
                "id_alm": self._extraer_campo(e, "id"),
                "nombre": self._extraer_campo(e, "name"),
                "tc_pipeline_id": self._extraer_campo(e, "user-03"),
                "req_origen": self._extraer_campo(e, "user-07"),
                "fecha_creacion": self._extraer_campo(e, "creation-time"),
                "accion_recomendada": (
                    "El QA engineer debe revisar y mover a Ready o Repair"
                )
            }
            for e in entidades
        ]

    def _detectar_duplicados(self) -> list[dict]:
        """
        Detecta posibles TCs duplicados buscando tests con el mismo
        Pipeline TC ID (user-03) en más de una entidad ALM.
        """
        respuesta = self.sesion.get(
            "tests",
            params={
                "query": "{user-03[!'']}",
                "fields": "id,name,user-03",
                "page-size": 2000
            }
        )
        entidades = respuesta.json().get("entities", []) \
            if respuesta.status_code == 200 else []

        # Agrupar por Pipeline TC ID
        por_tc_id: dict[str, list] = {}
        for e in entidades:
            tc_id = self._extraer_campo(e, "user-03")
            if tc_id:
                por_tc_id.setdefault(tc_id, []).append({
                    "id_alm": self._extraer_campo(e, "id"),
                    "nombre": self._extraer_campo(e, "name")
                })

        # Retornar solo los que tienen más de una instancia
        return [
            {
                "tc_pipeline_id": tc_id,
                "instancias": instancias,
                "accion_recomendada": (
                    "Conservar la instancia más reciente. "
                    "Eliminar o marcar como Obsolete las anteriores."
                )
            }
            for tc_id, instancias in por_tc_id.items()
            if len(instancias) > 1
        ]

    def _existe_en_grafo(self, nodo_id: str) -> bool:
        """Verifica si un nodo existe y está activo en el grafo de trazabilidad."""
        try:
            with self.trazabilidad.db.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM nodos_trazabilidad WHERE id = %s AND activo = TRUE",
                    (nodo_id,)
                )
                return cur.fetchone() is not None
        except Exception:
            return False

    @staticmethod
    def _extraer_campo(entidad: dict, nombre_campo: str) -> str:
        for campo in entidad.get("Fields", []):
            if campo.get("Name") == nombre_campo:
                valores = campo.get("values", [])
                return valores[0].get("value", "") if valores else ""
        return ""
```
{% endraw %}

### Informe de auditoría en Markdown

{% raw %}
```python
def generar_informe_auditoria_markdown(resultado: dict) -> str:
    """Formatea el resultado de la auditoría en Markdown para Confluence."""
    total_acciones = (
        len(resultado["tcs_obsoletos"]) +
        len(resultado["tcs_huerfanos"]) +
        len(resultado["tcs_en_estado_design_mas_de_1_sprint"]) +
        len(resultado["duplicados_potenciales"])
    )
    nivel_riesgo = (
        "🔴 ALTO" if total_acciones > 20
        else "🟡 MEDIO" if total_acciones > 5
        else "🟢 BAJO"
    )

    return f"""# Auditoría trimestral — Repositorio ALM
**Fecha:** {resultado['fecha_auditoria'][:10]}
**Nivel de riesgo:** {nivel_riesgo}
**Total acciones requeridas:** {total_acciones}

## Resumen ejecutivo

| Categoría | Cantidad | Acción recomendada |
|---|---|---|
| TCs obsoletos (criterio AC inexistente) | {len(resultado['tcs_obsoletos'])} | Marcar como Obsolete |
| TCs sin ejecutar en > 2 sprints | {len(resultado['tcs_sin_ejecutar_mas_de_2_sprints'])} | Incluir en próximo Test Set o deprecar |
| TCs huérfanos (sin Pipeline TC ID) | {len(resultado['tcs_huerfanos'])} | Asociar al pipeline o eliminar |
| TCs en Design > 1 sprint | {len(resultado['tcs_en_estado_design_mas_de_1_sprint'])} | QA engineer debe revisar |
| TCs duplicados | {len(resultado['duplicados_potenciales'])} | Eliminar duplicados |

## Detalle de TCs obsoletos

{"Sin TCs obsoletos detectados. ✅" if not resultado['tcs_obsoletos'] else
chr(10).join(
    f"- ALM {tc['id_alm']} | `{tc['tc_pipeline_id']}` | {tc['motivo']}"
    for tc in resultado['tcs_obsoletos'][:20]
)}

## TCs en estado Design con más de un sprint de antigüedad

{"Sin TCs pendientes de revisión. ✅" if not resultado['tcs_en_estado_design_mas_de_1_sprint'] else
chr(10).join(
    f"- ALM {tc['id_alm']} | `{tc['tc_pipeline_id']}` | Req: {tc['req_origen']} | Creado: {tc['fecha_creacion'][:10]}"
    for tc in resultado['tcs_en_estado_design_mas_de_1_sprint'][:20]
)}

---
*Auditoría generada automáticamente por el pipeline AI.*
*Referencia: Punto B — Gobierno del ciclo de vida de pruebas en ALM.*
"""
```
{% endraw %}

---

## Integración del Punto B en el orquestador principal

Los componentes del Punto B se invocan desde el orquestador principal del modelo como comandos específicos, separados del flujo de generación de artefactos:

```bash
# Generar Test Set automático al planificar el sprint
python orchestrator.py --generar-test-set --sprint SPRINT-15

# Sincronización diaria (ejecutar desde cron a las 22:00)
python orchestrator.py --sincronizar-alm --modo diario

# Sincronización al cerrar el sprint
python orchestrator.py --sincronizar-alm --modo sprint --sprint SPRINT-15

# Dashboard go/no-go para release candidate
python orchestrator.py --dashboard-release --nivel 2 --release v1.0

# Auditoría trimestral del repositorio ALM
python orchestrator.py --auditar-alm
```

La configuración de cron recomendada para el servidor donde corre el pipeline:

```cron
# Sincronización diaria ALM → trazabilidad (22:00 de lunes a viernes)
0 22 * * 1-5 cd /opt/pipeline-ai && python orchestrator.py --sincronizar-alm --modo diario

# Auditoría trimestral (primer lunes de enero, abril, julio y octubre)
0 9 1-7 1,4,7,10 * [ $(date +\%u) = 1 ] && cd /opt/pipeline-ai && python orchestrator.py --auditar-alm
```

---

## Relación entre el Punto A y el Punto B

Para evitar ambigüedades, esta tabla clarifica qué cubre cada punto cuando una pregunta podría pertenecer a ambos:

| Pregunta | Punto A | Punto B |
|---|---|---|
| ¿Cómo se autentica el pipeline con ALM? | ✓ | — |
| ¿Cómo se crean los TCs en ALM? | ✓ | — |
| ¿Cómo se estructura la jerarquía de Subject? | ✓ (decisión de diseño) | — |
| ¿Quién puede mover un TC de Design a Ready? | — | ✓ |
| ¿Cómo se crean los Test Sets de sprint? | — | ✓ |
| ¿Qué pasa cuando un TC falla en ejecución? | — | ✓ |
| ¿Cómo se sincronizan los resultados con el grafo? | ✓ (sincronizador técnico) | ✓ (orquestación y cadencia) |
| ¿Cuándo se autoriza una release? | — | ✓ |
| ¿Cómo se detectan TCs obsoletos? | ✓ (detección de impacto del Punto A) | ✓ (auditoría periódica) |
| ¿Qué campos personalizados crear en ALM? | ✓ | — |
| ¿Cómo se gestiona un cambio en un criterio AC? | ✓ (re-push técnico) | ✓ (proceso de gobierno) |

---

*Punto B desarrollado como parte del Modelo Operativo — Análisis Funcional AI-Ready.*
*Referencia cruzada: Punto A (Integración técnica con HPQC/ALM), Punto 8 (Detección de impacto de cambios), Punto 9 (Grafo de trazabilidad), Punto 12 (Gobierno del modelo).*
