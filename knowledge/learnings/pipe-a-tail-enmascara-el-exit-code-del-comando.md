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
