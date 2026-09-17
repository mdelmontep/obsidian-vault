---
title: retell — endpoints que se retiran en 2026 y sus sustitutos
date: 2026-09-14
source: centro-elphis
tags: [retell, api, deprecacion, sip, sdk]
---

Los correos «[ACTION REQUIRED] Deprecated API usage» llegan por **tráfico real** del
workspace (`org_Z0DHVMTvqfBpvZuH`), con IP y user-agent: el emisor puede ser un n8n de
cualquier cliente o una sesión de Claude siguiendo una skill vieja. No los dispara el repo.

| Se retira | Sustituto |
|---|---|
| `GET /get-agent-versions/{id}` | `GET /list-agent-versions/{id}` — 15-sep-2026 |
| `GET /list-phone-numbers` · `/list-batch-tests` · `/list-test-runs` · `/list-test-case-definitions` | sus `/v2/…` |
| `POST /v2/list-calls` | `POST /v3/list-calls` |
| `GET /list-agents` | `POST /v2/list-agents` |
| `POST /publish-agent/{id}` | `POST /publish-agent-version/{id}` con `{"version": N}` (el viejo ya daba 400 el 9-sep) |
| `POST /v2/create-web-call` | `POST /v3/create-web-call` — 30-sep-2026 |
| SIP `sip:5t4n6j0wnrl.sip.livekit.cloud` | `sip:sip.retellai.com` — 30-sep-2026 |

- **Todos los `list-*` nuevos paginan** (50/página, `{items, pagination_key, has_more}`) y la
  doc no lo dice: quien hacía `max(...)` sobre la lista entera ahora ve solo la primera
  página. **`v2/list-batch-tests` además NO viene ordenado** (212 lotes medidos): hay que
  recorrer todas las páginas antes de elegir el último.
- **`v3/list-calls` cambia también el filtro y la forma** → [[migrar-un-endpoint-deprecado-cambia-la-forma-y-el-consumidor-lo-calla]]
- **`v3/create-web-call` exige SDK `retell-client-js-sdk` 3.x** (el 2.x se retira el 30-sep):
  un `access_token` solo ya no conecta, `startCall` necesita además `callId`, `transport`
  (`gateway`) e `iceServers`. Medido: con solo el token, LiveKit responde «invalid API key».
- **La fecha anunciada no es el apagado real**: el 17-sep `get-agent-versions` seguía dando
  200. Sirve de colchón, no de plan.
