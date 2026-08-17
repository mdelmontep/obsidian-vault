---
title: un trigger diferido no dispara dentro de BEGIN…ROLLBACK, así que el arnés da verde midiendo cero
date: 2026-08-17
source: TuFacturaIA — mig 704, candado de feature_dependencies
tags: [postgres, testing, triggers, verificacion, supabase]
---

Un `CONSTRAINT TRIGGER … DEFERRABLE INITIALLY DEFERRED` se evalúa **en el COMMIT**, no en el
statement. El patrón normal de arnés SQL —`BEGIN; <escritura que debe fallar>; ROLLBACK;`— **nunca
llega al COMMIT**, así que el trigger no corre y todos los casos que «deben fallar» pasan callados.
Verde perfecto, cero medido.

Se cierra forzando la comprobación tras cada escritura:

```sql
SET CONSTRAINTS <nombre_del_trigger> IMMEDIATE;
```

dentro de un sub-bloque `BEGIN … EXCEPTION WHEN OTHERS`, cuyo savepoint implícito deshace también el
`SET CONSTRAINTS` y devuelve el modo a DEFERRED para el caso siguiente.

Y elige el diferido a conciencia: hace falta cuando un seed activa varias filas relacionadas en un
statement (un trigger inmediato revienta en un estado intermedio que al final es consistente), pero
cambia dónde aparece el error para todo el que escriba — llega con `errcode 23514` al cerrar la
transacción, no en la línea que lo causó. Dilo en el `gotchas` del proyecto.

Comprobación de que el arnés discrimina: mutar el trigger por partes y exigir rojo en el caso
correspondiente y solo en ése. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
