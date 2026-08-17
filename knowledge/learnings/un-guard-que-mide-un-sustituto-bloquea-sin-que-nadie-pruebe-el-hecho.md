---
title: un guard que mide un sustituto bloquea durante días sin que nadie pruebe el hecho
date: 2026-08-17
source: claude-code-session
tags: [gates, arnes, migraciones, metodo]
---

Un guard puesto **antes** de una operación para dar un mensaje bonito («¿eres miembro del
rol dueño?») mide un **sustituto**, no el hecho («¿puedo crear la política?»). Si el
sustituto se equivoca, la operación **nunca se intenta** y el error nunca aparece: no hay
nada que contradiga la suposición. Caso real: once días de épica parada
([[postgres-de-supabase-no-puede-el-grant-de-storage-pero-si-crear-sus-politicas]]).

Patrón correcto cuando la operación es transaccional: **quita el guard de entrada y
comprueba el RESULTADO al final** («¿existen las dos políticas?»). Si falla, la transacción
deshace todo igual — que es lo único que el guard defendía — y mides el hecho, no el permiso.

**Y el daño compuesto, que es lo caro:** si además hay una regla de inmutabilidad
(«una migración publicada no se reescribe»), una pieza bloqueada por un motivo **equivocado**
queda condenada: no se puede aplicar por lo que dice dentro, ni corregir lo que dice dentro.
Toda exención de inmutabilidad necesita una puerta para el commit que DESBLOQUEA — y sólo
para ése, o el marcador se vuelve llave maestra de reescritura.

Señal de que tienes uno: la prosa del gate declara un principio **más ancho** que su código.
Ahí el código gana y nadie lo nota, porque el comentario se cita como si fuera la regla.
