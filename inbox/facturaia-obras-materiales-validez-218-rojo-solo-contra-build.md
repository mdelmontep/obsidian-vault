---
title: facturaia · obras-materiales-validez:218 rojo solo contra el build de producción
date: 2026-09-22
source: facturaia
tags: [e2e, obras]
---
`tests/e2e/smoke/obras-materiales-validez.spec.ts:218`: `getByText('E2EOBR-… Planta baja')` resuelve un elemento **oculto**. Se reproduce solo, y únicamente contra `next start`; con `next dev` pasaba. Hay que abrir un issue y ver si es el locator o un render distinto en producción. Visto al pasar el smoke a servidor compilado (#2848).
