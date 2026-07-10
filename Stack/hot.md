---
title: hot cache
date: 2026-07-05
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo activo ahora (1 línea + link al learning). Los patrones
transversales recurrentes (git/worktrees · método prod · frontend glass · deps) se
movieron a [[index]] §Transversales. Lo demás vive en `knowledge/learnings/` (recall por
relevancia) y los universales en [[patterns-cross-proyecto]]. Podado 2026-07-05 (~60→10,
recorte agresivo — el contenido retirado sigue íntegro en sus learnings, solo desaparece
del índice rápido).

- **Auditar/fixear con red** (AGH, activo) — worktree desde origin/main + dedup vs issues abiertos ANTES de filar; re-audita tus propios fixes con agentes independientes antes de mergear. Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] · [[maker-checker-re-auditar-fixes-propios-antes-de-merge]].
- **Fix validado solo in-memory oculta bug pg-solo-prod** (AGH, activo) — campo nuevo en estado persistido: grep el store Postgres + test pg round-trip + backstop pg antes de "hecho". Ver [[fix-validado-solo-in-memory-oculta-bug-pg-solo-prod]].
- **Recall/RAG sin umbral = confidently-wrong** (AGH capacidad, activo) — k=1 sin piso de distancia miente con seguridad; devolver distancia + umbral + top-k + atribución + golden negativo. Ver [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]].
- **Evals de modelo real: agregar corridas + baseline con margen** (AGH capacidad, activo) — un fichero de 3 casos oscila 100%↔33%; gate = N corridas agregadas + baseline − margen − tolerancia. Es la red para tocar el prompt. Ver [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]].
- **Required check en FAILING bloquea incluso `gh pr merge --admin`/API** — solo pending/no-arrancó se salta con admin; failing real solo lo evita la UI web con permiso de bypass. Ver [[github-required-check-failing-bloquea-incluso-admin-merge]]
- **`unaccent()` en un índice de Postgres → 42P17 (no IMMUTABLE)** — envolver en función SQL propia marcada IMMUTABLE. Ver [[postgres-unaccent-no-immutable-index-necesita-wrapper]]
- **Resolver con match fuzzy: el escape-hatch "colapsa al más reciente" solo vale para duplicados EXACTOS** — con capas parciales/difusas, ambigüedad real debe preguntar, nunca adivinar. Ver [[resolver-ambiguo-escape-hatch-duplicados-exactos-vs-fuzzy]]
- **Gate agéntico que "no aprende" → inanido en el origen, no mal calibrado** — dry-run antes de bajar umbral/backfillear: mide el embudo + motivos bloqueantes con datos reales. FacturaIA OCR: 0 verdes por 86% recibidas sin aprobar, backfill de efecto cero. Ver [[gate-agentico-que-no-dispara-suele-estar-inanido-no-mal-calibrado]]

