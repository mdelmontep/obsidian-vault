---
title: callback psd2 sin oauth (salt edge) que recibe un connection_id debe validar dueño antes de persistir
date: 2026-07-05
source: claude-code-session
tags: [seguridad, idor, multitenant, psd2, open-banking]
---

Tink/TrueLayer usan OAuth: el `access_token` del callback ya viene ligado al grant
del usuario, así que el recurso que trae está scoped por diseño. Salt Edge NO usa
OAuth — el redirect solo trae un `connection_id` (id de recurso, no secreto de un
solo uso) y el backend lo resuelve con credenciales **globales** de la app (`App-id`/
`Secret`), no con un token del usuario.

Si el callback no compara el `customer_id` que devuelve `GET /connections/{id}`
contra el `customer_id` esperado para la `orgId` que inició el flujo, un usuario de
la Org B puede sustituir el `connection_id` por uno de la Org A (adivinado o de una
conexión propia anterior) y el callback persiste cuentas/IBAN/movimientos ajenos
como si fueran suyos — fuga cross-tenant real, aunque el `state` del flujo sea
válido y propio.

Regla: en cualquier integración de recursos externos SIN OAuth (el id de recurso es
solo un id consultable, no un secreto scoped), el callback debe resolver el owner
esperado y comparar contra el owner real devuelto por el proveedor antes de
persistir. Extiende [[idor-detras-de-canal-hmac-validar-membresia-del-recurso]] al
caso "canal legítimo (state válido) + recurso ajeno".
