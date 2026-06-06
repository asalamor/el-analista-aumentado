# Análisis de cobertura de negocio

## Qué se cubre, qué se ignora y cómo saberlo antes de que llegue al sprint

---

David Sanz llegó a la reunión de planificación trimestral con una pregunta que Carlos no supo responder en el momento: «¿Tenemos requisitos para todo lo que nos comprometemos a entregar este trimestre, o hay objetivos de negocio que todavía no tienen ni un solo requisito detrás?»

Carlos sabía que la pregunta era legítima. El equipo llevaba tres meses construyendo el repositorio de requisitos AI-ready, y el pipeline generaba artefactos de calidad creciente. Pero nadie había mirado el problema desde el otro extremo: no desde los requisitos hacia los artefactos, sino desde los objetivos de negocio hacia los requisitos. ¿Existía algún objetivo declarado por Ana López para el trimestre que no tuviera ningún requisito asociado? ¿Había requisitos en el repositorio que no respondían a ningún objetivo concreto, requisitos huérfanos que alguien había escrito porque le parecía buena idea pero que nadie del negocio había pedido?

Carlos no lo sabía. Nadie lo sabía. Y eso era exactamente el problema.

---

## El punto ciego del análisis funcional orientado a requisitos

El modelo operativo que hemos construido a lo largo de este libro funciona de arriba hacia abajo: los objetivos de negocio se capturan en el Event Storming, se convierten en requisitos AI-ready, los requisitos generan historias, las historias generan test cases, y la trazabilidad mantiene la cadena. Todo eso es correcto.

El problema es que ese flujo asume que la captura inicial fue completa. Asume que todo lo que el negocio necesita quedó recogido en los talleres de Event Storming. Asume que no hay objetivos que nunca se articularon en requisitos porque nadie hizo la pregunta correcta en el momento correcto.

En la práctica, esa asunción falla con regularidad. Falla porque los objetivos de negocio no siempre están completamente articulados cuando empieza el análisis funcional. Falla porque algunos objetivos son implícitos: todo el mundo da por sentado que el sistema debe cumplir ese objetivo, pero nadie lo escribió. Y falla porque los objetivos evolucionan durante el proyecto mientras el repositorio de requisitos permanece anclado al momento en que se escribió.

El resultado es siempre el mismo: llega la revisión trimestral, el PO pregunta por qué cierto objetivo no tiene cobertura, y el equipo descubre que nadie lo convirtió en un requisito porque nadie verificó explícitamente que estuviera cubierto.

El análisis de cobertura de negocio es la pieza que cierra ese hueco. No es un paso del pipeline de generación de artefactos: es una consulta que el analista o el PO pueden lanzar en cualquier momento para obtener una respuesta a la pregunta de David: «¿qué está cubierto, qué no lo está y qué está cubierto a medias?»

---

## Los objetivos de negocio como primer ciudadano del repositorio

Antes de poder cruzar requisitos con objetivos, los objetivos tienen que existir en algún lugar del repositorio con estructura suficiente para que el sistema pueda procesarlos. En la mayoría de organizaciones, los objetivos de negocio viven en presentaciones de PowerPoint, en documentos de visión de producto que nadie lee después del kick-off, o en la cabeza del PO.

Para que el análisis de cobertura funcione, los objetivos necesitan estar en el repositorio con el mismo nivel de formalidad que los requisitos: identificados, nombrados y con criterios que permitan determinar cuándo un requisito contribuye a un objetivo y cuándo no.

La estructura que recomendamos es deliberadamente ligera. No se trata de añadir un nivel de gestión estratégica que nadie va a mantener. Se trata de capturar lo suficiente para que el sistema pueda hacer la pregunta de cobertura.

