---
title: facturaia módulo stock/inventario
date: 2026-06-01
source: claude-code-session
tags: [facturaia, stock, inventario, rama]
---

# TuFacturaIA — Módulo Stock / Inventario

Estado al cierre 2026-06-01. **Rama `feat/stock`** (checkout `/Users/manueldelmonte/facturaia-stock`). NO está en `main` ni en prod.

## Qué es
Módulo de inventario como **add-on de pago** (12,90€/mes). Extiende `catalogo_servicios` (NO tabla nueva) + ledger append-only `stock_movimientos` como fuente de verdad; `stock_actual` es proyección cacheada en la misma transacción. Valoración PMP (PGC NRV 10ª), IVA fuera del coste.

## Hecho (Fases A-C, todo verde lint/typecheck/build)
- **Migraciones 205-210**: 205 columnas stock en catalogo_servicios · 206 `stock_movimientos` (RLS) · 207 `lineas_factura.catalogo_id` · 208 motor (`aplicar_movimientos_stock`, `recompute_stock`, trigger AFTER INSERT lineas_factura statement-level + trigger AFTER UPDATE facturas, RPC `create_factura_with_lineas` recreado con catalogo_id) · 209 registro feature add-on · 210 RPC `ajustar_stock_manual`.
- **Código**: `lineas_factura.catalogo_id` propagado (create-document.ts, anular-factura.ts, generar-view.tsx ×3 caminos, PATCH /api/facturas/[id], v1 schemas). UI `/inventario` (listado, ficha+historial, ajuste manual), endpoints `/api/stock/*`, módulo en catalog.ts, icono `box`, EstadoPill estados stock, métricas, gating dual (server+cliente+BD).
- **Auditado en composición** por 3 agentes → 6 bugs corregidos (2 bloqueantes: anulación no reponía stock por catalogo_id no propagado; escritura cross-org por join sin org_id).
- **Smoke validado end-to-end** en proyecto Supabase de pruebas cloud `vtovkkrcybstlzpgqsaq` (`facturaia-stock-test`, free, desechable): alta con stock inicial (apertura +10) → emitir factura (venta −2) → anular (devolucion +2) → 2ª venta (−8, disparó "bajo mínimo") → ajuste manual (+5). Invariante `SUM(ledger) == stock_actual` cuadra siempre.

## Commits en feat/stock
- `d5ff1ed` feat(stock) módulo A-C (renumerado 205-210) + `e8858aa` merge origin/main (pusheados).
- `2d972ff` fix(onboarding) series B/F — **mig 211** — SIN pushear.

## Pendiente
1. **Push** de `2d972ff` a `feat/stock`.
2. **Merge a main + `supabase db push` a prod** (desde main limpio) + smoke prod. Incluye mig 211.
3. **Fase D** (compras + IA): el OCR de recibidas NO extrae líneas (solo cabecera) → requiere sprint OCR de líneas estructuradas. Matching IA = fuzzy `pg_trgm` + confirmación (no pgvector). Limitación: presupuesto→factura y voz no propagan catalogo_id todavía; `auto_descontar` marcado implemented:false (no cableado).
4. **Fase E**: openapi/docs de `/api/v1/stock/*`.
5. **UX a pulir**: el CTA "Activar control de stock" de `/inventario` lleva al catálogo de Ajustes (que NO tiene campos de stock; los campos están en el modal de alta rápida de `/generar`); validador de teléfono rechaza móvil español válido.

## Entorno de pruebas (cómo retomar)
- Proyecto test `vtovkkrcybstlzpgqsaq`, `.env.local` del checkout apunta ahí (claves + db password). `npm run dev` → :3001 (3000 ocupado).
- Saltar OTP teléfono: `UPDATE profiles SET phone_verified_at=now()` del user. Activar módulo: `INSERT org_features (org_id, feature_id='stock', enabled=true, source='manual')`.
- Sin Docker local (Supabase local no disponible); por eso se usó proyecto cloud de pruebas. Borrar el proyecto al terminar.

## Hallazgo colateral (ya corregido, mig 211)
El onboarding creaba series A,R,P,T pero NO B (abonos) ni F (proformas) → clientes NUEVOS en prod no podrían anular ni hacer proformas. Ver [[feature-recurso-por-org-actualizar-onboarding-no-solo-backfill]]. Y la colisión de numeración detectada: [[supabase-db-push-colision-numeracion-migraciones-rama-stale]].
