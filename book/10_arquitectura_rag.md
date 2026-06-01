# Capítulo 10. Arquitectura RAG: la memoria del pipeline

---

*En este capítulo aprenderás:*

- *Qué es RAG y por qué el pipeline necesita memoria para no contradecirse a sí mismo*
- *Cómo transformar el repositorio de requisitos en una base de conocimiento consultable en segundos*
- *Qué estrategia de chunking funciona mejor para documentos funcionales y por qué*
- *Cómo integrar el contexto recuperado en los prompts de generación y validación*

---

El lunes de la semana cinco del piloto, Carlos abrió Jira con la intención de generar la historia para REQ-034. El requisito describía la exportación de facturas a PDF con membrete corporativo. Rellenó la plantilla, pasó la validación —sin bloqueantes— y ejecutó el pipeline.

El JSON llegó en cuarenta y dos segundos. Historia, cuatro tareas, ocho test cases. Carlos lo revisó con la tranquilidad que ya había adquirido después de dos semanas usando el sistema. Aprobó. Push a Jira.

Esa tarde, en el refinamiento, María García levantó la mano.

—Esto ya lo tenemos. REQ-022 es exportar facturas a PDF. Lo implementamos en el sprint tres.

Carlos abrió el YAML de REQ-022. Era cierto. No idéntico —REQ-022 exportaba el listado completo y REQ-034 exportaba una factura individual con membrete—, pero la mitad de las tareas técnicas eran exactamente las mismas: el servicio de generación de PDF, la librería de plantillas, la integración con el gestor de documentos.

El pipeline había generado cuatro tareas que ya existían. Dos horas de refinamiento para llegar a la conclusión de que solo había trabajo nuevo para dos de ellas.

Carlos lo anotó en el cuaderno. No era un fallo del prompt. Era un fallo de memoria. El pipeline no sabía que REQ-022 existía.

Esa noche construyó el sistema RAG.

---

## El problema de la amnesia del pipeline

En los capítulos anteriores, el pipeline ha procesado un requisito a la vez. Le das el YAML de REQ-023, le das el glosario, y genera la historia, las tareas y los test cases. Funciona bien para un requisito aislado.

El problema aparece cuando el proyecto lleva semanas en marcha y el repositorio tiene cuarenta, ochenta, ciento veinte requisitos. El pipeline sigue procesando cada requisito como si fuera el primero. No sabe qué se ha generado antes. No sabe qué patrones usa el equipo. No sabe si la funcionalidad que está a punto de generar ya existe bajo otro nombre.

Esta amnesia tiene tres consecuencias prácticas que Carlos ya había experimentado:

**Duplicidades funcionales.** El pipeline genera tareas técnicas que ya existen porque no sabe que se implementaron en otro requisito. El equipo las detecta en el refinamiento, si las detecta, y pierde tiempo des-duplicando trabajo.

**Inconsistencias terminológicas.** El pipeline usa el término «exportar» en una historia y «generar» en otra para describir la misma operación. El glosario corrige las inconsistencias más obvias, pero no puede detectar cuando dos conceptos distintos del repositorio colisionan semánticamente.

**Contradicciones entre requisitos.** REQ-034 establece que el PDF tiene membrete corporativo. REQ-022 establece que el PDF no tiene formato especial. Si se implementan en sprints distintos, el comportamiento en producción depende de cuál se deployó último.

RAG —Retrieval-Augmented Generation— resuelve exactamente estos tres problemas. Antes de llamar al LLM para generar un artefacto, el sistema recupera del repositorio los fragmentos más relevantes y los inyecta como contexto. La IA genera sabiendo lo que ya existe.

---

## Qué es RAG en términos no técnicos

La explicación canónica de RAG suele implicar vectores, embeddings y similitud coseno. Todo eso es real y lo veremos en detalle. Pero antes conviene tener la intuición correcta.

Imagina que tienes que escribir la descripción técnica de una tarea nueva para el sprint. Para hacerlo bien, consultas las tareas similares que el equipo ya ha escrito: miras las de la semana pasada, las del sprint anterior, buscas el patrón que usa tu equipo para describirlas. Luego escribes la nueva con esa referencia.

RAG hace exactamente eso, pero a escala y en décimas de segundo.

El sistema tiene tres componentes que trabajan en secuencia:

**El índice** es el repositorio de requisitos transformado en una estructura que permite búsqueda por significado, no solo por palabras exactas. Si buscas «exportar facturas», el índice devuelve también requisitos que hablan de «generar PDFs de documentos contables» aunque no contengan la palabra «exportar».

**El recuperador** es el componente que, dado el requisito que el pipeline está a punto de procesar, consulta el índice y devuelve los fragmentos más relevantes del repositorio. No el repositorio completo —eso consumiría demasiados tokens—, sino los diez o quince fragmentos con mayor similitud semántica.

**El generador** es el LLM, que ahora recibe dos cosas: el requisito que tiene que procesar y el contexto recuperado del repositorio. Genera la historia, las tareas o los test cases sabiendo qué existe ya, qué patrones usa el equipo y qué podría contradecirse.

```
Sin RAG:
  Requisito + Glosario → LLM → Artefacto

Con RAG:
  Requisito + Glosario + [Contexto del repositorio] → LLM → Artefacto
```

La diferencia en el output es equivalente a la diferencia entre pedirle a alguien que escriba un documento nuevo de cero frente a pedirle que lo haga después de haber leído los veinte documentos similares más recientes del equipo.

---

## Cómo funciona el índice: embeddings y similitud semántica

Para que el recuperador pueda encontrar los fragmentos relevantes en milisegundos, el repositorio no se almacena como texto plano. Se almacena como vectores numéricos —embeddings— que representan el significado de cada fragmento.

Un embedding es una lista de números (típicamente entre 768 y 3.072) que sitúan el significado de un texto en un espacio matemático multidimensional. Textos con significados similares quedan cerca en ese espacio. Textos con significados distintos quedan lejos.

No necesitas entender la geometría para usarlo. Lo que importa es el efecto:

