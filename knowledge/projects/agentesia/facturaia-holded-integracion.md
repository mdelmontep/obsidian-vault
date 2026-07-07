---
title: FacturaIA — Integración Holded (v1) estado + fase 2
date: 2026-07-07
source: claude-code-session
tags: [facturaia, holded, integraciones, sync, erp]
---

# Integración Holded (bidireccional)

**Estado (2026-07-07 tarde):** smoke v1 **6/6 verde** contra la API viva con key real, PERO **giro a v2 en curso** — v1 está *archivada* por Holded, una sesión paralela reescribe el provider a v2 sobre la misma rama. Esta sesión (worktree `.claude/worktrees/holded`) **se retiró de la rama** para no colisionar. Detalle abajo en §GIRO a v2.

PR **#787** abierto (sin merge) — rama `feat/holded-integration`. 9 slices con TDD (92 tests), auditado por 2 agentes. **API v1** (header `key`, `api.holded.com/api/invoicing/v1`). Migraciones **440-444**. Gate `HOLDED_ENABLED` (dark hasta encenderlo). Runbook en repo: `docs/architecture/holded-runbook.md`. Compila limpio (lint+typecheck+build exit 0, 2026-07-07).

## Qué está hecho (v1)
- Provider `holded` (`src/lib/integrations/providers/holded/`): client, mappers+contentHash, push/pull, conflict (LWW empate→FacturaIA), config.
- BD: `holded_entity_map` + `holded_sync_queue` (outbox) + RPCs SKIP LOCKED + zombie sweep + triggers (clientes/proveedores/catálogo/facturas con filtros de estado). RLS deny-all + REVOKE. `updated_at`+trigger en clientes/catálogo.
- Bidireccional: contactos + productos. Emitidas **push-only** (Veri*Factu intacto). Gastos: pull **create-only**. Anti-eco por hash + borrado de fila auto-encolada en pull de gastos.
- Crons `holded-sync-dispatcher` (1min) + `holded-pull` (15min) en CRON_REGISTRY. Endpoint "Sincronizar ahora" + toggles UI (`HoldedSyncRow`).
- Docs: runbook + secciones manual usuario/admin. Smoke harness `scripts/smoke-holded-api.mjs`.

## Pendientes antes de encender en prod
1. ~~Smoke API v1~~ **HECHO (2026-07-07): 6/6 verde** con key real (cuenta trial — Holded NO tiene sandbox). Confirmado contra la API viva: header `key`, base `/invoicing/v1`, campos `code`=NIF/`vatnumber`/`billAddress`, respuesta escritura `{status:1,id}`. Contacto de prueba creado, leído, actualizado y **borrado** (cuenta limpia). El mapper **no necesitó ajustes**. *(Ver §GIRO a v2: el smoke E2E de app queda pendiente del cierre de la reescritura.)*
2. `gen:types` tras aplicar migs (elimina cliente MiniDb local `holded-db.ts`; opcional).
3. Alta de los 2 crons en Dokploy schedules + `HOLDED_ENABLED=true` (recrear contenedor) + `supabase db push --linked` (migs 440-444).

## GIRO a v2 + coordinación de 2 sesiones (2026-07-07)

