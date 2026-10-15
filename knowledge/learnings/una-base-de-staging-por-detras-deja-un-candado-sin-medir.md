---
title: una base de staging por detrás deja un candado sin medir, y el rojo parece del código
date: 2026-09-08
updated: 2026-10-15
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

Cómo se mide: `supabase migration list --db-url "$STAGING_DB_URL"` devuelve en JSON
`local`/`remote` por versión, y las que tienen `remote` vacío son las que faltan.
8-sep: 109 sin aplicar. 15-oct: faltaban de la 1055 a la 1063, y `visual-app` daba
`db_error` («column … pdf_portal_no_derivable_at does not exist»). Nadie aplica a
staging al mergear: se queda atrás cada semana.

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]] ·
[[un-e2e-rojo-por-timeout-de-navegacion-mide-el-servidor-de-desarrollo]].
