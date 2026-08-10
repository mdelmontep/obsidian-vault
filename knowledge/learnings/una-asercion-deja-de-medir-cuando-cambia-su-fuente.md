---
title: una aserción no falla cuando cambia su fuente: deja de medir, y eso no se ve
date: 2026-08-10
source: claude-code-session
tags: [testing, sql, migraciones, arnes]
---
Al cambiar de dónde lee un agregado (de `activity_events` a `product_events`), la aserción que
comprobaba «una organización de prueba no cuenta como activa» **pasó de proteger a no medir nada**:
seguía sembrando la tabla vieja, así que el agregado ya no se movía.

El modo de fallo es peor que un rojo: la aserción sigue ahí, se lee igual, y quien la mire dirá que la
exclusión está probada. Sólo se cayó porque el recuento no cuadraba; con otra forma habría quedado verde.

**Regla**: cambiar la FUENTE de un agregado obliga a revisar toda aserción que la siembre, no sólo las
que la nombren. Grep por la tabla vieja, no por la función.

Y el hermano, del mismo día: renombrar una columna de una función consumida dejó **1.767 tests en verde
con el contrato ya roto**, porque el doble del test devolvía la forma vieja. Un doble no puede ver que un
contrato cambió — eso sólo lo ve ejecutar contra la base de verdad (`db:replay`, migraciones sobre un
Postgres desechable). Ver [[cambio-en-shape-compartido-grep-todos-los-consumidores]].
