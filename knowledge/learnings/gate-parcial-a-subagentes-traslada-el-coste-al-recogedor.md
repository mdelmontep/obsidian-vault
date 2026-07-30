---
title: recortar el gate a los subagentes no ahorra trabajo, lo traslada al que recoge
date: 2026-07-30
source: claude-code-session facturaia
tags: [claude-code, subagentes, harness, gate, metodo]
---
Con la máquina saturada prohibí a 5 agentes de fix correr `lint` y `build`: solo
`vitest` y `typecheck`. Los 5 obedecieron y lo declararon. Al recoger:

- 1 de 5 no pasaba `lint` (error `react-hooks/set-state-in-effect` + 2 warnings),
  y era una regla que ya está escrita en el CLAUDE.md global.
- 2 de 5 no pasaban `build` (uno por symlink de `node_modules`, ver
  [[worktree-qa-next-standalone-symlink-node-modules]]; otro por llamar una función
  `'use client'` desde un Server Component, ver
  [[server-component-no-puede-llamar-funcion-use-client]]).

O sea: **8.500 tests verdes y typecheck limpio en 5 worktrees, y 3 de ellos no
compilaban o no lintaban.** El coste no desapareció, se pagó más tarde y por mí,
cuando ya había dado el trabajo por bueno.

Si la máquina no aguanta el gate completo, la respuesta es **serializar los agentes
hasta que aguante**, no recortar la verificación de cada uno. Y si aun así recortas,
el gate completo en ventana exclusiva es obligatorio ANTES de commitear, no después
de abrir el PR.

Corolario: devolver el fix al agente que lo escribió (con el diagnóstico y "imita el
patrón de los ficheros vecinos") sale mejor que parchearlo tú — la salida correcta
exige leer esos vecinos, y él ya tiene el contexto cargado.
Ver [[claude-code-agentes-worktree-failure-modes]].
