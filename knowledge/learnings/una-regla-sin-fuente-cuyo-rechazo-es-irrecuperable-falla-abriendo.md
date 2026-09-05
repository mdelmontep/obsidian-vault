---
title: una regla sin fuente cuyo rechazo es irrecuperable falla abriendo
date: 2026-09-05
source: mandadm
tags: [seguridad, arquitectura, decisiones]
---

Habíamos puesto una ventana de frescura de 5 min al `signed_request` del callback de borrado de Meta.
Un tribunal de tres agentes la tumbó, y el argumento se generaliza. Antes de añadir una comprobación
defensiva, pásale las cuatro preguntas:

1. **¿La documenta la fuente?** Si no, la inventaste tú y el emisor no tiene por qué cumplirla.
2. **¿Es la autenticación?** Si la autenticación real es otra cosa (aquí, el HMAC en tiempo constante),
   esto no defiende de nada: quien puede falsificar la firma tiene el secreto, y con él pone la hora
   que quiera. Los campos de tiempo eran telemetría, no credencial.
3. **¿El rechazo es recuperable?** El 400 salía **antes** del insert, así que una solicitud de borrado
   rechazada por reloj no dejaba ni fila ni código de confirmación: el usuario no podía reintentar ni
   consultar nada. Un falso positivo aquí es pérdida de datos del usuario, no un reintento.
4. **¿El paso es idempotente?** Si dejar pasar dos veces no hace daño, no hace falta rechazar.

Sin fuente + no autentica + rechazo irrecuperable + paso idempotente ⇒ **falla abriendo**. Contra el
replay se protege con un `unique` sobre el hash de la firma aceptada, escrito en la misma transacción
que el efecto — no con el reloj.

Ver [[un-fail-closed-cuenta-la-fuente-que-puede-fallar-no-el-agregado]]
