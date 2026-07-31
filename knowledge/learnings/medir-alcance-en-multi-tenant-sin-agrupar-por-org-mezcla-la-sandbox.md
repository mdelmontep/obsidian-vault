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

**Reincidencia 2026-07-31, y con la regla ya escrita aquí.** Un subagente midió el daño de
`qa-023` y devolvió "92 facturas recibidas atribuidas a otra empresa". Lo publiqué en el informe,
en el incidente, en un learning y en el hub sin repetir la consulta. Al agruparla por `org_id`:
**84 eran de la sandbox y 8 de clientes**, y de esas 8 solo **2** eran atribución a otra empresa.
Inflado 11 veces.

Dos cosas que aprender de la reincidencia:
- **La regla escrita no se aplica sola a lo que devuelve un subagente.** Una cifra que llega en un
  informe ajeno pesa igual que una que escribes tú, y se audita igual: pídele el `group by` o
  repite la consulta antes de citarla.
- **Un alcance inflado no es "conservador".** Dimensiona mal el trabajo, convierte una reparación
  de dos filas en un proyecto, y cuando alguien lo comprueba se lleva por delante la credibilidad
  del resto del informe.

