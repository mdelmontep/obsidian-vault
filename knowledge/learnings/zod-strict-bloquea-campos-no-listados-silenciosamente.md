---
title: zod strict bloquea campos no listados silenciosamente
date: 2026-04-22
source: claude-code-session
tags: [zod, nextjs, api, facturaia]
---

Cuando un schema Zod usa `.strict()`, cualquier campo extra en el body del request devuelve 400 con "Datos inválidos". El frontend no muestra error visible al usuario — el campo simplemente no se guarda.

**Caso real**: `adminUpdateOrgSchema` en FacturaIA tenía `.strict()` con solo 6 campos. El admin panel intentaba guardar `telefono` y `settings` (WhatsApp config) via PATCH, pero Zod los rechazaba. El input se descartaba sin feedback.

**Regla**: al añadir campos editables desde cualquier UI que haga PATCH, verificar siempre el schema Zod del endpoint. Si usa `.strict()`, el campo nuevo DEBE añadirse al schema o el guardado falla silenciosamente.

Fix: añadir `telefono` y `settings` al schema en `src/lib/schemas.ts`.
