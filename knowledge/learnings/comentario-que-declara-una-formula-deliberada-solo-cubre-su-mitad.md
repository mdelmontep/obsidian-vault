---
title: un comentario que declara "esto es deliberado" solo cubre el caso que su autor tenía delante
date: 2026-07-28
source: claude-code-session
tags: [metodo, bugs, documentacion, facturaia]
---

Una línea compartida por dos tipos de entidad, documentada como intencionada para
uno de ellos, es un bug con coartada para el otro. Y la coartada es lo que impide
que nadie lo mire.

Caso real (TuFacturaIA): el editor rápido del listado calculaba
`total = base*(1+iva−irpf)`. La migración que crea `importe_cobrable` **señala esa
línea por número** y explica que ahí el total se guarda neto a propósito. Cierto,
pero solo para RECIBIDAS: la misma línea servía también a emitidas, donde `total`
es el importe fiscal bruto que firma VeriFactu, y le restaba la retención por
segunda vez. El comentario llevaba meses convirtiendo el bug en contrato.

Señal para detectarlo: un comentario que justifica una fórmula nombrando UN tipo,
UN estado o UN flujo, sobre código que no discrimina ninguno de los tres. Si la
justificación es más específica que el `if` que la protege, falta el `if`.

Corolario, del mismo caso: el manual de usuario describía el comportamiento CON el
bug ("el total que aparece en la factura es 1.060") y el de admin se contradecía
consigo mismo entre dos páginas. Documentar un comportamiento no lo valida; al
arreglar, hay que grepear la doc, que también lo afirmaba.

Es la versión en código del tripwire de `~/.claude/CLAUDE.md`: cuando la respuesta
a "¿esto está bien?" es "es por diseño", valida el RESULTADO antes de cerrar.

Ver [[estar-en-el-catalogo-de-crons-no-es-estar-programado]] ·
[[antes-de-tocar-un-ticket-mira-si-otra-sesion-ya-lo-esta-cerrando]]
