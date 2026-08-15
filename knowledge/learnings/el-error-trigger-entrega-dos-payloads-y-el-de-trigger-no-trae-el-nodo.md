---
title: el error trigger entrega dos payloads y el de trigger no trae el nodo
date: 2026-08-15
source: claude-code-session
tags: [n8n, observabilidad, elphis, gotcha]
---
El handler de Elphis avisaba `Nodo: sin nodo · unknown error` cada mañana. No era un fallo
del handler: **el Error Trigger entrega dos formas distintas** según dónde falle
(`packages/cli/src/execution-lifecycle/execute-error-workflow.ts`):

- ejecución → `{workflow, execution:{id, url, error, lastNodeExecuted, mode, retryOf}}`
- **trigger** → `{workflow, trigger:{error, mode}}` — sin `execution`, sin `lastNodeExecuted`

Leer solo `execution.*` deja el aviso en blanco justo cuando falla un trigger. Y hay una
segunda capa: si el error es un `WorkflowActivationError` llega serializado como
`{message, timestamp, name, context}` — **pierde `node` y pierde `cause`**, así que ni el nodo
ni la causa original ("IMAP connection closed") viajan. El nombre solo está dentro del texto:
rescatarlo con `/node "([^"]+)"/` cubre las dos redacciones de n8n.

Regla: en un error handler, leer `execution` **y** `trigger`, y como cinturón coger la primera
clave de primer nivel que traiga `.error` dentro — así no depende de la versión.
Ver [[n8n-error-handler-global-via-errorworkflow]] · [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]]
