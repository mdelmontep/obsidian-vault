---
title: n8n — un nodo sin items de entrada no corre y corta la cadena hasta el aviso
date: 2026-09-09
source: simarro
tags: [n8n, observabilidad, alertas, simarro]
---
Cadena `Plan → A escribir → Escribir → Aviso → Slack`. El día que no hay nada que escribir —el caso
**normal** de un sync— `A escribir` emite 0 items, `Escribir` no se ejecuta, y con él **tampoco se
ejecuta el nodo de aviso**: el sync corre en verde y en silencio para siempre, incluida la rama que
debía gritar "me he bloqueado por fail-closed".

Dos reglas al montar un aviso al final de una cadena n8n:

1. **El nodo que abre la cadena del aviso emite siempre al menos un item** aunque sea inocuo (aquí un
   GET de ping). "Cero items" no es un camino, es una cadena rota.
2. **El nodo que avisa no lleva `onError: continueRegularOutput`.** Un nodo con esa bandera no marca
   la ejecución como fallida, así que el `errorWorkflow` global **nunca dispara** — si el aviso falla,
   nadie se entera de nada. El nodo de aviso debe fallar ruidosamente y dejar que lo cace el Error
   Handler.

**Y al revés (10-sep):** ese mismo comportamiento es la forma limpia de **callar** un aviso sin meter
un IF. Con el cron cada 5 min, avisar de "sin novedades" son 288 mensajes/día que entierran las
incidencias reales. El nodo de aviso hace `if (todo_ok) return [];` y el de Slack no llega a
ejecutarse. La regla 1 sigue en pie: se calla cuando NO hay nada que contar, nunca cuando la cadena
podría estar rota — habla siempre si el fail-closed bloqueó o si se planificaron N y salieron menos.

Ver [[un-nodo-de-log-con-onerror-continue-puede-no-haber-escrito-nunca]] · [[n8n-error-handler-global-via-errorworkflow]] · [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]]
