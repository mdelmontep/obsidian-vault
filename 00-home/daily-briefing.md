---
title: daily briefing
date: 2026-06-25
tags: [home, briefing]
---

# 🌅 Briefing 25-jun

## ✅ Lo que cerraste ayer

**SEPA: el sistema de devoluciones de cobro ya funciona**

Has cerrado la Fase 1 del módulo SEPA. TuFacturaIA ahora procesa los ficheros `pain.002` que manda BBVA cuando te devuelven una domiciliación: los cruza con la remesa original, bloquea el reintento automático para ese mandato y te muestra el motivo en texto legible ("cuenta cerrada", "cliente lo revocó"). La UI también recibió un polish completo: copy más claro, icono de devolución, contraste AA, calendario unificado. Solo falta que Dani te pase un fichero real de BBVA para que el test automático pase solo.

**Cómo lo usas en la práctica:**
- BBVA te devuelve un cobro → subes el `pain.002` en Remesas SEPA → la factura queda marcada como devuelta con el motivo real, no con el código bancario.
- El sistema impide que generes otra remesa para ese mandato por error — no hay doble intento accidental.
- En el historial ves el motivo legible desde el primer vistazo.

**Además:** PR #477 — el copiloto de WhatsApp ya responde siempre en prosa (antes a veces soltaba JSON crudo; doble defensa: prompt v13 + sanitizador). PR #449 — Declaración Responsable del Centro Fiscal mergeada al repo (página oculta hasta activar flag `VIGENTE`; docs de compliance en `docs/compliance/centro-fiscal-pre-beta/`).

## 🎯 Hoy en orden de prioridad

1. **Notifs fiscal residuales** — Marcar leídas las notifs viejas + recalcular borradores modelo 130 (2T/3T/4T, drift real: abono B2026-0001) + revisar drawer (X cierre 28px, fade chips). Fix #214 ya en prod. ~30 min.
2. **Centro Elphis — desbloquear go-live** — El código está al 100%. El freno son los externos. Escríbele hoy a Pablo (659 877 708) para la coexistencia de WA por app móvil, y a Enrique para los DPAs y la sesión de crisis. Sin esos dos no hay go-live.
3. **agency-portal — smoke onboarding en prod** — Confirma que "Progreso por sección" y "Respuestas extraídas" se rellenan tras cada turno con dato extraíble (PR #67, REO RAFTING en curso). Si ves `activity_event.action='onboarding.extraction_failed'`, abre issue.

## ⏳ Pendientes y bloqueos

- **Acción Manu — GitHub Actions billing**: CI bloqueado desde 17/06, merges con `--admin`. Arreglar en Billing org `AgentesIA-MAdrid`.
- **Acción Manu — OpenAI Tier 2**: bot WA en rate-limit (30k TPM). Subir en platform.openai.com → Organization → Limits.
- **Esperando a Dani**: fichero `pain.002` real de BBVA para test automático SEPA + revisión ADR-002 PSD2. Sin fecha.

## 💡 Quick win sugerido

**Cron Dokploy `onboarding-reminders`** — el botón manual ya funciona desde el PR #95. Clonar el schedule de `sync-facturaia`: cron `0 10 * * *`, ruta `/api/internal/onboarding-reminders` (POST, header `x-service-key`). ~15 min y los recordatorios se envían solos cada mañana sin tocar nada.

## ⚠️ Stale (>7 días)

- **Ticket bgchivite `1762f07e`**: el fix lleva semanas en prod, solo queda responder. 5 min.
- **ID receptor obsoleto en `CLAUDE.md`**: `zYcHHa8jWXB6dY5i` → `pqSWkDIHqmSVHotB` (el viejo da 404). 1 línea, 1 minuto.
