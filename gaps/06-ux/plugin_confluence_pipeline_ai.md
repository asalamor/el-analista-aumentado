# Plugin de Confluence para el Pipeline AI Funcional
## Integración nativa sin salir de Confluence

**Versión:** 1.0  
**Contexto:** Complemento al Modelo Operativo AI-Ready  
**Audiencia:** Analistas funcionales, responsable técnico, champion del pipeline

---

## 1. Por qué un plugin de Confluence y no una herramienta separada

El modelo operativo completo establece que **el usuario de negocio no debe notar el cambio** y que **el analista no debe abandonar su flujo de trabajo habitual**. Ambas premisas chocan con una herramienta externa que el analista debe abrir en una ventana aparte para ejecutar el pipeline.

El plugin de Confluence resuelve esto de forma definitiva: el analista redacta el requisito en Confluence, ejecuta el pipeline desde la misma página, revisa el output en un panel lateral y aprueba el push a Jira sin cambiar de contexto. El usuario de negocio sigue viendo una página de Confluence con una plantilla estructurada. La maquinaria ocurre en el mismo espacio donde ya trabaja.

Hay tres fricciones concretas que el plugin elimina y que sin él frenan la adopción:

**La brecha entre escribir y ejecutar.** Sin el plugin, el analista termina de rellenar el YAML, abre un terminal o una interfaz web distinta, copia el contenido, ejecuta el pipeline y vuelve a Confluence para actualizar el estado. Con el plugin, ese flujo se convierte en un botón.

**La validación fuera de contexto.** El validador automático del punto 6 del modelo detecta problemas mientras el analista escribe, no después. Sin integración en Confluence, esa retroalimentación llega tarde o no llega. Con el plugin, los errores aparecen en un panel lateral mientras se edita el requisito, igual que un corrector ortográfico.

**La aprobación desconectada.** La cola de aprobación del punto 8 es una interfaz separada. El plugin la lleva al propio espacio de trabajo del analista: el JSON aparece en un panel colapsable dentro de la página, el analista lo revisa en contexto y aprueba con un clic.

---

## 2. Opciones de integración en Confluence: análisis comparado

Antes de diseñar el plugin, hay que elegir el mecanismo técnico correcto. Confluence ofrece cuatro vías de extensión con características muy distintas.

### 2.1 Macros de Confluence (Connect / Forge)

Las macros son el mecanismo nativo de Confluence para embeber contenido dinámico en páginas. Existen en dos variantes según la infraestructura del workspace.

**Atlassian Connect** es el modelo clásico para Confluence Cloud y Server. La macro vive en un servidor externo que Confluence consulta por iframe. El desarrollador controla completamente el backend. Es la opción más flexible para integraciones complejas, pero requiere mantener infraestructura propia.

**Atlassian Forge** es el modelo moderno, serverless y hospedado en la infraestructura de Atlassian. El código se ejecuta en el runtime de Forge sin necesidad de servidor propio. Tiene límites de ejecución más estrictos pero reduce significativamente la carga operativa.

Para este modelo, **Forge es la recomendación** si el workspace es Confluence Cloud y el equipo no tiene recursos para mantener infraestructura adicional. Connect es preferible si el workspace es Server/Data Center o si el pipeline necesita más de los límites de ejecución de Forge (que son suficientes para los casos de uso aquí descritos).

### 2.2 Panel lateral (Confluence Connect Panel)

Los paneles laterales son extensiones que aparecen en la barra derecha de cualquier página de Confluence. No modifican el contenido de la página: se superponen como un asistente contextual. Son ideales para mostrar el estado del pipeline, las sugerencias del RAG y los resultados de la validación sin interferir con la edición.

### 2.3 Macro de página (Page Macro)

Las macros de página se insertan directamente en el contenido de la página. Permiten embeber formularios interactivos, botones de acción y visualizaciones dentro del cuerpo del documento. Son el mecanismo correcto para la vista estructurada del requisito y para el botón de ejecución del pipeline.

### 2.4 Extensión de teclado / Slash Command

Confluence permite registrar comandos de barra inclinada (`/`) que el analista puede invocar mientras escribe. Son útiles para insertar la plantilla YAML estructurada con un solo comando sin necesidad de copiar y pegar.

**La arquitectura recomendada combina los tres últimos mecanismos** con roles distintos:

| Mecanismo | Rol en el plugin |
|---|---|
| Slash command `/ai-requisito` | Insertar la plantilla YAML en el cuerpo de la página |
| Page macro `{pipeline-ai}` | Botones de acción: Validar, Generar, Aprobar |
| Panel lateral | Estado del pipeline, sugerencias RAG, historial de runs |

---

## 3. Arquitectura técnica del plugin

### 3.1 Visión general

```
┌─────────────────────────────────────────────────────────────┐
│  CONFLUENCE (navegador del analista)                        │
│                                                             │
│  ┌─────────────────────────────────┐  ┌──────────────────┐ │
│  │  PÁGINA DE REQUISITO            │  │  PANEL LATERAL   │ │
│  │                                 │  │                  │ │
│  │  [Contenido YAML / plantilla]   │  │  Estado pipeline │ │
│  │                                 │  │  Validación live │ │
│  │  ╔══════════════════════╗       │  │  Sugerencias RAG │ │
│  │  ║  MACRO pipeline-ai   ║       │  │  Historial runs  │ │
│  │  ║  [Validar] [Generar] ║       │  │                  │ │
│  │  ║  [Ver output] [Aprobar]      │  │                  │ │
│  │  ╚══════════════════════╝       │  │                  │ │
│  └─────────────────────────────────┘  └──────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │ API REST (Forge Functions / Connect)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  BACKEND DEL PLUGIN                                         │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Extractor  │  │  Validador   │  │  Orquestador     │  │
│  │  YAML       │  │  (punto 6)   │  │  (orchestrator   │  │
│  │             │  │              │  │   .py)           │  │
│  └──────┬──────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                │                    │            │
│         └────────────────┴────────────────────┘            │
│                          │                                 │
│  ┌───────────────────────▼──────────────────────────────┐  │
│  │  Orquestador principal (orchestrator.py via API)     │  │
│  │  Pasos 1-9: validación, RAG, generación, push Jira   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes del backend del plugin

El plugin no reimplementa la lógica del pipeline: la invoca. El backend del plugin es una capa delgada de integración que:

- Extrae el YAML del cuerpo de la página de Confluence usando la API de Confluence.
- Llama al `orchestrator.py` existente (punto 12 del modelo) como proceso o como API REST.
- Devuelve el resultado al frontend del plugin.
- Gestiona el estado del run asociado a la página de Confluence.

Esto es deliberado: **el plugin no duplica lógica de negocio**. Toda la inteligencia sigue en el orquestador. El plugin es solo la interfaz de usuario.

### 3.3 Modelo de datos del plugin

El plugin necesita persistir el vínculo entre una página de Confluence y el estado del pipeline. Atlassian Forge ofrece un almacén clave-valor nativo (`@forge/kvstore`) que cubre esta necesidad sin base de datos adicional.

```javascript
// Estructura del estado por página de Confluence
{
  "page_id": "123456789",
  "requisito_id": "REQ-023",           // Extraído del YAML
  "ultimo_run": {
    "run_id": "REQ-023_20250512_101532",
    "estado": "pendiente_aprobacion",   // iniciada | validacion_fallida |
                                        // pendiente_aprobacion | completado | fallido
    "timestamp": "2025-05-12T10:15:32Z",
    "score_validacion": 84,
    "artefactos_generados": {...},       // JSON del pipeline
    "test_cases_generados": [...],
    "informe_validacion": {...},
    "resultado_jira": null              // Se rellena tras el push
  },
  "historial_runs": [
    // Últimos 10 runs para el panel de historial
  ],
  "sugerencias_rag": [
    // Requisitos relacionados recuperados en el último análisis
  ]
}
```

---

## 4. El slash command: `/ai-requisito`

### 4.1 Comportamiento

Cuando el analista escribe `/ai-requisito` en el cuerpo de una página de Confluence, aparece el comando en el menú de sugerencias. Al seleccionarlo, el plugin inserta la plantilla YAML completa del modelo (punto 1 del modelo operativo) con todos los campos pre-rellenados con valores de ejemplo y comentarios guía.

Esto reemplaza el proceso actual de copiar la plantilla desde otro documento o recordar los campos obligatorios.

### 4.2 Implementación (Forge)

```javascript
// src/slash-command/index.js
import ForgeUI, { render, Text, ContentAction } from '@forge/ui';
import { useProductContext } from '@forge/ui';
import api, { route } from '@forge/api';

