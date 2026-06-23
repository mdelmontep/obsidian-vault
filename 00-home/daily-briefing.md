---
title: daily briefing
date: 2026-06-23
tags: [home, briefing]
---

# 🌅 Briefing 23-jun

## ✅ Lo que cerraste ayer

**Pizarra del agency-portal — bloques C y D listos**

Terminaste dos bloques nuevos de la Pizarra del portal: el C es el centro de mando del negocio (alertas activas, cobros que vencen esta semana, MRR, salud de cada cliente y estado de onboardings en curso), y el D es tu vista de trabajo personal con filtros que se guardan en la URL y agrupación por tipo de tarea. Todo pasa tests, lint y build verde. Está listo en rama `feature/pizarra-dashboard` esperando validación visual tuya antes del merge.

**Cómo lo usas en la práctica**:
- Abres la Pizarra y de un vistazo ves qué clientes tienen alertas activas y qué cobros vencen esta semana, sin entrar uno a uno.
- Los filtros quedan en la URL: mandas el enlace a Borja y ve exactamente tu vista, sin explicaciones extra.
- El bloque D filtra solo las tareas asignadas a ti — no mezclas clientes activos con los que esperan algo externo.

**Además:**
- PR #450 TuFacturaIA: el selector de estado en conciliación usa ahora el mismo `Segmented` canónico que el resto de la app. Los chips restyled y scroll móvil funcionando. Mergeado con `--admin`.
- Cron stock-alarmas: en vez de un email por producto en alarma, llega un solo correo con la tabla completa por org.

## 🎯 Hoy en orden de prioridad

1. **Notifs fiscal residuales** — Marcar leídas notifs viejas + recalcular borradores 130 del 2T/3T/4T + revisar drawer (X 28px, fade chips). ~30 min.
2. **Centro Elphis — go-live** — Hardening al 100 %. Bloqueo son externos: Pablo (WA 659), 4 plantillas HSM, DPAs Enrique, número Alba. Empuja hoy a al menos uno.
3. **agency-portal — smoke extracción onboarding en prod** — Verificar que "Progreso" y "Respuestas extraídas" se rellenan tras cada turno. Si ves `extraction_failed`, abrir issue.

## ⏳ Pendientes y bloqueos

- **Acción Manu — GitHub Actions billing**: CI muerto desde 17/06, merges con `--admin`. Arreglar en Billing org `AgentesIA-MAdrid`.
- **Acción Manu — OpenAI Tier 2**: bot WA salta rate-limit (30k TPM). Subir en platform.openai.com.
- **Esperando a Dani/legal**: DPAs Elphis + PSD2. Sin fecha.

## 💡 Quick win sugerido

**Corregir ID receptor en `CLAUDE.md`** — Una línea: `zYcHHa8jWXB6dY5i` → `pqSWkDIHqmSVHotB`. Cualquier agente nuevo acaba en 404. 1 minuto.

## ⚠️ Stale (>7 días)

- **agency-portal smoke PR #67** (mergeado 18-may, >35 días en NOW): verificar o mover a LATER.
- **Ticket bgchivite `1762f07e`**: fix en prod hace semanas, solo queda responder. 5 min.

---
> ⚠️ **Nota de entrega**: ntfy.sh bloqueado por política de red del entorno remoto (`host_not_allowed`). Briefing guardado en el vault vía commit. Para restaurar la entrega por push, añade `ntfy.sh` a los hosts permitidos en egress: https://code.claude.com/docs/en/claude-code-on-the-web
