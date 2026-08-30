---
title: un subagente cita el mecanismo y no el guard que lo cierra treinta líneas antes
date: 2026-08-30
source: facturaia
tags: [subagentes, verificacion, evidencia]
---
Pregunté si algún flujo reescribía las líneas de una factura y el subagente respondió con
`ruta:175-182`, el `delete` + `insert` real, y con un «el riesgo es real, no es hipotético».
Lo repetí al usuario. Treinta líneas más arriba, en 143-148, el guard exigía otro tipo y otro
estado: por esa ruta no entraba. La mitigación que se iba a diseñar sobraba entera.

El subagente no mintió: encontró el mecanismo, que es lo que le pedí. **Lo que no hizo fue leer
hacia arriba.** Una cita `fichero:línea` prueba que el código existe, nunca que sea alcanzable.

Patrón: al pedir «¿puede pasar X?», exigir en el prompt que **cite el guard que lo permite o
diga que no hay ninguno** — y antes de repetir el hallazgo, abrir la función entera, no las ocho
líneas citadas. Un barrido posterior con esa exigencia cerró el riesgo del todo: cero caminos.

Relacionado: [[una-cita-fichero-linea-caduca-en-silencio-el-gate-debe-corregirla]]
