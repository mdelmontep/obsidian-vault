---
title: hot cache
date: 2026-05-07
tags: [stack, index]
---

# Hot Cache

Resúmenes 1-2 líneas con link al learning. Leer learning completo solo si necesario.

> Patrones permanentes cross-proyecto movidos a [[patterns-cross-proyecto]] (poda 2026-06-02).

## 🔥 Últimas 2 semanas

### facturaia — Admin panel CSS gotchas (2026-06-09)

- **Turbopack no convierte kebab-case → camelCase en CSS Modules** — `.kpi-grid` en CSS + `s.kpiGrid` en TSX = `undefined` silencioso, el layout desaparece sin error. Usar camelCase directo en `.module.css`. Detectar: `grep -E "^\.[a-z]+-[a-z]" *.module.css`. Ver [[css-module-camelcase-turbopack]]
- **Tokens D3 `--panel/--border/--text` no están definidos** — solo existen los alias canónicos `--bg-elev/--line/--fg`. Cualquier CSS Module que use los D3 queda transparente/sin borde/sin texto visible. Ver [[facturaia-tokens-admin-sin-definir]]

### facturaia — Design system + CSS theming (2026-06-09)

- **`--pill-*` vars con fallback = theming scoped sin tocar tokens globales** — `[data-pill-theme="pastel"]` redefine solo `--pill-*`; el UI global no cambia. Preview en la UI de settings aplica el atributo en su propio div. Ver [[css-scoped-theming-pill-vars]]
- **Playwright `filter({ has: locator })` puede timeout** — en páginas con transiciones activas o fuentes cargando, el locator filtrado por heading no resuelve; pasar a `fullPage: true` en `toHaveScreenshot`. Ver [[playwright-section-locator-filter-timeout]]
- **Baselines Playwright son OS-dependientes** — `darwin` ≠ `jammy`; para CI estable regenerar dentro del container `mcr.microsoft.com/playwright:vX-jammy`.

### Postgres — contador serie + INSERT = misma TX (2026-06-08)

- **Split-TX quema números de serie** — `next_invoice_number_for_org` en TX1, INSERT en TX2: si TX2 falla el contador ya commitió → hueco. Fix: `SELECT FOR UPDATE` + `UPDATE contador` + INSERT dentro del mismo RPC. Ver [[postgres-split-tx-counter-burn-serie-numeracion]]

### Multiempresa SaaS — 3 ejes (2026-06-05)

- **Navegar=membresía · agregar=propiedad · cobrar=cuenta** — no mezclar: agregar por membresía cruda suma datos de clientes que gestionas (bug + RGPD). Ver [[multiempresa-saas-tres-ejes-navegar-agregar-cobrar]] · [[ADR-028-multiempresa-scope-navegar-agregar-cobrar]]

### Seguridad — SSRF pinning de IP (2026-06-05)

- **Validar la IP no basta sin pinar el fetch** — fetch por hostname re-resuelve DNS (rebinding TOCTOU); pinear con undici Agent `connect.lookup` a la IP validada, manteniendo hostname para SNI. Ver [[ssrf-validar-dns-no-cierra-rebinding-sin-pinar-ip]]

### Git / CI — gotchas (2026-06-05)

- **rebase --onto sobre upstream movido suelta tu commit** — "Successfully rebased" miente; verifica `git log origin/main..HEAD` antes de push, recupera con reflog+cherry-pick. Ver [[git-rebase-onto-upstream-movido-suelta-commit-reflog-recupera]]
- **build no corre vitest** — registry/enum con test de conteo rompe en CI al añadir entrada; corre `npx vitest run` antes de push. Ver [[pre-commit-build-no-corre-tests-registry-conteo-rompe-ci]]

### OCR — consumidor lee claves fantasma (2026-06-05)

- **Consumidor lee claves que el productor no emite** — JSONB sin tipo compartido = falla silenciosa + tests verdes si prueban el shape equivocado. Ver [[consumidor-lee-claves-que-productor-no-emite]]

### Email/BD — enum código sin CHECK (2026-06-04)

- **Enum nuevo en código sin ampliar el CHECK de BD = insert muere mudo** — outbox-first aborta el envío entero (recover-password no enviaba a NADIE); el 200 anti-enum del endpoint lo oculta. Ver [[enum-nuevo-en-codigo-sin-ampliar-check-bd-rompe-insert-silencioso]]

