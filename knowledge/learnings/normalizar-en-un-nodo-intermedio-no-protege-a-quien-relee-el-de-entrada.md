---
title: normalizar en un nodo intermedio no protege a quien relee el nodo de entrada
date: 2026-09-10
source: ecobox
tags: [n8n, datos, anti-patron, auditoria]
---
En n8n cada nodo puede leer **cualquier** nodo anterior por nombre (`$('Edit Fields').item.json.x`),
así que un validador que normaliza a mitad del grafo **no gobierna** a los que se saltan su salida.

Caso real (EcoBox, `Reservar_cita`): `Validar horario` corregía `preferred_date` (offset de Madrid
mal puesto por el LLM) y `sede`, y aun así Google recibía el valor crudo — tres nodos rehacían el
item desde `Edit Fields` y otros cuatro leían ese nodo directamente. **El bug que motivó todo el
trabajo seguía vivo entero** en la creación del evento, con la puerta de validación en verde.

- El arreglo NO es parchear los siete consumidores: es normalizar en el **punto de entrada único**
  (el propio `Edit Fields` que sigue al Webhook). Un consumidor nuevo nace ya correcto.
- Cómo se detecta, y no es leyendo el flujo: `grep -o "\$('[^']*')" <workflow>.json | sort | uniq -c`.
  Si el nodo de entrada aparece más veces que las flechas que salen de él, hay lectores por detrás.
- Corolario: **la validación va delante del efecto**, no detrás. Aquí además colgaba de dos llamadas
  a Google, así que una fecha imposible costaba dos peticiones y salía como 400 con alerta a Slack.

Ver [[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]] · [[normalizar-dato-dictado-en-la-frontera-del-write-no-en-el-canal]]
