---
title: botón HITL debe referenciar estado persistido propio, no IDs efímeros del proveedor
date: 2026-06-12
source: claude-code-session
tags: [whatsapp, n8n, hitl, meta]
---

Un botón interactivo WhatsApp cuyo payload apunta a un ID del proveedor
(`mov_si:<media_id>` de Meta) falla en diferido: el media caduca (~5 min URL,
30 días el id) y hay caminos del flujo donde ese ID ni existe (multi-org: el
click de selección de empresa no trae media). Caso TuFacturaIA extractos
2026-06-12.

Fix/patrón: el payload referencia estado persistido propio
(`mov_sip:<bandeja_id>` → fila con `org_id` + `documento_url` en Storage); el
rescate re-descarga del propio Storage con service key y fija la org ya
elegida (no re-preguntar). Regla general: todo botón que se pulsa "más tarde"
debe poder resolverse solo con filas de tu BD.
