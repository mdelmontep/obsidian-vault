---
title: retell conversation flow flex compila todo y dispara token-scaling
date: 2026-05-22
source: claude-code-session
tags: [retell, voice, coste]
---

Flex Mode compila TODO el flow (nodos + edges + KB + tools) en UN prompt. Si supera 3.500 tokens compilados, Retell aplica **token-scaling multiplier** (x2-x5 sobre el LLM).

Rigid Mode sólo envía el prompt del nodo activo + global_prompt. Cero scaling, predecible.

Coste por minuto castellano:
- Flex + gpt-4.1 cascading high_priority + KB attached: €0.20-0.35/min
- **Rigid + gpt-4.1 cascading SIN high_priority: €0.135/min** ← sweet spot
- Rigid + gpt-4o-mini: €0.115/min (perdida calidad para voice)

Para techos de €0.20/min impuestos por cliente, Rigid es la única opción viable. Flex sólo si necesitas context-switching real entre tareas y has acotado tokens.

Decisión: por defecto Rigid en agentes con KB + tools. Flex solo tras medir token count del flow compilado en simulator Retell.

Caso real: EcoBox 2026-05 — pasé Flex→Rigid + high_priority=false para encajar bajo €0.20/min.
