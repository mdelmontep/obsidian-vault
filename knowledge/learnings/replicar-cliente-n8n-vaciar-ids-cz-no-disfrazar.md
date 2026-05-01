---
title: replicar workflows n8n entre clientes vaciar IDs origen a placeholders
date: 2026-05-01
source: claude-code-session
tags: [n8n, replicar, kommo, gotcha]
---

Al replicar workflows de un cliente A (CZ) a uno B (Simarro), los IDs hardcodeados rompen B silenciosamente si se dejan o se mapean mal. Tipos: `task_type_id`, `responsible_user_id`, sheet IDs, pipeline/status IDs, custom field IDs, calendar IDs, salesbot IDs, amojo_id, email destinatarios.

Regla: vaciar a placeholder explícito (`TASK_TYPE_ID_TODO`, `SHEET_ID_X_TODO`) en vez de dejar el ID origen disfrazado. Documentar tabla de pendientes en `CLAUDE.md` del proyecto destino. Probar end-to-end (no solo sintaxis) — un task con type inválido devuelve 400 y los nodos posteriores (email, calendar) NO se disparan.

Diff por nombres de nodo detecta nodos que faltan tras el clonado (típicos olvidados: `Create event` GCal, `Eliminar evento`, `Edit Fields Retell`, `Respond Retell`, `Send Confirmation Email` form web, `Append row in sheet`):
```python
faltan = {n['name'] for n in cz} - {n['name'] for n in cliente}
```
