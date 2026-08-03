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

**Corregido el mismo día: «falta un barrido de caducidad» era el diagnóstico
equivocado.** Un barrido por antigüedad habría cerrado también avisos
legítimamente vivos, y la causa no era que envejecieran: era que a esa clase le
faltaba **dueño**. Se vio mirando el ciclo de vida por origen —`select source,
count(*) filter (where resolved_at is null), avg(resolved_at - created_at) …
group by source`—: `health-sweep` cerraba en 2,7 h y `ocr-process` en 21,5 h con
0 abiertas, y `resolve-ia` acumulaba 3 porque **no tenía ni una llamada a
resolve en todo el repo**. El arreglo son los caminos de cierre reales (un
reintento que va bien, el cierre del ticket), no un temporizador. Y el tope del
panel que escondía las viejas sin decirlo, aparte.

Casos: `ocr-process:502:<org>` de un `bandeja_ingesta` ya borrado (4 días) y
`resolve-ia:job_fallido:*` (15 cerradas a mano, 3 colgadas). PRs #1495 y #1496.
Ver [[4xx-que-culpa-al-archivo-no-es-caida-del-pipeline]] ·
[[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]] ·
[[alert-collector-cron-vs-live-dedup-gap]]
