---
title: Verifica qué modelo LLM corre DE VERDAD en prod antes de optimizar el prompt
date: 2026-07-12
source: claude-code-session
tags: [llm, facturaia, copiloto, openai, prod]
---
El Copiloto de FacturaIA llevaba tiempo en `gpt-4o` (dos generaciones por detrás; la cuenta ya
tenía acceso hasta gpt-5.2) y NADIE lo sabía: el modelo lo decide `system_config.llm_provider`
en BD, que GANA sobre la env `LLM_PROVIDER` (override sin redeploy desde /admin/llm). El runner
tenía el modelo hardcodeado (`OPENAI_MODEL='gpt-4o'`, `ANTHROPIC_MODEL='claude-sonnet-4-6'`).

Se habían parcheado 31 versiones del system prompt... sin saber contra qué modelo se probaban.
Medir el modelo real contra el golden set: gpt-4o 9/10, gpt-5.1 8/10 (regresión), gpt-5.2 10/10
y **más barato** ($0.88/$7 vs $2.50/$10 por 1M). Un cambio de una línea batió a varias fases de
prompt-engineering.

Regla: antes de tocar el prompt de un asistente, comprueba el modelo EFECTIVO en prod (no el
default del código ni la env — mira el override de BD). Modelo del copiloto ahora configurable
por env `COPILOTO_OPENAI_MODEL`/`COPILOTO_ANTHROPIC_MODEL` (revert en caliente). Ver
[[evals-de-agente-descartan-features-que-parecian-necesarias]].
