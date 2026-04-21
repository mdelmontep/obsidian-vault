---
title: zod v3 no tiene z.email ni z.uuid como top-level
date: 2026-04-21
source: claude-code-session
tags: [zod, validacion, typescript]
---

Zod v3 (la versión más comúnmente instalada en proyectos) no expone `z.email()`, `z.uuid()` ni `z.iso.datetime()` como funciones top-level. Son métodos de `z.string()`:

| Zod v4 (NO usar si v3 instalado) | Zod v3 (correcto) |
|---|---|
| `z.email()` | `z.string().email()` |
| `z.uuid()` | `z.string().uuid()` |
| `z.iso.datetime()` | `z.string().datetime()` |

El error es en **runtime**, no en compilación — TypeScript no lo atrapa. Resultado: `TypeError: z.email is not a function`, que rompe TODAS las API routes que importan el schema afectado.

Caso real: en FacturaIA, `schemas.ts` usaba sintaxis v4, rompiendo `/api/admin/orgs`, `/api/admin/features` y todas las rutas que importaban los schemas. El admin panel entero dejó de funcionar.

**Regla**: antes de escribir schemas Zod, verificar la versión instalada (`package.json` o `node_modules/zod/package.json`).
