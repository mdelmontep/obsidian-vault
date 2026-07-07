---
title: FacturaIA — Integración Holded (v1) estado + fase 2
date: 2026-07-07
source: claude-code-session
tags: [facturaia, holded, integraciones, sync, erp]
---

# Integración Holded (bidireccional)

**Estado (2026-07-07):** PR **#787** abierto (sin merge) — rama `feat/holded-integration`, worktree `.claude/worktrees/holded`. 9 slices con TDD (92 tests), auditado por 2 agentes. **API v1** (header `key`, `api.holded.com/api/invoicing/v1`). Migraciones **440-444**. Gate `HOLDED_ENABLED` (dark hasta encenderlo). Runbook en repo: `docs/architecture/holded-runbook.md`.

## Qué está hecho (v1)
- Provider `holded` (`src/lib/integrations/providers/holded/`): client, mappers+contentHash, push/pull, conflict (LWW empate→FacturaIA), config.
- BD: `holded_entity_map` + `holded_sync_queue` (outbox) + RPCs SKIP LOCKED + zombie sweep + triggers (clientes/proveedores/catálogo/facturas con filtros de estado). RLS deny-all + REVOKE. `updated_at`+trigger en clientes/catálogo.
- Bidireccional: contactos + productos. Emitidas **push-only** (Veri*Factu intacto). Gastos: pull **create-only**. Anti-eco por hash + borrado de fila auto-encolada en pull de gastos.
- Crons `holded-sync-dispatcher` (1min) + `holded-pull` (15min) en CRON_REGISTRY. Endpoint "Sincronizar ahora" + toggles UI (`HoldedSyncRow`).
- Docs: runbook + secciones manual usuario/admin. Smoke harness `scripts/smoke-holded-api.mjs`.

## Pendientes antes de encender en prod
1. **Smoke E2E real** — necesita **API key de cuenta Holded sandbox** (validar que los campos v1 reales casan: `code`=NIF, `vatnumber`, `billAddress`, header `key`). Correr `HOLDED_API_KEY=... node scripts/smoke-holded-api.mjs`. Bloqueo: Manu consigue la key (¿pedir a Borja?).
2. `gen:types` tras aplicar migs (elimina cliente MiniDb local `holded-db.ts`; opcional).
3. Alta de los 2 crons en Dokploy schedules + `HOLDED_ENABLED=true` (recrear contenedor) + `supabase db push --linked` (migs 440-444).

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
