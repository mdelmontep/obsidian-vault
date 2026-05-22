---
title: FacturaIA — Conciliación bancaria · Roadmap maestro
date: 2026-05-20
source: sesiones 2026-05-18→2026-05-20 + spec docs/architecture/conciliacion-copiloto-spec.md
tags: [facturaia, conciliacion, roadmap, ia]
---

# Conciliación bancaria — Roadmap maestro

Subfile canónico. Cualquier sesión nueva sobre conciliación lee primero este archivo. Hub `00-home/facturaia.md` enlaza aquí desde NOW.

Si tocas el módulo: actualiza estado + fase actual + backlog al cerrar la sesión.

---

## Estado actual (2026-05-22)

**PR-PSD2-1 + 1.1 + 2 + 2.1 + 3.1 HARDENING completos** — conexión bancaria PSD2 vía Tink/TrueLayer funcional end-to-end + security/compliance production-grade. Smoke contra Tink Demo Bank ES verde con 6 movimientos importados. PR-PSD2-3.2 BONITO (UI logo + IBAN + saldo + picker) pendiente como próximo paso.

Migraciones aplicadas en prod Supabase: 105 · 106 · 107 · 107b · 108 · 109 · 111 · 112 · 113 · 114 · 115 · 116 · 117 · 128 · 131 · **144** · **145** · **146**.

Próximo paso recomendado: (1) smoke desconectar+reconectar Tink para validar state_nonce single-use; (2) PR-PSD2-3.2 BONITO; (3) compliance legal con Dani antes de cutover live (DPA Tink + Privacy Notice + DPIA + pentest + app live Tink).

---

## Fases hechas

### PR-A1 — Base módulo (commit `f56a0b3`)
Mig 105 (extracts + dedup) + parser CSV/MT940/OFX + endpoint import + drawer básico + sidebar + EstadoPill extendido + 45 tests Vitest. Fix ON CONFLICT con índice parcial → filter-pre-insert + retry SQLSTATE 23505.

### PR-A1.5 — Metadata + N:N + soft delete
Mig 106 (movimiento_metadata + movimiento_factura_asignacion + soft delete) + endpoints CRUD + drawer detail completo + helper `src/lib/conciliacion/inter-module.ts`. Patrón: movimientos_bancarios inmutable, capa editable en metadata con campos puente cross-module, event bus `module_events`.

### PR-A1.6 + A1.6.1 — IA enrich movimientos (2026-05-19)
Mig 107 + 107b + 108. Endpoint `/api/internal/conciliacion/enrich-batch` + cron Dokploy `*/10 * * * *`. 5 features: auto-categorización con **gate signo server-side** (importe>0 → solo categorías ingreso/neutro), detección determinista pre-LLM transferencias internas, enriquecimiento concepto bancario, redact NIF/IBAN/email pre-envío, retry/backoff `callLlm`. Prompt evolucionado v1→v5 con 5 agentes (correctness + prompt + SRE + UX + behavioral trust): categorías agrupadas por tipo en prompt → modelo solo "ve" compatibles con signo. Cap coste $0.50/día/org + tracking `conciliacion_enrich_runs`. Kill switch `AI_ENRICH_DISABLED=1`. Watchdog cron-zombies `*/5 * * * *`.

UI: banner CTA "X por revisar [Confirmar todas]", badge "Revisar" en ia_sugerencia, drawer Confirmar/Descartar inline, concepto enriquecido (solo si difiere del crudo), transferencias internas atenuadas opacity 0.6 + toggle, onboarding modal first-run (localStorage) **sin mencionar IA/GPT** (operational transparency Buell & Norton HBS). Endpoint bulk-confirm pasa ia_sugerencia/ia_auto → manual sin tocar categoría.

Smoke 18 movs: 14 ia_auto, 3 ia_sugerencia, 1 manual, 0 null. Coste $0.012.

### PR-A2 — Sugerencias deterministas factura↔movimiento (2026-05-20)
Mig 109. Funciones `compute_sugerencias_for_movimiento(mov_id)` + `compute_sugerencias_for_factura(fact_id)` con tolerancia 2× del config, score lineal 1.0→0.5, confidence alta/media/baja. Triggers `trg_zz_sugerencias_after_*` post mig 103 auto-match. Double-write `mirror_factura_match_to_nn` espejea legacy 1:1 → N:N. Backfill 1:1 existentes.

