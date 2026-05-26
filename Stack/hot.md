---
title: hot cache
date: 2026-05-07
tags: [stack, index]
---

# Hot Cache

Resúmenes 1-2 líneas con link al learning. Leer learning completo solo si necesario.

## ⭐ Permanentes (cross-proyecto)

- **ETag por path + upsert mutable** — 304 indefinido tras regen blob. ETag fuerte = hash del buffer + `no-cache`. Ver [[etag-por-path-upsert-stale-304]]
- **PDF adjunto email** — congelado en inbox cliente; reenviar para refrescar. Link = siempre actualizado. Ver [[pdf-adjunto-email-vs-link-frozen-blob]]
- **Retell Flex vs Rigid coste** — Flex compila TODO (nodos+KB+tools), token-scaling x2-5 si >3500 tokens. Rigid + gpt-4.1 sin high_priority = €0.135/min. Default Rigid. Ver [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
- **Calendar idempotency sha1(phone+slot)** — eventId determinista pasado al create. Si ya existe → 409 nativo, no duplica. Sin estado externo. Ver [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]
- **PR externa sobre modelo sunsetado** — portar al modelo nuevo antes de mergear, no después. Caso: PR76 iCloud sobre settings.email → PR77 sobre plataforma. Ver [[pr-externa-sobre-modelo-sunsetado-portar-no-mergear]]
- **IMAP attachment selectivo** — bodyStructure → download(partId), no client.download(uid) completo. Evita OOM proporcional al RFC822. Ver [[imap-attachment-selectivo-bodystructure-evita-oom]]
- **n8n toolCode post-`$fromAI`** — `specifyInputSchema: true + schemaType:'manual' + inputSchema` JSON Schema obliga al LLM a mandar JSON en `query`. Sin schema, el LLM envía texto crudo. Ver [[$fromAI-en-toolCode-lanza-no-execution-data-available-en-n8n-2.15.x]]

Patrones que aplican siempre, no expiran. Lo más reusado.

- **LLM tool-use con cards visuales** — instruir explícito en system prompt a NO duplicar la lista del card en texto. Ver [[llm-tool-use-card-visual-instruir-no-duplicar-lista]]
- **LLM safety-critical = 1 tool, no cascada** — bajo presión el LLM puede invertir el orden de 2 tools. Side-effects al post-evento. Ver [[llm-safety-critical-un-tool-no-cascada-de-tools]]
- **Retell transfer_call built-in es el único que transfiere SIP** — custom function solo pasa datos al LLM, la línea sigue activa. Ver [[retell-transfer-call-builtin-vs-custom-function-para-sip]]
- **n8n executeWorkflowTrigger filtra campos no declarados** — añadir `dry_run`/nuevos campos al `workflowInputs.values` del trigger en TODOS los sub-workflows. Ver [[n8n-executeworkflowtrigger-schema-estricto-filtra-campos]]
- **Whitelist ≠ dry-run** — añadir flag explícito `dry_run:true` con cortocircuito a IDs sintéticos si quieres seguridad en smokes. Ver [[whitelist-no-es-dry-run-añadir-flag-explicito]]
- **Next.js 16 = `proxy.ts` no `middleware.ts`** — NO revertir el rename. `middleware.ts` solo sigue por backcompat con warning. Ver [[nextjs16-middleware-to-proxy]]
- **Cookie impersonación pegada ≠ middleware caído** — primero override-vs-union en `resolveAllowedOrgIds`, después middleware. Ver [[nextjs16-impersonation-cookie-stuck-no-implica-middleware-off]]
- **extractError objeto anidado** — `String(body.error)` colapsa a `[object Object]`. APIs modernas devuelven `{error:{message,...}}`. Ver [[extract-error-objeto-anidado-en-apis-modernas]]
- **openapi-fetch revienta con binarios** — fuerza JSON aunque el endpoint devuelva PDF. Bypass con `fetch` nativo + Content-Type negotiation. Ver [[openapi-fetch-parsea-todo-como-json-incluido-binarios]]
- **Supabase RLS olvidado** — policies sin ENABLE RLS = tabla pública, alerta 24-48h tarde. Toda tabla nueva = ENABLE en la misma migración. Ver [[supabase-enable-rls-olvidado-tabla-publica]]
- **NOT NULL post-backfill misma migration** — ADD nullable → UPDATE → SET NOT NULL en una transacción. Ver [[migration-add-column-backfill-not-null-misma-transaccion]]
- **PostgREST schema reload** — `NOTIFY pgrst, 'reload schema';` al final de migration con columna nueva. Ver [[postgrest-schema-cache-notify-tras-migration]]
- **Webhook idempotency transient** — borrar `event_id` log en 5xx/timeout para que el retry no sea replay falso. Ver [[webhook-idempotency-borrar-log-en-errores-transitorios]]
- **UPSERT sombra por remote_id** — múltiples paths convergen sin duplicar. Ver [[upsert-sombra-por-id-remoto-no-por-id-local]]
- **Signed URL proxy** — endpoint que regenera on-demand, no cachear URL firmada en BD. Ver [[signed-url-proxy-endpoint-vs-cached-en-bd]]
- **Signed URL fetch server-side ≠ href de email** — la URL corta (60s) para descargar PDF y adjuntarlo NO vale como CTA del email. Firmar 2 URLs separadas. Ver [[signed-url-corta-fetch-interno-no-reusar-en-email]]
- **Security API routes** — checklist (auth + rate limit + whitelist + magic bytes + timingSafeEqual + path traversal). Ver [[checklist-seguridad-api-routes-nextjs]]
- **RLS multi-tenant** — `get_user_org_id()` SECURITY DEFINER, falla con service_role. Ver [[rls-multi-tenant-supabase-con-security-definer]]
- **Re-auth password admin** — campos disabled + modal password + `signInWithPassword` para acciones sensibles. Ver [[re-autenticacion-con-password-para-acciones-sensibles-admin]]
- **PGRST203 RPC overloads** — pasar TODOS los named params, no solo los del overload viejo. Ver [[postgrest-pgrst203-rpc-overloads-pasar-todos-los-params]]
- **Cloudflare WAF + ilike** — patrones SQL inj en URL Supabase devuelven HTML → endpoint 500 (defensa OK). Ver [[cloudflare-waf-bloquea-sql-patterns-en-query-params-supabase]]
- **AI Agent contrato real antes de modificar** — leer system prompt + tools vía API; JSON-out vs conversational es contrato distinto. Ver [[leer-system-prompt-y-tools-actuales-antes-de-modificar-ai-agent]]
- **useEffectEvent NO desde setTimeout** — patrón debounce reactivo va con useCallback + deps. Ver [[useeffectevent-react19-no-se-llama-desde-settimeout]]
- **LLM ambiguity con voz** — devolver lista numerada de candidatos + memoria conversacional, nunca "dime el número exacto". Ver [[llm-ambiguity-lista-candidatos-numerados-y-memoria-conversacional]]
- **LLM tool-use multi-turno replay** — persistir calls+results juntos OK, pero emit role:'tool' por call_id en orden; skip huérfanos. Ver [[llm-tool-use-multi-turno-replay-tool-calls-y-results-emparejados]]
- **Tipo nuevo en agente JSON-out** — parchear downstream o lookup recurso real (mejor lookup). Ver [[extender-tipo-en-agente-json-out-parchear-downstream-o-lookup-recurso]]
- **Verificar persistencia post-PUT** — HTTP 200 ≠ aplicó. Grep marker único en re-fetch. Ver [[verificar-persistencia-tras-put-api-con-grep-marker-unico]]
- **Métricas tabla + events** — diseñar con tabla de dominio como fuente primaria, events como complemento. Ver [[metricas-fuente-fuerte-mas-event-log]]
- **Parser ES vs HTML input number** — input type=number siempre punto US como decimal; parser ES naïve rompe '33.33' → '3333' (×100 silencioso). Ver [[parser-numero-es-bug-con-input-html5-number-punto-como-decimal-no-millares]]
- **State string para inputs numéricos** — `value={0}` ancla cursor + bloquea edición de "0"; state string + parseo lazy + onFocus.select() + step="any" = UX Holded. Ver [[react-state-string-vs-number-para-inputs-numericos]]
- **Toggle UX-only sin contaminar storage canónico** — apps fiscales: flag a sessionStorage por documento, storage siempre canónico (base imponible). Ver [[toggle-ux-only-no-contamina-storage-canonico-fiscal]] + [[ADR-019-precio-inclusive-iva-storage-canonico-vs-columna-precio-modo]]
- **Impersonate por query** — `?org_id=` + isSuperadmin check, no fiar cookie (middleware la borra). Ver [[endpoints-impersonate-por-query-no-cookie]]
- **Cron Dokploy** — Command = solo `curl -sf -X POST URL -H "x-service-key: $VAR"` + Shell dropdown = bash. NO añadir `bash -c` (doble wrap rompe args). Ver [[cron-dokploy-curl-service-key]]
- **Form defaults schema** — `value !== undefined ? value : default`. Nunca `!!value` ni `value || default`. Ver [[form-defaults-respetar-schema-no-bang-bang-config]]
- **Overlays sobre cards** — `--bg-elev2` no `--panel`, sombra doble + `isolation: isolate`. Ver [[overlays-sobre-cards-usar-bg-elev2-no-panel]]
- **BEFORE INSERT + ON CONFLICT** — trigger cuenta fila fantasma que ON CONFLICT iba a descartar. Skip si EXISTS activo con misma clave. Ver [[trigger-before-insert-on-conflict-do-nothing-cuenta-fila-fantasma]]
- **Cron queue top-N+filter-JS** — anti-pattern: nunca procesa antiguos. SQL `NOT EXISTS` o RPC pendientes. Ver [[cron-queue-top-n-by-date-filter-js-no-procesa-antiguos]]
- **c68 IVA = regularización anual, NO deducibles** — bug clásico fórmula 303 infla c69 x2 en AIB intracom. Ver [[iva-modelo-303-c68-es-regularizacion-anual-no-deducibles]]
- **AIB excluido régimen anticipos LIVA 75.Dos** — fecha_devengo AIB ignora fecha_cobro_anticipo. Ver [[aib-intracom-excluido-regimen-anticipos-liva-75-dos]]
- **DT 18ª vivienda doble condición** — pre-2013 + rdto previo <33.007,20€/año (NO solo pre-2013). Ver [[irpf-dt-18-vivienda-habitual-doble-condicion]]
- **Verifactu APLAZADO a 2027** — IS 01-ene-2027, IRPF/IRNR-EP 01-jul-2027 (RDL 15/2025). Ver [[verifactu-aplazado-2027-rdl-15-2025]]
- **Focus trap modal cicla Tab** — WCAG 2.1.2 en modals: foco NO escapa, Escape SÍ sale. Ver [[wcag-2-1-2-no-keyboard-trap-vs-modal-focus-trap]]
- **supabase db push falla por histórico desincronizado** — workaround: db query -f + migration repair selectivo. Ver [[supabase-cli-db-push-fail-por-historico-desincronizado-workaround]]
- **Dokploy schedule.list expone env completo del compose** — secrets en plano. API key Dokploy = master key. Ver [[dokploy-api-get-schedule-list-expone-env-completo-secrets]]
- **Dokploy schedule.update NO es PATCH parcial** — payload completo obligatorio (re-send pattern). Ver [[dokploy-api-schedule-update-requiere-payload-completo-no-patch]]
- **Dokploy compose.update SÍ admite parcial** — contradicción vs schedule.update. Probar por endpoint. Ver [[dokploy-api-compose-update-admite-payload-parcial-vs-schedule-update-no]]
- **Backblaze Computer Backup ≠ B2 Cloud Storage** — productos separados, paneles distintos, B2 exige 2FA. Ver [[backblaze-computer-backup-vs-b2-cloud-storage-productos-distintos]]
- **Skip validación solo INSERT** — UPDATE puede setear flag bypass. `IF TG_OP = 'INSERT' AND ...`. Ver [[skip-validacion-solo-en-insert-no-update-evita-vector-evasion]]
- **EXCEPTION WHEN OTHERS** atrapa check_violation → 500 opaco. Discriminar SQLSTATE + pattern SQLERRM. Ver [[exception-when-others-colapsa-check-violation-discriminable]]
- **pg_trigger_depth() > 1 SKIP** — rompe loops cascade sin flag de sesión. Aplicar a TODA la cadena. Ver [[pg-trigger-depth-1-skip-rompe-loops-cascade]]
- **3 agentes paralelos auditoría** — security/backend/frontend simultáneos antes de cambios grandes, ~50% falsos positivos esperados. Ver [[3-agentes-paralelos-auditoria-cambios-grandes]]
- **Migrations por módulo** — si commits van por módulo, migrations separadas (`060_ocr_*`, `061_concilia_*`). Ver [[migrations-por-modulo-si-commits-van-por-modulo]]
- **React 19 derived state** — state mirror durante render evita setState en useEffect (lint bloquea). Ver [[react-19-strict-bloquea-setstate-en-useeffect]]
- **Zod ↔ OpenAPI doc** — refine de Zod no llega a clientes openapi-typescript. Tocar `openapi.json` en el mismo commit. Ver [[zod-vs-openapi-doc-contrato-real-de-clientes-generados]]
- **ARIA radiogroup vs aria-pressed** — selección exclusiva (segmented control, filter chips) es radiogroup+radio APG, no toggles aria-pressed. Ver [[aria-pressed-vs-radiogroup-seleccion-exclusiva]]
- **Scroll shadows dark mode** — `--scroll-shadow` var + override `:root[data-theme="dark"]`, rgba negro hardcoded invisible en oscuro. Ver [[scroll-shadows-komarov-con-css-variable-dark-mode]]
- **color-mix() para sombras tematizables** — `color-mix(in srgb, var(--brand) 25%, transparent)` reemplaza rgba hardcoded sin token `--brand-rgb` aparte. Ver [[color-mix-in-srgb-para-sombras-tematizables]]
- **PR review stale** — el reviewer puede haber pusheado fixes propios. `git log origin/<rama> -5` antes de actuar. Ver [[pr-review-ya-resuelta-por-el-reviewer-mismo]]
- **Enum fiscal hardcoded en UI** — botón hardcodea R5 = falsifica motivos R1-R5 en Verifactu. Modal select obligatorio. Ver [[enum-legal-hardcodeado-en-ui-falsifica-motivos]]
- **Estado fiscal con sombra externa** — cuando hay shadow emitida, acciones de estado van vía sistema externo, no local. Ver [[acciones-de-estado-fiscal-vs-sombra-en-sistema-externo]]
- **Validar input antes de RPC atómico** — validación post-RPC que falla quema contador atómico y deja hueco no recuperable (fiscal AEAT). Orden: input → reads-que-niegan → RPC → INSERT. Ver [[validar-input-antes-de-rpc-atomico-e-insert]]
- **Mock Supabase fail-fast** — terminales sin respuesta devuelven error explícito, no `{data:null,error:null}`. Fuerza encolar en orden, evita falsos positivos. Ver [[mock-supabase-fail-fast-default-en-tests-vitest]]
- **Defensa en código vs prompt LLM** — invariantes de dominio (precio>0, NIF presente) NO se defienden con regla del prompt; el LLM se las salta. Validar en code node downstream y devolver conversacional. Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]]
- **n8n Set node output ≠ input** — expressions usan `$json.X` del input pero el output solo lleva assignments. Si downstream necesita X, añadir assignment. Ver [[n8n-set-node-output-solo-lleva-assignments-explicitos]]
- **n8n $json post-HTTP es la respuesta, no el item** — tras httpRequest, $json downstream es la response. Para el item upstream usar `$('NodeName').first().json.X`. Ver [[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]]
- **NIF España paraguas DNI/NIE/CIF** — desde RD 1065/2007 unificado bajo "NIF"; aceptar 3 algoritmos bajo misma función. Ver [[nif-espana-paraguas-dni-nie-cif-desde-rd-1065-2007]]
- **WhatsApp Interactive List límites** — max 10 rows, title 24, button 20, id 200 (patrón `tipo:UUID` + regex switch). Ver [[whatsapp-interactive-list-limites-y-row-id-pattern]]

