# Interfaz de Analista para el Pipeline AI-Ready

**Componente 13 del Modelo Operativo — Análisis Funcional AI-Ready**

---

## Por qué hace falta este componente

Los puntos 4 al 10 del modelo operativo construyen un pipeline técnicamente completo: validación automática de requisitos, generación de artefactos Jira, test cases, RAG, detección de impacto, trazabilidad y push a Jira. Todo ello orquestado por un script Python que acepta parámetros por línea de comandos.

El problema es que ese script no lo puede usar un analista funcional sin conocimientos técnicos. Copiar un YAML a una carpeta, abrir un terminal, escribir `python orchestrator.py --req REQ-023` y saber interpretar el output no forma parte del perfil ni de las expectativas de los profesionales que van a usar el sistema a diario.

La interfaz de analista es la capa que hace todo lo anterior accesible para alguien cuya herramienta habitual es Confluence, Jira o Word. No añade lógica al pipeline: añade accesibilidad. Y en términos de adopción real, la accesibilidad es tan importante como la funcionalidad.

La regla del modelo es que **el analista es el protagonista, no el receptor**. La interfaz debe reforzar ese principio: el analista ve lo que genera la IA, decide si es correcto y aprueba o rechaza. El sistema nunca empuja a Jira sin esa decisión humana.

---

## Dónde vive la interfaz: dos opciones complementarias

El modelo plantea dos opciones que no son excluyentes: una integración en Confluence para los analistas que ya trabajan ahí, y una aplicación web ligera independiente para los equipos que prefieren mantener Confluence como repositorio de lectura solamente.

La recomendación es empezar con la aplicación web y, en paralelo, añadir la integración en Confluence una vez que el proceso está estabilizado. La razón es pragmática: la aplicación web es más rápida de desplegar, más fácil de iterar y no requiere permisos de administración en Confluence durante el piloto.

---

## Opción A — Aplicación web del pipeline

### Arquitectura general

La aplicación es una SPA (Single Page Application) construida con React que se conecta directamente al backend del orquestador mediante una API REST. No tiene servidor propio de base de datos: consume la misma API que usa el script de línea de comandos.

```
Navegador (React SPA)
       │
       │  HTTP/WebSocket
       ▼
API Gateway del Pipeline
       │
       ├──→ orchestrator.py (los pasos 1-10)
       ├──→ Base de datos de estado (state.py)
       ├──→ Grafo de trazabilidad (PostgreSQL + pgvector)
       └──→ Jira API / Xray API
```

El WebSocket es crítico para la experiencia de usuario: permite que la pantalla de ejecución muestre el progreso en tiempo real paso a paso, sin que el analista tenga que pulsar actualizar ni esperar a que termine todo para ver qué ocurrió.

### Backend: la API del pipeline

El backend expone los endpoints que necesita la SPA. Se construye sobre FastAPI (ya usado en el webhook del punto 9) para mantener consistencia en el stack.

```python
# api/main.py
from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import asyncio
import json

app = FastAPI(title="Pipeline AI — API de analista")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pipeline-ai.interno"],
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# ── Autenticación ─────────────────────────────────────────

def verificar_token(credentials = Depends(security)):
    """
    Verifica el token del analista contra el directorio de la organización.
    En producción: validar contra Azure AD, Okta o el IdP corporativo.
    """
    token = credentials.credentials
    usuario = _verificar_token_corporativo(token)
    if not usuario:
        raise HTTPException(401, "Token inválido o expirado")
    return usuario


# ── Endpoints de requisitos ───────────────────────────────

@app.get("/api/requisitos")
async def listar_requisitos(
    epica: str = None,
    estado: str = None,
    usuario = Depends(verificar_token)
):
    """
    Lista los requisitos del repositorio con filtros opcionales.
    Respuesta paginada para épicas con muchos requisitos.
    """
    requisitos = await _cargar_requisitos_del_repositorio(
        epica=epica, estado=estado
    )
    return {
        "requisitos": requisitos,
        "total": len(requisitos)
    }


@app.get("/api/requisitos/{req_id}")
async def obtener_requisito(
    req_id: str,
    usuario = Depends(verificar_token)
):
    """Retorna el YAML de un requisito como objeto JSON."""
    req = await _cargar_requisito(req_id)
    if not req:
        raise HTTPException(404, f"Requisito {req_id} no encontrado")
    return req


@app.put("/api/requisitos/{req_id}")
async def actualizar_requisito(
    req_id: str,
    payload: dict,
    usuario = Depends(verificar_token)
):
    """
    Guarda los cambios del analista en el YAML del requisito.
    Dispara re-indexación RAG en background si el estado es validado.
    """
    await _guardar_requisito(req_id, payload, usuario["email"])
    if payload.get("estado") in ("en-revision", "validado"):
        asyncio.create_task(
            _reindexar_requisito_background(req_id, payload)
        )
    return {"ok": True, "req_id": req_id}


# ── Endpoints del pipeline ────────────────────────────────

@app.post("/api/pipeline/ejecutar")
async def ejecutar_pipeline(
    payload: dict,
    usuario = Depends(verificar_token)
):
    """
    Lanza la ejecución del pipeline para un requisito o épica.
    Retorna inmediatamente con el run_id; el progreso
    se sigue por WebSocket.
    """
    req_id = payload.get("req_id")
    epica_id = payload.get("epica_id")
    dry_run = payload.get("dry_run", True)   # DRY-RUN por defecto

    if not req_id and not epica_id:
        raise HTTPException(400, "Debes indicar req_id o epica_id")

    run_id = await _lanzar_pipeline_background(
        req_id=req_id,
        epica_id=epica_id,
        dry_run=dry_run,
        analista=usuario["email"]
    )

    return {"run_id": run_id, "estado": "iniciado"}


@app.get("/api/pipeline/runs/{run_id}")
async def estado_run(
    run_id: str,
    usuario = Depends(verificar_token)
):
    """Retorna el estado completo de un run (para polling o recarga)."""
    run = await _cargar_estado_run(run_id)
    if not run:
        raise HTTPException(404, "Run no encontrado")
    return run


@app.websocket("/ws/pipeline/{run_id}")
async def websocket_pipeline(websocket: WebSocket, run_id: str):
    """
    WebSocket para seguimiento en tiempo real del pipeline.
    Emite un evento por cada paso que se completa o falla.
    """
    await websocket.accept()
    try:
        async for evento in _suscribir_eventos_run(run_id):
            await websocket.send_json(evento)
            if evento.get("estado_final"):
                break
    except Exception:
        pass
    finally:
        await websocket.close()


# ── Endpoints de aprobación ───────────────────────────────

@app.get("/api/aprobaciones/pendientes")
async def aprobaciones_pendientes(usuario = Depends(verificar_token)):
    """
    Lista todos los artefactos pendientes de aprobación
    asignados al analista autenticado.
    """
    pendientes = await _cargar_aprobaciones_pendientes(
        analista=usuario["email"]
    )
    return {"aprobaciones": pendientes, "total": len(pendientes)}


@app.post("/api/aprobaciones/{aprobacion_id}/decidir")
async def decidir_aprobacion(
    aprobacion_id: str,
    payload: dict,
    usuario = Depends(verificar_token)
):
    """
    Aprueba, edita o rechaza los artefactos generados.
    Si aprueba: dispara el push real a Jira/Xray.
    """
    decision = payload.get("decision")   # aprobar | editar | rechazar
    motivo = payload.get("motivo", "")
    artefactos_editados = payload.get("artefactos_editados")

    if decision not in ("aprobar", "editar", "rechazar"):
        raise HTTPException(400, "decision debe ser: aprobar, editar o rechazar")

    resultado = await _procesar_decision(
        aprobacion_id=aprobacion_id,
        decision=decision,
        analista=usuario["email"],
        motivo=motivo,
        artefactos_editados=artefactos_editados
    )

    return resultado


# ── Endpoints de consulta ─────────────────────────────────

@app.get("/api/trazabilidad/{req_id}")
async def trazabilidad_requisito(
    req_id: str,
    usuario = Depends(verificar_token)
):
    """Retorna la traza completa descendente de un requisito."""
    from steps.s7_traceability import ConsultorTrazabilidad
    consultor = ConsultorTrazabilidad(config.db.to_dict())
    return consultor.traza_completa_requisito(req_id)


@app.get("/api/dashboard/metricas")
async def metricas_dashboard(usuario = Depends(verificar_token)):
    """Métricas del pipeline para el dashboard del analista."""
    return await _calcular_metricas_dashboard()
```

