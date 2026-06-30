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
- **IPS ≠ IVA (recibos de seguro)**: "Impuestos repercutibles" / "Impuesto sobre Primas de Seguros" es IPS, no deducible como IVA. Fix: REGLA 14 (`iva:0, iva_pct:0` en seguros) + guard display en `hero-card.tsx` (PR #599).
- **NIF emisor extranjero (US/UK/IE) sin NIF español es esperado, no anomalía grave**: `anomaly.ts` marcaba `missing_nif_emisor` siempre `severity:'high'` → forzaba revisión en TODO recibo SaaS extranjero (Resend, AWS, Stripe) aunque la propia REGLA 10 ya documentaba el caso. Fix: severidad `medium` (no fuerza revisión sola) si `pais≠ES` o `moneda≠EUR`. 2026-06-30.
