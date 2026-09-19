---
title: una validación "si decides X sin Y, rechaza" debe mirar el estado persistido, no solo el lote
date: 2026-09-20
source: agh-iberica
tags: [validacion, revision, dominio]
---
Regla nueva en un endpoint de decisiones: «si el lote fija la fecha de efecto del salario pero no
aplica salario, rechaza». Salía verde con el gate entero y con sus tests. Dos casos legítimos caían:
(a) el salario decidido como `unchanged` —donde la fecha SÍ se persistía, o sea justo lo contrario de
lo que la regla quería impedir—, y (b) la aprobación en bloque posterior a una decisión de salario ya
tomada, que quedaba **permanentemente** inutilizable.

Patrón: una validación redactada sobre «lo que trae este lote» es falsa en cuanto parte del efecto ya
vive en la BD. La condición se escribe sobre el estado RESULTANTE (lote + lo ya persistido), no sobre
el payload. Y el caso "sin cambio" no es "sin efecto".

Lo cazó una revisión con contexto limpio leyendo la spec, no el gate ni la autorrevisión.
Ver [[una-clave-nueva-en-el-json-de-una-rpc-no-llega-a-nadie-sola]].