const PLANTILLA_YAML = `
requisito:
  # ─── BLOQUE 1: IDENTIDAD ───────────────────────────────
  id: REQ-000                    # Formato: REQ-NNN. Nunca reutilizar IDs.
  titulo: ""                     # Máx. 80 chars. Empieza por sustantivo o verbo en infinitivo.
  version: "1.0"
  estado: borrador               # borrador | en-revision | validado | rechazado | deprecado
  epica: EP-00                   # Debe existir en el catálogo de épicas.
  modulo: ""
  origen:
    solicitante: ""
    area: ""
    fecha_solicitud: ""          # YYYY-MM-DD
    referencia: ""
  analista: ""

  # ─── BLOQUE 2: CONTEXTO DE NEGOCIO ──────────────────────
  actor: ""                      # Rol del glosario. NUNCA "el usuario".
  actores_secundarios: []
  evento_disparador: ""          # Situación concreta que activa este requisito.
  objetivo_negocio: ""           # Por qué existe. Mínimo 20 palabras.
  descripcion: ""                # Narrativa en lenguaje de negocio. Mínimo 30 palabras.
  prioridad: must-have           # must-have | should-have | could-have | wont-have
  reglas_negocio:
    - ""
  dependencias:
    requisitos: []
    sistemas: []
    decisiones: []

  # ─── BLOQUE 3: COMPORTAMIENTO ESPERADO ──────────────────
  flujo_principal:
    - paso: 1
      actor: ""
      accion: ""
      resultado: ""
  flujos_alternativos: []
  excepciones:
    - condicion: ""              # Mínimo una por campo obligatorio de entrada.
      comportamiento: ""
  criterios_aceptacion:
    - id: AC-000-01
      titulo: ""
      dado: ""                   # Estado previo del sistema. NO una acción.
      cuando: ""                 # UNA acción concreta.
      entonces: ""               # Resultado observable. Verificable con true/false.
      tipo: positivo             # positivo | negativo | contorno
      datos_ejemplo: {}
  definition_of_done:
    - "Todos los criterios de aceptación superan las pruebas de regresión"
    - "Revisión de código aprobada"

  # ─── BLOQUE 4: DATOS ────────────────────────────────────
  datos_entrada:
    - nombre: ""
      tipo: ""                   # string | integer | decimal | boolean | date | enum | ...
      requerido: true
      formato: ""
      longitud_max: null
      rango:
        min: null
        max: null
      valores_enum: []
      valor_defecto: null
      descripcion: ""
  datos_salida:
    campos: []
    formato: ""                  # JSON | CSV | PDF | pantalla | email
    paginacion:
      aplica: false
      tamanyo_pagina_defecto: null
      max_registros: null
    orden_defecto: ""
    tiempo_respuesta_max_ms: null

  # ─── BLOQUE 5: METADATOS TÉCNICOS (completa el equipo técnico) ──
  componentes_afectados: []
  integraciones_externas: []
  restricciones_no_funcionales:
    rendimiento: ""
    seguridad: ""
    disponibilidad: ""
    accesibilidad: ""
    volumen_datos: ""
  notas_implementacion: ""
  trazabilidad:
    historias_generadas: []      # Auto-rellenado por el pipeline.
    test_cases_generados: []     # Auto-rellenado por el pipeline.
    jira_issues: []              # Auto-rellenado por el pipeline.
`;

