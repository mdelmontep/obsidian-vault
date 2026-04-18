---
title: mejoras térmicas pendientes macbook pro 2019
date: 2026-04-15
source: claude-code-session
tags: [inbox, hardware, macbook]
---

Tras diagnóstico del 2026-04-15 confirmado el MacBook Pro i9 2019 tiene throttling severo bajo carga sostenida (Claude Code + Docker + Chrome + Electron apps). Ver nota completa en `knowledge/learnings/macbook-pro-i9-2019-throttling-severo-bajo-carga-sostenida.md`.

Mejoras propuestas pero **no ejecutadas** esta sesión. Pendientes de decidir/accionar:

### 1. Reaplicación de pasta térmica

- **Impacto esperado**: −10-15 °C
- **Coste**: ~60-120 € en servicio técnico
- **Urgencia**: alta (es la mejora nº1 en coste/beneficio)
- **Pendiente**: elegir servicio técnico, llevar el Mac
- Desde 2019 probablemente está la pasta de fábrica, ~6 años resecándose

### 2. Turbo Boost Switcher Pro

- **Impacto esperado**: −15-20 °C, ventiladores casi inaudibles, +1 h autonomía
- **Coste**: gratis la versión básica, ~10 € la Pro
- **Urgencia**: media (se puede instalar ahora mismo, es software)
- **Pendiente**: descargar, instalar, aceptar extensión de sistema en Ajustes → Privacidad → Seguridad
- **Trade-off**: pierdes ~20 % rendimiento pico en ráfagas cortas. Para Claude Code / Docker / navegador no se nota. Para renders de vídeo o compilaciones pesadas puntuales sí

### Decisión pendiente

¿Instalar Turbo Boost Switcher ya como quick win, dejar la pasta térmica para cuando haga falta más? ¿O llevarlo al servicio técnico cuanto antes y desbloquear ambos beneficios de un tirón?
