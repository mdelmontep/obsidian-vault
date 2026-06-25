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

- **Migrar input nativo → componente con overlay** — borra las reglas CSS del nativo (`.wrapper input[type=checkbox]{width}` (0,2,1) gana al `.input{width:100%}` (0,1,0) y encoge el área clicable); wrapper `<span>` no `<label>`. Ver [[checkbox-overlay-migracion-especificidad-css]]
- **Motor con input requerido → defaultea, no falles mudo** — un default sensato en el motor (FEFO) > parchear N bordes; los canales ciegos no pueden aportar el campo. Ver [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]]
- **Chatwoot API: `/contacts/search` es GET (POST→404) + `source_id` de `POST /contacts` en `payload.contact_inbox`** — gotchas al crear contacto/conv vía API Channel. Ver [[../Stack/chatwoot]] §API contacts/conversations
- **Error handler n8n global** — 1 workflow `Error Trigger→Set→httpRequest`, asignar `settings.errorWorkflow` a todos vía API; Incoming Webhook Slack > nodo OAuth (portable); NO se hereda en nuevos. Ver [[n8n-error-handler-global-via-errorworkflow]]
- **n8n: ramas paralelas no garantizan orden** — si B usa `$('A')` y A es hermana, ponerlo en serie (no `$if(isExecuted)`, que deja el dato vacío). Ver [[n8n-ramas-paralelas-no-garantizan-orden-poner-en-serie]]
- **Actions caído (billing) → hooks locales = único gate** — un merge con `--no-verify` cuela lint/build roto a main (caso SEPA: `react-hooks/set-state-in-effect` en facturas-view). `npm run lint` global antes de cada merge; node_modules real (`npm ci`) para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]]
- **NIF receptor solo si B2B** — consumidor final no lo necesita ni con Verifactu activo (clave F2). Exigirlo es más restrictivo que la ley. Ver [[nif-receptor-obligatorio-solo-3-supuestos-verifactu]]

- **Remesa SEPA pain.008 (adeudo directo)** — SeqTp a nivel PmtInf, control del Id de Acreedor `98-mod97(idNac+ES00)`, CtrlSum en céntimos, IBAN single-source. Ver [[sepa-pain008-remesa-adeudo]]
- **Reconciliar estado externo al reiniciar** — no cancelar+recrear (avalancha de filas fantasma + pérdida de SL/TP); re-trackear por clave natural preservando id. Ver [[reconciliar-estado-externo-al-reiniciar-no-cancelar-recrear]]
- **Cron materializador + collector en vivo = dedup en runtime, no con filtro de origen** — filtrar el cron crea gap cuando el servicio recupera entre ticks. Ver [[alert-collector-cron-vs-live-dedup-gap]]
- **TS `as const` no indexable con genérico K** — cast a `Record<TemplateKind, ...>[K]`. Ver [[ts-as-const-no-indexable-con-generico-k]]
- **`git stash` sin `-u` deja untracked; hook pre-commit los detecta igual** — build falla; usar `git stash -u`. Ver [[git-stash-sin-u-deja-untracked-y-hook-falla]]

- **Loop/harness design** — LOOP SPEC (GOAL/VERIFY/STOP WHEN/ON STOP) + maker/checker + 4 criterios "¿vale un loop?" + herramientas por complejidad. Ver CLAUDE.md §Loops y harness · §Modo de trabajo

