---
title: Mezclar UTC y local para "hoy" desincroniza cliente y servidor
date: 2026-07-25
source: claude-code-session
tags: [fechas, timezone, validacion, facturaia, sepa]
---

Dos preguntas distintas que se resuelven en relojes distintos, y confundirlas cuesta un bug:

- **"¿Qué día de la semana cae esta fecha?"** es un hecho absoluto. Se resuelve parseando `YYYY-MM-DDT00:00:00Z` y usando `getUTCDay()`, para que no dependa de la zona del servidor.
- **"¿Qué día es hoy?"** es una pregunta sobre el calendario del usuario. Va en hora local.

En FacturaIA, `hoyIso()` usaba `toISOString().slice(0,10)` (UTC) mientras la vista calculaba su mínimo con `new Date()` local. En España, entre las 00:00 y las 02:00, UTC marca todavía el día anterior. En esa franja:

- el servidor daba por futura una fecha de cargo que para el usuario era hoy, y aceptaba un adeudo el mismo día;
- la UI proponía un valor por debajo de su propio mínimo, así que el campo nacía inválido y el botón de generar salía bloqueado sin que nadie hubiera tocado nada.

Dos reglas que evitan la clase entera de fallo:

1. **Un solo origen para el mínimo.** Si la UI y el validador de servidor lo calculan por separado, tarde o temprano discrepan. Exportar una función (`minFechaCargo()`) y que la consuman los dos.
2. **Tests con invariantes, no con fechas fijas.** "La propuesta nunca queda por debajo del mínimo", iterando sobre varias fechas de partida y varias configuraciones. Un test con una fecha concreta pasa tan campante mientras el bug solo aparece dos horas al día.

Corolario para revisar código ajeno o propio: busca `toISOString()` cerca de cualquier cosa que se llame "hoy", "ahora" o "mínimo". Casi siempre está mal.

Ver [[facturaia-modulo-sepa-config]].
