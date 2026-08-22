---
title: git toma destino e identidad del entorno, no del cwd — aislar un test con cwd no aísla nada
date: 2026-08-10
source: claude-code-session
tags: [git, testing, arnes, hooks]
---
Un test que monta un repo desechable y lanza `git` con `cwd: <tmp>` **no está aislado**. `cwd` sólo
decide dónde BUSCA git cuando nadie se lo ha dicho; las variables de entorno se lo dicen y ganan.

Costó un repositorio vaciado: 1.082 ficheros borrados y empujados a `main`, con el árbol de `HEAD`
reducido a los tres ficheros que el test creaba, y el commit firmado con la identidad de mentira del test.

Son **doce** variables, en dos familias, y la segunda casi nadie la limpia:
- **Dónde escribe**: `GIT_DIR`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`,
  `GIT_OBJECT_DIRECTORY`, `GIT_CEILING_DIRECTORIES`.
- **Quién firma**: `GIT_AUTHOR_NAME/EMAIL/DATE`, `GIT_COMMITTER_NAME/EMAIL/DATE`. **`git commit` las
  exporta a sus hooks**, y pisan el `user.name` que el repo temporal acaba de configurarse.

Por eso el arreglo se hace en dos pasadas si no se prueba bien: la suite pasa en solitario y **falla al
correr desde el `pre-commit`**, que es el camino real. Ver [[una-suite-en-verde-no-prueba-el-camino-real]].

Fix: un único ayudante que borre las doce del entorno del hijo y compruebe `git rev-parse
--show-toplevel` ANTES de escribir nada, fallando ruidosamente si no es el temporal. Y un gate que
prohíba invocar `git` fuera de ese ayudante — si no, vuelve con el siguiente test.

**Reincidió el 22-ago y la profecía del párrafo anterior se cumplió literalmente**: el ayudante se
escribió, el gate «prohíbe invocar git fuera de él» no, y volvió con el siguiente test. Tres
precisiones que faltaban:
- **Solo detona pusheando desde un worktree ENLAZADO**: su `pre-push` exporta `GIT_DIR`; el de un
  checkout normal no. O sea, lo dispara la práctica que el CLAUDE.md ORDENA cuando hay dos sesiones.
- **Leer también rompe**, no solo escribir: un guard que lee una migración con `git show` leía otro
  repositorio y salía rojo sin haber nada roto.
- **El sitio del arreglo es el `setup` de la suite, no cada llamada.** Limpiar `GIT_*` una vez en
  `src/test-setup.ts` hace que el camino del hook sea IDÉNTICO al manual, que es la propiedad que
  faltaba; el ayudante por llamada se queda como cinturón. Aguanta además el hook ABORTADO a mitad
  (medido): la limpieza ocurre antes del primer test, así que no hay ventana sucia.
- Y el síntoma mandaba al sitio equivocado: el push se rechazaba con «la suite está en rojo» y los
  rojos eran los ~18 tests que enumeran con `git ls-files`, que veían cero por el índice corrupto.
  Consecuencia, no causa. Ver [[una-suite-en-verde-no-prueba-el-camino-real]] ·
  [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]]

