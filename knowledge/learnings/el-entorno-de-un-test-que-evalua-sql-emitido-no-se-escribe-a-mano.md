---
title: si el fixture da de alta el identificador que el emisor inventó, el guard queda desarmado
date: 2026-08-02
source: claude-code-session
tags: [testing, generadores, sql, rls, tucrmia]
---
Un generador emitía el predicado de una policy y el test lo evaluaba con un evaluador propio que **lanza
ante un término desconocido** — esa era su defensa declarada. El entorno del test se escribía a mano:

```ts
[`${tabla}.pipeline_id`, fila.pipelineId]   // ← fabrica el término que el emisor necesita
```

El emisor asumía que la columna se llamaba igual en todas las tablas y en una era `id`. Salieron cuatro
`create policy` contra una columna inexistente. Postgres las habría rechazado con `42703`; el test decía
verde porque **el fixture daba de alta el error**. Tres gates lo dejaron pasar: el de deriva compara texto
contra texto, y el de equivalencia se validaba contra sus propias suposiciones.

Regla: el entorno de un test que evalúa texto generado se DERIVA de la misma declaración que usa el
emisor, nunca se escribe en paralelo. Si hay que escribirlo a mano, es que falta una declaración.
Y añadir un gate que cruce lo emitido contra el esquema real. Ver
[[replay-de-migraciones-contra-un-postgres-desechable-en-docker]].
Un fixture escrito así **dentro del árbol** además corre contra cualquier test
que lo recorra: [[un-fixture-escrito-dentro-del-arbol-que-otro-test-recorre-es-una-carrera]].
