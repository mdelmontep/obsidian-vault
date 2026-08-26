---
title: una línea roja que un toggle de informes puede levantar no es una línea roja
date: 2026-08-26
source: facturaia
tags: [arquitectura, invariantes, feature-flags, agentico, seguridad]
---
El PRD decía «transferencia interna: jamás verde» (línea roja DURA), pero su
cumplimiento dependía de `ia_detectar_transferencias_internas`, un toggle cuya
promesa al usuario es de **informes** («que no inflen tus ingresos/gastos»).
Apagado, el traspaso entre cuentas propias se registraba en verde y, con la org
en activo, se auto-categorizaba en silencio como ingreso o gasto: nadie había
levantado el candado, solo apagado una preferencia.

Y el arreglo obvio era otro fallo: forzar la detección habría escrito
`es_transferencia_interna` y emitido evento, justo lo desactivado. Son DOS
decisiones — `detectar` (la evidencia del candado) y `marcar` (la preferencia).

Regla: por cada invariante duro, preguntar de qué flag depende su DETECCIÓN; si
ese flag lo ve el usuario y promete otra cosa, separar evidencia de acción. En
observación tampoco es benigno: esas verdes falsas son el denominador del gate,
así que abren la autonomía con datos que no debían contar. Ver
[[un-gate-cuyo-denominador-es-la-zona-que-sus-candados-vetan-nunca-abre]].
