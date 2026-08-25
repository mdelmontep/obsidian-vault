---
title: un comando de reparación corrido desde un checkout viejo repara a la versión vieja, y te felicita
date: 2026-08-07
source: claude-code-session agh-iberica
tags: [git, migraciones, verificacion, worktree, gotcha]
---
La BD de tests estaba envenenada y el remedio documentado era `dropdb` + `createdb` +
`npm run db:migrate`. Lo corrí desde el checkout principal, **75 commits por detrás de
`origin/main`**. Resultado: base con **31 migraciones y 14 valores** en el CHECK contra
**33 y 15** de una sana — faltaban `0032` y `0033`, y la `0033` era justo la que añadía el
valor ausente. El comando imprimió **«migraciones aplicadas»** igual.

Un script de reparación no repara «a HEAD»: repara **al código que tiene delante**. Su fuente
de verdad es el directorio del checkout desde el que lo lanzas. Te mueve de *rota de una forma*
a *rota de otra*, y la segunda es peor: «envenenada» daba 5 rojos ajenos, «desfasada» no da
ninguno hasta que un test toca justo lo que falta.

Aplica igual a `db:migrate`, seeds, codegen, `openapi generate`, sync de fixtures.

**Antes de lanzarlo:** `git rev-list --count HEAD..origin/main`. En un repo con worktrees el
checkout **principal** es el que más se queda atrás, porque nadie trabaja en él.
**Después:** verificar por RESULTADO, nunca por el mensaje de éxito, y comparando **las dos
listas**, no el conteo — dos bases con el mismo número de migraciones pueden diferir:
`diff <(psql -d a -tAc 'select name from schema_migrations order by 1') <(psql -d b -tAc '…')`.

Es la cara "escritura" de [[auditar-sobre-origin-main-worktree-no-cwd-stale]]; la causa del
envenenamiento previo, en [[registrar-una-migracion-sin-ejecutarla-envenena-la-bd]]. Un guard
derivado del código (`discoverMigrations()` + el CHECK que declara `schema.sql`) aborta este
caso aunque su autor no lo imaginara — a diferencia de una lista escrita a mano.

**Segunda ocurrencia, y no era una BD: era el CANDADO que estaba verificando** (AGH 12-ago, #1056).
Monté un worktree desechable para ver el lock bloquear *en el camino real*, lancé dos barridos a la
vez… y no bloqueó. El worktree estaba en el commit anterior y **mi cambio no estaba commiteado**:
corría el script de antes. Peor que el caso de la BD porque **las dos lecturas fáciles eran falsas** —
«funciona» (sus 6 tests llevaban verdes todo el rato) y «no funciona», que me habría hecho reescribir
un candado correcto. Generalización: al verificar algo en el camino real, lo primero no es el
resultado, es **qué versión ejecuta el proceso que mides** — `git log -1` del worktree de prueba,
`git status` de donde editas, y un `grep -c "<símbolo nuevo>"` sobre el fichero que va a ejecutarse.

