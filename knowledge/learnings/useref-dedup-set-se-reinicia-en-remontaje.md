---
title: useRef como set de "ya notificado" se reinicia en cada remontaje del componente
date: 2026-06-16
source: claude-code-session (facturaia ticket bandeja)
tags: [react, nextjs, hooks, useref, facturaia]
---
Un `useRef<Set>(new Set())` usado para "no repetir X" (toasts, eventos) arranca VACÍO
en cada montaje. Si el componente se desmonta/remonta al navegar (App Router: salir y
volver a la página), el efecto que lo consume re-dispara para TODOS los items
preexistentes, no solo las transiciones nuevas. Síntoma: toast/notificación que
reaparece cada vez que vuelves a la página.

Fix: sembrar el ref en la primera carga sin actuar (`seededRef` que marca "ya vistos"
los items presentes al montar) y solo reaccionar a transiciones que ocurren con el
usuario ya en la página. localStorage solo si debe sobrevivir refresh completo (añade
coste de limpiar huérfanos).

Caso real: bandeja IA facturaia, toasts "no se pudo extraer datos" (PR #276).
Relacionado: [[recuperacion-ui-gated-por-estado-pierde-items-en-estado-hermano]].
