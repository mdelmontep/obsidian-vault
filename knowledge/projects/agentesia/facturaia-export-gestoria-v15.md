---
title: FacturaIA — Export gestoría v1.5 (spec/prompt de la siguiente iteración)
date: 2026-07-03
source: claude-code-session
tags: [facturaia, fiscal, export, spec]
---

Prompt entregado a Manu el 2026-07-03 (tras mergear el tren #653/#654/#657/#658). 5 workstreams, en orden; multi-agente + plan corto + OK antes de codificar; PRs pequeños apilados; auditoría 3-agentes al final + resumen ELI5.

1. **Validación Pre303 (HITL)** — generar XLSX AEAT real de FacturaIA Sandbox (2T 2026), validar offline contra plantilla LSI v9.0 (posiciones, Decimal(12,2), dd/mm/yyyy, fichero `Ejercicio+NIF@Nombre`), checklist paso a paso para que Manu lo importe en Pre303 con certificado; iterar el serializador si falla. Registrar resultado en el hub.
2. **Asientos de diario PGC** (diseño ADR-036) — columna `cuenta_contable` en clientes/proveedores (mig NNN al abrir PR) + defaults en `org_module_config` fiscal (430/400/700/600/472/477/4751) + autoasignación 430.0001… al exportar. Serializador `formato=asientos` (fecha, asiento, cuenta, concepto, debe, haber; test de cuadre debe=haber). Emitida = 430x/700x/477x (+4751x IRPF); recibida = 600x/400x/472x.
3. **Datos no capturados** — epígrafe IAE en perfil_fiscal (wizard + Settings), flag `bien_inversion` en recibidas (aprobación + editor), prorrata en perfil (default 100). Criterio de caja NO (régimen bloqueado) — solo hueco documentado. Cablear cada dato al serializador AEAT con test.
4. **IA "Revisa mi export"** — botón en Avisos (+card /informes) que abre el copiloto con los avisos como contexto y tools: completar NIF/nombre vía VIES (`src/lib/fiscal/vies.ts`), listar facturas sin líneas con deep-link, re-generar export. Patrón preview/commit; nunca modificar sin confirmación.
5. **WhatsApp fase 1** — intención "mándame el libro del 2T" → deep-link firmado de un solo uso (HMAC+TTL, patrón vincular Slack). Adjuntar fichero = fase 2 (análisis de seguridad aparte). Gate: feature fiscal + rol del user vinculado.

Referencias: `src/lib/fiscal/export/{export-contable,load-facturas-contables,aeat-libros-xlsx}.ts`, route `/api/fiscal/[ejercicio]/export-contable`, plantilla oficial parseada en la cabecera de `aeat-libros-xlsx.ts`, [[ADR-036-export-contable-libro-registro-sin-pgc]].

---

## Estado 2026-07-03 (sesión de implementación)

**Worktree**: `/Users/manueldelmonte/facturaia/.claude/worktrees/export-v15`. PRs apilados base main, **sin merge** (QA localhost + Pre303 HITL pendientes):
- **#668 · WS1** `feat/export-v15-ws1-pre303` — `scripts/verify-export-aeat.ts` + fixture plantilla oficial `LSI_plantilla_v9.0.xlsx` (cotejo real, no circular) + `docs/fiscal/pre303-import-checklist.md`. XLSX real del Sandbox 2T 2026 en `~/Downloads/2026B87654323@FacturaIA Sandbox.xlsx` — 36/42 cabeceras exactas, 60/60 + 9/9 facturas, Σ cuadra al céntimo.
- **#669 · WS2** — asientos PGC `formato=asientos` (`src/lib/fiscal/export/asientos-contables.ts`) + mig **425** `cuenta_contable` + 8 cuentas PGC en `catalog.ts`. Autoasignación 8 díg. (43000001…). Cuadre debe=haber verificado (69 asientos, 32.066,55 €).
- **#672 · WS3** — mig **426** `es_bien_inversion` + `epigrafe_iae` + `prorrata_deduccion_pct`; wiring al serializador AEAT (IAE col 5, Bien Inversión col 21, Cuota Deducible×prorrata) + captura UI (wizard/settings/bandeja).

**Decisiones fijadas**: subcuentas 8 díg contiguos · IRPF **473** emitidas / **4751** recibidas (doc `docs/architecture/asientos-contables-pgc.md`) · consentimiento permanente (esta sesión) para migs aditivas a prod.

**Follow-ups**: (1) pooler Supabase caído → `supabase db push` para registrar mig 426 en `schema_migrations` al recuperar (columnas ya en prod, no-op IF NOT EXISTS) — ver [[supabase-pooler-caido-aplicar-ddl-via-mcp]]; (2) Pre303 HITL (Manu, con certificado); (3) QA localhost (:3010).

**Falta**: WS4 (IA "revisa mi export": 3 tools copiloto preview/commit — VIES/facturas-sin-líneas/regenerar — + botón Avisos + card /informes), WS5 (WhatsApp deep-link firmado HMAC + tabla ledger `export_signed_links` mig 427 + intención n8n), auditoría 3 agentes, manuales, 2 resúmenes. Retomar por WS4.

---

## Estado 2026-07-03 (sesión 2 — WS4+WS5+auditoría+manuales)

- **#674 · WS4** `feat/export-v15-ws4-copiloto` (sobre #672, draft) — 3 tools copiloto: `revisarExportContable`/`listarFacturasSinLineas` (lectura, agrupan avisos sin generar fichero) + `completarNifContraparte` (destructive, NIF←NIF-IVA validado por VIES, nunca escribe si no_concluyente/inválido). Botón "Revisar con IA" en dropdown Gestoría (`header-acciones.tsx`) + card en `informes-view.tsx`, ambos vía `CustomEvent('open-ai-assistant')`.
- **#677 · WS5** `feat/export-v15-ws5-whatsapp` (sobre #674, draft) — mig **427** `export_signed_links` (ledger single-use, RLS service-role). `signExportLink`/`consumeExportLink` (HMAC+TTL 30min, patrón `action-token.ts`). `build-export-response.ts` extraído del route de sesión — fuente única para el endpoint autenticado y el nuevo `GET /api/fiscal/export-contable-firmado` (público, token en query, añadido a `isServiceRoute`). Tool `enviarLibroExportWhatsapp`: **sin cambios en n8n** — reusa el puente `/api/internal/whatsapp/copiloto` ya existente (mismo registry que la web, `channel` ya no filtra tools desde G5·A S5). Adjuntar fichero = fase 2, sin implementar.
- **Migraciones 426+427 registradas en prod** vía `mcp__supabase__apply_migration` (pooler 5432 seguía caído). `get_advisors` solo INFO esperado (RLS sin políticas, mismo patrón que `bot_error_log`). `database.types.ts` regenerado vía MCP (nota: el JSON de la MCP omite el schema `graphql_public` que sí trae `supabase gen types --linked`; sin consumidores en el repo, typecheck limpio — vigilar si se re-genera con el CLI en el futuro y reaparece el diff).
- **Auditoría cross-PR (3 agentes paralelos, diff completo main..ws5)**: sin bloqueantes. 2 fixes aplicados (commit `aec11bb9`): granularidad de error restaurada en `build-export-response.ts` (`db_error`/`cuentas_error` en vez de genérico) + mensaje claro en `completarNifContraparte` cuando el NIF-IVA validado ya pertenece a otro contacto (23505).
- **Manuales actualizados** (commit `289e9508`): `manual-usuario.md` (5 descargas del menú Gestoría, epígrafe IAE/prorrata en Settings, checkbox "Bien de inversión", secciones "Revisar con IA" y envío por WhatsApp) + `manual-admin.md` (endpoint firmado, conteo tools copiloto 57→63).
- **Verificador numérico re-corrido tras el refactor** (`scripts/verify-export-aeat.ts` contra Sandbox 2T 2026) — VERDE, confirma que `build-export-response.ts` no cambió el fichero generado.

**Falta**: QA localhost/prod de todo el stack (ver hub `Smoke tests pendientes`), Pre303 HITL (Manu), registrar mig 426 vía CLI cuando el pooler recupere (ya registrada por MCP, solo verificar sin duplicados), 2 resúmenes de cierre (técnico + ELI5).

---

## QA en localhost contra Sandbox real (2026-07-03, misma sesión)

Login e2e+smoke en `:3010` contra FacturaIA Sandbox (org `b5f86e8f-...`, ejercicio 2026 2T con datos reales). 6 flujos probados, 1 bug real encontrado y arreglado, 0 bloqueantes tras el fix.

- **Menú Gestoría**: las 6 opciones visibles y correctas (Excel/CSV×2/Libros AEAT/Asientos/Revisar con IA).
- **revisarExportContable**: 47 avisos reales del periodo (31 sin NIF, 6 divisas≠EUR, 10 sin líneas) — coincide con el verificador `verify-export-aeat.ts`.
- **🐛 Bug real encontrado**: pedir "completa el NIF de la primera contraparte" tras revisarExportContable devolvía "No he encontrado ese cliente" — `revisarExportContable` solo da CONTADORES (`contrapartes_sin_nif_completables: number`), nunca ids, así que el LLM no tenía de dónde sacar el `id` que exige `completarNifContraparte`. Fix: nueva tool `listarContrapartesSinNif` (simétrica a `listarFacturasSinLineas`, da `tabla+id+completable`), commit `f5d0fd0e` en #677. Verificado tras el fix: la cadena de 3 tools funciona y el guard de VIES rechaza correctamente un NIF-IVA de test inválido del Sandbox (no escribe nada, mensaje claro).
- **listarFacturasSinLineas**: deep-links correctos (`/recibidas?factura=ID`).
- **Settings Fiscal (IAE/prorrata)**: guardado confirmado por consulta directa a BD (`epigrafe_iae='763'` persistido) — el primer intento pareció fallar por un problema del navegador automatizado (botón fuera del viewport reducido, no del producto).
- **Bandeja "Bien de inversión"**: checkbox interactivo confirmado (toggle a `checked=true`); no se aprobó el documento para no archivar datos reales del Sandbox.
- **WS5 WhatsApp**: verificado por API (POST firmado HMAC a `/api/internal/whatsapp/copiloto` simulando el receptor n8n, `from_phone` de un admin real del Sandbox) — generó el enlace, la descarga devolvió el XLSX válido (`export-contable-2026-2T.xlsx`, 16.569 bytes), y el segundo intento con el mismo token devolvió **410 single-use** como diseñado. No probado desde un WhatsApp real (teléfono físico).

Informe completo con capturas (Artifact Claude Code, sesión 2026-07-03).

**Pendiente real tras este QA**: (1) Pre303 HITL con certificado (Manu); (2) smoke desde un WhatsApp real (el flujo API está probado, falta el canal físico); (3) mergear el stack 668→669→672→674→677 y repetir el smoke básico en prod.
