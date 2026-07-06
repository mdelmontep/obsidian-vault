---
title: para que un llm resuelva «mañana/el martes» pásale el now en zona local con el día de la semana, nunca el iso utc crudo
date: 2026-07-06
source: claude-code-session
tags: [llm, fechas, timezone, agentes]
---
Si dejas que el LLM resuelva fechas relativas («mañana», «el martes», «el lunes que viene») a una fecha concreta, lo que le pases como "ahora" decide el resultado. Pasarle `message.timestamp` en ISO UTC crudo (`...Z`) es un bug latente: cerca de medianoche el **día en UTC ≠ el día en la zona del usuario** (Madrid UTC+1/+2), así que el modelo elige el día equivocado (23:30Z del lunes ya es martes en Madrid → «mañana» se va un día).

Fix: formatea el now a la **zona local con el día de la semana explícito** antes de meterlo en el prompt: `Intl.DateTimeFormat("es-ES", { timeZone: "Europe/Madrid", weekday:"long", day, month, year, hour, minute })` → «martes, 7 de julio de 2026, 01:30». El formateo de SALIDA (recap/confirmación) suele estar bien en TZ local, pero repite fielmente la fecha ya mal elegida en la entrada → el bug se ve en el resultado pero nace en el "now".

Test que lo caza: `now` en el borde de medianoche (día UTC ≠ día local). La cobertura típica usa timestamps a media mañana (10:00Z, donde ambos días coinciden) y nunca ejercita el borde. Caso real: AGH #215.
