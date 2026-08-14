---
title: `.dockerignore` no es `.gitignore`, y la basura local da rojos con cara de reales
date: 2026-08-14
source: claude-code-session
tags: [docker, tests, gates, falsos-positivos]
---

Un test que asevera «qué entra en la imagen» escanea el **disco** (`readdirSync`) filtrando por
`.dockerignore`. Un fichero en `.gitignore` pero **no** en `.dockerignore` —`dump.rdb` de Redis, 88 B,
de hace dos semanas— lo enciende: *«entra en la imagen y no está declarado»*.

Lo caro no es el fichero, son tres cosas:

- El mensaje es **idéntico** al de un rojo real (un directorio nuevo sin declarar), así que el rojo
  ajeno no se distingue del propio.
- Solo aparece en el **checkout raíz**: los worktrees no tienen esa basura, así que las PRs salen
  verdes y el rojo asoma en la corrida de `main` mergeado — cuando más tientas a culpar al merge.
- En prod no pasa (el build sale de un `git clone` limpio) → **invisible donde importa, visible solo
  en local**, o sea que a nadie le urge.

Fix: el test debe cruzar con `git ls-files` y, para lo no versionado, **fallar con otro mensaje** que
diga que es basura del árbol de trabajo. Segunda variante de la misma clase: un artefacto de build que
**falta** (`web/dist`) da 8 rojos que apuntan a ficheros de otra PR. Ver
[[el-control-en-rojo-invalida-cualquier-veredicto-de-mutacion]].
