---
title: agentes background muertos por session limit se reanudan con sendmessage, no relanzando
date: 2026-07-10
source: claude-code-session
tags: [claude-code, agentes, workflow]
---
Cuando el session limit mata agentes background a mitad de tarea ("Agent terminated early due to an API error: You've hit your session limit"), NO relanzar un agente nuevo a ciegas:

1. `git status` primero — inventariar qué archivos dejó escritos (los writes en disco sobreviven; lo no escrito se pierde).
2. `SendMessage` al MISMO agentId con: qué quedó en el working tree, qué se perdió (p.ej. tests que había escrito y no llegaron a disco) y qué falta. Reanuda desde su transcript con todo el contexto de decisiones.
3. Relanzar fresco solo si murió sin escribir nada (tree limpio) — ahí no hay nada que aprovechar y el transcript corto no compensa.

Gotcha: si relanzaste ya un duplicado y el original revive, NO reanudar ambos — dos agentes sobre los mismos archivos se pisan. Reanudar el que más progreso dejó y abandonar el otro.
