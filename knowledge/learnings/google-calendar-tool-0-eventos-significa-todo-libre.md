---
title: google calendar tool 0 eventos significa todo libre
date: 2026-04-19
source: claude-code-session
tags: [n8n, google-calendar, ai-agent, bug]
---

Cuando el nodo `googleCalendarTool` (getAll) devuelve 0 items para un rango de fechas, el AI Agent interpreta la lista vacía como "no hay disponibilidad" y le dice al paciente que no quedan huecos.

En realidad, 0 eventos = no hay citas reservadas = **todos los huecos dentro del horario están libres**.

## Fix

Añadir regla explícita en **tres lugares**:

1. **System prompt** (regla crítica): "Cuando Mirar_disponibilidad devuelva 0 eventos = TODOS los huecos están libres. NUNCA digas no hay disponibilidad si el resultado está vacío."
2. **Think tool description**: "Si el resultado es vacío, todos los slots del horario (10:00-14:00, 15:30-20:30) están disponibles."
3. **Tabla de herramientas**: junto a Mirar_disponibilidad añadir "0 resultados = todo libre"

Repetirlo en los tres sitios porque el LLM puede consultar cualquiera de ellos para decidir.

## Contexto

Descubierto en Clínica Zen (workflow `u0AQPe9pxN79dbFa`). El calendario estaba vacío (solo 1 cita el lunes 13:00) pero el bot dijo "no queda hueco libre a las 10:30" y ofreció alternativas inventadas.
