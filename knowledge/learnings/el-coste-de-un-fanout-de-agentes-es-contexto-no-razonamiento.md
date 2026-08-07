---
title: el coste de un fan-out de agentes es contexto, no razonamiento
date: 2026-08-07
source: claude-code-session
tags: [harness, agentes, coste, workflow]
---

Un gate de cierre con 9 agentes costó **$34,72** auditando 144 líneas de diff.
El recibo, sacado del `usage` real:

| | Tokens | Coste |
|---|---|---|
| Output (razonamiento) | 90.181 | $2,25 (6 %) |
| Cache read | 25.256.544 | $12,63 |
| Cache write | 3.164.724 | $19,78 (57 %) |

**El 94 % era contexto rearrastrado.** 236 tool calls: cada agente redescubría
el mismo diff con `Bash` y cada llamada reenviaba todo el contexto acumulado. La
misma migración se leyó 11 veces y el `openapi.json` 13.

**La palanca no es bajar el effort ni recortar prompts: es no hacerles buscar lo
que ya sabes.** Inyecta el diff en el prompt (10K tokens cacheados una vez contra
236 exploraciones), agrupa dimensiones por dónde vive el riesgo en vez de por
cómo se llama la preocupación, y pon un presupuesto explícito de tool calls.

**Cómo medirlo**: `usage` de los `agent-*.jsonl` del run. Contar prompts offline
no vale — ver [[medir-el-coste-de-un-prompt-el-recibo-no-el-proxy]].

Relacionado: [[claude-code-harness]] · [[el-alcance-de-una-auditoria-lo-decide-lo-que-cambio]]
