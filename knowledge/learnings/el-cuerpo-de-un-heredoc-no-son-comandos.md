---
title: el cuerpo de un heredoc no son comandos, y un troceador que no lo sabe te encola el commit
date: 2026-09-11
source: claude-harness
tags: [bash, hooks, arnes, parsing]
---
Un clasificador de comandos (hook que decide si algo es "pesado") trocea por `&&`, `|`, `(`, `)`
para exigir que lo pesado esté en POSICIÓN de comando. Si no quita antes los heredocs, el cuerpo
entra al troceo como si fueran comandos.

Consecuencia medida: `git commit -F - <<'MSG'` con un asunto de conventional-commit tan corriente
como `chore(vitest):` deja, al partir por paréntesis, un segmento **pelado** `vitest`. El commit
se clasificó como trabajo pesado, se encoló 1h46m detrás del gate de otra sesión y murió por OOM
sin commitear nada. Lo mismo con `python3 - <<PY`.

Arreglo: quitar las LÍNEAS DEL CUERPO antes de trocear, no la que abre el heredoc (esa sí lleva
comando real — si la quitas, `npm run test <<X` deja de detectarse).

El caso que DEBE seguir enrutando es el que fija que no has abierto la puerta: ponlo en la suite.
Mismo género que [[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]] — todo lo que es DATO dentro de la
cadena de un comando acaba leído como comando si no lo quitas primero.
