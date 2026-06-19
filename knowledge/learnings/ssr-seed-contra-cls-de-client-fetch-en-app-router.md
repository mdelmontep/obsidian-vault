---
title: ssr-seed contra cls de datos fetcheados client-side en app router
date: 2026-06-19
source: claude-code-session
tags: [next, performance, cls, react]
---
Síntoma: un provider/hook que fetchea client-side (`ready` false→true, o items
[]→datos) hace que el nav del sidebar o widgets aparezcan/crezcan TRAS el primer
paint → empujan el layout → CLS alto y variable (peor en redes lentas).
Fix: el server component (layout/page) precomputa los datos y los pasa como
`initialData` → el cliente monta con `ready=true` y el contenido en su sitio desde
el primer paint.
- fetch + resolve en un módulo COMPARTIDO server/cliente (misma query, misma
  transformación) → cero divergencia, hidratación idéntica. Props serializables.
- El refetch cliente (refresh) se mantiene; el seed solo arregla el primer paint.
- PARALELIZA el fetch server con las demás queries del layout (Promise.all) o
  cambias CLS por TTFB.
- NO reservable con altura fija si el contenido es condicional/variable (deja hueco):
  ahí el seed es la única salida limpia, o se acepta el salto.
Caso real FacturaIA #395: FeatureProvider (nav sidebar) + bandeja de ingesta.
Medir antes/después: [[medir-cwv-autenticado-sin-lighthouse]].
