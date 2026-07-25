---
title: un aviso con "parche disponible" puede tener el parche inaplicable — probarlo antes de creerlo
date: 2026-07-25
source: claude-code-session facturaia
tags: [npm, seguridad, dependencias, auditoria]
---

Que un GHSA diga `first_patched_version: X` no significa que puedas llegar a X. Antes de dar por
arreglada una vulnerabilidad transitiva, o de rechazar baselinearla "porque tiene parche", hay que
**instalar el override y ejecutar algo real**. Un `npm audit` en verde no prueba nada.

Caso real: `brace-expansion` GHSA-mh99-v99m-4gvg (high, DoS por OOM), parche en 5.0.8. Con
`overrides: {"brace-expansion":"^5.0.8"}` el árbol instala, las 3 instancias colapsan a 5.0.8, `npm
audit` baja de 16 avisos a 2 y el trinquete se pone verde. **Y está roto**: la 5.x pasó a
`type: module` con mapa `exports` y cambió la forma del export, mientras `minimatch@3` hace
`require('brace-expansion')` esperando una función → `TypeError: expand is not a function` y
`npm run lint` con exit 2 en `@eslint/config-array`. Si te fías del audit verde, subes el lint roto.

Comprobación que decide si el parche es alcanzable: mirar qué rango pide **cada** consumidor
intermedio. Aquí `minimatch@3` pide `^1.1.7`, `minimatch@9` pide `^2.0.1` y `minimatch@10` ya no la
declara → ninguna versión de minimatch acepta la 5.x, y 1.x/2.x están cerradas sin backport. Parche
inalcanzable, no "pendiente de aplicar".

Y para aceptarla con criterio, medir explotabilidad en vez de suponerla: el fallo exigía un *patrón*
que expandir → `grep` de `glob(`/`minimatch(` en el código propio (0 hits) y prueba funcional de la
cadena de runtime (escribir y releer un xlsx real). Ver [[npm-audit-fix-force-propone-downgrades-trampa]] ·
[[defensa-cableada-vs-codigo-muerto]]
