---
title: «Cierra #N» no cierra el issue — GitHub solo reconoce las keywords en inglés
date: 2026-07-28
source: claude-code-session
tags: [github, gh-cli, proceso, issues]
---
Escribiendo las PRs en español sale natural poner `Cierra #632` / `Resuelve #632` en el cuerpo. **GitHub no lo reconoce**: las únicas keywords que autocierran al mergear son las inglesas — `close`/`closes`/`closed`, `fix`/`fixes`/`fixed`, `resolve`/`resolves`/`resolved`.

Resultado: la PR se mergea, el issue **se queda abierto** y nadie lo nota hasta revisar el backlog. Peor en repos con varias sesiones en paralelo: un issue abierto es la señal de "libre", así que otra sesión puede cogerlo y reimplementar algo que ya está en `main`.

- Usar `Closes #N` en inglés aunque el resto del cuerpo vaya en español.
- Al cerrar sesión, **verificar el estado real** (`gh issue view N --json state`, o `gh issue list --state open` para ver de golpe lo que se dio por resuelto y sigue abierto), no asumir que el merge lo cerró.
- Ojo también: la keyword debe estar en el **cuerpo de la PR** (o en el commit del default branch); en un comentario posterior no cuenta.

El fallo es **sistemático, no un despiste**: en estos repos se escribe todo en español, así que cualquier issue dada por cerrada "por PR" puede seguir abierta contaminando el recuento de pendientes.

Casos reales: agh-iberica PR #633 mergeada (`66026f4`), issue #632 abierto — cerrado a mano. TuFacturaIA PR #1262 con "Cierra #1259" en el cuerpo, misma historia (27-jul).

*(Fusionado el 29-jul con `cierra-en-espanol-no-cierra-la-issue-de-github`, que decía lo mismo.)*
