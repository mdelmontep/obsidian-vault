---
title: convertir una dependencia inyectada en llamada global rompe el doble del test
date: 2026-08-16
source: claude-code-session
tags: [testing, diseño, tucrmia]
---
Al mover una capacidad a su propia puerta (`almacenDeFicheros()`), la forma cómoda es llamarla DENTRO
de la función que la necesitaba. Eso convierte una dependencia inyectada en una lectura global del
entorno, y el test que doblaba esa dependencia se queda sin nada que doblar.

**La señal es inconfundible y conviene reconocerla**: la prueba pasa a fallar con «faltan
credenciales» / «no hay conexión» en vez de con una aserción. Eso no es un test desactualizado — es el
módulo diciendo que ya no se puede probar sin las credenciales de verdad.

Fix: la puerta entra por **parámetro con valor por defecto** (`fn(db, abrir = puertaReal)`).
Producción no cambia una línea y la prueba sigue pudiendo mentirle.

Corolario para revisar diffs ajenos: un cambio que sustituye un parámetro por una llamada importada
casi siempre empeora la testabilidad aunque el diff parezca más limpio.
