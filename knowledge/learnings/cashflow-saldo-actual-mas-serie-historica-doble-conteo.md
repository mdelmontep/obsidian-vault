---
title: combinar saldo-actual con serie acumulada desde el pasado = doble conteo
date: 2026-05-27
source: claude-code-session
tags: [cashflow, correctness, facturaia]
---
Un forecast que arranca el acumulado en meses pasados (offset -N) y SUMA los netos reales de esos meses NO debe recibir el saldo-de-hoy como `saldoInicial`: el saldo de hoy YA refleja esa actividad pasada → se cuenta dos veces e infla/deprime el saldo proyectado (el número que decide veredictos).

Patrón correcto: arrancar la serie en 0 y combinar `saldo_real_hoy + (acum_mes_objetivo − acum_mes_actual)`. La resta cancela el histórico y deja solo el neto futuro.

Caso FacturaIA `analisis-compra`: pasaba `saldoInfo.saldo` a `buildCashflowData` (acumula desde offset -5) → ok/apretado/no_recomendado mal. El cliente web ya compensaba con un pre-pass (`computeSaldoInicialTotal`); el endpoint no.

Trampa: si el test mockea la función de forecast, el doble conteo no se ve (falso verde). Ver [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] · [[narrative-headline-no-mezclar-saldo-acumulado-con-delta-mensual]].
