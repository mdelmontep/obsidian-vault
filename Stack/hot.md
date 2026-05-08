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
- **Métricas tabla + events** — diseñar con tabla de dominio como fuente primaria, events como complemento. Ver [[metricas-fuente-fuerte-mas-event-log]]
- **Impersonate por query** — `?org_id=` + isSuperadmin check, no fiar cookie (middleware la borra). Ver [[endpoints-impersonate-por-query-no-cookie]]
- **Cron Dokploy** — `bash -c "curl -sf -X POST URL -H x-service-key:$VAR"` + Run Now valida exit + response. Ver [[cron-dokploy-curl-service-key]]
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
- **SDK oficial como ground truth para verify webhook** — si tu impl falla con `digest_mismatch` y `Provider.verify()` dice true → bug tuyo. Ver [[webhook-impl-verificar-contra-sdk-oficial-del-provider]]
- **`pnpm/action-setup@v4` vs packageManager** — declarar versión en UN sitio o "Multiple versions of pnpm specified". Quitar `with: version` del workflow. Ver [[pnpm-action-setup-v4-conflict-con-packageManager]]
- **Next.js `unstable_cache` no invalida con escrituras directas a BD** — script externo cambia BD, cache sirve valor viejo. Reiniciar dev o `revalidateTag`. Ver [[nextjs-unstable-cache-no-invalida-con-escritura-directa-bd]]
- **Cloudflared quick tunnel** — `cloudflared tunnel --url http://localhost:PORT --no-autoupdate`. URL temporal trycloudflare.com sin login para webhooks E2E. Ver [[claude-code-gotchas]]
- **Next.js route handlers solo permiten exports estándar** — exportar helper desde `route.ts` rompe typecheck. Mover a archivo aparte o privado. Ver [[claude-code-gotchas]]

### FacturaIA / agency-portal
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
- **Dokploy reload tras redeploy** — Bad Gateway hasta Traefik reload manual
- **Alpine sin bash/curl** — `apk add` en Dockerfile para crons. Ver [[alpine-docker-sin-bash-ni-curl-anadir-via-dockerfile-para-crons]]
- **Dokploy schedule comando** — `curl -H` corto vs `node -e` largo, word-wrap UI mete espacios. Ver [[dokploy-schedule-bash-c-rompe-process-exit-con-word-wrap]]
- **Supabase JWT vs sb_secret** — `sb_secret_*` no vale Bearer directo, JWT legacy. Ver [[supabase-sb-secret-vs-jwt-http]]
