---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Kanban: **NOW** = en lo que estás esta sesión (máx 3). **NEXT** = próximas 2 semanas. **LATER** = todo lo demás. Entradas = 1-2 líneas mirando hacia delante; la ✅-historia vive en git/`[[facturaia-historico-detallado]]`. Podado 2026-06-26.

## NOW

- **TuFacturaIA — notifs fiscal residuales (manual)** — marcar leídas notifs viejas + abrir/recalcular borradores 130 2T/3T/4T (drift: abono B2026-0001) + check visual drawer (X 28px, fade chips). Fix #214 en prod.
- **Centro Elphis — go-live** — hardening ✅. Pendiente (todo externo): (1) Pablo coexistencia WA vía A (659); (2) 4 plantillas HSM; (3) 659 877 708 → Cloud API; (4) DPAs Enrique; (5) sesión crisis Enrique; (6) número Alba. HUB `elphis/CLAUDE.md`
- **agency-portal — verificar extracción onboarding en prod (PR #67)** — confirmar "Progreso por sección" + "Respuestas extraídas" se rellenan por turno; si `activity_event.action='onboarding.extraction_failed'`, abrir issue.

## NEXT (próximas 2 semanas)

- **TuFacturaIA — auditoría correctness+seguridad ✅ mergeada + en prod** — #494 lote quirúrgico 12 bugs · #495 M2 anulación no bloqueada por cuota · #497 H6 cobro + H7 concurrencia. Migs **393/394 aplicadas en prod** (verificado `migration list --linked`, 06-26). **Smoke BD pendiente**: 2 `POST /api/sepa/remesas` concurrentes misma factura → una falla (23505); 2 confirmaciones de una revisión recurrente → una sola factura. **Cola**: H1 (Opción A repartir descuento_global en líneas, PR fiscal; hay test que asegura lo bruto) · **L3/export 303 (investigación fiscal PRIORITARIA, ver entrada 303)** · H5 (paginación adaptadores OCR) · H2/M1 (RPC agregación KPIs) · M5 (config race) · M2-resto (`get_org_usage` excluir abonos). **27 tests rotos en main PRE-EXISTENTES** (`ocr-process`/`stock-alarmas-email`/`crons/registry-wired`) — ¿tarea aparte? Ver [[postgrest-max-rows-trunca-agregacion-en-js]] · [[idor-detras-de-canal-hmac-validar-membresia-del-recurso]]- **TuFacturaIA — SEPA cobros/pagos/recurrentes ✅ en prod** (#486-493, migs 386/389-392; B2B, pain.001 pago proveedores, devoluciones, atómico, hardening). Pendiente: (a) golden-file `pain.002` REAL BBVA (Dani) → `tests/fixtures/sepa/retorno-bbva-real.xml`; (b) validación Dani `modo='auto'` recurrentes; (c) gap concurrencia cobro #497 (mig 393) pendiente merge+prod. `issues/prd-sepa-paridad-holded.md` · Ver [[sepa-pain008-remesa-adeudo]]
- **TuFacturaIA — refactor arquitectura ✅ #472/#473/#474** — Pendiente: (a) fix E2E `generar-factura.spec` (desfasado: IVA `<Select>`, toggle envío `uncheck({force})`, modal cliente nuevo, factura PERMANENTE mig 086) PR dedicado; (b) smoke+QA visual copiloto #477. Ver [[tool-result-sintetico-necesita-render-prosa-o-sale-json-crudo]] · [[agente-background-en-worktree-build-cuelga-watchdog]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10 nocional, ~88 USDT; 4 estrategias en paper. Dashboard cryptobruj-bot.185.99.186.76.sslip.io/analisis. Sin validar → vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.
- **agency-portal — cron Dokploy `onboarding-reminders`** — botón manual en prod; falta el automático. Clonar schedule `sync-facturaia`: cron `0 10 * * *`, ruta `/api/internal/onboarding-reminders` (POST, `x-service-key`). Ver [[whatsapp-fuera-ventana-24h-requiere-plantilla-hsm]]
- **agency-portal — Pizarra/board PR #91 en review (Borja)** — rama `feature/pizarra-dashboard`. Pendiente: review+merge Borja (aplica mig `board_comments` con `db push`) + QA visual Manu local (`PORT=3002`). Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]] · [[supabase-tabla-ausente-postgrest-pgrst205-no-42p01]]
- **TuFacturaIA — smoke deploy ingesta+stock** (mig 378) — en prod: (a) factura USD muestra `US$`; (b) progreso monótono sin parpadeo; (c) cantidades/precios largos no se cortan; (d) factura Retell USD servicios aprueba sin bloqueo descuadre; (e) bienes con líneas a productos → footer Σ-vs-base bloquea si no cuadra. Ver [[progreso-real-vs-simulado-tareas-opacas]]
- **TuFacturaIA — auditar resto de Settings (bug lectura impersonando)** — empresa+plantillas ✅ (#460/#462). Revisar email-settings y cualquier sección con `createClient()`/`getOrgId()` → 0 filas o org del superadmin. + smoke logo impersonando. Ver [[settings-leen-con-createclient-getorgid-se-rompen-impersonando]]
- **TuFacturaIA — Copiloto WhatsApp paridad MCP** — Issue 001 ✅ (22 tools). Siguiente: issue 002 (buscarCatalogo read-only). 13/14 pendientes. `issues/prd-copiloto-whatsapp-paridad-mcp.md`
- **TuFacturaIA — smoke deploy #412 (perf DB + CLS)** — prod: (a) sidebar sin shift superadmin; (b) ingesta progress-row no salta; (c) tabla facturas 2 líneas móvil ≤640px; (d) Advisors auth_rls_initplan + multiple_permissive_policies bajaron.
- **TuFacturaIA — PR #376 Floating UI (popovers)** — 10 componentes a `useAnchoredMenu`, verde, QA 8/10. Pendiente: merge (CI billing) + QA visual `bank-connections-card` y `header-acciones` (sin datos sandbox). Rama `fix/team-member-menu-posicion-derecha`. Ver [[react-hooks-refs-falso-positivo-floating-ui]] · ADR-033
- **TuFacturaIA — fase unificación fields** — Drawers ✅ (#374). Falta: `<Field>`/clase única por tokens (`.form-input`/`.set-input`/`.adm-select`/`.input` divergen) + revisar copiloto. Smoke 2 drawers fiscal en prod. Ver [[controles-form-nativos-no-estilables-construir-componente]] · [[zindex-capa-overlay-orden-portal]] · [[no-forzar-base-en-paneles-divergentes]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — decidido pagar para mantener Code Quality (scan + gate PR); si caduca el trial se apaga. Ver [[github-code-quality-triage]]
- **TuFacturaIA — corregir ID receptor en routing `CLAUDE.md`** (1 línea) — `zYcHHa8jWXB6dY5i` → `pqSWkDIHqmSVHotB` (404; ya corregido en `gotchas.md` #368, falta la tabla de routing).
- **TuFacturaIA — 116 decomiso bot intención (Fase C, dejar bakear)** — set de creación flipado al Copiloto. Queda retirar nodos de emisión muertos del receptor `pqSWkDIHqmSVHotB` (con plan+OK; bakear ~1-2 sem). Plan: [[facturaia-decomiso-bot-intencion-116]]
- **TuFacturaIA — ticket Abba BORME** — en `/ingesta` de Abba re-escanear 2 docs (`...310785.jpg`/`...269660.jpg`) → responder a gonzalo.riera. Fix #291 en prod. Ver [[gpt-4o-mini-falla-fotos-baja-calidad-bleed-through]] · [[recuperacion-ui-gated-por-estado-pierde-items-en-estado-hermano]]
- **TuFacturaIA — responder ticket bgchivite `1762f07e`** — deploy #209 en prod; responder.
- **TuFacturaIA — smoke PR #453 (descartar recibida)** — prod: descartar recibida → desaparece de `/recibidas` y no reaparece; filtro "Disputada" sigue mostrándola. Ver [[descartar-soft-exclude-ocultar-de-listado-no-hard-delete]]
- **TuFacturaIA — Stock en `beta` (pilotaje gratis)** — monitorizar uso/feedback + decidir flip a `activo` (12,90€). Lotes/cajas/unidad compra en prod (migs 375/383/384). Smoke pendiente polish #475 (badge coste/ud + "Por cajas" en aprobación). Ver [[facturaia-modulo-stock]] · [[unidad-compra-convertir-en-insert-no-en-motor]] · [[motor-con-input-requerido-debe-defaultear-no-fallar-mudo]]
- **TuFacturaIA — seed org test stock-fase-d.spec.ts** — crear org `7d9a2cfe-...` + "producto test" + bandeja `e2e00002` + factura `e2e00001` para que el gate spec pase P1-P6.
- **TuFacturaIA — smoke E2E cobro empresa extra (F3b)** — código en prod (#144). Requiere pago real/Stripe test clock: comprar empresa extra → subscription item quantity + proración + webhook `billing_accounts.empresas_extra`. Hoy 409 `no_active_subscription` (complimentary). Ver [[stripe-subscription-multi-item-resolver-por-price-no-indice]]
- **IET — deploy a iet.es** — web en `iet-preview.surge.sh` (SEO 81/100). Pendiente: (1) FTP `dist/` a Apache + TLS; (2) verificar coords geo JSON-LD; (3) fotos reales (cliente); (4) si form→Gmail, key Web3Forms `administracion@iet.es`. HUB [[iet|IET]]
- **TuFacturaIA — Multidivisa Recibidas: queda S4 + WA cutover + ISP** — S1-S3.5 ✅ en prod (mig 187). Pendiente: S4 Copiloto (`revisarBandejaMoneda` + notif FX>5% + badge) · cutover SSOT WhatsApp `pqSWkDIHqmSVHotB` (sprint) · ISP intracom keywords · auditoría cross-PR 3 agentes. [[facturaia-multidivisa-recibidas]] · ADR-024
- **TuFacturaIA — cerrar bucle catálogo productos/servicios** — código en `origin/main` ✅. Falta: cableado n8n (`consultar_catalogo` + write-back `/api/internal/voice/catalogo/guardar`), mig 172 `copiloto_usage_increment` a prod, manuales.
- **EcoBox — voz + chat WhatsApp E2E LIVE** (voz `+34919932797`; chat Chatwoot+bot, WA `+34910054813`). Pendiente smoke: (a) grúa/Mutua→handoff+email; (b) reserva E2E que dispare `Build Emails`; (c) tope 7º. Manu: smoke chat hueco nuevo (no-doble-booking). Cristian: logo PNG+color+firma. Publicar app Meta (sale dev mode). HUB [[clientes/ecobox/index|EcoBox HUB]]
- **TuFacturaIA — fix locators spec `conciliacion-vinculacion`** — el viejo comparte bug `table[aria-label]` (está en `<div role=region>`) + `isVisible()` no espera → `[aria-label=…]` + `waitFor`. Ver [[playwright-isvisible-ignora-timeout-usar-waitfor]]
- **TuFacturaIA — UI fiscal-panel mostrar aeat_health derivado** (~30 líneas) — endpoint ya devuelve health (verde/ámbar/rojo/gris) + last_10; añadir 2º HealthRow + lista compacta. Commit b6014de
- **TuFacturaIA — PSD2 cutover live** — bloqueado Dani/legal: ADR-002 review + Privacy Notice (Tink encargado art 28) + DPA Tink + DPIA art 35 + pentest PSD2 (~3-5k€) + app live console.tink.com. Sandbox production-grade.
- **TuFacturaIA — setting catalog `bancario_umbral_anomalia`** (~5min) — añadir al `MODULES_CATALOG.conciliacion.settings` (~L258 catalog.ts). Sin esto el cron usa default `0.5` hardcoded.
- **TuFacturaIA — 3 envs `.env.test` smoke middleware A/B** (~5min) — `E2E_SUPERADMIN_TEST_ORG_ID`, `E2E_UNVERIFIED_EMAIL/PASSWORD`. Commit cafc8dc
- **TuFacturaIA — coherencia `manual-usuario` vs `manual-admin` §31 Equipo** — etiqueta "Inactivo" vs `revocado/expirado`; "revocar invitación" (⋯) no en admin; "transferencia de propiedad" sin documentar. Decidir si UI existe y unificar.
- **TuFacturaIA — decidir VerifACTU worker Dokploy** (hoy Disabled) — si queda off, eliminar entrada; si on, Run Now + verificar pendiente_envio→aceptada.
- **TuFacturaIA — Stripe en activación de add-ons** — CTA "+XX€/mes" redirige sin cobro. Conectar checkout para que toggle=compra (Conciliación 19€/Anti-fraude 9€ seedeados). Seguridad ✅ (toggle rechaza enable fuera de plan 402). Ver [[endpoint-toggle-feature-debe-gatear-enable-por-plan-o-compra]]
- **TuFacturaIA — decidir cliente live vs congelado** — snapshot fiscal al crear factura; editar cliente no cambia PDFs viejos (legal pero confunde). ¿Botón "Re-emitir con datos actuales" o congelado siempre?
- **TuFacturaIA OTP — patch n8n delivery status** (~5min) — key nueva en `n8n.tufacturaia.com/Settings/API` + `python3 ops/n8n-patches/apply-delivery-status.py`.
- **TuFacturaIA — quitar dominio viejo `facturaia.agentesia.world`** — repo limpio; queda infra externa (DNS IONOS + entrada stack Dokploy).
- **TuFacturaIA — MCP residuales post-Directory** — conector en main; Directory 057 en revisión Anthropic (reviewer [[reference_mcp_reviewer_user]]). Queda: alias IONOS `privacidad@`/`info@`/`soporte@` → buzón leíble (Resend no sirve).
- **TuFacturaIA — Daily Briefing trigger** — `/daily` listo; falta cron Dokploy o trigger automático que escriba `00-home/daily-briefing.md`.
- **agency-portal — n8n router consulta Supabase como source of truth** — TTL 30d en `aia_ob:{phone}` es tirita. Endpoint `/api/onboarding/is-active-by-phone` + nodo HTTP en `ChatBOT mejorado` antes del IF Activo + Redis a caché con re-seed. Ver [[Stack/n8n]] · [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding]]
- **TuFacturaIA — proteger columnas regulatorias con trigger guard** — billing+verifactu ya blindados (migs 321/162). Falta replicar para `regimen_iva`/`nif`/`iae`/`verifactu_num_instalacion` (hoy `org_member_update` deja UPDATE a cualquier miembro). Copiar trigger mig 321. Ver [[Stack/facturaia]]
- **Agentesia chatbot ticketing — test cliente real** — pedir teléfono cliente "Soporte técnico" + verificar AI a TICKET_CREATED/APPENDED/ERROR_NO_CLIENTE. Limpiar workflow temporal `a96XVFKX4WujMCKW`.
- **Simarro — Matching inteligente LIVE + multi-pool** — 3 etapas + cron semanal `RGu1FLq9l3PKaX2B`. Pendiente: chatbot WA mueve a pool (voz ✅); mapeo agente→`kommo_user_id` (Ramón); re-notificar bajada precio; LIMPIAR leads ZZ TEST (`32287686`/`32288360`/`32293872`/`32295018`/`32302304`/`32314286`) + `36016032` + Bad Bunny `32281284` + embudo `13862727`. Ver [[project-matching-inteligente]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email interno. Crash "node hasn't been executed" cerrado; falta corrida real. Ver [[n8n-ramas-paralelas-no-garantizan-orden-poner-en-serie]]
- **Simarro — outbound reactivación: re-test guion** — bug `n_motivo` callejón sin salida corregido en vivo (06-25). Pendiente: re-test "no, me pareció cara → sigo buscando" + marcar consentimiento `1376604` (Ramón). Lanzador `2LqwDgLecHwjgIQl` activo. Ver [[project-outbound-reactivacion]] · [[conversation-flow-outbound-gotchas]]
- **Simarro/CZ — bug recordatorios por task_type** — el workflow disparaba por cualquier tarea; viene del blueprint compartido → revisar si CZ lo tiene. Ver [[recordatorios-visita-por-task-type]]
- **Simarro — preguntar a Ramón** — (1) ¿bot reserva directo o fecha provisional? (2) ¿pipeline Kommo vale o ajustes?
- **Simarro — verificar salesbot 88183** — acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo.
- **Simarro — go-live routing por-agente** — Ramón añade `agente:` en Idealista → sync `3zBDpPwBYLZgMink` → E2E con vivienda real. Hoy `properties.agent=NULL`. Voz publicada (v29). Ver [[simarro]] · [[routing-citas-por-agente]]
- **Simarro — limpiar 9 leads test Kommo + cred SMTP** — leads `32260874`/`32260174`/`32260184`/`32260262`/`32260290`/`32260318`/`32260370`/`32257958` + "Ramon Demo". SMTP App Password `simarroproperties@gmail.com` (cred `oKRmYFhljczyvzV8` fantasma).
- **Clínica Zen — status_id Kommo 'Cita cancelada'** — workflow `DkueIeGFWLKh8nTj` da 400 NotSupportedChoice. Pedir ID correcto pipeline 13495347.
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani. Tras merge → smoke E2E con llamada real.
- **TuFacturaIA Centro Fiscal IA — operativa legal/comercial pre-beta** — entregables redactados en `docs/compliance/centro-fiscal-pre-beta/` (#449). Pendiente Manu: enviarlos + certificado de representante (AgentesiaLab no lo tiene). Smoke E2E Stripe pendiente.
- **TuFacturaIA — SIF Declaración Responsable + inalterabilidad** — #449 mergeado + mig 376 viva (inerte, 0 facturas aceptadas). Queda (externo/legal): P2 validación XSD AEAT + P3 smoke `pre` (cert) + flip `VIGENTE`+firma. `docs/compliance/centro-fiscal-pre-beta/`
- **TuFacturaIA — fichero 303 → sandbox AEAT Pre303 (HITL)** — descargar fichero oficial → importar en Pre303. **Causa raíz hallada (06-26) — PRIORITARIO FISCAL**: numeración de casillas 303 inconsistente en 3 capas — motor `iva.ts` mete cuotas en `02/05/08`, spec posicional oficial (`export/spec-303-2026.generated.ts`) las lee en `03/06/09`, fixtures otra. Posible `.txt` AEAT con cuotas por tipo vacías + puede afectar declaraciones presentadas. Investigar ANTES de tocar `casillas-labels.ts` (L3). Ver [[consumidor-lee-claves-que-productor-no-emite]]
- **TuFacturaIA — 349 Fase 2** — export posicional oficial (HITL sandbox) + drill-down + captura auto-intracom OCR. Resto bloqueado por sourcing/gate legal.

## LATER

- **TuFacturaIA — optimistic-UI en TODAS las acciones** — descartar ya cubierto (#453); auditar aprobar/marcar cobrada/anular/enviar. Candidato a sprint UX. Ver [[descartar-soft-exclude-ocultar-de-listado-no-hard-delete]]
- **TuFacturaIA — multiempresa follow-ups** — (1) panel asesor "empresas que gestiono"; (2) guard `is_account_owner` para billing; (3) RPC `consolidar_orgs_en_cuenta`. Ver [[ADR-028-multiempresa-scope-navegar-agregar-cobrar]]
- **TuFacturaIA — backends módulos pendientes** — Firma eIDAS, Cashflow IA forecast. ~14 opciones config "Próximamente".
- **TuFacturaIA — Asistente IA multi-canal** — copiloto WhatsApp consultas (vencidas, resúmenes, cobrador, cashflow, alertas, presupuestos, informe fiscal). [[facturaia-bloque-4-agent-query-spec]]
- **TuFacturaIA — cablear `sendEmail` google-workspace a envío de facturas** — infra hecha; el port `EmailProvider` (#472) ya está en `send.ts` → falta adapter Gmail + seleccionarlo en `pickProvider` + toggle por org.
- **TuFacturaIA — Canales Ingesta + Plan/Facturación** (spec 2026-04-24) — rediseño canales sin toggles + página planes reales con pago e historial.
- **Tecnocloud — WhatsApp en TuFacturaIA** — phone_number_id Meta + webhook override.
- **Simarro — IDs TODO en n8n** — TASK_TYPE_ID, RESPONSIBLE_USER_ID, SHEET_ID_LEADS_WEB, calendar Ramón, Supabase pending.
- **Simarro — oportunidad monitor inmuebles** (StateFox) — scraping Idealista/Fotocasa + alertas precio/m²/zona. Confirmar interés/presupuesto.
- **Clínica Zen — configurar Retell en leads entrantes** — workflow `RN0wl8RaRmwLpnfQ`, verificar webhooks dominio CZ.

## Bloqueos

- **TuFacturaIA — subir tier OpenAI (Manu)** — bot WhatsApp salta rate-limit (TPM 30k Tier 1). Subir a Tier 2 (450k) en platform.openai.com/settings/organization/limits.
- **TuFacturaIA — billing GitHub Actions re-bloqueado (Manu)** — desde 17/06 jobs mueren a 0 pasos (spending limit). Subir límite en Settings → Billing org `AgentesIA-MAdrid`. Ver [[github-actions-org-private-free-tier-2000-min]]. **Mientras siga, merges con `gh pr merge --admin`** (bypass checks; requiere OK explícito).
- **TuFacturaIA — HIBP leaked-password requiere Supabase Pro (Manu)** — toggle "Prevent use of leaked passwords" falla en free. Activar al subir a Pro.

## Vistas por cliente

- [[facturaia]] · [[agentesia]] · [[simarro]] · [[clinica-zen]] · [[tecnocloud]] · [[clientes/centro-elphis/index|centro-elphis]]

## Completado reciente

Ver `00-home/archive-completed.md`