const App = () => {
  const context = useProductContext();

  const insertarPlantilla = async () => {
    const pageId = context.contentId;
    // Obtener el contenido actual de la página
    const response = await api
      .asUser()
      .requestConfluence(route`/wiki/rest/api/content/${pageId}?expand=body.storage,version`);
    const page = await response.json();

    // Insertar la plantilla como bloque de código YAML
    const plantillaHtml = `
      <ac:structured-macro ac:name="code" ac:schema-version="1">
        <ac:parameter ac:name="language">yaml</ac:parameter>
        <ac:plain-text-body><![CDATA[${PLANTILLA_YAML}]]></ac:plain-text-body>
      </ac:structured-macro>
    `;

    // Actualizar la página
    await api.asUser().requestConfluence(
      route`/wiki/rest/api/content/${pageId}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          version: { number: page.version.number + 1 },
          title: page.title,
          type: 'page',
          body: {
            storage: {
              value: page.body.storage.value + plantillaHtml,
              representation: 'storage'
            }
          }
        })
      }
    );
  };

  return (
    <ContentAction>
      <Text>Plantilla AI-Ready insertada correctamente.</Text>
    </ContentAction>
  );
};

export const run = render(<App />);
```

---

## 5. La macro de página: `{pipeline-ai}`

La macro es el componente central del plugin. Se inserta al final de cualquier página de requisito y proporciona los controles de acción del pipeline en contexto.

### 5.1 Estados de la macro

La macro muestra una interfaz diferente según el estado del pipeline para esa página. No es una interfaz estática: refleja el estado real del último run.

**Estado: Sin ejecutar**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-000                                       ║
╠══════════════════════════════════════════════════════════════╣
║  Este requisito aún no ha sido procesado.                    ║
║                                                              ║
║  [  Validar calidad  ]   [  Generar artefactos  ]            ║
╚══════════════════════════════════════════════════════════════╝
```

**Estado: Validación en curso**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-023                    ⟳ Validando...    ║
╠══════════════════════════════════════════════════════════════╣
║  Analizando estructura · Verificando semántica               ║
║  Comprobando consistencia con el repositorio...              ║
║                                                              ║
║  ████████████░░░░░░░░  65%                                   ║
╚══════════════════════════════════════════════════════════════╝
```

**Estado: Validación completada con advertencias**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-023          ⚠ Aprobado con advertencias ║
╠══════════════════════════════════════════════════════════════╣
║  Score: 84/100                                               ║
║                                                              ║
║  ⚠  [datos_entrada → fecha_inicio]  Formato no especificado  ║
║  ⚠  [excepciones]  Sin excepción para error de servidor      ║
║                                                              ║
║  [  Generar artefactos de todos modos  ]   [  Corregir  ]    ║
╚══════════════════════════════════════════════════════════════╝
```

**Estado: Bloqueado por problemas críticos**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-028                         ✗ BLOQUEADO  ║
╠══════════════════════════════════════════════════════════════╣
║  Score: 34/100  ·  2 problemas bloqueantes                   ║
║                                                              ║
║  ✗  [titulo]  Verbo ambiguo "gestionar". Especificar         ║
║               la operación concreta.                         ║
║  ✗  [criterios_aceptacion → AC-028-01 → entonces]            ║
║               "el sistema funciona correctamente" no         ║
║               es verificable.                                ║
║                                                              ║
║  El pipeline no puede continuar hasta resolver los           ║
║  problemas bloqueantes.                                      ║
║                                                              ║
║  [  Ver informe completo  ]   [  Abrir modo edición  ]       ║
╚══════════════════════════════════════════════════════════════╝
```

**Estado: Pendiente de aprobación**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-023           ⏸ Pendiente de aprobación  ║
╠══════════════════════════════════════════════════════════════╣
║  Artefactos generados · Pendiente revisión humana            ║
║                                                              ║
║  HISTORIA GENERADA:                                          ║
║  "Como gestor de facturación, quiero filtrar facturas        ║
║  por rango de fechas para localizar documentos de un         ║
║  período contable"   · 5 SP · Must Have                      ║
║                                                              ║
║  · 4 tareas técnicas (BD · backend · frontend · testing)     ║
║  · 3 criterios de aceptación                                 ║
║  · 9 test cases (2 pos · 4 neg · 3 contorno)                 ║
║                                                              ║
║  [  Ver JSON completo  ]   [  Aprobar → Push Jira  ]         ║
║  [  Editar antes de aprobar  ]   [  Rechazar  ]              ║
╚══════════════════════════════════════════════════════════════╝
```

**Estado: Completado**

```
╔══════════════════════════════════════════════════════════════╗
║  Pipeline AI — REQ-023                        ✓ Completado  ║
╠══════════════════════════════════════════════════════════════╣
║  Historia: FACT-47   Tareas: FACT-48, 49, 50, 51            ║
║  Test cases en Xray: 9                                       ║
║  Última ejecución: 12/05/2025 10:15                          ║
║                                                              ║
║  [  Ver en Jira  ]   [  Regenerar  ]   [  Ver trazabilidad  ]║
╚══════════════════════════════════════════════════════════════╝
```

### 5.2 Implementación de la macro (Forge / React)

```javascript
// src/macro/index.jsx
import ForgeUI, {
  render, Macro, useState, useEffect,
  Button, ButtonSet, Text, Heading,
  SectionMessage, Tag, Spinner,
  Fragment, Strong, Em, Code
} from '@forge/ui';
import { useProductContext } from '@forge/ui';
import { storage } from '@forge/kvstore';
import api, { route } from '@forge/api';

// ─── Constantes de estado ─────────────────────────────────────────
const ESTADOS = {
  SIN_EJECUTAR:          'sin_ejecutar',
  VALIDANDO:             'validando',
  VALIDACION_FALLIDA:    'validacion_fallida',
  VALIDACION_ADVERTENCIA:'validacion_advertencia',
  GENERANDO:             'generando',
  PENDIENTE_APROBACION:  'pendiente_aprobacion',
  APROBANDO:             'aprobando',
  COMPLETADO:            'completado',
  FALLIDO:               'fallido'
};

// ─── Componente principal ─────────────────────────────────────────
const MacroPipelineAI = () => {
  const context = useProductContext();
  const pageId = context.contentId;

  // Estado del plugin
  const [estadoPipeline, setEstadoPipeline] = useState(ESTADOS.SIN_EJECUTAR);
  const [runData, setRunData] = useState(null);
  const [mensaje, setMensaje] = useState('');
  const [cargando, setCargando] = useState(false);

  // Cargar estado persistido al montar el componente
  useEffect(async () => {
    const estadoGuardado = await storage.get(`pipeline:${pageId}`);
    if (estadoGuardado) {
      setEstadoPipeline(estadoGuardado.ultimo_run?.estado || ESTADOS.SIN_EJECUTAR);
      setRunData(estadoGuardado.ultimo_run);
    }
  }, []);

  // ── Acción: Validar ──────────────────────────────────────────────
  const handleValidar = async () => {
    setCargando(true);
    setEstadoPipeline(ESTADOS.VALIDANDO);
    setMensaje('');

    try {
      // 1. Extraer el YAML de la página
      const yamlContent = await extraerYamlDePagina(pageId);
      if (!yamlContent) {
        setMensaje('No se encontró un bloque YAML válido en esta página. Usa /ai-requisito para insertar la plantilla.');
        setEstadoPipeline(ESTADOS.FALLIDO);
        setCargando(false);
        return;
      }

      // 2. Llamar al endpoint de validación del backend del plugin
      const respuesta = await api.asApp().requestBackend(
        '/pipeline/validar',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            page_id: pageId,
            yaml_content: yamlContent
          })
        }
      );
      const resultado = await respuesta.json();

      // 3. Persistir el estado
      const nuevoEstado = resultado.veredicto === 'BLOQUEADO'
        ? ESTADOS.VALIDACION_FALLIDA
        : resultado.veredicto === 'APROBADO_CON_ADVERTENCIAS'
          ? ESTADOS.VALIDACION_ADVERTENCIA
          : ESTADOS.SIN_EJECUTAR;  // APROBADO → listo para generar

      await storage.set(`pipeline:${pageId}`, {
        ultimo_run: { estado: nuevoEstado, ...resultado }
      });

      setEstadoPipeline(nuevoEstado);
      setRunData(resultado);
    } catch (error) {
      setMensaje(`Error de comunicación: ${error.message}`);
      setEstadoPipeline(ESTADOS.FALLIDO);
    } finally {
      setCargando(false);
    }
  };

  // ── Acción: Generar artefactos ────────────────────────────────────
  const handleGenerar = async () => {
    setCargando(true);
    setEstadoPipeline(ESTADOS.GENERANDO);

    try {
      const yamlContent = await extraerYamlDePagina(pageId);

      const respuesta = await api.asApp().requestBackend(
        '/pipeline/generar',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            page_id: pageId,
            yaml_content: yamlContent,
            dry_run: false
          })
        }
      );
      const resultado = await respuesta.json();

      await storage.set(`pipeline:${pageId}`, {
        ultimo_run: {
          estado: ESTADOS.PENDIENTE_APROBACION,
          ...resultado
        }
      });

      setEstadoPipeline(ESTADOS.PENDIENTE_APROBACION);
      setRunData(resultado);
    } catch (error) {
      setMensaje(`Error generando artefactos: ${error.message}`);
      setEstadoPipeline(ESTADOS.FALLIDO);
    } finally {
      setCargando(false);
    }
  };

  // ── Acción: Aprobar y push a Jira ────────────────────────────────
  const handleAprobar = async () => {
    setCargando(true);
    setEstadoPipeline(ESTADOS.APROBANDO);

    try {
      const respuesta = await api.asApp().requestBackend(
        '/pipeline/aprobar',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            page_id: pageId,
            run_id: runData?.run_id,
            aprobado_por: context.accountId
          })
        }
      );
      const resultado = await respuesta.json();

      await storage.set(`pipeline:${pageId}`, {
        ultimo_run: {
          estado: ESTADOS.COMPLETADO,
          ...resultado
        }
      });

      setEstadoPipeline(ESTADOS.COMPLETADO);
      setRunData(resultado);

      // Actualizar el campo de estado en la propiedad de la página
      await actualizarEstadoPagina(pageId, 'validado');
    } catch (error) {
      setMensaje(`Error en el push a Jira: ${error.message}`);
      setEstadoPipeline(ESTADOS.FALLIDO);
    } finally {
      setCargando(false);
    }
  };

  // ── Acción: Rechazar ─────────────────────────────────────────────
  const handleRechazar = async () => {
    await storage.set(`pipeline:${pageId}`, {
      ultimo_run: {
        ...runData,
        estado: ESTADOS.SIN_EJECUTAR,
        rechazado_en: new Date().toISOString()
      }
    });
    setEstadoPipeline(ESTADOS.SIN_EJECUTAR);
    setRunData(null);
  };

  // ── Renderizado según estado ──────────────────────────────────────
  return (
    <Fragment>
      {renderCabecera(runData)}
      {renderContenidoSegunEstado(
        estadoPipeline, runData, cargando, mensaje,
        handleValidar, handleGenerar, handleAprobar, handleRechazar
      )}
    </Fragment>
  );
};

