# Few-shot learning con artefactos históricos propios

## Por qué este punto cambia la naturaleza del pipeline

Existe una diferencia cualitativa entre un pipeline que genera artefactos correctos y uno que genera artefactos que el equipo reconoce como suyos. El primero es útil. El segundo se adopta sin resistencia.

Los prompts de los puntos 4 y 5 producen historias y test cases con la estructura correcta, el vocabulario del glosario y los criterios verificables que exige el modelo. Lo que no producen de forma natural es el **estilo propio del equipo**: el nivel de detalle concreto que usa este analista, el tono de las notas técnicas de esta organización, la forma en que este equipo formula los flujos de error, la granularidad de las tareas que este Tech Lead considera razonable.

Esa distancia entre "correcto" y "nuestro" es la que genera las ediciones en la cola de aprobación del paso 8. Y son esas ediciones las que, acumuladas, producen la fricción que ralentiza la adopción.

El few-shot learning con artefactos históricos resuelve ese gap sin modificar los prompts base ni reentrenar ningún modelo. Consiste en seleccionar los mejores artefactos que el equipo ya ha producido y aprobado, convertirlos en ejemplos de referencia, e inyectarlos en cada llamada al pipeline para que el LLM aprenda por analogía qué significa "bien escrito" en este contexto específico.

---

## Principios del enfoque

**El historial es el mejor formador.** Ningún prompt engineer externo puede capturar mejor el estilo del equipo que los propios artefactos que ese equipo ha aprobado y llevado a producción con éxito. Cada historia validada es un caso de referencia implícito de lo que "funciona" en esta organización.

**La calidad de los ejemplos importa más que la cantidad.** Diez artefactos excelentes como referencia producen mejor output que cien artefactos mediocres. El objetivo no es maximizar el número de ejemplos sino maximizar su calidad representativa.

**Los ejemplos deben cubrir la variedad del dominio.** Un único ejemplo de requisito de filtrado no prepara al pipeline para requisitos de integración, de migración o de configuración. El conjunto de referencia debe representar los tipos de requisito más frecuentes del proyecto.

**El few-shot no reemplaza el glosario ni los prompts base: los complementa.** La jerarquía es: glosario (vocabulario), prompts (estructura), ejemplos (estilo y granularidad). Los tres capas trabajan juntas.

---

## Qué son los artefactos de referencia y cómo se seleccionan

Un artefacto de referencia es cualquier artefacto generado por el pipeline o creado manualmente que ha pasado por los siguientes filtros:

Primero, fue aprobado por el analista en la cola de aprobación del paso 8 **sin ediciones** o con ediciones mínimas (menos de dos campos modificados). Esto indica que el output del pipeline ya estaba alineado con las expectativas del equipo.

Segundo, la historia fue implementada y los test cases pasaron en el primer ciclo de QA sin ambigüedades funcionales. Esto valida que la historia no solo era estilísticamente correcta sino funcionalmente precisa.

Tercero, el requisito origen tiene un score de calidad del validador superior a 80. Esto garantiza que el ejemplo de referencia parte de una base de requisito bien definida, no de una historia generada a partir de un requisito ambiguo que por casualidad salió bien.

### Proceso de selección

La selección de artefactos de referencia no es automática: requiere una decisión humana. El proceso recomendado se ejecuta cada dos sprints y sigue estos pasos.

El champion extrae del grafo de trazabilidad del punto 9 todos los artefactos con los tres criterios anteriores. Normalmente son entre el 15% y el 25% del total de historias generadas en el período.

De esa lista, el champion y el analista líder seleccionan entre tres y cinco artefactos por cada categoría funcional del proyecto. Las categorías típicas son: requisito de consulta y filtrado, requisito de creación o modificación de entidad, requisito de integración con sistema externo, requisito con reglas de negocio complejas, y requisito de exportación o reporting.

Cada artefacto seleccionado se etiqueta en el repositorio con la etiqueta `referencia: true` en su YAML y se añade al catálogo de ejemplos. Este catálogo es el insumo del sistema de few-shot.

