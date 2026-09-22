---
title: un test saltado puede esconder una aserción invertida, no solo cobertura ausente
date: 2026-09-22
source: facturaia
tags: [testing, e2e, metodo, skips]
---
Al hacer ejecutable un test que llevaba saltando, la expectativa por defecto es «ahora
cubrirá lo que no cubría». Falsa: un test que nunca ha corrido **tampoco se ha comprobado a
sí mismo**, así que puede afirmar lo CONTRARIO del contrato y nadie lo ha visto.

Medido (FacturaIA #2870). `proxy-active.spec.ts` caso A llevaba desde su commit inicial en
doble skip (le faltaban un id de org y una sesión de superadmin). Al darle las dos, salió
rojo — y no por el proxy: exigía que la cookie `impersonate_org` se borrara al salir de
`/admin`, que es justo el bug que el middleware documenta **haber arreglado** (si se borra
en el primer hop a `/dashboard`, la impersonación no toma efecto nunca).

- El error venía de la doc: la línea de `gotchas.md` contaba **una de las tres ramas** de la
  lógica («borra sin `?impersonate=`») y omitía que eso solo pasa en páginas `/admin/*`.
  Media verdad en una línea de doc se convierte en un test invertido.
- Corolario al arreglar: no basta con invertir la aserción — pon también la rama que SÍ
  ocurre, o el caso mide media lógica y el `if` queda sin vigilar por el otro lado.
- Al rojo de un test recién despertado, **sospecha primero del test**, no del código: el
  código lleva corriendo en producción y el test no ha corrido nunca.

Relacionado: [[tests-pg-self-skip-levantar-pgvector-local]] (aquello es el skip que oculta
ausencia; esto es el skip que oculta una afirmación falsa) ·
[[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]]
