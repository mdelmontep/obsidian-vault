---
title: hot cache
date: 2026-07-13
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo activo ahora (1 línea + link). El resto vive en `knowledge/learnings/`
(recall por relevancia) y transversales en [[index]] §Transversales / [[patterns-cross-proyecto]].
Podado 2026-07-13 (~40→15; lo retirado sigue íntegro en sus learnings, solo sale del índice rápido).

## UI / listados (reutilizable)
- **Server Component NO puede llamar función de módulo `'use client'`** (Next 16): revienta en runtime y el `build` NO lo caza → smoke de navegación real obligatorio. Ver [[server-component-no-puede-llamar-funcion-use-client]].
- **`agent-browser screenshot` cuelga en apps con polling** (nunca network-idle) → Playwright con `waitUntil: 'domcontentloaded'`. Ver [[agent-browser-screenshot-cuelga-apps-con-polling]].
- **Migrar en masa a un primitivo sin cambiar píxeles**: alinea su geometría al legacy primero (mide computed styles; ojo `line-height`), className-merge desbloquea los omitidos, enforcement con trinquete + error solo en carpeta limpia. Ver [[migracion-invisible-de-primitivo-alinear-geometria-al-legacy]].
- **Scroll-fade dinámico** en riel que no cabe (`.scroll-fade-x`+`useScrollFade`): difumina solo el borde con contenido oculto. Gotchas: sin `transition` sobre `@property` (se clava en 0px), la máscara recorta `box-shadow` externo, callback ref para portales. Ver [[scroll-fade-dinamico-mascara-gotchas]].
- **Buscador de listado = lupa expandible**, no fila propia ni inline fijo (estruja/hueco). Ver [[buscador-listado-lupa-expandible-no-fila-propia]].
- **Column-picker: ocultar por CSS (display:none), no desmontar** th/td → preserva colSpan/sort/bulk. Ver [[ocultar-columnas-tabla-por-css-no-desmontar]].
- **Refactor UI grande con agentes**: particiona por archivo disjunto (no por feature) + antes/después vía `git stash`. Ver [[refactor-ui-grande-agentes-paralelos-particionados-por-archivo]].
- **Submodal dentro de un drawer/contenedor que coordina Escape/focus a mano → NO migrar a `<Modal>` sin más** (doble cierre). Ver [[migrar-submodal-a-modal-choca-con-escape-del-contenedor]].
- **Auditar "0 consumidores" de una clase CSS antes de borrarla: grep `\bclase\b` sin anclar, no solo `className="clase"`** — template literals/ternarios se escapan del regex plano y subestiman el alcance real (~30 ficheros de más en una sesión real). Ver [[grep-classname-plano-subestima-template-literals]].

## Agente AGH (capacidad conversacional)
- **Recall/RAG sin umbral = confidently-wrong** — k=1 sin piso de distancia miente; devolver distancia+umbral+top-k+atribución+golden negativo. Ver [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]].
- **Presenter grounded: conserva los ítems verbatim, no aflojes el verificador** — el guard estricto es demasiado en ítems compuestos; arregla el prompt del presenter, no el verificador. Ver [[presenter-grounded-conservar-items-verbatim-no-aflojar-verificador]].
- **Evals de modelo real: agregar corridas + baseline con margen** — un fichero de 3 casos oscila 100%↔33%; gate = N corridas + baseline − margen − tolerancia. Es la red para tocar el prompt. Ver [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]].
- **Correr evals opt-in: `vitest --repeat` no es CLI + timeout 5s da falsos timeouts** — bucle bash o runner; `--testTimeout=25000`; el full ×1 amplifica la varianza del baseline (×3 es el comparable). Ver [[evals-opt-in-vitest-repeat-timeout]].
- **Fix validado solo in-memory oculta bug pg-solo-prod** — campo nuevo en estado persistido: grep el store Postgres + test pg round-trip antes de "hecho". Ver [[fix-validado-solo-in-memory-oculta-bug-pg-solo-prod]].

