---
title: un precio de catálogo no es un coste y aplicarle margen encima lo infla sin fallar
date: 2026-08-01
source: claude-code-session
tags: [pricing, obras, facturaia, modelo-de-datos]
---

En material de construcción la tarifa del fabricante es un **PVP inflado** sobre el que
cada distribuidor tiene su descuento pactado (40-54 % lo normal, hasta 78 %). Si el
descuento no está cargado, el motor toma la tarifa por coste y le suma el margen: el precio
sale alto y **nada falla**, no hay error ni aviso.

Medido contra el ERP del cliente: tarifa 64,19 € → su venta 53,55 € (dto 38,65 % + margen
36 %) → nuestro cálculo **83,45 €**, un 56 % de más.

- Un descuento del **0 % pactado es un dato**, distinto de "nunca lo he tocado": el modelo
  tiene que distinguir "no hay fila" de "hay fila con 0".
- Cuidado con las familias-cajón (`SIN FAMILIA`): un descuento a nivel de ese cajón se
  aplica a los artículos más caros y sin clasificar. Excluirla de cualquier volcado masivo.
- Antes de un backfill de precios: snapshot previo, informe de impacto separando orgs de
  prueba de las reales, y que lo vea el cliente. Aquí el −63 % que asustaba era casi todo
  de una org `is_test`.
