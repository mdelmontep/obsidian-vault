---
title: los scopes restringidos de gmail exigen evaluación de seguridad anual si almacenas los datos
date: 2026-08-09
source: claude-code-session
tags: [google, oauth, email, integraciones]
---
Para leer correo con la API de Gmail hace falta un scope **restringido** (`gmail.modify` / `gmail.readonly`),
y la documentación de Google es explícita: *«If you store restricted scope data on servers (or transmit),
then you must go through a security assessment»*. Cualquier producto que sincronice buzones los almacena
por definición, así que **siempre aplica**: es auditoría por un tercero y es recurrente, no un formulario.

Consecuencia práctica al planificar un canal de correo: **IMAP/SMTP primero**, que funciona hoy sin
verificación de nadie, y OAuth cuando haya un cliente que pague la auditoría.

Aviso que descoloca el plan si se descubre tarde: **en Microsoft 365 el IMAP con autenticación básica ya
no existe**, así que allí la salida equivalente es un buzón de reenvío, no IMAP.
