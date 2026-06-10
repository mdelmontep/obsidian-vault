---
title: clase decorativa compartida en css = 2 trampas de cascada
date: 2026-06-10
source: claude-code-session
tags: [css, cascade, design-system]
---
Al extraer una clase global decorativa que solo aporta `background-image` (ej. `.glass-sheen`,
un glaze sobre `.glass-panel`), dos trampas de igual especificidad donde gana el orden de fuente:

1. **El shorthand `background:` de cualquier regla posterior resetea `background-image` a none.**
   Las superficies que conviven con la clase decorativa deben declarar `background-color:`, nunca el shorthand.
2. **Los guards de fallback (`@supports not`, `@media (prefers-reduced-transparency)`) deben vivir
   al FINAL del archivo.** Al inicio quedan silenciosamente muertos para toda clase declarada después
   (los `@media`/`@supports` no suman especificidad). Bonus: su shorthand `background` anula la
   decoración en modo fallback, que es lo deseado.

Caso real: guards glass de TuFacturaIA (PR #171) nunca aplicaron a 4 superficies legacy; detectado al extraer `.glass-sheen` (PR #175). Verificar en el chunk compilado: byte-offset del guard > byte-offset de la última clase.
