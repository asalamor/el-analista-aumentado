# Detección automática de requisitos candidatos a épica nueva

## El problema que resuelve

En el flujo normal del pipeline, cada requisito declara explícitamente su épica en el campo `epica: EP-NN`. Esa declaración la hace el analista durante o después del taller de Event Storming, cuando el mapa de eventos ya ha producido una propuesta de agrupación por módulos funcionales. En ese momento el sistema de épicas está bien definido y la asignación es directa.

El problema aparece cuando el proyecto evoluciona. A medida que el backlog crece, los usuarios de negocio plantean necesidades que no encajan bien en ninguna épica existente. Algunas veces el analista lo detecta en el momento y abre la conversación con el product owner. Muchas otras veces, bajo presión de tiempo, el analista asigna el requisito a la épica que más se parece, aunque el encaje sea forzado. Ese requisito mal clasificado produce historias vinculadas a la épica incorrecta en Jira, test cases agrupados con funcionalidad no relacionada, y una matriz de trazabilidad que se vuelve difícil de leer conforme acumulan más casos similares.

El sistema de detección automática actúa antes de que ese error se consolide. Analiza el requisito en borrador antes de que entre al pipeline de generación, lo compara semánticamente con las épicas existentes y, si la similitud con todas ellas está por debajo de un umbral, lanza una alerta que sugiere que puede estar naciendo un módulo funcional nuevo.

---

## Cuándo se activa la detección

La detección no se ejecuta en cada llamada al pipeline. Se activa en tres momentos específicos donde la señal es más fiable y la intervención más oportuna.

**Al cambiar el estado del requisito de `borrador` a `en-revision`.** Este es el momento más valioso: el analista ha terminado de escribir el requisito pero todavía no ha comprometido la asignación de épica ante el equipo. Una alerta en este punto cuesta menos de corregir que cualquier momento posterior.

**En el procesamiento batch de una épica completa.** Cuando el orquestador del punto 13 procesa todos los requisitos de una épica con `--epica EP-XX`, verifica de forma agregada si hay requisitos del lote que tienen mayor afinidad semántica entre sí que con la épica declarada. Un cluster de requisitos mutuamente similares pero distintos a la épica es una señal fuerte de que deberían formar su propia épica.

**En la auditoría semanal del repositorio del punto 12.** El auditor automático incluye un paso de análisis de coherencia de épicas que detecta requisitos que han derivado temáticamente respecto a la épica a la que fueron asignados, especialmente en proyectos donde las épicas se definieron al inicio y el alcance ha evolucionado.

---

## Arquitectura del detector

El detector tiene tres componentes que trabajan en secuencia. El primero calcula la afinidad semántica del requisito con cada épica existente. El segundo decide si la afinidad es suficiente o si el requisito es un outlier. El tercero, cuando detecta un outlier, busca si hay otros requisitos en el repositorio con los que el requisito candidato forma un cluster natural.

```
Requisito en borrador o en-revision
        │
        ▼
[Componente 1] Cálculo de afinidad con épicas existentes
        │
        ├── Afinidad alta con una épica existente → OK, sin alerta
        │
        └── Afinidad baja con todas las épicas
                │
                ▼
        [Componente 2] Decisión de outlier
                │
                ▼
        [Componente 3] Búsqueda de cluster natural
                │
                ├── Cluster encontrado → Alerta: posible épica nueva con N requisitos
                │
                └── Sin cluster → Alerta: requisito huérfano, posible nueva épica emergente
```

---

## Componente 1: cálculo de afinidad con épicas existentes

La afinidad de un requisito con una épica no se mide comparando el requisito con la definición formal de la épica solamente. Esa comparación sería demasiado superficial porque las épicas a menudo tienen descripciones breves que no capturan toda la variedad funcional que contienen. La afinidad se mide comparando el requisito con el **centroide semántico de los requisitos ya asignados a esa épica**.

El centroide semántico es el embedding promedio de todos los chunks de tipo `identidad_requisito` de los requisitos en estado `validado` que pertenecen a esa épica. Representa el "centro de gravedad" temático de la épica tal como realmente está siendo utilizada, no como fue descrita en su definición original.

