---
title: acotar un tipo con Pick destapa, por contravarianza, las firmas demasiado anchas
date: 2026-08-16
source: claude-code-session
tags: [typescript, seguridad, refactor]
---
Al recortar un tipo que se pasa por ahí (`SupabaseClient` → `Pick<…,'from'|'rpc'>`), lo que se rompe
NO son los usos del tipo: son las **firmas receptoras** que pedían el tipo ancho sin necesitarlo. Por
contravarianza, un parámetro declarado ancho obliga a que todo el que llame traiga el juego completo.

Caso medido (TuCRMIA): recortar el cliente rompió 26 puntos, y debajo había 17 firmas de módulos que
sirven a dos canales —pantalla con sesión, API con clave— declarando el cliente entero. Ensancharlas
de nuevo habría reabierto la puerta; lo correcto es que **cada parámetro declare lo mínimo que la
función usa**, y entonces el compilador afirma en cada una que no toca las superficies peligrosas.

Leer el error como «me he pasado recortando» es el reflejo equivocado: la cascada es el inventario
gratis de quién pedía de más.

Y aparecerá alguna excepción legítima: se resuelve con una puerta CON NOMBRE que entregue **la
superficie concreta y no el objeto entero**, visible en un grep y vigilable por gate — nunca con un
hueco en la lista, que se lo abre a todos a la vez.
