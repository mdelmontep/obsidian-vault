---
title: npx de una CLI versionada baja la última major y rompe con el schema del repo
date: 2026-08-20
source: panel-tecnocloud
tags: [prisma, npx, monorepo, gotcha]
---

En un worktree nuevo de `panel-tecnocloud`, `pnpm typecheck` fallaba con `Module '@prisma/client' has no exported member 'PrismaClient'` — faltaba generar el cliente. El reflejo (`npx prisma generate`) **empeora el diagnóstico**: `npx` no encuentra el binario local, baja la **última** versión publicada (7.9.1) y su validador rechaza el schema del repo, que es de la 6:

```
P1012 · The datasource property `url` is no longer supported in schema files
```

El error apunta al schema, que está bien, y no a la versión de la CLI, que es lo que cambió. Lo correcto: `pnpm --filter <pkg> generate` (o `pnpm run generate` dentro del paquete), que usa la versión declarada en su `package.json`.

Patrón general, no solo Prisma: **`npx <cli>` en un repo que fija la versión de esa CLI es una fuente de rojos ajenos**, y el mensaje señala tu código en vez de la herramienta. Vale igual para `supabase`, `eslint` y `tsc`.

Y el contexto: un worktree recién creado **no trae `node_modules` ni artefactos generados**; antes de leer ningún rojo, instalar y generar.
