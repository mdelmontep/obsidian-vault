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
copia en todo el árbol, incluida la referencia interna de `next`. Verificar
con `npm ls sharp` — debe mostrar `next → sharp@X deduped`, no dos versiones
distintas. `npm audit fix --force` NO es la solución aquí (puede proponer
downgradear `next` entero como atajo, ver
[[npm-audit-fix-force-propone-downgrades-trampa]]).
