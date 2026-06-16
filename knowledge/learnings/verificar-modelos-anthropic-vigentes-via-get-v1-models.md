---
title: verificar si un modelo anthropic sigue vigente con GET /v1/models
date: 2026-06-17
source: claude-code-session
tags: [anthropic, llm, smoke]
---
Para saber si un model-id concreto lo sirve la cuenta sin gastar crédito:
GET https://api.anthropic.com/v1/models?limit=100 (header x-api-key) → lista
ids vigentes. POST /v1/messages NO sirve para esto si la key no tiene saldo:
el error de billing precede a la validación de modelo, así que un model-id
retirado y uno válido devuelven el MISMO error de crédito (no concluyente).
Caso: bump SDK 0.104.2 destapó que claude-sonnet-4-20250514 (tier smart) ya
no se sirve → habría dado model_not_found en runtime. Fix: claude-sonnet-4-6.
Anthropic retira model-ids viejos periódicamente; tras subir el SDK, validar
los model-ids hardcodeados contra /v1/models.

Ver [[npm-audit-fix-force-propone-downgrades-trampa]]
