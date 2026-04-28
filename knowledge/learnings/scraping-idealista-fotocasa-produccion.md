---
title: scraping idealista/fotocasa en producción — apify es lo viable
date: 2026-04-29
source: claude-code-session
tags: [scraping, apify, inmobiliaria, n8n]
---

Idealista usa **DataDome** (no Cloudflare) — scrapers propios se rompen cada 2-4 semanas tras updates de modelos.
API oficial: acceso por aprobación manual, ~100 peticiones/mes en plan básico. Descartada para uso comercial.

**Opción viable**: Apify con actores de `igolaizola` (autor español, activo, proxies residenciales incluidos):
- `igolaizola/idealista-scraper` — 96% success rate, código abierto en GitHub
- `igolaizola/fotocasa-scraper` — mismo autor, activo
- `friendly_keelboat/spain-portugal-real-estate` — actor combinado Idealista + Fotocasa + Milanuncios

**Coste**: plan Apify $29/mes + $0.50/1.000 resultados ≈ $65-100/mes para barridos cada 2h en 1-2 zonas.

**Arquitectura n8n**: Cron cada 2h → Apify run con filtros (zona/precio/m²) → Supabase dedup por ID → alertas WhatsApp/Kommo.

**Riesgo a monitorizar**: si DataDome actualiza y el actor tarda en adaptarse, hay ventana de downtime. Añadir alerta cuando success rate del run baje de 80%.

Descartados: Bright Data (mínimo $499/mes), ZenRows (~$500/mes en volumen), scraper propio (proxies residenciales $150-400/mes + mantenimiento continuo).
