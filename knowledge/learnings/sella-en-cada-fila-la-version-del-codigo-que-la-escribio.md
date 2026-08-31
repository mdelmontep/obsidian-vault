---
title: sella en cada fila la versión del código que la escribió
date: 2026-09-01
source: agency-portal
tags: [batch, deploy, llm, observabilidad]
---
Un lote asíncrono (Batch API: horas entre enviar y recoger) puede quedar **a
caballo de un despliegue**. El de las 20:30 salió con el prompt viejo; el de las
21:30, ya con el nuevo. Mismo cron, misma cola, dos versiones de código.

Sin sello no es contestable: «¿está reprocesado?» solo se responde mirando
`agent_evaluations.prompt_version`, que dice qué código produjo ESA fila. El
commit mergeado no vale — dice qué hay en `main`, no qué corría cuando se
construyó cada petición.

Y para saber qué código está vivo AHORA, el panel de deploys tampoco vale
(`done` es que el build terminó, no qué responde). Se mide en el artefacto:

    docker exec <ct> grep -rl "judge-2026-08-31.1" /app/.next   # sale → está vivo
    docker exec <ct> grep -rl "judge-2026-08-28.2" /app/.next   # no sale → ya no

Corolario: la constante de versión tiene que viajar al bundle, no quedarse en un
`package.json` que nadie compara. Ver [[agentesia]]
