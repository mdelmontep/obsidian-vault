---
title: «Cierra #N» no cierra el issue — GitHub solo reconoce las keywords en inglés
date: 2026-07-28
source: claude-code-session
tags: [github, gh-cli, proceso, issues]
---
Escribiendo las PRs en español sale natural poner `Cierra #632` / `Resuelve #632` en el cuerpo. **GitHub no lo reconoce**: las únicas keywords que autocierran al mergear son las inglesas — `close`/`closes`/`closed`, `fix`/`fixes`/`fixed`, `resolve`/`resolves`/`resolved`.

Resultado: la PR se mergea, el issue **se queda abierto** y nadie lo nota hasta revisar el backlog. Peor en repos con varias sesiones en paralelo: un issue abierto es la señal de "libre", así que otra sesión puede cogerlo y reimplementar algo que ya está en `main`.

- Usar `Closes #N` en inglés aunque el resto del cuerpo vaya en español.
- Al cerrar sesión, **verificar el estado real** (`gh issue view N --json state`), no asumir que el merge lo cerró.
- Ojo también: la keyword debe estar en el **cuerpo de la PR** (o en el commit del default branch); en un comentario posterior no cuenta.

Caso real: agh-iberica PR #633 mergeada (`66026f4`), issue #632 abierto — cerrado a mano.