```yaml
# objetivos/OBJ-2025-Q3.yaml
# Los objetivos de negocio del trimestre para EP-04 Gestión de Facturación
# Propietario: David Sanz (Product Owner)
# Revisión: inicio de cada trimestre con Ana López

objetivos:
  - id: OBJ-01
    titulo: "Reducir el tiempo de cierre contable mensual"
    descripcion: >
      El proceso de cierre contable mensual del equipo de Ana López tarda
      actualmente entre dos y tres días. El objetivo para Q3 es reducirlo
      por debajo de un día laborable, automatizando o agilizando las tareas
      de búsqueda y validación de facturas que consumen más tiempo.
    kpi_principal: "Tiempo de cierre contable (días laborables)"
    valor_actual: 2.5
    valor_objetivo: 1.0
    fecha_medicion: "2025-09-30"
    prioridad: critico
    area_negocio: "Dirección Financiera"
    epicas_relacionadas: ["EP-04"]

  - id: OBJ-02
    titulo: "Eliminar las facturas duplicadas en el sistema"
    descripcion: >
      Actualmente el sistema registra entre 8 y 12 facturas duplicadas
      al mes, que el equipo detecta manualmente durante la conciliación.
      Cada duplicado requiere entre 45 y 90 minutos para investigar y
      corregir. El objetivo es que el sistema detecte automáticamente
      los posibles duplicados antes de que se aprueben.
    kpi_principal: "Facturas duplicadas registradas por mes"
    valor_actual: 10
    valor_objetivo: 0
    fecha_medicion: "2025-09-30"
    prioridad: alto
    area_negocio: "Dirección Financiera"
    epicas_relacionadas: ["EP-04"]

  - id: OBJ-03
    titulo: "Habilitar la trazabilidad completa de aprobaciones"
    descripcion: >
      Auditoría reciente detectó que no existe registro completo de quién
      aprobó cada factura y cuándo. El objetivo es que el sistema registre
      automáticamente el histórico completo de cambios de estado de cada
      factura, incluyendo el usuario, la fecha y la hora, para poder
      responder a cualquier consulta de auditoría sin búsqueda manual.
    kpi_principal: "% de facturas con histórico de aprobación completo"
    valor_actual: 0
    valor_objetivo: 100
    fecha_medicion: "2025-09-30"
    prioridad: alto
    area_negocio: "Dirección Financiera / Auditoría interna"
    epicas_relacionadas: ["EP-04"]

  - id: OBJ-04
    titulo: "Permitir la exportación de datos para reporting externo"
    descripcion: >
      El equipo de finanzas exporta manualmente datos de facturas a Excel
      cada semana para alimentar los informes del sistema de reporting
      corporativo. El objetivo es que esa exportación sea directa desde
      el módulo de facturación, en formato compatible con el sistema de
      reporting, sin intervención manual.
    kpi_principal: "Horas semanales dedicadas a exportación manual"
    valor_actual: 4
    valor_objetivo: 0
    fecha_medicion: "2025-09-30"
    prioridad: medio
    area_negocio: "Dirección Financiera"
    epicas_relacionadas: ["EP-04"]
```

La clave de esta estructura es el campo `descripcion`: no es un objetivo abstracto al estilo de «mejorar la eficiencia», sino una descripción concreta del problema actual con valores medibles del estado actual y del estado deseado. Eso es lo que permite que el análisis de cobertura sea semántico, no solo por palabras clave.

---

## Cómo funciona el análisis de cobertura

El análisis de cobertura cruza los objetivos de negocio con los requisitos del repositorio usando dos mecanismos en combinación: la trazabilidad explícita (el campo `objetivo_negocio` de la plantilla YAML del capítulo 4) y la similitud semántica del sistema RAG del capítulo 10.

La trazabilidad explícita detecta los requisitos que el analista vinculó conscientemente a un objetivo. La similitud semántica detecta los requisitos que contribuyen a un objetivo aunque nadie haya registrado esa relación. La combinación de los dos produce un resultado mucho más completo que cualquiera de los dos por separado.

El resultado del análisis es una matriz de cobertura con cuatro estados posibles para cada par objetivo-requisito:

```
ESTADO DE COBERTURA

✅ Cubierto directamente
   El requisito declara explícitamente este objetivo en su campo
   `objetivo_negocio` Y la similitud semántica es alta (> 0.80).
   Alta confianza en que el requisito responde a este objetivo.

🔶 Cubierto indirectamente
   El requisito no declara el objetivo explícitamente, pero la
   similitud semántica sugiere que contribuye a él (0.60–0.80).
   Requiere validación humana: ¿lo cubre realmente o es una
   coincidencia terminológica?

⚠️  Cobertura parcial
   El objetivo tiene algunos requisitos que lo cubren pero el
   análisis detecta áreas del objetivo sin requisito asociado.
   El objetivo está definido pero no está completamente desglosado
   en requisitos implementables.

❌ Sin cobertura
   No existe ningún requisito en el repositorio que cubra este
   objetivo, ni de forma explícita ni semántica. El objetivo
   declarado es un punto ciego del análisis funcional.
```

---

## El analizador de cobertura

Construimos el analizador como un componente independiente que puede ejecutarse en cualquier momento sin alterar el pipeline. No es un paso del orquestador: es una consulta que el analista o el PO lanzan cuando quieren ver el estado de cobertura.

