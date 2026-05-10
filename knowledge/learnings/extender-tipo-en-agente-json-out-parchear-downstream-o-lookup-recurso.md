---
title: extender tipo en agente JSON-out — parchear downstream o lookup recurso
date: 2026-05-10
source: claude-code-session
tags: [n8n, ai-agent, llm, contract]
---

Si un agente JSON-out tiene contrato `{tipo, cliente, lineas[], totales}` y añades un `tipo` nuevo que **NO necesita lineas** (porque el recurso ya existe en BD), los nodos downstream que iteran `data.lineas` calculan 0 → resumen vacío al usuario.

**Dos opciones**:

(a) **Parchear cada downstream**: branch al inicio que detecta el nuevo tipo y construye el shape esperado.

(b) **Lookup del recurso real**: branch que hace HTTP/SQL al recurso (usando el id que el agente ya resolvió) y obtiene los datos reales. Más fiable porque el LLM puede equivocarse en números.

**Recomendación**: (b) cuando el recurso tiene fuente de verdad clara (BD propia). (a) cuando es agregación pura.

Caso real FacturaIA: agente para `tipo='convertir_presupuesto'` devuelve solo `presupuesto_id` (sin lineas — las copia el backend al convertir). `Parsear y Calcular Totales` iteraba data.lineas → resumen WhatsApp con base/IVA/total a 0,00€. Fix con (b): branch que llama Supabase REST con `presupuesto_id+org_id` para totales reales y construye el resumen.
