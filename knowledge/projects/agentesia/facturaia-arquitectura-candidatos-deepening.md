---
title: facturaia — candidatos de deepening arquitectónico
date: 2026-06-27
source: claude-code-session (skill improve-codebase-architecture)
tags: [cliente, facturaia, arquitectura, refactor, roadmap]
---

# TuFacturaIA — Candidatos de deepening (módulos shallow → profundos)

Raíz común de #1/#2/#4: **no hay capa de dominio entre los puntos de entrada (route handlers, tools, voz) y PostgREST** → cada sitio reimplementa resolve/validar/auditar acoplado al builder de Supabase. El #2 estableció el patrón replicable: módulo de dominio con **resultado discriminado sin throw** + tests al límite + HTTP solo en el borde.

| # | Candidato | Estado | Profundidad | RFC |
|---|---|---|---|---|
| 2 | find-or-create cliente/proveedor | ✅ CERRADO (deployado, smoke E2E verde) | exploración profunda + 3 diseños | `issues/rfc-find-or-create-contacto-nif-opcional.md` |
| 1 | 45 tools copiloto shallow | ⏳ solo identificado | — | — |
| 3 | seam emisión voz↔web (núcleo) | ⏳ solo identificado | — | ⚠️ existe `issues/rfc-unificar-creacion-documentos.md` (previo, revisar vigencia) |
| 4 | lógica de negocio en route handlers | ⏳ parcial (la #2 quitó ~215 LOC de `pending-action/execute`) | — | — |

## #1 — Tools del copiloto (recomendado siguiente)
`src/lib/copiloto/tools/*` (46) + `registry.ts` + `runner.ts`. Cada tool reimplementa plomería: `resolveFactura()`/`resolvePresupuesto()` (~45 LOC ≈ idénticos en `marcarCobrada.ts:56`, `marcarPresupuestoAceptado.ts:50`, `anularFactura.ts`), `assertMarcable()`/`assertAceptable()`, `createAdminClient().from(...).eq('org_id',...)`, bloque `logAgentAction(...)`. ~1.300-1.500 LOC duplicados (≈20%). `marcarPresupuestoAceptado.ts` = 72% plomería / 22% lógica. Dep: cat 2/4 (mock builder). Impacto tests: ~15 suites con ~35 LOC boilerplate cada una (≈525 LOC). **Mayor volumen; el patrón del #2 aplica casi directo.**

## #3 — Seam emisión voz↔web (mayor riesgo)
`lib/documents/create-document.ts` (fuente única) vs `api/voice/generate/route.ts:471,539` (RPC `create_factura_with_lineas`/`create_presupuesto`) y `api/voice/convert-presupuesto/route.ts:310` (RPC `convertir_presupuesto_a_factura`). `calcularTotales()` + decisión H1 (reparto descuento global) reimplementados en `create-document.ts:232` y `voice/generate.ts:335,456`. Riesgo: divergencia silenciosa de totales/IVA/numeración voz↔web. Toca núcleo + RPCs → revisar el RFC previo antes de actuar.

## #4 — Lógica de negocio en route handlers (transversal, incremental)
Handlers gordos con dominio inline: `enrich-batch` (830), `voice/generate` (684), `conciliacion/movimientos/[id]` (593). ~79 `route.test.ts` mockean `withApiAuth` (40/79) + `createAdminClient` (70/79) con builders ad-hoc. Existe `createMockAdminClient()` (`documents/__tests__/__fixtures__/mock-admin-client.ts`) usado en 10 suites de `lib/` pero 0/79 route tests. Se cierra incrementalmente al hacer #1.

## Proceso por candidato (skill `improve-codebase-architecture`)
Encuadre del problema + 3 diseños de interfaz en paralelo (minimizar / unificar / ports&adapters) + recomendación + RFC en `issues/`. **No implementar sin OK.** Validar siempre: gates verdes + smoke E2E real (no solo unit).
