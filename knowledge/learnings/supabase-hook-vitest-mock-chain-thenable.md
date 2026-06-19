---
title: mock chain thenable para hooks supabase en vitest
date: 2026-06-19
source: claude-code-session
tags: [testing, vitest, supabase, react]
---

El chain Supabase es PromiseLike (thenable) además de builder encadenable.
Queries secundarias (autores, bandeja, movs) se awaitean directamente sin .range().

Patrón del mock:
- `basePromise = Promise.resolve({ data: [], count: null, error: null })`
- El chain implementa `then/catch/finally` delegando a basePromise
- Terminal (query principal): `mockRange` retorna `{ data, count, error }`
- Chainables devuelven `this`: `for (const k of [...]) chain[k].mockReturnValue(chain)`

La distinción clave: `mockRange` es el terminal paginado; el resto awaitea el thenable.
`beforeEach`: `vi.clearAllMocks()` + `mockRange.mockResolvedValue({data:[],count:0,error:null})`.

`mockFrom = vi.fn().mockReturnValue(mockChain)` — todas las tablas devuelven el mismo chain;
distinguir por tabla solo si el test lo requiere.

Ver: `use-facturas-data.test.ts`, `use-presupuestos-data.test.ts`.
