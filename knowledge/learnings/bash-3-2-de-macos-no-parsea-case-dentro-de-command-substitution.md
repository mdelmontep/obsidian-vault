---
title: el /bin/sh de macOS (bash 3.2) no parsea un case dentro de $(...)
date: 2026-08-03
source: claude-code-session
tags: [shell, bash, macos, scripting]
---
Un `case` dentro de una sustitución de comandos revienta al parsear con el `/bin/sh` de macOS (bash 3.2, congelado por licencia GPLv3):

```sh
real=$(printf '%s\n' "$x" | while read -r a b; do
  case "$a" in
    exec_*) continue ;;      # <-- syntax error near unexpected token ';;'
  esac
done)
```

El error (`syntax error near unexpected token ';;'`) apunta a la línea del `;;`, no al `$(` que es la causa: bash 3.2 no equilibra el `)` del patrón del `case` con el de la sustitución. En bash 5 / zsh el mismo script funciona, así que se cuela si solo lo pruebas en tu shell interactivo.

Salidas: reescribir el filtro con `grep -E`/`awk` fuera de la sustitución (lo más limpio), sacar el `case` a una función definida antes, o abrir el patrón con paréntesis `(exec_*)`.

Regla: un script pensado para un LaunchAgent o un hook se valida con `sh -n script.sh` **y** se ejecuta con `sh`, no con zsh — el intérprete real no es el de tu terminal. Ver [[presencia-y-cpu-no-miden-uso-el-healthcheck-falsea-la-senal]]
