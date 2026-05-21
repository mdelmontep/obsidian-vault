---
title: audit feed multi-source — shape snapshot/diff o columna detalle queda vacía
date: 2026-05-21
source: claude-code-session
tags: [audit, supabase, react, ux]
---

Al añadir nueva fuente al audit feed unified (`audit_log`, `phone_otp_audit`, `module_events`...), la UI espera el `detalles` en uno de 2 shapes:
- `snapshot: {key: val}` — modo creación, valores escalares planos.
- `{key: {de: x, a: y}}` — modo update diff.

Payload plano sin ninguno de los dos → `formatAuditDiff` devuelve `''` → columna DETALLE vacía → promesa "Queda registrado en auditoría" rota visualmente.

Patrón: en el mapper de la nueva source, construir `snapshot` legible específico por tipo:
```ts
detalles.snapshot = { factura: 'X', tipo: 'Pago', importe: '333,33 €', motivo: '...' }
```

Y añadir labels al map `AUDIT_DIFF_KEY_LABEL` del settings-view para evitar humanizeKey raw → ugly title case.

Caso real: PR #69 añadió `module_events` source a feed, PR #70 (5 min después) fix porque columna detalle salía vacía aunque la fila apareciera con nombre y acción correctos.

Aplica cualquier tabla de events que se quiera mostrar en `/settings?tab=auditoria`. Test: snapshot legible debe estar en mapper antes de mergear nueva source.
