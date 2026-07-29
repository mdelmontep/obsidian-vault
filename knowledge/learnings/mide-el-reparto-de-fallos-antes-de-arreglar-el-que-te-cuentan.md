---
title: mide el reparto de fallos antes de arreglar el que te cuentan
date: 2026-07-29
source: claude-code-session
tags: [metodo, observabilidad, agentes, facturaia]
---

Encargo: "un ticket murió por timeout, mejora el prompt". Una consulta a `feedback_ai_jobs` y
`feedback_ai_job_events` (91 jobs, 6 semanas) dio otro cuadro: de 34 fallidos, **11** eran una
cuenta mal configurada, **7** cuota agotada, **6** jobs sanos matados por el watchdog y solo **6**
timeouts. Lo reportado era el 18% del problema, y "prompt con más criterios de calidad" no tocaba
ninguno de los otros.

Corolario incómodo: con esa n (decenas de jobs) **no puedes distinguir prompt v1 de v2**. Reescribir
un prompt "para subir la calidad" es una mejora infalsable; quitarle una contradicción es un bug,
y eso sí se justifica solo.

Segundo hallazgo del mismo tirón: **el camino de fallo menos frecuente suele ser el que nadie
instrumentó**. Aquí el camino de `exit≠0` sí reportaba stdout/stderr y el de timeout no, así que el
modo de fallo del que había que aprender era justo el ciego. Cuando dos caminos terminan el mismo
trabajo, dales la misma telemetría.

Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]] · [[latido-que-solo-cubre-el-tramo-interesante-deja-el-resto-a-merced-del-watchdog]]