### Frontend: la SPA del analista

La SPA tiene cinco pantallas principales que cubren el flujo completo del analista:

| Pantalla | Propósito |
|---|---|
| **Dashboard** | Vista general: requisitos por estado, aprobaciones pendientes, métricas del pipeline |
| **Requisitos** | Listado navegable con filtros; acceso al editor de YAML |
| **Editor de requisito** | Formulario estructurado para editar la plantilla AI-ready |
| **Ejecución** | Seguimiento en tiempo real del pipeline paso a paso |
| **Aprobación** | Revisión de artefactos generados; decisión antes del push a Jira |

A continuación se desarrolla cada una con el detalle necesario para su implementación.

---

#### Pantalla 1 — Dashboard

El dashboard responde a la pregunta que se hace el analista cada mañana: "¿Qué tengo pendiente hoy?"

Tiene tres zonas visuales diferenciadas:

**Bandeja de aprobaciones pendientes.** Una lista ordenada por antigüedad que muestra los artefactos generados que esperan decisión del analista. Cada ítem muestra el ID del requisito, el tiempo que lleva esperando y un acceso directo a la pantalla de aprobación. Si el analista tiene más de cinco pendientes, se muestra una alerta visual porque los artefactos que esperan más de 48 horas suelen perder contexto y necesitan más tiempo de revisión.

**Estado del repositorio.** Un conjunto de indicadores tipo semáforo que muestran el número de requisitos por estado (borrador, en revisión, validado, bloqueado) y el score medio de calidad del repositorio según la última auditoría. Cuando el score cae por debajo de 70, el indicador cambia a amarillo y muestra un enlace al informe de auditoría.

**Actividad reciente.** Un log de las últimas ejecuciones del pipeline con su resultado (completado, fallido, dry-run) y los issues de Jira generados. Permite recuperar rápidamente el enlace a una historia creada hace una hora sin tener que navegar por Jira.

```jsx
// components/Dashboard.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

export function Dashboard() {
  const [aprobaciones, setAprobaciones] = useState([]);
  const [metricas, setMetricas] = useState(null);
  const [actividad, setActividad] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      api.get("/aprobaciones/pendientes"),
      api.get("/dashboard/metricas"),
      api.get("/pipeline/runs/recientes")
    ]).then(([apr, met, act]) => {
      setAprobaciones(apr.aprobaciones);
      setMetricas(met);
      setActividad(act.runs);
    });
  }, []);

  return (
    <div className="dashboard">
      {/* Bandeja de aprobaciones */}
      <section className="panel panel--aprobaciones">
        <h2>
          Pendientes de aprobación
          {aprobaciones.length > 0 && (
            <span className="badge badge--alerta">{aprobaciones.length}</span>
          )}
        </h2>
        {aprobaciones.length === 0 ? (
          <p className="estado-vacio">No hay artefactos pendientes de revisión.</p>
        ) : (
          <ul className="lista-aprobaciones">
            {aprobaciones.map(apr => (
              <li key={apr.id} className="item-aprobacion">
                <span className="req-id">{apr.requisito_id}</span>
                <span className="titulo">{apr.titulo}</span>
                <span className={`tiempo ${apr.horas_espera > 24 ? "tiempo--alerta" : ""}`}>
                  {apr.horas_espera}h esperando
                </span>
                <button
                  className="btn btn--primario"
                  onClick={() => navigate(`/aprobacion/${apr.id}`)}
                >
                  Revisar
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Indicadores de repositorio */}
      {metricas && (
        <section className="panel panel--metricas">
          <h2>Estado del repositorio</h2>
          <div className="grid-indicadores">
            <Indicador
              etiqueta="Validados"
              valor={metricas.validados}
              color="verde"
            />
            <Indicador
              etiqueta="En revisión"
              valor={metricas.en_revision}
              color="amarillo"
            />
            <Indicador
              etiqueta="Borradores"
              valor={metricas.borrador}
              color="neutro"
            />
            <Indicador
              etiqueta="Bloqueados"
              valor={metricas.bloqueados}
              color={metricas.bloqueados > 0 ? "rojo" : "verde"}
            />
            <Indicador
              etiqueta="Score medio"
              valor={`${metricas.score_medio}/100`}
              color={metricas.score_medio >= 75 ? "verde" : metricas.score_medio >= 60 ? "amarillo" : "rojo"}
              tooltip="Puntuación media de calidad del validador automático sobre los últimos 30 requisitos"
            />
          </div>
        </section>
      )}

      {/* Actividad reciente */}
      <section className="panel panel--actividad">
        <h2>Actividad reciente</h2>
        <table className="tabla-actividad">
          <thead>
            <tr>
              <th>Requisito</th>
              <th>Resultado</th>
              <th>Historia Jira</th>
              <th>Hace</th>
            </tr>
          </thead>
          <tbody>
            {actividad.map(run => (
              <tr key={run.run_id}>
                <td>{run.requisito_id}</td>
                <td>
                  <span className={`estado estado--${run.estado}`}>
                    {run.estado}
                  </span>
                </td>
                <td>
                  {run.historia_key ? (
                    <a
                      href={`${run.jira_base_url}/browse/${run.historia_key}`}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {run.historia_key}
                    </a>
                  ) : "—"}
                </td>
                <td>{run.hace}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
```

---

#### Pantalla 2 — Listado de requisitos

El listado es el punto de entrada para trabajar con requisitos existentes o navegar a uno concreto. Tiene tres controles de filtrado que corresponden exactamente a los campos de la plantilla YAML: épica, estado y analista responsable.

El elemento más importante de esta pantalla no es el listado sino el indicador visual de calidad que aparece junto a cada requisito: un score numérico con fondo verde, amarillo o rojo según el resultado de la última validación automática. Este indicador hace visible de un vistazo cuáles requisitos necesitan atención antes de entrar al pipeline.

