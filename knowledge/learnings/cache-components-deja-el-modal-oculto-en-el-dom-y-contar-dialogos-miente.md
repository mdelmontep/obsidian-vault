---
title: cache components deja el modal oculto en el dom y contar dialogos miente
date: 2026-10-03
source: facturaia (smoke de #3224, reembolsos)
tags: [nextjs, cache-components, activity, smoke, agent-browser]
---

Con `cacheComponents: true` (Next 16), al navegar con un `<Link>` desde dentro de un modal portaleado a `body`, la ruta anterior queda en `<Activity>` oculta y el nodo del modal SIGUE en el DOM con `display: none` (rect 0×0).

Tell: un smoke que cuenta `document.querySelectorAll('[role=dialog]').length` o lista su `innerText` ve la ficha de la página anterior «abierta» sobre la nueva. Parece un bug de UX y no lo es: costó 15 min de diagnóstico.

Patrón en smokes: filtrar por visibilidad antes de concluir nada.
`[...document.querySelectorAll('[role=dialog]')].filter(d => getComputedStyle(d).display !== 'none' && d.getBoundingClientRect().width > 0)`
Y lo mismo al clicar un botón dentro de un diálogo: `b.offsetParent !== null`, o se clica el de la ruta oculta.

Relacionado: [[nextjs-activity-no-resetea-estado-libreria-externa-con-recurso-imperativo]], [[cerrar-un-overlay-desde-el-cleanup-de-un-efecto-lo-rompe-en-strictmode]].
