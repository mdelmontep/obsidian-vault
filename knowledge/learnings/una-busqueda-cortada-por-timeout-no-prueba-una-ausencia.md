---
title: una búsqueda cortada por timeout no prueba una ausencia
date: 2026-09-06
source: mandadm
tags: [verificacion, shell, metodo, sesiones-paralelas]
---
Corrí `timeout 90 grep -rl "<ref>" Projects … | head -10`, no salió nada, y lo afirmé —a Manuel y a
otra sesión— como «cero coincidencias, en ningún fichero». Repetido sin pipe: **EC=124**, muerto por
tiempo. La cadena estaba a la vista en `agentesia-crm/supabase/config.toml:5`. La etiqueta de Docker
de la otra sesión no me confirmó nada: me desmintió.

Es la regla de «ningún gate por pipe» aplicada donde no estaba escrita: no a un gate, a un
**negativo**. Con `| head` delante, «vacío» y «no llegué a mirar» se ven idénticos.

**Fix:** la búsqueda que sostiene una afirmación va a fichero y con `ec=$?`. De `grep`: `0` hubo
coincidencias, `1` no hay, `2` errores, `124` lo mató el timeout. Solo el `1` autoriza a decir «no
está»; con `2` o `124` la frase correcta es «no lo sé».

Y la mitad que ahorra el barrido entero: **antes del grep bruto, mira si hay un documento que ya lo
responda.** Ese ref llevaba un mes documentado con su nombre y su organización en
`facturaia/docs/architecture/inventario-entornos-supabase.md`.
Ver [[un-resultado-vacio-no-es-un-hecho-hasta-que-miras-el-exit-code]]
