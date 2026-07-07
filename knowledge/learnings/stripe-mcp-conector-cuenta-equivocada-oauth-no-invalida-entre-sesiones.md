---
title: conector MCP de Stripe puede autenticar contra la cuenta equivocada, y desconectar en otra sesión no lo arregla
date: 2026-07-07
source: claude-code-session
tags: [stripe, mcp, claude-code, oauth, gotchas]
---

El conector MCP de Stripe hace OAuth contra la cuenta que esté activa en el
navegador en ese momento — si el login tiene varias cuentas Stripe (típico:
una del CLI, otra de producción), puede autenticar contra la incorrecta sin
avisar. `get_stripe_account_info` da `display_name` pero eso no basta para
confiar: verifica con un objeto real conocido, ej.
`fetch_stripe_resources('price_XXX')` de un price ID que SÍ existe en prod —
"No such price" = cuenta equivocada.

Gotcha adicional: **desconectar el conector desde OTRA sesión de Claude Code
no invalida la conexión OAuth de esta sesión** — cada sesión cachea su propio
token. Hay que desconectar y reautorizar dentro de la MISMA sesión que lo va
a usar, eligiendo la cuenta correcta en el selector de Stripe ANTES de
aceptar el consentimiento OAuth.

Para verificar el account_id real de una API key sin exponerla:
`curl https://api.stripe.com/v1/account -u "$(op read 'op://vault/item/campo')":`
— el `id` de la respuesta no es secreto, es seguro compartirlo/pegarlo.
