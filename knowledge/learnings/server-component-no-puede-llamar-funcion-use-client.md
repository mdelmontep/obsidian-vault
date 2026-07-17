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

Fix: o marcar la página `'use client'`, o no llamar la función cliente en
servidor (usar clase estática / componente cliente hijo). Caso real: página
placeholder `/obras`. Ver [[agent-browser-screenshot-cuelga-apps-con-polling]].
