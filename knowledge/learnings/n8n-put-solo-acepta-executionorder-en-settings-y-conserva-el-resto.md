---
title: el PUT de la API pública de n8n solo acepta executionOrder en settings, y conserva el resto
date: 2026-08-17
source: claude-code-session
tags: [n8n, api, workflow, elphis]
---
`PUT /api/v1/workflows/{id}` devuelve `400 request/body/settings must NOT have additional properties`
si mandas el `settings` que te dio el GET. Los culpables medidos en n8n Community (Elphis, 17-ago):
`errorWorkflow` y `binaryMode`. El mensaje **no dice qué clave sobra**, así que se localiza quitando
de una en una.

Lo que no es obvio y evita el susto: **mandar `{executionOrder}` a secas NO borra las demás**. Tras
el PUT, el GET seguía devolviendo `errorWorkflow` y `binaryMode` intactos — n8n fusiona en vez de
reemplazar. Sin eso, la tentación es no editar el workflow por API por miedo a perder el
[[n8n-error-handler-global-via-errorworkflow]] y quedarte sin avisos de error.

Patrón para el payload: `{name, nodes, connections, settings: {executionOrder}}`. Y verifica el
`settings` en el GET posterior, no lo asumas.
