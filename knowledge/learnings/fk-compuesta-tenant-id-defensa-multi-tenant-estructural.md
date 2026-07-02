---
title: FK compuesta (tenant_id, id) = defensa multi-tenant estructural, no solo WHERE
date: 2026-07-02
source: claude-code-session
tags: [postgres, multi-tenant, fk, seguridad, schema]
---

En multi-tenant, un `WHERE tenant_id = $1` protege lecturas/updates pero NO impide **enlazar entre tenants**: una FK normal `child.parent_id → parent(id)` acepta un padre de otro tenant si el código olvida el guard.

**Patrón (defensa a nivel BD, no solo código):**
1. `CREATE UNIQUE INDEX parent_tenant_id_uidx ON parent (tenant_id, id);` (redundante con la PK pero habilita la FK compuesta).
2. En el hijo: `FOREIGN KEY (tenant_id, parent_id) REFERENCES parent (tenant_id, id)`.
→ Insertar un `parent_id` cuyo tenant no coincide es rechazado por la BD, imposible cruzar tenants aunque el código falle. Aplícalo también a tablas N-N (ambas FKs compuestas con tenant_id + PK compuesta anti-duplicado + `ON DELETE CASCADE` anti-huérfano).

La validación de dominio (error limpio "not found in tenant") vive en el executor; la FK es el backstop estructural. Verificado empíricamente: el INSERT cross-tenant lanza `foreign_key_violation`. RLS es ortogonal (esto no la sustituye). No cubre same-tenant-distinto-owner: eso es guard de código.

Caso real: AGH Ibérica #8 (oportunidad→cliente, oportunidad↔consultor N-N). Complementa [[columnas-regulatorias-requieren-guard-rol-trigger-no-solo-rls]].
