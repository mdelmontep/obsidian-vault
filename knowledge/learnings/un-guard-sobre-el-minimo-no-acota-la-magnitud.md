---
title: un guard sobre el mínimo no acota la magnitud
date: 2026-08-08
source: claude-code-session
tags: [testing, css, frontend, guards]
---

Guard que fija `min-height: 28px` en el primitivo y lo da por vigilado: **un
mínimo es un suelo, no un techo**. Subir el relleno (`padding: 4px 8px` →
`16px 8px`) devuelve el botón a 46 px de alto y la fila a lo que medía antes,
con el test en verde. Si el guard promete una MAGNITUD ("la fila baja a 50 px"),
tiene que acotar todo lo que la compone, no el número que se escribió ese día:
`relleno + contenido <= mínimo` lo cierra en una línea.

Hermano del mismo fallo, y también real: localizar el elemento vigilado con
`indexOf('aria-label="Guardar"')` es coger la PRIMERA aparición. El día que
alguien añada otro botón con ese rótulo en la misma vista, el guard se pone a
comprobar ese y da verde mientras el de la fila revierte. Exige unicidad y
rómpete con el motivo escrito.

Las dos se cazan igual: [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
mutando lo que el guard NO mira, no lo que mira.
Ver [[el-tap-target-del-boton-compartido-es-el-suelo-de-la-altura-de-fila]] · [[facturaia]].
