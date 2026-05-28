---
title: bot multi-acción fallback active_org_id silencia routing
date: 2026-05-28
source: claude-code-session
tags: [whatsapp, multi-org, n8n, ux]
---

`profiles.active_org_id` como fallback de org en un bot WhatsApp es conveniente
para chat (no re-preguntar cada mensaje de texto) pero silencia preguntas de
routing en acciones independientes como ingesta de facturas.

Síntoma: usuario con 2+ orgs sube foto → el bot carga en la org del switcher
web sin preguntar, aunque el usuario quería otra. Además escribe un sticky de
6h que perpetúa el silencio.

Separación correcta:
- **Chat/conversación**: sticky 6h está bien; no interrumpir flujo de texto.
- **Ingesta (foto/PDF)**: siempre preguntar si `candidate_orgs >= 2`, ignorar sticky.

Implementación en n8n: tras `resolve-context`, si `ctx.matched && ctx.candidate_orgs?.length >= 2`
→ forzar `multi_org_pending: true` en `Preparar Datos Ingesta` antes de subir nada.
En backend (`whatsapp-resolve.ts`): no sincronizar `active_org_id` → sticky automáticamente.
