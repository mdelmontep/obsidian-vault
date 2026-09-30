---
title: un campo que rellena un solo camino de alta sale vacío en los demás
date: 2026-09-30
source: simarro (n8n iMoTKZWxYLymGuHF + Calendario_a_Kommo)
tags: [n8n, kommo, crm, auditoria, patron]
---
Cuando una entidad (lead, cita, cliente) se crea por varios caminos (agenda manual, bot de voz, chatbot, formulario), un campo añadido para arreglar un camino no llega a los otros. El síntoma aparece como un caso suelto («¿por qué esta no tiene agente?»), no como un bug de un camino entero.

Caso real: «Agente asignado» (CF 1373105) de Simarro solo lo escribía `Calendario_a_Kommo`. Las reservas de voz y WhatsApp (`iMoT`) enrutaban bien la cita a la agenda del agente, pero el lead salía sin agente, y `Calendario_a_Kommo` se saltaba el evento porque ya venía marcado.

Método: bajar todos los workflows activos y cruzar dos greps, uno por el id del campo (quién lo escribe) y otro por los endpoints de alta (`/leads`, `leads/complex`, nodo Kommo create). Cada camino que crea la entidad y no escribe el campo es un hueco.

Probar sin efectos una expresión que referencia `$('Nodo')`: workflow temporal con nodos Code mock con el MISMO nombre, el nodo de lectura real y un Set que evalúa la expresión. Después, borrarlo. Ver [[workflow-temporal-webhook-para-operaciones-bulk-calendar]] · [[gate-en-wrapper-web-no-cubre-canales-con-otro-auth]]
