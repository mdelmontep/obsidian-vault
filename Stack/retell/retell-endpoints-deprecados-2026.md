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

## Quién emite: cómo se averigua (12-oct)

El correo da IP, cliente HTTP y nombre de la clave, nunca el sistema. Se cruzan así:
- **IP → DNS inverso**: `147.96.4.164` resolvía a `dani-mac.red.ucm.es`.
- **IP → dominios conocidos**: resolver cada dominio del vault y de los ítems Dokploy de
  1Password y buscar coincidencias. Así salió que `185.47.13.164` es `n8n-borja.tecnocloud.es`.
- **Cliente `axios` a hora fija** = nodo HTTP Request de un n8n programado. `python-urllib` y `node`
  = scripts o sesiones de Claude.
- **Cruzar la hora con el alta en Retell**: un `import-phone-number` fallido a las 11:36 y un
  número modificado a las 11:37 (`last_modification_timestamp` en `v2/list-phone-numbers`)
  identificaron a Admicom.

## Migración SIP en Netelip (hecha el 12-oct)

- **El aviso solo lista los DDI que tuvieron llamadas.** Netelip tenía 7 apuntando a LiveKit, no 3:
  hay que mirar el panel (SIP Trunking → Numeración de acceso), no el correo.
- **Cada llamada dice por dónde entró**: por LiveKit trae `custom_sip_headers` con
  `x-lk-real-ip`/`x-lk-transport`/`x-lk-call-info`; por `sip.retellai.com` solo `x-called-ddi`. Es
  la verificación objetiva (`v2/get-call` o `v3/list-calls`), mejor que «contestó».
- **En Netelip no hay editar**: «Desactivar» (enlace GET directo, sin confirmación) y luego
  «Activar», que abre el formulario *Actualizar acceso* con Servidor SIP, la casilla «Añadir al
  número E164 el signo +» y Puerto. Mientras tanto el DDI queda como «Línea SIP» sin destino,
  unos 20-30 s sin entrada. No hay campo de transporte (va UDP, que Retell acepta).
- **Valores**: Servidor `sip.retellai.com`, casilla `+` marcada, puerto `5060`. Funciona también
  para los DDI que antes iban sin `+` (AGH, Admicom). **Vuelta atrás**: lo mismo con
  `5t4n6j0wnrl.sip.livekit.cloud`, mientras exista.
- **No hay que añadir rangos de IP de Retell en Netelip**: las entrantes no se filtran y la
  terminación (salientes y transferencias) se autentica con usuario y contraseña, con el campo IP vacío.
- **Sin transcripción ni grabación no es fallo** si el agente tiene
  `data_storage_setting: basic_attributes_only` (Elphis Psicología): mirar las latencias de ASR y TTS.
- **Verificador**: `python3 -I ~/Projects/obsidian-vault/Stack/retell/verificar-migracion-sip.py` lista,
  por DDI, las llamadas posteriores a la migración y por qué vía entraron (lee la clave con `opsa`).
  Llamadas de 3-12 s con `user_hangup` a mitad del saludo son llamantes que cuelgan al oír «IA», no
  cortes: si la transcripción tiene voz del llamante, el audio va en los dos sentidos.
- Quedó en LiveKit el **+34846635194**, que no está dado de alta en Retell.
- Hacer clic en Desactivar/Guardar desde Claude in Chrome lo bloquea a veces el clasificador del modo auto
  («Modify Shared Resources»). Con el permiso explícito del usuario en el chat se pudo.