```python
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class AfinidadEpica:
    epica_id: str
    epica_nombre: str
    similitud_con_centroide: float
    similitud_con_definicion: float
    similitud_combinada: float
    n_requisitos_en_epica: int
    requisito_mas_similar: Optional[str]  # ID del requisito de la épica más cercano


class CalculadorAfinidadEpicas:
    """
    Calcula la afinidad semántica de un requisito con cada épica
    existente en el repositorio usando el centroide de sus requisitos.
    """

    PESO_CENTROIDE = 0.70
    # El centroide pondera más porque refleja el uso real de la épica
    PESO_DEFINICION = 0.30
    # La definición formal pondera menos porque suele ser más escueta

    def __init__(self, repositorio_rag, db_config: dict):
        self.rag = repositorio_rag
        self.db_config = db_config

    def calcular_afinidades(
        self,
        requisito: dict
    ) -> list[AfinidadEpica]:
        """
        Calcula la afinidad del requisito con todas las épicas activas.
        Retorna la lista ordenada de mayor a menor afinidad.
        """
        # Texto representativo del requisito para el cálculo
        texto_requisito = self._texto_representativo(requisito)
        embedding_requisito = self.rag.embeder_texto(texto_requisito)

        epicas = self._cargar_epicas_activas()
        afinidades = []

        for epica in epicas:
            # Similitud con la definición formal de la épica
            sim_definicion = self._similitud_con_definicion(
                embedding_requisito, epica
            )

            # Similitud con el centroide de los requisitos de la épica
            sim_centroide, req_mas_similar = self._similitud_con_centroide(
                embedding_requisito, epica["id"]
            )

            # Si la épica está vacía (sin requisitos validados todavía),
            # usar solo la similitud con la definición
            if epica["n_requisitos"] == 0:
                sim_combinada = sim_definicion
            else:
                sim_combinada = (
                    sim_centroide * self.PESO_CENTROIDE +
                    sim_definicion * self.PESO_DEFINICION
                )

            afinidades.append(AfinidadEpica(
                epica_id=epica["id"],
                epica_nombre=epica["nombre"],
                similitud_con_centroide=sim_centroide,
                similitud_con_definicion=sim_definicion,
                similitud_combinada=sim_combinada,
                n_requisitos_en_epica=epica["n_requisitos"],
                requisito_mas_similar=req_mas_similar
            ))

        return sorted(
            afinidades,
            key=lambda a: a.similitud_combinada,
            reverse=True
        )

    def _texto_representativo(self, requisito: dict) -> str:
        """
        Construye el texto que se embeda para representar el requisito.
        Pondera más los campos que definen la esencia funcional.
        """
        partes = [
            requisito.get("titulo", ""),
            requisito.get("descripcion", ""),
            f"Actor: {requisito.get('actor', '')}",
            f"Evento: {requisito.get('evento_disparador', '')}",
            f"Objetivo: {requisito.get('objetivo_negocio', '')}"
        ]
        # Incluir las reglas de negocio como señal semántica adicional
        for regla in requisito.get("reglas_negocio", [])[:3]:
            partes.append(f"Regla: {regla}")

        return " ".join(p for p in partes if p.strip())

    def _similitud_con_definicion(
        self,
        embedding_requisito: list[float],
        epica: dict
    ) -> float:
        """Similitud coseno entre el requisito y la definición de la épica."""
        if not epica.get("embedding_definicion"):
            return 0.0
        return self._coseno(embedding_requisito, epica["embedding_definicion"])

    def _similitud_con_centroide(
        self,
        embedding_requisito: list[float],
        epica_id: str
    ) -> tuple[float, Optional[str]]:
        """
        Calcula la similitud con el centroide de los requisitos de la épica
        y retorna también el ID del requisito más cercano individualmente.
        """
        import psycopg2
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                # Recuperar embeddings de los requisitos de la épica
                cur.execute("""
                    SELECT
                        metadatos->>'requisito_id' AS req_id,
                        embedding
                    FROM chunks_requisitos
                    WHERE metadatos->>'epica' = %s
                      AND metadatos->>'chunk_tipo' = 'identidad_requisito'
                      AND metadatos->>'estado' = 'validado'
                      AND activo = TRUE
                """, (epica_id,))
                filas = cur.fetchall()

        if not filas:
            return 0.0, None

        embeddings = [np.array(f[1]) for f in filas]
        req_ids = [f[0] for f in filas]

        # Calcular centroide como promedio de embeddings
        centroide = np.mean(embeddings, axis=0)
        sim_centroide = self._coseno(embedding_requisito, centroide.tolist())

        # Requisito individualmente más cercano
        similitudes_individuales = [
            self._coseno(embedding_requisito, e.tolist())
            for e in embeddings
        ]
        idx_max = np.argmax(similitudes_individuales)
        req_mas_similar = req_ids[idx_max]

        return sim_centroide, req_mas_similar

    def _cargar_epicas_activas(self) -> list[dict]:
        """Carga las épicas activas del repositorio con sus metadatos."""
        import psycopg2
        import yaml
        import os

        epicas = []
        ruta_epicas = os.path.join(
            os.environ.get("REPO_REQUISITOS", "./requisitos"), "epicas"
        )

        for archivo in os.listdir(ruta_epicas):
            if not archivo.endswith(".yaml"):
                continue
            with open(os.path.join(ruta_epicas, archivo)) as f:
                epica_def = yaml.safe_load(f)
            if epica_def.get("estado") == "deprecada":
                continue

            # Contar requisitos validados en la épica
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT COUNT(DISTINCT metadatos->>'requisito_id')
                        FROM chunks_requisitos
                        WHERE metadatos->>'epica' = %s
                          AND metadatos->>'estado' = 'validado'
                          AND activo = TRUE
                    """, (epica_def["id"],))
                    n_requisitos = cur.fetchone()[0]

            # Generar embedding de la definición formal si no existe
            texto_definicion = (
                f"{epica_def.get('nombre', '')}. "
                f"{epica_def.get('descripcion', {}).get('objetivo', '')}. "
                f"{epica_def.get('descripcion', {}).get('alcance', '')}"
            )
            embedding_def = self.rag.embeder_texto(texto_definicion)

            epicas.append({
                "id": epica_def["id"],
                "nombre": epica_def.get("nombre", ""),
                "n_requisitos": n_requisitos,
                "embedding_definicion": embedding_def
            })

        return epicas

    @staticmethod
    def _coseno(v1: list[float], v2: list[float]) -> float:
        """Similitud coseno entre dos vectores."""
        a = np.array(v1)
        b = np.array(v2)
        norma = np.linalg.norm(a) * np.linalg.norm(b)
        if norma == 0:
            return 0.0
        return float(np.dot(a, b) / norma)
```

