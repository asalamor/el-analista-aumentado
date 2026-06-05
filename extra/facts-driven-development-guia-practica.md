# FACTS-Driven Development: de las especificaciones narrativas a los hechos atómicos verificables

> **Versión:** Junio 2026 · **Dominio de ejemplos:** Banca digital (cuenta corriente, pagos, autenticación)
> **Prerequisito recomendado:** familiaridad básica con Spec-Driven Development (SDD)

---

## 1. El problema de las specs narrativas a escala

### Por qué las specs en prosa se degradan con el tiempo

Una especificación narrativa nace con buenas intenciones: describe en lenguaje natural lo que el sistema debe hacer, por qué, y bajo qué condiciones. En los primeros sprints funciona. El equipo la lee, la entiende y la usa como referencia.

El problema aparece en el sprint 8, cuando alguien añade un párrafo nuevo al documento sin borrar el párrafo contradictorio que había tres páginas antes. O cuando el product owner actualiza la sección de "flujo de autenticación" pero olvida que esa misma lógica está descrita también en el documento de "gestión de sesiones". Nadie lo detecta porque nadie relee la spec entera para cada cambio.

Con el tiempo, la spec narrativa se convierte en **arqueología**: hay que excavar capas de texto para reconstruir qué es verdad hoy. Para un agente de IA, esto es fatal.

**Las tres patologías de las specs narrativas maduras:**

```
SPEC NARRATIVA en el tiempo
│
├── Sprint 1:  "El usuario puede autenticarse con email y contraseña"
│              [texto claro, conciso, útil]
│
├── Sprint 4:  [párrafo añadido] "También se soporta autenticación biométrica
│              en dispositivos móviles, excepto en la versión web"
│              [spec creciendo, aún manejable]
│
├── Sprint 9:  [párrafo nuevo] "El equipo de seguridad ha decidido que todos
│              los logins requieren 2FA a partir de ahora, salvo usuarios
│              corporativos con SSO"
│              [¿qué pasa con la biométrica? ¿es 2FA? ¿los corporativos
│               también usan biométrica? El texto no lo dice]
│
└── Sprint 14: [hotfix doc] "IMPORTANTE: la autenticación biométrica queda
               desactivada temporalmente por el bug #1204"
               [¿sigue así? ¿cuándo se reactivará? Nadie lo sabe]
```

Para el sprint 14, un agente de IA que lea esta spec puede generar cuatro implementaciones distintas, todas "razonables" según el texto. Ninguna será la correcta.

### Ambigüedad, redundancia y context decay en documentos largos

| Patología | Descripción | Coste en desarrollo con IA |
|---|---|---|
| **Ambigüedad** | Frases como "el sistema debe responder rápidamente" o "en la mayoría de casos" | El agente elige su propio criterio; el output varía entre sesiones |
| **Redundancia** | El mismo comportamiento descrito en dos lugares con ligeras diferencias | El agente puede seguir cualquiera de las dos versiones; las contradicciones producen código inconsistente |
| **Context decay** | Decisiones antiguas enterradas bajo capas de texto nuevo | El agente no ve la decisión original; la contradice sin saberlo |
| **Acoplamiento narrativo** | Un párrafo mezcla comportamiento, restricción técnica y justificación de negocio | El agente no puede extraer solo la parte ejecutable; genera ruido |
| **Specs zombie** | Secciones que describen comportamiento ya eliminado pero no se han borrado | El agente puede implementar funcionalidad que el equipo eliminó hace tres sprints |

### El coste de mantener specs narrativas en proyectos vivos

En proyectos con IA como implementador, el coste de una spec ambigua no es que un desarrollador humano pierda tiempo interpretándola. Es que el agente genera código incorrecto con total confianza, el desarrollador no detecta el problema hasta el code review, y el ciclo de regeneración comienza de nuevo.

**Estimación de impacto por tipo de defecto de spec:**

```
DEFECTO EN SPEC          COSTE (sin IA)    COSTE (con agente IA)
─────────────────────────────────────────────────────────────────
Ambigüedad menor         30 min reunión    2-4h regeneración + review
Contradicción entre      1h clarificación  4-8h código incorrecto en
secciones                                  producción
Spec zombie (comporta-   Ninguno si no     Feature eliminado reimple-
miento obsoleto)         se toca           mentado en código nuevo
Requisito NFR sin        Se asume default  Agente elige peor default;
métrica concreta         razonable         requiere refactoring
```

La conclusión es directa: **a mayor velocidad del agente, mayor coste de la ambigüedad**. SDD narrativo mejora esto, pero no lo resuelve completamente cuando las specs crecen. FACTS es la respuesta a esa brecha.

---

## 2. Qué es un "fact" en este contexto

### Definición formal

Un **fact** es la unidad mínima de conocimiento verificable sobre un sistema software. Es una afirmación:

- **Atómica:** expresa una sola verdad, no un conjunto de ellas
- **Explícita:** no requiere interpretación ni contexto adicional para entenderse
- **Verificable:** existe al menos una evidencia objetiva (test, métrica, log) que confirma o refuta la afirmación
- **Trazable:** tiene un identificador único y una referencia a su origen (requisito de negocio, decisión técnica, norma regulatoria)
- **Con vigencia:** tiene un estado que indica si sigue siendo verdad hoy

Un fact no es una historia. No tiene personajes, flujos ni motivaciones. Es una verdad del sistema expresada en la forma más compacta y precisa posible.

### Propiedades de un fact bien formado

**Atomicidad** significa que si descompones el fact en dos, cada parte sigue siendo una verdad independiente y útil. Si no puedes dividirlo más sin que pierda sentido, es atómico.

**Sin ambigüedad** significa que dos personas distintas que lean el fact llegan a la misma conclusión sobre qué debe verificarse. Palabras como "rápido", "seguro", "apropiado" o "en la mayoría de casos" rompen esta propiedad.

**Falsabilidad** (tomada de la epistemología de Popper) significa que existe al menos un escenario en el que el fact podría ser falso, y que ese escenario es comprobable. Un fact no falseable no es un fact: es una declaración de intenciones.

### Diferencia entre un fact, una spec narrativa y un requisito EARS

| Dimensión | Spec narrativa | Requisito EARS | Fact |
|---|---|---|---|
| **Granularidad** | Párrafo o sección | Frase estructurada (una historia de usuario) | Afirmación atómica única |
| **Unidad de cambio** | Se edita el documento completo | Se edita la historia o criterio | Se crea un nuevo fact; el anterior se depreca |
| **Consumible por agente** | Con dificultad; requiere parseo | Mejor, pero aún puede mezclar concerns | Directamente; un fact = una instrucción |
| **Trazabilidad** | Referencia implícita al documento | Referencia al ID de historia | ID único + origen + evidencia |
| **Estado de vigencia** | Implícito (hay que leer el historial de Git) | Implícito | Explícito: active / deprecated / in-review |
| **Detecta contradicciones** | Manual; muy costoso | Parcial | Automático: dos facts con misma clave y distinto valor = conflicto |

