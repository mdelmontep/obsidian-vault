---
title: reset multi-tenant — allowlist ordenada + to_regclass, no catálogo dinámico
date: 2026-07-02
source: claude-code-session
tags: [postgres, multi-tenant, seguridad]
---

Reset destructivo de un tenant (borrar sus datos operativos, conservar la instalación). Tentación: barrer por `information_schema` toda tabla con `tenant_id`. **Peligroso**: borra en silencio tablas de "instalación" nuevas (whitelist/roles) si olvidas excluirlas, e ignora el orden de FKs → ROLLBACK.

Mejor: **allowlist constante ordenada hijas→padres**, `DELETE FROM <tabla> WHERE tenant_id=$1` (nombre desde la allowlist, tenant siempre `$1` → sin inyección). Para cubrir tablas de PRs aún no mergeadas: `to_regclass('public.x')` skip-missing → forward-compatible sin editar.

Red de seguridad: **test-guard de completitud bidireccional** — toda tabla con `tenant_id` debe estar clasificada (operacional/install) o el CI falla; y toda operacional presente debe tener `tenant_id`. Así una tabla nueva obliga a decisión humana, no a borrado/olvido silencioso. Guard duro contra tenant vacío/null (nunca DELETE global). Ver [[fk-compuesta-tenant-id-defensa-multi-tenant-estructural]].
