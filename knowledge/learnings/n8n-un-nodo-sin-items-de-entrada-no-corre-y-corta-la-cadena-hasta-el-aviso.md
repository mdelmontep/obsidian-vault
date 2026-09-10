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

Ver [[un-nodo-de-log-con-onerror-continue-puede-no-haber-escrito-nunca]] · [[n8n-error-handler-global-via-errorworkflow]] · [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]]
