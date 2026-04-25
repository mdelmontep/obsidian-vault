---
title: n8n executeWorkflowTrigger v1.1 requiere input schema
date: 2026-04-25
source: claude-code-session
tags: [n8n, workflows, sub-workflows]
---

El nodo `executeWorkflowTrigger` con `typeVersion: 1.1` requiere definir los inputs esperados en `workflowInputs`. Sin esto, activar el workflow falla:

```
Cannot publish workflow: 1 node have configuration issues:
Node "Execute Workflow Trigger": Missing or invalid required parameters (1 issue)
```

## Solución

Si no necesitas validación de inputs (el sub-workflow acepta cualquier dato del caller), usar `typeVersion: 1.0`:

```json
{
  "parameters": {},
  "name": "Execute Workflow Trigger",
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "typeVersion": 1.0
}
```

v1.0 acepta cualquier input sin schema. v1.1 es más estricto y requiere declarar cada campo.
