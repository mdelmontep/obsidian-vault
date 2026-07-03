---
title: FacturaIA — Histórico detallado de hitos cerrados
date: 2026-06-28
tags: [facturaia, historico]
---

<!-- Archivo destino para hitos cerrados movidos desde facturaia.md hub.
     Añadir en orden cronológico descendente. 1-2 líneas por hito. -->

2026-07-03 · **Exportación contable para gestorías COMPLETA (tren #653/#654/#657/#658 mergeado)** — libro registro normalizado (1 fila por factura × tipo IVA, XLSX 3 hojas + CSV `;`/coma, IRPF prorrateado con ajuste de céntimo, degradación por hoja Avisos) + **formato oficial AEAT** (plantilla LSI v9.0 de la sede, importable en Pre303 y A3 sin mapeo) + /informes conectado al endpoint (fix TZ rangos −1 día, columna IVA=total−base, resumen con floats, cards muertas) + deep-link en copiloto. De regalo: **fix Libro IVA roto en prod** (500 permanente, columnas x100 inexistentes) + loader compartido con paginación max-rows y chunking `.in()` + `isOrgInTrial` con regla fiscal server-side. QA: Playwright 6/6, verificación numérica independiente al céntimo (export ≡ casillas 303 en pantalla ≡ recompute BD), auditoría 3-agentes con fixes. Merge `--admin` (OK Manu). Pendiente: deploy+smoke prod, Pre303 HITL. Ver [[ADR-036-export-contable-libro-registro-sin-pgc]] · [[facturaia-export-gestoria-v15]].

2026-07-02 · **Migración clientes Supabase tipados COMPLETA (PR #648, mergeado con review 8-ángulos)** — `createAdminClient`/`createServerSupabase`/browser → `SupabaseClient<Database>`; 341 errores→0 en 12 commits gate-verdes (alias tipado incremental), suite 4320 tests, `as any` src 29→10. **10 bugs prod destapados** (clase 42703 silencioso): worker VeriFACTU no-op desde 05-18, emails branding fallback, duplicar v1 404, is_admin nunca concedido, fallback PDF email, export fiscal sin NIF, getURLPDF presupuestos, /api/health modo lectura, audit admin global, rama muerta sourceTable. Nuevos `zod-json.ts` + `database-overrides.ts`. Decisiones pendientes → gotchas.md (§VeriFACTU, §Auth). Merge `--admin` (revisión delegada por Manu). Ver [[supabase-tipar-admin-client-global-cascada-300-errores]] · [[supabase-select-columna-inexistente-falla-query-entera-42703]] · [[supabase-gen-types-numeric-override-bigint-string]].

2026-07-01 · Ticket rápido (PRs #620-#635, #631, #637) — emisión proactiva de factura simplificada sin movimiento bancario, para cobro en efectivo/Bizum al momento. Fase 1 web (endpoint + modal standalone + entrada sidebar/generar + PDF/email) y Fase 2 Copiloto (`emitirTicket`). Fix same-day tras QA visual del usuario: `estado` quedaba `pendiente` sin marcar cobrado (contaminaba KPIs/cashflow/vencidas) + inputs/select sin estilo canónico `form-input`. Verificado en real contra sandbox. Ver [[documento-dinero-ya-cobrado-debe-marcarse-cobrada-explicito]].

2026-06-30 · Presupuestos propios detectados en OCR (issues `ingesta-presupuesto-001..006`, `40a6b0c3`+`810aa86c`): `doc_type='presupuesto'` local a `ocr-process` (sin ensuciar el `DocType` compartido con conciliación), descarte+`tipo_generado` reutilizado, migración `presupuesto_id`, endpoint `crear-presupuesto` idempotente con guard de duplicado y cierre de race, CTA en ingesta-view. Smoke real cazó y arregló 2 bugs de prompt; clasificación queda pendiente de validar con un presupuesto real (no solo el fixture sintético). Ver [[mock-no-actualizado-tras-refactor-io-rompe-suite-sin-aviso]] (de paso arreglé la suite de tests rota).

2026-06-30 · PR #607 — «Convertir en recurrente» en menú `…` lista de emitidas + overlay panel en modal detalle (gateado módulo SEPA) + refactor ingesta justificante a state machine keyed por item. Ticket Borja.

2026-06-28 · fix duplicar factura: copia líneas+presentación (`unidad_medida`, `cantidad_presentacion`), nunca hereda `lote_id` (#578) + test regresión e2e + invariante CLAUDE.md (#580). Ticket Dani 3eb1aec3.
