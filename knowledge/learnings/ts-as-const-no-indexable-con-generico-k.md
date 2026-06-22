---
title: ts as const no indexable con genérico k — ts2536
date: 2026-06-23
source: claude-code-session
tags: [typescript, patterns]
---

`RENDERERS[kind]` donde `kind: K extends TemplateKind` y `RENDERERS` es `as const` → TS2536.

TS no puede probar que `K` indexa el tipo concreto del objeto `as const`.

**Fix:**
```ts
const fn = (RENDERERS as Record<TemplateKind, (d: TemplateData[TemplateKind]) => RenderedEmail>)[kind]
           as (d: TemplateData[K]) => RenderedEmail
```

Patrón: cualquier registry `as const` con indexación genérica (renderers, handlers, validators).
