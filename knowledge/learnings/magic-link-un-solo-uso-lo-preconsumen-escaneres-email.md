---
title: magic link de un solo uso lo pre-consumen los escáneres de email corporativos
date: 2026-05-27
source: claude-code-session
tags: [auth, email, supabase, onboarding]
---

Los `generateLink` de Supabase (invite/magiclink) son GET de un solo uso con
TTL ~1h. Los escáneres de seguridad de email (Outlook SafeLinks, antivirus,
proxies corporativos) PRE-ABREN los enlaces → los consumen antes de que el
humano haga clic → "Email link is invalid or has expired" en el primer intento
real. Subir el TTL solo mitiga el caso "tardó >1h", NO el pre-consumo.

Patrón robusto (lo que hacen Stripe/GitHub/Slack): no mandar magic link
auto-consumible. Enviar token PROPIO → landing page → la sesión se crea al
ENVIAR un formulario (POST), inmune a prefetch. Validez en días.

Mitigación rápida sin rediseño: página de "enlace caducado" con **reenvío
self-service** (el invitado pide otro sin depender del admin) + subir TTL.
Caso 2026-05-27 invitación FacturaIA. Ver
[[2fa-telefono-solo-para-canal-que-lo-usa-no-gate-global]].
