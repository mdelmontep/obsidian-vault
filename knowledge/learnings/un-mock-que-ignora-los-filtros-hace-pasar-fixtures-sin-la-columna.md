---
title: un mock que ignora los filtros hace pasar fixtures a las que les falta la columna
date: 2026-08-23
source: facturaia
tags: [tests, supabase, mocks, refactor]
---
Mientras el criterio vive en el `.eq()` del servidor, el mock de Supabase encadena y
devuelve las filas **sin aplicar el filtro**. Resultado: las fixtures pueden no llevar
la columna por la que se filtra y los tests pasan igual — pasan por el motivo equivocado.

Caso real: mover el criterio de estado del `.eq()` a TS (para leerlo por el helper del
espejo) tiró 7 casos de golpe en `trial-ending-notice`; ninguna de sus 8 fixtures tenía
`billing_status`. El test no medía nada de eso y nadie lo sabía.

Dos consecuencias prácticas:
- **Mover un criterio de SQL a TS es un cambio de contrato de las fixtures.** Antes de
  tocarlo, grep de la columna en el fichero de tests: si no aparece, van a caer todas.
- **Lo vio solo el gate COMPLETO.** Correr los tests del área que tocas no basta: el
  fichero que rompes puede estar en otra carpeta. Ver [[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]].

Corolario: una fixture a la que le falta la columna del filtro es una fixture que miente,
aunque el test esté verde. Al añadir el campo, añadir también el caso que discrimina
(cuenta y espejo divergentes en los dos sentidos).
