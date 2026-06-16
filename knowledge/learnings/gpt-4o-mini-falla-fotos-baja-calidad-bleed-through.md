---
title: gpt-4o-mini (vision) falla en fotos de baja calidad con transparencia del reverso
date: 2026-06-16
source: claude-code-session
tags: [ocr, llm, vision, openai, facturaia]
---

En fotos de factura donde el reverso se transparenta (bleed-through), `gpt-4o-mini`
mezcla el texto de ambas caras → inventa el emisor y lee mal el NIF (dígito de
más). `gpt-4o` lo resuelve en los mismos documentos.

- Verificado reproduciendo el ticket real contra ambos modelos (facturas Registro
  Mercantil / BORME, org Abba).
- El cuello NO es el prompt ni la resolución: es la capacidad visual del modelo.
  No malgastes tiempo tuneando el prompt antes de probar a subir de tier.
- Coste/doc de `gpt-4o` ~15-20× el de mini, pero siguen siendo céntimos por factura.
- Ojo al lado servidor: `gpt-4o` es más lento → vigila timeouts del disparo (caso
  facturaia: webhook n8n con AbortController a 30s).

NIF del emisor que NO está impreso en el documento (típico en minutas registrales):
el modelo cae en el del receptor; no se puede extraer lo que no existe → debe
neutralizarlo un guard (comparar con el NIF de la propia org).
