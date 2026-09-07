---
title: un guard que enumera motivos de fallo deja pasar los motivos que no enumera
date: 2026-09-07
source: simarro
tags: [validacion, fail-closed, n8n]
---
La última verificación antes de reservar preguntaba `motivo === 'slot_ocupado'`. La
función de disponibilidad devolvía además `fin_de_semana`, `fuera_horario`, `pasado`
y `sin_fecha`, y los cuatro caían por la rama que **sí reserva**: se agendaban visitas
en sábado y en fechas pasadas, y el cliente colgaba con una cita que nadie iba a
atender.

El guard debe preguntar por el **éxito explícito**, no por la lista de fracasos
conocidos: `libre !== true` bloquea también la respuesta inesperada, el timeout y el
motivo que alguien añada mañana. Enumerar fallos convierte cada motivo nuevo en un
agujero silencioso, y el que lo añade no sabe que existe este `if`.

Antes de invertirlo, comprobar en ejecuciones reales **dónde vive el campo** (raíz vs.
anidado): un fail-closed sobre un campo que nunca llega bloquea el 100 %.
