---
title: una política RLS de insert atada a "visibilidad own" rechaza en silencio si no fijas owner_id
date: 2026-08-05
source: claude-code-session — TuCRMIA, crearLead()
tags: [rls, supabase, postgres, multi-tenant, gotcha]
---

Patrón: `org_members.record_visibility` por defecto `'own'`, y la política de `insert`
exige `owner_id = auth.uid() OR visibilidad IN ('org','team')`. Si la función que crea
la fila no fija `owner_id` explícitamente (queda `NULL`), la condición es falsa para
CUALQUIER miembro nuevo — el insert se rechaza, y `mapearErrorDeEscritura` (o similar)
lo traduce a un mensaje genérico «no se pudo guardar», indistinguible de cualquier
otro fallo. No hay excepción ruidosa: PostgREST devuelve un error de política normal.

Detectado solo probando el flujo end-to-end en el navegador con un usuario real recién
dado de alta — ningún test unitario lo cazaba porque las pruebas usaban `service_role`
o pasaban `ownerId` a mano.

**Fix / regla**: cualquier función de creación bajo una política de visibilidad `own`
tiene que fijar `owner_id` (o el campo equivalente) al usuario que escribe por defecto,
nunca dejarlo implícito. Al construir el `insert` de una entidad nueva bajo RLS,
preguntar explícitamente: "¿qué visibilidad tiene el rol que va a crear esto, y contra
qué columna la compara la política?" — no asumir que la política solo protege lecturas.
