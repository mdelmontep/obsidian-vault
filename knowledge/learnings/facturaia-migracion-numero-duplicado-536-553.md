---
title: migración con número duplicado se cuela cuando ramas paralelas mergean el mismo hueco
date: 2026-07-24
source: claude-code-session
tags: [facturaia, migraciones, supabase, git]
---

PR #1111 (`536_obras_uo_calcular_batch.sql`, creada 21-jul) y PR #1114
(`536_obras_responsable.sql`, creada 21-jul, mergeada primero el mismo día)
reservaron el mismo número `536` al abrir rama, y solo se detectó el choque
al revisar #1111 tres días después, ya mergeada.

Por qué: la convención de FacturaIA numera "al abrir el PR", no al crear la
rama — pero si dos ramas abren PR casi a la vez, ambas pueden ver el mismo
hueco libre antes de que la primera mergee.

Fix aplicado: `git mv` al primer hueco real tras el máximo actual (no el
primer hueco histórico — había gaps antiguos sin rellenar) + actualizar
cabecera del SQL y las referencias cruzadas en comentarios de código
(`grep -rn "mig 536"` para no tocar referencias al OTRO 536 por error).

Detección: `git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d`
— correrlo tras cada merge de migración, no solo antes de abrir PR (ya es la
4ª vez que pasa en este proyecto, ver CLAUDE.md §Migraciones "Caso real").
