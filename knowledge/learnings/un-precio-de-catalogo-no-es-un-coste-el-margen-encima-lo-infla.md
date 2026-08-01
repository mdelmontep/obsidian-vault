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
- Antes de un backfill de precios: snapshot previo, informe de impacto separando orgs de
  prueba de las reales, y que lo vea el cliente. Aquí el −63 % que asustaba era casi todo
  de una org `is_test`.
- **CORREGIDO 02-ago con la respuesta de la clienta**: di por «familia-cajón peligrosa» una
  llamada `SIN FAMILIA` con descuento del 78 % y artículos de 5 cifras. Era deliberada. Como
  la app exige descuento para poder presupuestar, ella **crea familias a propósito**
  (`SIN FAMILIA`, `proyecto`, `desplazamiento`) para dárselo a **servicios propios** que no
  vienen de ningún fabricante. El dato que lo confirma y que no miré antes de alarmar: de
  esos 1.306 materiales, **0 tienen referencia de fabricante y 0 tienen marca**. Lección: un
  valor raro en datos de cliente puede ser su forma de sortear una restricción que le
  pusiste tú; antes de llamarlo error, comprueba si el resto de columnas lo explica y
  pregúntale. El backfill masivo se descartó igualmente, pero por otro motivo suyo: muchos
  descuentos están obsoletos o son de proveedores con los que ya no trabaja.