## 🔥 Últimas 2 semanas

Patrones recientes de proyectos activos. Mover a sección permanente o eliminar tras 2 semanas.

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

### smoke / supabase (2026-05-22)
- **PostgREST hint revela signature RPC** — probe con args incompletos → 404 con hint enumera params reales. Verifica mig aplicada sin psql. Ver [[postgrest-rpc-hint-revela-signature-aplicada-en-prod]]
- **CHECK constraint: validar invariante con REST count=0** — query con la NEGACIÓN del invariante + `count=exact` + `Range: 0-0`. Sin tocar filas reales. Ver [[verificar-check-constraint-sin-tocar-prod-con-count-exacto-rest]]

### meta-ops (2026-05-21)
- **GitHub Actions free tier engaña** — "payments have failed" es "se agotaron los 2000 min/mes", no cobro fallido. Ver [[github-actions-org-private-free-tier-2000-min]]
- **Dokploy deploya pese a CI rojo** — webhook independiente de Actions. Ver [[dokploy-webhook-independiente-del-ci-status]]

### facturaia — Conciliación hardening audit (2026-05-21 tarde, PR #65/#66/#67/#69/#70)
- **Helper SQL con chain triggers: setear guard ANTES del UPDATE source** — sin orden correcto, chain loop infinito + bug fiscal reentra. Ver [[helper-sql-orden-last-revert-at-antes-de-update-mfa]]
- **fmtDate(null) tumba página entera React** — formatters compartidos requieren guard null defensivo desde día 1. Ver [[fmtdate-null-tumba-pagina-entera-react]]
- **Audit feed nueva source requiere shape snapshot/diff** — sin snapshot, columna detalle queda vacía → promesa "queda en auditoría" rota. Ver [[audit-feed-multi-source-snapshot-vs-diff-shape]]
- **PG RETURNS TABLE con SELECT INTO → prefijo out_** — evita ambiguity + alinear archivo migración con prod tras hotfix. Ver [[pg-returns-table-prefijo-out-para-evitar-ambiguity]]
- **4 agentes paralelos en worktrees + cherry-pick combinado a 1 PR** — verificar scope archivo-disjoint ANTES de delegar. Ver [[cherry-pick-4-worktrees-agentes-paralelos]]

