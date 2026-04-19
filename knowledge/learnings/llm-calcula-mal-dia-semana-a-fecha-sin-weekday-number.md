---
title: llm calcula mal dia de semana a fecha sin weekday number
date: 2026-04-19
source: claude-code-session
tags: [n8n, ai-agent, fechas, bug]
---

GPT-5.1 calculó "lunes" como 20 de abril (domingo) estando a sábado 19 de abril 2026. El error: restó mal los días de la semana sin tener referencia numérica del día actual.

## Fix

En la Think tool description del AI Agent, incluir:

1. **`{{ $now.weekday }}`** — número del día (1=lunes...7=domingo) para que el LLM tenga referencia numérica
2. **`{{ $now.setLocale('es').toFormat('EEEE') }}`** — nombre del día en español
3. **Fórmula explícita**: `días_restantes = día_objetivo - día_actual; si resultado <= 0, sumar 7`
4. **Ejemplos concretos**: "Si hoy sábado (6) y piden lunes (1): 1-6=-5, -5+7=2 → hoy+2 días"
5. **Paso de verificación**: "VERIFICACIÓN OBLIGATORIA: confirma que la fecha resultante cae en el día de la semana correcto"

## Timezone

También corregir el offset estacional en los ejemplos de formato ISO:
- Abril-octubre: `+02:00` (CEST)
- Noviembre-marzo: `+01:00` (CET)

El prompt original tenía `+01:00` hardcodeado, incorrecto para abril.

## Contexto

Clínica Zen, workflow chatbot `u0AQPe9pxN79dbFa`. Think tool generó `2026-04-20T10:00:00+02:00` (domingo) cuando el paciente pidió "lunes" = 21 de abril.
