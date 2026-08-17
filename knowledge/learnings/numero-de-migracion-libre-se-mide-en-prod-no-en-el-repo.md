---
title: El número de migración libre se mide en PRODUCCIÓN, no en el repo
date: 2026-08-12
source: claude-code-session
tags: [supabase, migraciones, facturaia, gotcha]
---

`supabase db push` decide por **versión**, no por contenido: si el número ya está en
`supabase_migrations.schema_migrations`, da la migración por hecha, **se la salta sin error** y el
push dice que todo está al día mientras prod se queda sin el cambio.

El repo no basta para saber qué número está libre. En una tarde, dos veces:

- Elegí **672** mirando `origin/main` (máximo 669). Prod ya tenía **670 y 671**, aplicadas por una
  rama de contenido **antes de mergear**.
- Elegí **673** mirando `origin/main` (máximo 672, ya con mi 672 dentro). Prod ya tenía **673**
  (`marketing_cola_aprobacion`), otra vez de una rama sin mergear.

La comprobación que las cazó las dos veces es la misma, y cuesta un segundo:

```sql
select version, name from supabase_migrations.schema_migrations order by version desc limit 4;
```

`npm run mig:renumerar` avisa, pero **no decide**: propone mover tu número porque ve el de prod
ocupado, y ese número puede ser **tuyo** (si aplicaste antes del merge para generar tipos). Hay que
comprobar por catálogo de quién es antes de moverlo — la columna `name` lo dice.

Y sus «apariciones sin traducir» incluyen falsos positivos: el SVG del grafo de dependencias tiene
coordenadas que contienen el número (`673` dentro de un `<path d="…">`). Traducirlas corrompería el
fichero. Por eso el script **lista** en vez de sustituir.

**Dentro de un worktree las dos herramientas FALLAN ABIERTAS** (17-ago): `mig:renumerar` avisa «no se
pudo leer el remoto, el número sale SOLO del repo» y el `pre-push` avisa «no se puede comprobar si ya
está aplicado en producción» — a los dos les falta `opsa`/`psql`/`supabase/.temp/pooler-url`, que no
se hereda del repo raíz. Avisan y siguen. Dos silencios seguidos se leen como confirmación: la única
comprobación válida sigue siendo la consulta de arriba.

Ver [[aplicar-migracion-antes-del-merge-deja-el-registro-mintiendo]].
