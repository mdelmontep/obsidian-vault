---
title: un arnés de mutación sobre vitest no ve los candados de tipos
date: 2026-08-14
source: claude-code-session
tags: [testing, typescript, mutacion, metodo]
---
El checker de un arnés de mutación suele ser la suite de **vitest**, que transpila con **esbuild y no
typechequea**. Consecuencia: los mutantes que caen sobre una interfaz o un tipo **no se ejecutan** —
el arnés los marca «excluidos / solo-tipo» y sigue. En AGH (#1154): 5 de 12 mutantes excluidos, y el
barrido informó **`0 SIN VÍCTIMA`**, cierto de lo que midió y **falso como cobertura**.

El peligro es que sale bien: leer «0 sin víctima» sobre un diff con aserciones de tipo y darlo por
cubierto es la falsa seguridad que el arnés existe para evitar. Ver [[un-candado-derivado-no-se-defiende-de-una-mutacion-de-si-mismo]].

**Fix:** si el diff mete candados de tipos, el contrafáctico va **a mano con `tsc`** y se declara así.
Dos requisitos para que el candado exista siquiera:
- **`satisfies X`, no `: X`** — con la anotación el tipo del literal se borra a la interfaz y la
  aridad/forma real deja de ser legible, que es justo el dato a vigilar.
- **Derivar de `keyof`**, no enumerar: un miembro nuevo entra solo. Ver [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]].

Y su límite, a declarar en el código: un candado de tipos no existe en runtime (se rodea con un `as`).
La pareja tipos + runtime, cada una diciendo qué NO caza, es lo que cubre el hueco.
