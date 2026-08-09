---
title: un límite delante de tu acción no protege si la operación de debajo es pública
date: 2026-08-09
source: claude-code-session
tags: [seguridad, supabase, ratelimit]
---

Contador antifuerza bruta impecable —10 intentos/15 min, HMAC del correo, almacén durable en
Postgres, cierra si no puede contar— y **no protegía de nadie**: estaba delante de nuestra acción
de servidor, y `signInWithPassword` es la operación pública `POST /auth/v1/token` de GoTrue,
alcanzable con la clave anónima que viaja al navegador.

Medido: 40 intentos → 14 rechazos y 26 limitaciones, y las 26 eran el límite **por IP de Supabase**.
Nuestro contador no contó ni uno.

No es «la pieza no está enchufada». Es peor: **enchufada donde el atacante no pasa**, con un
comentario prometiendo lo contrario.

**Antes de escribir un control, pregunta por dónde entra el atacante.** Si la operación protegida
la expone el proveedor, el control tiene que vivir en el proveedor: hook (`hook_password_verification_attempt`,
solo Teams), captcha (`security_captcha_enabled`, cualquier plan) o su límite por IP. Ver
[[una-afirmacion-repetida-no-es-una-verificacion]].