---

## Estructura del catálogo de ejemplos

El catálogo no es un documento estático. Es un conjunto de archivos YAML versionados en Git, organizados por categoría funcional, que el pipeline consulta en el paso 3 (recuperación de contexto RAG) junto con el contexto histórico del repositorio.

```
pipeline-ai/
└── ejemplos-referencia/
    ├── catalogo.yaml                    # Índice del catálogo con metadatos
    ├── consulta-filtrado/
    │   ├── EJ-001.yaml                  # Historia completa + requisito origen
    │   ├── EJ-002.yaml
    │   └── EJ-003.yaml
    ├── creacion-modificacion/
    │   ├── EJ-004.yaml
    │   └── EJ-005.yaml
    ├── integracion-externa/
    │   ├── EJ-006.yaml
    │   └── EJ-007.yaml
    ├── reglas-negocio-complejas/
    │   └── EJ-008.yaml
    └── exportacion-reporting/
        ├── EJ-009.yaml
        └── EJ-010.yaml
```

### Estructura de un ejemplo de referencia

Cada ejemplo incluye los tres artefactos vinculados para que el LLM vea la cadena completa: del requisito a la historia, y de la historia a los criterios de aceptación. Los test cases son opcionales como parte del ejemplo, pero mejoran la calidad de los test cases generados cuando se incluyen.

