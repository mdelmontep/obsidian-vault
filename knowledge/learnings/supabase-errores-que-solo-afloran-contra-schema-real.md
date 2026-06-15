---
title: supabase — bugs que solo afloran contra el schema/estado real (mocks y review estático no los ven)
date: 2026-06-15
source: claude-code-session
tags: [supabase, postgrest, testing, onboarding, e2e]
---
Dos bugs P0 de TuFacturaIA invisibles para 5 agentes de review estático + tests con mocks; un E2E real contra prod los cazó en minutos:

1. **`.order('col')` / `.select('col')` por columna inexistente** → PostgREST `42703`, y `.maybeSingle()` lo entrega como `{ data: null }`. La query "falla en silencio": el código la trata como "no hay fila". Caso: `getOnboardingState` ordenaba `org_members` por `created_at` (la columna real es `invited_at`) → owner=null → propietario enviado a /dashboard, que rebota a /onboarding → **loop infinito de redirects**. Fix: usar la columna real. Verifica nombres con `select('*')` contra la fila real, no de memoria.

2. **RPC que inserta filas que un trigger AFTER INSERT también siembra** → `unique_violation 23505`. Caso: RPC creaba 6 series A/R/P/T/F/B y un trigger previo (mig 211) ya metía B/F al insertar la org → 500 en toda alta. Fix: `ON CONFLICT (...) DO NOTHING` en el INSERT de la RPC (autosuficiente y convive con el trigger).

Meta: errores de nombre-de-columna y de colisión trigger×RPC NO se ven en `tsc`, lint ni vitest mockeado. Para flujos críticos (signup/onboarding), **smoke E2E real contra prod/sandbox** es la única red. Ver [[otp-onboarding-patterns]].
