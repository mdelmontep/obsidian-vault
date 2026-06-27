---
title: bd como fuente de verdad vía cache en memoria: hidratar en lectura, no solo al escribir
date: 2026-06-27
source: claude-code-session
tags: [arquitectura, cache, nextjs]
---
Patrón: la BD es la fuente de verdad pero los getters son SÍNCRONOS y leen una
cache module-level. Si la cache solo se hidrata cuando alguien ESCRIBE (ej el
panel admin tras editar), en un proceso Node largo (Dokploy) arranca `null` tras
cada deploy y se queda null hasta la 1ª escritura → TODO el runtime resuelve por
el FALLBACK (ej la env var antigua), no por la BD. Bug silencioso: "BD fuente de
verdad" que en la práctica casi nunca se consulta.

Fix: `ensureCache()` lazy (hidrata si null) llamado al ENTRAR en cada consumidor
de LECTURA (checkout, webhook, change-plan…), no solo en el write. Las firmas
siguen síncronas; solo el entrypoint `await`-ea la hidratación.

Caso real: `stripe-plans.ts` — `refreshPriceCache` solo se llamaba dentro de
`createPriceForTarget` (escritura). Añadido `ensurePriceCache()` en los 4 flujos.
