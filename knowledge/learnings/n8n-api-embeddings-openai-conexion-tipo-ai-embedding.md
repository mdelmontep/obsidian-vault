---
title: n8n api embeddings openai se conecta via ai_embedding no ai_vectorStore
date: 2026-04-16
source: claude-code-session
tags: [n8n, api, pgvector, embeddings, conexiones]
---

Al crear conexiones por API (`PUT /api/v1/workflows/{id}`) entre un nodo `Embeddings OpenAI` y un `PGVector Store`, el tipo de conexión correcto es `ai_embedding`:

```json
{
  "Embeddings OpenAI": {
    "ai_embedding": [[{
      "node": "Buscar FAQ",
      "type": "ai_embedding",
      "index": 0
    }]]
  }
}
```

## Error si se usa `ai_vectorStore`

```
Issues:
- No node connected to required input "Embedding"
```

El nodo PGVector aparece con triángulo rojo en el editor. El workflow puede guardarse pero no ejecutarse.

## Regla general

Los tipos de conexión en n8n siguen el nombre del input slot del nodo destino:
- `ai_tool` → herramientas del agente
- `ai_languageModel` → modelo LLM
- `ai_embedding` → embeddings para vector stores
- `ai_memory` → memoria del agente
- `ai_vectorStore` → vector store conectado al agente (no al embedding)
