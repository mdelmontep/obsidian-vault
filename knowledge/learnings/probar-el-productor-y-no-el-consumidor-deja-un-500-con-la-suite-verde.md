---
title: probar el productor y no a quien lo consume deja un 500 con la suite en verde
date: 2026-07-31
source: claude-code-session
tags: [testing, refactor, api, verificacion]
---

Renombrar una clave de un dict de retorno es el cambio que más fácil se cuela: el módulo que
la produce tiene tests propios y siguen verdes, porque prueban **la función**, no el
contrato con quien la llama.

Caso (cryptobruj-bot): `faltan_para_veredicto` → `faltan_trimestres` en un módulo. Su
consumidor seguía con la clave vieja → `KeyError` → **500 en la ficha de CUALQUIER
estrategia**, no solo la afectada. 207 tests en verde y el panel entero sin detalle.

Regla: por cada estructura que cruza un módulo, un test **del consumidor** que compruebe las
claves del contrato. Y para endpoints, uno que construya la respuesta **de todas** las
entidades del registro, no de una:

```python
for sid in BY_ID:            # no solo "swing-1h"
    d = api.get_strategy(sid)
    assert "aprendizaje" in d and "params" in d
```

Los dicts sin tipo no avisan al renombrar; el test del consumidor es el único que sí. En TS
esto lo caza el compilador — en Python hay que escribirlo. Ver
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
