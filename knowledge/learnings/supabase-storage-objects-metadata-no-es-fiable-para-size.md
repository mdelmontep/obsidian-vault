---
title: supabase storage.objects metadata no es fiable para size
date: 2026-04-25
source: claude-code-session
tags: [supabase, storage, facturaia]
---

La columna `metadata` en `storage.objects` no siempre almacena el campo `size`. La Storage API lo computa al leer (devuelve `metadata.size` en la respuesta), pero una función SQL `SECURITY DEFINER` que haga `metadata->>'size'` puede obtener NULL → resultado 0.

**Solución**: calcular storage real en la capa API usando el SDK de Storage:

```ts
const { data: files } = await admin.storage.from('facturas').list(orgId, { limit: 1000 })
const storageBytes = files?.reduce((sum, f) => sum + (f.metadata?.size || 0), 0) ?? 0
const storageMb = Math.ceil(storageBytes / 1048576)
```

No usar RPCs SQL para calcular storage. El SDK sí devuelve tamaños fiables.