```python
# cobertura/analizador_cobertura.py
"""
Analiza la cobertura de los objetivos de negocio por los requisitos
del repositorio.

Combina dos fuentes de información:
  1. Vínculos explícitos: el campo objetivo_negocio de los requisitos YAML.
  2. Similitud semántica: el sistema RAG del capítulo 10.

La combinación produce una imagen de cobertura más fiel que cualquier
fuente por separado.
"""

import yaml
import json
import asyncio
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# ── Estructuras de datos ────────────────────────────────────────────────────

@dataclass
class ObjetivoNegocio:
    id: str
    titulo: str
    descripcion: str
    kpi_principal: str
    valor_actual: float
    valor_objetivo: float
    prioridad: str
    area_negocio: str
    epicas_relacionadas: list[str]


@dataclass
class ContribucionRequisito:
    """
    Representa la relación entre un requisito y un objetivo.
    Puede ser explícita (el analista la declaró) o inferida (el RAG la detectó).
    """
    requisito_id: str
    titulo_requisito: str
    estado_requisito: str
    vinculo_explicito: bool           # True si el analista lo declaró
    similitud_semantica: float        # 0.0–1.0 del sistema RAG
    confianza_total: float            # Combinación ponderada de los dos
    tipo_contribucion: str            # directo | parcial | indirecto
    aspecto_cubierto: str             # Qué parte del objetivo cubre este req.
    aspecto_no_cubierto: str          # Qué parte del objetivo no cubre


@dataclass
class ResultadoCobertura:
    objetivo: ObjetivoNegocio
    estado: str                       # cubierto | parcial | indirecto | sin_cobertura
    confianza: float                  # 0.0–1.0
    requisitos_contribuyentes: list[ContribucionRequisito] = field(default_factory=list)
    gaps_detectados: list[str] = field(default_factory=list)
    preguntas_sin_responder: list[str] = field(default_factory=list)
    recomendacion: str = ""


# ── Cargador de objetivos ───────────────────────────────────────────────────

def cargar_objetivos(ruta_yaml: Path) -> list[ObjetivoNegocio]:
    """
    Carga los objetivos de negocio desde el archivo YAML.
    Retorna una lista de ObjetivoNegocio ordenada por prioridad.
    """
    with open(ruta_yaml, encoding="utf-8") as f:
        datos = yaml.safe_load(f)

    orden_prioridad = {"critico": 0, "alto": 1, "medio": 2, "bajo": 3}

    objetivos = [
        ObjetivoNegocio(**obj)
        for obj in datos.get("objetivos", [])
    ]

    return sorted(
        objetivos,
        key=lambda o: orden_prioridad.get(o.prioridad, 99)
    )


# ── Analizador principal ────────────────────────────────────────────────────

class AnalizadorCobertura:
    """
    Cruza los objetivos de negocio con los requisitos del repositorio
    para producir la matriz de cobertura.
    """

    # Un requisito necesita esta similitud mínima para considerarse
    # relevante para un objetivo. Por debajo de este umbral, la relación
    # es probablemente coincidencia terminológica, no cobertura real.
    UMBRAL_SIMILITUD_MINIMA = 0.55

    # Por encima de este umbral, la cobertura es directa sin necesidad
    # de validación humana adicional.
    UMBRAL_COBERTURA_DIRECTA = 0.78

    def __init__(self, motor_rag, repositorio_requisitos: Path, llm_client):
        self.rag = motor_rag
        self.repo = repositorio_requisitos
        self.llm = llm_client

    async def analizar_objetivo(
        self,
        objetivo: ObjetivoNegocio
    ) -> ResultadoCobertura:
        """
        Analiza la cobertura de un único objetivo de negocio.

        El análisis tiene tres fases:
          1. Búsqueda de vínculos explícitos en el repositorio.
          2. Búsqueda semántica de requisitos relacionados.
          3. Evaluación con LLM de los gaps de cobertura.
        """

        # FASE 1: Vínculos explícitos
        # Buscamos requisitos cuyo campo objetivo_negocio mencione este objetivo.
        requisitos_explicitos = self._buscar_vinculos_explicitos(objetivo.id)

        # FASE 2: Búsqueda semántica
        # Usamos el texto completo del objetivo para buscar requisitos
        # semánticamente relacionados en el vector store.
        query_semantica = (
            f"{objetivo.titulo}. {objetivo.descripcion}. "
            f"KPI: {objetivo.kpi_principal}. "
            f"Valor actual: {objetivo.valor_actual}. "
            f"Objetivo: {objetivo.valor_objetivo}."
        )
        candidatos_rag = self.rag.buscar_por_similitud(
            query_texto=query_semantica,
            filtros={
                "estado": "validado",
                # Solo buscar en las épicas relacionadas con el objetivo
                # para no recuperar ruido de módulos no relacionados
            },
            top_k=10
        )

        # Filtrar por umbral mínimo
        candidatos_relevantes = [
            c for c in candidatos_rag
            if c.similitud >= self.UMBRAL_SIMILITUD_MINIMA
        ]

        # FASE 3: Combinar resultados y evaluar con LLM
        contribuciones = await self._evaluar_contribuciones(
            objetivo=objetivo,
            explicitos=requisitos_explicitos,
            semanticos=candidatos_relevantes
        )

        # Determinar el estado de cobertura global
        estado, confianza = self._determinar_estado_cobertura(contribuciones)

        # Identificar gaps con el LLM
        gaps, preguntas = await self._identificar_gaps(objetivo, contribuciones)

        # Generar recomendación
        recomendacion = self._generar_recomendacion(estado, gaps, objetivo)

        return ResultadoCobertura(
            objetivo=objetivo,
            estado=estado,
            confianza=confianza,
            requisitos_contribuyentes=contribuciones,
            gaps_detectados=gaps,
            preguntas_sin_responder=preguntas,
            recomendacion=recomendacion
        )

    def _buscar_vinculos_explicitos(self, objetivo_id: str) -> list[dict]:
        """
        Busca en el repositorio todos los requisitos que declaran
        explícitamente su vínculo con este objetivo.

        En la plantilla YAML del Cap. 4, el campo objetivo_negocio
        puede referenciar un ID de objetivo o describirlo en texto libre.
        Buscamos ambos casos.
        """
        requisitos_vinculados = []

        for yaml_file in self.repo.rglob("REQ-*.yaml"):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    req = yaml.safe_load(f)

                if req.get("estado") not in ("en-revision", "validado"):
                    continue

                objetivo_negocio = req.get("objetivo_negocio", "")

                # Vínculo explícito: el campo referencia el ID del objetivo
                if objetivo_id in str(objetivo_negocio):
                    requisitos_vinculados.append({
                        "requisito": req,
                        "tipo_vinculo": "explicito_id"
                    })

            except Exception:
                continue

        return requisitos_vinculados

    async def _evaluar_contribuciones(
        self,
        objetivo: ObjetivoNegocio,
        explicitos: list[dict],
        semanticos: list
    ) -> list[ContribucionRequisito]:
        """
        Para cada candidato (explícito o semántico), evalúa qué parte
        del objetivo cubre y calcula la confianza total.

        Para los candidatos con similitud alta, la evaluación es automática.
        Para los candidatos en la zona gris (0.55–0.78), el LLM evalúa
        si la cobertura es real o es coincidencia terminológica.
        """
        contribuciones = []

        # Combinar explícitos y semánticos, eliminando duplicados
        candidatos_procesados = set()

        # Primero los explícitos: siempre tienen alta confianza
        for vinculado in explicitos:
            req = vinculado["requisito"]
            req_id = req.get("id", "")

            if req_id in candidatos_procesados:
                continue
            candidatos_procesados.add(req_id)

            # Buscar si también aparece en los semánticos para combinar scores
            similitud = next(
                (c.similitud for c in semanticos
                 if req_id in c.chunk_id),
                0.70    # Default razonable para un vínculo explícito
            )

            # La confianza de un vínculo explícito es alta por defecto,
            # pero se refuerza si el RAG también lo confirma
            confianza = min(1.0, 0.80 + (similitud * 0.20))

            contribuciones.append(ContribucionRequisito(
                requisito_id=req_id,
                titulo_requisito=req.get("titulo", ""),
                estado_requisito=req.get("estado", ""),
                vinculo_explicito=True,
                similitud_semantica=similitud,
                confianza_total=confianza,
                tipo_contribucion="directo",
                aspecto_cubierto=await self._evaluar_aspecto_cubierto(
                    objetivo, req
                ),
                aspecto_no_cubierto=""
            ))

        # Después los semánticos que no son explícitos
        for candidato in semanticos:
            req_id = candidato.metadatos.get("requisito_id", "")

            if req_id in candidatos_procesados:
                continue
            candidatos_procesados.add(req_id)

            # Para similitud alta, aceptar sin validación LLM adicional
            if candidato.similitud >= self.UMBRAL_COBERTURA_DIRECTA:
                tipo = "directo"
                confianza = candidato.similitud
            else:
                # Zona gris: el LLM valida si la cobertura es real
                es_real, confianza_ajustada = await self._validar_cobertura_llm(
                    objetivo=objetivo,
                    texto_candidato=candidato.texto
                )
                if not es_real:
                    continue   # Descartamos el candidato
                tipo = "indirecto"
                confianza = confianza_ajustada

            contribuciones.append(ContribucionRequisito(
                requisito_id=req_id,
                titulo_requisito=candidato.metadatos.get("titulo", ""),
                estado_requisito=candidato.metadatos.get("estado", ""),
                vinculo_explicito=False,
                similitud_semantica=candidato.similitud,
                confianza_total=confianza,
                tipo_contribucion=tipo,
                aspecto_cubierto=await self._evaluar_aspecto_cubierto_texto(
                    objetivo, candidato.texto
                ),
                aspecto_no_cubierto=""
            ))

        # Ordenar por confianza descendente
        return sorted(
            contribuciones,
            key=lambda c: c.confianza_total,
            reverse=True
        )

    async def _validar_cobertura_llm(
        self,
        objetivo: ObjetivoNegocio,
        texto_candidato: str
    ) -> tuple[bool, float]:
        """
        Pide al LLM que evalúe si el requisito candidato realmente
        contribuye al objetivo o si la similitud semántica es coincidencia.

        Este paso es fundamental para la zona gris (0.55–0.78) donde
        el RAG no puede determinar por sí solo si hay cobertura real.
        """
        prompt = f"""Evalúa si el siguiente requisito funcional contribuye al objetivo de negocio dado.

OBJETIVO DE NEGOCIO:
Título: {objetivo.titulo}
Descripción: {objetivo.descripcion}
KPI: {objetivo.kpi_principal} (actual: {objetivo.valor_actual}, objetivo: {objetivo.valor_objetivo})

REQUISITO CANDIDATO:
{texto_candidato[:600]}

Responde SOLO con este JSON, sin texto adicional:
{{
  "contribuye": true | false,
  "confianza": 0.0-1.0,
  "razon": "Una frase explicando por qué sí o por qué no contribuye"
}}

Criterio: un requisito contribuye si su implementación hace avanzar el KPI hacia el valor objetivo,
aunque sea de forma parcial. No contribuye si la similitud es solo terminológica sin impacto real en el KPI."""

        respuesta = self.llm.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            datos = json.loads(respuesta.choices[0].message.content)
            return datos.get("contribuye", False), datos.get("confianza", 0.0)
        except Exception:
            # Si el LLM falla, asumimos no contribuye para ser conservadores
            return False, 0.0

    async def _evaluar_aspecto_cubierto(
        self,
        objetivo: ObjetivoNegocio,
        requisito: dict
    ) -> str:
        """
        Identifica qué aspecto específico del objetivo cubre este requisito.
        Útil para detectar si múltiples requisitos cubren el mismo aspecto
        (redundancia) o si cubren aspectos complementarios (cobertura completa).
        """
        prompt = f"""Dado este objetivo de negocio y este requisito funcional,
identifica en una frase corta qué aspecto específico del objetivo cubre el requisito.

OBJETIVO: {objetivo.titulo}
KPI a mover: {objetivo.kpi_principal} (de {objetivo.valor_actual} a {objetivo.valor_objetivo})

REQUISITO: {requisito.get('titulo', '')}
Descripción: {requisito.get('descripcion', '')[:300]}

Responde en una sola frase sin prefijos. Ejemplo: "Reduce el tiempo de búsqueda de facturas por fecha"
Si el requisito no cubre un aspecto claro del objetivo, responde: "Contribución indirecta"
"""
        respuesta = self.llm.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=60,
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content.strip()

    async def _evaluar_aspecto_cubierto_texto(
        self,
        objetivo: ObjetivoNegocio,
        texto_chunk: str
    ) -> str:
        """Versión que opera sobre el texto del chunk del RAG en lugar del YAML completo."""
        prompt = f"""Objetivo: {objetivo.titulo}
KPI: {objetivo.kpi_principal}

Texto del requisito: {texto_chunk[:300]}

En una frase, ¿qué aspecto del objetivo cubre este requisito?"""

        respuesta = self.llm.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=60,
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content.strip()

    def _determinar_estado_cobertura(
        self,
        contribuciones: list[ContribucionRequisito]
    ) -> tuple[str, float]:
        """
        Determina el estado de cobertura global de un objetivo
        basándose en sus contribuciones.
        """
        if not contribuciones:
            return "sin_cobertura", 0.0

        directas = [c for c in contribuciones if c.tipo_contribucion == "directo"]
        indirectas = [c for c in contribuciones if c.tipo_contribucion == "indirecto"]

        if not directas and not indirectas:
            return "sin_cobertura", 0.0

        # Cobertura directa fuerte
        if directas and max(c.confianza_total for c in directas) >= 0.85:
            # Pero verificar si la cobertura es completa o parcial
            n_directas = len(directas)
            if n_directas >= 2:
                return "cubierto", min(1.0, max(c.confianza_total for c in directas))
            else:
                # Una sola contribución directa puede ser cobertura parcial
                return "parcial", directas[0].confianza_total

        # Cobertura indirecta o directa débil
        if directas or indirectas:
            confianza_max = max(
                c.confianza_total for c in (directas + indirectas)
            )
            if confianza_max >= 0.65:
                return "parcial", confianza_max
            else:
                return "indirecto", confianza_max

        return "sin_cobertura", 0.0

    async def _identificar_gaps(
        self,
        objetivo: ObjetivoNegocio,
        contribuciones: list[ContribucionRequisito]
    ) -> tuple[list[str], list[str]]:
        """
        Usa el LLM para identificar qué aspectos del objetivo NO están
        cubiertos por ningún requisito existente.

        Este es el output más valioso del análisis: no qué existe,
        sino qué falta.
        """
        if not contribuciones:
            # Sin ninguna contribución, el gap es el objetivo completo
            return (
                [f"El objetivo completo '{objetivo.titulo}' no tiene ningún requisito asociado"],
                [f"¿Qué funcionalidad del sistema haría avanzar el KPI '{objetivo.kpi_principal}' "
                 f"de {objetivo.valor_actual} a {objetivo.valor_objetivo}?"]
            )

        aspectos_cubiertos = "\n".join([
            f"- {c.aspecto_cubierto} ({c.requisito_id})"
            for c in contribuciones
            if c.aspecto_cubierto and c.aspecto_cubierto != "Contribución indirecta"
        ])

        prompt = f"""Analiza si los requisitos existentes cubren completamente este objetivo de negocio.

OBJETIVO: {objetivo.titulo}
Descripción: {objetivo.descripcion}
KPI a mover: {objetivo.kpi_principal} (de {objetivo.valor_actual} a {objetivo.valor_objetivo})

ASPECTOS YA CUBIERTOS POR REQUISITOS EXISTENTES:
{aspectos_cubiertos if aspectos_cubiertos else "Ninguno identificado con claridad"}

Identifica:
1. Los gaps: aspectos del objetivo que NO están cubiertos por ningún requisito.
2. Las preguntas que el analista debería hacer al negocio para completar la cobertura.

Responde SOLO con este JSON:
{{
  "gaps": [
    "Descripción concreta de aspecto no cubierto 1",
    "Descripción concreta de aspecto no cubierto 2"
  ],
  "preguntas_para_negocio": [
    "¿Qué...?",
    "¿Cómo...?"
  ]
}}

Si no detectas gaps significativos, retorna listas vacías.
Sé específico: los gaps deben describir funcionalidad concreta que falta, no abstracciones."""

        respuesta = self.llm.chat.completions.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            datos = json.loads(respuesta.choices[0].message.content)
            return (
                datos.get("gaps", []),
                datos.get("preguntas_para_negocio", [])
            )
        except Exception:
            return [], []

    def _generar_recomendacion(
        self,
        estado: str,
        gaps: list[str],
        objetivo: ObjetivoNegocio
    ) -> str:
        """Genera la recomendación de acción según el estado de cobertura."""

        if estado == "sin_cobertura":
            return (
                f"Este objetivo no tiene ningún requisito funcional asociado. "
                f"Antes del próximo sprint, el analista debería convocar un "
                f"taller de Event Storming focalizado en el KPI "
                f"'{objetivo.kpi_principal}' para identificar los eventos "
                f"de negocio que lo mueven."
            )

        if estado == "parcial" and gaps:
            n_gaps = len(gaps)
            return (
                f"La cobertura es parcial: {n_gaps} aspecto(s) del objetivo "
                f"sin requisito asociado. Completar la cobertura antes de dar "
                f"por cerrado el análisis de este módulo."
            )

        if estado == "indirecto":
            return (
                f"Los requisitos encontrados contribuyen indirectamente al objetivo. "
                f"Revisar si existe algún requisito más directo que no fue detectado "
                f"por falta de vínculo explícito, o considerar si hace falta "
                f"un requisito dedicado."
            )

        if not gaps:
            return (
                f"La cobertura parece completa. Revisar la matriz en el próximo "
                f"trimestre o cuando se modifiquen los objetivos de negocio."
            )

        return (
            f"Cobertura buena pero con {len(gaps)} gap(s) menores. "
            f"Valorar si los gaps detectados justifican nuevos requisitos "
            f"o son aspectos fuera del alcance del trimestre."
        )
```

