---
title: un guard en el prepare de un item declina el batch entero; la validación que afecta al batch va en el orquestador
date: 2026-07-21
source: claude-code-session
tags: [agentes, hitl, arquitectura, composicion, agh]
---
En un flujo que propone un BATCH de acciones (varios writes en un turno HITL), si validas/declinas
dentro del `prepare` de UN item, el freno se propaga a TODO el batch (el orquestador corta el turno
al primer `decline`/`clarify`). Caso AGH #543: el interpreter fabricaba una reunión vacía junto al
alta de cliente; un guard «reunión sin contenido → decline» en el meeting-executor habría matado
también el `crm.createClient` que el usuario SÍ quería.

Regla: la validación que decide si una acción DEBE EXISTIR en el batch (precisión de composición) va
en quien COMPONE el batch (el interpreter/prompt, o un filtro previo), no en el handler de un item.
El handler de un item solo valida SUS datos (falta el cliente, id inexistente), no si el item sobra.
Relacionado: [[hitl-turnos-criticos-deterministas-antes-del-llm]].
