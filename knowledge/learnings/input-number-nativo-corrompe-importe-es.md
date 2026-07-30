---
title: "input type=number nativo corrompe importes en formato español, en silencio"
date: 2026-07-30
source: auditoría funcional total TuFacturaIA
tags: [frontend, importes, i18n, facturaia, p0]
---

`<input type="number">` no rechaza un importe español con separador de miles: lo **descarta a
trozos**. Teclear `1.234,56` deja `1.23456` en el `.value`.

El navegador acepta `1.234` como número válido (mil doscientos treinta y cuatro **milésimas**),
después tira la `,` porque en su locale no es decimal, y concatena `56`. No hay evento de error,
no hay `:invalid`, no hay nada que avisar: la validación nativa está contenta porque el resultado
sí es un número.

Caso real (FacturaIA, `src/components/ui/number-field.tsx`): factura **A2026-0177** emitida con
base 1,23 € y total 1,49 € en vez de 1.234,56 €, persistida en `lineas_factura.precio_unitario`
y registrada en VeriFactu. Afectaba también a cantidad y a descuento, por ser la misma casilla
compartida. El modal de confirmar emisión no muestra el importe, así que no había ningún punto
de corte entre teclear y firmar fiscalmente.

Detalle que acota la causa: **sin** separador de miles (`12,50`) el navegador sí interpreta la coma
como decimal. El fallo es específico de miles+coma.

## Lo que de verdad hay que llevarse

Una auditoría anterior mirO este mismo sitio y lo descartó con este comentario en el código:

> «verificado NO peligroso — `input` es `type="number"`, su `.value` nunca lleva coma ni separador
> de miles (lo sanea el propio navegador)»

La premisa es cierta y la conclusión falsa: el navegador **sanea descartando**, no rechazando. Que
un valor llegue "limpio" no significa que llegue **correcto**. Cuando el razonamiento para descartar
un riesgo es "ya lo normaliza la plataforma", hay que comprobar **a qué** lo normaliza, con el dato
real en la BD, no con el tipo del input.

Corolario del [[feedback_evidencia_antes_de_hipotesis]]: un `type="number"` no es un guard de
formato, es un guard de *sintaxis*. Para importes con locale, el parseo es de la app.

Ver [[put-objeto-completo-borra-campos-no-mapeados]] para el otro patrón de corrupción silenciosa
en el que la plataforma "ayuda" y te borra datos.
