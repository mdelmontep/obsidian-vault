---
title: equivalente derivado que debe seguir sincronizado → columna GENERATED STORED, no trigger de sync
date: 2026-05-27
source: claude-code-session
tags: [postgres, supabase]
---

Cuando una columna es función pura de otras de la MISMA fila y debe estar siempre coherente (ej. `total_eur = round(total * tipo_cambio, 2)`, equivalente en moneda base de un importe en divisa), usar `GENERATED ALWAYS AS (...) STORED` en vez de trigger de sincronización o cálculo en la app.

Por qué: Postgres la recalcula en cada INSERT/UPDATE → **ningún camino de escritura puede desincronizarla** (RPC, REST, insert directo del cliente). Backfill automático al añadir la columna. Respeta single-source-of-truth (CLAUDE.md prohíbe triggers col↔col).

Gotchas:
- No se pueden INSERT/UPDATE explícitamente — omítelas del payload (un `.update()` que las incluya falla).
- `ADD COLUMN ... STORED` reescribe la tabla (lock ACCESS EXCLUSIVE breve).
- El caller solo fija los inputs (`tipo_cambio`, `moneda`); el equivalente sale gratis.

Cierra el agujero típico: una capa nueva (web, voz, API) inserta saltándose el helper canónico y olvida el campo derivado. Con generada, no hay nada que olvidar. Relacionado: [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]].