### Ejemplos concretos: facts válidos vs inválidos

**Dominio:** módulo de autenticación de un banco digital

```
❌ FACT INVÁLIDO — Ambiguo
"El sistema debe gestionar las sesiones de usuario de forma segura"
→ Problema: "segura" no tiene definición operativa. No es testeable.

❌ FACT INVÁLIDO — No atómico (mezcla dos verdades)
"Los tokens JWT expiran en 1 hora y los refresh tokens en 30 días"
→ Problema: son dos facts independientes mezclados en uno.

❌ FACT INVÁLIDO — No falseable
"El sistema debe ofrecer una buena experiencia de autenticación"
→ Problema: no existe test que confirme o refute "buena experiencia".

❌ FACT INVÁLIDO — Condición implícita
"Los usuarios pueden autenticarse con biometría"
→ Problema: ¿en qué plataformas? ¿bajo qué condiciones? Incompleto.

✅ FACT VÁLIDO
"Un token JWT de sesión expira exactamente 3600 segundos tras su emisión"
→ Atómico, explícito, testeable con una llamada a /me con token expirado.

✅ FACT VÁLIDO
"Un refresh token emitido para un dispositivo móvil tiene validez de 2592000 segundos (30 días)"
→ Atómico, explícito, distingue plataforma, testeable.

✅ FACT VÁLIDO
"La autenticación biométrica solo está disponible en clientes iOS y Android; no en la interfaz web"
→ Atómico (una restricción de plataforma), explícito, testeable en cada plataforma.

✅ FACT VÁLIDO
"Un intento de login fallido incrementa en 1 el contador de intentos fallidos asociado al email; al llegar a 5 la cuenta queda bloqueada durante 900 segundos"
→ Podría argumentarse que son dos hechos, pero la relación causal directa los hace inseparables como unidad funcional. Testeable con 5 llamadas a /login con credenciales incorrectas.
```

---

## 3. FACTS como evolución de SDD

### La línea de evolución: Vibe Coding → SDD → FACTS

```
EVOLUCIÓN DE LA DISCIPLINA DE ESPECIFICACIÓN CON IA
─────────────────────────────────────────────────────────────────────────

VIBE CODING (2025)
  "Añade login con email y contraseña"
  │
  ├── Ventaja: velocidad máxima en prototipado
  └── Problema: output impredecible, no mantenible, sin trazabilidad
       │
       ▼
SDD NARRATIVO (2025-2026)
  spec.md con historias de usuario y criterios EARS
  │
  ├── Ventaja: intención documentada, checkpoints humanos, trazabilidad básica
  └── Problema: specs crecen, se ambiguan, son difíciles de consumir
       por agentes a escala, las contradicciones son invisibles
       │
       ▼
FACTS-DRIVEN DEVELOPMENT (2026→)
  Repositorio de facts atómicos, versionados, con estado de vigencia
  │
  ├── Ventaja: cada fact es consumible directamente por el agente,
  │   las contradicciones son detectables automáticamente, el
  │   conocimiento del sistema no se degrada con el tiempo
  └── Complejidad: requiere disciplina de equipo y tooling adecuado
```

### Qué aporta FACTS que SDD narrativo no resuelve bien

| Limitación de SDD narrativo | Solución en FACTS |
|---|---|
| Una spec de 500 líneas supera el contexto efectivo de muchos agentes | Cada fact cabe en 5-10 líneas; el agente carga solo los facts relevantes |
| Detectar contradicciones requiere lectura humana completa | Dos facts con el mismo `subject` y `property` pero distinto `value` generan alerta automática |
| No hay forma de saber si un requisito sigue vigente sin leer el historial de Git | Cada fact tiene campo `status: active / deprecated / in-review` |
| El agente no sabe qué parte de la spec aplicar a qué función | Cada fact tiene `scope` que lo vincula a módulo, función o endpoint |
| Cambiar un requisito requiere editar texto en prosa y esperar que nadie use la versión vieja | Cambiar un fact crea nueva versión; la vieja pasa a `deprecated` con fecha |

### Cuándo tiene sentido el salto a FACTS y cuándo no

**FACTS es la elección correcta cuando:**
- El proyecto tiene más de 3 meses de vida y las specs están creciendo
- El equipo usa agentes de IA para la mayor parte de la implementación
- Hay requisitos de cumplimiento normativo (trazabilidad obligatoria)
- El sistema tiene múltiples módulos con comportamiento interdependiente
- El equipo rota y el conocimiento debe ser explícito, no tácito

**SDD narrativo sigue siendo suficiente cuando:**
- El proyecto es un prototipo o MVP de menos de 4 semanas
- El scope es muy limitado y estable (no crecerá)
- El equipo es de una sola persona con contexto completo en su cabeza
- La velocidad de entrega supera en importancia a la mantenibilidad

### Compatibilidad: ¿SDD y FACTS son excluyentes o complementarios?

No son excluyentes. La relación más productiva es:

- **Las specs SDD narrativas son el origen de los facts**, no su reemplazo. Una spec narrativa bien escrita puede descomponerse en 20-50 facts atómicos.
- **La CONSTITUTION.md de SDD se convierte en un conjunto de facts de arquitectura** en FACTS-Driven Development.
- **Los criterios EARS de SDD son el formato intermedio** que facilita la extracción de facts: un buen criterio EARS normalmente contiene 1-3 facts.

La transición natural es: **escribir specs narrativas para explorar y capturar intención → extraer facts atómicos de esas specs → usar los facts como input del agente en implementación**.

---

## 4. Taxonomía de facts en un sistema software

Un sistema software puede describirse completamente con seis categorías de facts. Cada categoría responde a una pregunta diferente.

### Las seis categorías

**Facts de comportamiento** — *¿Qué hace el sistema?*
Describen acciones observables del sistema ante inputs específicos. Son los más comunes y los primeros en definirse.

```
FACT-AUTH-001: Al recibir credenciales válidas en POST /auth/login,
el sistema emite un token JWT firmado con RS256 y un refresh token opaco.
```

**Facts de estado** — *¿En qué condiciones opera?*
Describen las condiciones bajo las que el sistema funciona de forma diferente, los estados posibles de una entidad y las transiciones válidas entre ellos.

```
FACT-ACC-007: Una cuenta bancaria puede estar en estado: active, frozen,
closed. Las transiciones válidas son: active→frozen, frozen→active,
active→closed. La transición frozen→closed no está permitida.
```

**Facts de restricción** — *¿Qué no puede hacer o no puede ser?*
Describen límites, prohibiciones y umbrales. Suelen derivarse de requisitos no funcionales o de negocio.

```
FACT-PAY-003: El importe máximo de una transferencia nacional sin
autorización adicional es 10.000,00 EUR por operación.
```

**Facts de contrato** — *¿Qué garantiza a otros sistemas?*
Describen los compromisos que este sistema hace a sus consumidores: tiempos de respuesta, formatos de respuesta, SLAs, versiones de API.

