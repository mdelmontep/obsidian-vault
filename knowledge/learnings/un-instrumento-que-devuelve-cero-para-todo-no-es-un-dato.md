---
title: si todos los contadores salen a cero a la vez, el roto es el instrumento
date: 2026-09-15
source: agh-iberica
tags: [medicion, diagnostico, pdf, sesgo]
---
Grepeando el stream descomprimido de un PDF conté operadores: `Tj`=0, `TJ`=0, `Tf`=0,
`BT`=0, `re`=0, `Do`=0, `m$`=0, `l$`=0, `c$`=0. Concluí «cero operadores de texto: las
letras son curvas» y lo escribí en dos issues. Pero **acababa de ver `m`, `l` y `c` en
ese mismo stream**, así que los nueve ceros eran imposibles: mis patrones estaban mal
anclados. Otra sesión midió 104 `BT` y 104 `TJ` reales (los rótulos del formulario).

La conclusión de fondo aguantó —los valores rellenados SÍ son vectores, y ninguna
librería de texto los lee— pero la afirmación absoluta era falsa, y encima debilitaba
el hallazgo bueno: el documento **parece** tener capa de texto porque la tiene para los
rótulos, y eso es justo lo que engaña a un enrutador «¿tiene texto? → camino de texto».

Regla: cuando TODAS las celdas de una medición salen al mismo valor extremo, el
contrafáctico no es el objeto medido, es el medidor. Un patrón de control que DEBE dar
un número distinto de cero cuesta una línea.

Ver [[el-canal-obligatorio-caido-deja-el-ciclo-sin-cerrar]], [[con-la-fuente-caida-toda-cifra-es-un-proxy]].
