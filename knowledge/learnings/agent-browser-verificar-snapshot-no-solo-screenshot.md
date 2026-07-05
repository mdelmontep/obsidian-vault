---
title: agent-browser — verificar mensajes con snapshot de accesibilidad, no solo screenshot
date: 2026-07-05
source: claude-code-session
tags: [agent-browser, qa, testing, gotcha]
---

Antes de concluir "no aparece ningún error/toast" en un smoke con `agent-browser`, buscar el texto en `agent-browser snapshot` (árbol de accesibilidad completo), no solo mirar capturas de pantalla. Un modal con scroll interno puede tener contenido fuera del encuadre visible incluso con `screenshot --full` (el full-page scrollea la PÁGINA, no el contenedor interno del modal).

**Caso real**: smoke de TuFacturaIA concluyó que un mensaje de error tras un 409 "nunca se pintaba" — la captura del modal no llegaba a la parte baja donde vivía. `agent-browser snapshot | grep -iE "alert|error"` lo habría confirmado sin reproducir el escenario dos veces.

**Regla**: tras cualquier acción que dispare error/aviso, antes de reportar "silencioso": (1) `agent-browser snapshot | grep -iE "alert|error|toast"`, (2) si hay match, `scrollintoview` a ese ref antes de la captura final. Solo reportar ausencia si el snapshot completo tampoco lo tiene.
