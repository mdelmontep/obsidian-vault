---
title: pedir un valor nuevo en un enum cerrado suele ser una dimensión nueva disfrazada
date: 2026-08-06
source: claude-code-session
tags: [modelado, bd, producto]
---

Cuando piden «añade X a ese desplegable», comprueba antes si X responde a la
MISMA pregunta que los valores que ya están. Si no, meterlo destruye información
en silencio y contamina a todos los consumidores del campo.

- Caso TuFacturaIA: «que la forma de pago pueda ser pago de un tercero». Pero
  `forma_pago` responde a CÓMO se paga (transferencia, efectivo, confirming) y
  lo que pedían es QUIÉN pone el dinero. Un valor `pago_tercero` habría perdido
  el medio real de pago y, en facturas recibidas —donde ese campo es texto libre
  que rellena el OCR y alimenta el export contable y el 347—, habría falseado la
  columna que ve la gestoría.
- Test rápido: ¿puede un caso real tener a la vez el valor viejo y el nuevo?
  («transferencia» Y «la pagó su aseguradora» → sí). Entonces son dos ejes, no
  dos valores del mismo.
- Coste de equivocarse asimétrico: eje nuevo mal metido en un enum se arrastra a
  exports, declaraciones y datos históricos; eje separado de más es una columna
  nullable que no molesta a nadie.

Ver [[importe-fiscal-no-es-importe-a-cobrar-retenciones]]
