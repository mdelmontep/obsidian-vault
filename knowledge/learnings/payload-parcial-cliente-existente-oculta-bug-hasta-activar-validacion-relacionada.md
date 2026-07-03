---
title: arreglar un campo de un payload puede activar una validación que expone otro campo roto
date: 2026-07-03
source: claude-code-session
tags: [frontend, validation, payload, debugging]
---

Patrón: una validación de negocio depende de 2+ campos relacionados
(`if (tieneEmpresa && !tieneNif) throw`). Si uno de los dos (`empresa`) nunca
llegaba al backend, la validación nunca se disparaba — enmascarando que el
OTRO campo (`nif`) TAMBIÉN faltaba en el mismo payload. Al arreglar solo
`empresa` (el bug reportado), la validación se activó por primera vez y
reventó con el `nif` que llevaba roto desde siempre, sin relación aparente
con el fix recién hecho.

Fix del fix: al añadir un campo a un payload parcial, grepear qué
validaciones lo usan como condición (`if (campoX && ...)`) y auditar TODOS
los campos que esa validación necesita, no solo el reportado — copiar el
payload completo de la rama "funciona bien" en vez de añadir un campo suelto.

Caso real TuFacturaIA PR #665→#667: `empresa` arreglado en #665/#666 sin
`nif`, mismo bug en 2 sitios (factura+presupuesto), 2 PRs para cerrarlo del
todo.