### facturaia — Phase 1 bot multi-org (2026-05-21)
- **`n8n_chat_histories` vive en Postgres local n8n, no en Supabase** — gotcha smoke + limpieza memoria LLM. Ver [[n8n-chat-histories-en-postgres-local-no-supabase]]
- **Smoke multi-org WhatsApp limpia 3 tablas + no abrir web** — sticky/active_org_id/n8n_chat_histories. Ver [[smoke-multi-org-whatsapp-clean-state]]

### facturaia — Multi-org real + Equipo + Bot WhatsApp (2026-05-20, PRs #54-#63)
- **`.limit(1)` sin ORDER BY en multi-tenant = bug latente** — patrón canónico Postgres/Supabase. Ver [[rls-multi-tenant-limit-1-sin-order-bug-latente]]
- **Supabase `signOut` solo invalida refresh, NO access JWT** — access vive ~1h tras signOut. Necesita fallback `/sin-acceso`. Ver [[signOut-solo-invalida-refresh-no-access-token]] + [[ADR-007-sin-acceso-fallback-vs-loop-redirect]]
- **Matriz permisos rol-aware: SQL `user_can_write_in_org` + espejo TS `role-matrix.ts`** — single source of truth, defense-in-depth real. Ver [[matriz-permisos-rol-aware-bd-mas-espejo-ts]] + [[ADR-008-matriz-permisos-rol-aware-bd]]
- **`createUser` + trigger `handle_new_user` race** — orden estricto + rollback `deleteUser` ante fallo email. Ver [[supabase-createuser-race-trigger-handle-new-user]]
- **Audits per-PR pasan pero cross-PR detecta bugs por composición** — patrón de process para subsistemas con 4+ PRs encadenados. Ver [[audits-cross-pr-vs-per-pr]]

