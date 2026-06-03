# Análisis Funcional de Migraciones — Equivalencia con Sistema Legado

> Complemento al Modelo Operativo AI-Ready  
> Integra los puntos 1–12 del modelo base con las particularidades de proyectos de migración

---

## Por qué las migraciones son un caso especial

En un proyecto de funcionalidad nueva, el requisito describe algo que aún no existe. El analista parte de una conversación con el negocio y construye la definición desde cero.

En una migración, el requisito describe la relación entre lo que ya existe y lo que debe existir. El sistema legado es a la vez la fuente de verdad y el primer obstáculo: documenta el comportamiento real del negocio con una precisión que ningún workshop puede igualar, pero lo hace en un lenguaje que nadie ha leído en años.

Esto cambia tres cosas estructurales del modelo operativo:

**La captura de requisitos tiene dos fuentes simultáneas.** El usuario de negocio describe qué debería hacer el nuevo sistema. El sistema legado describe qué hace realmente hoy. Estas dos fuentes no siempre coinciden: hay comportamientos del legado que el negocio olvidó que existen, hay comportamientos que el negocio describe de forma diferente a como están implementados, y hay comportamientos que el negocio quiere cambiar aprovechando la migración.

**La ambigüedad funcional tiene una dimensión adicional.** Además de los criterios de aceptación verificables del modelo base, cada requisito de migración debe resolver explícitamente si el comportamiento del sistema nuevo debe ser idéntico al legado, equivalente pero mejorado, o deliberadamente diferente. Esta decisión, que en un proyecto nuevo no existe, es la fuente más frecuente de conflictos durante el desarrollo y las pruebas de aceptación.

**La trazabilidad necesita una dimensión adicional.** La matriz del punto 9 del modelo base traza `REQ → US → TC → Jira`. En migraciones esta traza tiene que incluir la referencia al comportamiento del sistema legado: `LEGADO-REF → REQ → US → TC → Jira`. Sin esa referencia, es imposible saber si un test case que falla indica un bug en la implementación nueva o un comportamiento que se decidió conscientemente no replicar.

---

## Ampliación de la plantilla YAML para migraciones

La plantilla del punto 1 del modelo base se extiende con un bloque específico de migración. La regla de diseño del punto 1 se mantiene: los bloques nuevos van al final, en el Bloque 5 (metadatos técnicos), para no alterar la estructura que los prompts de generación ya conocen.

```yaml
# BLOQUE DE MIGRACIÓN
# Solo presente en requisitos de tipo migración.
# Se omite completamente en requisitos de nueva funcionalidad.
migracion:

  # ── Referencia al sistema legado ──────────────────────────────
  sistema_origen:
    nombre: ""           # Nombre comercial o interno del sistema. Ej: "SAP R/3", "Oracle EBS", "aplicación inhouse FACT-98"
    modulo: ""           # Módulo o subsistema específico. Ej: "Módulo de facturación", "Batch FACT_MONTHLY"
    tecnologia: ""       # Stack técnico relevante para el análisis. Ej: "COBOL/DB2", "Oracle Forms 6i", "VB6/SQL Server 2008"
    version: ""          # Versión exacta si se conoce
    responsable_conocimiento: ""  # Quién en la organización conoce este sistema en profundidad
    documentacion_disponible:     # Qué hay documentado del legado
      - tipo: ""         # Valores posibles: manual_usuario, especificacion_tecnica, codigo_fuente, diagrama_bd, ninguna
        ubicacion: ""    # Ruta, URL o descripción de dónde está

  # ── Comportamiento actual en el legado ────────────────────────
  # Esta sección es el corazón del requisito de migración.
  # Documenta qué hace exactamente el sistema legado hoy,
  # con la misma precisión que los criterios de aceptación del nuevo sistema.
  comportamiento_actual:

    descripcion: >
      # Narrativa del comportamiento actual en lenguaje de negocio.
      # No tecnicismos de implementación del legado.
      # Mínimo 50 palabras.

    flujo_actual:
      - paso: 1
        actor: ""        # Quién o qué sistema ejecuta este paso en el legado
        accion: ""       # Qué hace exactamente
        resultado: ""    # Qué produce o qué cambia

    reglas_actuales:
      - id: RA-000-01    # Formato: RA-[REQ_ID]-NN. "RA" = Regla Actual
        descripcion: ""  # Regla de negocio tal como funciona HOY en el legado
        origen: ""       # Cómo se descubrió: código_fuente, entrevista, prueba_exploratoria, documento

    datos_actuales:
      - campo: ""
        tipo_en_legado: ""      # Tipo físico en el sistema origen (VARCHAR(50), NUMBER(15,2), DATE...)
        tipo_en_nuevo: ""       # Tipo en el sistema destino
        transformacion: ""      # Lógica de conversión si aplica. Ej: "dividir entre 100 (el legado guarda céntimos)"
        valores_nulos: ""       # Cómo gestiona el legado los nulos. Frecuente fuente de bugs de migración.
        valores_especiales: []  # Valores con significado especial en el legado. Ej: "999999 = sin límite"

    volumetria:
      registros_actuales: null  # Número aproximado de registros en el sistema origen
      crecimiento_anual: ""     # Ej: "15% anual"
      pico_uso: ""              # Cuándo se usa más. Ej: "últimos 5 días de cada mes"
      tiempo_respuesta_actual: ""  # Rendimiento real del legado como referencia

  # ── Decisión de equivalencia ──────────────────────────────────
  # Este es el campo más importante y más frecuentemente omitido.
  # Cada comportamiento del legado necesita una decisión explícita.
  # La ausencia de esta decisión es la causa raíz del 60% de los
  # conflictos en pruebas de aceptación de migraciones.

  equivalencia:
    decision_global: ""
    # Valores permitidos (vocabulario controlado):
    #   identico      → el nuevo sistema debe comportarse exactamente igual que el legado
    #   equivalente   → mismo resultado de negocio, puede diferir en implementación o UX
    #   mejorado      → misma funcionalidad con cambios deliberados acordados con negocio
    #   reemplazado   → el comportamiento del legado se abandona y se sustituye por uno nuevo
    #   eliminado     → la funcionalidad no se migra al nuevo sistema

    justificacion: >
      # Por qué se tomó esta decisión. Quién la aprobó y cuándo.

    diferencias_deliberadas:
      # Lista de aspectos donde el nuevo sistema se comporta
      # de forma conscientemente diferente al legado.
      # Si está vacía, el equipo asume que todo debe ser idéntico.
      - aspecto: ""
        comportamiento_legado: ""
        comportamiento_nuevo: ""
        aprobado_por: ""
        fecha_aprobacion: ""
        referencia: ""          # Acta, email, ticket donde se documentó la decisión

    comportamientos_no_migrar:
      # Funcionalidades del legado que se descartan explícitamente.
      # Sin esta lista, el equipo puede intentar migrar algo que negocio
      # ya decidió eliminar.
      - funcionalidad: ""
        motivo_exclusion: ""
        aprobado_por: ""

  # ── Criterios de aceptación de equivalencia ───────────────────
  # Complementan los criterios de aceptación estándar del Bloque 3.
  # Verifican específicamente que la equivalencia funcional se cumple.
  criterios_equivalencia:
    - id: CE-000-01      # Formato: CE-[REQ_ID]-NN. "CE" = Criterio de Equivalencia
      aspecto: ""        # Qué comportamiento del legado se está verificando
      dado_legado: ""    # Estado en el sistema legado
      cuando_legado: ""  # Acción en el sistema legado
      resultado_legado: "" # Qué produce el legado (medido, no estimado)
      resultado_esperado_nuevo: ""  # Qué debe producir el nuevo sistema
      tipo_equivalencia: ""
      # Valores: identico │ equivalente │ mejorado
      dato_contraste: {}  # Dataset concreto usado para contrastar ambos sistemas

  # ── Estrategia de pruebas de regresión ────────────────────────
  pruebas_regresion:
    estrategia: ""
    # Valores: paralelo │ shadow │ comparacion_batch │ muestreo
    # paralelo:          ambos sistemas en producción, mismos inputs, comparar outputs
    # shadow:            el nuevo sistema corre en paralelo sin servir respuestas reales
    # comparacion_batch: comparar resultados de proceso batch entre ambos sistemas
    # muestreo:          subset representativo de transacciones reales para contraste

    periodo_coexistencia: ""  # Cuánto tiempo corren ambos sistemas en paralelo
    criterio_cutover: ""      # Qué condición debe cumplirse para apagar el legado
    plan_rollback: ""         # Qué pasa si el cutover falla

  # ── Gestión de datos históricos ───────────────────────────────
  datos_historicos:
    migrar_historico: true    # Si se migran datos históricos o solo los activos
    fecha_corte: ""           # Hasta qué fecha se migran datos históricos
    transformacion_historico: ""  # Lógica especial para datos históricos vs datos nuevos
    validacion_historico: ""  # Cómo se verifica que los datos históricos se migraron correctamente
```

