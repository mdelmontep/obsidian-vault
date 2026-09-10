---
title: un espejo entre dos funciones sql se ancla leyendo el prosrc de la otra
date: 2026-09-10
source: facturaia
tags: [supabase, postgres, espejo, candados, migraciones]
---
`abono_anular` copiaba los seis estados en los que `recompute_factura_estado` se va por la puerta
de atrás sin hacer nada. Un comentario «mantener en sync» al lado de la copia no es un candado.
El ancla es un `DO $verify$` al final de la MISMA migración que lee `pg_proc.prosrc` de la otra
función y revienta si dejó de nombrar cada valor:

- `strpos(p.prosrc, '''' || v_valor || '''') > 0` para cada miembro de la lista, en las dos
  direcciones que se pueden medir.
- Para lo propio, `regexp_split_to_table(prosrc, E'\n')` y descartar las líneas que empiezan por
  `--`, o el guard se conforma con encontrar el término dentro de un comentario.
- **Declara en el comentario la dirección que NO mide.** Aquí: si alguien añade un séptimo estado
  allá y no acá, esto no lo ve, porque haría falta parsear el `IF`. Un candado que promete más de
  lo que mide es peor que ninguno.

Hermano de [[auditar-un-lado-de-par-simetrico-revisar-el-espejo]]: allí el espejo se vigila en
revisión, aquí lo vigila la base cada vez que se aplica.
