---
title: source_quote literal del usuario como ancla anti-alucinación en extracción LLM
date: 2026-05-18
source: claude-code-session
tags: [openai, llm, prompt-engineering, hallucination]
---

Cuando el LLM extrae campos estructurados de la conversación, exige una cita
literal del usuario por cada campo. Si no puede citar, no extrae.

Schema:
```ts
extracted_fields: z.array(z.object({
  section: z.enum([...]),
  field_key: z.string(),
  value: z.string(),
  source_quote: z.string().min(1).max(240),  // cita literal
}))
```

Prompt: *"source_quote: copia literal del fragmento del usuario del que
extraes el valor. Si no puedes citar fielmente, NO extraigas ese campo."*

Parser descarta entradas con quote vacío como red de seguridad runtime.

Coste: ~50 tokens extra por field. Beneficio:
- Elimina invenciones del modelo ("normalizando" lo que dijo el usuario).
- Trazabilidad: para cada valor en BD sabes la frase exacta que lo generó.
- Auditoría: cuando un cliente reclama un valor "no lo dije así", tienes la cita.

No reemplaza validación de schema; complementa. Patrón universal para
extracción LLM en flujos críticos (onboarding, formularios, KYC).
