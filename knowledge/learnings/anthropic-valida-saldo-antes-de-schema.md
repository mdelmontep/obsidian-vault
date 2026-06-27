---
title: la API de Anthropic valida saldo antes que el schema — no sirve para smoke-testear tool-schemas sin crédito
date: 2026-06-27
source: claude-code-session
tags: [anthropic, llm, tool-use, testing]
---

`messages.create` con `tools` devuelve `400 invalid_request_error "credit balance is too
low"` ANTES de validar el `input_schema` de las tools. Si la cuenta/key no tiene crédito,
no puedes distinguir "schema malformado" de "sin saldo" — el smoke contra API real no
informa nada del schema.

Fix: valida el tool-schema OFFLINE contra el contrato documentado (root `type:'object'`,
`properties` objeto, `required ⊆ keys(properties)`, serializable sin ciclos, sin `$schema`).
Reserva la llamada real para cuando haya crédito. Caso: smoke de FacturaIA Fase 0 bloqueado
por saldo en la key de dev. Ver [[zod-v4-tojsonschema-nativo-deriva-tool-schema]].
