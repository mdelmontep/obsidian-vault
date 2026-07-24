---
title: una columna jsonb con varios escritores convierte cualquier PATCH parcial en borrado
date: 2026-07-25
source: claude-code-session facturaia
tags: [supabase, jsonb, seguridad-datos, arquitectura]
---

Mismo mecanismo que [[put-objeto-completo-borra-campos-no-mapeados]] pero **dentro de tu propio
sistema**: si una columna `jsonb` la escriben N sitios y uno hace `upsert({config: loQueYoConozco})`,
borra las claves de los demás. No hay API externa ni verbo ambiguo que culpar.

Caso real TuFacturaIA: `org_module_config.config` tiene **13 escritores**. `PATCH /api/modules/[id]`
reemplazaba el objeto entero → guardar la config de Previsión de tesorería borraba
`saldo_manual_valor` (el saldo bancario inicial del cliente, misma fila `feature_id='cashflow_ia'`) y
la previsión se recalculaba desde 0 €. Un toggle en otra pantalla, con un tipo cerrado de 3 claves
sobre un módulo de 9, borraba los 6 restantes.

**Antes de escribir un subconjunto a una columna jsonb: inventariar sus escritores y lectores**
(`grep` del nombre de la columna, no del endpoint). Si hay más de uno:
1. Merge por clave en el servidor con allowlist de las que ese endpoint posee.
2. Borrado solo explícito (`unset: string[]`), nunca por omisión.
3. Claves de otros subsistemas → rechazar con 422 nombrando el endpoint dueño; si no, ese PATCH es
   un bypass del que sí tiene audit y versionado.
4. El merge tiene que ser por clave **también dentro de la allowlist**: un cliente que conoce 3 de 9
   claves del mismo schema no puede borrar las otras 6.

Trampa extra: un trigger sobre `UPDATE OF config` puede convertir el borrado en pérdida de trabajo
del usuario (aquí borraba todas las sugerencias `pending` al "cambiar" dos claves a su default).
