---
title: anthropic prompt caching cachea por prefijo — un campo variable en `system` invalida también el cache de los `tools`
date: 2026-05-27
source: claude-code-session
tags: [claude-api, anthropic, caching, coste]
---
`cache_control: {type:'ephemeral'}` cachea TODO el prefijo del request hasta el breakpoint. Orden del prefijo: `system` → `tools` → `messages`.

Si metes un campo que cambia (fecha del día, idioma del user) dentro de `system`, rompes el cache de system Y de los `tools` (van después en el prefijo) → pagas tokens completos. Para cachear los tools de forma estable, el contenido variable debe ir en el primer mensaje de usuario, NO en system; o asume bust diario/por-idioma.

TTL por defecto 5 min: en multi-turno (loop de tools + turnos seguidos en <5 min) el hit es el caso común y ahí vive el ahorro. Poner el breakpoint en el último tool cachea system+tools juntos. SDK `@anthropic-ai/sdk` ≥0.90: `system` admite array de TextBlockParam con `cache_control`.
