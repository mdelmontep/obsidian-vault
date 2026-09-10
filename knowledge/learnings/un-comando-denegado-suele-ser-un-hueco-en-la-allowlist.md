---
title: un comando denegado suele ser un hueco en la allowlist, no una política
date: 2026-09-10
source: facturaia
tags: [claude-code, permisos, arnes]
---
«El clasificador me lo deniega» se dijo dos sesiones seguidas de `gh issue comment` como si
fuera una prohibición. No lo era: la allowlist tenía `gh pr *`, `gh api *`, `gh repo *` y
`gh run *`, y **`gh issue` no estaba en ninguna**. Una línea en `settings.local.json` y el
comando pasó, **en caliente, sin reiniciar la sesión**.

Dos reglas que salen de ahí:

- Antes de decir «no puedo» y delegar el gesto en el usuario, **leer la allowlist** y decir
  qué falta. Un bloqueo sin causa nombrada se convierte en tarea suya para siempre.
- Y el reverso: `gh api` estaba permitido y habría publicado el mismo comentario. Usar otro
  binario para hacer justo lo que se acaba de denegar es rodear el bloqueo, no resolverlo.
  Lo que se arregla es el permiso, a la vista, no el camino.

El fichero local es el sitio: `.claude/settings.local.json` está gitignorado, así que no
cambia la política del repo ni la de nadie más.

Y antes de dar por hueco de allowlist una denegación, mira si el comando era **compuesto**: al
denegarse se pierde también lo que preparabas en la misma llamada →
[[un-comando-compuesto-denegado-no-escribe-ni-su-parte-inocua]].
