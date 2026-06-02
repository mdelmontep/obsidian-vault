---
title: ios safari body scroll lock: position fixed + top -scrollY
date: 2026-06-02
source: claude-code-session
tags: [ios, safari, css, mobile, ux]
---

`overflow: hidden` en body NO bloquea scroll en iOS Safari (momentum scroll lo ignora).

Fix probado:
```js
let savedScrollY = 0;
function lockBody() {
  savedScrollY = window.scrollY;
  document.body.style.position = 'fixed';
  document.body.style.top = `-${savedScrollY}px`;
  document.body.style.width = '100%';
}
function unlockBody() {
  document.body.style.position = '';
  document.body.style.top = '';
  document.body.style.width = '';
  window.scrollTo(0, savedScrollY);
}
```

Aplica a: menús móviles, modales, drawers, cualquier overlay full-screen.
El `scrollTo` al cerrar es obligatorio o el usuario salta al top de página.
