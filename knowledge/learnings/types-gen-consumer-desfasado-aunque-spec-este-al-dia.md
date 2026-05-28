---
title: types.gen.ts del consumer puede estar desfasado aunque la spec del backend esté al día
date: 2026-05-28
source: claude-code-session
tags: [openapi, sdk, drift, integraciones]
---

`openapi-typescript` solo refleja el spec del backend **en el momento del último `npm run gen:`**. Si el backend actualizó el OpenAPI hace tiempo y nadie regeneró en el consumer, los tipos en `types.gen.ts` mienten silenciosamente: `data.<campo-nuevo>` queda `undefined`, no salta error de TypeScript ni de runtime.

**Caso real 2026-05-28 (agency-portal #75)**: backend de FacturaIA llevaba semanas declarando `DocumentResult.lineas: LineaResponse[]` en `openapi.json` y el handler `GET /facturas/{id}` ya las devolvía. El portal nunca regeneró `src/lib/facturaia/types.gen.ts`, así que la UI no podía mostrar líneas en facturas direct. Fix: `npm run gen:facturaia` y consumir `data.lineas`.

**Regla**: cuando se toca un endpoint en el backend (response shape, nuevo campo), abrir un PR en cada repo consumer con `gen:` + commit. CI ideal: job que falle si `git diff types.gen.ts` no es vacío tras regen contra prod. Complementario a [[openapi-spec-mantenido-a-mano-deriva-del-handler]] — esta cara es del consumer, esa del backend.