// ─── Renders auxiliares ──────────────────────────────────────────
const renderCabecera = (runData) => (
  <Fragment>
    <Heading size="medium">
      Pipeline AI {runData?.requisito_id ? `— ${runData.requisito_id}` : ''}
    </Heading>
  </Fragment>
);

const renderContenidoSegunEstado = (
  estado, runData, cargando, mensaje,
  onValidar, onGenerar, onAprobar, onRechazar
) => {
  if (cargando) {
    return (
      <Fragment>
        <Spinner size="medium" />
        <Text>{mensaje || 'Procesando...'}</Text>
      </Fragment>
    );
  }

  switch (estado) {
    case ESTADOS.SIN_EJECUTAR:
      return (
        <Fragment>
          <Text>Este requisito aún no ha sido procesado por el pipeline.</Text>
          <ButtonSet>
            <Button text="Validar calidad" onClick={onValidar} />
            <Button text="Generar artefactos" onClick={onGenerar} appearance="primary" />
          </ButtonSet>
        </Fragment>
      );

    case ESTADOS.VALIDACION_FALLIDA:
      return (
        <Fragment>
          <SectionMessage appearance="error"
            title={`Score: ${runData?.score}/100 · BLOQUEADO`}>
            {(runData?.bloqueantes || []).slice(0, 3).map((p, i) => (
              <Text key={i}>
                <Strong>[{p.campo}]</Strong> {p.problema}
              </Text>
            ))}
          </SectionMessage>
          <ButtonSet>
            <Button text="Ver informe completo" href={runData?.informe_url} />
          </ButtonSet>
        </Fragment>
      );

    case ESTADOS.VALIDACION_ADVERTENCIA:
      return (
        <Fragment>
          <SectionMessage appearance="warning"
            title={`Score: ${runData?.score}/100 · Con advertencias`}>
            {(runData?.advertencias || []).slice(0, 3).map((a, i) => (
              <Text key={i}>
                <Em>[{a.campo}]</Em> {a.problema}
              </Text>
            ))}
          </SectionMessage>
          <ButtonSet>
            <Button text="Generar de todos modos"
              onClick={onGenerar} appearance="primary" />
          </ButtonSet>
        </Fragment>
      );

    case ESTADOS.PENDIENTE_APROBACION:
      const historia = runData?.artefactos?.historia;
      const tareas = runData?.artefactos?.tareas || [];
      const tcs = runData?.test_cases || [];
      return (
        <Fragment>
          <SectionMessage appearance="info" title="Artefactos generados · Pendiente revisión">
            <Text><Strong>Historia:</Strong> {historia?.summary}</Text>
            <Text><Strong>Story Points:</Strong> {historia?.story_points}
              &nbsp;&nbsp;<Strong>Prioridad:</Strong> {historia?.priority}</Text>
            <Text><Strong>Criterios AC:</Strong> {historia?.acceptance_criteria?.length || 0}</Text>
            <Text><Strong>Tareas:</Strong> {tareas.length}
              ({tareas.map(t => t.capa).join(' · ')})</Text>
            <Text><Strong>Test cases:</Strong> {tcs.length}
              ({tcs.filter(t => t.tipo?.includes('positivo')).length} pos ·&nbsp;
              {tcs.filter(t => t.tipo?.includes('negativo')).length} neg ·&nbsp;
              {tcs.filter(t => t.tipo?.includes('contorno')).length} contorno)</Text>
          </SectionMessage>
          <ButtonSet>
            <Button text="Aprobar → Push Jira" onClick={onAprobar} appearance="primary" />
            <Button text="Ver JSON completo" href={runData?.json_preview_url} />
            <Button text="Rechazar" onClick={onRechazar} appearance="subtle" />
          </ButtonSet>
        </Fragment>
      );

    case ESTADOS.COMPLETADO:
      const jira = runData?.resultado_jira;
      return (
        <Fragment>
          <SectionMessage appearance="confirmation"
            title="Pipeline completado">
            <Text><Strong>Historia:</Strong> {jira?.historia_key}</Text>
            <Text><Strong>Tareas:</Strong> {(jira?.tareas_keys || []).join(', ')}</Text>
            <Text><Strong>Test cases:</Strong> {runData?.test_cases?.length || 0} en Xray</Text>
          </SectionMessage>
          <ButtonSet>
            <Button text="Ver en Jira" href={runData?.jira_url} />
            <Button text="Ver trazabilidad" href={runData?.trazabilidad_url} />
            <Button text="Regenerar" onClick={onGenerar} appearance="subtle" />
          </ButtonSet>
        </Fragment>
      );

    default:
      return <Text>{mensaje || 'Estado desconocido.'}</Text>;
  }
};

// ─── Utilidades ──────────────────────────────────────────────────
const extraerYamlDePagina = async (pageId) => {
  const respuesta = await api
    .asUser()
    .requestConfluence(route`/wiki/rest/api/content/${pageId}?expand=body.storage`);
  const pagina = await respuesta.json();
  const contenido = pagina.body.storage.value;

  // Extraer el contenido de los bloques de código YAML
  const regex = /<ac:plain-text-body><!\[CDATA\[([\s\S]*?)\]\]><\/ac:plain-text-body>/g;
  const coincidencias = [];
  let m;
  while ((m = regex.exec(contenido)) !== null) {
    coincidencias.push(m[1]);
  }

  // Devolver el primer bloque YAML que contenga la clave 'requisito:'
  const yamlReq = coincidencias.find(y => y.includes('requisito:') || y.includes('id: REQ'));
  return yamlReq || null;
};

const actualizarEstadoPagina = async (pageId, nuevoEstado) => {
  // Actualizar una propiedad de página para reflejar el estado del requisito
  await api.asUser().requestConfluence(
    route`/wiki/rest/api/content/${pageId}/property/pipeline-estado`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        key: 'pipeline-estado',
        value: { estado: nuevoEstado, timestamp: new Date().toISOString() }
      })
    }
  );
};