```yaml
# ejemplos-referencia/consulta-filtrado/EJ-001.yaml

metadatos:
  id: EJ-001
  categoria: consulta-filtrado
  fecha_seleccion: "2025-04-15"
  seleccionado_por: "Carlos Ruiz (champion)"
  motivo_seleccion: >
    Historia aprobada sin ediciones. Test cases pasaron en primer ciclo.
    Representa bien el patrón de filtrado con validación de rangos
    y estado vacío informativo.
  metricas:
    score_requisito_origen: 88
    story_points_real: 5
    sprints_sin_reabrir: 2
    ediciones_en_aprobacion: 0

requisito_origen:
  id: REQ-023
  titulo: "Filtrar facturas por rango de fechas"
  actor: "Gestor de facturación"
  descripcion: >
    El gestor de facturación necesita filtrar el listado de facturas
    por un rango de fechas para agilizar la búsqueda y exportación
    en el cierre mensual.
  evento_disparador: "Acceso al módulo de Facturas para cierre mensual"
  reglas_negocio:
    - "Solo facturas del ejercicio fiscal en curso"
    - "Rango máximo permitido: 365 días"
  datos_entrada:
    - nombre: fecha_inicio
      tipo: date
      requerido: true
      formato: ISO-8601
    - nombre: fecha_fin
      tipo: date
      requerido: true
      formato: ISO-8601
  datos_salida:
    tipo: lista_paginada
    max_registros: 100
    orden_defecto: "fecha_factura DESC"
  excepciones:
    - condicion: "Rango superior a 365 días"
      comportamiento: "Mensaje de validación. No ejecutar consulta."
    - condicion: "Sin resultados en el período"
      comportamiento: "Estado vacío con mensaje informativo y botón de ampliar búsqueda"

historia_generada:
  summary: >
    Como gestor de facturación, quiero filtrar el listado de facturas
    por rango de fechas para localizar rápidamente documentos
    de un período contable concreto
  descripcion:
    contexto: >
      El gestor dedica actualmente entre 15 y 30 minutos al cierre
      mensual buscando facturas manualmente. Un filtro por rango de
      fechas elimina esta fricción y permite preparar la conciliación
      en menos de 2 minutos.
    notas_importantes:
      - "Rango máximo: 365 días por restricción de rendimiento documentada en RG-BD-04"
      - "Solo facturas del ejercicio fiscal en curso. Históricos anteriores en módulo Archivo."
    flujo_principal:
      - "1. El gestor accede al módulo Facturas"
      - "2. Introduce fecha_inicio y fecha_fin en el panel de filtros"
      - "3. Pulsa Buscar"
      - "4. El sistema devuelve el listado paginado ordenado por fecha descendente"
      - "5. El gestor visualiza el listado con el contador de resultados"
    flujos_error:
      - condicion: "Rango superior a 365 días"
        comportamiento: >
          El sistema no ejecuta la consulta. Campos de fecha resaltados
          en rojo. Mensaje: 'El rango no puede superar 365 días'.
      - condicion: "Sin resultados en el período"
        comportamiento: >
          Estado vacío con mensaje 'No se encontraron facturas para
          el período seleccionado' y botón 'Ampliar búsqueda'.
  criterios_aceptacion:
    - id: AC-023-01
      titulo: "Filtrado válido devuelve resultados ordenados en tiempo"
      dado: "El gestor está autenticado con rol gestor_facturacion y accede al módulo Facturas"
      cuando: "Introduce fecha_inicio=2024-01-01 y fecha_fin=2024-03-31 y pulsa Buscar"
      entonces: >
        El sistema devuelve las facturas del período en menos de 2 segundos,
        ordenadas por fecha descendente, mostrando el contador de resultados.
      tipo: positivo
      datos_ejemplo:
        fecha_inicio: "2024-01-01"
        fecha_fin: "2024-03-31"
        resultado_esperado: "Lista paginada, orden descendente, contador visible"
    - id: AC-023-02
      titulo: "Rango superior a 365 días bloquea la búsqueda"
      dado: "El gestor selecciona un rango de fechas superior a 365 días"
      cuando: "Pulsa Buscar"
      entonces: >
        El sistema no ejecuta ninguna consulta. Los campos fecha_inicio
        y fecha_fin se resaltan en rojo. Aparece el mensaje exacto:
        'El rango no puede superar 365 días'.
      tipo: negativo
      datos_ejemplo:
        fecha_inicio: "2023-01-01"
        fecha_fin: "2024-01-02"
        dias_diferencia: 366
    - id: AC-023-03
      titulo: "Sin resultados muestra estado vacío con acción de recuperación"
      dado: "El gestor ejecuta una búsqueda válida sin facturas en el período"
      cuando: "El sistema procesa la consulta"
      entonces: >
        Se muestra el estado vacío con el texto 'No se encontraron facturas
        para el período seleccionado' y el botón 'Ampliar búsqueda' visible.
      tipo: positivo
      datos_ejemplo:
        fecha_inicio: "2000-01-01"
        fecha_fin: "2000-01-31"
  story_points: 5
  priority: "Highest"
  labels: ["facturacion", "filtrado", "fase-1"]
  components: ["modulo-facturacion"]
  definition_of_done:
    - "Todos los criterios de aceptación superan pruebas de regresión"
    - "Rendimiento validado con dataset de 10.000 registros en staging"
    - "Revisión de accesibilidad WCAG 2.1 AA completada"

tareas_generadas:
  - summary: "Crear índice de rendimiento en tabla facturas para filtrado por fecha"
    capa: base_datos
    estimacion_horas: 3
    criterio_calidad: "Consulta < 200ms p95 con 10.000 registros en staging"
  - summary: "Implementar endpoint REST de filtrado de facturas por rango de fechas"
    capa: backend
    estimacion_horas: 6
    criterio_calidad: "Tests unitarios ≥80% cobertura en lógica de validación"
  - summary: "Implementar componente de filtrado por fechas en módulo Facturas"
    capa: frontend
    estimacion_horas: 8
    criterio_calidad: "Accesibilidad WCAG 2.1 AA. Tests de componente con React Testing Library."
  - summary: "Ejecutar pruebas de integración y rendimiento del filtrado"
    capa: testing
    estimacion_horas: 4
    criterio_calidad: "Todos los AC documentados en Xray con resultado PASS"
```

### El catálogo como índice de recuperación

El archivo `catalogo.yaml` funciona como índice del conjunto de ejemplos. El pipeline lo consulta en el paso 3 para seleccionar los ejemplos más relevantes para el requisito en proceso sin cargar todos los ejemplos a la vez.