## Auditoría / agentes / rutinas cloud
- **Auditar/fixear con red** — worktree desde origin/main + dedup vs issues abiertos ANTES de filar; re-audita tus fixes con agentes independientes antes de mergear. Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] · [[maker-checker-re-auditar-fixes-propios-antes-de-merge]].
- **Bot de auditoría recurrente: idempotencia por estado de issues** — dedup contra abiertos Y cerrados; cerrar = corregido (suprime salvo regresión) / `wontfix` (supresión permanente). La fuente de datos no sabe qué está arreglado. Ver [[audit-bot-recurrente-idempotencia-por-estado-de-issues]].
- **`audit_log` con 2º escritor (agente): procedencia en el `after` jsonb (sin columna), before sin carrera (FOR UPDATE / DELETE RETURNING), audit en la misma tx, deps opcionales** — atomicidad se prueba con pg-real (fake in-memory no lo demuestra). Ver [[audit-log-multi-escritor-procedencia-en-after-before-sin-carrera]].
- **Delegar implementación con deps opcionales → revisar el camino de composición, no solo la hoja** — gate verde ≠ cableado; el código muerto no rompe tests. Ver [[subagente-feature-sin-cablear-composicion]].
- **Capacidad en 2 capas (tool que anuncia + gate de endpoint que autoriza) → paridad como test de invariante** — desajuste = tool muerta (403) que el inventario aislado da por sana; cruzar tool↔endpoint. Ver [[capacidad-en-dos-capas-tool-mas-gate-endpoint-verificar-paridad-o-queda-muerta]].
- **Hook-guard de comandos: matchea sobre el comando SIN comillas (scrub `"…"`/`'…'`), no substring cruda** — si no, un `gh pr create --body`/`git commit -m` que menciona la frase da falso positivo. Ver [[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]].
- **Rutinas cloud (RemoteTrigger/CCR): egress allowlist + identidad bot** — 403 en CONNECT a host privado → Network access Custom + Allowed domains (aplica a sesiones NUEVAS); postea por webhook, no por conector personal (suplanta). Ver `Stack/claude-code-harness.md` §Rutinas cloud.
- **Agentes background muertos por session limit → SendMessage al mismo agentId** — inventariar working tree primero; nunca dos sobre los mismos archivos. Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]].
- **Burndown grande con subagentes**: máx 2-3 concurrentes (5 tumban la sesión), agentes NUNCA tocan estado compartido (`build`/`.next`, `git stash/checkout`, `eslint.config`), y el orquestador es el checker real (tsc completo + tests + grep red flags; su auto-verify falla). Commit por zona. Ver [[orquestar-subagentes-paralelos-burndown-grande-limites-y-checker]].
- **Rules de proyecto (`.claude/rules`) no se comparten si `.claude` está gitignored** — mover un inviolable de `CLAUDE.md` ahí deja un puntero colgando (rule perdida en clones/CI). `git check-ignore` antes; y solo mover reglas file-scoped, nunca transversales (un `paths:` que no casa no aparece, silencioso). Ver [[claude-code-project-rules-no-se-comparten-si-claude-gitignored]].
- **Prompt caching Anthropic: cachear solo system+tools deja el HISTORIAL sin cachear** — en runner multi-turno/agéntico añade 3er breakpoint MÓVIL en el último mensaje (máx 4/request); `input_tokens` ya excluye lo cacheado, loguea `cache_read`. Ver [[anthropic-prompt-cache-prefijo-system-tools]].

