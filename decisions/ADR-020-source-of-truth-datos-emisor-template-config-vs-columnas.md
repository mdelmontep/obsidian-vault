---
title: ADR-020 — source of truth de datos del emisor: template_config.emisor JSON con columnas legacy deprecadas
date: 2026-05-25
status: accepted
tags: [adr, facturaia, postgres, arquitectura]
---

## Contexto

`organizations` tenía datos del emisor duplicados: columnas (`nombre`, `nif`, `direccion`, `email`, `telefono`, `logo_url`) Y `template_config.emisor` JSON con los mismos + IBAN/web/cp exclusivos. UI dividida: `/settings?tab=empresa` editaba columnas (sin tocar JSON), `/settings?tab=plantillas` editaba JSON. PDF render lee JSON con fallback a columnas → desincronización producía PDFs con nombre viejo.

## Opciones consideradas

- **A** Migrar todo a columnas dedicadas (ADD COLUMN iban/web/cp), eliminar `template_config.emisor` — pierde flexibilidad para campos futuros (`logo_position`, `pie_personalizado`), invasivo en render.
- **B** `template_config.emisor` JSON único como SoT del PDF, columnas legacy deprecadas (no eliminadas), sincronización en código desde único endpoint UI — equilibrio entre flexibilidad y simpleza.
- **C** Trigger BD BEFORE UPDATE col↔JSON sincronizando ambos sentidos — rechazado: CLAUDE.md inviolable "no triggers de sync" (fallo silencioso, race, recursión, audit ciego). Ver [[triggers-bd-sync-son-antipatron]].

## Decisión

**B**, porque el JSON ya era consumido por el render PDF (canal crítico). Migrar todo a columnas (A) implica refactor de render + 3 columnas nuevas. C es estructuralmente peor (magia oculta). B mantiene retrocompat de queries legacy y permite eliminar columnas en mig futura cuando todo el código lea JSON.

## Consecuencias

- Mig 166 backfill one-shot JSON desde columnas + COMMENT `DEPRECATED` en columnas duplicadas.
- `SetEmpresa.handleSave` actualiza ambos en UPDATE único (sincronización explícita, debugable, una sola transacción cliente).
- `TemplateCustomizer` (settings/plantillas) deja de duplicar bloque "Datos del emisor" — solo apariencia visual.
- Futura mig 180+: DROP COLUMN columnas legacy cuando todos los consumers (búsqueda, listados admin) lean JSON.
- Patrón replicable: otras tablas con duplicación col↔JSON resolverlas con la misma estrategia.
