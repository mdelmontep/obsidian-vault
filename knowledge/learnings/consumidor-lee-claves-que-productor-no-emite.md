---
title: consumidor que lee claves de campo que el productor no emite falla en silencio
date: 2026-06-05
source: claude-code-session
tags: [contratos, jsonb, testing, ocr]
---
JSONB sin tipo compartido entre productor y consumidor = contrato implícito por
nombres de campo. Si divergen, el lector recibe `undefined`, no error.
Caso TuFacturaIA: OCR (route n8n + prompt) emite shape corto `prov/nif/total/
base/iva/iva_pct`; `anomaly.ts` leía shape largo `nif_emisor/importe_total/...`
→ `missing_*` saltaba en TODA factura (falsos positivos) y bank/p95/iva nunca
corrían (features muertas en silencio ~semanas).
Doble fallo: los tests pasaban porque usaban el shape largo fantasma, y los del
route mockeaban la función bajo prueba → el bug nunca se ejercitó.
Fix: alinear el lector al shape real (única fuente; ambos productores ya
coinciden) + migrar tests al shape de producción + 1 test de regresión con
datos reales. Regla: shape compartido → grep TODOS los consumidores y testear
con el shape que produce el sistema, no uno inventado.
Ver [[cliente-react-bypasa-endpoint-canonico-bug-fiscal-latente]], [[test-mocks-rename-import-path-no-rename-import]].
