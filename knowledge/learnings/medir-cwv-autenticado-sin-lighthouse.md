---
title: medir core web vitals autenticado sin lighthouse (playwright)
date: 2026-06-19
source: claude-code-session
tags: [playwright, performance, testing, cls]
---
Para medir CWV lab en páginas con login, sin instalar lighthouse:
- Playwright con `storageState` (reutiliza el login del harness e2e).
- `context.addInitScript` con PerformanceObserver ANTES del load:
  `largest-contentful-paint`, `layout-shift` (suma `value` si `!hadRecentInput`),
  `event` (proxy de INP), `longtask`. Navigation/paint timing → TTFB/FCP.
- Para localizar QUÉ salta: en `layout-shift` usa `entry.sources` → node + rects
  prev/current → selector y delta exacto en px.
- CLS es VARIABLE entre corridas (depende del timing de datos/red). Para no
  engañarte midiendo en localhost (más rápido → CLS menor), incluye una página
  que NO tocaste como CONTROL: si sigue alta, la mejora en otra es real.
Apuntar a prod (`E2E_BASE_URL`) da el baseline más realista; localhost aísla la app.
Cruza con [[supabase-ssr-cookie-injection-qa-playwright]] (login via storageState).