```
"El gestor filtra facturas por fecha"
→ embedding: [0.23, -0.41, 0.87, ..., 0.12]   # 1536 números

"El operador busca documentos por período contable"
→ embedding: [0.21, -0.38, 0.89, ..., 0.15]   # Muy parecido al anterior

"El sistema envía un correo de bienvenida al usuario"
→ embedding: [-0.67, 0.92, -0.31, ..., 0.44]  # Muy diferente
```

El modelo que usamos en Meridian para generar embeddings es `text-embedding-3-large` de OpenAI. Produce vectores de 1.536 dimensiones y tiene buenas prestaciones para texto técnico en español. No es el único disponible, pero es el que produce resultados más consistentes con el tipo de texto de un repositorio de análisis funcional.

---

## La estrategia de chunking: cómo fragmentar los requisitos

La decisión más importante de toda la arquitectura RAG no es qué modelo de embeddings usar ni qué base de datos vectorial escoger. Es cómo fragmentar los requisitos antes de indexarlos.

Un chunk demasiado grande devuelve información irrelevante junto con la relevante. Si indexas el YAML completo de REQ-022 como un único fragmento, cuando el sistema busca «criterios de aceptación de exportación PDF» devuelve también los campos de actor, origen, datos de entrada y metadatos técnicos que no tienen nada que ver con la búsqueda.

Un chunk demasiado pequeño pierde contexto. Si indexas cada criterio de aceptación por separado sin referencia al requisito que lo contiene, el sistema no puede saber que ese criterio pertenece al módulo de facturación y que el actor es el gestor de facturación.

La solución que funciona en la práctica es **chunking semántico por bloque funcional**: cada bloque de la plantilla YAML se indexa como un chunk independiente, con metadatos que permiten recuperar su origen y filtrar por módulo, estado o tipo.

Esto produce entre cuatro y seis chunks por requisito, según cuántos bloques tenga datos:

| Chunk | Contenido | Para qué se recupera |
|---|---|---|
| Identidad + contexto | Título, actor, descripción, evento disparador, objetivo | Detectar duplicidades funcionales |
| Reglas de negocio | Lista de reglas del requisito | Detectar contradicciones entre módulos |
| Criterios de aceptación | Cada AC como chunk individual | Detectar criterios duplicados o solapados |
| Datos de entrada/salida | Tipos, formatos, rangos | Detectar incompatibilidades de interfaz |
| Flujos de error | Excepciones y comportamientos en error | Sugerir flujos de error en requisitos nuevos |

Este diseño permite hacer búsquedas específicas. Cuando el pipeline está generando test cases de contorno, no necesita recuperar todos los fragmentos de un requisito similar: solo necesita los de datos de entrada, donde están los rangos y formatos que generan los casos límite.

Aquí está la implementación que Carlos desplegó en Meridian:

```python
# chunking.py
# Transforma un YAML de requisito en chunks semánticos indexables.
# Cada bloque funcional se convierte en un chunk independiente
# con sus metadatos para permitir filtrado en el retrieval.

import yaml
import hashlib
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Chunk:
    """Unidad mínima de indexación del repositorio."""
    id: str           # Identificador único: REQ-023::criterios_ac::AC-023-01
    texto: str        # Texto que se embedda y almacena
    tipo: str         # Tipo de chunk para filtrado posterior
    metadatos: dict   # Campos para filtrado: req_id, epica, estado, actor...

def chunkerizar_requisito(ruta_yaml: str) -> list[Chunk]:
    """
    Convierte un archivo YAML de requisito en una lista de chunks.
    Preserva el contexto semántico de cada bloque mientras mantiene
    la granularidad necesaria para búsquedas específicas.
    """
    with open(ruta_yaml, encoding="utf-8") as f:
        req = yaml.safe_load(f)

    chunks = []
    req_id  = req["id"]
    epica   = req.get("epica", "")
    actor   = req.get("actor", "")
    titulo  = req.get("titulo", "")

    # Metadatos base que heredan todos los chunks del requisito.
    # Se usan para filtrar en el retrieval sin necesidad de leer el texto.
    meta_base = {
        "requisito_id": req_id,
        "epica":        epica,
        "estado":       req.get("estado", "borrador"),
        "actor":        actor,
        "prioridad":    req.get("prioridad", ""),
        "modulo":       req.get("modulo", ""),
    }

    # ── CHUNK 1: Identidad y contexto de negocio ─────────────────────────
    # Es el chunk más consultado: lo recupera cualquier búsqueda sobre
    # la funcionalidad general del requisito. Incluye la descripción
    # completa para que la similitud semántica sea precisa.
    texto_identidad = f"""
Requisito {req_id}: {titulo}
Módulo: {req.get("modulo", "")} ({epica})
Actor principal: {actor}
Prioridad: {req.get("prioridad", "")}
Descripción: {req.get("descripcion", "")}
Evento disparador: {req.get("evento_disparador", "")}
Objetivo de negocio: {req.get("objetivo_negocio", "")}
""".strip()

    chunks.append(Chunk(
        id=f"{req_id}::identidad",
        texto=texto_identidad,
        tipo="identidad_requisito",
        metadatos={**meta_base, "chunk_tipo": "identidad"}
    ))

    # ── CHUNK 2: Reglas de negocio ────────────────────────────────────────
    # Se recupera cuando el pipeline necesita verificar que las reglas
    # del nuevo requisito no contradicen las de otros del mismo módulo.
    if req.get("reglas_negocio"):
        reglas_texto = "\n".join(
            f"- {r}" for r in req["reglas_negocio"]
        )
        texto_reglas = f"""
Reglas de negocio del requisito {req_id} ({titulo}):
{reglas_texto}
Módulo: {epica} | Actor: {actor}
""".strip()

        chunks.append(Chunk(
            id=f"{req_id}::reglas_negocio",
            texto=texto_reglas,
            tipo="reglas_negocio",
            metadatos={**meta_base, "chunk_tipo": "reglas_negocio"}
        ))

    # ── CHUNK 3: Criterios de aceptación (uno por criterio) ──────────────
    # Granularidad máxima para este bloque: cada AC es un chunk
    # independiente. Permite detectar criterios duplicados o solapados
    # a nivel de escenario específico, no solo a nivel de requisito.
    for ac in req.get("criterios_aceptacion", []):
        texto_ac = f"""
Criterio {ac["id"]} del requisito {req_id} ({titulo}):
Dado: {ac.get("dado", "")}
Cuando: {ac.get("cuando", "")}
Entonces: {ac.get("entonces", "")}
Tipo: {ac.get("tipo", "positivo")}
Contexto: módulo {epica} | actor {actor}
""".strip()

        chunks.append(Chunk(
            id=f"{req_id}::{ac['id']}",
            texto=texto_ac,
            tipo="criterio_aceptacion",
            metadatos={
                **meta_base,
                "chunk_tipo": "criterio_aceptacion",
                "ac_id":      ac["id"],
                "ac_tipo":    ac.get("tipo", "positivo")
            }
        ))

    # ── CHUNK 4: Datos de entrada y salida ───────────────────────────────
    # Se recupera para verificar compatibilidad de interfaces entre
    # requisitos que comparten datos o que operan sobre las mismas entidades.
    datos_entrada = req.get("datos_entrada", [])
    datos_salida  = req.get("datos_salida", {})

    if datos_entrada or datos_salida:
        campos_entrada = [
            f"{d['nombre']} ({d.get('tipo','?')}, "
            f"{'requerido' if d.get('requerido') else 'opcional'})"
            for d in datos_entrada
        ]
        campos_salida = datos_salida.get("campos", [])

        texto_datos = f"""
Interfaz de datos del requisito {req_id} ({titulo}):
Entradas: {", ".join(campos_entrada) if campos_entrada else "no especificadas"}
Salidas: {", ".join(campos_salida) if campos_salida else "no especificadas"}
Formato respuesta: {datos_salida.get("formato", "")}
Tiempo máximo respuesta: {datos_salida.get("tiempo_respuesta_max_ms", "")} ms
Módulo: {epica}
""".strip()

        chunks.append(Chunk(
            id=f"{req_id}::datos",
            texto=texto_datos,
            tipo="datos_interfaz",
            metadatos={**meta_base, "chunk_tipo": "datos_interfaz"}
        ))

    # ── CHUNK 5: Flujos de error y excepciones ───────────────────────────
    # Se recupera para sugerir flujos de error en requisitos nuevos
    # que aún no los tienen documentados. También detecta tratamientos
    # inconsistentes del mismo tipo de error en módulos distintos.
    excepciones = req.get("excepciones", [])
    if excepciones:
        texto_exc = "\n".join(
            f"- Si {e.get('condicion', e if isinstance(e, str) else '')}: "
            f"{e.get('comportamiento', '') if isinstance(e, dict) else ''}"
            for e in excepciones
        )
        texto_flujos_error = f"""
Flujos de error del requisito {req_id} ({titulo}):
{texto_exc}
Módulo: {epica} | Actor afectado: {actor}
""".strip()

        chunks.append(Chunk(
            id=f"{req_id}::excepciones",
            texto=texto_flujos_error,
            tipo="flujos_error",
            metadatos={**meta_base, "chunk_tipo": "flujos_error"}
        ))

    return chunks
```