Endpoint `/api/internal/conciliacion/sugerencias-run` + endpoints confirm/reject. UI: banner sugerencias en `/conciliacion`, modal sugerencias por factura desde `/emitidas`, comparison cards mov vs factura, botón PDF.

### Auditoría 4 agentes + Bloques 1-4 (2026-05-20)
Auditoría paralela security multi-tenant / fiscal AEAT / E2E backend / UX frontend.

**Bloque 1 quick wins**:
- S1 categorías POST valida parent_id pertenece a org
- S2 MetadataPatchSchema narrow `categoria_source: z.literal('manual')`
- S3 PATCH valida categoria_id + transferencia_pareja_id pertenecen a org
- S4 confirm valida UUID + rechaza factura `estado NOT IN (...)` con 409 `factura_no_conciliable`
- S5 sanitizeClienteName + redactPII en prompt enrich
- E1 strip BOM 0xFEFF + dedup CSV sin external_id usa `.is(null)`
- FE1/2/4 modal sugerencias a `<Modal/>` accesible, busyAny global, error-labels.ts dictionary, responsive KPIs grid + media query <520px

**Bloque 2 — Mig 111** (F1 + F5 + F-rev + F3):
- Drop UNIQUE legacy `uniq_facturas_cobrada/pagada_movimiento`
- 4 triggers reescritos: `fecha_cobro/fecha_pago = mb.fecha` NO `CURRENT_DATE` (criterio caja AEAT)
- Trigger A recibidas SETEA `fecha_pago` (asimetría histórica fixed)
- `recompute_factura_estado(factura_id)` lee Σ N:N tol 0.5%/0.10€
- `trg_zzz_mfa_recompute` AFTER INSERT/UPDATE/DELETE en mfa
- `invalidate_sugerencias_on_config_change` borra pending si cambia tolerancia/ventana

**Bloque 3 — Mig 112 F4 detect_reembolso**:
- Columnas `es_devolucion BOOLEAN` + `devolucion_de_movimiento_id UUID` en mov_metadata
- Función busca cobro positivo previo conciliado a factura cobrada → revierte + marca es_devolucion + emite evento `cobro_devuelto`
- Llamada desde `auto_mark_pagadas_on_movimiento` antes de buscar factura recibida (evita marcar reembolso como pago de gasto)

**Mig 113 — hotfix `facturas.fecha_pago`**: mig 111 referenciaba columna inexistente. Solo existía `fecha_cobro` (mig 034). ADD COLUMN + backfill + index parcial. Aprendizaje: [[postgres-asumir-columna-existente-en-trigger-rewrite-verifica-information-schema]]

**Mig 114 — hotfix stack overflow reembolso**:
- `pg_trigger_depth() > 4` guard en detect_reembolso
- Predicado neutralización `NOT EXISTS (... devolucion_de_movimiento_id = mb.id)` en auto_mark_cobrada (UPDATE-side) + on_movimiento (INSERT-side)
- `fecha_cobro = mb.fecha` retroactivo a `auto_mark_cobrada_on_bank_match`
- Skip si mov entrante ya tiene es_devolucion=true (defensa segundo orden)

Aprendizaje: [[trigger-recursivo-revertir-estado-deja-candidato-libre-que-otro-trigger-rematchea]]

**Bloque 4 UI**:
- Filtro `.is('deleted_at', null)` en lista movimientos (comentario "defensivo mig 106" caducado meses)
- Log warn server-side cuando `parsed.movimientos.length === 0` (warnings se perdían en UI)

**Smoke F4 VERDE end-to-end (3 queries SQL verificadas)**:
1. Import +100€ → factura A2026-0009 `cobrada`, `fecha_cobro=2026-05-19` (NO CURRENT_DATE).
2. Import -100€ → factura revertida a `pendiente`, mov original neutralizado, mov devolución es_devolucion=true, evento cobro_devuelto registrado. Sin stack overflow.

### PR-PSD2-1 + 1.1 + 2 + 2.1 — Conexión bancaria Tink/TrueLayer (2026-05-22)

11 commits `6faca9a` → `1bc0d20`. Mig 144 (bank_consents AES-256-GCM cifrado consent_id + refresh_token) + mig 145 (tink en CHECK fuente + columnas rate-limit `manual_syncs_today_*`).

