---
title: desasir con nohup salva un push largo, pero invalida el arnés de mutación
date: 2026-08-22
source: facturaia
tags: [arnes, hooks, mutacion, harness]
---
Con un `pre-push` que corre lint, typecheck, build y ahora la suite, un `git push` tarda
minutos y **el arnés lo mata a mitad**: quedó cortado dentro del build y la rama no llegó
al remoto (el log acababa en «Creating an optimized production build»).

- **Para el push, desasirlo funciona**: `nohup git push … &` sobrevive al arnés y termina.
  Se verifica luego por SHA (`ls-remote` == `rev-parse`), nunca por exit code.
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
