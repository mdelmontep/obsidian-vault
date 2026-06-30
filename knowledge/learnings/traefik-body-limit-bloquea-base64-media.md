---
title: traefik body limit (~4mb) corta silenciosamente base64 de imágenes en http interno
date: 2026-06-30
source: claude-code-session
tags: [traefik, dokploy, whatsapp, ocr, arquitectura]
---

Traefik tiene un body limit por defecto (~4MB). Una imagen WhatsApp en base64 son 7-11MB.
El POST interno llega al endpoint pero Traefik lo corta → el body llega truncado o vacío → el
endpoint falla silenciosamente (no 413 explícito al caller, depende de la config).

Síntoma: ingesta/OCR funciona con PDFs pequeños pero no con imágenes → "Sin datos extraídos".

## Patrón seguro

No pasar buffers grandes por HTTP interno. Dos opciones:

1. **Función directa**: extraer la lógica a una función TS e importarla (sin HTTP layer). Option B en PR #597.
2. **Download en destino**: el endpoint receptor descarga el recurso desde Storage usando los IDs. El payload HTTP queda en ~200 bytes.

Aplica a: cualquier endpoint interno que reciba media (ocr-process, ingesta, procesadores de adjuntos).

Ver [[whatsapp-ocr-trigger-no-es-ingesta-es-caller]] · [[dokploy-requiere-reload-manual-traefik-tras-redeploy]]