```
FACT-API-012: El endpoint GET /accounts/{id}/balance responde en menos
de 200ms en el percentil 95 bajo carga nominal (≤500 req/s).
```

**Facts de arquitectura** — *¿Cómo está construido?*
Describen decisiones de diseño que no pueden cambiar sin impacto en otros módulos: tecnologías elegidas, patrones de comunicación, estrategias de datos.

```
FACT-ARCH-004: Toda comunicación entre el servicio de autenticación
y el servicio de cuentas ocurre mediante eventos asíncronos sobre
el bus de eventos (Apache Kafka, topic: account-events).
No se permiten llamadas síncronas HTTP entre estos dos servicios.
```

**Facts de dominio** — *¿Qué verdades del negocio refleja el sistema?*
Describen reglas de negocio invariantes: definiciones, cálculos, clasificaciones. Son independientes de la implementación.

```
FACT-DOM-002: Un cliente se considera "de alto valor" si el saldo
medio de todas sus cuentas durante los últimos 90 días supera
los 50.000 EUR. Este umbral es revisado trimestralmente por el
equipo de producto.
```

### Ejemplo de tabla de facts para el módulo de autenticación

| ID | Categoría | Fact | Estado | Origen |
|---|---|---|---|---|
| FACT-AUTH-001 | Comportamiento | Al recibir credenciales válidas en POST /auth/login, se emite JWT (RS256) + refresh token opaco | active | REQ-SEC-001 |
| FACT-AUTH-002 | Restricción | Un JWT de sesión expira exactamente 3600s tras su emisión | active | DEC-SEC-2025-03 |
| FACT-AUTH-003 | Restricción | Un refresh token para móvil expira en 2592000s (30 días); para web en 86400s (1 día) | active | REQ-SEC-004 |
| FACT-AUTH-004 | Comportamiento | Tras 5 intentos de login fallidos consecutivos para el mismo email, la cuenta se bloquea 900s | active | REQ-SEC-007 |
| FACT-AUTH-005 | Restricción | La autenticación biométrica solo está disponible en clientes iOS y Android, no en web | active | DEC-PROD-2025-11 |
| FACT-AUTH-006 | Contrato | POST /auth/login responde en < 300ms en p95 bajo carga nominal | active | SLA-INT-001 |
| FACT-AUTH-007 | Arquitectura | Los tokens JWT se firman con RS256; la clave privada rota cada 90 días | active | DEC-SEC-2025-07 |
| FACT-AUTH-008 | Comportamiento | La autenticación biométrica era soportada en web hasta el 2025-11-15; deprecada por bug #1204 | deprecated | INC-2025-1204 |

---

## 5. Propiedades formales de un fact bien escrito

### Atomicidad

**Regla práctica:** si puedes usar la conjunción "y" para separar el fact en dos, probablemente no es atómico.

```
NO ATÓMICO:
"Los tokens JWT expiran en 3600s y se firman con RS256"
→ Dos propiedades distintas: duración y algoritmo de firma.
→ Pueden cambiar de forma independiente.

ATÓMICO:
FACT-AUTH-002: "Un JWT de sesión expira exactamente 3600s tras su emisión"
FACT-AUTH-007: "Los JWT se firman con el algoritmo RS256"
```

**Excepción justificada:** cuando la relación causal directa entre dos propiedades es la propia verdad que importa capturar (como en FACT-AUTH-004: el contador + el bloqueo son inseparables como regla de negocio), mantenerlos juntos es correcto.

### Trazabilidad

Cada fact debe poder responder a: *¿de dónde viene esta verdad?*

Los orígenes posibles son:
- **REQ-XXX:** requisito de negocio documentado
- **DEC-XXX:** decisión técnica o arquitectónica (Architecture Decision Record)
- **NRM-XXX:** norma regulatoria (PCI-DSS, GDPR, PSD2, ISO 27001...)
- **INC-XXX:** incidente o bug que generó una restricción
- **SLA-XXX:** acuerdo de nivel de servicio

### Falsabilidad

Un fact es falseable si puedes responder a: *¿qué test o evidencia demostraría que este fact es falso?*

```
FACT-AUTH-002: "Un JWT expira en 3600s"
→ Evidencia de falsación: emitir un JWT, esperar 3601s,
  llamar a /me con ese token. Si responde 200 OK, el fact es falso.
→ Test automatizable: ✅ Sí
→ ¿Es falseable? ✅ Sí → Es un fact válido.

"El sistema es seguro"
→ ¿Qué test demostraría que es falso?
→ No existe definición operativa de "seguro" en este contexto.
→ ¿Es falseable? ❌ No → No es un fact. Es una aspiración.
```

### Vigencia

El estado de vigencia es lo que distingue un repositorio de facts de una base de documentación muerta.

| Estado | Significado | Qué hace el agente |
|---|---|---|
| `active` | El fact es verdad hoy y el sistema debe cumplirlo | Lo usa como constraint en generación de código |
| `in-review` | El fact está siendo revisado; su verdad es incierta | No lo usa; alerta al humano antes de continuar |
| `deprecated` | El fact fue verdad pero ya no lo es; se mantiene por trazabilidad | Lo ignora en generación; lo usa solo para contexto histórico |
| `proposed` | El fact ha sido propuesto pero no aprobado aún | No lo usa; lo presenta al humano para aprobación |

### Plantilla mínima de un fact

```yaml
# Plantilla YAML — Fact bien formado
id: FACT-AUTH-002
title: "Expiración de token JWT de sesión"
statement: >
  Un token JWT de sesión expira exactamente 3600 segundos (1 hora)
  tras su fecha de emisión, codificada en el claim 'iat'.
category: restriction          # behavior | state | restriction | contract | architecture | domain
scope:
  module: auth-service
  endpoint: POST /auth/login
  function: issueSessionToken
status: active                 # active | deprecated | in-review | proposed
version: "1.2"
created: "2025-03-10"
last-updated: "2026-01-15"
origin:
  type: decision               # requirement | decision | regulation | incident | sla
  ref: DEC-SEC-2025-03
  description: "Decisión del equipo de seguridad en sesión del 10-mar-2025"
falsification:
  test: "auth/session-expiry.test.ts → test: 'JWT expires after 3600s'"
  evidence: "CI pipeline: auth-service tests (green)"
tags:
  - authentication
  - jwt
  - security
  - session-management
related-facts:
  - FACT-AUTH-003   # Refresh token expiry
  - FACT-AUTH-007   # JWT signing algorithm
deprecates: null
deprecated-by: null
notes: >
  Anteriormente era 7200s. Reducido a 3600s por recomendación
  de auditoría de seguridad Q1-2025 (INC-2025-0087).
```

---

## 6. Flujo de trabajo FACTS con agentes de IA

### Cómo un agente consume facts vs una spec narrativa

Cuando un agente recibe una spec narrativa de 800 palabras para implementar autenticación, hace lo siguiente (implícitamente):

1. Parsea el texto completo buscando instrucciones
2. Resuelve ambigüedades con sus propios defaults
3. Puede ignorar restricciones enterradas en párrafos secundarios
4. No detecta si dos párrafos se contradicen
5. El output depende de qué parte del texto "pesó más" en el contexto