```yaml
# ejemplos-referencia/catalogo.yaml

version: "1.3"
propietario: "Carlos Ruiz (champion)"
fecha_ultima_actualizacion: "2025-05-08"
total_ejemplos: 10

categorias:
  consulta-filtrado:
    descripcion: >
      Requisitos que permiten al actor buscar o filtrar registros
      aplicando criterios estructurados sobre atributos de una entidad.
    patrones_cubiertos:
      - "Filtrado por rango (fechas, importes, cantidades)"
      - "Filtrado por enumerado (estado, categoría, tipo)"
      - "Combinación de criterios con AND implícito"
    ejemplos: [EJ-001, EJ-002, EJ-003]
    palabras_clave: ["filtrar", "buscar", "consultar", "listar", "ordenar", "paginar"]

  creacion-modificacion:
    descripcion: >
      Requisitos que permiten al actor crear nuevos registros o modificar
      el estado o los atributos de registros existentes.
    patrones_cubiertos:
      - "Creación con validación de campos obligatorios"
      - "Edición con historial de cambios"
      - "Cambio de estado con regla de transición"
    ejemplos: [EJ-004, EJ-005]
    palabras_clave: ["crear", "registrar", "editar", "modificar", "actualizar", "cambiar"]

  integracion-externa:
    descripcion: >
      Requisitos que implican comunicación con sistemas externos
      a través de API, EDI, fichero o evento.
    patrones_cubiertos:
      - "Integración síncrona REST con manejo de error y timeout"
      - "Integración asíncrona por evento con retry"
    ejemplos: [EJ-006, EJ-007]
    palabras_clave: ["integrar", "sincronizar", "enviar", "recibir", "importar", "exportar a"]

  reglas-negocio-complejas:
    descripcion: >
      Requisitos con cálculos, condiciones múltiples o reglas
      que requieren Specification by Example para ser verificables.
    patrones_cubiertos:
      - "Regla de aprobación con umbral variable"
      - "Cálculo con múltiples parámetros de entrada"
    ejemplos: [EJ-008]
    palabras_clave: ["calcular", "aprobar", "validar", "aplicar regla", "comisión", "límite"]

  exportacion-reporting:
    descripcion: >
      Requisitos que permiten al actor obtener datos del sistema
      en formato descargable o en una vista agregada.
    patrones_cubiertos:
      - "Exportación de listado filtrado a CSV/XLSX"
      - "Generación de informe con agregaciones"
    ejemplos: [EJ-009, EJ-010]
    palabras_clave: ["exportar", "descargar", "generar informe", "reporte", "resumen"]
```

---

## Cómo se inyectan los ejemplos en el pipeline

La inyección no es una simple concatenación de ejemplos al principio del prompt. Eso desperdiciaría tokens y diluyiría la atención del modelo. La estrategia es una **inyección selectiva y comprimida** que sigue tres principios.

### Principio 1: selección por similitud semántica

En el paso 3 del orquestador, junto con la recuperación de contexto RAG del repositorio de requisitos, el sistema selecciona el ejemplo de referencia más similar al requisito en proceso. La consulta al catálogo usa embeddings, igual que el RAG principal.

