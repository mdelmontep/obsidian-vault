---
title: colima solo comparte $HOME, así que un bind mount desde /tmp aparece como directorio vacío
date: 2026-07-27
source: claude-code-session
tags: [docker, colima, macos, tooling]
---

Colima (Docker en Mac sin Docker Desktop) monta por defecto **solo `$HOME`** dentro de la
VM. Un `-v /private/tmp/algo/fichero.ts:/app/fichero.ts` no falla: Docker crea en su lugar
un **directorio vacío**, y el error que ves después es del programa, no del montaje.

Síntoma real (27-jul): montar un script en `/app/render.cts` daba
`ERR_MODULE_NOT_FOUND ... /app/render.cts/index.ts` — el resolutor lo trataba como carpeta.
`ls -la` dentro del contenedor lo confirmó: `drwxr-xr-x` en vez de fichero.

Reglas:
- Todo lo que se monte en un contenedor bajo colima, debajo de `$HOME`. El scratchpad de
  `/tmp` no viaja.
- Ante un `MODULE_NOT_FOUND` raro con un bind mount, comprobar primero `ls -la` de la ruta
  DENTRO del contenedor: si es directorio, es el montaje, no el código.
- Se puede ampliar con `colima start --mount /ruta:w`, pero es más simple mover el material.
- Instalación mínima para levantarlo: `brew install colima docker` + `colima start --cpu N
  --memory N`. El heap de `next build` va por RAM detectada: en una VM de 8-12 GB Node topa
  el old-space en ~2 GB y el build muere por OOM; se arregla con
  `NODE_OPTIONS=--max-old-space-size=6144`, no con más RAM de VM.
