---
title: reabrir lo que se cerró solo vuelve a armar el cierre automático
date: 2026-09-05
source: facturaia
tags: [webhooks, idempotencia, soporte]
---
Un cliente recibió **dos** correos de «tu incidencia está resuelta». El cierre por merge es
idempotente y estaba bien escrito: corta con `ya_cerrado` y no envía. Lo que falló fue el
estado, no el guard.

Secuencia real: merge → cierre → correo 1 → **yo reabrí el ticket** → siguiente merge →
correo 2. Reabrir no manda nada por sí solo, pero **devuelve el registro al único estado en
el que el disparador vuelve a morder**.

- Un guard idempotente protege **mientras el estado no vuelva atrás**. Reabrir, restaurar
  un backup o un `UPDATE` de corrección son formas de rearmarlo.
- Antes de reabrir algo que tiene automatismos colgando, pregunta **qué se vuelve a armar**,
  no solo qué se desbloquea. Casi siempre no hace falta reabrir: el trabajo pendiente se
  sigue en el tracker y al interesado se le escribe por el hilo, no por la plantilla.
- El disparador aquí acepta también **prosa**, y no entiende de negaciones: un descargo del
  tipo «esto no cierra el ticket de feedback 171» lo cierra.

Ver [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]]
