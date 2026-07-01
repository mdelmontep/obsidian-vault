---
title: vitest fileparallelism:false para tests de integración que comparten una bd
date: 2026-07-02
source: claude-code-session
tags: [vitest, testing, postgres, ci, flakiness]
---

Vitest paraleliza **ficheros** de test por defecto. Si dos ficheros de integración comparten
una única Postgres y cada uno hace `TRUNCATE … CASCADE` global en `beforeAll`, se pisan entre
sí → fallos intermitentes (fila borrada a mitad, FK violada en un upsert). Pasa "a veces",
según el timing → difícil de diagnosticar.

Fix: `vitest.config.ts` → `test: { fileParallelism: false }`. Serializa la ejecución de
ficheros; los casos dentro de un fichero ya van en orden. La suite pequeña lo absorbe
(coste de segundos) y elimina toda una clase de flakiness para cualquier test DB-backed.

Señal de que es patrón real, no anécdota: dos personas del equipo convergieron en la misma
solución el mismo día al añadir cada una un fichero `*.pg.test.ts`.
