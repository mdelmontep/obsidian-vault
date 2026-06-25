---
title: zod strict bloquea campos no listados silenciosamente
date: 2026-04-22
source: claude-code-session
tags: [zod, nextjs, api, facturaia]
---

Cuando un schema Zod usa `.strict()`, cualquier campo extra en el body del request devuelve 400 con "Datos inválidos". El frontend no muestra error visible al usuario — el campo simplemente no se guarda.

**Caso real**: `adminUpdateOrgSchema` en TuFacturaIA tenía `.strict()` con solo 6 campos. El admin panel intentaba guardar `telefono` y `settings` (WhatsApp config) via PATCH, pero Zod los rechazaba. El input se descartaba sin feedback.

**Cara B (sin `.strict()`, peor)**: un schema SIN `.strict()` hace lo contrario — **descarta** el campo extra en silencio, ni siquiera devuelve 400. Caso 2026-06-25: `POST /api/facturas` perdía `lote_id` porque su `LineaSchema` no-strict lo stripeaba **y** el mapeo a `createDocument` tampoco lo reenviaba → línea sin lote → stock no se movía. Ver [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]].

**Regla**: al añadir un campo (editable o de línea), revisar TODOS los schemas Zod del endpoint (`.strict()` → 400 mudo; no-strict → descarte mudo) **y los mapeos intermedios** a la capa de dominio. El campo puede caerse en el schema o en el `.map()` posterior.

Fix: añadir el campo al schema (`src/lib/schemas.ts`, etc.) y al mapeo a la capa de dominio.
