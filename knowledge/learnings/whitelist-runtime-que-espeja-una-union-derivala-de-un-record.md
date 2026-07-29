---
title: una whitelist de runtime que espeja una unión de TS derívala de un Record, o se desincroniza en silencio
date: 2026-07-30
source: claude-code-session
tags: [typescript, tipos, validacion, parse-dont-validate, agh]
---
`const TIPOS: readonly MiUnion[] = ["a", "b", "c"]` **compila con miembros de menos**: a TypeScript le vale cualquier subconjunto. Así que una lista de runtime que valida un valor no confiable (columna TEXT/JSONB, payload de API) puede quedarse corta y el error no aparece hasta producción — y de forma muda, porque el validador degrada a `undefined` en vez de lanzar.

Caso real (AGH #674): la unión tenía 6 variantes y la whitelist listaba 5 (faltaba `note`). El puntero `{entityType:"note"}` se escribía bien en JSONB y se leía `undefined` → una feature entregada («bórrala» sobre una nota) **nunca funcionó en prod**, y al quedar el puntero vacío el turno caía a un fallback que hablaba de otra entidad.

Patrón: declarar un `Record<MiUnion, true>` y derivar la lista de sus claves. Ahora falta un miembro = **error de compilación** (`TS2741`), y la pertenencia se pregunta al Record (no depende del orden ni de que nadie reconstruya el array):

```ts
const SET: Record<MiUnion, true> = { a: true, b: true, c: true };
export const TIPOS = Object.keys(SET) as readonly MiUnion[];
```

Señales de que falta este candado: un comentario tipo *«keep in sync with X»* (instrucción manual = el mecanismo que falla), o la misma lista escrita dos veces en dos módulos. Verificar el candado añadiendo un miembro falso a la unión y comprobando que **no compila** — si compila, no hay candado.

Relacionado: [[normalizacion-escrita-dos-veces-diverge]] · [[fake-vs-postgres-orden-sort-utf16-vs-collation]] · [[agh-iberica]].
