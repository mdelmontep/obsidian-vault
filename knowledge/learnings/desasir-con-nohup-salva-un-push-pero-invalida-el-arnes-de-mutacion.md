---
title: desasir con nohup salva un push largo, pero invalida el arnés de mutación
date: 2026-08-22
source: facturaia
tags: [arnes, hooks, mutacion, harness]
---
Con un `pre-push` que corre lint, typecheck, build y ahora la suite, un `git push` tarda
minutos y **el arnés lo mata a mitad**: quedó cortado dentro del build y la rama no llegó
al remoto (el log acababa en «Creating an optimized production build»).

- **Para el push, desasirlo funciona… hasta que deja de funcionar.** El 22-ago
  `nohup git push … &` sobrevivió; el **5-sep, tres intentos seguidos murieron sin llegar
  a arrancar** — ni proceso, ni fichero de log, ni rama en el remoto. Lo que sí funciona es
  el `run_in_background` del propio arnés, que adopta el proceso en vez de dejarlo huérfano.
- **La ausencia de log NO es «sigue corriendo».** Leí «aún no hay log» como progreso durante
  varios minutos, cuando significaba «nunca arrancó». Distínguelo siempre con algo que
  discrimine: `pgrep -f <script>` para saber si vive, y `git ls-remote` para saber si llegó.
  Y en las dos lecturas, **el exit code no vale**: se verifica por SHA.
- **Para `mutate`, desasirlo NO vale, y el propio arnés lo rechaza**: aborta si arranca
  huérfano (`ppid=1`), porque un arnés desacoplado sigue mutando fuentes cuando ya no hay
  quien lea el resultado — AGH #1253 barrió 1 h 56 min solo, con un fuente de producción
  mutado en disco.

**Regla**: desasir vale para lo idempotente y de una pasada (un push, una suite volcada a
fichero). Nunca para algo que muta y restaura. Si la medición no cabe en el timeout, se
parte en dos tramos —control y mutante— cada uno en primer plano, y se comprueba entre
medias que el árbol volvió a su sitio.

Y ojo al orden: si el control tarda tanto que el árbol cambia por debajo (aquí `main` se
movió diez veces en dos horas), la medición caduca antes de acabar. Ver
[[el-arnes-se-mide-a-si-mismo]] · [[push-que-falla-por-red-imprime-everything-up-to-date-al-final]]
