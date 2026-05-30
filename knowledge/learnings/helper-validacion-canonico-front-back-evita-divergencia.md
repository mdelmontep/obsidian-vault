---
title: validador de invariante de dominio en módulo único front+back
date: 2026-05-30
source: claude-code-session
tags: [arquitectura, validacion, anti-divergencia]
---

Cuando un invariante (NIF, IBAN, currency, postal code) se valida en UI
y en endpoint, vive en UN módulo importado por ambos. Discriminated
union `{ ok: true, ...meta } | { ok: false, reason }`:

- UI usa `.ok` + `.reason` (feedback inline).
- Backend usa `.ok` + `.normalized` (canonicaliza antes de INSERT).

Si el helper crece para añadir tipo/normalización, extender el union,
no duplicar. Test único cubre ambos consumidores.

Caso TuFacturaIA: `src/lib/fiscal/nif.ts` consumido por
`clientes-view.tsx` y `/api/internal/voice/clientes/crear`. Sin esto,
dos agentes paralelos en distinto scope duplican lógica y divergen al
1er edge case (CIF letra control).

Aplica también a UPDATE de columnas regulatorias entre admin UI y API.

Ver [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]].
