---
title: hot cache
date: 2026-05-07
tags: [stack, index]
---

# Hot Cache

Resúmenes 1-2 líneas con link al learning. Leer learning completo solo si necesario.

> Patrones permanentes cross-proyecto movidos a [[patterns-cross-proyecto]] (poda 2026-06-02).

## 🔥 Últimas 2 semanas

### facturaia — cuotas por tier: contratos implícitos (2026-06-12)

- **Collector alertas admin: dismissKey 2 partes** (`${alert_type}:${org_id}`) — granularidad extra embebida en el alert_type, no como sufijo; verificar contra el route real, no contra el mock. Ver [[admin-alert-collectors-dismiss-contract]]
- **Migs paralelas CREATE OR REPLACE se pisan** — consolidar la definición completa de la función en la mig de mayor número antes de prod. Ver [[migraciones-paralelas-create-or-replace-se-pisan]]

### supabase — auth.getUser() es red, no local (2026-06-12)

- **N helpers que llaman getUser = N round-trips GoTrue por request** — validar 1 vez en el wrapper del pipeline y pasar `user` como param opcional; `React.cache()` solo dedupea render pass RSC, no route handlers. Ver [[supabase-auth-getuser-valida-en-red-dedupe-pipeline]]

### git — sesiones paralelas mismo repo (2026-06-12)

- **Working tree compartido sucio → ship via worktree + diff-0** — worktree desde origin/main; archivo con `git diff origin/main HEAD` = 0 se copia wholesale; la sesión paralela puede commitear tu trabajo uncommitted. Ver [[shippear-quirurgico-desde-working-tree-compartido-sucio]]
- **Colisiones git en merge** — `Unable to write index` / `MERGE_HEAD` perdido a mitad / push bloqueado por `next build` lock; salida = worktree desde origin/main + cherry-pick aislado → PR. Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]]
- **Triaje ramas/worktrees multi-sesión** — borrable si cherry 0 **o** diff vs main vacío; lock huérfano = `ps -p` al PID antes de `remove -f -f`. Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]

### facturaia — Supabase: JWT de usuario sin password para smokes (2026-06-11)

- **`generate_link` magiclink (service role) + `/auth/v1/verify` (anon)** → `access_token` real del usuario sin conocer ni resetear su password. Ver [[supabase-mint-access-token-sin-password-via-generate-link]]

### facturaia — output LLM: Zod + audit en BD (2026-06-11)

- **Output LLM nunca con cast ciego** — safeParse Zod + parse failure a tabla de auditoría queryable antes del 5xx; obligatorios omitidos → default conservador que dispare revisión. Ver [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]]

### facturaia — glass: cascada de clase decorativa + AA compuesto (2026-06-10)

- **Clase decorativa compartida (solo `background-image`) = 2 trampas de cascada** — shorthand `background:` posterior la pisa (usar `background-color:`); guards de fallback al FINAL del archivo o quedan muertos. Ver [[css-clase-decorativa-compartida-trampas-cascada]]
- **AA sobre glass se verifica componiendo capas alpha en script** (peor fondo→scrim→panel→velo), no contra un color. Ver [[verificar-aa-sobre-glass-componer-capas-alpha]]

### facturaia — audit 349: normalización en group-by + .catch() muerto en supabase-js (2026-06-10)

- **Group-by sobre campo texto libre (nif_iva) exige normalizar en write path + migración de saneo** — una sola pata no basta. Ver [[agrupacion-por-campo-texto-libre-exige-normalizacion-en-write-path]]
- **supabase-js: `.catch()` sobre un query es código muerto** — los errores van en `{error}`; destructurar y throw. Ver [[supabase-js-catch-sobre-query-es-codigo-muerto]]

### facturaia — pulido UX 303/349 post-smoke visual (2026-06-10)

- **CSS Grid: `1fr` a secas = `minmax(auto,1fr)` y desborda si el min-content gana** — usar `minmax(0,1fr)` + `overflow-x:auto` interno. Ver [[css-grid-1fr-desborda-usa-minmax-0-1fr]]
- **Código de error de dominio (422 `sin_facturas`) = estado de producto** — mapear a estado vacío guiado, nunca volcar JSON crudo al banner. Ver [[codigo-error-de-dominio-es-estado-de-producto-no-error]]
- **Cada aviso una sola superficie** — panel de avisos solo accionables; lo informativo a badge/banner único. Ver [[cada-aviso-una-sola-superficie]]

