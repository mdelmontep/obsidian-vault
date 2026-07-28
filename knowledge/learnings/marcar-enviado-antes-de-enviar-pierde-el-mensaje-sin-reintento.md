---
title: marcar "enviado" antes de enviar pierde el mensaje sin reintento ni rastro
date: 2026-07-28
source: claude-code-session
tags: [n8n, dedup, recordatorios, clinica-zen, idempotencia]
---
Un deduplicador que escribe la marca de "ya enviado" ANTES de la llamada de envío
convierte cualquier fallo del envío en pérdida definitiva y silenciosa: el siguiente
barrido ve la clave y salta. No hay error visible para nadie — el sistema cree que lo mandó.

Caso real (Clínica Zen, `PJBMjLLE0vNJjZH8`): `staticData.enviados[clave] = now` se ejecuta
dentro del Code de filtrado, y el `salesbot/run` que envía el WhatsApp va 2 nodos después.
El 400 de Kommo del 28-jul dejó a un paciente sin su recordatorio, con la clave marcada.

Patrón: marcar DESPUÉS del envío OK, en el nodo posterior al emisor (o con `onError` que
borre la clave). Si el dedup vive en `$getWorkflowStaticData` no hay transacción — el orden
de escritura ES la única garantía. Vale para cualquier scanner periódico con memoria propia.
Ver [[webhook-idempotency-borrar-log-en-errores-transitorios]] · [[clinica-zen]]
