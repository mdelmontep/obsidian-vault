---
title: decorar una interfaz para interceptar sin tocar el core de otro
date: 2026-07-02
source: claude-code-session
tags: [arquitectura, patterns, parallel-work]
---

Necesitas añadir un modo/flujo nuevo que intercepta el turno, pero el core (p. ej. el `Brain`/loop conversacional) es de otra persona y no puedes editarlo. Si el punto de entrada es una **interfaz de 1 método** que el resto solo consume por tipo (`Brain.handle(msg)`), la vía limpia es un **decorator que implementa esa misma interfaz** y envuelve al real: intercepta cuando aplica, y **delega tal cual al inner** cuando no (no-op transparente).

Clave: el estado del modo (p. ej. "en onboarding") vive en un **store propio**, NO en el estado cerrado del owner. Se cablea en el composition root (`brain = mode.wrap(inner)`), cero ediciones al core. Si el modo necesita el HITL del core (proponer→confirmar), **delega el turno al inner** en vez de reimplementarlo.

Se compone incluso si el owner cambia el *interior* del core, mientras no cambie la firma de la interfaz. Ver [[cross-pr-integrar-interfaz-por-tipado-estructural]].
