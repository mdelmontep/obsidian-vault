---
title: un await import() dentro del it consume el timeout del test con la máquina cargada
date: 2026-10-13
source: agency-portal
tags: [vitest, testing, flaky]
---
Síntoma: un test pasa en solitario (2,5 s) y falla en la suite completa con «Test timed out in 5000ms», también en `main`. Solo falla el PRIMER `it` del fichero.

Causa: el patrón `vi.mock(...)` + `const { fn } = await import('./service')` DENTRO de cada `it`. El primer import transforma todo el grafo del módulo y ese tiempo cuenta contra el timeout del test. Con carga alta (load 30-60, varias sesiones) pasa de 5 s.

Fix: si el fichero no usa `vi.resetModules()`, subir el import a top-level await junto a los mocks. El coste pasa a la fase `collect`, que no tiene timeout: los tests bajaron de 2,2 s a 10 ms (`src/lib/billable-charges/unlink.test.ts`, 13-oct).

Antes de culpar a tu rama: correr la suite en un worktree de `origin/main`. Si falla igual, es flake preexistente.
