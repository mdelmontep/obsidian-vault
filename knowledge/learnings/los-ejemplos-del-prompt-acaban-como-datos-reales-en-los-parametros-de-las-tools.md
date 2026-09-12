---
title: los ejemplos del prompt acaban como datos reales en los parámetros de las tools
date: 2026-09-12
source: simarro
tags: [llm, agentes, n8n, tools, prompting]
---
Un parámetro de tool resuelto por el modelo (`$fromAI` en n8n, function calling en general) se
rellena con **lo que el modelo tenga a mano**, y lo que tiene a mano es el ejemplo literal que le
pusiste en la descripción. Caso real 12-sep-2026 (Simarro): la descripción decía
`por ejemplo "+34 645 452 253"` y el agente mandó ese teléfono como el del cliente — cuyo número
real estaba en el CRM, a un GET de distancia. Igual con el email de contacto de la empresa, que
viajaba en el system prompt y salió como email del cliente.

No es un fallo de obediencia: el modelo no puede distinguir un hueco vacío de un hueco con ejemplo.
- Dato que ya existe en un sistema → **no lo resuelva el modelo**: léelo antes de invocar y mapea el
  parámetro a esa lectura (`$('Contexto lead').first().json.telefono`).
- En las descripciones, **formato sin valor** ("E.164, `+34` y 9 dígitos"), nunca un ejemplo rellenable.
- Lo que el modelo ya tiene, dáselo en el input y dilo: "no lo preguntes, no lo inventes" — así
  además deja de pedirle al cliente datos que el CRM ya tiene.
Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]]
