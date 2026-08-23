---
title: `git diff --name-only` cita los paths no-ASCII, y el grep de extensiones deja de encajar
date: 2026-08-23
source: claude-code-session facturaia
tags: [git, hooks, arnes, encoding]
---
`core.quotePath` está **activo por defecto**, así que `git diff --cached --name-only` devuelve
`"src/\303\241.ts"` en vez de `src/á.ts`. Cualquier hook o script que filtre con
`grep -E '\.(ts|tsx|js)$'` **no encaja nunca** con esos ficheros. Medido el 23-ago en `mutate-guard`:
`src/á.ts` + `src/á.test.ts` sin víctima → `exit 0`; con `core.quotePath=false` → `exit 2`. En un repo
español un fichero con acento no es una rareza, así que el guard llevaba meses desapareciendo solo.

Fix: leer con `-z` (NUL-separado, sin citar) y no con `-c core.quotePath=false`, porque **con eso git
sigue citando** los paths que llevan `"` o un salto de línea. Es decir, `quotePath=false` arregla el
acento y deja la misma forma de fallo abierta.

Y arréglalo en **los dos lados** de cualquier comparación: si un lado va con `-z` y el otro no, el
`comm -23` deja de emparejar y rompes el caso legítimo en vez del agujero. Verifícalo con acento, con
CJK, con espacio y con `"` en el nombre.
