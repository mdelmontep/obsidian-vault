---
title: el arreglo de formulario parcial se escribe en una entidad y el hermano se queda con el bug
date: 2026-08-15
source: claude-code-session
tags: [frontend, formularios, tucrmia, patrones]
---
F12 («formulario parcial nunca dispara upsert de la fila completa») se arregló en `contacts` cuando la
edición inline del teléfono borró el email guardado, con su helper `camposOpcionalesDeContacto` que
distingue **«el campo no viene»** (`undefined`, no se toca) de **«viene vacío»** (`null`, se vacía).

`companies` nunca lo recibió. Su acción traducía los seis campos ausentes con un `textoOpcional` que
devuelve `null` para el campo que falta, y la mutación sólo salta `undefined`: **cada edición del
dominio ponía a NULL el NIF, el país y las cuatro columnas de la dirección**. En producción, en
silencio, y la pantalla ni siquiera pinta esos campos para que se note.

Los dos gotchas que lo hacían invisible:
- **La fixture del test del hermano nace con `tax_id: null`**, así que la suite no puede ver que se
  borra algo que ya era nulo. Un test que parte de nulls no prueba una regresión de borrado.
- El helper del bueno tiene el antipatrón citado **en su cabecera**, así que buscar el patrón por texto
  encuentra el sitio ARREGLADO y no el roto.

Regla: al arreglar un formulario parcial, `grep` de las otras entidades con edición inline **el mismo
día**, y que su test parta de una fila con todos los campos llenos.
