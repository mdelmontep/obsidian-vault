---
title: una rejilla de casillas con el distintivo en un span hermano deja N controles con el mismo nombre
date: 2026-08-11
source: claude-code-session
tags: [a11y, react, testing, ui, tucrmia]
---
Matriz de permisos: una fila por recurso, y en cada fila casillas «Leer»/«Escribir»/«Exportar».
El recurso está en un `<span>` de la fila, **hermano** de los `<label>`, así que no forma parte
del nombre accesible de ninguna casilla → 12 controles con **5 nombres** entre todos. Con la
vista puesta se entiende por la fila; con lector de pantalla son 12 casillas indistinguibles
que conceden permisos distintos.

**Por qué no lo caza la suite**: el propio test la usa como `getAllByLabelText('Leer')[0]` y
pasa — el índice tapa la ambigüedad. Sale al abrir un `snapshot` de accesibilidad en un
navegador de verdad (`agent-browser snapshot -i` lista rol + nombre de cada control).

**Fix**: `aria-label={\`${recurso}: ${accion}\`}` en la casilla, dejando el texto visible corto
—repetir el recurso en cada celda convierte la retícula en ruido para quien sí ve la fila—.
Un `<fieldset>/<legend>` por fila también vale, pero cambia la retícula.

**El test que impide que vuelva no es «existe el label»**: es que **no haya dos controles con el
mismo nombre accesible** (`new Set(nombres).size === nombres.length`). Ver
[[getbyrole-casa-el-nombre-accesible-por-subcadena]].
