---
title: busqueda hibrida sql + pgvector en supabase para catalogos
date: 2026-05-03
source: claude-code-session
tags: [supabase, pgvector, embeddings, rag, search]
---

Patrón reusable para catálogos con criterios estructurados + texto libre (inmuebles, productos, libros, etc): combinar filtros SQL con ranking semántico pgvector en una sola RPC.

## Esquema

```sql
CREATE TABLE items (
  id UUID PRIMARY KEY,
  -- campos estructurados (zona, tipo, precio...)
  embedding VECTOR(1536),
  status TEXT DEFAULT 'active'
);
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## Función match

```sql
CREATE FUNCTION match_items(query_embedding VECTOR, ...filtros, match_count INT)
RETURNS TABLE (..., similarity FLOAT) LANGUAGE SQL STABLE AS $$
  SELECT ..., 1 - (embedding <=> query_embedding) AS similarity
  FROM items WHERE status='active' AND (filtro1 IS NULL OR ...) ...
  ORDER BY embedding <=> query_embedding LIMIT match_count;
$$;
```

## Uso desde n8n

OpenAI `text-embedding-3-small` (1536d) → POST `/rest/v1/rpc/match_items` con embedding + filtros opcionales → top-K con similarity score.

Validado en Simarro: query "chalet con piscina y jardín en Las Rozas" → 2 resultados similarity 0.64 y 0.61.
