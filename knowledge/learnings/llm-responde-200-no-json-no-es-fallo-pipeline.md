---
title: llm responde 200 con no-json (negativa) no es fallo de pipeline
date: 2026-07-11
source: claude-code-session
tags: [llm, ocr, observabilidad, colas, alertas]
---
Un LLM que responde 200 pero con texto no-JSON (o JSON que no valida el schema)
suele ser una NEGATIVA/narración, no un fallo técnico: la API respondió. Caso
real: gpt-4o rehúsa leer un DNI y contesta "I'm sorry,"/"Lo siento," → JSON.parse
falla.

Anti-patrón: tratarlo como 5xx. El worker de cola lo reintenta N veces (inútil —
una negativa no cambia al reintentar, solo quema llamadas) y dispara alerta de
outage al superadmin (falso positivo; en TuFacturaIA saltó "OCR en fallo" ALTA
en 3 orgs reales por documentos de identidad).

Patrón: ramificar por el status HTTP del proveedor. `!resp.ok` (non-2xx) = fallo
real → retry + alerta. resp 200 no-parseable = resultado esperado → estado de
revisión manual (sin datos), SIN retry, SIN alerta; auditar el motivo en BD.
NUNCA auto-descartar (no distingues un doc no-factura de una factura real
ilegible). La regresión sistémica se detecta con un sweep sobre la tabla de
audit, no con una alerta por documento.

Caso: ocr-process TuFacturaIA #834 (2026-07-11).
Ver [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]] · [[n8n-502-deja-items-huerfanos-en-bandeja-sin-retry]] · [[caller-timeout-debe-cubrir-peor-caso-del-retry-interno]]
