---
title: build no corre vitest; un test de cardinalidad de registry rompe en CI al añadir entrada
date: 2026-06-05
source: claude-code-session
tags: [ci, testing, facturaia]
---
El pre-commit del repo (`lint && typecheck && build`) NO ejecuta los tests; el
step "Test" del CI (vitest) sí. Añadir una tool al registry del copiloto
(`src/lib/copiloto/registry.ts`) pasó lint/typecheck/build local pero **CI falló**:
`registry.test.ts` fijaba "expone N tools" + `toHaveLength(N)`.
- Patrón: cualquier coleccion con test de conteo/listado (registries, enums,
  catálogos) rompe al añadir un elemento aunque compile.
- Fix: actualizar el test (lista + length) al añadir.
- Prevención: si tocas un registry/catálogo con test, corre `npx vitest run`
  antes de push (build no basta).