export const run = render(<Macro app={<MacroPipelineAI />} />);
```

---

## 6. El panel lateral: asistente contextual permanente

El panel lateral es el componente que proporciona retroalimentación continua mientras el analista escribe, sin interferir con la edición. Aparece en la barra derecha de la página y se actualiza automáticamente al detectar cambios en el contenido.

### 6.1 Secciones del panel

**Sección A: Estado actual**

Muestra el score de la última validación con un indicador visual (semáforo) y el estado del pipeline para esa página.

**Sección B: Sugerencias del RAG**

Lista los requisitos del repositorio semánticamente relacionados con el que se está editando. Permite al analista detectar posibles duplicados y consultar cómo se resolvieron casos similares antes de escribir.

**Sección C: Campos pendientes**

Lista los campos obligatorios que aún están vacíos o tienen valores por defecto sin rellenar. Se actualiza en tiempo real al guardar la página.

**Sección D: Historial de runs**

Los últimos cinco runs del pipeline para esta página con su estado, fecha y resultado.

### 6.2 Implementación del panel (Forge)

```javascript
// src/panel/index.jsx
import ForgeUI, {
  render, SidebarPanel,
  Heading, Text, Strong, Em, Tag,
  Link, Fragment, useEffect, useState
} from '@forge/ui';
import { useProductContext } from '@forge/ui';
import { storage } from '@forge/kvstore';
import api, { route } from '@forge/api';

const PanelPipelineAI = () => {
  const context = useProductContext();
  const pageId = context.contentId;

  const [estadoPanel, setEstadoPanel] = useState(null);
  const [sugerenciasRag, setSugerenciasRag] = useState([]);
  const [camposPendientes, setCamposPendientes] = useState([]);
  const [historialRuns, setHistorialRuns] = useState([]);
  const [cargandoRag, setCargandoRag] = useState(false);

  useEffect(async () => {
    // Cargar el estado del pipeline para esta página
    const datos = await storage.get(`pipeline:${pageId}`);
    if (datos) {
      setEstadoPanel(datos.ultimo_run);
      setHistorialRuns(datos.historial_runs || []);
      setSugerenciasRag(datos.sugerencias_rag || []);
    }

    // Analizar campos pendientes en el YAML actual
    const yamlContent = await extraerYamlDePagina(pageId);
    if (yamlContent) {
      const pendientes = analizarCamposPendientes(yamlContent);
      setCamposPendientes(pendientes);

      // Obtener sugerencias RAG en segundo plano
      setCargandoRag(true);
      try {
        const resp = await api.asApp().requestBackend(
          '/rag/sugerencias',
          {
            method: 'POST',
            body: JSON.stringify({ yaml_content: yamlContent })
          }
        );
        const resultado = await resp.json();
        setSugerenciasRag(resultado.sugerencias || []);

        // Persistir las sugerencias para la próxima apertura
        const datosActuales = await storage.get(`pipeline:${pageId}`) || {};
        await storage.set(`pipeline:${pageId}`, {
          ...datosActuales,
          sugerencias_rag: resultado.sugerencias
        });
      } catch (e) {
        // Las sugerencias RAG no son críticas; silenciar el error
      } finally {
        setCargandoRag(false);
      }
    }
  }, []);

  return (
    <SidebarPanel>

      {/* ── Sección A: Estado actual ────────────────────────────── */}
      <Heading size="small">Estado del pipeline</Heading>
      {estadoPanel ? (
        <Fragment>
          <Tag
            text={estadoPanel.estado?.toUpperCase() || 'SIN EJECUTAR'}
            color={colorPorEstado(estadoPanel.estado)}
          />
          {estadoPanel.score && (
            <Text>Score: <Strong>{estadoPanel.score}/100</Strong></Text>
          )}
          {estadoPanel.resultado_jira?.historia_key && (
            <Text>
              Jira: <Link href={estadoPanel.jira_url}>
                {estadoPanel.resultado_jira.historia_key}
              </Link>
            </Text>
          )}
        </Fragment>
      ) : (
        <Text><Em>Sin ejecutar todavía</Em></Text>
      )}

      {/* ── Sección B: Campos pendientes ────────────────────────── */}
      {camposPendientes.length > 0 && (
        <Fragment>
          <Heading size="small">Campos por completar</Heading>
          {camposPendientes.slice(0, 5).map((campo, i) => (
            <Text key={i}>
              · <Em>{campo.nombre}</Em>
              {campo.obligatorio ? ' (obligatorio)' : ''}
            </Text>
          ))}
          {camposPendientes.length > 5 && (
            <Text><Em>+{camposPendientes.length - 5} más</Em></Text>
          )}
        </Fragment>
      )}

      {/* ── Sección C: Sugerencias del RAG ──────────────────────── */}
      <Heading size="small">Requisitos relacionados</Heading>
      {cargandoRag ? (
        <Text><Em>Consultando repositorio...</Em></Text>
      ) : sugerenciasRag.length > 0 ? (
        <Fragment>
          {sugerenciasRag.slice(0, 4).map((sug, i) => (
            <Fragment key={i}>
              <Tag
                text={sug.relacion}
                color={sug.similitud_pct > 90 ? 'red' : 'blue'}
              />
              <Text>
                <Link href={sug.confluence_url || '#'}>
                  {sug.requisito_id}
                </Link>
                {' '}{sug.titulo?.slice(0, 50)}
                {' '}<Em>({sug.similitud_pct}%)</Em>
              </Text>
            </Fragment>
          ))}
        </Fragment>
      ) : (
        <Text><Em>No se encontraron requisitos similares en el repositorio.</Em></Text>
      )}

      {/* ── Sección D: Historial de runs ─────────────────────────── */}
      {historialRuns.length > 0 && (
        <Fragment>
          <Heading size="small">Historial</Heading>
          {historialRuns.slice(0, 5).map((run, i) => (
            <Text key={i}>
              <Tag
                text={run.estado}
                color={run.estado === 'completado' ? 'green' : 'grey'}
              />
              {' '}<Em>{run.timestamp?.slice(0, 10)}</Em>
            </Text>
          ))}
        </Fragment>
      )}

    </SidebarPanel>
  );
};

// ─── Utilidades del panel ────────────────────────────────────────
const colorPorEstado = (estado) => {
  const mapa = {
    'completado':            'green',
    'pendiente_aprobacion':  'blue',
    'validacion_advertencia':'yellow',
    'validacion_fallida':    'red',
    'fallido':               'red',
    'generando':             'purple',
    'validando':             'purple',
  };
  return mapa[estado] || 'grey';
};

const analizarCamposPendientes = (yamlContent) => {
  // Lista de campos obligatorios y su detección en el YAML
  const camposObligatorios = [
    { nombre: 'titulo',              patron: /titulo:\s*""\s*$/ },
    { nombre: 'actor',               patron: /actor:\s*""\s*$/ },
    { nombre: 'descripcion',         patron: /descripcion:\s*""\s*$/ },
    { nombre: 'evento_disparador',   patron: /evento_disparador:\s*""\s*$/ },
    { nombre: 'objetivo_negocio',    patron: /objetivo_negocio:\s*""\s*$/ },
    { nombre: 'criterios_aceptacion',patron: /- id: AC-000-01/ }
  ];

  return camposObligatorios
    .filter(c => c.patron.test(yamlContent))
    .map(c => ({ nombre: c.nombre, obligatorio: true }));
};

// Reusar la función extraerYamlDePagina del módulo de macro
const extraerYamlDePagina = async (pageId) => {
  const respuesta = await api
    .asUser()
    .requestConfluence(route`/wiki/rest/api/content/${pageId}?expand=body.storage`);
  const pagina = await respuesta.json();
  const contenido = pagina.body.storage.value;
  const regex = /<ac:plain-text-body><!\[CDATA\[([\s\S]*?)\]\]><\/ac:plain-text-body>/g;
  let m;
  while ((m = regex.exec(contenido)) !== null) {
    if (m[1].includes('requisito:') || m[1].includes('id: REQ')) return m[1];
  }
  return null;
};

