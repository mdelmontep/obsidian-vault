---
title: el nodo que envía el mensaje no debe escribir también la etapa del lead
date: 2026-09-08
source: clinica-zen
tags: [kommo, n8n, crm, diseño]
---
En el blueprint de chatbot los 10 nodos `salesbot*` mandan el texto con un PATCH que además lleva
`status_id` fijo a "Contestados". El nodo que decide la etapa de verdad (`Marcar Pendiente si
Reserva`) va al FINAL de la cadena, así que solo repara la etapa **en la ejecución en la que se
llamó a la tool**. Cualquier mensaje posterior del bot —una despedida, un "¿algo más?", el cron de
reenganche— devuelve el lead a Contestados y borra "Pendiente de asignar" o "Derivación Humana".

Peor con ejecuciones solapadas: el paciente escribe mientras corre la anterior y el run nuevo pisa
lo que el viejo acaba de poner. Medido: exec 13494 pone Pendiente a las 16:38:57, exec 13497 lo
devuelve a Contestados a las 16:39:05.

Regla: **la etapa la escribe UN solo nodo**, y ese nodo mira la etapa actual antes de pisar (lista
de etapas avanzadas intocables). El PATCH del mensaje manda texto y nada más.
Antes de culpar al salesbot de Kommo ([[kommo-salesbot-puede-mover-leads-de-estado-sin-n8n]]),
mira el `jsonBody` del nodo n8n: el estado suele ir hardcodeado ahí. Ver [[clinica-zen]]
