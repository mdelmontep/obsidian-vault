---
title: TuFacturaIA — Drive sync architecture
date: 2026-05-29
source: claude-code-session
tags: [facturaia, drive-sync, integraciones, outbox, postgres]
---

# Drive sync architecture

Subir PDFs de facturas emitidas/recibidas al Google Drive del cliente, en jerarquía año > tipo > mes, con idempotencia por hash, resistente a fallos transitorios, observable. Estado a 2026-05-29: backbone + UI desplegados, **cron n8n inactivo** bloqueado por mismatch `FACTURAIA_SERVICE_KEY`.

## Capas

1. **Trigger BD** (`trg_facturas_drive_sync`, mig 177+178)
   - `AFTER INSERT OR UPDATE OF documento_url ON facturas`.
   - Función helper `_enqueue_drive_sync_for_factura` `SECURITY DEFINER` resuelve `integration_connections` activa con `config.drive_upload_enabled=true`. Si no hay → no encola (silencio intencional).
   - LEFT JOIN clientes/proveedores para popular `cliente_proveedor_nombre`.
   - `INSERT ... ON CONFLICT (org_id, source_kind, source_id) DO UPDATE SET status='pending'` solo si `storage_path` cambió O `status` previo terminal.
   - Cubre los **8 puntos de código** que mutan `documento_url`: `createDocument`, `emitir-borrador`, `render-and-upload`, `update-presupuesto`, `process-attachments`, `/api/upload`, `whatsapp/ingesta`, `anular`.

2. **Tabla outbox** (`drive_sync_queue`, mig 177)
   - PK uuid + `(org_id, connection_id, source_kind, source_id, storage_path, filename)`.
   - `source_date date` + `cliente_proveedor_nombre text` (mig 178) → el worker los usa para resolver subcarpeta + filename.
   - `pdf_sha256` para detectar regeneraciones (hash distinto = re-upload PATCH; igual = skip).
   - `priority smallint` (5=realtime, 9=backfill) → backfill no bloquea sync nuevo.
   - **CHECK constraint** `storage_path LIKE org_id::text || '/%'` → defensa BD anti-IDOR cross-org.
   - Status lifecycle: `pending → processing → synced | failed | cancelled`.
   - RLS deny-all + sin policies → service-role only.

3. **RPC claim** (`claim_drive_sync_batch`, mig 177+179)
   - `SECURITY DEFINER` con CTE `picked` + `SELECT FOR UPDATE SKIP LOCKED` + `UPDATE` atómico a `status='processing'`.
   - Devuelve `source_date` + `cliente_proveedor_nombre` (mig 179 reescribe RETURNS — PostgreSQL no permite cambiar RETURN type con OR REPLACE).
   - Race-safe entre workers concurrentes.

4. **Zombie sweep** (`release_stale_drive_sync_processing`)
   - Devuelve a `pending` filas `processing` cuyo `processing_started_at < now() - 10 min`.
   - El worker lo invoca al inicio de cada ciclo. NO requiere cron propio.

5. **Worker** (`src/lib/integrations/drive-sync-worker.ts`)
   - Backoff exponencial: 1m, 5m, 30m, 2h, 12h, 24h. Tras 6 attempts → `failed`.
   - Errores diferenciados:
     - Storage 404 → `failed` inmediato (`storage_object_missing`).
     - Drive 401 → cascade revoke por `external_id` (ver [[oauth-cascade-revoke-por-external-id-multi-org]]) + cancel pendings.
     - Drive 404 carpeta → `failed` + marca conn `error` con `drive_folder_not_found`.
     - Drive 403/429 → retry con backoff (puede ser quota o rate limit).
     - Drive 5xx → retry normal.
   - PATCH vs POST según `drive_file_id`: si existe → `PATCH /upload/drive/v3/files/{id}/content` preserva `webViewLink` ya compartido con gestoría.

6. **Subfolders auto** (`drive-sync-paths.ts` + `resolveSubfolder` en worker)
   - Estructura: `<root>/<año>/<tipoLabel>/<MM-mesEs>/<filename>`. Ej: `Facturas TuFacturaIA/2026/Facturas emitidas/05-mayo/2026-05-29 F-A-0023 Acme SL.pdf`.
   - Fecha del documento (`facturas.fecha`), NO fecha de upload — respeta periodo fiscal.
   - **Lazy creation**: subcarpetas mes solo cuando hay PDF que va dentro.
   - **Cache JSONB** en `integration_connections.config.drive_subfolders` con shape `{"2026/factura_emitida/05": "<folder_id>", "2026/year": "<folder_id>", ...}`. La 2ª factura del mismo mes va directa sin llamadas Drive API.
   - Resistente a moves/renames en Drive (folder_id estable).

