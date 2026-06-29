---
title: vitest mock clase es module - vi.hoisted para evitar "not a constructor"
date: 2026-06-30
source: claude-code-session
tags: [vitest, testing, mocks, esm]
---

Al mockear un módulo ES que exporta una clase (openai, stripe, etc.), el factory de `vi.mock`
se evalúa ANTES de que los `vi.fn()` declarados en el scope del módulo existan → error "not a constructor".

Fix: extraer los fns con `vi.hoisted()` primero, luego referenciarlos en el factory:

```ts
const { mockCreate } = vi.hoisted(() => ({ mockCreate: vi.fn() }))

vi.mock('openai', () => ({
  default: class OpenAI {
    audio = { transcriptions: { create: mockCreate } }
  },
}))
```

Módulos que solo exportan funciones (no clases) no necesitan hoisting:
`vi.mock('@/lib/foo', () => ({ myFn: vi.fn() }))` funciona directo.

Caso real: `src/lib/whatsapp/__tests__/whisper.test.ts` mockeando el SDK openai.