Cuando un agente recibe 12 facts atómicos para implementar el mismo módulo:

1. Carga cada fact como una constraint independiente
2. No hay ambigüedades que resolver (los facts son explícitos)
3. Genera código que satisface cada fact o reporta que no puede
4. Si dos facts son contradictorios, puede detectarlo antes de escribir una línea
5. Cada función del output puede referenciarse a uno o más facts específicos

### Flujo completo: Identificar → Formalizar → Validar → Versionar → Consumir

```
CICLO DE VIDA DE UN FACT
─────────────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────┐
  │  FUENTE                                                      │
  │  Spec narrativa / Reunión de requisitos / Bug / ADR /        │
  │  Auditoría / Código legacy sin documentar                    │
  └──────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FASE 1: IDENTIFICAR                                         │
  │  Detectar una verdad candidata del sistema.                  │
  │  Herramienta: humano o agente con prompt de extracción       │
  │  Output: fact en estado 'proposed'                           │
  └──────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FASE 2: FORMALIZAR                                          │
  │  Escribir el fact según la plantilla: id, statement,         │
  │  category, scope, origin, falsification                      │
  │  Herramienta: editor + plantilla YAML                        │
  │  Output: fact completo en estado 'proposed'                  │
  └──────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FASE 3: VALIDAR (checkpoint humano obligatorio)             │
  │  - ¿Es atómico?                                              │
  │  - ¿Es falseable? ¿Existe el test?                           │
  │  - ¿Contradice algún fact existente?                         │
  │  - ¿El origen es trazable?                                   │
  │  Herramienta: checklist §11 + revisión de par                │
  │  Output: fact aprobado → estado 'active'                     │
  │          o rechazado → vuelve a FORMALIZAR                   │
  └──────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FASE 4: VERSIONAR                                           │
  │  Añadir el fact al repositorio. Commit en Git con            │
  │  referencia al origen (ticket, ADR, etc.)                    │
  │  Si reemplaza un fact anterior: deprecar el anterior         │
  │  con 'deprecated-by: FACT-XXX-nueva-version'                 │
  └──────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  FASE 5: CONSUMIR                                            │
  │  El agente de IA carga los facts relevantes al scope         │
  │  de la tarea. Los usa como constraints en generación,        │
  │  verificación y documentación de código.                     │
  └──────────────────────────────────────────────────────────────┘
```

### Cómo los agentes detectan contradicciones entre facts

Dado que cada fact tiene `subject`, `property` y `value` implícitos o explícitos, un agente puede detectar contradicciones con un prompt estructurado:

```
Analiza los siguientes facts del módulo [auth-service].
Para cada par de facts, verifica:
1. ¿Tienen el mismo subject y property pero distinto value?
   → CONTRADICCIÓN DIRECTA: reportar antes de continuar.
2. ¿Describe uno una condición que hace imposible lo que describe otro?
   → CONTRADICCIÓN LÓGICA: reportar con explicación.
3. ¿Uno extiende o especializa a otro sin contradecirlo?
   → RELACIÓN VÁLIDA: añadir 'related-facts' si no existe.

Antes de generar código, lista todas las contradicciones encontradas
y espera confirmación humana para resolverlas.
```

### Cómo los agentes generan código trazable a facts individuales

La convención clave: **cada bloque de código generado incluye una referencia al fact que lo origina**, como comentario o como anotación.

```typescript
// Implementación trazable a facts

/**
 * Emite un token JWT de sesión para el usuario autenticado.
 *
 * @fact FACT-AUTH-002 - JWT expira en 3600s
 * @fact FACT-AUTH-007 - JWT firmado con RS256
 * @fact FACT-AUTH-006 - Tiempo de respuesta < 300ms en p95
 */
async function issueSessionToken(userId: string): Promise<string> {
  const now = Math.floor(Date.now() / 1000);

  // FACT-AUTH-002: expiración exacta en 3600s desde emisión
  const payload = {
    sub: userId,
    iat: now,
    exp: now + 3600,  // exactamente 3600s → FACT-AUTH-002
  };

  // FACT-AUTH-007: algoritmo RS256 obligatorio
  return jwt.sign(payload, privateKey, { algorithm: 'RS256' });
}
```

Con esta convención, si el FACT-AUTH-002 cambia (por ejemplo, la expiración pasa a 1800s), el agente puede localizar exactamente qué funciones necesitan actualizarse buscando `@fact FACT-AUTH-002` en el código.

---

## 7. Estructura de repositorio orientado a FACTS

### Organización de archivos y carpetas

```
mi-proyecto/
│
├── facts/                           # Repositorio de facts (fuente de verdad)
│   │
│   ├── _index.yaml                  # Índice de todos los facts con estado y módulo
│   ├── _contradictions.md           # Log de contradicciones detectadas y resueltas
│   │
│   ├── architecture/                # Facts de arquitectura (todo el sistema)
│   │   ├── FACT-ARCH-001.yaml
│   │   ├── FACT-ARCH-002.yaml
│   │   └── ...
│   │
│   ├── domain/                      # Facts de dominio (reglas de negocio)
│   │   ├── FACT-DOM-001.yaml
│   │   └── ...
│   │
│   └── modules/                     # Facts por módulo
│       ├── auth/
│       │   ├── FACT-AUTH-001.yaml
│       │   ├── FACT-AUTH-002.yaml
│       │   └── ...
│       ├── accounts/
│       │   ├── FACT-ACC-001.yaml
│       │   └── ...
│       └── payments/
│           ├── FACT-PAY-001.yaml
│           └── ...
│
├── specs/                           # Specs SDD narrativas (origen de facts)
│   ├── CONSTITUTION.md              # Reglas del proyecto (ahora genera facts de arquitectura)
│   ├── TECH_STACK.md
│   └── features/
│       └── auth/
│           ├── spec.md              # Spec narrativa → origen de facts
│           ├── plan.md
│           └── tasks.md
│
├── src/                             # Código fuente (con anotaciones @fact)
├── tests/                           # Tests (vinculados a facts por ID)
└── README.md
```

### Formato recomendado

El formato YAML es el recomendado para facts individuales por tres razones:
1. Es legible por humanos y parseble por máquinas sin ambigüedad
2. Soporta campos opcionales sin romper el esquema
3. Es compatible con la mayoría de herramientas de CI/CD y MCP servers

El formato Markdown estructurado (con frontmatter YAML) es una alternativa válida cuando el equipo prefiere visualización directa en GitHub/GitLab.

### Ejemplo completo de fact en YAML