7. **Naming** (`buildFilename`)
   - Emitidas: `YYYY-MM-DD NUM Cliente.pdf` (ordena alfa + cronológico).
   - Recibidas: `YYYY-MM-DD Proveedor.pdf` (mental model del user, no num del proveedor).
   - Sanitización: rechaza `/`, `\`, control chars; colapsa espacios; nombre cliente/proveedor recortado a 60 chars.

8. **Cascade revoke** (`tokens.ts`)
   - Cuando refresh devuelve `invalid_grant`: marca conn `expired` + sweep TODAS las conn con mismo `external_id` (sub Google estable) → todas a `expired` + cancel pendings.
   - Cierra modo "cron muerto silenciosamente" (incidente cut-over OCR 2026-05-26).

9. **Dispatcher endpoint** (`/api/internal/drive-sync-dispatcher`)
   - `withCronTracking('drive-sync-dispatcher', ...)` + `requireServiceKey`.
   - Lock distribuido vía `cron_runs` `uniq_cron_in_flight` partial unique → si runner anterior aún corre, skip limpio.
   - Query `batch_size` 1-100 (default 20).

10. **UI wizard** (`/settings?tab=integraciones`)
    - Card Google conectada muestra `DriveStatusRow` inline: sin configurar / activo / pausado.
    - Modal `DriveConfigModal` con 2 modos: crear nueva carpeta (POST `/create-folder`) o usar existente (POST `/validate-folder` con URL Drive).
    - PATCH `config` con `drive_upload_enabled + drive_folder_id + drive_folder_name`.
    - Toggle pausar/reanudar = solo `drive_upload_enabled`, no toca carpeta.

## PRs y migraciones

| PR | Contenido |
|---|---|
| #85 | Backbone: mig 177, worker, dispatcher, drive-api, cascade revoke en tokens.ts. ~1280 LOC + 11 tests drive-api. |
| #86 | Hook pre-push migraciones + auto-install npm prepare + CLAUDE.md convención. |
| #87 | Wizard config: endpoints validate-folder + create-folder, modal Portal, DriveStatusRow. |
| #88 | Subcarpetas año/tipo/mes: mig 178 (cols + trigger updated) + mig 179 (RPC RETURNS). drive-sync-paths.ts puro + 17 tests. |

Migraciones aplicadas: 177, 178, 179. Plus reconciliación: 172 (copiloto_usage_increment finalmente aplicada), 173 (multidivisa marcada applied tras descubrir que Borja aplicó SQL a mano), 176 (oauth_onboarding repair de timestamp huérfano `20260528185823`).

## Pendiente operativo (próxima sesión, ~10 min)

1. Verificar `FACTURAIA_SERVICE_KEY` en Dokploy compose `tufacturaia-app` env. Smoke directo a `/api/internal/drive-sync-dispatcher` con la key del `.env.local` devuelve 401 (mismo `webhook-dispatcher` — afecta a TODOS los crons con `withCronTracking`). Actualizar `.env.local` o crear nueva con `openssl rand -hex 32` añadiéndola a app + n8n con MISMO valor + redeploy.
2. Activar workflow n8n `TwDd1OkMqr3nhSso` "Drive Sync - FacturaIA" (creado inactivo): `curl -X POST 'https://n8n.tufacturaia.com/api/v1/workflows/TwDd1OkMqr3nhSso/activate' -H 'X-N8N-API-KEY: ...'`.
3. Smoke end-to-end: conectar Drive desde wizard → emitir factura nueva → al minuto verificar `drive_sync_queue.status='synced'` + PDF en Drive en jerarquía esperada.

## Diferido a futuros PRs

- **PR5 backfill histórico**: endpoint `/api/integrations/google-workspace/backfill` que toma `{from, to, source_kinds[]}` y encola con `priority=9` + `backfill_batch_id`. UI con progreso + cancel.
- **PR6 Picker SDK**: para "elegir carpeta existente" sin pegar URL. Requiere developer key extra + JS SDK + endpoint server `picker-token` con TTL corto.
- **PR7 Drive como ingesta OCR**: estilo FacturaDirecta — el user arrastra PDF a la carpeta Drive y se importa a `bandeja_ingesta`. Anti-bucle: filtrar `appProperties.uploaded_by_app=true`. Duplicidad con Gmail/iCloud resuelta por hash.
- **PR8 Compartir con gestoría 1-click**: botón en card que invita email gestor como `viewer` en la carpeta raíz Drive.
- **PR9 Metadata rica en card**: `connected_at`, `last_sync_at`, contador de archivos subidos. Requiere extender `/api/integrations` response.

## Referencias

- ADR: [[ADR-025-drive-sync-outbox-vs-fire-and-forget]]
- Learnings: [[outbox-trigger-bd-vs-hook-js-multiples-entry-points]], [[outbox-idempotencia-por-hash-contenido]], [[select-for-update-skip-locked-via-rpc-security-definer]], [[oauth-cascade-revoke-por-external-id-multi-org]], [[supabase-migration-new-rompe-secuencia-nnn-name]]
- Incidente padre cut-over OCR: ver hub `facturaia.md` Progreso 2026-05-26.
