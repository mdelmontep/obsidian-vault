---
title: un nodo de log con onerror continue puede no haber escrito nunca
date: 2026-08-15
source: claude-code-session
tags: [n8n, observabilidad, anti-patron, elphis]
---
Tres nodos de log de Elphis no habían escrito **jamás** una fila, y las ejecuciones salían todas
en `success`. Dos fallos independientes, cada uno bastaba:

1. **La credencial no existía**: `Credential with ID "R9aMmpO1jdJ8XPJP" does not exist`. Un id
   huérfano en el JSON del workflow no se ve por la UI ni por un GET del workflow.
2. **Las columnas tampoco**: la query escribía `bot_outbound_log(channel, phone, content, ...)`
   y la tabla real tenía `(chatwoot_conv_id, message_type, text_summary, ...)`. Ninguna coincidía.

Con `onError: continueRegularOutput` los dos fallos son invisibles: ni ejecución en rojo, ni
aviso, ni fila. Lo que se perdió: cada mensaje de WhatsApp enviado, cada llamada de voz y **cada
detección de crisis**.

Al auditar un workflow no basta con que las ejecuciones estén verdes: por cada nodo con
`continueRegularOutput`, comprobar que **la credencial resuelve** y que **la tabla y las columnas
existen**. Y contrastar volumen: si la tabla debería tener una fila por evento, contarlas.
Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] · [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]]
