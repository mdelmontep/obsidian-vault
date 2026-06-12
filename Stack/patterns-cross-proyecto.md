---
title: patterns cross-proyecto
date: 2026-06-02
tags: [stack, index, permanente]
---

# Patrones permanentes (cross-proyecto)

Movido de `hot.md` en la poda 2026-06-02. Resúmenes 1-2 líneas con link al learning.


- **Kommo CF + emoji 4-byte (🏡)** — Kommo descarta el valor en silencio (200) y el CF queda vacío (utf8 no utf8mb4); si alimenta una plantilla, Meta manda el ejemplo. Ver [[kommo-custom-field-rechaza-emoji-4-byte]]
- **Plantilla WhatsApp: variables sin `\n`/tab/>4 espacios** — Meta rechaza con #132018; salesbot/run da 200 pero el envío no llega (rechazo async). Texto multi-item en una línea. Ver [[whatsapp-template-variable-no-admite-saltos-de-linea]]
- **Stripe "precio + IVA": `tax_behavior=exclusive` + registro UE con `place_of_supply_scheme`** — checkout con `automatic_tax`+`billing_address_collection=required`+`customer_update[address]=auto`+`tax_id_collection`; `tax/registrations` UE exige `country_options[es][standard][place_of_supply_scheme]=standard`. `curl` sin `-f` da falso OK en 4xx. Ver [[stripe-tax-registro-ue-via-api]]
- **Filtros URL bookmarkeables: hidratar antes de sincronizar** — el efecto estado→URL borra los query params si corre antes de leer la URL al montar; flag `hydrated`. Ver [[useeffect-sync-estado-a-url-pisa-query-params-si-corre-antes-de-hidratar]]
- **Outbox para integraciones externas (Drive sync, futuros)** — triggers BD AFTER UPDATE para cubrir múltiples entry points + hash de contenido para idempotencia + SKIP LOCKED para race + cascade revoke por external_id en OAuth. Ver [[outbox-trigger-bd-vs-hook-js-multiples-entry-points]] [[outbox-idempotencia-por-hash-contenido]] [[select-for-update-skip-locked-via-rpc-security-definer]] [[oauth-cascade-revoke-por-external-id-multi-org]]
- **Campo huérfano = UI vacía silenciosa** — código referencia columna sin migración paralela → PostgREST 400 → cliente Supabase JS deja `data:null` sin lanzar → `setState([])` → grid vacía + texto fallback. Síntoma característico: id en minúscula donde se esperaba nombre capitalizado. Detección: `from('T').select()` vs `CREATE/ALTER TABLE T`. Ver [[campo-huerfano-shape-sin-migracion-paralela]]
- **`date_trunc(col) = ...` en WHERE no es sargable aunque haya índice** — Postgres pide columna desnuda al izquierdo. Reescribir con range `>= start AND < end` para usar `(otra_col, col)` existente. Ver [[date-trunc-en-where-no-sargable-aunque-haya-indice]]
- **Migración auth sin downtime con `SIGNING_LEGACY_UNTIL`** — aceptar ambos formatos hasta fecha env, log warn cada legacy, rechazo auto al expirar. Mejor que flag boolean: deadline visible. Ver [[migracion-auth-sin-downtime-con-signing-legacy-until]]
- **Env con fecha mal formada → fail-closed** — typo en cutover de auth/feature crítica NO debe extender la ventana indefinidamente. `Date.parse → NaN` → desactiva la funcionalidad protegida + log error. Ver [[env-fecha-mal-formada-fail-closed-no-fail-open]]
- **Migrar auth: cambiar el default del wrapper migra N rutas de golpe** — vs handler-por-handler. Solo válido si la auth nueva acepta también la vieja durante una ventana (legacy compat) y el default funciona para el caso mayoritario. Cuerpo sensible: handler por handler con body firmado. Ver [[migrar-auth-wrapper-default-vs-handler-por-handler]]
- **Refactor de import en código = actualizar TODOS los `vi.mock` que apuntan al path viejo** — Vitest no detecta el rename; los mocks quedan fantasmas y los tests rompen masivamente. `grep -rln 'vi.mock.*lib/old' src/` antes de pushear. Ver [[test-mocks-rename-import-path-no-rename-import]]
- **`supabase migration new` rompe la secuencia NNN_** — registra timestamp huérfano en schema_migrations. SQL aplicado a mano tampoco se registra. Reconciliar con `migration repair --status reverted/applied`, NO con `db pull`. Hook pre-push lo previene. Ver [[supabase-migration-new-rompe-secuencia-nnn-name]]
- **`db push` no ejecuta migraciones cuyo NNN ya existe en remoto (rama stale)** — numeras 197-202 pero prod ya tiene 197-204 de otra rama → push las da por aplicadas SIN error. `migration list --linked` ANTES de push; renumerar al hueco real. Ver [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]
- **Feature con recurso por-org: actualizar onboarding, no solo backfill** — migración que da el recurso (serie B/F) a orgs existentes pero olvida la función de alta → clientes NUEVOS sin el recurso, falla en prod. Trigger AFTER INSERT org idempotente. Ver [[feature-recurso-por-org-actualizar-onboarding-no-solo-backfill]]
- **n8n API PUT settings whitelist** — campos extras en settings (binaryMode, etc.) hacen 400 aunque el panel los guarde. Strip antes de PUT + re-activar con POST /activate. Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]]
- **Validador de invariante en módulo único front+back** — discriminated union `{ok,reason}|{ok,normalized}` importable por UI y endpoint. Sin esto, divergencia al 1er edge case. Ver [[helper-validacion-canonico-front-back-evita-divergencia]]
- **n8n langchain toolCode con schema → args en `query` como objeto (no string)** — `JSON.parse(query)` lanza/devuelve {}. Usar `if (typeof query === 'object') params = query`. `$fromAI(name, descr, type)` con descripción NO vacía también funciona. Ver [[n8n-langchain-toolcode-args-en-input-no-en-query]]
- **AI Agent con chat memory no re-llama tool tras bugfix** — el LLM "recuerda" turnos de error previos y deja de invocar la tool. Purgar `n8n_chat_histories WHERE session_id=<hash>` para validar fix. Ver [[n8n-chat-memory-contamina-tool-retry-tras-bugfix]]
- **Soft-delete cliente/proveedor para no romper FK fiscal** — facturas RD 1619/2012 no pueden quedar huérfanas. `archivado_at TIMESTAMPTZ` + filtro `IS NULL` por defecto en TODAS las superficies (autocomplete, búsqueda, dashboard, tools del bot, API v1 con opt-in). DELETE duro captura código 23503 y propone Archivar.
- **`??` no cubre env vacía** — `Number(env ?? 500)` con `env=""` → 0 (no 500) porque nullish coalesce solo cubre `null/undefined`. Helper `parseNumEnv` que rechace string vacía + NaN + ≤0. Ver [[env-vacia-rompe-default-con-nullish-coalescing-numeric]]

