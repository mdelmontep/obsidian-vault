---
title: ccxt no implementa crear órdenes de futuros en MEXC (createSwapOrder es stub)
date: 2026-06-24
source: claude-code-session
tags: [ccxt, exchange, trading]
---
Al abrir una posición de futuros en MEXC vía ccxt: `mexc createSwapOrder() does not support yet`. Es un stub no implementado en ccxt, NO un problema de claves/permisos/KYC. Solo falla al CREAR órdenes de swap; fetch de balance, posiciones y velas sí funciona (engaña: parece que "casi" va).

Verificar el soporte de órdenes de futuros del exchange en ccxt ANTES de elegirlo, no tras integrar claves. Alternativas que sí crean órdenes swap: BingX (sin passphrase; tiene demo VST en open-api-vst.bingx.com, exige one-way mode) y Bitget (requiere passphrase).