export const run = render(<PanelPipelineAI />);
```

---

## 7. El backend del plugin: endpoints de la API

El backend recibe las peticiones del frontend (macro y panel) y las traduce en llamadas al `orchestrator.py` existente. Es deliberadamente delgado: no contiene lógica de negocio propia.

### 7.1 Endpoint: POST /pipeline/validar

```python
# backend/routes/validar.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yaml
import asyncio

from pipeline_ai.steps.s2_validate import validar_requisito
from pipeline_ai.config import PipelineConfig
from pipeline_ai.state import GestorEstado

router = APIRouter()
config = PipelineConfig()
gestor = GestorEstado(config.carpeta_runs)

class SolicitudValidacion(BaseModel):
    page_id: str
    yaml_content: str

@router.post("/pipeline/validar")
async def validar(solicitud: SolicitudValidacion):
    """
    Valida el YAML de un requisito y devuelve el informe de calidad.
    Llamado desde la macro de Confluence al pulsar "Validar calidad".
    """
    try:
        requisito = yaml.safe_load(solicitud.yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(
            status_code=400,
            detail=f"YAML inválido: {str(e)}"
        )

    glosario = _cargar_glosario(config)

    informe = await validar_requisito(
        requisito=requisito,
        glosario=glosario,
        config=config
    )

    # Formato simplificado para el frontend del plugin
    return {
        "requisito_id":  requisito.get("id", "REQ-000"),
        "score":         informe.get("puntuacion_global", {}).get("valor", 0),
        "veredicto":     informe.get("veredicto_final", "BLOQUEADO"),
        "bloqueantes": [
            {"campo": p.get("campo"), "problema": p.get("problema")}
            for p in informe.get("problemas_por_prioridad", {}).get("bloqueantes", [])
        ],
        "advertencias": [
            {"campo": p.get("campo"), "problema": p.get("problema")}
            for p in informe.get("problemas_por_prioridad", {}).get("advertencias", [])
        ],
        "proximos_pasos": informe.get("proximos_pasos", []),
        "informe_completo": informe
    }
```

### 7.2 Endpoint: POST /pipeline/generar

```python
# backend/routes/generar.py
from fastapi import APIRouter
from pydantic import BaseModel

from pipeline_ai.orchestrator import ejecutar_pipeline_requisito
from pipeline_ai.config import PipelineConfig
from pipeline_ai.state import GestorEstado

router = APIRouter()
config = PipelineConfig()
gestor = GestorEstado(config.carpeta_runs)

class SolicitudGeneracion(BaseModel):
    page_id: str
    yaml_content: str
    dry_run: bool = True  # Por defecto dry_run hasta aprobación explícita

@router.post("/pipeline/generar")
async def generar(solicitud: SolicitudGeneracion):
    """
    Ejecuta los pasos 1-7 del pipeline (carga, validación, RAG,
    generación de artefactos y test cases, trazabilidad).
    No hace push a Jira: devuelve los artefactos para revisión.
    Llamado al pulsar "Generar artefactos" en la macro.
    """
    # Guardar el YAML temporalmente para que el orquestador lo encuentre
    import tempfile, os, yaml
    requisito = yaml.safe_load(solicitud.yaml_content)
    req_id = requisito.get("id", "REQ-TEMP")

    tmp_dir = config.repo_requisitos / "_temp"
    tmp_dir.mkdir(exist_ok=True)
    ruta_tmp = tmp_dir / f"{req_id}.yaml"
    ruta_tmp.write_text(solicitud.yaml_content, encoding="utf-8")

    try:
        # Ejecutar el orquestador en modo dry_run + sin aprobación
        config_run = PipelineConfig(
            dry_run=True,
            modo_interactivo=False  # No interrumpir para aprobación
        )

        resultado = await ejecutar_pipeline_requisito(
            requisito_id=req_id,
            config=config_run,
            gestor=gestor
        )

        # Leer el estado del run para obtener los artefactos generados
        from pipeline_ai.state import GestorEstado
        gs = GestorEstado(config.carpeta_runs)
        # El run se creó internamente; recuperar por req_id
        run = gs._buscar_run_reanudable(req_id, "")  # Último run

        return {
            "exito":               resultado.get("exito", False),
            "run_id":              resultado.get("run_id"),
            "requisito_id":        req_id,
            "artefactos": {
                "historia": run.artefactos_generados.get("historia") if run else None,
                "tareas":   run.artefactos_generados.get("tareas", []) if run else [],
                "epica":    run.artefactos_generados.get("epica") if run else None,
            },
            "test_cases":          run.test_cases_generados if run else [],
            "informe_validacion":  run.informe_validacion if run else None,
            "informe_impacto":     run.informe_impacto if run else None,
            "error":               resultado.get("error")
        }
    finally:
        # Limpiar el archivo temporal
        if ruta_tmp.exists():
            ruta_tmp.unlink()
```

### 7.3 Endpoint: POST /pipeline/aprobar

```python
# backend/routes/aprobar.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from pipeline_ai.steps.s9_push import push_a_jira, push_a_xray
from pipeline_ai.config import PipelineConfig
from pipeline_ai.state import GestorEstado

router = APIRouter()
config = PipelineConfig()
gestor = GestorEstado(config.carpeta_runs)

class SolicitudAprobacion(BaseModel):
    page_id: str
    run_id: str
    aprobado_por: str          # accountId de Confluence del analista
    artefactos_editados: Optional[dict] = None  # Si el analista editó algo

@router.post("/pipeline/aprobar")
async def aprobar(solicitud: SolicitudAprobacion):
    """
    Ejecuta el push a Jira y Xray con los artefactos aprobados.
    Registra quién aprobó y cuándo para el gobierno del modelo.
    """
    # Recuperar el run
    run = gestor._buscar_run_reanudable(
        solicitud.run_id.split("_")[0],  # req_id del run_id
        ""
    )
    if not run:
        raise HTTPException(
            status_code=404,
            detail=f"Run {solicitud.run_id} no encontrado"
        )

    # Si el analista editó los artefactos, usar la versión editada
    if solicitud.artefactos_editados:
        run.artefactos_generados.update(solicitud.artefactos_editados)

    # Cambiar la config a modo real (no dry_run)
    config_real = PipelineConfig(dry_run=False)

    # Push a Jira
    resultado_jira = await push_a_jira(
        artefactos=run.artefactos_generados,
        requisito_id=run.requisito_id,
        config=config_real
    )

    # Push a Xray (si está configurado)
    resultado_xray = {}
    if config_real.xray.activo and run.test_cases_generados:
        resultado_xray = await push_a_xray(
            test_cases=run.test_cases_generados,
            historia_key=resultado_jira.get("historia_key"),
            requisito_id=run.requisito_id,
            config=config_real
        )

    # Registrar la aprobación para el gobierno del modelo
    _registrar_aprobacion(
        run_id=solicitud.run_id,
        aprobado_por=solicitud.aprobado_por,
        resultado_jira=resultado_jira
    )

    return {
        "exito":       resultado_jira.get("exito", False),
        "run_id":      solicitud.run_id,
        "resultado_jira":  resultado_jira,
        "resultado_xray":  resultado_xray,
        "jira_url": (
            f"{config.jira.base_url}/browse/"
            f"{resultado_jira.get('historia_key', '')}"
        )
    }

def _registrar_aprobacion(run_id, aprobado_por, resultado_jira):
    """
    Persiste la aprobación para el sistema de métricas de gobierno
    del punto 12 del modelo operativo.
    """
    import json
    from pathlib import Path
    from datetime import datetime

    log_path = Path("governance/aprobaciones.jsonl")
    log_path.parent.mkdir(exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp":    datetime.now().isoformat(),
            "run_id":       run_id,
            "aprobado_por": aprobado_por,
            "historia_key": resultado_jira.get("historia_key"),
            "edito":        False  # Se actualizaría si hubo edición
        }) + "\n")
