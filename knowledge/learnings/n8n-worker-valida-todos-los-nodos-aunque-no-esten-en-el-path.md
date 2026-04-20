---
title: n8n worker valida todos los nodos aunque no estén en el path de ejecución
date: 2026-04-20
source: claude-code-session
tags: [n8n, worker, plugins]
---

El worker de n8n valida TODOS los nodos del workflow al recibirlo de la cola, incluso los que no están en el path de ejecución actual. Si un nodo usa un tipo de plugin no instalado en el worker (ej: `@retellai/n8n-nodes-retellai`), la ejecución se queda en "Queued/Starting soon" indefinidamente sin error visible.

**Síntoma**: el workflow funciona en modo manual (main instance) pero se congela en producción (queue mode con worker).

**Fixes posibles**:
1. Instalar el plugin en el container del worker (imagen custom o volumen compartido)
2. Mover los nodos del plugin problemático a un sub-workflow separado que se llame vía Execute Workflow

Descubierto en Clínica Zen: nodos Retell en "Leads entrantes" bloqueaban toda ejecución del workflow en el worker.
