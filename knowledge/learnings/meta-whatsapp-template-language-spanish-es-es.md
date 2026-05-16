---
title: Plantillas WhatsApp "Spanish (SPA)" se aprueban como es_ES, no es
date: 2026-05-16
source: claude-code-session
tags: [whatsapp, meta-cloud-api, i18n, gotcha]
---

Meta Business Manager ofrece "Spanish (SPA)" al crear plantillas. Internamente queda como **`language: "es_ES"`** (Spain locale), no como `es` (Spanish genérico).

Si el payload de send pasa `language.code = "es"` y la plantilla está aprobada como `es_ES`, Meta devuelve `(#132001) Template name does not exist in the translation`. El sistema cae a fallback (email/SMS) y el OTP nunca llega por WhatsApp.

**Verificar siempre antes de codificar el send:**
```
GET /v21.0/{WABA_ID}/message_templates?name=<name>
→ devuelve el campo `language` literal exacto.
```

**Default razonable**: `es_ES` para España, override con env si añades otras locales (`es_MX`, `es_LA`). Aplica a cualquier proyecto WhatsApp Cloud API.

Relacionado: [[otp-onboarding-patterns]]
