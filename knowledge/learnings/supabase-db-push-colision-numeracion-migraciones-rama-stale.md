---
title: supabase db push da por aplicadas las migraciones cuyo NNN ya existe en remoto y no las ejecuta
date: 2026-06-01
source: claude-code-session
tags: [supabase, migraciones, git]
---
Rama feature creada sobre un `main` viejo: numeras tus migraciones 197-202, pero
`main` avanzó y prod ya tiene 197-204 aplicadas (con OTROS nombres). `supabase db
push` compara por VERSIÓN (el número NNN), ve "197-202 ya aplicadas" y **NO ejecuta
las tuyas — sin error**, dejándote creer que sí. Fallo silencioso peligroso.

Detección: SIEMPRE `supabase migration list --linked` ANTES de `db push`. Columnas
`Local | Remote` desalineadas (tu NNN aparece en ambas pero es otro archivo, o hay
remotas sin local) = colisión.

Fix: reconciliar con `git merge origin/main` + **renumerar** tus migraciones al
siguiente hueco real (`git mv` + `sed` en headers, refs cruzadas en comentarios y
código). Luego `db push` aplica solo las nuevas, limpio.

Ojo: en repos muy activos la colisión REAPARECE si otra rama mergea ENTRE tu PR y tu
merge (caso 2026-06-04: stock chocó 2× — billing 213-218 y luego fase3 219). Tras
renumerar, mergear RÁPIDO y verificar en main post-merge que no hay duplicados:
`git ls-files supabase/migrations | grep -oE '[0-9]{3}_' | sort | uniq -d`.

Relacionado: [[supabase-migration-new-rompe-secuencia-nnn-name]].
