---
title: una regla eslint de comparación de secretos en llamada a método debe mirar el nombre del método, no solo el objeto
date: 2026-08-06
source: claude-code-session
tags: [eslint, seguridad, ast, timing-attack, static-analysis]
---
Una regla AST que detecta "esto parece un secreto" en una llamada a método
(`CallExpression` con `callee.type === 'MemberExpression'`) y solo comprueba
`callee.object.name` (el receptor: `secreto.trim()`) deja pasar el caso simétrico donde
es el NOMBRE DEL MÉTODO el que delata el secreto y el objeto es neutro:
`fila.obtenerTokenHash() === entrada`. Mismo bug de fondo que "mirar solo el nombre en el
propio nodo de la comparación" (la auditoría anterior de este mismo proyecto): cualquier
heurística de nombre que solo mire UNA de las dos posiciones de un `MemberExpression`
(objeto vs. propiedad) se queda corta por construcción — hay que comprobar las dos.

Fix: en la función que decide "esto parece un secreto", además de
`callee.object.type === 'Identifier' && RAIZ.test(callee.object.name)`, añadir
`callee.property.type === 'Identifier' && RAIZ.test(callee.property.name)`.

Generalizable a cualquier regla de seguridad estática que resuelva "¿de dónde viene este
valor?" mirando un identificador: listar todas las posiciones sintácticas donde el nombre
relevante puede aparecer, no solo la más obvia. Ver
[[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]].