### facturaia — Modelo invitación consent-explícito (2026-05-21)
- **Toda invitación = `estado='invitado'` + accept endpoint** — modelo SaaS multi-org estándar. Ver [[ADR-009-invitacion-consent-explicito-vs-activo-directo]]
- **Trigger `handle_new_user` con rama legacy choca con INSERT explícito** — duplicate key UNIQUE. Auditar triggers al cambiar modelo. Ver [[trigger-handle_new_user-rama-legacy-choca-con-insert-explicito]]
- **Cookie de scope estrecho (impersonate) leak fuera de su path** — `request.cookies.delete()` ANTES del handler, no solo response. Ver [[cookie-impersonate-leak-fuera-de-admin]]
- **Hash del magic link Supabase requiere `setSession` explícito** — `getUser()` antes devuelve null. Ver [[hash-magic-link-supabase-requiere-setsession-explicito]]
- **RLS `org_members_select` debe OR `user_id = auth.uid()`** — sin esto, invitado no puede leer su propia fila pending. Ver [[rls-org-members-select-debe-incluir-own-memberships]]
- **`useSearchParams` requiere Suspense en Next.js 15+ prerender** — wrapping pattern estándar. Ver [[usesearchparams-requiere-suspense-en-next15-prerender]]
- **`NEXT_PUBLIC_*` Dokploy no siempre propagan al runtime** — fallback con headers `x-forwarded-host`. Ver [[next-public-envs-dokploy-runtime-fallback-headers]]

### supabase CLI (2026-05-20)
- **Migration con prefijo no-numérico (`107b`) se skipea silente** — el SQL nunca corre en fresh setup. Renombrar a número >max actual, NO usar prefijos parecidos al existente (`1071` rompe parser). Ver [[supabase-cli-skipea-migrations-con-prefijo-no-puramente-numerico]]
- **Postgres `CREATE OR REPLACE FUNCTION` no toca overloads con signature distinta** — refactor de firma deja la vieja huérfana. DROP explícito en la misma migración + assert post-drop. Ver [[create-or-replace-function-no-toca-overloads-distinta-signature]]

### facturaia — descripcion en líneas API v1 (2026-05-20, PR #49)
- **Verifactu huella NO incluye conceptos/descripciones** — solo NIF+Num+Fecha+TipoFactura+CuotaTotal+ImporteTotal+Huella_ant (mig 091:122-128). Añadir/quitar campos textuales a `lineas_factura` es seguro retroactivamente, no rompe cadena AEAT.
- **`.strict()` Zod rechaza con 400, no ignora** — si un integrador externo afirma "vuestra API tolera campo extra", grep el schema antes de creerle. Caso real: Borja decía ignorar, devolvía `400 unrecognized_keys`. Ver [[verificar-comportamiento-real-api-antes-de-creer-al-integrador]].
- **Recrear RPC entero al añadir campo a INSERT con columnas explícitas** — `CREATE OR REPLACE` reemplaza la función completa, no parchea. Copiar versión vigente byte-a-byte + insertar campo nuevo.

