---
title: un test de forma sobre postgres mide tuplas leídas, no milisegundos
date: 2026-10-13
source: facturaia (#3454, mig 1053)
tags: [postgres, testing, performance, flakes]
---
**Qué pasa**: un test de «escala lineal» medido con reloj (o con bloques) da de x3 a x20 sobre el mismo árbol según la carga, y se lee como flake. En FacturaIA era el rojo más repetido de la integración.

**Por qué**: la variación no era ruido, era el bug. La RPC inserta y procesa en la misma transacción una tabla sin estadísticas, y el planificador estima 1 fila. Un `UPDATE ... WHERE id = x AND org_id = y` o un `EXISTS` correlado por fila puede elegir un índice sin la clave y recorrer el lote entero en cada fila: cuadrático según el plan del momento (2.000 filas, 4 M tuplas en una sentencia).

**Fix**:
- UPDATE solo por la clave primaria.
- Lo «¿hay otra fila que...?» con ventanas (`max() OVER` las anteriores, `lead()`, `count() OVER PARTITION`) en la misma lectura que abre el bucle.
- `ANALYZE` dentro de la transacción no sirve: su lock serializa todas las llamadas.

**Medición**: tuplas de la tabla de interés en `pg_stat_xact_user_tables`, tope por fila + ratio entre dos tamaños. Es determinista: la cifra del gate coincide con la aislada. Probar que muerde reintroduciendo cada lectura cuadrática.
