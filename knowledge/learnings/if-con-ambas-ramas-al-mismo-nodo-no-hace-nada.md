---
title: un if cuyas dos ramas van al mismo nodo es decoración, no control de flujo
date: 2026-07-31
source: claude-code-session
tags: [n8n, workflow, agentesia]
---

Que exista un nodo `IF` con la condición correcta no significa que haga algo. Hay que
mirar `connections`, no el canvas.

Caso real (ChatBOT WhatsApp de Agentesia): el prompt mandaba cerrar con `[FIN]` y había un
`Es FIN` comprobando `output contains "[FIN]"`. Sus dos ramas iban a `Dividir mensaje`:

```
Es FIN → true  → Dividir mensaje
       → false → Dividir mensaje
```

Ni limpiaba el marcador ni resolvía la conversación. Y midiendo las ejecuciones, el modelo
**no emitía `[FIN]` ni una sola vez** (0 de 30). Doble fallo que se tapaba mutuamente: si
el marcador llegara a salir, se lo comería el cliente en el mensaje.

- Verificar un marcador de control es medir dos cosas: que el modelo lo emite y que el
  cableado hace algo distinto en cada rama.
- Síntoma visible desde fuera: conversaciones que nunca se cierran (12 abiertas sin asignar
  en Chatwoot).

Ver [[error-de-tool-de-ai-agent-no-marca-la-ejecucion-como-fallida]]