Para REQ-023, este código produce exactamente cinco chunks:

```
REQ-023::identidad          →  "Requisito REQ-023: Filtrar facturas por rango de fechas..."
REQ-023::reglas_negocio     →  "Reglas de negocio del requisito REQ-023..."
REQ-023::AC-023-01          →  "Criterio AC-023-01 del requisito REQ-023..."
REQ-023::AC-023-02          →  "Criterio AC-023-02 del requisito REQ-023..."
REQ-023::datos              →  "Interfaz de datos del requisito REQ-023..."
REQ-023::excepciones        →  "Flujos de error del requisito REQ-023..."
```

Con cuarenta requisitos en el repositorio de Meridian, el índice tiene aproximadamente 220 chunks. Una búsqueda semántica sobre 220 vectores tarda menos de 50 milisegundos en pgvector con el hardware más básico.

---

## El vector store: pgvector sobre PostgreSQL

El vector store es la base de datos que almacena los embeddings y permite búsqueda por similitud semántica. Hay varias opciones en el mercado —Pinecone, Chroma, Weaviate, Qdrant—, pero para la mayoría de equipos que están empezando con RAG, la opción más práctica es **pgvector**, una extensión de PostgreSQL.

La razón es sencilla: casi todos los proyectos ya tienen PostgreSQL. pgvector añade un tipo de dato `vector` y un índice especializado sin necesidad de gestionar una base de datos adicional.

> 💡 **Idea clave**
>
> Chroma es excelente para un prototipo local que quieres tener en marcha en treinta minutos. pgvector es la opción correcta para producción en una organización que ya tiene PostgreSQL. Pinecone o Qdrant tiene sentido cuando el repositorio supera los 100.000 chunks o cuando necesitas alta disponibilidad gestionada. Para Meridian —y para la mayoría de equipos de análisis funcional— pgvector es suficiente durante años.