- **Hallazgo**: la API v1 (`/invoicing/v1`, header `key`) está **archivada** por Holded — "conservada solo para integraciones existentes; las nuevas deben usar v2" (Bearer, `/api/v2`). Confirmado en developers.holded.com por la sesión paralela. El PR #787 está escrito **enteramente** contra v1 (no un mismatch de campos): decisión de arranque, no bug.
- **Decisión (1) — versión**: nacer sobre API deprecada = deuda desde el día 1. Manu: "lo correcto y profesional" → **reescribir a v2 ahora**. Alternativa no elegida (pero válida): shipear v1 hoy (funciona, smoke 6/6, auditado) y migrar a v2 como la fase 2 que ya estaba planificada.
- **Alcance de la reescritura a v2** (estimación sesión paralela): `client.ts` (auth Bearer, base URL, ruteo de documentos por tipo, paginación cursor en vez de `?page`) ~150-250 LOC + los **13 ficheros de `__tests__/`** (mockean wire format v1: `status/id`, `?page`, header `key`) + `scripts/smoke-holded-api.mjs` retarget. `mappers.ts`/`types.ts` probablemente estables (desacoplados del wire). **Migs 440-444 NO afectadas** (schema FacturaIA). Riesgo: el shape de **escritura** v2 no está documentado (consola interactiva, no scrapeable) → hay que descubrirlo contra la cuenta trial real.
- **Coordinación crítica**: las 2 sesiones estaban sobre la **misma rama `feat/holded-integration` / PR #787** = riesgo de machacar HEAD. Esta sesión (la del smoke v1) **se retiró de la rama**. La otra (en el host Dokploy) es la *maker* del giro v2.
- **Decisión (2) — reparto de sesiones (PENDIENTE)**: **A** handoff total a la otra sesión · **B** esta sesión de *checker* del diff v2 (maker/checker) · **C** otra tarea FacturaIA.
- **Keys**: v1 (trial, usada en el smoke que pasó) y v2 (`pat_…`, entregada) están en la conversación, **no en el vault**. Si se consolidan → item 1Password + pointer en hub `Credenciales`.

## Fase 2 — lo que Holded ofrece y NO usamos (decisión consciente v1)

| Capacidad Holded | ¿Usamos? | Impacto de NO usarla |
|---|---|---|
| **API v2** (Bearer/OAuth, actual) | ❌ v1 (obsoleta pero mantenida) | Deuda futura: v1 marcada "obsoleta", riesgo de retirada |
| **Webhooks tiempo real** (v2: ventas, compras, contactos, productos, stock) | ❌ polling 15min | **Gap más grande**: latencia + pull de gastos create-only (no detecta *updates* de un purchase en Holded) |
| **Stock / almacenes** | ❌ | FacturaIA tiene módulo stock; no sync de niveles con warehouses Holded |
| **Contabilidad** (asientos, cuentas, impuestos) | ❌ (solo documentos) | Para gestoría, el sync a nivel de asiento es "la joya"; llegamos a documento |
| Series numeración, tarifas, remesas SEPA, recurrentes, tesorería/bancos | ❌ | Fuera del alcance acordado (contactos/productos/documentos) |
| Rate limits ("tres ventanas deslizantes") | ⚠️ parcial | Manejamos 429→backoff, sin honrar `Retry-After` ni throttle proactivo |

**Prioridad de fase 2 (por valor):** (1) **Webhooks v2 inbound** — convierte el pull de create-only a tiempo real *con updates*; mantener v1 para push/CRUD y v2 solo para webhooks = "lo mejor de ambos". (2) Migrar CRUD a v2 cuando esté rodada (~1 mes de vida). (3) Stock↔warehouses. (4) Honrar `Retry-After`.

**Decisión pendiente (Manu):** ¿fase 2 webhooks v2 como PRD/slices nuevos ahora, o dejarlo como NEXT tras cerrar v1 con el smoke?

## Prompt para siguiente sesión

> Retoma la integración Holded (PR #787, rama `feat/holded-integration`, worktree `.claude/worktrees/holded`). Estado en [[facturaia-holded-integracion]]. Pasos para cerrar v1: (1) con la API key sandbox de Holded que te doy, corre `HOLDED_API_KEY=... node scripts/smoke-holded-api.mjs` y ajusta el mapper si algún campo v1 no casa (code/vatnumber/billAddress); (2) si el smoke pasa, confírmame para mergear el PR #787, aplicar migs 440-444 (`supabase db push --linked`), dar de alta los 2 crons en Dokploy y `HOLDED_ENABLED=true`; (3) smoke E2E real: conectar Holded en Ajustes→Integraciones, crear cliente en FacturaIA→verlo en Holded, editar en Holded→verlo bajar, emitir factura→verla en Holded, crear purchase en Holded→verla como gasto. Luego decidimos **fase 2**: webhooks v2 (tiempo real + updates de gastos, el gap más grande), migración CRUD a v2, y stock↔warehouses — ver la tabla de "Fase 2" en la nota. Todo el diseño y decisiones cerradas están en `issues/holded-integration-prd.md`.
