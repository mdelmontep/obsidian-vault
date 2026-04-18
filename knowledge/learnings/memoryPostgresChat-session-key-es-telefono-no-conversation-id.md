---
title: memoryPostgresChat session key es telefono no conversation id
date: 2026-04-17
source: claude-code-session
tags: [n8n, chatwoot, postgres, memoria, chatbot]
---

En el ChatBOT mejorado con Chatwoot, la session key de `memoryPostgresChat` es el **número de teléfono** del contacto (ej: `34617314938`), no el ID de conversación de Chatwoot.

## Consecuencias

1. **Resolver conversación en Chatwoot NO limpia la memoria del agente** — el historial persiste bajo la misma session key (teléfono) y contamina conversaciones futuras del mismo contacto
2. **Respuestas alucinadas se fosilizan** — si el agente halucina una respuesta (ej: "ticket #1 creado" sin ejecutar la tool), esa respuesta queda en memoria. En el siguiente turno, el agente ve "ya confirmé el ticket" en el historial y no vuelve a intentar la tool call
3. **Limpiar memoria requiere SQL directo** — no hay UI en n8n para borrar sesiones individuales

## Cómo limpiar

```sql
DELETE FROM n8n_chat_histories WHERE session_id = '<telefono>';
```

Ejecutar en el contenedor Postgres:

```bash
docker exec <postgres_container> psql -U postgres -d n8n -c "DELETE FROM n8n_chat_histories WHERE session_id = '34617314938';"
```

## Cuándo aplica

Siempre que se depure un AI Agent con `memoryPostgresChat` y el agente parezca "recordar" cosas que no pasaron o no ejecute tools que debería ejecutar. Primer paso de diagnóstico: verificar qué hay en la memoria con `SELECT * FROM n8n_chat_histories WHERE session_id = '<telefono>' ORDER BY id DESC LIMIT 10;`
