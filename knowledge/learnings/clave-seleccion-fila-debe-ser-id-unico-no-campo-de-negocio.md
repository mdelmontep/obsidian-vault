---
title: la clave de selección/expansión de fila debe ser el id único, no un campo de negocio
date: 2026-07-14
source: FacturaIA — bug aprobación masiva recibidas (#888)
tags: [frontend, react, seleccion, facturaia]
---
`docKey = num ?? id` para las filas de facturas. En RECIBIDAS los números se
repiten (mismo `num` de proveedores distintos, escaneos con nombre duplicado) →
la clave NO era única. Efectos, todos silenciosos:
- el `Set` de `selected` colapsaba duplicados;
- las acciones en lote resolvían la fila con `data.find(f => docKey(f)===key)`,
  que devuelve **solo la primera** con ese número → el resto no se procesaba
  (síntoma real: "aprobar seleccionadas" dejaba facturas sin aprobar);
- `toggleAll` (`selected.size === data.length`) nunca se cumplía → no limpiaba.

Regla: la clave de un `Set`/`Map` de selección o expansión de filas = el `id`
garantizado único de la fila, **nunca** un campo que el dominio permita duplicar
(número de factura recibida, SKU, email…). Fallback `?? id` no basta si el campo
principal puede repetirse. Toggle "seleccionar todo": `size>0 ? limpiar : todo`.
