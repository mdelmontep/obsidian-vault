---
title: facturaia verificar visual post seed
date: 2026-04-20
source: claude-code-session
tags: [inbox, facturaia, pendiente]
---

Pendiente de verificar visualmente después de hard refresh (Cmd+Shift+R):

1. Facturas emitidas muestran nombres de clientes (no "?") — datos OK en BD, confirmado via API
2. Facturas recibidas distribuidas entre 7 proveedores (no solo Vodafone) — seed usa round-robin
3. Click en número de factura abre modal preview con PDF embebido (iframe)
4. Columnas de tabla no se cortan (table-layout: fixed aplicado)
5. Botones "Abrir" y "Descargar" en el modal de preview funcionan
6. Fuente Mermaid aparece como opción en Ajustes → Apariencia → Tipografía

Los 60 PDFs están generados y `documento_url` seteado en todas las facturas.
