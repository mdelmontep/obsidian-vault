---
title: un fix validado solo con fakes in-memory puede ocultar un bug de prod solo-Postgres
date: 2026-07-09
source: claude-code-session
tags: [testing, postgres, persistencia, in-memory-fake, tdd]
---

Añadí un campo nuevo (`lastThreadDigest`) a un objeto de estado persistido (`ConversationState`).
Los tests in-memory pasaron (el `InMemory*Store` guarda el objeto entero) → mergeado. Pero el
`Postgres*Store` **no persistía el campo** (no estaba en el `SELECT`/`INSERT` ni había columna) →
en prod (canal stateless: cada mensaje es un request nuevo que relee de la BD) el campo se perdía y
el fix **no funcionaba en producción**, solo in-memory.

**Regla:** al añadir un campo a un objeto de estado que se persiste, la verificación in-memory NO
basta:
1. Grep el store Postgres (columnas + `get`/`set`/`toRow`): ¿está el campo en el round-trip?
2. Añadir migración (columna) + reflejo en `schema.sql` (+ pasar el drift-gate).
3. Test pg de **round-trip** (`set` → `get` devuelve el campo; y se limpia al reconstruir sin él).
4. Correr el backstop pg ANTES de declarar hecho un fix de persistencia/migración.

El fake in-memory es un espejo INCOMPLETO del store real; un test que solo lo ejercita valida la
lógica, no la persistencia. Ver [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]].