---

## El informe de cobertura

El análisis produce un informe que el analista puede compartir con el PO antes de cualquier revisión trimestral. El formato está pensado para ser legible tanto en Confluence como en una presentación de diapositivas.

```python
# cobertura/generador_informe.py

def generar_informe_cobertura(
    resultados: list[ResultadoCobertura],
    trimestre: str
) -> str:
    """
    Genera el informe de cobertura en Markdown.
    Estructura pensada para ser renderizada en Confluence o exportada a PDF.
    """

    # Calcular estadísticas globales
    total = len(resultados)
    cubiertos  = sum(1 for r in resultados if r.estado == "cubierto")
    parciales  = sum(1 for r in resultados if r.estado == "parcial")
    indirectos = sum(1 for r in resultados if r.estado == "indirecto")
    sin_cobert = sum(1 for r in resultados if r.estado == "sin_cobertura")

    # Semáforo global
    if sin_cobert > 0 or parciales > total * 0.3:
        semaforo = "🔴 Cobertura insuficiente"
    elif parciales > 0 or indirectos > 0:
        semaforo = "🟡 Cobertura con gaps"
    else:
        semaforo = "🟢 Cobertura completa"

    md = f"""# Análisis de cobertura de negocio — {trimestre}

**Estado global:** {semaforo}

| Estado | Objetivos | % |
|---|---|---|
| ✅ Cubierto completamente | {cubiertos} | {cubiertos/total:.0%} |
| ⚠️ Cobertura parcial | {parciales} | {parciales/total:.0%} |
| 🔶 Cobertura indirecta | {indirectos} | {indirectos/total:.0%} |
| ❌ Sin cobertura | {sin_cobert} | {sin_cobert/total:.0%} |

---

"""

    # Primero los objetivos críticos sin cobertura (los más urgentes)
    criticos_sin_cobert = [
        r for r in resultados
        if r.estado == "sin_cobertura" and r.objetivo.prioridad == "critico"
    ]
    if criticos_sin_cobert:
        md += "## 🚨 Objetivos críticos sin cobertura funcional\n\n"
        md += "_Estos objetivos no tienen ningún requisito en el repositorio. "_
        md += "_Requieren atención inmediata antes del próximo sprint._\n\n"
        for r in criticos_sin_cobert:
            md += _formatear_objetivo_sin_cobertura(r)
        md += "\n---\n\n"

    # Objetivos parcialmente cubiertos con gaps
    parciales_con_gaps = [
        r for r in resultados
        if r.estado in ("parcial", "indirecto") and r.gaps_detectados
    ]
    if parciales_con_gaps:
        md += "## ⚠️ Objetivos con cobertura incompleta\n\n"
        for r in parciales_con_gaps:
            md += _formatear_objetivo_parcial(r)
        md += "\n---\n\n"

    # Objetivos completamente cubiertos (para confirmación)
    completamente_cubiertos = [
        r for r in resultados if r.estado == "cubierto"
    ]
    if completamente_cubiertos:
        md += "## ✅ Objetivos con cobertura completa\n\n"
        for r in completamente_cubiertos:
            md += _formatear_objetivo_cubierto(r)
        md += "\n---\n\n"

    # Matriz completa al final (para referencia)
    md += _generar_matriz_completa(resultados)

    return md


def _formatear_objetivo_sin_cobertura(r: ResultadoCobertura) -> str:
    obj = r.objetivo
    md = f"### ❌ {obj.id} — {obj.titulo}\n\n"
    md += f"**KPI:** {obj.kpi_principal} · Actual: {obj.valor_actual} · Objetivo: {obj.valor_objetivo}\n\n"
    md += f"**Área:** {obj.area_negocio}\n\n"
    md += f"**Recomendación:** {r.recomendacion}\n\n"
    if r.preguntas_sin_responder:
        md += "**Preguntas para el próximo taller con negocio:**\n\n"
        for pregunta in r.preguntas_sin_responder:
            md += f"- {pregunta}\n"
        md += "\n"
    return md


def _formatear_objetivo_parcial(r: ResultadoCobertura) -> str:
    obj = r.objetivo
    md = f"### ⚠️ {obj.id} — {obj.titulo}\n\n"
    md += f"**Confianza de cobertura:** {r.confianza:.0%}\n\n"

    if r.requisitos_contribuyentes:
        md += "**Requisitos que contribuyen:**\n\n"
        for contrib in r.requisitos_contribuyentes[:4]:
            icono = "✅" if contrib.tipo_contribucion == "directo" else "🔶"
            md += (
                f"- {icono} `{contrib.requisito_id}` — "
                f"{contrib.titulo_requisito[:60]}  \n"
                f"  _Cubre: {contrib.aspecto_cubierto}_\n"
            )
        md += "\n"

    if r.gaps_detectados:
        md += "**Gaps detectados (sin requisito asociado):**\n\n"
        for gap in r.gaps_detectados:
            md += f"- ❌ {gap}\n"
        md += "\n"

    md += f"**Recomendación:** {r.recomendacion}\n\n"
    return md


def _formatear_objetivo_cubierto(r: ResultadoCobertura) -> str:
    obj = r.objetivo
    directos = [c for c in r.requisitos_contribuyentes if c.tipo_contribucion == "directo"]
    return (
        f"**{obj.id} — {obj.titulo}**  \n"
        f"{len(directos)} requisito(s) con cobertura directa · "
        f"Confianza: {r.confianza:.0%}\n\n"
    )


def _generar_matriz_completa(resultados: list[ResultadoCobertura]) -> str:
    """Genera la tabla resumen de la matriz completa."""
    md = "## Matriz de cobertura completa\n\n"
    md += "| Objetivo | Prioridad | Estado | Confianza | Requisitos | Gaps |\n"
    md += "|---|---|---|---|---|---|\n"

    iconos_estado = {
        "cubierto":       "✅",
        "parcial":        "⚠️",
        "indirecto":      "🔶",
        "sin_cobertura":  "❌"
    }

    for r in resultados:
        obj = r.objetivo
        icono = iconos_estado.get(r.estado, "?")
        n_req = len(r.requisitos_contribuyentes)
        n_gaps = len(r.gaps_detectados)
        reqs = ", ".join(
            c.requisito_id for c in r.requisitos_contribuyentes[:3]
        ) or "—"

        md += (
            f"| **{obj.id}** {obj.titulo[:40]} "
            f"| {obj.prioridad} "
            f"| {icono} {r.estado} "
            f"| {r.confianza:.0%} "
            f"| {reqs} "
            f"| {n_gaps} |\n"
        )

    return md
```

