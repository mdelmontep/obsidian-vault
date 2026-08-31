---
title: extraer a `_parts/` para esquivar un trinquete de tamaño crea un ciclo si la parte importa el tipo del padre
date: 2026-08-31
source: facturaia
tags: [arquitectura, dependencias, trinquetes, madge]
---
Un trinquete que topa un fichero y **solo le deja bajar** convierte "añade una
línea" en "extrae el módulo". Eso es el diseño, no un obstáculo.

**La trampa está en cómo extraes.** Lo natural es sacar la función a
`_parts/x.ts` e importar de vuelta el tipo que necesita desde el padre: eso
cierra un ciclo `X.tsx ↔ X/_parts/x.ts` que `madge` cuenta aunque los tipos se
borren al compilar. Facturaia arrastra **26 ciclos** nacidos así.

**Fix**: dale a la parte su **propio tipo de entrada, estrecho**, con solo los
campos que usa; el del padre lo satisface estructuralmente y nadie importa a
nadie. Verifica con `deps:circular` antes y después: el número no debe moverse.

El trinquete cuenta **líneas de código**, no líneas: un import multilínea cuesta
más que uno de una línea.
Ver [[un-estado-sin-caducidad-es-una-promesa-permanente-en-pantalla]].
