---
title: Patrones OTP teléfono onboarding (TuFacturaIA 2026-05-16)
date: 2026-05-16
source: facturaia/docs/manuals/manual-admin.md §26
tags: [otp, whatsapp, meta-cloud-api, onboarding, security, facturaia]
---

# Patrones OTP teléfono onboarding

- **Plantilla Meta AUTHENTICATION obligatoria** desde julio 2023 para entrega de OTPs. Meta rechaza UTILITY con códigos `132001` / `131008`. La categoría se elige al crear y no se puede cambiar (toca recrear plantilla).
- **Language code exacto: `es_ES` no `es`** para plantillas "Spanish (SPA)" — error 132001 si no coincide. Ver [[meta-whatsapp-template-language-spanish-es-es]].
- **Body fijo generado por Meta** en plantillas AUTHENTICATION. Solo se admite `{{1}}` (el código) + `code_expiration_minutes` + botón `OTP COPY_CODE`. Cualquier intento de body personalizado se rechaza en review.
- **Fallback text mode NO sirve para onboarding**: la ventana de 24h de Meta exige que el usuario haya escrito primero al bot; en signup el usuario nunca ha contactado, así que solo plantillas funcionan. Falla con `131047` si se intenta.
- **Pepper en `system_config` cifrado > variables de entorno**: permite rotación sin redeploy. Eliminar OTPs vivos (`DELETE FROM phone_verifications`) tras rotar invalida solicitudes en curso pero no afecta a usuarios ya verificados.
- **`withApiAuth` debe chequear `phone_verified_at` (defensa profunda)**: el middleware Next.js puede ser saltado con un fetch directo a `/api/*`. La guardia en `withApiAuth` con allowlist `OTP_BYPASS_ENDPOINTS` cierra el agujero.
- **Hard-cap mensual con kill-switch**: defensa contra DoS económico — un atacante con bot puede pedir miles de OTPs si no hay cap. Default 30 €/mes editable desde admin con notif al 80 %.
- **Webhook delivery Meta tiene dos tipos `messages` + `statuses`** en el mismo endpoint. El receptor v2 debe rutar `statuses[0]` a un branch separado que reporta al backend, o se pierden los KPIs de delivery y la detección de plantilla pausada (`130472`).
- **Grandfathering D+N con constante de código** (no env var): permite ajustar el deadline con un commit pequeño y revertir fácil. Pre-deadline solo banners UI, post-deadline guardias backend devuelven 403.
- **Cambio de teléfono post-verificado requiere re-auth password**: regla universal "config global o acciones multi-org requieren re-auth" aplicada también al teléfono porque controla la identidad fiscal del usuario.
