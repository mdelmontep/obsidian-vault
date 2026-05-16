---
title: Dokploy env panel solo llega al contenedor si docker-compose la referencia
date: 2026-05-07
source: claude-code-session
tags: [dokploy, docker, deploy]
---

Añadir `MI_VAR=valor` en panel Environment de Dokploy NO basta — el contenedor solo recibe las que están explícitamente listadas en `environment:` del `docker-compose.yml` con sintaxis `${VAR}`.

Síntoma: la app arranca sin error pero alguna feature falla en runtime (SMTP vacío, AEAT no descifra, OAuth Google rompe). Logs no avisan — process.env.X es simplemente `undefined`.

Patrón:

```yaml
services:
  app:
    environment:
      - WEBHOOK_SIGNING_KEY=${WEBHOOK_SIGNING_KEY}        # required, falla si no está
      - SMTP_HOST=${SMTP_HOST:-}                          # optional, fallback vacío
      - LLM_PROVIDER=${LLM_PROVIDER:-anthropic}           # default razonable
```

Regla: cuando añades `process.env.NUEVA_VAR` en código, también añadirla a `docker-compose.yml`. Y a `.env.example` para que el siguiente dev sepa que existe.

**Caso real FacturaIA 2026-05-16**: módulo Cobros no enviaba WhatsApp en prod desde 12-mayo silente — `META_WHATSAPP_*` y `RESEND_API_KEY` estaban en Dokploy panel pero NO en `docker-compose.yml environment:`. El OTP onboarding lo destapó al fallar Meta en todos los envíos.
