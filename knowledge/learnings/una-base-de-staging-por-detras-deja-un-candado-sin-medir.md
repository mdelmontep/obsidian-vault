---
title: una base de staging por detrás deja un candado sin medir, y el rojo parece del código
date: 2026-09-08
source: facturaia
tags: [staging, migraciones, e2e, seguridad]
---
Si la base contra la que corren los E2E va por detrás del código, los endpoints
piden funciones y tablas que ahí no existen. En pantalla eso sale como **«no se
pudo cargar, comprueba tu conexión»**: parece red, parece bug, y es esquema.

Lo caro no es el rojo ruidoso: es el **trinquete de cobertura que deja de
morder**. En facturaia (8-sep) la frontera cross-org medía 29 endpoints con
403/404 sobre un suelo declarado de 59, con 101 sin medir. Ese eje no estaba
verde ni rojo: estaba **sin medir**, y nada lo decía en alto.

Cómo se mide el desfase sin acceso a `schema_migrations`: saca de cada migración
la tabla que crea (`grep -oiE "create table ..."`) y biseca por PostgREST con la
service role — 200 = aplicada, 404 = no. Staging cortaba entre la 754 y la 764,
con el repo en la 880: **109 migraciones sin aplicar**, no las 10 del issue.

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]] ·
[[un-e2e-rojo-por-timeout-de-navegacion-mide-el-servidor-de-desarrollo]].
