---
title: kommo webhook seleccionar solo mensaje entrante recibido
date: 2026-04-17
source: claude-code-session
tags: [kommo, n8n, webhook]
---

En la configuración de webhooks de Kommo (Ajustes → Integraciones → webhook), si se seleccionan **todas las acciones**, llegan eventos `talk[update]` que no contienen el contenido del mensaje. El evento `add_message` (que sí trae el mensaje) puede no llegar o quedar enterrado.

**Fix**: seleccionar únicamente **"Mensaje entrante recibido"** en la sección de chat/mensajes.

Descubierto en Clínica Zen: el webhook de n8n recibía `talk[update]` pero no `add_message` hasta que se desmarcaron todas las acciones y se dejó solo la de mensaje entrante.
