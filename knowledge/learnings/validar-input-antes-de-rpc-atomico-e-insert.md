---
title: validar input puro antes de RPC atómico e INSERT
date: 2026-05-18
source: claude-code-session
tags: [arquitectura, integridad-datos, fiscal]
---

Si el flow es `validación → RPC atómico (numeración/secuencia) → INSERT`, toda
validación de input puro (que no depende de BD) debe correr **antes** del RPC.

**Por qué**: si una validación post-RPC falla, el counter atómico avanza pero
no se crea documento. Hueco no recuperable. En contexto fiscal (AEAT, series
A/B/P/F) los huecos requieren justificación documental.

**Patrón**: ordena las validaciones por dependencia.
1. Input puro (Zod, checks de campos) — antes de todo.
2. Lecturas BD que pueden negar (org existe, cliente pertenece a org) — antes del RPC.
3. RPC atómico (`next_invoice_number_for_org`).
4. INSERT(s).

Caso real TuFacturaIA: `create-document.ts` validaba `exencion_codigo` ⇔ `iva_pct=0`
en bloque post-INSERT → row huérfana + num quemado. Fix commit `0e94de4`. Para
errores INSERT residuales (constraints, RLS), ver ADR-001 en repo. Ver
[[incidents]].
