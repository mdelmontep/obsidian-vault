---
title: los scripts .mjs no los typechequea astro check, y un cambio de shape los rompe mudo
date: 2026-09-10
source: ecobox
tags: [typescript, astro, gates, refactor]
---
`astro check` (y `tsc` sin `checkJs`) **no mira los `.mjs`**. En un repo donde los
scripts de build/verificación son `.mjs` pero importan tipos y datos de `src/lib/*.ts`,
un cambio de shape sale con **build verde y typecheck verde**, y revienta en
runtime la próxima vez que alguien corra el script — que suele ser después de
desplegar.

Medido: `SITE.address` → `LOCATIONS[]` dejó `scripts/verify-desplegado.mjs`
llamando a una propiedad inexistente. Ningún gate lo vio; se descubrió corriéndolo
a mano contra un servidor local.

Aplicación del «cambio en shape compartido = grep todos los consumidores»: el
compilador enumera los consumidores **tipados**, no todos. Los `.mjs`, los
templates y lo que vive fuera del repo hay que enumerarlos a mano.

Fix barato: `// @ts-check` en cabecera del `.mjs` + `checkJs` en el tsconfig de
scripts, o convertirlos a `.ts`. Ver [[un-consumidor-del-shape-puede-vivir-fuera-del-repo]].
