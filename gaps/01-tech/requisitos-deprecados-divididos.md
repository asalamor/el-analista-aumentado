# Manejo de requisitos deprecados o divididos — Split y fusión

> **Módulo complementario del Modelo Operativo AI-Ready**
> Capa: Núcleo técnico del pipeline · Dependencias: Puntos 4, 7, 8, 9

---

## Por qué este módulo merece tratamiento propio

El pipeline descrito en los puntos 4 al 10 asume que un requisito nace, se valida y genera artefactos de forma lineal. Pero en la práctica, los requisitos tienen un ciclo de vida más complejo: se descubren demasiado grandes durante el refinamiento y hay que partirlos, se solapan con otro y hay que fusionarlos, o el negocio cambia de dirección y hay que retirarlos.

Ninguna de estas tres operaciones es trivial en un pipeline AI-ready porque cada una rompe la trazabilidad existente de formas distintas. Un `REQ-023` que se convierte en `REQ-023a` y `REQ-023b` tiene historias Jira que ya existen, test cases indexados en el vector store, aristas en el grafo de trazabilidad y un campo `requisito_origen` en docenas de artefactos. Sin un protocolo explícito, el pipeline genera duplicados, el RAG trabaja con contexto obsoleto y la matriz de trazabilidad queda inconsistente.

Este módulo define los tres patrones de operación y los integra con la arquitectura ya construida.

---

## Taxonomía de operaciones sobre el ciclo de vida del requisito

```
OPERACIONES SOBRE REQUISITOS EXISTENTES
│
├── DEPRECACIÓN
│   └── El requisito se retira del alcance sin sustituto
│       o con sustituto explícito declarado en 'sucesor'
│
├── SPLIT (división)
│   ├── Split simple: REQ-A → REQ-A1 + REQ-A2
│   │   El requisito original es demasiado grande
│   │
│   └── Split con pivot: REQ-A → REQ-B + REQ-C
│       El requisito original cambia completamente de título
│       porque la comprensión del negocio ha evolucionado
│
└── FUSIÓN (merge)
    ├── Fusión directa: REQ-A + REQ-B → REQ-C
    │   Dos requisitos solapados se consolidan en uno
    │
    └── Absorción: REQ-A absorbe REQ-B
        REQ-A se amplía, REQ-B se depreca con sucesor = REQ-A
```

---

## Patrón 1 — Deprecación

### Cuándo aplicar

Un requisito se depreca cuando el negocio decide que la funcionalidad ya no es necesaria, cuando es reemplazado por otro de mayor alcance o cuando el contexto que lo originó ha desaparecido. La deprecación **nunca es una eliminación**: el requisito permanece en el repositorio con estado `deprecado` para mantener la auditoría histórica y la explicabilidad de las decisiones pasadas.

### Campos YAML que cambian

```yaml
# ANTES
id: REQ-023
estado: validado
sucesor: null

# DESPUÉS
id: REQ-023
estado: deprecado
version: "2.0"          # Incremento mayor obligatorio al deprecar
sucesor: REQ-047        # null si se depreca sin sustituto
fecha_depreciacion: "2025-06-10"
motivo_depreciacion: >
  La funcionalidad de filtrado por fechas queda absorbida
  por el nuevo módulo de búsqueda avanzada (REQ-047) que
  cubre este caso con mayor alcance.
```

El campo `motivo_depreciacion` no es opcional. Es el artefacto que permite a cualquier miembro del equipo, seis meses después, entender por qué existe un `REQ-023` con estado `deprecado` en el repositorio.

### Acciones del pipeline de deprecación

**Paso 1 — Detección del cambio de estado.**
El webhook de Confluence o el trigger de Git detecta que el campo `estado` pasa a `deprecado`. Se ejecuta automáticamente el analizador de impacto del punto 8 con el tipo de cambio `D` (el de mayor alcance estructural).

**Paso 2 — Desactivación en el vector store.**
El motor RAG del punto 7 marca como inactivos todos los chunks del requisito deprecado. No se eliminan: se marcan con `activo = FALSE` para que el retrieval no los recupere como contexto futuro, pero queden disponibles para consultas históricas explícitas.

```python
def deprecar_en_rag(requisito_id: str, repositorio: RepositorioRequisitosRAG):
    """
    Desactiva los chunks del requisito en el vector store.
    Los chunks permanecen para trazabilidad histórica pero
    no se recuperan en búsquedas normales de contexto.
    """
    with repositorio.db.cursor() as cur:
        cur.execute("""
            UPDATE chunks_requisitos
            SET activo = FALSE,
                metadatos = metadatos || '{"deprecado": true}'::jsonb
            WHERE metadatos->>'requisito_id' = %s
        """, (requisito_id,))
        repositorio.db.commit()
```