```python
class SelectorEjemplosReferencia:
    """
    Selecciona los ejemplos del catálogo más relevantes para
    el requisito en proceso usando similitud semántica.
    """

    def __init__(self, repositorio_rag, catalogo_path: str):
        self.rag = repositorio_rag
        self.catalogo_path = catalogo_path

    def seleccionar(
        self,
        requisito: dict,
        max_ejemplos: int = 2
    ) -> list[dict]:
        """
        Selecciona los N ejemplos más similares al requisito dado.
        Retorna los ejemplos completos listos para inyectar en el prompt.
        """
        # Construir query desde el requisito en proceso
        query = (
            f"{requisito.get('titulo', '')}. "
            f"{requisito.get('descripcion', '')}. "
            f"Actor: {requisito.get('actor', '')}. "
            f"Evento: {requisito.get('evento_disparador', '')}"
        )

        # Buscar en el índice de ejemplos (indexados en el mismo vector store
        # que los requisitos, con metadatos tipo="ejemplo_referencia")
        resultados = self.rag.buscar_por_similitud(
            query_texto=query,
            filtros={"tipo": "ejemplo_referencia"},
            top_k=max_ejemplos * 2  # Recuperar el doble para filtrar después
        )

        # Filtrar por umbral mínimo de similitud
        # Un ejemplo con baja similitud puede confundir más que ayudar
        UMBRAL_MINIMO = 0.72
        relevantes = [
            r for r in resultados if r.similitud >= UMBRAL_MINIMO
        ]

        # Cargar los ejemplos completos desde disco
        ejemplos = []
        vistos = set()
        for resultado in relevantes[:max_ejemplos]:
            ejemplo_id = resultado.metadatos.get("ejemplo_id")
            if ejemplo_id and ejemplo_id not in vistos:
                ejemplo = self._cargar_ejemplo(ejemplo_id)
                if ejemplo:
                    ejemplos.append({
                        "ejemplo": ejemplo,
                        "similitud": resultado.similitud,
                        "categoria": resultado.metadatos.get("categoria")
                    })
                    vistos.add(ejemplo_id)

        return ejemplos

    def _cargar_ejemplo(self, ejemplo_id: str) -> dict | None:
        """Carga el YAML completo de un ejemplo desde disco."""
        import yaml
        import os

        for root, _, files in os.walk(self.catalogo_path):
            for archivo in files:
                if archivo.startswith(ejemplo_id) and archivo.endswith(".yaml"):
                    with open(os.path.join(root, archivo)) as f:
                        return yaml.safe_load(f)
        return None
```

### Principio 2: compresión inteligente del ejemplo

Un ejemplo de referencia completo puede ocupar entre 1.500 y 3.000 tokens. Inyectar dos ejemplos completos consume entre el 30% y el 60% de la ventana de contexto antes de incluir el requisito actual. La solución es comprimir el ejemplo conservando solo las partes que el LLM realmente necesita para aprender el estilo.

```python
def comprimir_ejemplo_para_prompt(ejemplo: dict) -> str:
    """
    Comprime un ejemplo de referencia al formato mínimo que el LLM
    necesita para aprender el estilo sin desperdiciar tokens.

    La compresión conserva:
    - El resumen de la historia (patrón de narrativa)
    - Un criterio AC positivo completo (patrón Dado/Cuando/Entonces)
    - Un criterio AC negativo completo (patrón de flujo de error)
    - Los títulos de las tareas (patrón de descomposición técnica)
    - Los story points y la estimación de horas por capa

    Elimina:
    - El requisito origen completo (el LLM ya lo tiene en el prompt principal)
    - Los metadatos del ejemplo (fechas, motivo de selección, etc.)
    - Los criterios AC adicionales después del primero positivo y negativo
    - El bloque definition_of_done (el LLM usa la plantilla base)
    """
    h = ejemplo.get("historia_generada", {})
    acs = h.get("criterios_aceptacion", [])
    tareas = ejemplo.get("tareas_generadas", [])

    # Seleccionar un AC positivo y uno negativo como muestra
    ac_positivo = next(
        (ac for ac in acs if ac.get("tipo") == "positivo"), None
    )
    ac_negativo = next(
        (ac for ac in acs if ac.get("tipo") == "negativo"), None
    )

    # Construir el bloque comprimido
    lineas = ["── EJEMPLO DE REFERENCIA ──────────────────────────"]

    # Narrativa de la historia
    lineas.append(f"HISTORIA: {h.get('summary', '')}")
    if h.get("descripcion", {}).get("contexto"):
        ctx = h["descripcion"]["contexto"][:200]
        lineas.append(f"CONTEXTO: {ctx}...")

    # Notas importantes (patrón de restricciones)
    notas = h.get("descripcion", {}).get("notas_importantes", [])
    if notas:
        lineas.append("NOTAS: " + " | ".join(notas[:2]))

    # Un criterio positivo completo
    if ac_positivo:
        lineas.append(f"\nCRITERIO POSITIVO ({ac_positivo['id']}):")
        lineas.append(f"  Dado:    {ac_positivo['dado']}")
        lineas.append(f"  Cuando:  {ac_positivo['cuando']}")
        lineas.append(f"  Entonces:{ac_positivo['entonces'][:200]}")
        if ac_positivo.get("datos_ejemplo"):
            datos = str(ac_positivo["datos_ejemplo"])[:100]
            lineas.append(f"  Datos:   {datos}")

    # Un criterio negativo completo
    if ac_negativo:
        lineas.append(f"\nCRITERIO NEGATIVO ({ac_negativo['id']}):")
        lineas.append(f"  Dado:    {ac_negativo['dado']}")
        lineas.append(f"  Cuando:  {ac_negativo['cuando']}")
        lineas.append(f"  Entonces:{ac_negativo['entonces'][:200]}")

    # Patrón de descomposición técnica
    if tareas:
        lineas.append("\nPATRÓN DE TAREAS:")
        for t in tareas:
            lineas.append(
                f"  [{t.get('capa', '?').upper():10}] "
                f"{t.get('summary', '')[:60]} "
                f"({t.get('estimacion_horas', '?')}h)"
            )

    # Story points de referencia
    lineas.append(f"\nSTORY POINTS APROBADOS: {h.get('story_points', '?')}")
    lineas.append("────────────────────────────────────────────────────")

    return "\n".join(lineas)
```

