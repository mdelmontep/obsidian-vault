---
title: hot cache
date: 2026-06-14
tags: [stack, index]
---

# Hot Cache

- **Supabase Storage REST + keys `sb_secret_`** — subir/borrar por curl exige `apikey` + `Authorization` (solo Authorization → 400, despista). Ver [[supabase-storage-rest-upload-requiere-apikey-y-authorization]]

Resúmenes 1 línea + link al learning. Solo lo **activo ≤2 semanas**. Lo anterior
vive en sus learnings (recall por relevancia) y los permanentes en
[[patterns-cross-proyecto]]. Poda 2026-06-14.

## git / sesiones paralelas / migraciones (núcleo activo)

- **Shippear desde working tree compartido sucio → worktree + diff-0** [[shippear-quirurgico-desde-working-tree-compartido-sucio]]
- **Colisiones git multi-sesión (index/MERGE_HEAD/build-lock) → worktree + cherry aislado** [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]]
- **Triaje ramas/worktrees: borrable si cherry-0 o diff-main vacío** [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
- **Worktree facturaia: `node_modules` real para `next build` (symlink rompe Turbopack)** [[worktree-facturaia-build-supabase]]
- **E2E: `request.newContext` hereda storageState (anon → vacío); multi-org → fijar `active_org_id` en seed** [[playwright-request-newcontext-hereda-storagestate]]
- **Colisión NNN migraciones (rama stale) → renumerar + `uniq -d` post-merge; el hook pre-push NO la detecta** [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]
- **`migration repair` exige el fichero NNN en el cwd → reparar desde worktree de origin/main** [[supabase-migration-repair-requiere-fichero-nnn-en-cwd]]
- **Migs paralelas CREATE OR REPLACE se pisan → consolidar en la de mayor número** [[migraciones-paralelas-create-or-replace-se-pisan]]
- **Migración aplicada fuera de historial → idempotente + reconciliar schema_migrations** [[migracion-aplicada-fuera-de-historial-supabase]]

- **RPC secundaria opcional (stock inicial, webhook) → devolver warning flag, no silenciar ni 500** [[non-blocking-secondary-rpc-warning-flag]]
- **`.next/lock` stale bloquea `next build`** — `rm .next/lock` cuando "Another build process running" sin proceso activo. Dev server usa `.next/dev/lock` (distinto). Ver [[next-build-lock-stale-devserver]]
- **Runner/bot que hace `git push` dispara el pre-push hook (`npm build`) → doble build → OOM** — push con `--no-verify` (el runner ya gatea aparte); y chequear exit codes de subprocesos o un fallo se disfraza de éxito. Ver [[runner-headless-git-push-dispara-pre-push-hook]]

## prod / supabase / observabilidad

- **GitHub Code Quality** — preview sin API, triaje en UI; 4 reglas ≈ ruff (S110/SIM115/F401/F841). Ver [[github-code-quality-triage]]
- **CodeQL Code Scanning (seguridad)** — REST sí funciona (dismiss vía API, auto-mode lo bloquea→`!`); recetas fix bad-tag-filter/redos-email/biased-random. Ver [[codeql-security-alerts-fixes]]
- **Bugs solo afloran contra schema real** — `.order` columna inexistente → 42703; RPC+trigger misma fila → 23505. E2E real los caza, mocks no. Ver [[supabase-errores-que-solo-afloran-contra-schema-real]]
- **Smoke de RPCs/triggers contra prod sin residuo: `BEGIN; DO $$..asserts..$$; ROLLBACK`** [[smoke-prod-en-transaccion-rollback]]
- **Dokploy `compose.one` devuelve `deployments[]` SIN ordenar → sort por createdAt** [[dokploy-api-deployments-sin-ordenar]]
- **supabase `auth.getUser()` es red (round-trip GoTrue) → validar 1 vez en el wrapper** [[supabase-auth-getuser-valida-en-red-dedupe-pipeline]]
- **Output LLM nunca con cast ciego: safeParse Zod + audit del parse failure en BD** [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]]
- **Propuesta destructiva (propose/confirm) NO se persiste como texto del assistant → el LLM imita y narra en vez de llamar al tool; persistir como tool_use+tool_result sintético** [[persistir-propuesta-destructiva-como-texto-entrena-al-llm-a-narrar]]
- **`max_tokens` bajo trunca el JSON de OCR largo (multi-albarán) → faltan líneas; subirlo no encarece las cortas** [[max-tokens-es-tope-no-consumo-trunca-json-ocr-largo]]
- **Agregado cacheado sobre ledger (ej anticipo) → recompute por trigger desde Σ activas** [[agregado-cacheado-sobre-ledger-recompute-trigger]]
- **Proyección de ledger sin detector de drift diverge en silencio (UPDATE directo/recompute la oculta) → detector + reconcile con audit** [[proyeccion-de-ledger-sin-guardia-diverge-en-silencio]]
- **Sembrar base desde total IVA-incluido pierde céntimo** — base sin redondear si el precio no se ve; tolerancia "conciliado" = fuente única BD/UI (no umbral por capa). Ver [[sembrar-base-desde-total-con-iva-pierde-centimo]]
- **`migration repair`/`db push` necesitan pooler 5432; si cae → Dashboard SQL + repair luego** [[reference-supabase-db-access]]
- **API route que hace `fetch` a sí mismo falla en Docker (hairpin NAT) → extraer lógica a lib, no HTTP; smoke en PROD no solo local** [[self-fetch-entre-api-routes-falla-en-docker-prod-extraer-a-lib]]
- **Smoke `/api/internal/*` en prod: firma HMAC con secreto de PROD (no .env.local) + mutaciones solo sobre sandbox** [[smoke-endpoint-interno-prod-firma-hmac-prod-secret]]

