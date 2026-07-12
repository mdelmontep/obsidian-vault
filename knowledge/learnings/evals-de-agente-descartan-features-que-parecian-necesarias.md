---
title: Un harness de evals para un agente descarta features que parecían necesarias
date: 2026-07-12
source: claude-code-session
tags: [llm, evals, copiloto, facturaia, proceso, agentes]
---
Al mejorar el Copiloto de FacturaIA (agente con ~60 tools) el plan tenía 6 fases. Antes de
construir nada monté un harness de evals (`npm run eval:copiloto`): golden set de casos de
regresión reales (los mismos bugs que habían provocado 31 versiones del system prompt),
corriendo el runner REAL con el LLM REAL contra la org sandbox, asertando DECISIONES
observables (qué tool llama/propone, prosa vs JSON), no cifras. `userConfirmed:false` → las
tools destructivas se proponen pero no se ejecutan (no muta datos).

Medir cambió qué se construyó:
- **Subir el modelo** (gpt-4o → gpt-5.2, una línea + más barato) cerró un bug real Y volvió
  innecesarias 2 fases: routing de tools (gpt-5.2 no se confunde con 60 tools: 14/14) y
  ranking de memoria (había 1 sola memoria en toda la plataforma).
- Descartar con evidencia = no gastar por gastar. Construir esas 2 fases "porque estaban en
  el plan" habría sido complejidad especulativa.

Patrón: para un agente, el primer entregable es la RED DE MEDIDA, no la primera feature.
Truco útil: `knownBaselineGap` + `it.fails` → un objetivo que el baseline aún no cumple queda
verde pero se pone rojo al arreglarse ("ya está, quita el flag"). Ver [[gpt-4o-era-el-modelo-real-en-prod-sin-saberlo]].
