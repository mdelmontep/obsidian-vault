---
title: tabla limbo (bandeja) + tabla real con FK RESTRICT — borrar de un lado debe sincronizar el otro
date: 2026-05-28
source: claude-code-session
tags: [arquitectura, bd, fk, ux]
---

Patrón: tabla "staging/inbox" (bandeja_ingesta) crea fila en tabla "real" (facturas) y guarda FK con RESTRICT. El usuario ve cada una en UI distinta. Si el borrado solo opera sobre una, queda huérfano del otro lado.

Síntomas: borrar en UI A → fila en B sigue visible en estado limbo; borrar en UI B → fila en A queda apuntando a NULL; blob de Storage acumulado.

Fix: endpoint server-side único por dirección (NO trigger BD de sync — anti-patrón). Orden: nullify FK → DELETE hijo → DELETE padre → DELETE blob (best-effort, requiere service_role si bucket no tiene policy DELETE para `authenticated`). Si el destino está "activo" (estado integrado a contabilidad/conciliación), conservar y devolver flag para toast UX en lugar de borrar a ciegas.

Sniff antes de codear: ¿hay `entidad_id` apuntando a otra tabla visible en UI distinta? Mapear las 2 puertas de borrado o re-aparece el huérfano. Caso real TuFacturaIA 2026-05-28: bandeja_ingesta↔facturas, commit `7ace1dc`.

[[campo-sincronizado-entre-tablas-debe-poblarse-en-todos-los-puntos-de-escritura]] · [[triggers-bd-sync-son-antipatron]] · [[n8n-502-deja-items-huerfanos-en-bandeja-sin-retry]]
