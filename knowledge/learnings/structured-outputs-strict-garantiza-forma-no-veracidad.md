---
title: Structured Outputs (json_schema strict) garantiza la FORMA, no la veracidad
date: 2026-07-11
source: claude-code-session
tags: [openai, llm, structured-outputs, grounding]
---
OpenAI Structured Outputs (`response_format: {type:"json_schema", strict:true}`) es el modo
recomendado sobre el `json_object` antiguo: garantiza que la salida cumple el schema (type-safety,
sin reintentos de formato). Soportado en `gpt-4o-2024-08-06`+ y `gpt-4o-mini` (pinear snapshot).

GOTCHA: garantiza **solo la forma, NO la veracidad del contenido** (docs: "you remain responsible
for validating content accuracy separately"). Un LLM con strict puede inventar datos y aun así
devolver un JSON perfectamente válido.

Consecuencia: si le das hechos al LLM para que los reformule (reads fraseados, resúmenes grounded),
strict NO impide que añada/cambie filas o cifras → hace falta un **verificador determinista aparte**
(en código: todos los items presentes, ningún dígito nuevo, conteo conservado → si no, fallback al
texto original). No confundir "JSON válido" con "JSON verdadero".
