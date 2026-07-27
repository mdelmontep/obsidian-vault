---
title: un guard nuevo se mide contra los datos que ya existen, y su mensaje debe dar salida
date: 2026-07-27
source: claude-code-session
tags: [validacion, datos, ux, backend]
---

Al añadir una validación a un sistema con años de datos, **cuenta cuántas filas la violan
ya** antes de desplegarla. Una consulta de 30 segundos. Caso real: guard `vencimiento >=
fecha_factura`; en prod había 8 de 498 recibidas al revés, y no por capricho — el OCR había
leído mal la FECHA de la factura (fecha en el futuro, vencimiento el día de la subida).

Consecuencia: el guard es correcto pero **bloquea a quien intenta arreglar el dato**, porque
compara contra el campo que está mal. Si el mensaje no dice la salida, es un callejón. En ese
caso el campo erróneo era fiscal (decide el trimestre del 303) y no se corrige suelto: la
salida real era eliminar el documento y volver a subirlo. Eso hay que decirlo.

Corolario: **no dupliques la regla como `min`/`max` del control del cliente**. Ahí no hay
sitio para explicar nada: el usuario ve el selector limitado, no entiende por qué y no puede
ni intentarlo. Deja que el servidor la imponga y la explique con su 409.

Y no confundas el síntoma: si el guard salta mucho, sospecha del dato contra el que compara
antes que del dato que entra. Ver
[[staging-deja-de-ser-fuente-de-verdad-tras-el-commit-y-editarlo-no-cambia-nada]]
