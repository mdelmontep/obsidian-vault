---
title: un insert masivo de supabase-js rellena con null las claves que una fila no trae
date: 2026-10-13
source: facturaia (#3457, seed del test de integración de cobros_pending_for_org)
tags: [supabase, postgrest, tests, seed]
---
`admin.from('t').insert([filaA, filaB])` usa como columnas la UNIÓN de las claves de todas las filas. Si una sola fila trae una columna nueva, en las demás va `NULL`, no el `DEFAULT` de la columna: `defaultToNull` vale `true` por defecto y solo afecta a inserts masivos.

Caso real: añadí `registro_externo: true` a una fila del seed; las otras 5 iban con NULL y la columna es NOT NULL. El test se saltaba en local por falta de entorno y solo cayó en la base efímera del gate.

Fix: poner la clave en las filas comunes (`registro_externo: false` en el objeto que se esparce) o pasar `{ defaultToNull: false }` al insert. Con una columna nullable no falla nada: el NULL entra en silencio y el test mide otra cosa.
