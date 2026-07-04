---
title: meta whatsapp dev — usa el test number, no la app asociada al Business de prod
date: 2026-07-04
source: claude-code-session
tags: [meta, whatsapp, dev, seguridad]
---
Al crear una app de desarrollo Meta para un bucle rápido: si la asocias a un **Business que ya
tiene un WABA de producción**, el "Desde" de API Setup muestra el **número/WABA de PRODUCCIÓN**,
no un test number.

Peligro real: configurar el webhook de esa app + suscribir `messages` puede **secuestrar el
webhook del número de prod** → los mensajes reales se van a tu túnel local y el agente en vivo se
queda mudo (lo pillé a tiempo en AGH).

Regla: en API Setup selecciona el **"Número de prueba" que autocrea Meta** (+1…, aislado, hasta 5
recipients gratis) y usa SU `phone_number_id` + WABA; idealmente crea la app **bajo tu cuenta dev
sin Business** para forzar test number aislado. El destinatario de test necesita confirmar OTP.
Túnel al webhook: [[cloudflared-tunnel-bloqueado-puerto-7844-usar-hotspot]].
