---
title: sembrar una columna calculada en el INSERT la pisa el trigger
date: 2026-08-03
source: claude-code-session
tags: [postgres, triggers, testing, fixtures, facturaia]
---

Dos tests de integración sembraban `precio_venta_calculado: 100` en el propio
`INSERT` del material. El trigger `AFTER INSERT` recalcula esa columna desde sus
entradas, así que el 100 no sobrevivía ni un milisegundo: quedaba
`tiempo_mo_horas × precio_hora_mo`.

**La asimetría que despista:** el trigger de UPDATE del mismo repo escucha solo
columnas de ENTRADA (`UPDATE OF tiempo_mo_horas, familia, precio_tarifa…`), así
que un `UPDATE` posterior sobre la columna calculada **sí** persiste. El propio
test lo usaba más abajo para llevar el valor a 500 y le funcionaba. Sembrar en
el insert y actualizar después parecen lo mismo y no lo son.

**Síntoma:** el valor esperado va cambiando entre pasadas siguiendo a otro
ajuste de la org (aquí `obras_settings.precio_hora_mo`), lo que se lee como
contaminación entre tests en vez de como semilla ignorada.

**Fix:** insertar solo las entradas y fijar la columna derivada en un `UPDATE`
aparte. Antes de sembrar cualquier columna, comprobar si hay trigger que la
escriba: `\d+ tabla` o grep de `UPDATE OF` en las migraciones.