- **Invitar a crear org sin saber email → token propio** — Supabase magic-link ata link al email. Tabla `*_signup_invites` + landing + consumo en callback (no en trigger SQL). Ver [[signup-invite-token-propio-vs-magic-link-supabase]]
- **vi.fn(() => ...) sin rest param** — spread (...args) rompe con TS2556. Declarar `(..._args: unknown[])` en el spy. Ver [[vitest-vi-fn-sin-params-rompe-spread-args]]
- **Bandeja staging ↔ tabla real con FK RESTRICT** — borrar de un lado debe sincronizar el otro o queda huérfano + blob bloat. Ver [[bandeja-staging-tabla-real-fk-restrict-borrar-sincroniza-ambos-lados]]
- **Dokploy env `CLAVE:valor` no se parsea** — el `:` en vez de `=` deja la var ausente en runtime (silencioso). Verificar con API/`docker exec env`, no el panel. Ver [[dokploy-env-clave-dos-puntos-no-se-parsea]]
- **Dokploy env custom → compose + panel** — var en panel no basta; necesita línea `- VAR=${VAR}` en `environment:` del compose + Deploy. Ver [[dokploy-env-compose-section-necesaria-para-variables-custom]]
- **Org-gate bloquea aceptar la 1ª invitación** — middleware que exige org activa rompe el onboarding pre-org (invitado sin org aún). Bypass explícito tipo `allowNoOrg`. Ver [[auth-org-gate-bloquea-aceptar-primera-invitacion]]
- **2FA/teléfono diferido a la activación del canal, NUNCA gate de login** — verificar on-demand al activar WhatsApp, no al entrar; gate global atrapa invitados (coste + callejón). Ver [[2fa-telefono-solo-para-canal-que-lo-usa-no-gate-global]]
- **Magic link 1-uso lo pre-consumen escáneres de email** — TTL no basta; usar token-landing + POST, y reenvío self-service. Ver [[magic-link-un-solo-uso-lo-preconsumen-escaneres-email]]
- **Gate de rol en endpoint debe contemplar superadmin** — superadmin trae `role=null` (salta lookup); `role !== X` lo bloquea. Usa `isSuperadmin || role in [...]`. Ver [[role-gate-endpoint-debe-contemplar-superadmin]]
- **Cifras en capa nueva (IA/copiloto/export) reusan el filtro canónico** — no reimplementar; divergencia = bug de confianza. Ver [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]]
- **Equivalente derivado siempre coherente → columna GENERATED STORED** — no trigger de sync ni cálculo en app; ningún insert puede desincronizar. Ver [[columna-generada-stored-para-equivalente-derivado]]
- **Migración aplicada fuera de `db push` no entra en schema_migrations** — psql/MCP la dejan out-of-band; reaplicar falla. Hazla idempotente + reconcilia. Ver [[migracion-aplicada-fuera-de-historial-supabase]]
- **Anthropic prompt cache es por prefijo** — campo variable en `system` invalida también el cache de `tools`. Ver [[anthropic-prompt-cache-prefijo-system-tools]]
- **Toggle optimista sin check de error miente** — revertir al fallar; mejor por endpoint. Ver [[toggle-optimista-sin-rollback-miente-al-usuario]]
- **ETag por path + upsert mutable** — 304 indefinido tras regen blob. ETag fuerte = hash del buffer + `no-cache`. Ver [[etag-por-path-upsert-stale-304]]
- **WhatsApp Cloud API exclusivo con número** — no coexiste con app Business móvil. Ver [[whatsapp-cloud-api-vs-business-app-numero-exclusivo]]
- **PDF adjunto email** — congelado en inbox cliente; reenviar para refrescar. Link = siempre actualizado. Ver [[pdf-adjunto-email-vs-link-frozen-blob]]
- **Retell Flex vs Rigid coste** — Flex compila TODO (nodos+KB+tools), token-scaling x2-5 si >3500 tokens. Rigid + gpt-4.1 sin high_priority = €0.135/min. Default Rigid. Ver [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
- **Calendar idempotency sha1(phone+slot)** — eventId determinista pasado al create. Si ya existe → 409 nativo, no duplica. Sin estado externo. Ver [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]
- **PR externa sobre modelo sunsetado** — portar al modelo nuevo antes de mergear, no después. Caso: PR76 iCloud sobre settings.email → PR77 sobre plataforma. Ver [[pr-externa-sobre-modelo-sunsetado-portar-no-mergear]]
- **IMAP attachment selectivo** — bodyStructure → download(partId), no client.download(uid) completo. Evita OOM proporcional al RFC822. Ver [[imap-attachment-selectivo-bodystructure-evita-oom]]
- **n8n toolCode post-`$fromAI`** — `specifyInputSchema: true + schemaType:'manual' + inputSchema` JSON Schema obliga al LLM a mandar JSON en `query`. Sin schema, el LLM envía texto crudo. Ver [[$fromAI-en-toolCode-lanza-no-execution-data-available-en-n8n-2.15.x]]
- **Supabase `sb_secret_*` en HTTP directo necesita header `apikey`** — solo `Authorization: Bearer` da `Invalid Compact JWS`. Siempre añadir `apikey: <key>` también. Ver [[supabase-sb-secret-vs-jwt-http]]
- **n8n que reimplementa lógica backend se salta sus defensas** — sanitización, validación, permisos del endpoint no se heredan. Ver [[n8n-reimplementa-endpoint-backend-pierde-sus-defensas]]
- **Integración crítica en JSONB pierde observabilidad** — sin schema/FKs/enum status, errores van a logs efímeros y nadie se entera. Tabla dedicada con `status` enum + tabla de eventos. Ver [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]]
- **Monitor deploy con señal de comportamiento** — 404/401/307→login coinciden en versión vieja y nueva → falso positivo. Usar endpoint cuyo body/redirect SÍ cambia entre versiones. Ver [[monitor-deploy-usar-senal-comportamiento-no-existencia]]
- **MCP n8n no cubre todas las instancias** — si `get_workflow_details` falla en TODOS los MCP, REST API `/api/v1/workflows?active=true` con `X-N8N-API-KEY` localiza el real. Ver [[mcp-n8n-no-tiene-todos-los-workflows-fallback-rest-api]]
- **`import 'server-only'` bloquea scripts CLI** — split primitivas a `crypto-primitives.ts` (sin guard) + re-export con guard. Misma implementación, sin duplicar. Ver [[crypto-modulo-server-only-bloquea-scripts-cli-extraer-primitivas]]
- **Saldo-actual + serie histórica = doble conteo** — no pasar saldo-de-hoy como `saldoInicial` a un forecast que acumula desde meses pasados; sumar saldo real + solo neto futuro. Ver [[cashflow-saldo-actual-mas-serie-historica-doble-conteo]]
- **Tool conversacional en agente "solo JSON"** — envolver la respuesta en el `{tipo}` que el parser enruta (`conversacion`) o el parser revienta; distinguir tools lectura/acción para `ok=true`. Ver [[agente-llm-json-estricto-tool-conversacional-envolver-en-tipo]]
- **Mock de función compartida = falso verde** — el test del consumidor no ve si la llama con el arg equivocado. Test de integración o aserción sobre los args. Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **Panel suma columna que ningún writer rellena → siempre 0** — INSERT olvida `cost_usd/tokens_in/out` aunque la columna exista. Auditoría: `select count(*), count(col)` — si `col << *` y el panel suma `col`, hay bug. Preferir derivar al vuelo desde columnas que ya se escriben. Ver [[coste-derivado-de-tokens-mensaje-vs-columna-tool-calls-vacia]]
- **Formateador `< $0.01 → "$0.00"` esconde gasto real** — copy "$0.00" es indistinguible de gasto cero vs sub-centavo. Mostrar 4 decimales en sub-centavo (`$0.0005`) o `<$0.01`. Reservar `$0.00` para `=== 0` exacto. Ver [[coste-derivado-de-tokens-mensaje-vs-columna-tool-calls-vacia]]

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
- **OpenAI Chat Completions PDF → `image_url`** — `type:'file'` es Responses API, causa 400. Usar `image_url` con data URI + guard b64 + normalizar MIME. Ver [[openai-chatcompletions-pdf-usar-image-url-no-file]]
- **Bot multi-org: sticky silencia ingesta** — `active_org_id` sync conveniente en chat, pero cada foto es decisión independiente → siempre preguntar empresa si ≥2 orgs. Ver [[bot-multi-accion-fallback-activo-silencia-routing]]
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
- **n8n Code node NO interpola `{{ }}`** — al migrar HTTP→Code, el `jsonBody` va como objeto JS, no como string literal `={...{{ }}...}` (se manda crudo → JSON inválido → 400 silencioso). Caso: rompió toda la selección multi-org del bot ~2 sem. Ver [[n8n-code-node-no-interpola-llaves-dobles]]
- **NIF España paraguas DNI/NIE/CIF** — desde RD 1065/2007 unificado bajo "NIF"; aceptar 3 algoritmos bajo misma función. Ver [[nif-espana-paraguas-dni-nie-cif-desde-rd-1065-2007]]
- **WhatsApp Interactive List límites** — max 10 rows, title 24, button 20, id 200 (patrón `tipo:UUID` + regex switch). Ver [[whatsapp-interactive-list-limites-y-row-id-pattern]]


