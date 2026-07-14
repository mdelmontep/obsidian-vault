---
title: un hook con canal realtime Supabase de nombre fijo revienta si se monta dos veces
date: 2026-07-15
source: claude-code-session
tags: [supabase, realtime, react-hooks]
---
`supabase.channel('nombre-fijo')` devuelve el MISMO canal por nombre en el cliente. Si dos instancias del hook lo montan a la vez (p.ej. Sidebar + tabbar móvil), la 2ª hace `.on(...)` sobre un canal ya suscrito → `cannot add postgres_changes callbacks for realtime:<topic> after subscribe()` y crashea el árbol de React.

Fix: nombre único por instancia con `useId()` → `supabase.channel(\`nombre-${channelId}\`)`. Hace el hook reentrante y SSR-safe. Coste: N canales en vez de 1 (candidato a provider único si el nº de consumidores crece). Caso real: `useSidebarCounts` FacturaIA PR1 vista móvil.