---

## El informe de Meridian

Cuando Carlos ejecutó el análisis sobre EP-04 al cierre del segundo mes del piloto, el informe que obtuvo le reveló algo que no había visto en tres meses de trabajo.

```
# Análisis de cobertura de negocio — Q3 2025

**Estado global:** 🟡 Cobertura con gaps

| Estado                      | Objetivos | %   |
|-----------------------------|-----------|-----|
| ✅ Cubierto completamente   | 1         | 25% |
| ⚠️ Cobertura parcial       | 2         | 50% |
| 🔶 Cobertura indirecta      | 0         | 0%  |
| ❌ Sin cobertura            | 1         | 25% |

---

### ❌ OBJ-02 — Eliminar las facturas duplicadas en el sistema

**KPI:** Facturas duplicadas registradas por mes · Actual: 10 · Objetivo: 0
**Área:** Dirección Financiera

**Recomendación:** Este objetivo no tiene ningún requisito funcional
asociado. Antes del próximo sprint, el analista debería convocar un
taller focalizado en el KPI 'Facturas duplicadas' para identificar
los eventos de negocio que lo mueven.

**Preguntas para el próximo taller con negocio:**

- ¿Cuándo se considera que dos facturas son duplicadas?
  ¿Mismo proveedor, mismo importe, mismo período? ¿O con qué criterio?
- ¿El sistema debe bloquear el registro del duplicado o solo alertar?
- ¿Quién tiene autoridad para confirmar que dos facturas no son
  duplicadas aunque parezcan serlo?
```

