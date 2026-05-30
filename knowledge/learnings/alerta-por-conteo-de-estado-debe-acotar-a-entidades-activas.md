---
title: alerta por conteo de filas en estado no-terminal debe acotar a entidades activas
date: 2026-05-30
source: claude-code-session
tags: [monitoring, alertas, sql, patron]
---

Una alerta de salud que cuenta filas en un estado no-terminal (`pendiente`, `stuck`, `en cola`) debe **acotar a las entidades que de verdad deberían progresar**. Si no, las filas inertes de entidades inactivas se acumulan en ese estado para siempre → falso positivo permanente.

Caso (TuFacturaIA): collector contaba `facturas WHERE verifactu_estado='pendiente_envio' AND created_at < now()-2h` como incidencia alta. Pero las facturas de orgs con Veri*Factu **desactivado** nunca se cursan a la AEAT → viven en `pendiente_envio` eternamente. 4 facturas reales → burbuja roja en falso. Fix: `.in('org_id', orgsConVerifactuActivo)`.

Regla: antes de alertar por "N filas atascadas", pregúntate qué proceso debería sacarlas de ese estado y si está activo para esa entidad. Aplica a colas n8n, backlogs de cron, reintentos, ingestas pendientes.
