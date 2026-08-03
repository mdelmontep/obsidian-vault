---
title: un fixture de bytes fijos contra deduplicación por contenido es un test de un solo uso
date: 2026-08-03
source: claude-code-session
tags: [e2e, testing, fixtures, idempotencia, facturaia]
---

El smoke de importar factura genera el **nombre** único por ejecución
(`E2E-IMPORT-${Date.now()}.pdf`) pero sube siempre el **mismo buffer**. El
servidor deduplica por contenido, así que la segunda vez responde 409 y el modal
lo salta: «1 duplicada omitida».

El nombre único da falsa sensación de aislamiento. Lo que decide es el eje por
el que deduplica el sistema, no el que tú variaste.

**Y el teardown no salva:** solo borra si el test llegó a capturar los ids. Como
falla en el paso del alta, no borra nada — el rastro que lo rompe es justo el
que su limpieza no alcanza. Bastó una fila huérfana de una sesión anterior
(cuyo smoke murió antes del teardown) para dejarlo rojo de forma permanente.

**Fix:** variar el contenido por ejecución, no solo el nombre. Y comprobarlo
como se comprueba la idempotencia: **correr el test dos veces seguidas**. Un
test que solo pasa la primera vez es indistinguible de uno correcto hasta que
alguien repite.

Ver [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]]
