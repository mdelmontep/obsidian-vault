---
title: escribir "Cierra #N" no cierra la issue, GitHub solo entiende las palabras clave en inglés
date: 2026-07-27
source: claude-code-session
tags: [github, proceso]
---

GitHub cierra issues desde un PR solo con su lista cerrada de keywords, y **todas son en
inglés**: `close/closes/closed`, `fix/fixes/fixed`, `resolve/resolves/resolved`. Cualquier
otra cosa ("Cierra #1259", "Resuelve #1259") queda como un enlace bonito que no hace nada.

Caso real (27-jul): PR #1262 mergeada con "Cierra #1259" en el cuerpo; la issue siguió
abierta hasta cerrarla a mano.

Importa porque en estos repos se escribe todo en español, así que el fallo es sistemático,
no un despiste: cualquier issue cerrada "por PR" puede seguir abierta y contaminando el
recuento de pendientes.

Reglas:
- En el cuerpo del PR, la línea de cierre en inglés: `Closes #N`. El resto del texto, en
  español, sin problema.
- Va en el **cuerpo del PR o en el commit del merge**; en un comentario suelto no cuenta.
- Al cerrar sesión, `gh issue list --state open` y comprobar que lo que se dio por resuelto
  está de verdad cerrado.
