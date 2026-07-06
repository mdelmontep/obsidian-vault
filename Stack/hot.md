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

- **Stripe: el CLI puede ir a OTRA cuenta que la sk_live de la app** — IDs con sufijo de cuenta (`…GgQMT2aOqB` vs `…QY4tV8FMxQ`); `retrieve --live` da "No such price" falso si es la del CLI. Verifica con `curl -u $SK` de la app. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]]
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

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas, docker-infra) y transversales en [[index]]. Lo retirado de aquí sigue en `knowledge/learnings/` (recall por relevancia), no se ha borrado ningún learning.
