---
title: el parche que hizo el usuario atascado dispara el guard del arreglo que lo desatasca
date: 2026-08-01
source: claude-code-session
tags: [producto, postgres, guards, soporte]
---
Al arreglar un callejón sin salida, mira **qué hizo el usuario mientras estaba atascado**: su
apaño suele quedar en los datos y activar el guard nuevo, dejándolo fuera del arreglo.

Caso TuFacturaIA (ticket nº130, mig 620): una recibida con entrada de stock no se podía borrar
(«deshaz el movimiento de stock», operación inexistente). El fix revierte el inventario y solo
bloquea si el reverso deja saldo negativo. Pero el usuario, 41 min después de aprobar, había metido
un **ajuste manual de −2** para dejar la partida a cero: el guard lo leyó como consumo real y
bloqueó **su propia factura**. El parche que la app le obligó a hacer era el candado.

- Línea correcta: un movimiento **con documento** (venta, salida de obra) prueba que la mercancía
  salió; un **ajuste suelto sin documento** solo dice que alguien cuadró a mano. El reverso se lleva
  los ajustes sin documento que cuelgan de lo que se revierte (neutro: +2 y −2 se anulan).
- Verificarlo **con la fila real del ticket**, no con un caso de laboratorio: el fix pasaba todos los
  tests y fallaba justo en el caso que lo motivó.
- Y comprobar al **mismo grano que el código**: yo miré el saldo por producto (positivo) cuando el
  guard mira también por partida (−2). Ver [[smoke-trigger-sql-tx-rollback-contra-prod]].
