---
title: un valor css inválido tira la declaración entera en silencio, y stylelint sí lo caza
date: 2026-08-14
source: claude-code-session
tags: [css, stylelint, gates, fallo-silencioso, tucrmia]
---
`minmax()` **no admite otro `minmax()`** como argumento. `grid-template-columns: repeat(auto-fit,
minmax(minmax(0, 8rem), 1fr))` es sintácticamente inválido, así que el navegador **descarta la
declaración entera** y la rejilla cae a una columna — `gridTemplateColumns` computa un solo valor
en píxeles. Caso real (TuCRMIA, 14-ago): cuatro contadores apilados en cuatro filas de ancho
completo, semanas, sin que nada avisara.

**Nadie de la cadena habitual lo ve**: lint, typecheck y build no leen gramática CSS, y jsdom no
resuelve cascada ni calcula anchos, así que un test unitario tampoco. Es el hermano de
[[un-var-de-css-que-no-existe-no-falla-se-queda-con-lo-heredado]] un escalón más abajo: allí
faltaba la variable, aquí sobra un argumento que la propiedad no acepta.

**Fix**: la regla `declaration-property-value-no-unknown` de stylelint (core desde la 17, usa
`css-tree`) valida el VALOR contra la gramática de su propiedad y lo pone en rojo. Encenderla
sobre `src/**/*.css` costó cero excepciones en 81 hojas — el único rojo era el caso conocido.

Antes de darla por buena, pruébala aislada contra el valor que te ocupa: no todas las reglas de
stylelint miran el valor, la mayoría miran el origen (tokens, colores, breakpoints).
