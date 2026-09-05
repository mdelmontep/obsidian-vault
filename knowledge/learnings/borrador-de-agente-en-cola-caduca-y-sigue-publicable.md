---
title: un borrador de agente que espera en cola caduca, y sigue a un clic de publicarse
date: 2026-07-31
source: TuFacturaIA — ticket de soporte #115
tags: [agentes, hitl, soporte, gotcha]
---

Un borrador redactado por un agente (resumen al cliente, respuesta de soporte,
descripción de PR) es una foto del estado del sistema **en el momento en que se
escribió**. Si el trabajo avanza mientras el borrador espera revisión, el
borrador no se invalida solo: sigue ahí, con su botón de publicar.

Caso real: el runner analizó el ticket #115 ("faltan los textos tipo en
facturas") y dejó un borrador explicando **por qué no se podía hacer**, con dos
opciones para que el cliente eligiera. Horas después, cuatro PRs construyeron
exactamente esa función. Al cerrar el ticket el borrador seguía en el panel: un
clic y el cliente recibía una negativa sobre algo ya entregado. Nadie lo había
tocado; simplemente nada lo caducó.

Reglas: (1) leer el borrador **antes** de publicarlo, no darlo por bueno porque
lo generó el mismo sistema; (2) al cerrar el asunto, limpiar los borradores
pendientes en la misma tanda que la respuesta — en TuFacturaIA,
`feedback_ai_jobs.resumen_cliente = null` deja el resto de la traza intacta;
(3) si el ciclo es habitual, el estado del job debería caducar el borrador solo
(un `resumen_caducado_at` al mergear un PR del mismo ticket).

**Ampliado el 5-sep-2026 (ticket de soporte 171): también caduca el borrador que
escribe un humano-agente, y la señal de que caducó suele ser que el cliente escribió
mientras tanto.** El borrador de respuesta presentaba como hallazgo nuestro justo lo
que el cliente había descrito por su cuenta esa mañana. Publicar eso no es un error
de dato: es contarle su propio informe como si fuera nuestro. Regla: **releer el hilo
justo antes de enviar** —no cuando se escribió el borrador— y, si el cliente ha
hablado, reescribir la apertura para contestarle, no para anunciarle.
