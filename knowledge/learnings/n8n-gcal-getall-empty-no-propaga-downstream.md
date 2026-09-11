---
title: n8n Google Calendar getAll vacío no propaga a nodos downstream
date: 2026-05-25
source: claude-code-session
tags: [n8n, google-calendar, gotcha]
---

Si `Google Calendar > Get Many Events` devuelve 0 eventos (franja libre), n8n NO ejecuta nodos downstream — la rama muere silente. Esto rompe pattern habitual "consultar disponibilidad → si vacío respond 'libre'".

Fix con dos cambios:
1. Setear `alwaysOutputData: true` en el nodo GCal → emite item vacío en lugar de 0 items.
2. En el Code node downstream, filtrar el item placeholder:
```js
const events = $input.all().filter(e => e.json && e.json.start);
```
Sin el filter, `e.json.start.dateTime` crashea con TypeError porque `e.json.start` es undefined en el placeholder.

Caso real: EcoBox `Mirar_disponibilidad` 2026-05-25 — el primer fix `alwaysOutputData` solo no era suficiente; necesitaba el filter en `Format slots`.

**Ha vuelto a pasar (11-sep-2026, Laserys Las Rozas).** Encendí `alwaysOutputData` en el getAll
de `recordatorios` sin tocar el Code node de abajo, que llevaba desde el import haciendo
`evento.start.dateTime` sin guarda. Con la agenda vacía —lo normal ahí: 1 cita en 45 días— el
cron reventó **cada 30 minutos durante 12 horas**, 23 ejecuciones y el doble de avisos. El flag
y el filtro son **un solo cambio en dos sitios**: encender uno sin el otro cambia una rama muda
por un crash periódico. Y al revés: si no hay nada que hacer con 0 eventos, el flag sobra.

Corolario (2026-06-01): si `timeMin`/`timeMax` llegan vacíos o null, getAll NO acota → devuelve el calendario ENTERO (eventos de otros días) → falsos "está ocupado". Validar que la ventana llega no-null antes del getAll y filtrar `Format slots` a [After,Before]. Causa de origen: [[n8n-edit-fields-optional-chaining-body-args-plano-vs-wrapped]].
