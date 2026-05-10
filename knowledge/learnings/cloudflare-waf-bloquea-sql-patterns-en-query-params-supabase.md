---
title: cloudflare waf bloquea sql patterns en query params supabase
date: 2026-05-10
source: claude-code-session
tags: [supabase, cloudflare, security, bug]
---

`escapeLike()` en LIKE/ILIKE escapa `%`, `_`, `\` pero NO comillas. Cuando el input usuario contiene patrón SQL inj clásico (`' OR 1=1--`), Supabase REST devuelve **HTML de Cloudflare** (no JSON) → supabase-js error → endpoint cae a 500.

Esto ES defensa correcta (no se ejecuta SQL), pero cosméticamente devuelve el código equivocado.

**Verificado**: comillas legítimas (`O'Brien`) sí funcionan — Cloudflare solo bloquea el patrón completo `' OR 1=1--`, `; DROP`, etc.

**Patrón de fix**: en el catch del query error, detectar el síntoma (HTML response, parseo JSON falla) y mapear a 422 graceful con código distinguible. O aceptar el 500 — a un atacante le da igual.

Aplica a cualquier endpoint Supabase con `.ilike()`/`.like()` sobre input usuario-controlado en producción detrás de Cloudflare.