### facturaia — CI: mock admin.rpc + Playwright getByText en hidden details (2026-06-10)

- **`admin.rpc()` en mock `createAdminClient` necesita declararse explícitamente** — sin él `TypeError: admin.rpc is not a function` rompe todos los tests del handler. Ver [[mock-supabase-fail-fast-default-en-tests-vitest]]
- **`getByText(x).first()` puede caer en elemento dentro de `<details>` cerrado** — scopear siempre al contenedor visible: `page.locator('.lista').getByText(x)`. Ver [[playwright-getbytext-first-hidden-details-element]]

### facturaia — Form parcial + UPSERT fila completa = pérdida silenciosa (2026-06-10)

- **Form que edita un subconjunto + endpoint que UPSERTea la fila entera defaulteando ausentes = borra columnas no mostradas** en cada guardado (caso perfil_fiscal: recargo/vivienda/rendimiento se reseteaban → cálculo 303/130 mal). Fix: mapper preserva `payload.x ?? existing.x ?? default` (lee fila antes del upsert; `??` no cae en `false` explícito). Ver [[form-parcial-upsert-fila-completa-borra-columnas-no-enviadas]]

### facturaia — Presentar modelos AEAT: fichero / conducto / colaborador social (2026-06-10)

- **3 formas de presentar un modelo AEAT** — (2) fichero oficial importable + el cliente firma; (3b) presentas con el cert del propio cliente (modelo Holded) → esquiva colaborador social; (3) colaborador social RD 1065/2007 = figura gestoría con RC obligatorio. 3b reaprovecha cert+firma de Verifactu. Ver [[aeat-formas-presentacion-fichero-vs-conducto-vs-colaborador-social]]

### facturaia — RLS: policy que subconsulta su tabla → recursión 42P17 (2026-06-10)

- **Anti-escalada en RLS sin recursión** — una policy con `SELECT FROM <tabla>` sobre la propia tabla protegida lanza `42P17`; usar función `SECURITY DEFINER` que bypasa RLS y comparar contra ella. Ver [[rls-policy-recursion-42P17-subquery-misma-tabla]]
- **PostgREST `.single()` → 406 con RLS multi-fila** — confiar en que la RLS devuelva 1 fila es frágil (p.ej. `profiles_select_same_org` expone N perfiles); filtrar por PK + `.maybeSingle()`. Ver [[supabase-maybesingle-devuelve-null-si-multiples-filas]]

### facturaia — Overflow móvil: layout viewport + grid span (2026-06-10)

- **Un `overflow-x:auto` con contenido más ancho que su caja expande el LAYOUT VIEWPORT móvil** (`innerWidth` crece, la página "encoge"); ni `overflow:clip` en ancestros lo arregla → `contain:layout` en el scrollable. Y `grid-column:span N` en grid colapsado a 1 col crea columna implícita → `1 / -1`. Diagnóstico: `pageScrollX=0` pero `innerWidth>vw` = viewport expandido, ≠ scroll de página (medir, no a ojo). Ver [[mobile-overflow-layout-viewport-contain-y-grid-span]]

### facturaia — Modal sin portal atrapado por sidebar sticky (2026-06-09)

- **Modal `position:fixed z:1000` sin `createPortal` montado en ancestro con stacking context queda por debajo de otro subárbol** — el feedback widget cuelga del `<aside sticky>`; su backdrop z:1000 quedaba scoped en el sidebar y `<main>` (KPI cards dashboard) se pintaba encima → botones no clicables. `position:sticky` crea stacking context (igual que transform/opacity<1/will-change/isolation). Fix: `Modal` → `createPortal(document.body)` + guard `mounted` SSR. Antes de portar un primitivo compartido: grep que ningún consumidor tenga `<form>` envolviendo al `<Modal>`. Ver [[modal-portal-stacking-sticky-sidebar]]

### facturaia — Admin panel CSS gotchas (2026-06-09)