Stack:
- Interfaz `Psd2Provider` (initiateConsent / exchangeCallback / fetchTransactions / refreshConsent / listProviders).
- `TinkProvider` (principal ES — mejor cobertura BBVA/Caixa/Sabadell/Bankinter/Abanca/Kutxabank; pricing €0.50/usuario/mes fijo vs TrueLayer per-call ~20× más caro con cron diario).
- `TrueLayerProvider` (fallback/UK).
- Cifrado AES-256-GCM con key separada `BANK_CONSENT_ENCRYPTION_KEY` (separation of duties vs CREDENTIAL_ENCRYPTION_KEY).
- State CSRF firmado HMAC con key `WEBHOOK_SIGNING_KEY` (mejorado en PR-3.1 a key dedicada).
- Endpoints: `POST /banks/connect`, `GET /banks/callback` (público, isServiceRoute), `GET /banks` (lista), `DELETE /banks/[id]` (revoca + crypto-erasure tokens), `POST /banks/[id]/sync` (manual), `GET /banks/providers` (catálogo cacheado 24h), `POST /api/internal/conciliacion/banks/sync` (cron).
- Cron Dokploy 1×día 06:00 Madrid (PSD2 art 10: 4 calls/día/cuenta sin SCA, deja margen para 3 manuales).
- Manual sync con cooldown 30min + cap 3/día/consent. Cooldown solo aplica si `partialSuccess` (inserted>0 || duplicates>0 || errors===0) — debugger no penalizado.
- UI: `BankConnectionsCard` muestra consents activos, redirect directo a Tink Link (sin picker propio — Tink no listProviders sin USER token, sigue patrón Holded/Quipu/Sage).

Smoke verde end-to-end: 6 movimientos Demo Bank ES importados (gastos negativos correctos, dedupe second-pass `inserted:0 duplicates:6`, expiring_notified emite notif 7d antes).

Bugs+fixes durante el smoke:
1. TrueLayer `/providers` exige `providers=` param (sandbox solo `mock` UK).
2. Tink no listProviders con client_credentials → delegamos selector a Tink Link UI hosted.
3. Redirect URI cogía `0.0.0.0:3000` del container interno → fix `getCallbackUrl()` deriva del header `x-forwarded-host` (Traefik). `TINK_REDIRECT_URI` env deprecated.
4. Tink scope `offline_access` obligatorio para refresh_token.
5. Tink `pageSize=200` excede `/data/v2/transactions` → 100.
6. Refresh UI tras sync manual via callback `onSynced` propagado a `BankConnectionsCard`.

Aprendizaje: [[psd2-tink-link-vs-truelayer-picker-decision]] · [[psd2-redirect-uri-derivar-del-host-no-env-build-time]].

### PR-PSD2-3.1 HARDENING — security/compliance pre-Bonito (2026-05-22)

Commit `80036ab` (+1015/-164 sobre 19 archivos) + mig 146 `state_nonce`. Audit previa 3 agentes paralelos (backend / security / UX) detectó 9 issues P0/P1 + 5 diferidas P2 → todas cerradas en este PR antes de la UI bonita.

**Bloqueantes cerrados**:
- **C1 requireRole** propietario|admin|contable en `POST /banks/[id]/sync` (antes cualquier rol activo consumía cuota PSD2 → privilege escalation + DoS).
- **C2 state CSRF** reforzado: mig 146 `bank_consents.state_nonce` con UNIQUE PARCIAL pending, `signState()` devuelve `{token, nonce}`, `/connect` persiste nonce, `/callback` claim atómico `UPDATE WHERE state_nonce=X AND status=pending RETURNING` (replay rechazado), key dedicada `BANK_PSD2_STATE_KEY` (fallback `WEBHOOK_SIGNING_KEY` con warn → key separation arreglada).
- **C3 audit_log** completo PSD2 art 67 + GDPR art 30. Helper `logBankAccess()` en `public.audit_log` con actions: `bank.connect_initiated/completed/failed/disconnect/sync_manual/sync_cron/view_balance/access_report`.
- **C4+M3 redactPII** unificado. Helper `logProviderError()` con regex que tapa `access_token`/`refresh_token`/`Bearer`/`consent_id`/IBAN/NIF/email en logs Dokploy/Sentry. Helper `sanitizeProviderErrorForStorage()` aplicado en `last_sync_error` antes de persistir.
- **A3 validateProviderId** server-side contra catálogo cacheado (`providers-cache.ts`). TrueLayer estricto, Tink regex canónico (no expone catálogo). Cierra OAuth provider injection vía XSS/devtools.
- **A5 maskIban** en `GET /banks` response → `ES** **** **** **** XXXX`. IBAN completo solo en BD para sync interno (service-role). Cierra leak intra-org a `comercial`/`solo_lectura`.

