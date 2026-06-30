---
title: ADR-035 — control de un canal de ingesta vive en una sola pantalla, con estado de solo lectura en el resto
date: 2026-07-01
status: accepted
tags: [adr, facturaia, ux]
---

## Contexto
Pausar/reanudar Gmail OCR + cambiar intervalo de revisión acabó implementado dos veces:
en Ajustes→Integraciones (catálogo OAuth genérico, todas las integraciones) y en
Agentes IA→Canales de entrada (vista de negocio, "por dónde entran mis facturas").
Mismo dato (`ocr_enabled`/`poll_interval_minutes`), dos editores → riesgo de divergencia
visual (opciones de intervalo distintas en cada panel) si no se mantienen sincronizados.

## Opciones consideradas
- **A — control editable en ambas pantallas, sincronizadas** — visibilidad máxima, pero doble superficie de mantenimiento y riesgo real de divergencia (ya ocurrió: intervalos con valores distintos en cada panel).
- **B — control solo en Agentes IA, nada en Integraciones** — fuente única, pero Integraciones (que sí debe responder "¿mi cuenta Google está bien conectada?") pierde toda señal de si el canal está realmente pausado.
- **C — control único en Agentes IA + estado de solo lectura y link en Integraciones** — fuente única para editar, visibilidad cruzada sin duplicar el editor.

## Decisión
**C**. Integraciones responde "¿está la cuenta conectada?" (modelo cuenta/permisos);
Agentes IA responde "¿está funcionando el flujo de negocio?" (modelo tarea). El control
vive donde se hace la pregunta de negocio; el catálogo genérico solo informa + enlaza.

## Consecuencias
Cualquier integración futura con un control operable post-conexión (pausar, intervalo,
etc.) que tenga también una pantalla de negocio propia debe seguir este patrón: editar en
la pantalla de negocio, solo-lectura + link en el catálogo de Integraciones. No añadir un
segundo editor "por comodidad" sin revisar primero si ya existe una pantalla de negocio
para ese canal.