- **Turbopack no convierte kebab-case → camelCase en CSS Modules** — `.kpi-grid` en CSS + `s.kpiGrid` en TSX = `undefined` silencioso, el layout desaparece sin error. Usar camelCase directo en `.module.css`. Detectar: `grep -E "^\.[a-z]+-[a-z]" *.module.css`. Ver [[css-module-camelcase-turbopack]]
- **Tokens D3 `--panel/--border/--text` no están definidos** — solo existen los alias canónicos `--bg-elev/--line/--fg`. Cualquier CSS Module que use los D3 queda transparente/sin borde/sin texto visible. Ver [[facturaia-tokens-admin-sin-definir]]

### facturaia — Design system + CSS theming (2026-06-09)

- **`--pill-*` vars con fallback = theming scoped sin tocar tokens globales** — `[data-pill-theme="pastel"]` redefine solo `--pill-*`; el UI global no cambia. Preview en la UI de settings aplica el atributo en su propio div. Ver [[css-scoped-theming-pill-vars]]
- **Playwright `filter({ has: locator })` puede timeout** — en páginas con transiciones activas o fuentes cargando, el locator filtrado por heading no resuelve; pasar a `fullPage: true` en `toHaveScreenshot`. Ver [[playwright-section-locator-filter-timeout]]
- **Baselines Playwright son OS-dependientes** — `darwin` ≠ `jammy`; para CI estable regenerar dentro del container `mcr.microsoft.com/playwright:vX-jammy`.

### Frontend mobile — marquee + iOS overlay (2026-06-02)

- **Marquee seamless** — wrapper único `w-max` animado + `loading="eager"` en imgs. Sin `w-max` el `-50%` se calcula sobre el viewport → logos desaparecen. Ver [[marquee-css-seamless-loop-w-max-eager]]
- **iOS scroll lock** — `position:fixed + top:-scrollY + width:100%`; `overflow:hidden` no funciona en Safari. Ver [[ios-safari-body-scroll-lock-position-fixed]]
- **Overlay iOS** — `h-[100dvh]` no `inset-0`; el dynamic viewport height respeta el chrome del browser. Ver [[css-fixed-overlay-100dvh-ios]]

Patrones recientes de proyectos activos. Mover a sección permanente o eliminar tras 2 semanas.

### facturaia — Observabilidad WhatsApp en /admin/ia-ops (2026-06-01)

- **Tab WhatsApp** (5º módulo IA): consumo (mensajes/tokens/coste) desde nueva `voice_usage` (mig 202), errores reales desde `bot_error_log`, invocaciones desde `voice_invocations`. n8n reporta uso por turno vía `POST /api/voice/usage` (nodo "Reportar Uso WhatsApp" en `pqSWkDIHqmSVHotB`).
- **Coste WhatsApp = estimación suelo**: el LLM corre en n8n, no expone tokens reales → se estiman del texto (chars/3.5 in, /3 out, como `estimateTokens`). Mensajes exactos. El copiloto web sí lleva tokens reales (corre en backend).
- **Tokens CSS admin sin definir** (`--panel`/`--border`/`--text`) → todo el admin plano + modal invisible. Ver [[facturaia-tokens-admin-sin-definir]].
- **`bot_error_log` no es un error log limpio**: el backfill clasifica toda ejecución n8n como `validation_error/warn` por defecto. Filtrar a severity error/fatal/critical para errores reales.

### facturaia — Pestaña Seguridad + 2FA TOTP + política org (2026-05-31, WIP sin commit)

- **Supabase MFA TOTP** — step-up obligatorio (signIn deja aal1 aunque haya factor), OAuth via middleware `/verificar-2fa`, recovery codes a mano, session timeout solo client-side. Ver [[supabase-mfa-totp-integracion-gotchas]]

### facturaia — visor PDF + modal detalle Holded (2026-05-30, PR #121)

- **Visor PDF en Next** — iframe nativo = cromo feo (barra/miniaturas/gris); usar react-pdf (pdf.js) + `next/dynamic ssr:false` (DOMMatrix en SSR). Ver [[pdfjs-en-next-iframe-nativo-vs-react-pdf-ssr-false]]
- **Pie PDF al fondo A4** — raíz flex column + `min-height:1122` + spacer `flex-grow` antes del pie. Ver [[anclar-pie-pdf-al-fondo-pagina-puppeteer-html]]
- **Smoke con agent-browser (Vercel)** — en forms React: `click` no submite (usar `form.requestSubmit()`), `fill` no dispara onChange (keyboard type / setter+input), Mac select-all `Meta+a`. Ver [[agent-browser-cdp-formularios-react-requestsubmit]]

