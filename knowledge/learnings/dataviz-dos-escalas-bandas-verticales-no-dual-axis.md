---
title: dos escalas distintas en un chart → bandas verticales TradingView, no dual-axis
date: 2026-05-26
source: claude-code-session
tags: [dataviz, frontend, charts, ux]
---

**Problema**: cuando un chart necesita mostrar dos métricas con órdenes de magnitud distintos (ej. saldo €k vs flujo €), un dual-axis (Y izquierda saldo, Y derecha flujo) es **ilegible** — el usuario tiene que cruzar mentalmente dos escalas y la lectura nunca es directa.

**Patrón correcto**: dos bandas verticales que comparten eje X (estilo TradingView "price + volume"):
- Banda superior 65-75% de altura: la métrica primaria (línea de saldo, precio, KPI continuo).
- Banda inferior 20-30%: la secundaria (barras de flujo, volumen, deltas).
- Separador sutil 0.5px entre bandas, no border completo.
- Eje X común con las mismas etiquetas (meses, días).
- Etiquetas micro a la izquierda nombrando cada banda (`SALDO` / `FLUJO`).

**Por qué funciona**: cada métrica tiene su propio espacio visual con su propia escala, el ojo sabe dónde mirar para cada pregunta, y el eje X compartido conecta las dos historias temporalmente.

**Cuándo NO aplica**:
- Si una métrica es claramente derivada de la otra (ej. neto = ingresos − gastos) → mejor stacked o tooltip.
- Si la secundaria es opcional y el usuario rara vez la mira → tooltip al hover, no banda permanente.

**Caso real**: FacturaIA chart cashflow `26cb553` — saldo proyectado arriba (línea suavizada Catmull-Rom→Bézier) + flujo mensual abajo (barras pareadas ingresos/gastos). Iteración previa con toggle Saldo|Flujo se sentía fragmentada. Cross-ref [[toggle-vistas-relacionadas-es-sintoma-mal-diseno-ux]].
