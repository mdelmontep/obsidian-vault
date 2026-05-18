---
title: mock Supabase con fail-fast por defecto en tests Vitest
date: 2026-05-18
source: claude-code-session
tags: [testing, supabase, vitest]
---

Mock chainable de Supabase devolviendo `{ data: null, error: null }` por defecto
genera **falsos positivos**: el código bajo test recibe respuesta "vacía OK" y
el test pasa por accidente.

**Patrón fail-fast**: terminales (`single`, `maybeSingle`, `then`) sin respuesta
configurada devuelven `{ data: null, error: { message: 'mock-no-response' } }`.
El código real explota → el test rompe inmediatamente si olvidaste mockear una
query. Fuerza al autor a encolar respuestas explícitas en orden.

Implementación: `vi.hoisted` con ref mutable + builder polimórfico + cola FIFO
por tabla + `setDefaultResponse` opcional. Tipos TS estrictos en API pública
(`any` solo interno por la naturaleza polimórfica del chain de Supabase).

Referencia FacturaIA: `src/lib/documents/__tests__/__fixtures__/mock-admin-client.ts`
(97 tests Vitest construidos sobre este patrón, 0 falsos positivos).
