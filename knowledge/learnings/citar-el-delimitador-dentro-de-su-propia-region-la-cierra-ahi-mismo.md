---
title: citar el delimitador dentro de su propia región la cierra ahí mismo, y el error sale lejos
date: 2026-08-15
source: claude-code-session
tags: [sql, javascript, harness, gates, tucrmia]
---
Tres veces en una noche, tres lenguajes, el mismo fallo: escribir el delimitador **dentro** de
la región que ese delimitador abre. Un comentario no protege — el analizador ve el par antes.

- SQL: ``-- cada `do $$` es su propia invocación`` dentro de un `do $$` → cierra el bloque ahí,
  y el resto se analiza como SQL suelto. El error salió **168 líneas más allá**, señalando una
  línea sin relación, tras 9 min de contenedor.
- JS: un nombre entre acentos graves dentro de una plantilla → la cierra.
- JSDoc: un patrón con `**/*.ts` dentro de `/** */` → el `*/` cierra el comentario.

**Lo que hay que arreglar no es el comentario: es que NADA los analizaba.** `allowJs:false` +
`include` sólo `.ts`/`.tsx` deja los `.mjs` fuera de `tsc`; ejecutar es analizar, pero los
smokes no corren en el gate (piden credenciales) y el `.sql` sólo lo lee el replay (pide
Docker). Un error de sintaxis ahí es invisible **hasta que alguien lo ejecuta a mano**.

Fix: `node --check` sobre todo `.mjs` rastreado + recorrido de `$$` por pares sobre `.sql`, lo
primero de la cadena (responde en 1 s). Al escribir la prosa, **nombra el delimitador sin
escribirlo**.

Ver [[dos-trampas-al-escribir-un-gate-por-arbol-de-sintaxis]] · [[write-tool-byte-nulo-en-template-literal]]
