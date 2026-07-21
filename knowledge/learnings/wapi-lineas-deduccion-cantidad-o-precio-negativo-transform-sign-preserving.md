---
title: al importar líneas negativas de un ERP legado, normalizar signo con transform que preserva el total
date: 2026-07-21
source: claude-code-session
tags: [migracion, erp, facturaia, obras]
---
Un ERP legado (wapi) codifica una "línea de deducción" a veces con `cantidad` negativa y precio positivo, otras con `cantidad` positiva y `precio` negativo — sin regla fija, incluso dentro del mismo presupuesto. El esquema destino (FacturaIA) exige `cantidad<0` como única señal de ajuste y `precio>=0` siempre (para no contaminar el desglose material/MO del motor de precio).

Fix: como `total = cantidad × precio`, la transformación `cantidad = -|cantidad|, precio = |precio|` preserva el total exacto sin importar en qué campo venía el signo original. Validar contra el total AUTORITATIVO del origen (el stored procedure/función real del ERP, no un recálculo propio) antes de dar por buena la paridad — en este caso destapó 2 filas mal resueltas (nodo/material) que un chequeo solo-interno no habría visto.