---

## Componente 2: decisión de outlier

Con las afinidades calculadas, el decisor determina si el requisito es un outlier respecto al sistema de épicas existente. La decisión usa dos umbrales independientes que deben cumplirse simultáneamente para disparar la alerta.

```python
@dataclass
class DecisionEpica:
    veredicto: str
    # OK                → encaja bien en una épica existente
    # POSIBLE_OUTLIER   → afinidad baja pero no concluyente
    # OUTLIER           → afinidad claramente insuficiente con todas las épicas
    epica_recomendada: Optional[str]
    similitud_maxima: float
    justificacion: str
    requiere_decision_po: bool


class DecisorOutlier:
    """
    Determina si un requisito es un outlier respecto al sistema
    de épicas existente en función de sus afinidades calculadas.
    """

    # Umbral por encima del cual el requisito encaja bien en una épica
    UMBRAL_AFINIDAD_OK = 0.75

    # Umbral por debajo del cual el requisito es claramente un outlier
    UMBRAL_OUTLIER_CLARO = 0.58

    # Entre ambos umbrales: posible outlier, requiere revisión

    # Número mínimo de épicas con las que comparar antes de emitir veredicto
    # Con pocas épicas, un outlier puede ser simplemente el primer requisito
    # de un área nueva que el proyecto todavía no ha formalizado
    MIN_EPICAS_PARA_OUTLIER = 3

    def decidir(
        self,
        afinidades: list[AfinidadEpica],
        requisito: dict
    ) -> DecisionEpica:
        """
        Emite el veredicto sobre si el requisito encaja en el sistema
        de épicas existente o puede ser candidato a épica nueva.
        """
        if not afinidades:
            return DecisionEpica(
                veredicto="OK",
                epica_recomendada=requisito.get("epica"),
                similitud_maxima=1.0,
                justificacion="Sin épicas en el repositorio para comparar.",
                requiere_decision_po=False
            )

        mejor = afinidades[0]
        sim_max = mejor.similitud_combinada

        # Encaje claro: sin alerta
        if sim_max >= self.UMBRAL_AFINIDAD_OK:
            # Verificar si la épica declarada coincide con la de mayor afinidad
            epica_declarada = requisito.get("epica")
            if (epica_declarada and
                    mejor.epica_id != epica_declarada and
                    sim_max - afinidades[
                        next(
                            (i for i, a in enumerate(afinidades)
                             if a.epica_id == epica_declarada), 0
                        )
                    ].similitud_combinada > 0.10):
                # El requisito encaja mejor en otra épica diferente a la declarada
                return DecisionEpica(
                    veredicto="EPICA_INCORRECTA",
                    epica_recomendada=mejor.epica_id,
                    similitud_maxima=sim_max,
                    justificacion=(
                        f"El requisito encaja mejor en '{mejor.epica_nombre}' "
                        f"({sim_max:.0%} afinidad) que en la épica declarada "
                        f"'{epica_declarada}'."
                    ),
                    requiere_decision_po=True
                )

            return DecisionEpica(
                veredicto="OK",
                epica_recomendada=mejor.epica_id,
                similitud_maxima=sim_max,
                justificacion=(
                    f"Encaje adecuado con '{mejor.epica_nombre}' "
                    f"({sim_max:.0%} afinidad)."
                ),
                requiere_decision_po=False
            )

        # Outlier claro
        if (sim_max < self.UMBRAL_OUTLIER_CLARO and
                len(afinidades) >= self.MIN_EPICAS_PARA_OUTLIER):
            return DecisionEpica(
                veredicto="OUTLIER",
                epica_recomendada=None,
                similitud_maxima=sim_max,
                justificacion=(
                    f"Afinidad máxima con épicas existentes: {sim_max:.0%}. "
                    f"Por debajo del umbral mínimo ({self.UMBRAL_OUTLIER_CLARO:.0%}). "
                    f"El requisito puede pertenecer a un módulo funcional "
                    f"no contemplado todavía en el proyecto."
                ),
                requiere_decision_po=True
            )

        # Zona intermedia: posible outlier
        return DecisionEpica(
            veredicto="POSIBLE_OUTLIER",
            epica_recomendada=mejor.epica_id,
            similitud_maxima=sim_max,
            justificacion=(
                f"Afinidad con '{mejor.epica_nombre}': {sim_max:.0%}. "
                f"Encaje débil. El requisito puede estar en el límite "
                f"entre módulos o pertenecer a un módulo emergente."
            ),
            requiere_decision_po=True
        )
```

---

## Componente 3: búsqueda de cluster natural

