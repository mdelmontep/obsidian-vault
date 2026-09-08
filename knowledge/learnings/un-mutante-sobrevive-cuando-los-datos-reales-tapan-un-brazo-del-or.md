---
title: un mutante sobrevive cuando los datos reales tapan un brazo del OR
date: 2026-09-08
source: centro-elphis
tags: [testing, mutacion, puertas]
---

Criterio bajo prueba: `cerrado = status===3 || status===4 || actual_closed_date`. Las puertas
corrían contra los 1.574 deals reales del CRM y todas pasaban. Al mutar `status===3` a
`status===30`, **ningún test se puso rojo**: los 74 deals ganados reales traen *además*
`actual_closed_date`, así que el tercer brazo tapaba al primero. El brazo llevaba sin
verificarse desde que se escribió.

Los datos reales dan confianza en la cobertura de casos, pero **no verifican una condición
compuesta**: solo prueban las combinaciones que la realidad produce, y las que faltan son
invisibles. La puerta que faltaba probaba cada brazo por separado con entradas construidas.

Regla: para cada `||`/`&&` de una regla de negocio, una puerta por brazo con un caso donde
SOLO ese brazo sea cierto — y comprobarlo mutando ese brazo, no leyéndolo. Ver
[[la-mutacion-que-desbloquea-el-guard-tiene-que-ser-sobre-un-fichero-del-stage]].
