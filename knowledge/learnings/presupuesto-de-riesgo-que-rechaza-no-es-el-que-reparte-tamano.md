---
title: un presupuesto que RECHAZA solicitudes no es el mismo que REPARTE el tamaño
date: 2026-08-02
source: claude-code-session
tags: [trading, riesgo, diseño, backtest]
---

Al poner un tope agregado (riesgo total de cartera, cuota de API, concurrencia) hay dos
implementaciones que suenan iguales y no lo son:

- **Rechazar**: al llegar al tope, las siguientes solicitudes se caen. Introduce un sesgo
  de **orden de llegada** — te quedas con las primeras, no con las mejores, y pierdes la
  diversificación que justificaba el tope.
- **Repartir**: el tope se divide entre los participantes y cada uno entra más pequeño.
  Todos siguen dentro; solo cambia la escala.

Medido (cryptobruj, presupuesto 13% sobre 217 pares): rechazar tiró el **38% de las
entradas** y llevó el CAGR de 14,76% a **1,66%**, con el Sharpe de 0,81 a 0,21. Repartir
por tamaño dejó el Sharpe **exactamente igual** (0,81) y solo movió la escala. El tope no
era el problema: la forma de aplicarlo sí.

Señal de alarma: si al activar un límite el número de eventos cae mucho, lo has puesto como
puerta y no como divisor. Blíndalo con un test que afirme el reparto, no el tope.
