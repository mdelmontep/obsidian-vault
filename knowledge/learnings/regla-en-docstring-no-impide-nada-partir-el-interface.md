---
title: una regla que solo vive en un docstring no impide nada — pártela en dos interfaces
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [typescript, arquitectura, multi-tenant, tests]
---
Un store tenía métodos cross-tenant con docstrings correctos («NOT a user-facing read»,
«nunca expuesto como tool del brain»). Nadie los había violado, pero nada lo impedía:
pasarle el store entero a una lectura nueva y llamar al método cross-tenant compilaba,
pasaba el gate, y habría devuelto las filas de todos los usuarios de todos los tenants.

Fix: partir el interface en su mitad **permitida** y su mitad de **sistema**, y tipar al
consumidor contra la estrecha — el método prohibido no existe en su tipo. Aditivo: el
interface completo sigue siendo el mismo por extensión, así que **ningún consumidor se
toca** (que el typecheck pase sin editar nada más es la prueba).

Tres candados, y el 2º es el que no se ve venir:
1. `@ts-expect-error` por acceso prohibido — **es una aserción**: si vuelve a compilar,
   `tsc` cae por directiva sin usar (TS2578). ⚠️ su función **no puede ejecutarse**: la
   directiva suprime el error de tipos, no la llamada.
2. `type NoOverlap<A,B> = Extract<keyof A, keyof B> extends never ? true : never` — sin
   esto, la vía de escape no es escribir el acceso prohibido, es **mover el método** a la
   mitad estrecha para callar el error, y eso vuelve a compilar sin que nada falle.
3. Un fake mínimo de la mitad estrecha: añadirle un método obliga a tocarlo.

Verificar el candado rompiéndolo (mover el método → saltan los tres). Y el tipo dice quién
**puede** llamar, no que el `WHERE` filtre: eso es [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]].
Prima de [[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]].