```jsx
// components/ListadoRequisitos.jsx
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../services/api";

export function ListadoRequisitos() {
  const [requisitos, setRequisitos] = useState([]);
  const [filtros, setFiltros] = useState({ epica: "", estado: "", texto: "" });
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/requisitos", { params: filtros }).then(r => setRequisitos(r.requisitos));
  }, [filtros]);

  const COLOR_ESTADO = {
    validado: "verde",
    "en-revision": "amarillo",
    borrador: "neutro",
    rechazado: "rojo",
    deprecado: "gris"
  };

  return (
    <div className="listado-requisitos">
      <header className="listado-header">
        <h1>Requisitos</h1>
        <Link to="/requisitos/nuevo" className="btn btn--primario">
          + Nuevo requisito
        </Link>
      </header>

      {/* Filtros */}
      <div className="filtros">
        <input
          type="text"
          placeholder="Buscar por ID o título..."
          value={filtros.texto}
          onChange={e => setFiltros(f => ({ ...f, texto: e.target.value }))}
          className="input-busqueda"
        />
        <select
          value={filtros.epica}
          onChange={e => setFiltros(f => ({ ...f, epica: e.target.value }))}
        >
          <option value="">Todas las épicas</option>
          {/* Opciones cargadas desde el repositorio */}
        </select>
        <select
          value={filtros.estado}
          onChange={e => setFiltros(f => ({ ...f, estado: e.target.value }))}
        >
          <option value="">Todos los estados</option>
          <option value="borrador">Borrador</option>
          <option value="en-revision">En revisión</option>
          <option value="validado">Validado</option>
          <option value="rechazado">Rechazado</option>
        </select>
      </div>

      {/* Tabla de requisitos */}
      <table className="tabla-requisitos">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Épica</th>
            <th>Estado</th>
            <th>Calidad</th>
            <th>Última ejecución</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {requisitos.map(req => (
            <tr key={req.id}>
              <td>
                <Link to={`/requisitos/${req.id}`} className="link-req-id">
                  {req.id}
                </Link>
              </td>
              <td>{req.titulo}</td>
              <td>{req.epica}</td>
              <td>
                <span className={`badge badge--${COLOR_ESTADO[req.estado] || "neutro"}`}>
                  {req.estado}
                </span>
              </td>
              <td>
                {req.score_calidad != null ? (
                  <span className={`score score--${req.score_calidad >= 75 ? "verde" : req.score_calidad >= 60 ? "amarillo" : "rojo"}`}>
                    {req.score_calidad}
                  </span>
                ) : (
                  <span className="score score--sin-validar">—</span>
                )}
              </td>
              <td>
                {req.ultima_ejecucion ? (
                  <span className={`estado estado--${req.ultima_ejecucion.estado}`}>
                    {req.ultima_ejecucion.estado}
                  </span>
                ) : "Nunca"}
              </td>
              <td className="acciones">
                <button
                  className="btn btn--secundario btn--pequeño"
                  onClick={() => navigate(`/requisitos/${req.id}`)}
                >
                  Editar
                </button>
                <button
                  className="btn btn--primario btn--pequeño"
                  onClick={() => navigate(`/pipeline/ejecutar?req=${req.id}`)}
                  disabled={req.estado === "borrador"}
                  title={req.estado === "borrador" ? "Cambia el estado a 'en-revision' para ejecutar el pipeline" : ""}
                >
                  Ejecutar pipeline
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

#### Pantalla 3 — Editor de requisito

El editor es la pantalla más importante de toda la interfaz porque es donde el analista interactúa con la plantilla estructurada del punto 1. El diseño resuelve el problema central que tiene cualquier editor de YAML para usuarios no técnicos: **el analista no debe ver ni escribir YAML directamente**.

La solución es un formulario por bloques que mapea exactamente los cinco bloques de la plantilla del modelo operativo:

- **Bloque 1 — Identidad:** ID, título, versión, estado, épica, origen
- **Bloque 2 — Contexto de negocio:** actor, evento disparador, objetivo, descripción, prioridad, reglas de negocio
- **Bloque 3 — Comportamiento esperado:** flujo principal, excepciones, criterios de aceptación, definition of done
- **Bloque 4 — Datos:** entradas y salidas
- **Bloque 5 — Metadatos técnicos:** restricciones no funcionales, notas para el equipo técnico

El formulario tiene tres características que son claves para la usabilidad:

**Validación en línea.** Cuando el analista sale de un campo (evento `onBlur`), el formulario llama al validador estructural del punto 6 para ese campo específico y muestra el resultado inline sin necesidad de guardar. Si el campo tiene un problema bloqueante, aparece un mensaje en rojo debajo del input. Si tiene una advertencia, aparece en amarillo. El analista corrige en el momento, no días después.

**Sugerencias contextuales del glosario.** Los campos de actor y entidades de negocio tienen autocompletado contra el glosario del proyecto. Si el analista escribe "usuario" y el glosario tiene "Gestor de facturación" como término oficial, aparece la sugerencia con el texto "Término oficial: Gestor de facturación". Si el analista usa un sinónimo no oficial, el campo muestra una advertencia.

**Vista paralela YAML/formulario.** Un toggle en la esquina superior derecha permite al analista avanzado cambiar entre la vista de formulario y la vista YAML raw. Los analistas que dominan el formato pueden trabajar directamente en YAML; los que prefieren el formulario nunca necesitan ver el YAML. Ambas vistas están sincronizadas: un cambio en una se refleja en la otra en tiempo real.

```jsx
// components/EditorRequisito.jsx
import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { BloqueCriteriosAceptacion } from "./BloqueCriteriosAceptacion";
import { BloqueRegласNegocio } from "./BloqueRegласNegocio";
import { BloqueFlujoPrincipal } from "./BloqueFlujoPrincipal";
import { BloqueExcepciones } from "./BloqueExcepciones";
import { ValidadorCampo } from "./ValidadorCampo";
import { SelectorActor } from "./SelectorActor";
import { BotonesPipeline } from "./BotonesPipeline";

