# Análisis de cobertura de negocio

## Qué resuelve este punto y por qué no es obvio

La trazabilidad del modelo operativo, tal como está construida en el punto 9, recorre la cadena hacia abajo: de requisito a historia, de historia a tarea, de tarea a commit. Es una trazabilidad de implementación. Responde a la pregunta de si lo que está en el código corresponde a lo que estaba en el requisito.

Lo que esa trazabilidad no responde es la pregunta inversa: si los requisitos del proyecto cubren los objetivos de negocio que la organización declaró al inicio. Esa pregunta es la que hace el product owner cuando prepara una demo, la dirección cuando revisa el avance del trimestre, o el analista cuando sospecha que el backlog ha derivado de su propósito original.

El análisis de cobertura de negocio cierra ese hueco. Cruza el catálogo de objetivos de negocio del proyecto con el repositorio de requisitos para producir una matriz que responde, por cada objetivo, cuántos requisitos lo soportan, cuáles son, en qué estado están y qué porcentaje del objetivo se considera cubierto por los artefactos ya generados.

El resultado no es solo un informe de auditoría. Es una herramienta de toma de decisiones: identifica objetivos de negocio sin cobertura antes de que el product owner los descubra en producción, detecta requisitos huérfanos que no contribuyen a ningún objetivo declarado, y cuantifica el avance funcional del proyecto en términos que la dirección entiende sin necesidad de contar historias de usuario.

---

## El catálogo de objetivos de negocio

El catálogo es la pieza que hace posible el análisis. Sin objetivos declarados de forma estructurada, el cruce es imposible o trivialmente superficial. El catálogo no es un documento de visión libre: es un YAML estructurado con campos que el sistema puede procesar de forma determinista.

### Quién lo crea y cuándo

El catálogo se crea en la Fase 0 del roadmap, junto con la plantilla de requisitos y el glosario. Lo redacta el analista funcional en colaboración con el product owner, a partir de la documentación de negocio existente: el plan de proyecto, la propuesta de valor, los OKRs del trimestre o el acta de kick-off.

No es un documento exhaustivo. Cinco a quince objetivos bien definidos son suficientes para la mayoría de proyectos. Un catálogo con más de veinte objetivos suele ser señal de que se están capturando funcionalidades como objetivos, no resultados de negocio.

La diferencia entre un objetivo de negocio y una funcionalidad es la unidad de medida: un objetivo de negocio se mide en términos del negocio (tiempo, coste, tasa de error, satisfacción del cliente), no en términos del sistema (pantallas, botones, módulos).

| Formulación incorrecta | Formulación correcta |
|---|---|
| "Implementar el módulo de facturación" | "Reducir el tiempo de cierre contable mensual de 3 días a 4 horas" |
| "Mejorar la búsqueda de facturas" | "Eliminar la búsqueda manual de facturas como causa de retraso en el cierre" |
| "Añadir filtros al listado" | "Permitir que el gestor localice cualquier factura en menos de 30 segundos" |

### Estructura del catálogo

```yaml
# objetivos-negocio/catalogo-objetivos.yaml

metadata:
  proyecto: "Sistema de Gestión de Facturación"
  version: "1.2"
  propietario: "Ana López (Product Owner)"
  fecha_creacion: "2025-01-15"
  fecha_ultima_revision: "2025-04-01"
  proxima_revision: "2025-07-01"
  nota: >
    Los objetivos se revisan al inicio de cada trimestre con la dirección.
    Los cambios de versión menor (1.1, 1.2) indican ajustes de redacción.
    Los cambios de versión mayor (2.0) indican cambio de estrategia que
    requiere re-evaluar toda la cobertura del repositorio.

objetivos:
  - id: OBJ-001
    titulo: "Reducir el tiempo de cierre contable mensual"
    descripcion: >
      El equipo de contabilidad dedica actualmente entre 2 y 3 días
      laborables al cierre mensual. El objetivo es reducirlo a menos
      de 4 horas mediante la automatización de la búsqueda, validación
      y conciliación de facturas.
    area_negocio: "Dirección Financiera"
    stakeholder_principal: "Ana López"
    kpi:
      metrica: "Tiempo de cierre contable mensual"
      valor_actual: "2-3 días laborables"
      valor_objetivo: "< 4 horas"
      unidad: "horas"
      forma_medicion: >
        Registro de tiempo en el sistema de gestión de proyectos interno.
        Medición durante los 3 meses siguientes al despliegue.
    prioridad: critica
    plazo: "Q2 2025"
    estado: activo
    dependencias_externas: []
    notas: >
      Este objetivo es el más crítico del proyecto. El resto de objetivos
      son instrumentales respecto a este.

  - id: OBJ-002
    titulo: "Eliminar el procesamiento manual de facturas recibidas"
    descripcion: >
      Actualmente el 60% de las facturas de proveedor se registran
      manualmente copiando datos del correo electrónico. El objetivo
      es que el 90% de las facturas se registren de forma automática
      mediante integración con el buzón corporativo y reconocimiento
      de datos.
    area_negocio: "Dirección Financiera"
    stakeholder_principal: "Ana López"
    kpi:
      metrica: "Porcentaje de facturas registradas automáticamente"
      valor_actual: "40%"
      valor_objetivo: "> 90%"
      unidad: "porcentaje"
      forma_medicion: >
        Log del sistema durante el primer mes de operación completa.
    prioridad: alta
    plazo: "Q3 2025"
    estado: activo
    dependencias_externas:
      - "Acceso al buzón corporativo de facturas"
      - "Contrato con proveedor de reconocimiento de documentos"
    notas: ""

  - id: OBJ-003
    titulo: "Garantizar trazabilidad completa del ciclo de aprobación"
    descripcion: >
      En el proceso actual no hay registro de quién aprobó qué factura
      ni cuándo. El objetivo es que el 100% de las aprobaciones queden
      registradas con usuario, fecha, hora y justificación, y que ese
      registro sea auditable en cualquier momento.
    area_negocio: "Dirección Financiera / Auditoría Interna"
    stakeholder_principal: "Roberto Vega (Auditoría)"
    kpi:
      metrica: "Porcentaje de aprobaciones con registro completo"
      valor_actual: "0%"
      valor_objetivo: "100%"
      unidad: "porcentaje"
      forma_medicion: >
        Consulta al log de auditoría del sistema durante las primeras
        4 semanas de operación.
    prioridad: alta
    plazo: "Q2 2025"
    estado: activo
    dependencias_externas: []
    notas: >
      Requerimiento implícito de la auditoría interna anual programada
      para noviembre de 2025.

  - id: OBJ-004
    titulo: "Reducir los errores de pago por facturas duplicadas o incorrectas"
    descripcion: >
      Se detectan entre 3 y 5 errores de pago mensuales atribuibles
      a facturas duplicadas o a facturas registradas con datos incorrectos.
      El objetivo es reducirlos a cero mediante validación automática
      antes de la aprobación.
    area_negocio: "Dirección Financiera / Tesorería"
    stakeholder_principal: "Carmen Ruiz (Tesorería)"
    kpi:
      metrica: "Errores de pago mensuales por causa de factura"
      valor_actual: "3-5 por mes"
      valor_objetivo: "0"
      unidad: "número de incidencias"
      forma_medicion: >
        Registro de incidencias de tesorería durante 3 meses consecutivos
        tras el despliegue completo.
    prioridad: alta
    plazo: "Q3 2025"
    estado: activo
    dependencias_externas: []
    notas: ""

  - id: OBJ-005
    titulo: "Habilitar el acceso a información de facturación para los gestores de área"
    descripcion: >
      Los gestores de área no tienen acceso directo al estado de las
      facturas relacionadas con sus proveedores. El objetivo es que
      puedan consultar el estado sin intermediación del equipo financiero,
      reduciendo las consultas internas al departamento de contabilidad
      en al menos un 70%.
    area_negocio: "Múltiples áreas"
    stakeholder_principal: "Varios (gestores de área)"
    kpi:
      metrica: "Consultas internas al departamento de contabilidad por estado de factura"
      valor_actual: "~40 consultas/mes"
      valor_objetivo: "< 12 consultas/mes"
      unidad: "número de consultas mensuales"
      forma_medicion: >
        Registro en el sistema de tickets internos del departamento.
    prioridad: media
    plazo: "Q4 2025"
    estado: activo
    dependencias_externas: []
    notas: ""
```

