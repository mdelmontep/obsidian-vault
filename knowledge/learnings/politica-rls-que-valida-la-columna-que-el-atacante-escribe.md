---
title: una política RLS que valida la columna que el atacante escribe no valida nada
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, rls, multi-tenant, seguridad, idor]
---

Si el `WITH CHECK` de un INSERT comprueba `org_id = get_user_org_id()`, está validando
el valor que el propio atacante pone en la fila. Basta escribir su org de verdad y
apuntar la FK a un registro AJENO: la política pasa y el hijo queda colgando de un
padre de otro tenant.

Caso TuFacturaIA (mig 640 → 646): `factura_pagos` comprobaba `org_id` y el permiso de
escritura sobre ese mismo `org_id`, pero nada ataba `factura_id` a esa organización, y
su FK era simple. Reproducido en prod: fila con mi `org_id` + factura ajena → el trigger
recalcula ESA factura → «la factura ajena pasó de pendiente a cobrada». Escritura en el
estado de cobro de otro, que arrastra tesorería y reclamaciones.

- Fix estructural: **FK COMPUESTA** `(org_id, hijo_id) REFERENCES padre (org_id, id)`.
  Exige un `UNIQUE (org_id, id)` en el padre, redundante en cardinalidad con su PK y que
  existe solo para ser referenciable.
- **FK y no política**, porque `service_role` salta RLS y por ahí escribe toda la app: un
  bug propio pasando el `orgId` equivocado entra igual. La FK no la esquiva nadie.
- Señal para buscarlo: una tabla hija con `org_id` propio y varias FK; si alguna es
  simple, está sin atar. En el mismo repo `movimiento_factura_asignacion` sigue así.
- Verificar EJECUTANDO el ataque en `BEGIN … ROLLBACK` y exigiendo
  `foreign_key_violation`, en los dos sentidos: que antes se aceptaba y ahora no. Ver la
  constraint en el catálogo no prueba que proteja.

Complemento de [[clave-compuesta-por-tenant-elimina-el-guard-de-upsert-cross-tenant]] ·
[[defense-in-depth-estado-activo-cuando-admin-client-bypasa-rls]]
