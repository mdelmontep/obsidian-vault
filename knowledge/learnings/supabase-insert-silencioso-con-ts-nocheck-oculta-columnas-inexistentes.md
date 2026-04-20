---
title: supabase insert silencioso con ts-nocheck oculta columnas inexistentes
date: 2026-04-20
source: claude-code-session
tags: [supabase, typescript, facturaia, seed]
---

Con `// @ts-nocheck`, un `.insert({ campo_inexistente: 0 })` devuelve error de PostgREST (`Could not find the 'campo' column of 'tabla' in the schema cache`) pero TypeScript no lo detecta en build.

Si el código no verifica `{ error }` del resultado, parece que el insert funcionó pero no insertó nada.

Caso real: seed de FacturaIA insertaba `{ ...cliente, facturado: 0, pendiente: 0 }` en tabla `clientes`. Los campos `facturado` y `pendiente` son calculados en runtime, no existen como columnas. El seed reportaba `clientes: 0` sin error visible.

**Regla**: en seeds y scripts con `@ts-nocheck`, siempre verificar `{ data, error }` y retornar el error explícitamente:

```ts
const { data, error } = await supabase.from('clientes').insert({ ... }).select('id').single()
if (error) return NextResponse.json({ error: error.message }, { status: 500 })
```
