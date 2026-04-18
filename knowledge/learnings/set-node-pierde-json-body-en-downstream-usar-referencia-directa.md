---
title: set node pierde json body en downstream — usar referencia directa
date: 2026-04-18
source: claude-code-session
tags: [n8n, workflow, bug]
---

Un nodo Set que extrae campos de `$json.body.args.*` (ej: nombre, telefono, accion) **reemplaza `$json`** con solo los campos definidos. Los nodos posteriores — especialmente tras un Switch — ya no tienen acceso a `$json.body` original.

## Síntoma

El nodo downstream lee `$json.body?.args?.subject` → `undefined` → cae al fallback genérico ("Incidencia reportada por teléfono") aunque el webhook recibió datos reales.

## Fix

Referenciar el nodo fuente directamente en vez de `$json`:

```
// MAL (body ya no existe en $json)
={{ $json.body?.args?.subject || 'fallback' }}

// BIEN (lee directo del Webhook)
={{ $('Webhook').first().json.body.args.subject || 'fallback' }}
```

## Contexto

Descubierto en workflow AIA Llamadas (`O80k1QzfSkJUgzkD`): `Normalizar Datos` (Set) → `Switch Acción` → `Normalizar Datos Ticket` perdía todos los args de Retell. Los datos estaban en el Webhook pero el Set los eliminaba del flujo.