## supabase / postgrest SDK

- **PostgREST SDK `.or()` no compara columnas entre sí** — usar filtro en memoria o RPC con SQL nativo. Ver [[postgrest-sdk-or-no-compara-columnas]]
- **Validar migración sin tocar prod** — supabase local: init + puertos 544xx (si hay otro stack) + `db reset --local` + smoke con `session_replication_role=replica`. Ver [[validar-migracion-en-supabase-local-sin-tocar-prod]]
- **Unique de idempotencia con dimensión opt-in** — `NULLS NOT DISTINCT` (PG15+): filas NULL intactas, las nuevas habilitan la dimensión. Ver [[nulls-not-distinct-idempotencia-con-discriminador-opcional]]
- **Función `RETURNS composite` con 0 filas → PostgREST devuelve `{id:null,…}` (truthy), NO `null`** — `data ?? null` lo deja pasar como objeto fantasma; validar un campo clave (`data?.id`). Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]]

## frontend (FacturaIA glass / UX activo)

- **Modal/popover sin `createPortal` atrapado por ancestro con stacking (sticky/transform/backdrop-filter)** [[modal-portal-stacking-sticky-sidebar]]
- **Efecto que recarga por entidad + setters que mergean → reset explícito del estado per-entidad** [[effect-reload-por-entidad-setters-merge-exigen-reset]]
- **Playwright: `isVisible({timeout})` no espera (usa `waitFor`); `page.request` cachea HTTP** [[playwright-isvisible-ignora-timeout-usar-waitfor]]
- **CSS Module Turbopack: kebab-case → `undefined` silencioso; usar camelCase** [[css-module-camelcase-turbopack]]
- **2× `<Document>` react-pdf con misma URL no-cache → `onLoadError`; cache-buster por instancia** [[dos-react-pdf-document-misma-url-nocache-onloaderror]]
- **Color runtime sin inline style: `data-estado={val}` + CSS `[data-estado="X"]`** — esquiva trinquetes + mantiene dinamismo. Ver [[inline-style-data-attribute-para-color-semaforo]]
- **Layout server App Router NO ve el pathname → guard por página con helper, no en layout** [[nextjs-layout-no-lee-pathname-server-side]]
- **Header sticky con glass translúcido sangra el mesh por las esquinas → opaco** [[header-sticky-glass-sangra-mesh-debe-ser-opaco]]
- **Proxy de impersonación reimplementa la API de Supabase y se queda corto (falta `.not()`/`count`/`maybeSingle`) → lista única + test de paridad; memoizar el cliente o bucle de re-fetch** [[proxy-impersonacion-reimplementa-api-supabase-se-desincroniza]]
- **RPC con overloads/DEFAULT → pasar TODOS los named params (los nuevos como `null`)** — supabase-js no resuelve por subconjunto; síntoma "Could not find function …". Imita al endpoint hermano que ya la llama. [[postgrest-pgrst203-rpc-overloads-pasar-todos-los-params]]
- **PostgREST embed: clonar `.select()` entre tablas gemelas rompe si difieren columnas** — `proveedores` no tiene `empresa` (sí `clientes`) → 500 runtime, invisible en typecheck/mocks. Grepea columnas reales antes de copiar. [[proveedores-no-tiene-columna-empresa-asimetria-clientes]]
- **Audit trigger no ve service-role** — trigger por `auth.uid()` se salta copiloto/crons/jobs; auditar explícito desde el código con la entidad EXACTA que lee la UI. Ver [[trigger-audit-solo-registra-sesion-humana]]

## dependencias / npm / LLM

- **Modelo Anthropic retirado tras bump SDK** — validar model-ids con `GET /v1/models` (POST messages no sirve sin saldo: billing error precede a model-not-found). Ver [[verificar-modelos-anthropic-vigentes-via-get-v1-models]]
- **`npm audit fix --force` downgradea majors** — leer "Will install"; para vulns transitivas usar `overrides` en package.json, no --force a ciegas. Ver [[npm-audit-fix-force-propone-downgrades-trampa]]
