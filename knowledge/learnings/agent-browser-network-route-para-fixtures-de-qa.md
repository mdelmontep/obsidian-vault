---
title: agent-browser network route inyecta fixtures que sobreviven recargas; mockear window.fetch no
date: 2026-08-20
source: facturaia
tags: [agent-browser, qa, fixtures, nextjs]
---

Para QA visual de estados de UI que no existen con datos reales (tabla llena, propuestas
del LLM), `agent-browser network route "<glob>" --body '<json>'` intercepta a nivel CDP y
**sobrevive recargas y navegaciones**: rutear el endpoint, recargar la página y el
componente monta con el fixture. `network unroute` al terminar.

Lo que NO funciona: mockear `window.fetch` por `eval` — muere con cada carga completa, y
en Next App Router la navegación SPA de vuelta restaura la página desde la Router Cache
**sin remontar el componente**, así que el mock nunca llega a usarse.

Etiquetar el fixture como simulado en el artifact de QA: capturas de datos inventados
presentadas como reales son deuda de confianza.

Caso real: card de términos de búsqueda de TuFacturaIA (FB-02) — la cuenta no tenía
términos y los 3 estados ricos se QA-aron con fixtures ruteados, dicho en el artifact.
