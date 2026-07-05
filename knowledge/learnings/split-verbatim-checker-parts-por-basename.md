---
title: partir ficheros grandes sin cambiar comportamiento — verbatim + checker independiente + _parts/<basename>/
date: 2026-07-05
source: claude-code-session
tags: [refactor, arquitectura, subagentes, next]
---
Reorg de ficheros grandes preservando comportamiento, con agentes:
- Extrae SOLO verbatim: tipos, constantes, helpers puros, subcomponentes props-only. NUNCA conviertas closures/handlers/hooks en props (eso es transformación, no reorg); ante la duda, dejar. El tamaño no importa, el comportamiento sí.
- CHECKER independiente (otro agente, no el que hizo el split): `git show origin/main:<f>` vs rama → character-identity + superficie de exports idéntica + no-closure-to-prop + sin ciclos. Si la extracción es verbatim, el comportamiento se preserva por construcción y la calidad del maker deja de ser crítica.
- Namespacing: si varios ficheros de una carpeta se parten, cada uno a `_parts/<basename>/`, NUNCA a un `_parts/` plano compartido (nombres genéricos `types.ts`/`constants.ts` colisionan al mergear). Al bajar de nivel, los imports `../` externos pasan a `../../` → mejor alias `@/`.
- Verificación barata e independiente del checker (hazla tú, orquestador — no te fíes solo de la palabra del agente): `git diff <rama>^..<rama>`, ignora import/export/comentarios, y exige **0 líneas de código eliminadas que no reaparezcan añadidas Y 0 líneas añadidas nuevas** → prueba de reubicación pura (descarta closure→prop, pérdidas y reescrituras). Los "missing" que sean solo prefijo `export` añadido son falsos positivos.
- Gate: UN build agregado de todas las ramas combinadas (disjuntas), no N builds por rama. App Router: `route.ts`/`page.tsx` no se mueven (el path es la URL), solo extraer helpers a hermanos.
Ver [[claude-code-agentes-worktree-failure-modes]] · [[cherry-pick-4-worktrees-agentes-paralelos]].