```

### 7.4 Endpoint: POST /rag/sugerencias

```python
# backend/routes/rag.py
from fastapi import APIRouter
from pydantic import BaseModel
import yaml

from pipeline_ai.steps.s3_rag_context import recuperar_contexto_rag
from pipeline_ai.config import PipelineConfig

router = APIRouter()
config = PipelineConfig()

class SolicitudRAG(BaseModel):
    yaml_content: str

@router.post("/rag/sugerencias")
async def obtener_sugerencias(solicitud: SolicitudRAG):
    """
    Recupera requisitos relacionados del repositorio para el panel lateral.
    Se llama en segundo plano al abrir la página de un requisito.
    """
    try:
        requisito = yaml.safe_load(solicitud.yaml_content)
    except Exception:
        return {"sugerencias": []}

    glosario = _cargar_glosario(config)

    contexto = await recuperar_contexto_rag(
        requisito=requisito,
        glosario=glosario,
        config=config
    )

    # Formatear para el panel lateral
    sugerencias = []
    for chunk in contexto.get("funcionalidad_similar", [])[:6]:
        req_id = chunk.metadatos.get("requisito_id", "")
        similitud = chunk.similitud
        sugerencias.append({
            "requisito_id":   req_id,
            "titulo":         chunk.texto[:80],
            "similitud_pct":  int(similitud * 100),
            "relacion": (
                "⚠ Posible duplicado" if similitud > 0.90 else
                "→ Relacionado"       if similitud > 0.80 else
                "~ Referencia"
            ),
            "confluence_url": _buscar_url_confluence(req_id)
        })

    return {"sugerencias": sugerencias}

def _buscar_url_confluence(req_id: str) -> str:
    """
    Construye la URL de la página de Confluence para un requisito dado.
    En producción, buscar la página por el título o por una propiedad.
    """
    # Placeholder: en producción consultar la API de Confluence
    return f"/wiki/spaces/PROJ/pages/search?title={req_id}"
```

---

## 8. Configuración del manifest.yml (Forge)

El archivo de manifiesto declara todos los puntos de extensión del plugin ante la plataforma de Atlassian.

```yaml
# manifest.yml
app:
  id: ari:cloud:ecosystem::app/pipeline-ai-funcional
  name: Pipeline AI Funcional

permissions:
  scopes:
    - read:confluence-content.all
    - write:confluence-content
    - read:confluence-props
    - write:confluence-props
    - storage:app
  external:
    # URL del backend del pipeline (orchestrator.py expuesto como API)
    fetch:
      backend:
        - https://pipeline-ai.interna.empresa.com

modules:
  # ── Macro de página ─────────────────────────────────────────────
  confluence:contentBylineItem:
    - key: pipeline-ai-macro
      name:
        value: Pipeline AI
      title:
        value: Pipeline AI — Estado del requisito
      function: macro-pipeline-ai
      resolver:
        function: resolver-pipeline-ai

  # ── Panel lateral ───────────────────────────────────────────────
  confluence:contextMenu:
    - key: pipeline-ai-panel
      name:
        value: Asistente Pipeline AI
      function: panel-pipeline-ai

  # ── Slash command ────────────────────────────────────────────────
  confluence:spacePage:
    - key: slash-ai-requisito
      name:
        value: Insertar plantilla AI-Ready
      description:
        value: Inserta la plantilla YAML estructurada para requisitos AI-Ready
      function: slash-plantilla

functions:
  - key: macro-pipeline-ai
    handler: src/macro/index.run

  - key: resolver-pipeline-ai
    handler: src/macro/resolver.handler

  - key: panel-pipeline-ai
    handler: src/panel/index.run

  - key: slash-plantilla
    handler: src/slash-command/index.run
```

---

## 9. Flujo de trabajo completo con el plugin

Este es el flujo que vive el analista con el plugin instalado. Sin abrir ninguna herramienta adicional.

```
ANALISTA EN CONFLUENCE
│
├── Crea página nueva para el requisito
│
├── Escribe /ai-requisito  →  slash command inserta la plantilla YAML
│
├── Rellena la plantilla en la página (con el panel lateral mostrando
│   sugerencias RAG y campos pendientes en tiempo real)
│
├── Abre la macro {pipeline-ai} al final de la página
│
├── Pulsa [Validar calidad]
│   ├── BLOQUEADO: ve los problemas en la macro, corrige en la página
│   │             y vuelve a validar
│   └── APROBADO / ADVERTENCIAS: continúa
│
├── Pulsa [Generar artefactos]
│   └── El pipeline ejecuta pasos 1-7 en background (~30-90s)
│       (validación, RAG, generación de historia+tareas+test cases,
│        trazabilidad)
│
├── Revisa el output en la macro:
│   · Historia generada (resumen)
│   · Número de tareas por capa
│   · Número de test cases por tipo
│
├── Pulsa [Ver JSON completo]  →  panel expandible con el JSON completo
│   · Puede editar campos directamente en el JSON antes de aprobar
│
└── Pulsa [Aprobar → Push Jira]
    └── Pipeline empuja Historia + Tareas a Jira, Test Cases a Xray
        La macro muestra:  ✓  FACT-47 · FACT-48, 49, 50, 51
        El panel lateral actualiza el estado a "Completado"
```

**Tiempo total de interacción del analista:** 5-10 minutos de revisión y aprobación, frente a 30-90 minutos de creación manual.

---

## 10. Integración con el sistema de gobierno (punto 12)

El plugin no es solo una interfaz: contribuye datos al sistema de gobernanza del modelo operativo.

### 10.1 Métricas que el plugin registra automáticamente

Cada acción del analista genera un evento que alimenta las métricas del punto 12:

| Evento | Métrica que alimenta |
|---|---|
| `validar` invocado | Frecuencia de uso; tasa de detección temprana |
| `validar` devuelve BLOQUEADO | Score de calidad del repositorio por analista |
| `generar` completado | Tiempo de procesamiento del pipeline |
| JSON aprobado sin ediciones | Tasa de aprobación directa (objetivo >80%) |
| JSON aprobado con ediciones + campos modificados | Campos más editados (señal de ajuste de prompts) |
| JSON rechazado + motivo | Tasa de rechazo; categoría de problema |
| `aprobar` completado | Tiempo total desde validar hasta completado |

### 10.2 Webhook del plugin hacia el sistema de observabilidad

```javascript
// src/shared/metricas.js
import api from '@forge/api';

/**
 * Registra un evento de uso del plugin para el sistema de métricas.
 * El endpoint de métricas es el mismo backend del pipeline.
 */
