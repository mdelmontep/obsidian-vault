---
title: ADR-013 — EcoBox Retell Conversation Flow en Rigid Mode (no Flex)
date: 2026-05-22
status: accepted
tags: [adr, ecobox, retell, conversation-flow, coste]
---

## Contexto
Agente voz Alex EcoBox: Conversation Flow 13 nodos, gpt-4.1 cascading, KB attached con 11 chunks (~2.5k tokens), 4 tools custom. Techo de coste impuesto por cliente: **€0.20/min**. Llamada típica ~3 min.

## Opciones consideradas
- **A — Flex Mode + gpt-4.1 cascading high_priority** — compila TODO el flow + KB + tools en 1 prompt (estimado 4.500+ tokens compilados). Activa token-scaling multiplier x2-x5 sobre el LLM. Coste estimado: €0.20-0.35/min. Mejor UX para context switching cliente.
- **B — Flex Mode + gpt-4.1 sin high_priority** — mismo problema scaling pero LLM ligeramente más barato. €0.18-0.28/min. Sigue cerca del techo.
- **C — Rigid Mode + gpt-4.1 cascading sin high_priority** — solo prompt del nodo activo + global_prompt va al LLM. Sin token-scaling. €0.135/min. ~35% margen bajo techo.
- **D — Rigid Mode + gpt-4o-mini** — €0.115/min. Calidad inferior con español + clientes 35-65, descartado.

## Decisión
**C (Rigid Mode + gpt-4.1 cascading sin `high_priority`)**, porque (a) cabe bajo €0.20/min con margen, (b) global_prompt EcoBox bien escrito cubre identidad/tono/temas tabú que el LLM ve siempre, (c) flujo lineal (welcome → extract → classifier → ramas) no necesita context switching de Flex.

## Consecuencias
- Cualquier regla cross-nodo (objeciones, derivación) DEBE vivir en `global_prompt`, no en nodos individuales. El LLM no ve otros nodos en Rigid.
- Si futuras conversaciones requieren saltos no lineales (cliente cambia de "info" a "cita" sin reiniciar), evaluar Flex con auditoría de tokens primero. Posible necesidad de componentes para acotar tamaño.
- `tool_call_strict_mode: false` mantenido (sin Flex el LLM tiene menos contexto, strict puede ser demasiado restrictivo). Cambiar a true si se observan args inventados en producción.
- Replicable: para cualquier cliente AgentesIA voz con techo <€0.20/min y KB attached, Rigid es default.
