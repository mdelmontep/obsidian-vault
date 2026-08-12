---
title: audit_log multi-escritor — procedencia en el `after` jsonb, before sin carrera vía for-update / delete-returning
date: 2026-07-14
source: claude-code-session
tags: [postgres, audit, agentes, multi-tenant, transacciones]
---
Cuando un SEGUNDO escritor (p. ej. el agente) entra a un `audit_log` que ya tiene un dueño (el dashboard), sin romper nada:

- **Procedencia sin columna nueva**: mete el canal (voice/onboarding/import/chat) DENTRO del `after` JSONB. Cero migración; el lector del otro escritor ignora claves extra. Evita el ADD COLUMN + drift.
- **Audit en la MISMA tx que la entidad** (all-or-nothing). Si los stores son finos (una query cada uno) y el seam transaccional vive en el caller/executor (no en el store, como sí hace un write-store unificado), enhebra el `TransactionHandle` por el camino de escritura y bindea el INSERT del audit a esa conexión.
- **`before` sin carrera read-then-write**: en UPDATE → `SELECT … FOR UPDATE` dentro de la tx y luego el patch; en DELETE → `DELETE … RETURNING` (el `before` **sobrevive al cascade** porque `audit_log.entity_id` va SIN FK). 🔴 **CORREGIDO 13-ago (AGH #1042): ese `FOR UPDATE` cierra la carrera de ACTUALIZACIÓN y NO la de creación** — en un upsert, la mitad de los casos. Sin fila que bloquear no toma candado, así que dos primeras escrituras concurrentes leen las dos `null` y auditan las dos `create`/`before: null`: la serie cuenta **dos creaciones de la nada** y el salto entre valores desaparece. La transición hay que decidirla **a la vez que se escribe**. Ver [[select-for-update-sin-fila-no-bloquea-y-el-subquery-del-from-no-se-reevalua]].
- **Deps nuevas (audit/tx) OPCIONALES** en los executors (default noop/in-memory) para no romper los N call sites de tests; inyecta las reales SOLO en el composition root.
- **Atomicidad se prueba con pg-real**: inyecta un audit que lanza → la entidad debe hacer rollback. Gate verde con fakes in-memory NO lo demuestra (el runner in-memory es no-op). Ver [[subagente-feature-sin-cablear-composicion]].

Caso real: AGH #485 (el agente = 2º escritor de `audit_log`). Reusable en cualquier plataforma de agentes con dashboard + audit compartido.
