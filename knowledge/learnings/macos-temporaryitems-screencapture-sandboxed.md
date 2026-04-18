---
title: macOS screencapture en TemporaryItems está sandboxed (Operation not permitted)
date: 2026-04-16
source: claude-code-session
tags: [macos, claude-code, sandbox, troubleshooting]
---

Rutas tipo `/var/folders/<hash>/T/TemporaryItems/NSIRD_screencaptureui_<random>/Captura*.png` — las temporales que macOS crea cuando haces `Cmd+Shift+4` o `Cmd+Shift+Ctrl+4` sin guardar la captura — dan **"Operation not permitted"** desde la Bash tool o Read tool de Claude Code.

El archivo puede incluso existir en disco según `ls` interno, pero el proceso de Claude Code no tiene permiso de lectura en esa jerarquía — la sandbox del sistema bloquea accesos a `TemporaryItems`.

## Síntomas

```
$ ls /var/folders/.../TemporaryItems/NSIRD_screencaptureui_.../
ls: Operation not permitted
```

## Solución

Pedir al usuario que **arrastre la imagen al chat** en lugar de pegar el path. Al arrastrar, Claude Code copia el archivo a su propio temp accesible y lo pasa como attachment del mensaje.

Alternativa: pedirle que guarde la captura en `~/Desktop/` o `~/Downloads/` y pase esa ruta.

## Por qué pasa

`TemporaryItems` vive en el sandbox del proceso que la creó (screencaptureui). Cualquier otro proceso con sandbox distinta — incluido Claude Code — no tiene entitlements para leer ahí, aunque `stat` lo vea.
