# Clinica Zen — Supabase Vector Store

## Infraestructura

- **Servidor**: `185.47.13.168`
- **n8n**: `n8nclinicazen.agentesia.madrid`
- **Supabase**: solo acceso interno (sin dominio público), accesible desde n8n vía red Docker
- **Stack**: Supabase self-hosted en Dokploy

## Schema SQL (pgvector + LangChain)

```sql
-- 1. Habilitar la extensión pgvector (necesaria para columnas vector)
create extension if not exists vector;

-- 2. Crear la tabla documents (esquema estándar LangChain)
create table if not exists documents (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(1536)
);

-- 3. Crear índice para búsquedas rápidas por similitud coseno
create index on documents using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);

-- 4. Crear la función match_documents (la que usa n8n para el RAG)
create or replace function match_documents (
  query_embedding vector(1536),
  match_count int default 5,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

## Conexión desde n8n

- Nodo: **Supabase Vector Store**
- URL interna: `http://supabase-kong:8000` (dentro de dokploy-network)
- Autenticación: Service Role Key (JWT)

## Notas

- Embeddings de 1536 dimensiones = modelo OpenAI `text-embedding-ada-002` o `text-embedding-3-small`
- El índice ivfflat con `lists = 100` es adecuado hasta ~100k documentos. Si crece más, considerar HNSW
- La función `match_documents` filtra por `metadata @> filter` — permite filtrar documentos por campos del jsonb (ej: por cliente, categoría, etc.)
- Google Service Account bloqueado por política de org `iam.disableServiceAccountKeyCreation` — se usa OAuth2 como fallback para Calendar/Gmail

---

*Creado: 2026-04-16*
