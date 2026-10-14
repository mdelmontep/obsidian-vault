---
title: un post-call que solo registra leads hace invisibles los cuelgues
date: 2026-10-14
source: centro-elphis (retell-post-call-webhook McMHWTdHo7hgQL2d)
tags: [retell, voz, n8n, crm, post-call]
---
**Síntoma**: el cliente dice «una llamada no se registró» y «hoy no ha llegado nada». No hay ningún error: el webhook corre en verde en cada llamada.

**Causa**: el post-call solo registra lo que el extractor LLM da por lead (`es_lead`). Quien cuelga durante el saludo, o habla y se va sin dar datos, no deja nada: ni CRM ni aviso. En Elphis eran 5-8 llamadas al día de 10, y el cliente lo vive como «no funciona».

**Patrón**: toda llamada telefónica entrante deja rastro, aunque sea mínimo.
- Rótulos: «sin conversación» (≤6 palabras del usuario) o «sin datos» (habló pero no hay lead).
- Rastro: CRM en la etapa «volver a contactar» + email.
- Deduplicar por teléfono durante 15 min, porque quien cuelga suele rellamar enseguida.
- Número oculto: solo email.

**Gotcha**: las pruebas del panel de Retell (`call_type: web_call`, sin `from_number`) llegan al MISMO webhook. Filtra `call_type === 'phone_call'`, o cada prueba manda un email al cliente.

**Auditar en**: Clínica Zen, Laserys, Simarro, EcoBox, Tecnocloud. En cada uno, mirar qué hace su post-call con `es_lead=false`.

Ver [[clientes/centro-elphis/index|centro-elphis]].
