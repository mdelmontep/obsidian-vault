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

**Ampliación 1-ago: el coste no es el rojo, es lo que el rojo bloquea.** El runner de tickets de TuFacturaIA corre el gate y, si falla, **abre el PR en draft** con el log pegado. Un OOM de `tsc` (exit 134, `Ineffective mark-compacts near heap limit`) dejó el #1435 aparcado **dos días** con el trabajo correcto dentro: nadie distinguió «la herramienta se murió» de «el código está mal». Antes de dar por malo un PR del runner, mirar si el fallo es de tipos o de heap y volver a correr el gate en local. Y la salida de fondo es la de arriba: `NODE_OPTIONS=--max-old-space-size` en el gate del runner, no en el criterio de quien revisa.

**Y el número importa (1-ago, PR #1459).** En el runner de tickets el arreglo NO es el 6144 de arriba: ese valor es para runners de GitHub Actions. El contenedor tiene `memory: 3G`, y pedir un heap MAYOR que el límite del cgroup es peor que no pedir nada — el kernel mata el proceso (exit 137, sin log útil) en vez de fallar V8 limpio. Quedó en `--max-old-space-size=2560` y **acotado a los pasos del gate**, no en el env del servicio: global se lo comería también el proceso `claude`, que tiene otro perfil de memoria.

**Y el hook te miente sobre la causa (3-sep, facturaia).** El `pre-push` abortó con
«Push bloqueado: build con errores. Corre 'npm run build' para ver el detalle» — el log
real traía `Ineffective mark-compacts near heap limit` justo encima. El mensaje manda a
buscar un error de tipos que no existe. Se distingue en un comando: `npm run typecheck`
suelto da `exit 134` (Abort trap), no una lista de errores. Y el heap se le pasa al hook
por entorno del propio push, que lo hereda: `NODE_OPTIONS=--max-old-space-size=8192 git
push …`. Nunca `--no-verify`, que es rodear el gate por un fallo que no es del código.