**Paso 3 — Actualización del grafo de trazabilidad.**
En el grafo del punto 9, el nodo del requisito deprecado se marca con `estado = 'deprecado'`. Las aristas existentes se conservan para poder reconstruir la historia completa del artefacto. Si existe un `sucesor`, se crea una arista nueva de tipo `reemplaza` entre el sucesor y el deprecado.

```python
def registrar_depreciacion(
    motor: MotorTrazabilidad,
    requisito_id: str,
    sucesor_id: str | None
):
    # Actualizar estado del nodo
    motor.registrar_nodo(Nodo(
        id=requisito_id,
        tipo="requisito",
        titulo=f"[DEPRECADO] {requisito_id}",
        estado="deprecado"
    ))

    # Registrar relación con el sucesor si existe
    if sucesor_id:
        motor.registrar_arista(Arista(
            origen_id=sucesor_id,
            destino_id=requisito_id,
            tipo_relacion="reemplaza",
            confianza=1.0,
            origen_relacion="operacion_ciclo_vida"
        ))
```

**Paso 4 — Gestión de artefactos Jira activos.**
El pipeline consulta qué historias generadas desde el requisito deprecado están en estado activo en Jira (no en `Done`). Para cada una, añade un comentario automático y una etiqueta `req-deprecado` para que el equipo las identifique en el siguiente refinamiento.

```python
def gestionar_issues_activos_post_depreciacion(
    requisito_id: str,
    sucesor_id: str | None,
    cliente_jira: ClienteJira
):
    # Buscar historias activas del requisito deprecado
    jql = (
        f"project = {cliente_jira.config.project_key} "
        f"AND 'Requisito Origen' ~ '{requisito_id}' "
        f"AND statusCategory != Done"
    )
    issues = cliente_jira.get("search", params={"jql": jql}).get("issues", [])

    for issue in issues:
        key = issue["key"]

        # Añadir etiqueta
        campos_actuales = issue["fields"].get("labels", [])
        cliente_jira.put(f"issue/{key}", {
            "fields": {"labels": campos_actuales + ["req-deprecado"]}
        })

        # Comentario explicativo
        mensaje = (
            f"⚠ El requisito origen *{requisito_id}* ha sido deprecado.\n\n"
            + (
                f"El sucesor es *{sucesor_id}*. Revisar si esta historia "
                f"queda cubierta por los artefactos generados desde el sucesor."
                if sucesor_id else
                "Este requisito ha sido retirado del alcance sin sustituto. "
                "Revisar en el próximo refinamiento si esta historia debe cerrarse."
            )
        )
        cliente_jira.post(f"issue/{key}/comment", {
            "body": {"type": "doc", "version": 1, "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": mensaje}]}
            ]}
        })
```

**Paso 5 — Informe de deprecación para el analista.**

```yaml
# informe_depreciacion_REQ-023.yaml
operacion: depreciacion
requisito_id: REQ-023
sucesor: REQ-047
timestamp: "2025-06-10T10:30:00Z"

artefactos_afectados:
  historias_activas:
    - id: US-047
      jira_key: FACT-47
      estado: "En progreso"
      asignado: "María García"
      accion: "Etiqueta 'req-deprecado' añadida. Requiere decisión en refinamiento."

  test_cases_obsoletos:
    - TC-111
    - TC-112
    - TC-113
    accion: "Marcar como obsoletos en Xray. No eliminar hasta confirmar cobertura en sucesor."

  chunks_desactivados: 5
  aristas_conservadas: 22

proximos_pasos:
  - "Confirmar con el PO que FACT-47 queda cubierta por los artefactos de REQ-047"
  - "Verificar en Xray que los test cases de REQ-047 cubren los AC de REQ-023"
  - "Cerrar FACT-47 si queda sin desarrollo pendiente"
```

---

## Patrón 2 — Split (división)

### Cuándo aplicar

El split es la operación más frecuente en el refinamiento Agile. Un requisito se divide cuando su estimación supera los 8 story points, cuando mezcla dos actores distintos que el pipeline de validación detectó como problema de atomicidad, o cuando el equipo técnico identifica que la implementación puede entregarse en partes independientes con valor incremental para el negocio.

La regla de oro del split: **los requisitos hijos deben ser independientes entre sí y cada uno debe tener valor de negocio por sí solo**. Un split que produce `REQ-023a` (la pantalla) y `REQ-023b` (la lógica de negocio sin pantalla) no es un split correcto: el hijo B no tiene valor de negocio sin el hijo A.

