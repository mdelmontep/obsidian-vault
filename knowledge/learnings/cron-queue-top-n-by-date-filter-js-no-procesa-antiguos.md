---
title: cron tipo queue con "top-N by date + filter JS" no procesa pendientes antiguos
date: 2026-05-21
source: claude-code-session
tags: [cron, postgres, anti-pattern]
---

Anti-pattern frecuente al refactorizar un cron de "procesar lo nuevo":

```ts
// MAL: cuando los recientes están "done", retorna nothing_pending para siempre
const { data: candidates } = await admin
  .from('movs')
  .select('*')
  .order('fecha', { ascending: false })
  .limit(500)
const pending = candidates.filter(c => !c.processed_at)
```

Una vez los 500 más recientes están todos `processed_at IS NOT NULL`,
el cron NUNCA llega a movs antiguos sin procesar — la cola se atasca
silenciosa. Orgs con histórico se quedan fuera para siempre.

Fix correcto: filtro en SQL con `NOT EXISTS` o RPC dedicada:
```sql
SELECT * FROM movs mb
WHERE mb.deleted_at IS NULL
  AND NOT EXISTS (SELECT 1 FROM mb_proc WHERE mb.id = ... AND version = $1)
ORDER BY fecha DESC LIMIT $2
```

PostgREST embed da problemas con N FKs ambiguas → mejor RPC
`get_pending_*(p_limit, p_version)` callable via `admin.rpc(...)`.

Caso real: FacturaIA cron `anomaly-batch` mig 141.
