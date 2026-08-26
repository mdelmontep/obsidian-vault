---
title: automatizar un paso intermedio puede no hacer daño, sino borrar la oportunidad de hacerlo bien
date: 2026-08-26
source: facturaia
tags: [agentic, automatizacion, stock, diseño, riesgo]
---
El veto que impedía auto-aprobar una factura recibida con líneas de stock se justificaba así:
«movería inventario insertando líneas de OCR sin que un humano confirme los mapeos». Medido en
prod, lo que pasa es lo contrario: de 89 bandejas con líneas, **ninguna trae `catalogo_id`** —
ese mapeo lo pone el humano *en la bandeja*. Sin él, las líneas entran como texto libre y el
trigger **no proyecta stock**. Auto-aprobar no movería inventario mal: no lo movería, la compra
no entraría nunca, y la factura saldría de la bandeja, con lo que el mapeo ya no ocurriría.

El riesgo real no era una escritura equivocada, era **la desaparición silenciosa del punto donde
el humano aportaba el único dato que nadie más puede aportar**. Y ese punto se usa: 51 de 52.

Regla: antes de quitar un veto que bloquea la mayoría de los casos, no preguntes «¿qué haría mal
si lo suelto?» sino **«¿qué dato deja de entrar, y quién lo aportaba?»**. Un paso automatizado
que salta una intervención humana enriquecedora produce un resultado *válido y vacío*, que no
falla ni avisa. Y no te fíes del comentario que justifica el veto: aquí afirmaba lo contrario de
lo que el sistema hace. Ver [[dos-castigos-por-el-mismo-evento-hacen-inalcanzable-el-estado-bueno]].