## Git / worktrees / merge (multi-sesión)
- **Working tree en rama STALE → verifica antes de reimplementar** — lee de `git show origin/main:<path>` + `git merge-base --is-ancestor` antes de construir. Ver [[working-tree-en-rama-stale-verifica-antes-de-reimplementar]].
- **Stash/WIP viejo puede estar ya en main** — con ramas en paralelo se vuelve obsoleto; `git log origin/main -S "<firma>"` antes de reconciliar, y `git apply --3way` con 0 diff = ya aplicado. Ver [[stash-o-wip-viejo-puede-estar-ya-en-main-verificar-antes-de-reconciliar]].
- **`git worktree add` sin `cd` inmediato → Bash cae en el checkout principal** — verifica `pwd`+`git branch --show-current` justo después. Ver [[worktree-add-sin-cd-bash-cae-en-checkout-principal]].
- **Worktree monorepo → symlinkar TAMBIÉN el node_modules anidado** (`dashboard/node_modules`), no solo el raíz; si no, tests del subpaquete fallan (`react/jsx-dev-runtime`) y parece regresión tuya. Ver [[worktree-monorepo-symlink-node-modules-anidado]].
- **`gh pr merge` miente en stdout** — verifica `gh pr view <n> --json state` == MERGED. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]].
- **PR stackeada + squash → `rebase --onto <base-vieja>`, no rebase normal** — el squash mete la base con SHA nuevo; un rebase normal la duplica. Luego retarget a main + verificar `baseRefName`. Ver [[rebase-onto-pr-stackeada-squash-no-duplicar]].
- **Conflicto de rebase en JSON generado (baseline/lockfile) → `checkout --ours` + regenerar con el script, nunca a mano.** Ver [[conflicto-rebase-json-generado-regenerar-no-mergear-a-mano]].
- **PR apilado: NO borres la base antes de reapuntar el dependiente** — `gh pr merge PR0 --delete-branch` AUTO-CIERRA el PR dependiente (no reapunta) y ya no se puede reabrir → recrear. Reapunta (`gh pr edit N --base main`) o mergea sin `--delete-branch`; merge commits, no squash, en stacks. Ver [[gh-pr-merge-delete-branch-cierra-pr-apilado-dependiente]].
- **Actions caído (billing) → hooks locales = único gate** — `npm run lint` global antes de cada merge; node_modules real para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]].
- **`gh pr merge --delete-branch` puede fallar en local (worktree con `main` en otro path) aunque el merge en GitHub YA se hizo** — verificar `state=MERGED` antes de asumir fallo; borrar rama remota/worktree aparte. Ver [[gh-pr-merge-delete-branch-falla-local-si-main-en-otro-worktree]].
- **Un aviso advisory añadido a una función compartida (find-or-create) debe ser opt-in + try/catch** — si la función la llama también una ruta crítica (emisión de factura), un lookup "solo informativo" sin proteger la rompe; lo atrapa el test suite, no lint/typecheck/build. Ver [[advisory-lookup-en-funcion-compartida-debe-ser-opt-in]].
- **Limpiar root checkout viejo con worktrees → stash selectivo + ff-only** — nada de reset (git-guard lo bloquea); caracteriza los cambios (monolito pre-refactor = obsoleto); `stash push -- <paths>` (recuperable) + `merge --ff-only`. Ver [[limpiar-root-checkout-viejo-con-worktrees-stash-selectivo-ff-only]].
- **Semáforo de CPU entre sesiones (build/typecheck/lint)** — throttle automático por hook + admisión adaptativa por carga (MIN/MAX/loadavg) + badge SwiftBar; automatiza el "espera a la ventana libre". Ver [[fia-gate]].
- **UI flotante desde script macOS → swiftDialog, no osascript** — un NSPanel/WKWebView por osascript da `visible=true` pero no pinta. Ver [[ui-flotante-desde-script-macos-swiftdialog-no-osascript-panel]]. Y gotchas BSD sed/`while read` → [[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]].

## Infra / Dokploy / Supabase / Stripe (FacturaIA)
- **NUNCA `compose.one`/`application.one`/`schedule.one` de Dokploy en crudo** — vuelcan el `env` con secrets en plano (fuga real 07-03); hook global BLOQUEA, usa `~/.claude/bin/dokploy-safe.sh`. Ver [[dokploy-api-get-schedule-list-expone-env-completo-secrets]].
- **Schedule Dokploy compose exige `serviceName`** — sin él runManually→500 y el cron no dispara (invisible); verifica el 1er run a mano. Ver [[dokploy-compose-schedule-requiere-servicename]].
- **Supabase egress restringido tumba la app vía healthcheck → Traefik 404** (Docker "healthy" engaña; `curl -I` da 404). Restaurar plan; egress es mensual. Ver [[supabase-egress-restringido-tumba-app-via-healthcheck-traefik-404]].
- **Stripe: el CLI puede ir a OTRA cuenta que la sk_live de la app** — "No such price" falso; verifica con `curl -u $SK` de la app. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]].
- **Holded v2: el rol de un contacto es `client_record`/`supplier_record`, no `type`** — un contacto puede ser cliente Y proveedor; decidir por `type` mete proveedores en clientes. Ver [[holded-v2-contacto-rol-por-record-no-por-type]].
- **Lista de columnas reusada entre tablas parecidas → 42703 si una no tiene la col** (`proveedores` sin `updated_at`/`telefono_e164`); un helper que traga `error` lo degrada a null silencioso → comportamiento erróneo. Lee `error`, haz throw; reproduce por supabase-js no psql. Ver [[column-list-drift-clientes-proveedores-select-inexistente-42703]].
- **Castear `.data` de una query oculta el 42703 que el tipo YA detecta** (`(data ?? []) as X[]`, `.maybeSingle<T>()`, select concatenado). Erradicado 100% en TuFacturaIA (9 PRs, ~450 casts, guardarráil ESLint global `src/**`): `?? []` = lista de query (marcar) vs `?? {}` = jsonb (no). CAVEAT: si el cliente no lleva `<Database>` (`useOrgClient()`) quitar el cast NO da protección real. Ver [[casts-sobre-data-de-query-supabase-ocultan-42703-que-el-tipo-ya-detecta]].
- **RPC con `RETURNS TABLE` explícito devuelve subconjunto tras un add-column** — el cast al Row completo miente, los campos nuevos llegan null y corrompen al editar (precio ×1000, caso obras). Redefine el RPC (DROP+CREATE) o usa `SETOF <tabla>`; alto riesgo con migraciones en paralelo. Ver [[rpc-returns-table-subconjunto-tras-add-column-cast-miente]].
- **Comparar fecha `'YYYY-MM-DD'` vs `timestamptz` ISO como strings falla** — el prefijo de 10 chars es "menor" que el string con hora → un rango pierde el primer día; `split('-')` sobre timestamp da basura. Normaliza con `.slice(0,10)` (o `::date`); verifica el tipo real de la columna. Ver [[comparar-fecha-date-string-vs-timestamp-iso-como-string-falla]].
- **Dokploy: `compose.deploy` del MISMO commit = no-op** (no recrea contenedor); `deployments[]=done` no garantiza swap. Verifica por `docker ps` (antigüedad) + `docker exec grep <string-literal>` en `.next/server`; cambia el SHA para forzar. Ver [[dokploy-redeploy-mismo-commit-es-no-op-cambiar-sha-fuerza-recreacion]].
- **`NEXT_PUBLIC_*` nueva en el panel de envs no llega al cliente sin build-arg explícito** — Dockerfile necesita `ARG`+`ENV` en el stage builder ANTES de `npm run build`, y docker-compose `build: args:`; ningún redeploy (ni sin caché) lo arregla sin ese cableado. Ver [[next-public-env-necesita-build-arg-explicito-en-docker]].

