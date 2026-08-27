---
title: un gate que solo mide lo aplicado puntúa al filtro humano, no al proponente
date: 2026-08-27
source: agency-portal
tags: [agentes, metricas, autonomia, maker-checker]
---

Puerta para dar autonomía a un proponente automático: «≥10 propuestas resueltas con
≥70 % de acierto». Medía solo las **aplicadas** — o sea, las que un humano ya había
aprobado. Eso puntúa la calidad del filtro humano, no la del proponente; y las
**descartadas** son exactamente las que el siguiente nivel aplicaría solo.

Tres fallos más en la misma puerta, todos genéricos de «promocionar a un agente»:

- **Circularidad**: el criterio de éxito («bajan las ocurrencias») lo producía el
  propio juez que hizo la propuesta. Hace falta al menos una señal que no venga de él
  (en este caso, deterministas: `error_flag`, `handoff`, duración).
- **Goodhart**: una propuesta del tipo «no menciones X» lleva su contador a cero y
  puntúa como acierto mientras empeora el negocio.
- **Muestra**: n=10 con ≥70 % tiene IC95 ≈ [35 %, 93 %]. Es una moneda al aire con
  cara de umbral.

Y el gate lo **aplica el código**, no lo pinta el panel: auditar un cambio de nivel
no es bloquearlo. Un nivel que se puede poner a mano el primer día no es una puerta.
