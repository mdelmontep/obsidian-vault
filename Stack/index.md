---
title: stack index
date: 2026-04-20
tags: [stack, index]
---

# Stack — Patrones Reutilizables

Índice de conocimiento técnico organizado por herramienta.
Para lo reciente (< 2 semanas), ver [[hot]].

## Infraestructura

- [[docker-infra]] — Traefik, Dokploy, healthchecks, passwords, credenciales

## Servicios

- [[n8n]] — workflows, Kommo, AI Agents, API, migraciones
- [[chatwoot]] — deploy, automation rules, teams, WhatsApp Cloud
- [[supabase-cloud]] — proyectos SaaS (TuFacturaIA), psql, connection pooler, RLS
- [[supabase-selfhosted]] — vector store para RAG, pgvector, LangChain schema

## Voice / Retell

- [[retell/retell-sdk-patterns]] — SDK, webhooks, parameter_type, checklist pre-deploy
- [[retell/retell-nuevas-features-abril-2026-evaluar]] — Subagent Nodes, JS inline, SMS en llamada

## Frontend

- [[frontend-css-mobile]] — overflow horizontal, sticky headers, checklist mobile
- [[frontend-motion]] — motion/react, performance, willChange, repeat:Infinity
- [[frontend-images]] — webp, SVG marcas, overlays

## Herramientas

- [[notion]] — estructura workspace, API limitations
- [[slack]] — bot API, canvas, scopes

## Learnings

- Ver `knowledge/learnings/` — 40+ aprendizajes técnicos individuales con tags

## Transversales recurrentes (movidos de [[hot]] en poda 2026-06-19)

### git / worktrees / migraciones
- **Shippear desde working tree compartido sucio → worktree + diff-0** [[shippear-quirurgico-desde-working-tree-compartido-sucio]]
- **Colisiones git multi-sesión (index/MERGE_HEAD/build-lock) → worktree + cherry aislado** [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] · triaje borrable si cherry-0/diff-main vacío [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
- **Worktree facturaia: `node_modules` real para `next build` (symlink rompe Turbopack)** [[worktree-facturaia-build-supabase]]
- **Colisión NNN migraciones (rama stale) → renumerar + `uniq -d` post-merge; el hook pre-push NO la detecta** [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]
- **Migración aplicada fuera de historial → idempotente + reconciliar schema_migrations** [[migracion-aplicada-fuera-de-historial-supabase]]

### método prod / supabase
- **Bugs solo afloran contra schema real** — `.order` columna inexistente → 42703; RPC+trigger misma fila → 23505. E2E real los caza, mocks no. [[supabase-errores-que-solo-afloran-contra-schema-real]]
- **Smoke de RPCs/triggers contra prod sin residuo: `BEGIN; DO $$..asserts..$$; ROLLBACK`** [[smoke-prod-en-transaccion-rollback]]
- **Auditar performance: priorizar por tamaño real de tabla (`pg_stat_user_tables`)** [[auditoria-performance-priorizar-por-tamano-real-de-tabla]] · tablas de log sin retención dominan la BD [[tablas-de-log-sin-retencion-dominan-el-tamano-de-la-bd]]
- **`auth.getUser()` es red (round-trip GoTrue) → validar 1 vez en el wrapper** [[supabase-auth-getuser-valida-en-red-dedupe-pipeline]]
- **Output LLM nunca con cast ciego: safeParse Zod + audit del parse failure en BD** [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]]
- **`migration repair`/`db push` necesitan pooler 5432; si cae → Dashboard SQL + repair luego** [[reference-supabase-db-access]]
- **Rate-limit key por IP confiable** — nunca `xff[0]` (spoofeable); `x-real-ip` / último hop. Helper `lib/http/client-ip.ts`. [[traefik-dokploy-client-ip-x-real-ip-o-ultimo-xff]]

### frontend glass / UX
- **Controles nativos no estilables** — el popup de `<input type=date>` y la lista de `<select>` los pinta el SO; componente propio + portar. [[controles-form-nativos-no-estilables-construir-componente]] · unificar sin tocar N clases [[unificar-controles-regla-global-not-specificity]]
- **Modal/popover sin `createPortal` atrapado por ancestro con stacking (sticky/transform/backdrop-filter)** [[modal-portal-stacking-sticky-sidebar]]
- **z-index: overlays portados = una capa + orden de portal decide; tokenizar value-preserving** [[zindex-capa-overlay-orden-portal]] · no forzar base en paneles divergentes [[no-forzar-base-en-paneles-divergentes]]

### dependencias / LLM
- **Modelo Anthropic retirado tras bump SDK** — validar model-ids con `GET /v1/models` (POST messages no sirve sin saldo). [[verificar-modelos-anthropic-vigentes-via-get-v1-models]]
- **`npm audit fix --force` downgradea majors** — leer "Will install"; vulns transitivas → `overrides`, no --force a ciegas. [[npm-audit-fix-force-propone-downgrades-trampa]]
