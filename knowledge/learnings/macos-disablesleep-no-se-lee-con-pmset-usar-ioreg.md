---
title: macos disablesleep (dormir al cerrar tapa) no se lee con pmset -g; usar ioreg
date: 2026-07-22
source: claude-code-session
tags: [macos, pmset, power, clamshell]
---
`sudo pmset -a disablesleep 0|1` fija el reposo al cerrar la tapa (clamshell sleep), pero `pmset -g` / `-g custom` / `-g live` **NO lo muestran** (ni cuando está a 1). Un toggle que intente leer el estado de `pmset -g` siempre creerá que es 0 → nunca alterna.

Leer el estado REAL: `ioreg -r -c IOPMrootDomain | grep -i SleepDisabled` → `"SleepDisabled" = Yes`/`No`.

Para un botón sin contraseña: regla sudoers NOPASSWD acotada `usuario ALL=(root) NOPASSWD: /usr/bin/pmset -a disablesleep *` en `/etc/sudoers.d/` (chmod 440).

Gotchas al pegar comandos en zsh interactivo: `#` NO es comentario → un `# nota` al final de la línea se pasa como argumentos (rompió un `visudo -cf`); y zsh NO hace word-splitting de variables sin comillas (un `for x in $lista` con lista multi-palabra falla) → usar arrays o `while read`.

Ver [[swiftbar-templateimage-tamano-por-puntos-no-pixeles]].
