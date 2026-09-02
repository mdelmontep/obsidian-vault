---
title: facturaia — histórico detallado
date: 2026-05-31
tags: [cliente, facturaia, historico]
---

Índice del histórico de FacturaIA. El contenido pesado vive partido en los ficheros de abajo (uno por snapshot de poda del hub, más uno de eventos puntuales con fecha propia). El hub vivo y actual es [[facturaia]].

- [[facturaia-historico-snapshot-2026-05-31]] — snapshot fundacional del hub (contenido original del archivo desde su creación): log cronológico en blockquotes (~2026-05-16 a 2026-07-19), foto congelada del hub a 2026-05-31 (Estado actual, NOW, Smoke, WIP, Progreso en vivo, NEXT, LATER, Decisiones, Bloqueos, Seguridad, Stack, credenciales, histórico de hitos) y la Auditoría SaaS 2026-05-29.
- [[facturaia-historico-snapshot-2026-06-15]] — dos podas del hub del mismo día: "dieta del hub" (Estado/NOW/PRIORIDADES/Progreso en vivo/Decisiones/Histórico de hitos) y "purga hub" (NEXT/Smoke/Bloqueos/WIP cerrados movidos).
- [[facturaia-historico-eventos]] — entradas de evento puntual con fecha propia en el header, 2026-06-16 a 2026-07-13 (informes de analítica, bug NIF proveedor, stock por lotes, hitos 06-28→07-04, dedup NOTES, ingesta, drawers, cierre de pendientes).
- [[facturaia-historico-snapshot-2026-07-15]] — poda del NOW del hub a 2026-07-15.
- [[facturaia-historico-snapshot-2026-07-23]] — poda más reciente del hub a 2026-07-23 (Obras: certificación/ficha/adicionales/retención de garantía, modales adaptables, nombres por UUID).
- [[facturaia-historico-snapshot-2026-07-25]] — poda del NOW del hub a 2026-07-25: 38 entradas cerradas (Obras completo, unificación UI, Centro Fiscal, billing/cupones, Slack, seguridad npm, ticket-runner, import de extractos, API v1 Obras).
- [[facturaia-historico-snapshot-2026-07-27]] — poda del 27-jul: 12 entradas cerradas del NOW (gate del 26-jul y sus remates, vigilante externo, lote conciliación, retención del copiloto, Obras, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta).
- [[facturaia-historico-snapshot-2026-07-28]] — poda del 28-jul: 10 entradas cerradas del NOW (IVA negativo de presupuestos, `/api/health` con versión real, ticket de vencimiento de IET, panel `/admin` sin falsas incidencias de precios + `proxy.ts`, gate del 26-jul y sus remates, lote de conciliación).
- [[facturaia-historico-snapshot-2026-07-29]] — dos podas del 29-jul: la de la mañana y, al cierre, 11 entradas más del NOW (área de tickets y su fuga de mensajes internos, avisos de respuesta del cliente, impersonación en listados, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta, recurrentes).
- [[facturaia-historico-snapshot-2026-07-30]] — poda del 30-jul: los 4 smokes de prod que Manu ya verificó (runner, OCR de nº de factura y RAEE, condiciones de pago en PDF, impersonación tras `proxy.ts`).
- [[facturaia-historico-snapshot-2026-08-19]] — track de contenido de la spec #1908 (nueve tickets, migs 713-720, motor de edición): detalle retirado del NOW, los cuatro fallos que aparecieron al renderizar y los dos cabos de #1959.
- [[facturaia-historico-snapshot-2026-08-30]] — poda del 30-ago al cerrar el super test V2: 9 entradas retiradas del NOW (la campaña del barrido y la «salida A» del albarán, ticket 156, IA agéntica de categorías, las 22 llamadas al modelo, el arnés `eval:ocr`, el cuerpo de un error, el 303 y la unidad de obra desde el presupuesto).

## 3-sep-2026 · tickets 166/167/168 y su code review en tres PRs (#2408 · #2410 · #2411, mig 805 · #2417 · #2418 · #2419)

