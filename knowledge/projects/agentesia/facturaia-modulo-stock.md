---
title: facturaia módulo stock/inventario
date: 2026-06-02
source: claude-code-session
tags: [facturaia, stock, inventario, rama]
---

# TuFacturaIA — Módulo Stock / Inventario

Estado al cierre **2026-06-02**. Dos frentes:
- **Fases A-C → EN MAIN + PROD** (módulo base, invisible para clientes).
- **Fase D (compras + IA) → rama `feat/stock-compras`** (checkout `/Users/manueldelmonte/facturaia-stock`, dev :3001). NO en main/prod.

## Qué es
Add-on de pago (12,90€/mes). Extiende `catalogo_servicios` (NO tabla nueva) + ledger append-only `stock_movimientos` (fuente de verdad); `stock_actual` es proyección cacheada en la MISMA transacción. Stock se mueve por **transición de estado** de `facturas` (no en createDocument): triggers AFTER INSERT lineas_factura (statement-level) + AFTER UPDATE facturas. Valoración **PMP** (PGC NRV 10ª), IVA fuera del coste, coste EUR con tipo_cambio congelado. Matching IA = fuzzy `pg_trgm` + **confirmación humana (nunca auto-aplica** — contamina PMP irreversible).

## EN MAIN + PROD (Fases A-C) — 2026-06-01
- **PR #130 (commit `19214b3`)** mergeado. **Migs 205-212 aplicadas a prod**: 205 columnas stock · 206 `stock_movimientos` · 207 `lineas_factura.catalogo_id` · 208 motor ventas (`aplicar_movimientos_stock`+triggers+`create_factura_with_lineas`) · 209 feature add-on · 210 `ajustar_stock_manual` · 211 fix series B/F onboarding · **212 `features.disponibilidad`** (oculto/proximamente/activo).
- **Stock en prod = `disponibilidad='proximamente'` → invisible** (sidebar "Inventario · Próximamente" no clickable; `/inventario` redirige salvo superadmin). Control genérico por módulo en **`/admin/modules`**.
- **Para ACTIVAR a un cliente**: `/admin/modules` → stock → "Activo" + dar el add-on a su org (`org_features`).
- Auditado en composición (3 agentes, 6 bugs corregidos; 2 bloqueantes: anulación no reponía stock por catalogo_id no propagado; escritura cross-org por join sin org_id). Smoke ventas A-C validado en test cloud.

## Fase D — EN MAIN (2026-06-04), falta `db push`
Mergeada vía **PR #137** (`feat/stock-compras`→main) + **PR #139** fix renumber. + UX crear producto (commit `949ed4e`).
**Migs renumeradas 213-216 → `223-226`** (colisión: billing mergeó 213-218, fase3 mergeó 219). ✅ **APLICADAS A PROD 2026-06-04** (`db push` OK; `pg_proc` confirma funciones `aplicar_movimientos_stock`/`aprobar_recibida_con_lineas`/`sugerir_productos_por_descripcion` + triggers `trigger_stock_lineas_insert`/`trigger_stock_emit`; cache PostgREST recargado vía `NOTIFY pgrst`). 223=compras+PMP · 224=matching · 225=aprobar_recibida_con_lineas · 226=bandeja_factura_id (idempotente, ya existía por drift).

- **D2 · mig 213** motor compras: recibida factura→ENTRADA + PMP incremental `(stock·pmp + qty·coste_eur)/(stock+qty)`; recibida abono→salida; trigger ampliado a `sin_aprobar→pendiente`. ✅ **VALIDADO** test (compra 5@8 sobre 7@5 → 12@6.25 exacto).
- **D3 · mig 214** matching: índice gin trigram + RPC `sugerir_productos_por_descripcion` (`word_similarity(proveedor_normalizado(nombre), proveedor_normalizado(desc))` + operador `nombre <% desc`). ✅ **VALIDADO**.
- **D1-repo · `5012795`** prompt OCR (`ocr-process/route.ts`) amplía a `lineas:[{descripcion,cantidad,precio_unitario}]` + `sanitizeLineas`. Verde, NO probado con LLM real.
- **D5 · mig 215 + ruta + endpoint** (`45285fa`): RPC **`aprobar_recibida_con_lineas`** (atómico SECURITY DEFINER: inserta `lineas_factura` con catalogo_id confirmado + reconcilia Σlíneas vs base tol 1% [raise `descuadre_lineas|suma|base`] + transiciona sin_aprobar→pendiente; el trigger 213 mueve stock/PMP; idempotente). `/api/recibidas/[id]/aprobar`: rama stock (org con feature + bandeja.datos_extraidos.lineas) llama al RPC, **copia FX ANTES** de mover stock (PMP correcto en divisa), mapea descuadre→422; path legacy SIN líneas intacto. + endpoint `/api/stock/sugerencias`. ✅ **RPC VALIDADO por smoke SQL** (12→17, PMP 7.3529; descuadre 40 vs 50 bloqueado).
- **D4 · UI** (`45285fa`): `details-panel.tsx` sección "Líneas detectadas" (selector producto por línea con sugerencias preseleccionadas + reconciliación en vivo Σlíneas vs base). `ingesta-view.tsx`: carga catálogo+sugerencias solo si feature stock, persiste catalogo_id en `datos_extraidos.lineas`, toast descuadre. Construido, NO validado por UI/OCR real.

