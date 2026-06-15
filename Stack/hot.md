---
title: hot cache
date: 2026-06-14
tags: [stack, index]
---

# Hot Cache

Resúmenes 1 línea + link al learning. Solo lo **activo ≤2 semanas**. Lo anterior
vive en sus learnings (recall por relevancia) y los permanentes en
[[patterns-cross-proyecto]]. Poda 2026-06-14.

## git / sesiones paralelas / migraciones (núcleo activo)

- **Shippear desde working tree compartido sucio → worktree + diff-0** [[shippear-quirurgico-desde-working-tree-compartido-sucio]]
- **Colisiones git multi-sesión (index/MERGE_HEAD/build-lock) → worktree + cherry aislado** [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]]
- **Triaje ramas/worktrees: borrable si cherry-0 o diff-main vacío** [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
- **Worktree facturaia: `node_modules` real para `next build` (symlink rompe Turbopack)** [[worktree-facturaia-build-supabase]]
- **Colisión NNN migraciones (rama stale) → renumerar + `uniq -d` post-merge; el hook pre-push NO la detecta** [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]
- **`migration repair` exige el fichero NNN en el cwd → reparar desde worktree de origin/main** [[supabase-migration-repair-requiere-fichero-nnn-en-cwd]]
- **Migs paralelas CREATE OR REPLACE se pisan → consolidar en la de mayor número** [[migraciones-paralelas-create-or-replace-se-pisan]]
- **Migración aplicada fuera de historial → idempotente + reconciliar schema_migrations** [[migracion-aplicada-fuera-de-historial-supabase]]

- **RPC secundaria opcional (stock inicial, webhook) → devolver warning flag, no silenciar ni 500** [[non-blocking-secondary-rpc-warning-flag]]
- **`.next/lock` stale bloquea `next build`** — `rm .next/lock` cuando "Another build process running" sin proceso activo. Dev server usa `.next/dev/lock` (distinto). Ver [[next-build-lock-stale-devserver]]

## prod / supabase / observabilidad

- **Bugs solo afloran contra schema real** — `.order` columna inexistente → 42703; RPC+trigger misma fila → 23505. E2E real los caza, mocks no. Ver [[supabase-errores-que-solo-afloran-contra-schema-real]]
- **Smoke de RPCs/triggers contra prod sin residuo: `BEGIN; DO $$..asserts..$$; ROLLBACK`** [[smoke-prod-en-transaccion-rollback]]
- **Dokploy `compose.one` devuelve `deployments[]` SIN ordenar → sort por createdAt** [[dokploy-api-deployments-sin-ordenar]]
- **supabase `auth.getUser()` es red (round-trip GoTrue) → validar 1 vez en el wrapper** [[supabase-auth-getuser-valida-en-red-dedupe-pipeline]]
- **Output LLM nunca con cast ciego: safeParse Zod + audit del parse failure en BD** [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]]
- **Agregado cacheado sobre ledger (ej anticipo) → recompute por trigger desde Σ activas** [[agregado-cacheado-sobre-ledger-recompute-trigger]]
- **`migration repair`/`db push` necesitan pooler 5432; si cae → Dashboard SQL + repair luego** [[reference-supabase-db-access]]

## frontend (FacturaIA glass / UX activo)

- **Modal/popover sin `createPortal` atrapado por ancestro con stacking (sticky/transform/backdrop-filter)** [[modal-portal-stacking-sticky-sidebar]]
- **Efecto que recarga por entidad + setters que mergean → reset explícito del estado per-entidad** [[effect-reload-por-entidad-setters-merge-exigen-reset]]
- **Playwright: `isVisible({timeout})` no espera (usa `waitFor`); `page.request` cachea HTTP** [[playwright-isvisible-ignora-timeout-usar-waitfor]]
- **CSS Module Turbopack: kebab-case → `undefined` silencioso; usar camelCase** [[css-module-camelcase-turbopack]]
- **Layout server App Router NO ve el pathname → guard por página con helper, no en layout** [[nextjs-layout-no-lee-pathname-server-side]]
