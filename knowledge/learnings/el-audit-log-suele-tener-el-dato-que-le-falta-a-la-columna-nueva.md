---
title: el audit log suele tener el dato que le falta a la columna nueva
date: 2026-08-06
source: claude-code-session
tags: [migraciones, backfill, auditoria, postgres, facturaia]
---
Al añadir «quién cerró esto y cuándo» a una tabla, el reflejo es dejar el histórico a NULL
porque «ese dato no se guardaba». Casi nunca es cierto: si el endpoint escribía en un audit
log, el dato lleva meses ahí, solo que en JSONB y sin poder consultarse desde la app.

`feedback_tickets` no tenía fecha de cierre (mig 651) — `updated_at` no vale, lo pisa el
trigger en cada guardado —, pero `admin_audit_log` guardaba `action='feedback.ticket_update'`
con `actor_user_id` y `new_value->>'cierre'`. Un `distinct on (target_key) … order by
created_at desc` recuperó autor y fecha del cierre vigente de cada ticket.

- **Un `distinct on` bien ordenado resuelve el caso «se cerró, se reabrió, se recerró»**: vale
  el último evento, no el primero.
- **El FK muerde**: `actor_user_id` apunta a `auth.users` y la columna nueva a `profiles`. Un
  actor sin perfil tumba el UPDATE entero → resolverlo con subconsulta, no con join directo.
- **Rellena solo lo que puedas demostrar.** Lo demás se queda NULL y la UI lo dice («sin
  registrar»): inventar una categoría plausible para el 45 % de las filas contamina para
  siempre cualquier métrica que se saque después.
- Guarda de cordura: los eventos podados o anteriores a que el endpoint auditara no salen. Una
  cota (`updated_at`) para la fecha es aceptable; para la autoría, no.

Ver [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]] · [[facturaia]]
