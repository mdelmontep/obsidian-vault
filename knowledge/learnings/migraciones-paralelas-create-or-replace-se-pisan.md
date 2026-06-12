---
title: migraciones paralelas con create or replace de la misma función se pisan
date: 2026-06-12
source: claude-code-session
tags: [supabase, migrations, sql]
---
N ramas paralelas que hacen `CREATE OR REPLACE FUNCTION` de la misma función
se pisan al mergear: la última migración aplicada gana y borra silenciosamente
los añadidos de las otras (sin error, sin conflicto git si los archivos son
distintos).

Fix: antes de aplicar a prod, consolidar la definición COMPLETA (todas las
ramas/keys de todas las migs) en la migración de número más alto, y dejar las
anteriores como histórico.

Detección: grep de la función en `supabase/migrations/` — si aparece en >1
archivo de la misma tanda, revisar que la última contenga todo.
Caso: `get_org_usage` pisada 3× en las migs de cuotas TuFacturaIA (2026-06).
