---
title: estado de dinero sin fecha de caja obligatoria rompe en silencio
date: 2026-07-23
source: claude-code-session
tags: [postgres, data-integrity, cashflow]
---
Si un estado implica un hecho temporal (cobrada ⇒ cuándo entró el dinero), la fecha debe ser invariante en BD, no convención de los escritores. En FacturaIA, 1.372/1.396 cobradas tenían `fecha_cobro NULL` porque 3 de ~12 escritores hacían `UPDATE {estado}` a pelo; todo cálculo base caja (gráfico, KPIs, forecast) caía a fallbacks silenciosos y cada vista divergía.

Fix en 3 capas (mig 549):
1. Trigger BEFORE que RELLENA solo si falta (nunca pisa ni limpia). En UPDATE → hoy; en INSERT → `least(coalesce(vto,fecha), hoy)` — un import histórico con `hoy` concentraría años de cobros en el mes actual.
2. Backfill audit-first: la tabla de auditoría genérica (trigger de diff de estado) guarda CUÁNDO ocurrió la transición real → fecha exacta; fallback `least(greatest(fecha, vto), hoy)` (cap por FUERA del greatest o una emisión futura arrastra la caja al futuro).
3. Consumidores: los cálculos capan a hoy la fecha de caja futura (dato incompleto) en vez de descartar la fila.

Corolario: el % `cobradas/emitidas` mezcla universos si solo el numerador pasa a base caja (puede dar >100%) — cambiar la base de UNA métrica exige revisar cada ratio que la consume.
