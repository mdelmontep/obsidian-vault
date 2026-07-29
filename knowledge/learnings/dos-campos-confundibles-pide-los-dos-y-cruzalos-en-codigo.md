---
title: dos campos confundibles del mismo documento, pide los dos al LLM y crúzalos en código
date: 2026-07-29
source: claude-code-session
tags: [llm, ocr, prompt-engineering, extraccion, facturaia]
---
Factura de mayorista con la cabecera en tabla (`Fecha | Factura | Cliente |
C.I.F. | Ref.Proveedor | Agente | Página`): el modelo devolvía el código de
cliente (`00743`) como nº de factura en vez del número real (`624214649`).

Se "arregló" DOS veces escribiendo la regla en el prompt, con el ejemplo
literal y el `00743` citado dentro. Falló las dos. Una regla del prompt es
una preferencia, no un control: si el pipeline no verifica el campo, no hay
nada que impida la tercera vez.

Técnica que sí lo cierra: cuando dos campos del MISMO documento se pueden
confundir, no elijas cuál pedir — **pide los dos** (`num_factura` y
`num_cliente`) y crúzalos en código. Pedir ambos obliga al modelo a asignar
cada valor a su columna en vez de adivinar una, y la colisión es una señal
determinista de lectura mala. Si coinciden (normalizado: mayúsculas, solo
alfanuméricos, ceros de relleno fuera) → no persistas ninguno y manda a
revisión humana. Si falta cualquiera de los dos, no concluyas nada: cero
falsos positivos.

Generaliza a: base vs importe neto, total vs subtotal, emisor vs receptor.
Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]] y
[[ocr-prompt-campo-sin-regla-anti-invencion-se-alucina]].
