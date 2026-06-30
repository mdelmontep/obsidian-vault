---
title: ocr llm clasifica como justificante_pago docs con iva=0 si prompt requiere iva para "factura"
date: 2026-06-30
source: claude-code-session
tags: [ocr, llm-prompt, ingesta, seguros]
---
- Recibos de prima de seguro: IVA=0 por Ley 37/1992 art. 20.Uno.16. Son facturas recibidas, no justificantes bancarios.
- Si PASO 0 define "factura" mencionando IVA, el LLM excluye docs con iva=0 → los clasifica `justificante_pago` → auto-descarte → `hasData=false` → "Sin datos extraídos".
- Mismo riesgo: sanidad, educación, intracomunitarias (todos iva=0, todos son facturas válidas).
- Fix: definir "factura" por presencia de EMISOR identificado (empresa/autónomo que cobra), no por IVA.
- "justificante_pago" = comprobante bancario de UNA transferencia. NO recibo de proveedor ni aseguradora.
- Archivo: `src/app/api/internal/whatsapp/ocr-process/route.ts` `buildExtractionInstruction()` PASO 0.
- UI: cuando `doc_type` es `justificante_pago`/`extracto`, mostrar destino (`/conciliacion`) en vez del genérico "Sin datos".
