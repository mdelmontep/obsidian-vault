---
title: campo de extracción LLM sin regla anti-invención explícita se alucina por defecto
date: 2026-07-22
source: claude-code-session
tags: [ocr, llm, prompt-engineering, hallucination, facturaia]
---
Prompt de extracción con 15+ campos, la mayoría con guard explícito ("NUNCA
inventes X, devuelve null si no aparece") — NIF, IRPF, referencia catastral,
intracomunitario. Un campo (`forma_pago`) solo tenía el ejemplo inline
`"Transferencia, Domiciliacion, Tarjeta, Efectivo..."` sin esa regla.

Resultado real: un ticket de restaurante con "PENDIENTE DE COBRO" y sin
ninguna mención de medio de pago salió con `forma_pago: "Efectivo"`. El LLM
no alucina todos los campos por igual — alucina justo los que no tienen el
guard, aunque el resto del prompt sea estricto.

Fix: no basta con dar un ejemplo de valores válidos en el JSON de salida;
cada campo opcional/inferible necesita SU PROPIA regla explícita de "solo si
aparece literal, si no null" (mismo patrón que [[llm-source-quote-anti-alucinacion-extraccion]]
pero sin necesitar cita — basta la prohibición explícita).

Al auditar un prompt de extracción, listar TODOS los campos y verificar que
cada uno tiene guard, no asumir que "está implícito" por los vecinos.
