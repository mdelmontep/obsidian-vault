---
title: Un backfill se guarda por el INVARIANTE, no por el síntoma que lo delata
date: 2026-08-12
source: claude-code-session
tags: [sql, migraciones, datos, facturaia, patron]
---

Caso: `activar_lotes_producto` creaba la partida de stock sin su apunte en el ledger, y desde que el
ledger es la única fuente del saldo, el primer `recompute_lote` la habría puesto a 0.

El backfill obvio era «a toda partida sin movimiento `apertura`, insértale uno». **Habría corrompido
106 de 115 partidas en producción**: esas ya tenían su entrada en el ledger con otro tipo (la
`compra` del documento que las creó), así que el apunte extra les habría **duplicado** las unidades.

Lo que discrimina no es el síntoma («no tiene apertura») sino el invariante que hace la operación
neutra:

```
cantidad_inicial + Σ(movimientos) = cantidad_actual
```

Solo donde eso se cumple, insertar una apertura de `cantidad_inicial` hace que el ledger reproduzca
**exactamente** el saldo que la fila ya tiene: no se crea ni se destruye nada. Medido: 9 lo cumplen,
106 no (y no lo necesitan), 0 quedan en un tercer estado. Lo que no cuadra por ninguna vía se deja
intacto y se **nombra** con `RAISE WARNING`, nunca se arregla a ciegas.

Método que lo sacó, y es repetible: escribir la migración, ejecutarla contra producción dentro de
`BEGIN … ROLLBACK` midiendo **antes y después dentro de la misma transacción**, y comprobar el
residuo a 0 al salir. Ahí se vio el 106 y se vio también que ningún saldo, stock ni coste se movía.

Dos preguntas que hay que hacerse antes de un backfill de ledger, porque cualquiera de las dos lo
convierte en incidente:
- **¿Hay triggers en la tabla?** (`pg_trigger`) Insertar puede disparar proyecciones.
- **¿Alguna función deriva algo de esas filas?** Aquí `recompute_pmp` acumula TODOS los movimientos
  en su stock corriente aunque solo pondere las compras, así que el apunte nuevo cambia el precio
  medio calculado. La migración no lo llama: cambiar precios de coste no se cuela en un arreglo de
  ledger.
