---
title: en eslint flat config el último bloque que casa reemplaza el array de la regla, no concatena
date: 2026-07-30
source: claude-code-session
tags: [eslint, lint, guards, ci]
---
Con `no-restricted-syntax` (y cualquier regla cuyas opciones sean un array) los bloques de
flat config **no se suman**: para un fichero dado gana el último bloque que casa, y su array
sustituye entero al anterior. Separar una regla en dos bloques por ámbito parece organizar y
en realidad **mata en silencio los selectores del bloque anterior**. Sin warning, sin error:
la regla sigue "puesta" y ya no dispara.

Me pasó al resolver un conflicto entre dos guards: dejé muerto el de controles nativos en
`src/components/` (seguía vivo en `src/app/`, que es lo que engañaba) y de paso dos
preexistentes que no había tocado nadie.

Fix: los selectores viven en **constantes** y cada bloque compone su propia unión completa.
Y la comprobación no es leer el config, es **verlo en rojo**: reintroducir el patrón a
propósito en un fichero temporal, confirmar el error, borrarlo. Un guard que nunca has visto
fallar no está demostrado. Ver [[crawler-que-escribe-informe-y-sale-cero-es-recolector-no-test]].
