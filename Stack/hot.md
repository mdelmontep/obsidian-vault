---
title: hot cache
date: 2026-06-26
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo de la semana (1 línea + link al learning). Los patrones
transversales recurrentes (git/worktrees · método prod · frontend glass · deps) se
movieron a [[index]] §Transversales. Lo demás vive en `knowledge/learnings/` (recall por
relevancia) y los universales en [[patterns-cross-proyecto]]. Podado 2026-06-26 (49→6).

- **`git checkout <file>` en el red-check TDD deja el commit sin el fix** — restaura a HEAD (borra fix+export); `next build` no compila tests → PR roto pasa el build. Verifica `git show --stat` (source+test) y corre el TEST, no solo build. Ver [[git-checkout-file-en-red-check-deja-commit-sin-fix]]
- **Integrar SaaS en codebase existente: grep el wrapper antes de asumir el SDK** — puede haber cliente REST propio (FacturaIA: `stripe-rest`, no el paquete `stripe`); instruir a subagentes "reusa el patrón del repo", no "usa el SDK". Ver [[codebase-existente-grep-wrapper-antes-de-asumir-sdk]]
- **`fork` (hereda contexto) se va meta en features grandes** — para implementar 10 ficheros hazlo inline o con `general-purpose` acotado, no un fork; verifica en disco lo que produjo. Ver [[claude-code-agentes-worktree-failure-modes]] §F
- **Columna nueva sin desplegar rompe el typecheck del `.select()` supabase** — la migración no está en prod → `gen:types` no la trae → el cliente tipado marca error-branded toda la query. Cast local del builder, retirar tras gen:types. Ver [[supabase-select-columna-nueva-no-en-gen-types-falla-typecheck]]
- **Paso de elección conversacional: resolver la respuesta primero, la pregunta es fallback** — guardar "cualquier texto" traga preguntas/órdenes/emoji; el STT mete "?" por entonación. Ver [[paso-eleccion-conversacional-resolver-respuesta-antes-que-pregunta]]
- **No pidas elegir opciones que el usuario no puede probar aún** — voz por nombre (clara/diego) sin TTS viva = elección a ciegas; pregunta por atributo (femenina/masculina) o default. Ver [[no-pedir-elegir-opciones-que-el-usuario-no-puede-probar]]
- **Voz streaming (retell): dedup de turnos por firma del transcript, re-emitir voz sobre el response_id actual** — reemit de turno duplica efectos; no descartes el turno (latest-wins → caller mudo). Ver [[voz-dedup-turno-por-firma-transcript-reemitir-sobre-response-id-actual]]
- **QA contra agente con memoria = hilo limpio o reset entre rondas** — el historial envenenado ancla al LLM y los fixes parecen no aplicar. Ver [[llm-hilo-envenenado-ancla-tools-frescos-mandan]]
- **`void` sobre builder supabase = query NUNCA ejecutada** — thenables lazy; fire-and-forget con `.then(()=>{})`. Ver [[supabase-builders-lazy-void-nunca-ejecuta]]
- **`new Date(y,m,d).toISOString()` = día anterior fuera de UTC** — rangos de fecha corridos un día; strings + Intl con timeZone. Ver [[new-date-toisostring-desplaza-un-dia-fuera-de-utc]]
- **PostgREST: max-rows trunca a 1000 en silencio + `.in()` grande revienta la URL** — paginar `.order(pk).range()` y chunkear ids ≤150; caso export contable. Ver [[postgrest-max-rows-trunca-silencioso-in-revienta-url]]
- **Tipar admin client Supabase = migración por fases (HECHA en FacturaIA, PR #648)** — alias incremental + gate por commit + flip final. Ver [[supabase-tipar-admin-client-global-cascada-300-errores]]
- **Select con columna inexistente = query ENTERA a null, error tragado (42703)** — así vivió el worker VeriFACTU 6 semanas como no-op. Ver [[supabase-select-columna-inexistente-falla-query-entera-42703]]
- **`curl -sf` trata 3xx como éxito** — cron con redirect de middleware reporta verde sin ejecutar el handler jamás. Ver [[curl-sf-trata-redirect-3xx-como-exito-en-crons]]
- **`next build` huérfano corrompe `.next` + hook pre-push bloquea push** — "Another next build running"/ENOENT `_ssgManifest.js`; `rm -rf .next`, rebuild, o push por ref + `--no-verify`. Ver [[next-build-lock-huerfano-hace-fallar-pre-push-hook]]
- **Dos toasters (ToastContext vs sileo): usar el que no tiene provider en esa área = no-op silencioso** — FacturaIA `(admin)` monta sileo, no `ToastProvider`; `useToast` allí no mostraba nada. Ver [[dos-sistemas-toast-usar-el-sin-provider-es-noop-silencioso]]
- **Pooler Supabase caído (5432 timeout) → DDL vía MCP execute_sql + gen:types (API HTTPS sigue viva)** — no bloquea la sesión; luego `db push` registra la migración. Ver [[supabase-pooler-caido-aplicar-ddl-via-mcp]]
- **Tipos Supabase: regenerar con `--linked`, no augmentar Database global a mano** — `--db-url` borra `__InternalSupabase` (rompe drift-check); override global dispara errores en cascada. Ver [[gen-types-linked-no-db-url]]
- **Antes de migrar cualquier cron FacturaIA a `sign-call.sh` (HMAC v2): grep el 2º arg de `withCronTracking` por `auth:` custom** — se repitió el mismo error (`verifactu-process`) 2 meses después de documentarlo. Ver [[dokploy-cron-docker-exec-no-hereda-env-de-app-env]] ADENDA 3
- **Cron sin NINGÚN run histórico → salud `'desconocido'`, nunca `'rojo'` → nunca alerta** — auditar `CRON_REGISTRY` vs `schedule.list` real de Dokploy, no fiarse del panel. Ver [[cron-health-desconocido-para-cron-sin-ningun-run]]
- **Filtro adjuntos email por `Content-Disposition:inline` no basta** — ESPs sin esa cabecera cuelan logos vía `cid:`; cruzar Content-ID vs HTML + tamaño mínimo. Ver [[ingesta-email-imagenes-inline-firma-tratadas-como-adjuntos-facturables]]
- **Callback PSD2 sin OAuth (Salt Edge): validar dueño del `connection_id` antes de persistir** — sin token scoped, el id de recurso solo, cruza tenants. Ver [[psd2-callback-connection-id-sin-oauth-debe-validar-dueno]]
- **Payment link con importe congelado: revalidar el pendiente al conciliar, no confiar en el importe fijado al crearlo** — cobro parcial concurrente por otra vía lo deja obsoleto. Ver [[payment-link-importe-congelado-revalidar-pendiente-al-conciliar]]

## de la semana

- **cloudflared quick tunnel muere si la red bloquea el puerto 7844** — WiFi oficina lo bloquea (QUIC+TCP); usa hotspot 4G o ngrok/443; localtunnel rompe el webhook de Meta. Ver [[cloudflared-tunnel-bloqueado-puerto-7844-usar-hotspot]]
- **Meta WhatsApp dev: usa el test number, no asocies la app al Business de prod** — muestra el WABA de prod y suscribir `messages` secuestra el webhook en vivo. Ver [[meta-whatsapp-dev-sandbox-usar-test-number-no-business-de-prod]]
- **Agente de acciones robótico/interroga = system prompt sin 3 secciones** — capacidades declaradas + asumir(lectura)/confirmar(escritura) + few-shot; confirmación = resumen determinista + envoltura. Ver [[agente-accion-disclosure-capacidades-y-asumir-vs-confirmar]]
- **`op read` con timeout de autorización → parar y pedir reautorización, NUNCA pegar el secreto literal en el comando como fallback** — el clasificador de Claude Code bloquea cualquier bash con el secreto en texto plano, venga de donde venga. Ver [[op-read-secreto-nunca-en-comando-bash-ni-desde-memoria]]
- **ADR/roadmap propio puede estar stale vs. código real** — verificar contra git log + API en vivo del sistema externo (n8n, etc.) antes de planificar encima, aunque el propio doc del repo lo dé por pendiente. Ver incidente 2026-07-04 en `Stack/incidents.md`
- **HITL: el resumen de confirmación debe nombrar la entidad que un campo desambigua** — y NO early-return del caso único antes de aplicar ese filtro (o lo ignora en silencio). Ver [[hitl-resumen-debe-nombrar-entidad-desambiguada]]
- **Tests `*.pg.test.ts` que se autosaltan sin DB → levantar `pgvector/pgvector:pg16` local** — postgres pelado falla por `CREATE EXTENSION vector` (el catch lo traga como "no disponible"). Ver [[tests-pg-self-skip-levantar-pgvector-local]]
- **ZIP mínimo en navegador sin deps: método STORE + DataView a mano** — local header 30B + central dir 46B + EOCD 22B, CRC32 tabla estándar. Ver [[zip-minimo-navegador-sin-dependencias-store]]
- **Graph calendarView ignora `Prefer:timezone` en la ventana** — start/end se interpretan en UTC sin offset; incluir offset real (Intl longOffset, DST). Ver [[graph-calendarview-ventana-utc-no-prefer-timezone]]
- **OAuth PKCE sin store → verifier en `state` cifrado** (no solo firmado) + nonce/exp. Ver [[oauth-state-cifrado-para-pkce-verifier-sin-store]]
- **Tests integración comparten BD → `vitest fileParallelism:false`** — TRUNCATE global entre ficheros se pisa. Ver [[vitest-fileparallelism-false-tests-integracion-bd-compartida]]
- **FK compuesta `(tenant_id, id)` = anti-cross-tenant estructural** — impide enlazar entre tenants a nivel BD, no solo con WHERE. Ver [[fk-compuesta-tenant-id-defensa-multi-tenant-estructural]]
- **Frontera de datos (PII) = ausencia de columna + test de conjunto-exacto** — no filtres lo que no debe existir; introspección `information_schema` con `toEqual`. Ver [[frontera-de-datos-por-ausencia-de-columna-no-por-filtro]]
- **Migración colisión NNN entre ramas** — git mv → placeholder → repair --status applied → push. Ver [[supabase-migration-numero-colision-renumerar]]
- **`supabase db push` sube TODAS las pendientes, no solo la tuya** — aparta con `mv` la migración ajena sin commitear, push, devuélvela. Ver [[supabase-db-push-aplica-todas-pendientes-aparta-las-ajenas]]
- **Recordatorio WhatsApp programado → SIEMPRE plantilla utility** — no hay API de ventana 24h; asume el peor caso. Ver [[whatsapp-recordatorio-diferido-siempre-plantilla-utility]]
- **BullMQ = disparador efímero, BD fuente de verdad + reconciliar al boot** — `removeOnFail:true` (un job fallido retenido bloquea el re-arma por jobId). Ver [[bullmq-cola-efimera-bd-fuente-de-verdad]]
- **Integrar interfaz de otra PR no mergeada → tipado estructural, no import** — `import type` de fichero ausente rompe `tsc`; misma firma satisface la interfaz al mergear. Ver [[cross-pr-integrar-interfaz-por-tipado-estructural]]
- **Validar enum lanzando en el mapper de LECTURA tumba el barrido de arranque** — fix de origen = CHECK en BD / validar en escritura; en lectura degrada, nunca lances en un reconciler/hot-path. Ver [[store-guard-lanza-en-lectura-tumba-reconciler]]
- **Agendar por LLM: reloj en el prompt + hora local del modelo + conversión UTC en código** — sin "ahora" no resuelve "el jueves"; resuelve el instante ANTES del HITL. Ver [[llm-agendado-reloj-en-prompt-y-conversion-utc-en-codigo]]
- **HITL: re-resuelve nombre→id en execute, no en prepare** — el move `correct` salta `prepare`; id inyectado queda stale al corregir el nombre. Pre-valida en prepare (el confirm no captura). Ver [[hitl-reresolver-nombre-id-en-execute-no-inyectar-en-prepare]]
- **Reset multi-tenant → allowlist ordenada + to_regclass, no catálogo dinámico** — + test-guard de completitud bidireccional; guard duro contra tenant vacío. Ver [[reset-multi-tenant-allowlist-ordenada-vs-catalogo-dinamico]]
- **Fake vs Postgres divergen en orden** — `.sort()` UTF-16 ≠ collation; usar `localeCompare` en el fake. Ver [[fake-vs-postgres-orden-sort-utf16-vs-collation]]
- **Guard cross-tenant en upsert de clave global** — `DO UPDATE ... WHERE tenant_id=EXCLUDED` + rowCount (cierra TOCTOU, nunca reasigna dueño). Ver [[guard-cross-tenant-do-update-where-tenant-id-toctou]]
- **Extender un flujo sin tocar el core de otro → decorator de su interfaz** — envuelve e intercepta; delega tal cual cuando no aplica; estado en store propio. Ver [[decorator-de-interfaz-para-extender-sin-tocar-el-core]]
- **JS `\b` no casa junto a acentos** — "sí"/"ya está" no matchean; normaliza NFD (quita diacríticos) antes de matchear comandos; comando exacto, no `contains`. Ver [[regex-word-boundary-no-casa-acentos-js-normalizar-nfd]]
- **`git mv` sobre untracked falla pero renombra igual** — no asumas que no hizo nada por el exit≠0. Ver [[git-mv-archivo-untracked-falla-pero-renombra-igual]]
- **CSS Module + glass tokens** — `composes: glass-panel scrim from global`; eliminar local `background`. Ver [[css-modules-composes-glass-panel-scrim]]
- **Tour spotlight in-modal** — tourBlocker z-5 + tourHighlight z-10 + tourTooltip z-20; lookup CSSProperties por step; localStorage gate. Ver [[modal-tour-spotlight-pattern]]

- **Prompt doc_type PASO 0: "factura" por EMISOR, no por IVA** — seguros/sanidad/intracom tienen iva=0 y son facturas; "justificante_pago" = solo comprobante bancario de transferencia. Ver [[ocr-clasificacion-iva-zero-seguros]]
- **doc_type no-factura (justificante/extracto) → OCR solo clasifica, no extrae campos** — `datos_extraidos.total/fecha/prov` siempre vacíos para esos tipos; features sobre ellos necesitan segundo pase (`extractMovimientosFromDoc`). Ver [[ocr-clasificacion-doc-type-no-factura-sin-campos]]

- **WhatsApp OCR: discriminadores internos divergen producer→caller → silencio total en paths non-success** — leer body real del endpoint antes de escribir el caller; grep callers al cambiar shapes. Ver [[whatsapp-internal-http-discriminador-shape]]

- **OCR WhatsApp: ingesta almacena, el caller dispara ocr-process por separado** — portar solo ingesta deja bandeja en `procesando` indefinidamente. Ver [[whatsapp-ocr-trigger-no-es-ingesta-es-caller]]
- **Vitest mock clase ES module → `vi.hoisted` antes del factory** — "not a constructor" si referencias vi.fn() no hoisted. Ver [[vitest-mock-clase-esm-vi-hoisted]]
- **Webhook HMAC test → computar firma real, no mockear verify** — mock bypassa la verificación → falso positivo estructural. Ver [[whatsapp-webhook-test-hmac-computar-real]]
- **PostgREST `!inner` join sin FK directa → 400 runtime** — query separada + `.in('org_id', ids)`. Ver [[postgrest-join-inner-sin-fk-directa]]
- **`triggered_by` CHECK violation → 23514, no 23505** — valores válidos: `'cron'|'manual'`; usar `'manual'` para copiloto/UI. Ver [[supabase-check-constraint-triggered-by-enum]]
- **`clientes`/`proveedores`: filtrar activos con `.is('archivado_at', null)`, NO `.eq('activo', true)`** — mig 190: soft-delete por timestamp, columna `activo` no existe. Ver [[clientes-proveedores-filtrar-activos-archivado-at]]
- **Tool copiloto: campo en interface pero no en `.select()` → guard mudo** — preview PASS, execute FAIL en RPC. Añadir campo al select y al interface. Ver [[copiloto-tool-select-campo-faltante-guard-mudo]]

- **Turn lock para agentes LLM con historial persistido** — SETNX Redis + Map fallback; acquire antes del runner, release en finally. WhatsApp: 200 en vez de 409. Ver [[copiloto-turn-lock-concurrent-llm-calls]]

- **PostgREST: columna inexistente en SELECT → 400 silencioso (data=null, no error)** — se propaga como "no encontrado"; verificar schema tabla-específica en arquitecturas two-table. Ver [[postgrest-columna-inexistente-en-select-retorna-400-data-null]]
- **UPDATE atómico no acopla lo crítico (liberar lock) con lo cosmético (status)** — `cleanup_cron_zombies` escribía `status='zombie'` fuera del CHECK → tumbaba el UPDATE entero → el lock del watchdog nunca se liberaba (auto-curador suicida). Separar: liberar recurso (campos sin constraint) + metadata best-effort (`EXCEPTION WHEN check_violation`). Ver [[update-atomico-no-acopla-liberacion-critica-con-metadata-cosmetica]]
- **Copiloto WhatsApp — campo faltante → preview gate** — Zod optional + preview throw si falta; LLM reintenta con el dato en siguiente turno. Ver [[copiloto-zod-required-blocks-llm]]
- **Verifactu XSD: SistemaFacturacion.xsd (404) → SuministroInformacion.xsd + SuministroLR.xsd** — dos namespaces, envelope vs. datos; confirmar split en smoke PRE. Ver [[verifactu-xsd-namespace-suministroinfo-vs-sistemafacturacion]]

- **Zod v4 trae `z.toJSONSchema` nativo — deriva el tool-schema del LLM, no lo dupliques** — un `input_schema_json` a mano en paralelo al Zod miente al LLM (required/enum divergen). Fuente única: derivar; `.describe()` por campo. Ver [[zod-v4-tojsonschema-nativo-deriva-tool-schema]]
- **Outbox: event-type fuera del catálogo suscribible muere en silencio** — el trigger lo encola pero nadie puede suscribirse → `fanout_completed` sin delivery. Guard: test-contrato emisor(SQL)⊆catálogo(enum). Ver [[outbox-event-type-fuera-del-catalogo-muere-silencioso]]
- **Port devuelve dato discriminado; el caller traduce a throw en su borde** — el port nunca lanza por precondición (found/none/ambiguous, ok/conflict); el framework no cambia y el adapter in-memory testea sin mockear el query-builder. Inyección opcional (`ctx.store?`) = blast radius mínimo. Ver [[port-devuelve-dato-discriminado-tool-traduce-throw-en-borde]]
- **Converger un canal divergente sobre la fuente única** — bordes (auth/cuotas/audit/error-codes) se quedan en el canal; pasar IDs ya resueltos; flags opt-in (`skipAudit`/`checkQuota`/`nifValidation`) para deltas sin tocar otros callers; traductor de errores al `error_code` del canal. Ver [[converger-canal-divergente-sobre-fuente-unica]]
- **Skin app-wide = una palanca de superficie + base opaca aparte** — cards usan `--bg-elev` (el skin lo vuelve translúcido vía `[data-skin]` → todas esmerilan a la vez); `--elev-solid` opaco sostiene el compositing del glass. Blur por regla, no por token. Ver [[skin-app-wide-token-superficie-unico-base-opaca]]
- **Dokploy `autoDeploy=false` = desfase silencioso** — los merges a main no despliegan; el servicio sirve build viejo sin avisar. Fix: GH Action path-filtered o alerta de desfase (hash de `/health` vs main). Ver [[dokploy-autodeploy-false-desfase-silencioso]]

- **E2E smoke: skip honesto por precondición, no falso rojo** — gating por la fuente autoritativa (`featureActive` → `GET /api/settings/features`), nunca texto de UI ni 404; skip SOLO si falta la precondición, jamás relajar una aserción que cace un bug. Ver [[e2e-smoke-skip-honesto]]
- **BD fuente de verdad vía cache en memoria → hidratar en LECTURA** — la cache module-level arranca null tras deploy; si solo hidratas al escribir, el runtime cae al fallback (env) hasta la 1ª escritura. `ensureCache()` lazy en cada consumidor. Ver [[bd-fuente-verdad-via-cache-memoria-hidratar-en-lectura]]
- **Smoke test-mode contamina BD prod si la fn escribe en BD** — Stripe TEST no aísla la BD (única=prod); aísla por dato sentinel desechable + guard que rehúsa `sk_live`. Ver [[smoke-test-mode-contamina-bd-prod-si-la-fn-escribe-bd]]
- **Gate solo en wrapper web no cubre canales** — voz/WA/v1/cron/MCP usan otro auth; el enforcement de plan/cuota/billing debe replicarse por canal o centralizarse en la fuente única. Ver [[gate-en-wrapper-web-no-cubre-canales-con-otro-auth]]
- **Contador de cuota best-effort = cuota infinita** — increment con solo `console.error` tras el check; si el RPC falla, el contador se congela. Hacerlo observable (alerta/tabla con status). Ver [[contador-de-cuota-best-effort-tras-check-es-cuota-infinita]]
- **Stripe price (lo que cobra) ≠ precio BD editable** — lo cobrado vive en el env (`STRIPE_PRICE_ID_*`, price inmutable), no en `plans.precio_mes`; editar admin no cambia el cobro → drift (UI 14€, checkout 19€). Ver [[stripe-price-id-en-env-vs-precio-bd-editable-derivan]]
- **PostgREST corta agregaciones en JS (cap max-rows 1000)** — sumar filas con `reduce` infravalora en silencio; `count:'exact'` sí es exacto → cifra y count incoherentes. Agrega en BD (RPC SUM) o `.limit(N+1)`+`truncated`. Ver [[postgrest-max-rows-trunca-agregacion-en-js]]
- **Motor con input requerido → defaultea, no falles mudo** — un default sensato en el motor (FEFO) > parchear N bordes; los canales ciegos no pueden aportar el campo. Ver [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]]
- **Actions caído (billing) → hooks locales = único gate** — un merge con `--no-verify` cuela lint/build roto a main. `npm run lint` global antes de cada merge; node_modules real (`npm ci`) para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]]
- **Hook pre-commit (build) muere por OOM si hay dev server vivo** — lo reporta como "lint con errores" (falso positivo). Matar `npm run dev` antes de commitear. Ver [[pre-commit-hook-oom-con-dev-server]]
- **Remesa SEPA pain.008 (adeudo directo)** — SeqTp a nivel PmtInf, control del Id de Acreedor `98-mod97(idNac+ES00)`, CtrlSum en céntimos, IBAN single-source. Ver [[sepa-pain008-remesa-adeudo]]
- **Cron materializador + collector en vivo = dedup en runtime, no con filtro de origen** — filtrar el cron crea gap cuando el servicio recupera entre ticks. Ver [[alert-collector-cron-vs-live-dedup-gap]]
- **Cron de mantenimiento auto-sanable no debe paginar (email), solo panel** — tunear umbral por-cron es frágil (recurrió); clasifícalo por criticidad → 'housekeeping' emite severidad 'media' sin email. Ver [[cron-mantenimiento-auto-sanable-no-debe-paginar-severidad-por-criticidad]]
- **Turbopack rechaza node_modules symlinkeado en worktree** — `tsc`/`vitest` sí, `next build` no; usar `npm install` real. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **`git diff main <branch>` engaña si tu main local avanzó** — otra sesión mergea → ves cambios fantasma como del branch; usa `git diff $(git merge-base main <branch>) <branch>` o `git show --stat HEAD` en el worktree. Ver [[git-diff-vs-main-drifteado-usar-merge-base]]
- **Working tree en rama STALE → verifica antes de reimplementar un follow-up** — con N worktrees el checkout principal puede estar en rama vieja; lee de `git show origin/main:<path>` + `git merge-base --is-ancestor <commit> origin/main` antes de construir (casi reimplementé #82, ya mergeado). Ver [[working-tree-en-rama-stale-verifica-antes-de-reimplementar]]
- **Pill `overflow:hidden` en grid rígido se recorta en modal estrecho** — dentro de modal/drawer el ancho ≠ viewport → usa **container query** (`container-type: inline-size` + `@container`), no `@media`. Ver [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]]
- **Reempaquetar planes → grandfathering ANTES de tocar `plan_features`** — snapshot a `org_features` (source `grandfathered`) de lo que cada org activa tiene hoy, misma migración, o los clientes pierden acceso. Ver [[grandfathering-snapshot-antes-de-reempaquetar-planes]]
- **Sanitizador que reconstruye objeto por allowlist se ejecuta también al RENDERIZAR, no solo al guardar** — campo nuevo no listado se pierde en cada render aunque esté bien en BD. Ver [[sanitizador-allowlist-reconstruye-objeto-descarta-campos-nuevos]]
- **Campo opcional ya en el tipo compartido puede seguir vacío por N `.select()` distintos que no lo piden** — grep `.select(`/`from('tabla')` sobre la tabla origen, no solo el tipo. Ver [[campo-opcional-en-tipo-compartido-no-implica-seleccionado-en-todos-los-selects]]
- **Dokploy `compose.one`/`schedule.one` devuelven el `env` completo del compose** — nunca llamarlos solo para leer metadata; usar `deployment.allByCompose`. Ver [[docker-infra]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/` (recall por relevancia).

- **Smoke visual SSR sin password** — sesión Supabase inyectada en Playwright (generateLink+verifyOtp+cookie sb-ref base64). Ver [[smoke-visual-ssr-sesion-inyectada-playwright]]
- **Playwright + componentes custom (checkbox hidden / Select portal)** — clickar label wrapper no input; `waitFor([role="listbox"])` antes de leer opciones; `toHaveValue()` entre fill y submit. Ver [[playwright-custom-components-e2e-selectors]]
- **WhatsApp interactive → await upsert antes de enviar botones** — el button_reply llega antes que el fire-and-forget; escritura en BD debe ser await+guard antes del send. Ver [[whatsapp-await-upsert-antes-de-botones-interactivos]]
- **Docker cache activa → builder prune no basta si hay contenedor activo** — usar `docker compose build --no-cache <svc>` desde el dir del compose. Ver [[docker-layer-cache-persiste-con-contenedor-activo]]
- **Gate de drift de schema Postgres** — `DROP/CREATE DATABASE` un `-c` por sentencia; filtrar `\restrict` (token aleatorio de pg_dump ≥16); `pg_dump` dentro del contenedor por paridad de versión. Ver [[drift-gate-schema-postgres-psql-c-y-pg-dump-16]]
- **Migraciones incrementales + schema.sql idempotente** — migraciones *guarded* (no-op en BD nueva, aplican en existente) → un solo camino de runner; drift-gate prueba que convergen. Ver [[migraciones-incrementales-conviviendo-con-schema-sql-guarded]]
- **gh: borrar base de PR apilada cierra la hija (irreversible)** — retargetear hijas a main ANTES de mergear/borrar la base. Ver [[gh-borrar-base-de-pr-apilada-cierra-la-hija-irreversible]]
- **Split de fichero sin cambiar comportamiento** — extracción verbatim + checker independiente + `_parts/<basename>/` (no `_parts/` plano). Ver [[split-verbatim-checker-parts-por-basename]]
- **gh pr merge miente en el stdout** — verifica `gh pr view <n> --json state` == MERGED, no el texto ("will be automatically merged" contiene "merged"). Ver [[gh-pr-merge-no-confirma-verificar-state-merged]]
- **`gen:types --linked` cuelga sin error si 5432/6543 están bloqueados en la red** — usar `--project-id <ref> --schema public,graphql_public` (HTTPS); ojo caché, verificar tablas eliminadas contra `information_schema` antes de commitear. Ver [[supabase-pooler-timeout-isp-fallback-dashboard]]
- **agent-browser: verificar mensajes con `snapshot`, no solo screenshot** — un modal con scroll interno oculta contenido fuera del encuadre aunque sea `--full`. Ver [[agent-browser-verificar-snapshot-no-solo-screenshot]]
- **Import CSV de precios: desambiguar ES/US por presencia de coma, nunca `replace(/\./g,'')` incondicional** — "9.99" formato US se lee como 999 sin error. Ver [[csv-import-precio-decimal-es-us-desambiguar-no-asumir]]