- **Datos (#2417)** — `fetchLineasDeNodos`/`fetchNodosDePresupuesto` (`presupuestos-db.ts`) son la única lectura de partidas y nodos: paginada con `fetchAllPages` y por lotes de 300 ids con `fetchAllInChunks`, error si la lectura queda incompleta. Ocho lectores migrados (copiar, proforma, xlsx, pdf, copiloto ×2, materiales pendientes, proveedores resueltos); candado en `presupuesto-orden-espejo-check.test.ts` §lecturas; integración 7/7 con 1.001 líneas (el `.in()` a pelo devolvía 1.000 sin error). La selección de partidas se copia en el orden visual de la rejilla (`lineasEnOrdenVisual`), no en el de los clics.
- **UX y contrato (#2418)** — crear un producto desde un albarán devuelve el foco a Cantidad (línea nueva) o al Select de la línea (detalle), y solo avisa «Producto creado y asignado» cuando el emparejado responde OK; `NuevoProductoModal` abre en Nombre vía `initialFocus` y desplaza el `role="alert"` a la vista; `submitLabel` opcional («Crear producto»); copy del catálogo vacío con la acción; `orden` documentado en el openapi; `inventario-vacio.test.tsx` nuevo.
- **Proceso (#2419)** — `cierre:alcance -- --registrar` se niega con el árbol sucio (tres cierres del 2-sep apuntaban al mismo `1debb02de`, el main del momento) y acepta `--commit <sha>`; Paso 5 de `/fia-cierre`: commit → registrar → commit `chore(cierre)`. Guard probado con `mutate`.
- **Decidido y NO hecho, con motivo** — mover `csv.ts` (no es de Obras), portal propio para el modal anidado (el bug era el foco), `orden` opcional en el tipo (la mig 805 lo garantiza), `defaultIva` opcional (el 21 es del llamador). Gemelo abierto: #2416 (`obras_unidad_obra_lineas` sin paginar al duplicar).
- **Ticket 165 (2-sep, #2401 + #2404, mig 803)** — cuota IVA 337,22 vs 337,23: la cadena de importes calcula en decimal exacto; A2026-0081 anulada (abono B2026-0006) y sustituida por A2026-0091. De propina, la mig 792 dejaba todo abono fuera de los motores de stock (anular no reponía): canario en 5 min, un abono dañado y reparado en la propia mig 803. → [[un-candado-que-fija-la-forma-literal-del-filtro-consagra-el-bug]]
- Aprendizaje: [[un-registro-que-estampa-head-vale-solo-con-el-arbol-limpio]].

## 2-sep-2026 · los slides del carrusel salen maquetados (PR #2379, migs 793/794/795)

El bug era silencioso: el productor de imagen dejaba los slides limpios —la ilustración sin los
titulares del guion encima— y se publicaban así, sin que nada lo dijera. Ahora el panel avisa («se
publicarían sin los titulares del guion») y «Maquetar los slides» compone.

Lo que entró: `maquetado` como `kind` de `marketing_piece_assets` con índice único parcial por slide
(793) · `marketing_brand_assets`, la biblioteca de marca, service-role-only (794) · reglas de estilo
tipadas con `eje`/`fuerza`/`vigente_hasta` (795).

**Smoke real en prod**, pieza «Un WhatsApp basta para facturar» (`7ee13237`): 7 assets `maquetado`,
1080×1350 (4:5), `origen=runner`. La prueba de que compone y no es un no-op: PNG→JPEG cambia el peso
en los siete, de −23,9 % a −80,2 % (slide 0: 723.297 → 143.054 B). El panel Material pasó de 7 a 14
archivos y el aviso desapareció.

Dos gotchas del camino, ya en learnings: el barrido de renumeración con BSD `sed` **no sustituyó
nada** y salió en verde ([[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]]), y el
censo `tap-target-inventario` se repunta a mano porque su generador solo imprime
([[un-censo-cuyo-generador-solo-imprime-no-se-regenera-se-repunta]]).

## 2-sep-2026 · los tres tickets de Pescados Chivite (PR #2382 · #2386 · #2387 · #2393 · #2396, mig 796)

- **163/164 (#2387)** — la ficha del albarán vuelve al listado y deja cambiar un producto ya asignado mientras está `abierto`.
- **156.2 (#2386, mig 796)** — la recibida duplicada 73056007 (`disputada`) se retira con respaldo en `facturas_reclasificadas_albaran`; los cuatro apuntes (+3, +2, −2, −3) se quedan en el ledger desenganchados y cruzados, porque borrarlos pondría en rojo `detect_lote_drift`. El cliente ya había compensado el stock el 1-ago: nuestro «te sumó 5» del 29-ago era falso y se corrigió en el hilo.
- **156.3** — 95015083 no estaba perdida: `disputada`, que el listado oculta por defecto. No hay camino de vuelta a `pendiente`: decisión de producto pendiente.
- **156.4 (#2382 + #2393)** — el OCR ya no crea un proveedor cuando existe uno con el mismo NIF salvo prefijo: cae a revisión con `proveedor_posible_duplicado`, dice qué ficha y no ofrece «Corregir» sobre el NIF (ADR-064 corolario 2).
- **Guías** — capturas con recuadro y etiqueta pintadas en el propio navegador, un mensaje por paso en el hilo del ticket.
- **Copy del 409 (#2396)** — «cruza una vez aprobada» era del 28-ago; la mig 768 lo invirtió y AL014 ya no deja corregir después. Constante compartida del título del panel + candado que lee la fuente; ADR-030 y dos hallazgos de QA enmendados. `docs/plan/cierres.json` limpio (39 registros).
- Aprendizajes: [[un-copy-que-afirma-una-limitacion-tecnica-caduca-con-ella]] · [[capturas-guiadas-overlay-svg-en-el-navegador]].

## 1-sep-2026 · el rastro de quién mira, y el DPA que faltaba (PR #2361 + #2364)

- **Panel de Accesos en `/admin/ia-ops` (#2361, ADR-067)** — cada vez que alguien del equipo abre una ficha de cliente queda una fila con quién, cuándo, de qué org y si el contenido se sirvió **en claro o tapado**; si la fila no se puede escribir, el contenido no se sirve. Consultable desde el panel, así que a un cliente que pregunte «¿quién ha visto mis facturas?» se le puede responder sin entrar en la BD. Smoke en prod con las dos filas reales del día. La ruta no se audita a sí misma a propósito: auditar la lectura de la auditoría es una escalera sin peldaño final.
- **Borrador del DPA del art. 28 (#2364)** — 620 líneas, 16 cláusulas + Anexo I (subencargados) + Anexo II (medidas), escrito desde el código y no desde una plantilla: el doble papel del §1.1, las 48 h del §10 (el cliente tiene 72), y el §16 con las siete decisiones que no puede tomar un desarrollador. El **Anexo II §10 declara las ocho cosas que hoy NO hay** (PITR apagado con RPO de 24 h, sin guardián automático de RLS, verificación de copias sin cron, sin purga automática de una org, WORM vacío, sin ISO ni SOC 2). Entra en `/admin/documents`.
- **Un duplicado de meses en el registro de documentos** — `verifactu-auditoria-cumplimiento` estaba dos veces con el mismo `id` y distinta categoría: el listado lo pintaba dos veces y la segunda entrada era inalcanzable, porque el detalle resuelve con `find`. Ni el typecheck ni nadie lo veían. Cerrado con candado de ids únicos + `filePath` existente, probado por mutación.
- **Superadmins de prod: 8, y 4 sobran** — inventario hecho contra la BD (`profiles.is_superadmin`, que va por `user_id`, no por `id`). Quitarlos es escritura sobre permisos de personas, así que queda del lado de Manu. En Dokploy quedan además dos líneas muertas de entorno, `SUPERADMIN_EMAILS` (retirada el 2-ago) e `IA_OPS_SHOW_TRANSCRIPTS`.
- Aprendizaje: [[una-vista-en-cargando-con-su-api-en-200-esta-sin-hidratar]].

## 26-ago-2026 (cierre) · la auditoría de Albaranes, cerrada (PR #2235 `4ad5534e1` + #2237 `553e77845`)

Las **18 propuestas** de `AUDITORIA-albaranes-2026-08-26.md` decididas una a una con su argumento en
**ADR-030**: 12 implementadas, 4 rechazadas por escrito (entre ellas `AL014` por línea y vaciar el PMP:
no reabrir sin datos nuevos) y 2 de campo. Migs **756-760**, ya aplicadas en prod y con `migration list
--linked` verificado (local == remote hasta 761): los números estaban congelados, así que **no** se
renumeró.

Lo que cierra el área: entra desde la ficha del proveedor, un widget del dashboard y deep-link; el
listado se busca por número o proveedor y se ordena; el filtro de proveedor busca en servidor; aprobar
una factura pregunta antes por los albaranes sin cruzar y el panel los resuelve en el mismo modal; la
procedencia (`creado_via`) se guarda y se ve; el copiloto sabe responder qué has recibido y no te han
facturado. Y `validado_parcial` se retira (mig 760) — nadie podía escribirlo.

Tres hallazgos que no venían en la auditoría:
1. **El aviso miraba menos días que el panel que lo resuelve**, y excluía las fechas nulas. Esa
   diferencia es la rendija del doble conteo → [[el-aviso-y-el-panel-que-lo-resuelve-tienen-que-medir-la-misma-ventana]]
2. **`validado_parcial` seguía vivo en `openapi-spec.json`**, o sea en el contrato público, porque el
   test de espejo ataba dos de las tres caras → [[retirar-un-valor-de-un-enum-lo-deja-vivo-en-el-contrato-publico]]
3. **Dos defectos que solo se vieron conduciendo el navegador**: faltaban fronteras `<Suspense>` en las
   dos páginas (con `cacheComponents`, error en consola en cada visita) y un mensaje de «ningún
   proveedor con ese nombre» que no podía renderizarse nunca.

Evidencia: gate entero verde (lint, typecheck, **15.712** tests, build), los tests de los arreglos
**mutados** (al estrechar la ventana o quitar la rama del nulo, caen), QA en 1440 claro / 1440 oscuro /
390 contra la org `is_test` de prod (el artifact con las 22 capturas lo borraron el 27-ago y la sesión
perdió el enlace; el HTML sigue en el scratchpad → [[artifact-solo-lo-republica-la-cuenta-que-lo-publico]]),
y el grafo regenerado y leído: cero circulares nuevas y **ningún quinto pipeline de auth** —
`withAlbaranesAuth` envuelve `withApiAuth` y solo aporta el `moduleGate`; anotado en `dependency-map.md`.

El #2237 cierra el paso externo: schedule `SckQKegrM1-4D8ZEs_Z-H` en Dokploy (`50 7 * * *`, TZ
Europe/Madrid), `runManually` → `cron_runs` **success** con `{"orgs":1,"total":1}` leído por psql, y
retirado `pendiente_de_schedule`. De paso corrigió una hora: el registry decía «08:50 Madrid» para
`50 7 * * *`, que es la lectura en UTC — con `timezone` explícito dispara a las **07:50** todo el año.

**27-ago 07:50:01 Madrid: disparó solo y la hora corregida quedó probada por el propio run** — `success`
en 208 ms, `{"orgs":1,"total":1}`, `triggered_by: dokploy`. La cadena llega al final, no al 200: la
notificación se **reabrió** (`occurrence_count` 2, `warning`, CTA `/albaranes?estado=abierto`), que es el
comportamiento de `notify_upsert` por el que el cron es diario y no cada N minutos. El 1 cuadra con la
base —un único albarán `abierto`, en la org `is_test`—. Sigue sin ejercer que el CTA aterrice filtrado.

## 26-ago-2026 (cierre) · el cableado del bloque, vigilado y probado en prod (PR #2232, `c50bb1180`)

El #2230 dejó un agujero declarado: las tres líneas de pegamento de la ruta no estaban ejercidas en
ningún sitio, y `aprenderCategoriaBulk` es no-throw, así que un fallo ahí devuelve 200, confirma y deja
de aprender **en silencio**. Cerrado por los dos lados.

**Candado.** `bulk-confirm/__tests__/route.aprendizaje.test.ts`: siete tests que ejecutan el handler
real (con `withApiAuth` mockeado, patrón del repo) y afirman sobre los argumentos de la llamada al
aprendizaje — la columna `categoria_id` en el SELECT, los pares `(movimientoId, categoriaId)`, el
cliente admin reutilizado, la categoría nula que pasa tal cual, que con cero filas no llama a nada, que
`confirm_all` también aprende (su rama de query es otra) y que la medición se cierra además del
aprendizaje. Cuatro mutaciones, cuatro víctimas. Los espías van con `vi.hoisted` y **firma real**, no
`(...args: unknown[])`: así un cambio de contrato rompe en `typecheck`, no solo en runtime.

**Smoke del camino real** (org de test `Obras tufacturaia sandbox`, todo por endpoints de la app y el
botón de la UI): el GET de categorías dispara el seed lazy (16 categorías), `/api/conciliacion/import`
crea tres apuntes —dos `COMPRA TARJ. 5540XXXXXXXX0013 OPENAI-SAN FRANCISCO` y uno
`PAGO RECIBO IONOS ESPANA HOSTING`—, se clasifican uno a uno (el camino que ya aprendía: openai=2,
ionos=1, **y ahí queda verificado en prod el arreglo del extractor**: la clave es `openai`, no la
máscara), `bulk-revert` los devuelve a `ia_sugerencia`, y «Confirmar todas» deja **openai=3, ionos=2**:
+1 por clave, no +2 en la repetida. Ese +1 maduró openai a **verde** (umbral 3), o sea que el ciclo
entero —aprender, madurar, quedar lista para aplicarse sin LLM— está demostrado end-to-end contra el
RPC y el trigger de verdad. Limpieza: los tres movimientos borrados por el DELETE de la app y la org
activa devuelta; se quedan las dos reglas y las 16 categorías (datos legítimos de una org `is_test`, y
borrarlos exigía escribir fuera del camino de la app).

**Lo que salió a la luz midiendo → #2231.** `categoria_reglas_aprendidas` no tiene NINGUNA superficie
de usuario: su único consumidor es `enrich-batch`, y `GET /api/conciliacion/reglas-aprendidas` —el que
alimenta el enlace «Reglas aprendidas» de Conciliación— lee `conciliacion_reglas_aprendidas`, la de
emparejamiento (mig 155). Con dos reglas de categoría vivas devolvía `{"reglas":[]}`. El dominio OCR
tiene resuelto lo mismo (GET + DELETE + sección en Ajustes) y sirve de plantilla. Importa ahora porque
esa memoria **ya actúa**: en verde clasifica sin LLM y escribe `categoria_source='regla'`.

Sigue abierta la otra mitad de #2229 y es decisión de Manu: el gate se queda abierto con la medición
caducada (`evaluarGate` devuelve `mantener` con `autoAccuracy === null`, `src/lib/agentic/gate.ts:60`).
Tres opciones en el comentario del issue.

## 26-ago-2026 (noche) · el atajo en bloque aprende, y la máscara de la tarjeta deja de ser la clave (PR #2230)

Cierra la primera mitad de #2229. `bulk-confirm` cerraba la medición y no
aprendía nada, y las 126 decisiones de categoría cerradas en prod habían llegado
todas por ahí, en dos clics (2 el 1-jul, 124 el 23-jul): la memoria de reglas
estaba vacía **por construcción**, no por falta de uso.

- **`aprenderCategoriaBulk`** colapsa el lote por combinación `(clave, categoría)`
  antes de tocar la BD, así que el coste va por patrón distinto: los 124 apuntes
  son **37 llamadas al RPC, no 124**. Sin migración: la mig 372 ya suma +1 por
  llamada, así que una llamada por clave *es* «+1 por clave y por lote». Y ese
  colapso es justo lo que conserva el «aprender lento» de §0.bis-3 cuando la
  acción humana es masiva: un clic en bloque no puede madurar una regla de golpe.
- **El coste que justificaba no aprender estaba estimado por apunte y era por
  patrón.** La nota de alcance del docstring («por coste, resolver clave + RPC por
  cada uno de hasta miles de ids») era una estimación que nadie midió.
- **El extractor descarta ahora todo token con algún dígito**, no solo los 100 %
  numéricos: 68 de esos 124 apuntes son `COMPRA TARJ. 5540XXXXXXXX0013 <comercio>`
  y compartían clave —el enmascarado de la tarjeta, alfanumérico, que pasaba el
  filtro—. `tarj` y `devolucion` entran en stopwords. La regla vieja `token:tarj`
  queda inalcanzable: fila muerta e inocua, se deja.
- **Backfill idempotente por la misma función que el endpoint** (un SQL paralelo
  no probaría nada del camino vivo), sellando cada decisión en
  `valor_humano.aprendizaje_backfill` — y a propósito SIN añadir `categoria_id`,
  porque `auto_accuracy` deriva «corregida» de la presencia de esa clave y
  añadirla habría convertido en correcciones un montón de aceptaciones.
- **Aplicado a prod**: 126 decisiones, 2 orgs, 126/126 claves resueltas, 37 reglas
  con +1, 126 selladas; segunda pasada no encuentra nada. Estado medido después:
  42 filas (27 no ambiguas, 15 ambiguas), 26 en `veces_confirmada=1`, una en 2
  (`token:laura`), **0 reglas verdes** → cero cambio de comportamiento, que era la
  condición.
- **7 claves quedan ambiguas** (`openai` 30 vs 7, `costco`, `brico`, `ionos`,
  `social` y dos contrapartes): el humano les puso dos categorías. Mismo desenlace
  que esos clics de uno en uno, y como el RPC degrada pero no borra filas siguen
  ambiguas mientras convivan. No se hizo excepción para el histórico —un backfill
  con semántica propia deja de reproducir el camino vivo—; si el 30-vs-7 debiera
  ganar por mayoría, es un cambio de §0.bis-3 y va aparte.
- Verificación: gate completo verde (15.511 tests), 14 tests nuevos, **tres
  mutaciones con víctima** (romper el colapso, devolver el filtro a `^[0-9]+$`,
  anular la contraparte de una emitida) y cuatro tests que comparan los
  **argumentos reales del RPC** entre bloque e individual — si divergen, lo que el
  sistema aprende depende del botón que se pulse.

Sigue abierta la otra mitad de #2229: `evaluarGate` devuelve `mantener` con
`auto_accuracy = null`, así que el mismo `null` dice «no abras» y «no cierres» y
nada va a cerrar lo que se abrió el 23-jul.

## 26-ago-2026 (tarde) · los cuatro agujeros que quedaban donde la IA decide sola (PR #2226) y lo que dijo prod

Ejecución del prompt de continuación §8 + §1. Mergeado en `7c657ac6f`, 19 ficheros, +757/−69, sin migración.

1. **`DOMINIOS`/`MODOS` a fuente única** (`src/lib/agentic/dominios.ts`, espejo del CHECK de la mig 367 con test de espejo). No eran las tres copias que decía el prompt: eran **seis** — la cuarta en `agentic-diagnostico.ts` y dos uniones locales en el componente de Ajustes. El candado se verificó como manda la regla: metiendo un `'facturas'` falso en la unión, `typecheck` falla en TS2345/TS2741 exactamente en los cuatro sitios que hay que actualizar.
2. **`decidirMuestreo` con tests** (11): decide qué verdes van a confirmación humana, o sea la señal con la que se mide `auto_accuracy`. Documentado de paso el peligro del porcentaje: el camino OCR pasa `muestreo_rate` sin clamp propio, al contrario que conciliación.
3. **La degradación del gate por fin AVISA.** `aplicarGate` escribía `degradado_at`/`degradado_motivo` y **nadie los leía**: ni notificación, ni alerta, ni texto en Ajustes — la mitad `avisa` del «degrada+avisa» del §0.bis-5 no existía. Ahora emite un kind **no silenciable** (`agentic_degradado_*`, el dominio va en el kind porque `ref_id` es UUID) que se resuelve solo al reabrir el gate, y Ajustes explica por qué está en observación. Un descenso manual no inventa explicación.
4. **Dos docs que contradecían al código**: `agentic-ocr-conciliacion.md` §0.bis-7 (la detección de transferencias ya no depende del toggle) y `aprendizaje-ocr.md:166` (decía «pendiente» lo que `auto-approve.ts:203/:215` ya hace).

Verificación: **12 mutaciones, 11 víctimas inmediatas.** La 12.ª sobrevivió y fue la útil: mi test de la UI usaba `gate_abierto: true`, así que el guard exterior tapaba la condición que decía comprobar — verde por el motivo equivocado. Se cerró con el caso que discrimina (`activo` + gate cerrado, estado que el backend no produce y solo llega por escritura directa). Gate completo `EC=0`, 15.493 tests. Otra vez el hook del grafo paró el push y otra vez se resolvió por su vía (`npm run deps:json`), no con `--no-verify`.

### Lo que dijo prod (medición de solo lectura)

La primera aplicación silenciosa **no ha ocurrido** —0 filas con `categoria_source='regla'` en toda la BD, 0 en `audit_log` con `actor_type='agent'`— y por esa vía **no puede llegar**: 107 de las 109 verdes de AgentesiaLab se cerraron por `bulk_confirm`, y `closeCategoriaDecisionsBulk` no llama a `aprenderCategoria` (a propósito, por coste, y lo dice su docstring). El atajo que el usuario usa de verdad alimenta el denominador del gate y no la memoria. Corolario: ninguna org tiene una verde resuelta en 30 días, así que `auto_accuracy` es `null` para todas y `evaluarGate` devuelve `mantener` cada día — AgentesiaLab sigue en `activo` por un acierto del **23-jul**. Las dos decisiones que salen de ahí → #2229. Learnings → [[el-camino-en-bloque-cierra-la-medicion-pero-no-aprende]] · [[un-gate-abierto-con-la-metrica-caducada-no-vuelve-a-cerrarse]].

De paso, dos mediciones más: **#2227** (de 240 módulos que escriben sin humano, 91 sin ningún test que los alcance; mi primer script decía 12 porque casaba imports por basename en vez de resolverlos) y **#2228** (las 22 circulares de `_parts`: 21 son `import type` y una es de valor y real, `cuerpos.ts` leyendo `UUID_INEXISTENTE` del barrel en tiempo de evaluación).

## 26-ago-2026 · las tres decisiones que escriben en silencio dejan de vivir sin test (PR #2224)

Auditoría de qué escribe sola la IA agéntica, el día siguiente a activar `categorias`. El agujero lo encontró un grep, no un razonamiento: **ningún** fichero de test importa `enrich-batch/_parts/enrich-batch/helpers.ts`, así que no había cobertura posible por muchos tests que hubiera al lado.

1. **Camino de regla aprendida**: reimplementaba `autoReal && !esTI` a mano (escrito dos veces) más su propia zona. Ahora `decidirReglaSource` delega en el mismo `decidirCategoria` que el camino LLM, con test de PARIDAD que exige que los dos coincidan en si la escritura es silenciosa.
2. **Auto-aprobación OCR**: la condición vivía inline en `ocr-process/route.ts:1509` y su único test la REPLICABA — lo decía en su propia cabecera —, así que daba verde por definición; y la réplica ya estaba corta, no modelaba `direccionDoc`. Ahora `puedeAutoAprobar` (`src/lib/ocr/auto-gating.ts`) es el único sitio donde se decide, y el test recorre las 36 combinaciones exigiendo que apruebe exactamente una.
3. **Línea roja DURA levantada por un toggle de informes**: con `ia_detectar_transferencias_internas` apagado no se detectaban los pares, así que un traspaso entre cuentas propias se registraba en zona VERDE y, con la org en activo, se auto-categorizaba en silencio como ingreso o gasto. El arreglo obvio era **otro fallo**: el paso 9 de `helpers.ts` ESCRIBE `es_transferencia_interna` y emite evento, o sea justo lo que el usuario había desactivado. De ahí que `planificarTransferencias` devuelva dos campos — `detectar` sostiene el candado y la zona registrada, `marcar` sigue siendo del usuario. Medido antes de tocar: **ninguna org de producción** tiene ese toggle apagado, así que el comportamiento de nadie cambia.

Verificación: **7 mutaciones, 7 víctimas** (aflojar la línea roja en el motor y en el adaptador, aflojar la zona del OCR, quitar el guard de dirección, derivar la zona de `esVerdeAuto`, y las dos direcciones del plan de transferencias). Gate 1465/1465 ficheros, 15.464 tests, `EXIT=0`. La primera corrida dio 5 fallos con duraciones de 17 minutos por test: inanición de CPU (load 12,2), los 5 pasan aislados y la corrida limpia sale verde. Dos guards del pre-push pararon el push y ninguno se rodeó: subido el baseline de `file-size` (+3 en helpers, +1 en el route, que es literalmente la línea de import nueva) y regenerado el grafo de dependencias, que confirma **2 importadores** del módulo nuevo y cero fan-out. `deps:circular` sigue en 22, idénticos a un checkout limpio de `origin/main`: deuda preexistente del patrón `_parts`, ajena a este cambio.

Estado que deja: `AgentesiaLab SL` es la única org de producción en activo (`categorias`, gate abierto) y sus 2 reglas aprendidas están a **2** confirmaciones de las 3 que exige el umbral (`veces_confirmada = 1` cada una; el «a 1» que escribí esa mañana era mío, medido mal). El arreglo entró **antes** de la primera escritura silenciosa, no después.

Esa misma tarde, al auditar el prompt de continuación que dejaba escrito, salieron cuatro agujeros más en el área que acababa de dar por cerrada —`DOMINIOS` a mano tres veces sin candado, `decidirMuestreo` sin un solo test, la degradación del gate que nadie lee ni avisa, y `aprendizaje-ocr.md` contradiciéndose— y un puntero mío a un prompt SUPERSEDED. Los cinco van especificados en [[facturaia-prompt-continuacion-26-ago]] §8. Método → [[un-prompt-de-continuacion-propaga-los-punteros-que-no-abriste]].

## trámites AgentesiaLab · certificado FNMT, VeriFACTU y alta en el ROI (detalle retirado del hub el 26-ago)

En standby por decisión de Manu (24-ago). Texto íntegro tal como vivía en el NOW del hub:

**EN STANDBY por decisión de Manu (24-ago). Los DOS trámites que esperan el certificado FNMT de representante de AgentesiaLab** (corregido 19-ago) — el mismo certificado desbloquea las dos cosas, así que se hacen en la misma tanda:
    1. **`.p12` para VeriFACTU** → Ajustes → VeriFactu (fichero + contraseña, rol propietario/admin) y pasar la org a `verifactu_entorno='prod'`. El gate del paso a prod ya lo pasa: su `regimen_iva` es `general`. Hoy las 9 orgs reales están en `pre` con 0 certificados. **Corrección**: esto NO bloquea la cadena de #1778 — el PR 4 del plan dice literal «NO entra: activar VeriFACTU», y AgentesiaLab lleva **160 facturas emitidas** con `verifactu_activo=false`. Bloquea el **sellado**, no la emisión.
    2. **Modelo 036, alta en el ROI** (#1686) → Sede AEAT → Censos → modelo 036 → **modificación**, apartado «Registro de operadores intracomunitarios». Da el NIF-IVA (`ES`+B27602085) visible en VIES, y **sin él no se puede facturar sin IVA a empresas de otros países UE** (el reverse charge exige que las dos partes estén en VIES; si no, el IVA lo debes tú). Hasta 3 meses y **silencio negativo**. Comprobar al final en el validador VIES. Ojo: el número de casilla (582) sale del issue, **no verificado contra el formulario vigente** — confirmarlo en el propio 036 o con la gestoría, porque la numeración cambia entre versiones. No afecta a clientes españoles ni a particulares.
    Queda también firmar la DR y presentar la consulta a la DGT (`docs/compliance/consulta-dgt-clave-regimen-rere.md`). → [[la-org-emisora-de-tu-propio-saas-no-es-un-cascaron]]
    **MEDIDO el 24-ago contra el validador oficial: `ESB27602085` sale `valid: false`.** O sea que el alta en el ROI NO está hecha, y eso ordena la cadena entera: certificado → 036 → *hasta 3 meses, silencio negativo* → recién entonces se le puede dar el NIF-IVA a Anthropic, OpenAI y GoDaddy. Dárselo antes no sirve de nada: su comprobación contra VIES falla y siguen repercutiendo IVA. **El paso 0 es una pregunta, no un trámite**: el certificado es el mismo con el que AgentesiaLab presenta IVA/IS/Seguridad Social, así que si ya entráis a la sede con certificado, el paso de la FNMT sobra. Guía → `docs/compliance/centro-fiscal-pre-beta/GUIA-CERTIFICADO-Y-ENTORNO-PRE-AEAT.md` §A.
    **No bloquea el 3T**: el motor ya declara bien la inversión del sujeto pasivo (#2122), y el IVA extranjero que te cobran de más es recuperable por rectificativa dentro de los 4 años de cada factura. Lo que se pierde mientras tanto es caja, no derecho — y el cuadre C-15 se lo dice al usuario en cada declaración.

## DR de SIF · detalle retirado del hub el 26-ago

**[ACCIÓN — exigible YA, NO aplazada] Declaración Responsable de fabricante de SIF (RD 1007/2023, art 13)** — _verificado en sede AEAT + Orden HAC/1177/2024 art 3, 2026-06-22_. Aplazamiento RDL 15/2025 = solo USUARIOS, NO fabricante. Autocertificación (no se presenta a AEAT): in-app visible por versión + PDF descargable. Decir "adaptado al RD 1007/2023", nunca "homologado". **Auditoría de código hecha (2 agentes)**: de los 2 "bloqueantes" detectados, (1) **registro de eventos + firma de registros NO aplican** porque somos solo-Verifactu (Orden art 3 exime arts 8/9 y 6.c/d/14); (2) **inalterabilidad (art 8.2.a) cubierta con mig `376_facturas_inalterabilidad_verifactu.sql`** (trigger BEFORE UPDATE, congela contenido fiscal en cadena + huella tras aceptación; **PR #449**, **pendiente merge + `supabase db push`**). **Antes de firmar, cerrar tareas técnicas (no bloqueantes legales):** ~~residuo 1 céntimo huella~~ → _auditado 2026-06-22: NO es bug vivo, ambas rutas (RPC atómico+091 / emit trigger 303:348) calculan con Σ; la rama NOOP es inalcanzable por el advisory lock_; quedan validación XSD oficial, smoke real contra entorno `pre` AEAT, confirmar encadenamiento por-serie vs por-obligado con asesor. Fragilidad Σ duplicado: RESUELTA — totales unificados en #869 (`lib/documents/totales.ts`) y worker/trigger VeriFactu en Fase 5 (`lib/verifactu/cuota.ts`, PR #947). Análisis referenciado: `docs/compliance/centro-fiscal-pre-beta/SIF-declaracion-responsable-analisis.md`. (P12 por org y USO de Verifactu sí diferidos a 2027.)

## 25/26-ago-2026 · la bandeja de soporte a cero (PR #2194, #2198, #2208)

Once tickets en `en_revision`. Tres se arreglaron con código —154 «Copiar enlace», que además resuelve el documento aunque no caiga en la página, los filtros o el orden de quien lo abre; 157 el nombre del producto en Inventario; 134 la densidad de la rejilla del presupuesto, la tercera vuelta que quedó sin reaplicar del #1536—. **Cinco llevaban semanas arreglados en `main` sin que nadie cerrara el ticket** (89, 125, 126, 128, 129): contestados uno a uno, con la divergencia dicha en voz alta (el filtro de materiales arranca en «Todos» porque «Válidos» enseña 1 de 1.296 en el catálogo real de la clienta). Los tres restantes —155/156/158— eran el mismo agujero y se fueron al #2209.

El 157 volvió el mismo día porque quitar la unidad repetida daba aire sin atacar la causa: los anchos iban en porcentaje y la escasez se repartía entre las once columnas, así que el nombre pagaba el ancho de ocho columnas de dos cifras. #2198 lo arregla con anchos fijos de 86 px, `width:auto` al nombre y retirada por prioridad con `@container` —no `@media`: el rail plegable da 1.128 px abierto y 1.400 px plegado con la misma ventana de 1.280—. La pregunta «¿y si quiero ver las que se retiran?» produjo el modelo de tres estados por columna (auto/fija/oculta) con `aria-checked="mixed"`, escalones de ancho mínimo de 86 px y la columna del nombre anclada al scrollear.

#2208 salió del smoke en producción, no de una revisión: con cuatro columnas fijadas y `scrollLeft=250`, tres celdas numéricas se leían a través del nombre. La columna anclada usaba `var(--bg-elev)`, que en el tema glass vale `color-mix(in oklch, white 60%, transparent)` — y el comentario de ese mismo bloque, escrito horas antes, ya decía «tiene que ser OPACO». Arreglado componiendo el cristal sobre `var(--bg)`, con guard que parte el `background` por comas de primer nivel.

Cierre: 0 tickets abiertos, 144 resueltos. → [[una-columna-que-se-retira-sola-necesita-un-tercer-estado]] · [[header-sticky-glass-sangra-mesh-debe-ser-opaco]] · [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]] · [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]]

**Retirado del NOW el 26-ago**: Holded cerrado del todo (#2152/#2160/#2163-65, prod 24-ago), sin cabos — el hallazgo transversal (escribir `last_error` no basta si las superficies exigen `state === 'error'`) vive en [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]. Y el detalle del 303 (#2121/#2122/#2161): 2.644,64 € de líneas que contradecían su cabecera, los SaaS de terceros países a las casillas 32/33, `nif_iva` vacío en 627 de 673 proveedores y la mig 752 que nunca se había aplicado.

## 26-ago-2026 · el albarán deja de ser cosa de Obras (PR #2209, mig 754, ADR-029)

Los tickets **155, 156 y 158 de Pescados Chivite** eran el mismo agujero visto por tres lados:
abrir una partida de varias mercancías sin papeles, asignar los albaranes diarios a la factura
semanal, y dejar de mezclar albaranes con facturas en la misma bandeja. Hasta ese día la app solo
sabía de albaranes dentro de Obras (`obras_albaranes`, mig 506) y Chivite tiene `stock`, no `obras`.

**Lo entregado** (81 ficheros, +8.299/−740): renombrado `obras_albaranes` → `albaranes` sin vista de
compatibilidad (una vista con escrituras vivas por detrás es la segunda verdad con otro nombre),
puente N:M **por línea y con cantidad** `albaran_factura_lineas`, vista derivada
`albaranes_facturacion`, pantalla propia `/albaranes` con entrada en sidebar y menú móvil, panel de
casación dentro del modal de la recibida, alta manual, entrada por foto (el OCR ya clasifica
`albaran`), tool de copiloto `recepcionarAlbaran` y envoltorio `withAlbaranesAuth` (sesión + doble
puerta `stock` o sector Obras, 404 en vez de 403).

**Las decisiones (ADR-029, en el repo)**: el albarán MUEVE stock al validarse, como Odoo/Sage/Holded;
por tanto la factura que agrupa albaranes ya asentados NO vuelve a asentar, y eso se resuelve **dentro
de las dos funciones de Postgres que asientan compras**, no con un `if` en el endpoint —ese `if` se
esquiva desde el copiloto, la API v1, el OCR o un cron—; el eje de facturación **no es columna, es
vista**; y el tercer caso, los dos documentos asentados por su lado, se **rechaza** con `AL014` en vez
de duplicar inventario en silencio. Lo fiscal: RD 1619/2012 + art. 97 y 75.Uno.1 LIVA → el albarán no
entra en 303, 347, 349, 130, 111, 115, cuadres ni VeriFACTU, y eso lo **mide** un test que barre el
motor fiscal en TS y las funciones `fiscal_*`/`verifactu_*` en SQL, verificado por mutación.

**Verificación**: gate entero verde (15.459 tests) antes del merge y otra vez tras integrar
`origin/main`; mutación de los dos guards del doble conteo, víctima en las dos direcciones; cinco
escenarios en Postgres real (`754_…validate.sql`); mig 754 aplicada y comprobada **por catálogo**, no
por el mensaje del CLI; smoke de escritura en prod con navegador contra la org sandbox (alta →
listado con los dos ejes → validar → borrar, `movimientos_revertidos: 0` porque la línea no tenía
producto de catálogo). **No cubierto en prod**: el camino con producto real y lotes, que está probado
por los escenarios SQL.

**Cierre con el cliente**: una respuesta pública por ticket (155, 156, 158), con su email, y los tres
a `resuelto` / `resuelto_via: manual` — el cuerpo del PR no llevaba el trailer `Ticket-feedback:`, así
que el webhook no cerró nada y hubo que hacerlo a mano. Informe end-to-end publicado como artifact
«Entrega antes que factura».

Aprendizajes: [[un-panel-nuevo-dentro-de-un-modal-ajeno-hereda-sus-tests]] ·
[[reserializar-un-json-tracked-lo-reescribe-entero]] ·
[[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]] (siete guards de arquitectura se pusieron
rojos de golpe al hacer `git add -A`, no antes).

## 25-ago-2026 · revisión de toda la IA implementada: 22 sitios, 12 hallazgos, 8 PRs, todos en prod

Auditoría de lectura de las **22 llamadas a un LLM** del repo (copiloto, OCR, conciliación,
VeriFACTU, Obras, marketing, Google Ads, fiscal, playground de voz, inventario). Ninguna era un
fallo visible en pantalla: todas fallaban en silencio, en un log o en una columna que nadie mira.

- **#2185** — la nota de voz de WhatsApp se transcribía (y se pagaba) **antes** de saber quién la
  manda. El pre-gate se movió delante; y comprobado que no autoriza nada: el copiloto vuelve a
  preguntar con las mismas funciones. Y ningún turno del copiloto muere ya en un log: un turno
  cortado por el tope de tokens tiene texto que decir.
- **#2186** — cinco llamadas sin `jsonMode` ni `temperature`, o con el texto del modelo yendo a
  pantalla sin sanear. `sanitizeUserFacingText` sale de `runner.ts` a `@/lib/llm/texto-usuario`
  (el problema no es del copiloto, es de cualquier respuesta que acabe leyendo una persona) y el
  diagnóstico AEAT devuelve **502** en vez de una cadena vacía.
- **#2187** — la extracción de facturas leía a **temperatura 1** (el valor por defecto de la API,
  no el que nadie eligió). Va solo en su PR porque `gotchas.md` §OCR exige comparar evals de pago
  antes y después: 18/18 en `main` limpio, 2×18/18 en la rama. Candado en un test, porque los
  evals cuestan dinero y no corren en el gate.
- **#2188** — `interpretAeatError` podía lanzar por tres vías y su llamador la invoca **antes** de
  escribir la fila del rechazo: la factura se quedaba sin `verifactu_estado: rechazada`, sin la
  prueba de lo que dijo la AEAT, y con un «429» del LLM en el campo que el usuario LEE. La función
  se hace total. Estaba latente (0 facturas con `verifactu_error` en prod).
  → [[un-llm-puede-adornar-un-registro-nunca-condicionar-que-se-escriba]]
- **#2189** — arnés de evals de la pre-validación de VeriFACTU (`npm run eval:verifactu`), y lo que
  encontró en su **primera corrida**: un NIF de emisor inventado (`XY1234`) pasaba con
  `valid: true`, tres de tres. Se arregla donde el propio fichero ya decía que se arregla —en TS,
  determinista— y no con más prompt. Medido antes de mergear: **0 de las 9 orgs reales** de prod
  tienen un NIF que el validador rechace.
  → [[lo-que-se-puede-calcular-no-se-le-pregunta-al-modelo]]

- **#2190** — los tres arneses de evals que faltaban de las llamadas de texto: `eval:conciliacion`
  (8 casos sobre el enriquecedor de movimientos), `eval:obras` (5 sobre el generador de
  presupuestos) y los 6 de `enriquecer-materiales`. Los parámetros de cada llamada salen a
  constantes compartidas (`ENRICH_LLM_PARAMS`, `GENERADOR_LLM_PARAMS`, …) para que el eval mida lo
  que corre en producción y no una copia que deriva. **Dos lecciones del arnés**: un caso de eval
  que duplica lo que ya prueba un test determinista no es cobertura extra, es coste extra con ruido
  encima (se quitó el de `redactPII`, que el modelo absorbía); y un fallo del eval es antes una
  aserción mía equivocada que un defecto del sistema — el de la inyección en el concepto bancario
  lo era.

- **#2191** — las tres rutas que el censo no vio, porque llaman al SDK **sin pasar por el wrapper**.
  Dos con defecto real: el **explicador fiscal** pedía la explicación con `maxTokens: 500`, no
  miraba `finishReason` y la cacheaba por hash en `fiscal_explicaciones` — un texto cortado a media
  frase no se servía una vez, se servía para siempre. Latente: las 6 explicaciones de prod acaban
  las 6 en punto y la más larga son 841 caracteres (~230 tokens de 500). Y el **playground de voz**
  de `/admin` probaba prompts **sin `temperature`** (la API va a 1) mientras el runner que contesta
  los WhatsApp va a 0.2: el admin afinaba contra un modelo que no es el que responde. De propina,
  ese panel pinta tokens y coste desde que se escribió y el endpoint nunca le mandó `usage`, así
  que ese badge no se había visto nunca. La tercera, `inventario/importar/analizar`, estaba bien.
  → [[censo-de-llamadas-al-llm-por-el-helper-no-ve-al-sdk-a-pelo]]
  Smoke en prod con el build ya desplegado, conduciendo el navegador: el playground responde y por
  fin pinta su badge de coste (**789 in · 334 out · ~0,0023 €**, que es la prueba de que corre el
  build nuevo: ese `<span>` no existía antes), y «Explícame esto» en un 303 2T de sandbox generó
  texto completo y **escribió fila nueva** en `fiscal_explicaciones` (19:11:44Z, acaba en punto).
  0 `system_alerts` nuevas.

- **#2192** — el candado del método: un censo por **el import del SDK**, que es lo que no se puede
  evitar, contra cinco excepciones declaradas con su motivo (dispatcher, runner del copiloto,
  whisper de audio, `verifactu/ai-error` con su timeout propio y el playground que espeja al
  runner). Barre **todo el repo trackeado**, no solo `src/`, porque `services/` y `scripts/` son
  código que corre igual (hoy 0 de 297 ficheros fuera de `src/`, mañana quién sabe); `import type`
  no cuenta y los tests quedan fuera. Un segundo test tumba las entradas obsoletas para que la
  lista no acabe siendo un cementerio. Cuatro dientes probados, incluido el script fuera de `src/`,
  que es justo lo que gana el barrido ampliado.

**Un hallazgo del método, no del código**: los dos arneses de evals imprimían su reporte con
`console.info` y **vitest descarta la salida de los tests que pasan**. Tres corridas verdes sin una
línea de log. → [[un-gap-que-no-se-lee-es-un-gap-que-nadie-cierra]]

Verificado en prod tras el deploy: `/api/health` ok, 0 `system_alerts` nuevas en 90 min y un smoke
real del copiloto en navegador (pregunta → tool ejecutada → 3 facturas listadas), que recorre la
línea exacta que se tocó en `/api/copiloto/message`.

## 22-ago-2026 · el arnés, los casts y el smoke que sacó el #2100

- **#2096**: ningún hook corría `vitest`. `npm run gate` (lint && typecheck && test && build) solo se
  corría a mano, así que «hooks en verde» no incluía los tests — y por eso #2077 dejó `main` en
  `1 failed | 14613 passed` (arreglado en #2094). La suite corre ya en `pre-push`, antes del build.
  Probado con un test roto sembrado en un fichero EXISTENTE: uno nuevo aborta antes, en el check de
  deriva del grafo. De paso, `if ! cmd; then rc=$?` capturaba 0 en los dos bloques.
  → [[pre-push-que-typechequea-con-next-build-no-mira-los-tests]]
- **#2097**: tres casts `as unknown as` con el mismo comentario falso («`billing_accounts` aún no está
  en los tipos generados»). Uno sobraba; otro tapaba que el `select` estaba concatenado y supabase-js
  pierde la inferencia; el tercero se queda, con su motivo real escrito.
  → [[supabase-js-select-con-embeds-necesita-string-literal-no-concatenado]]
- **#2098**: la gobernanza listaba como deuda prioritaria un `pre-commit` que ya corría lint+typecheck.
- **#2099 / #1919**: `supabase start` sí aplica las 746 y siembra; muere levantando `vector` con colima
  y al caerse tira el stack. `-x vector` → ec=0. La causa declarada en #1919 (mig 643) era falsa.
  → [[supabase-start-colima-macos-vector-container-falla]]
- **Smoke en prod** (navegador): #2080a, #2085a, #2085b, #2087 y #2088 verdes; #2077, #2079 y #2080b no
  alcanzables con los datos de prod. Salió el **#2100**.
  → [[update-que-afecta-cero-filas-no-devuelve-error-en-postgrest]]

## 21/22-ago-2026 · tandas cerradas retiradas del NOW

- 🟢 **Cerradas: growth/contenido/cookies (7 PRs, 21-ago) · spec #1908 (queda #1959, sin urgencia) · empaquetado ola 5 (quedan #1813 y #1936)** — **Tuyo (pre-campaña)**: abogado ADR-023 + Safari ITP; token Meta ~10-oct. Detalle → [[facturaia-historico-detallado]] · [[proxy-de-next-trunca-el-body-a-10mb-y-rompe-firmas-hmac]] · [[gate-que-exige-el-artefacto-a-la-fase-que-lo-produce-es-deadlock]]

## 22-ago-2026 · multidivisa recibidas, cierre del área

- Sin filas congeladas en prod, barrido diario verde a las 04:20 y el aviso de desvío >5 % en pantalla (#2089-#2092). Del S4 quedó solo la notificación en campanita. → [[facturaia-multidivisa-recibidas]] · [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
- Conciliación: 0 discrepancias mirror↔N:N, 0 huérfanas y 0 sobre-cobros (#1932/#1979).

## 18-ago-2026 (noche) — once PRs en el día, y los dos incidentes los causé con herramientas del repo

Segunda tanda: **#1882** (trinquete `series-formato-guard`), **#1883** (tipos al día + `gen:types`
blindado + migs 709/710 sin consumidores), **#1884** (aviso de `requires_recalc` en hub y calendario),
**#1885** (§13 del plan: el PR 2 bloqueado), **#1886** (PR 1b: guards de serie protegida),
**#1887** (el aging deja de dar la baja de WhatsApp por irreversible).

Cierre medido sobre `main` mergeado: 1.250 ficheros, **12.934 tests**, 0 fallos, lint y typecheck
limpios, `gen:types:check` en 0 y prod en la **710**. 1 worktree, ramas de la tanda retiradas.

- **Dos incidentes, los dos míos y los dos recuperados**: `gen:types` truncó el fichero de tipos antes
  de fallar (401), y un `\i` de migración dentro de un `BEGIN … ROLLBACK` de prueba ejecutó su `COMMIT`
  y dejó una función creada en prod. Detalle en `Stack/incidents.md`.
- **La nota del `>` llevaba escrita dos veces desde el 7 y el 11 de agosto y no impidió nada**, porque
  nadie había cambiado el script. Ahora hay script, test que prohíbe la redirección y `--check` de
  drift. → [[redirigir-con-mayor-que-destruye-el-fichero-antes-de-arrancar-el-comando]]
- **Decisión: el PR 2 de #1778 no se escribe** contra un fixture inventado. 0 invoices/subscriptions
  en live, ninguna clave de sandbox, y el repo no usa el SDK de Stripe, así que nada validaría la forma
  de un objeto del que se mapean importes fiscales. Bloqueado en la `sk_test`, y arrastra PR 3 y PR 4.
- **Decisión: la serie protegida va en el dato**, no en `SERIES_RESERVADAS`, que se deriva de
  `SERIE_BY_TIPO`. → [[una-lista-derivada-no-admite-excepciones-la-marca-va-en-el-dato]]
- El arnés de mutación destapó **dos tests sin dientes** en el trinquete nuevo, y el caso del comentario
  SQL necesitó tres intentos hasta discriminar.

## 18-ago-2026 (tarde) — las tres ramas en prod, y los dos PRs que nadie había planeado

Cinco PRs mergeados: **#1877** (candado de idempotencia de #1778, mig 708), **#1880** (el formato
de serie de esa migración), **#1878** (las 8 lecturas del inventario que PostgREST cortaba a 1.000
filas, 6 tests), **#1879** (ADR-019: el export fiscal `oficial` con gate de servidor, y el 500 del
fichero oficial), **#1881** (la FK del candado justificada en el guard de `recibida_eliminar`).

- **Prod en la 708**, verificada por catálogo: tabla con 4 índices y RLS, `stripe_suscripcion` en el
  CHECK de `factura_pagos.origen`, serie `X`, override de cuota y `facturas.stripe_invoice_id`.
- **El `db push` murió a mitad** con un 23514: la migración copió el formato de serie del `DEFAULT`
  del `001_schema.sql`, que la mig 021 dejó inválido meses antes. Sin daño: `BEGIN`/`COMMIT`
  explícitos → rollback total. Antes de reintentar se auditaron los otros cinco statements contra el
  catálogo de prod. → [[default-del-schema-inicial-puede-estar-invalidado-por-un-check-posterior]]
- **La suite completa sobre `main` mergeado volvió a pagar, segundo día seguido**: rojo por un guard
  estructural (toda FK bloqueante a `facturas` la debe desenganchar `recibida_eliminar`). Justificado
  en su ALLOWLIST con el porqué, y comprobado por mutación que el guard sigue discriminando. Cierre
  verde: **12.881/0 en 1.244 ficheros**, lint y typecheck limpios.
- Las dos mutaciones pendientes de la tanda anterior, con víctima: el gate de `requires_recalc` y el
  em-dash de `STATUS_303_POSICIONAL`.
- Limpieza: 3 worktrees y 5 ramas de la tanda retirados, más 16 ramas `worktree-agent-*` muertas
  (ninguna con commits propios). Queda 1 worktree, el repo raíz.
- El conflicto de las tres ramas era el mismo: el SVG del grafo de dependencias. Se resuelve
  regenerando desde el código fusionado, no eligiendo lado.

## 18-ago-2026 — cierre de los tres pendientes: #1712 cerrado y #1778 listo para construir

- **#1712 CERRADO** (PR #1875). AC5: la cabecera de la matriz de empaquetado muestra el recuento de
  organizaciones **por plan efectivo**, dato que ya viajaba en el payload (`orgCounts`) y solo se
  veía en el modal de apagado. Cero se escribe «Sin organizaciones». `--fia-head-h` 40 → 52 px
  porque la variable la comparten la altura del `th` y el `top` de las filas de categoría sticky.
  Deuda anotada que sigue viva: ese recuento lee `organizations` sin paginar (PostgREST corta a
  1.000 en silencio) y ahora se ve en pantalla.
- **#1778: el plan ya existía** desde el 15-ago (#1828) y el prompt de arranque lo daba por
  pendiente. Se restauró intacto y se le añadió una §11 (74 líneas, 0 borradas, PR #1876) con tres
  decisiones —serie dedicada, la org emisora que ya existe, construir con flag— y cuatro huecos:
  el gate de cuota (override en `org_limits`, no un `skipQuota`), la factura que nacería
  `pendiente` y entraría en reclamación, los complementos que resuelven la empresa por su
  suscripción y no por el customer (ADR-016 §7.4), y el punto de partida remedido.
- **#1686 cerrado salvo el 036**: NIF `B27602085` por defecto, email de soporte y descriptor
  `TUFACTURAIA`. El domicilio fiscal nunca estuvo vacío, contra lo que decía el issue.
- **Empaquetado ola 4** (#1713, #1714, #1708, #1715, #1751, TOCTOU, #1837): cerrada el 17-ago,
  migs 706/707 en prod. Siguiente ola → `docs/architecture/PROMPT-empaquetado-fase2-ola5.md`.
- **Contenido spec #1791**: 7/7 en prod desde el 17-ago (pestañas, publicar en IG, Ads en PAUSED;
  migs 698/703/699, ADR-014 y ADR-015).
- Gate sobre `main` mergeado: lint · typecheck · build · Vitest **12.858/0** en 1.236 ficheros.
- Learnings: [[la-org-emisora-de-tu-propio-saas-no-es-un-cascaron]] ·
  [[facturar-lo-ya-cobrado-sin-registrar-el-cobro-lo-mete-en-reclamacion]].

## 17-ago-2026 — `crm_link`: el vínculo TuCRMIA↔FIA deja de exigir Enterprise (#1844 / PR #1847, `551f36021`)

TuCRMIA se integra pegando una api key de la propia org del cliente; nace `key_type='cliente'` (mig 685) y el gate de #1700 le exigía `api_access`, que solo tiene enterprise (mig 399:252). Por debajo, el primer `POST /v1/clientes` daba 403 y el paquete CRM+FIA no podía ser autoservicio.

**Decisión (ADR-018, en el repo):** feature `crm_link` como SEGUNDA llave del mismo gate, estrecha, habilitada en los **cuatro planes** (mig 700). No abre la v1: abre 15 endpoints (clientes, presupuestos, factura en lectura, `org/perfil`). `api_access` intacta y enterprise-only.

- **Por qué allowlist de endpoints y no scopes**: con `clientes:*` + `presupuestos:*` + `facturas:*` se colaban `proveedores/*`, `catalogo/*`, `fiscal/*`, `resumen`, `clientes/top`, recibidas, `anular` y `marcar-cobrada`. → [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]]
- **Por qué en los cuatro planes**: el vínculo ya se cobra en el CRM; cobrarlo aquí sería cobrarlo dos veces. Zoho/HubSpot lo hacen así, Salesforce es el contraejemplo. → [[la-integracion-entre-productos-propios-no-se-cobra-como-acceso-a-api]]
- **Medición de prod que lo sostuvo**: 9 orgs reales (8 enterprise, 1 starter); 14 api_keys, las 14 `interna` → el gate de #1700 no bloqueaba aún a nadie. `api_access` **no** es complemento comprable, tiene `visible=false` y no se pinta en el highlight de plan (cae fuera del `slice(0,2)` tras `fiscal` y `antifraud`). Lo que se cobraba era el delta de plan (99 vs 49).
- **Rojo medido**: barrido de mutación 3/3 con víctima (quitar el estrechamiento → 3 rojos; no comprobar el derecho → 2; desincronizar una etiqueta → 1).
- De paso: `docs/qa/inventario/gating.md` decía «api_access → Pro+», falso desde la mig 399.

## 17-ago-2026 — la v1 gana webhooks y estado de cobro (#1849 `9b7dc07c9` · #1850 `8fe6716ac` · #1851 `ce89a78d0`)

**El vínculo TuCRMIA↔FIA queda COMPLETO**: las cuatro piezas (#1844 `crm_link`, #1849, #1850, #1851) en prod el mismo día.

- **#1849 — `GET|POST /v1/webhooks`, `PATCH|DELETE /v1/webhooks/{id}`, `POST /v1/webhooks/{id}/test`.** El scope `webhooks:manage` existía desde la **mig 025 sin un solo endpoint detrás**: activar una integración exigía que alguien de la casa entrara a Ajustes por cada cliente. → [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]]
- **#1850 — `GET /v1/facturas/{id}` publica el estado de cobro** (cobrado y pendiente cobrable), que es de lo que depende #1851.
- **#1851 — `factura.cobro_registrado` (mig 705)**, evento NUEVO en vez de ampliar `factura.paid`: cambiarle el disparador habría hecho que un CRM diera por cobrada una factura a medias, y en un webhook eso no da error. Emite también al ANULAR un cobro. Smoke en prod con `ROLLBACK`, 5/5: el payload salió con `estado: parcial` cuando la factura estaba en `pendiente`, que es lo que **demuestra** que las cuatro `z` del nombre del trigger lo hacen correr después del recompute.
- **Lo que destapó el barrido de mutación**, y no la revisión: un contrato que aseveraba el `import` de `deliverOne` en vez de su llamada (6 tests verdes con la protección anti-SSRF sustituida), y cinco tests de la aritmética de `pendienteCobrable` que no cubrían el cableado del DTO (`yaCobradoEur: 0` seguía verde — el pendiente habría ignorado todo lo ya pagado). → [[aseverar-sobre-el-import-no-asevera-sobre-la-llamada]] · [[probar-la-aritmetica-no-prueba-el-cableado-que-la-invoca]]
- **Tres marcadores que mentían, cazados entre dos sesiones paralelas**, los tres con la misma forma —la herramienta no miente, CALLA, y el silencio se lee como conformidad—: `gh pr merge --delete-branch` sale con EC=1 habiendo mergeado (3 veces, reproducible con worktrees vivos sobre `main`); `mig:renumerar` y el `pre-push` fallan abiertos dentro de un worktree; y `Cierra #N` en español no cierra el issue. → [[numero-de-migracion-libre-se-mide-en-prod-no-en-el-repo]] · [[keywords-de-cierre-de-github-solo-funcionan-en-ingles]] · [[gh-pr-merge-delete-branch-no-borra-la-rama-si-falla-su-checkout-local]]
- **Y un gate que muerde donde no lo esperas**: `madge` indexa `__tests__/`, así que un PR cuyo diff es «solo un test» mueve el grafo de dependencias y el `pre-push` lo para. Verificado dos veces el mismo día, en dos sesiones distintas. → [[madge-indexa-los-tests-asi-que-anadir-solo-un-test-mueve-el-grafo]]
- **Abiertos con medición, no con sospecha**: **#1856** (el embudo de reclamación no ve el ledger de la mig 640 — 0 filas afectadas hoy) y **#1858** (nadie barre las dependencias entre features que YA existen en prod — 0 de 17 violadas). Los dos documentan riesgo latente sin vigilancia, no incendio.

## Poda del hub del 07-ago-2026 (noche) — tres entradas cerradas sin pendientes

- 🟢 **Panel de tickets: quién cerró, cuándo y por qué vía + filtros con contador (06-ago noche, #1528 · #1529, mig 651)** — `resuelto_at`/`resuelto_por`/`resuelto_via` (`manuela` = el runner · `manual` · `sin_codigo`), backfill desde `admin_audit_log`: **62 manuela · 53 a mano · 11 sin código**, ninguno sin registrar (los 59 que el backfill dejó en NULL, clasificados leyéndolos uno a uno el 07-ago; traza en `admin_audit_log`). Pestañas con contador (Sin abrir · Sin leer · Te toca · **Sin responder** · **Listo para cerrar**), hilo del revés con el compositor arriba, ⌘+Enter y ← → entre tickets. Destapó que **7 de los 8 abiertos no tenían ni una respuesta nuestra** y no salían en ningún filtro. Verificado conduciendo el navegador. Nada pendiente. → [[un-filtro-definido-por-el-ultimo-elemento-no-ve-la-lista-vacia]] · [[el-audit-log-suele-tener-el-dato-que-le-falta-a-la-columna-nueva]] · [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]]
- 🟢 **Tanda de soporte 133-138 + fiscal, en prod (06-ago, #1525-#1527, migs 648-650)** — 6 tickets resueltos. Destapó, con la suite en verde: coste previsto entregado MUERTO (nadie lo escribía), abono recibido con cuota 0 en el 303 (y el fichero AEAT sin poder generarse), y una migración registrada sin aplicar. Ninguna declaración presentada afectada. → [[campo-numerico-opcional-omitido-suma-cero-y-parece-dato]] · [[fiscal-rectificativa-recibida-va-a-casillas-40-41-no-a-28-29]] · [[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]]
- 🟢 **`/fia-cierre`: $34,72 → $5,29 por pase, MEDIDO tras estrenarlo (07-ago)** — el 94 % del coste era contexto rearrastrado, no razonamiento. Diff inyectado, 4 dimensiones en vez de 9, Sonnet en las mecánicas. **236 tool calls → 60**, 19 min → 8. Alcance por `scripts/cierre-alcance.mjs` con 14 tests que comprueban lo que APAGA y verificado por mutación (5/5 cazadas). Estrenado sobre su propio PR: **0 bloqueantes**, y cazó 2 bugs reales de formato ya arreglados. Registro en `docs/plan/cierres.json`. → [[el-coste-de-un-fanout-de-agentes-es-contexto-no-razonamiento]]

## Poda del hub del 08-ago-2026 — dos entradas cerradas retiradas del NOW

- 🟢 **Coste/hora medio: PUESTO en IET, 21 €/h (07-ago noche)** — Natalia lo dio «de momento» y quedó escrito en `obras_settings.coste_hora_mo` por el endpoint real impersonando, no con SQL suelto. Cerrado el aviso de pendientes. **Ojo al tocar esos ajustes**: guardarlos dispara `trg_obras_recalcular_por_settings`, que recalcula los 7.683 materiales de la org aunque el campo escrito no entre en el precio. Salió no-op (foto antes/después idéntica byte a byte, suma 1.071.146,80 €), pero solo porque la mig 656 los dejó cuadrados horas antes y nadie tocó los inputs. Si alguien hubiera cambiado tarifas o descuentos por medio, ese guardado se los publica al cliente sin pedirlo. → [[escribir-un-campo-que-no-entra-en-ninguna-formula-dispara-igual-el-recalculo]]
- ⚪ **`obras-091` (volcar los 7.707 descuentos de WAPI): DESCARTADO por Natalia el 02-ago** — muchos están desactualizados y otros son de proveedores con los que ya no trabaja; volcarlos propagaría datos obsoletos. Los alimenta por tres vías: lo que le manden los proveedores, lo que salga de las facturas (`obras-086`, ya construido y consciente de fabricantes: avisa de los que tienen acuerdo propio) y lo que ya tiene. Los dos cabos que había apuntados en el hub caen con el volcado.

## Copiar el catálogo de WAPI a la org real — RETIRADO el 07-ago-2026 (condensado en el hub el 08-ago)

Contradecía tres decisiones de Natalia del 2-ago escritas en `docs/architecture/obras/decisiones-migracion-iet.md` (§1 el orden, §2 «el catálogo se construye desde las tarifas, no heredando el de WAPI», §4 sus artículos propios los repasa ella antes). Y medido: el catálogo copiado **valdría 4,72× lo que IET cobra de verdad** (repricing de las 11.632 líneas de sus 554 presupuestos aceptados: 4,4 M € reales → 20,8 M €), porque el origen tiene 0 proveedores y 0 marcas, y `obras_descuento_aplicable` exige marca hasta para el descuento genérico de familia. Además el criterio de universo era falso: **2.486 de los 2.832 «nunca usados» sí se habían comprado** (constan en 28.149 líneas de pedido y 26.360 de albarán). Y los 554 presupuestos aceptados que se iban a descartar son el **único corpus del generador IA** (la RPC filtra `estado IN ('aceptado','ampliado')` por org). El camino que ella aprobó llega al 99,9 % de las UO sin nada de esto, y la herramienta ya existe (`scripts/wapi-uo-casado.mjs` + cascada).

## Tanda de soporte 142-145 + objetivo táctil del Segmented — cierre del 08-ago-2026

Cuatro tickets de IET sobre `/obras/presupuestos/[id]`, más una deuda de accesibilidad que había dejado documentada el gate de otra sesión. Todo en prod y contestado con captura en el propio ticket.

- **144 (el peor, y no era estético)** — llegó como «se superpone el texto al cuadradito». La columna congelada dejaba pasar lo de debajo por DOS causas a la vez: la celda fijada medía su contenido (18 px) y no la fila (37), y el `<input>` `opacity:0` del Checkbox compartido (`z-index:2`) ganaba a las celdas fijadas (`z-index:1`) en el contexto de la rejilla. Consecuencia real, medida con `elementFromPoint` a 612-632 px de desplazamiento: pulsar la casilla de seleccionar partida marcaba el tic «Instalación (CMO)» y le movía el precio a la línea. Fix: `isolation: isolate` + `align-self: stretch` + `z-index: 3`. Guard `presupuesto-columna-congelada.test.ts`, que lee el `z-index` DEL PRIMITIVO en vez de fijarlo; tres mutaciones matan casos. → [[columna-congelada-se-tapa-con-altura-y-con-apilado]]
- **142** — el cliente del presupuesto solo existía como UUID en la pantalla. Ahora sale en el encabezado con enlace a su ficha; la consulta va en el endpoint web y NO en `getObraPresupuestoDetail`, que `obra-arbol-db` llama una vez por presupuesto ligado a la obra. Cabecera plegable con preferencia recordada: «Partidas» sube de 841 px a 409. Plegada sigue diciendo los descuentos globales, que multiplican el importe de todas las partidas.
- **143** — la partida de material era texto muerto (casi la mitad de las líneas de un presupuesto). Ahora abre la misma ficha que ya se veía dentro de una unidad de obra: `PartidaComposicionModal` acepta `materialId` y salta el desglose, que para un material no existe.
- **145** — el reloj de la línea recongelaba precio y coste sin preguntar. Ahora confirma con el importe actual delante y dos avisos: sin descuento de proveedor se coge la tarifa a pelo (el salto de 1.583 € a 5.999 € del ticket 137) y no hay deshacer, porque el `coste_hora_mo` anterior no se historiza. No hay vista previa del precio nuevo: el PATCH de UNA línea no simula, escribe.
- **Respuestas 136 y 137** — contestada la confusión del fabricante (no es «un fabricante con varios proveedores», es la misma familia y el mismo proveedor con varios fabricantes y descuento distinto: 183 parejas medidas en sus datos) y cerrado el 137 confirmando que la obra nace al aceptar el presupuesto y que las ampliaciones son versiones nuevas.
- **Segmented (#1549)** — el área pulsable de una opción medía 20 px contra los 24×24 de WCAG 2.5.8 AA; el riel sí cumplía, y ahí estaba la trampa. Extendida con un pseudo del hijo sin tocar la caja visible: 20 → 26 px medidos en navegador, sin solape entre opciones adyacentes. Deliberadamente NO se estira a 44 en táctil: desbordar la caja del control le roba el toque al vecino de la misma fila. → [[el-objetivo-tactil-de-un-control-compuesto-es-su-hijo]]
- **Coordinación entre tres sesiones a la vez sobre los mismos ficheros de `ui/`** — lo que funcionó: anunciar alcance ANTES de escribir, verificar las cifras de la otra sesión en su worktree en vez de creerlas, y quedarse las dos mitades al resolver el conflicto de `manual-admin.md`. Un recado mío resultó falso (que el censo de tap targets habría que regenerarlo tras el cambio de alturas) y lo corrigió quien lo midió: el detector cuenta tallas declaradas en el JSX, no alturas resueltas.

## Módulo Obras — entrada retirada de `top-of-mind` el 03-ago-2026

**Módulo Obras (mini-ERP instalaciones, sustituye WAPI) EN PRODUCCIÓN.** Núcleo + FASE 2 + **FASE 3 (PR #999, 18-jul)** mergeados a main y con smoke prod verde. FASE 3 = decisiones de Natalia: coste MO fiel (tarifa por instalador, precio hora especial por obra, dieta default, calendario mensual de partes), módulo **Herramientas** (foto+event log+alta por WhatsApp vía copiloto), corregir descuento/precio desde recibida, **proforma a origen** (informe PDF, NO createDocument, ADR-obras-001), generar pedido desde presupuesto con expansión de UO, chip recibido X/Y. Migs 471-511 reconciliadas (schema_migrations local==remote). `/fia-cierre` cross-issue cazó 2 bloqueantes que los gates por-issue no vieron (`.or()` sin entrecomillar en tools copiloto con test mock no-op → ver [[postgrest-or-no-escapa-delimitadores]]; clave React/dedup rota al componer olas). **Org REAL de Natalia**: "Instalaciones Eléctricas y de Telecomunicación, S.A." (`b9d5d6f7-…`, is_test=false, creada 16-jul, miembro `administracion@iet.es`). Sembrado el catálogo de **745 tipos M.O.** (copiado del Sandbox, suma horas 3826,901 idéntica, 18-jul). Docs `docs/architecture/obras/fase3-plan-decisiones.md` + ADRs 001/002/003.

## Obras — IA/WhatsApp/MCP: dos entradas retiradas de `top-of-mind` el 03-ago-2026

Ambas describen trabajo ya EN PROD (19-20 jul). Se retiran del arranque porque su narrativa
(2.750 chars) se pagaba en cada sesión; los smokes que seguían pendientes quedan en una línea
del `top-of-mind`.

- **TuFacturaIA — Obras-IA: 14 issues + hardening/QA + confirmación de enriquecimiento EN PROD (obras-060..086 + #1094/#1096/#1097, 20-jul)** — descripción auto + clasificador M.O. + presupuesto conversacional, todo desplegado (incl. fix Telematel columnas, tope-1000 diff, drag-scroll ratón, desglose precio con MO). **Confirmación de enriquecimiento HECHA** (mig 529): la descripción IA ya no se ve al cliente sin OK; bandeja de sugerencias (aceptar/rechazar desc + tipo MO). **Precio con MO** (#1098-#1100): desglose con tooltip "cómo se calcula", suma cuadrada, y FIX de fondo — material sin proveedor se valoraba a 0 (catálogo entero a 0 € tras importar Telematel); ahora coste = base de tarifa ×(1+margen), mig 530 recalculó prod. **Desglose auditable por componente** (#1102 + fix #1105, migs 531/532, 20-jul): cada línea muestra su aportación (€/h "Aporta") + efecto del descuento (bruto→neto) + tooltip; `/fia-cierre` cazó un bug de precio-0 en UO con sub-UO vacía (array sin COALESCE + parse estricto) → arreglado y verificado en vivo. **Pendiente:** smoke prod presupuesto conversacional WhatsApp + que Manuel confirme visualmente los precios recalculados tras el deploy de #1100 (smoke P0.4 `test:integration` de `uo-calcular-desglose` ✅ verde 2026-07-21). [[facturaia]]

- **TuFacturaIA — Obras: IA + WhatsApp + MCP COMPLETO (7 PRs #1018/#1024/#1027/#1031/#1026/#1028/#1033, 19-jul)** — copiloto (generar presupuesto NL / explicar precio / insight desvío + imputar parte / aceptar presup. / pedidos / salida / recepción albarán), multimodal (enrutado por intención, factura default seguro), MCP paridad obras (15 tools read+write draft, `/api/v1/obras/*` user-token-only, guard api_key→404). **MCP redeployado 3× a mano, 48→64 tools verificado**. Aditivo, doble-gated, sin frontera fiscal, revisiones adversariales limpias, 3.3 rebasada sin revertir ajeno. **Smokes pendientes (Manu)**: WhatsApp + MCP con token. Follow-ups CERRADOS 19-jul: umbral margen configurable (#1035), single-source copiloto pedido/albarán (#1038), OCR estructurado del adjunto + clasificación por visión (#1039). **20-jul (+smoke real WhatsApp)**: manuales (#1041), negrita `**`→`*` (#1060), **resolución tolerante de entidades** (#1068, prompt v34: materiales fuzzy + obra/proveedor/instalador AND-palabras + `buscarMaterialesObra` + fix generador; causa raíz = el copiloto usaba `buscarCatalogo` genérico ciego a `obras_materiales`, ver [[copiloto-entidad-tabla-propia-necesita-tool-busqueda-y-regla-en-prompt]]). Mig 523 aplicada. E2E verificado en BD: parte (210 €). **Pendiente Manu (tras deploy #1068)**: pedido/salida/albarán + foto factura-sin-caption→factura. Ver [[namespace-v1-reservado-user-token-para-sacar-campo-del-contrato-api-key]]. [[facturaia]]

## Retiradas del dashboard en el cierre del 06-ago (ya cerradas, engordaban el arranque)

- **[03-ago, #1514] Prod y repo reconciliados: 626…637 contigua, sin duplicados** — obras-095 se mergeó sin renumerar a conciencia: sus migraciones ya estaban aplicadas y moverlas habría dejado `schema_migrations` con las dos numeraciones. Regla: con un PR paralelo en medio manda la BD, y se valida con `uniq -d` sobre los números, no mirando el hueco. Ver [[el-hueco-libre-de-migraciones-puede-estar-ya-ocupado-en-produccion]]
- **[03-ago, #1513, mig 637] Latido del runner de tickets, en prod y verificado** — sin cola, un runner muerto era idéntico a uno ocioso (4 h muertas el 02-ago). El sello va dentro del claim, no en un healthcheck aparte que también se puede quedar sin desplegar. Ver [[dockerfile-que-lista-modulos-uno-a-uno-mata-el-servicio-sin-fallar-el-build]]
- **[03-ago, `obras-095`, #1514, ADR-obras-008, migs 630-636] El descuento cuelga del fabricante, en prod** — clave `(org, proveedor, familia, marca)`, gana la más específica y un material sin marca no hereda. Desbloqueó `obras-091`. Al aplicar no se movió ni un precio: el ADR predecía 11.595 materiales subiendo y esa sandbox tenía 0 enlaces material-proveedor. Ver [[una-prevision-de-impacto-que-no-mira-el-join-que-conecta-sobreestima]]
- **[08-jul, #802, mig 449] Cutover de la cola de OCR, resuelto** — cron `ocr-dispatcher` dado de alta y verificado. Lo que quedaba vivo (el smoke) sigue en la sección Smoke del hub.


## Movido del hub en el cierre del 2026-08-06 (poda por trinquete de contexto)

- ~~PR #851 (v1 rechaza `tipo:'abono'`)~~ ✅ **RESUELTO 2026-07-13** — decisión Manu: agency-portal NO crea abonos vía `POST /api/v1/facturas` → mergeado (`d5bb63a4`). Canal correcto = `POST /v1/facturas/{id}/anular`.
<!-- RESUELTO 2026-06-22 (verificado por screenshot): Supabase Auth URL Config OK — Site URL = https://app.tufacturaia.com + 5 redirect URLs (app.tufacturaia.com/**, /invitacion, /invitacion?org=*, /api/auth/callback, /api/auth/callback?type=*). NO se añade localhost:3000 a un proyecto PROD (superficie de ataque innecesaria; el wildcard de prod ya cubre, y el reset usa admin.generateLink con URL propia). Cerrado. -->
- **Reempaquetado planes — casi cerrado** (act. 2026-06-26): mig 399 (#509) + Fase 2B (#513) aplicadas a prod ya cubrieron ~~grandfathering~~ ✅ (PASO 1, override `source='grandfathered'`), ~~Starter canónico 14€~~ ✅ (PASO 0, reconciliado desde 19), ~~sidebar candado~~ ✅ (#513). **Queda vivo**: (1) ~~crear prices Stripe live de Plus~~ ✅ hechos y activos (verificado 29-jul por API); (2) verificar que `stock` en beta no se cobra como add-on de pago (mig 399 PASO 6 tocó incoherencias de add-ons — confirmar). Detalle: [[facturaia-reempaquetado-planes]]


### Pagadores fase 1 — cerrada 2026-08-06 (migs 640→645, PR #1520)

Ledger `factura_pagos` para cobros sin movimiento bancario, `factura_cobros_resumen` como fuente única de la suma, `recompute_factura_estado` como único escritor del estado. Historial de cobros en la ficha y señal `pagador` en el score de conciliación.

Tres incidencias de la propia fase, todas encontradas por el gate de cierre y corregidas:

- **mig 643** — la 641 había hecho `GRANT EXECUTE ... TO authenticated` sobre `factura_cobros_resumen`, SECURITY DEFINER sin filtro de org: PostgREST la exponía con el anon key del bundle. Reproducido en prod. 6ª reincidencia del patrón → cerrado además con el hook `revoke-guard`.
- **mig 644** — la 640 convirtió `facturas.estado` en derivada sin backfill: 1.385 de 1.403 cobradas volvían a `pendiente` con `fecha_cobro` a NULL en cualquier recálculo (15 de 15 medidas). 1.312 filas de respaldo.
- **mig 645** — el backfill de la 644 se acotó con `pendiente_eur > tolerancia` y su verificación preguntaba lo mismo, así que se validó a sí misma: quedaban 99 de 108 negativas cayendo (88 emitidas históricas con total negativo + 7 abonos + 4 vencidas), no «7» como se reportó al muestrear las 60 más recientes. `target_eur` pasa a `ABS(...)` y 95 filas más de respaldo.

Estado final verificado sin muestrear: 1.444 cobradas/pagadas de producción recomputadas, 0 cambian de estado.

### Lo que destapó el /fia-cierre de la fase 1 (06-ago, PR #1520 mergeado en 00862a33)

Trece dimensiones en paralelo. Cuatro defectos gordos, los cuatro reproducidos en producción antes de tocarlos y ninguno cazado por una revisión humana:

- **Fuga cross-tenant de LECTURA** (mig 643): la 641 concedió `factura_cobros_resumen` a `authenticated`; PostgREST la exponía con el anon key del bundle. 6ª reincidencia del patrón → cerrada además con el hook `revoke-guard` en pre-commit.
- **1.407 cobradas a un trigger de volver a `pendiente`** (migs 644+645): la 640 convirtió `estado` en derivada sin backfill. Y el primer backfill se verificó con el mismo predicado que lo filtró, así que dejó 99 negativas fuera diciendo que quedaban 0.
- **Escritura cross-tenant** (mig 646): la política validaba `org_id`, la columna que el atacante escribe, y nada ataba `factura_id`. Un usuario podía marcar cobrada la factura de otra empresa.
- **Doble clic = doble cobro**: el guard de concurrencia vivía de que ese UPDATE escribiera `estado`, y al pasar a derivada dejó de serializar. 2.662 € sobre una factura de 1.331.

Verificación final sin muestrear: 1.444 cobradas/pagadas de prod recomputadas, 0 cambian. Suite Playwright: 125 pasan, incluidas las tres de conciliación (el camino bancario).

### Ledger fase 1 — cierre completo 06-ago (PRs #1520 + #1522)

PR #1520 mergeado con un bloqueante a sabiendas (código preexistente, las migs ya estaban en prod). Al revisar las 9 ramas/worktrees con trabajo sin mergear, encontré el checkout raíz con 3 días de WIP suelta (56 ficheros) mezclando dos cosas: una versión anterior y con bugs de trabajo YA mergeado (contraste AA, orden de providers, CSS movido a módulo compartido — descartada, verificada archivo a archivo), y una feature real sin equivalente en main (SkeletonTable en Obras+dashboard, fix `opsa` en agentes, docs de `cron_runs`, y el hook `/fia-cierre` que se disparó de verdad sobre mí en esta misma sesión). La real se organizó en 5 commits atómicos y se mergeó como PR #1522.

Al hacer inventario de las 87 ramas locales sin worktree, dos métodos rápidos (`git cherry`, diff de tres puntos) dieron falsos positivos por el mismo motivo: ninguno compara árboles actuales, y este repo hace squash-merge. Con el método correcto (árbol actual vs árbol actual, solo en los ficheros tocados), las 87 salieron confirmadas redundantes — 3 de ellas eran borradores anteriores de un informe QA que main ya tiene completo, así que mergearlas habría sido un retroceso. Ver [[tres-puntos-y-git-cherry-mienten-en-ramas-squash-mergeadas]].

Queda abierto el issue #1521: `importar_emitida_externa` es un tercer escritor de `facturas.estado` que regenera la misma mina que las migs 644/645 acabaron de desactivar. Prompt de continuación entregado con el fix ubicado línea a línea.

**Issue #1521 cerrado el mismo 06-ago (mig 647, PRs #1523+#1524).** Fix calcado del patrón de la 644: inserta la fila de ledger en el único punto donde convergen las dos ramas de `importar_emitida_externa` (antes del `INSERT INTO lineas_factura`), y deja de escribir `estado`/`fecha_cobro` a mano. Verificado en los dos sentidos con `supabase/tests/647_importar_emitida_externa_ledger.validate.sql` (patrón de la 470: org de prueba propia + rollback interno). **El pooler de Postgres (5432/6543) daba timeout desde la máquina de desarrollo** (ver [[supabase-pooler-timeout-isp-fallback-dashboard]]), así que la migración se aplicó y verificó a mano por el SQL Editor del dashboard en vez del `psql`+`BEGIN…ROLLBACK` habitual — mismo resultado, un paso más manual. Reconciliado además `supabase_migrations.schema_migrations` sin CLI: diff bidireccional por SQL puro (`string_agg` de versiones remotas vs `ls supabase/migrations/` local) confirmando 609=609 antes de cerrar. Con esto el bloque "ledger de cobros y pagadores" (#1519/#1520/#1521) queda cerrado del todo.

### 2026-08-03 (retirado del NOW el 06-ago)
- Color de marca de la org sembrado desde servidor, en prod (#1499).
- Ticket 133 fase 1: seleccionar partidas y copiar/mover/borrar/sumar (#1491); superado por la tanda del 06-ago.

## Podado del NOW el 2026-08-07 (12 entradas cerradas)

- 🟢 **Auditoría de barrido — 17 hallazgos, en el artifact (04-ago)** — 7 agentes en paralelo (auth, fiscal, Obras, OCR/WhatsApp/crons, cobros/Stripe, frontend, código). 3 altos: `/v1/facturas/[id]/recordatorio-pago` cobra de más con IRPF/parciales (usa `total` en vez de `importe_cobrable`); 6 sitios con `.limit()>1000` (reincidencia del truncado de PostgREST, uno sin `ORDER BY` da una cifra de negocio arbitraria); 4 violaciones de componentes `ui/` en `/admin`. Detalle completo → artifact `Tokens — TuFacturaIA` §22, https://claude.ai/code/artifact/9b4e72d0-1792-4bb1-9cac-ddf40e3341ed
- 🟢 **Truncado a 1.000 filas: cerrado donde importa (02-ago, #1475→#1483)** — queda por criterio: 30 lecturas de panel admin y listados, que muestran menos filas pero no calculan mal. Detalle → [[facturaia-historico-snapshot-2026-08-02]] · [[postgrest-max-rows-trunca-silencioso-in-revienta-url]]
- 🟢 **Encargo de Natalia: 3 de sus 4 peticiones en prod (02-ago, #1466→#1484, migs 624-626)** — **vivo**: (a) familias gestionables y (c) leer tarifas con IA, bloqueadas por respuestas suyas. **Ojo con `obras-092`**: la marca de «material sin preparar» hereda `es_valido`, así que un volcado de descuentos con la clave incompleta los pasa a «preparados» con el descuento de OTRO fabricante — el aviso se va y el precio sigue mal. Detalle → [[facturaia-historico-snapshot-2026-08-02]]
- 🟢 **Copiar una partida clona su árbol de componentes (03-ago, #1497, mig 629)** — el trigger regeneraba el desglose contra el catálogo de HOY mientras la línea hereda el snapshot congelado, y se contradecían. Se clona por RPC en SQL (los `Insert`/`Update` de esa tabla están a `never` a propósito), probado contra un Postgres real.
- 🟢 **El azul dejó de estar clavado, en prod, sin pendientes (03-ago, #1500)** — 47 `rgba()` a mano → `color-mix`. → [[facturaia-historico-snapshot-2026-08-03]] · [[css-modules-hashea-el-nombre-de-la-animacion-aunque-la-keyframes-sea-global]]
- 🟢 **Los avisos donde se arreglan, en prod (03-ago, #1507 + #1510)** — llega a la tarjeta del inicio y a los seis sitios que emiten. Único pendiente (baselines de linux) arriba. → [[facturaia-historico-snapshot-2026-08-03]] · [[elemento-pasado-como-prop-lee-el-contexto-de-donde-se-renderiza]]
- 🟢 **Las tres incidencias del panel, resueltas (03-ago, #1492 · #1495 · #1496)** — ninguna era lo que decía; el guard destapó 8 emisores más huérfanos, sin arreglar. → [[facturaia-historico-snapshot-2026-08-03]] · [[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]]
- 🟢 **Los avisos por email de tickets funcionaban; el falso negativo era el buzón (03-ago)** — 5 correos verificados end-to-end. **Queda**: alias `soporte@` en vez de buzones personales · aperturas en Resend (`opened`=0 en toda la tabla) · aviso a Slack. → [[facturaia-historico-snapshot-2026-08-03]] · [[delivered-del-proveedor-no-es-visto-el-cliente-lo-categoriza]]
- 🟢 **El ciclo del runner, CERRADO en prod (03-ago, #1497 + #1503, mig 629)** — los dos cabos del #1354 resueltos: (1) estado nuevo `pr_mergeado` + reconciliador en el runner (lo único con `GH_TOKEN`) que pregunta a GitHub y cierra; al desplegarse pasó **63 jobs** de `pr_abierto` a `pr_mergeado` de una vez, y `pr_abierto` quedó a cero. (2) el listado marca **«Resumen sin publicar»** cuando el runner redactó respuesta y nadie la publicó — verificado en vivo con el ticket 138. **Ojo al desplegar el runner**: el #1497 lo tiró 4 h porque el Dockerfile listaba los `.mjs` uno a uno; ya va por glob y con guard. → [[dockerfile-que-lista-modulos-uno-a-uno-mata-el-servicio-sin-fallar-el-build]] · [[el-parte-de-un-job-caido-no-es-evidencia-de-lo-que-dejo]]
- 🟢 **Una línea de factura puede salir de varias partidas, en prod (29-jul, #1347)** — **dos cabos**: `lote_reparto` no se persiste y `GET /api/stock/lotes` devuelve partidas archivadas que la previsualización suma. Ver [[preview-cliente-de-un-reparto-debe-copiar-los-filtros-del-motor-sql]]
- 🟢 **El recordatorio de cobro va a quien paga (29-jul, migs 590/591)** — el email ya; el WhatsApp espera a validar el teléfono del contacto (condiciones de Meta). **Tuyo**: confirmar el teléfono de los contactos principales. Ver [[redirigir-un-envio-sin-mover-su-gate-de-verificacion]]
- 🟢 **Arquitectura: grafo al día, capas enderezadas y auth con red, en prod (27-jul, #1266 · #1274 · #1288)** — ciclo cerrado, 60 tests de conformidad sobre las 604 rutas. Acciones tuyas en `Bloqueos`. → [[facturaia-historico-snapshot-2026-08-02]]

## Detalle de la sesión del 2026-08-07 (unidad de MO y gate de cierre)

- 🟠 **La unidad del tiempo de MO: NORMALIZADA a horas reales, migración lista SIN aplicar (07-ago, mig 656)** — deja sin efecto el «no se normaliza» de esta entrada: el bloqueo era no saber si había uno o dos factores, y hay **uno**. f = **1,42114**, R² = 0,9999998, idéntico en las tres orgs con catálogo. El gate ataca el PARÁMETRO (cada fila que declara sus horas en el nombre debe valer lo que dice), no el precio, y se probó **por barrido antes de escribirlo**: deja pasar 1,4142–1,4266 y rechaza 1,4918 en las 44 filas. Los 7 del +4,98 % **conservan su desviación** hasta que Natalia conteste. **Alcance real: 745 tipos, 1 material y 7 líneas de IET**; el volumen (7.871) está en sandbox — por eso ahora es barato. Probada contra un Postgres con las 603 migraciones del repo y sus 56 tipos reales; idempotente en 3 pases. El banco de pruebas cazó 3 fallos que habrían roto prod: `ALTER TYPE` bloqueado por triggers, el trigger de componentes regenerando desgloses, y la reaplicación abortando. **Y el gate de cierre cazó 2 bloqueantes más**: `obras_presupuesto_linea_componentes.tiempo_unit` sin convertir (0 filas hoy, pero convivirían dos escalas) y `coste_hora_mo * f` apoyado en un «hoy vale 0» medido fuera de la transacción. Ambos arreglados. La UI habla en minutos (`23 s` / `21 min` / `1 h 30 min`). **Pendiente: aplicar a prod y mergear.** → [[alter-column-type-choca-con-cualquier-trigger-update-of]] · [[un-guard-que-se-apoya-en-una-medicion-externa-no-es-un-guard]] · [[decidir-una-frontera-con-el-valor-crudo-produce-imposibles]]

- 🟠 **El coste/hora: Natalia lo dará desde cero, y eso pone la mig 656 en el camino crítico (07-ago)** — contestó que los datos de WAPI **no valen** («ese coste no se ha actualizado desde vetetuasabercuando») y que meterán el **precio real de hoy** para sus 10-15 trabajadores. Encaja con lo medido: solo 7 tarifas activas en 2022-23. Queda cerrado de dónde salían los 16,36 €/h: `dbo.TRABAJO` con el precio congelado en el parte, excluyendo las líneas de subcontrata a 1,00 (38 líneas con 53.111 «horas» falsas frente a 451 con 25.361 reales), y **es BRUTO de convenio, no coste-empresa** — lo prueban un `PEON 1º AÑO` a 5,50 €/h (imposible como coste-empresa, no llega al SMI) y que en 33 de 63 tipos la hora extra sea la normal ×1,5. El coste-empresa **no existe en WAPI**: barrido de `sys.columns` sobre 1.100 tablas por `segur`/`cotiz`/`nomina`/`salario`, cero campos. **El orden importa**: si teclea su coste antes de aplicar la 656, el coste previsto le sale un 42 % alto; el guard nuevo lo detecta y aborta, pero deja la migración sin aplicar. Migración primero, dato después. Los 21,6 €/h son estimación nuestra (×1,32), etiquetarlo siempre. → [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]] · [[barrer-el-catalogo-de-columnas-convierte-no-lo-encuentro-en-no-existe]]

- 🟢 **El gate `/fia-cierre` pasa de ~$35 a ~$5-7 por cierre (07-ago)** — medido del `usage` real: 9 agentes, 236 tool calls y **94 % del coste en cache read/write**, no en razonamiento (la misma migración leída 11 veces). Tres cambios: el **diff va inyectado** en el prompt en vez de que cada agente lo redescubra; **4 dimensiones** agrupadas por dónde vive el riesgo (`codigo`/`datos`/`plataforma`/`cabos`) en vez de 9 solapadas; y Sonnet en las mecánicas con Opus solo en cabos y síntesis. El alcance lo decide `scripts/cierre-alcance.mjs` (+ `docs/plan/cierres.json`), portado del `auditoria-alcance.mjs` de TuCRMIA, con **14 tests que comprueban lo que APAGA** y verificado por mutación (5 de 5 cazadas). Destapó que `src/lib/**` es demasiado ancho para decidir por ruta (847 ficheros, 429 tocan BD, sin patrón de nombre) → filtro por contenido con lector inyectable. **Sin estrenar**: el registro se escribe DESPUÉS de correr. → [[el-coste-de-un-fanout-de-agentes-es-contexto-no-razonamiento]]

## Entradas de julio retiradas del NOW el 2026-08-07 (20)

Seguían en el dashboard semanas después. Ninguna era bloqueante activo; los pendientes que citan siguen vivos aquí.

- ✅ **El backup de WAPI es del 20-jul 23:50, ANTERIOR al volcado del 21-jul (07-ago)** — leido de la cabecera MTF del `.BAK`, con doble verificacion (cabecera y cola del fichero). El 2-ago era solo la fecha de descarga. **La sandbox ya tiene todo lo del backup: no hay que re-volcar por frescura.** Contexto: `CONSTANTES.Precio_Mano_Obra` se toco el 2025-12-24 y hay partes en `TRABAJO` hasta 2026-01-01, asi que Natalia seguia metiendo datos en WAPI al menos hasta enero.
- 🟠 **Runner (31-jul, #1412→#1419): queda la opción (c) del #1409** — que «Confirmar emisión» diga a qué dirección envía. → [[facturaia-historico-snapshot-2026-08-01]]
- 🟠 **El recordatorio de cobro va a quien paga (29-jul, migs 590/591)*** — Tuyo. Detalle → [[facturaia-historico-detallado]]
- 🟠 **Cabo de acceso: el docstring de `obras/layout.tsx` miente (29-jul)** — dice que `orgHasSector` mira la org efectiva con impersonación y `getOrgId` solo lee `profiles.active_org_id`. Es un gate, no un seed, así que PR propio. Impacto **sin demostrar**: el intento de reproducirlo quedó viciado.
- 🟢 **Tickets de IET y del runner en prod (28/29-jul, #1324→#1327, migs 583-587)** — **queda** el DROP de `obras_contactos` y decidir el `vigencia_tarifa` vacío en los 17.831 materiales del CSV. Ver [[ADR-044-tabla-unica-de-contactos-en-vez-de-una-por-modulo]]
- 🟠 **Runner tirando con la cuenta de info por workaround; `CLAUDE_TOKEN_ALT1` sigue sin entrar (28-jul)** — clave a `default` y el token de info en `CLAUDE_CODE_OAUTH_TOKEN`; con eso abrió 3 PRs seguidos, así que el eslabón está probado. **Pendiente**: por qué no entra la variable (apuesta: guardada en el Environment del proyecto y no del servicio); mientras, el log miente sobre qué cuenta paga. Ver [[el-limite-de-uso-de-claude-es-de-organizacion-no-de-cuenta]]
- 🟡 **Cuatro decisiones sin tomar del barrido del 28-jul** — (1) `fiscal-perfil-preserve.spec.ts` degrada el perfil fiscal de la org aunque salga verde (su «restaurar» escribe valores inventados y está fuera de `finally`); (2) las 8 recibidas con la fecha mal leída por OCR, ¿se borran y resuben?; (3) el `.billing-banner` del CLS, ¿billing en servidor o hueco reservado?; (4) `ops/ticket-runner/claude-time-hook.mjs` sigue duplicado y dos generaciones por detrás.
- 🟠 **Cabos del cierre e2e/infra/perf (28-jul, #1292)** — cinco, ninguno bloqueante: tanda smoke limpia sin contención nunca vista entera · cifra de CLS contra `build`+`start` · **infra-001 sigue abierto** (falta la reconstrucción de cero, sin Docker en la máquina cuando se intentó) · baselines visuales sin regenerar. → [[facturaia-historico-snapshot-2026-08-02]]
- 🟠 **Lo que destapó verificar el ticket en prod (27-jul)** — **21 recibidas aprobadas sin vencimiento** en todas las orgs, y **8 de 498 con el `vto` anterior a su `fecha`**: el OCR leyó mal la FECHA, no el vencimiento. Su única salida es borrar y volver a subir, porque la `fecha` es fiscal. → [[facturaia-historico-snapshot-2026-08-02]]
- 🟠 **Residuo en las orgs de prueba (28/29-jul)** — los specs ya se limpian solos (#1306); **queda ejecutar** `tests/e2e/limpiar-residuo-e2e.sql` sobre el residuo viejo, con el inventario solo-SELECT primero. Inventario completo (huecos de serie P, `Smoke 575`, la *Merluza fresca* con sus lotes, la `A2026-0001` emitida y el NIF puesto a mano en la sandbox) → [[facturaia-historico-snapshot-2026-08-02]]
- 🟠 **Cuatro RPC estaban rotas en prod y sus acciones eran imposibles desde la app (26-jul, mig 569)** — `user_can_write_in_org` resuelve el rol por `auth.uid()` y los endpoints llaman con service role. Tercera ocurrencia con el learning ya escrito dos veces → check en `pre-push` (#1231/#1232). **Pendiente de Manu**: confirmar en la app que "marcar cuadrada" y "marcar presentada" funcionan, porque nunca se han podido usar. Ver [[rpc-rls-authuid-vacio-en-service-role]]
- 🟡 **Abiertos de la sesión del 26-jul, con medición** — `issues/conc-001`: el emparejamiento automático casa por importe sin mirar la contraparte (4 de 22 asignaciones automáticas eran falsas; **datos ya corregidos**, falta el matcher). `issues/fiscal-003`: extender la deriva a 111/115/347/349 (**prioridad baja medida**: hoy no existe ninguna declaración de esos modelos en prod). Ver [[universo-de-datos-reimplementado-en-dos-sitios-divergge]] · [[fk-restrict-no-sirve-como-regla-de-negocio-no-distingue-estados]] · [[ADR-041-recibida-duplicada-se-elimina-no-se-anula]]
- 🧹 **`ops/ticket-runner/claude-time-hook.mjs`: copia divergida del hook canónico, 2 generaciones por detrás (26-jul)** — el README de `ops/claude-time-tracker` prohíbe duplicarlo; sin los latidos `SubagentStop`/`PostToolUse` de #181 el runner infracuenta sus horas, y hay 64 líneas sin commitear de una sincronización a medias. Salida preferida: que el runner consuma el canónico, como ya hizo `feedback-runner` (toca el build en Dokploy).
- ⏳ **Importe cobrable con retenciones (25-jul)** — en prod. Queda que Manu confirme visualmente que al vencer `A2026-0147` y `A2026-0001` el recordatorio y el PDF digan 212,00 € y 265,00 €, no el bruto. Detalle → [[facturaia-historico-snapshot-2026-07-29]]
- ⏳ **OCR WhatsApp: aviso en fallo + `forma_pago` inventada (#1156, 22-jul)** — en prod. Queda el smoke real: foto ilegible por WhatsApp y comprobar que el usuario recibe aviso. Detalle → [[facturaia-historico-snapshot-2026-07-29]]
- ⏳ **Migración wapi → Obras en la org sandbox de IET (20-jul)** — casi completa. Queda QA visual de los datos importados. Detalle → [[facturaia-historico-snapshot-2026-07-29]]
- **[ACCIÓN MANU — seguridad] `SIGNING_LEGACY_UNTIL` sigue sin fijarse en Dokploy, dos meses después (27-jul).** `legacyEnabledNow()` hace `if (!until) return true`: variable ausente = ventana legacy ABIERTA para siempre. Y el legacy **no ata método, path ni body**, así que el HMAC v2 que se introdujo en mayo para cerrar el replay horizontal es **cosmético** mientras esto siga así: un secreto filtrado sirve contra cualquiera de las 90 rutas internas. No se puede cerrar a ciegas porque los emisores (n8n, schedules de Dokploy) viven fuera del repo. **Ahora sí hay dato**: cada uso queda en `admin_audit_log` con `action='internal.legacy_service_key'` (desplegado en #1288). Pasos, en orden: (1) **ahora mismo** poner `SIGNING_LEGACY_UNTIL=2026-09-01T00:00:00Z` — hoy no rompe nada porque la ventana sigue abierta, pero convierte "abierta para siempre" en "abierta hasta el 1-sep", que es lo que el patrón prometía y nadie activó; (2) el **2 de agosto**, cuando ya haya disparado hasta el cron mensual (`runtime-eol-check`, día 1, es el más espaciado: 40 días de tolerancia), consultar `admin_audit_log` por `action='internal.legacy_service_key'` agrupando por `target_key`; (3) migrar a `ops/cron/sign-call.sh` los emisores que aparezcan; (4) adelantar la fecha a pasado. Siempre **recreando el contenedor** (no restart) y verificando con `docker exec env`. **Ya no depende de que te acuerdes (28-jul, #1299)**: `legacySigningCollector` mira ese mismo `admin_audit_log` en cada barrido del `system-health-sweep` y avisa en `/admin/alerts` + email — te dirá cuándo se puede cerrar sin riesgo (`legacy_signing_cerrable`, alta) y, si pones fecha con emisores sin migrar, te avisará a ≤7 días del cierre (`legacy_signing_inminente`) antes de que los crons empiecen a dar 401.
- **[ACCIÓN MANU] NotCaído detecta pero sus avisos no llegan a nadie (verificado 27-jul).** El monitor está activo y pilló el corte del 26 a los 13 min; lo roto es la última milla: falta configurar y probar el canal de notificación hasta verlo en el móvil (detrás del `X-Admin-Token`, guardar en 1Password). Prueba de lo grave: `dokploy-manu-tecnocloud` llevaba 81 días caído sin que nadie se enterara. Sin esto, TuFacturaIA no tiene detección de caídas en vivo. Ver [[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]] · [[parada-de-flota-solo-se-ve-en-la-simultaneidad]]
- **¿3 réplicas del runner o seguimos en 2? (30-jul)** — **recomendación: 2.** El paralelismo funciona (`RUNNER_REPLICAS`, hoy 2), pero el freno no es la concurrencia: **la cuota de Claude es de organización**, así que N sesiones la agotan N veces más rápido y el fallo pasa de "cola lenta" a "todas fallan por cuota" (7 de 34 el 29-jul). El tiempo está en `analizando` (p90 26,3 min sobre 30), no en la cola, y cada réplica paga 3 GB, ~2 min de `npm ci` y ~1 GB de copia por job. Falta el dato que lo decide: RAM libre del host (gráfico de la home del panel; la API no expone el servidor local y el SSH por dominio da `Connection refused`). Cambiarlo exige Deploy, y un Deploy con jobs vivos se los lleva. Ver [[el-limite-de-uso-de-claude-es-de-organizacion-no-de-cuenta]]
- **¿Se puede corregir la `fecha` de una recibida YA aprobada? (29-jul, ticket #104)** — **recomendación: SÍ, abrirla.** El argumento es de coherencia, no de volumen: ya se puede **borrar** una recibida aprobada en cualquier estado (`recibida_eliminar`, migs 567/568), y editar un campo es menos destructivo que eliminar la fila. El workaround actual ("bórrala y resúbela") es peor que el problema: pierde conciliación, adjunto, histórico y movimientos de stock, y vuelve a pasar el documento por el OCR, que es quien se equivocó. Y sale **más barato de lo estimado**: de los 4 bloqueos del delete solo aplica el snapshot fiscal (los movimientos de stock tienen su propia fecha; SEPA y recordatorios van contra `vto` e importe; la conciliación casa por el movimiento bancario). Lo único nuevo a diseñar: si la fecha nueva **cruza de periodo o ejercicio**, marcar para recálculo las **dos** declaraciones, origen y destino. Alcance: 1 RPC + 1 endpoint + campo editable en el detalle de recibidas, donde ya viven los editores de `vto` y fecha de pago. Las 2 facturas afectadas ya se corrigieron a mano (29-jul), así que **no es urgente, es correcto**. Ver [[ocr-lee-dd-mm-yy-como-yy-mm-dd-y-manda-la-factura-a-otro-ejercicio]] · [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]]

## Estado previo de esas entradas, antes del cierre del 07-ago (noche)

- 🟠 **Unidad de MO normalizada a horas reales: mig 656 lista, SIN aplicar (07-ago)** — f = **1,42114** (R²=0,9999998), uno solo, despejado por org de las 44 filas que declaran sus horas en el nombre. El gate ataca el PARÁMETRO y se probó por barrido: pasa 1,4142–1,4266, rechaza 1,4918. Los 7 del +4,98 % conservan su desviación hasta que ella conteste. Toca 745 tipos, 1 material y 7 líneas de IET. Probada contra Postgres real, idempotente. **Pendiente: aplicar a prod y mergear** — y antes de que Natalia meta su coste/hora, o le sale 42 % alto. Detalle y los 5 fallos que cazaron el banco de pruebas y el gate → [[facturaia-historico-detallado]] · [[alter-column-type-choca-con-cualquier-trigger-update-of]] · [[un-guard-que-se-apoya-en-una-medicion-externa-no-es-un-guard]]

- 🟢 **`/fia-cierre` de ~$35 a ~$5-7 por cierre (07-ago)** — el 94 % del coste era contexto rearrastrado, no razonamiento. Diff inyectado en el prompt, 4 dimensiones en vez de 9, Sonnet en las mecánicas. Alcance por `scripts/cierre-alcance.mjs` con 14 tests y verificado por mutación. **Sin estrenar.** → [[el-coste-de-un-fanout-de-agentes-es-contexto-no-razonamiento]]

- 🟠 **El coste/hora lo dará Natalia desde cero (07-ago)** — los datos de WAPI no valen («no se ha actualizado desde vetetuasabercuando»); meterá el precio real de hoy para sus 10-15 trabajadores. Cerrado de dónde salían los 16,36 €/h y que son **bruto de convenio, no coste-empresa** (el coste-empresa no existe en WAPI). **Migración primero, dato después.** Detalle → [[facturaia-historico-detallado]] · [[facturaia-iet-preguntas-tiempos-mo]]

## Cerradas y retiradas del NOW el 07-ago (noche): el enigma de las escalas, el backup y la mig 652

- 🟢 **RESUELTO el enigma de las dos escalas: son 7 tipos con un +5 %, no dos criterios (07-ago)** — Natalia contesto que no sabe de que viene, asi que se busco el patron en los datos. Lo de «singular/plural» era un RASTRO, no la causa: de los 52 tipos autodescriptivos, **44 son consistentes con el factor 1,42** (41 exactos y 3 con ruido de redondeo de 2-4 diezmilesimas), **7 estan exactamente un 5 % por encima** (los de 1 · 1,1 · 1,2 · 1,3 · 1,4 · 1,6 y 1,7 horas) y **1 es basura** (`TIEMPO 1250 HORAS` = 1000, la partida en euros). La prueba de que no es gramatica: `TIEMPO 1,5 HORAS` (plural) esta bien y `TIEMPO 1,6 HORA` (singular) esta un 5 % alto, o sea la secuencia numerica se rompe pero la gramatical no: quien escribio esos 7 en singular los creo en otro momento y les puso un 5 %. **Y en la org REAL de IET no hay ni un material que use esos 7 tipos** (346 en la sandbox del volcado). Con eso **la normalizacion se desbloquea**: el factor es 1,42, y los 7 se alinean o se dejan segun diga ella.

- 🟢 **Un coste de mano de obra a 0 ya no se presenta como coste real (07-ago, mig 652, en prod, verificado por catálogo y ejecutando la función)** — espejo del #1527 en el eje de la MO, que había quedado fuera. Dos causas marcan `coste_mo_incompleto`: la org sin `coste_hora_mo`, o el material sin clasificar (`tipo_mo_id IS NULL`). Un material clasificado a 0 h NO se marca: ese cero es deliberado. `obras_uo_calcular` devuelve `mo_sin_clasificar` para que una UO con todos los componentes sin clasificar no se escape por detrás. Backfill: **las 11 líneas de IET marcadas** (7 por falta de coste/hora, 4 por sin clasificar). Ningún importe cambia. Añadido el pendiente `obras.coste_hora_mo` al banner (solo orgs con Obras) y el candado del #133 ahora exige la marca de MO a todo escritor de `coste_mo_unit`. Cierra también **#1409 (c)**: «Confirmar emisión» ya dice a qué dirección envía, y avisa si falta.

## Higiene de trinquetes · cerrada el 9-ago (wikilinks retirados del dashboard el 26-ago)

Seis trinquetes en `pre-commit`; el 6.º es `ratchet:size`, techo 400 líneas de CÓDIGO. Los cinco aprendizajes que dejó, movidos aquí para que no se paguen en el arranque de cada sesión: [[gate-con-ruta-relativa-no-corre-desde-subdirectorio-y-sale-verde]] · [[mover-un-fichero-rompe-todo-gate-indexado-por-ruta]] · [[al-partir-un-fichero-copia-todos-los-imports-y-resta-con-eslint]] · [[asercion-e2e-que-mide-datos-en-vez-de-montaje-es-verde-o-rojo-por-azar]] · [[los-buckets-de-storage-se-crean-en-el-panel-y-no-viajan-con-el-repo]]

## Cerradas y retiradas del NOW el 09-ago: las 12 quejas de UI de Obras y el sistema de diseño

- 🟢 **Las 12 quejas de UI de Obras, en prod (08-ago, #1546 + #1550)** — el hallazgo que no venía en la lista: la recepción de albarán rotulaba «Material» en vez del nombre, porque el modal resolvía el nombre en cliente contra un endpoint paginado (50 filas) y caía al UUID. Se arregló mandando denominación y unidad desde el servidor, con `unidad-material.ts` como fuente única (sustituye 4 resoluciones duplicadas) y `unidad-formato.ts` para la mitad de presentación, que no puede ser `server-only` porque la importan pantallas de cliente. **Alcance real medido en prod el 9-ago: CERO ocurrencias.** Los 10.057 albaranes son de las dos orgs `is_test` —10.055 de una importación del 21-jul— y ninguna org de cliente tiene uno, así que no hubo que preguntarle a IET si validó a ciegas. El primer agregado dio 0 por el filtro del join, no por los datos: lo destapó un control sin filtros. Ver [[resolver-label-nombre-en-cliente-contra-endpoint-paginado-cae-al-uuid]]
- 🟢 **El sistema de diseño, documentado para exportar y de paso auditado (03-ago, #1499 · #1500)** — `docs/design/sistema-de-diseno.html`, 21 secciones, offline y sin una petición a la red. Escribirla destapó siete defectos vivos en prod (la marca por org no llegaba a los textos, 47 azules a mano la ignoraban, «Anular factura» no parecía destructivo y tres fallos dentro de `prefers-reduced-motion`, ramal que ningún test ejercita). El PR de los keyframes queda **DESCARTADO, no aplazado**: CSS Modules hashea el `animation-name` aunque la keyframes sea global, así que unificar los 20 spinners los habría parado en silencio — no era deuda, era el scoping. Ver [[escribir-la-doc-de-exportacion-de-un-sistema-lo-audita-entero]] · [[lo-que-vive-dentro-de-prefers-reduced-motion-no-lo-mira-nadie]] · [[css-modules-hashea-el-nombre-de-la-animacion-aunque-la-keyframes-sea-global]]

### Rejilla de partidas — pulido en prod (08-ago, PR #1538)
- ✅ **[08-ago] Rejilla de partidas: pulido EN PROD y con smoke (PR #1538)** — fila 50 → 34 px (el suelo era el `min-height` del botón `sm`), capítulo vacío 284 → 44, columna de acciones y de cantidad con ancho por puntero, y la pestaña blanca que asomaba fuera del capítulo. Smoke en prod verificado midiendo el DOM y tecleando una cantidad (descartada con Escape, sin escribir). Antes/después: artifact `ac343eb9`. Ojo al rebase: el #1537 (Excel) tocaba los mismos 3 ficheros. **Y la deuda que arrastraba NO está cerrada (corregido 08-ago por el #1542)**: el #1539 arregló dos filas más (pedido 60 → 50, objetivos 57 → 41) y se dio por terminada; el barrido bueno devuelve **unas diez** con el mismo patrón, sin medir. Lista en `manual-admin.md` §48.7. Cada una necesita su medida antes/después: el suelo de la fila no siempre es el botón (en pedido resultó ser el `NumberField`). Guard en `src/components/__tests__/tap-target-filas-densas.test.ts` (el #1542 le añadió la magnitud: `min-height` es un SUELO, no un techo, así que subir el relleno de `.xs` devolvía la fila alta con los tests en verde). El **#1544** cerró el último agujero del guard —localizaba el botón por la PRIMERA aparición del `aria-label`, y un rótulo duplicado lo dejaba vigilando otro— y el **#1545** arregló algo que no era de UI: `--registrar` del gate de cierre moría con ENOENT y su `cierres.json` no estaba trackeado, o sea que **el histórico del gate no existía** (se perdió el registro de esa misma sesión al retirarse su worktree). Ahora va en el repo, con test que corre con el directorio ausente. → [[un-fichero-de-estado-sin-trackear-no-es-memoria]] · antes/después de las dos filas, medido y con capturas: artifact `e96162d8`

### Cerrados del 07/08-ago (movidos del dashboard el 09-ago)

- ✅ **Cerrado 07/08-ago sin pendientes**: panel de tickets (#1528/#1529), soporte 133-138, ticket 135 (Excel del presupuesto de obra, #1537), tanda 142-145 + tap target del `Segmented` (#1543/#1549), y **las 12 quejas de UI de Obras** (#1546+#1550: densidad en un token, selector de columnas de la vista de costes, unidad de medida en las 4 pantallas del pedido; artifact `d50dd108`). → [[facturaia-historico-eventos]] · [[facturaia-historico-detallado]] · [[un-guard-cuya-aguja-cubre-una-sola-forma-sintactica-se-esquiva-refactorizando]] · [[dos-salidas-contradictorias-no-son-un-mecanismo-hasta-que-lo-reproduces]] · [[columna-congelada-se-tapa-con-altura-y-con-apilado]]
- 🟢 **Coste/hora medio de IET: 21 €/h, puesto y cerrado (07-ago)** — guardar esos ajustes recalcula los 7.683 materiales de la org aunque el campo no entre en el precio; salió no-op de milagro. → [[escribir-un-campo-que-no-entra-en-ninguna-formula-dispara-igual-el-recalculo]] · [[facturaia-historico-detallado]]

### 2026-08-09 — barrido de higiene: alias de tipo único, el último `<style jsx>` y `.audit` fuera del global (#1575 · #1576 · #1577, main `93fcfd8c`)

- ✅ **#1575 `ToastFn`/`ConfirmFn` salen al fichero que DEFINE la firma** — había 20 declaraciones a mano de `ToastFn` y 11 de `ConfirmFn`; 19 copiaban bien y **una no**: `parte-modal.tsx` declaraba `(message, kind?: 'success'|'error'|'info')`, amputando el 3er parámetro `action?: ToastAction` (el botón de deshacer) y el nivel `'warn'`, y el compilador se lo imponía a quien recibiera ese tipo. El hogar es `components/ui/toast.tsx` y **no** un `components/obras/types.ts` nuevo: junto a la interfaz que copia, el alias ya no PUEDE divergir —que es el fallo, no la duplicación— y arrastra además la copia de `plantillas/textos-tipo-view.tsx` sin inventar una arista `obras → plantillas`. El plan hablaba de tres parciales que ya lo exportaban: eran **dos** (`_parts/obra-arbol-view/types.ts` no declara ninguno). El typecheck **no** se puso rojo: el único consumidor de `ParteModal` ya pasaba el `toast` real. Solo tipos, cero runtime.
- ✅ **#1576 el cuarto y último `<style jsx>` del repo pasa a CSS Modules** — `settings/auditoria-section.tsx` 1100 → 642 líneas; 51 clases, 152 ocurrencias. Ese CSS no lo auditaba nadie (`lint:css` solo ve `*.module.css`). Tres cosas escondidas: `audit-results` era **clase fantasma** (aplicada y definida por nadie, como `audit-toolbar-row-main` en el #1568), `var(--danger, #f5425a)` era fallback **muerto y equivocado en dark** (el token vale `#ff6480`), y un `!important` que **invertía un empate que no existía**. La pantalla no tenía ningún E2E —por eso se aparcó—: se verificó con **8.105 nodos de estilos computados en 7 estados** (desktop/móvil × cerrado/abierto + skeleton, vacío y error forzados por `page.route`), **0 diferencias reales**; los 52 diffs restantes son el hash del `@keyframes` y el `transform` de una animación viva. Deja `tests/e2e/smoke/settings-auditoria.spec.ts`, que **discrimina** (comprobado desmontando la sección y rompiendo `s.panel`).
- **Cómo se mergeó**: no hay CI (0 checks, billing de Actions bloqueado), así que el gate local es el único. Se mergeó #1575, se fusionó `main` dentro de la rama del #1576 y se corrió el gate ENTERO sobre el árbol combinado —lint · lint:css · typecheck · build · **1045 ficheros / 10.539 tests** · los cinco trinquetes · `deps:circular` · el smoke e2e— antes de mergear el segundo. El árbol de `main` se verificó idéntico al probado por hash de tree.
- **Colateral**: borrado el worktree muerto `facturaia-conciliacion` (limpio, 308 commits por detrás) y matado un `next dev` zombi de 2 días que ocupaba el 3000 devolviendo 500.
- Método reutilizable → [[baseline-de-estilos-computados-por-ruta-de-dom-para-migrar-css-sin-e2e]] · [[empate-de-especificidad-entre-globals-y-un-module-lo-decide-el-orden-de-inyeccion]]
- ✅ **#1577 remate: `.audit` sale del espacio global y con ella su regla muerta** — el #1576 ancló las reglas de la tabla al `.panel` hasheado para ganarle a `globals.css:7512` (`.set-table.audit td`, mismo (0,2,1)). Eso dejó la global **muerta** pero en pie, y `.audit` —nombre genérico donde los haya— siguió en el espacio global sin que nadie la definiese: gancho de un solo módulo y superficie para que una regla futura casara esa tabla por accidente. Verificado que era la ÚNICA regla global sobre `.audit` y que solo `auditoria-section.tsx:491` la renderiza, se borra; `.audit` pasa a clase del módulo (`:global(.set-table).audit td`) y el ancla `.panel` se retira de los 17 selectores, porque sin rival ya no pinta nada. **Se arregló también el smoke que dejó el #1576**: localizaba la tabla con `table.set-table.audit` y al hashear la clase ese locator queda MUERTO —y aquí un locator muerto no da rojo, da `count() === 0`, que el test lee como «no hay tabla»—. El trinquete de CSS global lo corrobora sin saber nada: **2534 → 2533 clases, 402 → 401 prefijos**.
- **La verificación no se dio por buena por salir verde**: el mismo arnés, con `.audit` hasheada en el CSS y el string global de vuelta en el `.tsx` (el fallo exacto que el PR podía introducir), canta **11.459 diferencias** contra las 0 del cambio real. Y el smoke corregido se comprobó rompiendo el montaje a propósito.
- ✅ **#1578 el 7º trinquete: `locator-guard`** — la regla «nunca localizar por clase de CSS Module» llevaba escrita desde el 27-jul en el vault **y en la primera pantalla de `hot.md`, que se carga en cada arranque**; aun así reincidió a los 13 días y en dos commits (el #1576 escribió `table.set-table.audit` cuando `.audit` era global, el #1577 la hasheó). Ahora bloquea `scripts/locator-guard.mjs` desde `pre-commit`. Dispara **por los dos lados**: con un `*.module.css` staged barre los 58 specs (0,09 s), porque el commit que mata el locator puede no tocar ninguno. No bloquea las clases que viven en global Y en módulo — un guard que adivina genera falsos positivos y acaba desactivado. `tests/e2e/layout/` queda fuera con motivo medido: monta el módulo a mano aplanando `:global()`, así que ahí lo correcto son los nombres SIN hashear. De regalo, 2 locators muertos que ya estaban en main (`button.tab:not(.active)` y `.modal` del crawler, este colgando de un `if (isVisible())`).
- **El guard entró a punto de nacer muerto**: su primera versión salía **verde sobre un repo que tenía 2 hallazgos** — el contenido del string excluía toda comilla y cortaba en la primera interior, así que `'[role="dialog"], .modal'` (la forma más común) no casaba. Se cazó porque el número esperado estaba MEDIDO antes de escribirlo. Y se probó por el camino real con `git commit` de verdad, no solo con su suite: escenario spec-staged y escenario solo-CSS-staged, los dos bloquean.
- Método que deja el #1578, y no es sobre locators: [[un-detector-nuevo-cuyo-cero-no-mediste-antes-no-vale]] — mide el corpus real ANTES de escribir el detector (su suite pasa con casos a mano), y si relaciona dos artefactos, dispáralo desde los dos lados.

### Bitácora de podas de `00-home/top-of-mind.md` (movida aquí el 9-ago)

Vivía en el preámbulo del propio índice, o sea que sus 1.071 bytes de historia se cargaban en CADA arranque de sesión. Es historia, no índice.

Reestructurado 2026-06-26 (poda: backlog por-cliente devuelto a cada hub; backup en `00-home/archive/top-of-mind-pre-poda-2026-06-26.md`). Podado 2026-07-25: retiradas 19 entradas de TuFacturaIA cuyo único pendiente era un smoke YA registrado en la sección Smoke del hub (verificado id a id: PR/migración presente en el hub y el pendiente vivo en Smoke o NOW). Backup en `00-home/archive/top-of-mind-pre-poda-2026-07-25.md`. Podado 2026-08-08: retiradas 5 entradas de TuFacturaIA duplicadas en el §Smoke del hub (verificado id a id imprimiendo la línea del hub que las respalda). La de Obras-IA/WhatsApp/MCP no estaba allí y se trasladó primero. NO se tocaron «skin Cristal» (decisión de negocio, no smoke) ni «retirada n8n» (arrastra la Fase 6).

## 10-ago · Motor de contrato y cierre de su cola (PRs #1583, #1585, #1587)

- **#1583 + #1585 (en prod)**: perímetro de auth de las 630 rutas (0 workers dormidos), rol de las 177
  escrituras sin parámetro (72/72 con 403) y de las 148 con parámetro (132/132), scopes de v1 + 64 tools
  MCP, espejo `MCP_RESOURCES` con `Record<Union,true>`. Registro en `docs/qa/funcional/`. **13 «hallazgos
  críticos» de la primera medición eran falsos**, y el falso positivo cross-org llegó a dañar la sandbox.
- **#1587 (sin mergear)**: cross-org de rutas con parámetro medido (29 de 149 con 403/404, **0 fugas y 0
  filas ajenas tocadas**, sonda de lectura antes de cada escritura y restauración verificada); páginas
  33 → 55 de 97; mig 657 para el descarte del banner **por miembro** (#1584), aplicada y verificada en
  prod con backfill de 12 filas; y la suite completa en **430/0** tras arreglar 5 rojos que **no** eran
  de carga. Al servidor lo mataba otra sesión con `pkill -f "next-server"` — cambiar de puerto no
  protege. Guard nuevo: el teardown compara los PIDs anotados al abrir.
- **Mergeado a main (411434ad, 94139195)** e issue #1584 cerrado. Perímetro de `/admin` medido con
  28 casos (`admin-perimetro.spec.ts`) y **ADR-011**: la suite E2E no lleva sesión superadmin —ese
  privilegio gobierna la plataforma y la suite corre contra el proyecto de producción—, así que las
  24 páginas de admin no se smokean y se cubren por contrato + expulsión. De la mutación salió que
  hay **dos puertas independientes** (proxy + `AdminGuardedShell`): quitar una no da víctima.
- **Cerrado 07/08-ago**: panel de tickets, soporte 133-138, ticket 135, tanda 142-145 y tap target del
  `Segmented`.

## 10-ago (tarde) · La cola del barrido, cerrada entera (PRs #1592, #1593, #1594)

- **Eje cross-org: 29 → 59 endpoints medidos**, 0 fugas, **0 no concluyentes**, 0 filas de la otra
  organización modificadas. Dos palancas. (1) Cuerpo válido en `CUERPOS_PARAM` para los 18 no
  concluyentes de Obras: los 16 handlers se abrieron uno a uno y comparten el orden **Zod (422) →
  tenancy del PATH (404) → recursos del CUERPO (422)**, que es lo que hace que el caso corte en la
  valla; los UUID del cuerpo son inexistentes a propósito, porque no llegan a resolverse y un id real
  le daría a una fuga algo que romper. (2) **Sonda hermana**: `sondaLecturaDe` solo aceptaba `GET`
  que TERMINAN en el parámetro, y eso dejaba sin medir las nueve escrituras de `facturas/{id}/*`
  aunque `facturas/{id}/pagos` exista.
- **El fallo de método que pagó la corrida**: al ampliar la sonda entró `GET /clientes/{id}/mandatos`,
  que es una **colección anidada** y devuelve **200 con lista vacía** para un cliente de otra org. El
  eje cantó **4 fugas cross-org que no existían** (sin escribir nada: la sonda corta antes). El
  arreglo no fue una lista negra sino exigirle a la sonda que **demuestre que sabe fallar** — se pide
  con un id inexistente y, si no da 403/404, el caso se declara no medido. Mismo error de fondo que
  el `>= 400` del corte anterior. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
- **Fuera del eje (b) con motivo, en lista APARTE de las exclusiones** para no perderlas en la
  dirección (a): las dos fusiones cliente/proveedor (eliminan el origen) y `PATCH facturas/[id]` (no
  hay cuerpo inerte: `lineas` es obligatorio y el handler las reemplaza).
- **Los 24 sin sonda: fuera de alcance por escrito**, con las dos salidas descartadas y su motivo —
  un `GET` de colección no discrimina (medido) y usar la escritura como control positivo exige
  escribir en la org A, sin vuelta atrás para los 18 DELETE.
- **Los 2 rojos que quedaban NO se reproducen**: ni encadenados con su fichero vecino (24/24) ni en
  tanda completa sobre main (**493 verdes, 0 rojos, 125 saltados, 21,5 min**). Sin tocar ningún tope,
  y `workers: 1` ya descartaba que «carga» pudiera ser concurrencia interna.
- **Páginas 55 → 66/97**: las 5 de `/informes`, 4 sueltas y `/login` + `/verificar-telefono`. De
  `/login` faltaban los **bordes** (el camino feliz lo recorre `auth.setup.ts`): credenciales
  inexistentes con el mensaje concreto, envío sin email y el `?redirect=`. **Hallazgo**: el registro
  daba `/verifactu` por «panel de cumplimiento AEAT» y es la **landing pública de captación**; el
  motivo escrito describía otra página.
- **Dos mutaciones sin víctima seguidas, dos causas distintas** (el orden de sospecha del CLAUDE.md,
  literal): primero el arnés —`mutate` no reinicia el servidor y **Turbopack no recarga el proxy**—,
  después dos guardas —el proxy pone `redirect` en dos sitios y se mutó el del step-up 2FA en vez del
  de sesión ausente—. Con el correcto: víctima.
- **La tanda de cierre destapó un rojo REAL (issue #1595)**, y es el hallazgo con más valor del día:
  `recibida-vencimiento` › «el vencimiento corregido tras aprobar llega a la factura» falla **2 de 3
  pases AISLADO**. Lo que discrimina: invirtiendo el orden de las aserciones para consultar la BD
  antes que el toast, cuando falla sale `NO_LLEGO_A_BD` — **no es un toast efímero, es el guardado
  que no ocurre**, sin aviso de éxito ni de error. El input muestra la fecha y la base no la tiene.
  El silencio nace en `ui/date-picker.tsx` › `commitDraft()`: su rama `else` ni llama a `onChange` ni
  avisa. El `toHaveValue` intermedio que se añadió el 10-ago por la mañana para cerrar esta carrera
  **no basta**: pasa, y el dato se pierde igual. No se arregló en el momento a propósito —
  `ui/date-picker.tsx` es el componente de fecha de TODA la app— y es misma familia que qa-002/003/008.

## Retirado del NOW en la poda del 11-ago-2026

Entradas cerradas o resueltas que estaban pagando peaje en el dashboard de arranque. Se conservan íntegras:

- ✅ **Logo oficial de tuFacturaIA en toda la app, favicon, PWA y emails, en prod (11-ago, #1608)** — sidebar/auth/onboarding/landing pública/emails con el mismo componente `<Logo>` (paths reales, `currentColor` sigue el tema solo). `/fia-cierre` cazó 2 bloqueantes reales: el logo se volvía invisible en dark mode y el PNG del footer de email sin trackear — corregidos antes de mergear. **Decidido NO llevar el azul del logo a `--brand` global** (falla contraste AA en texto blanco, verificado con artifact). Incidente aparte: 2 SVG de referencia se colaron en el PR ajeno #1600 (ya en main); limpieza en #1604. → [[git-head-compartido-entre-sesiones-paralelas-sin-worktree]]
- ✅ **Barrido funcional: ejes transversales cerrados y su rojo real arreglado (10/11-ago, #1583→#1597)** — cross-org 29→**59** sin fugas, #1595 cerrado. Detalle → [[facturaia-historico-detallado]] · `docs/qa/funcional/INFORME.md` · [[estado-cargado-por-effect-como-precondicion-de-escritura-descarta-el-gesto]]
- ⚪ **Copiar el catálogo de WAPI a la org real: RETIRADO (07-ago)** — contradecía tres decisiones de Natalia y el catálogo copiado valdría **4,72× lo que IET cobra**. Motivos y cifras → [[facturaia-historico-detallado]]
- ⚪ **Sugerencias de IA del tipo de MO: NO aceptar las 1.433 en lote (07-ago)** — contra los 43 con tiempo real de WAPI: 44 % dentro del ±10 %, error medio 131 %, y la confianza autodeclarada no discrimina (0,90 con −85 %; 0,80 con +3.757 %). Solo donde no haya dato de WAPI y con revisión. Cifras → [[facturaia-historico-eventos]]
- 🟠 **Truncado a 1.000 filas: cerrado donde importa (02-ago, #1475→#14** — tiene pendientes, ver histórico. Detalle → [[facturaia-historico-detallado]]
- 📗 **Referencia visual + `design-starter` en `agentesia-skills`, en prod (03/04-ago, #1517)** — clon del sistema de diseño para arrancar productos nuevos de AgentesIA con el mismo look desde el primer commit. Detalle → [[facturaia-historico-snapshot-2026-08-03]]
- 🟠 **Los avisos donde se arreglan, en prod (03-ago, #1507 + #1510)**** — tiene pendientes, ver histórico. Detalle → [[facturaia-historico-detallado]]
- 🟠 **Los avisos por email de tickets funcionaban; el falso negativo e** — Queda. Detalle → [[facturaia-historico-detallado]]

### 11-ago-2026 · crons por contrato (#1615) y el guard de partidas de Obras en prod (#1616)

- ✅ **Crons: la capacidad de reportar fallo, cerrada por CONTRATO (11-ago, #1615)** — el mecanismo existía (`withCronTracking` marca fallido con `ok:false`) y **diez de 45** crons no lo usaban; dos ni devolvían `ok`. En vez de parchear las diez puertas entra un contrato derivado del repo (`src/lib/cron/__tests__/conformidad-registro.test.ts`) que exige estar en `CRON_REGISTRY`, que cada entrada tenga handler, devolver `ok`, y derivarlo con `resultadoCron()`; excepción declarada en el fichero con razón de ≥20 caracteres. **Salió rojo en 4 de sus 6 casos** y corrigió mi propia cifra (yo conté 12 buscando incrementos; `enrich-batch` AGREGA con `reduce`). De paso: `verifactu/process` marcaba `rechazada` tras 26 h sin avisar (ya emite `verifactu_envio_fallido`, kind que llevaba desde el principio «reservado sin emisor»), y dos crons guardaban `cron_runs.summary` a NULL. `agentic-ocr-digest` registrado, con su horario marcado **sin confirmar** — hay que mirarlo en Dokploy.
- ✅ **Obras deja de escribir `stock_actual` de un producto con partidas — mig 659 EN PROD (11-ago, #1616)** — verificada por catálogo: las dos funciones con su `raise`, `anon`/`authenticated` sin `EXECUTE`. Redefinición comprobada con **diff normalizado** de los cuerpos contra las migs 506/518: el único delta es el guard. **OJO con el alcance**: el guard está verificado por catálogo y por texto, y las 190 smokes verdes descartan regresión, pero **no está ejercitado de punta a punta** — los casos de albarán que corren son de permisos (403, cross-org), no del camino de stock, y no existe en ningún sitio (ni en sandbox) un material con lotes dentro de un albarán de Obras.

### Retirado del NOW el 11-ago-2026 (segunda pasada)

Los baselines de linux siguen pendientes pero su propia entrada dice que no molestan mientras CI esté parado, así que no son NOW. Y lo de «main 5 commits por detrás» (04-ago) ya no es cierto: main está al día; lo que puede quedar de aquello es el WIP de skeletons, que tiene su propia entrada.

- 🔴 **`main` local 5 commits por detrás de `origin/main`, con WIP redundante encima (04-ago)** — faltan #1507/#1509/#1510/#1513/#1514, y hay cambios sin commitear en `pendientes-banner`, `welcome-banner`, `dashboard-shell`, `generar-view` y otros que parecen un intento paralelo de rehacer ese mismo trabajo ya mergeado. **Tuyo**: `git fetch && git diff origin/main` antes de tocar nada ahí — puede ser descartable entero.
- 🔧 **Regenerar los baselines visuales de linux (03-ago, #1510)** — a los `-linux` (los de CI) les faltan `TimeField`, `RadioCardGroup` y las píldoras de `Segmented`: al reactivar CI saldría rojo por desfase, no por regresión. Se regeneran dentro del container de Playwright, nunca en macOS (Docker sí hay, vía colima). Receta en `docs/design/13-gobernanza.md §5`. No molesta mientras CI siga parado. Ver [[baseline-de-screenshot-capturado-de-la-pagina-equivocada-es-verde-para-siempre]]

### 11-ago-2026 (tarde) · verificación de las tres capas y los dos cabos cerrados

- **Crons en Dokploy**: 45 schedules, todos `enabled`, y las 46 expresiones del registro coinciden una a una con las de Dokploy (comprobado por API con `dokploy-safe.sh`, compose `56B2b1ypWx3Xzdr06eYtG`). Cero discrepancias, cero schedules apagados, cero schedules fuera del registro.
- **`agentic-ocr-digest`**: 0 runs en `cron_runs`; aparece en `/admin/system?tab=crons` con «ÚLTIMA EJECUCIÓN —» y genera la alerta `cron_nunca_ejecutado` (severidad alta, se cierra sola). **No se le creó schedule a propósito**: empezaría a mandar correo semanal a dos clientes reales, decisión de Manuel. Antes de eso se arregló su asunto (#1618), que decía «aprobó 0 facturas» — y con 0 auto-aprobadas en las 3 orgs reales, ese era el 100 % de los correos que enviaría hoy.
- **Ejercicio de los guards en prod**: patrón `BEGIN … ROLLBACK` con escenario montado dentro de la transacción, así que residuo cero por construcción (verificado además por consulta). Sirvió para cerrar el límite que ambos agentes habían declarado honestamente: sus tests verifican texto SQL, no comportamiento.
- **Mig 660 (sobreventa)**: aplicada y verificada por catálogo (`anon`/`authenticated` sin EXECUTE). El `EXCEPTION WHEN OTHERS` que blinda la emisión puede ESCONDER un parámetro inválido para siempre, así que `severity` y `category` se comprobaron contra las constraints reales antes de fiarse.

### Retirado del NOW el 11-ago-2026 (cierre de la sesión del barrido)

- ✅ **Crons cerrados y auditados de punta a punta (11-ago, #1615/#1620)** — **46 de 46 con schedule activo en Dokploy, las 46 expresiones coinciden**. ¿Avisa siempre? **Sí** los 45 envueltos (fallo aislado pinga al instante); un zombi aislado no, **por diseño**; el único hueco era el propio `cron-watchdog` (exento del wrapper con razón, y por eso sin su aviso: 2 fallos, los dos invisibles) → cerrado. Y el salto a EMAIL **también medido**: 52 incidencias `alta` del health-sweep y **202 correos `system_alert` entregados** a 3 destinatarios desde el 16-jun. Límite estructural escrito: un envío fallido no puede avisar por email (sería circular) y sale como `emails_failed` MEDIA, solo visible entrando al panel. Detalle → [[facturaia-historico-detallado]]
- ✅ **Obras no escribe `stock_actual` de un producto con partidas — mig 659 EN PROD (11-ago, #1616), EJERCITADO** — ya no es solo catálogo: contra la función real en prod, producto con partidas → se planta con su mensaje; producto sin partidas → `validado`, `lineas_asentadas: 1`, stock 7 y su movimiento. En transacción con ROLLBACK, residuo 0/0/0 comprobado por consulta.
- ✅ **Sobreventa VISIBLE, no bloqueante — mig 660 EN PROD (11-ago, #1617)** — se descartó el `raise` (habría abortado la emisión desde `trg_stock_emit`) y entra un aviso `sobreventa_stock` blindado con `EXCEPTION WHEN OTHERS`, porque si el aviso falla no puede tumbar la factura. **Ejercitado en prod en transacción con ROLLBACK**: venta de 5 con 2 en stock → factura `pendiente`, stock −3, aviso con su forma exacta; control con stock suficiente → 45 y cero avisos. Residuo 0.

## Cierre del 12-ago-2026 — equipo de contenido: contenido-01 en prod

- 🟢 **contenido-01: pieza y máquina de estados de punta a punta (#1644 · PR #1658 · mig 667)** — `marketing_pieces` + `marketing_piece_versions` (RLS deny-all, CHECK que impide `aprobada`/`publicada` sin `approved_by`), función única `marketing_transicionar_pieza` (EXECUTE solo service_role), endpoints admin con `marketing_write`, espejo TS con gate anti-deriva verificado por mutación, panel `/admin/marketing/contenido`, 6 ideas sembradas y `calendario.md` reducido a investigación. Garantías probadas contra prod con ROLLBACK. El fia-cierre cazó un bloqueante real: la skill y el agente de marketing habían recibido la conexión psql de prod, contra ADR-012 — corregido antes del merge. Smoke post-deploy: lectura y 403 verificados en navegador; la mutación espera la decisión del grant `marketing_write` (hub §Decisiones). No se renumeró la 667: era de la propia rama ya aplicada (caso mig 651, verificado por catálogo). → [[adr-de-aislamiento-de-credenciales-aplica-a-todo-agente-con-ingesta-externa]]

## Hito 12-ago-2026 (tarde) — contenido-03 cerrado: topes con extensión aprobable

PRs #1666 (+#1667 registro del gate), issue #1646, migs 670+671 aplicadas y verificadas en prod. Gate de topes dentro de `marketing_claim_next_run` (runs/día global, €/mes de vídeo solo para `productor_video`; fila ausente = bloqueo), extensión puntual con ámbito temporal auditada con límite efectivo antes/después, incidencia por episodio en `system_alerts` que el claim cierra al volver a servir, tarjeta de topes + modal en el panel. Verificación: `scripts/smoke-topes-contenido.sql` 9/9 contra el esquema real (BEGIN/ROLLBACK). Dos cazas del cierre: el bug de coma flotante en la validación de decimales ([[math-round-por-100-rechaza-dos-decimales-legitimos]], del review de spec) y la fuga del marcador huérfano que motivó la 671 ([[marcador-de-bloqueo-sin-limpieza-en-todas-las-vias-de-salida]], del gate). Implementado con 4 subagentes en paralelo (Opus la migración, Sonnet endpoints/UI) contra un contrato de diseño único; el fia-cierre destapó además que los `args` del Workflow llegaron como string (ver `Stack/claude-code-harness.md`).

## Hito 12-ago-2026 (noche) — contenido-04 cerrado: aviso diario por email con deep link a la cola

PR #1670 (squash `b45bfd58`), issue #1647, sin migraciones. Cron `marketing-revision-aviso` (withCronTracking + resultadoCron): agrupa las piezas en `revision` en UN email a los perfiles `is_superadmin` («N piezas esperan tu revisión», hasta 10 títulos + «y N más», botón a `/admin/marketing/contenido`). Dedupe por destinatario y día de Madrid contra `email_log` (la idempotencia de `sendEmail` solo cubre 5 min); `failed` reabre el reintento de ese buzón, `pending` cuenta, fail-closed si no se puede leer; `count: 'exact'` contra el truncado de PostgREST en el «N» del asunto. Template `marketing_revision_aviso` en el sistema central con copy editable; `TIPO_PIEZA_LABEL` unificado en el espejo de dominio y traducido en el borde (el template no importa dominio, patrón ocr_digest — lo pidió el gate de deriva del grafo). La review de dos ejes cazó ANTES del merge el dedupe global que silenciaba el reintento en fallo parcial ([[dedupe-diario-de-email-multidestinatario-casa-destinatario-no-solo-dia]]). Schedule Dokploy dado de alta y verificado por API (`0 9 * * *`, timezone `Europe/Madrid` explícita, `sign-call.sh`); primer run ejecutado por el camino real (`docker exec` del comando exacto del schedule): 200, `sin_pendientes`, con lo que `cron_nunca_ejecutado` no llegó a sonar. Queda el smoke con piezas reales (hub §Smoke).

## 12-ago-2026 · copia de los PDF, watchdog, logo de emails y la partida inicial sin apunte

**PR #1671 — copia de los ficheros de Storage a B2 (mig 672).** Contenedor propio con `rclone` en
compose **aparte** del de la app (aísla las S3 keys del env que la API de Dokploy devuelve entero en
claro), que copia `facturas` y `logos`, verifica una muestra y reporta a un endpoint interno firmado.
Tabla `storage_backup_runs` + eventos, RLS deny-all. Tres cosas que no eran obvias: `copy` y nunca
`sync` (las S3 keys de Supabase no tienen variante de solo lectura); Supabase da MD5/ETag y B2 SHA-1,
así que `--checksum` cae a comparar TAMAÑOS y la muestra se verifica con `--download`; y la UI de B2
no sabe crear una key sin `deleteFiles` — medido con `b2_authorize_account`, «Read and Write» concede
25 capabilities, `bypassGovernance` incluida, al contrario de lo que afirma su runbook. El gate mide
B2 y Supabase por su cuenta con suelo en cada cifra; su primera versión decía «1415 objetos
verificados byte a byte» contra un bucket inexistente, el mismo error de `verificar-restauracion.sh`
cometido dentro del script que venía a evitarlo. Origen medido por dos fuentes independientes con
resultado idéntico al byte: 1.400 objetos / 524.349.117 B. Firma HMAC del contenedor comprobada
byte a byte contra `node:crypto`. **Falta solo el bucket y la key de B2.**

**PR #1672 — el watchdog y el logo de los emails.** El health-sweep mandó email ALTA el mismo día del
merge porque `storage-backup` no tiene schedule (espera credenciales): `pendiente_de_schedule` baja a
MEDIA sin silenciar. Y los emails de plataforma pintaban un monograma «T» porque `renderHeader` solo
acepta el logo de la ORG y en un email de plataforma no hay org; el logo de #1608 vivía solo en el
pie. El literal de config estaba **copiado en 7 ficheros**; ahora hay uno. El octavo
(`cobros/send-email.ts`) NO se tocó: ese email lo recibe el cliente de la org, y ahí nuestro logo
sería un error — queda como hallazgo de producto que ya sale con «TuFacturaIA» en cabecera.

**PR #1673 — mig 674, la partida inicial nace con su apunte.** Ver
[[backfill-guardado-por-invariante-en-vez-de-por-sintoma]] y
[[numero-de-migracion-libre-se-mide-en-prod-no-en-el-repo]]. Aplicada y verificada por catálogo:
partidas desalineadas 0 (eran 9), cero cambios en stock y coste.

**Issues abiertos**: #1668 (WORM escrito y sin enchufar: 23 declaraciones, 0 selladas, único
disparador un clic humano) · #1669 (staging 10 migraciones por detrás y la suite E2E midiéndose ahí).

## Contenido-05 — cierre del 12-ago-2026 (#1648 → PR #1674, mig 673)

Cola de aprobación del equipo de contenido como vista por defecto de `/admin/marketing/contenido` (ítem enfocado, contador, atajos A aprobar / C pedir cambios / S posponer — con guardas de modificadores y de modal abierto —, kanban de solo lectura, tabla original como tercera vista, acciones en barra fija en móvil). El rechazo exige comentario, versiona la MISMA pieza (historial colapsado en la card) y acumula el comentario como regla de estilo en la misma transacción del RPC (mig 673: `scheduled_for`, `marketing_style_rules` deny-all, `marketing_transicionar_pieza` redefinida con `p_scheduled_for`, DROP de la firma vieja). Reglas visibles/editables en el panel (CRUD auditado) y servidas al runner por `GET /api/internal/marketing/reglas-estilo` con whitelist `{id, texto}` (contrato §4). Al aprobar, fecha sugerida lun/mié/vie editable (`sugerirFechaPublicacion`, helper puro con tests). Manual-admin §50.4. Ejecutado con 6 subagentes Sonnet en paralelo (BD, API, UI, docs, e2e, review de 2 ejes) + síntesis crítica; el «hallazgo crítico» del review era un artefacto de base desactualizada (main avanzó 3 veces durante la sesión: #1671 ocupó el 672, #1672, #1673 ocupó el 674). Suite 11.523/0. Smoke e2e escrito (`marketing-contenido-cola.spec.ts`, solo lectura, + 5 mutadores a `BUTTON_BLOCKLIST` — «Añadir» regla era POST directo auto-habilitable por el monkey del crawler) pero sin correr: bloqueado por #1669 (staging desalineado). Ver [[boton-de-icono-nuevo-en-facturaia-button-sm-no-icon-btn]] · [[git-add-intent-to-add-rompe-stash]].

## Contenido-06 cerrado de punta a punta — 13-ago-2026 (movido del hub §Smoke)

Preview fiel + bucket de assets (issue #1649; PRs #1676 y #1677 de follow-ups; mig 675
aplicada y verificada por catálogo). Smoke COMPLETO en prod con agent-browser: MP4 real
subido desde la card y reproducido en el marco de móvil desde URL firmada de
`marketing-assets`; 2 slides PNG al carrusel (dots, contador 1/2→2/2, snap exacto slide
a slide); copy en vivo + guardado + vaciado persistidos en BD; borrado de los 3 assets
con confirmación; el 403 previo al grant probó el gate de permisos. **Grant
`marketing_write` ejecutado por Manu (12-ago)** para `m.delmonte.p@agentesia.madrid` —
primera fila de `superadmin_permissions`, desbloquea también el smoke de mutación de
contenido-01. Prod quedó limpio (0 assets, copy null). Gotchas de la sesión:
[[agent-browser-fill-vacio-no-dispara-onchange-react]] ·
[[turbopack-rechaza-symlink-node-modules-en-worktree]].

## 2026-08-13 — contenido-07 cerrado: runner esqueleto + coordinador determinista, DESPLEGADO en prod (#1719, #1720)

- **Coordinador en la APP, no en el runner** (el contrato de contenido-02 manda: «solo la app encola»): función pura `decidirRunsDeLaNoche` (`src/lib/marketing/contenido-coordinador.ts`, 13 fixtures) invocada por el cron `marketing-coordinador` (03:20 Europe/Madrid, schedule REAL en Dokploy `tYLXsRdoWtLPLJBXzdVll`). Reglas fijas: idea → guionista/copy_ads; guion de reel → productor; backlog <6 → ideación; lunes → analista. Sin LLM: sin cupo no hay empates, solo orden determinista de cola. Gate `AGENTES_CON_ESPECIALISTA` (espejo de `services/marketing-runner/agentes.mjs`): hoy todo apagado → el cron reporta `en_espera` y no inserta nada, evitando fabricar rachas de `fallido` sintéticas.
- **Runner** `services/marketing-runner/` (ADR-012, sin credenciales de BD): imagen node:22-slim + claude CLI, loop claim firmado → agente → resultado/error, modo `--once`. Desplegado como compose `marketing-runner` en Dokploy (PR #1720; alta por API: compose.create + compose.update + env solo porque era servicio nuevo). UNA réplica (gate de topes, mig 670). Secretos en 1Password FacturAIA (ids en la memoria del agente).
- **Salud con dueño** (`runner-salud.ts`): `runner_sin_claims` (pendiente >20 h, la resuelve el siguiente claim) y `runner_fallos_sostenidos` (3 fallidos seguidos, la resuelve un run completado); severidad alta, detección en el cron del coordinador. Guard toda-alerta-tiene-dueno verde.
- **Panel**: card «Runs del runner» + `GET /api/admin/marketing/contenido/runs`.
- **Verificado en prod**: primer run guionista encolado desde el panel a las 02:03, reclamado y completado por el contenedor a las 02:07 (resultado `esqueleto: true`); el intento previo local dejó probado también el camino `/error`. Piezas de prueba descartadas.
- Gotchas nuevos: [[claude-headless-hereda-hooks-y-mcp-del-proyecto-del-cwd]]; alta de compose por API documentada en [[docker-infra]] §alta de un servicio Compose por API.

## Hito del 13-ago-2026 — contenido-10 cerrado (#1653 → PR #1728, merge `1a1976ea`)

- **Ideación**: el ritmo 3/semana queda codificado como objetivo POR TIPO en el coordinador (`RITMO_SEMANAL {carrusel:2, reel:1}` × colchón 2 semanas); el déficit dispara la regla, viaja whitelisted al especialista (`GET /ideacion-contexto`, contrato §5: la app decide CUÁNTAS, el modelo CUÁLES) y recorta al aplicar, con dedupe por título normalizado contra todo lo no descartado. Pedido a cero → `{ideas: []}` sin lanzar Claude.
- **Copy de ads**: piezas `ad` con campos RSA (titulares 3-15 ≤30 sin `!`, descripciones 2-4 ≤90, keywords, campaña como enum del plan de Google Ads), validados por la app con 422/`fallido`; encadena hasta `revision` y la cola pinta el anuncio como resultado de búsqueda + desglose con contadores. La reescritura de un `ad` rechazado vuelve por `copy_ads`.
- `contenido-guion-aplicar.ts` → `contenido-aplicar.ts` (núcleo único guion/anuncio/ideación, incidencia con dueño por vía). `AGENTES_CON_ESPECIALISTA`: ideacion y copy_ads ON. Review de 2 ejes aplicada pre-merge (enum de campaña, límites explícitos en lecturas del backlog). Sin migración SQL; el runner se redesplegó solo con el merge.

## Hito del 13/14-ago-2026 — ticket #147 (ostra Chivite) cerrado, smoke real del runner de tickets, migración 685

- 🟢 **Ostra Nº3 de Pescados Chivite: causa raíz de código encontrada, no era un dato torcido (ticket #147, PR #1743, mig 685)** — `recompute_pmp` ponderaba compras sin `lote_id` en productos con lotes, mientras `recompute_stock`/`recompute_lote` (mig 312) ya las excluían desde meses antes: dos funciones sobre el MISMO ledger con criterio distinto. El `stock_actual=1` que el hub daba por «duplicado» YA era el saldo real — con el `audit_log` completo se ve que el «5» venía de DOS compras huérfanas de la misma mañana del 1-ago (no una), la primera la borró el propio cliente el 13-ago (recuperando el flujo que la mig 620 abrió) y la segunda sigue en una factura `disputada` sin cerrar. Lo que sí corrompía era `coste_medio`. Fix lote-aware + backfill, aplicado a prod vía Management API (push por CLI bloqueado por red del entorno, ver [[supabase-pooler-timeout-isp-fallback-dashboard]]) y verificado con datos sintéticos en sandbox antes/después del deploy. Cliente avisado en el hilo del ticket con aviso de riesgo de duplicado si reaprueba el mismo albarán. Ver [[una-media-ponderada-acumulada-no-se-corrige-repitiendo-la-operacion-buena]].
- 🟢 **Smoke real del runner «Resolver con Claude», cerrado el pendiente que llevaba desde el 25-jul** — ticket `32e1eebf` → job `dfe9b77b` → PR #1741 (fix aprobar-cierra-visor): el runner se comportó exactamente como debía, lo dejó en DRAFT sin merge automático cuando su propio gate de `tsc` murió por OOM (contenedor a 3 GB), con la justificación completa del `--no-verify` en el commit. Revisado con recursos normales (lint/typecheck/build limpios, 74/74 tests) y mergeado a mano. Resumen para el cliente publicado desde el panel. Confirma el eslabón de entrada que faltaba: el botón SÍ lanza el job headless y el runner NUNCA mergea solo.
- 🟢 **Colisión real de número de migración (678), detectada y cerrada antes de que hiciera daño** — otra rama (issue #1695, `api_keys.key_type`) reservó el mismo 678 sin haberla aplicado aún; sin corregirlo, el siguiente `db push` la habría dado por aplicada (por la mía) y se la habría saltado en silencio para siempre. Renumerada a 685 tras tres colisiones en cascada (repo fusionando ~1 migración cada 1-2 min ese rato). Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] (nuevo GOTCHA).

## Hito del 14-ago-2026 — contenido-09d + contenido-14 en prod, smoke del primer reel VERDE

- 🟢 **Productor de IMAGEN (#1745 → PR #1767, migs 689/690)** — carruseles y posts generan sus creatividades con Popcorn (0,092 $/img), referencia de marca por URL o por asset fijado (se guarda el path y se firma fresco en cada run, para que no caduque), imágenes limpias (el texto lo pinta la plantilla del preview), coste contra el tope renombrado «Generación (€/mes)». Discriminador del estado `guion` por datos (la versión vigente tiene `contenido` o no) compartido entre cron y preselección del modal.
- 🟢 **Mix semanal + pilares (#1747 → PR #1765, mig 688)** — `OBJETIVO_BACKLOG` a `system_config` (`marketing_mix_semanal`), posts auto-reponibles, pilares con cuota (resto mayor), columna `pilar` visible/filtrable (incluidos retirados). El coordinador sigue puro: la config viaja como parámetro.
- ✅ **Smoke del primer reel real (pendiente desde contenido-09): VERDE** — «Generar ahora» → claim → 5 clips Higgsfield → vídeo en bucket → pieza en `revision` con preview reproducible. Coste 2,25 € clavado a la estimación. Costó tres asaltos: créditos de API (`not_enough_credits`, el error ahora incluye el `detail` del cuerpo), tope `runs_dia` consumido por los fallos previos (extensión aprobada, auditada), y el segundo cuelgue del runner (abajo).
- 🔴→🟢 **Dos cuelgues del runner el mismo día**: 37 h de crash-loop por el `COPY` lista-blanca del Dockerfile (#1763, ahora glob + env Higgsfield mapeado en el compose) y 7 h de proceso wedged con contenedor `running` (restart vía `docker.restartContainer` de la API Dokploy). `runner-salud` no vio ninguno → issue **#1771** (alertar por cola pendiente sin claims, no por ausencia de 20 h). Ver [[dockerfile-copy-con-lista-blanca-crash-loopea-al-anadir-modulos]] · [[detector-de-salud-por-ausencia-larga-no-ve-un-cuelgue-con-cola-pendiente]]
- 📋 **Medido el catálogo real de la API de Higgsfield** (`GET /models`): 13 modelos (Soul/Popcorn imagen, DoP i2v, soul-id). Sin Seedance/Kling/Veo — esos son solo de su webapp; la vía API para ellos es fal.ai (adaptador listo, falta `FAL_KEY`). Prompt de continuación reescrito para #1748+#1655 (PR #1772).

## 2026-08-14 (noche) — Máquina de marketing completa (spec #1643, fases 1-4) + alta Meta

- **#1748 explorador de tendencias** → PR #1775, mig 691: corre los domingos con WebSearch como única herramienta (el contenido web hostil muere en su run), propone ≤8 tendencias con caducidad, el panel las muestra con descarte, y la ideación de esa noche las cita (`leerConceptosCitables` cierra la race descarte↔run).
- **#1771 salud del runner sensible a cola** → PR #1777: `hayColaParada` (45 min con pendientes y sin claims, lease vivo suprime), gate de topes recalculado para HOY (el episodio de ayer abierto ya no tapa un runner muerto), watchdog del ciclo a 55 min bajo el lease de 60.
- **#1654/#1655 métricas + analista semanal** → PR #1780, mig 692: snapshots ACUMULADOS diarios (UNIQUE pieza+fuente+fecha, ventana 7 días), `actividadEnSemana` por deltas contra la mediana orgánica de publicadas; analista en Opus los lunes con propuestas aceptar/descartar (reordenar backlog + mix), credenciales cifradas en `system_config` y el GET nunca las devuelve. La review Spec cazó el fallo gordo: el contexto servía acumulados de por vida etiquetados «de la semana».
- **Migs 691-692 por SQL editor** (pooler de prod caído todo el día): `INSERT` en `schema_migrations` para registro fiel + verificación por catálogo vía Management API. Ver incidente en `Stack/incidents.md`.
- **Alta Meta completa**: caso de uso «Administrar mensajes y contenido en Instagram» + `pages_show_list`/`pages_read_engagement` a mano; página FB `TuFacturaia` (1194843583723159) creada, `@tufacturaia` (IG 17841438173452357) enlazada; token largo canjeado leyendo secretos de 1Password sin imprimirlos, verificado con run manual del cron en `success` (`instagram.conectada: true`). Perfil y portada de la página generados con la marca en `~/Downloads/tufacturaia-facebook/`. Gotchas → [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]].
- Schedules Dokploy: `marketing-runner-salud` (*/15) y `marketing-metricas` (04:10 Madrid). Pendientes menores: `gen:types` al volver el pooler, renovar token Meta ~10-oct, conectar Google Ads, pegar `publicacion_ref` al publicar.


### 2026-08-14 · contenido, spec #1643 fases 1-4 (movido del hub el 15-ago)
- 🟢 **Contenido COMPLETO, spec #1643 fases 1-4 (14-ago)** — #1748/#1654/#1655/#1771 (PRs #1775/#1777/#1780, migs 691-692), Instagram conectada y verificada. Gestos: `publicacion_ref` al publicar · **token Meta ~10-oct** (ítem 1P) · `gen:types`. Siguiente: #1787 y grill panel/IG/Ads → [[facturaia-handoff-contenido-panel-ig-ads]] · [[facturaia-historico-detallado]] · [[graph-api-de-instagram-exige-pagina-vinculada-y-la-concesion-es-pegajosa]]

### 2026-08-16 · empaquetado, ola 1 de la fase 2 (movido del hub el 16-ago)
- 🟢 **Spec #1678 CERRADO (15-ago)** — circuito de cobro probado con eventos reales de Stripe. Su único pendiente, #1686, sigue vivo con entrada propia en el hub. → [[facturaia-historico-eventos]] · [[ADR-052-persistir-el-motivo-de-la-suspension-de-cobro]]
- 🟢 **Ola 1 del empaquetado, 6 PRs en `main` (16-ago)** — #1841 (#1702 PR 3/4: la compra sale del catálogo real), #1839 (#1711 invariantes + `alert-collectors` 900→183), #1840 (#1712 matriz en `/admin/packaging`), #1838 (el arnés de mutación emparejaba test↔código solo por alias y era ciego al 76 % de la suite), #1842 (main quedó rojo por composición: cuatro PRs verdes por separado) y #1843 (candados anti-duplicado que hacen segura la futura partición de `cron/registry.ts`). Salió además que la app anunciaba dos precios que nadie cobraba —19 € de conciliación y 30 € de multiempresa frente a los 12 € reales de `empresa_extra`— y un collector que iba a escribir en la base en cada apertura del panel de alertas. → [[columna-de-precio-que-se-rellena-sin-que-exista-el-cobro-anuncia-humo]] · [[un-collector-que-tambien-corre-en-un-get-no-puede-escribir]] · [[arnes-de-mutacion-que-busca-el-alias-no-ve-los-tests-en-relativo]] · [[la-suite-completa-bajo-paralelismo-no-distingue-regresion-de-saturacion]]

### 2026-08-18 (tarde) — cuatro pistas en paralelo, y un 500 que llevaba desde siempre

- **#1778 PR 1 abierta (#1877)**: `billing_facturas_suscripcion` con la forma literal del §6 del plan, `facturas.stripe_invoice_id` con índice único parcial, serie dedicada `X`, override de `org_limits` y `stripe_suscripcion` en el CHECK del ledger. El perímetro que le di al subagente **divergía de mi propio plan escrito** (le pedí otra tabla, con otro nombre y otras columnas); lo detectó él y lo dijo en su informe en vez de tragárselo. Verificado por catálogo en prod que el CHECK inline de la mig 640 se llama `factura_pagos_origen_check` — con otro nombre, el `DROP IF EXISTS` habría sido un no-op y el `ADD` habría creado un segundo CHECK que seguiría rechazando el valor nuevo en ejecución.
- **El fichero oficial de la AEAT nunca funcionó**: em-dash en `STATUS_303_POSICIONAL`, que viaja en `X-Fiscal-Status`. Toda descarga de `?formato=oficial` devolvía 500 tras componer el fichero entero. 0 descargas en toda la historia y 0 tests en la ruta: lo destapó el primer test escrito contra ella. → [[cabecera-http-con-caracter-fuera-de-latin1-tumba-la-respuesta]]
- **ADR-019**: el bloqueo por deriva parte por FORMATO. `oficial` se bloquea (409, mismos códigos que `sellar`); `apoyo` no, porque es un documento de trabajo que el usuario transcribe al Pre303 — lleva aviso en cabecera. `FiscalDeclaracionResumen` gana `requires_recalc`, que era la raíz de los siete consumidores ciegos.
- **Auditoría fiscal completa, medida**: la cadena de `requires_recalc` ya estaba cerrada donde produce un acto (`sellar`, `fiscal_marcar_presentada`, agregación del 390 en `modelo-390.ts:55`). Lo ciego era la capa de presentación. 26 declaraciones, 25 en `borrador`, 0 presentadas, 0 selladas. VeriFACTU apagado en las 9 orgs reales.
- **Inventario**: las 6 lecturas del T1 eran 8 físicas y ninguna estaba paginada. Dos daban el dato EQUIVOCADO, no menos filas. → [[postgrest-max-rows-trunca-silencioso-in-revienta-url]]
- **Decidido no tocar staging**: 46 migraciones por detrás y cero consumidores.

## Poda del dashboard — 2026-08-19 (cierre de #1856)

Retirado del dashboard del hub por el trinquete de contexto; queda aquí el detalle:

- **Contenido #1791**: spec cerrada, 7/7 en prod el 17-ago. En el dashboard queda solo el pendiente de Manuel (schedule `marketing-publicar` en Dokploy + wizard del token de Google).
- **Gate automático de promoción (12-ago)**: los jobs de Actions morían en 2 s con 0 pasos, y los verdes de Dependabot NO significan que Actions funcione. Los otros dos requisitos sí están cerrados: RLS (mig 665) y restauración ensayada (#1642).
- **Copia de los PDF / Backblaze**: login por la pestaña *Individual Account* con `info@agentesia.madrid`, contraseña en el ítem 1Password `Backblaze` (no hay 2FA guardada; si la cuenta la tiene, es lo que falta). Mientras los campos sigan con `PEGAR_AQUI`, `npm run backups:storage:verificar` sale rojo. Salidas alternativas medidas: Wasabi (su mínimo de 1 TB ya se paga → coste marginal cero) o R2; cambiar destino son 3 variables.
- **#1856 (cerrado, PR #1893, mig 711)**: el embudo de reclamación tenía dos mitades divergentes —la función SQL del cron y el espejo TS— y le faltaban dos de tres patas de «lo ya cobrado» (ledger `factura_pagos` y resto de conciliación). Las dos delegan ya en `factura_cobros_resumen`. Daño cero medido en las dos exposiciones. Deudas abiertas: #1897 (el selector SQL sin un solo test) y #1898 (`garantiasVivasPorFactura` sin trocear ni paginar). → [[cuenta-los-motores-que-calculan-el-mismo-numero-antes-de-arreglar-uno]]

## 2026-08-20 · Growth Fase B: la cadena de conversión entera, en prod en un día
- **FB-07** (#1987+#1996): outbox `marketing_conversion_outbox` (mig 725, doble idempotencia UNIQUE+transactionId), dispatcher a Data Manager API, cron `marketing-conversiones` cada 5 min con schedule verificado por run real. Bloqueado solo por el token con scope `datamanager` (2FA de Manu).
- **Consentimiento `fia_gclid`** (#2001+#2004): banner AEPD en /registro (gemelos, primera capa reescrita a tono de sector a petición de Manu), política /cookies nueva, `consentimiento_at` (mig 726, aplicada pre-merge y verificada por catálogo tras el aviso cross-sesión de que rompía `db push` de todos). El smoke de prod cazó que el aviso no se desmontaba al decidir (la decisión recién pulsada parecía «del futuro» frente a `CARGA_MS`); fix con reloj que avanza en cada escritura.
- **FB-02 negativas** (#2008+cabos): search_term_view agregado, juicio LLM con motivo, mutate atómico SharedSet/SharedCriterion/CampaignSharedSet verificado contra discovery v25. El gate cazó un bloqueante real (tope 60 propuestas vs schema 50 = botón muerto en 400) + 6 avisos, todos cerrados en el mismo PR.
- **FB-10 landing apex** (#2010+#2011, ADR-020): routing por host en el proxy (función pura con tests + test de la traducción), robots/sitemap POR HOST (el gate cazó que el apex heredaba `Disallow: /`), gclid EN el HTML servido (Suspense streaming de Cache Components), dominios+certs dados de alta por API (domain.create → compose.deploy → reloadTraefik). Smoke real: 200 con CTA `?gclid=`, www→308, path→307, Let's Encrypt emitido.
- **Incidente propio**: #2010 se mergeó una vez con la punta vieja (pre-push abortado + comparación remoto==local como echo, no como gate). Fixes en #2011; la comparación es ahora condición dura del merge. También main en rojo ~15 min por /cookies sin declarar en el registro de QA (#2004).
- Gates de cierre corridos y registrados (#2009, #2012); suite completa final 1.308 ficheros / 13.709 verde. Prompt de continuación: `PROMPT-growth-fase-b-resto.md` (#2013).

## 2026-08-21 — Growth Fase B cerrada: FB-09 + llave datamanager
- **FB-09 analista semanal** (#1952) en prod: PR #2029 (cron lunes 08:00 Madrid, informe sin LLM si la semana no tuvo actividad, tabla `marketing_ads_informes` mig 733, card en `/admin/marketing/google-ads`, email a superadmins), #2032 (composición + GAQL ligera) y #2034 (10 mejoras post-auditoría a dos agentes: dedupe de email POR SEMANA —un retry en martes reenviaba—, carrera de `guardarInforme` con `ignoreDuplicates`, cifras es-ES, pill «Informe antiguo», «50 o más» en el tope de recomendaciones; 2 mutaciones con víctima). Smoke real: cron success, informe persistido, 7 emails. Schedule Dokploy `0hUPoa7yHPpRVSw0icI23`.
- **Llave 1 girada**: token OAuth reacuñado con scope `datamanager`, GAQL validada antes de guardar, ingest validateOnly 200 (exige `loginAccount` del MCC en destinations).
- Abierto: **#2031** — la card de recomendaciones de FB-08 hace una GAQL que v25 rechaza (400 en prod); ver [[gaql-campos-del-discovery-doc-no-seleccionables-en-select]].
- **#2031 cerrado el mismo día** (#2041): en v25 la seleccionabilidad es por MENSAJE — el SELECT pide los padres (`campaign_budget_recommendation`, `impact`) y el apply con cifra validada queda intacto; guard de igualdad exacta con víctima por mutación; smoke real: card verde en prod.

## 2026-08-21 — la cola de tickets de soporte, vaciada (9 PRs) y el cierre automático al mergear

- **#2018** — el trailer `Ticket-feedback: #N` cierra el ticket al mergear el PR **aunque no lo haya abierto el runner** (antes solo cerraba los suyos). Vía github-webhook, `resuelto_via='manual'` + email de resolución.
- **#2019 + #2033 (ticket 152)** — el buscador del listado solo miraba `num`. Ahora busca por cliente/proveedor y NIF, y las recibidas **sin aprobar** por lo que leyó el OCR (`datos_extraidos->>prov`). El remate del #2033 es la insensibilidad a acentos: PostgREST no deja aplicar `unaccent()` a una columna, así que se pasa de `ilike` a **`imatch` con clases de equivalencia** (`[aáàäâ]`) y palabras unidas por `.*`. En prod convivían cuatro grafías del mismo proveedor; una consulta las devuelve las cuatro. → [[buscar-sin-acentos-en-postgrest-es-imatch-con-clases]]
- **#2020 (ticket 153)** — 26 recibidas en USD de una org llevaban desde el 13-ago sin poder aprobarse: el proveedor de divisas falló unos segundos y ese fallo quedó **escrito** en `bandeja_ingesta.tipo_cambio_fuente='manual_requerido'`, leído después como veredicto. Reintento en vivo al aprobar + descongelado de la bandeja, backoff en `getEurPorUnidad`, mensaje que ya no manda a un botón "Próximamente" y lote que enumera todos los motivos distintos. El pre-guard de cliente que aún cortaba la vía `/ingesta` cayó luego en **#2035** (otra sesión). → [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
- **#2021** (activar lotes abandonaba los movimientos anteriores; borrar la recibida no movía el stock), **#2022** (adjuntar PDF/XML en un ticket, no solo capturas), **#2023** (componer precio de venta ya no ofrece material sin mano de obra ni descuento).
- **#2026** — los tres candados que la tanda dejó en rojo sobre `main` (gates de rama que no ven la composición).
- **#2028 + mig 732** — auditoría cruzada de los seis PRs de la cola: el reenganche de huérfanos duplicaba stock.
- **#2033** — además del acento, los seis cabos diferidos de la auditoría: tipo canónico único de adjunto compartido por los tres consumidores, live region persistente en los avisos de búsqueda, chip de adjunto no-imagen sin recortar, y `eslint-disable` muerto.
- **Respuesta a 152 y 153 publicada en su hilo el 21-ago** (mensaje público → email al cliente). Los tickets se habían cerrado solos por trailer y `feedback_ticket_messages` no tenía **ni una fila** de aquel día: el estado es lo barato de automatizar, la respuesta no. → [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]]
- **Sin responder todavía**: #89, #129 y #134 (entregados, en `en_revision`). #125, #126 y #128 siguen abiertos a propósito.

## Condensado del NOW · 21-ago-2026

- 🟢 **Cola de tickets de soporte vaciada; el ticket se cierra solo al mergear (21-ago)** — 9 PRs en prod (#2018-#2023, #2026, #2028, #2033): buscador con tildes (152), las 26 recibidas en USD congeladas desde el 13-ago (153), adjuntos PDF/XML, stock de lotes, mig 732. **Respondidos 152 y 153. Queda**: #89, #129 y #134 arreglados y con el hilo **vacío** — cerrar por trailer no responde a nadie. Detalle → [[facturaia-historico-detallado]] · [[buscar-sin-acentos-en-postgrest-es-imatch-con-clases]] · [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]] · [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
- 🟢 **El OCR ya aprende el DATO de cada proveedor Y eso desbloquea la auto-aprobación (20-ago)** — migs 728+731 en prod, PRs #2015 y #2024. A la tercera corrección igual del mismo emisor (moneda, IVA, IRPF, forma de pago, categoría y ahora **`es_intracom`**) el sistema lo rellena solo; si el documento la contradice **no la pisa**, avisa. Con el paso 3, lo que ese proveedor hace SIEMPRE deja de pedir un clic: `tiene_irpf` y `es_intracom` ya no tumban a ámbar si coinciden con su regla verde (`moneda_manual_requerido` y `proveedor_no_confianza` siguen intactos, con test). Tres cosas que aparecieron por el camino: **`/ingesta` no registraba NINGUNA corrección** —el sitio donde de verdad se corrige la lectura— así que `auto_accuracy` medía de menos y ahora va a subir el número de correcciones registradas (ojo al gate ≥95/<90); la ambigüedad se calculaba mal y **una sola corrección mataba ese par (clave, campo) para siempre**; y `veces_confirmada` contaba peticiones, no confirmaciones humanas. Ninguno hizo daño: la tabla estaba vacía. **§4.2 (el cobro conciliado como señal) medido y DESCARTADO**: 30 casos en toda la historia de prod, 3 orgs, y `total` no es aprendible — su único destino sería §4.1, que no existe. **Lo siguiente del área es §4.1, confianza por CAMPO**, y antes el cierre: cinco hallazgos de la auditoría sin aplicar, cuatro decisiones de producto por investigar y decidir (la ventana para tocar la forma de la clave es AHORA, con la tabla vacía), un test rojo heredado en main, manuales y el smoke en pantalla. Arranque escrito → `docs/architecture/PROMPT-aprendizaje-ocr-cierre.md`. → [[clonar-una-migracion-clona-tambien-a-quien-puede-llamarla]] · [[un-mutante-sin-victima-tambien-puede-ser-un-guard-equivocado]]
- 🟢 **Google Ads — Fase B COMPLETA (21-ago)** — FB-09 (analista semanal) en prod y afinado tras auditoría a dos agentes (#2029/#2032/#2034); llave `datamanager` girada, smoke real verde. **#2031 CERRADO** (#2041: la GAQL selecciona los mensajes padre, smoke real verde en prod). **Encargada la siguiente tanda (21-ago)**: menú admin, cookies `fia_gclid` (decisión delegada), wizard del token, Growth desbloqueado, #1787, smokes y deudas → `docs/architecture/PROMPT-growth-menu-cookies-contenido.md` (en disco, entra en el primer PR). Campaña apagada. **Tuyo**: posible 2FA del token al arrancar. Detalle → [[facturaia-historico-detallado]] · [[gaql-campos-del-discovery-doc-no-seleccionables-en-select]] · [[data-manager-ingest-exige-loginaccount-del-mcc]]

## 2026-08-21 — Tanda growth/contenido/cookies (7 PRs, suite final 14.435/0)

- **#2048** menú admin: item Marketing en Negocio, promos deja de encender Cupones, ayudas grises (`topesHelp`) y variante `box` en el primitivo `Input` (el gate cazó la reimplementación a mano y obligó a llevarla a `ui/`). **#2067** el barrido: 12 `NumberField` de packaging/plans/marketing/cobros a `variant="box"`.
- **#2042** cookies: retirada del consentimiento en la web (AEPD §3.2.9), gclid huérfana borrable, responsable en capa 1, manuales usuario+admin. Gate cazó el test sin dientes (default-path RFC 6265) → spy sobre el setter con mutación verificada. Smoke prod: footer del apex → gestor, verde.
- **#2053** el 401 de los clips: el proxy de Next trunca a 10 MB en silencio y el HMAC hasheaba el body cortado (5 runs, ~5,40 € quemados 15-19 ago). Exclusión del matcher con guard compilado con el path-to-regexp real, reintentos re-firmando, preflight a coste cero, `last_error` con detalle. Issue #2055: assets del admin (100 MB declarados vs 10 efectivos), /api/upload y /api/feedback/upload siguen expuestas.
- **#2047** contenido-16 (#1787 cerrado): 4 hooks por modo + alternativos visibles en revisión, postura obligatoria en ideación, wizard de Instagram con el alta real de la Graph API 2026, y el recorte POR IDEA en el runner (el fix real de las 3 noches caídas: un campo >200 chars ya no tira el lote). El gate refutó con la API de Dokploy el «redeploy manual» del runner: autoDeploy=true, y el README que lo negaba se corrigió.
- **#2054** flujo de ideas: `fase=plan` rompe el deadlock de contenido-25 (el planificador no podía escribir el plan que se le exigía; la suite no lo vio por mockear el contrato), embudo por etapas con «Siguiente:», plan aprobable en el Preview, «Generar ahora» honesto (409 con motivo; distingue el caso que se serviría y gastaría sin aplicarse), runs pendientes no servibles marcados y cancelables (CAS atómico auditado), PATCH de ficha y PUT de guion fusionador con control optimista (conserva hooks_alternativos, anti-patrón Holded). Run de «Beta promoción» cancelado en prod desde la UI.
- **#2051** límites de presupuesto: DELETE con confirmación, auditoría antes→después en `marketing_audit_log`, vaciar campos avisa. El gate cazó el candado de trazas en rojo (regresión que habría roto main) → guard acepta `logMarketingMutation` y vigila el DELETE, con mutación. Residuo meta_ads del smoke borrado desde la UI nueva en prod.
- Método: fia-cierre en los 6 PRs con lógica (2 cazaron regresiones de main, 1 evitó un cuerpo de PR ajeno como mensaje de squash); QA visual claro+oscuro con artifact por PR; smokes de prod conducidos con sesión superadmin acuñada.

### 21/22-ago-2026 — retirado del NOW del hub en el cierre del 22-ago

- 🟢 **Cola de tickets de soporte vaciada; el ticket se cierra solo al mergear (21-ago)** — 9 PRs en prod (#2018-#2023, #2026, #2028, #2033). → [[facturaia-historico-detallado]]
- 🟢 **Retención de IRPF: área cerrada de punta a punta (21-ago)** — pasos 1-3 del aprendizaje en prod (migs 728/731/734) y hoy tres PRs más: #2050 (la retención se VE antes de aprobar, una sola aritmética del total, `EstadoPill` deja de hablar de cobrar en Recibidas), #2058 (mig 738: se corrige también en una factura YA aprobada, por RPC transaccional con bloqueo si está en declaración presentada) y #2066 (la cuota de IVA dejaba fuera la retención + guard sobre el patrón). Smoke real: **regla del emisor en VERDE** a la tercera corrección desde la ficha. → [[una-funcion-correcta-no-impide-que-la-reescriban-a-mano]] · [[un-candado-puesto-tras-un-incidente-puede-quedar-del-reves]] · [[facturaia-historico-detallado]]
- 🟢 **Google Ads — Fase B COMPLETA (21-ago)** — FB-09 en prod, llave `datamanager` girada, smoke verde. → [[facturaia-historico-detallado]]

- **2026-08-20 · compose que enumera variables** — los valores estaban en el panel de Dokploy pero sin línea en `docker-compose.yml`, así que no llegaban al contenedor: WhatsApp caído 8 días y el cifrado de IBAN nunca activo. Arreglado en #1993; el gotcha quedó en `docs/architecture/gotchas.md` §Repo y deploy (#2005).
- **2026-08-22 · multidivisa, remate del congelado** — #2089 (enum de motivo, deduplicación en vuelo, RPC `fx_aplicar_divisa_pendiente` mig 740, cron `fx-reintentar-pendientes` que abre y cierra sola su incidencia, UI en panel/ficha/listado), #2090 (equivalencia falsa «7,90 AED ≈ 7,90 €» y botón muerto en divisas sin cobertura) y #2091 (insignia de divisa a 1,1:1 en tema oscuro → 6,09:1). Prod: 26 filas congeladas → 0, 24 facturas mal denominadas → 0, 114 facturas a USD/bce, 1.353,15 USD → 1.183,87 EUR. Y **#2092** cerró el área: el campo de tipo de cambio manual no lo validaba nada, y `total_eur`/`base_eur` son columnas `GENERATED` desde la mig 173, así que un dedazo se multiplicaba en silencio hasta el 303, el libro de IVA, el cashflow y conciliación. Ahora se compara contra el BCE de la fecha de devengo (ADR-024) y se avisa por encima del 5 %, en `/generar` y en el bloque de `/ingesta`. Tres decisiones deliberadas: no bloquea (un tipo pactado es legítimo y la alternativa es no poder registrar la factura correcta), calla si no hay referencia (un aviso que sale siempre deja de leerse, y `null` no significa «está bien» — es el bug de #2089 otra vez), y juzga 400 ms después de la última tecla. El umbral cazó un bug real de coma flotante: `Math.abs(pct) > 5` era `true` para un 5 % exacto (`5.000000000000004`). Verificado conduciendo el navegador contra el BCE real del día (0,85477391 €/USD): 0,87 calla, el borde exacto del 5 % calla, un pelo por encima avisa. Contraste medido en los dos temas: 4,51:1 claro y 7,18:1 oscuro. Smoke en PROD tras el deploy (build 09:16) en las DOS superficies. `/generar`: sale con el BCE del día, 0,87 calla, 4,51:1 claro y 7,18:1 oscuro. `/ingesta`: el bloque «Falta el cambio a euros» solo existe cuando falta el cambio y el barrido dejó prod sin ninguna fila así, así que en vez de sembrar una se reescribió **la respuesta del listado en el navegador** (`--init-script` de agent-browser, solo GET) — componente real, CSS real y consulta al BCE real, con la fila intacta en la base. Ahí el aviso citó el tipo de la fecha DE LA FACTURA (07/08/2026 → 0,866927), que es exactamente el valor que la fila tenía en `tipo_cambio`: confirma la regla del devengo sin un solo write. Contraste con las 4 capas reales de esa superficie: 4,51:1 claro y 7,95:1 oscuro. **#2101 (22-ago, tarde)**: el barrido arreglaba lo arreglable y de lo demás no avisaba a nadie. Ahora emite `divisas_pendientes` en la campanita tras reintentar (agregada por org, `warning` porque sin el cambio no se puede aprobar, `expires_at` +36 h, conteo con `fetchAllPages` porque ese número lo lee el cliente). Cerradas sin código las otras dos puntas del S4 (el badge ya lo servía `counts.inbox`; `revisarBandejaMoneda` y la notif del desvío >5 % se retiran con motivo). La auditoría de composición de los cuatro PRs sacó `lib/multidivisa/aprobar-filter.ts`: un guard de aprobación que **solo llamaba su propio test**, y al borrarlo el módulo entero se quedó vacío. Gate completo verde (14.705 tests) y las cuatro aserciones nuevas verificadas por mutación.

### 22-ago-2026 · el `pre-push` escribía en el repositorio de todas las sesiones (#2103) + el aviso de los crons (#2104)

- **#2103 · la fuga de `GIT_DIR`.** Un `git push` desde un worktree ENLAZADO exporta `GIT_DIR` al hook; el hook corre la suite desde #2096; y con `GIT_DIR` puesto el `cwd` de los fixtures no aísla nada. Resultado en el repo LOCAL compartido por cuatro sesiones: 10 commits de fixture, ramas `qa/x`/`qa/ajenas`/`qa/ajenas-b`, la rama en curso movida a un commit «inicial» con un `a.txt`, `core.bare=true` (checkout raíz inservible para los demás) e índices de worktree desordenados —total correcto, `git ls-files <dir>` a cero—. Nada llegó al remoto. El síntoma engañaba: el push se rechazaba con «la suite está en rojo» y los rojos eran los ~18 tests que enumeran el repo, o sea consecuencia. **La primera versión del arreglo era insuficiente y su propio test era un foco**: el `beforeEach` montaba el repo víctima heredando `process.env`. Arreglo final: limpiar `GIT_*` en `src/test-setup.ts` (una vez para toda la suite, así el camino del hook queda idéntico al manual) + cinturón por llamada + repo GUARDIÁN de trinquete. Cuatro trinquetes verificados con `mutate`; probado con la suite ENTERA bajo un `GIT_DIR` de mentira (1.389/14.741 verde, víctima idéntica antes y después) y, gracias a la medición de una sesión paralela, también con el hook ABORTADO a mitad. Coordinado con dos sesiones paralelas: las dos retiraron claims propios al medirlos, y una identificó su push como el disparador.
- **#2104 · el aviso de «Ejecutar ahora».** Un único `confirm()` para los 59 crons, escrito con el peor caso de OTROS: «corre sobre TODAS las organizaciones» era falso en **13 de 59** y «no se deshace» se contradecía en tres. Ahora se compone por cron y la frase fija dice solo lo verdadero para los 59. Se retiró del test qa-036 la exigencia del literal falso —no es debilitarlo: exige más que antes— con la cifra en el docblock. Tres trinquetes recorren el registro completo. Encontrado y arreglado por el camino un recorte que partía identificadores (`marketing_publicaciones.`), y descartado un falso positivo (`calcular_score_match.` es un final legítimo).


## 2026-08-23 — el espejo de facturación se lee por la cuenta, y lo que quedó cerrado del 22-ago

- **#2119 · el espejo de facturación (mig 751).** `billing_accounts.billing_status` manda; `organizations.billing_status` es espejo. Había **11 lecturas crudas**, y la peor (`base-checkout.ts`) decidía con el espejo si llamar a `change_billing_status`: dejaba en **solo lectura a quien acababa de pagar** mientras Stripe le cobraba. Cerrado con lector único (`pickEffectiveBillingStatus`; `pickEffectiveSuspendReason` NO puede usar `??`, porque el `null` de la cuenta significa «sin motivo» y heredaría un `impago` viejo), trinquete **por ocurrencia** —no por fichero: `suspend-overdue` ya usaba el helper fuera y leía crudo dentro del bucle ([[un-trinquete-por-fichero-absuelve-al-que-ya-importa-el-helper]])—, canario `billing_espejo_divergente` en severidad `alta` (funcional: el barrido solo materializa y avisa por email las `alta`) y RPC idempotente `billing_espejo_realinear`, necesaria porque realinear no es una transición (`suspended → suspended` cae con `Invalid transition` en la matriz de la mig 693). Verificado en prod conduciendo el navegador: `tocadas: 1`, fila en `audit_log` y el barrido cerró la alerta solo. La divergencia real llevaba 8 días y era la Sandbox `is_test` — ningún cliente afectado.
- **#2119 · el cuerpo de los errores.** Tres convenios conviven (`errorJson` con `error` frase + `code`; `apiErrorJson` de v1/MCP donde `error` ES el código público; y los cuerpos históricos de write-gate con `reason`/`message`), así que **se discrimina por `code`, nunca por la frase**, y `detail` es lo que se PINTA, no un cajón de diagnóstico. La cifra «99 ficheros / solo 5» que se citaba en cinco sitios no la reproducía ningún grep: sustituida por **544 / 29** con los dos comandos escritos en `gotchas.md` — la proporción es el dato, no el número. Deuda excluida a propósito (`handleApiError` y el `detail` de Obras) → **#2131**.
- **#2119 · fixtures que pasaban por el motivo equivocado.** Mover el criterio de estado del `.eq()` a TS tiró 7 casos de `trial-ending-notice`: ninguna de sus 8 fixtures llevaba `billing_status`, porque el mock de Supabase encadena y no aplica filtros. Solo lo vio el gate COMPLETO → [[un-mock-que-ignora-los-filtros-hace-pasar-fixtures-sin-la-columna]].
- **22-ago · ningún hook corría la suite.** «Hooks en verde» no era «los tests pasan»: #2077 dejó `main` en `1 failed | 14613 passed` sin CI y con el squash fuera de todo gate. Síntoma #2094, causa #2096 (ya corre en `pre-push`). Misma pasada: #2078 cierra #2049, #2097 (casts caducados), #2098 (gobernanza) y el hook que capturaba `rc=0` por el `!`, con lo que su aviso de watchdog no salía nunca. Queda #1938 (el hook está, en CI no).
- **Conciliación: 0 dinero huérfano (22-ago, #1932/#1979)** — las 13 filas vivas son residuos de smokes en Sandbox y la causa murió con la mig 724. **#1919 cerrado vía #2099 y su causa declarada era falsa**: `supabase start` aplica las 746 y muere en el contenedor `vector` con colima; `-x vector` → ec=0. → [[supabase-start-colima-macos-vector-container-falla]]

### 2026-08-23 · la cola fiscal del 23-ago, cerrada, y el arnés que no vigilaba

- **#2120** — 7 de los 8 códigos `C-347-*` pintaban el código crudo (el comentario del fichero decía «ocho» y se equivocaba). Test de cobertura que extrae los `tipo` del calculador con **suelo real de 8**, no `>0`: con `>0` pasaba cazando 3 de 8. Cinco etiquetas se reescribieron porque **afirmaban hechos que la app no puede respaldar** — «Ya declarado en las retenciones» era falso para las emitidas, que las declara el cliente en su 190/180.
- **Emitidas en borrador**: medidas a **0 € en 9 orgs reales** (las 9 que hay están en la org de test). La partición del loader ya las separa; solo falta el cuadre. No se construyó nada.
- **Casilla 71**: propuesta publicada en el comentario de #2120. Afecta a **tres** superficies, no dos: API v1, conector MCP y copiloto in-app (`consultarIvaTrimestral.ts:186`).
- **#2127** — el ground truth del centro fiscal citaba mal la norma en **once** sitios, entre ellos el art. 84.Uno.2º completo (le faltaba justo la letra a), la de los no establecidos, que gobierna el caso vivo en prod) y las casillas 42/43/44 desplazadas una posición. Más dos secciones que no existían: IVA de proveedor extranjero y tipo de IVA no reconocido.
- **Arnés (#3, #4, #5 de `claude-harness`)** — tres PRs con refutación adversaria, que tumbó dos veces el primero. `mutate-guard` pasa de cazar 19 formas de `git commit` a 32 y deja de cortar los merges legítimos descontando en vez de eximir; `git-guard` deja de callarse sobre lo irreversible en cinco formas. El hook quedó **más barato** que antes (8 vs 9 ms). Un intento intermedio metió 1,3 s por llamada Bash y se cazó midiendo.

## Podado del hub — 23-ago-2026

- **Tres frentes de seguridad cerrados y podados del hub el 23-ago** (texto íntegro abajo): auditoría 04-jun (6 agentes + red team: RPCs `SECURITY DEFINER` expuestas, SSRF/CSRF/headers #131, outbox anti-spoofing #133/mig 217, fuga RLS `billing_accounts` mig 218) · auditoría 19-jun (red team 4 agentes: bypass de pago en `PATCH /api/settings/features`, deps HIGH, `/api/seed`; main `31f134f1` + mig 336) · crons → HMAC v2 05-jun, completa el 09-jun (24 schedules Dokploy a `sign-call.sh` v2, `SIGNING_LEGACY_UNTIL` cerrado).

### Auditoría de seguridad 2026-06-04 (6 agentes + red team activo) — ✅ CERRADA en prod
C1 crítico (RPCs SECURITY DEFINER expuestas), SSRF/CSRF/headers (PR #131), outbox anti-spoofing (PR #133/mig217), fuga RLS `billing_accounts` (mig 218) — todo resuelto y validado contra prod. [[supabase-rpc-security-definer-execute-public]] · [[facturaia-historico-detallado]]

### Auditoría de seguridad 2026-06-19 (red team 4 agentes) — ✅ CERRADA en prod (main `31f134f1` + mig 336)
HIGH bypass de pago en `PATCH /api/settings/features` + deps HIGH (nodemailer/undici) + MED `/api/seed`+search_path — todo corregido y verificado; residuales (HIBP sin Supabase Pro, extension_in_public) documentados como wontfix/no explotables. [[endpoint-toggle-feature-debe-gatear-enable-por-plan-o-compra]] · [[import-runtime-dep-no-declarada-solo-transitiva]] · [[supabase-advisor-trigger-functions-definer-son-ruido]] · [[facturaia-historico-detallado]]

### Migración crons → HMAC v2 (2026-06-05) — ✅ COMPLETA (2026-06-09)
24 schedules Dokploy migrados a `sign-call.sh` v2, Drive Sync y WhatsApp Receptor v2 incluidos, `SIGNING_LEGACY_UNTIL` cerrado. Huecos destapados en auditoría 2026-07-03 (agentic-gate-sweep/slack-dispatcher/verifactu-process sin schedule real) ya arreglados. [[dokploy-cron-docker-exec-no-hereda-env-de-app-env]] · [[cron-health-desconocido-para-cron-sin-ningun-run]] · [[facturaia-historico-detallado]]

### Auditoría de cifrado — texto íntegro, podado del hub el 23-ago

### Auditoría de cifrado — DESPLEGADA en prod 2026-07-19 (#998 + #1011)
Contrastada con NIST SP 800-38D/57, OWASP (Crypto/Secrets/Key/Password), RGPD art.32+AEPD, PSD2 EBA RTS, RD 1007/2023. Base ya sólida (AES-256-GCM+kid en integraciones/PSD2, hashing correcto, RLS 100%); el problema era **consistencia** (IBAN en claro incoherente vs `bank_consents` cifrado) + claves en env. El PR se **dividió** por composición (aditivo vs cutover destructivo).
- **#998 (aditivo, zero-downtime) — DESPLEGADO:** A1 `src/lib/crypto/pii.ts` (AES-256-GCM kid + blind index HMAC scoped por org), A4 cifrado `.p12` VeriFactu + IV 12B, A8 cache-control PDFs, A9/A10, B5-f1; A5 mig **519** (columnas `*_enc`/`*_bidx`/`cuenta_mask`+`cuentas_bidx`), A6 dual-write IBAN/cuenta (degrada a plaintext-only si falta clave). Smoke A6 en prod verde (alta cliente API v1 → `iban_enc` descifra con la clave de 1Password).
- **#1011 (hash tokens fiscal/phone) — DESPLEGADO como EXPAND zero-downtime:** A2 mig **521** (fiscal_share_tokens → id PK + token_hash único + token_suffix; CONSERVA `token` nullable + trigger que lo rellena; enlaces show-once, revoke por id) · A3 mig **520** (phone_change_revoke_tokens→token_hash vía trigger, RPC `change_phone_revoke` por hash; ya zero-dt porque la app solo toca token vía RPC). **DROP `token` fiscal diferido a B2.** Triggers verificados en prod. Ver [[cutover-token-hash-zero-downtime-expand-contract]].
- **Claves:** `PII_BANK_ENCRYPTION_KEY`+`PII_BANK_INDEX_KEY` (64-hex distintas) en Dokploy + 1Password (vault FacturAIA, item `kknqs4zua…`). Perder la ENCRYPTION_KEY = IBAN irrecuperables.
- **Decisiones:** B4 **ADR-010 Aceptado** (env+hardening+kid, no Vault). B6 **mantener TTL 7d**.
- **Registros migs 519/520/521 RECONCILIADOS** en `schema_migrations` (insert version NNN, workaround CLI-bloqueado). **Verificado**: smoke A6 + E2E A2 fiscal + triggers A2/A3 en prod + auditoría adversarial sin hallazgos.
- **3 bugs destapados por el E2E A2, todos arreglados+desplegados:** **#1020** (enlace fiscal usaba `new URL(req.url).origin` → `0.0.0.0` interno tras el proxy → `resolvePublicBaseUrl`; verificado host `app.tufacturaia.com`). **#1022** (500 en token inválido/revocado: `ErrorScreen` server llamaba `buttonClassName` client). **#1025 (sistémico)**: 7 páginas gated (cashflow, fiscal ×3, inventario, recurrentes, remesas) daban **500 en su rama upsell** por el mismo patrón → orgs SIN el módulo (conversión) veían crash; latente porque las orgs de test tienen todo activo. Fix de raíz: `buttonClassName`→`button-class.ts` sin `'use client'` + re-export (0 consumidores client tocados). Verificado 500→200 en dev. Ver [[server-component-no-puede-llamar-funcion-use-client]].
- **Pendiente:** A3 E2E de sesión (cambio tel→email revoke; no automatizable, mecanismo ya verificado en BD/RPC) · Gated orden estricto: B1 backfill prod → A7 matching por bidx → B2 cutover (**+ DROP `token` fiscal**).
- Learnings: [[cutover-token-hash-zero-downtime-expand-contract]] · [[server-component-no-puede-llamar-funcion-use-client]] · [[cifrado-columna-dual-write-degrada]] · [[blind-index-scoped-por-tenant]] · [[supabase-pooler-caido-aplicar-ddl-via-mcp]] · [[aplicar-migracion-por-psql-y-registrar-version-cuando-el-cli-supabase-esta-bloqueado]].


## 2026-08-23 — el cuerpo de un error: cerrado el `detail` (#2131) y su hermano `message`/`error` (#2138)

Dos PRs encadenados, los dos en prod: **#2140** (`5659d03bd`) y **#2146** (`600c9f6fb`).

- **#2131 (`detail`)** — el `detail` que se pinta llevaba el texto de Postgres, de Stripe y el
  `flatten()` de Zod. El arreglo salió de UN emisor (`handleApiError` → `{ error: 'Error interno',
  detail: FRASE_ERROR_INTERNO, causa: message }`) y las 132 rutas que lo llaman heredaron la
  decisión. Candado nuevo, `src/lib/errors/__tests__/detail-no-lleva-lo-interno.test.ts`, **por
  ocurrencia y sin lista de excepciones**: de 239 sitios en 152 ficheros a cero. Sus cuatro
  corolarios salieron de EJECUTAR el candado, no de leerlo: el alias de variable (21 sitios, entre
  ellos `cron/track.ts`), `fraseDeDominio` dentro de un `instanceof Error` (el candado bendecía lo
  que dice bloquear), nadie pinta `causa`, y **una ruta sin credencial no puede poner `causa`** —
  conjunto derivado de `isServiceRoute` + `src/lib/api/perimetro.ts`, nunca escrito a mano.
- **#2138 (`message` y `error`)** — el campo de al lado. Aquí **no** se mide por ocurrencia: la
  mayoría de los `message:` son legítimos, así que la sexta aserción mide solo el subconjunto que
  sale de una EXCEPCIÓN y solo en los cuerpos que se EMITEN (sin esa acotación daba 150 sitios, la
  mayoría columnas de BD llamadas `error` y discriminantes internos). Cuatro escapes, los cuatro
  derivados: narrowing de dominio (en la rama o en la expresión), humanizador, puerta de admin, y un
  `error` crudo con un `detail` que sí trae frase — el caso del fiscal, donde `error` ES el
  discriminante. Arreglados 16 sitios de crudo de Postgres, dos `new ApiError` de `/api/v1/*`, seis
  rutas que mandaban la prosa inglesa de Zod al campo pintado (a `campos` con `flatten()`), y el
  detalle del recordatorio masivo del copiloto, que volvía al LLM con el texto de Postgres dentro.
- **El hallazgo que más valía era una frase de prosa.** El gotchas decía «Nunca solo en `message`,
  que ningún componente lee» y era falso: 33 lecturas en 17 ficheros de pantalla, y
  `src/components/obras/http-client.ts:52` hace `json.message || json.error` —o sea que `message`
  **gana** a `error`— con 16 ficheros colgando. Corregida con el comando que la reproduce al lado.
- **Dos guards que no vigilaban.** `humanizeToolError` filtraba con `^[a-zA-Z]+_failed:` y dejaba
  pasar 3 de los 16 prefijos reales por llevar `_` en el nombre. Y el atajo de rendimiento del propio
  candado solo miraba la forma de literal de objeto, así que un fichero cuyo único emisor era
  posicional (`errorJson(frase, status)`) salía sin medirse: lo destapó `mutate` con **SIN VÍCTIMA**
  estando el candado en verde. Cuatro mutaciones para probar los dientes.
- Learnings: [[el-atajo-del-escaner-excluye-la-forma-que-nadie-penso-medir]] ·
  [[un-patron-sobre-nombres-generados-se-enumera-no-se-imagina]] ·
  [[el-detail-tecnico-se-pinta-antes-que-la-frase-humana-y-la-tapa]]

## 2026-08-25 — OCR: arnés de evals + fusión `documento_sin_lectura` + webhook sin pérdidas (#2180 → #2181 → #2183)

Tres PRs en prod el mismo día, con re-smoke real al final:

- **#2180** — arnés `eval:ocr` (fixtures ficticios, uno por patrón con ticket, `npm run eval:ocr:fixtures`)
  y JSON mode con guard `esLecturaSinDatos`: un JSON vacío del modelo entraba como `listo`; ahora va a
  bandeja `revisar` con `documento_sin_lectura`.
- **#2181** — la fusión del trío `missing_nif_emisor/missing_nombre_emisor/missing_importe_total` bajo
  `documento_sin_lectura` en el camino de ESCRITURA (`processOcrAudit`) + caso `moneda-extranjera-confianza`
  del eval cerrado.
- **#2183** — la fusión como PRESENTACIÓN: `ocr_extraction_audit.anomalies` guarda el array forense ÍNTEGRO
  y `componerMotivosRevision` fusiona al LEER, sanando las filas históricas de 4 motivos sin migración
  (fuente única `src/lib/ocr/sin-lectura.ts` + candado espejo `sin-lectura-espejo.test.ts`). Del gate del
  cierre salieron además dos fixes de datos del webhook de WhatsApp: el intent pendiente (PK=teléfono) ya
  FUSIONA items en vez de pisarlos —la 1ª foto quedaba huérfana en `_pending/`, 18 huérfanos medidos en
  prod— y el lote siempre habla al cerrar (duplicado idempotente, fallo, corte por quota a mitad con
  `break` etiquetado). Suite webhook 57/57, gate 15.263 tests, 8/8 mutaciones con víctima.

Re-smoke prod (25-ago, tarde): intent fusionado (`items:2`), escritura fusionada (las filas nuevas traen
`review_reasons=["documento_sin_lectura"]` a secas), reenvío idempotente sin fila nueva, y la fila
histórica `fb095efa` de 4 motivos servida con UN motivo por el endpoint real de revisión. Sandbox limpio
(4 recibidas borradas por API, `_pending/` a 0, org activa devuelta). Smoke del hub «foto que NO es
factura» ejecutado y retirado. Gap conocido que se queda: `multi-albaran-multipagina` (3/6 en el día,
`knownBaselineGap`, nombrado en el PR). Cierre `con-reservas` con 0 bloqueantes y los 6 avisos
implementados antes del merge. Learnings: [[intent-pendiente-upsert-por-usuario-pisa-la-pregunta-y-pierde-su-trabajo]]
· [[cookie-de-supabase-ssr-a-mano-para-smokes-sin-node]] ·
[[hook-formatter-prefer-const-entre-dos-ediciones-rompe-el-contador]] ·
[[json-mode-convierte-el-no-legible-en-json-vacio-y-el-guard-pasa-al-contenido]]

### 26-ago-2026 · La maduración de proveedores, y por qué el auto-OCR está inanido por diseño

**#2221 (mig 755, en prod y verificada por catálogo).** `factura_confianza_proveedor()` ponía
`facturas_ok = 0` en los tres brazos de «esta factura dejó de estar limpia», y
`esProveedorDeConfianza` exige `facturas_ok >= 3` **y** ninguna corrección en 30 días. Las dos
guardas juntas hacían el estado inalcanzable: un proveedor con 12 facturas limpias volvía a cero
*y* entraba en cuarentena. Ahora decrementa (`GREATEST(facturas_ok - 1, 0)`). `proveedor_reset_confianza`
(cambio de NIF/IBAN) **sigue** poniendo a 0 a propósito: otra identidad fiscal es otra contraparte.
Validador de 6 casos con dientes probados contra la función vieja — (a), (c) y (d) fallan con la 368.

**El paso 2 del auto-OCR, cerrado.** De 321 decisiones no-verdes de 60 días, **289 llevan el veto
`requiere_confirmacion_stock`**, que parecía la palanca obvia. Medido: de 106 bandejas en
`sin_aprobar`, 89 traen líneas y **0 traen `catalogo_id`** — ese mapeo lo pone el humano en la
bandeja, y lo pone en **51 de 52** en la única org con inventario. Sin él la mig 225 inserta texto
libre y no proyecta stock, así que auto-aprobar no movería mal el inventario: **no lo movería**, la
compra no entraría nunca y la factura saldría de la bandeja, matando el mapeo. El veto se queda, y
el comentario que lo justificaba afirmaba lo contrario de lo que mide el sistema (corregido). De
las 32 fuera del veto, 30 son documentos ilegibles y 2 casi-verdes con segundo motivo: encender
`ocr` hoy auto-aprobaría ~0. Única palanca viva: calidad de extracción.

**`categorias`**: 112 verdes / 17 ámbar / 2 rojas, gate **abierto** desde el 24-jul y modo `shadow`.
Sin una decisión desde el 23-jul porque no entran movimientos — PSD2 diferido por coste (26-ago),
los 138 de prod son CSV (129) y PDF (9). El paso a `activo` es opt-in del propietario por diseño
(`gate.ts`: abrir el gate **no** cambia el modo); solo lo escribe `POST /api/agentic-automation`.

De paso: `gen:types:check` abortaba el push de toda rama por un bump de PostgREST de plataforma
(`14.5` → `14.17`), y el encabezado del cron de sync bancario decía «4h» cuando siempre fue diario.

## 2026-08-28 — auditoría de diseño del shell y los listados (#2272, apilada sobre #2271)

Encargo: lo que la métrica de contraste APCA **no** ve — jerarquía, densidad, ritmo tipográfico y de espaciado, consistencia de componentes y el alcance real de la piel `freebie` que corre en prod. Modo Operate. Todo medido con arneses de Playwright contra el servidor de staging (puerto 3002, sesión reusada desde `tests/e2e/.auth/user.json`: los logins repetidos se rate-limitan), sobre 10 combinaciones de tema × piel × viewport.

**Auditoría: 13 de 20.** Reparado en el PR, con antes/después medido:

- **En móvil no había NINGÚN `<h1>`.** `dashboard-shell.tsx` bifurca el chrome por dispositivo: `Topbar` en escritorio, `MobileHeader` en móvil — y `MobileHeader` pintaba el título como `<span>`. El guard `un-solo-h1` de agosto había bajado las 14 vistas a `<h2>` «porque el Topbar ya pone el h1», premisa cierta solo en escritorio. Resultado: cero encabezados de nivel 1 en el dispositivo donde más se usa el producto. Ahora 0→1 en las cinco rutas, y el guard vigila también el **suelo** (`verificarSuelo`), no solo el techo.
- **El guard nació ciego y lo destapó `mutate`.** Con el `<h1>` sustituido por un `<span>` seguía dando OK: el comentario que hay justo encima —el que explica por qué tiene que ser un `h1`— contiene la cadena `<h1>` y el detector la contaba. Bastaba con **documentar** la regla para dejar de cumplirla. Arreglado con `cegarComentarios()`; las dos ramas fallan ya como deben.
- **Tipografía a escala rem fija**: 7 `clamp()` fuera. Un `clamp()` en UI de producto hace que el mismo dato ocupe distinto en dos pantallas del mismo usuario; la escala fluida es de páginas de marketing.
- **Peldaño de tinta mal elegido en 19 sitios → 0** (`-fg` donde tocaba `-fg-strong` por debajo de 18px).
- **Jerarquía de Ajustes**: h4×14 / h3×0 → h3×14 / h4×0.
- **Arial fuera de `/conciliacion`** (reset de fuente que faltaba).
- **Alcance de la piel**: 16 %→40 % en el dashboard y 2 %→16 % en conciliación, dando peldaño propio a lo que se escribía a mano (`--radius-md: 8px`, `--radius-card: 12px`, más `--space-1_5/2_5/3_5`). El modal deriva ahora su marco de la placa (`calc(var(--radius-card) + 6px)`) en vez de un 18 suelto, para conservar el escalón del «doble cristal» en las dos pieles.
- Cero desbordamiento horizontal en las 10 combinaciones.

**No reparado, con motivo escrito:** el cristal en móvil (97 capas de `backdrop-filter` frente a 58 en escritorio — apagarlo cambia el aspecto de la piel de la casa, y eso se decide con los números delante, no en un PR de auditoría) y las alturas de 44px que quedan (son mínimos táctiles, no la palanca de densidad; convertirlas a `--control-h-lg` sería trazabilidad falsa).

**Hallazgo aparte, sin issue:** `src/lib/ui/brand-tokens.ts` deriva la marca personalizada apuntando al **suelo** de contraste mientras los valores de fábrica van muy por encima, así que una org con marca propia recibe 10-13 Lc menos que la de casa sin que nada avise.

`npm run gate` entero verde: 1.501 ficheros, 15.784 tests, 8 skipped. Dos mutaciones con víctima (el `h1` y el acento de «Módulos»). PR **no** apunta a `main` a propósito: cuelga de `fix/freebie-peldano-tintado` (#2271) para no disparar deploy sin tu palabra.

→ [[una-piel-de-tokens-solo-alcanza-lo-que-no-esta-escrito-a-mano]] · [[un-fix-en-una-media-query-sobre-un-selector-que-no-existe-ahi-es-codigo-muerto]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]

## 31-ago-2026 · detalle retirado del hub en el cierre

- 🟢 **Los trece defectos del barrido funcional V2, en prod (31-ago, #2320 + #2321, migs 776-777)** — cada uno en su raíz, con candado probado por mutación. Los dos que tocaban a **clientes reales**: conciliar a mano ofrecía el BRUTO y el servidor lo rechazaba con 409 (4 facturas, 2 clientes), y una conexión bancaria a medias decía «Conectando…» **para siempre** (2 clientes, una desde el 12-jul). Invariante sobre las **2.335 facturas de prod**: cero ofrecen por encima del techo del guard. **Quedan 27 mediciones** (olas B/C: `integraciones` 17, `pagos-online` 10, +5 mal archivadas), archivadas como «bloqueadas por salud de máquina» con el swap al 87 %. **Ese motivo hay que reverificarlo antes de darlas por bloqueadas**: medido el 31-ago, el porcentaje de swap NO discrimina thrashing —al 89 % con **0 swapouts/s** el swap está asentado y se puede conducir un navegador; lo que sí lo delata son los pageins con swapouts subiendo, y la causa fue un `next build` de una sesión paralela. Para una ola de 3-4 el criterio del 50 % sigue mandando. → [[el-porcentaje-de-swap-no-discrimina-thrashing-los-swapouts-si]] → [[un-estado-sin-caducidad-es-una-promesa-permanente-en-pantalla]] · [[extraer-a-parts-para-esquivar-un-trinquete-de-tamano-crea-un-ciclo]]

- 🟢 **Numeración de ADR cerrada (31-ago, #2318 + #2319 en prod)** — el `ADR-032` duplicado se había arreglado al 034, que estaba libre aquí y ocupado en el vault. Hoy es el **062**, 86 citas reapuntadas, y un cuarto candado que sí lee el vault. **Contador único: el próximo ADR es el 063**, política en `docs/decisions/NUMERACION.md`. → [[dos-series-de-adr-con-el-mismo-prefijo-la-cita-resuelve-al-documento-equivocado]]

- 🟢 **Cerrado el 29-30 ago; en el hub queda solo su cola** — super test V2 93/94 (#2281→#2286): la ola 2 de M1 con navegador · iconografía (#2289→#2294): las 7 rutas de `/admin` sin ejercer y decidir ahí el trazo grueso · diseño (#2271, #2285): ~50 `border-radius: 8px` a mano fuera de `ui/` · ticket 156 (#2274→#2280, migs 764-767, ADR-032): la respuesta del cliente. → [[facturaia-historico-snapshot-2026-08-30]]

## Podado del hub el 2026-08-31 (cierre del repaso de stock)

- 🟢 **Numeración de ADR cerrada (31-ago, #2318 + #2319 en prod)** — **contador único: el próximo ADR es el 063**, política en `docs/decisions/NUMERACION.md`, con candado que lee el vault. → [[facturaia-historico-detallado]]
- 🟢 **Cola de lo cerrado el 29-30 ago** — super test V2 (#2281→#2286): ola 2 de M1 con navegador · iconografía (#2289→#2294): las 7 rutas de `/admin` sin ejercer · diseño (#2271, #2285): ~50 `border-radius: 8px` a mano fuera de `ui/` · ticket 156: la respuesta del cliente. → [[facturaia-historico-snapshot-2026-08-30]]
- 🟠 **#1778: PR 1-3 EN PROD, flag `FACTURAS_SUSCRIPCION_PROPIAS` APAGADA (20-ago)** — migs 708/709 verificadas; corregido un error fiscal del PR 2 (reverse charge UE B2B se emitía como `E5` siendo **no sujeta**, N2 → #1998). **Queda**: PR 4 (encender + smoke), PR 5 (devoluciones/disputas) y modelar N2 (#1994). Sin urgencia: 1 cliente live y es ES. → [[codigo-de-exencion-no-expresa-una-operacion-no-sujeta]]

### Versión larga de cinco entradas condensadas el 2026-08-31

- 🟢 **Los trece defectos del barrido funcional V2, en prod (31-ago, #2320 + #2321, migs 776-777)** — cada uno en su raíz, con candado probado por mutación; cero de las 2.335 facturas de prod ofrece por encima del techo del guard. **Queda**: 27 mediciones (olas B/C) archivadas como «bloqueadas por swap al 87 %» — **reverificar ese motivo antes de darlas por bloqueadas**: el porcentaje no discrimina thrashing, los `Swapouts` sí, y la causa fue un `next build` de una sesión paralela. → [[el-porcentaje-de-swap-no-discrimina-thrashing-los-swapouts-si]] · [[facturaia-historico-detallado]]
- 🟠 **Auditoría del 27-ago dentro, con seis cifras reverificadas y corregidas al pie (31-ago, #2318)** — su «0 `DROP FUNCTION`+`CREATE` sin `REVOKE`» era cierto hoy y falso como historia: la mig 602 dejó `aplicar_movimientos_lotes` abierta a `anon` **152 migraciones**, hasta la 754. **Queda**: los 29 issues #2238-#2266. → [[un-recuento-sobre-el-estado-final-no-ve-la-ventana-de-exposicion]]
- 🟢 **Truncado silencioso del listado y del calendario, en prod (31-ago, #2332 + #2334)** — smoke post-deploy verde, 74 en pantalla contra 74 en BD. **Queda**: `ratchet:maxrows` es textual y **ciego a una consulta sin `.limit()` ninguno**, que es el caso peor. → [[una-huella-de-chunks-de-otra-ruta-no-detecta-un-deploy]]
- 🔴 **Lo que no está en `docker-compose.yml` no llega al contenedor (20-ago, #1993)** — costó 8 días de WhatsApp tirando mensajes al suelo y el cifrado de IBAN nunca activo. **#1984 CERRADO (24-ago)**: `env-guard` en el pre-commit + colector `env-critica-vacia` (declarada no es llena), con la lista de críticas derivada del dato para que no fabrique avisos permanentes. **Queda**: un WhatsApp real con factura y una escritura que confirme el cifrado **antes** de tocar B2. → [[compose-que-enumera-variables-no-entrega-lo-que-guardas-en-el-panel]]
- 🟠 **Arnés y WORM: 3 de 5 tracks cerrados (20-ago)** — canario WORM, runbook de B2 y `git-guard`, los tres en prod. **Queda**: key de B2 sin `deleteFiles` (solo por API), sellar al exportar (**tuyo**, producto) y puerto por checkout en E2E. → `PROMPT-continuacion-20-ago-arnes-y-worm.md` · [[hook-que-resuelve-git-en-el-cwd-de-la-sesion-juzga-el-repo-equivocado]]
- **Planes**: Starter 14 / **Plus 29** / Pro 49 / Enterprise 99 €/mes (+IVA 21%, anual −20%) + add-on Centro Fiscal IA 14,90. **Stripe LIVE** desde 2026-06-01. Reempaquetado escalonado + tier Plus + grandfathering aplicados **en BD** (mig 399, #509/#513). **Plus ya es comprable** (verificado 29-jul contra la API de Stripe live): `price_1TmXAy…sL6pkhp1` 29 €/mes y `price_1TmXAy…ETcDK1NJ` 278,40 €/año, activos y en `plan_prices`, que es la fuente de verdad (`stripe-plans.ts`; el ENV es solo fallback). El pendiente de crearlos estaba obsoleto.
- **Tests**: Vitest **16.144/0** (8 skipped, 1.552 ficheros, `main` 31-ago tras #2334, gate entero `ec=0`; migs 776-777 aplicadas y verificadas contra prod por catálogo **y ejecutándolas**, que no es lo mismo). `maxWorkers: 5` fijado con guard desde el 24-ago (#2149). Se mide **ENTERA y sobre la composición**, nunca filtrada por carpetas: es el único marcador que ve los guards de arquitectura, y `gh pr merge --admin` no pasa por ninguno · E2E smoke **513/0/142** en 21,6 min contra staging (12-ago). Los tres modos de medir en falso, con su caso → [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[otra-sesion-con-pkill-mata-tu-servidor-y-parece-un-bug-del-producto]] · [[tanda-e2e-sin-comprobar-el-servidor-vivo-al-final-no-es-medicion]] · [[e2e-smoke-skip-honesto]]
  ⚠️ **Sin acceso desde Claude Code**: no hay API key de este Dokploy en 1Password (las que hay son de Ecobox, Elphis, Simarro, Gesfincas y n8n; `Tecnocloud DOKPLOYMANU` es usuario/contraseña del panel) y `~/.ssh/id_ed25519` **no existe** en la máquina pese a lo que decía la nota de SSH de abajo. La key pasada en chat el 28-jul da `Unauthorized` contra `dokploy.tufacturaia.com/api` y contra `dokploymanu.tecnocloud.es/api`, con la cabecera correcta (`x-api-key`) — **y está expuesta en el transcript: rotarla**. Si quieres que lo haga un agente, hace falta una API key válida de ese host guardada en 1Password. Ver [[migracion-auth-sin-downtime-con-signing-legacy-until]]
- ❓ **¿El coste/hora medio lleva los indirectos? La decide Natalia (07-ago)** — hoy 21 €/h de coste directo. Duda en voz alta si meter las nóminas no productivas (la suya, Goyo, Óscar). **Recomendado que NO**: metiendo estructura el coste deja de comparar obras entre sí, y el número se movería solo al cambiar la carga de trabajo sin que ninguna obra cambie; la estructura se cubre con un margen mínimo (hoy `margen_min_pct` 20, y con 21 de coste sobre 48,32 de venta el margen de MO es del 56 %). Cambiarlo luego es barato: `coste_mo_unit` se congela por línea, así que no reescribe presupuestos hechos.

- **[31-ago] Smoke en prod del aviso de albaranes reabiertos, verde.** Borrada una recibida cruzada de verdad en la org QA3 (entrando y saliendo por los endpoints del propio producto, no por impersonación): el toast dijo «Factura eliminada. Se ha deshecho su entrada de inventario (1 producto). Hay que volver a validar 1 albarán, que ha vuelto a estado abierto.», y la BD lo corroboró — `validado`→`abierto`, `validado_at` a NULL, `asentada` 1→0, factura borrada y casación 1→0. El fixture se consumió; se resiembra con `scripts/qa/seed-supertest-datos.sql`. Cerrado de paso el bloqueo de la org activa: se devolvió a AgentesiaLab con `POST /api/auth/switch-org`, la puerta del producto, sin el `UPDATE` que el clasificador había frenado.

- ✅ **Repaso completo del área de stock, en prod (31-ago, #2335 + #2336 + #2338, mig 781)** — el borrado de una recibida cruzada devolvía albaranes a `abierto` **en silencio**: la RPC ya lo hacía, pero la clave nueva del JSON no la leía nadie hasta el aviso del usuario. Cerrado de punta a punta (RPC → parser → endpoint → toast, incluida la rama de borrado masivo parcial, que se construía su propio texto y tiraba las consecuencias). Smoke en prod verde el mismo día: el toast nombra el albarán que vuelve a `abierto` y la BD lo confirma. → [[una-clave-nueva-en-el-json-de-una-rpc-no-llega-a-nadie-sola]] · [[una-piel-y-un-tema-empatan-en-especificidad-gana-el-ultimo-escrito]] · [[un-fixture-escrito-dentro-del-arbol-que-otro-test-recorre-es-una-carrera]] · [[facturaia-modulo-stock]]

- 🟢 **Los cuatro cabos del stock: decididos y tres construidos (31-ago)** — el mensaje del guard de borrado (mig 783) deja de inventar la causa y **dice las unidades en español** —`format('%s')` sobre NUMERIC(14,3) escribía «3.000» por «3»—; el `5` y el `×2` de reposición salen a `src/lib/stock/reposicion.ts`; y las **dos escrituras desatendidas** del PMP quedan cerradas (el importador en «sobreescribir» pisaba la valoración de productos existentes, el catálogo reenviaba el coste en cada PATCH). El candado en BD es la fase 2 → **[[ADR-065]]**, que deja escrito por qué NO se reemiten las cinco funciones del PMP (1.133 líneas contra ~100). Los tres candados nuevos, probados por mutación. **Queda**: Wildomar.

- 🟠 **Wildomar: la fusión de proveedores, medida y sin hacer (31-ago)** — no son dos filas sino tres (una en sandbox). Las dos reales difieren solo en el NIF y **las dos están vivas**: `B20987657` tiene 29 albaranes / 2 partidas / 2 facturas, `ESB20987657` tiene 5 / 14 / 6. El histórico está en la vieja y las partidas vivas en la nueva, así que el sentido de la fusión importa; el `ES` es el NIF-IVA, así que la canónica debería ser la del 2-ago. `merge_proveedor` (mig 767) repunta las 12 tablas con FK más otras 3, así que huérfanos no habrá. **Tuyo**: decidir superviviente. Ensayo en `is_test` antes de tocar prod.

- ✅ **El albarán empareja sus líneas con un producto, y validar sin decirlo se niega (1-sep, #2365 → PR #2367, mig 790, ADR-068 §2)** — sin `catalogo_id` ni `material_id` el asiento salta la línea (el `JOIN catalogo_servicios` es INNER) pero el paso (c) la marca `asentada` igual, y `validado` es terminal: el género no entraba nunca y no quedaba nada que corregir. En prod, **25 líneas en 7 albaranes de Pescados Chivite**, todos aún `abierto`. Construido: `PATCH /api/albaranes/[id]/lineas/[lineaId]`, selector en la ficha con el aviso y el modal de «Validar igualmente», y la mig 790 con `p_permitir_sin_producto DEFAULT false` (la firma de 2 argumentos se borra) que levanta OB065. El predicado es el **estrecho** — el ancho, que es el que usa el propio asiento, habría rechazado 9.567 albaranes ya validados de Obras. Verificado contra la función desplegada dentro de `BEGIN … ROLLBACK`, 6 mutaciones / 6 víctimas. → [[el-predicado-de-un-guard-se-mide-contra-el-historico-antes-de-escribirlo]] · [[un-gate-que-enumera-desde-el-indice-de-git-no-ve-el-fichero-nuevo]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]
