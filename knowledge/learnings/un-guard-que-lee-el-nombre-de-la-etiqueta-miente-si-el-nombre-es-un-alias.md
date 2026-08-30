---
title: un guard que lee el nombre de la etiqueta miente si ese nombre es un alias
date: 2026-08-30
source: facturaia
tags: [tests, guards, arnes, frontend]
---
Un trinquete que busca `<Icon ... size={12}>` cree estar hablando del componente propio, pero en JSX
el nombre de la etiqueta es **una variable local**, no una identidad. Cualquiera puede escribir
`const Icon = otraCosa` y el guard seguirá exigiéndole nuestra convención a un componente ajeno —
y peor: la corrección que el guard pide puede ser justo lo que lo rompa (caso real: pasar de
`size={14}` a `size="sm"` sobre un icono de lucide, #2289).

Regla: si un guard discrimina por nombre de etiqueta, hace falta un **segundo guard que reserve ese
nombre** (grep de `(const|let) <Nombre> *=` fuera del módulo dueño). Sin él, el primero no vigila lo
que dice vigilar. Mismo patrón que [[el-candado-audita-la-clase-no-la-lista-que-alguien-escribio]].

Y el corolario de siempre: probarlo al revés con `mutate`, que es lo único que distingue un guard con
dientes de uno decorativo.
