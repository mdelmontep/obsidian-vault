---
title: el magic link de supabase ignora un redirect que no esté en su allowlist
date: 2026-08-03
source: claude-code-session
tags: [supabase, auth, smoke, testing]
---

Para abrir sesión en un dev local sin teclear la contraseña, `auth.admin.generateLink`
con `redirectTo: http://localhost:PUERTO/...` parece la vía limpia. No lo es si ese
origen no está en **Redirect URLs** del proyecto: Supabase **no falla**, redirige al
Site URL (producción) y consume el token ahí. Resultado: sesión abierta en el dominio
real y el dev local sigue en la pantalla de login, sin ningún error que lo explique.

Cómo se detecta: el servidor local no registra ninguna petición a su ruta de callback.
Si no hay callback en el log, el token no llegó.

Salidas, en este orden: pedir al usuario que inicie sesión él (20 segundos, cero riesgo),
o añadir el origen a la allowlist, que es **cambiar configuración de producción** y no se
hace sin permiso. Añadir `localhost` a la allowlist de un proyecto de producción tiene su
propio coste de seguridad: cualquiera con un token válido puede redirigirlo ahí.

Ver [[smokes-de-lo-que-ve-el-cliente-con-navegador]].
