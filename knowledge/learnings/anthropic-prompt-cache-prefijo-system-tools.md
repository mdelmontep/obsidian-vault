---
title: anthropic prompt caching cachea por prefijo — cachear solo system+tools deja el historial sin cachear
date: 2026-05-27
source: claude-code-session
tags: [claude-api, anthropic, caching, coste, copiloto]
---
`cache_control: {type:'ephemeral'}` cachea TODO el prefijo hasta el breakpoint. Orden real de render: `tools` → `system` → `messages` (breakpoint en el último bloque de `system` cachea tools+system juntos).

Campo variable (fecha del día, idioma, uuid) dentro de `system` → rompe el cache de system Y de los tools → tokens completos. Volátil al final, estable delante; o asume bust diario/por-idioma.

GOTCHA (FacturaIA copiloto, PR #894 2026-07-14): cachear solo system+tools NO cachea el HISTORIAL, que es lo que crece (turnos, tool_results, imágenes). En un runner multi-turno/agéntico añade un 3er breakpoint MÓVIL en el último bloque del último mensaje, recolocándolo antes de cada llamada al SDK y limpiando el previo (máx 4 breakpoints/request; ventana de lookback 20 bloques). Cachea la conversación entre iteraciones del loop y entre turnos.

Observabilidad: `usage.cache_read_input_tokens` (~0,1×) y `cache_creation_input_tokens` (~1,25×); `input_tokens` ya EXCLUYE lo cacheado → cacheRead alto + input bajo = caché OK. No viene en la respuesta al cliente salvo que lo añadas: loguéalo en servidor. TTL 5 min. SDK `@anthropic-ai/sdk` ≥0.90: `system` = array TextBlockParam con cache_control.
