---
title: publicar un agente de voz no basta, el número puede tener fijada su versión
date: 2026-08-20
source: tecnocloud
tags: [retell, voz, agentes, despliegue, produccion]
---

`POST /publish-agent/{id}` sella el draft, pero **un número de teléfono puede apuntar a un
`agent_version` concreto**: entonces publicar no cambia nada y el fix nunca llega a una llamada.
Se ve como «el modelo ignora el prompt», y se depura durante horas el prompt equivocado.

Comprobación (2 s) antes de dar por bueno cualquier cambio de prompt:
`GET /list-phone-numbers` → el número debe mostrar `agent_version: "latest_published"`, no un entero.
Y la prueba definitiva está en la llamada: `list-calls` devuelve el `agent_version` que corrió.

Arreglo: `PATCH /update-phone-number/{numero}` con
`{"inbound_agents":[{"agent_id":"…","agent_version":"latest_published","weight":1}]}`.
Ojo: `inbound_agent_id`/`inbound_agent_version` están deprecados y se rechazan, y `agent_version:
null` lo rechaza el schema aunque los números existentes lo muestren así.

Medido el 18-ago en 3 clientes a la vez: Tecnocloud servía v40 con v43 publicada (un día de trabajo
sin llegar a nadie), Clínica Zen v54 con v67 — la causa real de un «fix que no funcionaba» que
llevaba 15 días abierto — y Laserys v6 con v14. Tras publicar, `get-agent` sin `?version` devuelve el
draft NUEVO con `is_published:false`: eso es normal, mira la versión publicada más alta.
