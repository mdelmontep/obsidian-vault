---
title: mutate-guard cruza rutas del stage, y mutar desde el subproyecto no desbloquea
date: 2026-09-10
source: ecobox
tags: [hooks, mutacion, gates, monorepo]
---
Segunda trampa del mismo guard, distinta de [[la-mutacion-que-desbloquea-el-guard-tiene-que-ser-sobre-un-fichero-del-stage]]:
allí el fichero mutado no estaba en el stage; aquí **sí lo estaba** y el guard
bloqueaba igual.

`mutate` anota en `~/.claude/state/mutaciones.jsonl` la ruta **tal como se la
pasas**, relativa al cwd. El guard la compara contra las rutas del stage, que
son relativas a la **raíz del repo**. En un repo donde el proyecto cuelga de un
subdirectorio (`ecobox/web/`) nunca casan:

    corrido desde web/  → {"fichero":"src/lib/schema.ts"}      ✗ no casa
    stage               →  web/src/lib/schema.ts
    corrido desde raíz  → {"fichero":"web/src/lib/schema.ts"}  ✓ desbloquea

Regla: **corre `mutate` desde la raíz del repo** y pasa la ruta con su prefijo;
el comando de test se encarga él de entrar al subproyecto (`bash -c 'cd web && …'`).

Y ojo con el `--`: recibe **un** comando. `mutate … -- pnpm build && pnpm test`
le pasa solo el `build`, la shell del invocador se queda el `&& pnpm test`, y no
corre un solo test. El arnés lo cazó con «ARNÉS ROTO» en vez de darme un «sin
víctima» falso, que es exactamente para lo que está ese candado.