Cuando el decisor emite un veredicto `OUTLIER` o `POSIBLE_OUTLIER`, el buscador de clusters analiza si hay otros requisitos en el repositorio —en cualquier estado, no solo en validado— con los que el requisito candidato forme un grupo temático coherente. La existencia de un cluster fortalece considerablemente la hipótesis de épica nueva: no es un requisito huérfano, sino el primero de una familia emergente.

```python
@dataclass
class ClusterDetectado:
    requisitos: list[str]        # IDs de los requisitos del cluster
    nombre_sugerido: str         # Nombre propuesto para la épica, generado por LLM
    descripcion_sugerida: str    # Descripción funcional del cluster
    cohesion: float              # Similitud media intra-cluster (0-1)
    confianza: str               # alta │ media │ baja


class BuscadorClusterEpica:
    """
    Busca clusters de requisitos que no encajan en épicas existentes
    y que podrían formar una nueva épica juntos.
    """

    UMBRAL_SIMILITUD_CLUSTER = 0.68
    # Dos requisitos forman parte del mismo cluster si su similitud
    # es al menos 0.68 entre sí

    MIN_REQUISITOS_CLUSTER = 2
    # Un cluster con menos de 2 requisitos no justifica una épica nueva;
    # puede ser un requisito genuinamente atípico

    def __init__(self, repositorio_rag, openai_client):
        self.rag = repositorio_rag
        self.openai = openai_client

    def buscar_cluster(
        self,
        requisito_candidato: dict,
        epicas_existentes: list[str]
    ) -> Optional[ClusterDetectado]:
        """
        Busca requisitos que formen cluster natural con el candidato.
        Excluye requisitos ya bien asignados a épicas existentes.
        """
        # Texto del candidato para la búsqueda
        texto_candidato = (
            f"{requisito_candidato.get('titulo', '')} "
            f"{requisito_candidato.get('descripcion', '')}"
        )

        # Buscar requisitos semánticamente similares en todo el repositorio
        resultados = self.rag.buscar_por_similitud(
            query_texto=texto_candidato,
            top_k=15
        )

        # Filtrar: solo requisitos que también son outliers respecto
        # a las épicas existentes (aquellos cuya épica declarada no
        # coincide con una épica del catálogo activo, o que están
        # en borrador sin épica asignada)
        candidatos_cluster = []
        for r in resultados:
            req_id = r.metadatos.get("requisito_id")
            epica_req = r.metadatos.get("epica", "")

            if req_id == requisito_candidato.get("id"):
                continue
            if r.similitud < self.UMBRAL_SIMILITUD_CLUSTER:
                continue

            # Incluir si: la épica no está en el catálogo activo,
            # o si el requisito está en borrador sin épica
            epica_activa = epica_req in epicas_existentes
            if not epica_activa or not epica_req:
                candidatos_cluster.append({
                    "req_id": req_id,
                    "similitud": r.similitud,
                    "epica_declarada": epica_req,
                    "titulo": r.texto[:80]
                })

        if len(candidatos_cluster) < self.MIN_REQUISITOS_CLUSTER - 1:
            return None

        # Calcular cohesión intra-cluster
        ids_cluster = (
            [requisito_candidato.get("id")] +
            [c["req_id"] for c in candidatos_cluster]
        )
        similitudes = [c["similitud"] for c in candidatos_cluster]
        cohesion_media = sum(similitudes) / len(similitudes)

        # Generar nombre y descripción del cluster con LLM
        titulos = [requisito_candidato.get("titulo", "")] + [
            c["titulo"] for c in candidatos_cluster[:4]
        ]
        nombre, descripcion = self._nombrar_cluster(titulos)

        # Determinar nivel de confianza
        if cohesion_media >= 0.80 and len(ids_cluster) >= 4:
            confianza = "alta"
        elif cohesion_media >= 0.72 and len(ids_cluster) >= 2:
            confianza = "media"
        else:
            confianza = "baja"

        return ClusterDetectado(
            requisitos=ids_cluster,
            nombre_sugerido=nombre,
            descripcion_sugerida=descripcion,
            cohesion=cohesion_media,
            confianza=confianza
        )

    def _nombrar_cluster(
        self,
        titulos: list[str]
    ) -> tuple[str, str]:
        """
        Usa el LLM para proponer un nombre y descripción
        para el cluster de requisitos detectado.
        """
        prompt = f"""
Analiza los siguientes títulos de requisitos funcionales que parecen
pertenecer al mismo módulo funcional sin clasificar todavía:

{chr(10).join(f'- {t}' for t in titulos)}

Propón:
1. Un nombre corto para el módulo (máximo 5 palabras, en infinitivo o sustantivo)
2. Una descripción de una frase de qué capacidad de negocio habilita este módulo

Responde SOLO con JSON válido, sin texto adicional:
{{
  "nombre": "...",
  "descripcion": "..."
}}
        """
        response = self.openai.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        import json
        datos = json.loads(response.choices[0].message.content)
        return datos.get("nombre", "Módulo sin clasificar"), datos.get("descripcion", "")
```

---

## Informe de detección y flujo de alerta

Cuando el sistema detecta un outlier, genera un informe estructurado y lo distribuye por los canales configurados. El informe está diseñado para que el product owner pueda tomar la decisión en menos de cinco minutos, con la información mínima necesaria y sin tecnicismos.

