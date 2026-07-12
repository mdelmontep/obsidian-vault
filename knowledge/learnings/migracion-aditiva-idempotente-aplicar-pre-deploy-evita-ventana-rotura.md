---
title: Migración aditiva e idempotente → aplicarla ANTES del deploy evita la ventana de rotura
date: 2026-07-12
source: claude-code-session
tags: [supabase, migraciones, deploy, facturaia, postgres]
---
Al mergear el código que llama a una RPC nueva, si el deploy del código llega ANTES de que la
migración esté aplicada, hay una ventana en la que el código nuevo llama a una función que aún
no existe → rompe en prod. El orden importa: para migraciones ADITIVAS (crean funciones/índices,
no tocan datos ni esquema existente) lo correcto es aplicarlas PRIMERO, luego desplegar el código.

Como los objetos SQL no llevan número (se llaman `buscar_clientes_fuzzy`, etc.), se pueden crear
en prod con `execute_sql` (idempotente: `CREATE OR REPLACE`, `CREATE INDEX IF NOT EXISTS`) sin
tocar `schema_migrations`. Luego `supabase db push` desde main registra la migración formalmente:
re-aplicar es inocuo (las NOTICE "already exists, skipping" lo confirman) y `migration list` queda
`NNN|NNN|NNN` sin divergencia. Así se desbloquea prod sin violar "el repo manda / db push desde main".

GOTCHA de numeración: el número `NNN` se ocupa al MERGEAR, no al crear la rama. Con ramas en
paralelo (aquí chocó copiloto 452 con una PR fiscal 452/453) → renumerar al hueco real justo antes
de mergear y `git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d` tras el merge.