### Tipos de split y cómo abordarlos

**Split por flujos:** El requisito cubre el flujo feliz y el flujo de error como si fueran una sola unidad. Se divide en `REQ-023a` (flujo principal) y `REQ-023b` (gestión de excepciones y errores).

**Split por actor:** El requisito involucra dos actores con permisos distintos que el validador marcó como problema. Se divide en `REQ-023a` (acción del Gestor de facturación) y `REQ-023b` (aprobación del Responsable financiero).

**Split por volumen:** El requisito es correcto funcionalmente pero demasiado grande para un sprint. Se divide por criterios de aceptación: `REQ-023a` contiene los AC de mayor prioridad y `REQ-023b` los de menor prioridad.

**Split por MVP:** El negocio quiere una versión mínima viable para el próximo sprint y una versión completa para más adelante. Se divide en `REQ-023a` (MVP) y `REQ-023b` (evolución).

### Campos YAML del proceso de split

El requisito original pasa a estado `deprecado` con referencia a sus sucesores. Los hijos son requisitos nuevos con referencia al padre en su bloque de origen.

```yaml
# REQ-023.yaml — PADRE (tras el split)
id: REQ-023
estado: deprecado
version: "2.0"
sucesor: null          # null porque tiene múltiples sucesores
sucesores: [REQ-023a, REQ-023b]   # campo específico para split
motivo_depreciacion: >
  Requisito dividido por exceder 8 story points y mezclar el flujo
  de filtrado estándar con la gestión de excepciones de rendimiento.
  Los sucesores cubren el alcance completo del requisito original.
fecha_depreciacion: "2025-06-10"
```

```yaml
# REQ-023a.yaml — HIJO A (flujo principal)
id: REQ-023a
titulo: "Filtrar facturas por rango de fechas — flujo estándar"
version: "1.0"
estado: en-revision
epica: EP-04

origen:
  solicitante: "Ana López - Dirección Financiera"
  area: "Finanzas"
  fecha_solicitud: "2025-06-10"
  referencia: "Derivado de REQ-023 por split en refinamiento sprint 8"

requisito_padre: REQ-023    # campo específico: referencia al origen del split
hermanos: [REQ-023b]        # otros hijos del mismo split

# Hereda del padre solo los campos que aplican a este subconjunto
actor: "Gestor de facturación"
prioridad: must-have

criterios_aceptacion:
  - id: AC-023a-01
    # Hereda AC-023-01 del padre — flujo feliz
    dado: "El gestor está autenticado y accede al módulo Facturas"
    cuando: "Introduce fecha_inicio y fecha_fin válidos y pulsa Buscar"
    entonces: >
      El sistema devuelve facturas del período en menos de 2 segundos,
      ordenadas por fecha descendente, con contador de resultados visible
  - id: AC-023a-02
    # Hereda AC-023-03 del padre — estado vacío
    dado: "El gestor ejecuta una búsqueda válida sin resultados"
    cuando: "El sistema procesa la consulta"
    entonces: >
      Se muestra el estado vacío con el mensaje definido
      y el botón 'Ampliar búsqueda'

trazabilidad:
  requisito_padre: REQ-023
  criterios_heredados: [AC-023-01, AC-023-03]
  historias_generadas: []
  test_cases_generados: []
  jira_issues: []
```

```yaml
# REQ-023b.yaml — HIJO B (validaciones y excepciones)
id: REQ-023b
titulo: "Filtrar facturas por rango de fechas — validaciones y límites"
version: "1.0"
estado: en-revision
epica: EP-04

origen:
  referencia: "Derivado de REQ-023 por split en refinamiento sprint 8"

requisito_padre: REQ-023
hermanos: [REQ-023a]

actor: "Gestor de facturación"
prioridad: should-have   # Menor prioridad que el flujo principal

dependencias:
  requisitos: [REQ-023a]   # B depende de A: necesita la pantalla del flujo principal

criterios_aceptacion:
  - id: AC-023b-01
    # Hereda AC-023-02 del padre — validación de rango
    dado: "El gestor selecciona un rango de fechas superior a 365 días"
    cuando: "Pulsa Buscar"
    entonces: >
      El sistema no ejecuta la consulta, muestra el mensaje
      'El rango no puede superar 365 días' y resalta los campos en rojo
  - id: AC-023b-02
    # AC nuevo: caso de contorno exacto
    dado: "El gestor selecciona un rango de exactamente 365 días"
    cuando: "Pulsa Buscar"
    entonces: "La búsqueda se ejecuta correctamente sin mensaje de error"

trazabilidad:
  requisito_padre: REQ-023
  criterios_heredados: [AC-023-02]
  historias_generadas: []
  test_cases_generados: []
  jira_issues: []
```

