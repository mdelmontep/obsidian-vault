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
- `ADD COLUMN ... STORED` reescribe la tabla (lock ACCESS EXCLUSIVE breve). En tabla grande de prod, medir el tiempo antes del `db push`.
- **Una generada NO puede referenciar otra generada** — hay que reexpandir la expresión (si ya tienes `total_eur` generada y quieres `importe_cobrable_eur`, repites `total * tipo_cambio` en vez de leer `total_eur`).
- El caller solo fija los inputs (`tipo_cambio`, `moneda`); el equivalente sale gratis.

**Segunda razón, de rendimiento (2026-07-25): la alternativa "función `STABLE` que lo calcule" es inutilizable si el derivado va en `WHERE` u `ORDER BY`.** Una plpgsql `STABLE` es caja negra para el planner (coste por defecto, sin inlining, sin índices, una llamada por fila candidata); dentro de triggers `FOR EACH ROW` de un import masivo es el peor sitio posible. La generada STORED es columna normal → **indexable** y resuelve el `ORDER BY` de raíz. Regla: si el derivado solo se lee, una función vale; si se **filtra u ordena** por él, columna generada.

**Cuándo NO usarla**: si el derivado depende de otra tabla o tiene **ciclo de vida propio** (ej. una retención de garantía que pasa de `retenida` a `liberada`), no cabe en una generada — va por `LEFT JOIN` al ledger que la posee. Un snapshot estático en la fila rompe single-source-of-truth y congela un valor que debía cambiar.

Cierra el agujero típico: una capa nueva (web, voz, API) inserta saltándose el helper canónico y olvida el campo derivado. Con generada, no hay nada que olvidar. Relacionado: [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]] · [[importe-fiscal-no-es-importe-a-cobrar-retenciones]].