### Seguridad Supabase — RPC grants (2026-06-04)

- **RPC SECURITY DEFINER = ejecutable por anon vía PostgREST** si no revocas: Postgres concede EXECUTE a PUBLIC por defecto → anon/authenticated invocables con el anon key público. Bypass de pago/IDOR si reciben org_id sin validar. Fix: REVOKE FROM PUBLIC, anon. Ver [[supabase-rpc-security-definer-execute-public]]

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

### EcoBox / Retell voz E2E (2026-05-25/26)

- **n8n `require('crypto')` bloqueado en task-runner** — Code node falla "Module disallowed". Hash puro JS FNV-1a × 3 seeds, charset `[0-9a-v]` válido GCal eventId. Ver [[n8n-crypto-module-bloqueado-task-runner-usar-fnv-puro]]
- **n8n public API no permite UPDATE credentials** — solo POST/DELETE. Recrear + repuntar workflows que la usan. Ver [[n8n-public-api-no-permite-update-credentials-recrear-y-repuntar]]
- **n8n respondToWebhook JSON expression** — `={ ... }` rompe "Invalid JSON". Sintaxis `={{ ({ key: val }) }}` con paréntesis. Ver [[n8n-respondtoWebhook-json-formato-expresion-objeto]]
- **n8n GCal getAll vacío no propaga** — calendar sin eventos rompe Code downstream. `alwaysOutputData: true` + filter `.filter(e => e.json?.start)`. Ver [[n8n-gcal-getall-empty-no-propaga-downstream]]
- **n8n GCal description `\\n` → literal** — almacenado doble-escaped, llega literal a Calendar UI. Usar `\n` single backslash. Ver [[n8n-gcal-additionalFields-newlines-no-double-escape]]
- **n8n emailSend onError continueRegularOutput** — skip si recipiente vacío sin romper workflow. Para campos opcionales tipo email cliente. Ver [[n8n-emailsend-onerror-continue-skip-sin-destinatario]]
- **Retell `{{from_number}}` NO auto-sustituye en tool args** — Retell + Zadarma SIP no rellena la dynamic var; LLM pasa el literal. Fallback en backend `body.call.from_number`. Ver [[retell-from_number-no-auto-sustituye-en-tool-args]]
- **Retell custom voice label ≠ audio real** — "Borja - Clever and Credible" sonaba femenina (mis-mapped underlying ElevenLabs). Verificar preview MP3 antes de confiar. Ver [[retell-custom-voice-label-no-garantiza-audio-real]]
- **Retell `tool_call_strict_mode` NO fuerza ejecutar tool** — solo valida args. Para forzar uso = prompt OBLIGATORIO + transition_condition que exija output del tool. Ver [[retell-tool-call-strict-mode-no-fuerza-ejecutar-solo-valida-args]]
- **LLM voz inventa fecha si no la sabe** — gpt-4o → año 2024 sin contexto temporal. `retell_llm_dynamic_variables.fecha_hoy` + global_prompt + guard backend año fuera de rango. Ver [[llm-current-date-debe-inyectarse-explicito-evita-alucinar-anyo]]
- **Retell boosted_keywords letras españolas** — "zeta, efe, eñe, doble uve, hache" + dígitos mejora STT al deletrear matrículas/emails. Ver [[retell-boosted-keywords-letras-españolas-stt]]
- **Chatwoot `/contacts/search` no autorizado para bot token** — "Access not authorized for bots". Admin cred o buscar en sistema source. Ver [[chatwoot-search-contact-api-requires-admin-token-no-bot]]
- **GCal q-search no fiable post-create** — eventual consistency. Delete by `event_id` determinista (devuelto por Buscar) en vez de search-by-phone. Ver [[gcal-q-search-no-encuentra-recien-creados-usar-event_id-deterministic]]
- **GCal eventId charset `[a-v0-9]`** — base32hex subset, 5-1024 chars. Hash FNV → `.toString(32)` válido directo. Ver [[gcal-eventid-charset-restriction-a-v0-9-base32hex]]
- **Retell subagent default = transfer** — sin instrucción "NO transfieras en CASO X" el LLM deriva al humano al recoger datos. Default semántico inseguro. Ver [[retell-subagent-default-transfer-debe-bloquearse-explicito-por-caso]]

