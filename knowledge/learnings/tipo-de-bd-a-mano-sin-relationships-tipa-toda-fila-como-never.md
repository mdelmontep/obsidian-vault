---
title: un tipo Database escrito a mano sin Relationships tipa TODA fila como never
date: 2026-08-30
source: agency-portal
tags: [supabase, typescript, tipos]
---

`supabase-js` parsea la cadena del `select()` con tipos condicionales que necesitan la
clave **`Relationships`** de cada tabla. Si el `Database` está escrito a mano y no la
lleva, el parser no resuelve y **toda fila cae a `never`**: `data` tipa `null` y cada
acceso a una propiedad da `TS2339`.

El engaño es el mensaje. `Property 'agency_id' does not exist on type 'never'` se lee
como «falta esa columna en el select», así que se pierde el tiempo tocando la cadena.
No es eso: pasa igual con `select('*')` y en **cualquier** tabla del proyecto. Comprobarlo
con una sonda de dos líneas sobre una tabla distinta antes de tocar nada.

Fix en un repo donde `database.types.ts` es a mano y no se regenera (aquí es regla dura):
interfaz local con las columnas que pides + `data as MiFila | null`. Es el patrón que ya
usaba `src/lib/facturaia/unlink-cancelled.ts`; buscar un precedente en el repo antes de
inventar otro.

Ver [[Stack/supabase-cloud]] · [[un-catalogo-de-capacidad-de-un-tercero-escrito-a-mano-miente-en-silencio]]
