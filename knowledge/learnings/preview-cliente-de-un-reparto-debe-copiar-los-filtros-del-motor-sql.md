---
title: la previsualización cliente de un reparto debe copiar los filtros del motor sql, no solo su orden
date: 2026-07-29
source: claude-code-session
tags: [frontend, sql, stock, facturaia]
---
Cuando la UI previsualiza lo que hará una función SQL (repartir una cantidad entre lotes, asignar saldos, aplicar pagos), copiar el ORDEN no basta: hay que copiar también los FILTROS de la query del motor. Si el endpoint que alimenta la UI devuelve filas que el motor descarta, la previsualización promete algo que la ejecución no cumple y el usuario ve un error donde la pantalla decía que todo cuadraba.

Caso TuFacturaIA (#1347, reparto FEFO de partidas): `planReparto` en cliente replica el orden de `aplicar_movimientos_lotes` (mig 388) — caducidad asc, entrada asc — y filtra `cantidad_actual > 0`. Pero la función SQL filtra además `coalesce(activo, true) = true`, y `GET /api/stock/lotes` devuelve también las partidas archivadas (ordena `activo desc` en vez de excluirlas). Con una partida archivada con stock, el "disponible en total" y los tramos que se enseñan son optimistas y al emitir salta `sobreventa_lote`.

Regla: al escribir el espejo, abre la query del motor y traslada su `where` entero, no solo su `order by`. Y si el endpoint es compartido, filtra en el consumidor. Ver [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]] · [[auditar-un-lado-de-par-simetrico-revisar-el-espejo]]
