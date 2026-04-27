---
title: hot cache
date: 2026-04-26
tags: [stack, index]
---

# Hot Cache — Últimas 2 semanas

Resúmenes de 1-2 líneas con link al learning. Leer el learning completo solo si es necesario.

> Si algo tiene más de 2 semanas, moverlo al índice correspondiente en Stack/ o eliminarlo.

---

- **Security API routes** — auth, rate limit, input whitelist, magic bytes, timingSafeEqual, sanitizar errores. Ver [[checklist-seguridad-api-routes-nextjs]]
- **Re-auth password admin** — campos disabled + modal password + `signInWithPassword` para config multi-org. Ver [[re-autenticacion-con-password-para-acciones-sensibles-admin]]
- **Auto-logo Google Favicon** — `google.com/s2/favicons?domain={slug}.es&sz=128`, filtro >750 bytes, sentinel `not_found`. Clearbit muerto. Ver [[google-favicon-api-patron-auto-logo]]
- **Impersonation proxy** — cookie `impersonate_org`, `useOrgClient()` hook, proxy via admin client, read-only. Ver [[facturaia-impersonation-proxy-client]]
- **RLS multi-tenant** — `get_user_org_id()` SECURITY DEFINER, falla con service_role. Ver [[rls-multi-tenant-supabase-con-security-definer]]
- **AI Agent 3 reglas** — 0 eventos=libre, weekday number en Think, tool description con consecuencias. Ver learnings
- **Kommo webhook status_lead** — dispara en TODOS los cambios, filtrar con IF. Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]
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
- **n8n Supabase `$json[0]` vs `$json`** — con `Prefer: return=representation`, PostgREST devuelve objeto directo, no array. En HTTP Request nodes, usar `$json.id` no `$json[0].id`. Sin esto: `factura_id: ""` → UUID parse error
- **n8n Code Node `fetch` no existe** — sandbox task-runner no tiene `fetch`. Usar `this.helpers.httpRequest` siempre. Error: `ReferenceError: fetch is not defined`
