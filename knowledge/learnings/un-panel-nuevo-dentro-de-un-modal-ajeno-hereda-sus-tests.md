---
title: un panel nuevo dentro de un modal ajeno hereda sus tests, y su mock genérico
date: 2026-08-26
source: facturaia
tags: [react, testing, blast-radius, componentes]
---
Montar un panel nuevo dentro de una ficha que ya existe (el casador de albaranes
dentro del modal de una factura recibida) mete tu componente en TODAS las suites
del padre. Esas suites mockean `fetch` de forma genérica y devuelven `{}`, así
que `data.propuesta.pares` reventó en el `useMemo` y tumbó la ficha entera:
8 tests rojos en ficheros que no hablaban de albaranes.

El fallo real no es de test: en producción, un cuerpo inesperado de TU endpoint
deja al usuario sin ver la factura. Regla: **un panel injertado se calla y
desaparece, nunca tumba a su anfitrión.** Guarda de forma antes de usarla
(`if (!Array.isArray(json?.propuesta?.pares)) { setData(null); return }`) y
encadenamiento opcional en los derivados.

Corolario de diagnóstico: si al añadir un componente se ponen rojos tests de
otra feature, no busques el bug en tu feature — busca dónde te han montado.
Ver [[gate-por-git-ls-files-no-ve-un-fichero-nuevo-sin-git-add]].
