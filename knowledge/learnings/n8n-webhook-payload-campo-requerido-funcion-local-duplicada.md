---
title: función local de webhook omite campos que el endpoint requiere
date: 2026-06-30
source: claude-code-session
tags: [n8n, ingesta, webhook, deuda-tecnica]
---
Problema: `process-attachments.ts` y `upload/route.ts` tenían cada uno su
propio `triggerOcrWebhook` local (30s timeout, sin reintentos completos).
Al añadir `factura_id` al workflow n8n, solo se actualizó la función canónica
(`@/lib/ingesta/trigger-ocr`); las locales siguieron sin el campo.

n8n arrojaba `Error('factura_id ausente')` → todos los adjuntos de email
quedaban en `procesando`; el stale-sweep los pasaba a `error` a los 30 min.

Fix: eliminar funciones locales, importar siempre la canónica.
Patrón: si existe `lib/ingesta/trigger-ocr.ts`, ningún entry point crea
su propio fetch al mismo endpoint.
