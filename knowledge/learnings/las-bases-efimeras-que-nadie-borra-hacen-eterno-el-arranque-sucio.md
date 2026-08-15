---
title: las bases efímeras que nadie borra hacen eterno el arranque sucio de un Postgres compartido
date: 2026-08-15
source: claude-code-session agh-iberica
tags: [postgres, docker, testing, infra]
---
El Postgres de los tests `.pg` tuvo un cierre no limpio y tardó **~15 minutos** en volver a aceptar
conexiones. Durante ese rato **ningún test de integración de ninguna sesión funciona**.

La lentitud **no es del volumen de datos: es del NÚMERO de bases.** El arranque tras un cierre sucio
hace `syncing data directory`, que recorre el árbol de ficheros de **todas** las bases del clúster.
Contadas: **100 bases `agh_*`** — cada corrida de gate crea la suya (`agh_a<issue>`, `agh_g<issue>`,
`agh_tren<N>`…) y **nadie la borra**. La factura no la paga quien la creó: la paga el siguiente que
necesite la BD.

👉 **Una base efímera por corrida se borra al terminar la corrida.** Falsable: contar
`select count(*) from pg_database` antes y después de un gate → la diferencia tiene que ser 0.

**Y una trampa de diagnóstico que costó lo suyo:** `localhost:5433` no era un Postgres local, sino un
contenedor dentro de **Colima** alcanzado por un **túnel SSH** (el proceso que escucha en el puerto
es `ssh`, no `postgres`). `docker ps` fallaba con el contexto por defecto **y** con el de OrbStack;
el bueno era `DOCKER_HOST=unix://~/.colima/default/docker.sock`. Antes de aceptar «el daemon está
parado», **prueba los contextos** (`docker context ls`) y mira **quién escucha de verdad**
(`lsof -nP -iTCP:<puerto> -sTCP:LISTEN`).

⚠️ Y no atribuyas el crash a lo último que hiciste solo porque coincide en el minuto: matar un
**cliente** no crashea un **backend**. Ver [[el-ultimo-commit-que-toco-el-fichero-no-es-el-que-lo-introdujo]].
