---
title: un hook que resuelve git en el cwd de la sesión juzga el repo equivocado, y en las dos direcciones
date: 2026-08-20
source: facturaia
tags: [claude-code, hooks, git, worktrees, arnes]
---
Un `PreToolUse` corre con el cwd de la SESIÓN, pero el comando real casi siempre empieza por `cd ~/wt-X &&` o lleva `git -C`. Si el guard mide `git branch` / `git status` a secas, mide otro checkout.

Falla en las dos direcciones y las dos se midieron: dejó pasar `cd <raíz compartido> && git commit` (el commit a `main` que venía a impedir) y bloqueó crear un repo de prueba en `/var/folders` (falso positivo).

- **Renunciar no es neutral.** El parche fácil —`exit 0` en cuanto se ve un `cd` o un `-C`— convierte el guard en decorativo justo en el caso que importa. Hay que RESOLVER el directorio y juzgarlo con `git -C`.
- El `cd` puede ir en **cualquier** segmento: en `T=$(mktemp -d) && cd $T && git commit` va en el tercero. Coge el ÚLTIMO `cd` antes del segmento del verbo, no el primero.
- Quita sangría y `(`/`{` antes de matchear: `(cd X && git commit)` y una línea indentada eran las dos formas de perder el `cd` de vista.
- Canoniza con `pwd -P`: en macOS `/var` y `/tmp` son symlinks de `/private/…`.
- Si el directorio no existe o no es repo, deja pasar: es el `mkdir X && cd X && git init` legítimo.

Y el orden que lo destapó: los casos que DEBEN bloquear, escritos primero y vistos en ROJO contra el hook sin arreglar (70/8 → 78/0). Dos casos "no debe bloquear" salieron verdes sin tocar nada: no medían.
Relacionado: [[un-gate-derivado-del-repo-necesita-guarda-contra-su-propia-ceguera]] · [[facturaia]]
