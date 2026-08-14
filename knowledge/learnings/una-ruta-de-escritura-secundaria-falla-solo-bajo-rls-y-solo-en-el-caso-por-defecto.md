---
title: la ruta de escritura secundaria omite el contexto que la principal sí pasa, y sólo falla bajo RLS
date: 2026-08-14
source: claude-code-session
tags: [supabase, rls, postgres, importacion, testing]
---

La importación de CSV no escribía **ni una ficha** en producción: llamaba a `crearContacto()` sin
`ownerId`, y la política de insert exige `owner_id = auth.uid()` salvo que la visibilidad del actor
sea `org`/`team`. La acción de la pantalla sí lo pasaba, así que **crear a mano funcionaba y sólo la
importación fallaba** — invisible mirando el producto por encima.

Tres cosas que lo hacen un patrón y no una anécdota:

- **Sólo falla en el caso POR DEFECTO.** La visibilidad nace en `own`, así que rompe justo para toda
  organización recién creada. Probarlo con un admin de visibilidad `org` da verde.
- **Ningún test lo ve**: el doble de Supabase acepta el insert que se le ponga. La política sólo la
  evalúa Postgres.
- **Falla en silencio y encima felicita**: el `42501` se traducía a un mensaje genérico y el
  resultado salía en caja de éxito diciendo «0 altas».

Regla: al añadir una segunda vía de escritura (importar, API, job, seed), **diff de los argumentos
contra la vía principal** — lo que falta suele ser el contexto de actor que la RLS exige. Y una
aserción contra Postgres real por cada vía, no sólo por la principal.