### Vínculo entre objetivos y requisitos

La vinculación puede ser explícita o inferida. La vinculación explícita es más precisa pero exige que el analista la declare en el YAML del requisito. La vinculación inferida, basada en similitud semántica, es automática pero menos determinista.

El modelo usa ambas en capas: primero busca vinculaciones explícitas declaradas en el campo `objetivos_negocio` del requisito, y luego completa la cobertura con vinculaciones inferidas por RAG para los requisitos que no declaran objetivos. Las vinculaciones inferidas tienen un nivel de confianza más bajo y se presentan diferenciadas en el informe.

Para soportar la vinculación explícita, la plantilla YAML del punto 1 se extiende con un campo opcional en el Bloque 2:

```yaml
# Adición al Bloque 2 de la plantilla de requisito

objetivos_negocio:
  - id: OBJ-001
    contribucion: directa
    # directa   → el requisito implementa funcionalidad que contribuye
    #             de forma principal al objetivo
    # indirecta → el requisito implementa funcionalidad de soporte
    #             que facilita el objetivo pero no lo implementa directamente
    justificacion: >
      El filtrado de facturas por fecha es la funcionalidad más solicitada
      por el equipo de contabilidad para acelerar el cierre mensual.
  - id: OBJ-004
    contribucion: indirecta
    justificacion: >
      Un filtrado eficaz reduce la probabilidad de aprobar facturas
      duplicadas al hacer más visible el historial del período.
```

---

## Arquitectura del analizador de cobertura

El analizador tiene cuatro componentes que se ejecutan en secuencia para producir la matriz de cobertura completa.

```
Catálogo de objetivos
        │
        ▼
[Componente 1] Indexación de objetivos en el vector store
        │
        ▼
[Componente 2] Resolución de vínculos
        │   ├── Explícitos: desde el campo objetivos_negocio del requisito
        │   └── Inferidos: por similitud semántica RAG
        │
        ▼
[Componente 3] Cálculo de métricas de cobertura por objetivo
        │
        ▼
[Componente 4] Generación del informe y detección de gaps
```

---

## Componente 1: indexación de objetivos

Los objetivos se indexan en el mismo vector store del punto 7 con metadatos específicos, igual que los ejemplos de referencia del punto de few-shot. Esto permite que el motor de consulta RAG los recupere cuando genera contexto para nuevos requisitos, sugiriendo al analista qué objetivos podría cubrir el requisito en borrador.