```python
@dataclass
class InformeDeteccionEpica:
    requisito_id: str
    titulo_requisito: str
    timestamp: str
    veredicto: str
    epica_declarada: Optional[str]
    epica_recomendada: Optional[str]
    similitud_maxima: float
    justificacion: str
    cluster: Optional[ClusterDetectado]
    top_afinidades: list[AfinidadEpica]   # Las 3 épicas con mayor afinidad
    opciones_accion: list[dict]
    requiere_decision_po: bool


def generar_informe_deteccion(
    requisito: dict,
    decision: DecisionEpica,
    afinidades: list[AfinidadEpica],
    cluster: Optional[ClusterDetectado]
) -> InformeDeteccionEpica:
    """
    Ensambla el informe de detección con las opciones de acción
    específicas al veredicto emitido.
    """
    opciones = _construir_opciones_accion(
        veredicto=decision.veredicto,
        epica_recomendada=decision.epica_recomendada,
        cluster=cluster,
        epica_declarada=requisito.get("epica")
    )

    return InformeDeteccionEpica(
        requisito_id=requisito.get("id", ""),
        titulo_requisito=requisito.get("titulo", ""),
        timestamp=__import__("datetime").datetime.now().isoformat(),
        veredicto=decision.veredicto,
        epica_declarada=requisito.get("epica"),
        epica_recomendada=decision.epica_recomendada,
        similitud_maxima=decision.similitud_maxima,
        justificacion=decision.justificacion,
        cluster=cluster,
        top_afinidades=afinidades[:3],
        opciones_accion=opciones,
        requiere_decision_po=decision.requiere_decision_po
    )


def _construir_opciones_accion(
    veredicto: str,
    epica_recomendada: Optional[str],
    cluster: Optional[ClusterDetectado],
    epica_declarada: Optional[str]
) -> list[dict]:
    """Construye las opciones de acción específicas al veredicto."""

    if veredicto == "EPICA_INCORRECTA":
        return [
            {
                "id": "A",
                "accion": f"Mover a '{epica_recomendada}'",
                "descripcion": (
                    f"Reasignar el requisito a la épica con mayor afinidad semántica. "
                    f"Actualizar el campo 'epica' en el YAML."
                ),
                "impacto": "Bajo. Solo requiere editar el YAML y re-indexar."
            },
            {
                "id": "B",
                "accion": "Mantener en la épica declarada",
                "descripcion": (
                    "El analista confirma que la asignación actual es correcta "
                    "a pesar de la baja afinidad semántica detectada. "
                    "Añadir una nota en el campo 'notas_implementacion' explicando "
                    "por qué pertenece a esa épica."
                ),
                "impacto": "Ninguno en el repositorio. La alerta se silencia."
            }
        ]

    if veredicto == "OUTLIER" and cluster:
        return [
            {
                "id": "A",
                "accion": f"Crear épica '{cluster.nombre_sugerido}'",
                "descripcion": (
                    f"Formalizar una nueva épica para los {len(cluster.requisitos)} "
                    f"requisitos del cluster detectado. El sistema propone el nombre "
                    f"'{cluster.nombre_sugerido}' con una cohesión del "
                    f"{cluster.cohesion:.0%}. El product owner revisa y aprueba "
                    f"antes de crear la épica en Jira."
                ),
                "impacto": (
                    "Medio. Requiere crear la épica en Jira, actualizar los YAMLs "
                    f"de {len(cluster.requisitos)} requisitos y re-indexar."
                )
            },
            {
                "id": "B",
                "accion": f"Asignar provisionalmente a '{epica_declarada or 'épica más cercana'}'",
                "descripcion": (
                    "Continuar con la asignación actual como medida provisional "
                    "mientras se decide si crear la nueva épica. Marcar el requisito "
                    "con la etiqueta 'epica-pendiente-revision' para no perderlo de vista."
                ),
                "impacto": (
                    "Bajo a corto plazo. Riesgo de que la deuda de clasificación "
                    "crezca si se añaden más requisitos del mismo módulo emergente."
                )
            },
            {
                "id": "C",
                "accion": "Descartarlo del sprint actual",
                "descripcion": (
                    "Si el módulo al que pertenece no está en el roadmap aprobado, "
                    "mover el requisito a estado 'wont-have' con nota de motivo "
                    "y programar su revisión para la siguiente planificación trimestral."
                ),
                "impacto": "Ninguno en el sprint. El requisito queda en el backlog no priorizado."
            }
        ]

    if veredicto == "OUTLIER" and not cluster:
        return [
            {
                "id": "A",
                "accion": "Marcar como 'requisito huérfano' y escalar al PO",
                "descripcion": (
                    "El requisito no encaja en ninguna épica existente y no forma "
                    "cluster con otros. Puede ser prematuro, fuera de alcance "
                    "o el precursor de un módulo nuevo. Requiere decisión explícita "
                    "del product owner antes de continuar."
                ),
                "impacto": "Ninguno en el sprint. Bloquea el procesamiento del requisito."
            },
            {
                "id": "B",
                "accion": "Crear épica nueva de un solo requisito",
                "descripcion": (
                    "Formalizar una épica nueva aunque tenga un solo requisito por ahora. "
                    "Útil cuando el analista tiene certeza de que el módulo va a crecer "
                    "en sprints futuros y quiere establecer la estructura desde el inicio."
                ),
                "impacto": "Bajo. La épica vacía no bloquea nada pero crea deuda de definición."
            }
        ]

    # POSIBLE_OUTLIER
    return [
        {
            "id": "A",
            "accion": "Continuar con la épica declarada",
            "descripcion": (
                "La afinidad es débil pero no concluyente. El analista confirma "
                "que el encaje es correcto. El pipeline continúa con normalidad."
            ),
            "impacto": "Ninguno."
        },
        {
            "id": "B",
            "accion": "Revisar la asignación con el PO antes de procesar",
            "descripcion": (
                "Pausar el procesamiento del requisito hasta confirmar con el "
                "product owner que la épica es la correcta."
            ),
            "impacto": "Retraso de uno a dos días en el procesamiento."
        }
    ]
```

