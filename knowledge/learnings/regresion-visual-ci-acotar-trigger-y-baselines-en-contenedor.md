---
title: regresión visual en ci — acotar trigger y regenerar baselines en el contenedor de ci
date: 2026-06-17
source: claude-code-session
tags: [ci, playwright, visual-regression, github-actions, gotcha]
---

Dos gotchas que convierten un check de regresión visual en ruido constante:

1. **Trigger demasiado amplio.** Filtrar por `src/**/*.css` dispara el check con CUALQUIER módulo CSS, aunque sea scoped a una página que no renderiza el showcase → rojos falsos que se acaban mergeando con `--admin`, vaciando de sentido el check. Acotar el `paths:` del workflow a lo que REALMENTE pinta la página objetivo (estilos globales/tokens + `components/ui/**` + la propia página + el spec/workflow). Un rojo así sí significa una regresión real.

2. **Regenerar baselines sin CI.** Los baselines pixel-perfect dependen del antialiasing del runner. Si Actions está bloqueado (billing) o el workflow falla, genéralos en local con el **mismo contenedor Docker que usa CI** (`docker run mcr.microsoft.com/playwright:<v>-jammy ... playwright test --update-snapshots`) → paridad exacta. Verifica en el mismo contenedor con un run limpio antes de commitear.

Relacionado: en el dev server de Next (RSC) `waitUntil:'load'` cuelga — ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]].