### facturaia — Conciliación F4 reembolso + audit 4 agentes (2026-05-20)
- **Guard per-transición no persiste si otro trigger re-UPDATEa** — `IF OLD.estado='X' AND NEW='Y'` falla cuando recompute chain hace otro UPDATE con OLD ya='Y'. Fix: columna timestamp `last_revert_at` + filtro `< NOW() - INTERVAL '30d'`. Mig 128. Ver [[postgres-guard-transition-no-persiste-en-recompute-chain]]
- **Smoke fixtures en repo, no en ~/Desktop** — `docs/runbooks/smokes/<área>/` con CSV/SQL/README. Entre sesiones Claude `~/Desktop` se evapora. Ver [[smoke-fixtures-en-repo-no-en-desktop]]
- **Trigger recursivo cuando revertir estado deja "candidato libre"** — revertir factura a pendiente liberó el +100€ original que otro trigger inmediatamente re-matcheó → stack overflow. Fix: marcar candidato como neutralizado (`devolucion_de_movimiento_id`) ANTES del UPDATE estado + predicado `NOT EXISTS` en trigger competidor. `pg_trigger_depth()` solo cura síntoma. Ver [[trigger-recursivo-revertir-estado-deja-candidato-libre-que-otro-trigger-rematchea]]
- **CREATE FUNCTION es lazy** — referencias a columnas no se validan en CREATE; binding deferred a runtime. `information_schema.columns` ANTES de reescribir trigger. Ver [[postgres-asumir-columna-existente-en-trigger-rewrite-verifica-information-schema]]
- **fecha_cobro/fecha_pago = mb.fecha NUNCA CURRENT_DATE** — criterio caja AEAT IVA exige fecha del movimiento, no de la inserción del registro. Mig 111 fix retroactivo a 4 triggers.
- **UI lista no filtraba `deleted_at`** — comentario decía "defensivo por mig 106 no aplicada", llevaba semanas aplicada. Coste: movs soft-deleted seguían apareciendo. Auditar comentarios "defensivos" caducados al deployar la mig que cubren.
- **CSV import `imported:0` con error oculto en UI** — log warn en endpoint cuando `parsed.movimientos.length === 0` o errors no vacíos. UI muestra solo 3 campos; warnings se perdían. Defense: console.warn server-side + Network preview DevTools.

### facturaia — toggle Verifactu fix (2026-05-19, PR #48)
- **Duplicado columna ↔ JSON settings nunca dura** — `verifactu_activo` (columna) + `settings.fiscal.verifactu` (JSON) → bug clásico: lectura defensiva `!== false` reactiva el flag silenciosamente cuando el JSON no tiene la clave. Fuente única, siempre. Ver [[Stack/facturaia]] "Toggle Verifactu".
- **Policy `org_member_update` permite UPDATE a CUALQUIER miembro** — sin distinguir rol. Para columnas regulatorias (Verifactu, entorno AEAT, etc.) el riesgo es real: cualquier becario apaga el envío a AEAT desde DevTools. Mitigación: trigger BEFORE UPDATE con guard de rol + API route con `requireRole`. Revisar otras columnas críticas (`regimen_iva`, `nif`, `iae`).
- **Trigger SQL captura IP via `current_setting('request.headers')`** — Supabase inyecta los headers HTTP en el GUC de sesión cuando viene del PostgREST. En SQL directo (psql, cron, migrations) el GUC no existe → wrap en `BEGIN…EXCEPTION WHEN OTHERS THEN v_ip:=NULL; END`. Útil para auditoría regulatoria.
- **Worktree desde `origin/main` cuando local diverge** — `git worktree add .worktrees/X origin/main -b fix/clean` evita arrastrar commits locales no pusheados al PR. Patrón canónico cuando hay sprint pre-cutover con commits acumulados.
- **`gh auth switch -u AgentesIAMadrid`** antes de tocar repo TuFacturaIA via gh CLI. Default `mdelmonteagentesia` da 404.

### facturaia / fiscal AEAT Sprint 3 audit
- **RPC SQL atómico para multi-INSERT con triggers** — `admin.rpc()` con `SECURITY DEFINER` envuelve N INSERTs en 1 transacción; advisory_xact_lock sobrevive hasta COMMIT del RPC. Cierra race entre triggers BEFORE/AFTER. Ver [[verifactu-rpc-atomico-cierra-race-transacciones-rest-separadas]]
- **UNIQUE INDEX CONCURRENTLY parcial anti-doble-create** — `WHERE col=valor` partial + catch SQLSTATE 23505 → idempotente a nivel BD. Smoke previo crítico para evitar INVALID. Ver [[unique-index-concurrently-parcial-para-idempotencia-bd]]
- **LLM error categorizar antes que loggear** — buckets accionables (timeout/rate_limit/auth_error/provider_unreachable/unknown) + log estructurado con propiedades primitivas. NUNCA `console.error('...', err)` con objeto crudo. Ver [[llm-error-categorizar-no-exponer-crudo-a-logs]]

### claude-code workflow
- **Sesiones paralelas mismo repo causan colisiones git** — verificar `git branch --show-current` + `ls migrations/0XX*` antes de cada commit/Write; stage explícito por path, nunca `-A`. Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]]
- **Agentes `isolation: worktree` — 3 failure modes** (muere sin commit dejando unstaged, forka de main desfasado con diff masivo, dos agentes pisan archivo "junk drawer"). Verificar siempre `git log <worktree-branch>` + `git status` + `git diff --stat`. Merge selectivo `git checkout <branch> -- <paths>`, no merge entero. Ver [[claude-code-agentes-worktree-failure-modes]]

### facturaia / mobile a11y
- **vh → dvh cascada doble declaración**, no `min()` atómico — Safari <15.4 descarta `min()` entero si no soporta `dvh`. Ver [[mobile-vh-dvh-cascade-vs-min-atomic-safari-15]]
- **`inert` + `aria-hidden` complementarios** en main cuando drawer mobile abierto — `inert` no funciona en iOS 15.0-15.4. Ver [[mobile-inert-plus-aria-hidden-ios-15-fallback]]
- **Restore-focus tras `inert` necesita `requestAnimationFrame`** — WebKit descarta `.focus()` sobre elemento aún inert. Ver [[mobile-restore-focus-after-inert-needs-raf]]
- **Tablas scroll-x necesitan `role="region" tabIndex={0} aria-label`** — WCAG 2.1.1 keyboard. Clase reusable `.set-table-wrap`. Ver [[mobile-table-scroll-x-needs-region-tabindex-wcag-2-1-1]]

