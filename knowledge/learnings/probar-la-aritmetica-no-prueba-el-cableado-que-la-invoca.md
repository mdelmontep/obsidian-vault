---
title: probar la aritmética de una función pura no prueba el cableado que la invoca
date: 2026-08-17
source: claude-code-session
tags: [testing, mutacion, cobertura, metodo]
---
Cinco tests probaban `pendienteCobrable(...)` con números correctos. Dentro del DTO que la usa,
sustituir `yaCobradoEur: resumen.cobradoEur` por `yaCobradoEur: 0` **dejó los cinco en verde**: ninguno
ejecutaba la función que une la lectura del ledger con el cálculo. Y el mutante no era cosmético — el
pendiente ignoraría todo lo ya pagado y un CRM reclamaría la factura entera a quien ya la había saldado
(FIA #1850, `GET /v1/facturas/{id}`). Se cerró con un test de la **función real** con dobles en sus dos
lecturas de BD; la misma mutación pasa a dar 2 rojos.

Peor cuando lo cableado es **no-throw a propósito** (aditivo: "perder esto jamas debe romper la
operacion"). Ahí el cableado roto no produce ni un error: FIA #2232, `bulk-confirm` con
`select('movimiento_id')` en vez de `select('movimiento_id, categoria_id')` devuelve 200, confirma
las filas y no aprende ni una regla. El test tiene que afirmar sobre los **argumentos de la llamada**
—y sobre las columnas que la query pide, que son parte del cableado—, no sobre el resultado, porque
el resultado es éxito en los dos casos.

Corolario incómodo: extraer una función pura «para poder testearla» **mueve** el hueco, no lo cierra.
Ver [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] ·
[[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] ·
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