```python
# indexador_objetivos.py

import yaml
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ChunkObjetivo:
    id: str
    texto: str
    metadatos: dict


def indexar_catalogo_objetivos(
    ruta_catalogo: str,
    repositorio_rag
) -> dict:
    """
    Indexa todos los objetivos del catálogo en el vector store.
    Crea un chunk por objetivo con el texto enriquecido para
    maximizar la recuperación semántica.
    """
    with open(ruta_catalogo, encoding="utf-8") as f:
        catalogo = yaml.safe_load(f)

    objetivos = catalogo.get("objetivos", [])
    indexados = 0
    errores = []

    for obj in objetivos:
        if obj.get("estado") == "cancelado":
            continue

        # Texto enriquecido para el embedding
        # Incluir título, descripción, KPI y área para maximizar
        # la recuperación en consultas semánticas variadas
        texto = f"""
Objetivo de negocio {obj['id']}: {obj['titulo']}
Área: {obj.get('area_negocio', '')}
Descripción: {obj.get('descripcion', '')}
Métrica: {obj.get('kpi', {}).get('metrica', '')}
Valor objetivo: {obj.get('kpi', {}).get('valor_objetivo', '')}
Prioridad: {obj.get('prioridad', '')}
Plazo: {obj.get('plazo', '')}
        """.strip()

        chunk = ChunkObjetivo(
            id=f"OBJETIVO::{obj['id']}",
            texto=texto,
            metadatos={
                "tipo": "objetivo_negocio",
                "objetivo_id": obj["id"],
                "titulo": obj["titulo"],
                "area_negocio": obj.get("area_negocio", ""),
                "stakeholder": obj.get("stakeholder_principal", ""),
                "prioridad": obj.get("prioridad", ""),
                "plazo": obj.get("plazo", ""),
                "estado": obj.get("estado", "activo"),
                "kpi_metrica": obj.get("kpi", {}).get("metrica", ""),
                "kpi_objetivo": obj.get("kpi", {}).get("valor_objetivo", "")
            }
        )

        try:
            # Reutilizar el método de indexación del repositorio RAG
            import hashlib
            hash_contenido = hashlib.md5(texto.encode()).hexdigest()
            embedding = repositorio_rag.embeder_texto(texto)

            import psycopg2, json
            with psycopg2.connect(**repositorio_rag.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO chunks_requisitos
                            (id, texto, tipo, embedding, metadatos, hash_contenido)
                        VALUES (%s, %s, %s, %s::vector, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            texto          = EXCLUDED.texto,
                            embedding      = EXCLUDED.embedding,
                            metadatos      = EXCLUDED.metadatos,
                            hash_contenido = EXCLUDED.hash_contenido,
                            fecha_indexado = NOW(),
                            activo         = TRUE
                    """, (
                        chunk.id,
                        chunk.texto,
                        "objetivo_negocio",
                        embedding,
                        json.dumps(chunk.metadatos),
                        hash_contenido
                    ))
                conn.commit()
            indexados += 1

        except Exception as e:
            errores.append({"objetivo_id": obj["id"], "error": str(e)})

    return {
        "total_objetivos": len(objetivos),
        "indexados": indexados,
        "errores": errores
    }
```

---

## Componente 2: resolución de vínculos

El resolvedor procesa todos los requisitos del repositorio y produce un grafo de vínculos entre requisitos y objetivos. Para cada vínculo registra su origen (explícito o inferido) y su nivel de confianza.

```python
# resolvedor_vinculos.py

import yaml
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class VinculoReqObjetivo:
    requisito_id: str
    objetivo_id: str
    contribucion: str           # directa │ indirecta │ inferida
    confianza: float            # 1.0 explícito, 0.5-0.9 inferido
    justificacion: str
    estado_requisito: str
    epica_requisito: str


class ResolvedorVinculos:
    """
    Resuelve los vínculos entre requisitos y objetivos de negocio
    combinando declaraciones explícitas y similitud semántica.
    """

    UMBRAL_VINCULO_INFERIDO = 0.72
    # Por debajo de este umbral, la similitud no es suficiente para
    # inferir una contribución al objetivo

    UMBRAL_VINCULO_FUERTE = 0.82
    # Por encima de este umbral, el vínculo inferido se considera
    # de contribución directa; entre ambos umbrales, indirecta

    def __init__(self, repositorio_rag, ruta_requisitos: str):
        self.rag = repositorio_rag
        self.ruta_requisitos = ruta_requisitos

    def resolver_todos(self, objetivos: list[dict]) -> list[VinculoReqObjetivo]:
        """
        Resuelve todos los vínculos entre el repositorio de requisitos
        y el catálogo de objetivos. Combina vínculos explícitos e inferidos.
        """
        vinculos = []
        vinculos_explicitos = self._resolver_explicitos()
        vinculos.extend(vinculos_explicitos)

        # Pares ya vinculados explícitamente (no re-inferir)
        pares_explicitos = {
            (v.requisito_id, v.objetivo_id) for v in vinculos_explicitos
        }

        # Completar con vínculos inferidos para el resto de requisitos
        vinculos_inferidos = self._inferir_vinculos(
            objetivos, pares_explicitos
        )
        vinculos.extend(vinculos_inferidos)

        return vinculos

    def _resolver_explicitos(self) -> list[VinculoReqObjetivo]:
        """
        Extrae los vínculos declarados en el campo objetivos_negocio
        de cada requisito del repositorio.
        """
        vinculos = []

        for root, _, files in os.walk(self.ruta_requisitos):
            for archivo in files:
                if not archivo.endswith(".yaml"):
                    continue
                ruta = os.path.join(root, archivo)
                try:
                    with open(ruta, encoding="utf-8") as f:
                        req = yaml.safe_load(f)

                    if not req or req.get("estado") not in (
                        "en-revision", "validado"
                    ):
                        continue

                    for vinculo in req.get("objetivos_negocio", []):
                        vinculos.append(VinculoReqObjetivo(
                            requisito_id=req["id"],
                            objetivo_id=vinculo["id"],
                            contribucion=vinculo.get(
                                "contribucion", "directa"
                            ),
                            confianza=1.0,
                            justificacion=vinculo.get("justificacion", ""),
                            estado_requisito=req.get("estado", ""),
                            epica_requisito=req.get("epica", "")
                        ))

                except Exception as e:
                    continue

        return vinculos

    def _inferir_vinculos(
        self,
        objetivos: list[dict],
        pares_excluidos: set
    ) -> list[VinculoReqObjetivo]:
        """
        Infiere vínculos por similitud semántica para los requisitos
        que no tienen declaraciones explícitas.
        """
        vinculos = []
        requisitos = self._cargar_requisitos_sin_objetivo()

        for req in requisitos:
            req_id = req.get("id", "")
            texto_req = (
                f"{req.get('titulo', '')} "
                f"{req.get('descripcion', '')} "
                f"{req.get('objetivo_negocio', '')}"
            )

            # Buscar objetivos semánticamente similares
            resultados = self.rag.buscar_por_similitud(
                query_texto=texto_req,
                filtros={"tipo": "objetivo_negocio"},
                top_k=3
            )

            for resultado in resultados:
                obj_id = resultado.metadatos.get("objetivo_id", "")

                if not obj_id:
                    continue
                if (req_id, obj_id) in pares_excluidos:
                    continue
                if resultado.similitud < self.UMBRAL_VINCULO_INFERIDO:
                    continue

                contribucion = (
                    "directa"
                    if resultado.similitud >= self.UMBRAL_VINCULO_FUERTE
                    else "indirecta"
                )

                vinculos.append(VinculoReqObjetivo(
                    requisito_id=req_id,
                    objetivo_id=obj_id,
                    contribucion=contribucion,
                    confianza=round(resultado.similitud, 2),
                    justificacion=(
                        f"Inferido por similitud semántica "
                        f"({resultado.similitud:.0%}). Revisar manualmente."
                    ),
                    estado_requisito=req.get("estado", ""),
                    epica_requisito=req.get("epica", "")
                ))

        return vinculos

    def _cargar_requisitos_sin_objetivo(self) -> list[dict]:
        """
        Carga los requisitos que no tienen ningún objetivo declarado
        explícitamente, para completar con inferencia.
        """
        requisitos = []
        for root, _, files in os.walk(self.ruta_requisitos):
            for archivo in files:
                if not archivo.endswith(".yaml"):
                    continue
                try:
                    with open(
                        os.path.join(root, archivo), encoding="utf-8"
                    ) as f:
                        req = yaml.safe_load(f)

                    if not req:
                        continue
                    if req.get("estado") not in ("en-revision", "validado"):
                        continue
                    # Solo incluir los que no tienen objetivos explícitos
                    if not req.get("objetivos_negocio"):
                        requisitos.append(req)

                except Exception:
                    continue

        return requisitos
```

