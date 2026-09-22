---
title: un teardown de playwright ignora el filtro de ficheros y se cuela en todo subconjunto
date: 2026-09-22
source: facturaia
tags: [playwright, e2e, arnes]
---
Con `teardown: 'X'` en un proyecto, X corre **entero** cada vez que corre aquel proyecto, **aunque la línea de comandos filtre por fichero**. Lo mismo pasa con `dependencies`.

Caso real (facturaia #2854): colgué `smoke-aislado` (specs que suspenden la org sandbox) como teardown de `escenarios` para que corriera al final aunque hubiera rojos. Resultado: el candado de permisos del pre-push (`--project=smoke-escritura permisos-*`) arrastraba además esas 15 pruebas, y también cualquier subconjunto del alcance. Ningún test lo veía, porque la tanda entera sale igual.

- Cómo detectarlo: `npx playwright test --list <filtro>` y contar por proyecto (`grep -oE "\[[a-z-]+\]" | sort | uniq -c`).
- Solución: colgar el teardown solo cuando la tanda lo pide, con una variable de entorno (`E2E_SMOKE_AISLADO_AL_FINAL=1`) que ponen los scripts de la tanda entera. Suelto, el proyecto lleva sus `dependencies` normales.
- El candado prueba los dos modos: carga la config con `vi.resetModules()` y `vi.stubEnv`, y comprueba que sin la variable no hay teardown.

Relacionado: [[tanda-e2e-sin-comprobar-el-servidor-vivo-al-final-no-es-medicion]]
