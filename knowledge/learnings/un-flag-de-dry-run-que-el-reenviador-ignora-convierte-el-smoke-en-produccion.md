---
title: un dry_run que el reenviador ignora convierte cada smoke en producción
date: 2026-08-17
source: claude-code-session
tags: [n8n, smoke, dry-run, subworkflows, elphis, retell]
---
El smoke documentado de Elphis mandaba `dry_run:true` al webhook `retell/crear-lead`. El eslabón
intermedio (`Map for registrar-lead`) **construía el payload del sub-workflow con `dry_run:false`
literal**, así que la prueba creó contacto real en el CRM y **disparó el aviso de WhatsApp al
teléfono del cliente**. La nota del vault decía «forward automático de dry_run»: era verdad en otro
tool y falsa aquí.

- Un flag de seguridad viaja por una cadena de sub-workflows y **basta un eslabón que lo reescriba**
  para que deje de existir, sin error ni aviso.
- En n8n se agrava: el trigger filtra los campos no declarados en `workflowInputs`, así que un flag
  nuevo puede desaparecer sin que nadie lo note ([[n8n-executeworkflowtrigger-schema-estricto-filtra-campos]]).
- **Verifica el flag en el destino, no en el origen**: la señal buena es un efecto imposible en real
  (`contact_id: "wl-+34…"`, `notified:false`), no un HTTP 200. Si el smoke devuelve un id real, no
  era un smoke.
- Y antes de la primera corrida, apunta el destinatario de los avisos a tu propio número: el modo
  seguro se comprueba DESPUÉS de haber gastado el primer envío.

Hermanos: [[el-utillaje-de-pruebas-se-queda-encendido-en-produccion]] · [[un-guard-que-mide-un-sustituto-bloquea-sin-que-nadie-pruebe-el-hecho]]
