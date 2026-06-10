---
title: supabase-js — .catch() sobre un query builder es código muerto
date: 2026-06-10
source: claude-code-session
tags: [supabase, supabase-js, error-handling]
---
supabase-js NUNCA rechaza la promesa por errores de query (RLS, columna
inexistente, constraint…): siempre resuelve con `{ data, error }`. Un
`.catch()` encadenado solo captura fallos de red/transporte — para errores
reales es código muerto y el fallo se traga en silencio.

Caso real (calculador 349): `cargarContactos(...).catch(() => [])` devolvía
`data` sin mirar `error` → un fallo de query producía cálculo con contactos
vacíos sin ninguna señal.

Fix: destructurar y propagar en origen:
```ts
const { data, error } = await query
if (error) throw new Error(`cargarContactos: ${error.message}`)
```
Grep sospechoso: `\.catch\(` junto a `supabase.from(`.
