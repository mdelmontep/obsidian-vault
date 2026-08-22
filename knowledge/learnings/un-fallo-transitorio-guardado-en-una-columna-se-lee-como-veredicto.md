---
title: un fallo transitorio guardado en una columna se lee después como veredicto
date: 2026-08-21
source: facturaia
tags: [resiliencia, diseno-datos, ocr, integraciones]
---

Al pedir un dato a un tercero hay fallos **transitorios** (caído, 429, timeout) y **permanentes** (el dato no existe para esa clave). Si los dos se escriben con el mismo veredicto en la fila, nada distingue lo que se arregla reintentando de lo que no, y nada reintenta nunca.

Caso real (TuFacturaIA, ago-2026): el proveedor de tipos de cambio falló unos segundos y ese "no hay tipo" quedó escrito en `bandeja_ingesta.tipo_cambio_fuente`. Cinco causas distintas —caído, 429, timeout, fecha no ISO y divisa sin cobertura del BCE— acababan las cinco como `manual_requerido` con `tipo_cambio=1`. 22 de 26 filas congeladas en el **mismo minuto** (ráfaga concurrente sobre el mismo par sin deduplicación en vuelo + memo negativo de 60 s propagando un solo tropiezo), y 24 facturas en dólares contadas como euros: 274,82 € falsos.

- **Un enum, no un booleano**: el estado debe decir *por qué* falló. Y guardar el porqué, o no guardar nada.
- **Todo estado transitorio necesita quien lo deshiele**: barrido que reintente, abra incidencia si falla y **la cierre sola** en la primera pasada limpia. Sin barrido, "temporal" significa "permanente y silencioso".
- **Reintentar en el momento de decidir no basta** (#2020, 21-ago): un reintento al aprobar no descongela lo que nadie aprueba — 26 filas siguieron rotas un día más hasta el barrido de #2089.
- **El valor de relleno pinta el bug en pequeño**: con `tipo_cambio=1` la interfaz mostraba "7,90 AED · ≈ 7,90 €". Un centinela no se multiplica; se comprueba antes de usarlo.
- Un mensaje de bloqueo nunca puede señalar a una acción que la interfaz no ofrece.

Ver [[un-catalogo-de-capacidad-de-un-tercero-escrito-a-mano-miente-en-silencio]] · [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]]