```python
# vector_store.py
# Gestiona la conexión con PostgreSQL + pgvector.
# Crea el esquema, indexa chunks y ejecuta búsquedas por similitud.

import psycopg2
from psycopg2.extras import execute_values
import json
import hashlib
from openai import OpenAI

class VectorStoreRequisitos:
    """
    Almacén vectorial del repositorio de requisitos.
    Usa pgvector como motor de búsqueda semántica y PostgreSQL
    estándar para los metadatos y el filtrado.
    """

    def __init__(self, db_config: dict, openai_api_key: str):
        self.db  = psycopg2.connect(**db_config)
        self.llm = OpenAI(api_key=openai_api_key)
        self._crear_esquema()

    def _crear_esquema(self):
        """
        Crea las tablas y los índices necesarios si no existen.
        El índice HNSW permite búsquedas aproximadas rápidas.
        """
        with self.db.cursor() as cur:
            # La extensión pgvector debe estar instalada en el servidor.
            # En PostgreSQL 15+: CREATE EXTENSION IF NOT EXISTS vector;
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS chunks_requisitos (
                    id              TEXT PRIMARY KEY,
                    texto           TEXT NOT NULL,
                    tipo            TEXT NOT NULL,
                    -- El vector tiene 1536 dimensiones porque usamos
                    -- text-embedding-3-large. Si cambias el modelo,
                    -- cambia también este número.
                    embedding       vector(1536),
                    metadatos       JSONB,
                    -- Hash del contenido para detectar cambios
                    -- sin re-indexar si el texto no ha cambiado.
                    hash_contenido  TEXT,
                    fecha_indexado  TIMESTAMP DEFAULT NOW(),
                    -- Requisitos deprecados se marcan inactivos,
                    -- no se eliminan, para preservar la trazabilidad histórica.
                    activo          BOOLEAN DEFAULT TRUE
                );
            """)

            # Índice HNSW: búsqueda aproximada de vecinos más cercanos.
            # m=16 y ef_construction=128 son valores equilibrados para
            # repositorios de hasta 500.000 chunks.
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_embedding
                    ON chunks_requisitos
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 128);
            """)

            # Índice GIN sobre JSONB para filtrado eficiente por metadatos:
            # permite filtrar por epica, estado, actor, etc. sin scan completo.
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunks_metadatos
                    ON chunks_requisitos USING gin (metadatos);
            """)

        self.db.commit()

    def embeder(self, texto: str) -> list[float]:
        """
        Genera el vector de embeddings para un texto.
        Usamos text-embedding-3-large por su precisión en texto técnico.
        La dimensión 1536 es un balance entre precisión y coste de almacenamiento.
        """
        respuesta = self.llm.embeddings.create(
            model="text-embedding-3-large",
            input=texto,
            dimensions=1536
        )
        return respuesta.data[0].embedding

    def indexar(self, chunk) -> bool:
        """
        Indexa un chunk en el vector store.
        Si el chunk ya existe y el contenido no cambió, lo omite.
        Si cambió, actualiza el embedding y los metadatos.
        Retorna True si se indexó (nuevo o actualizado), False si no cambió.
        """
        hash_nuevo = hashlib.md5(chunk.texto.encode()).hexdigest()

        with self.db.cursor() as cur:
            # Comprobar si existe y si el contenido cambió
            cur.execute(
                "SELECT hash_contenido FROM chunks_requisitos WHERE id = %s",
                (chunk.id,)
            )
            fila = cur.fetchone()
            if fila and fila[0] == hash_nuevo:
                return False  # Sin cambios, no re-indexar

            # Generar embedding solo cuando hay que indexar.
            # Cada llamada a la API de embeddings tiene un coste,
            # por eso verificamos primero si el contenido cambió.
            embedding = self.embeder(chunk.texto)

            cur.execute("""
                INSERT INTO chunks_requisitos
                    (id, texto, tipo, embedding, metadatos, hash_contenido)
                VALUES (%s, %s, %s, %s::vector, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    texto          = EXCLUDED.texto,
                    tipo           = EXCLUDED.tipo,
                    embedding      = EXCLUDED.embedding,
                    metadatos      = EXCLUDED.metadatos,
                    hash_contenido = EXCLUDED.hash_contenido,
                    fecha_indexado = NOW(),
                    activo         = TRUE
            """, (
                chunk.id,
                chunk.texto,
                chunk.tipo,
                embedding,
                json.dumps(chunk.metadatos),
                hash_nuevo
            ))

        self.db.commit()
        return True

    def buscar(
        self,
        query: str,
        top_k: int = 5,
        umbral_similitud: float = 0.72,
        filtros: dict = None
    ) -> list[dict]:
        """
        Búsqueda híbrida: similitud semántica + filtros por metadatos.
        
        umbral_similitud: chunks por debajo de 0.72 suelen ser ruido.
        Ajustarlo a la baja (0.65) si el dominio es muy especializado
        y los textos usan vocabulario muy específico.
        
        filtros: dict con pares campo/valor que se aplican sobre
        la columna JSONB metadatos. Ejemplo: {"epica": "EP-04"}
        """
        embedding_query = self.embeder(query)

        # Construir cláusulas WHERE adicionales desde los filtros
        where_extra = []
        params_extra = []
        if filtros:
            for clave, valor in filtros.items():
                where_extra.append(f"metadatos->>'{clave}' = %s")
                params_extra.append(str(valor))

        where_sql = "activo = TRUE"
        if where_extra:
            where_sql += " AND " + " AND ".join(where_extra)

        with self.db.cursor() as cur:
            # La función <=> calcula la distancia coseno entre dos vectores.
            # 1 - distancia = similitud coseno (1 = idéntico, 0 = opuesto).
            cur.execute(f"""
                SELECT
                    id,
                    texto,
                    1 - (embedding <=> %s::vector) AS similitud,
                    metadatos,
                    tipo
                FROM chunks_requisitos
                WHERE {where_sql}
                  AND 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [
                embedding_query,
                *params_extra,
                embedding_query,
                umbral_similitud,
                embedding_query,
                top_k
            ])

            return [
                {
                    "chunk_id":   fila[0],
                    "texto":      fila[1],
                    "similitud":  round(float(fila[2]), 3),
                    "metadatos":  fila[3],
                    "tipo":       fila[4]
                }
                for fila in cur.fetchall()
            ]

    def desactivar_requisito(self, requisito_id: str):
        """
        Marca como inactivos todos los chunks de un requisito deprecado.
        No los elimina: los chunks inactivos siguen en la base de datos
        para auditoría histórica, pero no aparecen en las búsquedas.
        """
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE chunks_requisitos
                SET activo = FALSE
                WHERE metadatos->>'requisito_id' = %s
            """, (requisito_id,))
        self.db.commit()
```

> ⚠️ **Error frecuente**
>
> El error más común al implementar el vector store es re-indexar todos los chunks en cada ejecución del pipeline. Una re-indexación completa de 200 chunks con `text-embedding-3-large` hace 200 llamadas a la API de OpenAI y tarda entre 30 y 60 segundos. El campo `hash_contenido` del código anterior resuelve esto: si el texto no ha cambiado desde la última indexación, el chunk se omite. En el repositorio de Meridian, una ejecución típica del indexador sobre los 220 chunks tarda menos de 3 segundos porque la mayoría no ha cambiado.

