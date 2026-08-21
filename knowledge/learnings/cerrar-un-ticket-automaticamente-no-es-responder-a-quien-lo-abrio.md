---
title: cerrar un ticket automáticamente no es responder a quien lo abrió
date: 2026-08-21
source: facturaia
tags: [soporte, automatizacion, producto]
---

Un trailer `Ticket-feedback: #N` en el PR que al mergear pone el ticket en `resuelto` y dispara el email de plantilla parece cerrar el círculo. No lo cierra: el hilo se queda **vacío**. El cliente ve "resuelto" y un correo genérico, sin saber qué se arregló ni qué le toca hacer a él.

Se ve en el dato: `feedback_ticket_messages` con **cero** filas nuevas el día en que tres tickets pasaron a `resuelto` por merge.

- El estado es lo barato de automatizar; la respuesta es lo que el usuario llama "me han contestado".
- Si el arreglo exige un gesto suyo (reintentar, volver a aprobar), sin mensaje ese gesto no ocurre nunca y el ticket vuelve.
- Regla: el cierre automático deja el ticket en una cola de **cerrado sin responder**, no en atendido.

Ver [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
