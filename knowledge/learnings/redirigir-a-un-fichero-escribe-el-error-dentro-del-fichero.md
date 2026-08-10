---
title: `comando > fichero` escribe el error DENTRO del fichero que querías generar
date: 2026-08-11
source: claude-code-session
tags: [shell, tooling, codegen]
---
`supabase gen types typescript --local > src/lib/database.types.ts` redirige **antes** de saber si
el comando funciona. Sin `DOCKER_HOST`, el CLI escribió su JSON de error dentro del fichero de
tipos, y lo que falló dos pasos después fue `tsc` con un `';' expected` en la línea 1 que no apunta
a nada.

Vale para cualquier generador: tipos, OpenAPI, migraciones, sitemaps.

Patrón: generar a temporal, **validar que la salida parece lo que debe**, y solo entonces mover.
```sh
TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
cmd > "$TMP" || { echo "✗ falló"; exit 1; }
head -1 "$TMP" | grep -q '^export type Json' || { echo "✗ no son tipos"; exit 1; }
mv "$TMP" "$DESTINO"
```
La comprobación tiene que **discriminar**: probarla en rojo (sin Docker) y ver que el fichero
anterior NO se toca.
