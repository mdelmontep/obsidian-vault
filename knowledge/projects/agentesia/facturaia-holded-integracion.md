---
title: FacturaIA — Integración Holded (v2, pull-only) — CERRADA
date: 2026-07-08
source: claude-code-session
tags: [facturaia, holded, integraciones, sync, erp, incidente]
---

# Integración Holded — CERRADA, pull-only, en prod

**Estado final (2026-07-07): viva en prod, pull-only.** Contactos/productos/gastos bajan de Holded a TuFacturaIA cada 15 min; TuFacturaIA nunca escribe en Holded. `HOLDED_ENABLED=true`. Sin pendientes. Runbook operativo (incluye el incidente completo) en `docs/architecture/holded-runbook.md`.

## Historial (5 PRs, en orden)

1. **#787** — integración original (9 slices, TDD). Escrita contra Holded API **v1** (`api.holded.com/api/invoicing/v1`, header `key`) — descubierto archivada por Holded a mitad de sesión ("las integraciones nuevas deben usar v2"). Reescrito `client.ts` a v2 (`Authorization: Bearer`, paginación cursor, endpoints separados por tipo de documento) en la misma sesión, antes de mergear.
2. **#789** — `database.types.ts`: #787 aplicó migraciones sin regenerar tipos (drift real detectado post-merge).
3. **#791** — `ApiKeyConnectModal`: el botón "Conectar" de providers `api_key` (Holded e iCloud Mail) solo mostraba un toast "próximamente" — el backend ya soportaba el flujo de 2 fases completo, faltaba el frontend.
4. **#792** — **eliminación completa del push** tras el incidente (ver abajo).
5. Todos mergeados vía `gh pr merge --admin` (CI de GitHub Actions a 0 pasos por billing bloqueado, decisión firme de no subir el límite).

## Incidente real de pérdida de datos (2026-07-07)

Al activar sync bidireccional en el smoke E2E (cuenta real de un cliente, Dani — no un trial vacío): el pull importó 409 contactos reales; el trigger de BD los re-encoló para push de inmediato; el push hacía `PUT` del contacto **completo** con solo el subconjunto de campos que mapea FacturaIA → Holded reemplazó el objeto entero, perdiendo `iban`/`swift`/`trade_name`/`client_record`/`supplier_record`/idioma/moneda en los 409 contactos. Dani confirmó después que los datos no se habían perdido realmente, pero la decisión ya estaba tomada.

**Decisión de Manuel: pull-only para siempre, no un merge no-destructivo.** Se eliminó el código de escritura por completo: `push.ts`, la ruta+cron `holded-sync-dispatcher`, los 4 triggers de BD que encolaban push (mig 445), los flags `holded_push_*` del allowlist y de la UI. `client.ts` solo expone lectura (`getContact`/`listAllContacts`/`listAllProducts`/`listAllDocuments`/`validateApiKey`).

**Lección aplicable a cualquier integración bidireccional nueva**: probar el ciclo completo (pull+push) primero contra una cuenta de verdad vacía, nunca contra una cuenta con datos de negocio reales, aunque sea "solo un smoke".

## Qué quedó (arquitectura final)

- `src/lib/integrations/providers/holded/`: `client.ts` (v2, solo lectura), `mappers.ts`, `pull.ts`, `conflict.ts` (LWW, empate→FacturaIA), `config.ts` (allowlist pull-only).
- BD: `holded_entity_map` + `holded_sync_queue` (infra de la antigua cola de push, inerte desde mig 445 — se conserva por el histórico del hash anti-eco que el pull sigue usando).
- Cron único `holded-pull` (15 min, polling con cursor — v2 no tiene webhooks propios en este momento).
- Nunca se crean/actualizan emitidas ni se empuja nada a Holded (numeración/Veri*Factu son fuente única de FacturaIA).

## Fase 2 (si se retoma en el futuro)

Si se quiere reintroducir push algún día: merge no-destructivo (GET antes de PUT, fusionar solo los campos conocidos) y probarlo primero contra una cuenta Holded vacía. Webhooks v2 (tiempo real) seguirían siendo la mejora de mayor valor sobre el polling actual. Stock↔warehouses y contabilidad a nivel de asiento, fuera de alcance.
