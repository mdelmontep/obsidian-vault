---
title: maps.app.goo.gl (Firebase Dynamic Links) rompe la vista previa de WhatsApp aunque el link resuelva bien en navegador
date: 2026-08-04
source: claude-code-session
tags: [n8n, whatsapp, kommo, google-maps, firebase]
---

Google apagó Firebase Dynamic Links el 25-ago-2025. `maps.app.goo.gl/...` sigue resolviendo bien
si lo abres tú (302 → `google.com/maps/place/...` → 200, comprobado con `curl`), pero el crawler
que genera la vista previa dentro de WhatsApp golpea el mismo backend roto y muestra "Invalid
Dynamic Link" en la tarjeta del chat. Afecta a cualquier link corto de Maps compartido antes del
apagón, aunque nadie lo haya tocado desde entonces.

**Fix**: sustituir por el formato largo y estable, que no depende de Dynamic Links:
`https://www.google.com/maps/search/?api=1&query=<lat>,<lng>` (o con el nombre del negocio en
`query` si no tienes coordenadas a mano).

**Caso real**: Clínica Zen, 3 workflows n8n (`qBUnBCRxKJEOJGFv`, `RN0wl8RaRmwLpnfQ`,
`13Roz21TOBwy8gp8`) con el mismo `maps.app.goo.gl` hardcodeado en plantillas HTML de email.

Transversal: cualquier cliente que comparta ubicación por WhatsApp con un link corto de Maps
generado antes de ago-2025 puede tener el mismo problema. Revisar en el resto de clientes
AgentesIA (Danny, Laserys, EcoBox, Simarro, Elphis, AGH, Tecnocloud).