```yaml
# facts/modules/payments/FACT-PAY-003.yaml
id: FACT-PAY-003
title: "Límite de transferencia nacional sin autorización adicional"
statement: >
  El importe máximo de una transferencia nacional (destino en España)
  sin requerir autorización adicional (segundo factor o confirmación
  de operaciones) es de 10.000,00 EUR por operación individual.
  Operaciones que superen este importe son rechazadas con HTTP 422
  y código de error TRANSFER_LIMIT_EXCEEDED.
category: restriction
scope:
  module: payments-service
  endpoint: POST /payments/transfer/national
  function: validateTransferAmount
status: active
version: "2.0"
created: "2024-08-01"
last-updated: "2025-09-20"
origin:
  type: regulation
  ref: NRM-PSD2-ART-97
  description: "Reglamento PSD2, Art. 97 - Autenticación reforzada de cliente"
falsification:
  test: "payments/transfer-limits.test.ts → test: 'rejects transfer over 10000 EUR'"
  evidence: "CI pipeline: payments-service tests + compliance-check suite"
tags:
  - payments
  - compliance
  - psd2
  - national-transfer
  - limits
related-facts:
  - FACT-PAY-004   # Límite transferencia internacional
  - FACT-PAY-005   # Proceso de autorización adicional
  - FACT-DOM-003   # Definición de "transferencia nacional"
deprecates: "FACT-PAY-003-v1"   # Anterior límite era 5.000 EUR
deprecated-by: null
notes: >
  Límite elevado de 5.000 EUR a 10.000 EUR en sept-2025 tras
  actualización interna de política de riesgo (POL-RISK-2025-09).
  El límite regulatorio de PSD2 no establece importe máximo;
  el valor de 10.000 EUR es decisión interna de la entidad.
```

### Integración con CONSTITUTION.md y TECH_STACK.md de SDD

La CONSTITUTION.md de SDD se convierte en un generador de facts de arquitectura. Cada regla de la constitución es un fact candidato:

```
CONSTITUTION.md (SDD):                    FACTS (resultado):
──────────────────────────                ────────────────────────────────
"Toda comunicación entre servicios    →   FACT-ARCH-004: "Toda comunicación
 usa eventos asíncronos"                   entre servicios ocurre mediante
                                           eventos sobre Kafka; no se
                                           permiten llamadas HTTP síncronas
                                           entre microservicios internos"

"No queries directas a BD desde       →   FACT-ARCH-008: "Los controllers
 controllers"                              no pueden importar directamente
                                           clases del ORM; solo pueden usar
                                           interfaces de Repository"

"JWT con expiración de 1h"            →   FACT-AUTH-002: "Un JWT de sesión
                                           expira exactamente 3600s tras
                                           su emisión"
```

---

## 8. De spec narrativa a facts: proceso de migración

### Estrategia general

La migración no es un proyecto de un sprint: es un proceso incremental que sigue la regla **"spec-near-the-change"** heredada de SDD: descompones en facts el área del sistema que vas a tocar, no todo el sistema de golpe.

```
PROCESO DE MIGRACIÓN INCREMENTAL
─────────────────────────────────────────────────────────

Sprint N: Feature de pagos internacionales
│
├── 1. Identificar spec narrativa afectada
│       specs/features/payments/spec.md (8 páginas)
│
├── 2. Extraer facts del área de cambio
│       Prompt de extracción → 15 facts candidatos
│       Revisión humana → 12 facts válidos, 3 rechazados
│
├── 3. Verificar que los facts extraídos tienen tests
│       8 de 12 tienen test existente
│       4 facts requieren nuevo test → añadir a tasks.md
│
├── 4. Implementar el feature referenciando facts
│       El agente usa los 12 facts como constraints
│       El código generado tiene anotaciones @fact
│
└── 5. Deprecar las secciones de spec narrativa
        que han sido completamente atomizadas en facts
        (no borrar: marcar como "atomized: true" con
        referencia a los IDs de facts generados)
```

### Prompt de IA para extraer facts desde documentación o código legacy

```
## Prompt: Extracción de facts desde spec narrativa

Actúa como un analista de requisitos experto en FACTS-Driven Development.

### Input
Lee el siguiente documento de especificación:
[PEGAR SPEC NARRATIVA AQUÍ]

### Tarea
Extrae todos los facts atómicos que puedas identificar en el documento.
Para cada fact candidato:

1. Escribe el `statement` en una sola frase afirmativa y explícita.
2. Clasifícalo en una de estas categorías:
   behavior | state | restriction | contract | architecture | domain
3. Identifica el `scope` (módulo, endpoint o función si se menciona).
4. Indica el `origin` si el documento lo menciona
   (requisito, decisión, norma).
5. Propón el test de falsación: ¿qué verificaría que el fact es falso?

### Reglas de extracción
- Un fact = una sola verdad. Si dudas, separa.
- Si el texto es ambiguo, escribe el fact y añade una nota con la
  ambigüedad detectada para que el humano la resuelva.
- Si encuentras dos afirmaciones contradictorias en el documento,
  extrae ambas como facts separados y márcalos con
  ⚠️ POSIBLE CONTRADICCIÓN CON: [el otro fact].
- No inventes información que no esté en el texto.
  Si falta un detalle necesario (como un valor numérico),
  escribe el fact con [PENDIENTE: especificar valor].

### Output
Genera los facts en formato YAML siguiendo esta plantilla:
[PEGAR PLANTILLA DEL §5]

Al final, incluye:
- Número total de facts extraídos
- Número de ambigüedades detectadas que requieren aclaración humana
- Número de contradicciones detectadas
- Lista de información que falta en la spec y que impide formalizar
  ciertos facts correctamente
```

### Criterio para saber cuándo una spec está suficientemente atomizada

Una spec narrativa está suficientemente atomizada cuando:

1. **Cobertura de comportamientos:** cada comportamiento observable descrito en la spec tiene al menos un fact de tipo `behavior`.
2. **Cobertura de restricciones:** cada límite, umbral o prohibición tiene un fact de tipo `restriction` con valor numérico o binario explícito.
3. **Test por fact:** al menos el 80% de los facts tienen un test de falsación identificado.
4. **Sin ambigüedades sin resolver:** no quedan facts en estado `proposed` con nota de ambigüedad pendiente.
5. **Sin contradicciones activas:** el log `_contradictions.md` no tiene contradicciones sin resolución.

No es necesario atomizar el 100% de la spec narrativa para empezar a usar facts en implementación. El 80% de cobertura en el área de cambio es suficiente para obtener la mayor parte del beneficio.

### Errores frecuentes en la migración

**Error 1: Copiar frases de la spec como facts sin reformular**
La spec dice: "El sistema debe gestionar correctamente los errores de pago". Esto no es un fact: es una intención. Hay que extraer los comportamientos específicos de error.

**Error 2: Crear un fact por cada párrafo (en lugar de por cada verdad)**
Un párrafo puede contener 5 verdades. Migrar párrafos como unidad produce facts no atómicos.

**Error 3: Omitir los facts negativos (restricciones y prohibiciones)**
Las restricciones son tan importantes como los comportamientos. "No se permite X" es un fact tan válido como "cuando Y ocurre, el sistema hace Z".

**Error 4: No crear el test de falsación en el momento de crear el fact**
Si no se crea el test en el momento, se crea un fact sin evidencia. El fact existe pero no hay forma de saber si el sistema lo cumple.

