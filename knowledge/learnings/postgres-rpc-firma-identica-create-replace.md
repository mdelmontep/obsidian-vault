---
title: al recrear rpc postgres mantener firma idéntica o queda función huérfana
date: 2026-05-25
source: claude-code-session
tags: [postgres, plpgsql, supabase, rpc]
---

`CREATE OR REPLACE FUNCTION nombre(args) RETURNS X` reemplaza la función SOLO si `(nombre, args)` matchea exactamente. Si cambias firma — añades/quitas un arg, cambias tipo, cambias return — Postgres crea una función NUEVA y deja la vieja huérfana. Resultado: callers que invocan la firma antigua siguen ejecutando la vieja; los que usan la nueva ejecutan la nueva. División silenciosa.

PL/pgSQL compila el body en lazy (al primer EXECUTE), no en CREATE FUNCTION. Por eso una mig que referencia `OLD.columna_que_no_existe` se aplica sin error y solo falla en runtime al ejecutar el trigger/func (caso real FacturaIA mig 095 → mig 162: `OLD.entorno_verifactu` cuando la columna real era `verifactu_entorno`).

**Patrón seguro**:
1. Antes de recrear un RPC, `\df nombre` o grep migraciones para encontrar la firma exacta vigente.
2. Si necesitas cambiar la firma, primero `DROP FUNCTION nombre(args_viejos)` explícito, luego CREATE nuevo. Romperá callers — aceptable solo si los controlas todos.
3. Si el body referencia columnas nuevas/renombradas, ejecuta `SELECT nombre(test_args)` en la propia mig como verificación post-creación.

Aplica también a triggers (`OLD.X` / `NEW.X`) y a constraints CHECK.
