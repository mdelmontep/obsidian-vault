---
title: tsc/next build mueren por OOM en CI de repos grandes sin ser error real
date: 2026-07-01
source: claude-code-session
tags: [ci, github-actions, typescript, nextjs, oom]
---

En repos que crecen a >1500 archivos TS/TSX, el heap de V8 auto-detectado desde cgroup
en runners containerizados de GitHub Actions no siempre es fiable. `tsc --noEmit` o
`next build` mueren con "JavaScript heap out of memory" (exit 134) sin que haya un
error de tipos real — local, con la misma versión de Node/TS, compila limpio.

`skipLibCheck`/`incremental` en tsconfig no lo arreglan (el límite es de memoria, no
de trabajo). Fix: heap explícito en el step de CI:

```yaml
env:
  NODE_OPTIONS: '--max-old-space-size=6144'
```

Aplica también al step de `build` si usa Next (hace su propio type-check interno, más
pesado por el bundling encima — mismo riesgo).

Confirmado 2026-07-23 que no es solo GitHub Actions: en un `docker build` local sobre
Colima con 10GB de RAM asignada, `next build` seguía haciendo OOM en el paso de
TypeScript con el mismo heap ~2GB fijo — subir la RAM del host/VM no lo arregla, hace
falta `NODE_OPTIONS` explícito dentro del contenedor (probado inyectándolo vía
`docker exec -e`, no vale con solo aumentar el `--memory` de la VM).

Relacionado (distinto pero cercano): [[pre-commit-hook-oom-con-dev-server]].