**Error 5: No deprecar la spec narrativa tras atomizarla**
El resultado son dos fuentes de verdad: la spec narrativa y los facts. Cuando divergen, el equipo no sabe cuál seguir.

---

## 9. Facts y trazabilidad end-to-end

### El mapa completo de trazabilidad

```
CADENA DE TRAZABILIDAD FACTS-DRIVEN
─────────────────────────────────────────────────────────────────

ORIGEN                          FACT                     IMPLEMENTACIÓN
──────                          ────                     ──────────────

PSD2 Art.97          ──────►  FACT-PAY-003         ──────►  validateTransferAmount()
(NRM-PSD2-ART-97)    │         "Límite 10.000 EUR"  │         en payments-service
                     │                              │
                     │                              ├──────►  @fact FACT-PAY-003
                     │                              │         en el comentario
                     │                              │         del método
                     │                              │
                     │                              └──────►  TEST:
                     │                                        transfer-limits.test.ts
                     │                                        → "rejects > 10000 EUR"
                     │
                     └──────►  TASK-PAY-007 en tasks.md
                               "Implementar validación
                                de límite por operación"

EVIDENCIA FINAL:
CI pipeline green → test "rejects > 10000 EUR" pasa
= FACT-PAY-003 está implementado y verificado
= NRM-PSD2-ART-97 está cubierto en el sistema
```

### Cómo la matriz de trazabilidad cambia al usar facts

**Matriz de trazabilidad tradicional (SDD narrativo):**

| Requisito | Historia de usuario | Código | Test |
|---|---|---|---|
| REQ-SEC-001 | US-AUTH-001 (párrafo 3 de spec.md) | auth-service/ (no especificado qué función) | test/auth.test.ts (no especificado qué test) |

Problemas: la referencia al código es vaga, el test no es específico, si la función cambia de nombre la traza se rompe.

**Matriz de trazabilidad con FACTS:**

| Origen | Fact ID | Función | Test | Estado |
|---|---|---|---|---|
| NRM-PSD2-ART-97 | FACT-PAY-003 | `payments-service/validateTransferAmount()` | `transfer-limits.test.ts:L45` | ✅ Verified |
| DEC-SEC-2025-03 | FACT-AUTH-002 | `auth-service/issueSessionToken()` | `auth/session-expiry.test.ts:L23` | ✅ Verified |
| REQ-SEC-007 | FACT-AUTH-004 | `auth-service/checkLoginAttempts()` | `auth/brute-force.test.ts:L67` | ✅ Verified |

La traza es exacta hasta el número de línea. Regenerable automáticamente buscando anotaciones `@fact` en el código.

### Ventajas para auditoría y cumplimiento normativo

En sectores regulados (banca, salud, aeroespacial), los auditores requieren evidencia de que cada norma tiene implementación y cobertura de test. Con FACTS:

- La norma está en el campo `origin.ref` del fact
- La implementación está en `scope.function` + código con `@fact`
- La evidencia está en `falsification.test` + resultado del CI pipeline

Un informe de cumplimiento puede generarse automáticamente desde el repositorio de facts: todos los facts con `origin.type: regulation`, sus tests asociados y el estado del CI.

### Ejemplo de traza completa para FACT-PAY-003

```
TRAZA: FACT-PAY-003

NIVEL 1 — NORMA
  PSD2 Art. 97: "Las entidades de crédito aplicarán autenticación
  reforzada del cliente cuando el importe supere los umbrales
  establecidos..."
  → Decisión interna: umbral = 10.000 EUR (POL-RISK-2025-09)

NIVEL 2 — FACT
  FACT-PAY-003 (active, v2.0)
  "El importe máximo de una transferencia nacional sin autorización
  adicional es 10.000,00 EUR por operación. Operaciones que superen
  este importe son rechazadas con HTTP 422 y código TRANSFER_LIMIT_EXCEEDED"

NIVEL 3 — TAREA
  TASK-PAY-007 en specs/features/payments/tasks.md
  "Implementar validación de límite por operación en
   validateTransferAmount(). Criterio de done: rechaza importes
   > 10000 con HTTP 422 + TRANSFER_LIMIT_EXCEEDED"

NIVEL 4 — CÓDIGO
  payments-service/src/validators/transfer.validator.ts:L34
  /**
   * @fact FACT-PAY-003 - Límite 10.000 EUR sin autenticación adicional
   * @fact FACT-PAY-004 - Límite diferente para transferencias internacionales
   */
  function validateTransferAmount(amount: number, type: TransferType): void {
    const limit = type === 'national' ? 10000 : 5000; // FACT-PAY-003 / FACT-PAY-004
    if (amount > limit) {
      throw new TransferLimitError('TRANSFER_LIMIT_EXCEEDED', amount, limit);
    }
  }

NIVEL 5 — TEST
  tests/payments/transfer-limits.test.ts:L45
  test('rejects national transfer over 10000 EUR with 422', async () => {
    const res = await post('/payments/transfer/national', { amount: 10001 });
    expect(res.status).toBe(422);
    expect(res.body.code).toBe('TRANSFER_LIMIT_EXCEEDED');
  }); // @fact FACT-PAY-003

NIVEL 6 — EVIDENCIA
  CI pipeline: payments-service → compliance-check suite → PASS
  Última ejecución: 2026-06-05 08:23 UTC
  → FACT-PAY-003 verificado en producción
```

---

## 10. Herramientas y ecosistema compatible con FACTS

> **Nota importante:** FACTS-Driven Development como metodología nombrada es un concepto emergente (2026). No existe aún una herramienta dedicada y específica llamada "FACTS framework". Las herramientas descritas a continuación son las del ecosistema SDD actual, adaptadas para trabajar con facts atómicos. Se indica explícitamente cuándo la integración es nativa y cuándo requiere configuración manual.

### Herramientas SDD actuales adaptadas a facts

**GitHub Spec Kit** (+90k estrellas, open source)
Diseñado para las cuatro fases de SDD. Adaptable a FACTS añadiendo una carpeta `facts/` al repositorio y configurando las plantillas de constitución para que generen YAML de facts en lugar de prosa. No tiene soporte nativo para validación de facts, pero el CLI acepta cualquier estructura de directorio.

*Integración con facts:* manual. Crear plantillas de facts en `.specify/templates/` y configurar el agente para cargarlas automáticamente.

**AWS Kiro**
Su sistema de `steering files` (archivos de contexto persistente que Kiro inyecta en cada sesión del agente) es directamente compatible con facts. Cada fact YAML puede ser un steering file, o se puede crear un steering file que cargue todos los facts del módulo activo.

*Integración con facts:* nativa para carga de contexto; no tiene validación de contradicciones integrada.

**Claude Code**
A través de skills (slash commands), se puede empaquetar el flujo completo de FACTS: carga de facts relevantes al scope, detección de contradicciones, generación de código con anotaciones `@fact`, y propuesta de nuevos facts cuando el agente encuentra comportamiento no documentado.

*Integración con facts:* via skill personalizada (ver §12 para el prompt maestro).

