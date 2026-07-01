---
title: FacturaIA — Histórico detallado de hitos cerrados
date: 2026-06-28
tags: [facturaia, historico]
---

<!-- Archivo destino para hitos cerrados movidos desde facturaia.md hub.
     Añadir en orden cronológico descendente. 1-2 líneas por hito. -->

2026-07-01 · Ticket rápido (PRs #620-#635, #631, #637) — emisión proactiva de factura simplificada sin movimiento bancario, para cobro en efectivo/Bizum al momento. Fase 1 web (endpoint + modal standalone + entrada sidebar/generar + PDF/email) y Fase 2 Copiloto (`emitirTicket`). Fix same-day tras QA visual del usuario: `estado` quedaba `pendiente` sin marcar cobrado (contaminaba KPIs/cashflow/vencidas) + inputs/select sin estilo canónico `form-input`. Verificado en real contra sandbox. Ver [[documento-dinero-ya-cobrado-debe-marcarse-cobrada-explicito]].

2026-06-30 · Presupuestos propios detectados en OCR (issues `ingesta-presupuesto-001..006`, `40a6b0c3`+`810aa86c`): `doc_type='presupuesto'` local a `ocr-process` (sin ensuciar el `DocType` compartido con conciliación), descarte+`tipo_generado` reutilizado, migración `presupuesto_id`, endpoint `crear-presupuesto` idempotente con guard de duplicado y cierre de race, CTA en ingesta-view. Smoke real cazó y arregló 2 bugs de prompt; clasificación queda pendiente de validar con un presupuesto real (no solo el fixture sintético). Ver [[mock-no-actualizado-tras-refactor-io-rompe-suite-sin-aviso]] (de paso arreglé la suite de tests rota).

2026-06-30 · PR #607 — «Convertir en recurrente» en menú `…` lista de emitidas + overlay panel en modal detalle (gateado módulo SEPA) + refactor ingesta justificante a state machine keyed por item. Ticket Borja.

2026-06-28 · fix duplicar factura: copia líneas+presentación (`unidad_medida`, `cantidad_presentacion`), nunca hereda `lote_id` (#578) + test regresión e2e + invariante CLAUDE.md (#580). Ticket Dani 3eb1aec3.
