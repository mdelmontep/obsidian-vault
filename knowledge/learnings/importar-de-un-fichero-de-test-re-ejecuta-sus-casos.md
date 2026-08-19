---
title: importar un helper desde otro fichero .test.ts re-ejecuta sus casos en el importador
date: 2026-08-19
source: agh-iberica
tags: [vitest, testing, metricas, gotcha]
---

`import { helper } from "./otro.test"` hace que vitest **ejecute también los `it` de `otro.test.ts`
dentro del fichero importador**, además de en el suyo. Medido: 5 casos ajenos aparecieron bajo
`status-vivo.test.ts`, y la rama declaró **+11 tests aportando 6**.

**Nada lo avisa.** `tsc` está contento (es un import legal), `eslint` también, y el resumen de vitest
solo cuenta más casos: la métrica cuadra consigo misma y **+11 es tan plausible como +6**. Lo destapó
cuadrar el desglose a mano contra la base.

El número es lo de menos. Si el fichero importado tiene `beforeAll` con efectos (BD, servidor, fichero
temporal), **corre dos veces en dos contextos** y el fallo sale en el fichero equivocado.

**Fix:** el helper compartido va a un módulo hermano que **no** sea `.test.ts`
(`test/db/sql-comentarios.ts`) y los tests lo importan de ahí. Si algún candado del repo declara ese
fichero **por ruta** (listas de excepciones), mover el helper obliga a **mover la fila**, o la excusa
queda colgando de un fichero que ya no hace nada.

**Verificación de que se fue:** el delta vuelve a ser exactamente el nº de casos añadidos.
Relacionado: [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]].
