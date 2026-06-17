---
title: Playwright domcontentloaded no espera hidratación RSC + attached vs isVisible
date: 2026-05-18
source: claude-code-session
tags: [playwright, e2e, react, nextjs, gotcha]
---

`page.goto(url, { waitUntil: 'domcontentloaded' })` retorna antes de que React Server Components hidraten los client components. Selectores con `useState` aún no están. Fix: `waitFor` explícito.

⚠️ Caveat (2026-06-17): NO uses `waitUntil:'load'` como fix en el **dev server de Next** (RSC streaming): el `load` NO se dispara fiable y el `goto` cuelga hasta el timeout (visto en visual regression: `light` pasaba, `dark` expiraba en el mismo run, ruta ya compilada). Robusto: `goto(...,{waitUntil:'domcontentloaded',timeout})` + `waitForLoadState('load',{timeout}).catch(()=>{})` best-effort + `document.fonts.ready`.

`isVisible()` puede devolver false aunque `count() > 0` — CSS `display: none` en breakpoints responsive, `aria-hidden`, fuera de viewport. Para preconditions usar:

```ts
await locator.waitFor({ state: 'attached', timeout: 10_000 })
```

`attached` para presencia DOM. Reservar `isVisible` para verificación real de UX.
