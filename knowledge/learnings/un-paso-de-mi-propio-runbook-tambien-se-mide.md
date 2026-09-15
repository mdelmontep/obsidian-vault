---
title: un paso que yo mismo escribí también hay que medirlo contra la env real
date: 2026-09-15
source: agh-iberica
tags: [sesgo, runbook, produccion, verificacion]
---
Escribí el guion de una operación en prod y uno de sus pasos —«el primer login del
usuario deja su correo en el log, de ahí lo sacamos»— era FALSO. Con la env real medida,
ese login sale `unknown`, y `unknown` es precisamente la rama que no registra ni correo
ni `oid`. El alta manual, la alternativa obvia, habría creado una fila nueva en vez de
vincular la que ya existe: justo el bug que la operación venía a arreglar.

El sesgo: las premisas de un brief ajeno se re-miden por costumbre; las de un texto
propio se leen como conocidas. Un runbook recién escrito es una hipótesis con la misma
caducidad que cualquier otra, y encima nadie más lo va a revisar.

Fix: antes de dar un guion por bueno, medir contra la env de prod el paso del que depende
todo lo demás (aquí: qué env vars están puestas y qué rama del código alcanzan). Un
comando de lectura.

Ver [[las-afirmaciones-de-mi-brief-van-como-hipotesis]], [[fijar-un-valor-no-es-verificarlo]].
