---
title: realtime se apaga en impersonación → UI con estado optimista se cuelga sin fallback
date: 2026-06-16
source: claude-code-session
tags: [supabase, realtime, impersonacion, react, ux, facturaia]
---

La suscripción a Supabase realtime suele desactivarse en impersonación (el cliente
anon solo recibe cambios de filas que su RLS permite; la sesión impersonada opera
cross-org vía service-role). Si la UI tiene estado optimista —p.ej. una barra de
progreso simulada que tope al 90% esperando el evento UPDATE que cambia el item a
'listo'— se queda clavada indefinidamente. Solo se desbloquea al recargar (el
fetch inicial lee BD). Síntoma: "se queda pensando y no responde" (caso Abba).

Fix: polling de seguridad mientras haya items "en proceso" → re-`fetch` de BD cada
pocos segundos, para en cuanto no queda nada en proceso. Cubre también eventos
perdidos por reconexión del canal o filas fuera del filtro RLS en el instante del
cambio. Patrón general: todo optimismo que depende de un evento que PUEDE no llegar
necesita fallback/timeout.

Gotcha React 19: el re-fetch no debe hacer `setState` en el cuerpo del effect
(regla `set-state-in-effect`) → query pura que devuelve filas + `setState` en `.then`.