### TuFacturaIA Fase 2.15 HMAC v2 (2026-05-30)

- **Dokploy compose pasa al container solo lo listado en YAML, no panel** — añadir env por panel sin tocar `composeFile` NO la inyecta. Editar ambos. Ver [[n8n-compose-env-vars-yaml-y-panel]]
- **n8n task-runner sandbox sin `URL` global** — `new URL()` lanza, aunque `crypto` esté permitido. Regex inline para path+search. Ver [[n8n-task-runner-sandbox-sin-url-global]]
- **n8n PUT workflow rechaza settings extra** — `callerPolicy`/`binaryMode` del GET previo dan 400. Filtrar a solo `executionOrder`. Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]]
- **Inventario auth n8n: filtrar `.code` deja fuera toolCode + HTTP** — usar `'x-service-key' in json.dumps(parameters).lower()` en todos los tipos. Ver [[n8n-inventario-auth-incluye-toolcode-y-httprequest]]
- **Stripe `subscription.deleted` por sub.id, no por kind** — handler que solo cubre `kind=fiscal_addon` ignora cancelaciones plan base → orgs en estado fantasma. Ver [[stripe-subscription-deleted-resolver-por-sub-id-no-por-kind]]
- **Stripe sub multi-item** — resolver item por price.id, no items[0]; sync quantity del add-on. Ver [[stripe-subscription-multi-item-resolver-por-price-no-indice]]

### EcoBox — voz 2ª ronda test (2026-06-02)

- **Anti-doble-booking = check overlap server-side** — el event_id determinista solo bloquea mismo phone+slot, no a otro cliente a la misma hora. GCal getAll en la ventana antes de crear. Ver [[n8n-reservar-overlap-guard-server-side-anti-doble-booking]]
- **Retell fecha sin hardcodear ni cron** — `{{current_time_Europe/Madrid}}` + `{{current_calendar_Europe/Madrid}}` (vars de sistema por llamada). Ver [[retell-current-time-y-current-calendar-dynamic-vars-evitan-fecha-hardcodeada]]
- **Retell transfer: cold vs warm + nº ≠ caller** — warm espera descuelgue+detección humano (frágil); cold reenvía directo; el nº destino no puede ser el del que llama. Ver [[retell-cold-vs-warm-transfer-y-numero-distinto-del-caller]]


### Centro Elphis — Retell v4 + n8n (2026-06-04)

- **Function node instruction = cómo construye ISO** — sin ella LLM inventa año 2024. Ver [[retell-function-node-instruction-construye-iso-params]]
- **Published flow → 400 → crear flow nuevo** — PATCH bloqueado, crear + reasignar agente. Ver [[retell-published-flow-400-crear-nuevo-y-reasignar]]
- **Map args no ignorar fechas LLM** — snap-forward, no override total. Ver [[n8n-retell-webhook-map-args-snap-forward-no-override-total]]
- **Chatwoot labels: GET + merge antes de POST** — POST reemplaza todo. Ver [[chatwoot-labels-post-replace-all-get-merge-pattern]]

### EcoBox — chat WhatsApp E2E (2026-06-01)

- **n8n tool-webhook no debe mentir** — Respond hardcodeado a éxito + nodo de acción con onError:continue = el bot confirma reservas/cancelaciones que no ocurrieron. Gatear efectos y Respond en `!$json.error`. Ver [[n8n-webhook-tool-respond-no-hardcodear-exito-gatear-en-error-nodo]]
- **Chatwoot audio → Whisper inline** — nota de voz llega con content null + audio en attachments; transcribir vía HTTP a OpenAI /v1/audio/transcriptions. Ver [[chatwoot-nota-voz-content-null-audio-en-attachments-transcribir-whisper]]
- **Edit Fields: optional chaining body.args vs body plano** — chat manda body plano, voz lo envuelve en args; `body.args.X` sin `?.` revienta → null silencioso. Aplica a TODOS los tools, no solo al primero. Ver [[n8n-edit-fields-optional-chaining-body-args-plano-vs-wrapped]]

