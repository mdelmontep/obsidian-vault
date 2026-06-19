---
title: hot cache
date: 2026-06-19
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo de la semana (1 línea + link al learning). Los patrones
transversales recurrentes (git/worktrees · método prod · frontend glass · deps) se
movieron a [[index]] §Transversales (poda 2026-06-19). Lo demás vive en
`knowledge/learnings/` (recall por relevancia) y los universales en [[patterns-cross-proyecto]].

## de la semana

- **MCP scope grantable vs verifier divergen** — añadir un scope solo en `policy.ts` (well-known/registro) y no en `VALID_SCOPE` del verifier (`user-token.ts`) → token 401 "non-grantable"; allowlist duplicada por defense-in-depth necesita test que itere la canónica. Ver [[mcp-scope-grantable-vs-verifier-divergen]]
- **Dokploy compose autoDeploy=false no recibe merges** — `mcp-server`/`ticket-runner` no auto-despliegan; tras mergear → `compose.deploy` manual. Ver [[dokploy-compose-autodeploy-false-no-recibe-merges]]
- **Paginación TuFacturaIA** — `PaginationBar` + `usePaginationParams` listos. Issues 004 ✅ 005 ✅ 006 ✅; 007 inventario → 008 conciliacion. Ver [[ADR-034-paginacion-offset-vs-keyset]] · [[tdd-pure-function-extraction]]
- **Hook paginado + hook índice separado** — lista paginada con stats por página + carga ligera full-list para merge/NIF dups. Mutations → `reload()+indexReload()`. Ver [[paginated-hook-dual-index-pattern]]
- **refreshKey en useEffect para invalidar hook paginado post-mutación** — en useEffect deps, no useCallback deps (eslint lo marca innecesario en useCallback). Ver [[paginated-hook-refreshkey-invalidation]]
- **pre-push hook: saltar build en --delete** — leer stdin al inicio; SHA local = `000…0` → exit 0 inmediato. Ver [[git-pre-push-hook-no-guarda-stdin-ni-sale-en-deletes]]

- **contador de numeración editable sin constraint único = duplicados** — bajar el "Nº actual" de una serie reusa números ya emitidos; guard en app (#414) + índice único en BD (#420, mig 343, en prod). Ver [[serie-contador-editable-sin-constraint-unico-genera-duplicados]]

- **`hidden` anulado por clase con `display`** — acordeón/disclosure siempre abierto si la clase pone `display:flex/grid`; `[hidden]{display:none}` (UA) pierde por orden de fuente. Fix `.clase[hidden]{display:none}`. Ver [[hidden-anulado-por-clase-con-display]]
- **next start sin HMR / puerto equivocado en QA** — edits invisibles, server sirve build viejo; el `next dev` con HMR puede estar en otro puerto. Ver [[next-start-build-estatico-sin-hmr-verificar-puerto]]
- **react-hooks/refs falso positivo con floating-ui** — el React Compiler marca `refs.setFloating` como ref-en-render; el hook expone `setReference`/`setFloating` top-level (no objeto `refs`). Ver [[react-hooks-refs-falso-positivo-floating-ui]]
- **Hilo con varios públicos → compositor con selector de destinatario** — cajas separadas con destino implícito = mensaje al destino equivocado; unificar + default seguro + etiqueta de destino. Ver [[compositor-multidestino-selector-explicito]]
- **Supabase Storage REST + keys `sb_secret_`** — subir/borrar por curl exige `apikey` + `Authorization` (solo Authorization → 400). Ver [[supabase-storage-rest-upload-requiere-apikey-y-authorization]]
- **Revocar JWT stateless antes de exp = tabla de revocación dedicada** — no inferir de filas de refresh; claim `gid` + `isGrantRevoked` sin caché. Ver [[revocacion-jwt-stateless-tabla-dedicada-no-inferir-de-filas-de-token]]
- **Revocación: comprobar en CADA resource server, no solo el gateway** — mismo JWT aceptado por la API directa lo salta; fail-closed. Ver [[oauth-revocacion-en-cada-resource-server-no-solo-gateway]]
- **QA página server-component con Playwright = inyectar cookie `@supabase/ssr`** — la hidratación del dev no prende (login hace submit nativo); firma server-side y captura la cookie. Ver [[supabase-ssr-cookie-injection-qa-playwright]]
- **Cron Dokploy para código no desplegado = `enabled:false` (pre-staged)** — si no, 404 diario + watchdog en rojo tras deploy. Ver [[dokploy-cron-pre-stage-disabled-si-endpoint-no-desplegado]]
- **Bypass de pago en toggle de features** — endpoint que escribe `org_features` overrides debe gatear enable por plan/compra (`org_has_feature` da precedencia al override). Ver [[endpoint-toggle-feature-debe-gatear-enable-por-plan-o-compra]]
- **Advisor Supabase: trigger fns DEFINER = ruido** — `RETURNS trigger` no es RPC-invocable; helpers RLS no revocar; verificar con `has_function_privilege`. Dep importada en runtime no declarada (solo transitiva/dev)=drift+CVE [[import-runtime-dep-no-declarada-solo-transitiva]]. Ver [[supabase-advisor-trigger-functions-definer-son-ruido]]
- **Watchdog cron: umbral 2× intervalo** — <1× da falso positivo por un tick perdido del scheduler (deploy/jitter). Ver [[watchdog-umbral-debe-tolerar-un-tick-perdido]]
- **CLS por client-fetch en App Router → SSR-seed** — provider/hook que fetchea (ready false→true) hace aparecer nav/widgets tras el paint; el server layout precomputa y pasa `initialData` (fetch+resolve compartido, paralelizado para no costar TTFB). Ver [[ssr-seed-contra-cls-de-client-fetch-en-app-router]]
- **Medir CWV autenticado sin lighthouse** — Playwright + storageState + PerformanceObserver (LCP/CLS/`entry.sources`); CLS variable → página-control sin tocar para descartar sesgo. Next 16 Turbopack no imprime First Load JS [[next16-turbopack-no-imprime-first-load-js]]. Ver [[medir-cwv-autenticado-sin-lighthouse]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/`.
- [[mcp-conector-remoto-limites-claude-chatgpt-cursor]] — no se puede "empujar" un conector MCP a Claude/ChatGPT; 1-clic solo en Cursor; Team/Enterprise solo Owner.
- [[mcp-connect-claude-origin-claude-com-y-aud-trailing-slash]] — connect MCP a Claude rompe por Origin claude.com (403) y aud con barra final (401, bucle refresh); diag reproduciendo el flujo + BD oauth_refresh_tokens.
- [[contenido-llm-en-pdf-render-como-react-no-html]] — texto de un LLM en un PDF: nodos React (escapa), nunca HTML crudo/innerHTML; markdown acotado = parser propio a React, no DOMPurify.
