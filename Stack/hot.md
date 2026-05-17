---
title: hot cache
date: 2026-05-07
tags: [stack, index]
---

# Hot Cache

Resúmenes 1-2 líneas con link al learning. Leer learning completo solo si necesario.

## ⭐ Permanentes (cross-proyecto)

Patrones que aplican siempre, no expiran. Lo más reusado.

- **Supabase RLS olvidado** — policies sin ENABLE RLS = tabla pública, alerta 24-48h tarde. Toda tabla nueva = ENABLE en la misma migración. Ver [[supabase-enable-rls-olvidado-tabla-publica]]
- **NOT NULL post-backfill misma migration** — ADD nullable → UPDATE → SET NOT NULL en una transacción. Ver [[migration-add-column-backfill-not-null-misma-transaccion]]
- **PostgREST schema reload** — `NOTIFY pgrst, 'reload schema';` al final de migration con columna nueva. Ver [[postgrest-schema-cache-notify-tras-migration]]
- **Webhook idempotency transient** — borrar `event_id` log en 5xx/timeout para que el retry no sea replay falso. Ver [[webhook-idempotency-borrar-log-en-errores-transitorios]]
- **UPSERT sombra por remote_id** — múltiples paths convergen sin duplicar. Ver [[upsert-sombra-por-id-remoto-no-por-id-local]]
- **Signed URL proxy** — endpoint que regenera on-demand, no cachear URL firmada en BD. Ver [[signed-url-proxy-endpoint-vs-cached-en-bd]]
- **Security API routes** — checklist (auth + rate limit + whitelist + magic bytes + timingSafeEqual + path traversal). Ver [[checklist-seguridad-api-routes-nextjs]]
- **RLS multi-tenant** — `get_user_org_id()` SECURITY DEFINER, falla con service_role. Ver [[rls-multi-tenant-supabase-con-security-definer]]
- **Re-auth password admin** — campos disabled + modal password + `signInWithPassword` para acciones sensibles. Ver [[re-autenticacion-con-password-para-acciones-sensibles-admin]]
- **PGRST203 RPC overloads** — pasar TODOS los named params, no solo los del overload viejo. Ver [[postgrest-pgrst203-rpc-overloads-pasar-todos-los-params]]
- **Cloudflare WAF + ilike** — patrones SQL inj en URL Supabase devuelven HTML → endpoint 500 (defensa OK). Ver [[cloudflare-waf-bloquea-sql-patterns-en-query-params-supabase]]
- **AI Agent contrato real antes de modificar** — leer system prompt + tools vía API; JSON-out vs conversational es contrato distinto. Ver [[leer-system-prompt-y-tools-actuales-antes-de-modificar-ai-agent]]
- **useEffectEvent NO desde setTimeout** — patrón debounce reactivo va con useCallback + deps. Ver [[useeffectevent-react19-no-se-llama-desde-settimeout]]
- **LLM ambiguity con voz** — devolver lista numerada de candidatos + memoria conversacional, nunca "dime el número exacto". Ver [[llm-ambiguity-lista-candidatos-numerados-y-memoria-conversacional]]
- **Tipo nuevo en agente JSON-out** — parchear downstream o lookup recurso real (mejor lookup). Ver [[extender-tipo-en-agente-json-out-parchear-downstream-o-lookup-recurso]]
- **Verificar persistencia post-PUT** — HTTP 200 ≠ aplicó. Grep marker único en re-fetch. Ver [[verificar-persistencia-tras-put-api-con-grep-marker-unico]]
- **Métricas tabla + events** — diseñar con tabla de dominio como fuente primaria, events como complemento. Ver [[metricas-fuente-fuerte-mas-event-log]]
- **Impersonate por query** — `?org_id=` + isSuperadmin check, no fiar cookie (middleware la borra). Ver [[endpoints-impersonate-por-query-no-cookie]]
- **Cron Dokploy** — Command = solo `curl -sf -X POST URL -H "x-service-key: $VAR"` + Shell dropdown = bash. NO añadir `bash -c` (doble wrap rompe args). Ver [[cron-dokploy-curl-service-key]]
- **Form defaults schema** — `value !== undefined ? value : default`. Nunca `!!value` ni `value || default`. Ver [[form-defaults-respetar-schema-no-bang-bang-config]]
- **Overlays sobre cards** — `--bg-elev2` no `--panel`, sombra doble + `isolation: isolate`. Ver [[overlays-sobre-cards-usar-bg-elev2-no-panel]]
- **3 agentes paralelos auditoría** — security/backend/frontend simultáneos antes de cambios grandes, ~50% falsos positivos esperados. Ver [[3-agentes-paralelos-auditoria-cambios-grandes]]
- **Migrations por módulo** — si commits van por módulo, migrations separadas (`060_ocr_*`, `061_concilia_*`). Ver [[migrations-por-modulo-si-commits-van-por-modulo]]
- **React 19 derived state** — state mirror durante render evita setState en useEffect (lint bloquea). Ver [[react-19-strict-bloquea-setstate-en-useeffect]]
- **Zod ↔ OpenAPI doc** — refine de Zod no llega a clientes openapi-typescript. Tocar `openapi.json` en el mismo commit. Ver [[zod-vs-openapi-doc-contrato-real-de-clientes-generados]]
- **PR review stale** — el reviewer puede haber pusheado fixes propios. `git log origin/<rama> -5` antes de actuar. Ver [[pr-review-ya-resuelta-por-el-reviewer-mismo]]
- **Enum fiscal hardcoded en UI** — botón hardcodea R5 = falsifica motivos R1-R5 en Verifactu. Modal select obligatorio. Ver [[enum-legal-hardcodeado-en-ui-falsifica-motivos]]
- **Estado fiscal con sombra externa** — cuando hay shadow emitida, acciones de estado van vía sistema externo, no local. Ver [[acciones-de-estado-fiscal-vs-sombra-en-sistema-externo]]

