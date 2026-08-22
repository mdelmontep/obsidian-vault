---
title: un catálogo de lo que un tercero soporta, escrito a mano, miente en silencio
date: 2026-08-22
source: facturaia
tags: [integraciones, gotcha, mantenimiento]
---

Cualquier lista nuestra de «qué cubre el proveedor» (divisas, países, idiomas, formatos, modelos)
nace correcta y se pudre sin que nada avise: el proveedor cambia su catálogo y nuestro comentario o
constante se queda igual. No hay test que lo cace, porque el test también se escribió a mano.

Caso real (TuFacturaIA, #2089): un comentario afirmaba que el BCE no publica «AED, MAD, ILS, KRW».
Consultado `GET /v1/currencies`, **ILS y KRW sí están cubiertas** y en cambio faltaba **BGN**, que
dejó de publicarse cuando Bulgaria entró en el euro en enero de 2026. La lista escrita a mano ya era
falsa por dos lados.

- **Preguntar al proveedor** por su endpoint de capacidades y cachear (12 h basta), en vez de
  declararlo.
- **Tres estados, no dos**: cubierto / no cubierto / **no lo sé** (el proveedor no contestó). Sin el
  tercero, un fallo de red se convierte en «no existe» — el mismo error de
  [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]].
- Un comentario que enumera capacidades de un tercero es deuda con fecha de caducidad invisible: o
  lo genera el código, o no se escribe.
