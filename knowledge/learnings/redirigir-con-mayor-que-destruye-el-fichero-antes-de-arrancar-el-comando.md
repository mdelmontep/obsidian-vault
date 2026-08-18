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

**Tercera vez, 18-ago-2026, y la lección ya no es el gotcha.** Volvió a pasar en facturaia
con el MISMO script (`gen:types`): la Management API devolvió 401 y el fichero de tipos
quedó en 151 bytes con el JSON de error dentro, **15.512 líneas borradas**. Esta nota y
[[redirigir-a-un-fichero-escribe-el-error-dentro-del-fichero]] llevaban escritas 11 y 7
días, con el patrón correcto explicado y todo: no sirvieron de nada porque **nadie había
cambiado el script**. Una nota describe; lo que impide es el código.

Lo que faltaba, y ya está: (1) el `package.json` llama a un script que genera a temporal,
valida y mueve; (2) un **test que grepea los scripts de npm buscando `> <fichero
versionado>`**, que es lo único que impide que alguien lo reescriba mañana; (3) un
`--check` de drift, porque sin CI nada avisa de que los tipos van por detrás del esquema.

Y al recuperar: `git restore` puede estar bloqueado por un guard de git que no distingue
basura generada de trabajo sin commitear. `git show HEAD:<ruta> > <ruta>` sí pasa y es
explícito sobre lo que descartas.
