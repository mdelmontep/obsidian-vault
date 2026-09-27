---
title: mig:renumerar sin el marcador provisional mueve el fichero antes de abortar
date: 2026-09-27
source: facturaia
tags: [migraciones, supabase, facturaia]
---
Si la cabecera de la migración no lleva la línea `-- mig:provisional — …`, `npm run mig:renumerar` hace el `git mv` (999 → 959), regenera el manifiesto y **después** aborta con exit 2 («CABECERA QUE NO DECLARA SU NUMERACIÓN»). El árbol queda a medias.

Si pegas el marcador y lo relanzas tal cual, el script vuelve a partir del nombre `999_`, calcula otro destino (960) y falla con `fatal: bad source` en el `git mv`.

Arreglo, en este orden:
1. `git mv` de vuelta al `999_`.
2. `npm run gen:migraciones-manifiesto`.
3. Añadir el marcador en la primera línea.
4. Volver a correr `mig:renumerar`, que esta vez sella la cabecera con `-- mig:959 — numero definitivo…`.

Un exit 2 con «QUEDAN N APARICIONES DEL NÚMERO VIEJO» es otra cosa. Revisa las N una a una: con un provisional `999` suelen ser importes de los manuales (9.999,99 €), que no se tocan.

Ver [[supabase-migration-numero-colision-renumerar]].
