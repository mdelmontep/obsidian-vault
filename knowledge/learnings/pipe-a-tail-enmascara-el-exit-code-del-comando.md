---
title: canalizar la salida a tail enmascara el exit code y da por bueno un fallo
date: 2026-08-02
source: claude-code-session
tags: [shell, gates, ci]
---
`npm install 2>&1 | tail -15` devuelve el exit code de **tail**, no de npm. Un `npm install` que falló por
conflicto de peer deps reportó éxito, `node_modules` quedó vacío y los tests siguieron pasando porque
`npx` descargaba vitest al vuelo. Se descubrió una hora después, al añadir un config que npx no resolvía.

Patrón: capturar el código antes de mirar la salida.
```sh
npm install > /tmp/log 2>&1; code=$?; [ $code -ne 0 ] && tail -15 /tmp/log
```
O `set -o pipefail`. Aplica a cualquier comando cuyo resultado importe y se canalice para acortar.

**La precaución también falla (2026-08-18, facturaia).** Dos formas medidas el mismo día:
- `${pipestatus[1]}` es de **zsh**. En el shell donde corren las herramientas del agente (bash) esa
  expansión sale **vacía**, así que el «exit capturado» no es 0 ni 1: es nada, y no mides. En bash es
  `${PIPESTATUS[0]}`. Si no sabes en qué shell estás, no uses el array: `cmd > log 2>&1; ec=$?`.
- Un **comando compuesto** devuelve el exit del ÚLTIMO, no del que importa: `git commit … ; git log`
  reportó éxito con el commit bloqueado por el hook, y un `git push` que no movió el remoto reportó 0.
  Para un push, la verificación no es el exit: es `git ls-remote origin <rama>` == `git rev-parse HEAD`.
