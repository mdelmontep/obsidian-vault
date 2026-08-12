---
title: el utillaje de pruebas se queda encendido en producción — inventaría los webhooks activos
date: 2026-08-12
source: claude-code-session
tags: [seguridad, n8n, go-live, elphis]
---
Auditando Elphis (en producción con pacientes desde julio) aparecieron cuatro webhooks vivos
de la fase de pruebas de mayo. El peor, `purge-idem`: **dos nodos, webhook POST sin ninguna
validación → `TRUNCATE TABLE idempotency_log; TRUNCATE TABLE slot_lock;`**. Un POST anónimo a
esa URL se lleva por delante el dedup de avisos, el guard anti-doble-deal de 30 días y los
locks de conversación. Los otros tres (dos test-runners y una tool de Retell retirada en
junio) sí pedían token; a este se le olvidó, y nadie lo notó porque **nunca se ejecutó**: cero
ejecuciones es justo lo que lo hacía invisible.

Su propia documentación decía «desactivar antes del go-live». El go-live fue en julio.

Antes de dar por vivo un despliegue, listar los workflows **activos con trigger de webhook** y
justificar uno a uno por qué siguen encendidos:
```sql
select w.name, x->'parameters'->>'path', coalesce(x->'parameters'->>'authentication','NINGUNA')
from workflow_entity w, jsonb_array_elements(w.nodes::jsonb) x
where w.active and x->>'type'='n8n-nodes-base.webhook';
```
Ojo: ese campo `authentication` **no** basta — varios validan el token en un Code node
posterior. Mirar los nodos, no solo la columna. Y purgar es `DELETE ... WHERE expires_at <
NOW()` con schedule, nunca un `TRUNCATE` colgado de una URL.