- **Sync bidireccional: anti-eco por hash canónico de la forma mapeada** — hashea `mapToExternal(x)` en ambos lados (no el raw); si las representaciones no convergen (doc con líneas vs importe agregado), borra la fila de push auto-encolada en el pull. Ver [[sync-bidireccional-anti-eco-hash-canonico]]
- **Stripe: el CLI puede ir a OTRA cuenta que la sk_live de la app** — IDs con sufijo de cuenta (`…GgQMT2aOqB` vs `…QY4tV8FMxQ`); `retrieve --live` da "No such price" falso si es la del CLI. Verifica con `curl -u $SK` de la app. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]]
- **Conector MCP de Stripe: mismo riesgo de cuenta equivocada + desconectar en otra sesión no lo arregla** — reautorizar dentro de la MISMA sesión, eligiendo cuenta ANTES del consentimiento OAuth. Ver [[stripe-mcp-conector-cuenta-equivocada-oauth-no-invalida-entre-sesiones]]
- **Stripe: resolver item de sub por price, no `items.data[0]`** — Stripe no garantiza el orden; `[0]` puede pillar el add-on y pisar su price al cambiar plan. Ver [[stripe-subscription-item-resolver-por-price-no-por-indice]]
- **Stripe Connect "sign up for Connect" al crear cuenta conectada** — no es código; la plataforma tiene el perfil de Connect incompleto (restricted / past_due). Testing local: `stripe listen --forward-connect-to`, `return_url` https. Ver [[stripe-connect-signup-gotcha-crear-cuenta-conectada]]
- **`gh pr merge` miente en el stdout** — verifica `gh pr view <n> --json state` == MERGED, no el texto ("will be automatically merged" contiene "merged"). Ver [[gh-pr-merge-no-confirma-verificar-state-merged]]
- **Split de fichero sin cambiar comportamiento** — extracción verbatim + checker independiente + `_parts/<basename>/` (no `_parts/` plano). Ver [[split-verbatim-checker-parts-por-basename]]
- **WhatsApp interactive → await upsert antes de enviar botones** — el button_reply llega antes que el fire-and-forget; escritura en BD debe ser await+guard antes del send. Ver [[whatsapp-await-upsert-antes-de-botones-interactivos]]
- **Actions caído (billing) → hooks locales = único gate** — un merge con `--no-verify` cuela lint/build roto a main. `npm run lint` global antes de cada merge; node_modules real (`npm ci`) para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]]
- **Turbopack rechaza node_modules symlinkeado en worktree** — `tsc`/`vitest` sí, `next build` no siempre; usar `npm install` real si el build falla raro. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]
- **`git diff main <branch>` engaña si tu main local avanzó** — otra sesión mergea → ves cambios fantasma como del branch; usa `git diff $(git merge-base main <branch>) <branch>` o `git show --stat HEAD` en el worktree. Ver [[git-diff-vs-main-drifteado-usar-merge-base]]
- **Working tree en rama STALE → verifica antes de reimplementar un follow-up** — con N worktrees el checkout principal puede estar en rama vieja; lee de `git show origin/main:<path>` + `git merge-base --is-ancestor <commit> origin/main` antes de construir. Ver [[working-tree-en-rama-stale-verifica-antes-de-reimplementar]]
- **Cron de mantenimiento auto-sanable no debe paginar (email), solo panel** — tunear umbral por-cron es frágil (recurrió); clasifícalo por criticidad → 'housekeeping' emite severidad 'media' sin email. Ver [[cron-mantenimiento-auto-sanable-no-debe-paginar-severidad-por-criticidad]]
- **Cron alta frecuencia: exigir ≥2 fallos consecutivos antes de email** — 1 blip de infra (Cloudflare/Supabase 520/522) tumba 1 run y se recupera solo; paginar por eso es ruido. 1 fallo → ámbar (panel), ≥2 → rojo+email. Ver [[cron-alta-frecuencia-exigir-2-fallos-consecutivos-antes-de-paginar]]
- **Payment link con importe congelado: revalidar el pendiente al conciliar, no confiar en el importe fijado al crearlo** — cobro parcial concurrente por otra vía lo deja obsoleto. Ver [[payment-link-importe-congelado-revalidar-pendiente-al-conciliar]]
- **Import CSV de precios: desambiguar ES/US por presencia de coma, nunca `replace(/\./g,'')` incondicional** — "9.99" formato US se lee como 999 sin error. Ver [[csv-import-precio-decimal-es-us-desambiguar-no-asumir]]
- **Dato dictado por voz (ASR): normalízalo en la frontera del write, no en el canal** — un chokepoint antes de proponer/persistir, idempotente, solo sobre el campo semántico. Ver [[normalizar-dato-dictado-en-la-frontera-del-write-no-en-el-canal]]
- **WhatsApp Cloud API fuera de la ventana 24h → plantilla; el botón-URL solo admite sufijo dinámico → acortador propio** — freeform solo dentro de 24h (fuera: error `131047`); variable no abre/cierra cuerpo (`2388299`). Ver [[whatsapp-cloud-api-fuera-de-ventana-24h-plantilla-y-acortador]]
- **LLM resolviendo «mañana/el martes»: pásale el now en TZ local con día de semana, no ISO UTC** — cerca de medianoche el día UTC ≠ día local → elige mal; test del borde de medianoche. Ver [[llm-fechas-relativas-pasar-now-en-tz-local-con-dia-de-semana]]
- **Full-bleed de un flex-item = `margin` negativo (stretch lo agranda)** — `-Npx` estira al borde sin sacarlo del flujo; compensa `padding` para no mover contenido; ancho en var; z-index del panel > item para pasar "por detrás". Ver [[full-bleed-flex-item-margin-negativo-stretch]]
- **Panel glass flotante necesita fondo detrás para no verse plano** — extender el mesh por detrás + z-index del panel sobre el fondo. Liquid Glass SVG = solo Chrome; usa subset: blur + specular layer + rim + sombra en capas. Ver [[glass-flotante-necesita-fondo-detras-liquid-glass-portable]]
- **Contador de tab/Segmented calculado sobre `data` ya paginado colapsa a 0 al filtrar** — separar conteo (query independiente por categoría) de datos de página. Ver [[contador-por-tab-derivado-de-datos-paginados-colapsa-a-0]]
- **Skeleton debe calcar el layout real (chrome + line-box) o hace snap/"2 cargas"** — un solo skeleton de página reusado en loading.tsx + early-return; nada de empty-state durante la carga; alturas = line-box no glifo; mismo `y` de arranque. Ver [[skeleton-debe-calcar-el-layout-real-para-no-hacer-snap]]
- **transform/filter en un ancestro rompe hijos position:absolute** — pasa a bloque contenedor; una animación de entrada con transform/blur reventó el carril de dígitos del odómetro. Un gesto por superficie. Ver [[transform-o-filter-en-ancestro-rompe-hijos-position-absolute]]
- **Stripe: un Coupon no es tecleable, hace falta un PromotionCode aparte** — `discounts[]` y `allow_promotion_codes` son mutuamente excluyentes; suscripción existente ≠ Checkout Session. Ver [[stripe-coupon-no-es-tecleable-necesita-promotion-code]]
- **`git worktree add` sin `cd` inmediato → Bash cae en el checkout principal** — falsos "lint limpio"/"migración pendiente" si no verificas `pwd`+`git branch --show-current` justo después. Ver [[worktree-add-sin-cd-bash-cae-en-checkout-principal]]
- **Supabase "restricted"/egress tumba la app entera vía healthcheck → Traefik 404** (Docker "healthy" engaña; `curl -I` da 404 `text/plain`). Restaurar plan; egress es mensual. Ver [[supabase-egress-restringido-tumba-app-via-healthcheck-traefik-404]]
- **≥2 botones de acción con un `busy` bool compartido → label de progreso en el botón equivocado** — al pulsar uno, todos cambian de label a la vez; estado POR-acción, no bool. Ver [[estado-busy-por-accion-no-un-bool-compartido]]

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/` (recall por relevancia), no se ha borrado ningún learning.
- **Agentes background muertos por session limit → SendMessage al mismo agentId, no relanzar** (activo) — inventariar working tree primero; reanudar el que más progreso dejó, nunca dos sobre los mismos archivos. Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]].
