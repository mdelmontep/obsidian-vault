---
title: la etiqueta humana de un slug debe seguir siendo única, o el filtro se vuelve ambiguo
date: 2026-07-30
source: claude-code-session
tags: [ux, frontend, copy]
---
Pintar un id interno en la UI no se arregla con CSS: `text-transform: capitalize`
sobre `system_alert:ocr-process` da "System Alert:Ocr-Process" — el prefijo interno
a la vista y capitalización por palabra sobre un slug. Se arregla con una función
`labelDe(tipo)` que sea fuente única para el badge Y para el desplegable de filtro.

El gotcha viene después: si el slug lleva un parámetro (`system_alert:<origen>`,
`price_mismatch:<plan>:<ciclo>`, `quota_warn_<cuota>`) y la etiqueta lo tira, dos
tipos distintos colapsan en la MISMA opción del filtro y el usuario no puede
distinguirlas ni saber cuál filtró. La etiqueta tiene que ser inyectiva respecto al
valor: mete el parámetro dentro ("Incidencia técnica · ocr-process"). Y esto solo se
ve renderizado con datos reales — el código y los tests pasan igual, porque cada
llamada por separado devuelve una cadena correcta.
Ver [[feedback_smokes_siempre_con_agent_browser]] · [[dos-mecanismos-de-cierre-y-la-ui-ofrece-el-que-no-aplica]]