### Principio 3: posicionamiento correcto en el prompt

Los ejemplos se inyectan en el prompt del paso 4 (generación de artefactos) en una posición específica: después del glosario y el contexto RAG, pero antes del requisito actual. Este orden no es arbitrario: el LLM lee el prompt de forma secuencial y los ejemplos funcionan como calibradores del nivel de detalle esperado antes de enfrentarse al caso concreto.

El fragmento relevante del Prompt 2 del punto 4, con la sección de ejemplos integrada:

```
Eres un analista funcional senior especializado en metodologías Agile.
[... system prompt base del punto 4 ...]

GLOSARIO APLICABLE:
[... glosario compacto del punto 2 ...]

CONTEXTO DEL REPOSITORIO (requisitos relacionados):
[... contexto RAG del punto 7 ...]

{{#if ejemplos_referencia}}
EJEMPLOS DE REFERENCIA DE ESTE EQUIPO
Los siguientes ejemplos son historias que este equipo ya ha producido,
aprobado sin ediciones y llevado a producción con éxito. Úsalos como
referencia de nivel de detalle, estilo y granularidad esperados.
NO copies su contenido: aprende el patrón y aplícalo al nuevo requisito.

{{#each ejemplos_referencia}}
{{comprimir_ejemplo_para_prompt this}}
{{/each}}
{{/if}}

REQUISITO A TRANSFORMAR EN HISTORIA:
{{requisito_yaml}}

Genera el JSON de la historia siguiendo exactamente el mismo nivel
de detalle que los ejemplos de referencia, adaptado al contenido
del nuevo requisito.
```

---

## Cómo se indexan los ejemplos en el vector store

Los ejemplos de referencia se indexan en el mismo vector store del RAG del punto 7, con metadatos específicos que los distinguen de los requisitos ordinarios. Esto permite que el selector de ejemplos y el motor de contexto RAG usen la misma infraestructura sin duplicarla.

