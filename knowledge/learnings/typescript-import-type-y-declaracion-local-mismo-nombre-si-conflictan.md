---
title: import type y una declaración local del mismo nombre SÍ conflictan (TS2440)
date: 2026-08-05
source: claude-code-session — gate G-RL-ENCHUFADO de tucrmia
tags: [typescript, gotcha]
---

Hipótesis a verificar: `import type { X } from 'mod'` vive en el namespace de TIPOS y una
`function X()`/`const X` local vive en el de VALORES, namespaces separados en TS, así que un
gate de "¿el identificador `X` viene de `mod`?" que sólo mira el texto del import podría
evadirse declarando `X` localmente al lado de un `import type` señuelo del mismo nombre.

**Falso.** TypeScript SÍ los trata como el mismo binding a efectos de colisión de nombres:
`import type { crearLimitador } from '...'` + `function crearLimitador() {}` en el mismo
ámbito da `TS2440: Import declaration conflicts with local declaration`. No compila, ni con
`function` ni con `const`.

Antes de asumir que una evasión de este tipo es posible en un gate/regla, reproducirla con
`tsc --noEmit` sobre un fichero mínimo — no basta con leer la especificación de namespaces de
tipos/valores, hay que probar el caso exacto.
