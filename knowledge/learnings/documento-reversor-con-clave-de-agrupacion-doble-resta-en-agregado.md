---
title: un documento reversor que hereda la clave de agrupación del origen anulado se resta dos veces en el agregado
date: 2026-07-18
source: claude-code-session
tags: [facturaia, facturacion, agregados, gotcha, contabilidad]
---

Al anular una factura se emite un ABONO (negativo). Si por trazabilidad el abono
hereda la misma clave de agrupación que su origen (caso obras: `obra_id`) para
aparecer en el listado de esa entidad, cuidado con los agregados por esa clave.

Gotcha: el agregado "facturado real" ya EXCLUYE la factura origen (está
`anulada`), así que el par origen+abono se anula solo con excluir el origen. Si
ADEMÁS sumas el abono (base negativa), lo restas DOS VECES → total negativo o
descuadre → disparas un falso banner "revisar".

Fix: el reversor entra en el LISTADO (para auditoría) pero NO en el sumatorio:
`filter(estado != 'anulada' && tipo_documento != 'abono')`. La regla general:
cuando un documento reversor lleva la clave de agrupación de su origen solo para
mostrarse, cualquier agregado que ya filtre el origen cancelado debe filtrar
también el reversor. Ver [[consumir-tope-y-emitir-documento-reservar-emitir-confirmar]]
y [[update-post-insert-que-lanza-sobre-documento-fiscal-numerado-causa-reemision]].