### panel-tecnocloud / Retell
- **Retell webhook signing** — `HMAC-SHA256(api_key, body + timestamp)` concat sin separador. Header `v=<ts_ms>,d=<hex>`. Ver [[retell-webhook-firma-hmac-body-mas-timestamp]]
- **Retell agent versioning + phone routing** — phone numbers anclan `inbound_agent_version`; `update-agent` no afecta hasta cambiar phone. Ver [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]]
- **Retell call_analyzed vs tool mid-call** — solo call_analyzed trae transcript final + recording + duration + summary. Args de tools en `transcript_with_tool_calls`. Ver [[retell-webhooks]]
- **gmail-poll self-sender** — si panel + n8n comparten cuenta OAuth, filtrar `From === oauth_email` antes del lookup o ingestas tickets falsos con contact = la propia cuenta. Ver [[gmail-poll-debe-filtrar-self-sender]]
- **n8n Gmail node sin headers custom** — no permite `X-*`; usar HTTP Request a Gmail API con MIME RAW o filtrar por From en el ingestor. Ver [[n8n-gmail-node-no-soporta-headers-custom]]
- **SDK oficial como ground truth para verify webhook** — si tu impl falla con `digest_mismatch` y `Provider.verify()` dice true → bug tuyo. Ver [[webhook-impl-verificar-contra-sdk-oficial-del-provider]]
- **`pnpm/action-setup@v4` vs packageManager** — declarar versión en UN sitio o "Multiple versions of pnpm specified". Quitar `with: version` del workflow. Ver [[pnpm-action-setup-v4-conflict-con-packageManager]]
- **Next.js `unstable_cache` no invalida con escrituras directas a BD** — script externo cambia BD, cache sirve valor viejo. Reiniciar dev o `revalidateTag`. Ver [[nextjs-unstable-cache-no-invalida-con-escritura-directa-bd]]
- **Cloudflared quick tunnel** — `cloudflared tunnel --url http://localhost:PORT --no-autoupdate`. URL temporal trycloudflare.com sin login para webhooks E2E. Ver [[claude-code-gotchas]]
- **Next.js route handlers solo permiten exports estándar** — exportar helper desde `route.ts` rompe typecheck. Mover a archivo aparte o privado. Ver [[claude-code-gotchas]]

### TuFacturaIA / agency-portal
- **pg_trgm word_similarity vs similarity** — para buscar nombre corto en descripción larga usa `word_similarity(needle, haystack)`, NO `similarity`. Threshold 0.50 ES OK para bancarios. Ver [[postgres-word-similarity-vs-similarity-para-needle-in-haystack]]
- **Defense-in-depth estado='activo'** — RLS sola no basta cuando endpoint usa `createAdminClient()` (service-role bypasa RLS). Añadir check explícito de membership activa antes de mutar. Ver [[defense-in-depth-estado-activo-cuando-admin-client-bypasa-rls]]
- **UPSERT atómico con RPC** — `.upsert()` Supabase no incrementa contador en colisión (sobrescribe). Para counters usa RPC plpgsql con `ON CONFLICT DO UPDATE SET col = tabla.col + 1`. Ver [[upsert-atomico-rpc-vs-check-then-act-evita-lost-update]]
- **Audit con 3 agentes paralelos cross-sprint** — security + SQL/math + UX en paralelo encuentra 10× más que un agente único. Filtrar ~30% falsos positivos. Solo si >5 archivos cambiados. Ver [[audit-3-agentes-paralelos-detecta-vulnerabilidades-cross-sprint]]
- **Match bancario multi-señal vs importe bruto** — auto-confirmar solo con varias señales (importe + texto + fecha) y umbral ≥80. Importe solo nunca basta. Ver [[conciliacion-multi-señal-vs-importe-bruto-falsos-positivos]]
- **Reglas aprendidas de confirms manuales** — opt-in explícito al confirmar match débil, el sistema extrae token + lo aprende para futuro. Cierra loop sin bajar umbral. Ver [[reglas-aprendidas-de-confirmacion-manual-cierra-loop-aprendizaje]]
- **Coexistencia 2 fuentes mismo dato** — manual no compite con automático, redefine su scope ("lo que la otra fuente no ve"). Ver [[saldo-inicial-cashflow-coexistencia-psd2-manual]]
- **Setting en /agentes vs inline** — si el dato cambia con el tiempo o se ve afectar la vista, inline. Settings de módulo son para preferencias estables. Ver [[opt-out-de-setting-en-agentes-cuando-inline-es-suficiente]]
- **Zod nullishOptional para webhooks n8n** — `.optional()` no admite `null` y n8n manda `null` para vacíos → 400. Helper `s.nullish().transform(v => v ?? undefined)`. Ver [[zod-optional-rechaza-null-en-webhooks-n8n]]
- **Tool calling con tool_choice forzado para extracción LLM** — elimina silent fail vs regex sobre texto libre. `gpt-4o-2024-11-20` + Structured Outputs strict. Ver [[llm-tool-calling-elimina-silent-fail-extraccion-estructurada]]
- **source_quote anti-alucinación** — exigir cita literal del usuario por campo extraído elimina invenciones. Ver [[llm-source-quote-anti-alucinacion-extraccion]]
- **Observabilidad destapa bugs viejos** — añadir `cron_runs` reveló `storage-quota-check` fallando hace meses. Ver [[observabilidad-nueva-destapa-bugs-viejos-en-silencio]]
- **Admin tooling no-técnico** — semáforo verde/ámbar/rojo + descripción español + ejemplo real + sin botones destructivos. Ver [[admin-tooling-para-no-tecnicos-read-only-semaforo-ejemplos]]
- **Webhook delete híbrido** — hard si no disparó, soft si tiene historial. Ver [[webhook-delete-hibrido-hard-si-no-disparo-soft-si-tiene-historial]]
- **Encryption key no rotable** — secrets cifrados en BD pierden acceso si cambias la key. Ver [[encryption-key-de-credenciales-en-bd-no-es-rotable-in-place]]
- **PR grande con migración** — checklist (filas, consumidores, rollback) antes de merge. Ver [[pr-grande-con-migracion-y-cambio-bucket-revisar-antes-de-mergear]]
- **Regen types.gen con PR abierto** — conflict garantizado. Esperar merge y consolidar. Ver [[regenerar-types-gen-conflict-con-pr-abierto]]
- **Embedded select supabase-js no va sobre views** — 2 queries + merge en cliente. Ver [[supabase-embedded-select-no-funciona-en-views]]
- **Supabase embed FK** — tipa array, runtime devuelve objeto. Cast defensivo. Ver [[supabase-js-fk-embed-tipa-array-pero-runtime-objeto]]
- **Profile lookup cross-canal scoping obligatorio** — `org_members!inner` o cross-tenant. Ver [[supabase-profile-lookup-cross-canal-debe-scoping-org-members]]
- **CREATE OR REPLACE VIEW + ADD COLUMN** — `f.*` reordena (42P16). DROP + CREATE + security_invoker. Ver [[supabase-create-or-replace-view-falla-tras-add-column]]
- **next/image PDF** — rompe en Puppeteer/server-side. `<img>` nativo. Ver [[next-image-server-side-pdf]]
- **table-layout fixed %s** — sumar 100% o hay gaps. Clase has-X por variante. Ver [[table-layout-fixed-columnas-porcentaje]]
- **Popover en modal overflow:hidden** — se corta. Inline disclosure. Ver [[popover-en-modal-con-overflow-hidden-se-corta-usar-inline-disclosure]]
- **Templates con tokens** — `replace()` deja literal lo desconocido. CHECK BD + API + UI. Ver [[postgres-template-tokens-replace-simple-no-rechaza-desconocidos]]
- **Supabase invitations** — no depender del trigger, crear `org_member` directo + estado `invitado`. Ver [[supabase-inviteuserbyemail-no-propaga-data-a-raw-user-meta-data]]
- **AI agent + entidad relacionada** — tool de lookup obligatoria (abono→factura). Ver [[agente-ia-genera-entidad-relacionada-necesita-tool-lookup-de-referencia]]
- **schema_migrations no fiable** — verificar columnas/triggers reales en prod, no la tabla. Ver [[schema-migrations-no-es-source-of-truth-si-aplicas-manual]]
- **Migrations versión duplicada** — supabase CLI rechaza, renombrar a slot libre tras max. Ver [[supabase-cli-rechaza-migrations-con-version-duplicada]]
- **Reportes fiscales filtran borradores** — modelo 303 inflado si sumas todo. Ver [[reportes-financieros-deben-excluir-estados-no-fiscales]]
- **Dokploy env → docker-compose** — env panel solo llega si compose la referencia con `${VAR}`. Ver [[dokploy-env-pass-through-requiere-docker-compose-environment]]
- **Tests integration Supabase** — validar schema antes de redactar (6 iteraciones CI por inventar campos). Ver [[tests-integration-supabase-validar-schema-antes-de-redactar]]
- **PRs encadenados GitHub** — merge no propaga a main. PR nuevo a main o merge local. Ver [[github-prs-encadenados-no-llegan-a-main]]
- **Skill chain UI** — impeccable→polish→audit→critique→guidelines→baseline→typeset (16→20). Ver [[skill-chain-ui-impeccable-polish-audit-critique-baseline-typeset]]
- **Impersonation proxy** — cookie `impersonate_org`, `useOrgClient()` hook. Ver [[facturaia-impersonation-proxy-client]]
- **Puppeteer PDF** — browser singleton, dynamic imports, no self-fetch en Docker. Ver [[puppeteer-html-to-pdf-pixel-perfect-con-plantillas-react]]
- **openapi-fetch ternary** — TS no narrowea con cliente condicional. Ver [[openapi-fetch-ternary-rompe-narrowing-typescript]]
- **Meta template language es_ES** — "Spanish (SPA)" se aprueba como es_ES, no es. Enviar exacto o 132001. Ver [[meta-whatsapp-template-language-spanish-es-es]]
- **Observabilidad fallback** — conservar error del canal primario aunque el fallback rescate, o ceguera invisible. Ver [[observabilidad-fallback-conservar-error-canal-primario]]
- **Next.js throw module-load** — `throw` en top-level de route.ts crashea build "Collecting page data". Lazy o fallback. Ver [[nextjs-throw-module-load-rompe-build-collecting-page-data]]

