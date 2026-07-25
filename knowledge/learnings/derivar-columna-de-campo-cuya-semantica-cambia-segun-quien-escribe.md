---
title: antes de derivar una columna de un campo, verifica que TODOS sus escritores le dan el mismo significado
date: 2026-07-25
source: claude-code-session
tags: [postgres, supabase, arquitectura, fiscal, facturaia]
---

Al añadir `importe_cobrable = total − retención` como GENERATED en `facturas`, la
fórmula era correcta para las emitidas y **doble resta** para las recibidas: ahí
`total` se persiste ya NETO de IRPF cuando lo escribe el formulario de edición
(`base * (1 + iva/100 − irpf/100)`) y BRUTO cuando lo escribe el OCR. El mismo
campo, dos significados, según el camino de escritura.

Lo delató un comentario en la UI ("en recibidas `f.total` ya se guarda neto, no
procede restar de nuevo"), no el schema: el tipo es idéntico y no hay CHECK que lo
distinga. Dos auditorías adversariales del diff tampoco lo vieron; salió de leer
quién PINTA el importe.

Regla: antes de derivar, `grep` de todos los escritores del campo base y comprueba
que persisten lo mismo. Si no, acota la derivada (`CASE WHEN tipo = 'x' THEN … END`
→ NULL fuera de su dominio, que significa "no aplica" y no un importe) en vez de
inventar una fórmula que acierte de media. Y verifícalo con datos: aquí una consulta
que usaba el `iva_pct` de cabecera dio un falso positivo porque en esas filas la
cuota real no coincide con ese porcentaje; el contraste bueno fue `total − base`.

Corolario: un campo sin invariante declarado en BD acaba con tantas semánticas como
caminos de escritura. Ver [[campo-huerfano-shape-sin-migracion-paralela]] ·
[[importe-fiscal-no-es-importe-a-cobrar-retenciones]].