**Diferidas (5) cerradas en el mismo PR**:
- **A4 key versioning AES**: formato `kid:iv:tag:ct` con backcompat v0 (3 partes). `BANK_CONSENT_ENCRYPTION_CURRENT_KID` env (default v1). Permite rotar key sin re-cifrar masivamente. Runbook rotación documentado en `psd2/encryption.ts`.
- **M2 atomicidad refresh_token mid-loop**: helper `persistRotatedTokens()` graba INMEDIATO cada cuenta. Si container muere procesando una cuenta posterior, no perdemos el token rotado.
- **M4 GDPR art 15** endpoint `GET /banks/[id]/access-report`: devuelve consent + accounts + count movs + audit_trail (200 últimas) + processors (Tink AB / TrueLayer Ltd) + retention policy. El propio acceso queda registrado en audit_log.
- **M5 ADR retención**: `docs/decisions/ADR-002-psd2-data-retention.md` documenta 7 años movimientos (Ley 58/2003 art 70 + Ley 11/2021 + Código Comercio art 30) + crypto-erasure tokens al revocar + base legal GDPR art 17(3)(b/e) frente a "derecho al olvido".

**Plus**: scope `balances:read` en Tink (sin él `/data/v2/accounts` no devuelve saldo).

20/20 tests verde. Lint + typecheck + build limpios.

Envs nuevas opcionales en Dokploy:
- `BANK_PSD2_STATE_KEY=<openssl rand -hex 32>` (recomendada, sin esto warn de key separation).
- `BANK_CONSENT_ENCRYPTION_CURRENT_KID` (default `v1`, cambiar a `v2`+`BANK_CONSENT_ENCRYPTION_KEY_v2` cuando se rote).

---

## Pendiente PR-PSD2-3.2 BONITO (~4h) — siguiente

UI a nivel Holded/Quipu/Sage tras hardening completo:
1. Mig nueva añade `financial_institution_id TEXT` + `display_name TEXT` + `last_known_balance_cents BIGINT[]` a `bank_consents`. Índice UNIQUE PARCIAL `(org_id, provider, financial_institution_id) WHERE status='active'` (anti-duplicados al renovar consent).
2. `TinkProvider.exchangeCallback` extrae `financialInstitutionId` del primer `account` (NO call extra — el campo viene en `/data/v2/accounts`).
3. Self-host `/public/banks/{bbva,caixa,santander,sabadell,bankinter,ing,abanca,kutxabank}.svg`. Hardcoded mapping `src/lib/conciliacion/spanish-banks.ts` con `as const`. Drift test CI contra `/providers` Tink.
4. Card reescrito: un card por banco con sub-filas por account, logo 48×48 con fallback monograma → fallback `<Icon name="bank">`, IBAN parcial `ES** **** **** **** 1234` (mascarado por A5), saldo, currency badge.
5. Banner full-width caducidad <7d arriba del módulo (no solo pill).
6. Pill granular: 0-2d rojo "Caducada"/"Caduca mañana", 3-7d amarillo "Caduca en N días", 8d+ verde "Activa".
7. Modal `<Modal>` confirm desconectar con `autoFocus` en Cancelar + microcopy con números reales ("3 cuentas, 1.247 movimientos").
8. Picker modal grid 4×2 SVG locales + buscador + botón "Ver todos" → Tink Link redirect (NO iframe, X-Frame-Options DENY).
9. Empty state trust signals "✓ PSD2 AISP regulado · ✓ Solo lectura · ✓ Bancos españoles".
10. Sync feedback inline (border-top progress 2px en card, no toast bloqueante).
11. Badge fuente 12-14px tenue en tabla movs con tooltip "Importado desde BBVA · Tink".

Falsos positivos descartados: WCAG AA pill contraste OK (7-8:1 verificado), 5+ bancos no rompe lista (media Holded 1.4), iframe Tink Link bloqueado X-Frame-Options DENY.

---

## Pendiente commit (próxima sesión, antes de cualquier feature nueva)

14 archivos modificados sin push, smoke local ya validado:

