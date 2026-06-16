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
merge (2026-06-04/05: stock chocó **3×** — billing 213-218, fase3 219, multiempresa
227 → renumerado 213-216→219-222→223-226 y beta 227→228). Tras renumerar, mergear
RÁPIDO y verificar en main post-merge que no hay duplicados:
`git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d` (con la
`/` inicial; sin ella, `e164` en `066_...e164...` da falso positivo "164"). Regla ya
en el CLAUDE.md del proyecto TuFacturaIA: **numerar al ABRIR el PR, no al crear la rama**.

El hook `pre-push` NO detecta la colisión de `NNN` (solo aborta ante timestamps
remotos) → el `uniq -d` post-merge es la única red. Caso 2026-06-14: conciliación
(#231/#235) y onboarding (#232) numeraron `279` en paralelo; el de conciliación ya
estaba aplicado en prod → renumerado **onboarding 279→281** (no la de conciliación).

Caso 2026-06-16: feedback (#275) y categorías (#278) numeraron `301` en paralelo; categorías mergeó primero → renumerado **feedback 301→302**.

Caso 2026-06-16 (2, cascada): factura-simplificada tomó `302/303` sobre main viejo; main ya tenía `302_feedback` → renumerado a **303/304** + traído `302_feedback` a la rama (local==remoto). Señal extra: `schema_migrations` tenía `302` registrado pero sus DDL ausentes del schema real → confirmó que el `302` remoto era OTRO.

Relacionado: [[supabase-migration-new-rompe-secuencia-nnn-name]], [[supabase-migration-repair-requiere-fichero-nnn-en-cwd]].
