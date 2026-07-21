---
title: "Obras: loaders que abren N queries por presupuesto/parte → Promise.all, no bucle serial"
date: 2026-07-21
source: claude-code-session
tags: [obras, rendimiento, n+1, supabase, facturaia]
---
Patrón recurrente en el módulo Obras (sale como "reservas · rendimiento" en varios `/fia-cierre`): un loader recorre una lista (presupuestos ligados a una obra, partes, líneas) y por cada elemento hace `await` a un lector que a su vez abre ~6 queries. En serie son N×6 round-trips secuenciales (peor caso ~600 con el cap de 100 presupuestos/obra); la latencia es la SUMA, no el máximo.

Fix: `Promise.all(lista.map(x => lectorPorElemento(x)))` y luego filtrar/mapear. `Promise.all` sobre un `map` **preserva el orden** del array, así que el orden funcional (p.ej. ROL_ORDER: base primero) se mantiene sin re-ordenar, igual que el bucle. El `.filter(Boolean)` posterior también conserva el orden al descartar los null. El cliente Supabase admite peticiones concurrentes sin problema.

Caso: `getObraArbol` (`src/lib/obras/obra-arbol-db.ts`, P1.4 programa "Toda la obra") — bucle `for...await` sobre `ordenadas` → `Promise.all`. Wall-clock pasa de N×(6 queries) a 1×(6 queries) aprox.

Regla: en Obras, antes de cerrar un loader, pregúntate si el `await` está dentro de un `for/map` sobre datos de BD → paraleliza salvo dependencia real entre iteraciones. Relacionado con [[obras-endpoint-service-role-sin-audit-ni-tope]] (tope de ventana en agregados).
