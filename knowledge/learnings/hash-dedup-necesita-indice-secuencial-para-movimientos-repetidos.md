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
