---
title: max_tokens es un tope (no consumo); si es bajo trunca el JSON de OCR largo
date: 2026-06-16
source: claude-code-session
tags: [llm, openai, ocr, prompt]
---
`max_tokens` limita la SALIDA del modelo, no es un coste fijo: solo se paga lo que
genera. Pero si es bajo (p.ej. 1024) y el documento es largo (factura multi-albarán /
multi-página con ~18 líneas), el JSON de `lineas` NO cabe → la respuesta se trunca a
media → faltan líneas → la suma descuadra. No es que el modelo "no sepa leerlas".

Fix: subir el tope (4096) — las facturas cortas no se encarecen (generan lo mismo).
Reforzar el prompt para recorrer todas las páginas/albaranes y excluir subtotales
("Total HT BL …") que si se cuelan como línea duplican el importe.
Caso: FacturaIA OCR ticket Chivite, base 4.828,85 € leía solo el 1er albarán (2.477,70).
