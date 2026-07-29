---
title: microsoft graph devuelve la hora del evento como pared sin offset, no como instante
date: 2026-07-29
source: claude-code-session
tags: [m365, microsoft-graph, calendario, timezone, testing]
---
`event.start.dateTime` de Graph es **hora de pared sin offset ni `Z`** (`"2026-07-06T09:00:00.0000000"`), renderizada en la zona que pidió el header `Prefer: outlook.timezone`. **No es un instante.**

Pasarlo por `Date.parse` lo interpreta en la zona del **PROCESO**:
- portátil de dev (Europe/Madrid) → 07:00Z ✔ casa por accidente;
- contenedor Docker (UTC por defecto, y casi nadie declara `TZ`) → 09:00Z ✘ nunca casa.

Resultado típico: un guard que compara `Date.parse(evento.start)` con un instante UTC **funciona en local y es un no-op silencioso en producción** — o peor, casa con el evento equivocado y bloquea algo legítimo (con offset +2, un evento de las 09:00 «es» las 11:00).

Fix: convertir la pared a instante con la MISMA zona con la que se pidió (`localWallClockToUtc(wall, timeZone)`), o comparar pared contra pared. Nunca aritmética temporal directa sobre ese campo.

Señal para detectarlo en revisión: si un fake de test emite `...Z` para un campo que la API real entrega sin offset, el test es verde permanente sobre una propiedad que no se comprueba → [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]. Y comprueba la TZ del contenedor, no la tuya: `docker exec <c> node -e "console.log(Intl.DateTimeFormat().resolvedOptions().timeZone)"`.

Caso real: agh-iberica #585 (dedup de reunión agendada), cazado por revisión adversarial ANTES de mergear; el gate estaba verde.
