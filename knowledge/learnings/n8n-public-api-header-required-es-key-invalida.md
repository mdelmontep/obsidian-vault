---
title: n8n Public API responde "X-N8N-API-KEY header required" aunque mandes la cabecera, si la key está revocada
date: 2026-06-24
source: claude-code-session
tags: [n8n, api, debugging, tufacturaia]
---

Llamar a la Public API de n8n con una key revocada/no reconocida devuelve
`401 {"message":"'X-N8N-API-KEY' header required"}` **aunque la cabecera vaya en la
request** (verificado con `curl -v`: el header sale por el cable). El mensaje engaña:
parece un proxy/Traefik filtrando la cabecera o la API apagada, y no lo es.

Cómo descartar hipótesis sin tocar el host:
- `GET /api/v1/docs` sirve el swagger "n8n Public API UI" → la API pública está ACTIVA
  (si estuviera apagada daría 404). Entonces el 401 es la key, no la config.
- Key válida vs revocada se distingue probando `GET /api/v1/workflows?limit=1`: 200 = OK.
- Un redeploy/restore de n8n NO siempre rota el secret de firma (las keys nuevas seguían
  validando 200); aquí la vieja estaba simplemente revocada, no había rotación.

Moraleja: no asumas "proxy filtra header" ni "secret rotado" por el mensaje; prueba 200
contra la instancia con la key candidata antes de tocar infra.
