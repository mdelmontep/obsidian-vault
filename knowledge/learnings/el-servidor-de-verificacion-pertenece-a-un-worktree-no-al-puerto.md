---
title: el servidor de verificación pertenece a un worktree, no al puerto
date: 2026-09-20
source: agh-iberica
tags: [verificacion, worktree, e2e, metodo]
---

Al correr el arnés de UI de una rama me encontré sus puertos (API 3007, vite 5173) **ya ocupados y
contestando 200**: eran la API y el vite levantados desde el worktree de **otra rama**, contra **otra
base**. Reutilizarlos habría medido 60 cruces de código ajeno y estampado esa línea en mi PR sin que
nada lo dijera.

«El puerto contesta» no dice QUÉ contesta — un health-check, un 200 y hasta un 401 salen idénticos
sirvas la rama que sirvas. El discriminante es **la ruta del proceso**:

```bash
lsof -ti :3007 -ti :5173 | while read p; do ps -p $p -o command=; done
```

Si no es tu worktree, matarlos y levantar los tuyos con **tu** `DATABASE_URL`. Y al terminar,
matarlos: dejarlos vivos es lo que le tiende la trampa al siguiente. Ver
[[tanda-e2e-con-specs-de-una-rama-y-binario-de-otra-no-mide-nada]] ·
[[next-start-build-estatico-sin-hmr-verificar-puerto]].
