---
title: una lista cerrada en un check de bd se queda atrás del catálogo de la ui
date: 2026-10-13
source: agency-portal
tags: [postgres, supabase, migraciones, check-constraint]
---
Síntoma: la UI ofrece una opción (conector «Anthropic» en `/agency/admin`) y guardarla falla con violación de CHECK (23514). Nadie lo ve hasta que alguien intenta usarla.

Causa: `platform_credentials.provider` tiene `check (provider in (...))`; el conector se añadió al catálogo TS y nadie amplió el CHECK. Cada migración que lo rehace copia la lista de la ÚLTIMA definición, así que un valor olvidado sigue olvidado.

Fix/patrón:
- Al añadir un valor al catálogo/enum TS, grep de la columna en `supabase/migrations/` y rehacer el CHECK con la unión de la última definición + lo nuevo.
- El bloque `DO` de la migración verifica con `pg_get_constraintdef` que el CHECK contiene cada valor; nunca fiarse de que no hubo error.
- Revisado el 13-oct en el resto de proyectos: sin otro caso (facturaia queda sin cotejar del todo, ~120 columnas). Relacionado: [[supabase-check-constraint-triggered-by-enum]]
