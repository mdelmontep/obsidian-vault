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

Variante sin PATCH y con la pérdida DENTRO de una RPC (2026-08-19, TuFacturaIA, #1933): la columna la
pisa un `UPDATE ... SET col = p_param` de una función `SECURITY DEFINER`, y el parcial lo manda la UI.
`fiscal_marcar_presentada` reescribe `sello_tiempo_eidas` con lo que le pase el modal, y el modal manda
`{serial, source}` (o `{}` si no selló él): se va el `tsr_b64`, el único dato con el que se puede
verificar el sello RFC 3161 del fichero ya subido a WORM. Con `fichero_aeat_path` igual, sustituido por
una ruta inventada `manual-<uuid>`. Tres nombres para el mismo campo en tres ficheros
(`serial_number` quien lo produce, `serial` quien lo manda, `tsr_id ?? id` quien lo lee) y ninguno
coincide, así que el dato no se leía nunca y nadie lo echó de menos.
Regla: si un parámetro de RPC alimenta una columna que otro flujo ya rellenó, **`COALESCE` o merge
condicionado** (`WHEN p ? 'clave_dura' THEN p ELSE col END`), nunca asignación directa. Y una columna
con un shape tipado (aquí `SelloEidas`) no acepta un objeto de dos claves montado en el cliente.
