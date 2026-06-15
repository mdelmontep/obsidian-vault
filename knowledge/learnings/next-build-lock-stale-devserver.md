---
title: next build falla con "another process running" por .next/lock stale
date: 2026-06-15
source: claude-code-session
tags: [nextjs, build, devserver]
---

`next build` falla con "Another next build process is already running" si existe
`.next/lock` (archivo vacío, 0 bytes) sin proceso activo que lo tenga abierto.

El dev server usa `.next/dev/lock` (JSON con `{pid, port}`). Son archivos distintos.
El build lock es `.next/lock` y se crea al arrancar `next build`.

Causa: build anterior murió sin limpiar el lock (CI abort, kill -9, etc.).

Fix: `rm .next/lock` y reintentar.

No confundir con el dev server corriendo — ese no bloquea `next build` en principio
salvo que el lock stale quede de una sesión previa.
