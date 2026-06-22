---
title: n8n $json tras nodo HTTP es la respuesta del HTTP, no el item original
date: 2026-05-21
source: claude-code-session
tags: [n8n, gotcha, http, expression]
---

En el nodo siguiente a un `httpRequest` (o cualquier node que transforme item), `$json` devuelve la respuesta de ese HTTP, NO el item que entró al flujo. Para acceder al item original hay que usar `$('NodeName').first().json.X` explícito.

Caso real 2026-05-21 TuFacturaIA bot: switch `Es Org Select?` colocado DESPUÉS de `Hash Session` (httpRequest a endpoint hash-session) leía `={{ $json.list_reply_id || '' }}` esperando el campo de `Parsear Mensaje`. Pero $json era la respuesta del endpoint (`{hash}`) → list_reply_id siempre undefined → regex contra '' → no match → la feature "cambiar org desde lista interactiva" JAMÁS disparaba en prod.

Auditoría 4-agentes pre-deploy lo detectó antes de smoke. Fix: `={{ $('Parsear Mensaje').first().json.list_reply_id || '' }}` explícito.

Regla: si un nodo intermedio reescribe el item (HTTP, Set, Code que retorna `{json: {...}}`), $json downstream YA es el output de ese nodo. Para campos del item original usa `$('NombreNodo').first().json.X`. Igual aplica al jsonBody de POST nodes que necesitan datos de un nodo anterior. Ver [[verificar-persistencia-tras-put-api-con-grep-marker-unico]] (verificar dat después de PUT n8n).

Caso real 2026-06-22 Elphis: se añadió nodo Postgres `Check deal abierto` entre `Upsert contacto` y `Crear deal`; el nodo `Crear deal` usaba `$json.contact_id` → recibía `{cnt:0}` del Postgres → `INVALID_INPUT: contact_id obligatorio`. Fix: `$('Upsert contacto').first().json.contact_id` explícito. Aplica a cualquier nodo (Postgres, HTTP, Code) insertado en medio de un flujo existente.