## CI / gates
- **`npm run typecheck | tail` enmascara el exit de tsc** — el pipeline devuelve el exit de `tail`(=0); un gate "verde" puede tener errores TS reales. Captura el exit real (`> f 2>&1; echo $?`) o `grep "error TS"`. Ver [[typecheck-pipe-tail-enmascara-exit]].
- **Literal BigInt (`300000n`) pasa vitest pero rompe tsc <ES2020 (TS2737)** — usa `BigInt(300000)` en tests fiscales. Ver [[bigint-literal-tsc-target-es2020]].

## Import / datos externos
- **CSV de tarifa de ERP español (Telematel/GO!Catalog) = cp1252 + `;` + precio por lote** — decodifica latin1 (o salen `�`) y divide `P.V.P./UNIDADES` (cable 2517 con UNIDADES=1000 = 2,517 €/m, no ×1000). Captura fichero real antes de codificar. Ver [[importar-csv-erp-espanol-encoding-cp1252-y-precio-por-unidad-multiple]].
- **Vídeo sin audio: léelo por fotogramas** — `ffmpeg -vf fps=1/5` + Read de los .jpg; no hay transcripción de voz, pero lo que se ve en pantalla sí. Ver [[transcribir-video-sin-audio-extraer-fotogramas-ffmpeg]].

