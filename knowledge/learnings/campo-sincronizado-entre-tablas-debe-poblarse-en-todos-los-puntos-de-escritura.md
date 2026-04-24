---
title: campo sincronizado entre tablas debe poblarse en todos los puntos de escritura
date: 2026-04-24
source: claude-code-session
tags: [arquitectura, supabase, facturaia]
---

Cuando un campo derivado (`settings.whatsapp.phone_number`) se sincroniza desde otro campo (`organizations.telefono`), hay que cubrir **todos** los puntos donde se escribe el campo fuente:

1. **Creación de org** (POST admin) — copiar al crear
2. **Update desde settings del usuario** — sincronizar al guardar
3. **Update desde admin panel** (PATCH admin) — sincronizar al guardar
4. **Auto-populate frontend** — si el campo derivado está vacío pero el fuente tiene valor, persistir al cargar

Si falta alguno, el campo derivado queda vacío y los consumidores (n8n workflow) fallan silenciosamente — devuelven `[]` sin error, el flujo se corta, y n8n marca la ejecución como "success".

No añadir fallbacks en el consumidor (ej: buscar también por `org.telefono` si no hay `settings.whatsapp.phone_number`). La fuente de verdad debe ser una sola; los fallbacks enmascaran el problema real y diluyen la arquitectura.

Caso real: FacturaIA WhatsApp ingesta — Borja tenía `telefono: "659834983"` pero `settings.whatsapp` solo tenía `phone_number_id: ""` (campo viejo). El nodo n8n no encontró match y la factura no se procesó.