### Pipeline de split

La operación de split tiene un flujo propio que el orquestador ejecuta cuando detecta la operación. Se invoca con:

```bash
python orchestrator.py --split REQ-023 --hijos REQ-023a REQ-023b
```

**Paso 1 — Validación de coherencia del split.**
Antes de procesar nada, el pipeline verifica que el split es correcto:

```python
async def validar_coherencia_split(
    requisito_padre: dict,
    hijos: list[dict],
    config: PipelineConfig
) -> dict:
    """
    Verifica que el conjunto de hijos cubre el alcance completo
    del padre sin solaparse entre sí.
    """
    prompt = f"""
Analiza si el siguiente split de requisito es correcto.

REQUISITO PADRE (completo):
{yaml.dump(requisito_padre, allow_unicode=True)}

REQUISITOS HIJOS (deben cubrir el alcance completo del padre):
{yaml.dump(hijos, allow_unicode=True)}

Verifica:
1. COBERTURA COMPLETA: ¿Todos los criterios de aceptación del padre
   están cubiertos por al menos un hijo?
2. SIN SOLAPAMIENTO: ¿Hay criterios duplicados entre hijos que
   generarán test cases redundantes?
3. INDEPENDENCIA: ¿Cada hijo tiene valor de negocio por sí solo
   (excepto dependencias declaradas explícitamente)?
4. ATOMICIDAD: ¿Cada hijo es suficientemente pequeño para
   estimarse en ≤8 story points?

Responde en JSON:
{{
  "cobertura_completa": true/false,
  "criterios_sin_cubrir": ["AC-023-XX"],
  "solapamientos_detectados": [
    {{"hijo_a": "REQ-023a", "hijo_b": "REQ-023b", "criterio": "descripción"}}
  ],
  "hijos_sin_valor_independiente": ["REQ-023b"],
  "hijos_demasiado_grandes": ["REQ-023a"],
  "veredicto": "SPLIT_CORRECTO | SPLIT_CON_ADVERTENCIAS | SPLIT_INCORRECTO",
  "recomendacion": "texto explicativo"
}}
    """
    # ... llamada al LLM ...
```

**Paso 2 — Gestión de artefactos Jira existentes.**
Si el padre ya tenía una historia `FACT-47` generada y en Jira, el pipeline tiene que decidir qué hacer con ella. La política recomendada:

```
HISTORIA JIRA DEL PADRE (estado: To Do o Backlog)
→ Cerrar con resolución "Dividida"
→ Crear dos historias nuevas desde los hijos
→ Crear issue link "is split by" entre padre y hijos

HISTORIA JIRA DEL PADRE (estado: En progreso)
→ NO cerrar automáticamente
→ Notificar al analista y al product owner
→ Crear las historias de los hijos como "To Do"
→ El PO decide si pausar la historia padre o completarla

HISTORIA JIRA DEL PADRE (estado: Done)
→ No tiene sentido hacer el split ahora
→ El pipeline bloquea la operación y solicita confirmación explícita
```

```python
async def gestionar_issues_en_split(
    historia_padre_key: str,
    hijos_yaml: list[dict],
    cliente_jira: ClienteJira,
    config: PipelineConfig
) -> dict:
    """
    Gestiona los issues Jira durante la operación de split.
    """
    # Obtener estado actual de la historia padre
    issue_padre = cliente_jira.get(f"issue/{historia_padre_key}")
    estado_categoria = (
        issue_padre["fields"]["status"]["statusCategory"]["key"]
    )

    if estado_categoria == "done":
        return {
            "bloqueado": True,
            "motivo": (
                f"La historia {historia_padre_key} está en estado Done. "
                "No se puede dividir una historia ya completada. "
                "Si el split es correcto, crea los hijos como requisitos nuevos."
            )
        }

    if estado_categoria == "indeterminate":
        # En progreso: no cerrar automáticamente
        resultado = {
            "historia_padre": historia_padre_key,
            "accion_padre": "mantenida_activa",
            "advertencia": (
                f"La historia {historia_padre_key} está en progreso. "
                "Las historias hijas se crearán en estado To Do. "
                "El PO debe decidir si pausar la historia padre."
            )
        }
    else:
        # To Do / Backlog: cerrar y sustituir
        cliente_jira.put(f"issue/{historia_padre_key}", {
            "fields": {"labels": ["split-origen"]}
        })
        cliente_jira.post(f"issue/{historia_padre_key}/transitions", {
            "transition": {"id": "31"},  # Closed
            "update": {"comment": [{"add": {"body": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [
                    {"type": "text", "text": (
                        f"Historia dividida en los sucesores: "
                        f"{', '.join(h['id'] for h in hijos_yaml)}"
                    )}
                ]}]
            }}}]}
        })
        resultado = {
            "historia_padre": historia_padre_key,
            "accion_padre": "cerrada",
            "historias_hijas": []
        }

    # Generar historias para cada hijo
    for hijo in hijos_yaml:
        historia_hijo = await generar_artefactos_jira(
            requisito=hijo,
            glosario=_cargar_glosario(config),
            contexto_rag={},
            config=config
        )
        resultado.setdefault("historias_hijas", []).append(historia_hijo)

        # Crear issue link entre padre e hijo
        if estado_categoria != "indeterminate":
            cliente_jira.post("issueLink", {
                "type": {"name": "Splits"},
                "inwardIssue": {"key": historia_padre_key},
                "outwardIssue": {"key": historia_hijo.get("jira_key")}
            })

    return resultado
```

