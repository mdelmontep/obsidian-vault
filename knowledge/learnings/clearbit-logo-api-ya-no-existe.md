---
title: clearbit logo api ya no existe
date: 2026-04-25
source: claude-code-session
tags: [api, logos, facturaia]
---

Clearbit fue adquirida por HubSpot y la API gratuita de logos (`https://logo.clearbit.com/{domain}`) ya no responde (connection refused, exit code 6).

**Alternativa**: Google Favicon API — gratis, sin API key, sin límite conocido:

```
https://www.google.com/s2/favicons?domain={domain}&sz=128
```

- Devuelve PNG 128x128
- Siempre responde 200 (incluso para dominios inexistentes)
- El icono default (globe) pesa ~726 bytes
- Favicons reales pesan >750 bytes (Telefónica: 1133, Amazon: 1761, IKEA: 1784)
- Filtrar por `byteLength > 750` para descartar defaults

Limitaciones:
- Son favicons, no logos de marca completos
- Empresas sin web propia (ej: Endesa con ~650 bytes) no se detectan
- Suficiente para avatares 40-48px pero no para uso a gran escala

Ver también: [[google-favicon-api-patron-auto-logo]]
