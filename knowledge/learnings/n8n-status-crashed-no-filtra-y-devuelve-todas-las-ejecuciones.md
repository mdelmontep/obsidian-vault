---
title: n8n `?status=crashed` no filtra y devuelve todas las ejecuciones
date: 2026-08-03
source: claude-code-session
tags: [n8n, api, observabilidad]
---
`GET /api/v1/executions?status=crashed` **ignora el filtro**: devuelve el listado completo,
incluidas las que están en `success`. Verificado contra Clínica Zen — la ejecución `10049` salía
en ese listado y su `status` real era `success`.

Solo `status=error` filtra de verdad. Un valor inventado (`status=chorizo`) sí devuelve vacío,
así que el parámetro se valida a medias y `crashed` cae en el hueco.

**Consecuencia:** un monitor que se fíe reporta el 100% de las ejecuciones como caídas. En el
primer run del check de efecto salieron ~200 rojos falsos en dos clientes.

**Fix:** usar `status=error` y **revalidar el campo `status` de cada item en cliente**
(parse-don't-trust). Un filtro que miente en silencio es peor que no filtrar.
