---
title: Retell subagent por defecto deriva a humano — bloquear explícito por caso
date: 2026-05-25
source: claude-code-session
tags: [retell, subagent, transfer, prompts]
---

Cuando un subagent tiene UNA sola edge saliente hacia `transfer_call`, el LLM transfiere en cuanto cree haber recogido los datos mínimos del prompt — incluso si el tool resolvía el caso autónomamente.

Síntoma: cliente dice "quiero cancelar", subagent tiene Buscar_reserva + Cancelar_cita como tools, pero acaba transfiriendo a humano. Los tools nunca se invocan.

Causa: el prompt original dice "tras recoger nombre+matrícula, deriva a humano" — el LLM interpreta el transfer como la salida estándar.

Fix:
1. **Reescribir prompt por casos explícitos**:
```
CASO A — cancelar → llama Buscar_reserva, confirma, llama Cancelar_cita, despídete. NO transfieras.
CASO B — cambio fecha → "mándanos un WhatsApp". NO transfieras.
CASO C — pide humano explícito → transfiere.
```
2. **Múltiples edges** con `transition_condition` semántico claro: una a `n-end-generic` (resuelto autónomamente), otra a `n-transfer-human` (caso que requiere humano). Sin la edge `end-generic`, el LLM no sabe a dónde ir tras resolver.

Caso real: EcoBox `n-gestionar` 2026-05-25/26 — primero hacía transfer en cancelar, tras añadir edge `e-gestion-resolved` + reescribir prompt en 4 casos numerados, ejecuta cancelar limpio.
