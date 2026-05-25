---
title: triggers bd de sincronización son antipatrón
date: 2026-05-25
source: claude-code-session
tags: [sql, postgres, antipatterns, arquitectura]
---

Trigger que copia col↔col o col↔JSON dentro de la misma tabla = magia oculta. 6 razones para evitar:

1. **Fallo silencioso**: jsonb_set con valor raro lanza excepción → UPDATE entero falla, nadie sospecha del trigger.
2. **Race condition**: dos endpoints concurrentes tocan distintos campos del par sincronizado → pisan resultados.
3. **Recursión accidental**: trigger A escribe campo que dispara trigger B que vuelve a A → depth 16 → error críptico.
4. **Auditoría imposible**: audit_log dice "user cambió X" pero el trigger derivó Y. Forense roto.
5. **Code review ciego**: dev lee `UPDATE org SET nombre=X` y piensa "solo nombre" — trigger toca 5 campos invisibles.
6. **Migraciones masivas explotan**: UPDATE 1M filas dispara trigger 1M veces → statement_timeout.

OK: triggers append-only (audit log), `updated_at=now()`, guards de seguridad, lógica de negocio derivada (matching).
NO OK: espejo col↔JSON, copia entre columnas de la misma tabla, "mantener consistente".

Solución: sincronización **en código** (endpoint hace UPDATE explícito a ambos en una transacción cliente) o `GENERATED ALWAYS AS` para columnas derivadas, o eliminar duplicación.

Ver [[ADR-019-source-of-truth-datos-emisor]] · CLAUDE.md "Single source of truth, no triggers de sync".
