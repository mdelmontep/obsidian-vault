---
title: un guard que se apoya en una medición externa no es un guard
date: 2026-08-07
source: claude-code-session
tags: [migraciones, verificacion, metodo]
---

En una migración escribí `coste_hora_mo = coste_hora_mo * f` con el comentario
`-- hoy 0 en todas las orgs`. Era verdad: lo había medido en producción esa
mañana. Lo cazó una auditoría: **entre la medición y el `db push` hay días**, y
la propia aplicación tenía un banner pidiéndole a la clienta que rellenara ese
campo — en otra unidad. Si lo rellenaba en esa ventana, la migración se lo
multiplicaba por 1,42 y el assert de precios no lo veía.

**La regla**: una medición externa justifica que el caso sea RARO, nunca que sea
imposible. Si la migración se rompe cuando la condición cambia, la condición se
comprueba DENTRO de la transacción, y si no se cumple se aborta con un mensaje
que diga qué decidir.

Señal para buscarlo: cualquier comentario en forma de fecha o de censo —
«hoy son 3», «ninguna org tiene», «actualmente vale 0». Cada uno de esos es un
`IF ... THEN RAISE EXCEPTION` que falta.

Relacionado: [[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
