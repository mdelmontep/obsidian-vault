---
title: next start sirve build estático sin hmr; verificar modo y puerto del server antes de qa
date: 2026-06-18
source: claude-code-session
tags: [nextjs, qa, playwright]
---
Síntoma: editas CSS/TSX toda la sesión y los pantallazos/QA no reflejan NADA.
Causa: el server en :3000 era `next start` (sirve el build de `.next` del último
`npm run build`, SIN hot-reload). El `next dev` con HMR estaba en OTRO puerto (:3001).
En repos con muchos git worktrees conviven varios servers → fácil mirar el equivocado.
Check antes de QA: `ps -o command -p $(lsof -ti :PORT)` → ¿`next-server` (start) o `next dev`?
Fix: para `next start`, `npm run build` + reiniciar; o apunta el QA al puerto del `next dev`.
Ojo `output: standalone`: `next start` no es el server correcto (usar `node .next/standalone/server.js`).

Variante peor (2026-07-03): correr `npm run build` (o borrar `.next` para forzar
regen de tipos) MIENTRAS un `next start` sigue vivo en ese puerto rompe la sesión
en caliente — el server mantiene referencias a hashes de chunk que el build nuevo
sobrescribe → `GET _next/static/chunks/*.js` 500, la página se queda en skeleton
infinito sin error visible en pantalla (solo en `network requests`/`errors`).
Fix: tras cualquier `npm run build` de verificación (typecheck/lint/pre-push),
matar y **reiniciar** el `next start` antes de dar por bueno un QA visual en ese puerto.
