---
title: agent-browser (vercel) en formularios react — el click no submite, usar form.requestSubmit()
date: 2026-05-31
source: claude-code-session
tags: [testing, agent-browser, react, smoke]
---

`agent-browser` (CLI de navegación de Vercel, `npm i -g agent-browser` + `agent-browser install`) sobre formularios React controlados:

- **`fill`/value-set por CDP no dispara `onChange` de React** → el estado queda vacío aunque el input muestre el valor → submit no-op. Fix: `keyboard type` (keystrokes reales) **o** setter nativo + evento: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,v); el.dispatchEvent(new Event('input',{bubbles:true}))`.
- **`click` en el botón submit no dispara el `onSubmit`** de React de forma fiable → la página no navega. Fix: `agent-browser eval "document.querySelector('form').requestSubmit()"`.
- **Mac: select-all es `Meta+a`, NO `Control+a`** — `press Control+a` no limpia y `keyboard type` concatena (valor duplicado).
- `find role button click "texto"`: el texto va al final; sin él matchea el primer botón (clicó "Continuar con Google" en vez de "Iniciar sesión"). Más fiable clicar el `@ref` del snapshot.
- Stateful: el navegador persiste entre invocaciones (la sesión/cookies viven ahí, no en el shell). Hook `window.fetch` por `eval` para inspeccionar respuestas (status auth, ids).
