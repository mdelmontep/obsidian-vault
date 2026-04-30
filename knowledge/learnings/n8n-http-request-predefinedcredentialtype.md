---
title: n8n http request soporta predefinedcredentialtype para reutilizar credenciales sin hardcodear token
date: 2026-04-30
source: claude-code-session
tags: [n8n, kommo, credenciales]
---

Los nodos HTTP Request de n8n permiten usar credenciales almacenadas sin hardcodear el Bearer token:

- `authentication: "predefinedCredentialType"`
- `nodeCredentialType: "kommoLongLivedApi"` (o el tipo que corresponda)
- `credentials: { "kommoLongLivedApi": { "id": "CRED_ID", "name": "Nombre" } }`

Verificado en Simarro con credential `xPvEqRp6NQwORUXi` haciendo PATCH a `/api/v4/leads` y POST a `/api/v2/salesbot/run`. Respuestas correctas, sin 401.

Alternativa (patrón CZ): hardcodear Bearer en header `Authorization`. Funciona pero ata el workflow a un token concreto.
