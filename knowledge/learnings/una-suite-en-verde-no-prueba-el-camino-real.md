---
title: una suite en verde no prueba que el arnés funcione por el camino real
date: 2026-08-10
source: claude-code-session
tags: [arnes, hooks, testing]
---
Tres casos ya, y siempre igual: el arnés se prueba en el entorno cómodo y falla en el que importa.

- Un hook con 15 casos en verde **que no disparaba nunca**, porque su `git status` corría en el cwd del
  hook y los comandos reales empezaban por `cd ~/wt-X &&`.
- 14 comprobaciones de un gate saliendo con 0 **sin haber mirado nada**, porque su guard de entrada
  comparaba con `file://` + ruta y una ruta con espacios va percent-encoded.
- Un test de aislamiento de git verde en solitario **y rojo desde el `pre-commit`**, porque `git commit`
  exporta `GIT_AUTHOR_*` a sus hooks. Ver [[git-toma-destino-e-identidad-del-entorno-no-del-cwd]].

**Regla**: todo arnés se ejecuta una vez por su camino real (desde el hook, desde el CI, desde una ruta
con espacios, con el entorno que tendrá de verdad) antes de darlo por bueno. Y los casos que DEBEN
bloquear son los que discriminan: los "no debe bloquear" pasan trivialmente cuando el arnés no mide nada.

Corolario para gates nuevos: `pathToFileURL(process.argv[1])` **lanza** si `argv[1]` no existe (`node -e`,
un REPL, un arnés que importe el módulo). Un guard de entrada tiene que evaluar a falso, nunca reventar.
