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

- **Tipar admin client Supabase = migración por fases (HECHA en FacturaIA, PR #648)** — alias incremental + gate por commit + flip final. Ver [[supabase-tipar-admin-client-global-cascada-300-errores]]
- **Select con columna inexistente = query ENTERA a null, error tragado (42703)** — así vivió el worker VeriFACTU 6 semanas como no-op. Ver [[supabase-select-columna-inexistente-falla-query-entera-42703]]
- **`curl -sf` trata 3xx como éxito** — cron con redirect de middleware reporta verde sin ejecutar el handler jamás. Ver [[curl-sf-trata-redirect-3xx-como-exito-en-crons]]
- **`next build` huérfano corrompe `.next` + hook pre-push bloquea push** — "Another next build running"/ENOENT `_ssgManifest.js`; `rm -rf .next`, rebuild, o push por ref + `--no-verify`. Ver [[next-build-lock-huerfano-hace-fallar-pre-push-hook]]

## de la semana

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
- **Turbopack rechaza node_modules symlinkeado en worktree** — `tsc`/`vitest` sí, `next build` no; usar `npm install` real. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **`git diff main <branch>` engaña si tu main local avanzó** — otra sesión mergea → ves cambios fantasma como del branch; usa `git diff $(git merge-base main <branch>) <branch>` o `git show --stat HEAD` en el worktree. Ver [[git-diff-vs-main-drifteado-usar-merge-base]]
- **Pill `overflow:hidden` en grid rígido se recorta en modal estrecho** — dentro de modal/drawer el ancho ≠ viewport → usa **container query** (`container-type: inline-size` + `@container`), no `@media`. Ver [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]]
- **Reempaquetar planes → grandfathering ANTES de tocar `plan_features`** — snapshot a `org_features` (source `grandfathered`) de lo que cada org activa tiene hoy, misma migración, o los clientes pierden acceso. Ver [[grandfathering-snapshot-antes-de-reempaquetar-planes]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/` (recall por relevancia).

- **Smoke visual SSR sin password** — sesión Supabase inyectada en Playwright (generateLink+verifyOtp+cookie sb-ref base64). Ver [[smoke-visual-ssr-sesion-inyectada-playwright]]
- **Playwright + componentes custom (checkbox hidden / Select portal)** — clickar label wrapper no input; `waitFor([role="listbox"])` antes de leer opciones; `toHaveValue()` entre fill y submit. Ver [[playwright-custom-components-e2e-selectors]]
- **WhatsApp interactive → await upsert antes de enviar botones** — el button_reply llega antes que el fire-and-forget; escritura en BD debe ser await+guard antes del send. Ver [[whatsapp-await-upsert-antes-de-botones-interactivos]]
- **Docker cache activa → builder prune no basta si hay contenedor activo** — usar `docker compose build --no-cache <svc>` desde el dir del compose. Ver [[docker-layer-cache-persiste-con-contenedor-activo]]