---

## Extensión del glosario para proyectos de migración

El glosario del punto 2 del modelo base necesita tres secciones adicionales en proyectos de migración.

### Sección de mapeo de términos legado → nuevo sistema

El sistema legado tiene su propio vocabulario. Es frecuente que el mismo concepto tenga nombres distintos en el legado y en el nuevo sistema, o que el legado use términos técnicos de su época que el negocio ya no reconoce.

```yaml
mapeo_terminologico:
  - termino_legado: ""       # Cómo se llama en el sistema legado (campo, pantalla, proceso)
    termino_nuevo: ""         # Cómo se llama en el nuevo sistema (término oficial del glosario)
    equivalencia: ""          # identico │ renombrado │ refactorizado │ eliminado │ nuevo_sin_equivalente
    notas: ""                 # Contexto que el analista necesita para no confundirlos
    ejemplo_legado: ""        # Un ejemplo concreto del uso en el legado
    ejemplo_nuevo: ""         # El equivalente en el nuevo sistema

# Ejemplo concreto:
#   termino_legado: "CLAVE_CLIE"
#   termino_nuevo: "id_cliente"
#   equivalencia: renombrado
#   notas: >
#     En el legado CLAVE_CLIE es un VARCHAR(8) con formato AAAANNNN
#     (4 letras + 4 números). En el nuevo sistema es un UUID.
#     La tabla de equivalencias se genera durante la migración de datos.
#   ejemplo_legado: "ABCD1234"
#   ejemplo_nuevo: "550e8400-e29b-41d4-a716-446655440000"
```

### Sección de entidades de transición

Durante la migración coexisten entidades del legado y del nuevo sistema que representan el mismo concepto de negocio pero tienen estructuras diferentes. Es necesario documentarlas explícitamente para que el pipeline genere criterios de aceptación que las distingan.

```yaml
entidades_transicion:
  - id: ET-001
    nombre: ""               # Nombre de la entidad durante la transición
    entidad_legado: ""       # Nombre en el sistema legado
    entidad_nueva: ""        # Nombre en el nuevo sistema (debe coincidir con el glosario base)
    periodo_coexistencia: "" # Durante qué fase del proyecto existen ambas
    fuente_verdad: ""        # legado │ nuevo │ ambos (indica cuál prevalece en caso de conflicto)
    regla_sincronizacion: "" # Cómo se mantienen sincronizadas mientras coexisten
```

### Sección de estados de migración

Durante el proceso de migración, las entidades pasan por estados propios que no existen ni en el legado ni en el nuevo sistema definitivo. Documentarlos en el glosario evita ambigüedad en los criterios de aceptación.

