---
title: la frescura del evento solo decide revivir, nunca limpiar el error
date: 2026-08-24
source: agency-portal
tags: [ingesta, cron, maquina-de-estados, auditoria, flota-ia]
---
Un cron de ventana deslizante (48 h cada 15 min) reprocesa cada evento ~100 veces con el **mismo timestamp** (`end_timestamp` de Retell). Si la "salud" de una conexión se gobierna por "evento más nuevo que `last_event_at`", ninguno de esos reprocesos es fresco.

Caso real (24-ago, Flota IA): arreglé un hallazgo de auditoría —un backfill viejo revivía a `connected` una conexión `silent`— condicionando TODO el touch a la frescura. Segunda auditoría: un `error` transitorio se quedaba rojo hasta que llegase una llamada más nueva (un fin de semana entero), porque la limpieza de `last_error` también dependía de la frescura.

Regla: separar los dos ejes.
- **Frescura** (evento > `last_event_at`) decide solo si `silent` → `connected`.
- **Éxito** de la ingesta limpia `error`/`last_error` siempre, fresco o no.
- Implementarlo como función pura (`resolveConnectionTouch`) con test de los cuatro casos: error+reproceso viejo → limpio; silent+viejo → silent; silent+nuevo → connected; disabled → disabled.

Meta: un fix de auditoría es código nuevo sin auditar. Tras aplicar hallazgos, segunda ronda con lentes distintas (esta vez concurrencia) antes de dar por cerrado.
