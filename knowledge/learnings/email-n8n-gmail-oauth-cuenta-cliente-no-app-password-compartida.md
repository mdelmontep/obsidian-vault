---
title: email de n8n por gmail oauth con la cuenta del cliente, no app password compartida
date: 2026-10-13
source: laserys-las-rozas
tags: [n8n, gmail, smtp, oauth, email, robustez]
---
SMTP de Google con contraseña de aplicación **compartida entre clientes** (`info@agentesia.madrid`) cayó en sept con `535-5.7.8 BadCredentials` en Simarro, Centro Elphis, Elphis Psicología y Laserys: Google revoca las app passwords al cambiar la contraseña de la cuenta, y una cuenta tumba a toda la flota a la vez.

Patrón (Laserys, 13-oct):
- Nodo **Gmail** (`gmailOAuth2`) con la cuenta **del propio cliente**, reutilizando el cliente OAuth de su proyecto GCP (el mismo que ya usan Calendar/Sheets). `senderName` + `replyTo` al buzón de la clínica.
- Cada nodo de email: `retryOnFail` (3×5 s) + `onError: continueErrorOutput`; la rama de error → Slack → **el mismo nodo siguiente**, para que Sheet/Kommo/respuesta al bot sigan ([[n8n-subworkflow-return-es-ultima-hoja-rama-paralela-contamina]]).
- Healthcheck diario: Gmail `getAll limit 1` → error → Slack con enlace a la credencial.

Gotchas: cambiar la contraseña también revoca el token OAuth con scope Gmail (no Calendar/Sheets) — por eso el healthcheck. `redirect_uri_mismatch` = el cliente OAuth tiene registrada la URL vieja de n8n (cambio de dominio): añadir `https://<n8n>/rest/oauth2-credential/callback`; la cuenta con la que entras no influye. Consent screen en «Prueba» = token caduca a 7 días.
