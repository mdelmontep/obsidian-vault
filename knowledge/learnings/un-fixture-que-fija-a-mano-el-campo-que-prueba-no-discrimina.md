---
title: un fixture que fija a mano el campo que prueba da verde sobre el bug que dice cubrir
date: 2026-09-20
source: facturaia
tags: [testing, fixtures, facturaia]
---
El fixture se llamaba `f08-rectificativa-cross-period.json` y su descripción decía, literal, «NO
recalcula T1: el abono entra en T3». Exactamente el comportamiento que se rompió. No lo cazó
porque el propio fixture ponía a mano `fecha_operacion` igual a `fecha`: fabricaba el mundo en el
que el bug no puede ocurrir y luego comprobaba que no ocurría.

El tell: un fixture que **fija el valor del campo cuya derivación es lo que se quiere probar**.
Si el sistema real deriva ese campo, el fixture tiene que dejar que lo derive, no dárselo hecho.

Y el nombre engaña doble: un fichero llamado `cross-period` se lee como cobertura de ese caso en
cualquier auditoría posterior, así que tapa el hueco además de no cubrirlo. Comprobarlo con
`~/.claude/bin/mutate`: si al invertir la regla el fixture sigue verde, no prueba nada.
