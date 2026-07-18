---
title: setState anidado dentro de otro updater se ejecuta dos veces bajo StrictMode
date: 2026-07-18
source: claude-code-session
tags: [react, hooks, strictmode]
---
Llamar a un `setState` DENTRO del updater funcional de otro `setState` es impuro:
React StrictMode (dev) invoca el updater dos veces → el `setState` interno corre
dos veces. En un toggle (`dir => dir==='asc'?'desc':'asc'`) eso lo deja igual, así
que "ordenar por la misma columna no invierte" — pero SOLO en dev (localhost),
donde justo se hace la QA; en prod funciona. Falso "no reproduce".

Patrón malo:
`setSortBy(prev => { if (prev===key) setSortDir(d=>flip(d)); return prev })`

Fix: un único estado que agrupe lo relacionado, con updater PURO:
`const [sort,setSort]=useState({by,dir}); onSort=k=>setSort(p=>p.by===k?{by:k,dir:flip(p.dir)}:{by:k,dir:'asc'})`

Regla: nunca anides setState en el updater de otro. Si dos estados dependen entre
sí en la misma acción, fusiónalos en un objeto. Caso real: `useSortState` del
módulo Obras de [[facturaia]].
