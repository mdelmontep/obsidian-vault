---
title: gh issue create rompe el título en silencio con backticks, y los números no se predicen
date: 2026-08-14
source: claude-code-session agh-iberica
tags: [gh-cli, zsh, github, gotcha]
---
Dos formas de estropear una referencia de GitHub desde el CLI, las dos medidas el mismo día.

**1. Backticks en `--title`.** zsh los trata como **sustitución de comando**:

```sh
gh issue create --title "el campo `base` de la línea…"
#  → command not found: base
#  → issue creado con el título «el campo  de la línea…»
```

Lo que lo hace caro: el `--body-file` con heredoc **entrecomillado** (`<<'EOF'`) no sufre nada, así que
el cuerpo queda perfecto y **el fallo pasa desapercibido**. Solo se ve leyendo el título después.
👉 Comillas simples en el título, o sin backticks (`el campo "base"`). Y tras crear un issue o PR desde
el CLI, **leer el título que quedó**, no el que enviaste.

**2. Predecir números.** Escribí «→ #1177 / #1178 / #1179» en el cuerpo de una PR para tres issues que
iba a abrir *después*: la PR salió con el número **1177** y las tres referencias quedaron mal, una
apuntando a sí misma. 👉 **Abrir primero, referenciar después.** Y si hay que reescribir el cuerpo de
una PR para arreglarlo, **comprobar que la línea de cierre sobrevivió** — un `Closes` se va con la
cabecera y el issue queda abierto tras el merge.

Ver [[keywords-de-cierre-de-github-solo-funcionan-en-ingles]]
