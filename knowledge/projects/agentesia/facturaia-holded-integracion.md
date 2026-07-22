---
title: FacturaIA — Integración Holded (v2, pull-only) — CERRADA
date: 2026-07-22
source: claude-code-session
tags: [facturaia, holded, integraciones, sync, erp, incidente]
---

# Integración Holded — CERRADA, pull-only, en prod

**Estado final (2026-07-07): viva en prod, pull-only.** Contactos/productos/gastos bajan de Holded a TuFacturaIA cada 15 min; TuFacturaIA nunca escribe en Holded. `HOLDED_ENABLED=true`. Runbook operativo (incluye el incidente completo) en `docs/architecture/holded-runbook.md`.

## Import de facturas recurrentes (migración de cliente) — EN PROD (4 PRs, 2026-07-22)

Capacidad nueva, distinta del pull continuo de arriba: import **one-shot** (admin-only, disparado a mano) de las recurring-invoices de Holded hacia `facturas_recurrentes` — para cuando un cliente que llevaba sus cuotas en Holded migra a TuFacturaIA. Mig 546 (`holded_recurrentes_import`, RLS por rol, no service-role-only — a diferencia de `holded_entity_map` este flujo lo revisa un humano fila a fila). Cada recurrente importada se crea **siempre** `pausada`+`modo_emision:'revision'` (nunca activa/auto), para no facturar dos veces si Holded sigue corriendo en paralelo durante la migración.

- **#1152** feature completa (client.ts recurring-invoices, matching de cliente reusando `pull.ts`, mapeo de cadencia, UI de revisión en `/recurrentes`).
- **#1153** fix de bloqueante real hallado en `/fia-cierre`: reimportar pisaba en silencio una vinculación manual de cliente ya hecha.
- **#1154** avisos del cierre: tooltip de "Confirmar" deshabilitado no se mostraba (ni por hover ni por teclado), auditoría en descartar/vincular-cliente, copy, `manual-admin.md` §44.5b.
- **#1155** aparte: subida de touch target 44px en `Button size="sm"` (cambio de sistema, 159 archivos, QA visual en 3 pantallas densas).

Bug real encontrado y corregido durante el smoke: `periodicity` de Holded usa códigos cortos (`m`/`q`/`a`...), no `monthly`/`quarterly`/`yearly` — ver [[holded-api-periodicity-codigos-cortos-no-nombres-ingles]]. Smoke real contra la sandbox (129 recurring-invoices, 100% cliente matched, cadencia mapeada tras el fix) + confirmación real de una fila (verificada `pausada`+`revision` correcta en `facturas_recurrentes`). Pendiente: que el propio Manuel/cliente revise y confirme el resto de filas reales desde la UI.

## Bug rol cliente/proveedor — PR #908 (2026-07-15, pendiente smoke prod)

El pull metía TODOS los contactos en `clientes` sin mirar el rol (sandbox: 409 → 0 proveedores). Ironía: los mismos `client_record`/`supplier_record` que el push perdía en el incidente eran la señal de rol que el pull ignoraba. Fix: `contactRoles()` deriva el rol real (record > type; cubre doble rol); `pullContactRole` rutea a `clientes`/`proveedores`; `holded_entity_map.entity_type` → `contact_client`/`contact_supplier` (mig 462 amplía el CHECK). Reconciliación de lo ya importado: `scripts/reconcile-holded-roles.ts` (idempotente) — aplicada al sandbox + mig 462 en remoto. **Pendiente:** smoke prod del próximo pull (debe ser no-op limpio). Ver [[holded-v2-contacto-rol-por-record-no-por-type]].

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
