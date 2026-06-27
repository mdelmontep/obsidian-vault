---
title: zod v4 trae z.toJSONSchema nativo — deriva el tool-schema del LLM, no lo dupliques a mano
date: 2026-06-27
source: claude-code-session
tags: [zod, llm, tool-use, schema, facturaia]
---

Zod v4 (≥4.3.6) expone `z.toJSONSchema(schema, { io: 'input' })` NATIVO: deriva el
JSON Schema que ve el LLM desde el Zod que ya valida los params. No hace falta la dep
externa `zod-to-json-schema`.

Anti-patrón: mantener un `input_schema_json` escrito a mano EN PARALELO al Zod. El Zod
es quien valida (`safeParse`), así que el JSON a mano es una copia lossy que diverge en
silencio y **miente al LLM**: `required:[]` cuando el Zod sí exige el campo (→ el LLM lo
omite → `invalid_params`), o `type:string` cuando es `z.enum`.

Fix: una sola fuente (Zod), JSON derivado. Las descripciones por campo van en `.describe()`
(toJSONSchema las propaga). `.refine()` se descarta (igual que el JSON a mano, sin regresión).
Strip `$schema` de la salida (Anthropic/OpenAI quieren el objeto plano). El derivado añade
`additionalProperties:false` / `format` / `pattern` / `anyOf`(nullable) — son mejoras, más
fieles al contrato real. Caso real: FacturaIA #536 (43 tools copiloto, −499 LOC).
Ver [[zod-v3-no-tiene-z-email-ni-z-uuid-como-top-level]] · [[output-llm-validar-zod-y-auditar-parse-failures-en-bd]].
