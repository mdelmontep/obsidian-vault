---
title: varios canales de captación callados a la vez es demanda, no avería — compruébalo antes de buscar el bug
date: 2026-08-15
source: claude-code-session
tags: [diagnostico, agentes, elphis, multicanal]
---

**Caso real (Centro Elphis, 15-ago):** tres canales sin actividad — voz sin llamadas desde finales de julio, Doctoralia sin correos desde el 3-ago, WhatsApp sin mensajes desde el 11-ago. Cada uno se investigó por separado y en cada uno se gastó tiempo probando que el canal estaba sano: Graph API (número `CONNECTED`/`GREEN`, app suscrita al WABA), el sync captando un correo en 4 s con Clientify respondiendo 200, el webhook de Retell. **Los tres estaban bien.** Lo que fallaba era la pregunta.

**El patrón:** un canal callado es sospecha de avería; **varios canales independientes callados a la vez es casi siempre causa común aguas arriba** — estacionalidad, campañas paradas, un cambio en la web, la ficha de Google. Que sean tecnológicamente independientes (Meta, IMAP, Retell) es justo lo que descarta el fallo técnico: no comparten nada donde romperse a la vez.

**Regla:** antes de auditar un canal en silencio, mira **los demás canales del mismo cliente en la misma ventana**. Si callan todos, la primera pregunta es para el cliente (¿habéis parado publicidad? ¿ha cambiado algo en la web?), no para los logs. Y al revés: si uno calla y los otros no, ahí sí hay avería que buscar.

Corolario para el aviso: un check de efecto por canal no ve esto. La señal útil es **leads totales por semana**, no ejecuciones de un workflow.

Relacionado: [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] · [[agentes-cliente-tres-capas]]
