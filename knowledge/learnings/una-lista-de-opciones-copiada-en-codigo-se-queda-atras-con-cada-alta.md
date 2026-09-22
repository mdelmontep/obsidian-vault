---
title: una lista de opciones copiada en código se queda atrás con cada alta del cliente
date: 2026-09-22
source: simarro
tags: [kommo, n8n, crm, integraciones]
---
Simarro dio de alta a una agente (Claudia). Su agenda entró sola en la tabla `agents`, pero sus leads
salían con «Agente asignado» vacío. El recordatorio decía «Tu agente:» sin nombre, y nada falló ni avisó.

Había dos copias de la lista de agentes a mano: las opciones del campo select de Kommo y un
`AGENTE_ENUM` fijo en el Code node. Un Code node que no encuentra la clave escribe `null` sin quejarse.

Patrón:
- El código lee las opciones del CRM en cada ejecución (`GET custom_fields/{id}`, `executeOnce`).
  No se copian en el código.
- El sync que ya mantiene la fuente de verdad (`agents`) añade en el CRM las opciones que faltan.
  Solo añade, nunca borra ni renombra. Reenvía la lista entera con sus ids, porque el PATCH la reemplaza.
  Si la lectura falla, no escribe. Todo cambio avisa a Slack.
- Se empareja por nombre con la misma regla que el resto del sistema (todas las palabras de la clave).

Dónde buscarlo en otros clientes: cualquier `const X = { 'nombre': id }` en un Code node. Por ejemplo,
doctores en Clínica Zen o agentes en Kommo.
