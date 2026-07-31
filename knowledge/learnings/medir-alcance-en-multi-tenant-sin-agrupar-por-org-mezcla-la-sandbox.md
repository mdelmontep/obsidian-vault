---
title: medir alcance en multi-tenant sin agrupar por org mezcla la sandbox con producción
date: 2026-07-31
source: claude-code-session
tags: [datos, multi-tenant, metodo]
---
Antes de un cambio que altera documentos ya emitidos se mide el alcance. Un
`count(*)` global sobre la tabla **no es esa medida** en una base multi-tenant:
mete en el mismo número las organizaciones de prueba y las reales.

Caso FacturaIA (31-jul): «34 de 8.854 pedidos traen saltos de línea en
observaciones» se reportó como *34 documentos ya enviados a proveedores*, y con
eso se planteó la decisión como delicada. Agrupando por organización, los **34
eran de `Obras tufacturaia sandbox`** — cero de un cliente real. El arreglo valía
igual, pero como prevención, no por daño consumado.

Regla: toda consulta de impacto lleva `join organizations ... group by o.nombre`,
o como mínimo excluye las orgs de prueba, ANTES de convertirse en argumento.
Un agregado suena a dato duro y por eso no se le pregunta de quién es.

Corolario: el mismo cuidado que se pone en que una aserción no esté satisfecha
por contenido ajeno, hay que ponerlo en que un número no esté inflado por filas
ajenas. Ver
[[la-aguja-de-una-asercion-sobre-el-documento-entero-debe-ser-unica-de-la-feature]] ·
[[smoke-test-mode-contamina-bd-prod-si-la-fn-escribe-bd]]
