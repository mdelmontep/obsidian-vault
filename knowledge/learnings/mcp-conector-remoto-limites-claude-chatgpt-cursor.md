---
title: Límites reales de los conectores MCP remotos (Claude/ChatGPT/Cursor)
date: 2026-06-19
source: docs oficiales Anthropic + OpenAI + Cursor (jun 2026)
tags: [mcp, oauth, claude, chatgpt, cursor, integraciones, facturaia]
---

No existe forma de que un servidor MCP "empuje" su conector a Claude o ChatGPT. La dirección es **inversa**: el usuario pega la URL del servidor en su cliente, y eso dispara el login OAuth a tu servicio. Implicaciones al diseñar un "botón Conectar":

- **Cursor** — único 1-clic real: deep-link `cursor://anysphere.cursor-deeplink/mcp/install?name=<n>&config=<base64({url})>`.
- **Claude** — el usuario pega la URL manualmente. En **cuenta personal** (Free/Pro/Max): Conectores → "+" → Añadir conector personalizado (atajo `claude.ai/settings/connectors?modal=add-custom-connector`). En **Team/Enterprise**: solo el **Owner** lo añade vía *Org settings → Conectores → Add → Custom → Web*; los miembros luego solo "Conectar". El "Directorio" son partners curados (botón "Solicitud"), no self-add.
- **ChatGPT** — requiere **Developer Mode** (Plus/Pro/Business/Enterprise/Edu): Conectores → Ajustes avanzados → activar → Crear app con la URL. En Business/Enterprise lo habilita el admin.

El "1-clic en Claude" (catálogo) solo se consigue **listándose en la Connectors Directory** (submission con privacy policy pública obligatoria — sin ella, rechazo automático). Por eso un modal "cómo conectar" con URL+Copiar+instrucciones por cliente es el techo realista para Claude/ChatGPT; el botón mágico solo es posible en Cursor.

Caso: TuFacturaIA modal de conexión (PR #384) + dossier directory (057).
