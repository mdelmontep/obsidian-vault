---
title: verificar una clave de firma en prod ejercitando el flujo, no el health
date: 2026-08-01
source: claude-code-session
tags: [verificacion, prod, oauth, hmac, smoke, secretos]
---
Tras poner una env de firma nueva (`OAUTH_STATE_SIGNING_KEY`, `BANK_PSD2_STATE_KEY`) y
desplegar, `/api/health = ok` NO prueba que la clave funcione: esos helpers (`getKey()`,
`signState()`) lanzan al INVOCARSE, no al bootear. Health verde solo dice que el proceso
arrancó.

Verifícalo ejercitando el flujo exacto que la usa, con una sesión real contra prod:
- POST al endpoint que FIRMA (los `/connect` de integraciones y banca). **200 con la URL
  de redirect firmada = la clave se leyó y firmó; 500 = falta o es demasiado corta.** Es
  la diferencia entre "confirmado" y "supuesto".
- Párate antes de autorizar nada en el proveedor: generar la URL firmada ya ejercita la
  clave; no hace falta completar el OAuth.

Cuidado con el residuo: el connect de banca (Tink/TrueLayer) CREA un `bank_consents`
`pending` por llamada. Es escritura, aunque parezca solo lectura. Bórralo después por id
exacto y `org_id` explícito de la sandbox. Caso real: FacturaIA, verificación de #1429.