```yaml
estados_migracion:
  - entidad: ""
    estados_especificos:
      - nombre: ""
        descripcion: ""        # Qué significa este estado durante la migración
        es_temporal: true      # Si desaparece una vez completada la migración
        transiciones: []       # A qué otros estados puede pasar
```

---

## Adaptación del Event Storming para migraciones

El taller del punto 3 del modelo base funciona igual en migraciones con tres diferencias en la facilitación.

### Antes del taller: sesión de exploración del legado (2–4 horas)

Antes del Event Storming con el negocio, el analista hace una sesión técnica con la persona que mejor conoce el sistema legado. El objetivo es entender qué hace realmente el sistema, no qué debería hacer según la documentación oficial, que frecuentemente está desactualizada.

El resultado de esta sesión son post-its de un color especial (se recomienda el color gris) que representan **comportamientos observados del legado**. Estos post-its se colocan debajo de la línea de tiempo del Event Storming como evidencia del comportamiento actual, en paralelo con los eventos que describen el comportamiento esperado del nuevo sistema.

Las preguntas que guían esta sesión son diferentes a las del Event Storming estándar:

```
¿Qué hace el sistema cuando ocurre esto?
¿Por qué lo hace así? ¿Es una regla de negocio o una limitación técnica?
¿Hay casos donde el sistema se comporta de forma diferente a lo esperado?
¿Qué pasa con los registros históricos cuando se ejecuta esta operación?
¿Existe algún proceso batch relacionado que el equipo de negocio no vea?
¿Cuándo fue la última vez que alguien modificó esta parte del sistema?
```

### Durante el taller: dos carriles en la línea de tiempo

El lienzo del Event Storming de migración tiene dos carriles horizontales:

- **Carril superior**: comportamiento del nuevo sistema (eventos naranjas estándar)
- **Carril inferior**: comportamiento actual del legado (eventos en gris)

Los post-its que conectan ambos carriles representan las **decisiones de equivalencia**: qué ocurre en el nuevo sistema cuando se produce el mismo evento en el legado.

La conversación más valiosa del taller emerge cuando negocio y técnicos discuten si el carril inferior y el carril superior deben ser idénticos o diferentes. Esa discusión, capturada con post-its rojos de pregunta abierta, es la materia prima de la sección `equivalencia` de la plantilla YAML.

### Post-its adicionales específicos de migración

Además del código de colores estándar del punto 3, se añaden dos tipos:

| Color | Elemento | Pregunta que responde |
|---|---|---|
| Gris | Comportamiento legado | ¿Qué hace el sistema actual cuando ocurre esto? |
| Amarillo oscuro | Decisión de equivalencia | ¿El nuevo sistema debe hacer lo mismo, algo equivalente o algo diferente? |

---

## Extensión de los prompts para migraciones

Los prompts del punto 4 del modelo base se extienden con un modificador específico para requisitos de migración. Se añade como bloque adicional al Prompt 2 (generación de historia de usuario), antes del campo JSON de salida.

### Modificador de migración para el Prompt 2

```
CONTEXTO ADICIONAL — REQUISITO DE MIGRACIÓN:

Este requisito describe la migración de funcionalidad desde un sistema legado.
El análisis debe considerar el comportamiento actual del sistema origen.

COMPORTAMIENTO ACTUAL DEL LEGADO:
{{migracion.comportamiento_actual.descripcion}}

FLUJO ACTUAL EN EL LEGADO:
{{migracion.comportamiento_actual.flujo_actual}}

REGLAS ACTUALES DEL LEGADO:
{{migracion.comportamiento_actual.reglas_actuales}}

DECISIÓN DE EQUIVALENCIA:
{{migracion.equivalencia.decision_global}}
Justificación: {{migracion.equivalencia.justificacion}}

DIFERENCIAS DELIBERADAS CON EL LEGADO:
{{migracion.equivalencia.diferencias_deliberadas}}

INSTRUCCIONES ADICIONALES PARA LA GENERACIÓN:

1. La historia de usuario debe incluir una sección específica
   "Comportamiento en el sistema actual" que describa el punto de partida.

2. Por cada criterio de aceptación estándar, añadir un criterio de equivalencia
   (tipo CE) que verifique explícitamente la relación con el comportamiento del legado.

3. Si la decisión de equivalencia es "identico", los criterios de equivalencia deben
   usar datos concretos extraídos del legado para el contraste.

4. Si la decisión es "mejorado" o "reemplazado", los criterios de equivalencia deben
   documentar explícitamente qué comportamiento del legado NO se replica y por qué.

5. La sección "flujos_error" debe incluir específicamente el comportamiento ante
   datos migrados que no cumplan las validaciones del nuevo sistema
   (registros legacy con formatos incompatibles, valores nulos inesperados, etc.).

6. Las tareas técnicas deben incluir obligatoriamente:
   - Una tarea de tipo "migracion_datos" con la lógica de transformación
   - Una tarea de tipo "validacion_migracion" con los criterios de verificación del dataset
   - Una tarea de tipo "coexistencia" si los sistemas operan en paralelo

7. La estimación de story points debe considerar la incertidumbre del legado:
   si el campo "documentacion_disponible" indica "ninguna" o solo "codigo_fuente",
   incrementar la estimación base en al menos 3 puntos.
```

### Modificador para el Prompt de test cases (punto 5)

