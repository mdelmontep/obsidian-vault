---
title: Retell omite los campos apagados, y un guardián por JSON.stringify da falso rojo
date: 2026-09-07
source: elphis-psicologia
tags: [retell, guardianes, gotcha, agentes-voz]
---
Poner `ambient_sound: null` en un agente de Retell no deja el campo a `null`: **Retell lo omite
del objeto**. Un guardián que compara repo contra desplegado con
`JSON.stringify(a) === JSON.stringify(b)` ve `"null"` contra `undefined` y se pone rojo sin que
nada esté mal.

Fix: normalizar los dos lados (`a ?? null`), **no** borrar el campo de la lista vigilada.
Borrarlo es lo natural y es justo la regresión: un clic en el panel devuelve el valor y ya no
se pone rojo nada. Tras relajar la comparación, **probar que sigue mordiendo** con una mutación
en cada dirección — aquí, `null → 'call-center'` y `flash → eleven_v3`, las dos con víctima.

La simétrica en n8n: **quitar `errorWorkflow` no muta nada**, porque n8n conserva el valor de
una clave que no viaja en el PUT. Misma clase de fallo, signo contrario — allí la mutación sale
sin víctima con el guardián sano.

Ver [[publicar-un-agente-no-basta-el-numero-puede-fijar-su-version]] · [[copiar-la-config-de-un-agente-vivo-copia-una-version-que-sigue-moviendose]]