```python
def indexar_ejemplo_referencia(
    ejemplo: dict,
    repositorio_rag
) -> bool:
    """
    Indexa un ejemplo de referencia en el vector store
    con los metadatos necesarios para su recuperación selectiva.
    """
    ejemplo_id = ejemplo["metadatos"]["id"]
    categoria = ejemplo["metadatos"]["categoria"]
    h = ejemplo.get("historia_generada", {})

    # Construir el texto a embeddar: la parte más representativa
    # del ejemplo para la búsqueda por similitud
    texto_indice = f"""
    Ejemplo de referencia: {ejemplo_id}
    Categoría: {categoria}
    Historia: {h.get('summary', '')}
    Contexto: {h.get('descripcion', {}).get('contexto', '')[:300]}
    Actor: {ejemplo.get('requisito_origen', {}).get('actor', '')}
    Evento: {ejemplo.get('requisito_origen', {}).get('evento_disparador', '')}
    Palabras clave del catálogo: {' '.join(
        _obtener_palabras_clave(categoria)
    )}
    """.strip()

    chunk = Chunk(
        id=f"EJEMPLO::{ejemplo_id}",
        texto=texto_indice,
        tipo="ejemplo_referencia",
        metadatos={
            "tipo": "ejemplo_referencia",
            "ejemplo_id": ejemplo_id,
            "categoria": categoria,
            "score_requisito_origen": ejemplo["metadatos"].get(
                "metricas", {}
            ).get("score_requisito_origen", 0),
            "story_points": h.get("story_points"),
            "n_criterios_ac": len(h.get("criterios_aceptacion", [])),
            "n_tareas": len(ejemplo.get("tareas_generadas", []))
        }
    )

    return repositorio_rag.indexar_chunk(chunk)


def _obtener_palabras_clave(categoria: str) -> list[str]:
    """Recupera las palabras clave de la categoría desde el catálogo."""
    mapa = {
        "consulta-filtrado": ["filtrar", "buscar", "consultar", "listar", "ordenar", "paginar"],
        "creacion-modificacion": ["crear", "registrar", "editar", "modificar", "actualizar"],
        "integracion-externa": ["integrar", "sincronizar", "enviar", "recibir", "importar"],
        "reglas-negocio-complejas": ["calcular", "aprobar", "validar", "aplicar regla"],
        "exportacion-reporting": ["exportar", "descargar", "generar informe", "reporte"]
    }
    return mapa.get(categoria, [])
```

---

## Cuándo los ejemplos mejoran el output y cuándo no ayudan

El few-shot no funciona igual en todos los escenarios. Conocer los límites del enfoque evita sobreestimar su impacto y permite concentrar el esfuerzo donde realmente importa.

**Escenarios donde el few-shot aporta más valor:**

Los requisitos de un tipo que el equipo ya ha implementado en sprints anteriores se benefician enormemente. El LLM tiene un patrón concreto de cómo este equipo descompone ese tipo de funcionalidad, qué nivel de detalle usa en los criterios, cómo formula las notas técnicas.

Los requisitos de un módulo maduro donde el vocabulario, los actores y las reglas de negocio están bien establecidos en el glosario. En ese contexto, el ejemplo añade la dimensión estilística que el glosario no cubre.

Los primeros meses de adopción del pipeline, cuando la tasa de aprobación directa está por debajo del 80% y las ediciones del analista son frecuentes. Los ejemplos aceleran la calibración del sistema sin necesidad de modificar los prompts base.

**Escenarios donde el few-shot aporta poco o puede perjudicar:**

Un requisito de un módulo completamente nuevo para el que no hay ningún ejemplo de referencia con similitud suficiente. En ese caso, inyectar un ejemplo de baja similitud puede llevar al LLM a aplicar patrones incorrectos. El umbral mínimo de similitud de 0,72 en el selector protege contra esto, pero el champion debe verificar que el catálogo tenga cobertura del nuevo módulo antes de procesarlo en batch.

Un requisito que es deliberadamente diferente en estructura a todo lo anterior: un spike técnico disfrazado de historia, un requisito de configuración sin actor humano, un requisito de SLA puro. Estos casos requieren una variante de prompt especializada, no ejemplos del catálogo general.

---

## Proceso de mantenimiento del catálogo

El catálogo se degrada de dos formas. La primera es por envejecimiento: los ejemplos seleccionados en los primeros sprints pueden no representar el estilo actual del equipo si los analistas han evolucionado su forma de escribir. La segunda es por falta de cobertura: a medida que el proyecto añade nuevos módulos, el catálogo queda sin representación de los nuevos tipos de requisito.

