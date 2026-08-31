---
title: una clave nueva en el json de una RPC no llega a nadie hasta que un test la exige
date: 2026-08-31
source: facturaia
tags: [testing, api, notificaciones, candados]
---

Añadir un dato al `jsonb_build_object` de una RPC **no lo conecta con nada**. La
migración se aplica, el dato existe, y entre la RPC y la pantalla hay 3-5
eslabones que hay que tocar a mano. Nadie avisa: no hay error, hay silencio.

En FacturaIA `recibida_eliminar` devolvía `albaranes_reabiertos` desde su
migración y **ningún consumidor lo leía**: al borrar la factura, el albarán
volvía a «abierto» sin decírselo a nadie. Se descubrió leyendo el manual que
alguien había escrito afirmando que el aviso lo mostraba.

El candado que falta casi siempre es el del **cuerpo de la respuesta**: los tests
de la ruta comprobaban estado 200 y los errores, y ninguno miraba las claves del
body, así que un renombrado pasaba en verde. Un test por clave que la UI use.

Dos trampas del último eslabón, las dos MUDAS (que es peor que ruidosas):
`Number(x)` sin sanear da `NaN`, y `NaN > 0` es `false`, así que el aviso
desaparece justo cuando el cuerpo viene mal. Y una rama de **éxito parcial**
que redacta su propio texto se queda fuera de la que sí lo pone: si el dato es
una ACCIÓN pendiente, hay que buscar todas las ramas que avisan, no solo la feliz.
