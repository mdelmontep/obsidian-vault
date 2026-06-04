---
title: retell function node instruction guía construcción de parámetros iso
date: 2026-06-04
source: claude-code-session
tags: [retell, conversation-flow, fechas, iso]
---
Los function nodes del Conversation Flow aceptan campo `instruction` (igual que conversation nodes).
Sin él, el LLM inventa `from_iso` con año 2024 u otros defaults incorrectos.
Con instrucción explícita + `{{current_time_Europe/Madrid}}` construye el ISO correcto.
Patrón mínimo:
```
Llamar <tool>. Fecha actual: {{current_time_Europe/Madrid}}. Año siempre 2026.
- Franja mañana: díaT09:00:00+02:00 → díaT14:00:00+02:00
- Franja tarde:  díaT14:00:00+02:00 → díaT21:00:00+02:00
- Hora concreta: díaT(h-1)00:00+02:00 → díaT(h+2)00:00+02:00
Ejemplo: lunes 8 jun → 2026-06-08T09:00:00+02:00
```
Sin instruction el nodo no aparece en docs pero sí funciona (verificado en prod).