**Cursor (Plan Mode)**
El modo de planificación de Cursor puede configurarse para leer facts del directorio `facts/` antes de generar código. La integración requiere un archivo `.cursorrules` que instruya al agente a cargar facts relevantes.

### Formatos de almacenamiento y query de facts a escala

Cuando el repositorio de facts supera los 200-300 facts, la búsqueda por tag, scope o categoría en archivos YAML individuales se vuelve lenta. Las opciones escalables son:

**Base de datos documental (SQLite + JSON)**
Solución ligera, funciona sin infraestructura externa. Los facts YAML se sincronizan a SQLite en el CI. Permite queries como "todos los facts del módulo auth con status active".

**Grafo de conocimiento**
Para proyectos con muchas interdependencias entre facts (`related-facts`), un grafo (Neo4j, o un grafo en memoria con `graphlib`) permite navegar relaciones: "todos los facts que dependen de FACT-ARCH-004" o "detectar ciclos de dependencia entre facts".

**Embeddings + búsqueda semántica (RAG)**
Cuando hay cientos de facts, el agente no puede cargarlos todos en contexto. Generando embeddings de los `statement` de cada fact, el agente puede recuperar los 10-20 facts más relevantes para el scope de la tarea actual. Implementable con cualquier sistema RAG estándar (LlamaIndex, embeddings de OpenAI/Anthropic + vector store).

### Integración con MCP servers

Los MCP (Model Context Protocol) servers permiten que el agente acceda a datos externos en tiempo real. Un MCP server de facts permitiría:

- `facts.list(module, status)` → listar facts activos de un módulo
- `facts.get(id)` → obtener un fact específico
- `facts.check_contradictions(ids[])` → verificar contradicciones entre un conjunto de facts
- `facts.propose(fact_yaml)` → proponer un nuevo fact para revisión humana

Esto no requiere construir un MCP server desde cero: el MCP server de filesystem estándar, combinado con el directorio `facts/` en el repositorio, ya ofrece las tres primeras capacidades. La cuarta (proponer facts) requiere un script de CI o un MCP server personalizado mínimo.

---

## 11. Checklist de calidad de un fact

Usar este checklist antes de aprobar un fact y moverlo de `proposed` a `active`.

### ✅ Atomicidad
- [ ] El fact expresa una sola verdad (no puedo usar "y" para separar dos verdades independientes)
- [ ] Si lo divido en dos, cada parte sigue siendo un fact útil y completo por sí mismo
- [ ] No mezcla comportamiento con restricción ni con arquitectura en la misma afirmación

### ✅ Claridad y ausencia de ambigüedad
- [ ] No contiene palabras subjetivas: "rápidamente", "seguro", "apropiado", "suficiente", "en la mayoría de casos"
- [ ] Si menciona valores numéricos, están expresados con unidades y precisión exacta
- [ ] Si menciona condiciones, están completamente especificadas (¿cuándo? ¿bajo qué estado? ¿para qué plataforma?)
- [ ] Dos personas del equipo que lean el statement llegan a la misma conclusión sobre qué verificar

### ✅ Falsabilidad
- [ ] Existe al menos un escenario concreto que demostraría que el fact es falso
- [ ] El campo `falsification.test` apunta a un test existente o hay una tarea creada para escribirlo
- [ ] El test es automatizable (no requiere inspección manual)

### ✅ Trazabilidad
- [ ] El campo `id` es único en todo el repositorio de facts
- [ ] El campo `origin.ref` apunta a un requisito, decisión, norma o incidente real y localizable
- [ ] El campo `scope` identifica al menos el módulo al que aplica
- [ ] Si reemplaza un fact anterior, el campo `deprecates` está relleno y el fact anterior tiene `deprecated-by` con este ID

### ✅ Vigencia
- [ ] El campo `status` refleja la realidad actual del fact
- [ ] Si el fact tiene menos de 7 días, está en `proposed` y ha pasado por revisión de par
- [ ] Si hay alguna duda sobre si sigue siendo verdad, está en `in-review`, no en `active`

### ✅ Integridad con el repositorio
- [ ] Se ha verificado que no existe ya un fact con el mismo `subject` y `property`
- [ ] Si hay facts `related-facts`, se ha verificado que no contradicen este fact
- [ ] El fact ha sido añadido al `_index.yaml` con su módulo y estado

---

## 12. Prompt maestro para trabajar con FACTS

El siguiente prompt está diseñado para ser reutilizable como skill de Claude Code, steering file de Kiro, o `.cursorrules` de Cursor. Permite que el agente opere sobre un conjunto de facts de forma disciplinada.

```markdown
# SKILL: FACTS-Driven Development Agent

## Contexto del proyecto
Antes de cualquier acción, lee estos archivos en este orden:
1. facts/_index.yaml              (mapa de todos los facts)
2. facts/architecture/            (todos los facts de arquitectura)
3. facts/domain/                  (todos los facts de dominio)
4. facts/modules/[modulo-activo]/ (facts del módulo en el que trabajas)
5. specs/TECH_STACK.md            (stack tecnológico fijo)

Solo carga facts con status: active.
Ignora facts con status: deprecated.
Si encuentras facts con status: in-review, alerta al humano
antes de continuar: "⚠️ Hay facts en revisión que afectan a
esta tarea. Confirma antes de proceder."

## Tu comportamiento como agente

### ANTES de generar código
1. Lista los facts relevantes para la tarea solicitada.
2. Verifica contradicciones:
   - ¿Algún par de facts tiene el mismo subject/property pero
     distinto valor? → DETENTE y reporta la contradicción.
   - ¿Algún fact hace imposible lo que describe otro? → DETENTE
     y reporta con explicación.
3. Si detectas comportamiento que debería estar documentado como
   fact y no lo está, propón el fact antes de implementar:
   "📋 FACT PROPUESTO: [statement]. ¿Apruebas añadirlo antes
   de continuar?"

### DURANTE la generación de código
- Cada función, método o clase que implemente un fact debe
  incluir una anotación en su docblock:
  `@fact FACT-ID — descripción breve del fact`
- Si una función implementa múltiples facts, lista todos.
- Si no puedes satisfacer un fact con la implementación actual,
  reporta: "⛔ No puedo satisfacer FACT-ID con la arquitectura
  actual. Razón: [explicación]. ¿Cómo quieres proceder?"

### DESPUÉS de generar código
- Lista los facts cubiertos en esta implementación.
- Lista los tests necesarios para falsear cada fact cubierto.
- Si algún fact no tiene test, crea una tarea pendiente:
  "📌 Falta test para FACT-ID: [descripción del test necesario]"
- Si el código que has generado implica que un fact existente
  debería actualizarse (por ejemplo, un valor ha cambiado),
  alerta: "🔄 El código generado parece contradecir FACT-ID.
  ¿Debo proponer una nueva versión del fact?"

## Comandos disponibles

/facts list [modulo] [categoria]
  → Lista todos los facts activos del módulo y/o categoría indicados

/facts check [id1] [id2] ...
  → Verifica contradicciones entre los facts indicados

/facts propose [statement]
  → Formaliza un fact candidato con la plantilla completa y
    lo presenta al humano para aprobación

/facts trace [id]
  → Muestra la traza completa: origen → fact → código (@fact) → test

/facts coverage [modulo]
  → Para cada comportamiento identificado en el módulo, indica
    si existe un fact que lo cubra o si hay comportamiento
    no documentado

## Reglas absolutas
1. NUNCA generes código que contradiga un fact con status: active
   sin aprobación humana explícita.
2. NUNCA omitas la anotación @fact en código que implementa un fact.
3. NUNCA uses facts con status: deprecated como guía de implementación.
4. SIEMPRE detente y reporta antes de proceder si detectas una
   contradicción entre facts.
5. Si no tienes los facts necesarios para completar la tarea,
   di qué facts faltan en lugar de asumir comportamiento.
```