**Paso 3 — Actualización del grafo de trazabilidad.**

```python
def registrar_split_en_grafo(
    motor: MotorTrazabilidad,
    padre_id: str,
    hijos_ids: list[str]
):
    """
    Registra la operación de split en el grafo.
    El padre queda como nodo histórico. Los hijos son nodos nuevos
    con aristas 'reemplaza' hacia el padre y 'hermano_de' entre ellos.
    """
    # Marcar el padre como deprecado
    motor.registrar_nodo(Nodo(
        id=padre_id,
        tipo="requisito",
        titulo=f"[SPLIT] {padre_id}",
        estado="deprecado",
        metadatos={"operacion": "split", "sucesores": hijos_ids}
    ))

    # Registrar cada hijo y su relación con el padre
    for hijo_id in hijos_ids:
        motor.registrar_arista(Arista(
            origen_id=hijo_id,
            destino_id=padre_id,
            tipo_relacion="reemplaza",
            confianza=1.0,
            origen_relacion="operacion_split",
            metadatos={"operacion": "split", "padre": padre_id}
        ))

    # Registrar relación entre hermanos
    for i, hijo_a in enumerate(hijos_ids):
        for hijo_b in hijos_ids[i+1:]:
            motor.registrar_arista(Arista(
                origen_id=hijo_a,
                destino_id=hijo_b,
                tipo_relacion="hermano_de",
                confianza=1.0,
                origen_relacion="operacion_split"
            ))
```

**Paso 4 — Re-indexación en el RAG.**
El padre se desactiva en el vector store. Los hijos se indexan como requisitos nuevos. Si el hijo hereda criterios de aceptación del padre, los chunks de esos criterios se re-indexan con el nuevo `requisito_id` del hijo para que el retrieval los recupere correctamente.

**Paso 5 — Gestión de test cases.**
Los test cases del padre que corresponden a criterios heredados por los hijos se reasignan. Los test cases de criterios que no han sido heredados por ningún hijo se marcan como obsoletos.

```python
def reasignar_test_cases_post_split(
    padre_id: str,
    hijos: list[dict],
    motor_traz: MotorTrazabilidad
):
    """
    Reasigna los test cases del padre a los hijos correspondientes
    basándose en los criterios AC heredados declarados en cada hijo.
    """
    for hijo in hijos:
        criterios_heredados = (
            hijo.get("trazabilidad", {})
            .get("criterios_heredados", [])
        )
        for ac_id in criterios_heredados:
            # Buscar test cases asociados a ese criterio en el padre
            tcs_del_criterio = _buscar_tcs_por_criterio(
                ac_id, padre_id, motor_traz
            )
            # Reasignar al hijo
            for tc_id in tcs_del_criterio:
                motor_traz.registrar_arista(Arista(
                    origen_id=tc_id,
                    destino_id=hijo["id"],
                    tipo_relacion="verifica",
                    confianza=1.0,
                    origen_relacion="reasignacion_split"
                ))
```

---

## Patrón 3 — Fusión (merge)

### Cuándo aplicar

La fusión es menos frecuente que el split pero ocurre en tres escenarios reconocibles. El primero es cuando el validador detecta que `REQ-045` y `REQ-046` tienen criterios de aceptación con similitud superior al 90% en el RAG: son el mismo requisito escrito dos veces por dos analistas distintos. El segundo es cuando dos requisitos de distintas épicas se descubren como implementaciones redundantes de la misma capacidad técnica. El tercero es cuando el negocio simplifica su proceso y dos flujos separados se convierten en uno.