## Rescatados de hot.md (poda 2026-06-02)

- **Worktree desde `origin/main` cuando local diverge** — `git worktree add .worktrees/X origin/main -b fix/clean` evita arrastrar commits locales no pusheados al PR. Patrón canónico cuando hay sprint pre-cutover con commits acumulados.
- **`gh auth switch -u AgentesIAMadrid`** antes de tocar repo TuFacturaIA via gh CLI. Default `mdelmonteagentesia` da 404.
- **Code Node sin `fetch`** — usar `this.helpers.httpRequest`. Ver learnings
- **Supabase `$json[0]` vs `$json`** — con `Prefer: return=representation` PostgREST devuelve objeto. Usar `$json.id`
- **toolWorkflow onError** — siempre `continueErrorOutput`, nunca `stopWorkflow`
- **AI Agent 3 reglas** — 0 eventos=libre, weekday number en Think, tool description con consecuencias
- **Dokploy reload tras redeploy** — Bad Gateway hasta Traefik reload manual
- **Policy `org_member_update` permite UPDATE a CUALQUIER miembro** — sin distinguir rol. Para columnas regulatorias (Verifactu, entorno AEAT, etc.) el riesgo es real: cualquier becario apaga el envío a AEAT desde DevTools. Mitigación: trigger BEFORE UPDATE con guard de rol + API route con `requireRole`. Revisar otras columnas críticas (`regimen_iva`, `nif`, `iae`).
- **Trigger SQL captura IP via `current_setting('request.headers')`** — Supabase inyecta los headers HTTP en el GUC de sesión cuando viene del PostgREST. En SQL directo (psql, cron, migrations) el GUC no existe → wrap en `BEGIN…EXCEPTION WHEN OTHERS THEN v_ip:=NULL; END`. Útil para auditoría regulatoria.