- `src/components/conciliacion/conciliacion-view.tsx` (filtro deleted_at + modal accesible + busyAny + error-labels)
- `src/app/api/conciliacion/import/route.ts` (log warn 0 movs)
- `src/app/api/conciliacion/sugerencias/[id]/confirm/route.ts` (S4 UUID + estado guard)
- `src/lib/conciliacion/error-labels.ts` (nuevo)
- `src/lib/conciliacion/ai-enrich.ts` (S5 sanitize cliente)
- `src/lib/conciliacion/import-parser.ts` (E1 BOM)
- `src/app/api/conciliacion/categorias/route.ts` (S1)
- `src/app/api/conciliacion/movimientos/[id]/route.ts` (S2 + S3)
- `src/lib/documents/anular-factura.ts` (F2 desvinc N:N)
- `src/app/globals.css` (responsive sug-card-body)
- `supabase/migrations/111_conciliacion_fixes_auditoria.sql`
- `supabase/migrations/112_conciliacion_reembolso_detection.sql`
- `supabase/migrations/113_facturas_fecha_pago.sql`
- `supabase/migrations/114_conciliacion_reembolso_no_rematch.sql`

Migs 111-114 ya aplicadas en prod por el user durante el smoke. Falta solo deploy Next.js para los archivos TS.

---

## Fase siguiente (decisión próxima sesión)

Recomendación: **#41 → #44 → #46**.

### #41 P0 BUG factura sin cliente cuando nombre nuevo (URGENTE FISCAL)
Detectado 2026-05-19 22:00 con factura A2026-0006 Consultoría 538,45€. En `/generar`: si escribes nombre cliente que NO existe en `clientes` y guardas, factura se emite con `cliente_id=NULL`. Cliente nuevo no se inserta automáticamente. Modal de detalle muestra "vacía de cliente".

**Impacto fiscal**: rompe cashflow por cliente, cobros recordatorios (no sabe a quién mandar), mod 347.

**Fix esperado (Holded-style)**: si nombre no coincide con ninguno → modal "Crear cliente nuevo: 'X'?" con campos mínimos (nombre + email/NIF opcional) o auto-create silencioso con flag.

Localizar en `src/components/.../generar-view.tsx` o handler `POST /api/facturas/crear`. Verificar si select del campo cliente bloquea texto libre (debería) o lo permite vacío silenciosamente.

### #44 PR-A2.1 parser num factura en descripción banco
Cuando `mb.descripcion` contiene un literal tipo `A2026-0006` (típico de transferencia con concepto "PAGO FRA A2026-0006"), parsearlo y **boost score sugerencia** al match con esa factura concreta.

Caso real encontrado durante audit: mov mencionaba A2026-0006 pero sugerencia apuntaba a A2026-0003 (importe igual, fecha cercana) con badge REVISAR correcto. Con parser num daría confidence='alta' al match correcto.

Regex `\b[ABFP]\d{4}-\d{4}\b` + lookup en `facturas.num` de la org + boost score +0.2 + flag motivo `match_num_en_descripcion`.

### #46 F4 detección reembolso bidireccional
Limitación actual: F4 dispara solo desde mov negativo buscando positivo previo. Si devolución entra ANTES del cobro (poco probable pero posible si import histórico desordenado o duplicate-import), F4 no dispara.

Fix: trigger simétrico también desde positivo nuevo → buscar mov negativo pendiente con `es_devolucion=null` que pudiera ser su devolución futura. Marca preventiva.

---

## Bloque 5 strategic (diferido, no urgente)

- **N:1 matching real** para pagos parciales/agrupados (cliente paga 250€ por 2 facturas 100+150). Hoy N:N existe en BD pero UI solo permite 1:1. Necesita: split flow en confirm, importe_aplicado por asignación.
- **Split-view full-width estilo Gmail/Linear** (canvas vs modal). Modal sugerencias actual es bloqueante. Mejor experiencia es lateral persistente.
- **Inline edit + j/k keyboard shortcuts**. Power user en lista movimientos.
- **RPC atómica `confirmar_sugerencia`** (S7 audit). Hoy es endpoint que hace UPDATE factura + INSERT mfa + UPDATE sugerencia en 3 queries. Si una falla deja estado inconsistente.
- **FE3 bulk-confirm preview modal con checkbox individual**. Hoy bulk-confirm pasa todos ia_sugerencia/ia_auto a manual de una. Mejor: preview + check-uncheck individual.
- **FE5 `<tr role="button">` → estructura semántica**. A11y limpieza tabla movimientos.
- **Columna `currency` en movimientos** (multi-divisa). Hoy asumimos EUR. Cuando llegue cliente con cuenta multi-currency romperá.

---

## Sprint A3 NEXT — Copiloto v2 con tools

Después de cerrar #41/#44 (que son refinamientos), arrancar Sprint A3.

4 tools core + 3 tools movimientos planeados:
- `suggest_note` — comentario contextual sobre mov o factura
- `explain_movimiento` — porqué se categorizó así
- `analyze_movimiento` — anomalías, comparativas, patrones

