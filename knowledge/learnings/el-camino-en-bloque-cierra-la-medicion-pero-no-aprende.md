---
title: el camino "en bloque" cierra la medición pero no aprende, y el loop nunca cierra
date: 2026-08-26
source: facturaia
tags: [facturaia, learning-loops, conciliacion, agentic, medicion]
---

Medido en prod el 26-ago-2026: `AgentesiaLab SL` lleva `categorias` en **activo**
con el gate abierto y **109 decisiones verdes aceptadas**, y sus dos reglas
aprendidas siguen en `veces_confirmada = 1` desde el 23-jul. Cero filas con
`categoria_source='regla'` en toda la BD: la primera aplicación silenciosa no ha
ocurrido nunca.

No es casualidad ni falta de uso. **107 de las 109 verdes se cerraron por
`bulk_confirm`, y `closeCategoriaDecisionsBulk` no llama a `aprenderCategoria`**
— por coste, y está escrito en su docstring. Solo aprende el PATCH individual.
Así que la vía que el usuario usa de verdad (confirmar todo de golpe) alimenta el
denominador del gate y no alimenta la memoria: la métrica sube, el aprendizaje se
queda plano, y el umbral de N confirmaciones no se alcanza jamás.

Regla: si un flujo tiene camino rápido y camino individual, **medir por cuál
entran los datos de verdad** antes de dar por vivo un contador que solo incrementa
el lento. Un umbral de aprendizaje colgado del camino minoritario es un umbral
inalcanzable.

Va con [[reglas-aprendidas-de-confirmacion-manual-cierra-loop-aprendizaje]] (el
diseño del loop) y [[un-gate-abierto-con-la-metrica-caducada-no-vuelve-a-cerrarse]].
