---
title: isoDate con toISOString().slice(0,10) desplaza un día en husos UTC+
date: 2026-07-23
source: claude-code-session
tags: [javascript, timezone, dates, facturaia]
---
`d.toISOString().slice(0,10)` sobre un `Date` que representa medianoche LOCAL de un día calendario convierte a UTC antes de leer los componentes. En cualquier huso de offset positivo (España en verano, UTC+2), la medianoche local del día 1 es "el día anterior a las 22:00 UTC" → el string devuelto es el día ANTERIOR al que representaba el `Date`.

**Caso real (FacturaIA, PR #1185)**: `isoDate()` usado para enviar `p_q_start`/`p_q_end` a una RPC de KPIs. El INICIO del rango se ensanchaba (colaba un día del periodo anterior, inofensivo) pero el FIN recortaba el último día real del periodo (ej. el 30/09 de un 3T quedaba fuera del "Cobrado del trimestre") — bug silencioso, ya en producción durante horas antes de detectarse.

**Detección**: comparar el valor mostrado en pantalla contra una consulta SQL directa con las mismas fechas — divergían. Confirmado con logging de red del payload real enviado a la RPC.

**Fix**: leer componentes LOCALES del `Date` (`getFullYear/getMonth/getDate`), nunca `toISOString()`, para serializar una fecha-calendario (no un instante).

**Test de regresión**: forzar `process.env.TZ = 'Europe/Madrid'` explícitamente — un CI en UTC no detecta esta clase de bug (el patrón buggy da el mismo resultado que el correcto en offset 0).

**Alcance más amplio**: el mismo patrón (`Date` local + `.toISOString()`) apareció en un grep de ~20 archivos más del repo, mayoría server-side (Dokploy corre en UTC → no manifiesta ahí). No auditado — candidato a barrido dedicado si se prioriza.
