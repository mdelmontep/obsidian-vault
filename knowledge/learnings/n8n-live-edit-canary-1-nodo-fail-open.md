---
title: editar workflow n8n vivo compartido — canary con 1 nodo code fail-open
date: 2026-06-28
source: claude-code-session
tags: [n8n, deploy, canary, prod]
---

Para tocar un workflow n8n en producción compartido por varios paths (voz/OCR/texto) sin romper a terceros:

1. **Backup del JSON primero** (GET → guardar). Rollback = re-PUT del backup.
2. Cambio mínimo = **1 nodo Code insertado en una arista**, "fail-open": ante cualquier error o si no es el target, `return $input.all()` (pass-through al comportamiento viejo). Así el blast radius queda acotado **aun en runtime**, no solo en estructura.
3. **Canary por identidad** (ej. `if normalized_phone !== TEST return $input.all()`): solo un usuario entra al camino nuevo.
4. **`node --check` del jsCode** envuelto en `(async function(){ ... })()` antes del PUT — un syntax error sí rompe a TODOS los que cruzan el nodo (el `node --check` directo falla por el `return`/`await` top-level; el wrapper lo arregla).
5. PUT con payload saneado: solo `name/nodes/connections/settings`, y `settings` sin props extra. Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]].

Caveat: el PUT por API a un workflow activo puede no recargar el trigger; si el comportamiento sigue siendo el viejo, reactivar ([[n8n-api-activate-es-POST-no-PATCH]]).