El objetivo OBJ-02 llevaba dos meses en la hoja de ruta de Ana López. Aparecía en la presentación trimestral. David Sanz lo había comprometido ante la dirección financiera. Y no existía ni un solo requisito en el repositorio que lo abordara.

El análisis de cobertura no descubrió un problema nuevo. Descubrió un problema que existía desde el principio y que nadie había detectado porque nadie había mirado el repositorio desde el ángulo correcto.

---

## Cuándo ejecutar el análisis

El análisis de cobertura no es un proceso continuo: es una consulta que tiene sentido en momentos específicos del ciclo de vida del proyecto. Ejecutarlo demasiado frecuentemente genera ruido porque el repositorio cambia constantemente durante el análisis activo. Ejecutarlo demasiado infrecuentemente deja que los gaps se acumulen hasta que se detectan en producción.

Los cuatro momentos con mayor retorno son estos.

**Al inicio de cada trimestre**, antes de comprometer el roadmap. Es el momento en que el análisis tiene más impacto porque todavía hay tiempo de ajustar los compromisos o de añadir los requisitos que faltan antes de que empiecen los sprints.

**Al cerrar la fase de Event Storming de un módulo nuevo**. Después de los talleres, antes de empezar a escribir requisitos, el análisis verifica que los eventos identificados en el lienzo realmente responden a todos los objetivos del módulo. Si hay un objetivo sin eventos asociados, es el momento de volver al lienzo, no de descubrirlo tres sprints después.