```
CONTEXTO ADICIONAL — TEST CASES DE MIGRACIÓN:

Además de los test cases estándar (positivos, negativos, contorno),
genera los siguientes tipos específicos de migración:

TIPO: comparacion_legado
Para cada criterio de equivalencia de tipo "identico":
  - Dado: el mismo input se procesa en el legado y en el nuevo sistema
  - Cuando: se ejecuta la misma operación en ambos
  - Entonces: el resultado del nuevo sistema es idéntico al del legado
  Incluir los datos_contraste concretos del requisito.

TIPO: regresion_dato_migrado
Para cada campo con transformacion en datos_actuales:
  - Probar con el valor original del legado (antes de transformación)
  - Probar con el valor transformado (después de transformación)
  - Probar con valores especiales del legado (valores_especiales del YAML)
  - Probar con valores nulos según el comportamiento del legado

TIPO: coexistencia
Si la estrategia de pruebas es "paralelo" o "shadow":
  - Verificar que las transacciones ejecutadas en el nuevo sistema
    son visibles en el legado durante el período de coexistencia
  - Verificar que las transacciones del legado son visibles en el nuevo sistema
  - Verificar el comportamiento ante conflictos de sincronización

TIPO: cutover
Verificar el estado del sistema en el momento del corte:
  - Transacciones en curso en el legado en el momento del cutover
  - Datos migrados pero no validados
  - Referencias cruzadas entre registros del legado y del nuevo sistema

Para cada test case de tipo comparacion_legado,
incluir el campo adicional:
  "resultado_legado_verificado": "[valor real obtenido del legado durante la preparación del test]"
```

---

## Validación automática para migraciones

El validador del punto 6 del modelo base incorpora un bloque adicional específico para los requisitos de migración. Se añade como una quinta llamada al pipeline de validación, después de la validación de completitud funcional.

### Prompt 5 — Validación específica de migración

```
Analiza si el siguiente requisito de migración tiene la información mínima
necesaria para garantizar que el nuevo sistema es funcionalmente equivalente
al legado sin ambigüedades.

REQUISITO A VALIDAR:
{{requisito_yaml}}

ANÁLISIS DE COMPLETITUD DE MIGRACIÓN:

BLOQUE A — Información del sistema legado
  ¿Está documentado el sistema de origen con suficiente precisión?
  ¿Existe al menos una persona identificada como responsable del conocimiento del legado?
  ¿Se conoce qué documentación existe sobre el comportamiento actual?

BLOQUE B — Comportamiento actual documentado
  ¿Está el flujo actual descrito paso a paso?
  ¿Las reglas actuales tienen evidencia de origen (código, entrevista, documento)?
  ¿Los campos con transformación tienen la lógica de conversión explícita?
  ¿Se documentaron los valores especiales y nulos del legado?

BLOQUE C — Decisión de equivalencia
  ¿Se tomó una decisión explícita sobre el tipo de equivalencia?
  ¿Las diferencias deliberadas con el legado están aprobadas por negocio con fecha?
  ¿Está documentado qué funcionalidades del legado NO se migran?

BLOQUE D — Criterios de equivalencia verificables
  ¿Existe al menos un criterio CE por cada regla actual documentada?
  ¿Los criterios CE tienen datos_contraste concretos?
  ¿Están documentados los criterios de aceptación para datos migrados incorrectos?

BLOQUE E — Estrategia de validación
  ¿Está definida la estrategia de pruebas de regresión?
  ¿Hay un criterio de cutover documentado?
  ¿Existe un plan de rollback?

Genera el JSON de validación con el mismo formato que los bloques anteriores,
usando el identificador "bloque": "migracion" para todos los problemas.
Añadir también:

"riesgo_especifico_migracion": {
  "nivel": "alto │ medio │ bajo",
  "factor_principal": "[el riesgo más importante del requisito]",
  "mitigacion_recomendada": "[acción concreta para reducirlo]"
}
```

---

## Ejemplos concretos de requisito de migración

### Requisito mal definido de migración

```
"El sistema debe migrar las facturas del sistema antiguo al nuevo.
Los datos deben mantenerse correctamente."
```

Problemas específicos de migración, además de los problemas estándar del punto 12 del modelo base:

- No indica qué sistema legado, qué módulo, ni qué tipo de facturas.
- "Mantener correctamente" no es verificable: ¿idéntico?, ¿equivalente?, ¿con transformaciones?
- No documenta las reglas de negocio del legado que deben preservarse.
- No hay decisión de equivalencia.
- No existe ningún criterio que permita contrastar el resultado con el legado.

### Requisito bien definido de migración

