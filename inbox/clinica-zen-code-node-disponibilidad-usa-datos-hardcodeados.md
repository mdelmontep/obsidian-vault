---
title: clinica zen code node disponibilidad usa datos hardcodeados
date: 2026-04-18
source: claude-code-session
tags: [clinica-zen, n8n, bug]
---

El nodo `Code in JavaScript2` del workflow "Leads entrantes" (`RN0wl8RaRmwLpnfQ`) en `n8nclinicazen.agentesia.madrid` define un array `const events = [...]` con datos de ejemplo hardcodeados y fechas de 2025, en vez de usar `$input.all()` del nodo Google Calendar anterior.

Si este código está tal cual en producción, la consulta de disponibilidad devuelve siempre el mismo resultado independientemente del estado real del calendario.

Pendiente: verificar si este nodo se ejecuta realmente o si hay otro flujo activo que lo bypasea.

**Nota (2026-04-19):** Este bug es del workflow **Leads Entrantes** (`RN0wl8RaRmwLpnfQ`), NO del chatbot. El chatbot (`u0AQPe9pxN79dbFa`) usa `Mirar_disponibilidad` (Google Calendar tool directo) que sí consulta el calendario real. Son flujos distintos.
