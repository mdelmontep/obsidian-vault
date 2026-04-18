---
title: n8n api publica no expone valores de credenciales
date: 2026-04-18
source: claude-code-session
tags: [n8n, api, seguridad]
---

`GET /api/v1/credentials` lista id, nombre y tipo de cada credencial pero nunca devuelve los valores secretos (tokens, passwords, API keys).

No existe endpoint en la API pública para extraer el valor real de una credencial. Los secrets solo son accesibles:
- Dentro de los workflows (en tiempo de ejecución)
- Desde la UI de n8n (editando la credencial)

Implicación: si necesitas un token almacenado en n8n (ej: Slack bot token) para usarlo fuera de n8n, hay que guardarlo aparte (memory de Claude, vault, etc.).
