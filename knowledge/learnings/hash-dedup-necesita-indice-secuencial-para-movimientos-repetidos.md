---
title: hash dedup necesita índice secuencial para movimientos repetidos
date: 2026-04-21
source: claude-code-session
tags: [dedup, importación, facturaia]
---

Al deduplicar registros importados (ej: movimientos bancarios de un extracto), un hash de `fecha + concepto + importe` produce falsos positivos cuando hay transacciones legítimas repetidas el mismo día (dos cafés de 3,50€ en el mismo bar).

**Fix**: añadir un índice secuencial (posición en el fichero fuente) al hash:

```
hash = sha256(cuenta_id + fecha + concepto + importe + idx)
```

Donde `idx` es la posición del movimiento dentro del extracto (0, 1, 2...).

Esto aplica a cualquier importación de datos donde puedan existir registros legítimamente duplicados en el mismo lote.

**Materializado en prod (2026-07-23)**: exactamente este bug, en `movimientos_bancarios` de TuFacturaIA — comisiones de divisa idénticas (fecha+importe+concepto) repetidas el mismo día se perdían silenciosamente. Esta nota estaba escrita desde abril pero no enlazada desde ningún sitio (`hot.md`/hub), así que no se encontró al escribir el importador real. El fix aplicado NO fue el hash+idx sugerido arriba (la clave de dedup en BD no guarda posición de origen y retrofitarla habría exigido migración): en su lugar, se agrupan las filas por clave ANTES de tocar la BD, se cuenta cuántas ya existen, y se inserta solo la diferencia hasta igualar el tamaño del lote — mismo objetivo (no perder duplicados legítimos), sin tocar esquema. Ver PR #1190.
