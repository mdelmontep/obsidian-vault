---
title: un cambio de env no está verificado hasta que el servicio se comporta distinto
date: 2026-07-26
source: claude-code-session
tags: [dokploy, deploy, env, verificacion, secretos]
---

"Contenedor recreado + logs limpios" NO prueba que el env nuevo esté dentro. Prueba que
arrancó. Si el guardado en el panel se revierte, se aplica a otra app o se pierde, el
servicio sigue levantando igual de limpio con el env VIEJO.

Caso real (agency-portal, 22→26 jul): se dio por aplicada una reestructuración de
`TIME_TRACKER_KEYS` con esa evidencia, y se anotó como hecha en 1Password y en el hub.
Tres días después, al reinstalar el hook, la key nueva daba 401. La vieja seguía
mapeando al member original: el cambio nunca entró. Coste = media hora persiguiendo un
fantasma, más una clave buena destruida por el camino.

Regla: la verificación es una llamada que devuelva el EFECTO del cambio, no su síntoma.
Aquí, `POST /api/internal/time-ingest` devuelve `{"member": ...}` → un `curl` dice en un
segundo bajo qué identidad entra cada clave. Si el endpoint no expone el efecto, ese es
el arreglo previo: exponerlo.

Corolario para las notas: escribir "aplicado y verificado" sin decir CON QUÉ se verificó
convierte la nota en una afirmación no auditable. Guarda el comando y su salida esperada.
Ver [[actions-sin-billing-hooks-locales-unico-gate]].
