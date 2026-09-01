---
title: un canal de avisos deduplicado no mide la frecuencia del fallo
date: 2026-09-01
source: agency-portal
tags: [alertas, slack, diagnostico, cron]
---
Los avisos del cron llegaban a Slack solo a las **:45** y a las **:00**, así que deduje que el schedule
corría cada 45 min. Falso: corría **cada 15 min**, como estaba documentado. El notificador dedupe por
**firma del fallo** y se tragaba los ticks idénticos.

Conté avisos y creí estar contando corridas. Lo que de verdad medía la cadencia estaba en la BD
(`fleet_judge_runs` sin filas, `received_at` de los logs), no en el chat.

Regla: un canal con dedup, agrupación o rate limit es una **notificación**, no un instrumento. Para
frecuencia, ir a la tabla que registra cada corrida; si no existe, ese es el bug de fondo — aquí las
tandas fantasma no dejaban fila, que es justo por lo que el fallo llevaba días invisible.

Corolario: al diagnosticar por captura de pantalla de un chat, decir en voz alta «esto son avisos
dedupeados» antes de inferir nada del intervalo entre ellos.
