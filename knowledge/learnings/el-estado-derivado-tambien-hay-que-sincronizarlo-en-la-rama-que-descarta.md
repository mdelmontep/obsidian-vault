---
title: el estado derivado también hay que sincronizarlo en la rama que descarta el caso
date: 2026-08-15
source: claude-code-session
tags: [n8n, elphis, sincronizacion, anti-patron]
---

**Caso real (Centro Elphis, 2026-08-15):** para que el bot pudiera confirmar citas, `doctoralia-email-sync` pasó a escribir `paciente_data.cita` en `conversation_state`. El nodo se colgó del camino principal… que un guard anterior (`Guard campos mínimos`) **corta cuando el email es una cancelación**: `if (d.es_cancelacion) return {_skip:true}`. Resultado si no llego a mirarlo: la cita se queda `confirmada` para siempre y el bot le confirma a un paciente una cita que anuló. **Peor que no tener el dato**, porque suena autorizado.

**El patrón:** los guards que descartan casos ("skip", "ignored", "no aplica") se escriben pensando en *no hacer trabajo*, y son invisibles cuando después añades un efecto que sí debería ocurrir en esos casos. Una cancelación no es "nada que hacer": es un cambio de estado.

**Regla:** al añadir persistencia de estado derivado a un flujo, recorre las ramas de descarte y pregunta por cada una si el estado cambia ahí. Si cambia, esa rama necesita su propia escritura. Se puede hacer sin `if` nuevo metiendo el discriminante en el `WHERE`: `WHERE $2::text = 'cancelacion_detectada' AND …` → 0 filas para los demás skips.

Relacionado: [[n8n-status-success-no-implica-camino-critico]] · [[un-nodo-de-log-con-onerror-continue-puede-no-haber-escrito-nunca]]
