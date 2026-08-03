---
title: la presencia de un recurso no mide su uso, y el healthcheck falsea cualquier métrica de CPU
date: 2026-08-03
source: claude-code-session
tags: [infra, docker, colima, macos, deteccion-de-entorno, observabilidad]
---
Al montar un auto-apagado por inactividad (VM de Colima en el Mac), los dos criterios intuitivos son los dos falsos:

- **"Sin contenedores corriendo" NO es "sin uso"**: los servicios de dev (`agh-postgres`, `agh-redis`) viven siempre arriba, así que nunca dispararía; y un contenedor de test olvidado 2 h antes lo bloquea **para siempre**. La presencia mide que algo existe, no que alguien lo esté usando.
- **La CPU tampoco**: el healthcheck `pg_isready` cada 5 s hace que `docker stats` marque **61 %** en un postgres con cero clientes conectados. El `loadavg` de la VM da 0,83-1,26 en reposo por lo mismo — y encima se contamina con la propia sonda (`colima ssh -- ps` spawnea los procesos que luego cuenta).

Señales que sí valen porque son deterministas: **conexión TCP establecida** a un puerto publicado (`lsof -nP -iTCP -sTCP:ESTABLISHED | grep ":<puerto>->"`), **evento del daemon** filtrando los `exec_*`/`health_status` de los contenedores permanentes (de 211 eventos en 6 min, los ~150 de healthcheck se van con un `grep -Ev`), y **proceso CLI vivo** en el host. Para confirmar a mano, preguntar al servicio: `pg_stat_activity` con `backend_type='client backend'`, o `redis-cli info clients` (recuerda que tu propio `redis-cli` cuenta como 1).

Corolarios:
- **Medir la señal ANTES de que tu script la contamine**: si el detector busca procesos `docker` en el host, tiene que hacerlo antes de invocar `docker` él mismo, o se detecta a sí mismo y nunca concluye "inactivo".
- **Un lock sin caducidad convierte el mecanismo en inerte y en silencio**: si un chequeo muere con SIGKILL, el lockdir huérfano hace que todos los siguientes salgan con exit 0 sin hacer nada. Descartarlo por `find -mmin +N` y dejar rastro en el log.
- **Escribir en el propio script qué caso NO cubre** (aquí: trabajo generado dentro de un contenedor sin conexiones ni eventos, p. ej. un cron interno) — un detector con hueco documentado es fiable; uno que promete todo, no.

Ver [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]] · [[docker-infra]]
