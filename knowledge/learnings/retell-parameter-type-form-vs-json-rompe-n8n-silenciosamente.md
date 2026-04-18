---
title: retell parameter_type form vs json rompe n8n silenciosamente
date: 2026-04-18
source: claude-code-session
tags: [retell, n8n, webhooks]
---

Si una custom tool de Retell usa `parameter_type: "form"` pero el workflow de n8n espera `$json.body.args.X` (JSON anidado), n8n recibe `body['args[name]']` en vez de `body.args.name`. La reserva o consulta falla sin error visible — n8n simplemente no encuentra el campo y lo deja vacío.

Regla: siempre usar `"json"` cuando n8n lee `body.args.*`. Solo usar `"form"` si el webhook destino espera `application/x-www-form-urlencoded` explícitamente.

Descubierto auditando el prompt de Clínica Zen donde `Mirar_disponibilidad` usaba `"json"` (correcto) pero `Reservar` usaba `"form"` (incorrecto).
