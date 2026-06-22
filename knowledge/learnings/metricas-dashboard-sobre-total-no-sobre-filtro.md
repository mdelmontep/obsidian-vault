---
title: las métricas de un dashboard van sobre el total, no sobre la vista filtrada
date: 2026-06-22
source: claude-code-session
tags: [dashboard, ux, frontend]
---

Si los KPIs de cabecera se calculan sobre el conjunto YA filtrado, mienten:
filtrar "solo proyectos" dejaba "Pipeline €" en 0 € (los presupuestos se habían
filtrado), y "Activos/Sin responsable" pasan a describir el subconjunto.

Regla: el filtro narra la VISTA (qué cards se ven), no los KPIs. Computar las
métricas siempre sobre el dataset completo y pasarlas aparte a la vista; el
filtro solo afecta a las columnas/cards.

Lo detectó una revisión de composición (los tests per-componente pasaban verde).
