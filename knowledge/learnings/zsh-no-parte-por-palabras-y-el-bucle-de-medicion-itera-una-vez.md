---
title: zsh no parte por palabras — un `for` sobre una variable multilínea itera UNA vez, en verde
date: 2026-08-31
source: claude-code-session
tags: [zsh, shell, gates, verificacion, metodo]
---
En bash, `for f in $lista` parte la variable por espacios y saltos. **En zsh no**: sin comillas
sigue siendo UN solo valor, así que el bucle itera una vez con todas las rutas pegadas. El daño no
es un error: es que lo de dentro se ejecuta sobre una cadena que no existe y **no casa nada**.

Caso real (31-ago, triando 12 ramas de agentesia-crm): `for f in $ficheros; do git diff --quiet
"$b" origin/main -- "$f"; done` dio «0 de 1 ficheros difieren» en las doce, y la conclusión habría
sido «todo esto ya está en main, se puede borrar». La rama medía 5 ficheros, no 1.

Lo que lo delató NO fue leer el bucle: fue que **el mismo `1` saliera en las doce**. Un contador
que no varía entre casos distintos no es un resultado. Remedido con `while IFS= read -r f`,
salieron 10 de 12 con contenido pendiente — la conclusión contraria.

- Fix: `while IFS= read -r f; do … done < <(comando)`, nunca `for x in $var`.
- El shell del agente es **zsh** (`echo $0`), no bash: lo aprendido en bash no se hereda.
- Corolario del método: en una medición ad-hoc, imprimir SIEMPRE el denominador (`n de N`) y
  sospechar del N constante. Es la versión de andar por casa de
  [[un-gate-derivado-del-repo-necesita-guarda-contra-su-propia-ceguera]].
