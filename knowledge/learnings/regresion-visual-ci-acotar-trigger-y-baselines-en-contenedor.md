---
title: regresión visual en ci — build prod (no next dev), acotar trigger, baselines en contenedor
date: 2026-06-17
source: claude-code-session
tags: [ci, playwright, visual-regression, github-actions, nextjs, gotcha]
---

Tres cosas para que un check de regresión visual no sea ruido:

1. **No uses `next dev`.** En página pesada/dev-gated compila on-demand y el primer `goto` agota el timeout en CI (rojo 100%); ni el pre-warm ni `domcontentloaded` lo arreglan del todo (ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]]). Fix determinista: el workflow hace `next build` + `next start` (prod, pre-compilado, sin HMR/lazy-compile) y la página gated en prod se expone con un env **server-only opt-in** (`DESIGN_SYSTEM_PREVIEW=1`, default off en prod real; gate en page + middleware).
2. **Trigger acotado.** `paths: src/**/*.css` dispara con cualquier CSS scoped a otra página → rojos falsos que se mergean con `--admin`. Filtrar a lo que pinta el showcase (globals/tokens + `components/ui/**` + la página + spec/workflow).
3. **Baselines sin CI.** Dependen del antialiasing del runner; si Actions está bloqueado, genéralos/verifícalos en el MISMO contenedor (`docker run mcr.microsoft.com/playwright:<v>-jammy ... --update-snapshots`) → paridad pixel exacta.
