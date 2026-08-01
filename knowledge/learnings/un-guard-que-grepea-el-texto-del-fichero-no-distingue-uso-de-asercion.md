---
title: un guard que grepea el texto del fichero no distingue el uso prohibido de la aserción que lo vigila
date: 2026-08-01
source: claude-code-session
tags: [hooks, ci, sql, gates]
---
Un hook/lint que busca un patrón **en el texto** del fichero bloquea también al código que comprueba
que ese patrón NO está. Al escribir la asserción, formúlala **en positivo**.

Caso TuFacturaIA: el `pre-push` aborta si una migración usa
`IF NOT public.user_can_write_in_org(` sin condicionar a `auth.uid()`. La migración 620 llevaba una
verificación que buscaba justo esa cadena en `pg_get_functiondef` para asegurar que el guard duro no
había vuelto → el hook la leyó como el uso prohibido y abortó el push que traía la comprobación.

- Fix: comprobar la forma **buena** (`v_def NOT LIKE '%auth.uid() IS NOT NULL AND NOT public.user_can_write_in_org(%'`)
  en vez de la mala. Además es mejor asserción: verifica lo que debe existir, no lo que no debe.
- Regla general: si tu test/asserción tiene que nombrar el string prohibido, o lo partes, o inviertes
  la comprobación. El hook no puede saber que estás de su lado.
