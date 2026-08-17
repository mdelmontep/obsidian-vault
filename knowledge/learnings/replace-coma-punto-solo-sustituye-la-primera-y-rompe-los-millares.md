---
title: replace(',', '.') solo sustituye la primera coma y parte el importe por los millares
date: 2026-08-17
source: claude-code-session
tags: [parsing, decimal, dinero, gotcha]
---

`String.replace` con un string (no regex global) cambia **solo la primera** ocurrencia.
Para parsear un importe en formato ES eso significa que `"3.060,50"` se queda en
`"3.060.50"` → `Number(...)` da **3.06**. No lanza, no avisa: guarda un precio mil veces
menor y sigue.

Es el hermano del bug contrario, ver
[[csv-import-precio-decimal-es-us-desambiguar-no-asumir]]: allí se limpian los puntos
asumiendo millares; aquí se sustituye la coma sin quitarlos.

**Fix**: el helper del proyecto (`parseNumeroEs`, y `parseNumeroEsStrict` cuando el valor
se PERSISTE — distingue el caso ambiguo en vez de resolverlo solo). Nunca parseo a mano
en el componente.

**Detección**: `grep "replace(',', '.')"`. Si el repo tiene un guard que lo prohíbe (en
TuFacturaIA, `parser-importes-unico.test.ts`), el guard vive fuera de la carpeta del PR y
un gate filtrado no lo corre — ver
[[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]].

Caso real: panel de complementos de TuFacturaIA (#1714), cazado al cerrar la tanda (#1869).
