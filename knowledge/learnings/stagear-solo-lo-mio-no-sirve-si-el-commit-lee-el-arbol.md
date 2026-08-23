---
title: reconstruir «solo mis líneas» en el índice no sirve si el commit hashea el árbol
date: 2026-08-23
source: claude-code-session facturaia
tags: [git, vault, sesiones-paralelas, arnes]
---
El ritual para no llevarte trabajo ajeno de un árbol compartido es: `git show HEAD:<ruta> > base`,
aplicar encima solo TUS ediciones, `cp` esa versión al fichero, `git add`, y **devolver la versión
completa al árbol** para que la otra sesión siga. Correcto… si el commit lee el **índice**.

`~/.claude/bin/vault-commit` **no lee el índice**: hashea los blobs con `git hash-object "$abs"`
**directo del árbol de trabajo** (lo dice su propia cabecera: «sin pasar por el índice real»), y monta
el commit con un `GIT_INDEX_FILE` temporal. Así que el `cp` de restauración —el último paso del
ritual— es justo lo que mete el trabajo ajeno en tu commit. Los dos pasos son correctos por separado y
**se anulan al encadenarlos**: 23-ago, mi commit del vault se llevó la poda de otra sesión y su entrada
del NOW, y lo detectó ella, no yo, aunque yo había «verificado» con `git diff --cached | grep`.

Regla: **averigua de dónde saca los bytes tu herramienta de commit antes de coreografiar el índice.**
Con una que hashea el árbol, el orden es: dejar la versión solo-mía EN EL ÁRBOL, commitear, y restaurar
la completa **después**. Y verificar por el `git show <sha> -- <ruta>` del commit ya hecho, no por
`git diff --cached`, que mira un índice que la herramienta ignoró.

Y hay una vuelta de tuerca mejor que invertir el orden, medida el mismo día por la otra sesión:
**si el blob no tiene que existir en el árbol, no lo pongas en el árbol.** `git show origin/main:<ruta>`
al scratchpad, editar allí, y hashear desde allí (`git hash-object <ruta-fuera-del-repo>`). El checkout
compartido no ve el fichero modificado en ningún momento, así que no hay ventana en la que otra sesión
pueda leerlo a medias ni en la que un `commit` ajeno se lo lleve. Con eso el ritual del paso 6 sobra:
no hay nada que restaurar.

Ver [[shippear-quirurgico-desde-working-tree-compartido-sucio]] · [[el-indice-de-git-es-compartido-entre-sesiones-como-el-arbol]]
