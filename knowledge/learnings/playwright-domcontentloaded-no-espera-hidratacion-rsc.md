---
title: Playwright domcontentloaded no espera hidratación RSC + attached vs isVisible
date: 2026-05-18
source: claude-code-session
tags: [playwright, e2e, react, nextjs, gotcha]
---

`page.goto(url, { waitUntil: 'domcontentloaded' })` retorna antes de que React Server Components hidraten los client components. Selectores con `useState` aún no están. Fix: `waitUntil: 'load'` o `waitFor` explícito.

`isVisible()` puede devolver false aunque `count() > 0` — CSS `display: none` en breakpoints responsive, `aria-hidden`, fuera de viewport. Para preconditions usar:

```ts
await locator.waitFor({ state: 'attached', timeout: 10_000 })
```

`attached` para presencia DOM. Reservar `isVisible` para verificación real de UX.