---

## Componente 3: cálculo de métricas de cobertura

Con el grafo de vínculos resuelto, el calculador produce las métricas por objetivo: cuántos requisitos lo cubren, qué estado tienen, qué porcentaje del objetivo está implementado y qué porcentaje está aún en borrador o pendiente.

```python
# calculador_cobertura.py

from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class MetricasObjetivo:
    objetivo_id: str
    titulo: str
    prioridad: str
    kpi_objetivo: str
    # Requisitos vinculados
    total_vinculos: int
    vinculos_directos: int
    vinculos_indirectos: int
    vinculos_inferidos: int
    # Desglose por estado
    requisitos_validados: list[str]
    requisitos_en_revision: list[str]
    requisitos_borrador: list[str]
    # Artefactos generados
    historias_generadas: int
    test_cases_generados: int
    # Cobertura calculada
    porcentaje_cobertura: float
    nivel_cobertura: str      # completa │ alta │ media │ baja │ sin_cobertura
    cobertura_implementada: float   # solo requisitos validados con artefactos
    # Gaps
    gaps: list[str]


class CalculadorCobertura:
    """
    Calcula las métricas de cobertura de cada objetivo a partir
    del grafo de vínculos resuelto y el grafo de trazabilidad.
    """

    def calcular(
        self,
        objetivos: list[dict],
        vinculos: list[VinculoReqObjetivo],
        consultor_trazabilidad
    ) -> list[MetricasObjetivo]:
        """
        Calcula las métricas de cobertura para todos los objetivos.
        """
        # Agrupar vínculos por objetivo
        vinculos_por_objetivo = defaultdict(list)
        for v in vinculos:
            vinculos_por_objetivo[v.objetivo_id].append(v)

        metricas = []
        for obj in objetivos:
            if obj.get("estado") == "cancelado":
                continue

            obj_id = obj["id"]
            vinculos_obj = vinculos_por_objetivo.get(obj_id, [])
            metricas_obj = self._calcular_objetivo(
                obj, vinculos_obj, consultor_trazabilidad
            )
            metricas.append(metricas_obj)

        return sorted(
            metricas,
            key=lambda m: (
                {"critica": 0, "alta": 1, "media": 2, "baja": 3}.get(
                    m.prioridad, 4
                ),
                m.porcentaje_cobertura
            )
        )

    def _calcular_objetivo(
        self,
        objetivo: dict,
        vinculos: list[VinculoReqObjetivo],
        consultor_trazabilidad
    ) -> MetricasObjetivo:
        """Calcula las métricas para un objetivo específico."""

        if not vinculos:
            return MetricasObjetivo(
                objetivo_id=objetivo["id"],
                titulo=objetivo["titulo"],
                prioridad=objetivo.get("prioridad", ""),
                kpi_objetivo=objetivo.get("kpi", {}).get("valor_objetivo", ""),
                total_vinculos=0,
                vinculos_directos=0,
                vinculos_indirectos=0,
                vinculos_inferidos=0,
                requisitos_validados=[],
                requisitos_en_revision=[],
                requisitos_borrador=[],
                historias_generadas=0,
                test_cases_generados=0,
                porcentaje_cobertura=0.0,
                nivel_cobertura="sin_cobertura",
                cobertura_implementada=0.0,
                gaps=[
                    f"Sin requisitos vinculados al objetivo. "
                    f"Ninguna historia del backlog contribuye "
                    f"a '{objetivo['titulo']}'."
                ]
            )

        # Clasificar vínculos
        directos = [v for v in vinculos if v.contribucion == "directa" and v.confianza == 1.0]
        indirectos = [v for v in vinculos if v.contribucion == "indirecta" and v.confianza == 1.0]
        inferidos = [v for v in vinculos if v.confianza < 1.0]

        # Clasificar por estado
        req_validados = [v.requisito_id for v in vinculos if v.estado_requisito == "validado"]
        req_en_revision = [v.requisito_id for v in vinculos if v.estado_requisito == "en-revision"]
        req_borrador = [v.requisito_id for v in vinculos if v.estado_requisito == "borrador"]

        # Contar artefactos generados para los requisitos validados
        historias = 0
        test_cases = 0
        for req_id in req_validados:
            try:
                traza = consultor_trazabilidad.traza_completa_requisito(req_id)
                historias += len(traza.get("historias", []))
                test_cases += len(traza.get("test_cases", []))
            except Exception:
                pass

        # Calcular porcentaje de cobertura
        # Fórmula: los vínculos directos valen 1.0, los indirectos 0.5,
        # los inferidos su nivel de confianza. Los requisitos validados
        # ponderan al doble que los no validados.
        peso_total = 0.0
        peso_cubierto = 0.0

        for v in vinculos:
            peso_vinculo = (
                1.0 if v.contribucion == "directa" else 0.5
            ) * v.confianza

            multiplicador_estado = (
                2.0 if v.estado_requisito == "validado" else
                1.0 if v.estado_requisito == "en-revision" else
                0.5
            )

            peso_total += peso_vinculo * multiplicador_estado
            peso_cubierto += peso_vinculo * multiplicador_estado

        # Normalizar entre 0 y 100
        # La escala asume que con 3 requisitos directos validados
        # el objetivo tiene cobertura completa (100%)
        REQUISITOS_REFERENCIA_COMPLETA = 3.0
        peso_referencia = (
            1.0 * 2.0 * REQUISITOS_REFERENCIA_COMPLETA
        )  # 3 directos validados

        porcentaje = min(
            (peso_cubierto / peso_referencia) * 100, 100.0
        )
        porcentaje = round(porcentaje, 1)

        # Cobertura implementada (solo validados con historias)
        cobertura_impl = (
            min(historias / REQUISITOS_REFERENCIA_COMPLETA, 1.0) * 100
            if historias > 0 else 0.0
        )

        # Nivel de cobertura
        nivel = (
            "completa"     if porcentaje >= 90 else
            "alta"         if porcentaje >= 65 else
            "media"        if porcentaje >= 35 else
            "baja"         if porcentaje > 0  else
            "sin_cobertura"
        )

        # Detectar gaps
        gaps = self._detectar_gaps(
            objetivo, vinculos, req_validados, historias, test_cases
        )

        return MetricasObjetivo(
            objetivo_id=objetivo["id"],
            titulo=objetivo["titulo"],
            prioridad=objetivo.get("prioridad", ""),
            kpi_objetivo=objetivo.get("kpi", {}).get("valor_objetivo", ""),
            total_vinculos=len(vinculos),
            vinculos_directos=len(directos),
            vinculos_indirectos=len(indirectos),
            vinculos_inferidos=len(inferidos),
            requisitos_validados=req_validados,
            requisitos_en_revision=req_en_revision,
            requisitos_borrador=req_borrador,
            historias_generadas=historias,
            test_cases_generados=test_cases,
            porcentaje_cobertura=porcentaje,
            nivel_cobertura=nivel,
            cobertura_implementada=round(cobertura_impl, 1),
            gaps=gaps
        )

    def _detectar_gaps(
        self,
        objetivo: dict,
        vinculos: list[VinculoReqObjetivo],
        req_validados: list[str],
        historias: int,
        test_cases: int
    ) -> list[str]:
        """Identifica los gaps de cobertura específicos del objetivo."""
        gaps = []

        # Gap: sin vínculos directos
        directos_validados = [
            v for v in vinculos
            if v.contribucion == "directa"
            and v.confianza == 1.0
            and v.estado_requisito == "validado"
        ]
        if not directos_validados:
            gaps.append(
                "Sin requisitos directos validados. La cobertura actual "
                "se basa en contribuciones indirectas o inferidas."
            )

        # Gap: sin historias generadas pese a tener requisitos validados
        if req_validados and historias == 0:
            gaps.append(
                f"{len(req_validados)} requisitos validados sin historias "
                f"de usuario generadas. Ejecutar el pipeline de generación."
            )

        # Gap: sin test cases
        if historias > 0 and test_cases == 0:
            gaps.append(
                f"{historias} historias generadas sin test cases asociados. "
                f"La implementación no tiene cobertura de pruebas verificable."
            )

        # Gap: dependencias externas no resueltas
        deps_externas = objetivo.get("dependencias_externas", [])
        if deps_externas:
            gaps.append(
                f"El objetivo tiene {len(deps_externas)} dependencias externas "
                f"que pueden bloquear su cumplimiento: "
                f"{'; '.join(deps_externas[:2])}."
            )

        # Gap: solo vínculos inferidos (sin declaraciones explícitas)
        explicitos = [v for v in vinculos if v.confianza == 1.0]
        if not explicitos and vinculos:
            gaps.append(
                "Todos los vínculos son inferidos por similitud semántica. "
                "Ningún analista ha declarado explícitamente la contribución "
                "de estos requisitos al objetivo. Revisar y confirmar."
            )

        return gaps
```

