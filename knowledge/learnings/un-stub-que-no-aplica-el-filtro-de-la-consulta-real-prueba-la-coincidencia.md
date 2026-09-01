---
title: un stub que no aplica el filtro de la consulta real prueba la coincidencia, no el código
date: 2026-09-01
source: agency-portal
tags: [testing, supabase, postgrest, flaky]
---
La función hacía **una consulta por gravedad** (`.eq('severity', s)` en un bucle) y el stub del test
devolvía las mismas filas a las dos. La unión llegaba con **cada `id` duplicado**, así que el lote de
diez plazas podía llenarse con cinco repetidos.

El test pasaba igual, por casualidad: el desempate del orden era `Date.parse(window_ended_at)` y las
30 filas se construían con `new Date()` dentro de un bucle. Todas en el mismo milisegundo → orden
estable → los duplicados quedan detrás → 10 ids distintos. En cuanto el bucle cruzaba **un**
milisegundo, `expected 9 to be 10` y a culpar a la rama que no toca ese fichero.

Reglas: el stub imita **todos** los filtros que la consulta real aplica, no solo los que el test mira;
y los datos del caso llevan claves de orden **separadas a propósito**, para que el fallo sea
determinista y no dependa del reloj. Verificado con `~/.claude/bin/mutate`: quitado el filtro del
stub, el test cae **siempre**, no a veces.

Un flake así no es ruido del arnés: es un stub que miente sobre el contrato. Ver
[[el-predicado-de-un-guard-se-mide-contra-el-historico-antes-de-escribirlo]].
