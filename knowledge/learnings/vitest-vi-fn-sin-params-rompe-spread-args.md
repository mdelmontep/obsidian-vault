---
title: vi.fn(() => ...) sin params declarados rompe spread (...args) con TS2556
date: 2026-05-28
source: claude-code-session
tags: [testing, vitest, typescript]
---

`const spy = vi.fn(() => Promise.resolve(...))` declara firma `() => ...`.
Si en el mock haces `(...args: unknown[]) => spy(...args)`, TS2556 "spread
must be tuple or rest parameter" porque el spy no tiene rest param.

Fix: declarar el rest en el spy.
`vi.fn((..._args: unknown[]) => Promise.resolve(...))`

Runtime intacto (vi.fn acepta cualquier arg en JS), solo cambia la firma TS.
Aplica a cualquier wrapper que reenvía args genéricos al spy (típico en
mocks de clientes chainables: Supabase admin, Prisma, etc).
