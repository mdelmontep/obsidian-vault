---
title: agent-browser — `set device` DESPUÉS de `open` no sirve para detección móvil server-side
date: 2026-07-15
source: claude-code-session
tags: [agent-browser, testing, qa, ssr, movil]
---

Si la app decide móvil-vs-desktop en el SERVIDOR a partir del User-Agent (patrón
`initial` server + corrección `matchMedia` en un `useEffect`, ver TuFacturaIA
`use-is-mobile.tsx`), hacer `agent-browser open <url>` y LUEGO `set device "iPhone
14"` no sirve: la navegación ya pidió el HTML con el UA desktop por defecto, el
servidor decidió `isMobile=false`, y aunque el viewport cambie después, el primer
render quedó fijado a desktop.

Síntoma real: viewport 390px + UA iPhone correctos por `eval` (`navigator.userAgent`),
pero el DOM mostraba el sidebar de escritorio en vez del tabbar móvil — parecía un bug
de producto, era orden de comandos.

Fix: `close --all` → `open about:blank` → `set device "iPhone 14"` (+ `set media dark`
si aplica) → **entonces** `open <url>`. El dispositivo debe estar seteado ANTES de la
primera navegación real. Ver [[facturaia]].

**El FLAG `--device` sobre una sesión ya abierta se ignora en silencio** (8-ago): no
avisa, no falla, y `innerWidth` se queda en 1280 — parece que la emulación no existe y
se acaba dando el smoke móvil por imposible. Es `set device` (subcomando), no
`--device` (flag), y con la sesión recién creada. Salida cuando hace falta puntero
grueso de verdad: exportar la sesión con `agent-browser state save auth.json` y conducir
Playwright con `newContext({ ...devices['iPhone 13'], storageState })` — da viewport Y
`pointer: coarse`, que es lo que se necesita para medir tap targets. Ver
[[columna-que-aloja-un-control-necesita-un-ancho-por-tipo-de-puntero]].
