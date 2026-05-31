---
title: supabase CLI skipea migrations con prefijo no puramente numérico
date: 2026-05-20
source: claude-code-session
tags: [supabase, migrations, cli]
---

`supabase migration list` / `db push` exigen patrón `<num>_name.sql`. Archivos tipo `107b_*.sql` se skipean con warning silente — el SQL nunca corre en `supabase db reset` / fresh setup.

Fix: renombrar a número libre. **Cuidado con prefijos similares**: `1071_*` colisiona visualmente con `107_*` al ordenar y rompe `db push` con error críptico `Remote migration versions not found in local migrations directory`.

Regla: usar número estrictamente >max actual (ej. `122` si el último es 121). Documentar en header del archivo que el orden cronológico real fue otro. El SQL debe ser idempotente (`IF NOT EXISTS`) por si un fresh setup lo ejecuta fuera del orden histórico.

Si el contenido del archivo skipeado **ya está aplicado en prod** (no solo pendiente): tras renombrar, `supabase migration repair --status applied <N>` lo registra en el ledger sin re-ejecutar el SQL (no hace DROP/CREATE). Caso 131b/131c→197/198 (2026-05-31).

Detectar antes de commit:
```bash
ls supabase/migrations/ | grep -vE '^[0-9]+_[^/]+\.sql$'
```

Relacionado: [[supabase-cli-rechaza-migrations-con-version-duplicada]] · [[supabase-cli-adoptar-tarde-en-proyecto-con-migrations-aplicadas-por-studio]]
