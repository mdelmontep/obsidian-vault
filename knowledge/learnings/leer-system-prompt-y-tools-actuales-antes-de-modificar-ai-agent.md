---
title: leer system prompt y tools actuales antes de modificar AI agent
date: 2026-05-10
source: claude-code-session
tags: [n8n, ai-agent, llm, workflow]
---

Antes de añadir un endpoint que sustituye/extiende el system prompt de un AI Agent productivo, **leer el prompt actual y las tools cableadas vía API** (n8n REST `GET /workflows/{id}` + `jq '.nodes[] | select(.name=="Agente X")'`).

El bot puede ser **JSON-out** (devuelve `{tipo, ...}` que un nodo downstream procesa) o **conversacional** (texto libre con tool-calls). Cada uno tiene contrato distinto. Mi default asumió conversacional, el real era JSON-out — sustituir el prompt habría roto producción inmediato.

Patrón:
1. `GET /workflows/{id}` → backup completo.
2. Inspeccionar nodo del agente: `parameters.options.systemMessage`, tools conectadas via `ai_tool` connections.
3. Si el contrato real difiere de tu diseño → realinear ANTES de PUT.

Aplica a cualquier integración con LLM agent existente (n8n, LangChain, custom). Caso real TuFacturaIA: el sistema híbrido del prompt asumió tools `find_presupuesto`/`convert_presupuesto` que no existían en el workflow — había `consultar_facturas`/`consultar_clientes`/`consultar_catalogo` y formato JSON estricto.