Spec en `docs/architecture/conciliacion-copiloto-spec.md` (subfile [[facturaia-conciliacion-copiloto-spec]]).

---

## Sprint B módulos paralelos (NEXT, no bloquean A3)

- **PR-B-anomalias** — extender Detector de Anomalías a scope bancario (duplicados borrosos + gasto anómalo) → escribe en `movimiento_metadata.anomalia_score`.
- **PR-B-cobros** — extender Agente de Cobros con predicción retraso por cliente → escribe en `movimiento_metadata.prediccion_cobro_dias`.
- **PR-B-tesoreria** — widget IA resumen mensual en Previsión de tesorería.
- **PR-A4** — panel `/admin/ia-ops` métricas internas (accuracy, coste $$$, prompt_version, model, sign_mismatches). NUNCA mostrar al usuario final (decisión 3 agentes: negativity bias → paranoia).

---

## Decisiones arquitectónicas clave

- **Movimientos_bancarios = inmutable** (datos del banco). Capa editable en `movimiento_metadata` con campos puente cross-module + event bus `module_events`. Cualquier módulo IA puede leer/escribir sin acoplamiento.
- **N:N `movimiento_factura_asignacion`** reemplaza 1:1 progresivamente. Expand-contract migration: legacy `cobrada/pagada_con_movimiento_id` mantiene 6 meses con double-write trigger `mirror_factura_match_to_nn`. Drop columna legacy en mig futura cuando todos los readers (dashboard, drawer, cashflow, /api/conciliacion/movimientos/[id]) lean de N:N.
- **Dokploy cron (NO n8n)** para crons del módulo. Mismo patrón que verifactu-process. n8n queda para flows con LLM agent + WhatsApp.
- **TrueLayer Data API** como proveedor PSD2 AISP (pivot 2026-05-19: GoCardless cerró signups nuevos). Cliente PSD2 abstraído tras interfaz `Psd2Provider` para swap futuro a Tink.
- **Operational transparency** (Buell & Norton HBS) en UX IA: mostrar trabajo accionable (count pendiente), NUNCA accuracy %, coste $$$, modelo, prompt_version, "powered by GPT-4".
- **Criterio caja AEAT** para fechas IVA: `fecha_cobro/fecha_pago = mb.fecha` siempre. NUNCA `CURRENT_DATE`.
- **Gate signo server-side**: importe>0 → solo categorías tipo=ingreso/neutro. Defense in depth contra prompt injection o alucinaciones.

---

## Deuda técnica activa

- **PR-A1.7 diferidos**: SKIP LOCKED claim atómico (lock global cron_runs cubre el caso actual), query rotada por org (round-robin para orgs grandes), tiktoken real (chars/3.5 in subestima ~10%), cap global plataforma además del por-org, uso real columna `ia_claim_at`.
- **Drop columna legacy `cobrada/pagada_con_movimiento_id`** en mig futura (3-6 meses) cuando todos los readers lean de N:N.
- **F4 bidireccional** — #46.
- **Multi-currency** — bloque 5.

---

## Smoke tests pendientes (post-deploy)

Ver hub sección "Smoke tests pendientes" entrada `Conciliación post mig 111-114 + Bloques 1-4`. Re-ejecutar en prod tras deploy:
1. Import CSV +X € factura emitida → cobrada con `fecha_cobro = mb.fecha`.
2. Import CSV -X € factura recibida → pagada con `fecha_pago = mb.fecha`.
3. Import devolución -X tras cobro +X → factura revertida, mov original neutralizado, evento cobro_devuelto.
4. Soft-delete mov SQL → no aparece en UI.
5. Confirmar sugerencia para factura anulada → 409 factura_no_conciliable.
6. PATCH mov con categoria_id de otra org → 400/403.
7. Cambiar tolerancia/ventana en config → sugerencias pending borradas.
8. Anular factura cobrada → mfa N:N desvinculada + cobrada_con_movimiento_id=NULL.

---

## Links

- Spec original: `docs/architecture/conciliacion-copiloto-spec.md`
- Subfile resumen: [[facturaia-conciliacion-copiloto-spec]]
- Hub: [[facturaia]] (00-home)
- Learnings: [[trigger-recursivo-revertir-estado-deja-candidato-libre-que-otro-trigger-rematchea]] · [[postgres-asumir-columna-existente-en-trigger-rewrite-verifica-information-schema]]
