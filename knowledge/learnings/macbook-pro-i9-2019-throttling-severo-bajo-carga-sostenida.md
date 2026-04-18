---
title: macbook pro i9 2019 throttling severo bajo carga sostenida
date: 2026-04-15
source: claude-code-session
tags: [hardware, macos, performance]
---

El Intel Core i9-9980HK (MacBook Pro 16" 2019) sube hasta ~5 GHz en Turbo Boost durante 10-30 s, llega a ~95-100 °C, y macOS lo baja a ~1.3 GHz — **por debajo de la frecuencia base de 2.4 GHz** — para no quemarse. El síntoma al usuario es "va a picos rápidos y luego se queda muy lento".

No es un problema de software ni de malas apps: es un defecto de diseño térmico del chasis 2019, que disipa ~35 W pero Apple puso un chip de 45 W TDP.

Bajo carga sostenida (Claude Code + Docker + Chrome + Electron apps + compilación), el throttling es prácticamente permanente.

**Mejoras ordenadas por impacto real:**

1. **Reaplicar pasta térmica** en servicio técnico. Si nunca se ha hecho en ~6 años, está reseca. Baja 10-15 °C. Mejora más importante.
2. **Turbo Boost Switcher Pro** — desactiva el Turbo Boost y fija la frecuencia en 2.4 GHz. Pierdes ~20 % en ráfagas pero **ganas rendimiento sostenido** porque nunca bajas de 2.4 (antes oscilabas entre 4.0 y 1.3). Temperatura baja 15-20 °C, ventiladores casi inaudibles, batería dura más.
3. **Macs Fan Control** con curva agresiva (ventiladores suben a 80 °C en vez de 95 °C).
4. **Base con ventilación** inferior — el i9 2019 toma aire por la parte de abajo.

Para cargas tipo Claude Code / Docker / navegador, desactivar el Turbo Boost no se nota como pérdida, solo como mejora. Para renders de vídeo y compilaciones pesadas puntuales sí se pierde tiempo.