---

## El recuperador: construir el contexto antes de llamar al LLM

Indexar es la mitad del trabajo. La otra mitad es saber qué recuperar y cómo inyectarlo en el prompt.

La tentación es hacer una única búsqueda genérica con el texto del requisito como query. Funciona, pero no es óptimo. Una búsqueda genérica recupera los cinco fragmentos más similares en global, que pueden ser cinco fragmentos del mismo tipo —cinco criterios de aceptación, por ejemplo— y perderse la información sobre reglas de negocio relacionadas que vive en otro tipo de chunk.

La estrategia que da mejores resultados es hacer **búsquedas especializadas en paralelo**, una por tipo de información que el pipeline necesita:

```python
# recuperador.py
# Ejecuta múltiples búsquedas especializadas en paralelo
# y ensambla el contexto para el pipeline de generación.

import asyncio
from dataclasses import dataclass

@dataclass
class ContextoRAG:
    """Resultado del proceso de recuperación para un requisito."""
    funcionalidad_similar:    list[dict]  # Para detectar duplicidades
    reglas_mismo_modulo:      list[dict]  # Para detectar contradicciones
    criterios_similares:      list[dict]  # Para detectar AC duplicados
    flujos_error_relacionados:list[dict]  # Para sugerir excepciones
    requisitos_mismo_actor:   list[dict]  # Para coherencia de permisos

class Recuperador:
    """
    Orquesta las búsquedas en el vector store y construye
    el contexto que se inyecta en los prompts del pipeline.
    """

    UMBRAL_SIMILITUD      = 0.72   # Chunks por debajo de este valor = ruido
    UMBRAL_DUPLICADO      = 0.90   # Por encima = posible duplicado, alertar
    RESULTADOS_POR_BUSQUEDA = 5    # Máximo por consulta especializada

    def __init__(self, vector_store: VectorStoreRequisitos):
        self.vs = vector_store

    async def recuperar(self, requisito: dict) -> ContextoRAG:
        """
        Ejecuta cinco búsquedas en paralelo y ensambla el contexto.
        El uso de asyncio.gather reduce el tiempo de espera total:
        cinco búsquedas secuenciales ≈ 500ms; en paralelo ≈ 120ms.
        """
        epica   = requisito.get("epica", "")
        actor   = requisito.get("actor", "")
        titulo  = requisito.get("titulo", "")
        desc    = requisito.get("descripcion", "")
        reglas  = " ".join(requisito.get("reglas_negocio", []))
        ac_texto = " ".join([
            f"{ac.get('dado','')} {ac.get('cuando','')} {ac.get('entonces','')}"
            for ac in requisito.get("criterios_aceptacion", [])
        ])

        # Las cinco búsquedas se lanzan en paralelo.
        # Cada una usa una query diferente para maximizar la cobertura
        # de información relevante y minimizar la redundancia.
        resultados = await asyncio.gather(
            # 1. Funcionalidad similar en todo el proyecto (no solo el módulo)
            asyncio.to_thread(self.vs.buscar,
                f"{titulo}. {desc}",
                self.RESULTADOS_POR_BUSQUEDA,
                self.UMBRAL_SIMILITUD,
                {"estado": "validado"}
            ),
            # 2. Reglas de negocio del mismo módulo
            asyncio.to_thread(self.vs.buscar,
                f"reglas de negocio módulo {epica}: {reglas}",
                self.RESULTADOS_POR_BUSQUEDA,
                self.UMBRAL_SIMILITUD,
                {"epica": epica, "chunk_tipo": "reglas_negocio"}
            ),
            # 3. Criterios de aceptación similares (detección de duplicados)
            asyncio.to_thread(self.vs.buscar,
                ac_texto,
                self.RESULTADOS_POR_BUSQUEDA,
                self.UMBRAL_SIMILITUD,
                {"chunk_tipo": "criterio_aceptacion"}
            ),
            # 4. Flujos de error del módulo (para sugerir excepciones)
            asyncio.to_thread(self.vs.buscar,
                f"flujos de error excepciones módulo {epica}",
                self.RESULTADOS_POR_BUSQUEDA,
                self.UMBRAL_SIMILITUD,
                {"chunk_tipo": "flujos_error"}
            ),
            # 5. Requisitos con el mismo actor (coherencia de permisos)
            asyncio.to_thread(self.vs.buscar,
                f"acciones del actor {actor}",
                self.RESULTADOS_POR_BUSQUEDA,
                self.UMBRAL_SIMILITUD,
                {"actor": actor, "chunk_tipo": "identidad"}
            )
        )

        # Deduplicar: un mismo chunk puede aparecer en varias búsquedas.
        # Lo mantenemos solo en la categoría más relevante.
        vistos = set()
        def deduplicar(lista):
            resultado = []
            for item in lista:
                if item["chunk_id"] not in vistos:
                    vistos.add(item["chunk_id"])
                    resultado.append(item)
            return resultado

        return ContextoRAG(
            funcionalidad_similar=     deduplicar(resultados[0]),
            reglas_mismo_modulo=       deduplicar(resultados[1]),
            criterios_similares=       deduplicar(resultados[2]),
            flujos_error_relacionados= deduplicar(resultados[3]),
            requisitos_mismo_actor=    deduplicar(resultados[4])
        )
```

---

## Cómo ensamblar el contexto en el prompt

Recuperar los chunks es necesario pero no suficiente. Hay que transformarlos en un bloque de texto que el LLM pueda usar eficientemente, sin desperdiciar tokens en información redundante ni en formato que el modelo no necesita.

El formato que mejor funciona en la práctica es un bloque estructurado con secciones claramente delimitadas, en el que cada sección tiene una instrucción explícita sobre cómo debe usarse:

```python
# ensamblador_contexto.py
# Transforma el resultado del recuperador en el bloque de contexto
# que se inyecta en los prompts del pipeline.

def ensamblar_contexto(contexto: ContextoRAG, requisito_actual: dict) -> str:
    """
    Construye el bloque de contexto para el prompt del pipeline.
    
    Principios de diseño:
    - Cada sección tiene una instrucción explícita para el LLM
    - Los chunks se truncan a 300 caracteres para controlar el consumo de tokens
    - Las advertencias de posibles duplicados se marcan prominentemente
    - El contexto nunca ocupa más del 40% del total del prompt
    """
    req_id = requisito_actual.get("id", "")
    secciones = []

    # ── Sección 1: Funcionalidad similar ─────────────────────────────────
    if contexto.funcionalidad_similar:
        items = []
        for c in contexto.funcionalidad_similar[:3]:
            similitud_pct = int(c["similitud"] * 100)
            req_origen    = c["metadatos"].get("requisito_id", "?")

            # Marcar prominentemente si la similitud supera el umbral de duplicado
            prefijo = "⚠ POSIBLE DUPLICADO" if c["similitud"] > 0.90 else "→ Relacionado"

            items.append(
                f"▸ [{req_origen}] {prefijo} ({similitud_pct}% similitud):\n"
                f"  {c['texto'][:300]}..."
            )

        secciones.append(
            "═════════════════════════════════════════════\n"
            "REQUISITOS CON FUNCIONALIDAD SIMILAR (ya validados)\n"
            "Instrucción: verifica que el nuevo requisito NO duplica estos.\n"
            "Si hay alta similitud (>90%), indica el posible solapamiento\n"
            "en la sección alertas_calidad de la historia generada.\n"
            "═════════════════════════════════════════════\n"
            + "\n\n".join(items)
        )

    # ── Sección 2: Reglas de negocio del módulo ───────────────────────────
    if contexto.reglas_mismo_modulo:
        items = [
            f"▸ [{c['metadatos'].get('requisito_id','?')}]: {c['texto'][:250]}"
            for c in contexto.reglas_mismo_modulo[:4]
        ]
        secciones.append(
            "═════════════════════════════════════════════\n"
            f"REGLAS DE NEGOCIO EXISTENTES EN {requisito_actual.get('epica','')}\n"
            "Instrucción: el nuevo requisito NO puede contradecir estas reglas.\n"
            "Si detectas contradicción, indícalo en alertas_calidad.\n"
            "═════════════════════════════════════════════\n"
            + "\n".join(items)
        )

    # ── Sección 3: Criterios de aceptación similares ─────────────────────
    # Solo incluir si la similitud es alta: criterios poco similares
    # son ruido que distrae al modelo más que ayuda.
    criterios_relevantes = [
        c for c in contexto.criterios_similares
        if c["similitud"] > 0.82
    ]
    if criterios_relevantes:
        items = [
            f"▸ [{c['metadatos'].get('ac_id','?')}] de "
            f"{c['metadatos'].get('requisito_id','?')} "
            f"({int(c['similitud']*100)}% similitud):\n"
            f"  {c['texto'][:280]}"
            for c in criterios_relevantes[:3]
        ]
        secciones.append(
            "═════════════════════════════════════════════\n"
            "CRITERIOS DE ACEPTACIÓN MUY SIMILARES\n"
            "Instrucción: verifica si son realmente distintos del nuevo requisito\n"
            "o si el escenario ya está cubierto. Similitud >88% indica riesgo alto.\n"
            "═════════════════════════════════════════════\n"
            + "\n\n".join(items)
        )

    # ── Sección 4: Flujos de error relacionados ───────────────────────────
    if contexto.flujos_error_relacionados:
        items = [
            f"▸ [{c['metadatos'].get('requisito_id','?')}]: {c['texto'][:220]}"
            for c in contexto.flujos_error_relacionados[:3]
        ]
        secciones.append(
            "═════════════════════════════════════════════\n"
            "FLUJOS DE ERROR YA DOCUMENTADOS EN EL MÓDULO\n"
            "Instrucción: estos son los patrones de error que ya usa el equipo.\n"
            "Úsalos como referencia para los flujos de error del nuevo requisito.\n"
            "═════════════════════════════════════════════\n"
            + "\n".join(items)
        )

    if not secciones:
        return "No se encontraron requisitos relacionados en el repositorio."

    return "\n\n".join(secciones)
```

El bloque resultante para REQ-034 (exportación de factura individual con membrete) habría tenido este aspecto antes del incidente del refinamiento:

```
═════════════════════════════════════════════
REQUISITOS CON FUNCIONALIDAD SIMILAR (ya validados)
Instrucción: verifica que el nuevo requisito NO duplica estos.
Si hay alta similitud (>90%), indica el posible solapamiento
en la sección alertas_calidad de la historia generada.
═════════════════════════════════════════════
▸ [REQ-022] → Relacionado (84% similitud):
  Requisito REQ-022: Exportar listado de facturas a PDF
  Módulo: Gestión de Facturación (EP-04)
  Actor principal: Gestor de facturación
  Descripción: El gestor necesita exportar el listado filtrado de
  facturas a un archivo PDF para adjuntarlo en informes de cierre...

═════════════════════════════════════════════
REGLAS DE NEGOCIO EXISTENTES EN EP-04
Instrucción: el nuevo requisito NO puede contradecir estas reglas.
═════════════════════════════════════════════
▸ [REQ-022]: Reglas de negocio del requisito REQ-022:
  - El archivo PDF generado no incluye logotipo ni membrete corporativo
  - El nombre del archivo sigue el patrón: facturas_{fecha}_{usuario}.pdf...
```

Con este contexto, la llamada 2 del pipeline (generación de la historia) habría generado una alerta en el campo `alertas_calidad`:

```json
"alertas_calidad": [
  "REQ-022 (similitud 84%) cubre exportación de listado de facturas a PDF sin membrete. REQ-034 exporta una factura individual con membrete. Son funcionalidades distintas pero comparten la infraestructura de generación de PDF. Revisar si las tareas técnicas de generación de PDF y gestión de plantillas deben referenciar la implementación existente en lugar de crear una nueva."
]
```

No habría detenido el pipeline. No habría bloqueado la historia. Pero sí habría llevado esa información al gate de aprobación, donde Carlos —o cualquier analista que revisara el JSON— habría tomado la decisión correcta antes del push a Jira.