---

## Componente 4: generación del informe

El informe de cobertura es el artefacto principal que consume el product owner y la dirección. Existe en tres formatos con propósitos distintos.

### Informe ejecutivo para dirección

```python
# generador_informe_cobertura.py

from datetime import datetime


class GeneradorInformeCobertura:
    """
    Genera los informes de cobertura de negocio en múltiples formatos.
    """

    def generar_markdown(
        self,
        metricas: list[MetricasObjetivo],
        catalogo_meta: dict,
        requisitos_huerfanos: list[str]
    ) -> str:
        """
        Genera el informe completo en Markdown para Confluence o GitHub.
        """
        fecha = datetime.now().strftime("%Y-%m-%d")
        total_obj = len(metricas)
        completos = sum(1 for m in metricas if m.nivel_cobertura == "completa")
        altos = sum(1 for m in metricas if m.nivel_cobertura == "alta")
        sin_cobertura = sum(1 for m in metricas if m.nivel_cobertura == "sin_cobertura")

        cobertura_media = (
            sum(m.porcentaje_cobertura for m in metricas) / total_obj
            if total_obj > 0 else 0
        )

        semaforo = (
            "🟢" if cobertura_media >= 75 else
            "🟡" if cobertura_media >= 45 else
            "🔴"
        )

        md = f"""# Análisis de cobertura de negocio
**Proyecto:** {catalogo_meta.get('proyecto', '')}
**Fecha:** {fecha}
**Versión del catálogo:** {catalogo_meta.get('version', '')}

---

## Resumen ejecutivo

{semaforo} La cobertura media del catálogo de objetivos es del **{cobertura_media:.0f}%**.

| Métrica | Valor |
|---|---|
| Objetivos analizados | {total_obj} |
| Cobertura completa (≥90%) | {completos} |
| Cobertura alta (65–89%) | {altos} |
| Sin cobertura | {sin_cobertura} |
| Requisitos sin objetivo declarado | {len(requisitos_huerfanos)} |

"""
        # Alertas críticas al inicio
        criticos_sin_cobertura = [
            m for m in metricas
            if m.nivel_cobertura == "sin_cobertura"
            and m.prioridad == "critica"
        ]
        if criticos_sin_cobertura:
            md += "### ⚠ Objetivos críticos sin cobertura\n\n"
            for m in criticos_sin_cobertura:
                md += (
                    f"- **{m.objetivo_id}**: {m.titulo} "
                    f"— KPI objetivo: {m.kpi_objetivo}\n"
                )
            md += "\n---\n\n"

        # Tabla de cobertura por objetivo
        md += "## Cobertura por objetivo\n\n"
        md += (
            "| ID | Objetivo | Prioridad | Cobertura | Nivel | "
            "Req validados | Historias | TCs |\n"
        )
        md += "|---|---|---|---|---|---|---|---|\n"

        for m in metricas:
            barra = self._barra_progreso(m.porcentaje_cobertura)
            icono = {
                "completa":     "✅",
                "alta":         "🟢",
                "media":        "🟡",
                "baja":         "🔴",
                "sin_cobertura":"⛔"
            }.get(m.nivel_cobertura, "?")

            md += (
                f"| {m.objetivo_id} "
                f"| {m.titulo[:45]}{'...' if len(m.titulo) > 45 else ''} "
                f"| {m.prioridad} "
                f"| {barra} {m.porcentaje_cobertura:.0f}% "
                f"| {icono} {m.nivel_cobertura} "
                f"| {len(m.requisitos_validados)} "
                f"| {m.historias_generadas} "
                f"| {m.test_cases_generados} |\n"
            )

        md += "\n---\n\n"

        # Detalle por objetivo
        md += "## Detalle por objetivo\n\n"
        for m in metricas:
            md += self._seccion_objetivo(m)

        # Requisitos huérfanos
        if requisitos_huerfanos:
            md += "---\n\n## Requisitos sin objetivo asignado\n\n"
            md += (
                f"Los siguientes {len(requisitos_huerfanos)} requisitos "
                f"no contribuyen a ningún objetivo del catálogo según "
                f"las declaraciones explícitas ni la inferencia semántica. "
                f"Pueden indicar funcionalidad fuera del alcance aprobado "
                f"o objetivos del catálogo que necesitan actualización.\n\n"
            )
            for req_id in requisitos_huerfanos[:20]:
                md += f"- {req_id}\n"
            if len(requisitos_huerfanos) > 20:
                md += f"- ... y {len(requisitos_huerfanos) - 20} más\n"

        return md

    def _seccion_objetivo(self, m: MetricasObjetivo) -> str:
        """Genera la sección de detalle para un objetivo."""
        icono = {
            "completa":     "✅",
            "alta":         "🟢",
            "media":        "🟡",
            "baja":         "🔴",
            "sin_cobertura":"⛔"
        }.get(m.nivel_cobertura, "?")

        seccion = f"### {m.objetivo_id} — {m.titulo}\n\n"
        seccion += (
            f"**Estado:** {icono} {m.nivel_cobertura.replace('_', ' ').title()} "
            f"({m.porcentaje_cobertura:.0f}%)  \n"
            f"**KPI objetivo:** {m.kpi_objetivo}  \n"
            f"**Cobertura implementada:** {m.cobertura_implementada:.0f}% "
            f"(requisitos validados con historias generadas)\n\n"
        )

        # Desglose de vínculos
        seccion += "**Vínculos con el repositorio:**\n\n"
        seccion += (
            f"| Tipo | Cantidad |\n|---|---|\n"
            f"| Directos (explícitos) | {m.vinculos_directos} |\n"
            f"| Indirectos (explícitos) | {m.vinculos_indirectos} |\n"
            f"| Inferidos (semánticos) | {m.vinculos_inferidos} |\n\n"
        )

        # Requisitos por estado
        if m.requisitos_validados:
            seccion += (
                f"**Requisitos validados:** "
                f"{', '.join(m.requisitos_validados)}\n\n"
            )
        if m.requisitos_en_revision:
            seccion += (
                f"**En revisión:** "
                f"{', '.join(m.requisitos_en_revision)}\n\n"
            )
        if m.requisitos_borrador:
            seccion += (
                f"**En borrador:** "
                f"{', '.join(m.requisitos_borrador)}\n\n"
            )

        # Gaps
        if m.gaps:
            seccion += "**Gaps detectados:**\n\n"
            for gap in m.gaps:
                seccion += f"- {gap}\n"
            seccion += "\n"

        seccion += "---\n\n"
        return seccion

    def _barra_progreso(self, porcentaje: float, ancho: int = 10) -> str:
        """Genera una barra de progreso en texto para Markdown."""
        llenos = int(porcentaje / 100 * ancho)
        vacios = ancho - llenos
        return f"{'█' * llenos}{'░' * vacios}"

    def generar_json(
        self,
        metricas: list[MetricasObjetivo]
    ) -> dict:
        """
        Genera el informe en JSON para consumo por otras herramientas
        o para alimentar dashboards en Power BI o Grafana.
        """
        from dataclasses import asdict
        return {
            "fecha_generacion": datetime.now().isoformat(),
            "resumen": {
                "total_objetivos": len(metricas),
                "cobertura_media": round(
                    sum(m.porcentaje_cobertura for m in metricas) / len(metricas), 1
                ) if metricas else 0,
                "por_nivel": {
                    nivel: sum(1 for m in metricas if m.nivel_cobertura == nivel)
                    for nivel in [
                        "completa", "alta", "media", "baja", "sin_cobertura"
                    ]
                }
            },
            "objetivos": [
                {
                    "id": m.objetivo_id,
                    "titulo": m.titulo,
                    "prioridad": m.prioridad,
                    "kpi_objetivo": m.kpi_objetivo,
                    "porcentaje_cobertura": m.porcentaje_cobertura,
                    "nivel_cobertura": m.nivel_cobertura,
                    "cobertura_implementada": m.cobertura_implementada,
                    "vinculos": {
                        "directos": m.vinculos_directos,
                        "indirectos": m.vinculos_indirectos,
                        "inferidos": m.vinculos_inferidos
                    },
                    "requisitos": {
                        "validados": m.requisitos_validados,
                        "en_revision": m.requisitos_en_revision,
                        "borrador": m.requisitos_borrador
                    },
                    "artefactos": {
                        "historias": m.historias_generadas,
                        "test_cases": m.test_cases_generados
                    },
                    "gaps": m.gaps
                }
                for m in metricas
            ]
        }
```

