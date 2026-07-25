---
title: si el signo de una columna duplica información que ya está en otra, divergirá
date: 2026-07-25
source: claude-code-session
tags: [postgres, modelado, contabilidad]
---

`movimiento_factura_asignacion.importe_aplicado` sin convención escrita: el sentido del flujo ya vivía en `tipo` (cobro/pago), así que el signo era información redundante. Los caminos manuales insertaban positivo y el trigger automático el importe del movimiento crudo (negativo en pagos). 24 filas negativas, 2 orgs, y 22 movimientos mostrados como "Parcial" estando cubiertos al céntimo.

Se sostuvo latente porque ~30 funciones SQL sumaban con `SUM(ABS(...))`. Los 3 consumidores que no lo hacían eran justo los que pintaban el estado al usuario.

- Si el sentido está en otra columna, la magnitud va **sin signo** y se defiende con `CHECK (col > 0)`.
- El `ABS()` disperso en consumidores es el síntoma, no el fix: tapa en la UI un dato malo que el resto del motor sí ve.
- Al normalizar, el predicado que excluye filas conflictivas debe ser **réplica literal de los triggers** que validan el UPDATE, leídos de su `prosrc` en prod. Uno olvidado (el resto de factura, el guard de capacidad del movimiento) = migración abortada.

Ver [[abs-en-agregacion-monetaria-y-signo-de-importe]] si existe · nació en TuFacturaIA, ver [[facturaia]].
