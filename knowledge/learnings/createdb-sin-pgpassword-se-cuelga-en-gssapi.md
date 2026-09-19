---
title: createdb sin PGPASSWORD no falla, se cuelga en GSSAPI y tiñe los gates siguientes
date: 2026-09-20
source: agh-iberica
tags: [postgres, gate, diagnostico]
---
`createdb -h localhost -p 5433 -U user <base>` **sin `PGPASSWORD`** no devuelve error: se queda
negociando GSSAPI indefinidamente, consumiendo CPU. Medido el 19-sep-2026 en AGH: un `createdb`
que dejó un subagente llevaba **2 h 25 min** vivo al 24 % de CPU, con `GSSCred` al 18 %.

Ese proceso no aparece en ningún log, pero sube la carga y **tiñe de rojo los gates siguientes por
timeout**: tres gates seguidos de la misma rama fallaron con ficheros DISTINTOS cada vez
(`exports-fantasma`, `open-threads-store.pg`, `reminder-store.pg`, `migration-0045.pg`), siempre por
timeout de test o de hook, nunca por aserción. Al matarlo, el cuarto salió verde sin tocar código.

Patrón: ante un gate rojo cuyos ficheros cambian entre intentos, antes de mirar el diff →
`ps -eo pcpu,etime,command -r | head` y buscar `createdb`, `psql` o `vitest` huérfanos. Y siempre
`PGPASSWORD=pass createdb …`. Ver [[gate-rojo-por-carga-de-la-maquina]].