---

## Cuándo re-indexar

El índice es solo tan bueno como su actualización. Un repositorio que se indexó la primera semana y nunca más actualizó es, en la práctica, un sistema sin RAG después de cuatro sprints.

El trigger de re-indexación más eficiente no es un cron job nocturno: es el propio workflow de estados de los requisitos. Cada vez que un requisito cambia de estado —de borrador a en-revision, de en-revision a validado, o de validado a deprecado— el indexador se ejecuta automáticamente sobre ese requisito.

```python
# indexador.py
# Se llama desde el webhook de Confluence cuando cambia el estado
# de un requisito, o desde el orquestador cuando procesa un YAML.

from pathlib import Path
import yaml
from chunking import chunkerizar_requisito
from vector_store import VectorStoreRequisitos

class Indexador:
    """
    Mantiene el vector store sincronizado con el repositorio de requisitos.
    Opera de forma incremental: solo re-indexa lo que cambió.
    """

    # Solo los requisitos en estos estados tienen valor para el pipeline.
    # Los borradores se excluyen para no contaminar el contexto con
    # información no validada.
    ESTADOS_INDEXABLES = {"en-revision", "validado"}

    def __init__(self, vector_store: VectorStoreRequisitos):
        self.vs = vector_store

    def procesar_yaml(self, ruta: str) -> dict:
        """
        Indexa un requisito desde su archivo YAML.
        Retorna un resumen con los chunks indexados y los omitidos.
        """
        with open(ruta, encoding="utf-8") as f:
            req = yaml.safe_load(f)

        req_id = req.get("id", ruta)
        estado = req.get("estado", "borrador")

        # Si el requisito se deprecó, desactivar sus chunks existentes
        if estado == "deprecado":
            self.vs.desactivar_requisito(req_id)
            return {"accion": "desactivado", "requisito_id": req_id}

        # Solo indexar estados procesables
        if estado not in self.ESTADOS_INDEXABLES:
            return {
                "accion":       "omitido",
                "requisito_id": req_id,
                "motivo":       f"Estado '{estado}' no indexable"
            }

        chunks = chunkerizar_requisito(ruta)
        indexados = 0
        sin_cambios = 0

        for chunk in chunks:
            if self.vs.indexar(chunk):
                indexados += 1
            else:
                sin_cambios += 1

        return {
            "accion":       "indexado",
            "requisito_id": req_id,
            "chunks_totales":    len(chunks),
            "chunks_indexados":  indexados,
            "chunks_sin_cambios": sin_cambios
        }

    def indexar_repositorio_completo(self, carpeta: str) -> dict:
        """
        Indexa todos los archivos YAML de una carpeta y sus subcarpetas.
        Útil para la indexación inicial o para sincronizar tras un merge
        de rama que añade muchos requisitos nuevos.
        """
        carpeta_path = Path(carpeta)
        resultados   = {"indexados": 0, "omitidos": 0, "errores": []}

        for ruta in sorted(carpeta_path.rglob("*.yaml")):
            # Excluir plantillas y archivos de configuración
            if "template" in ruta.name or "config" in ruta.name:
                continue
            try:
                resultado = self.procesar_yaml(str(ruta))
                if resultado["accion"] == "indexado":
                    resultados["indexados"] += resultado["chunks_indexados"]
                else:
                    resultados["omitidos"] += 1
            except Exception as e:
                resultados["errores"].append({
                    "archivo": str(ruta),
                    "error":   str(e)
                })

        return resultados
```

> 🛠️ **En la práctica**
>
> En los primeros dos meses de uso, la indexación inicial es el único proceso lento. Con 40 requisitos y 5 chunks cada uno, la primera indexación completa hace 200 llamadas a la API de embeddings y tarda entre 90 y 120 segundos. Después de eso, solo se re-indexan los requisitos que cambian. En el repositorio de Meridian al mes seis, con 120 requisitos validados, una semana típica re-indexa entre 5 y 15 chunks —los de los requisitos que pasaron de borrador a validado durante esa semana—. El coste de cada llamada a `text-embedding-3-large` con un chunk de tamaño medio (150 tokens) es de aproximadamente 0,002 €. La indexación semanal de 15 chunks cuesta menos de 0,04 €.

---

## Integrar RAG en el pipeline: el punto de conexión

El RAG no es un sistema independiente: es una capa que se inserta entre la validación y la generación. En el orquestador del Capítulo 12, el paso 3 llama al recuperador antes de pasar el requisito al prompt de generación.

La conexión es directa: el contexto ensamblado se inyecta en el system prompt base que comparten todas las llamadas del pipeline:

```python
# Fragmento del paso s3_rag_contexto del orquestador
# (el código completo está en el Capítulo 12)

async def ejecutar_paso_rag(
    requisito: dict,
    recuperador: Recuperador
) -> str:
    """
    Recupera el contexto del repositorio y lo ensambla
    en el bloque que se añadirá al system prompt del pipeline.
    """
    contexto_raw = await recuperador.recuperar(requisito)
    contexto_txt = ensamblar_contexto(contexto_raw, requisito)

    # Advertir si se detectaron posibles duplicados
    duplicados = [
        c for c in contexto_raw.funcionalidad_similar
        if c["similitud"] > 0.90
    ]
    if duplicados:
        print(
            f"  ⚠ {len(duplicados)} requisito(s) con similitud >90% detectado(s). "
            f"El pipeline continuará pero la historia generada incluirá "
            f"una alerta en alertas_calidad."
        )

    return contexto_txt
```

Y en el system prompt del Capítulo 8, hay un placeholder que recibe ese contexto:

```
📋 Prompt de IA — System prompt base con contexto RAG

Eres un analista funcional senior especializado en Agile. Tu función es
transformar requisitos funcionales estructurados en artefactos Jira precisos.

REGLAS:
1. Nunca inventes información que no esté en el requisito de entrada.
   Si falta algo, usa el marcador [PENDIENTE: descripción].
2. Usa exclusivamente los términos del glosario proporcionado.
3. Si detectas solapamiento con los requisitos del contexto histórico,
   indícalo en alertas_calidad. No bloquees la generación.
4. El output es siempre JSON válido. Sin texto fuera del JSON.

GLOSARIO:
{{glosario_compacto}}

CONTEXTO DEL REPOSITORIO (requisitos relacionados ya existentes):
{{contexto_rag}}

REQUISITO A PROCESAR:
{{requisito_yaml}}
```

