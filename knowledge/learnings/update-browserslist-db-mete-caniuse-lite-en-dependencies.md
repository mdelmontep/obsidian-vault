---
title: update-browserslist-db mete caniuse-lite en dependencies
date: 2026-08-01
source: claude-code-session
tags: [node, build, dependencias]
---
El aviso de Vite «browsers data is N months old» sugiere `npx update-browserslist-db@latest`.
Ese comando **añade `caniuse-lite` y `baseline-browser-mapping` a `dependencies`** del
`package.json` — como dependencias directas de producción, que no lo son: las usa la
cadena de build (browserslist, autoprefixer) por debajo.

Además el aviso no suele venir del paquete raíz sino de **copias anidadas** viejas
(`node_modules/autoprefixer/node_modules/caniuse-lite`). Comprobarlo antes de tocar nada:
`find node_modules -path "*caniuse-lite*" -name package.json`.

Fix limpio: `"overrides": { "caniuse-lite": "^<versión>" }` y reinstalar. Una sola copia,
manifiesto intacto.

Ojo al medir el beneficio: en este caso el propio actualizador dijo **«No target browser
changes»** — mismos 32 navegadores objetivo antes y después. Es higiene, no rendimiento.
