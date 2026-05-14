---
title: Incidentes resueltos — log cronológico
date: 2026-05-10
source: claude-code-session
tags: [incidents, postmortem, ops]
---

# Incidents log

Una línea por incidente. Formato: `YYYY-MM-DD · proyecto · síntoma → causa → fix (commit/PR)`. Si el aprendizaje universal ya está en CLAUDE.md, dejarlo aquí solo como pointer.

Para incidentes con análisis largo (>1 línea de causa), crear nota separada en `knowledge/incidents/<slug>.md` y enlazarla aquí con `[[wikilink]]`.

## Reglas
- **Cronológico inverso** (lo más reciente arriba).
- **Sin secrets**, sin nombres de cliente sensibles. Proyecto = nombre interno (Simarro, FacturaIA, agency-portal…).
- Si el fix ya está en CLAUDE.md como anti-patrón, marcar con `→ CLAUDE.md` para evitar duplicar.
- Si pasa de 80 entradas, archivar las >6 meses a `incidents-archive-YYYY.md`.

## 2026

<!-- añade nuevas entradas aquí debajo -->

- 2026-05-12 · panel-tecnocloud · 0 tickets de voz creados por Retell durante días → URL del webhook en Retell dashboard apuntaba a un túnel `trycloudflare.com` de dev caduco, no a producción → fix: cambiar URL a `https://portal.tecnocloud.es/api/webhooks/retell` + pegar la API key de Retell en campo "Webhook secret" del panel (Retell firma con la API key, no hay un secret separado en su dashboard) → CLAUDE.md
- 2026-05-12 · panel-tecnocloud · emails de notificación de llamadas Retell llegaban a `incidencias@` sin Subject → nodo `Send a message` referenciaba `$json.emailSubject` pero el `Registrar en Google Sheets` intermedio del workflow no hace pass-through del input (solo emite columnas mapeadas) → fix: `$('Registrar Llamada').first().json.emailSubject` → CLAUDE.md
- 2026-05-11 · FacturaIA · cron `storage-quota-check` fallando semanal en silencio → env `STORAGE_QUOTA_WARN_MB=""` + `Number("")=0` ≤ 0 → throw `invalid warn_mb` → fix helper `parseMb` con fallback null/empty/non-numeric → commit `5255547`. Destapado al primer run de tabla `cron_runs` (063). Ver [[observabilidad-nueva-destapa-bugs-viejos-en-silencio]]

## Pre-2026 (referencias migradas desde CLAUDE.md)

- **Simarro** · `Lead_id=null` en Google Calendar `getAll(query)` borraba todos los eventos del rango → guard IF "filtro no-vacío" antes de delete con query dinámico → CLAUDE.md
- **Simarro** · Webhook Retell disparaba `Edit Fields` de chat → ramas `Buscar Ainhoa/Carlos/...` con query vacío ejecutaban deletes masivos → severar paths multi-trigger → CLAUDE.md
- **Simarro** · 5 personas test con mismo teléfono → `Buscar_reserva` mezclaba leads → variar datos sintéticos por persona → CLAUDE.md
- **FacturaIA** · `motivo_rectificacion=R5` hardcoded en botón "Anular" → todas las anulaciones declaradas como "otras causas" ante AEAT → modal con select obligatorio de motivos R1-R5 → CLAUDE.md
- **agency-portal** · `cancelInvoiceAction` portal marcaba `status='cancelled'` localmente mientras factura seguía viva en FacturaIA → desincronización con Hacienda → cuando hay shadow externo, renderizar botonera del externo y ocultar acciones locales → CLAUDE.md
- **FacturaIA** · `digest_mismatch` en webhook Retell → asumía bug del provider → instalar SDK oficial y usar `Retell.verify()` reveló bug propio en 30s → CLAUDE.md
- **Retell** · `recording_url` y `duration_ms` solo aparecen en `call_analyzed` post-call, no en tool call mid-call → capturar 1 payload real antes de codificar → CLAUDE.md
- **Subagentes** · agente seguridad reportó hallazgos de `facturaia/...` cuando debía auditar `~/agency-portal-fix` → pasar ruta absoluta + "investiga SOLO en esa ruta" en primera línea del prompt → CLAUDE.md
