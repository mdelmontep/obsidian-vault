---
title: non-blocking secondary rpc → devolver warning flag en vez de silenciar o 500
date: 2026-06-15
source: claude-code-session
tags: [arquitectura, api, error-handling, ux]
---

Cuando un POST crea una entidad principal y luego dispara una RPC secundaria
opcional (ej. registrar stock inicial, enviar webhook, crear entrada de audit),
la secundaria puede fallar sin invalidar la operación principal.

**Antipatrones**:
- Silenciar el error (`console.error` y seguir) → bug invisible, dato perdido.
- Propagar como 500 → bloquea la operación principal por un efecto secundario.

**Patrón correcto**:
```
// backend
let xWarning = false
const { error } = await admin.rpc('operacion_secundaria', args)
if (error) { console.error('[context] secondary op', error); xWarning = true }
return NextResponse.json({ entity, ...(xWarning && { xWarning: true }) }, { status: 201 })

// frontend
if (data?.xWarning) toast('Operación completada, pero X falló. Revisa manualmente.', 'warn')
```

Caso real TuFacturaIA: `POST /api/catalogo/productos` crea el producto (201) pero
la RPC `ajustar_stock_manual` de apertura puede fallar → `stock_inicial_warning: true`
→ toast warn en `NuevoProductoModal`. El usuario sabe que necesita ajuste manual.