export function EditorRequisito() {
  const { id } = useParams();
  const navigate = useNavigate();
  const esNuevo = id === "nuevo";

  const [req, setReq] = useState(null);
  const [modoYaml, setModoYaml] = useState(false);
  const [guardando, setGuardando] = useState(false);
  const [erroresValidacion, setErroresValidacion] = useState({});
  const [requisitosSimilares, setRequisitosSimilares] = useState([]);

  // Carga inicial
  useEffect(() => {
    if (esNuevo) {
      setReq(PLANTILLA_REQUISITO_VACIA);
    } else {
      api.get(`/requisitos/${id}`).then(setReq);
    }
  }, [id]);

  // Sugerencias RAG en tiempo real (debounced)
  const buscarSimilares = useCallback(
    debounce(async (texto) => {
      if (texto.length < 30) return;
      const r = await api.post("/rag/sugerencias", { texto });
      setRequisitosSimilares(r.similares);
    }, 800),
    []
  );

  // Validar un campo específico al salir
  const validarCampo = async (campo, valor) => {
    const r = await api.post("/validacion/campo", { campo, valor, contexto: req });
    setErroresValidacion(prev => ({
      ...prev,
      [campo]: r.problemas
    }));
  };

  const actualizar = (campo, valor) => {
    setReq(prev => ({ ...prev, [campo]: valor }));
    if (campo === "descripcion") buscarSimilares(valor);
  };

  const guardar = async () => {
    setGuardando(true);
    await api.put(`/requisitos/${req.id}`, req);
    setGuardando(false);
  };

  if (!req) return <Cargando />;

  return (
    <div className="editor-requisito">
      {/* Cabecera */}
      <header className="editor-header">
        <div className="editor-header__izquierda">
          <h1>{esNuevo ? "Nuevo requisito" : req.id}</h1>
          <span className={`badge badge--${COLOR_ESTADO[req.estado]}`}>
            {req.estado}
          </span>
        </div>
        <div className="editor-header__derecha">
          <button
            className="btn btn--fantasma"
            onClick={() => setModoYaml(!modoYaml)}
          >
            {modoYaml ? "Vista formulario" : "Vista YAML"}
          </button>
          <button
            className="btn btn--secundario"
            onClick={guardar}
            disabled={guardando}
          >
            {guardando ? "Guardando..." : "Guardar"}
          </button>
          <BotonesPipeline
            req={req}
            onEjecutar={() => navigate(`/pipeline/ejecutar?req=${req.id}`)}
          />
        </div>
      </header>

      {/* Aviso de requisitos similares (RAG) */}
      {requisitosSimilares.length > 0 && (
        <div className="aviso-similares">
          <span className="aviso-similares__icono">⚠</span>
          <span>
            Requisitos similares detectados:{" "}
            {requisitosSimilares.map(s => (
              <a key={s.id} href={`/requisitos/${s.id}`} target="_blank" rel="noreferrer">
                {s.id} ({s.similitud_pct}%)
              </a>
            ))}
            . Verifica que no es un duplicado antes de continuar.
          </span>
        </div>
      )}

      {modoYaml ? (
        <EditorYaml
          valor={req}
          onChange={nuevoReq => setReq(nuevoReq)}
        />
      ) : (
        <div className="formulario-bloques">

          {/* ── BLOQUE 1: IDENTIDAD ─────────────────────── */}
          <section className="bloque bloque--identidad">
            <h2 className="bloque__titulo">
              <span className="bloque__numero">1</span>
              Identidad
            </h2>
            <p className="bloque__descripcion">
              Identificación unívoca y enrutamiento del requisito. Estos campos
              los usa la IA para construir la trazabilidad automática.
            </p>
            <div className="grid-campos">
              <CampoTexto
                id="id"
                etiqueta="ID del requisito"
                valor={req.id}
                placeholder="REQ-023"
                requerido
                patron="^REQ-\d{3}$"
                mensajePatron="Formato: REQ-NNN (tres dígitos)"
                onChange={v => actualizar("id", v)}
                onBlur={v => validarCampo("id", v)}
                errores={erroresValidacion.id}
                deshabilitado={!esNuevo}
              />
              <CampoTexto
                id="titulo"
                etiqueta="Título"
                valor={req.titulo}
                placeholder="Filtrar facturas por rango de fechas"
                requerido
                maxLength={80}
                ayuda="Máximo 80 caracteres. Empieza por verbo en infinitivo o sustantivo. Evita: gestionar, administrar, controlar."
                onChange={v => actualizar("titulo", v)}
                onBlur={v => validarCampo("titulo", v)}
                errores={erroresValidacion.titulo}
              />
              <CampoSelect
                id="estado"
                etiqueta="Estado"
                valor={req.estado}
                opciones={ESTADOS_REQUISITO}
                requerido
                ayuda="Solo los requisitos en 'en-revision' o 'validado' pueden entrar al pipeline."
                onChange={v => actualizar("estado", v)}
              />
              <CampoSelect
                id="prioridad"
                etiqueta="Prioridad (MoSCoW)"
                valor={req.prioridad}
                opciones={OPCIONES_PRIORIDAD}
                requerido
                onChange={v => actualizar("prioridad", v)}
              />
              <SelectorEpica
                valor={req.epica}
                onChange={v => actualizar("epica", v)}
              />
              <CampoTexto
                id="analista"
                etiqueta="Analista responsable"
                valor={req.analista}
                onChange={v => actualizar("analista", v)}
              />
            </div>
          </section>

          {/* ── BLOQUE 2: CONTEXTO DE NEGOCIO ───────────── */}
          <section className="bloque bloque--contexto">
            <h2 className="bloque__titulo">
              <span className="bloque__numero">2</span>
              Contexto de negocio
            </h2>
            <p className="bloque__descripcion">
              El "por qué" del requisito. La IA usa estos campos para generar
              el valor de negocio de la historia y la justificación de la épica.
            </p>
            <div className="grid-campos">
              <SelectorActor
                valor={req.actor}
                glosario={glosario}
                onChange={v => actualizar("actor", v)}
                onBlur={v => validarCampo("actor", v)}
                errores={erroresValidacion.actor}
              />
              <CampoTexto
                id="evento_disparador"
                etiqueta="Evento disparador"
                valor={req.evento_disparador}
                placeholder="El gestor accede al módulo Facturas para el cierre mensual"
                requerido
                ayuda="Qué situación concreta activa este requisito. Evita: 'cuando el usuario lo necesita'."
                onChange={v => actualizar("evento_disparador", v)}
                onBlur={v => validarCampo("evento_disparador", v)}
                errores={erroresValidacion.evento_disparador}
              />
              <CampoTextarea
                id="objetivo_negocio"
                etiqueta="Objetivo de negocio"
                valor={req.objetivo_negocio}
                placeholder="Por qué existe este requisito. Qué problema de negocio resuelve. Mínimo 20 palabras."
                filas={3}
                onChange={v => actualizar("objetivo_negocio", v)}
              />
              <CampoTextarea
                id="descripcion"
                etiqueta="Descripción"
                valor={req.descripcion}
                placeholder="Narrativa del requisito en lenguaje de negocio. Sin tecnicismos. Mínimo 30 palabras."
                requerido
                filas={4}
                contadorPalabras
                minimosPalabras={30}
                onChange={v => actualizar("descripcion", v)}
                onBlur={v => validarCampo("descripcion", v)}
                errores={erroresValidacion.descripcion}
              />
            </div>
            <BloqueRegласNegocio
              reglas={req.reglas_negocio || []}
              onChange={v => actualizar("reglas_negocio", v)}
            />
          </section>

          {/* ── BLOQUE 3: COMPORTAMIENTO ESPERADO ───────── */}
          <section className="bloque bloque--comportamiento">
            <h2 className="bloque__titulo">
              <span className="bloque__numero">3</span>
              Comportamiento esperado
            </h2>
            <p className="bloque__descripcion">
              Qué debe hacer el sistema de forma verificable. Es la fuente
              principal de los test cases automáticos.
            </p>
            <BloqueFlujoPrincipal
              pasos={req.flujo_principal || []}
              onChange={v => actualizar("flujo_principal", v)}
            />
            <BloqueExcepciones
              excepciones={req.excepciones || []}
              onChange={v => actualizar("excepciones", v)}
              errores={erroresValidacion.excepciones}
            />
            <BloqueCriteriosAceptacion
              criterios={req.criterios_aceptacion || []}
              idRequisito={req.id}
              onChange={v => actualizar("criterios_aceptacion", v)}
              onBlur={() => validarCampo("criterios_aceptacion", req.criterios_aceptacion)}
              errores={erroresValidacion.criterios_aceptacion}
            />
          </section>

          {/* ── BLOQUE 4: DATOS ──────────────────────────── */}
          <section className="bloque bloque--datos">
            <h2 className="bloque__titulo">
              <span className="bloque__numero">4</span>
              Datos
            </h2>
            <p className="bloque__descripcion">
              Especificación de entradas y salidas. La IA los usa para
              generar casos de contorno y validaciones en las tareas técnicas.
            </p>
            <BloqueDatosEntrada
              campos={req.datos_entrada || []}
              onChange={v => actualizar("datos_entrada", v)}
            />
            <BloqueDatosSalida
              salida={req.datos_salida || {}}
              onChange={v => actualizar("datos_salida", v)}
            />
          </section>

          {/* ── BLOQUE 5: METADATOS TÉCNICOS ────────────── */}
          <section className="bloque bloque--tecnico">
            <h2 className="bloque__titulo">
              <span className="bloque__numero">5</span>
              Metadatos técnicos
              <span className="etiqueta-opcional">Opcional — completa el equipo técnico en el refinamiento</span>
            </h2>
            <BloqueRestriccionesNoFuncionales
              restricciones={req.restricciones_no_funcionales || {}}
              onChange={v => actualizar("restricciones_no_funcionales", v)}
            />
          </section>

        </div>
      )}
    </div>
  );
}
```

##### Subcomponente: BloqueCriteriosAceptacion

El editor de criterios de aceptación merece atención especial porque es el campo más crítico para la calidad del pipeline y el más propenso a errores. El diseño usa una tarjeta por criterio con tres campos claramente etiquetados (Dado / Cuando / Entonces) y dos ayudas visuales:

Una guía de formato que aparece al activar cualquiera de los tres campos, recordando las reglas de oro: el "Dado" describe un estado, el "Cuando" describe una única acción, el "Entonces" describe algo observable.

Un indicador de verificabilidad que aparece al salir del campo "Entonces": un semáforo que evalúa en tiempo real si el criterio es verificable con un test concreto, usando el mismo clasificador semántico del validador.

```jsx
// components/BloqueCriteriosAceptacion.jsx
export function BloqueCriteriosAceptacion({ criterios, idRequisito, onChange, errores }) {
  const [verificabilidad, setVerificabilidad] = useState({});

  const evaluarVerificabilidad = async (acId, entonces) => {
    const r = await api.post("/validacion/verificabilidad", { entonces });
    setVerificabilidad(prev => ({ ...prev, [acId]: r.es_verificable }));
  };

  const añadir = () => {
    const nuevoAc = {
      id: `AC-${idRequisito.replace("REQ-", "")}-${String(criterios.length + 1).padStart(2, "0")}`,
      titulo: "",
      dado: "",
      cuando: "",
      entonces: "",
      tipo: "positivo",
      datos_ejemplo: {}
    };
    onChange([...criterios, nuevoAc]);
  };

  const actualizar = (idx, campo, valor) => {
    const nuevos = [...criterios];
    nuevos[idx] = { ...nuevos[idx], [campo]: valor };
    onChange(nuevos);
  };

  const eliminar = (idx) => {
    onChange(criterios.filter((_, i) => i !== idx));
  };

  return (
    <div className="bloque-criterios">
      <div className="bloque-criterios__cabecera">
        <h3>Criterios de aceptación</h3>
        <span className="ayuda-inline">
          Mínimo 1. Cada criterio = un test automático.
        </span>
      </div>

      {criterios.length === 0 && (
        <div className="estado-vacio-criterios">
          No hay criterios todavía. Añade al menos uno para que el
          pipeline pueda generar test cases.
        </div>
      )}

      {criterios.map((ac, idx) => (
        <div key={ac.id} className={`tarjeta-ac ${errores?.[idx] ? "tarjeta-ac--error" : ""}`}>
          <div className="tarjeta-ac__cabecera">
            <span className="tarjeta-ac__id">{ac.id}</span>
            <select
              value={ac.tipo}
              onChange={e => actualizar(idx, "tipo", e.target.value)}
              className="selector-tipo-ac"
            >
              <option value="positivo">Positivo (flujo feliz)</option>
              <option value="negativo">Negativo (flujo de error)</option>
              <option value="contorno">Contorno (valor límite)</option>
            </select>
            <button
              className="btn-eliminar"
              onClick={() => eliminar(idx)}
              aria-label="Eliminar criterio"
            >
              ×
            </button>
          </div>

          <div className="tarjeta-ac__campos">
            <CampoAC
              etiqueta="DADO"
              descripcion="Estado previo del sistema y del actor"
              valor={ac.dado}
              ayuda="Describe un ESTADO, no una acción. Ej: 'El gestor está en el módulo Facturas'"
              onChange={v => actualizar(idx, "dado", v)}
            />
            <CampoAC
              etiqueta="CUANDO"
              descripcion="Una única acción concreta"
              valor={ac.cuando}
              ayuda="UNA sola acción. Ej: 'Pulsa el botón Buscar'"
              onChange={v => actualizar(idx, "cuando", v)}
            />
            <CampoAC
              etiqueta="ENTONCES"
              descripcion="Resultado observable y verificable"
              valor={ac.entonces}
              ayuda="Algo que SE VE o SE MIDE. Evita: 'el sistema funciona correctamente'"
              onChange={v => actualizar(idx, "entonces", v)}
              onBlur={v => evaluarVerificabilidad(ac.id, v)}
              indicadorExtra={
                verificabilidad[ac.id] != null ? (
                  <span className={`verificabilidad verificabilidad--${verificabilidad[ac.id] ? "ok" : "ko"}`}>
                    {verificabilidad[ac.id] ? "✓ Verificable" : "✗ No es verificable con un test concreto"}
                  </span>
                ) : null
              }
            />
          </div>

          {errores?.[idx] && (
            <div className="errores-criterio">
              {errores[idx].map((e, i) => (
                <p key={i} className={`error-inline error-inline--${e.severidad}`}>
                  {e.problema}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}

      <button className="btn btn--secundario btn--anadir" onClick={añadir}>
        + Añadir criterio de aceptación
      </button>
    </div>
  );
}
```

---

#### Pantalla 4 — Ejecución del pipeline

Esta es la pantalla que más impacto tiene en la percepción del analista sobre el sistema. Cuando el pipeline se ejecuta, el analista ve exactamente lo que ocurre paso a paso en tiempo real, con mensajes que explican en lenguaje de negocio qué está haciendo la IA en cada fase.

El diseño usa el WebSocket del backend para recibir eventos a medida que cada paso se completa. Cada paso tiene tres estados visuales: en espera (icono gris), en progreso (spinner), completado con éxito (check verde) o fallido (cruz roja con el mensaje de error expandible).

La pantalla también muestra una previsualización de los artefactos generados a medida que aparecen, sin esperar a que termine el pipeline completo. El analista puede leer la historia de usuario mientras el sistema genera las tareas técnicas, lo que reduce la percepción de tiempo de espera.

```jsx
// components/EjecucionPipeline.jsx
import { useState, useEffect, useRef } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";

const PASOS_PIPELINE = [
  { id: "s1_carga",                   label: "Cargando requisito" },
  { id: "s2_validacion",              label: "Validando calidad" },
  { id: "s3_rag_contexto",            label: "Consultando el repositorio" },
  { id: "s4_generacion_artefactos",   label: "Generando historia y tareas" },
  { id: "s5_generacion_test_cases",   label: "Generando test cases" },
  { id: "s6_analisis_impacto",        label: "Analizando impacto de cambios" },
  { id: "s7_registro_trazabilidad",   label: "Registrando trazabilidad" },
  { id: "s8_aprobacion",              label: "Preparando para revisión" },
];

export function EjecucionPipeline() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const reqId = searchParams.get("req");

  const [runId, setRunId] = useState(null);
  const [pasos, setPasos] = useState({});
  const [artefactos, setArtefactos] = useState(null);
  const [estadoFinal, setEstadoFinal] = useState(null);
  const [lanzando, setLanzando] = useState(false);
  const [dryRun, setDryRun] = useState(true);
  const wsRef = useRef(null);

  const lanzar = async () => {
    setLanzando(true);
    const r = await api.post("/pipeline/ejecutar", {
      req_id: reqId,
      dry_run: dryRun
    });
    setRunId(r.run_id);
    setLanzando(false);
    suscribirWebSocket(r.run_id);
  };

  const suscribirWebSocket = (runId) => {
    const ws = new WebSocket(`wss://pipeline-ai.interno/ws/pipeline/${runId}`);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      const evento = JSON.parse(e.data);

      if (evento.tipo === "paso_actualizado") {
        setPasos(prev => ({
          ...prev,
          [evento.paso]: {
            estado: evento.estado,
            resultado: evento.resultado,
            error: evento.error,
            duracion: evento.duracion_segundos
          }
        }));
      }

      if (evento.tipo === "artefactos_disponibles") {
        setArtefactos(evento.artefactos);
      }

      if (evento.estado_final) {
        setEstadoFinal(evento.estado_final);
        if (evento.estado_final === "pendiente_aprobacion") {
          navigate(`/aprobacion/${evento.aprobacion_id}`);
        }
      }
    };

    ws.onerror = () => {
      setEstadoFinal("error_conexion");
    };
  };

  useEffect(() => {
    return () => wsRef.current?.close();
  }, []);

  return (
    <div className="ejecucion-pipeline">
      <header className="ejecucion-header">
        <h1>Pipeline — {reqId}</h1>
        {!runId && (
          <div className="opciones-ejecucion">
            <label className="toggle-dryrun">
              <input
                type="checkbox"
                checked={dryRun}
                onChange={e => setDryRun(e.target.checked)}
              />
              Modo prueba (no enviar a Jira)
            </label>
            <button
              className="btn btn--primario btn--grande"
              onClick={lanzar}
              disabled={lanzando}
            >
              {lanzando ? "Iniciando..." : "▶ Ejecutar pipeline"}
            </button>
          </div>
        )}
      </header>

      {runId && (
        <div className="contenido-ejecucion">
          {/* Columna izquierda: progreso de pasos */}
          <aside className="panel-progreso">
            <h2>Progreso</h2>
            <ol className="lista-pasos">
              {PASOS_PIPELINE.map(paso => {
                const estado = pasos[paso.id]?.estado || "pendiente";
                return (
                  <li key={paso.id} className={`paso paso--${estado}`}>
                    <span className="paso__icono">
                      {estado === "completado" && "✓"}
                      {estado === "en_curso" && <span className="spinner" />}
                      {estado === "fallido" && "✗"}
                      {estado === "omitido" && "⏭"}
                      {estado === "pendiente" && "○"}
                    </span>
                    <span className="paso__label">{paso.label}</span>
                    {pasos[paso.id]?.duracion && (
                      <span className="paso__duracion">
                        {pasos[paso.id].duracion.toFixed(1)}s
                      </span>
                    )}
                    {estado === "fallido" && (
                      <details className="paso__error">
                        <summary>Ver error</summary>
                        <p>{pasos[paso.id]?.error}</p>
                      </details>
                    )}
                  </li>
                );
              })}
            </ol>
          </aside>

          {/* Columna derecha: previsualización de artefactos */}
          <main className="panel-artefactos">
            {!artefactos && !estadoFinal && (
              <div className="estado-espera">
                <span className="spinner spinner--grande" />
                <p>La IA está generando los artefactos...</p>
              </div>
            )}

            {artefactos && (
              <PrevisualizacionArtefactos artefactos={artefactos} />
            )}

            {estadoFinal === "validacion_fallida" && (
              <div className="alerta alerta--error">
                <h3>El requisito no supera la validación</h3>
                <p>
                  Hay problemas bloqueantes que deben resolverse antes de
                  continuar. Ve al editor del requisito para corregirlos.
                </p>
                <button
                  className="btn btn--primario"
                  onClick={() => navigate(`/requisitos/${reqId}`)}
                >
                  Ir al editor
                </button>
              </div>
            )}
          </main>
        </div>
      )}
    </div>
  );
}
```

---

#### Pantalla 5 — Aprobación de artefactos

La pantalla de aprobación es el gate humano del modelo. Nada llega a Jira sin pasar por aquí.

El diseño responde a la pregunta que se hace el analista al revisar el output: "¿Esto representa correctamente lo que pidió el negocio?" Para facilitar esa evaluación, la pantalla muestra los artefactos en un formato cercano al de Jira, no en JSON crudo.

Tiene tres secciones:

**Comparativa contexto / artefacto generado.** Un panel dividido que muestra a la izquierda los campos clave del requisito origen (actor, descripción, criterios de aceptación) y a la derecha la historia generada. El analista puede comparar directamente sin tener que navegar entre pantallas.

**Lista de artefactos revisables.** La historia de usuario, las cuatro tareas técnicas y el resumen de test cases, cada uno con un indicador de estado (aprobado / pendiente / editado). El analista puede expandir cada artefacto para ver su contenido completo y editarlo en línea si necesita ajustes menores.

**Panel de decisión.** Tres botones con semántica clara: Aprobar y enviar a Jira (verde), Editar y aprobar después (naranja), Rechazar y devolver al analista (rojo). El botón de rechazo abre un campo de texto obligatorio para el motivo, que queda registrado en el log del sistema.

```jsx
// components/AprobacionArtefactos.jsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";

export function AprobacionArtefactos() {
  const { aprobacionId } = useParams();
  const navigate = useNavigate();

  const [datos, setDatos] = useState(null);
  const [ediciones, setEdiciones] = useState({});
  const [modoEdicion, setModoEdicion] = useState(null);
  const [motivo, setMotivo] = useState("");
  const [confirmando, setConfirmando] = useState(null);
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    api.get(`/aprobaciones/${aprobacionId}`).then(d => {
      setDatos(d);
      // Inicializar ediciones con los valores actuales
      setEdiciones(d.artefactos);
    });
  }, [aprobacionId]);

  const decidir = async (decision) => {
    setEnviando(true);
    const payload = {
      decision,
      motivo,
      artefactos_editados: Object.keys(ediciones).length > 0 ? ediciones : null
    };
    await api.post(`/aprobaciones/${aprobacionId}/decidir`, payload);
    setEnviando(false);
    navigate("/dashboard", { state: { mensaje: `Requisito ${datos.requisito_id} ${decision === "aprobar" ? "aprobado y enviado a Jira" : decision === "rechazar" ? "rechazado" : "guardado para edición"}` } });
  };

  if (!datos) return <Cargando />;

  const { historia, tareas, test_cases, requisito_origen } = datos.artefactos;

  return (
    <div className="aprobacion-artefactos">
      <header className="aprobacion-header">
        <h1>Revisión de artefactos — {datos.requisito_id}</h1>
        <p className="aprobacion-descripcion">
          Revisa los artefactos generados por la IA. Nada se enviará a Jira
          hasta que apruebes esta revisión.
        </p>
      </header>

      {/* Alertas de validación */}
      {datos.informe_validacion?.veredicto_final === "APROBADO_CON_ADVERTENCIAS" && (
        <div className="alerta alerta--advertencia">
          <strong>El requisito tiene advertencias de calidad.</strong> Los artefactos
          se han generado, pero revisa con atención los criterios de aceptación.
          <button onClick={() => setModoEdicion("informe_validacion")}>
            Ver informe completo
          </button>
        </div>
      )}

      {/* Alerta de impacto de cambios */}
      {datos.informe_impacto?.informe_impacto?.nivel_urgencia === "CRITICO" && (
        <div className="alerta alerta--critico">
          <strong>⚠ Cambio crítico detectado.</strong>{" "}
          {datos.informe_impacto.informe_impacto.plan_accion.resumen_ejecutivo}
          <a href={`/impacto/${datos.requisito_id}`}>Ver análisis completo</a>
        </div>
      )}

      {/* Comparativa requisito / historia */}
      <div className="comparativa">
        <div className="comparativa__origen">
          <h2>Requisito origen</h2>
          <dl className="ficha-requisito">
            <dt>Actor</dt>
            <dd>{requisito_origen.actor}</dd>
            <dt>Evento</dt>
            <dd>{requisito_origen.evento_disparador}</dd>
            <dt>Descripción</dt>
            <dd>{requisito_origen.descripcion}</dd>
          </dl>
        </div>
        <div className="comparativa__historia">
          <h2>Historia generada</h2>
          <div className="historia-preview">
            <p className="historia-narrativa">{historia.summary}</p>
            <div className="historia-ac">
              <h3>Criterios de aceptación ({historia.acceptance_criteria.length})</h3>
              {historia.acceptance_criteria.map(ac => (
                <div key={ac.id} className="ac-preview">
                  <span className="ac-id">{ac.id}</span>
                  <div className="ac-cuerpo">
                    <p><strong>Dado</strong> {ac.dado}</p>
                    <p><strong>Cuando</strong> {ac.cuando}</p>
                    <p><strong>Entonces</strong> {ac.entonces}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Tareas técnicas */}
      <section className="seccion-tareas">
        <h2>Tareas técnicas ({tareas.length})</h2>
        <div className="grid-tareas">
          {tareas.map((tarea, idx) => (
            <TarjetaTarea
              key={idx}
              tarea={tarea}
              editable={modoEdicion === `tarea_${idx}`}
              onEditar={() => setModoEdicion(`tarea_${idx}`)}
              onGuardar={t => {
                setEdiciones(prev => ({
                  ...prev,
                  tareas: prev.tareas.map((t2, i) => i === idx ? t : t2)
                }));
                setModoEdicion(null);
              }}
            />
          ))}
        </div>
      </section>

      {/* Resumen test cases */}
      <section className="seccion-test-cases">
        <h2>Test cases generados ({test_cases.length})</h2>
        <div className="resumen-tc">
          <span className="tc-tipo tc-tipo--positivo">
            {test_cases.filter(t => t.tipo.includes("positivo")).length} positivos
          </span>
          <span className="tc-tipo tc-tipo--negativo">
            {test_cases.filter(t => t.tipo.includes("negativo")).length} negativos
          </span>
          <span className="tc-tipo tc-tipo--contorno">
            {test_cases.filter(t => t.tipo.includes("contorno")).length} contorno
          </span>
        </div>
        <button
          className="btn btn--fantasma"
          onClick={() => setModoEdicion("test_cases")}
        >
          Ver todos los test cases
        </button>
      </section>

      {/* Panel de decisión */}
      <footer className="panel-decision">
        {confirmando === "rechazar" ? (
          <div className="confirmacion-rechazo">
            <label>
              Motivo del rechazo (obligatorio)
              <textarea
                value={motivo}
                onChange={e => setMotivo(e.target.value)}
                placeholder="Explica qué está mal para que el pipeline pueda mejorarse..."
                rows={3}
                required
              />
            </label>
            <div className="confirmacion-botones">
              <button
                className="btn btn--error"
                onClick={() => decidir("rechazar")}
                disabled={!motivo.trim() || enviando}
              >
                Confirmar rechazo
              </button>
              <button
                className="btn btn--fantasma"
                onClick={() => setConfirmando(null)}
              >
                Cancelar
              </button>
            </div>
          </div>
        ) : (
          <div className="botones-decision">
            <button
              className="btn btn--error"
              onClick={() => setConfirmando("rechazar")}
            >
              Rechazar
            </button>
            <button
              className="btn btn--advertencia"
              onClick={() => decidir("editar")}
              disabled={enviando}
            >
              Guardar para editar después
            </button>
            <button
              className="btn btn--exito btn--grande"
              onClick={() => decidir("aprobar")}
              disabled={enviando}
            >
              {enviando ? "Enviando a Jira..." : "✓ Aprobar y enviar a Jira"}
            </button>
          </div>
        )}
      </footer>
    </div>
  );
}
```

---

### API client y gestión de estado global

```javascript
// services/api.js
const BASE_URL = import.meta.env.VITE_API_URL || "https://pipeline-ai.interno/api";

class ApiClient {
  #token = null;

  setToken(token) {
    this.#token = token;
    localStorage.setItem("pipeline_token", token);
  }

  #headers() {
    return {
      "Content-Type": "application/json",
      ...(this.#token ? { Authorization: `Bearer ${this.#token}` } : {})
    };
  }

  async get(endpoint, { params } = {}) {
    const url = new URL(`${BASE_URL}${endpoint}`);
    if (params) {
      Object.entries(params).forEach(([k, v]) => v && url.searchParams.set(k, v));
    }
    const r = await fetch(url, { headers: this.#headers() });
    if (!r.ok) throw new Error(`API error ${r.status}: ${endpoint}`);
    return r.json();
  }

  async post(endpoint, body) {
    const r = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: this.#headers(),
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error(`API error ${r.status}: ${endpoint}`);
    return r.json();
  }

  async put(endpoint, body) {
    const r = await fetch(`${BASE_URL}${endpoint}`, {
      method: "PUT",
      headers: this.#headers(),
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error(`API error ${r.status}: ${endpoint}`);
    return r.json();
  }
}

export const api = new ApiClient();
// Restaurar token de sesión anterior
const tokenGuardado = localStorage.getItem("pipeline_token");
if (tokenGuardado) api.setToken(tokenGuardado);
```

---

### Despliegue de la aplicación web

```yaml
# docker-compose.pipeline-ai.yml
version: "3.9"

services:
  api:
    build: ./pipeline-ai
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - JIRA_BASE_URL=${JIRA_BASE_URL}
      - JIRA_API_TOKEN=${JIRA_API_TOKEN}
      - JIRA_USER_EMAIL=${JIRA_USER_EMAIL}
      - JIRA_PROJECT_KEY=${JIRA_PROJECT_KEY}
      - DB_HOST=postgres
      - DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - postgres
    restart: unless-stopped

  frontend:
    build: ./pipeline-ai/frontend
    environment:
      - VITE_API_URL=https://pipeline-ai.interno/api
    restart: unless-stopped

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: pipeline_ai
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - api
      - frontend
    restart: unless-stopped

volumes:
  pgdata:
```

---

## Opción B — Integración en Confluence

La integración en Confluence permite al analista trabajar sin salir del entorno que ya conoce. Funciona mediante dos mecanismos: una macro de Confluence que renderiza el YAML del requisito como formulario editable, y un botón de acción personalizado que lanza el pipeline desde la propia página.

### Macro de edición de requisito

Confluence permite crear macros de usuario (User Macros) que procesan el contenido de una página y lo muestran de forma diferente. La macro de requisito toma el bloque de código YAML del requisito y lo renderiza como una tabla estructurada para los usuarios de negocio y un formulario editable para los analistas.

```html
<!-- Macro de Confluence: pipeline-ai-requisito -->
<!-- Configuración: requiere parámetro req_id -->

## @param req_id:title=ID del requisito|type=string|required=true
## @param modo:title=Modo de visualización|type=enum|enumValues=lectura,edicion|default=lectura

<div class="pipeline-ai-requisito" data-req-id="$req_id" data-modo="$modo">

  #if ($modo == "lectura")
    <!-- Vista de negocio: tabla amigable -->
    #set($req = $action.getPageContent($req_id))
    <div class="requisito-tarjeta">
      <!-- Se renderiza desde el YAML como tabla legible -->
      <!-- Ver sección de renderizado para el detalle -->
    </div>
  #else
    <!-- Vista de analista: iframe con la SPA -->
    <div class="pipeline-ai-embed">
      <iframe
        src="https://pipeline-ai.interno/embed/requisito/$req_id"
        width="100%"
        height="800px"
        frameborder="0"
        title="Editor de requisito $req_id"
      />
    </div>
  #end

  <!-- Botón de acción: lanza el pipeline -->
  <div class="pipeline-ai-acciones">
    <button
      class="aui-button aui-button-primary pipeline-ai-btn-ejecutar"
      data-req-id="$req_id"
      onclick="PipelineAI.ejecutar('$req_id', event)"
    >
      ▶ Ejecutar pipeline
    </button>
    <span class="pipeline-ai-estado" id="estado-$req_id">
      <!-- Estado actualizado vía JavaScript -->
    </span>
  </div>

</div>

<script>
// JavaScript que se inyecta con la macro
// Requiere que el token de autenticación esté en el contexto de Confluence
window.PipelineAI = window.PipelineAI || {

  async ejecutar(reqId, evento) {
    const btn = evento.target;
    btn.disabled = true;
    btn.textContent = "Iniciando...";

    try {
      const token = await this.obtenerToken();
      const r = await fetch("https://pipeline-ai.interno/api/pipeline/ejecutar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ req_id: reqId, dry_run: true })
      });

      const { run_id } = await r.json();
      btn.textContent = "Ejecutando...";

      // Abrir la pantalla de seguimiento en la SPA
      window.open(
        `https://pipeline-ai.interno/pipeline/ejecutar?req=${reqId}&run=${run_id}`,
        "pipeline-ai",
        "width=1200,height=800"
      );

      document.getElementById(`estado-${reqId}`).textContent =
        `Pipeline iniciado · Run: ${run_id}`;

    } catch (e) {
      btn.disabled = false;
      btn.textContent = "▶ Ejecutar pipeline";
      alert(`Error al iniciar el pipeline: ${e.message}`);
    }
  },

  async obtenerToken() {
    // Obtener el token del usuario autenticado en Confluence
    // vía el contexto de la macro o un endpoint de autenticación propio
    return localStorage.getItem("pipeline_token") ||
           await this.autenticar();
  },

  async autenticar() {
    // Redirección al IdP si no hay token
    window.location.href = "https://pipeline-ai.interno/auth/login?redirect=" +
      encodeURIComponent(window.location.href);
  }
};
</script>
```

### Renderizado del YAML como tarjeta de negocio

El script de sincronización convierte el YAML de cada requisito en la vista de tabla amigable que ven los usuarios de negocio en Confluence. Reemplaza el bloque de código YAML por una representación visual estructurada equivalente a la del punto 14 del modelo operativo.

```python
# scripts/sincronizar_confluence.py
"""
Sincroniza el repositorio de requisitos YAML con Confluence.
Para cada requisito:
  1. Convierte el YAML a la representación de tabla legible para negocio
  2. Actualiza la página de Confluence con la representación actualizada
  3. Mantiene el YAML embebido en la página como bloque colapsable para el analista

Se ejecuta automáticamente vía CI/CD cuando hay cambios en el repositorio Git.
"""

import yaml
import requests
import json
from pathlib import Path
from config import PipelineConfig, ConfluenceConfig


def yaml_a_html_tarjeta(req: dict) -> str:
    """
    Convierte un dict de requisito al HTML de la tarjeta
    de usuario de negocio para Confluence.
    Equivale a la 'vista para el usuario de negocio' del punto 14.
    """
    color_prioridad = {
        "must-have": "#d32f2f",
        "should-have": "#f57c00",
        "could-have": "#388e3c",
        "wont-have": "#757575"
    }.get(req.get("prioridad", ""), "#757575")

    color_estado = {
        "validado": "#2e7d32",
        "en-revision": "#f57f17",
        "borrador": "#546e7a",
        "rechazado": "#c62828"
    }.get(req.get("estado", ""), "#546e7a")

    criterios_html = ""
    for ac in req.get("criterios_aceptacion", []):
        criterios_html += f"""
        <tr>
          <td style="padding:8px;border-bottom:1px solid #eee">
            ✓ Si {ac.get('dado', '')},
            cuando {ac.get('cuando', '')},
            {ac.get('entonces', '')}
          </td>
        </tr>"""

    reglas_html = ""
    for regla in req.get("reglas_negocio", []):
        reglas_html += f"<li>• {regla}</li>"

    return f"""
    <div style="border:1px solid #ddd;border-radius:4px;font-family:Arial,sans-serif;max-width:800px">
      <table style="width:100%;border-collapse:collapse">
        <tr style="background:#f5f5f5">
          <td colspan="2" style="padding:12px;border-bottom:2px solid #2196F3">
            <strong style="font-size:14px">REQUISITO {req.get('id','')}</strong>
            &nbsp;&nbsp;
            <span style="background:{color_estado};color:white;padding:2px 8px;border-radius:3px;font-size:11px">
              {req.get('estado','').upper()}
            </span>
            &nbsp;
            <span style="background:{color_prioridad};color:white;padding:2px 8px;border-radius:3px;font-size:11px">
              {req.get('prioridad','').upper()}
            </span>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding:12px;border-bottom:1px solid #eee;font-size:16px;font-weight:bold">
            {req.get('titulo','')}
          </td>
        </tr>
        <tr>
          <td style="padding:12px;width:50%;border-right:1px solid #eee;vertical-align:top">
            <strong>¿QUIÉN LO NECESITA?</strong><br/>
            {req.get('actor','')}
          </td>
          <td style="padding:12px;vertical-align:top">
            <strong>¿POR QUÉ?</strong><br/>
            {req.get('objetivo_negocio','') or req.get('descripcion','')[:200]}
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding:12px;border-top:1px solid #eee">
            <strong>¿QUÉ DEBE HACER EL SISTEMA?</strong><br/>
            {req.get('descripcion','')}
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding:12px;border-top:1px solid #eee">
            <strong>¿CUÁNDO DEBE FUNCIONAR? (Criterios de aceptación)</strong>
            <table style="width:100%;margin-top:8px">
              {criterios_html}
            </table>
          </td>
        </tr>
        {'<tr><td colspan="2" style="padding:12px;border-top:1px solid #eee"><strong>REGLAS IMPORTANTES</strong><ul style="margin:4px 0">'+reglas_html+'</ul></td></tr>' if reglas_html else ''}
        <tr style="background:#fafafa">
          <td colspan="2" style="padding:8px 12px;font-size:11px;color:#666;border-top:1px solid #eee">
            Solicitado por: {req.get('origen',{}).get('solicitante','')} · 
            Analista: {req.get('analista','')}
          </td>
        </tr>
      </table>
    </div>
    """


class SincronizadorConfluence:
    def __init__(self, confluence_config: ConfluenceConfig):
        self.cfg = confluence_config
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {confluence_config.api_token}"
        }

    def actualizar_pagina_requisito(self, req_id: str, req: dict):
        """
        Actualiza la página de Confluence de un requisito con
        la tarjeta de negocio y el YAML colapsable para el analista.
        """
        tarjeta_html = yaml_a_html_tarjeta(req)
        yaml_str = yaml.dump(req, allow_unicode=True, default_flow_style=False)

        cuerpo_confluence = f"""
        {tarjeta_html}

        <ac:structured-macro ac:name="expand">
          <ac:parameter ac:name="title">
            Ver YAML técnico (analistas y pipeline)
          </ac:parameter>
          <ac:rich-text-body>
            <ac:structured-macro ac:name="code">
              <ac:parameter ac:name="language">yaml</ac:parameter>
              <ac:plain-text-body><![CDATA[{yaml_str}]]></ac:plain-text-body>
            </ac:structured-macro>
          </ac:rich-text-body>
        </ac:structured-macro>

        <div class="pipeline-ai-requisito" data-req-id="{req_id}" data-modo="lectura">
          <div class="pipeline-ai-acciones" style="margin-top:16px">
            <button
              class="aui-button aui-button-primary"
              onclick="PipelineAI.ejecutar('{req_id}', event)"
            >
              ▶ Ejecutar pipeline AI
            </button>
          </div>
        </div>
        """

        pagina_id = self._buscar_pagina(req_id)
        if pagina_id:
            self._actualizar_pagina(pagina_id, req["titulo"], cuerpo_confluence)
        else:
            self._crear_pagina(req_id, req["titulo"], cuerpo_confluence)

    def _buscar_pagina(self, req_id: str) -> str | None:
        r = requests.get(
            f"{self.cfg.base_url}/rest/api/content",
            params={"spaceKey": self.cfg.space_key, "title": req_id},
            headers=self.headers
        )
        resultados = r.json().get("results", [])
        return resultados[0]["id"] if resultados else None

    def _actualizar_pagina(self, pagina_id: str, titulo: str, cuerpo: str):
        r = requests.get(
            f"{self.cfg.base_url}/rest/api/content/{pagina_id}",
            headers=self.headers
        )
        version_actual = r.json()["version"]["number"]

        requests.put(
            f"{self.cfg.base_url}/rest/api/content/{pagina_id}",
            headers=self.headers,
            json={
                "version": {"number": version_actual + 1},
                "title": titulo,
                "type": "page",
                "body": {
                    "storage": {
                        "value": cuerpo,
                        "representation": "storage"
                    }
                }
            }
        )

    def _crear_pagina(self, req_id: str, titulo: str, cuerpo: str):
        requests.post(
            f"{self.cfg.base_url}/rest/api/content",
            headers=self.headers,
            json={
                "type": "page",
                "title": titulo,
                "space": {"key": self.cfg.space_key},
                "ancestors": [{"id": self.cfg.pagina_padre_id}],
                "body": {
                    "storage": {
                        "value": cuerpo,
                        "representation": "storage"
                    }
                }
            }
        )
```

---

## Decisión: ¿aplicación web o integración Confluence?

La siguiente tabla resume los criterios para elegir en cada contexto de organización:

| Criterio | Aplicación web | Integración Confluence |
|---|---|---|
| **Tiempo de despliegue** | 1-2 semanas | 3-4 semanas (permisos admin) |
| **Perfil técnico requerido** | Backend Python + React | Admin Confluence + JavaScript |
| **Resistencia al cambio** | Mayor (nueva herramienta) | Menor (mismo entorno) |
| **Flexibilidad de UX** | Total | Limitada por macros Confluence |
| **Trazabilidad documental** | Separada de Confluence | Nativa en Confluence |
| **Mantenimiento** | Propio | Depende de versiones Confluence |
| **Recomendación** | Piloto y proyectos nuevos | Organizaciones con Confluence establecido |

La combinación óptima a medio plazo es la siguiente: la **aplicación web** como interfaz principal del pipeline (ejecución, aprobación, dashboard), y la **integración Confluence** para la vista de lectura y el botón de lanzamiento desde las páginas de requisitos existentes. El analista vive en Confluence para la documentación y tiene la SPA para las operaciones del pipeline.

---

## Guía rápida de uso para el analista

Esta es la hoja de referencia de una página que recibe el analista el primer día. No requiere conocimientos técnicos.

```
┌─────────────────────────────────────────────────────────────┐
│ GUÍA RÁPIDA — Interfaz del pipeline AI                      │
│ Acceso: https://pipeline-ai.interno                         │
├─────────────────────────────────────────────────────────────┤
│ EL FLUJO EN 5 PASOS                                         │
│                                                             │
│ 1. Abre el requisito en el listado y edítalo                │
│    Rellena los cinco bloques del formulario.                │
│    Campos obligatorios marcados con *.                      │
│    Guarda cuando termines.                                  │
│                                                             │
│ 2. Cambia el estado a "En revisión" y guarda                │
│    El validador automático se ejecuta al guardar.           │
│    Si hay errores bloqueantes, aparecen en rojo.            │
│    Corrígelos antes de continuar.                           │
│                                                             │
│ 3. Pulsa "Ejecutar pipeline"                                │
│    Elige modo prueba (no envía a Jira) para la primera vez. │
│    Verás el progreso paso a paso en tiempo real.            │
│                                                             │
│ 4. Revisa los artefactos generados                          │
│    La pantalla de aprobación muestra la historia,           │
│    las tareas técnicas y el resumen de test cases.          │
│    Compara con el requisito original.                       │
│                                                             │
│ 5. Decide: Aprobar, Editar o Rechazar                       │
│    Aprobar → los artefactos van a Jira automáticamente.     │
│    Editar → puedes ajustar antes de enviar.                 │
│    Rechazar → el pipeline aprende de tu feedback.           │
├─────────────────────────────────────────────────────────────┤
│ CUÁNDO RECHAZAR EL OUTPUT                                   │
│ × El actor no es el correcto                                │
│ × Un criterio AC no se puede testear                        │
│ × Las tareas mezclan trabajo de frontend y backend          │
│ × La estimación de puntos es claramente incorrecta          │
├─────────────────────────────────────────────────────────────┤
│ SI ALGO FALLA                                               │
│ 1. El pipeline no es un bloqueante: crea los artefactos     │
│    en Jira manualmente como siempre.                        │
│ 2. Reporta el problema en el canal #pipeline-ai.            │
│ 3. El champion responde en menos de 4 horas laborables.     │
└─────────────────────────────────────────────────────────────┘
```

---

## Relación con los demás componentes del modelo

La interfaz de analista no añade lógica nueva: conecta los componentes ya construidos con las personas que los usan.

El formulario del editor (Pantalla 3) consume la **plantilla de requisito del punto 1** y llama al **validador automático del punto 6** para cada campo. La pantalla de ejecución (Pantalla 4) lanza el **orquestador del script** que encadena los pasos 4 al 10. La pantalla de aprobación (Pantalla 5) implementa el **gate humano de la cola de aprobación del punto 10**, que garantiza que ningún artefacto llega a Jira sin revisión. Las sugerencias contextuales de requisitos similares usan el **motor RAG del punto 7**. Y el panel de impacto de cambios visible en la pantalla de aprobación muestra el output del **analizador de impacto del punto 8**.

La interfaz también alimenta el **sistema de gobierno del punto 12**: cada edición que hace el analista antes de aprobar queda registrada como feedback para el evaluador de prompts. El campo más editado en la semana aparece en el dashboard semanal del comité de gobierno como señal de qué prompt necesita atención.
```
