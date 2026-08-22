---
title: Architecture Decision Records (ADRs)
date: 2026-05-10
tags: [decisions, adr, architecture]
---

# Decisiones

Una decisión = un archivo `ADR-NNN-slug.md`. Cuando elijas A sobre B y la elección no sea obvia leyendo el código (porque B también funcionaría), regístrala aquí. Sin esto, en 6 meses no recuerdas por qué.

## Cuándo crear ADR
- Elegir librería/herramienta entre alternativas reales (no "uso fetch porque sí").
- Schema de BD donde había 2+ formas válidas (single table vs split, FK vs JSON, etc.).
- Patrón arquitectónico (monolito vs micro, queue vs sync, etc.).
- Decisión que revertir luego costaría >1 día.

## Cuándo NO crear ADR
- Convenciones obvias del framework.
- Cambios revertibles en <1h.
- Bug fixes (van a `Stack/incidents.md`).

## Formato
Copiar `_template.md`, máx 15 líneas. Si necesita más, hay debate pendiente — resuélvelo antes.

## Index
<!-- añade aquí cada ADR como 1 línea: NNN · YYYY-MM-DD · título -->
- 001 · 2026-05-11 · [[ADR-001-cron-observability|Observabilidad de crons via tabla cron_runs + Dokploy externo]] (TuFacturaIA)
- 002 · 2026-05-18 · [[ADR-002-bot-state-machine-postgres|State machine conversacional del bot WhatsApp en Postgres chat_state]] (TuFacturaIA)
- 003 · 2026-05-18 · [[ADR-003-slot-resolver-determinista|Slot resolver determinista pre-LLM con regex en español]] (TuFacturaIA)
- 004 · 2026-05-18 · [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding|Tool calling con tool_choice forzado para extracción estructurada]] (agency-portal)
- 005 · 2026-05-18 · [[ADR-005-exencion-codigo-per-linea|Código exención IVA per-línea en lineas_factura.exencion_codigo]] (TuFacturaIA)
- 006 · 2026-05-20 · [[ADR-006-defense-in-depth-superadmin-impersonation|Override vs union semantics en impersonación de superadmin]] (TuFacturaIA)
- 007 · 2026-05-20 · [[ADR-007-sin-acceso-fallback-vs-loop-redirect|Página /sin-acceso para JWT vivo sin org operable]] (TuFacturaIA)
- 008 · 2026-05-20 · [[ADR-008-matriz-permisos-rol-aware-bd|Matriz canónica user_can_write_in_org BD + espejo TS]] (TuFacturaIA)
- 009 · 2026-05-21 · [[ADR-009-invitacion-consent-explicito-vs-activo-directo|Invitaciones consent explícito (toda invite = pending hasta aceptar)]] (TuFacturaIA)
- 010 · 2026-05-21 · [[ADR-010-helper-sql-atomico-vs-endpoint-encadenado|Helper SQL atómico para acciones con chain de triggers fiscales]] (TuFacturaIA)
- 011 · 2026-05-21 · [[ADR-011-bot-whatsapp-org-switch-v1-dos-turnos-vs-reprocesado|Bot WhatsApp org switch — v1 dos turnos vs reprocesado automático]] (TuFacturaIA)
- 012 · 2026-05-22 · [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo|EcoBox sin CRM tradicional — Chatwoot compartido AgentesIA]] (EcoBox)
- 013 · 2026-05-22 · [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode|EcoBox Retell Conversation Flow en Rigid Mode]] (EcoBox)
- 014 · 2026-05-22 · [[ADR-014-ecobox-log-universal-sheet-vs-chatwoot-voice-conversation|EcoBox log universal de leads en Google Sheet, no Chatwoot conversation]] (EcoBox)
- 015 · 2026-05-22 · [[ADR-015-centro-fiscal-mvp-vs-roadmap-completo|Centro Fiscal IA arranca como MVP 4 semanas, no roadmap 11 semanas]] (TuFacturaIA)
- 016 · 2026-05-22 · [[ADR-016-centro-fiscal-pricing-14-90|Centro Fiscal IA pricing 14,90€/mes (149€/año), no 9€ spec original]] (TuFacturaIA)
- 017 · 2026-05-22 · [[ADR-017-centro-fiscal-no-presenta-v1|Centro Fiscal IA v1 NO presenta telemáticamente, convenio AEAT diferido]] (TuFacturaIA)
- 018 · 2026-05-22 · [[ADR-018-centro-fiscal-stripe-scope-3-tiers-plus-addon|Centro Fiscal IA Stripe scope = 3 tiers TuFacturaIA + add-on, no solo add-on]] (TuFacturaIA)
- 019 · 2026-05-24 · [[ADR-019-precio-inclusive-iva-storage-canonico-vs-columna-precio-modo|Precio "con IVA incluido" en form: storage canónico base + toggle UX-only]] (TuFacturaIA)
- 020 · 2026-05-25 · [[ADR-020-source-of-truth-datos-emisor-template-config-vs-columnas|Datos emisor: template_config.emisor JSON único, columnas legacy deprecadas, sync explícito en código]] (TuFacturaIA)
- 021 · 2026-05-25 · [[ADR-021-html-email-strings-vs-react-email-mjml|HTML strings tipados para 6 templates email vs React Email/MJML]] (TuFacturaIA)
- 022 · 2026-05-27 · [[ADR-022-multidivisa-facturas-equivalente-eur-congelado|Facturas en divisa: equivalente EUR congelado + agregar siempre en EUR, VeriFACTU diferido]] (TuFacturaIA)
- 023 · 2026-05-28 · [[ADR-023-mapping-client-portal-cliente-remote-id-facturaia|Mapping client portal ↔ cliente_remote_id FacturaIA via union de fuentes, sin migration]] (agency-portal)
- 024 · 2026-05-29 · [[ADR-024-multidivisa-facturas-recibidas|Multidivisa facturas recibidas: FX en bandeja_ingesta congelado al aprobar]] (TuFacturaIA)
- 025 · 2026-05-29 · [[ADR-025-drive-sync-outbox-vs-fire-and-forget|Drive sync de PDFs facturas usa outbox + worker, no fire-and-forget post-response]] (TuFacturaIA)
- 026 · 2026-05-29 · [[ADR-026-saas-billing-stripe-hmac-fases-1-2|SaaS billing Stripe + HMAC fases 1-2]] (TuFacturaIA)
- 027 · 2026-05-31 · [[ADR-027-disponibilidad-slots-precomputados-vs-calculo-en-llm|Disponibilidad de citas: backend devuelve slots pre-computados, el LLM no calcula]] (Simarro)
- 028 · 2026-06-05 · [[ADR-028-multiempresa-scope-navegar-agregar-cobrar|Multiempresa: navegar=membresía, agregar=propiedad, cobrar=cuenta]] (TuFacturaIA)
- 029 · 2026-06-13 · [[ADR-029-conciliacion-casos-asientos-no-ledger|Conciliación casos contables (préstamos/suplidos/compensación): NO ledger, aproximación por categorización como ámbito futuro]] (TuFacturaIA)
- 030 · 2026-06-16 · [[ADR-030-ingreso-sin-factura-ticket-vs-fuera-iva|Ingreso sin factura: ticket (simplificada) para ventas con IVA al 303; "sin factura" solo para no sujetos]] (TuFacturaIA)
- 031 · 2026-06-16 · [[ADR-031-stock-lotes-opt-in|Stock por partidas/lotes: opt-in híbrido por producto, motor aislado]] (TuFacturaIA)
- 032 · 2026-06-18 · [[ADR-032-mcp-oauth-as-split-app-servicio-handroll|AS OAuth del MCP partido app↔servicio + hand-roll (no @jmondi)]] (TuFacturaIA)
- 033 · 2026-06-18 · [[ADR-033-posicionamiento-popovers-floating-ui|Posicionamiento de popovers anclados con @floating-ui/react (no CSS anchor positioning aún, no cálculo casero)]] (TuFacturaIA)
- 034 · 2026-06-19 · [[ADR-034-paginacion-offset-vs-keyset|Paginación UI interna — offset vs keyset]] (TuFacturaIA)
- 035 · 2026-07-01 · [[ADR-035-control-canal-ingesta-pantalla-unica-vs-duplicado|Control de un canal de ingesta vive en una sola pantalla, con estado de solo lectura en el resto]] (TuFacturaIA)
- 036 · 2026-07-03 · [[ADR-036-export-contable-libro-registro-sin-pgc|Export contable gestorías: libro registro CSV/XLSX sin cuentas PGC; A3/Sage nativos diferidos]] (TuFacturaIA)
- 037 · 2026-07-04 · [[ADR-037-whatsapp-verificacion-proveedor-y-cobro-embebido|WhatsApp: verificación de proveedor externo por confirmación manual del admin (no OTP, no solo-NIF) + cobro embebido vía Stripe Connect (no Redsys/Bizum v1)]] (TuFacturaIA)
- 038 · 2026-07-17 · [[ADR-038-emitidas-importadas-registro-espejo-sin-verifactu|Facturas emitidas importadas de otro SIF: registro espejo contable sin VeriFactu (no re-emitir, no elegir usuario)]] (TuFacturaIA)
- 039 · 2026-07-25 · [[ADR-039-org-module-config-patch-merge-con-allowlist|org_module_config.config se escribe con PATCH de merge por clave + allowlist del schema resuelto (no replace, no RPC atómica en v1)]] (TuFacturaIA)
- 040 · 2026-07-25 · [[ADR-040-btchbookg-apunte-agrupado-por-defecto|BtchBookg a `true` por defecto en remesas SEPA: apunte agregado para que la auto-conciliación case, expuesto como ajuste (no fijo, no dejarlo en false)]] (TuFacturaIA)
- [ADR-041](ADR-041-recibida-duplicada-se-elimina-no-se-anula.md) — una recibida duplicada se elimina (no se anula: `anulada` no sale del 303 en recibidas)
- [ADR-042](ADR-042-base-imponible-neta-en-todos-los-tipos.md) — `base` es la base imponible NETA en todos los tipos; presupuestos conservan el descuento en cabecera y facturas lo reparten en líneas (VeriFACTU)
- [[ADR-043-sin-ci-el-gate-local-es-el-contrato]] — sin CI, los hooks locales son el contrato; los workflows dejan de arrancar solos para que el rojo vuelva a significar algo.
- [[ADR-044-tabla-unica-de-contactos-en-vez-de-una-por-modulo]] — una sola tabla de contactos para toda la app: dos tablas obligan al usuario a una distinción que no tiene en la cabeza, y copiar entre ellas congela el dato.
- [[ADR-045-el-coste-medio-se-rehace-desde-el-ledger-al-revertir-una-compra]] — al revertir una compra el coste medio se recalcula desde el ledger aunque pise un valor tecleado a mano: un acumulado no se arregla repitiendo la operación buena.
- [[ADR-046-secretos-por-service-account-no-en-env-en-claro]] — los secretos se leen con service account (`opsa`) y hook que bloquea el `op` interactivo; nunca se vuelcan a un `.env` en claro.
- [[ADR-047-escalon-1-openai-para-el-agente-de-agh-provisional]] — de momento OpenAI directo y se cambia si hace falta: la elección de proveedor es nuestra y reversible por config, pero NO autoriza el egress de filas al modelo, que es del cliente final.
- [[ADR-049-pagos-declarados-en-ledger-aparte-del-de-banco]] — los cobros sin banco detrás van a su propio ledger y recompute pasa a ser el único escritor del estado; se unifica la LECTURA (una sola función suma), no el almacenamiento.
- [[ADR-050-el-modelo-frasea-solo-donde-el-guard-puede-rechazarlo]] — el LLM reformula solo donde un guard determinista puede rechazarlo; la lectura cuyo texto lleva un hecho no verificable se declara literal. Ni ampliar la whitelist (persigue el caso) ni apagar el fraseo (era su único trabajo).
- [[ADR-051-el-redondeo-de-importes-sube-el-medio-centimo]] — el `x,xx5` sube (variante con `Number.EPSILON`): 55 copias del redondeo a una sola en `lib/dinero/`. `lib/fiscal` queda fuera, ya usa céntimos con `BigInt`.
- [[ADR-052-persistir-el-motivo-de-la-suspension-de-cobro]] — el motivo de la suspensión decide quién puede reactivar (facturaia, cobro)
- [[ADR-053-la-cita-de-doctoralia-vive-en-conversation-state]] — la cita se persiste en `conversation_state.paciente_data.cita` (JSONB ya existente) porque sin SSH no hay DDL; el upsert pasa a merge para no pisarla. Migrar a tabla propia si hace falta observabilidad.
- [[ADR-054-la-busqueda-del-vault-es-lexica-fts5-no-semantica-ni-grafo]] — índice FTS5 local (MRR@10 0,957 · Recall@10 100 %) frente a embeddings, híbrido o grafo: con el recall saturado, lo demás compra ~5 % a cambio de un modelo que mantener. Reabrir solo si `.vault-queries.log` acumula fallos por vocabulario.
- [[ADR-055-la-rectificativa-del-303-va-detras-de-capturar-el-justificante]] — el nº de justificante de la autoliquidación anterior (13 posiciones del diseño oficial) lo da la AEAT al presentar, así que registrar el resultado no es la alternativa barata a generar la rectificativa: es su dato de entrada. Orden #1933 → #1934 → #1899.
- [[ADR-056-que-va-al-claude-md-y-que-a-un-rule-con-paths]] — arriba la regla dura en una línea, abajo el porqué; puede bajar lo que un hook determinista ya bloquea, y se queda lo que se ejecuta sin leer ficheros (mergear, desplegar, renumerar). Un `paths:` dispara con `Read`, no con Bash.
- [[ADR-057-el-loop-de-tickets-no-mergea-a-main]] — sin CI ni branch protection, el gate local no basta para un squash irreversible: el gate mide el árbol y el commit es posterior, así que no existe un «HEAD validado». El loop deja PR. PR #2105.
