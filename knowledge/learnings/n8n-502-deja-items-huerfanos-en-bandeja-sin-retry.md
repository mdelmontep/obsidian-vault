---
title: n8n 502 deja items huerfanos en bandeja sin retry automatico
date: 2026-04-24
source: claude-code-session
tags: [n8n, facturaia, ocr, webhook]
---

Cuando n8n cae (502/503), los webhooks fire-and-forget de OCR fallan silenciosamente. Los items en `bandeja_ingesta` quedan en `procesando` / 0% indefinidamente — no hay retry automatico.

## Sintoma

- Items atascados en "procesando" con progreso 0%
- n8n devuelve 502 pero el frontend no lo muestra (fire-and-forget con timeout 30s)
- El usuario ve facturas que "nunca terminan de cargar"

## Solucion actual

1. Verificar que n8n esta corriendo (`curl https://n8n.tufacturaia.com/healthz`)
2. Si estaba caido, reiniciar y re-trigger manual desde frontend ("Revisar ahora") o desde admin
3. Para items ya huerfanos: actualizar `estado` a `error` o re-enviar al webhook OCR manualmente

**Reaper implementado (2026-06-16)**: cron `ingesta-stale-sweep` (`*/30`) marca `error` las filas en `procesando` con `created_at > 30 min`; `ocr-process` autodetecta `error` en sus early-returns (p.ej. `OPENAI_API_KEY` ausente) en vez de zombificar al 90%. El estado solo avanza por callback externo → un reaper por tiempo es la única red para los fallos donde no corre código nuestro.

## Patron reutilizable

Cualquier pipeline fire-and-forget con webhook externo necesita:
- Health check del destino antes de enviar (o al menos logging del status code)
- Mecanismo de retry o al menos deteccion de items stuck (>X minutos en procesando)
- UI para re-trigger manual como fallback
