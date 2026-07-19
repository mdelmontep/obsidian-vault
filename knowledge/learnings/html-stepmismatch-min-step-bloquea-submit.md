---
title: min/step incompatibles en input number → stepMismatch bloquea el submit sin aviso
date: 2026-07-19
source: claude-code-session
tags: [frontend, html, forms, react]
---
`<input type="number">` con `min` y `step` incompatibles marca `stepMismatch` para valores legítimos: HTML5 exige `value = min + n·step` (n entero). Ej real: `min=0.0001 step=1` → ningún entero cumple; `min=0.25 step=0.5` → valor 2 falla (2 = 0.25 + 3.5·0.5). Consecuencia silenciosa: `form.checkValidity()` = false → `requestSubmit()` no envía nada, no hay error visible, el guardado "no hace nada". Bloqueó guardar materiales y el kill-switch de mantenimiento en FacturaIA ([[facturaia]] #1030/#1034).
- Diagnóstico: `[...form.elements].filter(el => el.willValidate && !el.checkValidity())` para ver el input culpable.
- Fix en origen: si es magnitud continua, `step="any"`; si discreta, alinear `step` divisor de `min` (o `min` múltiplo de `step`). NUNCA quitar la validación a lo bruto.
- Un `<button type=submit>` clicado por JS sintético tampoco envía el form si hay stepMismatch; verifícalo con `checkValidity()`, no con "el click pareció ir".
