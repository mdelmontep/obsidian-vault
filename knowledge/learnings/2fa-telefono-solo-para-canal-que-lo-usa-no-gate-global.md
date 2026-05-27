---
title: verificación de teléfono/2FA debe alcanzar solo a quien usa el canal, no ser gate global de login
date: 2026-05-27
source: claude-code-session
tags: [auth, onboarding, multi-tenant, facturaia]
---

Si la verificación de teléfono (OTP SMS/WhatsApp) existe para un canal concreto
(en FacturaIA: enlazar el número del TITULAR con el bot de WhatsApp), NO debe
aplicarse como gate de acceso a TODOS los usuarios con sesión. Hacerlo:

- Atrapa a los miembros invitados (contable/solo_lectura) que solo usan la web
  → bucle en /verificar-telefono y, si aún no aceptaron, callejón /sin-acceso.
- Cuesta dinero (cada OTP WhatsApp) por miembro.
- Es ajeno al estándar (Holded/Stripe/Xero: invitar→aceptar→contraseña; 2FA
  opcional/por-política, casi siempre TOTP, nunca gate por-miembro de login).

Correcto (diseño final): NINGÚN gate de teléfono en el login. La verificación es
on-demand, en el punto donde el canal se ACTIVA — en FacturaIA, conectar
WhatsApp en Canales: el bot solo resuelve números verificados, así que la
tarjeta muestra "Verificar mi número" si no lo está. El owner que no usa
WhatsApp no verifica nada; el que lo activa, verifica en ese momento. (1ª
iteración fue "gate solo-propietario" — descartada por seguir siendo fricción
innecesaria al entrar.) Caso 2026-05-27, incidente invitación.
Ver [[rls-org-members-select-debe-incluir-own-memberships]].
