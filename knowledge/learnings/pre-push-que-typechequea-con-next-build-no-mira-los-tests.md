---
title: un pre-push que typechequea con next build no mira los ficheros de test
date: 2026-08-14
source: claude-code-session
tags: [next, typescript, gates, hooks, ci, facturaia]
---

El `pre-push` de facturaia corre TypeScript, pero **dentro de `next build`**, y next no
compila los `*.test.ts`. El que sí los mira es `npm run typecheck` (tsc con el tsconfig
entero), que vive en el `pre-commit`.

El agujero: una rama que **solo rebasa y empuja** —sin commit propio— no dispara el
`pre-commit`, así que puede meter en `main` un error de tipos en un test sin que nada lo
pare. Pasó al fusionar a mano dos harness de test de PRs hermanos: quedó un stub con el
interfaz de una rama y el cuerpo de la otra (TS2739), `main` en rojo y todas las ramas
siguientes bloqueadas al rebasar encima.

- Es exactamente el caso que más se da en una tanda de merges: rebasar, gate, push.
- Síntoma engañoso: el `pre-commit` de la SIGUIENTE rama es quien te lo cuenta, así que
  parece que lo rompió esa rama y no el merge anterior.
- Antes de mergear una rama sin commits nuevos: `npm run typecheck` a mano.
- El arreglo de verdad es que el hook corra el typecheck completo, no el de `next build`.

**CERRADO el 22-ago (facturaia #2096): la suite ya corre en `pre-push`.** Hasta ese día los
hooks cubrían tres de las cuatro etapas de `npm run gate` — `grep -nE "vitest|npm run test"
.githooks/*` no devolvía NADA —, así que «push con los hooks en verde» no significaba que los
tests pasaran, y esa frase se dijo en una tanda de merges. El coste medido: el merge de #2077
dejó `main` con `1 failed | 14613 passed` y nadie lo vio (sin CI, y el squash no pasa por
ningún gate). Se arregló el síntoma en #2094 y la causa en #2096. Va antes del build, que es
más caro y falla más tarde. No sube al `pre-commit`: ya se pasa del timeout del shell de los
agentes.

Relacionado: [[conflicto-rebase-json-generado-regenerar-no-mergear-a-mano]] · y el agujero mayor:
el `pre-push` no EJECUTA los tests, así que los guards estructurales solo salen en la suite
sobre `main` mergeado → [[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]].
