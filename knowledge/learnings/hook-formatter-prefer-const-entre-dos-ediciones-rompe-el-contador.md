---
title: un hook formatter con prefer-const entre dos ediciones rompe el contador añadido después
date: 2026-08-25
source: facturaia
tags: [hooks, eslint, harness, typescript]
---
Un hook PostToolUse que auto-formatea con `eslint --fix` corre ENTRE tus ediciones: si declaras
`let x = 0` en una edición y el `x++` llega en la siguiente, prefer-const convierte el `let` en
`const` en el hueco. La suite no lo caza por tipos (esbuild transpila sin typechequear): falla en
runtime con un TypeError tragado que se manifiesta como conteos a 0 en asserts lejanos del punto real.
Fix: declarar la variable y su primera reasignación EN LA MISMA edición; si el autofix ya pasó,
`grep 'const <var>'` antes de culpar a la lógica. Señal típica: un test que esperaba N llamadas ve 0
sin ningún error visible en el output.
