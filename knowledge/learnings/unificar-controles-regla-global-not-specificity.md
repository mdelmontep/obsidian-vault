---
title: unificar todos los <select>/controles sin tocar cada clase — regla global con :not (0,2,1)
date: 2026-06-18
source: claude-code-session
tags: [css, refactor, design-system]
---

Para imponer un estilo a TODOS los `<select>` cuando conviven N clases distintas
(`form-input`, `set-input`, `adm-select`…) sin editar las N:

```css
select:not([multiple]):not([size]) {  /* especificidad 0,2,1 */
  appearance: none;
  background-image: url("…chevron…");  /* gana al background shorthand de la clase (0,1,0) */
  padding-right: 32px;
}
```

`:not()` suma la especificidad de su argumento → `0,2,1` gana a cualquier clase
`0,1,0` SOLO en las props que tú fijas, y deja borde/fondo/radio a cada clase.
Patrón "dial central": un sitio gobierna el rasgo común sin refactor masivo.
Reaplicable a inputs/botones. Caja base aparte (`select {}`, 0,0,1) para los
huérfanos sin clase. Tema: dos variantes via `:root[data-theme='dark'] select…`.
