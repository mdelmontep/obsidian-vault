---
title: escribir un campo que no entra en ninguna fórmula dispara igual el recálculo
date: 2026-08-07
source: claude-code-session
tags: [postgres, triggers, supabase, prod, facturaia]
---

Un trigger `AFTER INSERT OR UPDATE ON settings FOR EACH ROW` **sin `WHEN` ni
`UPDATE OF`** cuelga de la FILA, no de la columna. Da igual que el campo que
escribes no aparezca en ninguna fórmula: tocarlo recorre y reescribe todas las
filas dependientes. En TuFacturaIA, poner `coste_hora_mo` (que por diseño no
entra en el precio de venta) recalculaba los **7.683 materiales** de la org.

Antes de escribir un campo "inocuo" en prod, mira qué triggers cuelgan de esa
tabla, no solo si tu columna entra en el cálculo. Y no lo despejes razonando:
**foto antes / foto después**. Aquí salió idéntico byte a byte, pero lo dijo el
`diff`, no el argumento.

Que el recálculo sea no-op depende de que el estado ya esté sincronizado con la
fórmula de HOY. Se comprueba con el `updated_at` de los inputs: si el último es
el de la migración que los dejó cuadrados, reejecutar es inocuo; si alguien tocó
tarifas o descuentos después, ese `UPDATE` de un campo ajeno le publica sus
cambios pendientes al cliente sin que nadie lo haya pedido.

Ver [[un-guard-que-se-apoya-en-una-medicion-externa-no-es-un-guard]] ·
[[alter-column-type-choca-con-cualquier-trigger-update-of]]