- **QA Next contra Supabase local sin tocar `.env.local` de prod** — `.env.development.local` (solo overrides locales) gana sobre `.env.local`. Ver [[next-env-development-local-precede-a-env-local]]
- **Pill/chip no reemplaza un dato accionable en un form denso** — consistencia de lenguaje (token color) ≠ de componente. Ver [[pill-no-reemplaza-dato-accionable-en-formulario]]
- **GitHub App no incluye repos creados tras la instalación** — añadir manualmente en GitHub → Settings → Applications → Configure. Ver [[github-app-no-incluye-repos-nuevos-automaticamente]]
- **`.next` typed-routes validator stale tras cambiar de rama** — `tsc` falla con `Cannot find module '.../route.js'` por caché del build anterior; `next build` antes de `tsc`. Ver [[next-typed-routes-validator-stale-tras-cambio-de-rama]]
- **2 PRs mismo archivo → `git merge-tree` antes de mergear** — detecta el conflicto sin checkout; squash rompe `branch --merged` (borrar con `-D`). Ver [[merge-tree-precheck-cross-pr-y-squash-branch-cleanup]]
- **Impersonación superadmin NO sirve para QA org-scoped** — caduca ~1h + el proxy no devuelve listas paginadas (vacías + parpadeo); QArear con usuario real. Ver [[impersonacion-superadmin-no-sirve-para-qa-de-ui-org-scoped]]
- **Settings rotos impersonando** — leer org con `createClient()`/`getOrgId()` devuelve 0 filas (RLS) o la org del superadmin; usar `useOrg().orgId` + `useOrgClient()`. Ver [[settings-leen-con-createclient-getorgid-se-rompen-impersonando]]
- **Turbopack rechaza node_modules symlinkeado en worktree** — `tsc`/`vitest` sí, `next build` no; usar `npm install` real. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **Tabla Supabase ausente = PGRST205 (no 42P01) vía supabase-js** — los guards de degradación deben mirar `code==='PGRST205'`; lo destapa un smoke, no typecheck/build. Ver [[supabase-tabla-ausente-postgrest-pgrst205-no-42p01]]
- **Aceptar sugerencia HITL debe cerrar la decisión** — si no, el gate de acierto mide ~0% y nunca abre. Ver [[aceptar-sugerencia-hitl-debe-cerrar-decision-o-el-gate-no-abre]]

- **CREATE OR REPLACE desde la versión vigente** — copiar el cuerpo del último `NNN_` que define la función (no del issue ni de memoria); `diff` verbatim base-vs-nueva. Regresión semántica que typecheck/tests no ven. Vale doble si lo escribe un subagente. Ver [[create-or-replace-copiar-de-version-vigente]]
- **useMemo para objeto en deps de hook** — objeto literal inline = nueva ref cada render = render loop; wrappear con useMemo en el consumidor. Ver [[usememo-objeto-inline-en-deps-render-loop]]
- **MCP scope grantable vs verifier divergen** — añadir un scope solo en `policy.ts` (well-known/registro) y no en `VALID_SCOPE` del verifier (`user-token.ts`) → token 401 "non-grantable"; allowlist duplicada por defense-in-depth necesita test que itere la canónica. Ver [[mcp-scope-grantable-vs-verifier-divergen]]
- **Dokploy compose autoDeploy=false no recibe merges** — `mcp-server`/`ticket-runner` no auto-despliegan; tras mergear → `compose.deploy` manual. Ver [[dokploy-compose-autodeploy-false-no-recibe-merges]]
- **Rotación refresh: ventana de gracia anti-falso-positivo** — reintento legítimo del mismo refresh rotado (red/doble submit) NO debe revocar la familia; gracia N s + mismo client_id (RFC 9700). Ver [[oauth-refresh-rotation-idempotencia-ventana-gracia]]
- **Paginación TuFacturaIA** — `PaginationBar` + `usePaginationParams` listos. Issues 004 ✅ 005 ✅ 006 ✅ 007 ✅; 008 conciliacion. Ver [[ADR-034-paginacion-offset-vs-keyset]] · [[tdd-pure-function-extraction]]
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
- [[progreso-real-vs-simulado-tareas-opacas]] — progreso async sin parpadeo: hitos reales backend + merge monótono `max()` + estimador `1−e^(−t/τ)`, nunca `Math.random`.
- [[verificacion-no-mutar-estado-prod-cuenta-real]] — tests no mutan estado prod del user real: `.env.test` puede apuntar a prod + `E2E_EMAIL`=tu cuenta → writes tocan tu sesión viva.
- **Glassmorphism en email sin backdrop-filter** — rgba borders + sombra capas + gradiente wrapper; animación CSS gated con `<!--[if !mso]>`. Ver [[email-glassmorphism-sin-backdrop-filter]]