La fusión tiene una asimetría importante respecto al split: mientras el split siempre genera requisitos nuevos, la fusión puede hacerse de dos formas. En la **absorción**, uno de los requisitos originales amplía su alcance para incluir el del otro (el absorbido se depreca con `sucesor` apuntando al absorbente). En la **fusión completa**, ambos se deprecan y se crea un tercero que consolida el alcance de ambos.

### Absorción — REQ-A absorbe REQ-B

```yaml
# REQ-045.yaml — ABSORBENTE (se amplía)
id: REQ-045
titulo: "Exportar listado de facturas filtradas"
version: "2.0"         # Incremento mayor: cambio de comportamiento
estado: validado

# Ahora incluye el alcance de REQ-046
alcance_absorbido:
  - requisito_id: REQ-046
    motivo: >
      REQ-046 definía la configuración de formato de exportación como
      un requisito separado, pero el equipo técnico confirmó que ambas
      funcionalidades son inseparables en la implementación.
    fecha_absorcion: "2025-06-10"

criterios_aceptacion:
  # Criterios originales de REQ-045
  - id: AC-045-01
    # ...
  # Criterios incorporados de REQ-046
  - id: AC-045-04   # Renumerado desde AC-046-01
    dado: "El gestor accede a las preferencias de exportación"
    # ...
```

```yaml
# REQ-046.yaml — ABSORBIDO
id: REQ-046
estado: deprecado
version: "2.0"
sucesor: REQ-045
motivo_depreciacion: >
  Funcionalidad absorbida por REQ-045 v2.0. Los criterios de aceptación
  de este requisito han sido incorporados como AC-045-04 a AC-045-06.
fecha_depreciacion: "2025-06-10"
```

### Fusión completa — REQ-A + REQ-B → REQ-C

```yaml
# REQ-045.yaml — FUSIONADO A
id: REQ-045
estado: deprecado
sucesores: [REQ-047]
motivo_depreciacion: "Fusionado con REQ-046 en REQ-047."
fecha_depreciacion: "2025-06-10"

# REQ-046.yaml — FUSIONADO B
id: REQ-046
estado: deprecado
sucesores: [REQ-047]
motivo_depreciacion: "Fusionado con REQ-045 en REQ-047."
fecha_depreciacion: "2025-06-10"

# REQ-047.yaml — RESULTADO DE LA FUSIÓN
id: REQ-047
titulo: "Exportar y configurar formato de facturas filtradas"
version: "1.0"
estado: en-revision

origen:
  referencia: "Fusión de REQ-045 y REQ-046 — refinamiento sprint 9"

requisitos_fusionados: [REQ-045, REQ-046]   # campo específico para fusión

# Consolida criterios de ambos requisitos sin duplicidades
criterios_aceptacion:
  - id: AC-047-01
    origen_padre: AC-045-01
    # ...
  - id: AC-047-02
    origen_padre: AC-046-01
    # ...
```

### Pipeline de fusión

```bash
python orchestrator.py --merge REQ-045 REQ-046 --resultado REQ-047
# o en modo absorción:
python orchestrator.py --absorb REQ-046 --en REQ-045
```

**Validación de coherencia antes de la fusión.**
El pipeline valida que la fusión tiene sentido antes de ejecutarla:

```python
async def validar_coherencia_fusion(
    requisitos_a_fusionar: list[dict],
    resultado: dict,
    config: PipelineConfig
) -> dict:
    """
    Verifica que la fusión es correcta y no genera un requisito
    demasiado grande o con responsabilidades mezcladas.
    """
    # Verificar que el resultado no supera los 13 SP estimados
    # (si supera, debería hacerse un split del resultado primero)

    # Verificar que los criterios del resultado cubren el alcance completo
    # de todos los requisitos fusionados

    # Verificar que no hay solapamiento entre los criterios incorporados
    # (dos criterios del mismo requisito fusionado no deben contradecirse)

    prompt = f"""
Analiza si la siguiente fusión de requisitos es correcta.

REQUISITOS A FUSIONAR:
{yaml.dump(requisitos_a_fusionar, allow_unicode=True)}

REQUISITO RESULTADO:
{yaml.dump(resultado, allow_unicode=True)}

Verifica:
1. COBERTURA: ¿El resultado cubre el 100% del alcance de todos los
   requisitos fusionados?
2. SIN CONTRADICCIONES: ¿Hay reglas de negocio contradictorias entre
   los fusionados que el resultado no resuelve?
3. ATOMICIDAD: ¿El resultado tiene un único actor y un único evento
   disparador claro, o mezcla responsabilidades?
4. TAMAÑO: ¿El resultado puede estimarse en ≤13 story points?

Responde en JSON:
{{
  "cobertura_completa": true/false,
  "criterios_sin_cubrir": [],
  "contradicciones_detectadas": [],
  "mezcla_responsabilidades": true/false,
  "demasiado_grande": true/false,
  "veredicto": "FUSION_CORRECTA | FUSION_CON_ADVERTENCIAS | FUSION_INCORRECTA",
  "recomendacion": "texto"
}}
    """
    # ... llamada al LLM ...
```