---

## Punto de entrada: el analizador completo

El analizador orquesta los cuatro componentes y produce el informe completo en una sola llamada. Se puede ejecutar manualmente o de forma programada.

```python
# analizador_cobertura.py

import yaml
import os
from pathlib import Path


class AnalizadorCoberturaNegocio:
    """
    Orquesta el análisis completo de cobertura de negocio.
    Combina los cuatro componentes en un único flujo ejecutable.
    """

    def __init__(
        self,
        ruta_catalogo: str,
        ruta_requisitos: str,
        repositorio_rag,
        consultor_trazabilidad,
        ruta_salida: str = "./reports"
    ):
        self.ruta_catalogo = ruta_catalogo
        self.ruta_requisitos = ruta_requisitos
        self.rag = repositorio_rag
        self.trazabilidad = consultor_trazabilidad
        self.ruta_salida = Path(ruta_salida)

        self.indexador = None
        self.resolvedor = ResolvedorVinculos(repositorio_rag, ruta_requisitos)
        self.calculador = CalculadorCobertura()
        self.generador = GeneradorInformeCobertura()

    def ejecutar(
        self,
        re_indexar_objetivos: bool = False
    ) -> dict:
        """
        Ejecuta el análisis completo y genera los informes.
        """
        print("\n══════════════════════════════════════════════")
        print("  ANÁLISIS DE COBERTURA DE NEGOCIO")
        print("══════════════════════════════════════════════\n")

        # Cargar el catálogo
        with open(self.ruta_catalogo, encoding="utf-8") as f:
            catalogo = yaml.safe_load(f)
        objetivos = [
            o for o in catalogo.get("objetivos", [])
            if o.get("estado") != "cancelado"
        ]
        print(f"  Objetivos activos: {len(objetivos)}")

        # Paso 1: Indexar objetivos si es necesario
        if re_indexar_objetivos:
            print("  [1] Indexando objetivos en el vector store...")
            resultado_idx = indexar_catalogo_objetivos(
                self.ruta_catalogo, self.rag
            )
            print(
                f"      ✓ {resultado_idx['indexados']} objetivos indexados"
            )

        # Paso 2: Resolver vínculos
        print("  [2] Resolviendo vínculos requisito → objetivo...")
        vinculos = self.resolvedor.resolver_todos(objetivos)
        explicitos = sum(1 for v in vinculos if v.confianza == 1.0)
        inferidos = sum(1 for v in vinculos if v.confianza < 1.0)
        print(
            f"      ✓ {len(vinculos)} vínculos "
            f"({explicitos} explícitos, {inferidos} inferidos)"
        )

        # Paso 3: Calcular métricas
        print("  [3] Calculando métricas de cobertura...")
        metricas = self.calculador.calcular(
            objetivos, vinculos, self.trazabilidad
        )

        # Identificar requisitos huérfanos
        req_con_objetivo = {v.requisito_id for v in vinculos}
        todos_req = self._obtener_todos_los_ids()
        huerfanos = [r for r in todos_req if r not in req_con_objetivo]

        # Paso 4: Generar informes
        print("  [4] Generando informes...")
        self.ruta_salida.mkdir(exist_ok=True)

        # Markdown
        md = self.generador.generar_markdown(
            metricas, catalogo.get("metadata", {}), huerfanos
        )
        ruta_md = self.ruta_salida / "cobertura-negocio.md"
        ruta_md.write_text(md, encoding="utf-8")
        print(f"      ✓ Markdown: {ruta_md}")

        # JSON
        import json
        informe_json = self.generador.generar_json(metricas)
        informe_json["requisitos_huerfanos"] = huerfanos
        ruta_json = self.ruta_salida / "cobertura-negocio.json"
        ruta_json.write_text(
            json.dumps(informe_json, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"      ✓ JSON: {ruta_json}")

        # Resumen en consola
        print("\n  RESUMEN")
        print("  ─────────────────────────────────────────────")
        for m in metricas:
            barra = self.generador._barra_progreso(m.porcentaje_cobertura, 8)
            icono = {
                "completa": "✅", "alta": "🟢", "media": "🟡",
                "baja": "🔴", "sin_cobertura": "⛔"
            }.get(m.nivel_cobertura, "?")
            print(
                f"  {m.objetivo_id:8} {barra} "
                f"{m.porcentaje_cobertura:5.1f}% "
                f"{icono} {m.titulo[:40]}"
            )

        cobertura_media = (
            sum(m.porcentaje_cobertura for m in metricas) / len(metricas)
        ) if metricas else 0
        print(f"\n  Cobertura media: {cobertura_media:.1f}%")
        print(f"  Requisitos huérfanos: {len(huerfanos)}")
        print("══════════════════════════════════════════════\n")

        return informe_json

    def _obtener_todos_los_ids(self) -> list[str]:
        """Obtiene los IDs de todos los requisitos procesables."""
        ids = []
        for root, _, files in os.walk(self.ruta_requisitos):
            for archivo in files:
                if not archivo.endswith(".yaml"):
                    continue
                try:
                    with open(
                        os.path.join(root, archivo), encoding="utf-8"
                    ) as f:
                        req = yaml.safe_load(f)
                    if req and req.get("estado") in (
                        "en-revision", "validado"
                    ):
                        ids.append(req["id"])
                except Exception:
                    continue
        return ids
```