## Frontend / UX / QA
- **Borde con luz que orbita + halo glass que crece**: anillo `conic-gradient(from var(--a))` recortado con máscara + `@property --a` para girar (transform no vale); acelerar en hover SIN salto con WAAPI `updatePlaybackRate` (no `animation-duration`). Ver [[css-border-beam-conic-property-playbackrate]].
- **Subida en lote vs rate-limit per-user: sin backoff el excedente se pierde** — Retry-After exacto (PTTL) + `code:rate_limited` en el 429 + `fetchWithTransientRetry` (backoff sobre 429-por-minuto/5xx/red, no sobre topes de plan) + panel de reintento. La cola de fondo NO cubre la ráfaga de subida HTTP. Ver [[subida-en-lote-cliente-backoff-sobre-rate-limit-servidor]].
- **Acción masiva en cliente con N round-trips en serie cuelga la UI** — batch read (`.in(ids)`) + un `UPDATE .in(ids)` si todas iguales, o pool acotado (~6) + contador `N/total` y relleno del botón. Ver [[accion-masiva-cliente-n-round-trips-serie-cuelga-usar-batch-y-pool]].
- **Clave de selección de fila = id único, no campo de negocio** — `num??id` colapsa duplicados (nº recibidas repite) → acciones en lote saltan filas en silencio. Ver [[clave-seleccion-fila-debe-ser-id-unico-no-campo-de-negocio]].
- **OpenAI vision lee un PDF del revés si rotas páginas con pdf-lib** — honra el `/Rotate`; auto-orientar reintentando en fallos [180,90,270]. Ver [[openai-vision-lee-pdf-del-reves-rotando-con-pdf-lib]].
- **Dep nativa (sharp) en ruta API → import dinámico en try/catch** — el import estático tumba TODA la ruta si el `.node` no carga en Alpine; + `serverExternalPackages`. Ver [[dep-nativa-import-dinamico-defensivo-en-ruta-api]].
- **agent-browser `eval` reutiliza contexto → `const` redeclarado peta** — envuelve en IIFE o usa `wait --fn` para esperar sin polling manual (evita cronometrajes falsos). Ver [[agent-browser-eval-contexto-persiste-const-usar-iife]].
- **Grid `1fr` no encoge bajo su contenido `nowrap` → desborda** — usar `minmax(0, 1fr)` + `min-width:0` en la cadena flex-column; el badge/importe se salía de pantalla pese al ellipsis. Lo caza el QA visual, no el build. Ver [[grid-1fr-no-encoge-con-contenido-nowrap-usar-minmax-0-1fr]].
- **`backdrop-filter` invisible en Turbopack: no declares `-webkit-` a mano** — lightningcss colapsa el par y sirve solo la variante `-webkit-`, dropando la sin prefijo → Chrome no aplica el glass. Solo `backdrop-filter`; el pipeline prefija. Ver [[turbopack-lightningcss-dropea-backdrop-filter-sin-prefijo]].
- **agent-browser `set device` DESPUÉS de `open` no sirve si la app decide móvil por UA server-side** — el primer render ya quedó fijado a desktop aunque el viewport cambie después; setea dispositivo/media ANTES de navegar. Ver [[agent-browser-set-device-antes-de-open-para-ssr-mobile]].
- **Contención de CPU multi-sesión puede parecer bug de UI (skeleton atascado)** — antes de diagnosticar, `uptime`/`ps aux` + esperar 30-60s reales; un "atasco" de segundos bajo load>10 puede no ser código. Ver [[cpu-contencion-multisesion-falso-positivo-ui-atascada]].
- **"Reinvención→primitivo" no es siempre migración: verifica comportamiento antes** — el nombre engaña (feedback-modal=panel flotante, .card-grid=layout grid); lee el componente entero y o extiendes el primitivo a superset o lo dejas bespoke. Ver [[verificar-primitivo-cubre-comportamiento-antes-de-consolidar-reinvencion]].
- **pre-push que buildea muere por OOM bajo sesiones paralelas** — `ps aux | grep "next build"`; espera ventana libre y pushea; nunca `--no-verify` el build. Ver [[pre-push-build-oom-bajo-sesiones-paralelas]].
- **SSRF-safe por IP pineada: verifica en el código fuente cómo la librería relaciona `host`/`servername`/flags TLS** — imapflow rompe SNI sin `servername` explícito y hace downgrade silencioso sin `doSTARTTLS` explícito. Ver [[imapflow-pinning-ip-servername-dostarttls-explicito]].
- **`react-hooks/static-components` bloquea `<MAP[key] />` aunque el mapa sea estático** — envolver el lookup en un único componente estable (`BrandIcon({slug})` con el lookup dentro), no exponer una función que devuelve componente. Ver [[react-hooks-static-components-lookup-dinamico]].
- **VeriFactu: huella=8 campos (cierra en FechaHoraHusoGenRegistro, hex MAYÚSCULAS, timestamp único), WS con mTLS, respuesta sin CodigoRespuesta** — valida la huella contra el ejemplo firmado oficial. Ver [[verifactu-huella-8-campos-mtls-parser-respuesta]].
- **TuFacturaIA tiene 4 dialectos de input CSS (`.field`/`.ob-input`/`.set-input`/`ui/input.tsx`)** — `.field` a pelo fuera de `.auth-card` hereda estilo de card de detalle, no de formulario; en modales nuevos usa `ui/input.tsx`. Ver [[facturaia-multiples-dialectos-input-field-generico-rompe-fuera-de-contexto]].
- **Centrar número+sufijo dentro de un input como unidad**: nunca `width:100%` (centra el dígito en toda la caja, el sufijo queda pegado y con 2-3 cifras se solapa); base `width:<N>ch` fija + `@supports(field-sizing:content)` para ancho exacto. Safari aún sin field-sizing → el fallback en `ch` es obligatorio. Ver [[centrar-numero-mas-sufijo-en-input-field-sizing-fallback-ch]].

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas/harness, docker-infra) y transversales en [[index]]. Lo retirado sigue en `knowledge/learnings/`, no se ha borrado ningún learning.