**Consolidación de test cases en la fusión.**
Esta es la operación más delicada de la fusión: los test cases de los requisitos fusionados pueden solaparse, contradecirse o necesitar consolidación. El pipeline delega esta decisión al analista porque requiere juicio funcional.

```python
async def consolidar_test_cases_fusion(
    requisitos_fusionados: list[str],
    resultado_id: str,
    motor_rag: MotorConsultaRAG,
    config: PipelineConfig
) -> dict:
    """
    Identifica test cases candidatos a consolidar y genera
    un informe para que el analista tome las decisiones finales.
    """
    # Recuperar todos los test cases de los requisitos fusionados
    tcs_por_requisito = {
        req_id: _obtener_tcs_de_requisito(req_id, motor_rag)
        for req_id in requisitos_fusionados
    }

    # Detectar test cases similares entre requisitos
    similitudes = []
    for req_a, tcs_a in tcs_por_requisito.items():
        for req_b, tcs_b in tcs_por_requisito.items():
            if req_a >= req_b:
                continue
            for tc_a in tcs_a:
                for tc_b in tcs_b:
                    similitud = _calcular_similitud_rag(tc_a, tc_b, motor_rag)
                    if similitud > 0.82:
                        similitudes.append({
                            "tc_a": tc_a["id"],
                            "tc_b": tc_b["id"],
                            "similitud": similitud,
                            "recomendacion": (
                                "consolidar" if similitud > 0.92 else
                                "revisar_manualmente"
                            )
                        })

    return {
        "resultado_id": resultado_id,
        "tcs_por_requisito": {
            req_id: [tc["id"] for tc in tcs]
            for req_id, tcs in tcs_por_requisito.items()
        },
        "posibles_duplicados": similitudes,
        "accion_requerida": (
            "El analista debe revisar los posibles duplicados antes de "
            "ejecutar el pipeline de generación de test cases para el "
            "requisito resultado. Los test cases marcados como 'consolidar' "
            "pueden fusionarse automáticamente. Los marcados como "
            "'revisar_manualmente' requieren decisión humana."
        )
    }
```

---

## Cuadro comparativo de las tres operaciones

| Dimensión | Deprecación | Split | Fusión |
|---|---|---|---|
| **Cuándo ocurre** | El negocio retira funcionalidad | El requisito es demasiado grande | Dos requisitos se solapan |
| **¿Se elimina el original?** | No, estado `deprecado` | No, estado `deprecado` | No, ambos a `deprecado` |
| **¿Se crean nuevos requisitos?** | Solo si hay `sucesor` | Sí, los hijos | Sí, el resultado |
| **¿Se cierran historias Jira?** | Depende del estado | Sí (si `To Do`), no (si `En progreso`) | Depende del estado |
| **¿Se reasignan test cases?** | No, se marcan obsoletos | Sí, a los hijos según AC heredados | Parcial, con revisión humana |
| **¿Se actualiza el RAG?** | Desactivar chunks del original | Desactivar padre, indexar hijos | Desactivar ambos, indexar resultado |
| **¿Requiere aprobación humana?** | Siempre | Siempre, con validación de coherencia | Siempre, con informe de consolidación |
| **Tipo de arista en el grafo** | `reemplaza` (si hay sucesor) | `reemplaza` + `hermano_de` | `reemplaza` (de cada fusionado al resultado) |
| **Nivel de complejidad operacional** | Baja | Media | Alta |

---

## Integración con el orquestador principal

Las tres operaciones se integran como modos de ejecución del `orchestrator.py` ya descrito. El orquestador detecta automáticamente si un requisito está pasando por una operación de ciclo de vida mediante la combinación de cambios en los campos `estado`, `sucesor`, `sucesores` y `requisitos_fusionados`.

```bash
# Deprecación
python orchestrator.py --req REQ-023
# El orquestador detecta estado=deprecado y ejecuta el flujo de deprecación

# Split
python orchestrator.py --split REQ-023 --hijos REQ-023a REQ-023b

# Absorción
python orchestrator.py --absorb REQ-046 --en REQ-045

# Fusión completa
python orchestrator.py --merge REQ-045 REQ-046 --resultado REQ-047
```