> Entradas anteriores a 2026-05-25 podadas (viven en sus learnings). Permanentes en [[patterns-cross-proyecto]].
- **supabase-js .in() UUID col puede devolver vacío** — aunque psql+service_role funciona, el cliente JS puede no encontrar filas; mover JOIN a SQL/RPC es el fix fiable. Ver [[supabase-js-in-uuid-column-text-empty]]

- **Aliases proveedor: trigger captura rename + resolve_proveedor RPC** — OCR dedup correcto aunque usuario renombre. GIN array_ops no acelera lower+unnest (seq scan OK <1000 rows). Ver [[proveedor-aliases-ocr-dedup]]

- **Worktree facturaia: `node_modules` real para `next build` + copiar `supabase/.temp`** — symlink de node_modules vale para typecheck/vitest pero rompe el build de Turbopack; el link de Supabase no está en el worktree. Ver [[worktree-facturaia-build-supabase]]

- **backdrop-filter no renderiza con Next 16/lightningcss** si escribes `-webkit-` a mano (lo deja solo, Chrome lo ignora) → solo `backdrop-filter`; tokens de blur en `:root` base. Ver [[frontend-css-mobile]]
- **Popover con backdrop-filter dentro de un ancestro con backdrop-filter/transform sale SIN blur** (el ancestro es *backdrop root*; el descendiente solo filtra dentro de su caja → fuera, backdrop vacío). CSS correcto, problema de DOM. Fix: portar el popover a `createPortal(body)` con `position:fixed` desde el trigger (como el Modal). Caso facturaia desplegables topbar 2026-06-12. Ver [[ancestro-con-backdrop-filter-anula-blur-descendiente-portar-popover]]
- **Cron detector de drift debe usar el MISMO rango que generó el snapshot** — si el productor es acumulado (130 = YTD) y el detector compara solo el trimestre, lo previo sale como "saliente" → falsos positivos diarios, amplificados si `notify_upsert` reabre la notif como no leída. Caso facturaia PR #214 2026-06-12. Ver [[cron-drift-detector-debe-usar-mismo-rango-que-genero-el-snapshot]]
- **Subagente runaway no se mata con TaskStop** (completed cada ciclo) → aislar trabajo grande en worktree; corte = Esc del humano. Ver [[claude-code-gotchas]]
- **Subagente de diseño = receta CSS literal en el prompt** (no descripción) o inventa genérico; y agentes custom con error `thinking.type.disabled` → `model: "sonnet"`. Ver [[claude-code-gotchas]]
- **APCA gate en script Node sobre tokens.css** — umbrales por uso (90/60/30/15), muted dark a 60 no 75, texto semántico via `*-fg`. Ver [[apca-gate-script-tokens]]

### retell — outbound Simarro (2026-06-11)
- **Conversation Flow: LLM alucina args de tool** (teléfono inexistente en el flow), **stall de promesas** ("dame un momento" sin transitar) e **IDs fijados a dynamic var** que rompen la selección → reglas literales "EXACTAMENTE {{var}}" + edge directo a la tool + "el de la elegida". Naturalidad: empatía enlatada = delator nº1; turbo_v2_5 robótica en ES → multilingual_v2 temp 1.1. Outbound: no re-ofrecer lo descartado, preguntar motivo y pivotar a matching. Ver [[conversation-flow-outbound-gotchas]]
- **Clientify GET /v1/deals/?contact=ID no filtra** → devuelve todo el pipeline; filtrar con `.endsWith('/contact_id/')`. Ver [[clientify]]
- **Playwright `page.request` respeta caché HTTP del browser** — endpoint 200 sin `Cache-Control: no-store` → lecturas stale tras mutación; cache-buster en test + header en el endpoint. Ver [[playwright-page-request-respeta-cache-http-del-browser]]
- **Editor/sesión paralela revierte tus edits en disco → stagea al ÍNDICE con `git apply --cached`** y commitea desde ahí; excluye hunks ajenos con patch parcial. Ver [[claude-code-gotchas]]
