---
title: pgrst203 con rpc overloads — pasar todos los named params
date: 2026-05-10
source: claude-code-session
tags: [supabase, postgrest, rpc, bug]
---

Si una función SQL tiene 2+ sobrecargas, supabase-js falla con `PGRST203` "Could not choose the best candidate function" cuando solo pasas los params del overload original.

**Síntoma**: endpoint que llamaba `rpc('fn', {a, b})` empieza a devolver 500 sin tocar nada — alguien añadió la versión `(a, b, c, d, e)` en BD.

**Fix**: pasar TODOS los named params explícitos (los nuevos como `null` si no aplican):
```ts
admin.rpc('fn', { a, b, c: 'voice', d: null, e: null })
```

**Detección**: ejecutar `select_function_overloads` en Supabase SQL Editor o llamar la RPC con curl REST (`POST /rest/v1/rpc/fn`) y leer el mensaje de PGRST203 — lista las firmas.

Caso real: `convertir_presupuesto_a_factura` tenía 2 versiones; código pasaba 2 params → todas las conversiones rotas en prod hasta el fix.
