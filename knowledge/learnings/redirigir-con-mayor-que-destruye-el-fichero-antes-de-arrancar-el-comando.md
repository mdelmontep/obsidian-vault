---
title: `cmd > fichero` vacía el fichero ANTES de arrancar cmd — un generador que falla borra su propia salida
date: 2026-08-07
source: claude-code-session
tags: [shell, gotcha, tooling]
---
`supabase gen types --linked > database.types.ts` desde un worktree sin enlazar: el CLI **escribe su
error en stdout** y sale con 1, pero la shell ya había truncado el fichero. Resultado: 3.131 líneas de
tipos generados sustituidas por una línea de JSON de error. Nada se queja — el `>` no propaga el código
de salida y `git status` sólo dice «modified». El siguiente `typecheck` culpa al código.

Aplica a cualquier `generador > fuente-de-verdad`: tipos, esquemas OpenAPI, migraciones, lockfiles.

**El arreglo no es un `try`:** el generador corre a memoria y el fichero sólo se toca si la salida pasa
una comprobación de forma. Descarta tres casos, y el tercero es el que ningún exit code distingue:

1. el error en stdout,  2. el vacío,  3. **la salida a medias con código 0**.

Y avisa de lo que DESAPARECE al regenerar: si la fuente nueva no trae algo que sí estaba, el `build` se
rompe en otro sitio y quien regeneró buscará la causa en su propio cambio.
