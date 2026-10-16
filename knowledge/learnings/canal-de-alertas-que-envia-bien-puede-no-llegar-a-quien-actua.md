---
title: un canal de alertas que envía bien puede no llegarle a quien tiene que actuar
date: 2026-10-17
source: agency-portal (sonda portal-db-probe, grupo Telegram de alertas)
tags: [alertas, telegram, monitorizacion]
---
- Instalada la sonda del portal, la prueba de fallo dio `ec=1` y Telegram confirmó el envío, pero Manuel no lo recibió. `TELEGRAM_ALERT_CHAT_ID` apuntaba a un grupo («Alertas infra AIA») creado por otra persona, con 2 miembros (bot + creador). Las alertas de seguridad y las de `readFailed` van al mismo grupo.
- «Enviado» ≠ «leído por quien actúa». Dar un canal por bueno exige que el DUEÑO vea llegar la prueba en su móvil, no solo que la API devuelva `ok`.
- Diagnóstico sin imprimir secretos: dentro del contenedor, `node` con `getMe` + `getChat` + `getChatMemberCount` + `getChatAdministrators`, con el token leído de `process.env`. Saca el nombre del bot, el tipo y nombre del chat, los miembros y el creador.
- Si el bot no es admin, `createChatInviteLink` falla con «not enough rights»: solo el creador puede meter a alguien.
- Relacionado: [[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]].