---

## Ejemplo de salida del informe

Este es el aspecto del informe generado para el proyecto de facturación del modelo operativo, con el catálogo de cinco objetivos definido anteriormente:

```
══════════════════════════════════════════════
  ANÁLISIS DE COBERTURA DE NEGOCIO
══════════════════════════════════════════════

  Objetivos activos: 5
  [1] Indexando objetivos en el vector store...
      ✓ 5 objetivos indexados
  [2] Resolviendo vínculos requisito → objetivo...
      ✓ 31 vínculos (19 explícitos, 12 inferidos)
  [3] Calculando métricas de cobertura...
  [4] Generando informes...
      ✓ Markdown: ./reports/cobertura-negocio.md
      ✓ JSON:     ./reports/cobertura-negocio.json

  RESUMEN
  ─────────────────────────────────────────────
  OBJ-001  ████████  82.4% 🟢 Reducir el tiempo de cierre contable
  OBJ-002  █████░░░  54.1% 🟡 Eliminar el procesamiento manual de fact...
  OBJ-003  ██████░░  71.3% 🟢 Garantizar trazabilidad del ciclo de apr...
  OBJ-004  ████████  88.7% 🟢 Reducir errores de pago por facturas dup...
  OBJ-005  ██░░░░░░  23.0% 🔴 Habilitar acceso para gestores de área

  Cobertura media: 63.9%
  Requisitos huérfanos: 4
══════════════════════════════════════════════
```

