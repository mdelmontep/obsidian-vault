---
title: una palanca que apaga al worker debe apagar también lo que anuncia que hay worker
date: 2026-09-22
source: agh-iberica
tags: [feature-flag, workers, api, testing]
---
**Patrón:** un worker nuevo se protege con una palanca por tenant (`claimOne` la exige), pero lo que anuncia su existencia —`hasWorker`, «reintentar», la fuente de la propuesta— se deriva de un registro ESTÁTICO de reclamos. Con la palanca apagada, la API dice «hay quien lo procese» y el reintento reencola algo que nadie coge: el documento se queda parado para siempre, en silencio.

**Cómo salió (#1702, PR #2023):** no lo cazó ningún test nuevo. Lo cazaron tres tests VIEJOS que usaban «contrato en visión» como ejemplo de «sin reclamante» y se pusieron en rojo al ampliar el reclamo. La tentación era cambiar el ejemplo del test, y eso habría enterrado el bug.

**Regla:**
- Al poner un flag delante de un consumidor, grep de todo lo que DERIVA «hay consumidor»: UI, reintento, estado. La condición vive en un solo sitio que los alimenta a todos.
- Un write que decide por lo leído (el UPDATE del reintento) vuelve a exigir la palanca. Si no, hay carrera.
- Un test viejo que se pone en rojo porque su ejemplo «ya no es verdad» es sospechoso de bug antes que de fixture caducado.

Mismo fallo sin cerrar: `documents_enabled` (#2025).