```yaml
id: REQ-M-041
titulo: "Migrar facturas de proveedor activas desde SAP R/3 módulo FI-AP"
epica: EP-04
actor: "Gestor de facturación"
estado: validado
prioridad: must-have
descripcion: >
  El gestor de facturación necesita acceder en el nuevo sistema a todas las
  facturas de proveedor activas (no archivadas) del ejercicio fiscal en curso
  que existen hoy en SAP R/3, con los mismos datos y el mismo estado que tienen
  en el momento del cutover.

evento_disparador: >
  El gestor accede al módulo Facturas del nuevo sistema tras el cutover
  para gestionar el cierre mensual de mayo.

criterios_aceptacion:
  - id: AC-M041-01
    dado: >
      El cutover se ha completado y el gestor accede al módulo Facturas
      del nuevo sistema con rol gestor_facturacion
    cuando: >
      Filtra por estado 'pendiente' y ejercicio fiscal '2025'
    entonces: >
      El listado muestra exactamente los mismos registros que
      la transacción FBL1N de SAP con los mismos filtros,
      con los mismos importes, fechas y proveedores.
      La diferencia máxima permitida es 0 registros.

  - id: AC-M041-02
    dado: >
      Una factura de SAP con importe en moneda extranjera (USD)
      está incluida en el lote de migración
    cuando: >
      El gestor consulta esa factura en el nuevo sistema
    entonces: >
      El importe se muestra en EUR calculado con el tipo de cambio
      de la fecha de factura, coherente con el campo WRBTR de SAP
      convertido según la tabla TCURR de la fecha de documento.

migracion:
  sistema_origen:
    nombre: "SAP R/3"
    modulo: "FI-AP (Accounts Payable)"
    tecnologia: "ABAP / SAP R/3 4.7"
    version: "4.7 Enterprise"
    responsable_conocimiento: "José Moreno — Dpto. SAP"
    documentacion_disponible:
      - tipo: especificacion_tecnica
        ubicacion: "Confluence: /SAP/FI-AP/estructura-tablas-FI"
      - tipo: codigo_fuente
        ubicacion: "Repositorio SAP: /abap/fi/ap/Z_FACT_EXTRACT"

  comportamiento_actual:
    descripcion: >
      SAP almacena las facturas de proveedor en la tabla BKPF (cabecera de
      documentos contables) y BSEG (posiciones). Una factura activa es un
      documento con BKPF.BSTAT = ' ' (espacio) y BKPF.GJAHR igual al
      ejercicio en curso. Los importes se almacenan en moneda del documento
      (BSEG.WRBTR) y en moneda local EUR (BSEG.DMBTR). Las facturas archivadas
      tienen BKPF.BSTAT = 'A' y están fuera del alcance de esta migración.

    flujo_actual:
      - paso: 1
        actor: "Proveedor / integración EDI"
        accion: "Envía factura a SAP vía interfaz Z_FACT_IN o entrada manual"
        resultado: "Se crea registro en BKPF y BSEG con BSTAT = ' '"
      - paso: 2
        actor: "Gestor de facturación"
        accion: "Accede a FBL1N para consultar facturas pendientes de su proveedor"
        resultado: "SAP muestra facturas activas filtradas por sociedad y proveedor"
      - paso: 3
        actor: "Gestor de facturación"
        accion: "Selecciona la factura y ejecuta la aprobación (transacción FB60)"
        resultado: "BKPF.BSTAT permanece ' ' pero se actualiza el campo de estado de pago"

    reglas_actuales:
      - id: RA-M041-01
        descripcion: >
          Solo las facturas del ejercicio fiscal en curso (BKPF.GJAHR = año actual)
          se gestionan activamente. Las de ejercicios anteriores son solo consulta.
        origen: entrevista
      - id: RA-M041-02
        descripcion: >
          Las facturas superiores a 10.000 EUR requieren aprobación de dos firmantes.
          En SAP esto se gestiona mediante el workflow WS20000050 que solo se activa
          cuando BSEG.DMBTR > 10000.
        origen: codigo_fuente
      - id: RA-M041-03
        descripcion: >
          SAP almacena el NIF del proveedor en la tabla LFA1.STCD1 con formato
          sin guiones ni espacios. El nuevo sistema valida el formato NIF/CIF español
          incluyendo el dígito de control.
        origen: prueba_exploratoria

    datos_actuales:
      - campo: "BSEG.WRBTR"
        tipo_en_legado: "CURR(13,2) en tabla BSEG"
        tipo_en_nuevo: "decimal(15,2)"
        transformacion: >
          Convertir a EUR usando tipo de cambio de BKPF.BUDAT
          consultando tabla TCURR de SAP. Si BKPF.WAERS = 'EUR',
          el valor es directo sin conversión.
        valores_nulos: "No puede ser nulo en SAP. Si existe registro nulo, es dato corrupto."
        valores_especiales:
          - "0.00: factura a coste cero (material gratuito, válida)"

      - campo: "LFA1.STCD1 (NIF proveedor)"
        tipo_en_legado: "CHAR(16)"
        tipo_en_nuevo: "string con validación formato NIF/CIF"
        transformacion: >
          Normalizar formato: eliminar espacios y guiones.
          Validar dígito de control al insertar.
          Si la validación falla: marcar el proveedor como
          'requiere_revision_nif' sin bloquear la migración.
        valores_nulos: "Posible. SAP permite proveedores sin NIF para facturas de importación."
        valores_especiales:
          - "FOREIGN: código especial para proveedores extranjeros sin NIF español"

    volumetria:
      registros_actuales: 47832
      crecimiento_anual: "12% anual"
      pico_uso: "últimos 3 días laborables de cada mes"
      tiempo_respuesta_actual: "FBL1N con filtro estándar: 3-8 segundos para 500 registros"

  equivalencia:
    decision_global: equivalente
    justificacion: >
      Se replica el comportamiento funcional de SAP FI-AP para la gestión
      de facturas de proveedor. Los datos se migran con transformaciones
      documentadas para adaptarse al modelo de datos del nuevo sistema.
      La UX y los flujos de aprobación mejoran respecto a SAP.
      Decisión aprobada por Ana López (Dirección Financiera) en reunión
      de kick-off del 2025-03-15.

    diferencias_deliberadas:
      - aspecto: "Flujo de aprobación de facturas >10.000 EUR"
        comportamiento_legado: >
          SAP usa workflow WS20000050 con dos firmantes de nivel jerárquico
          equivalente. El workflow no tiene timeout: puede quedarse bloqueado
          indefinidamente si un firmante no actúa.
        comportamiento_nuevo: >
          El nuevo sistema implementa un flujo de aprobación secuencial
          (primer aprobador → segundo aprobador) con timeout de 48h laborables.
          Si el primer aprobador no actúa, se reasigna automáticamente al
          Responsable financiero.
        aprobado_por: "Ana López"
        fecha_aprobacion: "2025-03-15"
        referencia: "Acta reunión kick-off REQ-MIGR-001 — sección 4.2"

      - aspecto: "Validación de NIF de proveedor"
        comportamiento_legado: >
          SAP no valida el formato del NIF. Existen 234 proveedores con NIF
          en formato incorrecto en la base de datos actual.
        comportamiento_nuevo: >
          El nuevo sistema valida el dígito de control del NIF/CIF.
          Los proveedores con NIF inválido se migran con estado
          'requiere_revision_nif' y no pueden recibir nuevas facturas
          hasta que el dato se corrija.
        aprobado_por: "Ana López"
        fecha_aprobacion: "2025-03-22"
        referencia: "Issue MIGR-089 — decisión en comentario del 2025-03-22"

    comportamientos_no_migrar:
      - funcionalidad: "Informes ABAP personalizados Z_FACT_RPT_*"
        motivo_exclusion: >
          Los 7 informes ABAP personalizados que existen en SAP se sustituyen
          por el módulo de Reporting del nuevo sistema. Ninguno se migra.
          Los usuarios recibirán formación en el nuevo reporting.
        aprobado_por: "Ana López"

      - funcionalidad: "Facturas de ejercicios anteriores a 2023"
        motivo_exclusion: >
          Las facturas anteriores a 2023 (26.847 registros) se archivan
          en formato PDF y no se migran al nuevo sistema como registros activos.
          Solo estarán disponibles en el archivo documental.
        aprobado_por: "Ana López"

  criterios_equivalencia:
    - id: CE-M041-01
      aspecto: "Número exacto de facturas activas migradas"
      dado_legado: >
        Consulta SELECT COUNT(*) FROM BKPF WHERE BSTAT=' ' AND GJAHR=2025
        ejecutada en SAP el día del cutover
      cuando_legado: "La consulta devuelve N registros"
      resultado_legado: "N registros activos en SAP"
      resultado_esperado_nuevo: >
        El nuevo sistema tiene exactamente N registros en estado no-archivado
        del ejercicio 2025. Tolerancia: 0 registros de diferencia.
      tipo_equivalencia: identico
      dato_contraste:
        fecha_consulta: "pendiente — se ejecuta el día del cutover"
        script_verificacion: "/scripts/migracion/verificar_conteo_facturas.sql"

    - id: CE-M041-02
      aspecto: "Integridad de importes tras conversión de moneda"
      dado_legado: >
        Factura BKPF.BELNR=1900045678 con WAERS=USD, WRBTR=1250.00,
        BUDAT=2025-02-15
      cuando_legado: "Se consulta el importe en EUR en FBL1N"
      resultado_legado: "SAP muestra 1.142,50 EUR (tipo de cambio 1,0941 de TCURR para 2025-02-15)"
      resultado_esperado_nuevo: >
        El nuevo sistema muestra 1.142,50 EUR para esa factura.
        Tolerancia: ±0,01 EUR por redondeo.
      tipo_equivalencia: identico
      dato_contraste:
        belnr: "1900045678"
        waers: "USD"
        wrbtr: 1250.00
        budat: "2025-02-15"
        importe_eur_esperado: 1142.50

  pruebas_regresion:
    estrategia: shadow
    periodo_coexistencia: "4 semanas tras el cutover"
    criterio_cutover: >
      Los 3 cierres mensuales posteriores al cutover no presentan diferencias
      entre el resultado del proceso en SAP y en el nuevo sistema.
      Diferencia máxima tolerada en totales de cierre: 0,00 EUR.
    plan_rollback: >
      Si se detecta una diferencia de más de 0,01 EUR en cualquier importe
      durante el período de coexistencia, se reactiva SAP como sistema principal
      y el nuevo sistema pasa a shadow. Se abre incidencia BLOQUEANTE.

  datos_historicos:
    migrar_historico: true
    fecha_corte: "2023-01-01"
    transformacion_historico: >
      Las facturas de 2023 y 2024 se migran en modo solo-lectura.
      No pueden recibir nuevas operaciones (aprobación, pago) en el nuevo sistema.
      Las operaciones en curso en el momento del cutover se completan en SAP.
    validacion_historico: >
      Reconciliación de totales por ejercicio: la suma de BSEG.DMBTR por GJAHR
      debe coincidir exactamente entre SAP y el nuevo sistema.
```

