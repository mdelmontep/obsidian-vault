---
title: un var() de css que no existe no falla, se queda con lo heredado
date: 2026-08-03
source: claude-code-session
tags: [css, tokens, design-system, gates, fallo-silencioso]
---

`panel.module.css` pedía `var(--f-ui)`, `var(--f-display)` y `var(--f-mono)` en cinco
sitios. Esos tokens **no existen**: se llaman `--font-ui`, `--font-display`, `--font-mono`.
El panel de administración entero llevaba **desde el primer día** con la tipografía por
defecto del navegador, y nadie lo vio.

CSS no avisa de una variable que no existe: la propiedad queda inválida, se hereda el valor
de arriba, y sigue. **Ni el lint, ni el typecheck, ni el build, ni 936 pruebas podían verlo,
porque ninguno lee CSS.** Es la peor forma del fallo silencioso: el resultado es plausible.

El fix es un gate propio (`tokens-check.mjs`): recorrer los `.css`, sacar cada `var(--x)` y
exigir que alguien lo declare. Dos cosas que no son opcionales:

- **Quitar los comentarios antes de buscar los usos**, o la prosa que explica un fallo pasado
  cuenta como uso (aquí, ocho falsos positivos a la primera).
- **Los huecos de entrada deliberados se declaran con un marcador en la propia hoja**
  (`token-entrada: --x`), no en una lista dentro del script: así aparecen en el diff.

Ver [[css-background-white-hardcoded-rompe-dark-mode-silencioso]] ·
[[llave-css-faltante-invalida-todo-el-css-posterior]]
