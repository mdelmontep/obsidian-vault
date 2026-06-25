---
title: motor con input requerido debe defaultear, no fallar mudo
date: 2026-06-25
source: claude-code-session
tags: [arquitectura, stock, facturaia]
---

Un motor (función BD/servicio) que EXIGE un input y, si falta, hace `raise warning + continue` o no-op, convierte el fallo en silencioso — y lo multiplica por cada borde que olvida propagar el campo (Zod schemas, mapeos a la capa de dominio, payloads de RPC).

**Caso real**: `aplicar_movimientos_lotes` exigía `lote_id` para descontar stock de productos con lotes; sin él avisaba a logs efímeros y seguía. Varios bordes (POST `/api/facturas`, PATCH, API v1, voz) perdían `lote_id` → el stock no se descontaba y nadie se enteraba (ticket Chivite).

**Fix robusto**: el motor —single source of truth— aplica un **default sensato** en vez de fallar mudo (aquí: consumir partidas en orden **FEFO** automáticamente, con split, y `raise exception` solo si el stock real es insuficiente). Propagar el campo en los bordes es **defensa en profundidad**, no la solución: los canales ciegos (voz, API) no pueden aportarlo.

Relacionado: [[proyeccion-de-ledger-sin-guardia-diverge-en-silencio]] · [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]] · [[zod-strict-bloquea-campos-no-listados-silenciosamente]]