### Historia de usuario AI-ready de migración

```yaml
historia:
  id: US-M-098
  titulo: "Consultar facturas migradas desde SAP con equivalencia funcional verificada"
  tipo: migracion
  epica: EP-04
  requisito_origen: REQ-M-041
  como: "gestor de facturación"
  quiero: >
    acceder en el nuevo sistema a las facturas de proveedor activas migradas
    desde SAP con los mismos importes, estados y datos que tenían en el momento
    del cutover
  para: >
    continuar gestionando el cierre mensual sin interrupción y sin necesidad
    de consultar SAP para verificar datos históricos

  comportamiento_sistema_actual: >
    En SAP R/3, el gestor accede a la transacción FBL1N filtrando por sociedad,
    proveedor y ejercicio. SAP muestra las facturas en estado BSTAT=' '
    (activas) con los importes en EUR calculados al tipo de cambio de la fecha
    de documento. El tiempo de respuesta actual es de 3-8 segundos para 500 registros.

  criterios_aceptacion:
    - id: AC-M098-01
      dado: >
        El gestor está autenticado y el cutover se completó hace 3 días.
        Existen 47.832 facturas activas migradas desde SAP.
      cuando: >
        Filtra por estado 'pendiente' y ejercicio '2025' en el módulo Facturas
      entonces: >
        El listado muestra exactamente los mismos registros que FBL1N en SAP
        con los mismos filtros. La diferencia es de 0 registros.
        Los importes coinciden con los de SAP con tolerancia máxima de ±0,01 EUR.
        El tiempo de respuesta es inferior a 2 segundos para los primeros 500 registros.

    - id: AC-M098-02
      dado: >
        Una factura migrada tenía NIF de proveedor en formato incorrecto en SAP
        (sin dígito de control válido). El proveedor tiene estado 'requiere_revision_nif'.
      cuando: >
        El gestor consulta esa factura en el nuevo sistema
      entonces: >
        La factura se muestra correctamente con todos sus datos.
        Aparece un aviso visible: 'El NIF del proveedor requiere revisión'.
        El gestor puede consultar la factura pero no puede aprobarla
        hasta que el NIF del proveedor sea corregido.

    - id: AC-M098-03  # Criterio de equivalencia
      dado: >
        La factura BELNR=1900045678 de SAP (USD, importe 1.250,00, fecha 2025-02-15)
        se migró al nuevo sistema.
      cuando: >
        El gestor consulta el detalle de esa factura
      entonces: >
        El sistema muestra el importe 1.142,50 EUR,
        coherente con la conversión USD→EUR al tipo de cambio de SAP
        para la fecha 2025-02-15 (tipo 1,0941).
        Tolerancia: ±0,01 EUR.

  definition_of_done:
    - "Todos los criterios de aceptación superan pruebas de regresión"
    - "Reconciliación de conteos entre SAP y nuevo sistema: diferencia = 0"
    - "Reconciliación de totales por ejercicio: diferencia = 0,00 EUR"
    - "Prueba de rendimiento con 47.832 registros en staging: p95 < 2s"
    - "Período de coexistencia en shadow completado sin diferencias"

  estimacion_story_points: 8
  # Incrementado desde la base de 5 por incertidumbre en datos del legado
  # (documentación parcial, 234 NIF incorrectos conocidos, transformación de moneda)
```

