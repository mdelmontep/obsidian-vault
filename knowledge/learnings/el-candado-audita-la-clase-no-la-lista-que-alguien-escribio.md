---
title: un candado se equivoca en dos ejes — a quién audita y qué trozo mira
date: 2026-08-30
source: facturaia
tags: [testing, mutacion, sql, candados]
---
Una migración movió el objetivo de cobro al líquido, **enumeró tres** sitios que
comparaban contra el bruto y avisó en su cabecera de que «un arreglo a medias es peor
que ninguno». Se le escapó un cuarto: la lista la escribió alguien leyendo, y la lista
es el punto débil, no el arreglo.

**A quién audita**: no el fichero arreglado — barre CADA función que inserte en la
tabla y exige la regla a todas, con guarda de medición (`emisores.length > 0`) para que
no pase en verde si no encuentra a nadie.

**Qué trozo mira**: dos versiones dieron SIN VÍCTIMA con `mutate`. La primera buscaba la
marca en el cuerpo entero (leerla arriba y estampar el valor malo abajo pasaba); la
segunda pedía UNA mención en el INSERT (la del campo `_eur` la satisfacía sola). Recorta
al bloque que DECIDE y **prohíbe la forma mala**, no basta con pedir la buena.

Un candado que cuenta ocurrencias de SQL ve una redefinición (`CREATE OR REPLACE` copia
el cuerpo) como sitio nuevo: correcto que salte — se documenta en su lista blanca.
Ver [[barrer-el-diff-en-vez-de-mutar-a-mano]].
