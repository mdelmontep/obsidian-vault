---
title: chatwoot automation rule assignee_id is_not_present dispara en cada update
date: 2026-04-16
source: claude-code-session
tags: [chatwoot, automation-rules, gate, chatbot]
---

Las Automation Rules de Chatwoot con condición `assignee_id is_not_present` disparan en **cada** evento `conversation_updated` cuando no hay assignee individual — que es el estado normal si el team tiene `allow_auto_assign: false`.

## Problema concreto

Se creó una regla "Reset a bot-activo al desasignar" con condiciones:
- `assignee_id is_not_present` AND
- `labels equal_to humano`

Intención: cuando un agente devuelve la conversación al bot (se desasigna), la regla quita `humano` y pone `bot-activo`.

Resultado real: la regla disparaba **inmediatamente después del handoff**. El flujo era:
1. Bot ejecuta handoff → pone label `humano`
2. Chatwoot emite `conversation_updated` (label changed)
3. Automation Rule detecta `assignee_id is_not_present` (true, porque nunca hubo assignee individual) + `labels contains humano` (true, recién puesto)
4. → Quita `humano`, pone `bot-activo` → el handoff se revierte

## Fix

Eliminar la condición `assignee_id is_not_present` y usar `status equal_to resolved` como señal explícita de "el agente humano terminó":

```json
{
  "conditions": [
    {"attribute_key": "status", "filter_operator": "equal_to", "values": ["resolved"]},
    {"attribute_key": "labels", "filter_operator": "equal_to", "values": ["humano"]}
  ],
  "actions": [
    {"action_name": "remove_label", "action_params": ["humano"]},
    {"action_name": "add_label", "action_params": ["bot-activo"]}
  ]
}
```

Así solo dispara cuando el agente resuelve explícitamente la conversación — una acción deliberada, no un efecto secundario.
