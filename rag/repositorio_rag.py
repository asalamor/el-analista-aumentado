# rag/repositorio_rag.py
"""
Arquitectura RAG para el repositorio de requisitos.
Gestiona la indexación de requisitos en pgvector y las consultas
semánticas para recuperar contexto relevante antes de generar artefactos.

Punto 7 del modelo operativo AI-ready.
"""

import json
import hashlib
import asyncio
import psycopg2
from dataclasses import dataclass
from typing import Optional, NamedTuple
from datetime import datetime


@dataclass
class Chunk:
    """Unidad de indexación del repositorio de requisitos."""
    id: str
    texto: str
    tipo: str
    metadatos: dict


class ResultadoRetrieval(NamedTuple):
    chunk_id: str
    texto: str
    similitud: float
    metadatos: dict
    tipo: str


class RepositorioRequisitosRAG:
    """
    Gestiona la indexación y consulta del repositorio de requisitos
    usando pgvector como vector store.
    """

    def __init__(self, db_config: dict, openai_client):
        self.db = psycopg2.connect(**db_config)
        self.openai = openai_client
        self._inicializar_schema()

    def _inicializar_schema(self):
        with self.db.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chunks_requisitos (
                    id              TEXT PRIMARY KEY,
                    texto           TEXT NOT NULL,
                    tipo            TEXT NOT NULL,
                    embedding       vector(1536),
                    metadatos       JSONB,
                    hash_contenido  TEXT,
                    fecha_indexado  TIMESTAMP DEFAULT NOW(),
                    activo          BOOLEAN DEFAULT TRUE
                );
                CREATE INDEX IF NOT EXISTS idx_chunks_embedding
                    ON chunks_requisitos
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 128);
                CREATE INDEX IF NOT EXISTS idx_chunks_tipo
                    ON chunks_requisitos (tipo);
                CREATE INDEX IF NOT EXISTS idx_chunks_metadatos
                    ON chunks_requisitos USING gin (metadatos);
            """)
            self.db.commit()

    def embeder_texto(self, texto: str) -> list[float]:
        """Genera el embedding del texto usando el modelo configurado."""
        respuesta = self.openai.embeddings.create(
            model="text-embedding-3-large",
            input=texto,
            dimensions=1536
        )
        return respuesta.data[0].embedding

    def indexar_chunk(self, chunk: Chunk) -> bool:
        """Indexa un chunk. Retorna True si es nuevo o fue actualizado."""
        hash_actual = hashlib.md5(chunk.texto.encode()).hexdigest()

        with self.db.cursor() as cur:
            cur.execute(
                "SELECT hash_contenido FROM chunks_requisitos WHERE id = %s",
                (chunk.id,)
            )
            fila = cur.fetchone()
            if fila and fila[0] == hash_actual:
                return False

            embedding = self.embeder_texto(chunk.texto)
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
                chunk.id, chunk.texto, chunk.tipo,
                embedding, json.dumps(chunk.metadatos), hash_actual
            ))
            self.db.commit()
            return True

    def indexar_requisito(self, requisito: dict) -> dict:
        """Chunkeriza un requisito e indexa todos sus chunks."""
        chunks = chunkerizar_requisito(requisito)
        resultado = {"indexados": 0, "sin_cambios": 0, "errores": []}
        for chunk in chunks:
            try:
                if self.indexar_chunk(chunk):
                    resultado["indexados"] += 1
                else:
                    resultado["sin_cambios"] += 1
            except Exception as e:
                resultado["errores"].append({"chunk_id": chunk.id, "error": str(e)})
        return resultado

    def desactivar_requisito(self, requisito_id: str):
        """Marca como inactivos todos los chunks de un requisito deprecado."""
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE chunks_requisitos SET activo = FALSE "
                "WHERE metadatos->>'requisito_id' = %s",
                (requisito_id,)
            )
            self.db.commit()


def chunkerizar_requisito(requisito: dict) -> list[Chunk]:
    """Convierte un dict de requisito en chunks semánticos independientes."""
    req_id  = requisito.get("id", "")
    epica   = requisito.get("epica", "")
    estado  = requisito.get("estado", "")
    version = requisito.get("version", "1.0")

    metadatos_base = {
        "requisito_id": req_id,
        "epica": epica, "estado": estado, "version": version,
        "actor": requisito.get("actor", ""),
        "prioridad": requisito.get("prioridad", "")
    }

    chunks = []

    # Chunk 1: Identidad completa
    texto_id = (
        f"Requisito {req_id}: {requisito.get('titulo', '')}\n"
        f"Módulo: {requisito.get('modulo', '')} ({epica})\n"
        f"Actor: {requisito.get('actor', '')}\n"
        f"Descripción: {requisito.get('descripcion', '')}\n"
        f"Evento disparador: {requisito.get('evento_disparador', '')}\n"
        f"Objetivo: {requisito.get('objetivo_negocio', '')}"
    ).strip()
    chunks.append(Chunk(
        id=f"{req_id}::identidad", texto=texto_id,
        tipo="identidad_requisito",
        metadatos={**metadatos_base, "chunk_tipo": "identidad"}
    ))

    # Chunk 2: Reglas de negocio
    reglas = requisito.get("reglas_negocio", [])
    if reglas:
        reglas_txt = "\n".join(f"- {r}" for r in reglas)
        chunks.append(Chunk(
            id=f"{req_id}::reglas_negocio",
            texto=f"Reglas de negocio de {req_id} ({requisito.get('titulo', '')}):\n{reglas_txt}",
            tipo="reglas_negocio",
            metadatos={**metadatos_base, "chunk_tipo": "reglas_negocio"}
        ))

    # Chunk 3: Criterios de aceptación (uno por criterio)
    for ac in requisito.get("criterios_aceptacion", []):
        texto_ac = (
            f"Criterio {ac.get('id', '')} de {req_id}:\n"
            f"Dado: {ac.get('dado', '')}\n"
            f"Cuando: {ac.get('cuando', '')}\n"
            f"Entonces: {ac.get('entonces', '')}\n"
            f"Tipo: {ac.get('tipo', 'positivo')}"
        ).strip()
        chunks.append(Chunk(
            id=f"{req_id}::{ac.get('id', '')}",
            texto=texto_ac, tipo="criterio_aceptacion",
            metadatos={
                **metadatos_base,
                "chunk_tipo": "criterio_aceptacion",
                "ac_id": ac.get("id", ""),
                "ac_tipo": ac.get("tipo", "positivo")
            }
        ))

    # Chunk 4: Datos de interfaz
    datos_entrada = requisito.get("datos_entrada", [])
    datos_salida  = requisito.get("datos_salida", {})
    if datos_entrada or datos_salida:
        campos_e = [f"{d['nombre']} ({d.get('tipo','?')})" for d in datos_entrada]
        campos_s = datos_salida.get("campos", []) if isinstance(datos_salida, dict) else []
        texto_datos = (
            f"Datos de {req_id} ({requisito.get('titulo', '')}):\n"
            f"Entradas: {', '.join(campos_e) or 'ninguna'}\n"
            f"Salidas: {', '.join(campos_s) or 'ninguna'}"
        )
        chunks.append(Chunk(
            id=f"{req_id}::datos",
            texto=texto_datos, tipo="datos_interfaz",
            metadatos={**metadatos_base, "chunk_tipo": "datos_interfaz"}
        ))

    return chunks


class MotorConsultaRAG:
    """Ejecuta consultas al vector store y ensambla el contexto."""

    UMBRAL_SIMILITUD = 0.72
    TOP_K = 5

    def __init__(self, repositorio: RepositorioRequisitosRAG):
        self.repo = repositorio

    def buscar_por_similitud(
        self,
        query_texto: str,
        filtros: dict = None,
        top_k: int = None
    ) -> list[ResultadoRetrieval]:
        """Búsqueda híbrida: similitud semántica + filtros por metadatos."""
        top_k = top_k or self.TOP_K
        embedding = self.repo.embeder_texto(query_texto)

        where_clauses = ["activo = TRUE"]
        params = [embedding]

        if filtros:
            for clave, valor in filtros.items():
                where_clauses.append(f"metadatos->>'{clave}' = %s")
                params.append(str(valor))

        where_sql = " AND ".join(where_clauses)

        with self.repo.db.cursor() as cur:
            cur.execute(f"""
                SELECT id, texto,
                       1 - (embedding <=> %s::vector) AS similitud,
                       metadatos, tipo
                FROM chunks_requisitos
                WHERE {where_sql}
                  AND 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [embedding] + params + [embedding, self.UMBRAL_SIMILITUD, top_k])

            return [
                ResultadoRetrieval(
                    chunk_id=f[0], texto=f[1],
                    similitud=float(f[2]), metadatos=f[3], tipo=f[4]
                )
                for f in cur.fetchall()
            ]

    async def recuperar_contexto_completo(self, requisito: dict) -> dict:
        """Ejecuta 5 consultas paralelas y ensambla el contexto."""
        epica  = requisito.get("epica", "")
        actor  = requisito.get("actor", "")
        titulo = requisito.get("titulo", "")
        desc   = requisito.get("descripcion", "")

        def q1():
            return self.buscar_por_similitud(
                f"{titulo}. {desc}", {"estado": "validado"}, 5
            )
        def q2():
            return self.buscar_por_similitud(
                f"requisitos del módulo {epica}",
                {"epica": epica, "estado": "validado"}, 8
            )
        def q3():
            return self.buscar_por_similitud(
                f"acciones del actor {actor}",
                {"actor": actor, "chunk_tipo": "identidad"}, 5
            )
        def q4():
            reglas = " ".join(requisito.get("reglas_negocio", []))
            return self.buscar_por_similitud(
                reglas,
                {"epica": epica, "chunk_tipo": "reglas_negocio"}, 5
            )
        def q5():
            ac_txt = " ".join([
                f"{ac.get('dado','')} {ac.get('cuando','')} {ac.get('entonces','')}"
                for ac in requisito.get("criterios_aceptacion", [])
            ])
            return self.buscar_por_similitud(
                ac_txt, {"chunk_tipo": "criterio_aceptacion"}, 5
            )

        resultados = [q1(), q2(), q3(), q4(), q5()]
        categorias = [
            "funcionalidad_similar", "mismo_modulo", "mismo_actor",
            "reglas_relacionadas", "criterios_similares"
        ]

        chunks_vistos = set()
        contexto = {cat: [] for cat in categorias}

        for i, resultado_consulta in enumerate(resultados):
            for chunk in resultado_consulta:
                if chunk.chunk_id not in chunks_vistos:
                    chunks_vistos.add(chunk.chunk_id)
                    contexto[categorias[i]].append({
                        "chunk_id": chunk.chunk_id,
                        "texto": chunk.texto,
                        "similitud": chunk.similitud,
                        "metadatos": chunk.metadatos
                    })

        return contexto
