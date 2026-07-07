---
title: anti-eco en sync bidireccional — hash canónico sobre forma mapeada, no sobre el raw
date: 2026-07-07
source: claude-code-session
tags: [integraciones, sync, arquitectura, holded]
---

En una integración bidireccional (push+pull) hay que cortar el bucle de eco: lo que el pull escribe local dispara el trigger de push, que lo devolvería al origen.

Patrón que funciona:
1. **Hash canónico sobre la MISMA forma mapeada** en ambos lados. push computa `hash(mapToExternal(local))`; pull, al recibir un registro externo, computa `hash(mapToExternal(mapToLocal(remote)))`. Guardas ese hash en la tabla de mapeo. El push worker SALTA si `hash(entidad local) == map.content_hash`. Clave: hashear la representación normalizada, NO el objeto crudo (el remoto trae campos extra que rompen la igualdad).
2. Solo funciona si el round-trip `local→external→local` es idempotente en los campos mapeados (testéalo con round-trip test).
3. **Cuando las representaciones NO convergen** (p.ej. doc externo con líneas vs entidad local con importes agregados), el hash no casa nunca → el eco se cuela una vez. Fix robusto ahí: tras el upsert del pull, **borrar la fila de cola de push auto-encolada** por el trigger para esa entidad (si el usuario edita luego, el trigger la re-encola = cambio legítimo).

Conflictos: last-write-wins por `updated_at`; empate/duda → gana el sistema autoritativo (el tuyo).
