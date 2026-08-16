---
title: una membresía dada de baja sigue siendo una fila de `org_members`
date: 2026-08-16
source: claude-code-session
tags: [supabase, rls, multi-tenant, seguridad]
---

Retirar a alguien de una organización no borra su fila: la deja en `status='disabled'`. Así que
**cualquier consulta que use «pertenencia» sin filtrar `status` incluye a los ex-miembros**, y el
índice único que impide dos membresías activas suele estar escrito `where status <> 'disabled'` — o
sea que **dar de baja a alguien es justo lo que le permite entrar en otra organización** mientras su
fila sigue en la primera.

Dónde duele de verdad: una tabla que **no puede llevar `org_id`** (un intento de acceso fallido no
tiene organización probada) y que por eso se lee con `service_role`, saltando RLS. Ahí el aislamiento
no lo da ninguna columna: lo da **la lista de identificadores que construye el código**. En TuCRMIA,
`/ajustes/accesos` la armaba sin `status` y la organización A veía las entradas de una ex-miembro en
la B — hora, método, red /24, intentos fallidos y bloqueos.

La RLS no lo tapa por ti: la política de lectura de `org_members` devuelve la organización activa
ENTERA, `disabled` incluidas. Comprobar en la migración, no suponerlo — si las escondiera, el arreglo
sería inerte.

Y el test que lo vigila tiene que **contar filas**, no anotar que se llamó al filtro: el doble aplica
los `.eq()` que recibe sobre dos filas (una activa, una de baja) y resuelve el `or(...)` de PostgREST.
Con el control de que la activa se sigue viendo — devolver cero también pasa la primera prueba.
