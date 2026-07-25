---
title: sin credenciales E2E, verifica un refactor de copy grepeando los fragmentos borrados contra los tests
date: 2026-07-25
source: claude-code-session
tags: [testing, e2e, copy, refactor, verificacion]
---

Un refactor de texto visible (de-slop, i18n, renombrar labels) rompe tests que localizan
por texto: `getByText`, `getByRole({name})`, `hasText`. El smoke E2E es el gate natural,
pero suele necesitar `.env.test` con credenciales de la org sandbox — y correrlo a ciegas
contra prod para "cerrar el checklist" es peor que no correrlo.

Sustituto **determinista y sin credenciales**: extraer del propio diff los fragmentos de
texto que DESAPARECEN y buscarlos en la suite entera.

```
git diff <base> HEAD -U0 | grep '^-'   → regex sobre los trozos con el patrón cambiado
                                       → buscar cada fragmento en tests/e2e/** + *.test.*
```

0 coincidencias = ningún selector apunta a un texto que ya no existe → el refactor no puede
romper la localización. N coincidencias = lista exacta de tests a actualizar, sin adivinar.

Barato, reproducible y contestable en el PR. No sustituye al smoke para regresiones
funcionales, sí para "¿he roto un selector?". Complementa
[[e2e-smoke-skip-honesto]] · nace de [[copy-espanol-raya-tell-ia-dominante]].
