---
title: toggle entre vistas de datos relacionados suele ser síntoma de mal diseño UX
date: 2026-05-26
source: claude-code-session
tags: [ux, diseño, frontend, dataviz]
---

Cuando una UI obliga al usuario a elegir entre dos vistas de datos **complementarios** (Saldo|Flujo, Histórico|Previsión, Lista|Tabla con mismas filas), el toggle suele ser síntoma de que esas vistas son una sola lectura mental partida en dos.

**Regla**: antes de añadir un toggle, preguntarse si las dos vistas responden preguntas que el cerebro hace a la vez. Si sí → integrar en una visualización única, no dos modos.

**Heurística para detectarlo**:
- ¿El usuario tendría que tocar el toggle varias veces para entender una situación? → integrar.
- ¿Las dos vistas tienen ejes/datos compartibles (eje X común, datos correlacionados)? → integrar.
- ¿Una de las dos vistas es claramente la principal? → entonces la otra debería ser detalle al hover o sub-zona, no un modo igual.

Toggle SÍ tiene sentido cuando las vistas son **mutuamente excluyentes** (cambiar de filtro, periodo, granularidad, idioma) o cuando una vista es muy densa y la otra simplificada para móvil/escaneo.

**Caso real (FacturaIA 2026-05-26)**: chart cashflow iteración 1 con toggle `Saldo|Flujo` se sintió "tosko"; iteración 2 integró ambos en un chart de dos bandas verticales (saldo arriba 72% + flujo abajo estilo volumen TradingView) → lectura única, fricción cero. Cross-ref [[dataviz-dos-escalas-bandas-verticales-no-dual-axis]].
