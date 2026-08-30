---
title: una suscripción realtime impide revocar el select de esa tabla a authenticated
date: 2026-08-30
source: agency-portal
tags: [supabase, rls, realtime, seguridad]
---

Endurecer una tabla con `revoke select … from authenticated` y conceder por columna es
la jugada correcta para esconder credenciales… salvo que **algún cliente tenga un canal
Realtime abierto sobre esa tabla**. Realtime exige que el rol del token tenga SELECT para
abrir el canal, y walrus valida además el `filter` contra el catálogo
(`subscription_check_filters`). Sin SELECT, el canal no abre: no da error de permisos en
la consulta, se queda mudo y la pantalla deja de refrescarse.

Consecuencia de diseño: **antes de revocar, grepear las suscripciones del navegador**
(`useRealtimeStream` / `useRealtimeRefresh` / `.channel(`) y las lecturas que usan el
cliente de usuario, no solo las de service-role. Si hay una, el candado por columna no
cabe y hay que elegir: mover el dato sensible a otra tabla, o dejar la revocación
documentada como deuda en vez de romper una pantalla viva.

Caso real: `board_comments` — la revocación pedida por la issue habría apagado la Pizarra
(`card-drawer.tsx` abre canal; `listBoardComments` lee con cliente de usuario). Se entregó
el candado que sí cabía + la documentación, y la issue se dejó abierta con `Refs`, no
`Closes`.

Ver [[Stack/supabase-cloud]]
