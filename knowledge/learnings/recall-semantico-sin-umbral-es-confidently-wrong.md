---
title: recall semántico con k=1 sin umbral de distancia es confidently-wrong por diseño
date: 2026-07-09
source: claude-code-session
tags: [rag, recall, pgvector, embeddings, agentes]
---

Un recall/RAG que hace `searchByEmbedding(query, LIMIT 1)` y devuelve el resultado SIN mirar la
distancia **siempre** devuelve el vecino más cercano como si fuera la respuesta — aunque no tenga
nada que ver con la pregunta. Delante de un cliente = mentir con seguridad (el peor modo de fallo).
Caso real AGH (`recallByQuery`): con una sola nota de "perfiles Java", preguntar por otro tema citaba
la nota de Java con su fecha.

**Fix (reusable en cualquier RAG):**
1. La query devuelve la **distancia coseno** (`embedding <=> $q AS distance` en pgvector; `1 - cos`
   en memoria), no solo las filas.
2. **Umbral de relevancia**: por encima → "no me consta" honesto, no el vecino más cercano.
3. **top-k** (no k=1) + **atribución** de cada cita a su fuente (la query semántica no trae el
   cliente/documento; sin atribuir, el usuario no sabe de quién es lo citado).
4. Calibra el umbral con un **golden set negativo** (consulta ajena → debe negar; paráfrasis → debe
   recuperar). Verifícalo contra el modelo real, no solo fakes. Ver [[busqueda-hibrida-sql-pgvector-supabase]].