### Formato del informe para el analista

El informe que llega al analista o al product owner tiene un formato compacto que cabe en un mensaje de Slack o en un comentario de Confluence:

```
╔══════════════════════════════════════════════════════════════╗
║  ALERTA DE CLASIFICACIÓN — REQ-041                           ║
╠══════════════════════════════════════════════════════════════╣
║  REQUISITO: Configurar alertas de vencimiento de contratos   ║
║  ÉPICA DECLARADA: EP-04 Gestión de Facturación               ║
║  VEREDICTO: OUTLIER                                          ║
╠══════════════════════════════════════════════════════════════╣
║  AFINIDAD CON ÉPICAS EXISTENTES                              ║
║  EP-04 Gestión de Facturación    ██░░░░░░░ 48%               ║
║  EP-02 Gestión de Usuarios       █░░░░░░░░ 32%               ║
║  EP-01 Autenticación             █░░░░░░░░ 28%               ║
╠══════════════════════════════════════════════════════════════╣
║  CLUSTER DETECTADO (confianza: alta)                         ║
║  Posible módulo nuevo: "Gestión de Contratos"                ║
║  Requisitos del cluster:                                     ║
║  → REQ-038 Registrar nuevo contrato de proveedor             ║
║  → REQ-039 Consultar condiciones de contrato vigente         ║
║  → REQ-040 Renovar contrato próximo a vencer                 ║
║  → REQ-041 Configurar alertas de vencimiento de contratos    ║
║  Cohesión interna: 83%                                       ║
╠══════════════════════════════════════════════════════════════╣
║  OPCIONES DE ACCIÓN                                          ║
║  [A] Crear épica 'Gestión de Contratos' (recomendado)        ║
║  [B] Asignar provisionalmente a EP-04                        ║
║  [C] Descartar del sprint actual                             ║
║                                                              ║
║  Decisión requerida del PO antes de: 2025-05-16              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Integración en el orquestador

El detector se integra como un sub-paso del paso 2 del orquestador, ejecutándose después de la validación estructural y semántica pero antes de la generación de artefactos. Si el veredicto es `OUTLIER` o `EPICA_INCORRECTA` y `requiere_decision_po` es `true`, el pipeline se pausa en modo interactivo hasta recibir la decisión.

```python
# Fragmento relevante del orchestrator.py — dentro del paso s2_validacion

# ... tras la validación de calidad del punto 6 ...

# ── Detección de épica ──────────────────────────────────────────
if requisito.get("estado") in ("en-revision", "validado"):
    calculador = CalculadorAfinidadEpicas(motor_rag, config.db.to_dict())
    afinidades = calculador.calcular_afinidades(requisito)

    decisor = DecisorOutlier()
    decision_epica = decisor.decidir(afinidades, requisito)

    if decision_epica.veredicto in ("OUTLIER", "POSIBLE_OUTLIER", "EPICA_INCORRECTA"):
        # Buscar cluster solo en veredictos fuertes
        cluster = None
        if decision_epica.veredicto in ("OUTLIER", "EPICA_INCORRECTA"):
            buscador = BuscadorClusterEpica(motor_rag, openai_client)
            epicas_activas = [a.epica_id for a in afinidades]
            cluster = buscador.buscar_cluster(requisito, epicas_activas)

        informe = generar_informe_deteccion(
            requisito=requisito,
            decision=decision_epica,
            afinidades=afinidades,
            cluster=cluster
        )

        # Registrar en el run para trazabilidad
        run.artefactos_generados["alerta_epica"] = {
            "veredicto": decision_epica.veredicto,
            "similitud_maxima": decision_epica.similitud_maxima,
            "cluster_detectado": cluster is not None,
            "n_requisitos_cluster": len(cluster.requisitos) if cluster else 0
        }
        run.advertencias_globales.append(
            f"Clasificación de épica: {decision_epica.veredicto}. "
            f"{decision_epica.justificacion}"
        )

        # Imprimir alerta en consola
        _imprimir_alerta_epica(informe)

        # Si el modo es interactivo y requiere decisión del PO,
        # pausar el pipeline hasta recibir respuesta
        if config.modo_interactivo and decision_epica.requiere_decision_po:
            decision_usuario = await _solicitar_decision_epica(informe)

            if decision_usuario == "A" and decision_epica.veredicto == "OUTLIER":
                # El usuario elige crear épica nueva
                # El pipeline se pausa: la épica debe crearse antes de continuar
                log.info(
                    "Pipeline pausado. Crear la épica nueva en Jira y en el "
                    "repositorio, luego re-ejecutar con el campo 'epica' actualizado."
                )
                run = gestor.finalizar(run, EstadoEjecucion.PAUSADO_EPICA)
                return _resultado_pausado(run, informe, time.time() - inicio_total)

            elif decision_usuario == "B":
                # Continuar con la asignación actual
                log.info("Continuando con la épica declarada por decisión del analista.")

            # Registrar la decisión en el run
            run.artefactos_generados["alerta_epica"]["decision_tomada"] = decision_usuario
