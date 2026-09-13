---
title: un ciclo de imports deja la constante undefined y el caso de test deja de medir
date: 2026-09-13
source: facturaia
tags: [modulos, imports, tests, e2e]
---

A importa de B una constante y B importa de A. Si el objeto de módulo de B se evalúa antes de que
A termine, la constante vale `undefined` (transpilado a CJS/esbuild no hay TDZ que avise). Un
`const CUERPOS = { id: UUID_INEXISTENTE }` queda con `id: undefined`, `JSON.stringify` quita la
clave, y el endpoint devuelve 400 por validación en vez del 404/403 que el caso quería medir. El
test sigue verde: «rechaza» es cierto por el motivo equivocado.

Fix: la constante compartida va a un módulo hoja sin imports del resto. Candado: un test que exige
que ningún cuerpo tenga campos `undefined`, y un suelo de casos medidos que no pueda bajar.

Caso real: `permisos-parametro` de TuFacturaIA, 27 casos cross-org sin medir desde el #2058 (#2758).
