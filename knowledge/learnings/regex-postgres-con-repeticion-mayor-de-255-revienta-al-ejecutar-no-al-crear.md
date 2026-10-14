---
title: regex de postgres con repetición mayor de 255 revienta al ejecutar, no al crear
date: 2026-10-14
source: agency-portal
tags: [postgres, plpgsql, migraciones, regex, gotcha]
---

El motor de regex de Postgres limita las repeticiones `{m,n}` a 255 (`DUPMAX`). Un `'^[0-9a-v]{5,1024}$'`
dentro de una función plpgsql **se crea sin error** —el cuerpo no se compila hasta la primera llamada— y
falla en CADA ejecución con `invalid regular expression: invalid repetition count(s)`.

Caso real (14-oct-2026, agency-portal): `pizarra_calendar_event_create` (mig `20261014170000`) aplicada
y «verificada» en catálogo (ACL y cuerpo correctos) estaba muerta; solo lo destapó ejecutar el script
de vectores `BEGIN…ROLLBACK` contra prod. Fix en migración nueva (`…171000`): `!~ '^[0-9a-v]+$'` más
`char_length(x) between 5 and 1024`.

Patrón:
- Longitudes > 255: carácter con `+` y la longitud con `char_length`, nunca en la regex.
- Verificar una función en catálogo (`proacl`, `prosrc like`) no prueba que FUNCIONE: ejecutarla con
  vectores en una transacción revertida. Barrido: `select proname from pg_proc where prosrc ~ '\{[0-9]*,?[0-9]{3,}\}'`.
- Relacionado: [[plpgsql-array-mas-literal-sin-cast-se-resuelve-como-array]] (otro error que solo sale al ejecutar).
