---
title: daily briefing
date: 2026-06-24
tags: [home, briefing]
---

# 🌅 Briefing 24-jun

## ✅ Lo que cerraste ayer

**agency-portal — recordatorios de onboarding activos en prod**

Mergeaste el PR #95: Retell sube de v2 a v3 (la voz del portal es más estable), el switcher de pestañas ya funciona en móvil, y lo más importante — el sistema de recordatorios de inactividad. El portal puede enviar un WhatsApp a clientes que llevan días sin completar su onboarding. La rama n8n ya está activa en prod con la plantilla HSM correcta. Solo queda el cron automático en Dokploy (ver Quick Win).

**Cómo lo usas en la práctica:**
- Un cliente lleva 5 días parado. Pulsas "Enviar recordatorio" en el admin y le llega el WhatsApp sin salir de la app.
- Cuando actives el cron, eso ocurre solo cada mañana a las 10:00 — cero gestión manual.
- En móvil, el tab switcher de onboarding navega limpio entre secciones.

**Además:** Simarro outbound reactivación validado en llamadas reales hoy (24-jun). La voz mueve al lead al pool, persiste su perfil completo (zona, precio, hab, m²) y no repite pisos ya vistos. Pendiente: marcar consentimiento en leads reales y activar el lanzador.

## 🎯 Hoy en orden de prioridad

1. **Notifs fiscal residuales** — Marcar leídas notifs viejas + recalcular borradores 130 2T/3T/4T + revisar drawer (X 28px, fade chips). ~30 min.
2. **Centro Elphis — empujar go-live** — Hardening al 100%. El freno son externos. Escribe hoy a Pablo (WA app móvil 659) y Enrique (DPAs + sesión crisis). Sin esos dos no hay go-live.
3. **agency-portal — smoke onboarding prod** — Verifica que "Progreso" y "Respuestas extraídas" se rellenan tras PR #95. Si ves `extraction_failed`, abre issue.

## ⏳ Pendientes y bloqueos

- **Acción Manu — GitHub Actions billing**: CI muerto desde 17/06, merges con `--admin`. Arreglar en Billing org `AgentesIA-MAdrid`.
- **Acción Manu — OpenAI Tier 2**: bot WA en rate-limit (30k TPM). Subir en platform.openai.com.
- **Esperando a Dani/legal**: DPAs Elphis + revisión PSD2. Sin fecha.

## 💡 Quick win sugerido

**Cron Dokploy `onboarding-reminders`** — el botón manual funciona desde ayer. Clonar schedule de `sync-facturaia`: cron `0 10 * * *`, ruta `/api/internal/onboarding-reminders` (POST, header `x-service-key`). ~15 min.

## ⚠️ Stale (>7 días)

- **Ticket bgchivite `1762f07e`**: fix en prod hace semanas, solo queda responder. 5 min.
- **Corregir ID receptor en `CLAUDE.md`**: `zYcHHa8jWXB6dY5i` → `pqSWkDIHqmSVHotB`. 1 línea, 1 minuto.

---
> ⚠️ **Nota de entrega**: ntfy.sh bloqueado por política de red del entorno remoto (HTTP 000). Briefing guardado en el vault. Para restaurar la entrega por push, añade `ntfy.sh` a los hosts permitidos en egress: https://code.claude.com/docs/en/claude-code-on-the-web