---

## Matriz de trazabilidad ampliada para migraciones

La matriz del punto 9 del modelo base se extiende con una columna adicional que referencia el comportamiento del legado verificado.

| Ref. Legado | Requisito | Historia | Criterio AC | Tipo | Test Case | Estado TC | Issue Jira | Equivalencia |
|---|---|---|---|---|---|---|---|---|
| BKPF/BSEG FI-AP | REQ-M-041 | US-M-098 | AC-M098-01 | Funcional | TC-M-201 | ✅ Pasado | FACT-M-047 | identico |
| LFA1.STCD1 | REQ-M-041 | US-M-098 | AC-M098-02 | Funcional | TC-M-202 | ✅ Pasado | FACT-M-047 | mejorado |
| BSEG.WRBTR + TCURR | REQ-M-041 | US-M-098 | AC-M098-03 (CE) | Equivalencia | TC-M-203 | 🔴 Fallido | FACT-M-047 | identico |
| WS20000050 | REQ-M-041 | US-M-099 | AC-M099-01 | Funcional | TC-M-210 | ⏸ Pendiente | FACT-M-052 | mejorado |

La columna **Ref. Legado** permite navegar desde cualquier test case fallido hasta el componente exacto del sistema legado que define el comportamiento esperado. Esto elimina la ambigüedad más frecuente en proyectos de migración: cuando un test falla, el equipo sabe en segundos si es un bug de implementación o un comportamiento del legado que no se había documentado correctamente.

---

## Riesgos específicos de migración

Los cinco riesgos adicionales que la migración incorpora al catálogo del punto 12 del modelo base.

### R-M-01: Comportamiento no documentado del legado descubierto en producción

**Descripción.** El sistema legado tiene comportamientos que nadie documenta porque están tan integrados en el flujo de trabajo diario que los usuarios los dan por sentados. Solo aparecen cuando faltan en el nuevo sistema.

**Señales tempranas.** Los usuarios de negocio durante el piloto dicen "esto siempre lo hacía automáticamente" o "qué raro, en SAP esto se calculaba solo". El número de incidencias post-cutover con tipo "funcionalidad faltante" supera el 10% del total.

**Mitigación.** Sesiones de observación directa del sistema legado en uso real (no solo entrevistas). Registro obligatorio del origen de cada regla de negocio en el YAML. Período de coexistencia de al menos 4 semanas con el sistema legado activo para que los usuarios detecten comportamientos faltantes antes del apagado definitivo.

**Contingencia.** Si se descubre un comportamiento no documentado durante el período de coexistencia: abrirlo como REQ-M-nuevo con decisión de equivalencia urgente. Si se descubre después del apagado del legado: evaluación de si es recuperable desde los datos migrados o si requiere desarrollo nuevo.

---

### R-M-02: Datos corruptos o inconsistentes en el legado

**Descripción.** El sistema legado puede tener datos que no cumplen las validaciones que el nuevo sistema implementa correctamente. Estos datos son válidos en el legado porque sus validaciones son más laxas o simplemente no existen, pero rompen la migración.

**Señales tempranas.** Durante la extracción de datos del legado para el entorno de staging, el script de transformación genera errores en más del 2% de los registros. El campo `valores_especiales` del YAML crece durante el análisis.

**Mitigación.** Análisis de calidad de datos del legado antes de comprometer el alcance de la migración. Documentar en el YAML todos los valores especiales y casos de dato corrupto conocidos. Definir la política explícita de qué hacer con cada tipo de dato inválido (rechazar, transformar, migrar con marca de revisión).

**Contingencia.** Plan de limpieza de datos en el legado antes del cutover si el volumen de datos inválidos supera el umbral acordado. Si no es posible limpiar, migrar con marca `requiere_revision` y proceso manual posterior.

---

### R-M-03: Divergencia entre la especificación y el comportamiento real del legado

**Descripción.** La documentación del sistema legado (si existe) describe cómo debería funcionar, no cómo funciona realmente. Los parches, las workarounds y los años de mantenimiento correctivo crean una brecha entre la especificación y la realidad. El analista confía en la documentación y diseña el nuevo sistema según lo que debería hacer el legado, no según lo que hace.

**Señales tempranas.** Los criterios de equivalencia no se pueden verificar porque los resultados del legado difieren de los documentados. Los usuarios de negocio tienen comportamientos contraintuitivos al usar el legado que no están en ningún manual.

**Mitigación.** Verificar cada regla de negocio documentada contra el comportamiento real del sistema mediante pruebas exploratorias antes de escribir el YAML. Registrar el origen de cada regla actual con el valor `prueba_exploratoria` o `codigo_fuente` cuando la documentación oficial no es confiable.

**Contingencia.** Si se detecta divergencia durante el desarrollo: análisis de impacto inmediato sobre todos los criterios de equivalencia que dependen de esa regla. Decisión de negocio sobre cuál es el comportamiento correcto: el documentado o el real.

---

### R-M-04: Pérdida de rendimiento por complejidad del modelo de datos legado

