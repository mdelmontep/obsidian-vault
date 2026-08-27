---
title: la fila de prueba que viola otra restricción finge que la nueva muerde
date: 2026-08-27
source: elphis-psicologia
tags: [postgres, migraciones, verificacion, arnes]
---
Al aplicar un `CHECK` nuevo sobre `service_slug`, el test obvio es
`INSERT INTO t (service_slug) VALUES ('valor-prohibido');` y ver que falla. **Falla
igual sin el CHECK**, por el `NOT NULL` de otra columna. El rechazo se lee como
«la restricción muerde» y no prueba nada.

- La fila de prueba tiene que ser **válida en todo salvo en lo que se prueba**:
  rellenar todas las `NOT NULL` y dejar solo el campo bajo examen mal.
- Hacen falta **dos** inserciones idénticas salvo en ese campo. Si la buena pasa y
  la mala no, discrimina; si pasan las dos, la restricción está puesta y es inerte.
- Van dentro de `BEGIN … ROLLBACK` — y comprobar **después** que el rollback
  deshizo, contando filas. (En n8n, el nodo Postgres sí respeta la transacción
  explícita: medido, no supuesto.)
- Leer el mensaje de error y exigir el **nombre de la restricción** en él separa
  «rechazado por lo que quiero» de «rechazado por otra cosa».

Familia de [[un-smoke-sale-verde-sin-ejercer-el-guard-si-el-dato-no-cumple-su-precondicion]]
y [[verificar-una-migracion-por-columnas-del-constraint-y-en-transaccion]].
