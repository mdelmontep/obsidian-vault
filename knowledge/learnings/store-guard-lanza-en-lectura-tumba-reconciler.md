---
title: validar un enum lanzando en el mapper de lectura de un store tumba el barrido de arranque
date: 2026-07-02
source: claude-code-session
tags: [postgres, multi-tenant, parse-dont-validate, reliability]
---

Al endurecer un `col as SomeEnum` ciego en el row-mapper de un store, el punto donde validas
importa más que el hecho de validar:

- **Lectura masiva (reconciler de arranque, `listScheduled`)**: si el guard **lanza**, una sola fila
  con valor fuera del enum tumba TODO el barrido → no se re-arma NADA (no solo la corrupta). Si
  **descarta en silencio**, pierdes esa fila (p. ej. un recordatorio `scheduled`) sin traza.
- **Regla**: el fix de origen va en el **borde de ESCRITURA** — un `CHECK` en BD (donde una fila
  ya lo tiene, el cast de lectura es seguro por construcción) o validar en `create()`. En lectura,
  **degrada** (skip+log sin PII en reads cosméticos/admin), nunca lances en un hot-path o un sweep.
- **JSONB de config por-turno** (p. ej. `pending` del HITL): parsea y **degrada a vacío**; lanzar
  deja al usuario encallado (cada turno relee la fila corrupta). Todo-o-nada por fila si es un batch.

Caso AGH #34: `reminders.channel` (TEXT sin CHECK) leído por el reconciler → diferido el CHECK; sí
endurecido `identities.channel` (read admin, degrada). Ver [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]].
