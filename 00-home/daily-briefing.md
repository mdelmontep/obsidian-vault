---
title: daily briefing
date: 2026-07-04
tags: [home, briefing]
---

# 🌅 Briefing 04-jul

## ✅ Lo que cerraste ayer

**Auditoría TuFacturaIA: trazabilidad legal en las operaciones críticas**

7 PRs cerrados hoy (bloques 1-3): cualquier mutación en la API v1, conciliación y RPCs deja rastro explícito — fecha, usuario y acción legible. Antes esas operaciones eran invisibles. Al pasar a prod detectaste y corregiste un bug propio: el campo "acción" mostraba el slug técnico en vez del texto humanizado. Bloque 4 (cobros y remesas) pendiente, baja prioridad.

**Cómo lo usas en la práctica:**
- Un cliente discute quién cambió algo → historial de auditoría: timestamp y usuario exactos.
- Inspección o reclamación → log explícito de cada operación, sin reconstruir nada.
- La UI ya muestra la acción en castellano, no el slug crudo.

Además, ayer cerraste el **Export gestoría v1.5**: la IA revisa el export (contrapartes sin NIF, facturas sin líneas) y lo manda por WhatsApp a tu gestoría con enlace de un solo uso.

## 🎯 Hoy en orden de prioridad

1. **CI Actions — subir límite de gasto (Manu)** — Mismo bloqueo billing de ayer. Settings → Billing de la org GitHub (AgentesIA-MAdrid). 5 min o los merges siguen yendo todos con `--admin`.
2. **Centro Elphis — empujar go-live** — Código terminado. Escríbele hoy a Enrique: arrancar verificación número real + decidir si migras 659→Cloud API o coexistes con BSP.
3. **agency-portal — PR #67 extracción onboarding** — Confirma en prod que "Progreso por sección" y "Respuestas extraídas" se actualizan en cada turno. Si ves `onboarding.extraction_failed`, abre issue.

## ⏳ Pendientes y bloqueos

- **Acción Manu — GitHub Actions billing**: CI caído desde 03-jul (recurrente). Límite en Settings → Billing org GitHub.
- **Acción Manu — Salt Edge Test access**: sin esto, PR #610 conexión bancaria no se puede validar. Aprobar en dashboard Salt Edge.
- **Esperando a Borja**: AGH Ibérica PR-2 (#87) y PR-3 (#88) en review. Sin fecha.
- **Esperando a Gonzalo**: .p12 para smoke PRE Verifactu (~semana que viene).

## 💡 Quick win sugerido

**Activar skin "Cristal"** — QA de contraste hecho el 02-jul sin fallos (luz+oscuro, pantallas densas). Solo falta tu decisión. Si dices sí, un flag activa el look en prod sin tocar código.

## ⚠️ Stale (>7 días)

- **Simarro — E2E reserva (25-jun, 9 días)**: Haz 2 reservas reales ahora (1 voz + 1 WA) y comprueba evento con calle+location+tarea Meeting+email. Si pasan, ciérralo.
- **agentesia-skills PR #3**: Sin reviewer asignado desde hace días. Mándaselo directamente a alguien del equipo hoy.