El objetivo OBJ-005 con 23% de cobertura señala que el módulo de acceso para gestores de área, aunque está en el roadmap, apenas tiene requisitos en el backlog. El product owner puede tomar esa señal en la siguiente planificación trimestral antes de que el desfase sea mayor.

Los cuatro requisitos huérfanos merecen revisión: pueden ser funcionalidad técnica correctamente excluida del catálogo de objetivos (infraestructura, seguridad transversal) o pueden ser el primer síntoma de scope creep.

---

## Integración con el orquestador y el gobierno

El análisis de cobertura no es una ejecución puntual. Se integra en dos momentos del flujo del modelo.

**En la auditoría semanal del punto 12.** El auditor automático del repositorio incluye un paso de cobertura de negocio que actualiza el JSON de salida y registra la evolución de la cobertura media semana a semana. Una caída de más de cinco puntos porcentuales en la cobertura media entre dos semanas consecutivas activa una alerta de gobierno, porque normalmente indica que se han añadido requisitos huérfanos o que se han cancelado requisitos que cubrían objetivos críticos.

**En el dashboard mensual del comité de gobierno.** El informe JSON se consume directamente por la herramienta de visualización configurada en el proyecto (Power BI, Grafana, Confluence macro). La dirección ve la evolución de la cobertura de cada objetivo a lo largo del tiempo, no solo el valor puntual del último análisis.

**Como sugerencia en tiempo real al analista.** Cuando el analista escribe un requisito en borrador, el paso 3 del orquestador ya recupera contexto RAG del repositorio. Con el catálogo indexado, ese mismo paso puede sugerir al analista qué objetivos de negocio podría declarar en el campo `objetivos_negocio` del nuevo requisito, basándose en la similitud semántica con el texto del borrador. Esa sugerencia aparece en la interfaz de aprobación del paso 8 como una recomendación no bloqueante.

---

## Limitaciones del análisis y cómo gestionarlas

**La cobertura mide vínculos, no cumplimiento del KPI.** Un objetivo con diez requisitos validados y sus historias implementadas tiene cobertura alta, pero no necesariamente cumple su KPI. El KPI real solo se puede medir en producción. El análisis de cobertura dice que el sistema tiene la funcionalidad necesaria para cumplir el objetivo, no que el objetivo ya está cumplido. Esta distinción debe comunicarse con claridad al presentar el informe a la dirección.

**Los vínculos inferidos necesitan revisión periódica.** La similitud semántica detecta vínculos plausibles, no vínculos correctos. Un requisito sobre la configuración de umbrales de notificación puede tener alta similitud con el objetivo de reducir errores de pago, pero en realidad no contribuye a ese objetivo. El champion debe revisar los vínculos inferidos con el analista al final de cada sprint y confirmar o descartar cada uno explícitamente.

**El catálogo de objetivos envejece.** Si el catálogo no se revisa trimestralmente, la cobertura calculada pierde significado porque los objetivos del negocio han evolucionado pero el catálogo no lo refleja. El gobierno del punto 12 incluye la revisión trimestral del catálogo como tarea del propietario del glosario.

**Los requisitos de infraestructura y seguridad son legítimamente huérfanos.** No todo requisito debe contribuir a un objetivo de negocio del catálogo. Los requisitos de rendimiento, seguridad, accesibilidad y deuda técnica son necesarios pero instrumentales. El catálogo puede incluir un objetivo genérico del tipo "Mantener los estándares de calidad técnica" al que estos requisitos se vinculen, o puede documentarse explícitamente que estos requisitos están exentos del análisis de cobertura.
