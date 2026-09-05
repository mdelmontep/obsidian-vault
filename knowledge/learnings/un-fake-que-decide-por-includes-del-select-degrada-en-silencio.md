---
title: un fake que decide por `includes` de una subcadena del select degrada en silencio
date: 2026-09-05
source: facturaia
tags: [tests, fakes, postgrest, supabase]
---
Un fake de cliente Supabase que mira `cols.includes('tabla(')` para decidir si anida la hija **no
falla cuando el select cambia de forma legítima: cambia de camino**. Al cualificar el embed con
`tabla!fk(` la subcadena deja de casar, el fake sirve las filas SIN anidar y el código bajo prueba
se va por su fallback — el test sigue corriendo, midiendo otra cosa.

Caso real (FacturaIA, 5-sep-2026): 13 tests fiscales se pusieron rojos al añadir el hint; el 303 se
calculaba por el fallback de cabecera en vez de por líneas. Salió a la luz **por suerte**, porque
las aserciones eran cifras duras; con un assert flojo se habrían mergeado 13 tests que ya no
comprueban nada.

Fix: que el fake emule la regla de verdad, no una subcadena —
`/\btabla(?:![A-Za-z_]\w*)*\s*\(/`, porque el hint elige la clave pero **no renombra la colección**
en la respuesta. Y al tocar la forma de un select, `grep` de `includes('<tabla>` en los fakes antes
de dar el verde por bueno. Relacionado: [[una-fk-nueva-hacia-una-tabla-ya-referenciada-rompe-los-embeds-de-postgrest]].
