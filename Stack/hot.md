---
title: hot cache
date: 2026-06-18
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: 1 línea + link al learning. Solo lo de la semana + transversales
que reaparecen cada sesión + el área activa hoy. Lo demás vive en `knowledge/learnings/`
(recall por relevancia, no hace falta indexarlo) y los patrones universales en
[[patterns-cross-proyecto]]. Poda 2026-06-18 (de ~50 → ventana caliente).

## de la semana

- **next start sin HMR / puerto equivocado en QA** — edits invisibles, server sirve build viejo; el `next dev` con HMR puede estar en otro puerto. Ver [[next-start-build-estatico-sin-hmr-verificar-puerto]]
- **react-hooks/refs falso positivo con floating-ui** — el React Compiler marca `refs.setFloating` como ref-en-render; el hook expone `setReference`/`setFloating` top-level (no objeto `refs`). Ver [[react-hooks-refs-falso-positivo-floating-ui]]
- **Hilo con varios públicos → compositor con selector de destinatario** — cajas separadas con destino implícito = mensaje al destino equivocado; unificar + default seguro + etiqueta de destino. Ver [[compositor-multidestino-selector-explicito]]
- **Supabase Storage REST + keys `sb_secret_`** — subir/borrar por curl exige `apikey` + `Authorization` (solo Authorization → 400). Ver [[supabase-storage-rest-upload-requiere-apikey-y-authorization]]
- **Rate-limit key por IP confiable** — nunca `xff[0]` (spoofeable); `x-real-ip` / último hop. Helper `lib/http/client-ip.ts`. Ver [[traefik-dokploy-client-ip-x-real-ip-o-ultimo-xff]]
- **MCP remoto = OAuth obligatorio** — conectores remotos no aceptan API key estática (solo MCP local stdio). Ver [[remote-mcp-exige-oauth-no-api-key-estatica]]
- **Acción irreversible ≠ tool MCP autónoma** — annotations son hints; preparar borrador + deep-link para que confirme un humano. Ver [[acciones-irreversibles-no-tool-mcp-autonoma]]
- **jose v6 = ESM-only + tsx→CJS rompe top-level await** — correr como ESM o envolver en `main()`. Ver [[jose-v6-esm-only-tsx-cjs-top-level-await]]
- **Revocar JWT stateless antes de exp = tabla de revocación dedicada** — no inferir de filas de refresh; claim `gid` + `isGrantRevoked` sin caché. Ver [[revocacion-jwt-stateless-tabla-dedicada-no-inferir-de-filas-de-token]]
- **Revocación: comprobar en CADA resource server, no solo el gateway** — mismo JWT aceptado por la API directa lo salta; fail-closed. Ver [[oauth-revocacion-en-cada-resource-server-no-solo-gateway]]
- **QA página server-component con Playwright = inyectar cookie `@supabase/ssr`** — la hidratación del dev no prende (login hace submit nativo); firma server-side y captura la cookie. Ver [[supabase-ssr-cookie-injection-qa-playwright]]
- **Cron Dokploy para código no desplegado = `enabled:false` (pre-staged)** — si no, 404 diario + watchdog en rojo tras deploy. Ver [[dokploy-cron-pre-stage-disabled-si-endpoint-no-desplegado]]

## git / worktrees / migraciones (transversal, reaparece siempre)

- **Shippear desde working tree compartido sucio → worktree + diff-0** [[shippear-quirurgico-desde-working-tree-compartido-sucio]]
- **Colisiones git multi-sesión (index/MERGE_HEAD/build-lock) → worktree + cherry aislado** [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] · triaje borrable si cherry-0/diff-main vacío [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
- **Worktree facturaia: `node_modules` real para `next build` (symlink rompe Turbopack)** [[worktree-facturaia-build-supabase]]
- **Colisión NNN migraciones (rama stale) → renumerar + `uniq -d` post-merge; el hook pre-push NO la detecta** [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]
- **Migración aplicada fuera de historial → idempotente + reconciliar schema_migrations** [[migracion-aplicada-fuera-de-historial-supabase]]

## método prod / supabase (recurrente)

- **Bugs solo afloran contra schema real** — `.order` columna inexistente → 42703; RPC+trigger misma fila → 23505. E2E real los caza, mocks no. Ver [[supabase-errores-que-solo-afloran-contra-schema-real]]
- **Smoke de RPCs/triggers contra prod sin residuo: `BEGIN; DO $$..asserts..$$; ROLLBACK`** [[smoke-prod-en-transaccion-rollback]]
- **Auditar performance: priorizar por tamaño real de tabla (`pg_stat_user_tables`) antes de tocar** [[auditoria-performance-priorizar-por-tamano-real-de-tabla]] · tablas de log sin retención dominan la BD [[tablas-de-log-sin-retencion-dominan-el-tamano-de-la-bd]]
- **`auth.getUser()` es red (round-trip GoTrue) → validar 1 vez en el wrapper** [[supabase-auth-getuser-valida-en-red-dedupe-pipeline]]
- **Output LLM nunca con cast ciego: safeParse Zod + audit del parse failure en BD** [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]]
- **`migration repair`/`db push` necesitan pooler 5432; si cae → Dashboard SQL + repair luego** [[reference-supabase-db-access]]

## frontend glass / UX (área activa — fase unificación fields)

- **Controles nativos no estilables** — el popup de `<input type=date>` y la lista de `<select>` los pinta el SO; componente propio + portar. Ver [[controles-form-nativos-no-estilables-construir-componente]] · unificar sin tocar N clases [[unificar-controles-regla-global-not-specificity]]
- **Modal/popover sin `createPortal` atrapado por ancestro con stacking (sticky/transform/backdrop-filter)** [[modal-portal-stacking-sticky-sidebar]]
- **z-index: overlays portados = una capa + orden de portal decide; tokenizar value-preserving** [[zindex-capa-overlay-orden-portal]] · no forzar base en paneles divergentes [[no-forzar-base-en-paneles-divergentes]]

## dependencias / LLM

- **Modelo Anthropic retirado tras bump SDK** — validar model-ids con `GET /v1/models` (POST messages no sirve sin saldo). Ver [[verificar-modelos-anthropic-vigentes-via-get-v1-models]]
- **`npm audit fix --force` downgradea majors** — leer "Will install"; vulns transitivas → `overrides`, no --force a ciegas. Ver [[npm-audit-fix-force-propone-downgrades-trampa]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra). Lo retirado de aquí sigue en `knowledge/learnings/`.
