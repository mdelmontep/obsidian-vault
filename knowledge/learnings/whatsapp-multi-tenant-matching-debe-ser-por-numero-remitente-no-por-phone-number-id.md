---
title: whatsapp multi-tenant matching debe ser por numero remitente no por phone_number_id
date: 2026-04-24
source: claude-code-session
tags: [n8n, facturaia, whatsapp, multi-tenant]
---

El `phone_number_id` de Meta es el ID interno del número **receptor** (el de FacturaIA: `1180494911802950`). Es el mismo para todas las orgs porque todas comparten el mismo número de WhatsApp Business.

Para multi-tenant, el matching debe comparar el número del **remitente** (`msg.from`, normalizado sin prefijo 34) contra `settings.whatsapp.phone_number` de cada org en Supabase.

Workflow n8n `zYcHHa8jWXB6dY5i` — nodo "Prepare Data":

```js
const org = allOrgs.find(o => {
  const wa = o.settings?.whatsapp;
  if (!wa || !wa.phone_number) return false;
  const orgPhone = normalizePhone(wa.phone_number);
  return orgPhone === fromNorm;
});
```

Si no encuentra org, devuelve `[]` y el flujo se corta silenciosamente (no hay error visible en n8n, status "success").

Ver también: [[campo sincronizado entre tablas debe poblarse en todos los puntos de escritura]]