## Rescatados de hot.md (poda 2026-06-12)

- **Split-TX quema números de serie** — contador en TX1 + INSERT en TX2: si TX2 falla el número ya commitió → hueco. `SELECT FOR UPDATE` + UPDATE contador + INSERT en el mismo RPC. Ver [[postgres-split-tx-counter-burn-serie-numeracion]]
- **Multiempresa SaaS 3 ejes** — navegar=membresía · agregar=propiedad · cobrar=cuenta; no mezclar (agregar por membresía cruda suma datos de clientes que gestionas → bug + RGPD). Ver [[multiempresa-saas-tres-ejes-navegar-agregar-cobrar]] · [[ADR-028-multiempresa-scope-navegar-agregar-cobrar]]
- **SSRF: validar IP no basta sin pinar el fetch** — fetch por hostname re-resuelve DNS (rebinding TOCTOU); pinear con undici Agent `connect.lookup` a la IP validada (hostname para SNI). Callback undici v7 = array `cb(null,[{address,family}])`. Ver [[ssrf-validar-dns-no-cierra-rebinding-sin-pinar-ip]]
- **rebase --onto sobre upstream movido suelta tu commit** — "Successfully rebased" miente; `git log origin/main..HEAD` antes de push, recupera con reflog+cherry-pick. Ver [[git-rebase-onto-upstream-movido-suelta-commit-reflog-recupera]]
- **build no corre vitest** — registry/enum con test de conteo rompe en CI al añadir entrada; `npx vitest run` antes de push. Ver [[pre-commit-build-no-corre-tests-registry-conteo-rompe-ci]]
- **Consumidor lee claves que el productor no emite** — JSONB sin tipo compartido = falla silenciosa + tests verdes si prueban el shape equivocado. Ver [[consumidor-lee-claves-que-productor-no-emite]]
- **Enum nuevo en código sin ampliar el CHECK de BD = insert muere mudo** — outbox-first aborta el envío entero; el 200 anti-enum del endpoint lo oculta. Ver [[enum-nuevo-en-codigo-sin-ampliar-check-bd-rompe-insert-silencioso]]
- **`ALTER TYPE ADD VALUE IF NOT EXISTS`** — idempotente; el valor nuevo NO es usable hasta commit → suéltalos al inicio del archivo, no en el `BEGIN` que lo use. Ver [[alter-type-add-value-en-migracion-supabase]]
- **RPC SECURITY DEFINER = ejecutable por anon vía PostgREST** si no revocas (EXECUTE a PUBLIC por defecto) → bypass de pago/IDOR si reciben org_id sin validar. REVOKE FROM PUBLIC, anon; `REVOKE PUBLIC` solo no basta si hay grant individual. Ver [[supabase-rpc-security-definer-execute-public]] · [[postgres-revoke-public-no-elimina-grants-individuales]]
