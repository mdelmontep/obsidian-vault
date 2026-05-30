---
title: Migrar auth — cambiar el default del wrapper vs handler por handler
date: 2026-05-30
source: facturaia Fase 2.5 — withCronTracking → HMAC default
tags: [auth, refactor, migracion, wrapper]
---

Cuando una auth nueva (HMAC, mTLS, OAuth refactor) debe llegar a N rutas que ya usan un wrapper común, cambiar el **default del wrapper** migra todas de golpe sin tocar handlers individuales. Ahorra N × edits + N × tests + N × code review.

Ejemplo facturaia (`src/lib/cron/track.ts`):

```ts
// Antes: ~30 crons usan requireServiceKey por default del wrapper.
const authCheck = options.auth ?? requireServiceKey

// Después: mismo wrapper, default migrado. Cero touch en los handlers.
const authCheck = options.auth ?? ((req) => requireServiceAuth(req, ''))
```

Pre-requisitos para que funcione sin downtime:
1. La auth nueva acepta **también** la auth vieja durante un período (ver [[migracion-auth-sin-downtime-con-signing-legacy-until]]). Si no, todos los callers existentes rompen al instante.
2. El default funciona para el caso mayoritario (en crons: body vacío). Para callers con body, dejas el opt-in vía `options.auth` custom.
3. Tu wrapper expone el opt-in. Si no, los pocos crons que tengan body firmado quedan rotos.

Caso "handler por handler" sí necesario:
- Cuando el body es relevante para la firma (`POST /api/internal/cobros-stop`, `/ocr-audit`, `/fiscal-upload-worm`). Aquí cambiar el default del wrapper firma sobre `""`, no sobre el body real → el HMAC anti-tampering se pierde.
- Para estas rutas críticas: migración manual (leer body raw antes de auth, pasarlo a `requireServiceAuth(req, body)`, parsear desde el string después).

Política aplicada en facturaia Fase 2.5:
- **Crons** (wrapper común): default migrado de golpe.
- **Rutas internas críticas** (cobros, fiscal WORM, OCR audit): handler por handler con body firmado.
- **Rutas internas voice/whatsapp helpers** (~22): pendientes en Fase 2.6, vivirán con legacy hasta `SIGNING_LEGACY_UNTIL`.

Filtro útil: si el endpoint recibe un body que mueve datos sensibles (dinero, documentos fiscales, decisiones de ML), migra a mano con body firmado. Si es un cron-style POST sin body o con body trivial, el default del wrapper es suficiente.

[[migracion-auth-sin-downtime-con-signing-legacy-until]] [[env-fecha-mal-formada-fail-closed-no-fail-open]]
