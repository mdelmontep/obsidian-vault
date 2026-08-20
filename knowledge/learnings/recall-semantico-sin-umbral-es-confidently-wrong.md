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
4. Calibra el umbral con un golden set en **las dos direcciones** (consulta ajena → debe negar;
   paráfrasis → debe recuperar), contra el modelo real y no solo fakes. Ver
   [[busqueda-hibrida-sql-pgvector-supabase]].

**El fallo simétrico es igual de caro y más difícil de ver** (Tecnocloud, 18-ago): umbral fijo alto
(`WHERE similarity > 0.70`) mata la paráfrasis del usuario y el sistema queda mudo pareciendo que
falta contenido. Medido sobre el mismo corpus: la frase del documento daba **0.8222** y la del
cliente («contraseña caducada») **0** — no 0.6, cero, porque el filtro la descartaba antes. Bajarlo a
0.55 pasó la cobertura de 2 a 12 temas de 20 sin añadir un documento. Regla: **recall en el SQL,
precisión en el LLM** — el umbral duro no sabe leer, el modelo sí, así que dale candidatos con su
nivel de confianza y una instrucción explícita de descartar lo que no trate del mismo problema (sin
esa frase, 4 de 10 recuperados eran impertinentes).
