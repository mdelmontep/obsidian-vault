---
title: una columna que se retira sola necesita un tercer estado, no un interruptor
date: 2026-08-26
source: facturaia
tags: [frontend, css, tablas, ux, container-query]
---
Si una tabla retira columnas por prioridad cuando no caben, el selector ya no
puede ser `on/off`: «visible» pasa a significar dos cosas —«si cabe» y «aunque
no quepa»— y quien fija una la ve desaparecer igual.

Modelo: **auto · fija · oculta**, con `auto` de fábrica. ARIA lo expresa sin HTML
inválido: `aria-checked="mixed" | true | false`. La regla es **lo explícito gana
a lo automático**, y no se deja a la intención: cada regla de retirada lleva
`:not(.colFijada)` y hay un test que recorre el CSS y falla si a alguna le falta.
Fijar obliga a la tabla a dejar de encogerse — ancho mínimo por escalones, uno
por columna fijable — y el contenedor scrollea con la columna identificadora
`sticky` y fondo opaco ([[header-sticky-glass-sangra-mesh-debe-ser-opaco]]).

Solo scroll horizontal es peor default cuando la fila entera navega: arrastrar y
clicar se pelean, y lo primero que sale de pantalla es lo que identifica la fila.
Ver [[pill-overflow-hidden-en-grid-se-recorta-usar-container-query-en-modal]].