### Decisiones de diseño Fase D (clave para retomar)
- Las líneas se insertan **AL aprobar** (dentro del RPC atómico) → invariante "recibida sin_aprobar SIN líneas" se mantiene.
- Trigger verifactu 091 hace `RETURN` si `tipo<>'emitida'` → insertar líneas en recibida **NO pisa base/total** ni recalcula huella. Verificado.
- Reconciliación **bloquea** (no avisa) si descuadra >1% (petición user "profesional, funcional"). Líneas con producto mueven stock; "sin asignar" = texto libre (no toda línea es stock: portes, descuentos).
- `created_via` es NOT NULL en facturas (enum web|voice|api|email|ocr|portal; en psql hay que pasarlo, la app lo rellena por contexto auth).

## Pendiente Fase D
1. ~~**D1-n8n**~~ ✅ **HECHO 2026-06-04** (vía API n8n, PUT workflow). Recableados **DOS** nodos OCR inline del workflow WhatsApp `pqSWkDIHqmSVHotB` al webhook SSOT `factura-ocr` (responseMode lastNode → firma HMAC → `ocr-process`): (a) `Disparar OCR` single-org → ahora `httpRequest` con retry×3; (b) `Procesar Ingesta Pendiente` multi-org → orquestación (storage+factura+bandeja) preservada, solo el bloque OCR delegado al webhook. Eliminado prompt inline duplicado + `OPENAI_API_KEY` de ambos (solo queda en `Transcribir Whisper`, voz). Backup pre-cambio en `n8n-backups/facturaia/pqSWkDIHqmSVHotB_..._pre-D1ocr_2026-06-04.json`. **active=true, 144 nodos, settings/conexiones intactas.** ✅ **VALIDADO EN VIVO 2026-06-04** mono-org y multi-org (ejecuciones webhook OCR `success`). Incidente previo: rompí prod ~10 min (`return` usaba var `bandeja` eliminada → ReferenceError); revert al backup + harness de runtime con mocks + re-deploy. Lección → [[n8n-code-node-validar-runtime-con-mocks-no-solo-sintaxis]].
2. ~~Validación E2E UI D4/D5~~ motor validado E2E (demo real: stock 12→15, PMP 7.00). E2E browser de la UI de stock = **gate pre-activación** (módulo `proximamente`, nadie lo ve aún).
3. ~~UX crear producto desde selector~~ ✅ **HECHO** (commit `949ed4e`): opción "+ Crear producto nuevo" reutiliza `POST /api/catalogo/productos` + auto-asigna.
4. ~~Merge + db push~~ ✅ **COMPLETO**: merge en main + `db push` 223-226 aplicado a prod 2026-06-04 (verificado `pg_proc` + cache recargado). Ojo worktrees: `facturaia-stock` tenía `main` tomado → `git checkout --detach` ahí para liberarlo antes del `db push` desde `facturaia` (linkado prod).
5. Fase E openapi/docs `/api/v1/stock/*`. Limitaciones previas: presupuesto→factura y voz no propagan catalogo_id; `auto_descontar` implemented:false.

## Drift de esquema detectado + fix (2026-06-02)
**`bandeja_ingesta.factura_id`** existe en PROD (uuid null, FK→facturas(id) sin ON DELETE, sin índice) y el código la usa (aprobar recibida, delete bandeja), pero **ninguna migración del repo la creaba** → aplicada fuera del control de versiones. Una BD regenerada desde migraciones (proyecto test) no la tenía → bandeja rota. Fix: **mig 216_bandeja_factura_id.sql** idempotente (`ADD COLUMN IF NOT EXISTS`, fiel a prod), commit `b57a0c7`, no-op al aplicar a prod. **PENDIENTE**: barrer el resto de tablas comparando esquema prod vs migraciones por si hay más drift.

## Entorno de pruebas + demo Fase D (cómo verlo en :3001)
- Proyecto test `vtovkkrcybstlzpgqsaq` (`facturaia-stock-test`, desechable). `.env.local` del checkout apunta ahí (claves + `SUPABASE_DB_PASSWORD`). Conexión psql: `host=aws-0-eu-west-1.pooler.supabase.com port=5432 user=postgres.vtovkkrcybstlzpgqsaq dbname=postgres sslmode=require`. Migs 199-216 aplicadas. `db push --linked` lo bloquea el clasificador (falso positivo prod) → el user lo corre con `!`.
- **Demo montada (2026-06-02)** para recorrer D4/D5 por UI: login `test@facturaia.dev` (org `7d9a2cfe-14ec-4268-a58f-37522915ffef`, OTP ok, NO superadmin). En test: `features.stock.disponibilidad='activo'`; 2 productos (producto test 12@6.25, Folios A4 50@3.00); recibida `DEMO-001` sin_aprobar + bandeja `listo` (`factura-demo.pdf`) con `datos_extraidos.lineas=[Producto test edicion grande(3@10), Portes envio(1@20)]` sin catalogo_id. Flujo: Inventario (ver productos) → Ingesta → abrir demo → asignar L1→producto test (sugerido 100%), L2 sin asignar → suma 50 cuadra base 50 → Aprobar → producto test 12→15, PMP 7.00 + movimiento compra.
- Saltar OTP en test: `UPDATE profiles SET phone_verified_at=now()`. Activar módulo a una org: `INSERT org_features (org_id, feature_id='stock', enabled=true, source='manual')`.

## Refs
Colisión numeración migraciones rama stale: [[supabase-db-push-colision-numeracion-migraciones-rama-stale]]. Onboarding por-org no solo backfill: [[feature-recurso-por-org-actualizar-onboarding-no-solo-backfill]].
