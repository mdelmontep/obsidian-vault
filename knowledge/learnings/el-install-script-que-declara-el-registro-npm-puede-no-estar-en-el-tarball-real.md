---
title: el install script que declara el registro npm puede no estar en el tarball real
date: 2026-08-07
source: claude-code-session — TuCRMIA, auditoría de cadena de suministro
tags: [npm, seguridad, supply-chain, docker, sharp]
---
npm 11.16+ avisa de paquetes con install scripts sin cubrir por `allowScripts`. Hoy es
**solo informativo** — los scripts SIGUEN ejecutándose; quien bloquea es
`--ignore-scripts` o `--strict-allow-scripts`.

Dos cosas que solo se ven mirando, no leyendo el aviso:

- **El aviso miente por exceso**: sale del manifiesto del REGISTRO, no del paquete.
  `fsevents@2.3.3` declara `install: node-gyp rebuild` en el registro y su tarball real
  NO trae ese script (comprobado con `npm pack` + leer el `package.json` de dentro).
  `package-lock.json` copia esa metadata en `hasInstallScript`, así que arrastra el error.
- **`--ignore-scripts` no rompe los binarios nativos modernos**: `sharp` no tiene
  `install`/`postinstall`; sus binarios llegan por `optionalDependencies` (`@img/sharp-*`).
  Igual `unrs-resolver` con `@unrs/*`.

Por eso `npm ci --ignore-scripts` es seguro en el Dockerfile — pero **compruébalo
instalando en un árbol vacío**, no leyendo el lockfile: `npm ls` puede enseñar versiones
que `npm ci` no reproduce si el lockfile va desfasado.

Relacionado: [[npm-overrides-necesario-cuando-dependencia-fija-optionaldependency-vieja]]
