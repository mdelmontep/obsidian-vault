---
title: slack agentesia lab — API y bot
date: 2026-04-20
source: claude-md-migration
tags: [slack, bot, api]
---

# Slack — AgentesIA Lab

- **Escritura en canales y canvas** via Slack API con bot token (guardado en memory). Patrón: `conversations.join` para unir el bot al canal + `canvases.edit` con `changes[].operation: "insert_at_end"` y `document_content.type: "markdown"`.
- **Canvas de Tareas Pendientes** está en `#01-tareas-pendientes` — es el sitio para añadir pendientes del equipo.
- **El bot no tiene scope `groups:read`** — no puede listar canales privados, solo públicos.
- **Barra de color = `attachments`, y entonces el `text` de primer nivel SOBRA**: `chat.postMessage` con `{text, attachments:[{color, blocks}]}` pinta el `text` encima del attachment y el aviso sale **duplicado**. El resumen va en `attachments[0].fallback` (que además es lo que se lee en la notificación del móvil), no en `text`. Útil cuando un canal recibe avisos de varios clientes: el color lateral clasifica de un vistazo sin leer (Elphis, 15-ago: rojo error / naranja trigger / azul flujo previsto).
- 🔴 **Un bloque de código pierde su PRIMERA línea si el texto va pegado a la apertura de ```**: se interpreta como especificador de lenguaje y se descarta. Medido el 15-ago — los **6** avisos de una sesión llegaron mutilados: se perdieron filas de tabla enteras y la mitad «antes» de un antes/después, dejando visible solo la mitad que no demuestra nada. **Salto de línea siempre tras la apertura.** El emisor no lo ve (su texto está bien; el defecto solo existe en lo que lee el equipo) → **releer el canal después de enviar** cualquier aviso del que dependa una decisión ajena. Ver [[leer-un-canal-con-limit-1-se-salta-mensajes]].