**Cuando cambian los objetivos de negocio durante el proyecto**. Meridian lo aprendió cuando Ana López revisó los KPIs del módulo a mitad de trimestre: el análisis detectó inmediatamente que dos requisitos ya aprobados habían dejado de ser relevantes y que el nuevo objetivo no tenía cobertura. Sin el análisis, esa información habría llegado en la retrospectiva del sprint siguiente.

**Antes de una auditoría o revisión de producto**. En proyectos regulados o en presentaciones a dirección, el análisis produce exactamente el tipo de evidencia que los auditores piden: una matriz que demuestra que cada objetivo de negocio comprometido tiene al menos un requisito funcional aprobado que lo implementa.

---

## Lo que el análisis no puede hacer

El análisis de cobertura es una herramienta de descubrimiento, no de validación. Detecta lo que falta, pero no puede determinar si lo que existe es suficiente.

Si existe un requisito que declara cubrir OBJ-01, el análisis lo marca como cubierto. Pero no puede saber si ese requisito, cuando se implemente, realmente moverá el KPI de 2,5 días a 1 día de tiempo de cierre contable. Esa evaluación requiere criterios de aceptación bien escritos —que es lo que garantiza el capítulo 4— y test cases ejecutados con datos reales —que es lo que garantiza el capítulo 9.