---

## 13. Ventajas, riesgos y limitaciones de FACTS

### Ventajas frente a SDD narrativo

| Dimensión | SDD narrativo | FACTS-Driven |
|---|---|---|
| **Consumo por agente** | El agente parsea prosa; el resultado varía | El agente carga facts estructurados; el resultado es consistente |
| **Detección de contradicciones** | Manual; requiere lectura completa de la spec | Automática: dos facts con mismo subject/property y distinto value = conflicto |
| **Actualización** | Editar texto en prosa; riesgo de dejar texto viejo | Deprecar el fact anterior; crear versión nueva; el cambio es atómico |
| **Trazabilidad código-requisito** | Referencia vaga al documento | Referencia exacta vía `@fact ID` en el código |
| **Generación de informes de cumplimiento** | Manual; muy costoso | Automática desde el repositorio de facts |
| **Onboarding de nuevos miembros** | Leer documentación extensa | Leer facts del módulo en el que van a trabajar |
| **Independencia de modelo de IA** | Alta si la spec es clara; moderada si es ambigua | Muy alta: los facts son el contrato; el modelo es el ejecutor |

### Riesgos de over-atomización (granularidad excesiva)

El mayor riesgo de FACTS no es la complejidad de mantenerlos: es crear facts tan granulares que el repositorio se vuelva inmanejable.

**Señales de over-atomización:**

- Facts que documentan detalles de implementación que pueden cambiar sin impacto en el comportamiento observable (por ejemplo, el nombre de una variable interna).
- Más de 50 facts por módulo de complejidad media.
- Facts que solo tienen sentido si se leen junto a otros 3-4 facts (falta de atomicidad real: son un conjunto que debería estar agrupado).
- El equipo tarda más en mantener facts que en escribir código.

**Regla práctica:** un fact debe documentar una verdad que, si cambia, requiere que alguien tome una decisión consciente. Si el cambio es trivial y no requiere decisión, probablemente no merece un fact.

### Cuándo FACTS no es la herramienta correcta

**Proyectos de exploración y prototipado**
Si el objetivo es descubrir si algo es posible o deseable, no si es correcto y mantenible, la overhead de formalizar facts ralentiza sin aportar valor. Usa vibe coding para explorar, SDD para validar, y solo migra a FACTS cuando el módulo está estabilizado.

**Sistemas con requisitos extremadamente volátiles**
Si los requisitos de negocio cambian varias veces por semana, el coste de mantener facts actualizados puede superar el beneficio. En estos casos, SDD narrativo con specs cortas y checkpoints frecuentes es más ágil.

**Equipos muy pequeños con contexto compartido total**
Un equipo de dos personas que trabajan juntas todos los días y tienen el contexto completo del sistema en sus cabezas puede operar eficientemente con SDD narrativo. La overhead de FACTS se justifica cuando el conocimiento del sistema necesita ser explícito porque no cabe en la memoria del equipo.

**Features de un solo uso o scripts de migración**
Código que se escribe, se ejecuta una vez y se descarta no necesita facts. FACTS es para conocimiento que debe sobrevivir al código.

---

## 14. Conclusión: el repositorio de facts como activo estratégico

### Por qué los facts acumulados son el activo más duradero del proyecto

El código de un sistema tiene una vida media de 3-5 años antes de ser reemplazado, refactorizado o migrado. Las decisiones que llevaron a ese código —los requisitos, las restricciones, los compromisos con el negocio y la regulación— duran décadas.

Un repositorio de facts bien mantenido captura exactamente esa capa: no cómo está construido el sistema hoy, sino qué verdades del negocio, qué compromisos regulatorios y qué decisiones técnicas rigen su comportamiento. Esa información tiene valor independiente del código que la implementa.

Cuando el equipo decide migrar de una arquitectura monolítica a microservicios, los facts de comportamiento y restricción no cambian: solo cambia cómo se implementan. La migración se convierte en un ejercicio de regeneración: tomar los facts existentes, escribir nuevos facts de arquitectura para la nueva estructura, y dejar que el agente genere la nueva implementación.

### La independencia de modelo que otorga un repositorio de facts maduro

En 2026, los modelos de IA relevantes se reemplazan cada 12-18 meses. Los equipos que trabajan con prompting ad-hoc o con specs narrativas están atados a los defaults del modelo que usaban cuando escribieron esas specs: si cambian de modelo, los defaults cambian con él.

Un repositorio de facts es agnóstico al modelo. Los facts son el contrato; el modelo es el ejecutor. Un equipo con 400 facts activos bien formados puede cambiar de Claude a GPT a Gemini y obtener implementaciones equivalentes porque los constraints son explícitos e independientes del modelo.

Más importante aún: cuando aparece un modelo con capacidades significativamente superiores, el equipo con facts puede regenerar módulos completos contra el nuevo modelo de inmediato. El repositorio de facts es el leverage que hace que cada nueva generación de IA sea un multiplicador de productividad, no un reset.

### La frase que resume FACTS-Driven Development

> *"En SDD, la spec es el prompt. En FACTS-Driven Development, cada fact es una constraint. La suma de constraints es el contrato. El contrato es lo que sobrevive al código, al modelo y al equipo."*

---

```
LÍNEA DE EVOLUCIÓN COMPLETA

Vibe Coding          SDD Narrativo         FACTS-Driven
─────────────        ─────────────         ────────────
"Añade login"   →    spec.md con       →   12 facts atómicos,
                     historias y           cada uno con ID,
                     criterios EARS        test de falsación
                                           y estado de vigencia

El output           El output es           El output es
depende del         predecible pero        determinista:
mood del modelo     puede ser ambiguo      los constraints
                    si la spec crece       son explícitos

El conocimiento     El conocimiento        El conocimiento
vive en el chat     vive en documentos     vive en el
                    en prosa               repositorio de
                                           facts, navegable,
                                           queryable y
                                           auditable
```

---

*Documento elaborado en junio de 2026. FACTS-Driven Development es un concepto emergente; las herramientas específicas para este flujo seguirán madurando. Las bases metodológicas descritas en esta guía son aplicables hoy con las herramientas actuales del ecosistema SDD.*
