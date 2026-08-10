---
title: filtrar por línea un volcado SQL con valores multilínea borra trozos de los datos
date: 2026-08-11
source: claude-code-session
tags: [postgres, pg_dump, migracion, datos]
---
Limpiar un `pg_dump` con `grep -v '^--'` para quitar comentarios parece inocente. No lo es: un
INSERT con HTML, Markdown o SQL de ejemplo dentro ocupa varias líneas, y ahí hay líneas que empiezan
por `--`. El filtro **borra parte del valor**.

Aquí saltó como error de sintaxis (`trailing junk after numeric literal`), pero sobre un texto sin
comillas dentro habría entrado limpiamente con el contenido mutilado y nadie se entera.

Regla: sobre un volcado, filtrar solo con patrones **anclados y exactos**, y lo que sea de cabecera,
solo hasta el primer `INSERT`:
```awk
/^INSERT INTO/ { datos = 1 }
datos == 0 && /^SET / { next }
```
(Los `SET` de cabecera sí hay que quitarlos entre versiones: pg_dump 17 emite `SET
transaction_timeout` y `\restrict`, que PostgreSQL 15 no conoce y abortan la transacción entera.)

Y no generar los INSERT a mano desde el cliente: adivinar tipos es reimplementar mal media capa de
Postgres — un `text[]` sale como jsonb y falla.
