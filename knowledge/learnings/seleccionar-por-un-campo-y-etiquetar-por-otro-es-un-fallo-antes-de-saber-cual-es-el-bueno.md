---
title: seleccionar por un campo y etiquetar por otro es un fallo antes de saber cuál es el bueno
date: 2026-09-20
source: facturaia
tags: [arquitectura, fiscal, export, verificacion]
---
Un export contable elegía las filas del trimestre por `fecha_devengo` y luego fechaba el asiento
resultante por la fecha de expedición del documento. El fichero cortado para 1T salía con asientos
de 2T. El issue lo planteaba como «¿cuál de las dos fechas es la correcta?», y esa pregunta llegaba
tarde: **cualquiera que sea la respuesta, filtrar por un campo y rotular por otro ya está mal.**

El patrón, fuera de lo fiscal: en todo lo que corta por periodo —informes, exports, cierres,
facturación por ciclo— hay un campo que decide QUÉ ENTRA y otro que decide QUÉ PONE. Si no son el
mismo, el consumidor ve un lote que se contradice a sí mismo. Y no lo caza ningún test de tipos:
los dos campos son `string` con la misma forma.

Cómo se busca: por cada sitio que pagina/filtra por un campo de fecha, grep de qué fecha escribe
la fila de salida. Aquí eran cuatro líneas en dos ficheros y **ningún fixture tenía las dos fechas
distintas**, así que la suite entera pasaba sin discriminar nada.

Corolario al decidir cuál gana: mira si el formato de salida ya transporta las dos. Si las lleva en
campos propios (el SUENLACE manda expedición y operación aparte de la fecha del asiento), la
elección no pierde información y deja de ser un dilema.
Ver [[un-campo-correcto-para-el-registro-decide-el-periodo-al-caer-en-un-coalesce]] · [[rectificativa-se-declara-en-el-periodo-de-su-expedicion]]
