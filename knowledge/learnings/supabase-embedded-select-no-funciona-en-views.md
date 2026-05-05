---
title: embedded select de supabase-js no funciona sobre views
date: 2026-05-05
source: claude-code-session
tags: [supabase, postgrest, views]
---

`supabase.from('vista_x').select('*, otra_tabla(*)')` falla — PostgREST necesita FKs declaradas para resolver el embed, y las vistas no propagan FKs aunque las tablas base las tengan.

Síntoma: `Could not find a relationship between 'vista_x' and 'otra_tabla'`.

Patrón resolutivo: 2 queries en paralelo + merge en cliente.

```ts
const [rowsRes, joinedRes] = await Promise.all([
  supabase.from('tabla').select('*, embed(*)').eq(...),  // FKs OK
  supabase.from('vista').select('id, campo_extra'),       // sin embed
])
const map = new Map(joinedRes.data.map(r => [r.id, r]))
const merged = rowsRes.data.map(r => ({ ...r, ...map.get(r.id) }))
```

Caso real FacturaIA: `facturas_con_autor` (vista con LEFT JOIN profiles + api_keys) no permite embed de `clientes/proveedores`. La tabla `facturas` sí. Hago las dos queries y mergeo.
