---
title: el camino de la primera vez no prueba el de régimen, y es el segundo el que se recorre mil veces
date: 2026-08-18
source: obsidian-vault
tags: [testing, metodo, arnes, gotcha]
---

Cuando algo tiene **estado inicial** y **estado de régimen**, probar el primero deja el segundo sin cubrir — y el segundo es el que corre siempre.

**Caso.** El indexador FTS5 vaciaba con `DELETE FROM fts`. Verde en todas las pruebas, porque todas creaban el índice **de cero**. Una tabla FTS5 *contentless* no admite `DELETE` (se vacía con `INSERT INTO fts(fts) VALUES('delete-all')`): el fallo solo podía aparecer **reindexando**, y reventó en el primer uso normal.

Mismo día, mismo patrón: el aviso de reconstrucción del índice iba a `stdout`, cosa que solo se ve **cuando el índice no existe todavía** — o sea, en una máquina nueva, donde `--paths | xargs cat` intentaba abrir un fichero llamado «indexadas».

**Fix.** El test fuerza el camino de régimen explícitamente: crear → tocar un fichero → volver a correr. Y si hay dos estados, se prueban los dos, empezando por el que más veces se ejecuta.

**Olor.** Un `setup` que siempre parte de vacío. Si borrar el estado es parte del arranque del test, el camino incremental no lo cubre nadie.

Ver [[una-suite-en-verde-no-prueba-el-camino-real]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
