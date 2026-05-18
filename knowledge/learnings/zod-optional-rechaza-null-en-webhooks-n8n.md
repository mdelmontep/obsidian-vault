---
title: zod .optional() rechaza null en webhooks externos
date: 2026-05-18
source: claude-code-session
tags: [zod, n8n, webhooks, gotcha]
---

n8n compone bodies con expressions `$json.foo || null`, así que campos
"opcionales" llegan como `null` cuando no hay valor. Zod `.optional()` solo
admite `undefined` → rechaza con `Invalid input: expected string, received
null` → 400 al caller.

Fix universal — helper:

```ts
const nullishOptional = <T extends z.ZodTypeAny>(s: T) =>
  s.nullish().transform((v) => (v ?? undefined) as z.infer<T> | undefined);
```

Aplicable a todos los schemas Zod expuestos a sistemas externos (n8n, Zapier,
Make, landing pages que usen `||` en JS antes de enviar). NO usar en Server
Actions ni en endpoints PATCH donde `null` tenga semántica de borrado.

Detección: meta-test que escanee `src/**/route.ts` buscando `.optional()`
plano en schemas de webhook. Permite override con `// allow-plain-optional:
razón`.

Caso real: agency-portal PR #65 rompió onboarding entero (95% del tráfico
fallaba con 400) durante 12h hasta merge del fix en PR #66.
