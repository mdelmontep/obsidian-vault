---
title: apify daily scrape -> supabase upsert + sweep removed
date: 2026-05-03
source: claude-code-session
tags: [apify, n8n, supabase, scraping, sync]
---

Patrón de sincronización diaria de fuentes externas (catálogos web, listings) a Supabase manteniendo estado vivo/muerto sin perder histórico.

## Pipeline

```
Apify schedule task (cron diario)
  → webhook ON RUN_SUCCEEDED (no esperar polling)
  → n8n: GET dataset items
  → OpenAI text-embedding-3-small (campos descriptivos concatenados)
  → Supabase REST upsert por external_ref (Prefer: resolution=merge-duplicates)
  → Sweep: UPDATE items SET status='removed' WHERE external_ref NOT IN (batch_actual) AND last_seen_at < NOW() - INTERVAL '1 day'
```

## Claves del patrón

- `external_ref` (UNIQUE) como id estable de la fuente — no usar el id propio para upserts
- `last_seen_at` actualizado en cada batch — el sweep usa esto para no marcar removed por error si el actor falla un día
- Trigger `track_price_change` en UPDATE para mantener histórico de cambios sin lógica en n8n
- Webhook `ON RUN_SUCCEEDED` mejor que polling — actor a veces tarda variable

Validado en Simarro: Apify Idealista → properties Supabase, 10 viviendas con embeddings, búsqueda semántica funcionando.
