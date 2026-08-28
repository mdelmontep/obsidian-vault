---
title: un cron que tira la respuesta a /dev/null no vigila nada
date: 2026-08-28
source: agency-portal
tags: [crons, ops, observabilidad, dokploy]
---

Doce crons de Dokploy con la forma `curl -s -X POST … >/dev/null`. Todos verdes. El
runner del portal (`runInternalCronRoute`) devuelve **207 Multi-Status** cuando la
corrida termina con fallos parciales — y 207 no es error para `curl`, ni siquiera con
`-f`, que solo mira ≥400. Resultado: una corrida a medias es indistinguible de una
limpia, para siempre.

El patrón correcto captura el código y lo compara con lo que se espera de verdad:

```bash
code=$(curl -s -o /tmp/x.json -w '%{http_code}' -X POST … )
if [ "$code" != "200" ]; then echo "HTTP $code"; head -c 500 /tmp/x.json; exit 1; fi
```

`!= "200"`, no `>= 400`: el punto es que el estado degradado que hay que ver está
DENTRO del rango de éxito. Vale para cualquier endpoint que use códigos 2xx con
significado (207, 202 encolado, 206 parcial).

Hermano de [[ningun-gate-por-pipe-el-exit-es-del-pipe]]: las dos son la misma forma de
fallo — un mecanismo de vigilancia que mide otra cosa que la que dice medir.
