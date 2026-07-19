---
title: server component no puede llamar una función exportada desde un módulo 'use client'
date: 2026-07-17
source: claude-code-session
tags: [nextjs, react, server-components]
---
En Next 16 (App Router), si un Server Component invoca una función exportada
desde un módulo marcado `'use client'` (ej. `buttonClassName()` de un
`components/ui/button` cliente), revienta EN RUNTIME:
"Attempted to call X from the server but X is on the client."

Lo insidioso: **el `build` de producción NO lo caza** — pasa lint, typecheck y
build verdes, y solo falla al renderizar la ruta en el navegador. Por eso un
smoke de navegación real (Playwright/agent-browser) es imprescindible; los
gates estáticos no bastan para páginas nuevas.

Fix preferido si la función es PURA (devuelve strings, no usa hooks): sácala a
un módulo SIN `'use client'` (ej. `button-class.ts`) y que el módulo cliente la
re-exporte; los callers server importan del módulo puro (el re-export a través
del `'use client'` la re-marca como client reference → seguiría petando). Así
no tocas los ~N consumidores client. Alternativas: marcar la página `'use
client'` o usar el CSS module directo.

BLIND SPOT (caso real 2026-07-19, `buttonClassName` en 7 páginas gated de
TuFacturaIA): la llamada estaba en las ramas UPSELL/empty/error, que las orgs de
test NUNCA renderizan (tienen todos los módulos → happy path) → las orgs SIN el
módulo (las de conversión) comían 500 semanas sin que nadie lo viera. Smokea las
ramas degradadas (upsell/empty/error/not-found), no solo el happy path.
Ver [[agent-browser-screenshot-cuelga-apps-con-polling]].
