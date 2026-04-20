---
title: ocr de facturas confunde receptor con emisor sin contexto de org_nombre
date: 2026-04-20
source: claude-code-session
tags: [ocr, openai, facturaia, n8n]
---

GPT-4o-mini Vision, al extraer datos de una factura, pone como "proveedor" la empresa más prominente del documento — que muchas veces es el receptor/cliente (la empresa que subió la factura), no el emisor.

**Fix**: incluir el nombre de la organización del usuario en el prompt:

```
IMPORTANTE: La empresa que sube esta factura es "NombreOrg". 
Esta empresa es el CLIENTE/RECEPTOR de la factura. 
El proveedor/emisor es la OTRA empresa que aparece en el documento.
No confundas receptor con emisor.
```

En FacturaIA, el API route `/api/upload` consulta `organizations.nombre` y lo envía como `org_nombre` en el body del webhook a n8n. El Code Node lo inyecta al inicio del prompt.

**Aplica a**: cualquier pipeline de OCR de facturas donde el usuario sube sus propias facturas recibidas.
