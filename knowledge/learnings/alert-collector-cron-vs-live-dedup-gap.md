---
title: cron materializador + collector en vivo necesitan dedup en runtime, no filtro de origen
date: 2026-06-23
source: claude-code-session
tags: [facturaia, admin, alerts, cron, health-sweep]
---
Cuando un cron escribe alertas en BD (`source='health-sweep'`) y un collector en
vivo emite el mismo tipo de alerta, filtrar el origen del cron (`.neq('source','health-sweep')`)
evita duplicados pero crea un gap: si el servicio se recupera entre ticks del cron,
la entrada BD queda sin resolver y el panel queda vacío aunque el banner siga encendido.

Fix/patrón:
1. Exponer todas las entradas sin resolver (sin filtro de origen).
2. Dedup en runtime: si un collector en vivo ya emite `type === kind` de la entrada BD, omitir la entrada BD.
3. Si el servicio ya está sano, el collector en vivo no emite → la entrada BD aparece con botón "Resolver".

Gotcha: el banner (lee BD directamente) y el tab Alertas (corre collectors en vivo) son 2 paths distintos.
Un filtro en uno no afecta al otro → inconsistencia visible para el usuario.
Caso: TuFacturaIA PR #451, `systemAlertsCollector` + `runSystemCollectors`.
