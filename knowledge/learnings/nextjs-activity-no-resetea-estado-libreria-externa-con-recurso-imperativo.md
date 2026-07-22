---
title: next.js activity no resetea estado de librerías externas con recurso imperativo
date: 2026-07-22
source: claude-code-session
tags: [nextjs, cache-components, activity, react-pdf]
---

Con Cache Components (`<Activity>`), ocultar una ruta NO desmonta sus
componentes — solo los oculta (fiber "vivo" en segundo plano). Librerías
externas que gestionan un recurso imperativo propio (worker, canvas,
websocket, transporte interno tipo pdf.js) suelen limpiar/invalidar ESE
recurso al ocultarse, pero el estado de React (documento/página ya
resueltos) no se resetea con ellas — solo al cambiar props clave como `file`.

Si la ruta reaparece antes de que la librería reasiente su recurso interno,
el componente pinta sobre un objeto ya destruido → crash real (sube hasta
el error boundary raíz de Next), no cosmético. Caso real: `react-pdf` +
`<Activity>`, `Cannot read properties of null (reading 'sendWithPromise')`.

**Fix**: error boundary local alrededor del componente que usa la librería
externa, keyed por un contador de generación. Si crashea, se descarta y
remonta desde cero (tope 1-2 reintentos, luego fallback estático) — barato
porque la causa es una carrera transitoria hide/show de `<Activity>`, no un
dato inválido.

**Antes de activar `cacheComponents` app-wide**: auditar qué componentes
usan `new Worker()`/`WebSocket()`/canvas context/librerías con transporte
interno propio — son los candidatos a este mismo patrón. Ver
[[next16-cache-components-migracion-por-etapas]].
