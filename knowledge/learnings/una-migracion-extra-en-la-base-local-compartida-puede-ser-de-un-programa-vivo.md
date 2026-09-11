---
title: una migración extra en la base local compartida puede ser de un programa vivo, no basura
date: 2026-09-11
source: facturaia
tags: [supabase, migraciones, worktree, medicion, gotcha]
---
El pre-vuelo de la base local avisó de una migración aplicada que mi rama no tenía y
**prescribe `db reset`**. La lectura fácil —«residuo de otra rama, reseteo y sigo»— era la
destructiva: la 888 era `888_marketing_asset_take.sql`, de un programa vivo, presente en
**15 ramas locales y 5 ya en origin**. El reset habría reventado las quince, en una base
que comparten ~20 worktrees.

La base local no es tuya aunque corra en tu máquina: es **estado compartido que otras
ramas necesitan**, como prod a otra escala.

**Antes de resetear, mide de quién es**, no de quién crees que es:
`git log --all --oneline -- supabase/migrations/<NNN>_*.sql` + `git branch -a --contains <sha>`.
Si sale más de una rama, no hay nada que limpiar: el aviso es informativo y la respuesta
correcta es **no hacer nada**.

Un remedio prescrito dentro de un aviso está escrito para el caso que su autor imaginó, no
para el tuyo. Ver [[migraciones-repartidas-entre-worktrees-dan-falsa-divergencia]] ·
[[colision-de-numero-de-migracion-hace-que-db-push-la-salte-en-silencio]]
