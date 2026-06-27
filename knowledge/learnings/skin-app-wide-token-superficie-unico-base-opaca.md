---
title: skin app-wide = una palanca de superficie (--bg-elev) + base opaca aparte para el glass
date: 2026-06-27
source: claude-code-session
tags: [css, theming, design-system, glassmorphism, facturaia]
---
Para un skin que vuelva translúcida TODA la app sin tocar N componentes: que las
cards usen un único token de superficie (`--bg-elev`) y el skin lo redefina
translúcido vía `[data-skin]`. Con ~92 sitios pintando `var(--bg-elev)`, esmerilan
todos a la vez.

Trampa: la matemática de compositing del glass (`color-mix(... var(--bg-elev) ...)`)
se rompe si la superficie deja de ser opaca → cristal demasiado transparente. Fix:
separar `--elev-solid` (opaco) y rebasar las fórmulas glass a él; `--bg-elev` queda
libre para volverse translúcido. Value-preserving en el tema base (mismo hex).

El blur NO se puede aplicar por token → reglas `[data-skin] .card { backdrop-filter }`
en contenedores grandes + EXCEPCIONES opacas (`--elev-solid`) para chips/iconos/
cabeceras sticky que no deben transparentar. Ojo a divisores tipo
`background:var(--line)+gap:1px`: se cuelan grises bajo la card translúcida.
Ver [[css-scoped-theming-pill-vars]], [[header-sticky-glass-sangra-mesh-debe-ser-opaco]].