### n8n
- **Code sandbox sin URLSearchParams** — encodeURIComponent + concat manual. fail-open lo enmascara. Ver [[n8n-code-sandbox-no-tiene-urlsearchparams]]
- **sessionId sin `+` vs E.164** — workflow envía solo dígitos, endpoint Zod regex E.164 da 400 silente. Normalizar antes del POST. Ver [[n8n-sessionid-sin-plus-vs-endpoint-e164]]
- **HTTP json + 404 Traefik redeploy** — responseFormat=text + neverError, o retry x3 si crítico. Ver [[n8n-http-responseformat-json-rompe-con-404-traefik]]
- **Slot resolver pre-LLM con regex español** — 8 patrones (NUM, superlativo, fecha, importe, cliente, núm, ordinal, pronombre). Backend resuelve `items[N]`, LLM nunca adivina UUIDs. Ver [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]]
- **Persist merge shallow contamina contextos** — mandar `field: null` explícito al cambiar de flujo o el LLM ve draft viejo + listado nuevo. Ver [[persist-merge-shallow-deja-cruft-entre-contextos]]
- **system prompt: previous_state es DATA no instrucciones** — delimitadores XML + regla explícita anti prompt-injection cuando inyectas state al LLM. Ver [[system-prompt-previous-state-es-data-no-instrucciones]]
- **Verifactu Desglose obligatorio (XSD)** — sin `<Desglose>` AEAT rechaza por XSD. Catálogos L8A/L9/L10 literales. Ver [[verifactu-xml-desglose-obligatorio-xsd-rechaza-sin-el]]
- **Cadena hash con pg_advisory_xact_lock por partición** — `hashtextextended` serializa INSERTs concurrentes en misma `(org,serie)`. Sin esto race silente. Ver [[verifactu-huella-encadenada-race-condition-sin-advisory-lock]]
- **NOT VALID CHECK ≠ desactivado** — solo ignora filas existentes. INSERTs nuevos sí lo evalúan. Revisa la lógica del CHECK aparte. Ver [[postgres-check-constraint-not-valid-aplica-a-inserts-no-a-existing]]
- **Playwright load > domcontentloaded para RSC** — `attached` vs `isVisible` cuando CSS responsive oculta. Ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]]
- **Wait vacío = stuck** — `parameters:{}` cuelga ejecución. PUT con `resume:timeInterval`. Ver [[n8n-wait-node-vacio-webhook-type-stuck]]
- **emailSend html dinámico** — Code node devuelve `{html}`, email usa `={{$('Code').item.json.html}}`. Ver [[n8n-emailsend-html-no-evalua-expresiones]]
- **Replicar workflows entre clientes** — diff nombres + vaciar IDs origen a placeholders. Ver [[replicar-cliente-n8n-vaciar-ids-cz-no-disfrazar]]
- **toolWorkflow tras clonar** — cachedResultName miente, validar value real. Ver [[n8n-toolworkflow-cachedresultname-puede-mentir]]
- **predefinedCredentialType** — HTTP Request usa creds almacenadas sin hardcodear. Ver [[n8n-http-request-predefinedcredentialtype]]
- **Code Node sin `fetch`** — usar `this.helpers.httpRequest`. Ver learnings
- **Supabase `$json[0]` vs `$json`** — con `Prefer: return=representation` PostgREST devuelve objeto. Usar `$json.id`
- **toolWorkflow onError** — siempre `continueErrorOutput`, nunca `stopWorkflow`
- **AI Agent 3 reglas** — 0 eventos=libre, weekday number en Think, tool description con consecuencias
- **n8n web UI paste convierte `'` ASCII a `'` Unicode** — SyntaxError críptico al ejecutar Code node, línea visualmente idéntica. Retypear quotes a mano o usar `$env.VAR`. Ver [[n8n-web-ui-paste-convierte-comillas-a-smart-quotes-syntaxerror]]

