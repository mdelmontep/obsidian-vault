---
title: COALESCE(agregado, 0) como salvaguarda anti-NULL puede ser una regla de negocio equivocada
date: 2026-07-20
source: claude-code-session
tags: [sql, pricing, gotcha, data, facturaia]
---
Un `COALESCE(MIN(...), 0)` (o `?? 0` en TS) puesto "para no dar NULL/NaN"
esconde una decisión de negocio: define qué vale el caso "sin filas". En el
motor de precio de Obras (TuFacturaIA), `PFVC_min = COALESCE(MIN(PFVC entre
proveedores), 0)` hacía que un material SIN proveedor enlazado se valorara a
coste 0 → se vendía solo por la mano de obra. Tras importar la tarifa de
Telematel (catálogo entero aún sin proveedores), TODO salía a 0 € de material:
un accesorio de tarifa 213,97 € → precio de venta 0,00 €. Nadie lo decidió; era
un default defensivo.

Regla: el fallback de un agregado sobre conjunto vacío es una REGLA DE NEGOCIO,
no un detalle técnico. Elige el valor correcto (aquí: la base de tarifa con el
margen aplicado, `base × (1+margen)`), no 0 por inercia. Señal de alarma: un
total/precio que sale exactamente 0 cuando el dato de partida no es 0.
Ver [[put-objeto-completo-borra-campos-no-mapeados]] (misma familia: defaults
silenciosos que corrompen datos de negocio).