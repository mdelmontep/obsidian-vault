---
title: una alerta que se cierra «cuando vuelva a funcionar» se queda abierta para siempre si su sujeto desaparece
date: 2026-08-03
source: claude-code-session
tags: [observabilidad, alertas, dedupe]
---
El patrón habitual de alerta autosanable es: emitir con `dedupe_key` al fallar y
resolver cuando el mismo camino vuelve a pasar OK. Tiene un agujero: si el
sujeto del fallo desaparece (la fila que se iba a reprocesar se borra, la org se
queda sin volumen, el recurso se retira), **nadie vuelve a pasar por ese
camino** y la alerta se queda abierta indefinidamente. No es un falso positivo
que se vaya solo: hay que resolverla a mano, y mientras tanto ensucia el panel y
entrena al equipo a ignorarlo.

Al revisar un panel de incidencias, la antigüedad es la pista: una alerta
«autosanable» de hace días no significa que el fallo siga vivo, significa que su
cierre depende de un evento que ya no va a ocurrir.

Falta el barrido de caducidad (resolver por antigüedad, o al borrar el sujeto).
Caso: TuFacturaIA, alerta `ocr-process:502:<org>` de un `bandeja_ingesta` ya
borrado, 4 días en `/admin/alerts`. Ver
[[4xx-que-culpa-al-archivo-no-es-caida-del-pipeline]] ·
[[alert-collector-cron-vs-live-dedup-gap]]
