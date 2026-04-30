---
title: hot cache
date: 2026-04-26
tags: [stack, index]
---

# Hot Cache — Últimas 2 semanas

Resúmenes de 1-2 líneas con link al learning. Leer el learning completo solo si es necesario.

> Si algo tiene más de 2 semanas, moverlo al índice correspondiente en Stack/ o eliminarlo.

---

- **Apify Idealista/Fotocasa** — igolaizola actors, DataDome resuelto, ~$65-100/mes por cliente en barridos cada 2h. Ver [[scraping-idealista-fotocasa-produccion]]
- **Security API routes** — auth, rate limit, input whitelist, magic bytes, timingSafeEqual, sanitizar errores. Ver [[checklist-seguridad-api-routes-nextjs]]
- **Re-auth password admin** — campos disabled + modal password + `signInWithPassword` para config multi-org. Ver [[re-autenticacion-con-password-para-acciones-sensibles-admin]]
- **Auto-logo Google Favicon** — `google.com/s2/favicons?domain={slug}.es&sz=128`, filtro >750 bytes, sentinel `not_found`. Clearbit muerto. Ver [[google-favicon-api-patron-auto-logo]]
- **Impersonation proxy** — cookie `impersonate_org`, `useOrgClient()` hook, proxy via admin client, read-only. Ver [[facturaia-impersonation-proxy-client]]
- **RLS multi-tenant** — `get_user_org_id()` SECURITY DEFINER, falla con service_role. Ver [[rls-multi-tenant-supabase-con-security-definer]]
- **AI Agent 3 reglas** — 0 eventos=libre, weekday number en Think, tool description con consecuencias. Ver learnings
- **Kommo webhook status_lead** — dispara en TODOS los cambios, filtrar con IF. Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]
- **Kommo salesbot IDs** — endpoint real: `/ajax/v4/bots/` desde consola navegador. JSONs del Drive tienen datos CZ hardcodeados, adaptar antes de importar. Ver [[kommo-salesbot-ids-ajax-v4]] [[kommo-salesbot-json-adaptation]]
- **Kommo salesbot sin acciones** — `salesbot/run` devuelve success:true aunque el bot esté vacío. Necesita acción "Enviar WhatsApp" con `{{lead.cf.FIELD_ID}}` en editor Kommo. Ver [[kommo-salesbot-run-success-sin-acciones]]
- **Kommo webhook tras update n8n** — PUT al workflow rompe el webhook de Kommo; borrar y volver a añadir en Ajustes → Webhooks. Ver [[kommo-webhook-deja-de-disparar-tras-update-n8n]]
- **n8n predefinedCredentialType** — HTTP Request puede usar credenciales almacenadas sin hardcodear token. Ver [[n8n-http-request-predefinedcredentialtype]]
- **n8n API import** — Python json.dump a /tmp, curl -d @file, activate es POST, executeWorkflowTrigger v1.0. Ver learnings
- **OCR pipeline** — base64 en Next.js (no n8n sandbox), enviar org_nombre, Realtime para progreso
- **Puppeteer PDF** — browser singleton, dynamic imports, no self-fetch en Docker, template_config deep merge. Ver [[puppeteer-html-to-pdf-pixel-perfect-con-plantillas-react]]
- **Complimentary orgs** — campo boolean, MRR excluye, estrella morada admin. Migración 007
- **Email OAuth Gmail** — HMAC state, polling per-org, dedup SHA256, last_checked solo en éxito
- **WhatsApp webhook override** — per-phone-number, matching por número remitente normalizado
- **n8n binary filesystem** — `getBinaryDataBuffer(0, 'data')`, nunca `$binary.data.data`
- **Settings JSONB toggle** — guardar ref local, no releer BD (race condition)
- **Supabase Storage size** — SDK `list()` + metadata.size, no SQL
- **toolWorkflow onError** — siempre `continueErrorOutput`, nunca `stopWorkflow`
- **Dokploy reload** — redeploy deja Bad Gateway, Traefik reload manual obligatorio
- **Supabase JWT vs sb_secret** — `sb_secret_*` no vale como Bearer HTTP directo, usar JWT legacy. Ver [[supabase-sb-secret-vs-jwt-http]]
- **next/image PDF** — rompe en Puppeteer/server-side, usar `<img>` nativo en plantillas PDF. Ver [[next-image-server-side-pdf]]
- **n8n Supabase `$json[0]` vs `$json`** — con `Prefer: return=representation`, PostgREST devuelve objeto directo, no array. En HTTP Request nodes, usar `$json.id` no `$json[0].id`. Sin esto: `factura_id: ""` → UUID parse error
- **n8n Code Node `fetch` no existe** — sandbox task-runner no tiene `fetch`. Usar `this.helpers.httpRequest` siempre. Error: `ReferenceError: fetch is not defined`
- **table-layout fixed %s** — porcentajes deben sumar 100% o hay gaps. Clase has-X por variante. Ver [[table-layout-fixed-columnas-porcentaje]]
- **PRs encadenados GitHub** — merge no propaga a main, crear PR nuevo a main o merge local. Ver [[github-prs-encadenados-no-llegan-a-main]]
- **AI agent + entidad relacionada** — tool de lookup obligatoria (abono→factura), prompt fuerza uso, agente devuelve `{error}` si no encuentra. Ver [[agente-ia-genera-entidad-relacionada-necesita-tool-lookup-de-referencia]]
- **Supabase invitations** — no depender del trigger, crear `org_member` directo + estado `'invitado'` que promueve a `'activo'` en primer login. Ver [[supabase-inviteuserbyemail-no-propaga-data-a-raw-user-meta-data]]
- **Templates con tokens** — `replace()` deja literal lo desconocido. CHECK BD + API + UI, tres redes. Ver [[postgres-template-tokens-replace-simple-no-rechaza-desconocidos]]
- **Popover en modal con overflow:hidden** — se corta. Inline disclosure es la opción simple. Ver [[popover-en-modal-con-overflow-hidden-se-corta-usar-inline-disclosure]]
- **Skill chain UI** — impeccable→polish→audit→critique→guidelines→baseline→typeset llevan componente de 16/20 a 20/20. Ver [[skill-chain-ui-impeccable-polish-audit-critique-baseline-typeset]]
- **Supabase RLS olvidado** — policies sin ENABLE RLS = tabla pública, alerta llega 24-48h tarde. Ver [[supabase-enable-rls-olvidado-tabla-publica]]
- **iOS input zoom** — font-size ≥ 16px en inputs, touch targets 44px, safe-area-inset, inputMode tel. Ver Stack/frontend-css-mobile.md
- **CSS stagger auth** — animation-delay por selector CSS, prefers-reduced-motion cubre cada selector. Ver Stack/frontend-motion.md
