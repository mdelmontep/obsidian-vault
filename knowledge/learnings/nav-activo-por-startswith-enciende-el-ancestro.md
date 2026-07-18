---
title: nav activo por startsWith enciende el ancestro además de la hoja
date: 2026-07-18
source: claude-code-session
tags: [react, nav, ux]
---
Marcar un ítem de menú activo con `pathname.startsWith(item.path)` enciende DOS
ítems cuando el path de uno es prefijo de otro. Caso real (sidebar Obras): la
hoja "Obras" (`/obras`) y "Materiales" (`/obras/materiales`) salían ambas activas
en `/obras/materiales`, porque `/obras` es prefijo de todo `/obras/*`.

Fix: activo = el prefijo navegable MÁS específico que matchea la ruta actual.
1. descartar si no es la ruta ni un ancestro (`pathname===p || pathname.startsWith(p+'/')`; el `/` evita que `/obras` matchee `/obras-xyz`).
2. de entre TODAS las rutas de nav, elegir la de mayor longitud que matchea; el ítem está activo solo si es esa.
El grupo/padre se resalta aparte (`some(hijo activo)`), no por su propio path.
Aplica a cualquier menú anidado. Ver [[facturaia]] · relacionado [[server-component-no-puede-llamar-funcion-use-client]].
