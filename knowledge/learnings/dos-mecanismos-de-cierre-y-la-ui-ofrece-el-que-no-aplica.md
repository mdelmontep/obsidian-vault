---
title: con dos mecanismos de cierre, ofrecer el que no aplica da un falso éxito perfecto
date: 2026-07-30
source: claude-code-session
tags: [ux, fallo-exito, admin, patron]
---
Cuando una lista mezcla filas que se cierran de formas distintas, la rama que
decide el botón tiene que ramificar por el mecanismo, no por un campo cualquiera
que suele correlacionar. En el panel de alertas de TuFacturaIA (#1366) se miraba
`org_id` antes que `alert_id`: una incidencia de `system_alerts` que ADEMÁS tenía
org caía en la rama de org y ofrecía "Descartar", que escribe en
`admin_alert_dismissals` — tabla que el collector de esas incidencias no consulta.
Resultado: toast de éxito, la fila desaparece del estado local, y vuelve al
recargar. El botón que sí cerraba ("Resolver") quedaba escondido justo en esas filas.

Regla: el escritor y el lector de un cierre tienen que ser la misma pareja. Si la
acción escribe en un sitio que el productor de la lista no lee, no es un cierre,
es un `setState`. Y la prueba que lo caza es recargar después de la acción, no ver
que la fila desaparece. Ver [[internal-fetch-res-ok-silencioso]]
· [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]]