### facturaia — Cashflow chart unificado (2026-05-26)

- **Toggle entre vistas relacionadas = síntoma UX** — antes de añadir toggle, preguntarse si las dos vistas son lectura única. Ver [[toggle-vistas-relacionadas-es-sintoma-mal-diseno-ux]]
- **Dos escalas en un chart → bandas verticales** — saldo arriba + flujo abajo estilo TradingView volume, nunca dual-axis. Ver [[dataviz-dos-escalas-bandas-verticales-no-dual-axis]]

### agency-portal — Prefill server→client form (2026-05-25)

- **Prefill server→client form** — page.tsx carga detalle entero pero pasa subset al form → campos opcionales (fiscal, dirección, teléfono) salen vacíos. Caso PR #73 factura nueva. Revisar mismo patrón en `/agency/quotes/new` y `/agency/contracts/new`. Ver [[agency-portal-forms-prefill]]

### facturaia — Sprint email Nivel 1+2 + UX form + /emitidas (2026-05-25 noche)
- **Pipeline asset con fallback debe devolver razón** — `Buffer|null` pierde causa (404/sign expired/puppeteer crash). Patrón `{ buffer, diag: { reason, http_status, error } }` + log + warning visible al user. Ver [[pdf-fallback-pipeline-devolver-razon-no-null]]
- **XSS en email se subestima** — Gmail web/Outlook.com renderizan HTML parser completo. TODO valor BD interpolado pasa por `escapeHtml`. Allowlist protocolo en `escapeUrl`. Ver [[xss-en-email-html-interpolado-de-bd]]
- **HTML strings tipados ganan a React Email/MJML para 5-10 templates** — 250KB deps no se justifica, control byte-a-byte cross-client (Outlook MSO, dark mode, tablas). Umbral cambio: 30+ templates. Ver [[html-email-strings-tipados-vs-react-email-mjml]] + [[ADR-021-html-email-strings-vs-react-email-mjml]]
- **UX duplicación filtros estado vs tipo doc** — si un valor del enum estado aparece como chip Y como tab tipo doc → simplificar. Backend dice qué es realmente. Ver [[ux-duplicacion-filtros-estado-vs-tipo-doc]]
- **createObjectURL en React sin revoke = memory leak silencioso** — patrón cleanup: setter functional revoke prev + closeHandler revoke + useEffect return revoke en unmount. Ver [[blob-url-cleanup-revokeobjecturl-react]]

### facturaia — Source-of-truth + RLS multi-org + IRPF perfil-driven (2026-05-25)
- **Artifacts emitidos no se regeneran al cambiar dato fuente** — PDF de factura ya emitida conserva el logo viejo. Pattern aplica a emails enviados, SSG, thumbnails, PDFs firmados. Ofrecer botón regenerar. Ver [[cache-invalidation-artifacts-emitidos]]
- **Triggers BD de sincronización = anti-patrón** — 6 razones (silent fail, race, recursión, audit ciego, code review ciego, mig masiva). Sync explícito en código. Ver [[triggers-bd-sync-son-antipatron]] + [[ADR-020-source-of-truth-datos-emisor-template-config-vs-columnas]]
- **NUMERIC(X,2) drift bruto↔neto IVA** — 10€ bruto IVA 21% → guarda 8.26 → reconstruye 9.99. Necesita NUMERIC(14,6) o redondeo desde total bruto. Ver [[numeric-precision-drift-bruto-neto-iva]]
- **RPC CREATE OR REPLACE firma idéntica obligatoria** — distinta deja función huérfana, callers fallan. PL/pgSQL lazy compile. Ver [[postgres-rpc-firma-identica-create-replace]]
- **RLS multi-org `get_user_org_id()` no `IN (SELECT org_members)`** — el segundo permite leer de TODAS las orgs del user, no solo la activa. Caso real: 16 tablas TuFacturaIA fixeadas en mig 163. Ver [[rls-multi-org-active-vs-membership]]


> Entradas anteriores a 2026-05-25 podadas (viven en sus learnings). Permanentes en [[patterns-cross-proyecto]].
