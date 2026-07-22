---
title: cuota por cuenta externa sin forma de detectar cuál está activa → credential separada por cuenta, no columna nueva
date: 2026-07-22
source: claude-code-session
tags: [time-tracking, arquitectura, claude-code, multi-cuenta]
metadata:
  type: learning
---

Si una persona opera bajo N cuentas intercambiables del mismo servicio externo (cada una con su propio cupo/rate-limit) y el proceso que reporta el uso NO tiene forma fiable de saber cuál está activa en cada momento, no añadas una dimensión "cuenta" al esquema esperando poblarla automáticamente — no hay señal que la rellene.

**Caso real 2026-07-22 (agency-portal, `/agency/time`)**: Manu usa 2 cuentas Claude (`info@agentesia.madrid` y personal). El hook local (`claude-time-hook.mjs`) no recibe del propio Claude Code qué cuenta está logueada — solo `session_id`/`cwd`/transcript. `member_rate_limits` tiene PK `(agency_id, member)`: si las dos cuentas reportan como el mismo `member`, una pisa el cupo de la otra.

**Decisión**: en vez de migrar el esquema (columna `account` + PK compuesta) para un dato que igual habría que rellenar a mano, mintar una API key (`tracker-key`) distinta por cuenta y tratarlas como dos `member` diferentes — reutiliza el mecanismo de identidad ya existente (la key resuelve el actor) sin tocar BD ni UI. Desplegado 2026-07-23: `manu` = key nueva (cuenta personal), `info` = key vieja (la que ya usaba) — el histórico previo queda intacto bajo `manu` con la key vieja, y desde el redeploy esa misma key reporta como `info` (separación deliberada, aceptada aun sabiendo que parte el histórico en dos filas de "Por persona"). El coste se traslada a swap manual del fichero de config local (`~/.agentesia-tracker.json`) al cambiar de cuenta — inevitable mientras no exista una señal automática.

**Regla general**: antes de añadir una dimensión a un esquema, confirma que existe una fuente que la puebla sola. Si la única forma de rellenarla es "que el humano la teclee cada vez", casi siempre es más barato modelarla como una identidad separada dentro del mecanismo de auth que ya tienes.
