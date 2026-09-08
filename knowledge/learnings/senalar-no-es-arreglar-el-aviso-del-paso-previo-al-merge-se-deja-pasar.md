---
title: señalar no es arreglar: el aviso del paso previo al merge se deja pasar
date: 2026-09-08
source: facturaia
tags: [harness, guards, metodo, migraciones]
---
`mig:renumerar` **sí** listaba las cabeceras «NÚMERO PROVISIONAL» sin traducir, y
aun así trece migraciones llegaron a `main` con ella puesta, una anunciando un
número que ya no era el suyo.
**El sitio del aviso lo condena**: quien renumera está a un paso del `gh pr
merge` y la lista trae falsos positivos que hay que leer uno a uno. El último
paso antes de mergear es el peor sitio para un aviso.
**Regla**: si la corrección es mecánica y sin ambigüedad, hazla en el mismo
gesto; la lista, solo para lo que exige leer. Aquí la cabecera es formato fijo
(se sella sola) y el cuerpo es prosa (se señala) — sustituir el cuerpo a ciegas
ya reescribió referencias ajenas en dos manuales y un test en agosto.
Corolario: **sellar la cabecera no significa que no quede el número viejo en el
fichero**; puede vivir en una constante que acaba en `audit_log`, sin test.

Ver [[colision-de-numero-de-migracion-hace-que-db-push-la-salte-en-silencio]]