```

---

## Detección en modo batch: análisis de coherencia de épicas

Cuando el orquestador procesa una épica completa con `--epica EP-XX`, el análisis de coherencia actúa sobre el lote completo de forma agregada. Este modo detecta un patrón distinto: no un único requisito outlier, sino una fractura interna en la épica donde un subgrupo de requisitos ha derivado temáticamente del núcleo original.

```python
class AnalizadorCoherenciaEpica:
    """
    Analiza la coherencia semántica interna de una épica completa.
    Detecta si todos sus requisitos pertenecen al mismo espacio temático
    o si hay subgrupos que deberían separarse.
    """

    UMBRAL_COHERENCIA_OK = 0.72
    # Una épica es coherente si la similitud media entre sus requisitos
    # supera este umbral

    def __init__(self, repositorio_rag, db_config: dict):
        self.rag = repositorio_rag
        self.db_config = db_config

    def analizar(self, epica_id: str) -> dict:
        """
        Calcula la coherencia interna de la épica y detecta posibles
        sub-épicas emergentes dentro de ella.
        """
        import psycopg2, numpy as np, json

        # Recuperar embeddings de todos los requisitos de la épica
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        metadatos->>'requisito_id' AS req_id,
                        metadatos->>'titulo'       AS titulo,
                        embedding
                    FROM chunks_requisitos
                    WHERE metadatos->>'epica' = %s
                      AND metadatos->>'chunk_tipo' = 'identidad_requisito'
                      AND metadatos->>'estado' IN ('validado', 'en-revision')
                      AND activo = TRUE
                """, (epica_id,))
                filas = cur.fetchall()

        if len(filas) < 3:
            return {
                "epica_id": epica_id,
                "coherencia": "indeterminada",
                "motivo": f"Solo {len(filas)} requisitos. Mínimo 3 para el análisis."
            }

        req_ids = [f[0] for f in filas]
        titulos = {f[0]: f[1] for f in filas}
        embeddings = [np.array(f[2]) for f in filas]

        # Calcular matriz de similitudes entre todos los pares
        n = len(embeddings)
        similitudes = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                sim = float(np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) *
                    np.linalg.norm(embeddings[j])
                ))
                similitudes[i, j] = sim
                similitudes[j, i] = sim

        # Similitud media intra-épica (excluyendo diagonal)
        mask = np.ones((n, n), dtype=bool)
        np.fill_diagonal(mask, False)
        coherencia_media = float(similitudes[mask].mean())

        # Detectar outliers internos: requisitos con similitud media
        # con el resto de la épica significativamente inferior a la media
        similitudes_medias_por_req = similitudes.mean(axis=1)
        umbral_outlier_interno = coherencia_media - 0.15

        outliers_internos = [
            {
                "req_id": req_ids[i],
                "titulo": titulos.get(req_ids[i], ""),
                "similitud_media_con_epica": float(similitudes_medias_por_req[i])
            }
            for i in range(n)
            if similitudes_medias_por_req[i] < umbral_outlier_interno
        ]

        resultado = {
            "epica_id": epica_id,
            "n_requisitos": n,
            "coherencia_media": round(coherencia_media, 3),
            "coherencia_ok": coherencia_media >= self.UMBRAL_COHERENCIA_OK,
            "outliers_internos": outliers_internos,
            "alerta": None
        }

        if outliers_internos and not resultado["coherencia_ok"]:
            resultado["alerta"] = (
                f"La épica {epica_id} tiene {len(outliers_internos)} requisitos "
                f"con baja afinidad interna. Posible candidatura a split "
                f"en dos épicas más cohesivas."
            )

        return resultado
```

---

## Umbrales y su calibración

Los umbrales del sistema no son fijos. Necesitan calibración para cada proyecto porque dominios de negocio diferentes tienen mayor o menor dispersión semántica natural. Un proyecto de e-commerce tiene requisitos temáticamente más variados que un proyecto de gestión de nóminas, y los umbrales deben reflejar esa diferencia.

El proceso de calibración inicial se ejecuta una sola vez, en la Fase 0 del roadmap del punto 14, cuando el repositorio tiene al menos veinte requisitos validados distribuidos en tres o más épicas.

```python
def calibrar_umbrales(repositorio_rag, db_config: dict) -> dict:
    """
    Calcula los umbrales óptimos para este proyecto en concreto
    basándose en la distribución de similitudes del repositorio actual.

    Retorna los umbrales recomendados que deben actualizarse en
    DecisorOutlier y AnalizadorCoherenciaEpica.
    """
    import psycopg2, numpy as np

    # Recuperar todos los pares de requisitos de la misma épica
    # (deben tener alta similitud: son el ground truth de "encajan bien")
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.metadatos->>'epica', a.embedding, b.embedding
                FROM chunks_requisitos a
                JOIN chunks_requisitos b
                  ON a.metadatos->>'epica' = b.metadatos->>'epica'
                  AND a.id < b.id
                WHERE a.metadatos->>'chunk_tipo' = 'identidad_requisito'
                  AND a.metadatos->>'estado' = 'validado'
                  AND a.activo = TRUE AND b.activo = TRUE
                LIMIT 500
            """)
            pares_misma_epica = cur.fetchall()

            # Pares de requisitos de épicas diferentes
            # (deben tener baja similitud: son el ground truth de "no encajan")
            cur.execute("""
                SELECT a.embedding, b.embedding
                FROM chunks_requisitos a
                JOIN chunks_requisitos b
                  ON a.metadatos->>'epica' != b.metadatos->>'epica'
                  AND a.id < b.id
                WHERE a.metadatos->>'chunk_tipo' = 'identidad_requisito'
                  AND a.metadatos->>'estado' = 'validado'
                  AND a.activo = TRUE AND b.activo = TRUE
                LIMIT 500
            """)
            pares_diferente_epica = cur.fetchall()

    def similitud_coseno(e1, e2):
        a, b = np.array(e1), np.array(e2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    sims_misma = [similitud_coseno(p[1], p[2]) for p in pares_misma_epica]
    sims_diferente = [similitud_coseno(p[0], p[1]) for p in pares_diferente_epica]

    if not sims_misma or not sims_diferente:
        return {"error": "Datos insuficientes para calibración"}

    # El umbral OK se sitúa en el percentil 25 de las similitudes intra-épica
    # (el 75% de los requisitos de la misma épica deben superarlo)
    umbral_ok = float(np.percentile(sims_misma, 25))

    # El umbral outlier se sitúa en el percentil 75 de las similitudes inter-épica
    # (solo el 25% de los requisitos de épicas distintas lo superan)
    umbral_outlier = float(np.percentile(sims_diferente, 75))

    return {
        "umbral_afinidad_ok": round(umbral_ok, 2),
        "umbral_outlier_claro": round(umbral_outlier, 2),
        "umbral_similitud_cluster": round((umbral_ok + umbral_outlier) / 2, 2),
        "percentil_25_misma_epica": round(umbral_ok, 2),
        "percentil_75_diferente_epica": round(umbral_outlier, 2),
        "n_pares_misma_epica": len(sims_misma),
        "n_pares_diferente_epica": len(sims_diferente),
        "nota": (
            "Recalibrar cuando el repositorio supere 100 requisitos validados "
            "o cuando se incorporen tres o más módulos nuevos."
        )
    }
```

---

## Métricas de efectividad del detector

Las métricas que indican si el detector está calibrado correctamente se miden comparando sus veredictos con las decisiones reales que tomó el equipo en cada caso.

**Precisión de la alerta.** Porcentaje de alertas emitidas que el analista o el PO confirmaron como correctas. Una precisión inferior al 70% indica que los umbrales están demasiado bajos y el sistema genera demasiado ruido. El objetivo es una precisión superior al 80% en el tercer mes de uso.

**Cobertura.** Porcentaje de épicas nuevas creadas en el proyecto que el detector anticipó con al menos una alerta. Una cobertura inferior al 60% indica que los umbrales están demasiado altos y el sistema deja pasar casos reales. El objetivo es una cobertura superior al 75%.

**Tiempo de anticipación.** Cuántos días antes de que el PO decidiera crear la épica nueva lo detectó el sistema. El objetivo es que la alerta llegue antes de que el tercer requisito del cluster sea procesado, cuando el coste de re-clasificar es todavía bajo.

**Tasa de falsos positivos silenciados.** Porcentaje de alertas que el analista descartó con la opción "continuar con la épica declarada". Una tasa elevada y estable indica que los umbrales necesitan subirse para ese tipo de módulo concreto.

---

## Relación con el resto del modelo

El detector se apoya en la misma infraestructura de embeddings y vector store del punto 7, que ya existe para el RAG de contexto. No añade coste de infraestructura: añade una consulta adicional en el paso 3 del orquestador.

La salida del detector alimenta directamente la cola de aprobación del paso 8 cuando emite un veredicto que requiere decisión humana, añadiendo la sección de alerta de clasificación al informe que ve el analista antes de aprobar los artefactos.

El catálogo de épicas que mantiene el buscador de clusters es el mismo que usa el generador de artefactos del punto 4 para asignar el `epic_link` correcto en el payload de Jira. Si el detector crea una épica nueva, el generador la usa automáticamente en el siguiente requisito del cluster.

El análisis de coherencia de épicas que ejecuta el orquestador en modo batch es el mismo análisis que la auditoría semanal del punto 12 ejecuta sobre todo el repositorio, con la diferencia de que en el batch se ejecuta solo sobre los requisitos del lote en curso.
