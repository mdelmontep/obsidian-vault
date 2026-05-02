---
title: scripts one-shot con .env.local divergente de prod dan 404 fantasmas
date: 2026-05-02
source: claude-code-session
tags: [ops, scripts, env]
---

Scripts tipo `backfill`, `setup-mapping`, `seed-credentials` con `npx tsx --env-file=.env.local` leen URLs y keys del `.env.local` local. Ese archivo puede llevar semanas/meses sin tocarse y apuntar a valores del `.env.example` (placeholders).

Caso real: `FACTURAIA_API_URL=https://facturaia.com` en `.env.local` (placeholder) → script da 404 inexplicable. Producción tenía `https://facturaia.agentesia.world` correcto en Dokploy. La integración productiva funcionaba; la ejecución local no.

Reglas:
- **Scripts que pegan a producción ejecutarlos desde el contenedor** (Dokploy "Open Terminal" → `npx tsx scripts/X.ts` sin `--env-file`). Las envs del runtime están alineadas con el deploy.
- Si tienes que ejecutarlos en local, primero `grep ^FACTURAIA_API_URL .env.local` y compara con la env real del deploy.
- Si el `.env.local` se quedó con placeholders, actualizar TODOS los valores de una vez (no solo el que rompió) — los demás también pueden estar caducados.
