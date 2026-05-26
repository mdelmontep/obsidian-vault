---
title: $fromAI en toolCode lanza no-execution-data-available en n8n 2.15.x
date: 2026-04-17
source: claude-code-session
tags: [n8n, toolCode, ai-agent, bug]
---

En n8n 2.15.x, usar `$fromAI()` dentro de nodos `toolCode` (`@n8n/n8n-nodes-langchain.toolCode`) conectados como `ai_tool` a un AI Agent lanza:

```
Cannot assign to read only property 'name' of object 'Error: No execution data available'
```

El error viene del contexto de ejecución del toolCode, no del HTTP ni de otros helpers. `$fromAI()` rompe el sandbox aunque es la forma "oficial" documentada de recibir parámetros en toolCode.

## Workaround validado

Usar la variable global `query` que el AI Agent pasa como string al toolCode. El LLM puede enviar los parámetros en 3 formatos distintos — hay que parsear los 3:

```javascript
let params = {};
try {
  params = JSON.parse(query); // formato JSON
} catch(e1) {
  if (query.trim().startsWith('{')) {
    try { params = new Function('return (' + query + ')')(); } catch(e2) {} // JS object literal
  }
  if (Object.keys(params).length === 0) {
    // key-value por líneas: "telefono: 34617314938\nsubject: ..."
    const lines = query.split('\n');
    for (const line of lines) {
      const idx = line.indexOf(':');
      if (idx > 0) {
        const key = line.substring(0, idx).trim().toLowerCase();
        const val = line.substring(idx + 1).trim();
        if (val) params[key] = val;
      }
    }
  }
}
```

## Diagnóstico

Para depurar qué variables hay disponibles en un toolCode, usar este código mínimo:

```javascript
const parts = [];
try { parts.push('$input.item.json=' + JSON.stringify($input.item.json)); } catch(e) { parts.push('ERR:' + e.message); }
try { parts.push('typeof_query=' + typeof query); } catch(e) {}
try { if (typeof query !== 'undefined') parts.push('query=' + String(query).substring(0,200)); } catch(e) {}
return parts.join('\n');
```

Resultado: `$input.item.json.value` contiene el mensaje original del usuario, `query` contiene los parámetros del tool call.

## Cuándo aplica

Cualquier toolCode con `$fromAI()` en n8n 2.15.x. Verificar en versiones posteriores si se ha corregido.

## Alternativa cuando los args vienen de state (no del LLM)

Si el arg que ibas a pasar por `$fromAI` viene de un `last_listado` ya resuelto deterministicamente server-side (slot resolver pre-LLM), elimina `$fromAI()` completamente. Lee el slot directo desde un nodo upstream:

```
const pia = $('Preparar Input Agente').first().json;
const stateJson = typeof pia.previous_state_json === 'string'
  ? JSON.parse(pia.previous_state_json) : pia.previous_state_json;
const presupuestoId = stateJson?.resolved_slot?.id;
```

Más limpio que el workaround `query`, elimina la clase entera de bugs (LLM no decide UUIDs) y resuelve también referencias en lenguaje natural ("el más caro", "del 18 de mayo"). Aplicado en TuFacturaIA bot WhatsApp 2026-05-18. Ver [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]] · [[ADR-003-slot-resolver-determinista]]

## Por qué el parser `query` solo no basta cuando los args vienen del LLM

Sin `$fromAI`, el toolCode tampoco declara schema al LLM. Resultado: el LLM mete el turno crudo del usuario en `query` ("45€ de gasolina") y el parser no encuentra estructura → `params={}` → `importe=undefined`. La pareja completa post-`$fromAI` para args generados por el LLM es:

```
specifyInputSchema: true
schemaType: 'manual'
inputSchema: <JSON Schema con required + description por campo>
```

Con eso n8n inyecta el schema al tool-calling del LLM y `query` llega como JSON estructurado. `JSON.parse(query)` del parser cubre el caso. Verificado contra MCP n8n SDK reference v1.3 de `@n8n/n8n-nodes-langchain.toolCode`. Aplicado en TuFacturaIA WA Boost v1 2026-05-26 (`registrar_gasto_rapido`, `analizar_compra`) tras smoke real que reveló que sin schema el LLM enviaba lenguaje natural.
