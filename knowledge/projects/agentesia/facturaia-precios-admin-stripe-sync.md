---
title: facturaia — panel precios admin sincronizado con Stripe
date: 2026-06-26
source: claude-code-session
tags: [facturaia, billing, stripe, admin, precios]
---

# Panel de precios admin ↔ Stripe (fuente única de verdad)

**Rama:** `feat/precios-admin-stripe-sync` (pusheada a origin, **sin PR abierto aún**).
**PRD:** `issues/prd-precios-admin-stripe-sync.md` · **issues:** `issues/precios-001..008`.

## Por qué
Los `STRIPE_PRICE_ID_*` vivían en el env de Dokploy y `plans.precio_mes` en BD, **desconectados** → bug real 2026-06-26: Starter BD=14€ / Stripe cobraba 19€. Este proyecto hace la BD la fuente única; editar precio en admin crea el price en Stripe (create+archive, grandfathering).

## Estado (2026-06-26) — 6 issues de código HECHOS, gate verde, pusheados
- **001** mig `404_plan_prices.sql` (tabla + RLS service-role-only + backfill 12 precios) — **APLICADA A PROD MANUALMENTE** (psql) + versión 404 registrada en `schema_migrations` (repo↔prod sin divergencia). 12 filas verificadas.
- **002** `stripe-plans.ts` lee de `plan_prices` (cache forward=active, reverse=incl. archivados para grandfathering) con fallback a env; **firmas sync intactas** (no rompe checkout/change-plan/webhook). 11 tests.
- **003** `stripe-prices.ts` helper `createPriceForTarget` (create+archive, idempotente por importe). 6 tests.
- **004** endpoint `POST/GET /api/admin/plans/[id]/prices` (requireAdmin+Zod+audit). 5 tests.
- **005** UI sección "Precios Stripe" en `/admin/plans` + modal grandfathering. **Smoke visual VERDE** (capturas en sesión): panel con Starter 14€, editor con la sección, modal abre. NO se pulsó "Crear price" (es `sk_live`).
- **006** `price-coherence.ts` + collector `price-coherence` en el health-sweep (alerta BD↔Stripe). 5 tests.

Commits: `53a792d3`(PRD) · `ba0d63a1`(001/002) · `a7db2ff8`(003) · `35a4ce1d`(004) · `6b81aa50`(006) · `3485f5f2`(005).

## Cómo continuar (próxima sesión) — pasos exactos
1. **Worktree**: el principal puede estar en otra rama (sesiones paralelas). Usar el worktree dedicado o recrearlo: `git worktree add .claude/worktrees/precios feat/precios-admin-stripe-sync`. El `.env.local` NO viaja al worktree → copiarlo del principal si hace falta dev server.
2. **Abrir PR** a `main`: `gh pr create`. Antes verificar colisión de número de migración: `git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d`. La 404 ya está aplicada en prod con ese número, así que **mantener 404** (no renumerar salvo que choque en el repo; si choca, renumerar archivo Y reconciliar `schema_migrations` en prod).
3. **Merge** (CI Actions sigue bloqueado por billing → `gh pr merge --admin` con OK de Manuel). Tras merge, `git log origin/main..HEAD` vacío.
4. **Issue 007 (go-live, HITL)**: probar "Crear price" en **Stripe TEST mode** primero (cambiar `STRIPE_SECRET_KEY` a test key en local), verificar create+archive+checkout; luego habilitar en LIVE con OK de Manuel. **NUNCA** pulsar el botón contra `sk_live` sin querer cobrar de verdad.
5. **Issue 008 (opcional)**: webhook `price.*` para reflejar cambios hechos desde el dashboard de Stripe.

## Gotchas de esta sesión
- **Smoke visual de página admin SSR sin password**: `generateLink`(service-role)+`verifyOtp`(anon)→session, e inyectar cookie `sb-<ref>-auth-token` = `base64-<base64(JSON session)>` (chunked .0/.1 si >3600) en Playwright. Ver [[smoke-visual-ssr-sesion-inyectada-playwright]].
- **No localhost en redirect allowlist de Supabase prod** → el magic-link navegado no sirve para local; por eso cookie inyectada.
- Materializa [[stripe-price-id-en-env-vs-precio-bd-editable-derivan]] y [[supabase-bypassear-plantilla-auth-con-admin-generatelink]].

## También cerrado esta sesión (no de este proyecto)
- **Cableado Starter 14€** aplicado a Dokploy prod (`STRIPE_PRICE_ID_STARTER_MENSUAL/ANUAL` → `price_1TmYfU/1TmYfV`) + deploy. Los prices de Plus (29/278,40) ya existían y estaban cableados.
