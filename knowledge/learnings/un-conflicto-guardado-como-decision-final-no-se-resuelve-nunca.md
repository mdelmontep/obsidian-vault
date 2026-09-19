---
title: un conflicto guardado como decisión final no se resuelve nunca
date: 2026-09-19
source: agh-iberica
tags: [hitl, diseño, postgres, revision]
---
En un flujo HITL de «aprobar campo a campo» (#1701, PR #1878), el primer diseño guardaba el CONFLICTO como una decisión más: con UNIQUE por campo no se podía volver a decidir, y el documento pasaba a `applied` con conflictos pendientes. El gate estaba verde; lo cazó una revisión contra la spec.
Tres huecos del mismo patrón:
- Sin **vista previa** pura, la revisora solo ve el conflicto después de gastar el clic.
- Un campo que depende de otro (el salario de su fecha, el NIF del nombre) quedaba congelado según el ORDEN de los clics.
- El hash de versión cubría las propuestas y no las decisiones: dos revisoras sobre vistas viejas no se detectaban si tocaban campos distintos.
Patrón:
- vista previa sin escritura;
- conflicto = estado pendiente, resuelto con `keep_current`/`overwrite` (y `overwrite` prohibido tras una edición manual posterior);
- una dependencia sin resolver es un error de validación que no escribe nada;
- el hash de versión cubre propuestas Y decisiones.
Relacionado: [[aceptar-sugerencia-hitl-debe-cerrar-decision-o-el-gate-no-abre]]
