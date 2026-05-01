---
title: n8n toolWorkflow cachedResultName puede mentir tras clonar workflow
date: 2026-05-01
source: claude-code-session
tags: [n8n, debugging, replicar]
---

Los nodos `toolWorkflow` guardan dos valores: `workflowId.value` (ID real) y `workflowId.cachedResultName` (etiqueta UI). Al clonar un workflow entre instancias n8n, el `value` queda apuntando al ID original (que no existe en la instancia destino) pero el `cachedResultName` muestra el nombre correcto. El AI Agent invoca el tool, n8n no encuentra el sub-workflow, devuelve error al agente, el agente responde mal — todo sin alerta visible.

Caso: Simarro tenía 4 toolWorkflow con `value` apuntando a IDs de CZ (`3vTcxzkNMnD7rORF`, etc.) pero `cachedResultName` decía "Leads cambio de fecha o anulación". El bot fallaba al cancelar/reservar/derivar/buscar.

Fix: tras importar/clonar, validar todos los `value` contra la lista de workflows reales:
```python
sub_refs = [n['parameters']['workflowId']['value'] for n in nodes if n['type']=='@n8n/n8n-nodes-langchain.toolWorkflow']
existing = {w['id'] for w in api.list_workflows()}
broken = set(sub_refs) - existing
```
