---
title: Playwright imprime la línea donde se declara el test, no donde falla
date: 2026-07-28
source: TuFacturaIA — conciliacion-ciclo, PR #1304
tags: [testing, playwright, e2e, debugging]
---

El reporter `list` de Playwright escribe `fichero:línea:col` junto al título del
test, y esa línea es la de la **declaración** (`test('...')`), no la de la
aserción que revienta. Sale igual en verde y en rojo.

`conciliacion-ciclo:172` estuvo varias sesiones apuntado como "falla en la 172,
sin causa conocida". La 172 era el `test('4. 047 ciclo real…')`. Nadie miraba
el mensaje, que es lo único que dice qué aserción cayó.

**Regla**: ante un fallo de Playwright, leer el mensaje del error, no la línea
del encabezado. Si el apunte de un fallo solo tiene un número de línea y esa
línea es un `test(`, el apunte no contiene información todavía.

Corolario del mismo caso: un test que toma "el primer elemento" de una lista
ordenada por fecha es un test cuyo sujeto lo elige el residuo de la tanda
anterior. Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]].
