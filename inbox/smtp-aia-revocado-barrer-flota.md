---
title: barrer la flota buscando credenciales SMTP con la app password de info@agentesia.madrid
date: 2026-10-13
source: laserys-las-rozas
tags: [n8n, smtp, email, flota]
---
La app password de `info@agentesia.madrid` está revocada (Elphis 14/18-sep, Laserys 13-oct). Cualquier credencial `smtp` de otro cliente que aún la use no envía nada. Buscar por instancia n8n las creds `smtp` en uso y migrar al patrón [[email-n8n-gmail-oauth-cuenta-cliente-no-app-password-compartida]]. Aparcado por el usuario el 13-oct («de momento se queda así»).