export const registrarEvento = async (tipo, datos = {}) => {
  try {
    await api.asApp().requestBackend(
      '/governance/metricas',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          timestamp:   new Date().toISOString(),
          evento:      tipo,
          // eventos: validar_invocado | validar_bloqueado | validar_advertencia |
          //          generar_completado | aprobado_directo | aprobado_con_ediciones |
          //          rechazado | completado
          datos:       datos
        })
      }
    );
  } catch {
    // Las métricas no deben bloquear el flujo principal
  }
};

// Uso en la macro (ejemplo):
// await registrarEvento('aprobado_directo', {
//   requisito_id: 'REQ-023',
//   run_id: runData.run_id,
//   tiempo_total_segundos: 47,
//   campos_editados: []
// });
```

---

## 11. Casos de uso especiales

### 11.1 Requisito que ya tiene issue en Jira (regeneración)

Cuando el analista pulsa [Regenerar] sobre un requisito ya procesado, el plugin muestra un aviso explícito antes de continuar:

```
╔══════════════════════════════════════════════════════════════╗
║  ⚠ Este requisito ya tiene artefactos en Jira              ║
╠══════════════════════════════════════════════════════════════╣
║  Historia existente: FACT-47 (estado: En progreso)          ║
║  Asignada a: María García                                    ║
║                                                              ║
║  Regenerar actualizará los artefactos en Jira. Si la        ║
║  historia está en desarrollo activo, el equipo recibirá     ║
║  una notificación de cambio.                                 ║
║                                                              ║
║  [  Continuar y regenerar  ]   [  Cancelar  ]               ║
╚══════════════════════════════════════════════════════════════╝
```

Esta advertencia se conecta directamente con el análisis de impacto de cambios del punto 8 del modelo.

### 11.2 Cambio de estado del requisito desde el plugin

El plugin permite cambiar el campo `estado` del YAML directamente desde la macro sin editar el código YAML a mano. Un selector desplegable en la macro modifica el campo y guarda la página automáticamente. Esto activa el webhook de re-indexación del repositorio RAG descrito en el punto 7.

### 11.3 Vista de trazabilidad embebida

Desde la macro de una página con estado Completado, el botón [Ver trazabilidad] abre un panel expandible que muestra el grafo de trazabilidad del punto 9 directamente en Confluence, sin necesidad de abrir una herramienta separada:

```
REQ-023  ──genera──▶  US-047 (FACT-47)
                          │
                          ├──descompone──▶  FACT-48 (BD)
                          ├──descompone──▶  FACT-49 (backend)
                          ├──descompone──▶  FACT-50 (frontend)
                          └──descompone──▶  FACT-51 (testing)

AC-023-01 ──verifica──▶  TC-111, TC-114
AC-023-02 ──verifica──▶  TC-112
AC-023-03 ──verifica──▶  TC-113
```

---

## 12. Guía de instalación y configuración

### 12.1 Prerrequisitos

- Confluence Cloud (Forge) o Server/Data Center (Connect)
- Acceso de administrador al espacio de Confluence del proyecto
- Backend del pipeline desplegado y accesible (orchestrator.py como API)
- Variables de entorno configuradas (ANTHROPIC_API_KEY, JIRA_API_TOKEN, etc.)

### 12.2 Instalación del plugin (Forge)

```bash
# 1. Instalar la CLI de Forge
npm install -g @forge/cli

# 2. Autenticar con la cuenta de Atlassian
forge login

# 3. Clonar el repositorio del plugin
git clone https://repo.empresa.com/pipeline-ai/confluence-plugin.git
cd confluence-plugin

# 4. Instalar dependencias
npm install

# 5. Configurar las variables del plugin
forge variables set --encrypt BACKEND_URL https://pipeline-ai.interna.empresa.com
forge variables set --encrypt BACKEND_API_KEY <clave-interna>

# 6. Desplegar en el entorno de desarrollo para pruebas
forge deploy --environment development

# 7. Instalar en el site de Confluence de desarrollo
forge install --site tu-empresa.atlassian.net

# 8. Tras validar en desarrollo, desplegar en producción
forge deploy --environment production
forge install --site tu-empresa.atlassian.net --upgrade
```

### 12.3 Configuración del espacio de Confluence

Tras instalar el plugin, un administrador del espacio debe:

1. Ir a **Configuración del espacio → Plantillas de página** y crear una plantilla llamada "Requisito AI-Ready" que incluya la macro `{pipeline-ai}` y un bloque YAML con la plantilla base.

2. Configurar la **plantilla como predeterminada** para las páginas del espacio o de la sección de requisitos.

3. Verificar que el plugin puede acceder al backend ejecutando una validación de prueba desde cualquier página del espacio.

### 12.4 Variables de configuración del plugin

| Variable | Descripción | Ejemplo |
|---|---|---|
| `BACKEND_URL` | URL base del backend del pipeline | `https://pipeline-ai.interna.empresa.com` |
| `BACKEND_API_KEY` | Clave de API para autenticar el plugin | `sk-interno-...` |
| `JIRA_PROJECT_KEY` | Proyecto Jira destino | `FACT` |
| `RAG_UMBRAL_DUPLICADO` | Similitud mínima para alertar duplicado | `0.90` |
| `XRAY_ACTIVO` | Activar push de test cases a Xray | `true` |

---

## 13. Limitaciones conocidas y mitigaciones

| Limitación | Mitigación |
|---|---|
| Forge tiene un límite de ejecución de 25 segundos por función | Las operaciones largas (generación, push) se hacen asíncronas: el plugin inicia el job y consulta el estado periódicamente |
| El extractor YAML solo funciona con bloques de código formateados con la macro de Confluence | El slash command garantiza que la plantilla siempre se inserta en el formato correcto |
| La edición del JSON antes de aprobar es básica (campo de texto) | Para ediciones complejas, el analista descarga el JSON, lo edita en su editor preferido y lo sube de vuelta |
| La vista de trazabilidad embebida es solo de lectura | Para la vista completa interactiva se enlaza a la interfaz web del sistema de trazabilidad |
| Forge no soporta WebSockets nativos | El polling cada 3 segundos simula la actualización en tiempo real; latencia máxima de 3s |

---

## 14. Relación con el resto del modelo operativo

El plugin es la interfaz de usuario de todo el modelo operativo. No reemplaza ningún componente: los invoca a través del orquestador del punto 12.

| Componente del modelo | Cómo lo usa el plugin |
|---|---|
| **Plantilla YAML (punto 1)** | El slash command la inserta en la página |
| **Glosario (punto 2)** | Lo inyecta automáticamente en cada llamada al pipeline |
| **Event Storming (punto 3)** | El analista usa los resultados del workshop para rellenar la plantilla |
| **Prompts de generación (punto 4)** | Invocados por el endpoint `/pipeline/generar` |
| **Test cases (punto 5)** | Invocados en el mismo endpoint; resultado visible en la macro |
| **Validación (punto 6)** | Invocada por el endpoint `/pipeline/validar` y en segundo plano |
| **RAG (punto 7)** | Invocado por el endpoint `/rag/sugerencias` para el panel lateral |
| **Impacto de cambios (punto 8)** | Invocado automáticamente al detectar que el requisito ya tiene artefactos |
| **Trazabilidad (punto 9)** | Actualizada al aprobar; visible en el botón "Ver trazabilidad" |
| **Jira API (punto 10)** | Invocada por el endpoint `/pipeline/aprobar` |
| **Gobierno (punto 12)** | El plugin registra automáticamente todos los eventos de uso |

---

*Documento generado como complemento al Modelo Operativo AI-Ready. Versión 1.0.*
