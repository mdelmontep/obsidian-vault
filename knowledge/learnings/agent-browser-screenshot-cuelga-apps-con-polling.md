---
title: agent-browser screenshot se cuelga en apps con polling; usar playwright con domcontentloaded
date: 2026-07-17
source: claude-code-session
tags: [agent-browser, playwright, screenshots, qa]
---
`agent-browser screenshot` (y `wait --load networkidle`) NO terminan nunca en
una SPA que hace polling continuo (notificaciones cada N s, realtime,
websockets): la red nunca queda "idle", así que la captura se queda colgada
hasta el timeout.

`snapshot` sí funciona (no espera idle); solo screenshot/networkidle cuelgan.

Fix fiable: Playwright con `page.goto(url, { waitUntil: 'domcontentloaded' })`
+ un `waitForTimeout` corto, luego `page.screenshot()` — no espera red idle.
Gotchas del script: playwright del repo es CommonJS → `import pw from
'.../node_modules/playwright/index.js'; const { chromium } = pw` (no named
import); y ejecútalo desde dentro del repo o importa por ruta absoluta, o no
resuelve el módulo. Login: rellena el form con las credenciales de `.env.test`
(E2E_EMAIL/E2E_PASSWORD). Ver [[server-component-no-puede-llamar-funcion-use-client]].