El `{{contexto_rag}}` es exactamente el string que produce `ensamblar_contexto`. En una ejecución típica de Meridian, ese bloque ocupa entre 800 y 1.200 tokens, que es un coste razonable frente al valor que aporta.

---

## Lo que el RAG no hace

Conviene ser honesto sobre los límites del sistema antes de que el lector los descubra por su cuenta.

**No detecta todas las contradicciones.** Si REQ-022 establece en su regla de negocio que «los PDFs no llevan membrete» y REQ-034 establece que «el PDF lleva membrete corporativo», el RAG recuperará REQ-022 como requisito relacionado. Si la similitud semántica entre ambos es alta —y lo será—, el LLM recibirá ambas reglas en el mismo contexto. Pero detectar que son contradictorias requiere que el LLM las interprete correctamente en el contexto del dominio. Lo hace bien el 80% de las veces. El 20% restante necesita la revisión humana del gate de aprobación, que es exactamente para lo que existe.

**No garantiza que el contexto recuperado sea el más relevante.** La búsqueda por similitud semántica no es búsqueda exacta. Un requisito muy relevante con vocabulario técnico muy diferente puede quedar por debajo del umbral de similitud y no recuperarse. Por eso el umbral es configurable y por eso el analista sigue teniendo el gate de aprobación: el RAG mejora estadísticamente la calidad del output, pero no elimina la necesidad de revisión.

**No aprende en tiempo real.** El vector store refleja el estado del repositorio en el momento de la última indexación. Si el analista valida REQ-035 a las 10:00 y a las 10:30 ejecuta el pipeline para REQ-036 que tiene relación con REQ-035, el RAG no recuperará REQ-035 a menos que se haya indexado entre las 10:00 y las 10:30. En Meridian, el indexador se ejecuta automáticamente al cambiar el estado de un requisito a validado, así que el desfase máximo es de segundos. Pero en setups donde la indexación es manual o se ejecuta en batch, el desfase puede ser de horas o días.

> ⚠️ **Error frecuente**
>
> Algunos equipos intentan compensar estos límites bajando el umbral de similitud a 0.60 o menos para que el sistema recupere más contexto. El resultado es el contrario al esperado: con un umbral bajo, el contexto incluye fragmentos poco relevantes que distraen al LLM y hacen que el output sea menos preciso. Si el repositorio tiene pocos requisitos (menos de veinte), es normal que las similitudes sean bajas: los pocos requisitos que existen pueden ser funcionalmente muy distintos entre sí. En ese caso, lo correcto es usar el RAG sin filtro de umbral mínimo, no bajarlo artificialmente. El umbral de 0.72 es un valor empírico válido para repositorios de más de treinta requisitos.

---

## Lo que funciona en la práctica

Carlos tardó tres días en desplegar el sistema RAG en Meridian. Uno para escribir el código de chunking e indexación, uno para integrarlo en el orquestador y uno para la indexación inicial del repositorio de cuarenta requisitos que había acumulado en las primeras semanas.

Lo que cambió desde el primer día fue sutil pero acumulativo.

Las historias generadas empezaron a incluir referencias explícitas a otras historias. «Esta tarea puede reutilizar el servicio de generación de PDF implementado en FACT-22 (REQ-022).» El desarrollador que recibía la tarea tenía contexto directo desde el primer momento, sin necesidad de preguntar al analista o de buscar en el histórico de Jira.

El gate de aprobación se volvió más rápido. Carlos tardaba entre cinco y ocho minutos en revisar un JSON antes del RAG. Después, tardaba tres o cuatro. No porque hubiera menos que revisar, sino porque el JSON ya le decía cuándo prestar atención: las alertas de posibles duplicados marcaban exactamente dónde mirar.

Las contradicciones entre módulos se detectaron antes. No todas —como dijimos, el RAG tiene límites—, pero suficientes para que David Sanz comentara en la revisión del sprint tres que era la primera vez en dos años que llegaban a una demo sin que el negocio señalara un comportamiento que contradecía algo que ya había pedido antes.

La métrica que más sorprendió al equipo fue la cobertura de flujos de error. Antes del RAG, los requisitos de Meridian tenían de media 1,2 excepciones documentadas. Después, 2,8. No porque Carlos se volviera más meticuloso: porque el contexto de flujos de error relacionados hacía que el LLM sugiriera excepciones que el analista no había considerado, y Carlos las aprobaba porque tenían sentido.

El sistema no es mágico. Sigue siendo el analista quien decide. Pero decide con más información y en menos tiempo.

---

## Tres puntos clave

- **RAG resuelve la amnesia del pipeline**: sin contexto del repositorio, el pipeline trata cada requisito como si fuera el primero. Con RAG, genera sabiendo qué existe ya, qué patrones usa el equipo y qué podría contradecirse.

- **El chunking semántico por bloque funcional es la decisión más importante de la arquitectura**: indexar cada bloque de la plantilla YAML como un chunk independiente permite búsquedas especializadas que maximizan la relevancia del contexto recuperado sin desperdiciar tokens.

- **El RAG mejora las probabilidades, no garantiza la perfección**: la revisión humana en el gate de aprobación sigue siendo la única garantía de calidad real. El RAG reduce la carga de esa revisión —señala dónde mirar— pero no la elimina.

---

## Pregunta de reflexión para el equipo

¿Cuántos requisitos del repositorio actual de tu proyecto contienen funcionalidad que ya está implementada, al menos parcialmente, en otro requisito del mismo módulo?

---

*El pipeline ya tiene memoria. En el Capítulo 11 añadiremos el siguiente nivel: la capacidad de detectar automáticamente qué artefactos ya generados quedan afectados cuando un requisito validado cambia, y de construir la trazabilidad completa desde el requisito de negocio hasta el test case ejecutado.*