## 🔥 Últimas 2 semanas

Patrones recientes de proyectos activos. Mover a sección permanente o eliminar tras 2 semanas.

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

### FacturaIA / agency-portal
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
- **Wait vacío = stuck** — `parameters:{}` cuelga ejecución. PUT con `resume:timeInterval`. Ver [[n8n-wait-node-vacio-webhook-type-stuck]]
- **emailSend html dinámico** — Code node devuelve `{html}`, email usa `={{$('Code').item.json.html}}`. Ver [[n8n-emailsend-html-no-evalua-expresiones]]
- **Replicar workflows entre clientes** — diff nombres + vaciar IDs origen a placeholders. Ver [[replicar-cliente-n8n-vaciar-ids-cz-no-disfrazar]]
- **toolWorkflow tras clonar** — cachedResultName miente, validar value real. Ver [[n8n-toolworkflow-cachedresultname-puede-mentir]]
- **predefinedCredentialType** — HTTP Request usa creds almacenadas sin hardcodear. Ver [[n8n-http-request-predefinedcredentialtype]]
- **Code Node sin `fetch`** — usar `this.helpers.httpRequest`. Ver learnings
- **Supabase `$json[0]` vs `$json`** — con `Prefer: return=representation` PostgREST devuelve objeto. Usar `$json.id`
- **toolWorkflow onError** — siempre `continueErrorOutput`, nunca `stopWorkflow`
- **AI Agent 3 reglas** — 0 eventos=libre, weekday number en Think, tool description con consecuencias

### Kommo / Retell
- **Retell publish requerido** — cambios LLM no afectan llamadas si agente unpublished. Ver [[retell-llm-cambios-sin-publish-agente-no-afectan-llamadas]]
- **Kommo webhook status_lead** — dispara en TODOS los cambios, filtrar con IF. Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]
- **Kommo salesbot IDs** — endpoint `/ajax/v4/bots/` desde consola. Ver [[kommo-salesbot-ids-ajax-v4]]
- **Kommo salesbot vacío** — `salesbot/run` devuelve success aunque vacío. Acción "Enviar WhatsApp" requerida. Ver [[kommo-salesbot-run-success-sin-acciones]]
- **Kommo webhook tras update n8n** — PUT al workflow rompe webhook, recrear. Ver [[kommo-webhook-deja-de-disparar-tras-update-n8n]]

### Infra (Dokploy / Docker)
- **Dokploy AgentesIA SSH** — `ssh -p 5251 root@185.47.13.166` (viejo) / `root@185.47.13.170` (nuevo FacturaIA). Key `~/.ssh/id_ed25519`. Ver [[docker-infra]]
- **Dokploy pegar compose duplica líneas** — al pegar YAML completo el editor corrompe la inserción. Verificar archivo en disco tras Save. Ver [[dokploy-paste-compose-corruption]]
- **`docker compose up -d` NO recrea container si solo cambia valor de `${VAR}`** — `--force-recreate` obligatorio. Ver [[docker-compose-env-not-recreate]]
- **Dokploy reload tras redeploy** — Bad Gateway hasta Traefik reload manual
- **Alpine sin bash/curl** — `apk add` en Dockerfile para crons. Ver [[alpine-docker-sin-bash-ni-curl-anadir-via-dockerfile-para-crons]]
- **Dokploy schedule comando** — `curl -H` corto vs `node -e` largo, word-wrap UI mete espacios. Ver [[dokploy-schedule-bash-c-rompe-process-exit-con-word-wrap]]
- **Supabase JWT vs sb_secret** — `sb_secret_*` no vale Bearer directo, JWT legacy. Ver [[supabase-sb-secret-vs-jwt-http]]
- **Dokploy BuildKit cache invencible** — `COPY . .` cacheado aunque src/ cambie. Bump `package.json.version`. Ver [[dokploy-buildkit-cache-invencible-bump-package-json]]

## 2026-05-10 — voz Retell + n8n + Kommo (sesión Simarro Ana)
- [[retell/voice-config-inbound-castellano]] — config canónica voice agent inbound castellano (Flash v2.5, timeouts, fillers, triage de patinazos, compresión prompt 38%)
- [[n8n#Gotchas Simarro voz]] — kommo `with` array, httpRequest responseFormat, settings allowed list, loop polling exit, TZ Madrid local, severar paths multi-trigger, respond temprano async branch
- [[kommo#Gotchas Simarro voz]] — salesbot API privada, WhatsApp duplicado triage, lead lookup desambiguación por nombre, status IDs + custom fields Simarro
