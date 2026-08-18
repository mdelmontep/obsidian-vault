---
title: ADR-054 — la búsqueda del vault es léxica (SQLite FTS5), no semántica ni de grafo
date: 2026-08-18
status: accepted
tags: [adr, vault, obsidian, busqueda]
---

## Contexto

1.606 learnings creciendo a ~24/día, sin más recuperación que `grep`: un `grep -ril test` devuelve 479 ficheros, el 30 % del corpus. Restricción real: lo consume un agente por shell (5.996 llamadas Bash frente a 1.039 Read), sin plugins de Obsidian instalados, y el mantenimiento recae en una sola persona.

## Opciones consideradas

- **A — índice léxico local (SQLite FTS5)** — cero dependencias (`node:sqlite`, Node ≥22), 80 ms/consulta, sin API ni servicio; no capta sinónimos.
- **B — embeddings + búsqueda densa** — encuentra sin compartir palabras; exige modelo, reindexado y una pieza más que mantener.
- **C — híbrido léxico+denso (RRF o ponderado)** — el mejor en los benchmarks públicos; suma el coste de A y B.
- **D — grafo de conocimiento / GraphRAG** — responde preguntas multi-salto; hay que construir el grafo, resumir comunidades y pagar varias llamadas de modelo por consulta.

## Decisión

**A**, porque medido sobre 120 consultas da **MRR@10 0,957 y Recall@10 100 %** (grep: 0,481 y 89,2 %). Con el recall saturado, B y C compran ~5 % de nDCG en benchmarks a cambio de un modelo y un índice más. D resuelve preguntas de varios saltos que aquí casi no se hacen.

## Consecuencias

Sin cobertura de sinónimos: si aparecen consultas fallidas por vocabulario, están en `.vault-queries.log` y **ese** es el disparador para reabrir esto, no la intuición. El ranking (cobertura de términos + bonus por nombre + penalización por tamaño) queda atado a `scripts/vault-find.test.mjs`: tocarlo sin correr el gate es tocarlo a ciegas. La cifra 0,957 sale de consultas derivadas del propio documento, así que es un techo optimista — la medida honesta llegará con consultas reales acumuladas.

Ver [[un-vault-sin-indice-invertido-obliga-a-nombrar-las-notas-como-frases]] · [[un-experimento-que-mide-algo-contra-si-mismo-da-el-100-por-cien]]
