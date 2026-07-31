---
title: facturaia — histórico snapshot 2026-07-30
date: 2026-07-30
tags: [facturaia, historico]
---

# TuFacturaIA — retirado de "Smoke tests pendientes" el 2026-07-30

Smokes que Manu ya verificó en producción, movidos íntegros aquí en la poda de `/obsidian-1`.
El hub se quedó con una línea de cierre. Índice: [[facturaia]].

- ✅ **[29-jul, #1350·#1351·#1352·#1353] Runner: prompt sin imposibles, timeout que rescata, URL entera en el ticket** — los 4 PRs en `main` y **rebuild del runner ya hecho por Manu** (hacía falta: su Dockerfile hace `COPY run-ticket.mjs`, así que mergear no bastaba). Tras el despliegue del app: (1) lanzar un ticket desde `/admin/feedback` y confirmar en logs que la sesión ya NO intenta `npm run build` ni instalar Playwright (era lo que se comía los 30 min: captura de pantalla pedida en un contenedor sin navegador + build prohibido por el system prompt y exigido por el prompt); (2) enviar feedback desde una pantalla con query y comprobar en `feedback_tickets.pagina` que el valor identificativo NO está y el de estado de UI sí (verificado ya en local con el smoke E2E, falta en prod); (3) remedir la fase `analizando` en `feedback_ai_job_events` (línea base 29-jul: media 17 min, p90 26,3 sobre límite de 30) y **entonces** decidir si se sube `JOB_TIMEOUT_MS` — si se sube, `QUEUED_STALE_MIN` del watchdog sube en el mismo commit o mata encolados sanos. Autopsia: de 34 fallidos, 11 eran `cuenta desconocida: alt1`, 7 cuota, 6 `runner sin latido` y solo 6 timeouts. **El latido, arreglado de verdad en el #1358**: moverlo al inicio del job NO bastaba (un `setInterval` no se dispara con el loop bloqueado por `cpSync`; repro: 4019 ms síncronos → 0 latidos), así que la copia pasa a `await cp` y se intercala `heartbeat()` entre los pasos síncronos. Verificado: 0 latidos con `cpSync`, 6 de 6 con la asíncrona. **Pero el síntoma NO lo cerraba eso**: la noche del 29 al 30 tres jobs murieron como "sin latido" y la causa era el `autoDeploy` del compose del runner contra `main` — cada merge recreaba el contenedor y cortaba la sesión (los latidos se perdieron a las 21:25 y 21:44 UTC, los minutos exactos de dos merges). Mi hipótesis de OOM/réplicas era falsa. **CERRADO el 30-jul (#1360, `a02df766`)**: `watchPaths: ["ops/ticket-runner/**"]` aplicado en el compose de Dokploy (de ~10 deploys al día a solo los suyos) + apagado grácil en `shutdown.mjs` con tests, que mata el grupo de `claude`, cierra el job en el acto con el motivo real y deja de reclamar (`stop_grace_period: 30s`). El smoke con SIGTERM real destapó una carrera invisible en el código: al morir el hijo, `processJob` reportaba "claude salió con código null" y ganaba el compare-and-set → durante el apagado solo habla el handler. Ver [[autodeploy-sin-watchpaths-mata-el-trabajo-en-vuelo-del-worker]]. Lo de `alt1` queda cerrado sin código: `system_config.resolver_claude_cuenta` está en `default` y esa cuenta ya no se usa. **`/fia-cierre` corrido sobre los 4 PRs (post-merge)**: 2 bloqueantes reales míos, arreglados en PR de seguimiento (el tipo de ticket no se podía elegir con teclado tras migrar a `Segmented`; el saneador dejaba pasar CR/LF y no redactaba el NOMBRE del parámetro hacia el prompt del agente). El tercer "bloqueante" (smoke rojo) era falso: pasa, solo es frágil bajo carga. Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]] · [[latido-que-solo-cubre-el-tramo-interesante-deja-el-resto-a-merced-del-watchdog]] · [[mide-el-reparto-de-fallos-antes-de-arreglar-el-que-te-cuentan]] · [[roving-tabindex-sin-seleccion-deja-el-grupo-fuera-del-tabulador]] · [[sanear-el-valor-y-olvidar-la-clave-el-nombre-del-parametro-tambien-es-entrada]] → **SMOKE HECHO por Manu (29-jul), correcto.**
- ✅ **[29-jul, #1342] OCR: nº de factura ≠ código de cliente + ecotasa RAEE (ticket 89d8a652, IET)** — mergeado a `main` (`cfe9d13d`). Falta la pasada real: reingestar el PDF de Guarconsa (5 págs, factura `624214649`, cliente `00743`) en la org de IET y comprobar dos cosas en `/ingesta`. (1) `Nº factura` sale `624214649`, no `00743`; si el modelo vuelve a confundirse, el guard deja el campo VACÍO con el aviso "El nº de factura leído era el código de cliente", y eso también es un pase (nunca guarda el número falso). (2) El desglose del HeroCard muestra `Ecotasa RAEE 1,10 €` entre Base `4.683,36 €` e IVA `983,51 €`, y en "Ver más detalles" hay una línea `Impuesto RAEE (reciclaje)` de 1,10 €. Mi verificación fue con una fila sembrada en la sandbox, no con una pasada real del OCR. Tercera ronda del mismo documento: las dos anteriores (83c8028d) se cerraron tocando solo el prompt y volvieron a fallar. → **SMOKE HECHO por Manu (29-jul), correcto.**
- ✅ **[29-jul, #1325] Emitir una factura real y comprobar que el PDF lleva el bloque de condiciones** — es el único trozo del ticket #96 sin verificar en producción: el arreglo está cubierto por tests y por barrido de todos los caminos de PDF, pero no lo he visto en un documento emitido. No lo hice yo porque emitir consume numeración fiscal y una emitida no se borra, solo se anula. Con un cliente que tenga plazo pactado: emitir → abrir el PDF → debe decir forma de pago, "a N días", la fecha concreta y la cuenta. → **SMOKE HECHO por Manu (29-jul), correcto.**
- ✅ **[27-jul, PR #1239] Impersonación superadmin tras el rename a `proxy.ts` — SMOKE HECHO por Manu y correcto.** Con eso los 3 casos del spec quedan verificados (los otros dos a mano: `/dashboard`→`/login` y `/api/v1/*` sin Bearer → 401 sin redirect). #1239 desbloqueado, solo pendiente de merge.

## Retirado del NOW del hub el 2026-07-30 (cerrado, sin pendientes)

- ✅ **[30-jul, #1366] El panel de alertas dice de qué es cada aviso, y la incidencia técnica se cierra de verdad, EN PROD** — el badge pintaba el slug interno («System Alert:Ocr-Process», «Emails Failed»): ahora `alertTypeLabel()` es fuente única para badge, filtro y dashboard. Y lo gordo: una incidencia de `system_alerts` **con org** ofrecía la ✕ (escribe en `admin_alert_dismissals`, que su collector no lee) y escondía «Resolver» → toast de éxito y la alerta de vuelta al recargar. Ahora manda `alert_id`. Smoke con navegador contra el dev local: badges, filtro (1 de 4) y **Resolver probado end-to-end** sobre la incidencia real del runner, que ya no reaparece. Manual admin actualizado con los tres cierres (✕ / Resolver / se cierra sola). Sin pendientes. Ver [[dos-mecanismos-de-cierre-y-la-ui-ofrece-el-que-no-aplica]] · [[etiqueta-humana-de-un-slug-debe-seguir-siendo-unica-por-tipo]]
- ✅ **[27-jul] Deuda propia en la cuenta Stripe de AgentesIA, CERRADA** — al comprobar si una restricted key era read-only lancé un `POST /v1/prices` esperando 403: devolvió 200 y creó producto y price reales. Producto `prod_UxN0I8nR5ZFAoi` y price `price_1TxSGmQY4tV8FMxQJf4lEPKT` archivados, y Manu revocó esa key. **Decisión tomada**: la key nueva de Tufacturaia se queda con su lectura amplia (lee `customers` además de Prices/Products) — no volver a proponer afinarla. Ver [[verificacion-no-mutar-estado-prod-cuenta-real]]
- ✅ **[28-jul, #1306] Los 8 specs que escriben retiran lo suyo por el id que devuelve el servidor**, nunca por "lo de hoy" (la org tiene seeds permanentes fechados hoy). Guards: aborta si la org no es `is_test`, ningún DELETE con lista vacía, `bandeja_ingesta.factura_id` a null antes de borrar, y las emitidas no se borran releyendo el estado en BD. El explorer, sospechoso de los 21 presupuestos, quedó descartado: su marcador `monkey-` **nunca sirvió** (se recalculaba en CADA campo con los 5 últimos dígitos del epoch, así que dos filas de la misma tanda no lo compartían), y la UI crea contactos por PostgREST directo, no por `/api/*`, así que el observador no los habría visto. Los movimientos de stock se dejan a propósito: van por RPC, la respuesta no trae id y borrar la fila descuadraría el stock.
- ✅ **[29-jul, #1348] El aviso del teléfono de un contacto ya no habla de WhatsApp a quien no tiene Cobros** (ticket #103, IET) — el bloque se pintaba sin gatear por feature y "verificar" prometía un código que no se manda; ahora va tras `hasFeature('cobros')` y el botón dice "Confirmar número". Ver [[aviso-de-modulo-sin-gatear-por-feature-es-ruido-con-pinta-de-error]] · [[verificar-en-ui-promete-envio-de-codigo-si-es-autodeclaracion-di-confirmar]]
- ✅ **[29-jul, #1344 + #1346] Las pastillas de un ticket usan el `<Pill>` compartido** — tres implementaciones a mano unificadas en `ticket-pills.tsx`, −387 líneas de CSS, hex del admin a tokens.
- ✅ **[29-jul, #1342 + manuales #1343] El OCR no guarda el código de cliente como nº de factura, y el RAEE se cuenta** (ticket 89d8a652, IET) — la causa no era el prompt sino que el pipeline no verificaba el campo: ahora pide las dos columnas y las cruza. Smoke real de Manu correcto. Ver [[dos-campos-confundibles-pide-los-dos-y-cruzalos-en-codigo]]
- ✅ **[29-jul, #1331] Los smokes que escriben dejan la org como la encontraron** — `fiscal-perfil-preserve.spec.ts` restauraba con valores inventados y fuera de `finally`: degradaba el perfil fiscal en cada pasada y salía verde. Quedan listados sin tocar `explorer/crawl.spec.ts` y `cierre-cuenta.spec.ts`.

## Decisiones cerradas retiradas del hub

> ✅ **Las tres decisiones de auth del 27-jul, cerradas en #1298** (`5d16aa99`). (1) `invitado` no era decisión de producto sino **código muerto**: el lookup de rol solo corre con `!superadmin`, y por esa vía el `orgId` sale siempre de `resolveActiveOrg()`, que ya filtra `activo` — alineado y los `DIVERGE:` pasan a conformidad. (2) `/api/me/` exento de billing **y** de cierre: es perfil personal, no recurso de la org, y rectificar los propios datos es el art. 16 RGPD, misma familia que el 20/15 ya eximido. (3) `/api/seed` exige `organizations.is_test=true` en sus tres vías de resolución: ni borrado ni guardado por `NODE_ENV`, porque la Sandbox vive en la BD de producción y eso habría roto su sembrado, que es su uso real. Ver [[helper-de-auth-que-asume-validacion-del-caller]]

- 🟢 **Mergear el PR del runner CIERRA el ticket solo y manda el email al cliente** — `api/internal/github-webhook`: merge → PR → job → ticket `resuelto` + email, idempotente. No hay que tocar el estado a mano; sí es manual el botón «Publicar al cliente». Desde #1354 ignora el PR obsoleto de un ticket reabierto. Ver [[callback-de-un-intento-viejo-cierra-lo-que-ya-se-reabrio]]

## Retirado del NOW del hub el 2026-07-30 (segunda poda, cierre de sesión)

- ✅ **La fecha corregida al revisar ya no se pierde, EN PROD (29-jul, #1349)** — ticket #104 de Chivite: la fila mostraba `dd/mm/aaaa` y el guardado solo aceptaba ISO con un `return` mudo. Las dos filas de fecha de la bandeja usan ya el `DatePicker` compartido. Ticket cerrado desde `/admin/feedback` (no por BD) para que saliera el email — `delivered` en `email_log`. La 10422P **ya corregida a mano en prod (2023-06-26 → 2026-06-23)** tras verificar el PDF original, con `audit_log`; y de paso otra igual en AgentesiaLab. **La decisión de fondo sigue viva** (¿editar `fecha` de una recibida aprobada desde la UI?), ver `Decisiones pendientes`. Ver [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]]
- ✅ **Descartar un ticket exige motivo, EN PROD (29-jul, #1329)** — se publica en el hilo, 422 si falta, y el email de cierre lo recoge. **Decisión abierta**: `/soporte` no está en la barra lateral, ¿merece navegación propia?
- ✅ **[30-jul, #1382] Guardar borrador con cantidad > partida — VERIFICADO en prod** (build `11:33:52Z`, org `Obras tufacturaia sandbox`, Merluza fresca LOTE-B 3 uds): línea de 20 uds guardó borrador sin error y salió en Emitidas (302,50 €); reabierto y emitido, avisó de LOTE-B y quedó en `borrador` con `num=null` y 0 movimientos de stock. Borrador de prueba borrado.

- ✅ **[30-jul, #1381 + #1382] Ticket #117 (Chivite): emitir sin stock dice qué partida falta, y guardar un borrador ya no lo exige** — el `raise sobreventa_lote` (migs 308/312/388) no estaba mapeado y salía por un 500 mudo; ahora es un 409 que nombra partida o producto. La emisión que el cliente logró **no se saltó ningún control**: no llegó a entrar género, lo que cambió fue la partida al reabrir el borrador (autopick FEFO). Los dos smokes en prod verificados. Retirado del NOW del hub el 31-jul. Ver [[workaround-que-le-funciono-al-cliente-no-es-la-explicacion-de-la-causa]] · [[guard-de-la-accion-irreversible-bloqueando-el-guardado-empuja-a-la-irreversible]]

- ✅ **[30/31-jul] Cola del runner vaciada: 8 PRs y 4 migraciones** — #1383 (archivo de tickets en `/soporte`, mig 595), #1384 (búsqueda de materiales por palabras sueltas, mig 597: literal completo → todas las palabras → trigram, y solo el escalón más preciso que exista), #1385 (fuera el "override" de la UI de tarifas), #1388 (`merge_cliente` repunta obras, presupuestos de obra, delegaciones, mandatos SEPA, recurrentes, opt-outs y recordatorios antes del DELETE; mig 599), #1396 (logo de proveedor en agentes: la regla vivía solo en `admin.css`, que ese layout no carga), #1397 (`copiloto_kpis` pasa a `tipo_documento is distinct from 'abono'`, mig 598), #1399 (`.export-card > div` alcanzaba también al icono y le pisaba el `flex-shrink`), #1400 (el menú de fila se pintaba sobre el modal de confirmación y quedaba colgado al cancelar). Ticket **#115** cerrado y contestado; borrados dos borradores obsoletos de Claude. Colisión de numeración dos veces (#1384: 595→596→597 · #1388: 596→599), cazada por el hook `pre-push` las tres.

## 31-jul — los tres cabos de la tanda de Textos Tipo (#1412, #1413, issue #1409)

**#1412 — el euro por duplicado en Obras.** `fmt2` (`format.ts:5-7`) ya devuelve el símbolo y los dos generadores de PDF de Obras se lo concatenaban otra vez, así que un texto tipo con `@total@` imprimía `1.234,50 € €` en presupuestos y pedidos que se envían al cliente y al proveedor. Barrido de las tres funciones que ya traen símbolo: **2 usos defectuosos de 135** (`fmt` y `fmtCur`, 0), así que el arreglo es local y `fmt2` no se toca. No se unifican los caminos de facturas y Obras: el de facturas resuelve el importe *a pagar* (IRPF, retención, divisa) y el de Obras el bruto — fusionarlos es decisión de negocio.

**#1413 — las notas sin saltos de línea.** 4 de 5 plantillas pintaban el contenedor sin `whiteSpace: 'pre-wrap'` (`custom` era la correcta y sirvió de referencia). Lo tenía congelado un comentario del propio código: *«Aquí no se arregla el de notas: eso cambiaría documentos que ya se están emitiendo»*. Medido en prod: de 1.415 facturas con notas, **1.339 son `registro_externo`** (PDF de terceros que no pasa por estas plantillas) y de las **76 propias, ninguna tiene un salto de línea**; los 7 presupuestos de la tabla legacy, tampoco. Alcance real: 0 documentos. Se añadió también el `pre-wrap` a la ficha de la app (`factura-detail-modal.module.css`), que si no enseñaba párrafo corrido y enviaba párrafos, y media frase al `manual-usuario.md`.

**Issue #1409 — decisión de producto, sin tocar código.** `generar-view.tsx:224` deja la casilla «Enviar al cliente por email al emitir» en `useState(true)`. Dato que se llevó al issue: por canal en 90 días, `api` 1350 emisiones / 2 con email, **`web` 61 / 8 (13 %)**, `voice` 14 / 2. O sea, del que ve la casilla marcada el **87 % acaba no enviando**. Tres opciones planteadas con su coste (desmarcado por defecto · recordar la elección en `organizations`, donde ya viven `forma_pago_default` y compañía · reforzar el diálogo `Confirmar emisión`, que hoy **no menciona el envío ni la dirección** en el caso factura). Hallazgo colateral en el mismo issue: `selectCliente` (`:1016`) no limpia `emailEnvio` al cambiar a un cliente sin email, así que la factura de B puede irse al correo de A.

**Lo que encontró el `/fia-cierre`** (6 dimensiones, con-reservas, 0 bloqueantes) — dos defectos en el trabajo propio: (1) un caso del test nuevo era **vacuo**, porque su aguja `>1.234,50 €<` la produce la píldora TOTAL del propio PDF; se demostró neutralizando el doble del texto tipo (caían 1 y 2, ese no) y se reanclò con marcador propio; (2) dos comentarios quedaban **falsos al mergear** (`textos-congelados.test.ts:202`, `textos-tipo-block.test.tsx:124`) y una afirmación mía en la cabecera del test nuevo citaba un contaminante que ese fixture no pinta.

**Error de método propio**: la comparación de maquetación antes/después se hizo con `git stash push/pop` y el `pop` **sacó un stash ajeno**, dejando 3 ficheros de otra sesión en conflicto dentro del worktree. Limpiado sin pérdida (los 3 stashes intactos), pero la comparación era inválida: rehecha con un worktree de control, la conclusión se dio la vuelta.

**Cabos que quedan abiertos**: `obra-pedido-pdf.tsx:151` pinta las *observaciones* del pedido a proveedor sin `pre-wrap` y ahí hay **34 de 8.854 `obras_pedidos` con salto de línea en prod** — más impacto real que el bug arreglado, que tenía 0. Un pedido impreso «sin totales» imprime el importe igualmente si el texto usa `@total@` (`pdf-obra-pedido.ts:205-216` no mira `opts.conTotales`). `recordatorio-pago/route.ts:121` manda «1234.50 €» con `toFixed(2)`. `renderPdfFallback` (`send-factura.ts:185`) envía el PDF de rescate sin QR ni leyenda VeriFactu. `manual-usuario.md:3219` afirma que la factura de obra no usa Textos Tipo, desfasado desde las migs 593/596.

---

## Auditoría funcional — segunda tanda (31-jul): de 13 a 21 PRs

**Cerrados**: `qa-009`/`qa-010`/`qa-013` (#1398, la validación que quedó a medias), entregables ronda 2 (#1401), `qa-027` (#1402), `qa-028` + mig 600 (#1404), `gen:types` (#1406), `qa-029` (#1407), `qa-024` (#1408), `qa-020` (#1410), `qa-022` (#1411).

**`qa-027` se validó solo.** El ensanche del `Database` global existía por UN caso local: el insert de snapshot fiscal. Medido antes de rediseñar — quitarlo dejaba 1 error, no los 61 en 43 ficheros que producía el escenario inverso. Al añadir después la tabla del antirreplay, el typecheck dio **un error local** en vez de ~15 en el módulo fiscal: la prueba de que el arreglo funcionaba.

**`qa-029` tenía una tercera salida que el issue no contemplaba.** Planteaba columna nueva en `bandeja_ingesta` o excepción al modelo «el JSONB manda». Ninguna hacía falta: los conceptos del OCR son el *valor por defecto* de la nota, no su dueño, así que basta con no pisar lo que ya hay. Sin migración y sin excepción, y `/ingesta` sigue mostrando solo OCR. Verificado antes de apoyarse en ello: la factura nace con `notas` a null y la derivación existe en un solo sitio del repo.

**`qa-020` tenía una hoja más de la que decía el issue** — `[modelo]/page.tsx` además de `[modelo]/[periodo]/page.tsx`. Apareció grepeando los hermanos: el patrón nº1 alcanzó al propio issue que lo describía. El test recorre el árbol de páginas, no una lista, y exime `fiscal/page.tsx` por derivación (no lee datos fiscales, solo redirige) en vez de por lista blanca.

**`qa-022` destapó tres cosas fuera de su enunciado**: la UI pintaba `posible_duplicado` como severidad media cuando el motor la emite alta (comparados los 19 tipos de los dos mapas: solo esa e `iva_mismatch` divergían, al revés); la rama `res.status === 409` del cliente se tragaba cualquier 409 con el mensaje «ya fue aprobada»; y el mock con proyección real de columnas —lección escrita en `qa-009` dos días antes— cazó que el `select` no pedía `proveedor_id`, así que en prod la búsqueda de colisiones no habría encontrado nada.

**Dos derivaciones propias salieron mal y se cazaron a tiempo**: contar `readonly !== true` daba 53 tools «que escriben» (flag sin dientes, default false); y un test que prohibía la palabra `orgHasFeature` falló contra los comentarios que explican por qué ya no se usa.

**Entorno**: la mitad del tiempo se fue peleando por memoria contra una sesión paralela y Spotlight reindexando. Un push tardó ~25 min con 57 MB libres y uno con 1,85 GB. Serializar sesiones antes de una tanda larga.

**Sin hacer y no maquillado**: los smokes de navegador de los 10 cambios visibles ya mergeados. Y en esta tanda se navegó un rato autenticado con la cuenta personal en vez de la de e2e (cero escrituras, tramo descartado); retomar exige sesión limpia del usuario e2e.

---

## Cierre: las dos decisiones, 4 agentes de análisis y 4 de smoke (31-jul)

**`qa-014` — retirada mi propia propuesta.** Iba a bloquear el envío con un estado nuevo `blocked_test`. Un agente adversarial la tumbó y los datos le dieron la razón: de los 89 emails de la sandbox, la mayoría son avisos internos al equipo. `is_test` describe la **organización**; el riesgo lo define el **destinatario**. La condición correcta es la conjunción, y se **redirige** en vez de bloquear (sin migración, sin estado nuevo). Pero el agente proponía usar solo el destinatario, lo que habría capturado también el correo de organizaciones reales: hubo que sintetizarlo críticamente, no obedecerlo. Un segundo agente cruzó sus afirmaciones y corrigió una (`send-emails.ts` **sí** propaga `org_id`) y añadió la decisiva: **tres caminos mandan email sin pasar por `sendEmail`** (`inviteUserByEmail`, el `auth.resend` del navegador, y el Gmail de Workspace).

**`qa-017` — el issue lo describía mal y la medición cambió el marco.** No era un fallo de cliente: el motor SQL tampoco filtraba. Y en producción hay **0 partidas caducadas fuera de la sandbox**, porque el alta por compra **nunca rellena `caducidad`** — la funcionalidad de lotes está inerte. El arreglo es preventivo: el automatismo nunca elige caducado, la elección manual sigue disponible, y se distingue "no hay stock" de "lo que queda está caducado".

**La mig 601 se desplegó muerta.** Firma con un parámetro inventado → sobrecarga → los llamantes seguían en la vieja. `db push` dijo `Finished`. Lo cazó `pg_proc` devolviendo dos filas. Mig 602 lo corrige. El learning existía desde mayo y no estaba en `hot.md`.

**Los smokes encontraron lo que la suite no veía.** El de UI destapó que mi arreglo de `qa-024` estaba a medias: cabecera corregida y **saludo del copiloto** diciendo todavía «Consulto tus datos, no hago cambios», en la misma pantalla. Mi test ataba la cabecera pero no prohibía la frase en el resto del fichero. El de ingesta descubrió que el guard de duplicados cuelga de un flag rancio (`qa-030`).

**Dos falsos positivos retirados verificando en Postgres**: los agregados negativos de `/recibidas` eran nuestra propia contaminación (`7265064420` con base −50), y el "FALLA" de `qa-022` venía de que el agente grepeó un checkout local desactualizado.

**Método**: agentes de navegador en paralelo exigen `--profile` **y** `--session` propios; uno lanzó `close --all` y mató el smoke de otro.

---

## Cierre de la auditoría funcional — 31-jul (8 PRs, #1423-#1431, mig 604)

**30 de 30 issues.** Los tres que quedaban, cerrados y verificados en producción.

**`qa-030` (#1423)** — el guard de duplicados de `qa-022` colgaba de `review_reasons`, que el OCR
escribe una vez: cubría **1 de 14** casos. Ahora consulta `facturas` en vivo, contando solo lo que ya
está en libros (`NOT IN ('sin_aprobar','disputada')`), para que la primera de un par recién subido no
se bloquee a sí misma. Verificado en prod sobre un caso real: la bandeja `97dbddd2` tiene
`review_reasons = ["total_mismatch"]`, sin marca de duplicado, y hoy devuelve 409 con las dos gemelas.
Antes se habría aprobado en silencio. Decisión escrita: la API v1 **no** recibe `confirmar_duplicado`
(dar a un cliente automático la llave de su propia confirmación vacía el guard).

**`qa-023` (#1424, mig 604)** — el código que nadie encontraba estaba en la RPC SQL
`resolve_proveedor`, no en TS. Eran **tres** implementaciones del mismo emparejado, no dos, y las tres
prometían por comentario que el NIF mandaba sin cumplirlo. La cifra que di primero, **92 facturas**, era mala: no
agrupaba por organización. Con `is_test` separado, 84 son de la sandbox y **8 de clientes**, de las que
**solo 2 son atribución a otra empresa** (IET, en libros y sin entrar en ninguna declaración), 1 es un
falso positivo (mismo NIF con prefijo `FR`) y 5 están en `sin_aprobar` con el proveedor correcto y un
NIF mal leído. Verificado contra `pg_proc` (una fila, sin sobrecarga) y con
consultas reales: NIF inexistente con nombre exacto, parecido o alias ajeno ya no empareja; sin NIF,
la dedup y el fuzzy siguen vivos. **La reparación de esas 92 filas NO va aquí**: `qa-031`.

**`qa-015` (#1425 · #1426 · #1427 · #1428)** — dos diagnósticos del issue eran incorrectos y esa es la
parte que valía: los tests "flaky" no dependen del reloj (es el coste de arranque del primer caso
contra el default de 5 s → `testTimeout` global), y el hydration mismatch no era ninguno de los cuatro
candidatos que salen leyendo código (era `classList.add` sobre un `className` que gobierna React; con
atributo tampoco vale, React 19 los diffea). Además: token de Meta en tiempo constante, `/api/health`
con caché corta y un límite que nunca responde 429, `<DateTimeField>` propio con el selector de eslint
que faltaba, y guard de cambios sin guardar en `/generar` (probado en navegador, incluido que un
editor en blanco NO pregunta).

Dos hallazgos colaterales: una recibida en estado `parcial` **era invisible** en el listado (lo delató
el candado de tipos puesto para el futuro), y dos fallos de fecha en paneles de admin, uno con dos
horas de desfase entre lo que se ve y lo que se guarda.

**Manuales al día (#1430)**: los 12 de prioridad alta, de los cuales cuatro no eran omisión sino
afirmaciones falsas (Textos Tipo en Obras, la factura que "no usa Textos Tipo", el copiloto "solo
consulta", y la promesa de confirmación con botón aplicada también al conector MCP).

Ver [[un-identificador-que-no-casa-tiene-que-vetar-el-respaldo-por-nombre]] ·
[[marcar-el-dom-por-fuera-de-react-rompe-la-hidratacion-tambien-con-atributos]] ·
[[un-limite-de-peticiones-en-el-healthcheck-no-puede-responder-429]] ·
[[beforeunload-no-cubre-el-atras-del-app-router-hace-falta-centinela-de-historial]] ·
[[guard-colgado-de-un-flag-calculado-una-vez-solo-cubre-ese-instante]]

---

## Cierre real de la sesión — `/fia-cierre` y lo que destapó (31-jul, #1437-#1441)

**Gate de cierre: con reservas, 0 bloqueantes, 23 avisos sobre 14 dimensiones.** Cero
hallazgos de seguridad, BD limpia (migs 604 y 606 con UNA firma cada una: la lección de la
sobrecarga de la 601 sí se aplicó).

**qa-032 implementado sin preguntar al cliente** (#1438): se miró cómo lo resuelven Odoo, SAP
ERP y Dynamics 365 BC y los tres coinciden, así que la pregunta ya tenía respuesta del
sector. Verificado en prod con datos reales: producto con 3 días de vida útil → partida con
caducidad a 3 días; sin el flag → NULL. Ver
[[el-dato-canonico-vive-en-el-lote-y-el-producto-solo-siembra]].

**Los cabos del gate, cerrados** (#1440). El más importante era mío: `qa-030` convirtió el
409 de duplicado de raro (1 de 14) a frecuente (6 de 24), y dos superficies se quedaron sin
salida, una de ellas el swipe del móvil, que no aprobaba y no decía nada. Al arreglarlo casi
entra algo peor: el `MouseEvent` habría entrado como `confirmarDuplicado` y **toda**
aprobación habría confirmado duplicados en silencio. Ver
[[un-guard-que-pasa-de-raro-a-frecuente-obliga-a-repasar-sus-superficies]] ·
[[anadir-un-parametro-a-un-handler-usado-como-onclick-mete-el-evento-dentro]].

**La suite E2E dio su primera tanda concluyente en meses** (#1441): `E2E_BASE_URL` apuntaba a
un puerto muerto y, como Playwright no levanta el servidor, cada spec agotaba su timeout y la
tanda acababa en "9 de 13 rojos" tras media hora. Con el preflight puesto: **109 pasan, 8
fallan, 23 saltados**. De los 8, dos son contención y uno es **preexistente**, comprobado
levantando un worktree del commit anterior a la sesión y viéndolo fallar igual. El resto, en
`qa-035`. Ver
[[un-checker-que-se-pone-rojo-por-la-razon-equivocada-es-peor-que-no-tenerlo]].

**Reparación de IECE ejecutada** (#1437): las dos facturas ya cuelgan de su proveedor real,
alias de GUARCONSA vacíos, cero discrepancias. Decidido NO avisar al cliente: importe, fecha
y número siempre fueron correctos, ninguna llegó a una declaración.


### Retirado del dashboard del hub el 31-jul (detalle íntegro)

- 🟢 **Dos tickets del runner ("manuela") en main (29-jul, #1326 + #1327)** — reimportar una tarifa ya no borra `vigencia_tarifa`, y "Nuevo presupuesto" deja de abrir una factura. Tickets #97/#98 en `resuelto`, smoke en prod hecho; el "gate FALLÓ" del runner era un OOM de su entorno. **Decisión pendiente**: en prod NINGUNO de los 17.831 materiales tiene `vigencia_tarifa` (el CSV de IET trae la columna vacía), así que el #98 se cierra sin que el cliente note nada → pedirle a IET un export con la fecha, o quitar la promesa de la ficha. Ver [[fia-gate-watchdog-mata-la-cadena-entera-con-un-solo-presupuesto]]

- 🟢 **Ticket #96 (IET) cerrado en código: contactos múltiples + condiciones de pago (28/29-jul, #1324 + #1325, migs 583-587)** — tabla única `contactos` que absorbió los 285 de Obras conservando su id; el vencimiento se pacta en la ficha del cliente con snapshot en la factura. Las revisiones adversariales (50 hallazgos) evitaron tres desastres, uno de ellos que el bloque no llegara al PDF emitido. PDF emitido **verificado por Manu (29-jul)**. **Queda solo** el PR-3 con el DROP de `obras_contactos`. Ver [[ADR-044-tabla-unica-de-contactos-en-vez-de-una-por-modulo]] · [[agent-browser-select-custom-click-opcion-no-registra-usar-teclado]]

