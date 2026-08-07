---
title: bump de una dep directa no basta si otra dep la fija como optionalDependency vieja
date: 2026-07-23
source: claude-code-session — FacturaIA PR #1177 (sharp CVE)
tags: [npm, dependencies, security, sharp, nextjs]
---
`next` declara `sharp` como su propia `optionalDependency` fijada a un rango
(`^0.34.5`) para su image-optimizer interno. Si subes `sharp` en tus propias
`dependencies` a una versión fuera de ese rango (p. ej. `^0.35.3` para un CVE),
npm NO falla — pero deja **dos copias** en el árbol: la tuya nueva top-level y
una vieja anidada bajo `next/node_modules/sharp`. `npm audit` puede seguir
marcando la vulnerabilidad como resuelta a medias, y el binario nativo real
que se empaqueta puede ser el viejo según el orden de resolución.

Fix: `"overrides": { "sharp": "^0.35.3" }` en `package.json` fuerza una única
copia en todo el árbol, incluida la referencia interna de `next`.
`npm audit fix --force` NO es la solución aquí (puede proponer
downgradear `next` entero como atajo, ver
[[npm-audit-fix-force-propone-downgrades-trampa]]).

**REINCIDIÓ en TuCRMIA el 07-ago**, mismo par `next`/`sharp` (+ `postcss@8.4.31`),
15 días después. Dos correcciones al método de arriba:

- **`npm ls` NO basta para verificar.** Enseña lo que hay en `node_modules`, que puede
  estar desfasado del lockfile: llegó a decir `sharp@0.35.3 invalid` mientras el lockfile
  fijaba `0.34.5` y `npm ci` habría reinstalado la vulnerable. **La verificación real es
  `npm ci` en un árbol vacío** (copiar `package.json` + `package-lock.json` a un temporal),
  que es lo que hace el Dockerfile.
- **Dentro de la misma minor puede no haber salida**: `next@16.2.12` seguía en
  `postcss@8.4.31`; sólo 16.3.0 lo subía. `overrides` evita tener que decidir la subida de
  framework dentro de un arreglo de seguridad.

Y lo de fondo: existía este learning y volvió a pasar, porque el repo nuevo **no tenía el
gate** — ver [[un-plan-que-hereda-patrones-de-un-repo-hermano-da-por-existente-lo-que-solo-existe-alli]].
