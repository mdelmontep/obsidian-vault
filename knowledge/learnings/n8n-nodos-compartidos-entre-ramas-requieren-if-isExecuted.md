---
title: n8n nodos compartidos entre ramas requieren $if isExecuted
date: 2026-04-21
source: claude-code-session
tags: [n8n, workflow, expresiones]
---

Cuando un workflow de n8n tiene **dos entry points** (ej: webhook para Retell + executeWorkflowTrigger para chatbot) y ambos convergen en un nodo downstream que referencia un Edit Fields de solo una rama, la expresión falla con "Invalid expression".

**Fix:** usar `$if` con `.isExecuted` para elegir la fuente correcta:

```
={{ $if($('Edit Fields Retell').isExecuted, $('Edit Fields Retell').item.json.nombre, $('Edit Fields Chatbot').item.json.nombre) }}
```

Distinto del patrón de ramas IF condicionales (where/else) dentro de un mismo flujo. Aquí el problema son **dos triggers distintos** que convergen en el mismo nodo.

Caso real: Clínica Zen, `Create an event1` referenciaba `$('Edit Fields3')` (rama Retell) pero fallaba cuando se llamaba desde el chatbot vía executeWorkflowTrigger.
