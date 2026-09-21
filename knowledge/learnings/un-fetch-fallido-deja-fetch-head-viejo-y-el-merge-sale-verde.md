---
title: un fetch fallido deja FETCH_HEAD viejo y el merge siguiente sale verde
date: 2026-09-21
source: agh-iberica
tags: [git, tren-de-merges, integracion]
---
**Qué pasó:** en un bucle `git fetch origin pull/N/head && git merge --no-ff FETCH_HEAD`, el fetch de #1964 falló por SSL. El merge usó el FETCH_HEAD de la PR anterior, que ya estaba contenido, así que salió con exit 0, y el bucle marcó #1964 como «ok» sin haberla metido.

**Por qué:** un fetch que falla no borra FETCH_HEAD, y hacer merge de un commit que ya es ancestro no da error.

**Patrón:**
1. Tras cada fetch, `git rev-parse FETCH_HEAD` debe ser igual al `headRefOid` de `gh pr view N --json headRefOid`. Si no coincide, reintentar.
2. Al terminar, comprobar `git merge-base --is-ancestor <sha> HEAD` para cada PR.

Relacionado: [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]].
