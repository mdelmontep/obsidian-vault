---
title: comparar el código de error contra la salida del humanizador nunca casa
date: 2026-09-13
source: facturaia
tags: [errores, frontend, dead-code]
---

Si un helper convierte slugs de API (`not_found`) en frases para el usuario, `if
(mensajeDeFallo(err, '') === 'not_found')` es código muerto: el helper ya quitó justo el slug que
se compara. La rama del aviso específico («no existe o no tienes acceso») no se ejecuta nunca, y
ningún test lo ve porque el genérico también es un texto razonable.

Fix: discriminar por el código que viaja en el objeto de error (`err instanceof ApiError &&
err.code === 'not_found'`) y humanizar solo para pintar. Regla: **decidir con el código, pintar con
la frase**; nunca decidir sobre la salida de una función de presentación.

Caso real: pedido y presupuesto de Obras en TuFacturaIA, muerto desde el #2281 hasta el #2758.