El análisis tampoco puede detectar objetivos implícitos: los que todo el mundo da por sentado que el sistema debe cumplir pero que nadie articuló en el archivo de objetivos. Un sistema de facturación que pierde datos, que tiene tiempos de respuesta inaceptables o que no es accesible desde dispositivos móviles puede fallar objetivos implícitos que nunca se escribieron. El análisis de cobertura solo trabaja sobre lo que está documentado.

Por eso el primer paso del modelo no es construir el pipeline: es documentar los objetivos de negocio con la misma disciplina con que documentamos los requisitos. Sin ese input, el análisis de cobertura produce una respuesta vacía.

---

> 💡 **Idea clave**
>
> El análisis de cobertura invierte la dirección del pipeline: en lugar de ir de los requisitos a los artefactos, va de los objetivos a los requisitos. Esa inversión revela lo que el flujo habitual oculta: los objetivos que nadie convirtió en funcionalidad implementable.

---

> ⚠️ **Error frecuente**
>
> Ejecutar el análisis de cobertura sobre objetivos vagos: «mejorar la experiencia del usuario», «aumentar la eficiencia», «modernizar el sistema». El LLM encontrará similitud semántica con casi cualquier requisito del repositorio y el informe dirá que todo está cubierto.
>
> Los objetivos necesitan un KPI con valor actual y valor objetivo para que el análisis sea útil. «Reducir el tiempo de cierre contable de 2,5 a 1 día» es un objetivo que el sistema puede cruzar con los requisitos de forma significativa. «Mejorar la eficiencia del proceso contable» no lo es.

---

> 🛠️ **En la práctica**
>
> En los primeros dos o tres meses de uso, el análisis de cobertura tiene una tasa de falsos negativos mayor de lo esperable: detecta gaps que en realidad sí están cubiertos por requisitos que no usaron el vocabulario correcto del objetivo. Eso no es un fallo del sistema: es información útil. Si un requisito cubre un objetivo pero usa vocabulario tan distinto que el RAG no establece la conexión, ese requisito probablemente también confundirá al equipo de desarrollo.
>
> La solución es doble: añadir el ID del objetivo al campo `objetivo_negocio` del requisito (vínculo explícito que el sistema siempre detecta) y revisar si la descripción del requisito usa el lenguaje del objetivo. Esa revisión suele mejorar la calidad del requisito más allá de la cobertura.
