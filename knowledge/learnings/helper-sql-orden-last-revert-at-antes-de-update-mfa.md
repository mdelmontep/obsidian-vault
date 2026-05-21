---
title: helper SQL con chain de triggers — setear guard ANTES del trigger source
date: 2026-05-21
source: claude-code-session
tags: [postgres, triggers, supabase, conciliacion, fiscal]
---

Cuando una función SQL dispara chain de triggers `UPDATE mfa → recompute → mirror → auto_mark_*` y existe guard de cuarentena (`facturas.last_revert_at` mig 128), **setear el guard ANTES del UPDATE source**, no después.

Síntoma si va después: chain corre con guard inactivo → `auto_mark_*` re-casa la factura con cualquier mov candidato similar → loop infinito → `stack depth limit exceeded`. Reproducible 100%.

Patrón correcto:
1. `FOR UPDATE` lock factura + mfa.
2. `UPDATE facturas SET last_revert_at=now()` (activa guard).
3. `UPDATE mfa SET desvinculado_at=now()` (dispara chain — ya protegido).
4. Re-leer estado factura post-recompute.
5. INSERT module_event audit.

Caso real: mig 131 `desvincular_asignacion` 2026-05-21 — primer intento ordenaba guard después, reprodujo `stack depth limit exceeded` en sandbox. Fix con orden correcto en mig 131c.

Ver [[audits-cross-pr-vs-per-pr]] — los audits per-PR del trigger no lo detectaron, lo cazó el agente composicional.
