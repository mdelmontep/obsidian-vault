---
title: la unidad de acumulación decide si una puerta de calidad es alcanzable, y cambiarla después invalida el expediente
date: 2026-08-09
source: claude-code-session
tags: [agentic, gates, metricas, producto]
---

Una puerta tipo "N decisiones acumuladas antes de conceder X" se discute siempre por el número, y
el número casi nunca es el problema: lo es **sobre qué se acumula**.

Con la unidad puesta en «el agente», un cliente pequeño tiene que acumular N sobre **todo** lo que
el agente hace antes de que se le conceda **cualquier cosa** — tarda mucho y luego concede ancho,
que es lo peor de los dos mundos. Con la unidad en **(cliente × clase de decisión)** cada clase
acumula por su cuenta: la clase frecuente llega a N sola, la infrecuente sigue sin concederse, y la
concesión nace acotada. La puerta deja de medir volumen y pasa a medir evidencia.

**Se descarta agregar por vertical** (juntar clientes "parecidos") aunque resuelva el volumen:
contradice el motivo de que la puerta sea por cliente, y es la vía por la que uno hereda una
autonomía que nadie ganó con sus datos.

Y el coste de tiempo: la unidad va en el catálogo **desde el día 0**, aunque la lista de clases
esté vacía. Cambiarla cuando ya hay decisiones registradas **invalida el expediente entero** —lo
acumulado con la unidad vieja no se puede reagrupar—, así que es de las decisiones que sólo son
baratas antes de existir.

Relacionado: [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]] ·
[[una-aceptacion-no-es-senal-hasta-que-envejece-sin-ser-contradicha]]
