---
title: Campo huérfano — código referencia columna sin migración paralela → UI vacía silenciosa
date: 2026-05-30
source: TuFacturaIA fix billing PR #110
tags: [postgrest, supabase, schema, billing, code-review, gotcha]
---

## Síntoma

`/settings?tab=facturacion` muestra solo "Estás en el plan enterprise" como texto suelto. La grid de tarjetas Starter/Pro/Enterprise no aparece. Ni error en pantalla, ni toast, ni log obvio.

## Causa raíz

`plan-billing.tsx` hacía `supabase.from('plans').select('id, nombre, precio_mes, precio_anual, descripcion')`. La columna `precio_anual` **nunca existió** en BD — el branch Stripe la añadió al código sin migración SQL paralela.

PostgREST devuelve `400 column plans.precio_anual does not exist`. El cliente Supabase JS NO lanza: deja `data: null` y la app pone `setPlans([])`. La grid `plans.map(...)` no renderiza. El subtítulo cae al fallback `|| currentPlan` → muestra el id en minúscula (`enterprise`) en vez del `nombre` (`Enterprise`).

**Tres señales que confirman el patrón**:
1. Texto del plan en minúscula = `.find()` devolvió undefined = array vacío
2. Grid totalmente ausente, no parcial
3. Nada en consola si no se inspecciona Network

## Prevención

- **Cambio de shape compartido = grep todos los consumers** antes del PR. Ya inviolable en CLAUDE.md, pero falló aquí porque el shape nuevo se introdujo solo en código, no en mig.
- **Auditoría puntual con [[Explore]]**: por cada tabla en branches grandes, contrastar `CREATE TABLE` + `ALTER TABLE ADD COLUMN` (verdad BD) contra `from('<tabla>').select(...)` / `.insert({...})` / `.update({...})` / `z.object({...})` / `interface XRow`. Caso del PR #110: el agente Explore validó 8 tablas billing/Stripe y encontró 0 huérfanos restantes — el caso `precio_anual` fue único.
- **El admin debe estar conectado**: si una columna existe pero el panel admin no la edita, está medio-huérfana. Aquí faltó ampliar `/api/admin/plans/[id]` (Zod) + UI admin con input dual. Ver [[admin-edita-toda-columna-editable-no-solo-las-criticas]].

## Detección rápida ad-hoc

```bash
# Para una tabla concreta T, listar campos REALES vs referenciados:
grep -rh "from('T')\\..*select" src/ | sort -u  # consumers
grep -rh "CREATE TABLE.*T\\b\\|ALTER TABLE.*T.*ADD COLUMN" supabase/migrations/ | sort -u  # verdad
```

Si una columna aparece solo en el primer set, es huérfana.

## Aplicación

- Cualquier branch que toque billing/shape compartido → pasar por [[Explore]] dedicado antes de merge
- Tras merges multi-PR en mismo subsistema → audit cross-PR ya en CLAUDE.md, añadir explícitamente "huérfanos de shape" al checklist del agente
- Pre-commit ideal (futuro): tooling que parsee `.select()` calls + diff con migraciones — no hay aún en repo
