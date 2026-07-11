---
title: output llm validar con zod y auditar parse failures en bd
date: 2026-06-11
source: claude-code-session
tags: [llm, zod, observabilidad, ocr]
---
Output de LLM parseado con cast ciego (`JSON.parse(x) as Tipo`) + fallo solo a
`console.error` = fallos invisibles: no sabes la tasa real de JSON inválido en prod.

Patrón:
1. `safeParse` Zod (todo opcional + `.passthrough()`).
2. En fallo (parse o schema): fila en tabla de auditoría queryable con anomaly
   type + raw truncado, ANTES de devolver el 5xx.
3. Campos que el prompt marca "OBLIGATORIOS" → default conservador que dispare
   revisión humana (p.ej. `confianza='baja'`), nunca `null` silencioso.

Caso: ocr-process TuFacturaIA 2026-06-11 (PR #197).
Matiz posterior (#834): un 200 no-parseable NO debe devolver 5xx — es una
negativa del modelo, no un fallo. Auditar sí, pero → revisión manual sin retry
ni alerta. Ver [[llm-responde-200-no-json-no-es-fallo-pipeline]] · [[llm-tool-calling-elimina-silent-fail-extraccion-estructurada]] · [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]]
