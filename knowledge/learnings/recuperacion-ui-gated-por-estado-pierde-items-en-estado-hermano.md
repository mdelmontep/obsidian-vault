---
title: recuperacion UI gateada por etiqueta de estado pierde items en estado hermano
date: 2026-06-16
source: claude-code-session
tags: [facturaia, ocr, race-condition, ux, fire-and-forget]
---

Dos gotchas que se combinan en un fallo invisible:

**(a) FAF vs await sobre la misma fila.** Un `void promise.then()` (fire-and-forget) que actualiza una fila compite contra un `await` que actualiza la MISMA fila. Gana el awaited; la escritura FAF se pierde sin error. Caso: en `ocr-process`, ante un fallo de extraccion, `auditParseFailure` (await → `processOcrAudit` con needs_review) deja el item en `estado='revisar'`, mientras `alertOcr502` (FAF) que lo pondria en `'error'` no llega a aplicarse antes del 502.

**(b) Recuperacion gateada por la ETIQUETA de estado, no por la condicion.** El boton "Reintentar OCR" solo salia con `estado==='error'` (y el endpoint rechazaba `'revisar'`). Los items que caen en el estado hermano `revisar` con datos vacios quedan sin via de recuperacion → "Sin datos extraidos" eterno.

Fix: gatear la afordancia por la **condicion real** (sin datos extraibles: prov/total/fecha) en CUALQUIER estado terminal, no por el nombre del estado. PR #277.

Relacionado: [[n8n-502-deja-items-huerfanos-en-bandeja-sin-retry]].