El proceso de mantenimiento recomendado tiene tres momentos:

**Cada dos sprints (revisión rápida, 30 minutos):** el champion revisa las métricas de la cola de aprobación. Si un tipo de requisito acumula más de tres ediciones en el mismo campo de forma sistemática, es señal de que el ejemplo de referencia de esa categoría está desactualizado o es insuficiente. Se selecciona un nuevo ejemplo y se añade al catálogo.

**Al inicio de cada nueva épica (revisión de cobertura, 60 minutos):** antes de procesar los primeros requisitos de un módulo nuevo, el champion verifica que existe al menos un ejemplo de referencia con similitud suficiente. Si no existe, se procesan los primeros dos o tres requisitos sin ejemplos, se validan manualmente con especial cuidado, y el mejor resultado se añade al catálogo como primer ejemplo de la nueva categoría.

**Cada trimestre (revisión de calidad, 90 minutos):** el champion y el analista líder revisan todos los ejemplos del catálogo para verificar que siguen siendo representativos del estilo actual del equipo. Los ejemplos cuyo score de similitud con los requisitos recientes haya caído por debajo del umbral se marcan como candidatos a reemplazar.

El gobierno del catálogo sigue el mismo modelo que el gobierno de los prompts del punto 12: cualquier adición o eliminación queda documentada en el changelog del pipeline con el motivo, la fecha y el responsable.

---

## Métricas de efectividad del few-shot

Las métricas que indican si el few-shot está funcionando son distintas de las métricas generales del pipeline. Se miden comparando los runs con ejemplos disponibles contra los runs sin ejemplos disponibles, manteniendo el resto de condiciones constante.

**Tasa de aprobación directa segmentada.** La métrica global del paso 8 se desglosa en: requisitos procesados con al menos un ejemplo de referencia con similitud ≥ 0,72, y requisitos procesados sin ejemplo de referencia disponible. Si el few-shot funciona, la primera tasa debe ser al menos 15 puntos porcentuales superior a la segunda. Una diferencia menor indica que los ejemplos no están siendo efectivos o que el umbral de similitud está mal calibrado.

**Número de ediciones por campo con y sin ejemplo.** El mismo desglose por campo que registra el gestor de estado del punto 12, comparado entre runs con y sin ejemplo. Los campos donde el few-shot no reduce las ediciones son candidatos a revisión del ejemplo de esa categoría.

**Estabilidad del catálogo.** Número de cambios al catálogo por trimestre. Un catálogo que cambia frecuentemente indica que la selección inicial no fue suficientemente representativa. Un catálogo que no cambia nunca indica que no se está revisando.

---

## Relación con el resto del modelo

El few-shot se activa en el paso 3 del orquestador, junto con la recuperación de contexto RAG. Ambos usan la misma infraestructura de vector store del punto 7, pero con propósitos distintos: el RAG aporta **contexto de consistencia** (qué existe ya, qué se ha decidido antes), mientras que el few-shot aporta **contexto de estilo** (cómo lo hace este equipo, a qué nivel de detalle, con qué tono).

En el prompt del paso 4, el orden de inyección refleja esa jerarquía:

```
1. System prompt base        → qué hacer y cómo estructurarlo
2. Glosario                  → con qué vocabulario hacerlo
3. Contexto RAG              → qué existe ya y qué hay que ser consistente con ello
4. Ejemplos de referencia    → a qué nivel de detalle y con qué estilo hacerlo
5. Requisito actual          → qué transformar
```

Cuando el catálogo madura y los ejemplos son suficientemente representativos, la tasa de aprobación directa del paso 8 supera de forma consistente el 90%, que es el objetivo del mes 12 del plan de adopción del punto 11. En ese punto, el few-shot ha absorbido el estilo del equipo de forma suficiente para que el pipeline no necesite ajustes frecuentes de prompts para mantener esa calidad.
