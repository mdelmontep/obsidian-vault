---
title: whatsapp cloud api fuera de la ventana 24h necesita plantilla, y el botón-url solo admite sufijo dinámico → acortador propio
date: 2026-07-06
source: claude-code-session
tags: [whatsapp, meta, integraciones]
---
WhatsApp Cloud API solo deja enviar texto libre (freeform) DENTRO de la ventana de 24h desde el último mensaje del usuario. Fuera de ventana (proactivo/business-initiated) Meta lo rechaza (error `131047` re-engagement) → hay que mandar una **plantilla aprobada** (categoría utility). Un push desde una llamada de voz es casi siempre fuera de ventana.

Gotchas al montar la plantilla con un enlace personalizado (p.ej. link OAuth):
- El botón-URL de plantilla solo admite **sufijo dinámico sobre base fija** (`https://base/fijo/{{1}}`). Una URL larga con varios params variables (state firmado + PKCE) NO cabe → monta un **acortador propio** (`/c/{token}` → 302 al link real; el token puede ser un blob cifrado que solo lleve quién, y el PKCE se acuña al abrir).
- La variable NO puede abrir ni cerrar el cuerpo del mensaje (error `2388299`).
- Robustez: intenta freeform y ante `131047` cae a plantilla (más fiable que trackear timestamps).
- El agente NO debe prometer «te lo mando por WhatsApp» si no es entregable; y debe decir el siguiente paso por el mismo canal (voz), no solo dentro del WhatsApp que puede no llegar.
Caso real: AGH agente de voz → enlace conectar M365 no llegaba (ventana cerrada). Aplica a cualquier cliente con WhatsApp Cloud API (FacturaIA, Elphis, EcoBox).
