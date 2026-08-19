---
title: ADR-055 — la autoliquidación rectificativa del 303 va detrás de capturar el justificante, no delante
date: 2026-08-19
status: accepted
tags: [adr, facturaia, fiscal]
---

## Contexto
El ciclo de la rectificativa (art. 74 bis RIVA) está en el esquema de TuFacturaIA desde la mig 146
(`es_rectificativa`, `declaracion_rectificada_id`, estados `rechazado`/`rectificada`) y **nada lo
escribe**: la base le dice al usuario «corrige vía rectificativa» y la app no tiene dónde. Issue #1899.

## Opciones consideradas
- **A — Generar la rectificativa** (fila nueva, recálculo, fichero con la marca del modelo). Es lo que
  promete el nombre, pero la posición 427 del diseño oficial es el **nº de justificante de la
  autoliquidación anterior, 13 caracteres**, que asigna la AEAT al presentar en la Sede: no se deriva
  de las facturas.
- **B — Solo registrar** lo presentado fuera (justificante, CSV, aceptada/rechazada) en `resultado_aeat`,
  que existe y está vacía. Barato, cierra el agujero de datos y el rechazo que hoy cuenta como válido.
- **C — Nada, y que la app no lo prometa.**

## Decisión
**B primero y A después**, porque B no es la alternativa barata a A: es su dato de entrada. Y delante de
las dos, el bug #1933 (marcar presentada borra el sello eIDAS y el puntero WORM). Orden: #1933 → #1934 →
#1899. A queda bloqueada por falta de payload real (0 presentaciones en prod) y porque el 303 ordinario
aún no está validado en el sandbox Pre303.

## Consecuencias
Hasta que B esté, la app **no ofrece** «crear rectificativa» en ningún sitio (era el menú «⋯» retirado
en el #1894). La rectificativa será fila nueva con su propio fichero y su propio sello: el objeto WORM
de la original no se toca nunca. Ver [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]].
