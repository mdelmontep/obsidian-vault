---
title: declarar `exclude` en vitest sustituye al de fábrica, y sin `**/` solo tapa la raíz
date: 2026-08-16
source: claude-code-session
tags: [vitest, eslint, tests, falsos-positivos, gates]
---

`exclude: ['node_modules/**']` **reemplaza** el default (`**/node_modules/**`), no se suma. Solo queda
fuera el `node_modules` **de la raíz**: cualquiera anidado entra en la suite. Y hay uno anidado en
cuanto un test enlaza `node_modules` dentro de un fixture para arrancar un `next dev` de verdad.

Medido (TuCRMIA, `vitest list --filesOnly`, mismo árbol): **571 ficheros recogidos vs 379**, 192 de
dependencias, ejecutados. El síntoma no es un rojo — es `Tests 5172 passed` sobre una suite de
**5.094**: pruebas ajenas contadas como propias, con el número **subiendo**, que es la dirección en la
que nadie mira. De ahí salían ficheros a 900 s, `Failed to start forks worker` y una víctima distinta
cada corrida durante ocho corridas.

Mismo error en `eslint.config.mjs` (`globalIgnores(['.next/**', 'next-env.d.ts'])`): analizaba el
`.next/dev/types/*.ts` del fixture → **41 errores de código que no es tuyo**. Y prettier reventaba con
`ENOENT` sobre el `tsconfig.json` que el fixture genera y borra → gate en **2**.

Regla: *lo que un test genera dentro del árbol no puede verlo quien recorre el árbol*, y se vigila
preguntando a la herramienta (`ESLint.isPathIgnored`), no al texto de su config — que es justo lo que
parecía correcto. Medido también: acotar `--maxWorkers` **no** protege si otra corrida no se acota (la
acotada es la que cae). Ver [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]].
