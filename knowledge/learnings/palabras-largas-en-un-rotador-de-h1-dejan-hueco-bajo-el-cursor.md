---
title: palabras largas en un rotador de h1 dejan hueco bajo el cursor
date: 2026-08-01
source: claude-code-session
tags: [frontend, css, copy]
---
Un H1 con efecto de tecleo suele reservar altura fija para una línea
(`min-height: 1.25em`) asumiendo que la palabra que rota **no envuelve**. Si el copy
nuevo es más largo que el original, envuelve a dos líneas, el cursor cae a una tercera
y aparece un hueco muerto bajo el titular que parece un bug de maquetación.

Caso real (agentesia-web): «automatizar lo que nadie automatiza» (35 chars) frente a
«no perder más clientes» (22) del original. El CSS lo avisaba en un comentario que
nadie leyó antes de escribir el copy.

Regla: al cambiar las palabras de un rotador, respetar la longitud de las que había —
son parte del contrato visual del componente, no texto libre. Y leer el CSS del
contenedor antes, que suele documentar el supuesto.
