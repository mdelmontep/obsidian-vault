---
title: la pregunta determinista se contesta con diez casos; la estadística, con mil
date: 2026-07-31
source: claude-code-session
tags: [metodo, verificacion, monitorizacion, testing]
---

Cuando "¿esto funciona?" resulta carísimo de contestar, casi siempre hay una pregunta
**contigua y determinista** que sí se contesta barato, y que suele ser donde están los bugs
de verdad.

Caso (cryptobruj-bot): saber si la estrategia tiene ventaja pide ~15 meses (variación entre
regímenes). Pero los tres fallos caros del proyecto fueron de **ejecución**, no de
estrategia: 17 puntos de winrate por saltarse velas, 36 posiciones zombi, un saldo ilegible
que escribió −87 USDT sobre un nocional de 6. Ninguno era la estrategia.

Y esa pregunta no es estadística: el sistema es una **función** de sus entradas, así que la
referencia y lo vivo deben producir la MISMA salida. Una discrepancia no es mala suerte, es
un bug — con diez casos ya se ve.

Patrón reutilizable (`conciliacion.py`): re-ejecutar la referencia sobre la ventana viva y
cruzar por clave natural, reportando por separado **falta en vivo** (señal perdida),
**sobra en vivo** (lo peor: la lógica viva no es la medida) y **mismo caso, valor
distinto**. Sirve igual para ETL, motores de reglas y precios recalculados.
