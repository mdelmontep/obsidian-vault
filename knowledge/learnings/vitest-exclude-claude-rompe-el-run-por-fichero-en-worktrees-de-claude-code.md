---
title: vitest con exclude de .claude no encuentra tests por fichero dentro de un worktree de claude code
date: 2026-09-13
source: agh-iberica
tags: [vitest, worktrees, claude-code, testing]
---
Los worktrees de la CLI viven en `<repo>/.claude/worktrees/<n>`. Un `vitest.config.ts` con
`exclude: ["**/.claude/**"]` (puesto para no duplicar tests de worktrees) casa también con la ruta ABSOLUTA
del propio worktree: `npx vitest run test/x.test.ts` da «No test files found», exit 1.
Trampa: el run completo (`npm run gate`) sí encuentra los tests, así que el gate sale verde y solo falla
el ciclo TDD por fichero — parece que el fichero no existe o el filtro está mal escrito.
Salida: config temporal SIN esa exclusión (`vitest.mut.config.ts`, sin commitear) y `--config`; un
symlink no sirve. Arreglo de raíz: anclar la exclusión a la raíz del proyecto, no `**/`. AGH #1717.
Relacionado: [[una-ruta-de-scratchpad-de-sesion-en-fichero-trackeado-caduca-con-la-sesion]]
