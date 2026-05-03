---
title: n8n wait node vacío es webhook-type y se queda stuck para siempre
date: 2026-05-04
source: claude-code-session
tags: [n8n, wait, debounce, stuck]
---

Un nodo Wait con `parameters: {}` (sin `resume`, `amount`, ni `unit`) NO espera un tiempo — espera una llamada de webhook externa que nunca llega. La ejecución aparece como "Running" indefinidamente.

## Síntoma

Ejecución corriendo >5min sin avanzar, colgada exactamente en el nodo Wait.

## Diagnóstico

```bash
jq '.nodes[] | select(.type == "n8n-nodes-base.wait") | {name, parameters}' workflow.json
```
Buscar nodos con `"parameters": {}`.

## Fix via REST API

```python
# Parchear el nodo en el PUT del workflow
node['parameters'] = {"resume": "timeInterval", "amount": 2, "unit": "seconds"}
# PUT /api/v1/workflows/{id} con settings saneado (solo executionOrder, timezone, callerPolicy)
```

## Contexto

Caso Simarro 2026-05: nodo "Wait" de debounce (Redis push → Wait → Redis get) quedó sin parámetros al replicar de CZ. Causaba que cada mensaje del chatbot se quedara colgado >5min.
