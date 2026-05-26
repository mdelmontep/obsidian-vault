---
title: LLM voz inventa el año si no se inyecta la fecha actual explícita
date: 2026-05-25
source: claude-code-session
tags: [llm, retell, dynamic-variables, dates]
---

Modelos modernos (gpt-4o, gpt-4.1) sin contexto temporal explícito construyen fechas ISO con el año de su training cutoff. Caso real: usuario en 2026-05-25 pide cita "el viernes que viene", LLM construye `2024-06-13T10:30:00+02:00`. Sin guard, el evento se crea en 2024 y el cliente no lo ve.

Fix de defensa en profundidad (los 3 simultáneos):

1. **Dynamic variable en agente**: `retell_llm_dynamic_variables.fecha_hoy = "26 de mayo de 2026"` + `ano_actual = "2026"` (sustituye en prompts).
2. **Global prompt explícito**: "HOY es {fecha}. Año actual: {año}. NUNCA uses 2024 ni 2025 en fechas ISO."
3. **Guard en backend**: validar `new Date(preferred_date).getFullYear()` está en `[year_actual, year_actual+1]`. Si no, devolver error legible al LLM para que vuelva a preguntar.

Solo (1)+(2) no basta — el LLM puede ignorarlo bajo carga. (3) es el cinturón.

Caso real: EcoBox 2026-05-25 — primera llamada real reservó cita en 2024-06-13 sin queja del LLM. Guard n8n cortó el segundo intento.