### Kommo / Retell
- **Retell publish requerido** — cambios LLM no afectan llamadas si agente unpublished. Ver [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]]
- **Tool description > prompt para evitar fire temprano** — precondiciones en `description` del tool + `tool_call_strict_mode: true`. El "PROHIBIDO" del system prompt el LLM lo ignora. Ver [[llm-tool-description-precondiciones-pesa-mas-que-prompt]]
- **Voice agent confunde persona-interna con cliente** — si menciona "quiero hablar con Dani", el LLM mete "Dani" como nombre_cliente. Aclarar en description del campo. Ver [[voice-agent-confunde-persona-interna-con-nombre-cliente]]
- **`execution_message_description` no debe comprometer acción** — neutro ("dame un segundo"), nunca "voy a derivarte" — el LLM lo verbaliza antes de saber qué pasa. Ver [[retell-execution-message-description-no-comprometer-accion]]
- **`call_summary` (transcript completo) > `args.intencion` para email post-llamada** — args.intencion truncado por el prompt; regenerar en n8n con gpt-4.1-mini desde transcript completo (5 puntos, max_tokens 700). Ver [[retell-call-summary-vs-tool-args-intencion-para-resumen-email]]
- **Kommo webhook status_lead** — dispara en TODOS los cambios, filtrar con IF. Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]
- **Kommo salesbot IDs** — endpoint `/ajax/v4/bots/` desde consola. Ver [[kommo-salesbot-ids-ajax-v4]]
- **Kommo salesbot vacío** — `salesbot/run` devuelve success aunque vacío. Acción "Enviar WhatsApp" requerida. Ver [[kommo-salesbot-run-success-sin-acciones]]
- **Kommo webhook tras update n8n** — PUT al workflow rompe webhook, recrear. Ver [[kommo-webhook-deja-de-disparar-tras-update-n8n]]

### Infra (Dokploy / Docker)
- **Dokploy AgentesIA SSH** — `ssh -p 5251 root@185.47.13.166` (viejo) / `root@185.47.13.170` (nuevo TuFacturaIA). Key `~/.ssh/id_ed25519`. Ver [[docker-infra]]
- **Dokploy pegar compose duplica líneas** — al pegar YAML completo el editor corrompe la inserción. Verificar archivo en disco tras Save. Ver [[dokploy-paste-compose-corruption]]
- **`docker compose up -d` NO recrea container si solo cambia valor de `${VAR}`** — `--force-recreate` obligatorio. Ver [[docker-compose-env-not-recreate]]
- **Dokploy reload tras redeploy** — Bad Gateway hasta Traefik reload manual
- **Alpine sin bash/curl** — `apk add` en Dockerfile para crons. Ver [[alpine-docker-sin-bash-ni-curl-anadir-via-dockerfile-para-crons]]
- **Dokploy schedule comando** — `curl -H` corto vs `node -e` largo, word-wrap UI mete espacios. Ver [[dokploy-schedule-bash-c-rompe-process-exit-con-word-wrap]]
- **Supabase JWT vs sb_secret** — `sb_secret_*` no vale Bearer directo, JWT legacy. Ver [[supabase-sb-secret-vs-jwt-http]]
- **Dokploy BuildKit cache invencible** — `COPY . .` cacheado aunque src/ cambie. Bump `package.json.version`. Ver [[dokploy-buildkit-cache-invencible-bump-package-json]]
- **Supabase Site URL = fallback silencioso** — si `redirectTo` no está en Redirect URLs allowlist, Supabase usa Site URL (dev `0.0.0.0:3000` olvidado rompe prod). Ver [[supabase-site-url-fallback-rompe-redirecturl-fuera-de-allowlist]]
- **IP cliente bajo Traefik/Dokploy** — `x-real-ip` primero, último XFF de fallback (no primero — spoofeable). Ver [[traefik-dokploy-client-ip-x-real-ip-o-ultimo-xff]]
- **Bypass plantillas Auth Supabase** — `admin.generateLink` + Resend propio + plantilla castellano. Ver [[supabase-bypassear-plantilla-auth-con-admin-generatelink]]

## 2026-05-10 — voz Retell + n8n + Kommo (sesión Simarro Ana)
- [[retell/voice-config-inbound-castellano]] — config canónica voice agent inbound castellano (Flash v2.5, timeouts, fillers, triage de patinazos, compresión prompt 38%)
- [[n8n#Gotchas Simarro voz]] — kommo `with` array, httpRequest responseFormat, settings allowed list, loop polling exit, TZ Madrid local, severar paths multi-trigger, respond temprano async branch
- [[kommo#Gotchas Simarro voz]] — salesbot API privada, WhatsApp duplicado triage, lead lookup desambiguación por nombre, status IDs + custom fields Simarro
