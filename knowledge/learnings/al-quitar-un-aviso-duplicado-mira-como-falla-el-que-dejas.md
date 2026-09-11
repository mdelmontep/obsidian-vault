---
title: al quitar un aviso duplicado, mira cómo falla el que dejas
date: 2026-09-11
source: laserys-las-rozas
tags: [alertas, observabilidad, n8n, fallos-silenciosos]
---

Un mismo incidente llegaba dos veces a Slack: el error handler del cliente posteaba en el
canal **y** reenviaba al bot central de la agencia, que volvía a postear y además mandaba el
correo. Borrar el aviso local parece lo obvio — hasta mirar el nodo que se queda: el reenvío
tenía `onError: continueRegularOutput`, así que si el bot central no responde el handler
termina **en verde y sin avisar a nadie**. Deduplicar habría convertido dos avisos en cero.

**Patrón**: en un fan-out de alertas, los caminos se tapan los fallos entre ellos. Al dejar uno
solo, ese uno pasa a ser punto único: comprueba **cómo falla** antes de quitar el otro.

**Fix aplicado**: el reenvío pasa a `continueErrorOutput` + `retryOnFail`, y el aviso local
cuelga de su **rama de error** con el texto «el bot de incidencias no responde». Uno en el caso
normal, uno también cuando el que manda se cae. Verificado provocando un error real y contando
los mensajes del canal, no leyendo el grafo.

Relacionado: [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] ·
[[pipeline-async-solo-notifica-camino-feliz-deja-fallo-silencioso]]