El informe generado al final de cualquiera de estas operaciones sigue el mismo formato que el informe de ejecución estándar, con una sección adicional `operacion_ciclo_vida` que documenta exactamente qué cambió, en qué artefactos y qué acciones requieren intervención humana posterior.

---

## Checklist del analista para cada operación

### Antes de deprecar

```
□ ¿El campo 'motivo_depreciacion' tiene al menos 20 palabras?
□ ¿Existe un 'sucesor' o se confirma explícitamente que no hay sustituto?
□ ¿Se ha notificado al product owner antes de ejecutar la operación?
□ ¿Se ha verificado si la historia Jira está en progreso o en el sprint activo?
```

### Antes de hacer split

```
□ ¿Cada hijo tiene valor de negocio independiente?
□ ¿Los criterios del padre están repartidos sin solapamiento entre los hijos?
□ ¿Las dependencias entre hijos están declaradas explícitamente?
□ ¿La suma de story points estimados de los hijos es razonable respecto al padre?
□ ¿La validación de coherencia del pipeline ha dado veredicto SPLIT_CORRECTO?
```

### Antes de fusionar

```
□ ¿El resultado cubre el 100% del alcance de todos los fusionados?
□ ¿Se han revisado los test cases candidatos a consolidar?
□ ¿El resultado tiene un único actor principal y un único evento disparador?
□ ¿Se puede estimar el resultado en ≤13 story points?
□ ¿La validación de coherencia ha dado veredicto FUSION_CORRECTA o CON_ADVERTENCIAS resueltas?
```

---

## Gestión del glosario en operaciones de ciclo de vida

Las operaciones de ciclo de vida tienen un efecto colateral sobre el glosario que a menudo se ignora: cuando un requisito padre define una entidad o un actor que solo existía en ese requisito, la deprecación del padre puede dejar esa definición huérfana en el glosario. Por eso, el pipeline de deprecación incluye una verificación adicional:

```python
def verificar_huerfanos_glosario(
    requisito_id: str,
    glosario: dict,
    repositorio: RepositorioRequisitosRAG
) -> list[dict]:
    """
    Detecta términos del glosario que solo son referenciados
    por el requisito que se va a deprecar. Estos términos
    pueden necesitar revisión o eliminación del glosario.
    """
    terminos_del_req = _extraer_terminos_usados(requisito_id, repositorio)
    huerfanos = []

    for termino in terminos_del_req:
        # Buscar otros requisitos activos que usen este término
        otros_usuarios = repositorio.buscar_por_similitud(
            query_texto=termino,
            filtros={"estado": "validado"},
            top_k=3
        )
        if not otros_usuarios:
            huerfanos.append({
                "termino": termino,
                "accion_recomendada": (
                    "Revisar si el término debe eliminarse del glosario "
                    "o si debe mantenerse como referencia histórica."
                )
            })

    return huerfanos
```

---

## Métricas de calidad de las operaciones de ciclo de vida

El sistema de gobierno del punto 12 incorpora métricas específicas para estas operaciones que permiten detectar patrones problemáticos:

**Tasa de split en refinamiento.** Un porcentaje elevado de requisitos que se dividen en el refinamiento (>20%) indica que el proceso de definición funcional no está siendo suficientemente granular. Es una señal de que los workshops de Event Storming no están produciendo unidades atómicas correctas.

**Tiempo entre creación y deprecación.** Un requisito que se depreca en menos de dos semanas desde su creación indica que el proceso de validación con el negocio no está funcionando correctamente: el requisito llega al pipeline sin estar realmente validado con los stakeholders correctos.

**Ratio de fusiones.** Un número elevado de fusiones (>5% del total de requisitos) señala problemas en el proceso de captura: distintos analistas están documentando el mismo requisito de formas independientes, lo que apunta a falta de coordinación o a un repositorio que no se consulta antes de crear requisitos nuevos.

**Cobertura de test cases tras el split.** Si tras un split la cobertura de test cases de los hijos es inferior a la del padre, el pipeline lo registra como una advertencia. El split no debe reducir la cobertura de pruebas.

---

> **Nota de implementación:** Este módulo se activa en la Fase 2 del roadmap de implantación (semi-automatización), una vez que el equipo tiene experiencia con el pipeline de generación estándar. Introducirlo antes añade complejidad operacional sin que el equipo tenga aún el contexto suficiente para gestionar las decisiones de coherencia que estas operaciones requieren.
