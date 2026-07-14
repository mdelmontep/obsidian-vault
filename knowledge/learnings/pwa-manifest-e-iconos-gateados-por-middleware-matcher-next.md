---
title: el matcher del middleware Next debe excluir manifest.webmanifest e iconos o la PWA no instala
date: 2026-07-15
source: claude-code-session
tags: [nextjs, pwa, middleware, auth]
---
En una app Next con middleware de auth, el navegador pide `/manifest.webmanifest` y los iconos CON credenciales incluso en `/login` → el middleware los redirige a `/login` (302) y la PWA no es instalable ni aparece el icono en standalone.

Síntoma en logs: `GET /login?redirect=%2Fmanifest.webmanifest 200`.

Fix: añade `manifest.webmanifest|icon-|apple-touch-icon|favicon.svg` al negative-lookahead del `matcher` del middleware (mismo trato que `favicon.ico`/`robots.txt`/`sitemap.xml`). El cambio de `matcher` NO hot-reloadea → reiniciar `npm run dev`. Caso real: FacturaIA PR1 vista móvil.
