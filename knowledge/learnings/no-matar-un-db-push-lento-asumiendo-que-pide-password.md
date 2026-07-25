---
title: un `supabase db push` sin output no está colgado, está aplicando
date: 2026-07-25
source: claude-code-session
tags: [supabase, claude-code, operacion]
---

`supabase db push --linked` con varias migraciones tarda minutos **sin escribir nada** por stdout hasta terminar. Al no ver output asumí que esperaba la contraseña de la BD (el flag `--password` existe, lo que reforzó la hipótesis) y lo maté con `pkill`. Había aplicado 5 de 9 migraciones.

No hubo daño porque cada migración es una transacción con su bloque `DO` auto-verificante, pero la conclusión era falsa y la evidencia estaba a un comando: `supabase migration list --linked` dice qué se aplicó de verdad.

- Antes de matar un proceso de deploy, **comprobar el efecto** (¿qué versiones constan aplicadas?), no interpretar el silencio.
- Diseñar las migraciones para sobrevivir a esto: una transacción por migración + bloque `DO` que aborte si el resultado no es el esperado. Es lo que convirtió un `pkill` a media faena en un no-evento.

Ver [[migracion-aplicada-fuera-de-historial-supabase]].
