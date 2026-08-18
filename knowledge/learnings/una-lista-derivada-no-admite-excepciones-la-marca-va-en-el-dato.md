---
title: una lista derivada de otra fuente no admite excepciones; la marca va en el dato
date: 2026-08-18
source: claude-code-session
tags: [diseño, modelo-de-datos, facturaia]
---
Cuando un candado se implementa como una lista **derivada** de otra estructura
(`new Set(Object.values(MAPA))`), añadirle una excepción exige corromper la fuente. Y esa
fuente casi siempre tiene un trabajo más importante que el candado.

Caso (TuFacturaIA #1778): proteger una serie de numeración de que el usuario la desactive.
`SERIES_RESERVADAS` se deriva de `SERIE_BY_TIPO`, el mapa del que `createDocument` resuelve
la serie por tipo de documento. Meter una letra que no corresponde a ningún tipo exigía
inventarse un tipo falso: pagar con la parte que numera facturas para conseguir un candado
de UI.

Las tres opciones y el criterio:
- ampliar la lista derivada → corrompe la fuente, y además aplica a TODOS los tenants;
- condicional por tenant en el código → mete un id de producción en el TS y no vale para
  un segundo caso;
- **una marca en el DATO** (columna booleana) → viaja con la fila, sirve para cualquier
  tenant, y el guard pasa a ser una condición más.

La derivación se queda para lo que sí deriva: añadir un tipo nuevo no debe exigir acordarse
de marcar su fila. Las dos cosas conviven, no se sustituyen.
