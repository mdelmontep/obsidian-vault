---
title: ocr clasifica doc_type no-factura pero no extrae sus campos
date: 2026-06-30
source: claude-code-session
tags: [facturaia, ocr, llm-prompt]
---
En ocr-process (PASO 0 del prompt), si doc_type clasificado NO es "factura"
(es "justificante_pago"/"extracto"/"desconocido"), el LLM devuelve SOLO
{"doc_type": "..."} y nada más — no extrae total/fecha/prov/nif. Es ahorro
de coste intencional (issue 036), pero cualquier feature que lea
bandeja_ingesta.datos_extraidos asumiendo esos campos poblados para esos
doc_type falla en silencio (siempre vacío).

Fix/patrón: features sobre justificante/extracto necesitan un SEGUNDO pase
de extracción específico (extractMovimientosFromDoc, doc-extract.ts) que
descargue el documento de Storage y lo vuelva a procesar — no leer
datos_extraidos directamente. Ya pasó antes con seguros IVA=0
([[ocr-clasificacion-iva-zero-seguros]]) — mismo prompt, gotcha hermano.
