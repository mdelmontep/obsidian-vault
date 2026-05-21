---
title: n8n Set node output solo lleva assignments explícitos
date: 2026-05-21
source: claude-code-session
tags: [n8n, gotcha, set-node]
---

En un Set node, las expressions `={{ $json.X }}` leen del INPUT del nodo. Pero el OUTPUT solo lleva los campos definidos en `assignments`. Si `X` no está en assignments, el downstream ve `null` aunque el input lo trajera y el chatInput lo use.

Caso real 2026-05-21 FacturaIA bot: `Preparar Input Agente` usaba `$json.memberships_count` en el chatInput (HAS_MULTI_ORG funcionaba) pero NO tenía assignment para `memberships_count` → `Parsear y Calcular Totales` leía `_agentIn.memberships_count = null` → `Number(null) || 1 = 1` → cabecera 🧾 sin org aunque el agente sabía que era multi-org.

Fix: añadir assignment numérico `{id: "a-memberships-count", name: "memberships_count", value: "={{ Number($json.memberships_count) || 1 }}", type: "number"}`.

Regla: si un downstream necesita un campo, hay que añadirlo a assignments, no basta con que el input lo tenga. Code nodes con `return [{ json: {...} }]` no tienen este problema (return explícito). Ver [[n8n-dollar-json-tras-http-es-respuesta-http-no-item-original]].
