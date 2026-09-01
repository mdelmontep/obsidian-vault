---
title: un alcance calculado contra la rama base se vacía al mergear y mide lo que haya suelto
date: 2026-09-01
source: facturaia
tags: [gates, repos-compartidos, harness]
---
Cualquier herramienta que derive «qué he tocado» de `git diff origin/main...HEAD` **más** lo no
commiteado tiene un modo degradado silencioso: si cierras DESPUÉS de mergear, la primera mitad sale
vacía —tu trabajo ya está dentro de la base, así que no aparece— y lo que queda es el árbol sucio,
que puede ser de otra sesión, otro día u otro cliente.

No falla, no avisa, no cambia de salida. Caso real (1-sep, `scripts/cierre-alcance.mjs` de
facturaia): el gate de cierre auditó ocho ficheros de AGH y **apagó la dimensión de datos**, la
única irreversible, con una migración recién aplicada a producción en el diff de verdad. El informe
habría salido en verde igual de convincente.

- El fix no es adivinar qué ficheros son tuyos —no se puede—: es **marcar la degradación**
  (`diff vacío && hay sucio` → aviso) y ofrecer `--desde <ref>` para cerrar sobre tus commits.
- El aviso solo salta cuando el diff está vacío. Si saltara también con «diff + algo sucio» —lo
  normal— sería ruido y se ignoraría.
- Se testea la SEÑAL sobre una función pura, no la lista: el caso no se puede provocar sin fabricar
  un repo.

Prima de [[un-baseline-que-mide-el-arbol-de-trabajo-hornea-el-wip-ajeno]]: allí el árbol contamina
la MEDIDA, aquí sustituye a la ENTRADA.
