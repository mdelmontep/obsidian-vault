---
title: parser ES naïve rompe valores de `<input type=number>` (siempre punto US)
date: 2026-05-24
source: claude-code-session
tags: [react, forms, i18n, numbers, fiscal]
---

Parser ES típico (`s.replace(/\./g, '').replace(',', '.')`) elimina el `.` asumiendo millares. **HTML5 `<input type=number>` siempre devuelve formato US con `.` como decimal**, así que `'33.33'` se convierte en `'3333'` (×100 silencioso). Bug fiscal: base imponible y subtotales explotan sin que el linter ni el ojo lo cojan — solo lo pilla un test con literal.

**Fix**: heurística por separador:
- Si el string contiene `,` → formato ES (puntos son millares, coma es decimal).
- Si NO contiene `,` → formato US/JS, mantener puntos como decimales.

Aplica a cualquier React form ES con `type=number` que use parser propio. NO usar parsers ES "genéricos" sin validar el origen del input. Si el control es de teclado libre con coma admitida, ambos formatos deben funcionar.

Caso real TuFacturaIA `src/lib/documents/precio-helpers.ts` 2026-05-24: tests vitest detectaron el bug (`expected 45 to be 44995.5`) tras refactor a state string. Fix añadió ramificación + test específico `'1.234,56' → 1234.56` y `'1234.56' → 1234.56`.