**Descripción.** El sistema legado puede tener un rendimiento aceptable gracias a optimizaciones específicas de su tecnología (índices ABAP, cache de Oracle Forms, procesamiento batch COBOL) que no se replican directamente en el nuevo sistema. El nuevo sistema con un modelo de datos más limpio puede ser funcionalmente equivalente pero significativamente más lento.

**Señales tempranas.** El tiempo de respuesta del nuevo sistema en staging con el volumen de datos del legado supera el doble del tiempo del legado. Los test cases de rendimiento fallan consistentemente.

**Mitigación.** Documentar el tiempo de respuesta actual del legado en el campo `volumetria.tiempo_respuesta_actual` del YAML. Incluir criterios de aceptación de rendimiento comparativos, no solo absolutos. Realizar pruebas de rendimiento con el dataset de migración completo, no con datos de prueba reducidos.

**Contingencia.** Plan de optimización técnica (índices, cache, denormalización) si el rendimiento no alcanza el objetivo con el diseño inicial. Negociar con el negocio si el tiempo de respuesta del nuevo sistema puede ser ligeramente superior al del legado a cambio de otras mejoras.

---

### R-M-05: Resistencia al cambio disfrazada de problema funcional

**Descripción.** Los usuarios que conocen en profundidad el sistema legado a veces reportan como "bugs de migración" comportamientos que son en realidad diferencias deliberadas aprobadas por la dirección. Esta resistencia, si no se gestiona, consume tiempo del equipo en analizando problemas que no son problemas.

**Señales tempranas.** Incidencias post-cutover que, al analizarlas, corresponden a diferencias documentadas en el YAML en la sección `diferencias_deliberadas`. Los mismos usuarios reportan múltiples incidencias de este tipo.

**Mitigación.** La sección `diferencias_deliberadas` del YAML debe ser accesible para el equipo de soporte post-cutover. Para cada diferencia deliberada, preparar un texto de respuesta estándar que el equipo de soporte puede usar: "Este comportamiento es diferente al de SAP de forma intencional. La decisión fue aprobada por Ana López el 15/03/2025 (referencia: Acta kick-off, sección 4.2)."

**Contingencia.** Si el volumen de incidencias de este tipo supera el 20% del total post-cutover, revisar si la comunicación del cambio fue suficiente antes del cutover y planificar sesiones de refuerzo con los equipos afectados.

---

## Checklist de validación previa al cutover

Este checklist complementa el checklist de validación automático del punto 6 y se ejecuta manualmente por el analista líder en las 48 horas previas al cutover.

```
CHECKLIST PRE-CUTOVER — Validación funcional de migración

DATOS
□ Reconciliación de conteos completada: diferencia = 0 registros
□ Reconciliación de totales por ejercicio: diferencia = 0,00 EUR
□ Todos los registros con marca 'requiere_revision_*' están listados
  y el equipo responsable de revisarlos está notificado
□ El script de rollback de datos ha sido probado en staging

PRUEBAS
□ Todos los criterios de equivalencia (CE-*) tienen resultado PASS
□ Todos los test cases de tipo comparacion_legado tienen resultado PASS
□ Las pruebas de coexistencia en shadow no presentan diferencias
□ Las pruebas de rendimiento con volumetría completa cumplen el criterio
□ Los test cases de cutover han sido ejecutados en staging

DOCUMENTACIÓN
□ Todas las diferencias deliberadas están documentadas con aprobación
□ El plan de rollback está accesible para todo el equipo de guardia
□ El equipo de soporte tiene la lista de diferencias deliberadas
  y los textos de respuesta estándar

PERSONAS
□ El responsable de conocimiento del legado está disponible
  durante las 72 horas posteriores al cutover
□ El criterio de activación del rollback está acordado y comunicado
□ El product owner ha dado el visto bueno formal al go/no-go
```

---

## Integración con el pipeline de generación

El orquestador del script del modelo base detecta automáticamente si un requisito es de tipo migración por la presencia del bloque `migracion` en el YAML y activa el modificador correspondiente en todos los pasos del pipeline.

```python
# Detección automática en el paso s4_generacion_artefactos
def es_requisito_migracion(requisito: dict) -> bool:
    return "migracion" in requisito and bool(requisito["migracion"])

def seleccionar_modificador_prompt(requisito: dict) -> str:
    if es_requisito_migracion(requisito):
        return cargar_prompt("modificador_migracion.txt")
    return ""

# Estimación ajustada de story points para migraciones
def ajustar_estimacion_migracion(
    story_points_base: int,
    requisito: dict
) -> int:
    if not es_requisito_migracion(requisito):
        return story_points_base

    migracion = requisito["migracion"]
    ajuste = 0

    # Sin documentación del legado: +3 puntos por incertidumbre
    docs = migracion.get("sistema_origen", {}).get(
        "documentacion_disponible", []
    )
    tipos_doc = [d.get("tipo") for d in docs]
    if "ninguna" in tipos_doc or not tipos_doc:
        ajuste += 3
    elif tipos_doc == ["codigo_fuente"]:
        ajuste += 2

    # Con transformaciones de datos complejas: +2 puntos
    transformaciones = [
        d for d in migracion.get(
            "comportamiento_actual", {}
        ).get("datos_actuales", [])
        if d.get("transformacion")
    ]
    if len(transformaciones) > 2:
        ajuste += 2

    # Con equivalencia "reemplazado": +1 punto por gestión del cambio
    if migracion.get("equivalencia", {}).get(
        "decision_global"
    ) == "reemplazado":
        ajuste += 1

    return min(story_points_base + ajuste, 13)
```

---

*Este documento es un complemento al Modelo Operativo AI-Ready. Debe leerse junto con los puntos 1–12 del modelo base, especialmente la plantilla YAML (punto 1), el glosario estructurado (punto 2), la guía de Event Storming (punto 3), los prompts de generación (punto 4), la generación de test cases (punto 5), la validación automática (punto 6) y la arquitectura RAG (punto 7).*
