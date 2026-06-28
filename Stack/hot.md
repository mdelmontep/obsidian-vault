---
title: hot cache
date: 2026-06-26
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo de la semana (1 línea + link al learning). Los patrones
transversales recurrentes (git/worktrees · método prod · frontend glass · deps) se
movieron a [[index]] §Transversales. Lo demás vive en `knowledge/learnings/` (recall por
relevancia) y los universales en [[patterns-cross-proyecto]]. Podado 2026-06-26 (49→6).

## de la semana

- **Zod v4 trae `z.toJSONSchema` nativo — deriva el tool-schema del LLM, no lo dupliques** — un `input_schema_json` a mano en paralelo al Zod miente al LLM (required/enum divergen). Fuente única: derivar; `.describe()` por campo. Ver [[zod-v4-tojsonschema-nativo-deriva-tool-schema]]
- **Outbox: event-type fuera del catálogo suscribible muere en silencio** — el trigger lo encola pero nadie puede suscribirse → `fanout_completed` sin delivery. Guard: test-contrato emisor(SQL)⊆catálogo(enum). Ver [[outbox-event-type-fuera-del-catalogo-muere-silencioso]]
- **Port devuelve dato discriminado; el caller traduce a throw en su borde** — el port nunca lanza por precondición (found/none/ambiguous, ok/conflict); el framework no cambia y el adapter in-memory testea sin mockear el query-builder. Inyección opcional (`ctx.store?`) = blast radius mínimo. Ver [[port-devuelve-dato-discriminado-tool-traduce-throw-en-borde]]
- **Converger un canal divergente sobre la fuente única** — bordes (auth/cuotas/audit/error-codes) se quedan en el canal; pasar IDs ya resueltos; flags opt-in (`skipAudit`/`checkQuota`/`nifValidation`) para deltas sin tocar otros callers; traductor de errores al `error_code` del canal. Ver [[converger-canal-divergente-sobre-fuente-unica]]
- **Skin app-wide = una palanca de superficie + base opaca aparte** — cards usan `--bg-elev` (el skin lo vuelve translúcido vía `[data-skin]` → todas esmerilan a la vez); `--elev-solid` opaco sostiene el compositing del glass. Blur por regla, no por token. Ver [[skin-app-wide-token-superficie-unico-base-opaca]]
- **Dokploy `autoDeploy=false` = desfase silencioso** — los merges a main no despliegan; el servicio sirve build viejo sin avisar. Fix: GH Action path-filtered o alerta de desfase (hash de `/health` vs main). Ver [[dokploy-autodeploy-false-desfase-silencioso]]

- **E2E smoke: skip honesto por precondición, no falso rojo** — gating por la fuente autoritativa (`featureActive` → `GET /api/settings/features`), nunca texto de UI ni 404; skip SOLO si falta la precondición, jamás relajar una aserción que cace un bug. Ver [[e2e-smoke-skip-honesto]]
- **BD fuente de verdad vía cache en memoria → hidratar en LECTURA** — la cache module-level arranca null tras deploy; si solo hidratas al escribir, el runtime cae al fallback (env) hasta la 1ª escritura. `ensureCache()` lazy en cada consumidor. Ver [[bd-fuente-verdad-via-cache-memoria-hidratar-en-lectura]]
- **Smoke test-mode contamina BD prod si la fn escribe en BD** — Stripe TEST no aísla la BD (única=prod); aísla por dato sentinel desechable + guard que rehúsa `sk_live`. Ver [[smoke-test-mode-contamina-bd-prod-si-la-fn-escribe-bd]]
- **Gate solo en wrapper web no cubre canales** — voz/WA/v1/cron/MCP usan otro auth; el enforcement de plan/cuota/billing debe replicarse por canal o centralizarse en la fuente única. Ver [[gate-en-wrapper-web-no-cubre-canales-con-otro-auth]]
- **Contador de cuota best-effort = cuota infinita** — increment con solo `console.error` tras el check; si el RPC falla, el contador se congela. Hacerlo observable (alerta/tabla con status). Ver [[contador-de-cuota-best-effort-tras-check-es-cuota-infinita]]
- **Stripe price (lo que cobra) ≠ precio BD editable** — lo cobrado vive en el env (`STRIPE_PRICE_ID_*`, price inmutable), no en `plans.precio_mes`; editar admin no cambia el cobro → drift (UI 14€, checkout 19€). Ver [[stripe-price-id-en-env-vs-precio-bd-editable-derivan]]
- **PostgREST corta agregaciones en JS (cap max-rows 1000)** — sumar filas con `reduce` infravalora en silencio; `count:'exact'` sí es exacto → cifra y count incoherentes. Agrega en BD (RPC SUM) o `.limit(N+1)`+`truncated`. Ver [[postgrest-max-rows-trunca-agregacion-en-js]]
- **Motor con input requerido → defaultea, no falles mudo** — un default sensato en el motor (FEFO) > parchear N bordes; los canales ciegos no pueden aportar el campo. Ver [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]]
- **Actions caído (billing) → hooks locales = único gate** — un merge con `--no-verify` cuela lint/build roto a main. `npm run lint` global antes de cada merge; node_modules real (`npm ci`) para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]]
- **Hook pre-commit (build) muere por OOM si hay dev server vivo** — lo reporta como "lint con errores" (falso positivo). Matar `npm run dev` antes de commitear. Ver [[pre-commit-hook-oom-con-dev-server]]
- **Remesa SEPA pain.008 (adeudo directo)** — SeqTp a nivel PmtInf, control del Id de Acreedor `98-mod97(idNac+ES00)`, CtrlSum en céntimos, IBAN single-source. Ver [[sepa-pain008-remesa-adeudo]]
- **Cron materializador + collector en vivo = dedup en runtime, no con filtro de origen** — filtrar el cron crea gap cuando el servicio recupera entre ticks. Ver [[alert-collector-cron-vs-live-dedup-gap]]
- **Turbopack rechaza node_modules symlinkeado en worktree** — `tsc`/`vitest` sí, `next build` no; usar `npm install` real. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **`git diff main <branch>` engaña si tu main local avanzó** — otra sesión mergea → ves cambios fantasma como del branch; usa `git diff $(git merge-base main <branch>) <branch>` o `git show --stat HEAD` en el worktree. Ver [[git-diff-vs-main-drifteado-usar-merge-base]]
- **Pill `overflow:hidden` en grid rígido se recorta en modal estrecho** — dentro de modal/drawer el ancho ≠ viewport → usa **container query** (`container-type: inline-size` + `@container`), no `@media`. Ver [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]]
- **Reempaquetar planes → grandfathering ANTES de tocar `plan_features`** — snapshot a `org_features` (source `grandfathered`) de lo que cada org activa tiene hoy, misma migración, o los clientes pierden acceso. Ver [[grandfathering-snapshot-antes-de-reempaquetar-planes]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/` (recall por relevancia).

- **Smoke visual SSR sin password** — sesión Supabase inyectada en Playwright (generateLink+verifyOtp+cookie sb-ref base64). Ver [[smoke-visual-ssr-sesion-inyectada-playwright]]
