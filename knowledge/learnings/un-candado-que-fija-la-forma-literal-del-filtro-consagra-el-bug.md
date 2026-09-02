---
title: un candado que fija la forma literal del filtro consagra el bug
date: 2026-09-02
source: facturaia
tags: [testing, candados, sql, mutacion]
---
Caso mig 792→803: `and l.cantidad > 0` en los agregados de stock dejaba fuera el
abono ENTERO (todas sus líneas son negativas por construcción). Tres candados en
verde durante la regresión; un canario de negocio la cazó en 5 min.

- **Fijar la forma literal consagra el bug**: el espejo exigía `and l.cantidad > 0`
  con regex — al corregir el bug, el candado se puso rojo defendiendo la forma rota.
  Candar el CRITERIO (signo canónico por tipo de documento), no el texto que hay hoy.
- **Vigilar el bucle no ve la puerta**: el test del espejo del ledger miraba el LOOP;
  el filtro mataba las filas antes de entrar. Candar también el predicado de entrada.
- **Match sobre fichero crudo casa con tus comentarios**: la cabecera que citaba la
  forma vieja daba el `>=1` del test. Quitar comentarios (`sinComentarios`) antes de
  contar ocurrencias, y verificar el candado por mutación (retirar la mig → rojo).
