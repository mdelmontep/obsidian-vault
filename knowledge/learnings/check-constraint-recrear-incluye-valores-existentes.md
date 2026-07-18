---
title: recrear un CHECK para añadir un valor debe incluir TODOS los existentes
date: 2026-06-27
source: claude-code-session
tags: [postgres, migrations, supabase]
---
Patrón habitual para "permitir un valor nuevo" en un CHECK tipo-enum: `DROP CONSTRAINT` + `ADD CONSTRAINT` con la lista. El error: escribir la lista nueva DE MEMORIA y omitir valores que ya existían → al re-añadir el constraint, las filas reales con esos valores lo violan (SQLSTATE 23514) y la migración FALLA (en prod, a mitad del `db push`).

Caso real FacturaIA: mig 408 recreaba `facturas_fuente_check` con solo 8 valores; el constraint vivo (mig 024) ya admitía `web`/`mobile`/`copiloto`/`recurrente` (filas reales) → 23514, deploy roto.

2ª reincidencia (mig 509, 2026-07-18, módulo Obras): recreaba `cashflow_events_source_check` con la lista de la mig 153 omitiendo `whatsapp_quick` (añadido por mig 168) → habría roto el gasto rápido de WhatsApp. Cazado en revisión ANTES de prod. Patrón recurrente → candidato a check en `/fia-cierre` (dimensión BD): toda mig con `DROP CONSTRAINT ... _check` debe diffear contra el `pg_get_constraintdef` vivo.

Regla: antes de recrear un CHECK, LEER el actual con `pg_get_constraintdef(oid)` (o `\d tabla`) y AÑADIR el valor a esa lista, nunca reescribirla. Verificar contra datos: `SELECT DISTINCT col` debe ⊆ lista nueva. Smoke con tx ROLLBACK → [[smoke-trigger-sql-tx-rollback-contra-prod]].
